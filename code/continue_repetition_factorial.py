"""Preserve a timeout and collect only the approved experiment's unsent requests."""
import argparse
import asyncio
from hashlib import sha256
import json
import os
from pathlib import Path
import zipfile

import run_validity_repetition_factorial as probe
from run_validity_continuation import preserve
from run_validity_claude import save_new

base=probe.base


def prepare(source,target):
    source=source.resolve();target=target.resolve()
    if source==target or source in target.parents or target in source.parents:raise ValueError('Separate roots required')
    m=json.loads((source/'manifest.json').read_bytes());planned,rows,seen=base.inventory(source,m)
    failed=[r for r in rows if r['terminal_failure']]
    if len(failed)!=1 or failed[0]['error_message']!='TimeoutError: ' or failed[0]['attempts']!=1:
        raise ValueError('This continuation permits only one diagnosed, preserved timeout')
    intents=[json.loads(p.read_bytes()) for p in (source/'dispatches').rglob('*.json')]
    if len(intents)!=len(rows) or {i['record_key'] for i in intents}!=seen:raise ValueError('Unresolved intents')
    if any(i!=base.dispatch_intent(i['record_key'],planned[i['record_key']][0],m) for i in intents):raise ValueError('Reservation mismatch')
    raw={name:(source/name).read_bytes() for name in ('manifest.json','dispatch_authorization.json','dispatch_approved.json')}
    if (source/'failures.jsonl').exists():raw['failures.jsonl']=(source/'failures.jsonl').read_bytes()
    for key in seen:
        for folder in ('records','dispatches'):
            name=folder+'/'+key+'.json';raw[name]=(source/name).read_bytes()
    ledger={'source_root':str(source),'design_hash':m['design_hash'],'source_files_sha256':{k:sha256(v).hexdigest() for k,v in raw.items()},
            'preserved_timeout_keys':[r['record_key'] for r in failed],'preserved_record_count':len(rows),
            'planned_new_requests':len(planned)-len(rows),'total_attempt_slots':len(planned),
            'continuation_code_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
            'rule':'Manual continuation after diagnosing a transport timeout. No failed slot is retried. All parent bytes preserved; same messages/seeds/model/count/cap. Original screen-invalid-on-API-failure rule remains.'}
    save_new(target/'continuation.json',ledger)
    for name,data in raw.items():preserve(target/name,data)
    verify_parent(target,m)
    print(json.dumps({'saved':len(rows),'new_requests':ledger['planned_new_requests'],'timeout_retries':0,'total_cap':m['design']['spending_ceiling_usd']}))
    return m


def verify_parent(root,m):
    ledger=json.loads((root/'continuation.json').read_bytes())
    if ledger['design_hash']!=m['design_hash'] or ledger['continuation_code_sha256']!=sha256(Path(__file__).read_bytes()).hexdigest():raise ValueError('Continuation changed')
    source=Path(ledger['source_root'])
    for name,h in ledger['source_files_sha256'].items():
        if sha256((source/name).read_bytes()).hexdigest()!=h or (source/name).read_bytes()!=(root/name).read_bytes():raise ValueError('Parent data changed')
    return ledger


