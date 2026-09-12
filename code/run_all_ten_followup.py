"""All-ten follow-up with settled-usage accounting and reserved in-flight batches."""
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
from itertools import combinations

import run_structural_encoding_validation as old
from engine.validity_sweep import digest, freeze, ValiditySink
from engine.validity_equivalence import tost
from engine.validity_analysis import analyze as legacy_analyze
from engine.validity_followup import gradient_comparison
from run_validity_claude import save_new

ROOT=old.BASE/'all_ten_followup_20260912'
PROTOCOL=ROOT/'PROTOCOL.md'
OLD_BUDGET=old.PACKAGE/'FINAL_BUDGET.json'


def build():
    source=json.loads((old.PACKAGE/'sweep/manifest.json').read_bytes());old.base.check(source)
    budget=json.loads(OLD_BUDGET.read_bytes())
    if budget['pending_requests']!=0:raise ValueError('Prior requests unresolved')
    prior_charge=budget['known_token_estimate_usd']+budget['unknown_usage_reserved_usd']
    templates=old.load_reviewed_paraphrases(old.TEMPLATES)
    backgrounds=[dict(zip(old.utils.PARAM_NAMES,map(float,r))) for r in old.utils.sample_agents(50,seed=20261020)]
    if set(map(digest,backgrounds))&set(map(digest,source['design']['backgrounds'])):raise ValueError('Reused backgrounds')
    logging.basicConfig(level=logging.INFO)
    old.utils.log_dataframe_summary(pd.DataFrame(backgrounds),'All50 draws; first25 for gradients, all50 for wording, fixed before outcomes',logging.getLogger('all-ten'))
    lookup={(c['parameter'],c['problem'],c['value']):c for c in source['design']['cells']}
    cells=[]
    for phase,nb,variants,values in [('gradients',25,('canonical','numeric_only','verbal_only'),old.VALUES),
                                    ('wording',50,('canonical',*templates),(.8,))]:
        for b,bg in enumerate(backgrounds[:nb]):
            for p in old.utils.PARAM_NAMES:
                for s in ('S1','S2','S3'):
                    for variant in variants:
                        for v in values:
                            c=deepcopy(lookup[p,s,.1]);profile=dict(bg);profile[p]=v
                            c.update(id=f'background_{b:02d}/{p}_{s}/{variant}/v{v:.1f}',background=b,phase=phase,
                                variant=variant,value=v,profile=profile,
                                rendered_profile={k:(old.verbal_level(x) if variant=='verbal_only' else float(f'{x:.2f}')) for k,x in profile.items()})
                            c['messages'][0]['content']=old.render(p,v,profile,variant,templates)
                            cells.append(c)
    d=deepcopy(source['design'])
    d.update(stage='all_ten_followup',experiment='all_ten_three_categories',cells=cells,n_backgrounds=50,
        backgrounds=backgrounds,backgrounds_hash=digest(backgrounds),draw_seed=20261020,seed=20261021,
        analysis_seed=20261022,planned_calls=17250,prior_accounted_usd=prior_charge,total_package_cap_usd=25.,
        spending_ceiling_usd=25.-prior_charge,
        primary='Separate gradient endpoint/interior, paired wording equivalence and numeric/verbal retention diagnostics. Existing all-ten audit retained separately. See protocol; no new original-gate pass.',
        phase_gate='Original gate unchanged; profile-average follow-up is not a retroactive original-battery pass.')
    paths=[Path(__file__),PROTOCOL,OLD_BUDGET,old.PACKAGE/'sweep/manifest.json',
        old.ROOT/'tests/test_all_ten_followup.py',old.ROOT/'code/engine/validity_equivalence.py',
        old.ROOT/'code/engine/validity_followup.py']
    d['source_hashes'].update({p.relative_to(old.ROOT).as_posix():sha256(p.read_bytes()).hexdigest() for p in paths})
    d['sum_of_individual_worst_case_reservations_usd']=sum(old.base.reserve(c,d) for c in cells)
    d['budget_policy']='Prior settled usage + prior unknown bounds + new settled usage + unresolved/in-flight reservation <=25 before every batch; full worst-case study funding is not guaranteed.'
    if len(cells)!=17250 or len({c['id'] for c in cells})!=17250:raise ValueError('Allocation mismatch')
    return d


