"""Third frozen execution segment; preserve both prior segments and unresolved intents."""
import argparse
import asyncio
from hashlib import sha256
import json
import os
from pathlib import Path
from datetime import datetime, timezone
import run_all_ten_continuation as previous
from run_all_ten_continuation import original, old, save_new, digest, ValiditySink, checkpoint, segment_inventory

PARENTS=(original.ROOT,previous.ROOT)
ROOT=old.BASE/'all_ten_followup_20260912_segment3'


def combined_inventory(roots,m):
    rows=[];intents={};known=0.;unknown=0.;pending=0
    for root in roots:
        part=segment_inventory(root,m)
        if set(intents)&set(part['intents']):raise ValueError('Overlapping segment dispatches')
        intents.update(part['intents']);rows.extend(part['rows'])
        known+=part['known'];unknown+=part['unknown'];pending+=part['pending']
    ids=[r['api_call_id'] for r in rows if r['api_call_id']]
    if len(ids)!=len(set(ids)):raise ValueError('Duplicate provider ID across segments')
    return dict(rows=rows,intents=intents,known=known,unknown=unknown,pending=pending)


def prepare():
    m=json.loads((PARENTS[0]/'manifest.json').read_bytes());parent=combined_inventory(PARENTS,m)
    ledger=json.loads((PARENTS[-1]/'budget_ledger.json').read_bytes())
    accounted=m['design']['prior_accounted_usd']+parent['known']+parent['unknown']
    if abs(accounted-ledger['total_accounted_usd'])>1e-9 or parent['pending']!=ledger['pending_requests']:
        raise ValueError('Parent ledger mismatch')
    schedule=list(old.jobs(m['design']))
    if set(parent['intents'])!={j[0] for j in schedule[:len(parent['intents'])]}:raise ValueError('Parent is not exact schedule prefix')
    paths=[PARENTS[0]/'manifest.json',Path(__file__),ROOT/'PROTOCOL.md',old.ROOT/'tests/test_all_ten_segment3.py',Path(previous.__file__)]
    for root in PARENTS:paths.extend([root/'budget_ledger.json',root/'local_backup.json'])
    plan={'design_hash':m['design_hash'],'parents':[p.relative_to(old.ROOT).as_posix() for p in PARENTS],
        'excluded_dispatch_keys':sorted(parent['intents']),'parent_records':len(parent['rows']),
        'parent_unresolved':parent['pending'],'remaining_calls':len(schedule)-len(parent['intents']),
        'prior_accounted_including_parents_usd':accounted,'cap_usd':25,
        'source_hashes':{p.relative_to(old.ROOT).as_posix():sha256(p.read_bytes()).hexdigest() for p in paths},
        'basis':'Researcher explicitly instructed continue after the verified interruption; unchanged fixed design and existing $25 total cap. Unresolved dispatches are never retried.'}
    save_new(ROOT/'continuation_plan.json',plan)
    print(json.dumps({k:v for k,v in plan.items() if k not in ('excluded_dispatch_keys','source_hashes')}),flush=True)
    return plan


def verify_plan():
    plan=json.loads((ROOT/'continuation_plan.json').read_bytes())
    for rel,h in plan['source_hashes'].items():
        if sha256((old.ROOT/rel).read_bytes()).hexdigest()!=h:raise ValueError('Frozen continuation source changed: '+rel)
    m=json.loads((PARENTS[0]/'manifest.json').read_bytes());parent=combined_inventory(PARENTS,m)
    if plan['design_hash']!=m['design_hash'] or sorted(parent['intents'])!=plan['excluded_dispatch_keys']:
        raise ValueError('Frozen plan or parent inventory differs')
    if len(parent['rows'])!=plan['parent_records'] or parent['pending']!=plan['parent_unresolved']:
        raise ValueError('Parent outcomes changed')
    accounted=m['design']['prior_accounted_usd']+parent['known']+parent['unknown']
    if abs(accounted-plan['prior_accounted_including_parents_usd'])>1e-9:raise ValueError('Prior budget differs')
    return m,plan,parent


async def execute(root,m,client,parent_roots, verified_parent=None):
    root.mkdir(parents=True,exist_ok=True)
    _,existing,_=old.inventory(root,m)
    parent=verified_parent if verified_parent is not None else combined_inventory(parent_roots,m)
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
            checkpoint(root,rows,progress_design,'RUNNING' if len(rows)-len(parent['rows'])<len(schedule) else 'DISPATCH_COMPLETE_WITH_MISSING_RESPONSES')
            print(f"{len(rows)}/{d['planned_calls']}; new cost ${spent:.5f}; cumulative ${spent+d['prior_accounted_usd']:.5f}",flush=True)
    return 'DISPATCH_COMPLETE_WITH_MISSING_RESPONSES' if parent['pending'] else 'COLLECTED'