async def execute(root,m,client):
    ledger=verify_parent(root,m);planned,rows,seen=base.inventory(root,m);d=m['design']
    allowed=set(ledger['preserved_timeout_keys'])
    if {r['record_key'] for r in rows if r['terminal_failure']}!=allowed:raise ValueError('New failure requires another review; cannot resume')
    intents=[json.loads(p.read_bytes()) for p in (root/'dispatches').rglob('*.json')]
    if len(intents)!=len(rows) or {i['record_key'] for i in intents}!=seen:raise ValueError('Unresolved intent; no retry')
    if any(i!=base.dispatch_intent(i['record_key'],planned[i['record_key']][0],m) for i in intents):raise ValueError('Reservation mismatch')
    reserved=sum(i['reserved_usd'] for i in intents)
    pending=[j for j in base.jobs(d) if j[0] not in seen]
    sink=base.ValiditySink(root/'records')
    async def one(job):
        key,c,k,seed=job
        if key in allowed:raise ValueError('Cannot retry preserved timeout')
        result=await client.complete([base.Message(**v) for v in c['messages']],temperature=d['temperature'],max_tokens=d['max_tokens'],seed=seed)
        decision,parse=base.parse_decision(result.text,tuple(c['labels']))
        mismatch=bool(result.ok and (result.model_version!=base.MODEL or result.provider!='openai'))
        r={'record_key':key,'design_hash':m['design_hash'],'arm':c['arm'],'wording':c['wording'],'problem_id':'S3',
           'agent_parameters':c['profile'],'call_index':k,'seed':seed,'schedule_seed':d['seed'],'timestamp_utc':result.timestamp_utc,
           'provider':result.provider,'model_version':result.model_version,'model_version_mismatch':mismatch,
           'api_call_id':result.api_call_id,'attempts':result.attempts,'request_messages':result.request_messages,
           'response_payload':result.raw_response,'raw_response':result.text,'parsed_decision':decision,
           'parsed_reasoning':base.parse_reasoning(result.text),'error_message':result.error,
           'parse_status':'failed_api' if result.error else 'model_mismatch' if mismatch else parse}
        cost=base.cost(r)
        r['terminal_failure']=bool(result.error or mismatch or cost is None or cost>base.reserve(c,d)
                                   or result.attempts!=1 or not result.api_call_id or result.request_messages!=c['messages'])
        r['record_hash']=base.digest(r);sink.write(key,r)
        if r['terminal_failure']:sink.write_failure({'record_key':key,'error':result.error,'terminal_failure':True})
        return r
    for start in range(0,len(pending),3):
        batch=pending[start:start+3];bound=sum(base.reserve(c,d) for _,c,_,_ in batch)
        if reserved+bound>d['spending_ceiling_usd']:raise RuntimeError('Spending guard')
        for key,c,_,_ in batch:save_new(root/'dispatches'/(key+'.json'),base.dispatch_intent(key,c,m))
        reserved+=bound;new=await asyncio.gather(*(one(j) for j in batch));rows.extend(new)
        if len(rows)%15==0:print(f"{len(rows)}/720 slots; known token estimate ${sum(base.cost(r) or 0 for r in rows):.5f}; timeout reservation retained",flush=True)
        if any(r['terminal_failure'] for r in new):raise RuntimeError('New failure preserved; stop')


