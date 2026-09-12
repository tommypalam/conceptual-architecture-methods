"""Independent two-dilemma PD confirmation after the complete all-ten sweep."""
import argparse
import asyncio
from copy import deepcopy
from hashlib import sha256
import json
import logging
import os
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import beta, binomtest
import run_structural_encoding_validation as run
from run_validity_claude import save_new
from engine.validity_sweep import digest, freeze

ROOT=run.PACKAGE/'pd_confirmation'
PROTOCOL=ROOT/'PROTOCOL.md'


def build():
    source=json.loads((run.PACKAGE/'sweep/manifest.json').read_bytes())
    run.base.check(source)
    backgrounds=[dict(zip(run.utils.PARAM_NAMES,map(float,row))) for row in run.utils.sample_agents(25,seed=20261012)]
    prior=set()
    for stage in ('diagnostics','sweep'):
        prior.update(map(digest,json.loads((run.PACKAGE/stage/'manifest.json').read_bytes())['design']['backgrounds']))
    if prior & set(map(digest,backgrounds)):raise ValueError('Reused backgrounds')
    run.utils.verify_psd(run.utils.R)
    logging.basicConfig(level=logging.INFO)
    run.utils.log_dataframe_summary(pd.DataFrame(backgrounds),'25 new PD backgrounds; no selection',logging.getLogger('PD'))
    cells=[]
    for b,bg in enumerate(backgrounds):
        for s,target in [('S2','FORMAL_REPORT'),('S3','WAIT')]:
            for v in (.1,.9):
                c=deepcopy(next(c for c in source['design']['cells'] if c['parameter']=='PD' and c['problem']==s and c['value']==v))
                profile=dict(bg,PD=v)
                c.update(id=f'background_{b:02d}/PD_{s}/canonical/v{v:.1f}',background=b,profile=profile,
                    rendered_profile={p:float(f'{x:.2f}') for p,x in profile.items()},target_label=target,
                    prespecified=True)
                c['messages'][0]['content']=run.render('PD',v,profile,'canonical',{})
                cells.append(c)
    d=deepcopy(source['design'])
    d.update(stage='pd_confirmation',experiment='independent_PD_endpoint_confirmation',cells=cells,
        seed=20261013,draw_seed=20261012,analysis_seed=20261014,planned_calls=100,n_backgrounds=25,
        params=['PD'],problems=['S2','S3'],backgrounds=backgrounds,backgrounds_hash=digest(backgrounds),
        primary='PD high-minus-low on FORMAL_REPORT/S2 and WAIT/S3. Exact matched binomial, Holm2; simultaneous conservative paired effect bounds. Both must pass.',
        phase_gate='Independent local confirmation only; original validity gate and Phase2 hold unchanged.')
    paths=[Path(__file__),PROTOCOL,run.ROOT/'tests/test_structural_pd_confirmation.py',run.PACKAGE/'sweep/manifest.json',run.PACKAGE/'sweep/analysis/result_f87bac164d8bfc5d.json',run.PACKAGE/'sweep/analysis/discrete_uncertainty_sensitivity.json',run.PACKAGE/'audit_schema_r3/manifest.json']
    d['source_hashes'].update({p.relative_to(run.ROOT).as_posix():sha256(p.read_bytes()).hexdigest() for p in paths})
    d['full_dispatch_reserve_usd']=sum(run.base.reserve(c,d) for c in cells)
    d['spending_ceiling_usd']=d['full_dispatch_reserve_usd']+1e-8
    audit=json.loads((run.PACKAGE/'audit_schema_r3/manifest.json').read_bytes())['design']
    d['other_package_reserved_usd']=audit['behavioural_reservation_usd']+audit['full_dispatch_reserve_usd']
    if d['full_dispatch_reserve_usd']+d['other_package_reserved_usd']>25:raise ValueError('Package exceeds $25')
    return d


def exact_effect(effects):
    """Union-bound simultaneous CIs: 4 marginals across 2 contrasts, family .05."""
    x=np.asarray(effects);n=len(x);pos=int(sum(x==1));neg=int(sum(x==-1))
    def cp(k):
        tail=.05/4/2
        return [0. if k==0 else float(beta.ppf(tail,k,n-k+1)),
                1. if k==n else float(beta.ppf(1-tail,k+1,n-k))]
    p=cp(pos);q=cp(neg)
    return {'effect':float(x.mean()),'simultaneous95':[p[0]-q[1],p[1]-q[0]],
        'positive_pairs':pos,'negative_pairs':neg,'tied_pairs':n-pos-neg,
        'p_two_sided':float(binomtest(pos,pos+neg,.5).pvalue) if pos+neg else 1.}


