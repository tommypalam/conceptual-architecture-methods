"""Exploratory offline diagnosis; does not alter frozen inference or make API calls."""
import argparse
from collections import Counter
from functools import lru_cache
import hashlib
import itertools
import json
import logging
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import binomtest

import utils
from engine.validity_analysis import wilson
from engine.validity_equivalence import tost
from engine.validity_sweep import digest
from run_validity_claude import save_new

VARIANTS=('hybrid','paraphrase_1','paraphrase_2','paraphrase_3')


def exact_bounds(k, n, unknown=0, family_size=120, alpha=.05):
    """Bonferroni exact binomial bounds, expanded over every unknown decision."""
    if not (n>0 and 0<=k<=n and 0<=unknown<=n-k and family_size>0):
        raise ValueError('Invalid counts or family size')
    confidence=1-alpha/family_size
    low=binomtest(k,n).proportion_ci(confidence_level=confidence,method='exact').low
    high=binomtest(k+unknown,n).proportion_ci(confidence_level=confidence,method='exact').high
    return [float(low),float(high)]


def difference_bounds(a,b):
    return [a[0]-b[1],a[1]-b[0]]


def prepare_cells(paraphrase, rotations):
    cells=[dict(c) for c in paraphrase['cells']]+[dict(c) for c in rotations['cells'] if c['variant']=='hybrid']
    keys=[(c['parameter'],c['problem'],c['variant']) for c in cells]
    expected=set(itertools.product(utils.PARAM_NAMES,('S1','S2','S3'),VARIANTS))
    if len(cells)!=120 or len(set(keys))!=120 or set(keys)!=expected:
        raise ValueError('Require exactly 120 formulation cells')
    for c in cells:
        if c['value']!=.8 or c['n_recorded']!=50 or c['n_expected']!=50 or c['n_valid']+c['n_invalid']!=50:
            raise ValueError('Incomplete or incompatible cell')
        c['simultaneous_bounds_unknowns_expanded']=exact_bounds(c['opt0_count'],50,c['n_invalid'])
    return cells


def diagnose(cells,equivalence):
    summaries=[]; pairs=[]
    lookup={(c['parameter'],c['problem'],c['variant']):c for c in cells}
    frozen={(r['parameter'],r['problem']):r for r in equivalence['cells']}
    for param,problem in itertools.product(utils.PARAM_NAMES,('S1','S2','S3')):
        cs=[lookup[param,problem,v] for v in VARIANTS]; original=frozen[param,problem]
        local=[]
        for a,b in itertools.combinations(cs,2):
            interval=difference_bounds(a['simultaneous_bounds_unknowns_expanded'],b['simultaneous_bounds_unknowns_expanded'])
            delta=a['rate']-b['rate']
            row={'parameter':param,'problem':problem,'a':a['variant'],'b':b['variant'],
                 'observed_difference':delta,'simultaneous_difference_bounds':interval,
                 'beyond_10pp_supported':bool(interval[0]>.1 or interval[1]<-.1),
                 'original_cell_parse_eligible':original['complete']}
            pairs.append(row); local.append(row)
        rates=[c['rate'] for c in cs]; span=max(rates)-min(rates)
        strong=any(p['beyond_10pp_supported'] for p in local)
        saturated=all(p>=.95 for p in rates) or all(p<=.05 for p in rates)
        if original['all_pairs_equivalent']:
            group='equivalent_saturated' if saturated else 'equivalent_not_saturated'
        elif strong:
            group='large_difference_supported'
        elif span>.10+1e-12:
            group='observed_large_difference_uncertain'
        else:
            group='within_margin_observed_but_not_established'
        summaries.append({'parameter':param,'problem':problem,'observed_range':span,
            'same_boundary_saturation_95pct':saturated,'original_equivalent':original['all_pairs_equivalent'],
            'original_parse_eligible':original['complete'],'large_difference_supported':strong,
            'diagnostic_category':group,'strong_pairs':sum(p['beyond_10pp_supported'] for p in local)})
    return summaries,pairs


@lru_cache(maxsize=None)
def equivalent_counts(n,k1,k2):
    return tost(k1,n,k2,n)['equivalent']