def checkpoint(root,rows,d,reason):
    known=sum(old.base.cost(r) or 0 for r in rows)
    report={'recorded':len(rows),'valid':sum(r['parse_status']=='ok' and not r['terminal_failure'] for r in rows),
        'planned':d['planned_calls'],'known_cost_usd':known,'prior_accounted_usd':d['prior_accounted_usd'],
        'total_accounted_usd':known+d['prior_accounted_usd'],'status':reason}
    tmp=root/'progress.tmp';tmp.write_text(json.dumps(report,indent=2),encoding='utf-8');os.replace(tmp,root/'progress.json')


async def execute(root,m,client):
    _,rows,_=old.inventory(root,m);d=m['design'];schedule=list(old.jobs(d))
    if rows or any((root/'dispatches').rglob('*.json')):raise ValueError('Existing attempts; no automatic resume')
    if len({j[3] for j in schedule})!=len(schedule):raise ValueError('Seed collision')
    spent=0.;sink=ValiditySink(root/'records')
    async def one(job):
        key,c,i,seed=job
        r=await client.complete([old.Message(**x) for x in c['messages']],temperature=1.,max_tokens=600,seed=seed)
        decision,parse=old.parse_decision(r.text,tuple(c['labels']))
        row={'record_key':key,'design_hash':m['design_hash'],'cell_id':c['id'],'call_index':i,'seed':seed,
            'arm':'full_harness','swept_parameter':c['parameter'],'sweep_value':c['value'],'problem_id':c['problem'],
            'agent_parameters':c['profile'],'phase':c['phase'],'request_messages':r.request_messages,
            'response_payload':r.raw_response,'raw_response':r.text,'parsed_decision':decision,
            'parsed_reasoning':old.parse_reasoning(r.text),'parse_status':parse,'api_call_id':r.api_call_id,
            'model_version':r.model_version,'provider':r.provider,'attempts':r.attempts,'error_message':r.error,
            'timestamp_utc':r.timestamp_utc,'temperature':r.temperature,'max_tokens':r.max_tokens}
        cost=old.base.cost(row)
        row['terminal_failure']=bool(r.error or r.provider!='openai' or r.model_version!=old.base.MODEL or r.attempts!=1
            or not r.api_call_id or cost is None or cost>old.base.reserve(c,d) or r.request_messages!=c['messages']
            or r.temperature!=1. or r.max_tokens!=600)
        row['record_hash']=digest(row);sink.write(key,row)
        if row['terminal_failure'] or parse!='ok':sink.write_failure({'record_key':key,'error':r.error,'parse_status':parse})
        return row
    for start in range(0,len(schedule),3):
        batch=schedule[start:start+3];bound=sum(old.base.reserve(c,d) for _,c,_,_ in batch)
        if d['prior_accounted_usd']+spent+bound>d['total_package_cap_usd']:
            checkpoint(root,rows,d,'BUDGET_STOP');return 'BUDGET_STOP'
        for key,c,_,_ in batch:save_new(root/'dispatches'/(key+'.json'),old.intent(key,c,m))
        new=await asyncio.gather(*(one(j) for j in batch));rows.extend(new)
        # Unknown usage causes a stop; its full dispatched bound remains in the final ledger.
        spent+=sum(old.base.cost(r) or 0 for r in new)
        if any(r['terminal_failure'] for r in new):checkpoint(root,rows,d,'TECHNICAL_STOP');return 'TECHNICAL_STOP'
        if len(rows)%30==0 or len(rows) in (3,len(schedule)):
            checkpoint(root,rows,d,'RUNNING' if len(rows)<len(schedule) else 'COLLECTED')
            print(f"{len(rows)}/{len(schedule)}; new cost ${spent:.5f}; cumulative ${spent+d['prior_accounted_usd']:.5f}",flush=True)
    return 'COLLECTED'


def paired_interval(effects,alpha=.10):
    x=np.asarray(effects);n=len(x);pos=int(sum(x==1));neg=int(sum(x==-1))
    def cp(k):return (0. if k==0 else float(beta.ppf(alpha/4,k,n-k+1)),1. if k==n else float(beta.ppf(1-alpha/4,k+1,n-k)))
    a,b=cp(pos),cp(neg)
    return {'difference':float(x.mean()),'ci90_conservative':[a[0]-b[1],a[1]-b[0]],'positive_pairs':pos,'negative_pairs':neg,'ties':n-pos-neg}