def assess(rows,m):
    d=m['design'];lookup={r['cell_id']:r for r in rows}
    complete=len(rows)==100 and len(lookup)==100 and all(not r['terminal_failure'] and r['parse_status']=='ok' for r in rows)
    groups=[]
    if complete:
        for s in ('S2','S3'):
            values=np.empty((25,2))
            cells=[c for c in d['cells'] if c['problem']==s]
            for c in cells:values[c['background'],0 if c['value']==.1 else 1]=int(lookup[c['id']]['parsed_decision']==c['target_label'])
            effects=values[:,1]-values[:,0]
            groups.append(dict(problem=s,target_label=cells[0]['target_label'],rates=values.mean(axis=0).tolist(),n_backgrounds=25,
                background_effects=effects.tolist(),**exact_effect(effects)))
        ordered=sorted(range(2),key=lambda i:groups[i]['p_two_sided']);running=0.
        for rank,i in enumerate(ordered):
            running=max(running,min(1.,(2-rank)*groups[i]['p_two_sided']))
            groups[i]['p_holm']=running
            groups[i]['supported']=running<.05 and groups[i]['simultaneous95'][0]>0
        run.utils.log_dataframe_summary(pd.DataFrame(groups),'100 responses to both contrasts; no exclusions',logging.getLogger('PD'))
    return {'design_hash':m['design_hash'],'complete':complete,'n_records':len(rows),'groups':groups,
        'both_supported':complete and all(g['supported'] for g in groups),'known_cost_usd':sum(run.base.cost(r) or 0 for r in rows),
        'configuration':'neutral','draw_seed':20261012,'schedule_seed':20261013,'phase_gate':d['phase_gate']}


def score(m):
    planned,rows,seen=run.inventory(ROOT,m)
    intents={json.loads(p.read_bytes())['record_key']:json.loads(p.read_bytes()) for p in (ROOT/'dispatches').rglob('*.json')}
    if not seen.issubset(intents):raise ValueError('Missing intents')
    for k,i in intents.items():
        if k not in planned or i!=run.intent(k,planned[k][0],m):raise ValueError('Intent mismatch')
    ids=[]
    for r in rows:
        if digest({k:v for k,v in r.items() if k!='record_hash'})!=r['record_hash']:raise ValueError('Record hash mismatch')
        if not r['terminal_failure']:
            if r['temperature']!=1. or r['max_tokens']!=600 or r['attempts']!=1:raise ValueError('Setting mismatch')
            ids.append(r['api_call_id'])
    if len(ids)!=len(set(ids)):raise ValueError('Duplicate IDs')
    result=assess(rows,m);save_new(ROOT/'analysis'/f'result_{digest(result)[:16]}.json',result)
    by_key={r['record_key']:r for r in rows}
    save_new(ROOT/'budget_ledger.json',{'known_cost_usd':result['known_cost_usd'],
        'unknown_usage_reserved_usd':sum(v['reserved_usd'] for k,v in intents.items() if k not in by_key or run.base.cost(by_key[k]) is None),
        'pending_requests':len(intents)-len(rows),'reserved_usd':sum(i['reserved_usd'] for i in intents.values()),'provider_balance_verified':False})
    return result


def main():
    p=argparse.ArgumentParser();p.add_argument('--prepare-only',action='store_true');p.add_argument('--yes',action='store_true');a=p.parse_args()
    if a.prepare_only:
        d=build();m=freeze(ROOT/'manifest.json',d);save_new(ROOT/'request_preview.json',{'design_hash':m['design_hash'],'cells':d['cells']})
        save_new(ROOT/'dispatch_authorization.json',{'design_hash':m['design_hash'],'basis':'User authorized needed structural tests within $25; fresh local confirmation after all-ten sweep, no theoretical departure.'})
        print(json.dumps({'calls':100,'reserve_usd':d['full_dispatch_reserve_usd'],'package_reserved_usd':d['full_dispatch_reserve_usd']+d['other_package_reserved_usd']}));return
    if not a.yes or not os.environ.get('OPENAI_API_KEY'):p.error('Need --yes and configured key')
    m=json.loads((ROOT/'manifest.json').read_bytes());run.base.check(m)
    if json.loads((ROOT/'dispatch_authorization.json').read_bytes())['design_hash']!=m['design_hash']:raise ValueError('Authorization mismatch')
    if m['design']['full_dispatch_reserve_usd']+m['design']['other_package_reserved_usd']>25:raise ValueError('Package budget breach')
    from openai import AsyncOpenAI
    import msvcrt
    async def work():
        async with AsyncOpenAI(base_url='https://api.openai.com/v1',max_retries=0,timeout=180) as sdk:
            client=run.base.SingleAttemptOpenAI(run.base.MODEL,concurrency=3,max_retries=1,timeout_s=180);client._client=sdk
            await run.execute(ROOT,m,client)
    with (run.ROOT/'output/structural_PD_confirmation.lock').open('a+b') as lock:
        lock.write(b'0');lock.flush();lock.seek(0);msvcrt.locking(lock.fileno(),msvcrt.LK_NBLCK,1)
        try:asyncio.run(work())
        finally:
            try:result=score(m)
            finally:run.archive_support.archive(ROOT,m)
            print(json.dumps(result,indent=2))


if __name__=='__main__':main()
