"""Render the frozen pilot analysis for review; no new hypothesis tests or API calls."""
import argparse
import hashlib
import json
import logging
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import utils
from engine.validity_sweep import digest
from run_validity_claude import save_new


def render(root,analysis_path):
    m=json.loads((root/'manifest.json').read_text(encoding='utf-8'));d=m['design']
    r=json.loads(analysis_path.read_text(encoding='utf-8'))
    if digest(d)!=m['design_hash'] or r['design_hash']!=m['design_hash'] or digest(r)[:16] not in analysis_path.name:
        raise ValueError('Manifest/analysis integrity failure')
    if any(c['n_recorded']!=c['n_expected'] for c in r['cells']):
        raise ValueError('Final report requires complete collection')
    frame=pd.DataFrame(r['cells'])
    logging.basicConfig(level=logging.INFO)
    utils.log_dataframe_summary(frame,'Final pilot report cells, all retained',logging.getLogger('axis-report'))
    eq=frame.loc[frame.stage=='equivalence'].copy()
    utils.log_dataframe_summary(eq,'Eight equivalence cells; sweep cells rendered separately',logging.getLogger('axis-report'))
    names=['canonical','paraphrase_1','paraphrase_2','paraphrase_3'];colors={'baseline':'#64748b','revision':'#147d92'}
    fig,ax=plt.subplots(figsize=(8,4.8))
    for offset,arm in [(-.15,'baseline'),(.15,'revision')]:
        cells=[next(c for c in r['cells'] if c['stage']=='equivalence' and c['arm']==arm and c['wording']==name) for name in names]
        y=np.array([c['rate'] for c in cells]);lo=np.array([c['ci95'][0] for c in cells]);hi=np.array([c['ci95'][1] for c in cells])
        ax.errorbar(np.arange(4)+offset,y,yerr=[y-lo,hi-y],fmt='o',capsize=4,color=colors[arm],label=arm.capitalize())
    ax.set(xticks=np.arange(4),xticklabels=['Canonical','P1','P2','P3'],ylim=(-.03,1.03),ylabel='ADOPT proportion',title='PD=.8 / S3: fresh baseline and numeric-axis instruction')
    ax.legend();ax.grid(axis='y',alpha=.2);fig.text(.5,.01,'Pointwise Wilson 95% intervals; equivalence decisions use the separately reported six-pair TOST.',ha='center',fontsize=8)
    fig.tight_layout(rect=(0,.04,1,1));fig.savefig(root/'analysis/wording_rates.png',dpi=180);plt.close(fig)
    fig,axes=plt.subplots(1,3,figsize=(11,3.8),sharey=True)
    for ax,problem in zip(axes,['S1','S2','S3']):
        for arm in ('baseline','revision'):
            curve=next(c for c in r['sweeps']['sweeps'] if c['arm']==arm and c['problem']==problem)
            cells=curve['cells'];y=np.array([c['rate'] for c in cells])
            ax.errorbar([c['value'] for c in cells],y,
                yerr=[y-np.array([c['ci95'][0] for c in cells]),np.array([c['ci95'][1] for c in cells])-y],
                fmt='o-',capsize=3,color=colors[arm],label=arm.capitalize())
        ax.set(title=problem,xlabel='PD value',ylim=(-.03,1.03));ax.grid(alpha=.2)
    axes[0].set_ylabel('First-option proportion');axes[-1].legend()
    fig.suptitle('Canonical PD sweeps: pointwise Wilson 95% intervals')
    fig.tight_layout();fig.savefig(root/'analysis/pd_sweeps.png',dpi=180);plt.close(fig)
    def number(value,digits=3): return 'NA' if value is None else f'{value:.{digits}f}'
    lines=['# Numeric-axis instruction: local pilot result','',
        f'Collection complete: {sum(c["n_recorded"] for c in r["cells"]):,}/{d["planned_calls"]:,} records; {sum(c["n_valid"] for c in r["cells"]):,} valid.',
        f'Frozen local-screen status: **{r["status"]}**. The original Phase 1.5 gate remains unchanged.','',
        f'Configuration neutral; model `{d["model"]}`; seed {d["seed"]}; temperature {d["temperature"]}; output cap {d["max_tokens"]}.',
        'All responses are fresh. The familiar PD/S3 wording problem was selected during development; this is not a new-problem holdout.','',
        '## Wording equivalence','',
        '| Arm | Wording | First-option count / valid N | Rate | Pointwise 95% interval | Invalid |',
        '|---|---|---:|---:|---:|---:|']
    for c in r['cells']:
        if c['stage']=='equivalence':
            lines.append(f'| {c["arm"]} | {c["wording"]} | {c["opt0_count"]}/{c["n_valid"]} | {c["rate"]:.3f} | {c["ci95"][0]:.3f} to {c["ci95"][1]:.3f} | {c["n_invalid"]} |')
    if (root/'collection_manifest.json').exists():
        collection=json.loads((root/'collection_manifest.json').read_text(encoding='utf-8'))
        lines+=['', 'Collection recovery: the original segment stopped after connection errors. '
            f'The separate continuation filled only never-dispatched slots; {collection["n_failures_preserved"]} '
            'original API failures remain in the complete allocation. They are unknown decisions, not parsing failures. '
            'Raw records were assembled byte-for-byte with disjoint original keys. '
            'The frozen local-screen status retains its terminal-failure flag, independently of the substantive criteria below. '
            'See [collection provenance](../collection_manifest.json).']
    lines+=['','![Wording rates](wording_rates.png)','',
        '| Arm | All six pairs equivalent | All invalid completions equivalent | Saturation flag |',
        '|---|---|---|---|']
    for arm,e in r['equivalence'].items():
        lines.append(f'| {arm} | {e["all_pairs_equivalent"]} | {e["all_unknown_completions_equivalent"]} | {e["saturated_all_formulations"]} |')
    lines+=['','Margin .10, alpha .05, original constrained-score TOST. The displayed intervals are descriptive pointwise rate intervals, not equivalence intervals.',
        'Failure to establish equivalence does not by itself prove a meaningful difference. A baseline-fail/revision-pass pattern is not a formal between-arm improvement test.','',
        '### All prespecified pair tests','',
        '| Arm | Pair | Rate difference | TOST p | Equivalent | Unknown sensitivity |','|---|---|---:|---:|---|---|']
    for arm,e in r['equivalence'].items():
        for p in e['pairs']:
            lines.append(f'| {arm} | {p["a"]} / {p["b"]} | {p["difference"]:.4f} | {p["p_value"]:.6g} | {p["equivalent"]} | {p["all_unknown_completions_equivalent"]} |')
    lines+=['','## PD sweep','',
        '| Arm | Problem | Fit | Slope | Slope p | Extreme Cohen h | Monotonic | Prespecified sign | Original criterion |',
        '|---|---|---|---:|---:|---:|---|---|---|']
    for c in r['sweeps']['sweeps']:
        f=c['fit'];lines.append(f'| {c["arm"]} | {c["problem"]} | {f["status"]} | {number(f.get("slope"))} | {number(f.get("p_value"),6)} | {number(c["cohens_h_extremes"])} | {c["monotonic"]} | {c["predicted_direction"]} | {c["criterion_met"]} |')
    lines+=['','![PD sweeps](pd_sweeps.png)','',
        'Only PD/S1 has a prespecified directional hypothesis. S2/S3 are descriptive; missing hypotheses are not failures. The original N=50 sweep retains its ceiling and precision limitations. Slope intervals, cell counts and endpoint-change contrasts are in the numerical analysis.','',
        '## Limits and next decision','',
        'The shared instruction was one fixed candidate, with original endpoints and controls preserved. It affects all ten trait positions although only PD was manipulated. Stable wording alone cannot establish graded encoding; the local screen additionally requires the original PD/S1 criterion and no all-formulation saturation.',
        'No inference of ethical competence, successful global encoding or phase closure follows from this pilot. The full battery still requires reasoning, representation and all-parameter checks. The added instruction itself was not paraphrased. Retain the theory and researcher review requirements for subsequent work.','',
        f'Returned-usage token estimate: **${r["recorded_token_estimate_usd"]:.6f}**, before taxes and unreported retry charges. Approximate additional-budget remainder: **${48.6856535-r["recorded_token_estimate_usd"]:.6f}**.',
        'Rates used were the September 10 verified $0.75/million input and $4.50/million output, without cache discounts. Provider billing is authoritative.',
        f'Numerical evidence: [{analysis_path.name}]({analysis_path.name}); [protocol](../PROTOCOL.md); [approval](../review_approved.json); [raw-record inventory](../record_checksums.json); [local ZIP metadata](../local_backup.json). Same-computer storage is not an off-device backup.','']
    report=root/'analysis/AXIS_PILOT_REPORT.md';content='\n'.join(lines)
    if report.exists() and report.read_text(encoding='utf-8')!=content: raise ValueError('Existing final report differs')
    report.write_text(content,encoding='utf-8')
    save_new(root/'analysis/render_provenance.json',{'analysis_hash':digest(r),
        'renderer_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'artifacts':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [report,root/'analysis/wording_rates.png',root/'analysis/pd_sweeps.png']},
        'note':'Post-collection formatting of frozen analysis; no new tests or outcome filtering.'})
    print(report)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--run-root',type=Path,required=True);p.add_argument('--analysis',type=Path,required=True)
    a=p.parse_args();render(a.run_root.resolve(),a.analysis.resolve())