def gradient_sensitivity(rows,m):
    cells=[c for c in m['design']['cells'] if c['phase']=='gradients']
    by_id={r['cell_id']:r for r in rows};canonical=[];new_cells=[];exact=[]
    for c in cells:
        r=by_id.get(c['id'])
        if c['variant']=='canonical' and r:
            canonical.append(dict(r,call_index=c['background']+1,labels=c['labels']))
    legacy=legacy_analyze(canonical,params=m['design']['params'],problems=['S1','S2','S3'],arms=['full_harness'],n=25)
    for p in m['design']['params']:
        for s in ('S1','S2','S3'):
            for variant in ('canonical','numeric_only','verbal_only'):
                block=np.full((25,5),np.nan)
                for vi,v in enumerate(old.VALUES):
                    selected=[c for c in cells if (c['parameter'],c['problem'],c['variant'],c['value'])==(p,s,variant,v)]
                    recorded=[by_id[c['id']] for c in selected if c['id'] in by_id]
                    valid=[r for r in recorded if not r['terminal_failure'] and r['parse_status']=='ok']
                    if variant!='canonical':new_cells.append({'parameter':p,'problem':s,'variant':variant,'value':v,
                        'n_expected':25,'n_recorded':len(recorded),'n_valid':len(valid),
                        'opt0_count':sum(r['parsed_decision']==selected[0]['labels'][0] for r in valid)})
                    for c in selected:
                        r=by_id.get(c['id'])
                        if r and not r['terminal_failure'] and r['parse_status']=='ok':block[c['background'],vi]=int(r['parsed_decision']==c['target_label'])
                for contrast,a,b in [('endpoint',4,0),('interior',3,1)]:
                    clean=bool(np.isfinite(block[:,[a,b]]).all())
                    x=block[:,a]-block[:,b]
                    pos=int(sum(x==1));neg=int(sum(x==-1))
                    pvalue=float(binomtest(pos,pos+neg,.5).pvalue) if clean and pos+neg else 1.
                    exact.append({'parameter':p,'problem':s,'variant':variant,'contrast':contrast,'complete_pairs':clean,
                        'missing_pairs':int(sum(~np.isfinite(x))),'positive_pairs':pos,'negative_pairs':neg,
                        'effect':float(x.mean()) if clean else None,'p_exact':pvalue})
    ordered=sorted(range(len(exact)),key=lambda i:exact[i]['p_exact']);last=0.
    for rank,i in enumerate(ordered):
        last=max(last,min(1.,(len(exact)-rank)*exact[i]['p_exact']));exact[i]['p_holm']=last
    retention=gradient_comparison(new_cells,legacy['sweeps'])
    old.utils.log_dataframe_summary(pd.DataFrame(new_cells),'All300 numeric/verbal value cells, including invalid/missing counts; no discarded cells',logging.getLogger('all-ten'))
    return {'legacy_independent_call_diagnostic':legacy,'representation_retention_diagnostic':retention,
        'exact_paired_180_comparisons':exact,
        'warning':'Legacy fit/retention p-values ignore repeated backgrounds; paired sensitivity retained. Incomplete contrasts use p=1 for multiplicity and never support a claim. No new gate.'}


def assess(rows,m):
    d=m['design'];by_id={r['cell_id']:r for r in rows};all_recorded=len(rows)==d['planned_calls']
    gc=[c for c in d['cells'] if c['phase']=='gradients'];gr=[r for r in rows if r['phase']=='gradients']
    sub=deepcopy(m);sub['design'].update(cells=gc,planned_calls=11250,n_backgrounds=25)
    gradient=old.assess(gr,sub)
    # A malformed response disqualifies its curve from complete-case claims;
    # original records remain counted and are never silently replaced or dropped.
    words=[]
    variants=('canonical','paraphrase_1','paraphrase_2','paraphrase_3')
    for p in d['params']:
        for s in d['problems']:
            values={};complete=True
            for v in variants:
                selected=sorted([c for c in d['cells'] if c['phase']=='wording' and c['parameter']==p and c['problem']==s and c['variant']==v],key=lambda c:c['background'])
                rs=[by_id.get(c['id']) for c in selected]
                if len(rs)!=50 or any(r is None or r['terminal_failure'] or r['parse_status']!='ok' for r in rs):complete=False
                else:values[v]=np.array([int(r['parsed_decision']==selected[i]['target_label']) for i,r in enumerate(rs)])
            pairs=[]
            if complete:
                for a,b in combinations(variants,2):
                    pair=paired_interval(values[a]-values[b]);lo,hi=pair['ci90_conservative']
                    pairs.append(dict(a=a,b=b,**pair,equivalent=lo>-.1 and hi<.1,
                        original_independent_TOST_sensitivity=tost(int(values[a].sum()),50,int(values[b].sum()),50)))
            words.append({'parameter':p,'problem':s,'complete':complete,'pairs':pairs,'all_pairs_equivalent':complete and all(x['equivalent'] for x in pairs)})
    return {'design_hash':m['design_hash'],'all_planned_recorded':all_recorded,'n_records':len(rows),
        'n_parse_invalid':sum(r['parse_status']!='ok' for r in rows),'n_terminal_failures':sum(r['terminal_failure'] for r in rows),
        'gradient_analysis':gradient,'gradient_sensitivity':gradient_sensitivity(rows,m),
        'wording_analysis':words,'original_gate_passed':False,
        'note':'Profile-average wording equivalence, not conditional equality for each profile. Existing independent TOST is a sensitivity only. Old audit is separate evidence; no new coder run.'}


