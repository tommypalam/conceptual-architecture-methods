"""Offline monotonicity probabilities and fixed-index rationale trace inventory."""
from hashlib import sha256
import json
import logging
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.optimize import brentq
from scipy.special import expit
from scipy.stats import binom
import utils
from engine.validity_sweep import verify_record, digest
from run_validity_claude import save_new

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'experiments/phase1_5_encoding_validity'
RUN=BASE/'repetition_retention_20260911'
DEST=BASE/'repetition_diagnosis_20260911'
SOURCES={
    'original':BASE/'option_c_20260909_restart/analysis/summary_8d2d0ab58fff59f9.json',
    'curve':BASE/'mor_curve_20260911/analysis/curve_38db0185e4a8dc94.json',
    'retention':RUN/'analysis/retention_ec81552b7a2c8ed7.json',
}


def ordered_probability(probabilities,n):
    """P(K1<=...<=K5) for independent Binomial(n,p_i), including ties."""
    p=np.asarray(probabilities,dtype=float)
    if p.shape!=(5,) or not np.all(np.isfinite(p)) or np.any((p<0)|(p>1)):
        raise ValueError('Require five finite probabilities in [0,1]')
    if not isinstance(n,int) or isinstance(n,bool) or n<1: raise ValueError('Positive integer N required')
    pmfs=binom.pmf(np.arange(n+1)[None,:],n,p[:,None])
    mass=pmfs[0]
    for following in pmfs[1:]: mass=following*np.cumsum(mass)
    return {'nondecreasing_probability':float(np.clip(mass.sum(),0,1)),
            'all_equal_counts_probability':float(np.prod(pmfs,axis=0).sum())}


def fitted_probabilities(sweep):
    fit=sweep['fit']; cells=sweep['cells']
    if fit['status']!='ok' or fit['slope']<=0: raise ValueError('Require an estimable positive source fit')
    values=np.array([c['value'] for c in cells]); n=np.array([c['n_valid'] for c in cells])
    k=np.array([c['opt0_count'] for c in cells])
    if values.tolist()!=[.1,.3,.5,.7,.9] or np.any(n<=0): raise ValueError('Incomplete grid')
    slope=fit['slope']
    intercept=brentq(lambda a:float((n*expit(a+slope*values)-k).sum()),-60,60)
    probabilities=expit(intercept+slope*values)
    if abs(float((n*probabilities-k).sum()))>1e-7: raise ValueError('Intercept score not solved')
    return {'intercept':float(intercept),'slope':slope,'probabilities':probabilities.tolist(),
            'observed_counts':k.tolist(),'observed_n':n.tolist(),
            'expected_counts_at_source_n':(n*probabilities).tolist()}


