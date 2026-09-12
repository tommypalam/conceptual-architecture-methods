"""Second execution segment; untouched requests from the original frozen schedule only."""
import argparse
import asyncio
from hashlib import sha256
import json
import os
from pathlib import Path
import run_all_ten_followup as original
from run_all_ten_followup import old, save_new, digest, ValiditySink, checkpoint

PARENT=original.ROOT
ROOT=old.BASE/'all_ten_followup_20260912_segment2'


def segment_inventory(root,m):
    planned,rows,seen=old.inventory(root,m)
    intents={}
    for p in (root/'dispatches').rglob('*.json'):
        value=json.loads(p.read_bytes());k=value['record_key']
        if k in intents or k not in planned or value!=old.intent(k,planned[k][0],m):
            raise ValueError('Unexpected dispatch intent')
        intents[k]=value
    if not seen.issubset(intents):raise ValueError('Record without intent')
    by_key={r['record_key']:r for r in rows}
    return dict(rows=rows,intents=intents,known=sum(old.base.cost(r) or 0 for r in rows),
        unknown=sum(v['reserved_usd'] for k,v in intents.items() if k not in by_key or old.base.cost(by_key[k]) is None),
        pending=len(intents)-len(rows))


def prepare():
    m=json.loads((PARENT/'manifest.json').read_bytes());parent=segment_inventory(PARENT,m)
    ledger=json.loads((PARENT/'budget_ledger.json').read_bytes())
    if parent['pending'] or ledger['status']!='TECHNICAL_STOP':raise ValueError('Parent not settled at technical stop')
    accounted=m['design']['prior_accounted_usd']+parent['known']+parent['unknown']
    if abs(accounted-ledger['total_accounted_usd'])>1e-9:raise ValueError('Parent accounting mismatch')
    paths=[PARENT/'manifest.json',PARENT/'budget_ledger.json',PARENT/'local_backup.json',
        Path(__file__),ROOT/'PROTOCOL.md',old.ROOT/'tests/test_all_ten_continuation.py']
    plan={'design_hash':m['design_hash'],'parent':str(PARENT.relative_to(old.ROOT)),
        'excluded_dispatch_keys':sorted(parent['intents']),
        'remaining_calls':m['design']['planned_calls']-len(parent['intents']),
        'prior_accounted_including_parent_usd':accounted,'cap_usd':25,
        'source_hashes':{p.relative_to(old.ROOT).as_posix():sha256(p.read_bytes()).hexdigest() for p in paths},
        'basis':'Previously authorized fixed all-ten design and $25 cumulative cap; administrative continuation of unattempted slots only.'}
    save_new(ROOT/'continuation_plan.json',plan)
    print(json.dumps({k:v for k,v in plan.items() if k not in ('source_hashes','excluded_dispatch_keys')}))
    return plan


def verify_plan():
    plan=json.loads((ROOT/'continuation_plan.json').read_bytes())
    for rel,h in plan['source_hashes'].items():
        if sha256((old.ROOT/rel).read_bytes()).hexdigest()!=h:raise ValueError('Continuation source changed: '+rel)
    m=json.loads((PARENT/'manifest.json').read_bytes());parent=segment_inventory(PARENT,m)
    if sorted(parent['intents'])!=plan['excluded_dispatch_keys'] or parent['pending']:
        raise ValueError('Parent dispatch inventory changed')
    if plan['design_hash']!=m['design_hash']:raise ValueError('Design mismatch')
    return m,plan


async def execute(root,m,client,parent_root):
    root.mkdir(parents=True,exist_ok=True)
    _,existing,_=old.inventory(root,m)
    parent=segment_inventory(parent_root,m)
    rows=list(parent['rows']);d=m['design']
    schedule=[j for j in old.jobs(d) if j[0] not in parent['intents']]
    if existing or any((root/'dispatches').rglob('*.json')):raise ValueError('Existing attempts; no automatic resume')
    if len({j[3] for j in schedule})!=len(schedule):raise ValueError('Seed collision')
    spent=parent['known']+parent['unknown'];sink=ValiditySink(root/'records')
    progress_design=dict(d,prior_accounted_usd=d['prior_accounted_usd']+parent['unknown'])
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
            checkpoint(root,rows,progress_design,'BUDGET_STOP');return 'BUDGET_STOP'
        for key,c,_,_ in batch:save_new(root/'dispatches'/(key+'.json'),old.intent(key,c,m))
        new=await asyncio.gather(*(one(j) for j in batch));rows.extend(new)
        # Unknown usage causes a stop; its full dispatched bound remains in the final ledger.
        spent+=sum(old.base.cost(r) or 0 for r in new)
        if any(r['terminal_failure'] for r in new):checkpoint(root,rows,progress_design,'TECHNICAL_STOP');return 'TECHNICAL_STOP'
        if len(rows)%30==0 or len(rows)-len(parent['rows']) in (3,len(schedule)):
            checkpoint(root,rows,progress_design,'RUNNING' if len(rows)<d['planned_calls'] else 'COLLECTED')
            print(f"{len(rows)}/{d['planned_calls']}; new cost ${spent:.5f}; cumulative ${spent+d['prior_accounted_usd']:.5f}",flush=True)
    return 'COLLECTED'


