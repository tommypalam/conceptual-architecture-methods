"""Execute the reviewed, single-candidate axis pilot; keep all observations immutable."""
import argparse
import asyncio
from collections import defaultdict
import hashlib
import itertools
import json
import logging
import os
from pathlib import Path
import random

import pandas as pd
import utils
from engine.llm_client import LLMClient,Message,utc_now_iso
from engine.parsing import parse_decision,parse_reasoning
from engine.seeding import derive_seed
from engine.validity_sweep import ValiditySink,digest
from engine.validity_analysis import analyze,wilson
from engine.validity_equivalence import tost
from prepare_validity_axis_revision import ROOT
from run_validity_claude import save_new
from run_validity_restart_followups import archive


def jobs(d):
    groups=defaultdict(dict)
    for c in d['cells']:
        groups[(c['stage'],c['wording'],c['problem'],c['value'])][c['arm']]=c
    pairs=[]
    for group,arms in groups.items():
        if set(arms)!={'baseline','revision'} or arms['baseline']['n']!=arms['revision']['n']:
            raise ValueError('Unbalanced candidate/control pair')
        for k in range(1,arms['baseline']['n']+1):
            pair=[]
            for arm in ('baseline','revision'):
                c=arms[arm];key=f"{c['stage']}/{c['variant']}/PD/{c['problem']}/{c['value']:.1f}/call_{k:04d}"
                pair.append((key,c,k))
            pairs.append(pair)
    rng=random.Random(d['seed']);rng.shuffle(pairs)
    for pair in pairs: rng.shuffle(pair)
    return [job for pair in pairs for job in pair]


def check_approval(m,path):
    r=json.loads(path.read_text(encoding='utf-8'));d=m['design']
    if not r.get('approved') or not r.get('reviewer') or r.get('proposal_hash')!=m['design_hash']:
        raise ValueError('Exact candidate review pending')
    if r.get('instruction_hash')!=digest(d['revision_text']) or r.get('template_hashes')!=d['template_hashes'] or r.get('exact_messages_hash')!=digest([c['messages'] for c in d['cells']]):
        raise ValueError('Review does not match exact instructions/messages')


def cost(row):
    u=(row.get('response_payload') or {}).get('usage',{})
    return (u.get('prompt_tokens',0)*.75+u.get('completion_tokens',0)*4.5)/1e6