def simulate_precision(seed,repetitions,sizes):
    """All four formulations truly equal; no observed outcomes fitted as truth."""
    output=[]
    for n in sizes:
        rng=np.random.default_rng(np.random.SeedSequence([seed,n]))
        for p in (.02,.10,.50,.90,.98):
            counts=rng.binomial(n,p,size=(repetitions,4))
            success=np.ones(repetitions,dtype=bool); first=None
            for a,b in itertools.combinations(range(4),2):
                ordered=np.sort(counts[:,[a,b]],axis=1)
                unique,inverse=np.unique(ordered,axis=0,return_inverse=True)
                decisions=np.array([equivalent_counts(n,int(k1),int(k2)) for k1,k2 in unique])
                passed=decisions[inverse]; success &= passed
                if first is None: first=passed
            k=int(success.sum())
            output.append({'n_per_formulation':n,'true_common_rate':p,'repetitions':repetitions,
                'all_six_pairs_success_rate':k/repetitions,'monte_carlo_ci95':wilson(k,repetitions),
                'one_pair_success_rate':float(first.mean())})
            print(f'Precision simulation N={n}, p={p}: all-pair success={k/repetitions:.3f}',flush=True)
    return output


def write_markdown(root,report):
    rows=report['profile_diagnostics']; counts=Counter(r['diagnostic_category'] for r in rows)
    lines=['# Offline wording-sensitivity diagnosis', '',
        '**Exploratory diagnosis only. Original gate, theory, prompts and saved observations are unchanged.**',
        'Neutral context; original study seed 20260604; diagnostic simulation seed '+str(report['simulation_seed'])+'.', '',
        '## Main results', '']
    for label,count in sorted(counts.items()): lines.append(f'- {label}: {count}/30 profiles.')
    lines.extend(['', 'The original result remains 8/30 equivalent. Categories below are explanatory,',
        'not replacement gates. Parse eligibility is retained separately; one profile is below the original floor.', '',
        '| Profile | Observed range (pp) | All four near same boundary? | Original equivalent? | Parse eligible? | Exploratory category |',
        '|---|---|---|---|---|---|'])
    for r in rows:
        lines.append(f'| {r["parameter"]}/{r["problem"]} | {100*r["observed_range"]:.1f} | {r["same_boundary_saturation_95pct"]} | {r["original_equivalent"]} | {r["original_parse_eligible"]} | {r["diagnostic_category"]} |')
    lines.extend(['','## Uncertainty and missing decisions','',
        'Construct exact Clopper–Pearson intervals for all 120 unique binomial rates, each at',
        'confidence 1−.05/120. Bonferroni gives at least 95% simultaneous coverage under the',
        'binomial sampling assumptions. Subtract interval endpoints to bound all 180 pair',
        'differences simultaneously; no extra correction for overlapping pairs is needed.',
        'For invalid parses, expand each rate interval over every possible allocation of those',
        'unknown decisions, using the full 50-call denominator. This assumes each unparsed',
        'response could correspond to either binary choice; it does not assign or repair it.',
        'The bounds are deliberately conservative. Not exceeding the margin with these bounds',
        'does not show equivalence or absence of a difference. Both saturation (.95/.05) and',
        'the diagnostic categories are post-collection descriptive choices.', '',
        'Method references: [SciPy exact binomial intervals](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.binomtest.html),',
        '[NIST Bonferroni simultaneous coverage](https://www.itl.nist.gov/div898/handbook/prc/section4/prc473.htm).', '',
        '## Precision simulation under true equality','',
        'All four true probabilities are identical within each simulation scenario. Trials',
        'are independent binomial draws, with no missing responses. Every replicate uses the',
        'unchanged six-pair TOST rule. These are simulated sampling properties, not extra API',
        'observations, estimated real-world power, or authority to enlarge the completed study.',
        'Intervals quantify Monte Carlo error only. Saturated probabilities and .50 are',
        'hypothetical sensitivity scenarios, not fitted values chosen to justify a gate pass.', '',
        '| N per formulation | True common rate | One-pair success | All-six success | MC 95% interval |',
        '|---|---|---|---|---|'])
    for r in report['precision_simulation']:
        lo,hi=r['monte_carlo_ci95']
        lines.append(f'| {r["n_per_formulation"]} | {r["true_common_rate"]:.2f} | {r["one_pair_success_rate"]:.1%} | {r["all_six_pairs_success_rate"]:.1%} | {lo:.1%}–{hi:.1%} |')
    lines.extend(['','## Attribution limits','',
        'Each formulation rewrites all ten endpoint pairs simultaneously. A sensitive PD=.8',
        'profile therefore does not identify PD wording as the cause. Formulation-wide',
        'shifts, altered salience, response-format compliance, and interactions with the',
        'fixed dilemma remain competing explanations. S1 agreement near a fixed choice',
        'is not evidence that the parameters control that choice. The existing reasoning',
        'audit also cannot resolve this because nine fixed means dominate aggregate accuracy.', '',
        'No new data collection or theory revision is authorised by this analysis.', ''])
    (root/'DIAGNOSIS.md').write_text('\n'.join(lines),encoding='utf-8')


