"""Recover only undispatched slots after connection failures; never replace failures."""
import argparse
import asyncio
import hashlib
import json
import os
from pathlib import Path
import shutil
import zipfile

from engine.llm_client import LLMClient,Message,utc_now_iso
from engine.parsing import parse_decision,parse_reasoning
from engine.seeding import derive_seed
from engine.validity_sweep import ValiditySink,digest,freeze
from prepare_validity_axis_revision import ROOT
from run_validity_claude import save_new
import run_validity_axis_revision as core


def archive_snapshot(root):
    m=json.loads((root/'manifest.json').read_text(encoding='utf-8'))
    rows=list(ValiditySink(root/'records').read_all())
    inventory={'design_hash':m['design_hash'],'n_records':len(rows),
        'n_expected':m['design']['planned_calls'],'n_missing':m['design']['planned_calls']-len(rows),
        'n_invalid':sum(r['parse_status']!='ok' for r in rows),
        'n_api_failures':sum(bool(r.get('error_message')) for r in rows),
        'models_returned':sorted({r['model_version'] for r in rows if r.get('model_version')}),
        'n_missing_model_identity':sum(not r.get('model_version') for r in rows),
        'index':[{'record_key':r['record_key'],'record_hash':r['record_hash']} for r in rows]}
    save_new(root/'record_checksums.json',inventory)
    usage={'input_tokens':0,'output_tokens':0,'cached_input_tokens':0}
    for r in rows:
        u=(r.get('response_payload') or {}).get('usage',{})
        usage['input_tokens']+=u.get('prompt_tokens',0);usage['output_tokens']+=u.get('completion_tokens',0)
        usage['cached_input_tokens']+=u.get('prompt_tokens_details',{}).get('cached_tokens',0)
    save_new(root/'token_usage.json',usage)
    folder=ROOT/'output/validity_backups';folder.mkdir(parents=True,exist_ok=True)
    target=folder/f'{root.name}_{digest(inventory)[:16]}.zip'
    if not target.exists():
        with zipfile.ZipFile(target,'x',compression=zipfile.ZIP_DEFLATED) as z:
            for p in sorted(root.rglob('*')):
                if p.is_file(): z.write(p,p.relative_to(root).as_posix())
    with zipfile.ZipFile(target) as z:
        if z.testzip(): raise ValueError('ZIP integrity failure')
    save_new(root/'local_backup.json',{'path':str(target),'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),
        'note':'Same-computer snapshot; may include preserved failures and missing slots. See inventory. Not off-device storage.'})


def prepare(source,root):
    m=json.loads((source/'manifest.json').read_text(encoding='utf-8'));d=m['design']
    if digest(d)!=m['design_hash']: raise ValueError('Core design damaged')
    core.check_approval(m,source/'review_approved.json')
    rows=list(ValiditySink(source/'records').read_all());planned=core.jobs(d);expected={k for k,_,_ in planned}
    seen={r['record_key'] for r in rows}
    if len(seen)!=len(rows) or not seen<=expected: raise ValueError('Invalid source allocation')
    if any(r['design_hash']!=m['design_hash'] or r.get('model_version_mismatch') for r in rows):
        raise ValueError('Source model/design changed; cannot recover as the same protocol')
    failures=[r for r in rows if r.get('error_message')]
    if not failures or any(not r['error_message'].startswith('APIConnectionError:') for r in failures):
        raise ValueError('This recovery is limited to the reviewed connection-error condition')
    allocation=[key for key,_,_ in planned if key not in seen]
    if not allocation: raise ValueError('No undispatched slots')
    c={'phase':d['phase'],'experiment':'axis_instruction_connection_continuation',
        'source_root':str(source.resolve()),'core_design_hash':m['design_hash'],
        'planned_calls':len(allocation),'allocation':allocation,
        'reserved_source_records':{r['record_key']:r['record_hash'] for r in rows},
        'preserved_failures':[r['record_key'] for r in failures],
        'prior_recorded_cost_usd':sum(core.cost(r) for r in rows),
        'total_pilot_dispatch_guard_usd':d['collection']['spending_ceiling_usd'],
        'source_hashes':{**d['source_hashes'],
            'code/run_validity_axis_continuation.py':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},
        'rule':'Collect only never-dispatched original slots; retain all failures; original prompts, settings, seeds, total N and analysis unchanged.'}
    cm=freeze(root/'manifest.json',c)
    save_new(root/'authorization.json',{'source_approval_sha256':hashlib.sha256((source/'review_approved.json').read_bytes()).hexdigest(),
        'basis':'Existing exact study approval; technical recovery collects only remaining authorised slots. No failed request is repeated.'})
    return cm