def finish(m,reason):
    parent=segment_inventory(PARENT,m);child=segment_inventory(ROOT,m)
    if set(parent['intents']) & set(child['intents']):raise ValueError('Repeated parent request')
    rows=parent['rows']+child['rows']
    ids=[r['api_call_id'] for r in rows if r['api_call_id']]
    if len(ids)!=len(set(ids)):raise ValueError('Repeated provider ID')
    known=parent['known']+child['known'];unknown=parent['unknown']+child['unknown']
    ledger={'status':reason,'n_parent_records':len(parent['rows']),'n_segment_records':len(child['rows']),
        'n_records':len(rows),'planned':m['design']['planned_calls'],
        'known_followup_cost_usd':known,'unknown_followup_reserved_usd':unknown,
        'pending_requests':parent['pending']+child['pending'],
        'total_accounted_usd':m['design']['prior_accounted_usd']+known+unknown,'cap_usd':25,
        'provider_balance_verified':False}
    if ledger['total_accounted_usd']>25+1e-8:raise ValueError('Cap exceeded')
    save_new(ROOT/'budget_ledger.json',ledger)
    result=original.assess(rows,m)
    result_path=ROOT/'analysis'/f'result_{digest(result)[:16]}.json';save_new(result_path,result)
    if original.assess(rows,m)!=result:raise ValueError('Recomputation differs')
    text=['# All-ten continuation assessment','',
        f"Status: {reason}. {len(rows):,}/{m['design']['planned_calls']:,} recorded across two execution segments.",
        f"Parse invalid (including API failures): {result['n_parse_invalid']}; terminal failures: {result['n_terminal_failures']}.",
        'All original failures remain. Allocation completion is distinct from valid-data completeness. Phase 1.5 remains open; Phase 2 held.',
        '', 'Same neutral configuration, 50 backgrounds (25 gradients), one response per condition, seeds 20261020/20261021/20261022.',
        'Model, exact messages, request seeds, temperature and analysis are the original frozen design. The interruption introduces a disclosed time segment.',
        '', '| Parameter | Complete wording cells /3 | Equivalent wording cells /3 |', '|---|---|---|']
    for p in m['design']['params']:
        cells=[w for w in result['wording_analysis'] if w['parameter']==p]
        text.append(f"| {p} | {sum(w['complete'] for w in cells)} | {sum(w['all_pairs_equivalent'] for w in cells)} |")
    text+=['',f"Total accounted ${ledger['total_accounted_usd']:.6f} / $25, including all unknown bounds.",
        f"[Full frozen analysis, all curves, contrasts and intervals](analysis/{result_path.name}).",
        'Recovery evidence remains the separate prior-cohort 200-item audit. No original gate pass is inferred.',
        'Frozen sources and both segment inventories verified; statistics recomputed. Raw archives remain separate; no off-device backup claimed.','']
    (ROOT/'STATUS.md').write_text('\n'.join(text),encoding='utf-8')
    save_new(ROOT/'analysis/verification.json',{'raw_provenance_verified':True,'disjoint_dispatches':True,
        'unique_provider_ids':len(ids),'recomputed_analysis':True,'result_sha256':sha256(result_path.read_bytes()).hexdigest()})
    print(json.dumps(ledger),flush=True)


def main():
    p=argparse.ArgumentParser();p.add_argument('--prepare-only',action='store_true');p.add_argument('--yes',action='store_true');a=p.parse_args()
    if a.prepare_only:prepare();return
    if not a.yes or not os.environ.get('OPENAI_API_KEY'):p.error('Need --yes and configured key')
    m,plan=verify_plan()
    from openai import AsyncOpenAI
    import msvcrt
    async def work():
        async with AsyncOpenAI(base_url='https://api.openai.com/v1',max_retries=0,timeout=180) as sdk:
            client=old.base.SingleAttemptOpenAI(old.base.MODEL,concurrency=3,max_retries=1,timeout_s=180);client._client=sdk
            return await execute(ROOT,m,client,PARENT)
    with (old.ROOT/'output/all_ten_followup.lock').open('a+b') as lock:
        lock.write(b'0');lock.flush();lock.seek(0);msvcrt.locking(lock.fileno(),msvcrt.LK_NBLCK,1)
        # Refuse repeated entry before finalization can touch an existing archive.
        if any((ROOT/'records').rglob('*.json')) or any((ROOT/'dispatches').rglob('*.json')):
            raise ValueError('Existing segment attempts; no automatic resume')
        reason='UNEXPECTED_STOP'
        try:reason=asyncio.run(work())
        finally:
            try:finish(m,reason)
            finally:old.archive_support.archive(ROOT,m)


if __name__=='__main__':main()