def plot(root,cells):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    lookup={(c['parameter'],c['problem'],c['variant']):c for c in cells}
    fig,axes=plt.subplots(1,3,figsize=(11,5.7),sharey=True,layout='constrained')
    for ax,problem in zip(axes,('S1','S2','S3')):
        matrix=np.array([[lookup[p,problem,v]['rate'] for v in VARIANTS] for p in utils.PARAM_NAMES])
        im=ax.imshow(matrix,vmin=0,vmax=1,cmap='viridis',aspect='auto')
        for i,p in enumerate(utils.PARAM_NAMES):
            for j,v in enumerate(VARIANTS):
                c=lookup[p,problem,v]; label=f'{100*c["rate"]:.0f}'+('*' if c['n_invalid'] else '')
                ax.text(j,i,label,ha='center',va='center',fontsize=8,color='black' if c['rate']>.55 else 'white')
        ax.set_title(problem); ax.set_xticks(range(4),['Canonical','P1','P2','P3'],rotation=30,ha='right')
        ax.set_yticks(range(10),utils.PARAM_NAMES)
    fig.colorbar(im,ax=axes,label='First-option rate',shrink=.8)
    fig.suptitle('Same profile, different approved wording\nRotated parameter = .8; other parameters at means; N=50 per formulation')
    fig.supxlabel('Percent among valid responses. * One or two invalid parses; retained in the diagnostic uncertainty bounds.',fontsize=9)
    fig.savefig(root/'wording_rates.png',dpi=180); plt.close(fig)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--paraphrase-report',type=Path,required=True)
    p.add_argument('--rotation-report',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True)
    p.add_argument('--repetitions',type=int,default=10000)
    p.add_argument('--simulation-seed',type=int,default=20260909)
    p.add_argument('--sizes',type=int,nargs='+',default=[50,100,200,400])
    a=p.parse_args()
    if a.repetitions<100 or any(n<2 for n in a.sizes): p.error('Invalid simulation size')
    inputs={name:json.loads(path.read_text(encoding='utf-8')) for name,path in
        [('paraphrase',a.paraphrase_report),('rotation',a.rotation_report)]}
    settings={'source_hashes':{k:digest(v) for k,v in inputs.items()},'simulation_seed':a.simulation_seed,
        'repetitions':a.repetitions,'sizes':a.sizes,'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'status':'EXPLORATORY_OFFLINE_ONLY','family_alpha':.05,'rate_family_size':120,'saturation_bounds':[.05,.95]}
    a.out.mkdir(parents=True,exist_ok=True); save_new(a.out/'manifest.json',settings)
    logging.basicConfig(level=logging.INFO); logger=logging.getLogger('offline_diagnosis')
    cells=prepare_cells(inputs['paraphrase'],inputs['rotation'])
    utils.log_dataframe_summary(pd.DataFrame(cells),'120 formulation cells; none removed',logger)
    rows,pairs=diagnose(cells,inputs['paraphrase']['paraphrase_equivalence'])
    utils.log_dataframe_summary(pd.DataFrame(rows),'30 profile diagnoses; none removed',logger)
    utils.log_dataframe_summary(pd.DataFrame(pairs),'180 descriptive pair bounds; includes parse-disqualified profile',logger)
    print('Category counts:',dict(Counter(r['diagnostic_category'] for r in rows)),flush=True)
    simulations=simulate_precision(a.simulation_seed,a.repetitions,a.sizes)
    utils.log_dataframe_summary(pd.DataFrame(simulations),'Hypothetical precision scenarios',logger)
    report={**settings,'configuration':'neutral','study_seed':20260604,'formulation_cells':cells,
        'profile_diagnostics':rows,'pair_diagnostics':pairs,'precision_simulation':simulations}
    save_new(a.out/'diagnosis.json',report)
    pd.DataFrame(rows).to_csv(a.out/'profile_diagnostics.csv',index=False)
    pd.DataFrame(pairs).to_csv(a.out/'pair_diagnostics.csv',index=False)
    write_markdown(a.out,report); plot(a.out,cells)
    print(a.out/'DIAGNOSIS.md',flush=True)


if __name__=='__main__': main()