def report(root,m):
    ledger=verify_parent(root,m);planned,rows,seen=base.inventory(root,m)
    if len(rows)!=720 or seen!=set(planned):raise ValueError('Incomplete slots')
    failure=set(ledger['preserved_timeout_keys']);good=[r for r in rows if r['record_key'] not in failure]
    if any(r['terminal_failure'] or r['model_version']!=base.MODEL or r['attempts']!=1 for r in good):raise ValueError('Additional failure')
    ids=[r['api_call_id'] for r in good]
    if len(set(ids))!=len(good) or any(not i or i.startswith('mock-') for i in ids):raise ValueError('Invalid IDs')
    intents=[json.loads(p.read_bytes()) for p in (root/'dispatches').rglob('*.json')]
    if len(intents)!=720 or {i['record_key'] for i in intents}!=seen:raise ValueError('Incomplete intents')
    if any(i!=base.dispatch_intent(i['record_key'],planned[i['record_key']][0],m) for i in intents):raise ValueError('Reservation mismatch')
    reserved=sum(i['reserved_usd'] for i in intents)
    if reserved>m['design']['spending_ceiling_usd']:raise ValueError('Cap exceeded')
    backup=json.loads((root/'local_backup.json').read_bytes());archive=Path(backup['path'])
    if sha256(archive.read_bytes()).hexdigest()!=backup['sha256']:raise ValueError('ZIP hash mismatch')
    with zipfile.ZipFile(archive) as z:
        if z.testzip():raise ValueError('ZIP corruption')
        for key in seen:
            name='records/'+key+'.json'
            if z.read(name)!=(root/name).read_bytes():raise ValueError('ZIP bytes mismatch')
    r=probe.score(root,m);unknown=sum(base.reserve(planned[k][0],m['design']) for k in failure)
    cost=r['recorded_token_estimate_usd'];prior=m['design']['prior_settled_token_estimate_usd']
    save_new(root/'analysis/verification.json',{'design_hash':m['design_hash'],'slots':720,'known_responses':len(good),'preserved_timeouts':1,
             'unique_known_api_ids':len(set(ids)),'unique_requested_seeds':len({r['seed'] for r in rows}),'parent_bytes_and_raw_zip_verified':True,
             'all_reservations_verified':True,'reserved_usd':reserved,'scientific_status':r['status']})
    save_new(root/'budget_ledger.json',{'known_current_token_estimate_usd':cost,'unknown_timeout_reserved_usd':unknown,
             'cumulative_known_token_estimate_usd':prior+cost,'cumulative_conservative_charge_usd':prior+cost+unknown,
             'remaining_original_allowance_conservative_usd':9-prior-cost-unknown,'pending_requests':0,'unresolved_usage_records':1,
             'timeout_retried':False,'provider_balance_verified':False,'automatic_expansion':False})
    data=('# Completed allocation with preserved timeout\n\n'
          f"Scientific status: **{r['status']}** under the unchanged API-failure rule.\n"
          f"720 attempt slots; {r['n_valid']} valid responses; one preserved timeout, never retried.\n"
          f"Known current token estimate ${cost:.6f}; add up to ${unknown:.6f} reserved for unknown timeout usage.\n\n"
          'This is diagnostic data, not a protocol pass. Contrasts retain the unknown outcome envelope.\n'
          'The paused collection resumed only previously unsent requests in its original schedule.\n\n'
          '```json\n'+json.dumps({'cells':r['cells'],'primary':r['primary_verbal_average_difference'],
                                  'endpoints':r['endpoint_effects'],'interactions':r['endpoint_effect_interactions']},indent=2)+'\n```\n').encode()
    preserve(root/'analysis/TIMEOUT_COLLECTION_REPORT.md',data)
    print(json.dumps({'status':r['status'],'valid':r['n_valid'],'known_cost':cost,'unknown_usage_reserved':unknown}))


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--source',type=Path,required=True);p.add_argument('--target',type=Path,required=True)
    p.add_argument('--prepare-only',action='store_true');p.add_argument('--yes',action='store_true');a=p.parse_args();root=a.target.resolve()
    if a.prepare_only:prepare(a.source,root);return
    if not a.yes or not os.environ.get('OPENAI_API_KEY'):p.error('Need --yes and key')
    m=json.loads((root/'manifest.json').read_bytes());verify_parent(root,m);probe.check_authorization(root,m)
    import msvcrt
    from openai import AsyncOpenAI
    logs=probe.ROOT/'output'/root.name;logs.mkdir(parents=True,exist_ok=True)
    async def run():
        client=base.SingleAttemptOpenAI(base.MODEL,concurrency=3,max_retries=1,timeout_s=90)
        async with AsyncOpenAI(base_url='https://api.openai.com/v1',max_retries=0,timeout=90) as sdk:
            client._client=sdk;await execute(root,m,client)
    with (logs/'execution.lock').open('a+b') as lock:
        lock.write(b'0');lock.flush();lock.seek(0);msvcrt.locking(lock.fileno(),msvcrt.LK_NBLCK,1)
        try:asyncio.run(run())
        finally:probe.score(root,m);base.archive(root,m)
        report(root,m)


if __name__=='__main__':main()
