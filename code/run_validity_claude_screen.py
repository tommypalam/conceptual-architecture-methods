"""Small Claude/provider screen using unchanged approved messages; no phase-pass claim."""
import argparse
import asyncio
import hashlib
import json
import logging
import os
from pathlib import Path
import random
import zipfile

import pandas as pd
from scipy.stats import beta
import utils
from engine.llm_client import LLMClient,Message,utc_now_iso
from engine.parsing import parse_decision,parse_reasoning
from engine.validity_analysis import wilson
from engine.validity_sweep import ValiditySink,digest,freeze
from run_validity_claude import save_new
import run_validity_axis_revision as original

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'experiments/phase1_5_encoding_validity/axis_instruction_20260910'
MODEL='claude-haiku-4-5-20251001'


def prepare(root):
    source=json.loads((SOURCE/'manifest.json').read_text(encoding='utf-8'))
    if digest(source['design'])!=source['design_hash']:raise ValueError('Source manifest damaged')
    original.check_approval(source,SOURCE/'review_approved.json')
    cells=[dict(c,n=20) for c in source['design']['cells'] if c['stage']=='equivalence' and c['arm']=='baseline']
    assert [c['wording'] for c in cells]==['canonical','paraphrase_1','paraphrase_2','paraphrase_3']
    hashes=dict(source['design']['source_hashes'])
    hashes['code/run_validity_claude_screen.py']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    return freeze(root/'manifest.json',{
        'phase':'phase1_5_encoding_validity','experiment':'claude_unchanged_prompt_gross_failure_screen',
        'model':MODEL,'configuration':'neutral','temperature':1.,'max_tokens':600,
        'seed':20260914,'seed_scope':'Schedule only; Anthropic requests use no seed',
        'planned_calls':80,'cells':cells,'source_design_hash':source['design_hash'],
        'source_approval_sha256':hashlib.sha256((SOURCE/'review_approved.json').read_bytes()).hexdigest(),
        'source_hashes':hashes,'spending_ceiling_usd':.75,
        'pricing':{'input_per_million':1.,'output_per_million':5.,
                   'source':'https://platform.claude.com/docs/en/about-claude/pricing','checked':'2026-09-11'},
        'analysis':'Primary P2 minus P3; two exact 97.5% binomial intervals give a conservative >=95% difference interval. Reject gross stability if wholly outside [-.10,.10]. Other rates descriptive. No equivalence/pass claim.',
        'collection':'20 shuffled four-wording blocks; concurrency 2; one transport attempt, SDK retries disabled; stop after active batch on any API/model error; reserve failures; no automatic expansion.',
        'limitations':'Selected familiar PD=.8/S3; model plus provider transport changes; Haiku generated prior paraphrases and is not an independent wording judge; historical OpenAI data not pooled or treated as concurrent controls.'})


def jobs(d):
    rng=random.Random(d['seed']);result=[]
    for k in range(1,21):
        block=list(d['cells']);rng.shuffle(block)
        result.extend((f'{c["wording"]}/call_{k:04d}',c,k) for c in block)
    return result


def cost(r):
    u=(r.get('response_payload') or {}).get('usage',{})
    return (u.get('input_tokens',0)+5*u.get('output_tokens',0))/1e6


def check(m):
    d=m['design']
    if digest(d)!=m['design_hash'] or d['model']!=MODEL:raise ValueError('Frozen design/model mismatch')
    for name,h in d['source_hashes'].items():
        if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=h:raise ValueError('Frozen source changed: '+name)
    source=json.loads((SOURCE/'manifest.json').read_text(encoding='utf-8'))
    if source['design_hash']!=d['source_design_hash']:raise ValueError('Source design changed')
    if hashlib.sha256((SOURCE/'review_approved.json').read_bytes()).hexdigest()!=d['source_approval_sha256']:
        raise ValueError('Source approval changed')
    original.check_approval(source,SOURCE/'review_approved.json')
    for c in d['cells']:
        old=next(v for v in source['design']['cells'] if v['stage']=='equivalence' and v['arm']=='baseline' and v['wording']==c['wording'])
        if {k:v for k,v in c.items() if k!='n'}!={k:v for k,v in old.items() if k!='n'}:
            raise ValueError('Original prompt/profile changed')