async def execute(cm,client,root):
    cd=cm['design'];source=Path(cd['source_root'])
    if digest(cd)!=cm['design_hash']: raise ValueError('Continuation manifest damaged')
    for name,h in cd['source_hashes'].items():
        if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=h: raise ValueError('Frozen source changed')
    m=json.loads((source/'manifest.json').read_text(encoding='utf-8'));d=m['design']
    if m['design_hash']!=cd['core_design_hash'] or digest(d)!=m['design_hash']: raise ValueError('Core changed')
    core.check_approval(m,source/'review_approved.json')
    originals=list(ValiditySink(source/'records').read_all())
    if {r['record_key']:r['record_hash'] for r in originals}!=cd['reserved_source_records']:
        raise ValueError('Original snapshot changed')
    allowed=set(cd['allocation']);sink=ValiditySink(root/'records');existing=list(sink.read_all())
    seen={r['record_key'] for r in existing}
    if len(seen)!=len(existing) or not seen<=allowed or seen&cd['reserved_source_records'].keys(): raise ValueError('Invalid continuation keys')
    if any(r.get('error_message') or r.get('model_version_mismatch') or r.get('continuation_manifest_hash')!=cm['design_hash'] or r['design_hash']!=m['design_hash'] for r in existing):
        raise ValueError('Continuation failure or mismatched provenance; cannot resume in place')
    pending=[job for job in core.jobs(d) if job[0] in allowed-seen]
    spent=cd['prior_recorded_cost_usd']+sum(core.cost(r) for r in existing)
    async def one(job):
        key,c,k=job;seed=derive_seed(d['seed'],c['stage'],c['arm'],c['wording'],c['problem'],c['value'],k)
        result=await client.complete([Message(**v) for v in c['messages']],temperature=d['temperature'],max_tokens=d['max_tokens'],seed=seed)
        decision,parse=parse_decision(result.text,tuple(c['labels']))
        expected=d['model']+'-mock' if d['provider']=='mock' else d['model']
        mismatch=result.ok and result.model_version!=expected
        r={'schema_version':'1.0','phase':d['phase'],'experiment':d['experiment'],'design_hash':m['design_hash'],
            'continuation_manifest_hash':cm['design_hash'],'record_key':key,'stage':c['stage'],'arm':c['arm'],
            'wording':c['wording'],'variant':c['variant'],'swept_parameter':'PD','sweep_value':c['value'],
            'problem_id':c['problem'],'labels':c['labels'],'agent_parameters':c['profile'],'call_index':k,'seed':seed,
            'timestamp_utc':result.timestamp_utc,'provider':result.provider,'model_version':result.model_version,
            'model_version_mismatch':bool(mismatch),'api_call_id':result.api_call_id,'attempts':result.attempts,
            'request_messages':result.request_messages,'response_payload':result.raw_response,'raw_response':result.text,
            'parsed_decision':decision,'parsed_reasoning':parse_reasoning(result.text),
            'parse_status':'failed_api' if result.error else 'model_mismatch' if mismatch else parse,'error_message':result.error}
        r['record_hash']=digest(r);sink.write(key,r)
        if result.error or mismatch: sink.write_failure({'record_key':key,'error':result.error,'model_mismatch':bool(mismatch)})
        return r
    for start in range(0,len(pending),4):
        batch=pending[start:start+4]
        reserve=sum((sum(len(v['content'].encode('utf-8')) for v in c['messages'])+128)*.75/1e6+d['max_tokens']*4.5/1e6 for _,c,_ in batch)
        if spent+reserve>cd['total_pilot_dispatch_guard_usd']: raise RuntimeError('Combined pilot budget guard reached')
        rows=await asyncio.gather(*(one(job) for job in batch));spent+=sum(core.cost(r) for r in rows)
        count=len(existing)+start+len(batch)
        if start==0 or count%100==0 or count==cd['planned_calls']: print(f'Continuation {count}/{cd["planned_calls"]}; combined cost ${spent:.4f}',flush=True)
        if any(r['error_message'] or r['model_version_mismatch'] for r in rows): raise RuntimeError('New terminal failure preserved; continuation stopped')