def score(root,m,reason):
    planned,rows,seen=old.inventory(root,m);by_key={r['record_key']:r for r in rows}
    intents={}
    for p in (root/'dispatches').rglob('*.json'):
        x=json.loads(p.read_bytes());k=x['record_key']
        if k not in planned or k in intents or x!=old.intent(k,planned[k][0],m):raise ValueError('Intent mismatch')
        intents[k]=x
    if not seen.issubset(intents):raise ValueError('Missing intents')
    ids=[r['api_call_id'] for r in rows if r['api_call_id']]
    if len(ids)!=len(set(ids)):raise ValueError('Duplicate returned API IDs')
    known=sum(old.base.cost(r) or 0 for r in rows)
    unknown=sum(x['reserved_usd'] for k,x in intents.items() if k not in by_key or old.base.cost(by_key[k]) is None)
    ledger={'status':reason,'known_cost_usd':known,'unknown_usage_reserved_usd':unknown,'pending_requests':len(intents)-len(rows),
        'prior_accounted_usd':m['design']['prior_accounted_usd'],'total_accounted_usd':known+unknown+m['design']['prior_accounted_usd'],
        'cap_usd':25,'provider_balance_verified':False,'n_records':len(rows)}
    if ledger['total_accounted_usd']>25+1e-8:raise ValueError('Accounted usage exceeds cap')
    result=assess(rows,m);save_new(root/'analysis'/f'result_{digest(result)[:16]}.json',result);save_new(root/'budget_ledger.json',ledger)
    return ledger


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--prepare-only',action='store_true');parser.add_argument('--yes',action='store_true');args=parser.parse_args()
    if args.prepare_only:
        d=build();m=freeze(ROOT/'manifest.json',d)
        save_new(ROOT/'request_preview.json',{'design_hash':m['design_hash'],'cells':d['cells']})
        save_new(ROOT/'dispatch_authorization.json',{'design_hash':m['design_hash'],'basis':'User confirmed all ten and all three categories, then instructed go. Existing $25 total cap retained with batch reservations and settled usage; no expanded budget assumed.'})
        print(json.dumps({'planned_calls':d['planned_calls'],'available_usd':d['spending_ceiling_usd'],'full_unreserved_worst_case_usd':d['sum_of_individual_worst_case_reservations_usd']}));return
    if not args.yes or not os.environ.get('OPENAI_API_KEY'):parser.error('Need --yes and configured key')
    m=json.loads((ROOT/'manifest.json').read_bytes());old.base.check(m)
    if json.loads((ROOT/'dispatch_authorization.json').read_bytes())['design_hash']!=m['design_hash']:raise ValueError('Authorization mismatch')
    from openai import AsyncOpenAI
    import msvcrt
    async def work():
        async with AsyncOpenAI(base_url='https://api.openai.com/v1',max_retries=0,timeout=180) as sdk:
            client=old.base.SingleAttemptOpenAI(old.base.MODEL,concurrency=3,max_retries=1,timeout_s=180);client._client=sdk
            return await execute(ROOT,m,client)
    with (old.ROOT/'output/all_ten_followup.lock').open('a+b') as lock:
        lock.write(b'0');lock.flush();lock.seek(0);msvcrt.locking(lock.fileno(),msvcrt.LK_NBLCK,1)
        reason='UNEXPECTED_STOP'
        try:reason=asyncio.run(work())
        finally:
            try:ledger=score(ROOT,m,reason)
            finally:old.archive_support.archive(ROOT,m)
            print(json.dumps(ledger))


if __name__=='__main__':main()