async def execute(root,m,client):
    check(m);d=m['design'];sink=ValiditySink(root/'records')
    planned={key:(c,k) for key,c,k in jobs(d)};rows=list(sink.read_all());seen={r['record_key'] for r in rows}
    if len(seen)!=len(rows) or not seen<=planned.keys():raise ValueError('Unexpected records')
    for r in rows:
        c,k=planned[r['record_key']]
        if r['design_hash']!=m['design_hash'] or r['request_messages']!=c['messages'] or r['agent_parameters']!=c['profile']:
            raise ValueError('Existing provenance mismatch')
        if r.get('error_message') or r.get('model_version_mismatch'):raise ValueError('Preserved terminal failure; no in-place resume')
    pending=[job for job in jobs(d) if job[0] not in seen];spent=sum(cost(r) for r in rows)
    async def one(job):
        key,c,k=job
        result=await client.complete([Message(**v) for v in c['messages']],temperature=d['temperature'],max_tokens=d['max_tokens'],seed=None)
        decision,parse=parse_decision(result.text,tuple(c['labels']))
        mismatch=bool(result.ok and result.model_version!=d['model'])
        r={'record_key':key,'design_hash':m['design_hash'],'wording':c['wording'],'call_index':k,
           'agent_parameters':c['profile'],'problem_id':c['problem'],'labels':c['labels'],
           'schedule_seed':d['seed'],'seed':None,'timestamp_utc':result.timestamp_utc,
           'provider':result.provider,'model_version':result.model_version,'model_version_mismatch':mismatch,
           'api_call_id':result.api_call_id,'attempts':result.attempts,'request_messages':result.request_messages,
           'response_payload':result.raw_response,'raw_response':result.text,'parsed_decision':decision,
           'parsed_reasoning':parse_reasoning(result.text),'error_message':result.error,
           'parse_status':'failed_api' if result.error else 'model_mismatch' if mismatch else parse}
        r['record_hash']=digest(r);sink.write(key,r)
        if result.error or mismatch:sink.write_failure({'record_key':key,'error':result.error,'model_mismatch':mismatch})
        return r
    for start in range(0,len(pending),2):
        batch=pending[start:start+2]
        reserve=sum((sum(len(v['content'].encode('utf-8')) for v in c['messages'])+256+5*d['max_tokens'])/1e6 for _,c,_ in batch)
        if spent+reserve>d['spending_ceiling_usd']:raise RuntimeError('Spending guard reached before dispatch')
        new=await asyncio.gather(*(one(job) for job in batch));spent+=sum(cost(r) for r in new)
        print(f'{len(rows)+start+len(batch)}/80; recorded cost ${spent:.5f}',flush=True)
        if any(r['error_message'] or r['model_version_mismatch'] for r in new):raise RuntimeError('Terminal failure preserved; collection stopped')


def exact(k,n,unknown=0):
    # Two 97.5% intervals cover the prespecified difference with >=95% coverage.
    return [0. if k==0 else float(beta.ppf(.0125,k,n-k+1)),
            1. if k+unknown==n else float(beta.ppf(.9875,k+unknown+1,n-k-unknown))]