def assemble(source,continuation,destination):
    m=json.loads((source/'manifest.json').read_text(encoding='utf-8'))
    cm=json.loads((continuation/'manifest.json').read_text(encoding='utf-8'))
    original=list(ValiditySink(source/'records').read_all());new=list(ValiditySink(continuation/'records').read_all())
    if len(new)!=cm['design']['planned_calls']: raise ValueError('Continuation is incomplete')
    if {r['record_key']:r['record_hash'] for r in original}!=cm['design']['reserved_source_records']:
        raise ValueError('Original records changed')
    keys=[r['record_key'] for r in original+new]
    if len(keys)!=len(set(keys)) or set(keys)!={k for k,_,_ in core.jobs(m['design'])}: raise ValueError('Allocation mismatch')
    save_new(destination/'manifest.json',m)
    save_new(destination/'collection_manifest.json',{'core_design_hash':m['design_hash'],'continuation_manifest_hash':cm['design_hash'],
        'source_root':str(source.resolve()),'continuation_root':str(continuation.resolve()),
        'n_original':len(original),'n_continuation':len(new),'n_failures_preserved':sum(bool(r.get('error_message')) for r in original+new),
        'note':'Byte-identical union of original planned slots; no historical study pooling, failure replacement or statistical override. Only archive writer handles null model identities.'})
    for name in [p.name for p in source.iterdir() if p.is_file() and p.name not in
            ('manifest.json','record_checksums.json','local_backup.json','token_usage.json')]:
        target=destination/name
        if target.exists():
            if target.read_bytes()!=(source/name).read_bytes(): raise ValueError('Existing assembly file differs')
        else: shutil.copyfile(source/name,target)
    for folder,rows in ((source,original),(continuation,new)):
        for r in rows:
            relative=Path('records')/(r['record_key']+'.json');target=(destination/relative).resolve()
            if not target.is_relative_to((destination/'records').resolve()): raise ValueError('Unsafe record path')
            data=(folder/relative).read_bytes();target.parent.mkdir(parents=True,exist_ok=True)
            if target.exists():
                if target.read_bytes()!=data: raise ValueError('Existing assembled record differs')
            else:
                with target.open('xb') as f:f.write(data)
    # Keep the frozen statistical scorer, including its terminal-failure flag.
    # The storage adapter alone permits a ZIP containing null model identities.
    previous=core.archive
    try:
        core.archive=archive_snapshot
        return core.score(destination,m)
    finally: core.archive=previous


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--source-root',type=Path,required=True)
    p.add_argument('--run-root',type=Path,required=True);p.add_argument('--prepare-only',action='store_true')
    p.add_argument('--assemble-to',type=Path);p.add_argument('--yes',action='store_true');a=p.parse_args()
    source=a.source_root.resolve();root=a.run_root.resolve()
    if a.prepare_only:
        cm=prepare(source,root);print(f'Prepared {cm["design"]["planned_calls"]} never-dispatched slots; no API calls.');return
    if a.assemble_to:
        assemble(source,root,a.assemble_to.resolve());return
    if not a.yes or not os.environ.get('OPENAI_API_KEY'):p.error('Need --yes and configured key')
    cm=json.loads((root/'manifest.json').read_text(encoding='utf-8'))
    if Path(cm['design']['source_root'])!=source: raise ValueError('Wrong source argument')
    import msvcrt
    logs=ROOT/'output'/root.name;logs.mkdir(parents=True,exist_ok=True)
    with (logs/'execution.lock').open('a+b') as lock:
        lock.write(b'0');lock.flush();lock.seek(0);msvcrt.locking(lock.fileno(),msvcrt.LK_NBLCK,1)
        def status(value): (logs/'status.json').write_text(json.dumps({'status':value,'timestamp_utc':utc_now_iso()},indent=2),encoding='utf-8')
        status('RUNNING')
        try:
            model=json.loads((source/'manifest.json').read_text(encoding='utf-8'))['design']['model']
            asyncio.run(execute(cm,LLMClient(model=model,concurrency=4),root));status('CONTINUATION_COLLECTED')
        except BaseException:status('STOPPED_WITH_ERROR');raise


if __name__=='__main__':main()