async def execute(m,client,sink):
    d=m['design']
    if digest(d)!=m['design_hash']: raise ValueError('Manifest integrity failure')
    for path,h in d['source_hashes'].items():
        if hashlib.sha256((ROOT/path).read_bytes()).hexdigest()!=h: raise ValueError(f'Frozen source changed: {path}')
    planned=jobs(d);expected={key:(c,k) for key,c,k in planned};rows=list(sink.read_all())
    seen={r['record_key'] for r in rows}
    if len(rows)!=len(seen) or not seen<=expected.keys(): raise ValueError('Unexpected existing records')
    for r in rows:
        c,k=expected[r['record_key']]
        if r['design_hash']!=m['design_hash'] or r.get('error_message') or r.get('model_version_mismatch'):
            raise ValueError('Mixed design or preserved terminal failure; new designation needed')
        if r['request_messages']!=c['messages']: raise ValueError('Existing request mismatch')
    spent=sum(cost(r) for r in rows)
    pending=[job for job in planned if job[0] not in seen]
    async def one(job):
        key,c,k=job
        seed=derive_seed(d['seed'],c['stage'],c['arm'],c['wording'],c['problem'],c['value'],k)
        result=await client.complete([Message(**v) for v in c['messages']],temperature=d['temperature'],max_tokens=d['max_tokens'],seed=seed)
        decision,parse=parse_decision(result.text,tuple(c['labels']))
        expected_model=d['model']+'-mock' if d['provider']=='mock' else d['model']
        mismatch=result.ok and result.model_version!=expected_model
        row={'schema_version':'1.0','phase':d['phase'],'experiment':d['experiment'],'design_hash':m['design_hash'],
            'record_key':key,'stage':c['stage'],'arm':c['arm'],'wording':c['wording'],'variant':c['variant'],
            'swept_parameter':'PD','sweep_value':c['value'],'problem_id':c['problem'],'labels':c['labels'],
            'agent_parameters':c['profile'],'call_index':k,'seed':seed,'timestamp_utc':result.timestamp_utc,
            'provider':result.provider,'model_version':result.model_version,'model_version_mismatch':bool(mismatch),
            'api_call_id':result.api_call_id,'attempts':result.attempts,'request_messages':result.request_messages,
            'response_payload':result.raw_response,'raw_response':result.text,'parsed_decision':decision,
            'parsed_reasoning':parse_reasoning(result.text),'parse_status':'failed_api' if result.error else 'model_mismatch' if mismatch else parse,
            'error_message':result.error}
        row['record_hash']=digest(row);sink.write(key,row)
        if result.error or mismatch: sink.write_failure({'record_key':key,'error':result.error,'model_mismatch':bool(mismatch)})
        return row
    for start in range(0,len(pending),4):
        batch=pending[start:start+4]
        # UTF-8 input bytes plus overhead conservatively budget ordinary text input;
        # provider billing and unreported retry charges remain externally authoritative.
        reserve=sum((sum(len(v['content'].encode('utf-8')) for v in c['messages'])+128)*.75/1e6+d['max_tokens']*4.5/1e6 for _,c,_ in batch)
        if spent+reserve>d['collection']['spending_ceiling_usd']:
            raise RuntimeError('Pilot spending ceiling: incomplete sample preserved; no further dispatch')
        batch_rows=await asyncio.gather(*(one(job) for job in batch));spent+=sum(cost(r) for r in batch_rows)
        count=len(rows)+start+len(batch)
        if start==0 or count%100==0 or count==d['planned_calls']: print(f'{count}/{d["planned_calls"]}; recorded token estimate ${spent:.4f}',flush=True)
        if any(r['error_message'] or r['model_version_mismatch'] for r in batch_rows):
            raise RuntimeError('Terminal failure preserved; dispatch stopped')


def equivalence(cells):
    eligible=len(cells)==4 and all(c['n_recorded']==c['n_expected'] and c['n_valid']/c['n_expected']>=.98 for c in cells)
    pairs=[]
    if eligible:
        for a,b in itertools.combinations(cells,2):
            result=tost(a['opt0_count'],a['n_valid'],b['opt0_count'],b['n_valid'])
            robust=all(tost(ka,a['n_expected'],kb,b['n_expected'])['equivalent']
                for ka in range(a['opt0_count'],a['opt0_count']+a['n_invalid']+1)
                for kb in range(b['opt0_count'],b['opt0_count']+b['n_invalid']+1))
            pairs.append({'a':a['wording'],'b':b['wording'],**result,'all_unknown_completions_equivalent':robust})
    saturated=bool(eligible and (all(c['rate']<=.05 for c in cells) or all(c['rate']>=.95 for c in cells)))
    return {'eligible':eligible,'pairs':pairs,'all_pairs_equivalent':bool(eligible and all(p['equivalent'] for p in pairs)),
        'all_unknown_completions_equivalent':bool(eligible and all(p['all_unknown_completions_equivalent'] for p in pairs)),
        'saturated_all_formulations':saturated}