def score(root,m):
    check(m);d=m['design'];rows=list(ValiditySink(root/'records').read_all())
    expected={key:c for key,c,_ in jobs(d)}
    if len({r['record_key'] for r in rows})!=len(rows):raise ValueError('Duplicate records')
    for r in rows:
        if r['record_key'] not in expected or r['design_hash']!=m['design_hash'] or r['request_messages']!=expected[r['record_key']]['messages']:
            raise ValueError('Record/request mismatch')
    cells=[]
    for c in d['cells']:
        group=[r for r in rows if r['wording']==c['wording']]
        valid=[r for r in group if r['parse_status']=='ok' and r['parsed_decision'] in c['labels']]
        k=sum(r['parsed_decision']=='ADOPT' for r in valid)
        cells.append({'wording':c['wording'],'n_expected':20,'n_recorded':len(group),'n_valid':len(valid),
                      'n_invalid':len(group)-len(valid),'n_missing':20-len(group),
                      'adopt':k,'rate':k/len(valid) if valid else None,'ci95':wilson(k,len(valid))})
    logging.basicConfig(level=logging.INFO)
    utils.log_dataframe_summary(pd.DataFrame(cells),'Claude screen cells; all invalid/missing retained',logging.getLogger('claude-screen'))
    complete=len(rows)==80;a=cells[2];b=cells[3]
    ai=exact(a['adopt'],20,20-a['n_valid']);bi=exact(b['adopt'],20,20-b['n_valid'])
    interval=[ai[0]-bi[1],ai[1]-bi[0]]
    failure=bool(complete and (interval[0]>.10 or interval[1]<-.10))
    saturated=bool(complete and all(c['rate'] is not None for c in cells) and
                   (all(c['rate']<=.05 for c in cells) or all(c['rate']>=.95 for c in cells)))
    quality=all(c['n_valid']/20>=.98 for c in cells)
    status='INCOMPLETE' if not complete else 'INVALID_OUTPUT_SCREEN_NOT_INFORMATIVE' if not quality else 'GROSS_WORDING_FAILURE_DETECTED' if failure else 'SATURATED_SCREEN_NOT_INFORMATIVE' if saturated else 'NO_GROSS_FAILURE_DETECTED_NOT_VALIDATED'
    result={'design_hash':m['design_hash'],'status':status,'cells':cells,'primary_pair':['paraphrase_2','paraphrase_3'],
            'primary_difference':a['rate']-b['rate'] if a['rate'] is not None and b['rate'] is not None else None,
            'primary_conservative_95_interval_unknown_envelope':interval,'validity_floor_met':quality,'n_records':len(rows),
            'n_valid':sum(c['n_valid'] for c in cells),'n_api_failures':sum(bool(r.get('error_message')) for r in rows),
            'recorded_token_estimate_usd':sum(cost(r) for r in rows),'phase_gate':'Unchanged; no equivalence or phase pass can follow this screen'}
    path=root/'analysis'/f'screen_{digest(result)[:16]}.json';save_new(path,result)
    print(json.dumps(result,indent=2));return result


def archive(root,m):
    rows=list(ValiditySink(root/'records').read_all())
    save_new(root/'record_checksums.json',{'design_hash':m['design_hash'],'n_records':len(rows),
        'index':[{'record_key':r['record_key'],'record_hash':r['record_hash']} for r in rows]})
    target=ROOT/'output/validity_backups'/f'{root.name}_{m["design_hash"][:16]}.zip';target.parent.mkdir(parents=True,exist_ok=True)
    if not target.exists():
        with zipfile.ZipFile(target,'x',compression=zipfile.ZIP_DEFLATED) as z:
            for p in sorted(root.rglob('*')):
                if p.is_file():z.write(p,p.relative_to(root).as_posix())
    with zipfile.ZipFile(target) as z:
        if z.testzip():raise ValueError('Corrupt ZIP')
        for r in rows:
            name='records/'+r['record_key']+'.json'
            if z.read(name)!=(root/name).read_bytes():raise ValueError('ZIP payload mismatch')
    save_new(root/'local_backup.json',{'path':str(target),'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),
                                     'note':'All raw bytes verified; same-computer backup only.'})


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--run-root',type=Path,required=True)
    p.add_argument('--prepare-only',action='store_true');p.add_argument('--yes',action='store_true');a=p.parse_args();root=a.run_root.resolve()
    if a.prepare_only:prepare(root);print('Prepared 80 unchanged-prompt calls; no API use.');return
    if not a.yes or not os.environ.get('ANTHROPIC_API_KEY'):p.error('Need --yes and configured Anthropic key')
    m=json.loads((root/'manifest.json').read_text(encoding='utf-8'))
    import msvcrt
    from anthropic import AsyncAnthropic
    logs=ROOT/'output'/root.name;logs.mkdir(parents=True,exist_ok=True)
    def status(v):(logs/'status.json').write_text(json.dumps({'status':v,'timestamp_utc':utc_now_iso()},indent=2),encoding='utf-8')
    with (logs/'execution.lock').open('a+b') as lock:
        lock.write(b'0');lock.flush();lock.seek(0);msvcrt.locking(lock.fileno(),msvcrt.LK_NBLCK,1)
        status('RUNNING')
        try:
            client=LLMClient(MODEL,concurrency=2,max_retries=1,timeout_s=90)
            client._client=AsyncAnthropic(max_retries=0,timeout=90)
            try:asyncio.run(execute(root,m,client))
            finally:result=score(root,m);archive(root,m)
            status(result['status'])
        except BaseException:status('STOPPED_WITH_ERROR');raise


if __name__=='__main__':main()