def finish(m,reason):
    combined=combined_inventory((*PARENTS,ROOT),m);rows=combined['rows']
    ledger={'status':reason,'n_records':len(rows),'n_valid':sum(r['parse_status']=='ok' and not r['terminal_failure'] for r in rows),
        'planned':m['design']['planned_calls'],'n_dispatched':len(combined['intents']),
        'never_dispatched':m['design']['planned_calls']-len(combined['intents']),
        'known_followup_cost_usd':combined['known'],'unknown_followup_reserved_usd':combined['unknown'],
        'pending_requests':combined['pending'],
        'total_accounted_usd':m['design']['prior_accounted_usd']+combined['known']+combined['unknown'],
        'cap_usd':25,'provider_balance_verified':False}
    if ledger['total_accounted_usd']>25+1e-8:raise ValueError('Budget exceeded')
    save_new(ROOT/'budget_ledger.json',ledger)
    result=original.assess(rows,m);path=ROOT/'analysis'/f'result_{digest(result)[:16]}.json';save_new(path,result)
    if original.assess(rows,m)!=result:raise ValueError('Recomputed result differs')
    ids=[r['api_call_id'] for r in rows if r['api_call_id']]
    save_new(ROOT/'analysis/verification.json',{'disjoint_intents':True,'raw_provenance_verified':True,
        'unique_provider_ids':len(ids),'result_recomputed':True,'result_sha256':sha256(path.read_bytes()).hexdigest()})
    lines=['# All-ten follow-up: three execution segments','',f"Status: {reason}.",
        f"{len(rows):,}/{m['design']['planned_calls']:,} saved responses; {ledger['n_valid']:,} valid; {combined['pending']} unresolved dispatches; {ledger['never_dispatched']} never dispatched.",
        'Full dispatch allocation is distinct from complete valid data. Failures and unresolved calls were not replaced. Phase 1.5 remains open; Phase 2 is held.',
        '', 'Neutral configuration; 50 sampled backgrounds (first25 for gradients); one response per condition. Original draw/schedule/analysis seeds20261020/20261021/20261022.',
        'Original frozen model, messages, request seeds, temperature and analysis retained across the disclosed time interruptions. Prior200-item recovery audit remains a separate cohort.',
        '', '| Parameter | Complete wording cells /3 | Equivalent cells /3 |','|---|---|---|']
    for p in m['design']['params']:
        words=[w for w in result['wording_analysis'] if w['parameter']==p]
        lines.append(f"| {p} | {sum(w['complete'] for w in words)} | {sum(w['all_pairs_equivalent'] for w in words)} |")
    lines+=['',f"Total accounted ${ledger['total_accounted_usd']:.6f} / $25, retaining all unknown bounds.",
        f"[Full unchanged analysis, effect estimates and confidence intervals](analysis/{path.name}).",
        'Incomplete comparisons retain their original restrictions. Wording equivalence concerns profile-average rates, not each profile. No new original-gate pass is inferred.',
        'All three raw inventories were verified and statistics recomputed. Separate raw archives remain on this computer; no off-device backup claimed.','']
    (ROOT/'STATUS.md').write_text('\n'.join(lines),encoding='utf-8')
    print(json.dumps(ledger),flush=True)


def main():
    p=argparse.ArgumentParser();p.add_argument('--prepare-only',action='store_true');p.add_argument('--yes',action='store_true');a=p.parse_args()
    if a.prepare_only:prepare();return
    if not a.yes or not os.environ.get('OPENAI_API_KEY'):p.error('Need --yes and configured key')
    import msvcrt
    from openai import AsyncOpenAI
    with (old.ROOT/'output/all_ten_followup.lock').open('a+b') as lock:
        lock.write(b'0');lock.flush();lock.seek(0);msvcrt.locking(lock.fileno(),msvcrt.LK_NBLCK,1)
        if any((ROOT/'records').rglob('*.json')) or any((ROOT/'dispatches').rglob('*.json')):
            raise ValueError('Existing segment attempts; no automatic resume')
        save_new(ROOT/'run_process.json',{'pid':os.getpid(),'started_utc':datetime.now(timezone.utc).isoformat(),
            'state':'VERIFYING_PARENTS','note':'Check this PID plus fresh progress or terminal ledger; a stale RUNNING checkpoint is insufficient.'})
        print('Verifying frozen parents before any dispatch.',flush=True)
        m,plan,parent=verify_plan()
        print(f"Verified; {plan['remaining_calls']} unattempted requests; prior accounted ${plan['prior_accounted_including_parents_usd']:.6f}.",flush=True)
        async def work():
            async with AsyncOpenAI(base_url='https://api.openai.com/v1',max_retries=0,timeout=180) as sdk:
                client=old.base.SingleAttemptOpenAI(old.base.MODEL,concurrency=3,max_retries=1,timeout_s=180);client._client=sdk
                return await execute(ROOT,m,client,PARENTS,verified_parent=parent)
        reason='UNEXPECTED_STOP'
        try:reason=asyncio.run(work())
        finally:
            try:finish(m,reason)
            finally:old.archive_support.archive(ROOT,m)


if __name__=='__main__':main()