def score(root,m):
    d=m['design'];rows=list(ValiditySink(root/'records').read_all());expected={key for key,_,_ in jobs(d)}
    if len({r['record_key'] for r in rows})!=len(rows) or any(r['record_key'] not in expected or r['design_hash']!=m['design_hash'] for r in rows):
        raise ValueError('Mixed or unexpected records')
    grouped=defaultdict(list)
    for r in rows: grouped[(r['stage'],r['arm'],r['wording'],r['problem_id'],r['sweep_value'])].append(r)
    cells=[]
    for c in d['cells']:
        data=grouped[(c['stage'],c['arm'],c['wording'],c['problem'],c['value'])]
        good=[r for r in data if r['parse_status']=='ok' and r['parsed_decision'] in c['labels']]
        k=sum(r['parsed_decision']==c['labels'][0] for r in good)
        cells.append({**{k:c[k] for k in ('stage','arm','wording','problem','value')},'n_expected':c['n'],
            'n_recorded':len(data),'n_valid':len(good),'n_invalid':len(data)-len(good),'n_missing':c['n']-len(data),
            'opt0_count':k,'rate':k/len(good) if good else None,'ci95':wilson(k,len(good))})
    logging.basicConfig(level=logging.INFO)
    utils.log_dataframe_summary(pd.DataFrame(cells),'All axis pilot cells; invalid/missing retained',logging.getLogger('axis-score'))
    eq={arm:equivalence([c for c in cells if c['stage']=='equivalence' and c['arm']==arm]) for arm in ('baseline','revision')}
    sweep_rows=[r for r in rows if r['stage']=='sweep']
    utils.log_dataframe_summary(pd.DataFrame(sweep_rows),'Sweep-only analysis selection; all source rows preserved',logging.getLogger('axis-score'))
    sweeps=analyze(sweep_rows,params=['PD'],problems=['S1','S2','S3'],arms=['baseline','revision'],n=50)
    complete=len(rows)==d['planned_calls'];terminal=any(r.get('error_message') or r.get('model_version_mismatch') for r in rows)
    revision_s1=next(c for c in sweeps['sweeps'] if c['arm']=='revision' and c['problem']=='S1')
    local=bool(complete and not terminal and eq['revision']['all_pairs_equivalent'] and
        eq['revision']['all_unknown_completions_equivalent'] and not eq['revision']['saturated_all_formulations'] and revision_s1['criterion_met'])
    result={'design_hash':m['design_hash'],'configuration':'neutral','seed':d['seed'],'cells':cells,'equivalence':eq,
        'sweeps':sweeps,'recorded_token_estimate_usd':sum(cost(r) for r in rows),
        'status':'LOCAL_SCREEN_MET_RESEARCH_REVIEW_REQUIRED' if local else 'LOCAL_SCREEN_NOT_MET_OR_INCOMPLETE',
        'phase_gate':'Unchanged; this selected-PD pilot cannot close the battery'}
    path=root/'analysis'/f'axis_pilot_{digest(result)[:16]}.json';save_new(path,result)
    if complete: archive(root)
    print(path,flush=True);return result


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--run-root',type=Path,required=True)
    p.add_argument('--approval',type=Path);p.add_argument('--yes',action='store_true');p.add_argument('--score-only',action='store_true')
    a=p.parse_args();root=a.run_root.resolve();m=json.loads((root/'manifest.json').read_text(encoding='utf-8'))
    if digest(m['design'])!=m['design_hash']: raise ValueError('Invalid manifest')
    if a.score_only: score(root,m);return
    if not a.yes or not a.approval or not os.environ.get('OPENAI_API_KEY'): p.error('Need --yes, exact approval and configured key')
    check_approval(m,a.approval)
    import msvcrt
    logs=ROOT/'output'/root.name;logs.mkdir(parents=True,exist_ok=True)
    with (logs/'execution.lock').open('a+b') as lock:
        lock.write(b'0');lock.flush();lock.seek(0);msvcrt.locking(lock.fileno(),msvcrt.LK_NBLCK,1)
        def status(value): (logs/'status.json').write_text(json.dumps({'status':value,'timestamp_utc':utc_now_iso(),'design_hash':m['design_hash']},indent=2),encoding='utf-8')
        status('RUNNING')
        try:
            try: asyncio.run(execute(m,LLMClient(model=m['design']['model'],concurrency=4),ValiditySink(root/'records')))
            finally: result=score(root,m)
            status(result['status'])
        except BaseException: status('STOPPED_WITH_ERROR');raise


if __name__=='__main__': main()