def main():
    raw={p:p.read_bytes() for p in SOURCES.values()}
    loaded={k:json.loads(raw[p]) for k,p in SOURCES.items()}
    select=lambda name,arm:next(s for s in loaded[name]['sweeps'] if
        (s['arm'],s['parameter'],s['problem'])==(arm,'MoR','S3'))
    specs=[('original_canonical','original','full_harness'),('previous_repetition','curve','repetition'),
           ('previous_grounding','curve','grounding'),('fresh_repetition','retention','full_harness')]
    scenarios={name:fitted_probabilities(select(src,arm)) for name,src,arm in specs}
    scenarios['flat_half_counterexample']={'probabilities':[.5]*5,'assumption':'Flat illustrative curve; not an encoding effect.'}
    scenarios['flat_verbal_floor_counterexample']={'probabilities':[1/150]*5,
        'assumption':'Illustrative flat curve at pooled observed verbal rate, not an estimated causal model or a fitted positive effect.'}
    rows=[]
    for name,s in scenarios.items():
        for n in (30,50,100,200,500,1000):
            rows.append({'scenario':name,'n_per_value':n,**ordered_probability(s['probabilities'],n)})
    logging.basicConfig(level=logging.INFO); logger=logging.getLogger('precision')
    utils.log_dataframe_summary(pd.DataFrame(rows),'All 6 assumed curves x 6 sample sizes, no exclusions',logger)
    manifest_path=RUN/'manifest.json';raw[manifest_path]=manifest_path.read_bytes()
    manifest=json.loads(raw[manifest_path]); assert digest(manifest['design'])==manifest['design_hash']
    inventory=[]; exceptions=[]
    # Fixed first-two scheduled indices in every cell: not selected for the observed action.
    for cell in manifest['design']['cells']:
        for index in (1,2):
            key=f"{cell['arm']}/{cell['wording']}/call_{index:04d}"
            path=RUN/'records'/(key+'.json');raw[path]=path.read_bytes();r=json.loads(raw[path]);verify_record(r)
            assert r['design_hash']==manifest['design_hash'] and r['request_messages']==cell['messages']
            assert r['agent_parameters']==cell['profile'] and r['parse_status']=='ok'
            inventory.append({'record_key':key,'value':cell['value'],'arm':cell['arm'],'decision':r['parsed_decision'],
                              'record_hash':r['record_hash'],'reasoning_sha256':sha256(r['parsed_reasoning'].encode()).hexdigest()})
    for path in sorted((RUN/'records/verbal_only').rglob('*.json')):
        content=path.read_bytes();r=json.loads(content);verify_record(r)
        if r['parsed_decision']=='ADOPT':
            raw[path]=content
            exceptions.append({'record_key':r['record_key'],'record_hash':r['record_hash'],
                               'reasoning_sha256':sha256(r['parsed_reasoning'].encode()).hexdigest()})
    assert len(inventory)==30 and len(exceptions)==1
    utils.log_dataframe_summary(pd.DataFrame(inventory),'450 saved responses -> fixed 30-item qualitative review; no new population scoring',logger)
    result={'method':'Exact independent-binomial dynamic programming for nondecreasing observed counts, including ties. No Monte Carlo or simulated agents; no random seed.',
            'scope':'Post-hoc conditional sensitivity analysis; assumes each plug-in positive logistic curve is true. Fit uncertainty/model misspecification omitted. Does not estimate the probability that this explanation is true.',
            'not_full_gate_power':'Nondecreasing probability is an upper bound on complete positive-direction sweep success under valid collection; significance, h and estimator conditions are not computed.',
            'scenarios':scenarios,'probabilities':rows,
            'floor_counterexample_p_at_most_one_adopt_in_150':float(binom.cdf(1,150,1/150)),
            'review_selection':'First two scheduled calls in each of all 15 cells: 30. Separately inspect the sole verbal ADOPT as an explicitly outcome-selected exception. Unblinded diagnostic notes, not new gold coding.',
            'review_inventory':inventory,'outcome_selected_exceptions':exceptions,
            'source_sha256':{p.relative_to(ROOT).as_posix():sha256(b).hexdigest() for p,b in raw.items()},
            'analysis_source_sha256':sha256(Path(__file__).read_bytes()).hexdigest()}
    save_new(DEST/'precision_and_traces.json',result)
    lines=['# Sampling sensitivity of the observed-monotonicity check','',
           'Exact P(nondecreasing counts), conditional on specified independent-binomial probabilities.',
           'This is not full-gate power, a probability that the fitted model is true, or a revised result.','',
           '| Assumed curve | N30 | N50 | N100 | N200 | N500 | N1000 |','|---|---|---|---|---|---|---|']
    for name in scenarios:
        vals=[f"{r['nondecreasing_probability']:.1%}" for r in rows if r['scenario']==name]
        lines.append('| '+name+' | '+' | '.join(vals)+' |')
    lines+=['','Positive curves use plug-in logistic fits to saved data; this smooth monotonic assumption is imposed, not established.',
            'The two flat curves are counterexamples: ordering can occur without any parameter effect, especially through ties near a boundary.',
            'Increasing N here is a hypothetical sensitivity calculation, not a sample-size recommendation or authorised allocation.',
            'See precision_and_traces.json for fitted probabilities, expected counts, tie probabilities and exact source hashes.','']
    target=DEST/'PRECISION_TABLE.md';out='\n'.join(lines).encode()
    if target.exists() and target.read_bytes()!=out:raise ValueError('Preserve previous output')
    if not target.exists():target.write_bytes(out)
    assert all(p.read_bytes()==b for p,b in raw.items())
    print('\n'.join(lines))


if __name__=='__main__':main()
