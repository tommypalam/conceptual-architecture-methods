"""Budgeted independent audit; existing brief coding prompt and scoring unchanged."""
import argparse
import asyncio
from copy import deepcopy
from hashlib import sha256
import json
import os
from pathlib import Path

from engine.llm_client import LLMClient, Message
from engine.validity_coherence import prepare_audit, score_audit, quartile
from engine.validity_sweep import ValiditySink, digest, freeze
from run_validity_audit_brief import brief_messages, parse_brief
from run_validity_claude import save_new
import run_structural_encoding_validation as run

MODEL='claude-haiku-4-5-20251001'
ROOT=run.PACKAGE/'audit'


def reserve(messages):
    return (sum(len(m['content'].encode('utf-8')) for m in messages)+512+2000*5)/1e6


def cost(row):
    u=(row.get('response_payload') or {}).get('usage',{})
    if not all(type(u.get(k)) is int and u[k]>=0 for k in ('input_tokens','output_tokens')):return None
    # No explicit caching requested. Conservatively charge any cache usage.
    return (u['input_tokens']+5*u['output_tokens']+2*(u.get('cache_creation_input_tokens',0) or 0)+(u.get('cache_read_input_tokens',0) or 0))/1e6


def prepare():
    source=run.PACKAGE/'sweep';m=json.loads((source/'manifest.json').read_bytes())
    _,rows,_=run.inventory(source,m)
    if len(rows)!=3000 or any(r['terminal_failure'] for r in rows):raise ValueError('Need complete verified sweep')
    pack,key=prepare_audit(source,seed=20261011)
    rendered_key=deepcopy(key);by_key={r['record_key']:r for r in rows};cells={c['id']:c for c in m['design']['cells']}
    changes=[]
    for item in rendered_key['items']:
        row=by_key[item['source_record_key']];profile=cells[row['cell_id']]['rendered_profile']
        for p,v in profile.items():
            q=quartile(v)
            if q!=item['true_quartiles'][p]:changes.append({'item_id':item['item_id'],'parameter':p,'active':p==item['swept_parameter']})
            item['true_quartiles'][p]=q
    if any(x['active'] for x in changes):raise ValueError('Active-level rounding mismatch')
    rendered_key['truth_basis']='Supplementary delivered two-decimal values; original full-precision answer key retained as specified.'
    jobs=[{'item_id':i['item_id'],'messages':[vars(m) for m in brief_messages(pack,i)]} for i in pack['items']]
    total=sum(reserve(j['messages']) for j in jobs)
    allocation=json.loads((run.PACKAGE/'allocation.json').read_bytes())
    if total>allocation['audit_reservation_available_usd']:raise ValueError(f'Exact audit reserve ${total:.6f} exceeds remaining ${allocation["audit_reservation_available_usd"]:.6f}; no calls')
    paths=[Path(__file__),run.ROOT/'code/run_validity_audit_brief.py',run.ROOT/'code/engine/validity_coherence.py',run.ROOT/'code/engine/llm_client.py',run.ROOT/'tests/test_structural_audit.py',source/'manifest.json',run.PROTOCOL]
    d={'task':'audit','model':MODEL,'temperature':1.,'max_tokens':2000,'planned_calls':200,
       'blind_pack_hash':digest(pack),'jobs':jobs,'full_dispatch_reserve_usd':total,
       'package_cap_usd':25,'behavioural_reservation_usd':allocation['behavioural_reservation_usd'],
       'source_hashes':{p.relative_to(run.ROOT).as_posix():sha256(p.read_bytes()).hexdigest() for p in paths},
       'policy':'Existing brief prompt/parser; single attempts, no retries or automatic resume. No private answer key sent.',
       'pricing_source':'https://platform.claude.com/docs/en/about-claude/pricing','pricing_checked':'2026-09-12',
       'analysis':'Existing literal thresholds, majority baselines and active-stratified permutation tests; 1999 permutations; no new coding manual.'}
    m=freeze(ROOT/'manifest.json',d);save_new(ROOT/'blind_pack.json',pack);save_new(ROOT/'private_answer_key.json',key)
    save_new(ROOT/'private_answer_key_rendered.json',rendered_key)
    save_new(ROOT/'rounding_check.json',{'selected_items':200,'estimates':2000,'changed_background_estimates':len(changes),'active_estimates_changed':0,
        'note':'Primary key unchanged; supplement checks bins against displayed values. Neither key is sent to coder.'})
    save_new(ROOT/'dispatch_authorization.json',{'design_hash':m['design_hash'],'authorization_basis':'Researcher authorised necessary tests then full sweep; existing independent audit follows completed source; package capped at $25.'})
    save_new(ROOT/'preflight.json',{'calls':200,'model':MODEL,'reserve_usd':total,'package_reserved_usd':allocation['behavioural_reservation_usd']+total,
        'manifest_sha256':sha256((ROOT/'manifest.json').read_bytes()).hexdigest(),'blind_pack_sha256':sha256((ROOT/'blind_pack.json').read_bytes()).hexdigest(),
        'answer_key_sha256':sha256((ROOT/'private_answer_key.json').read_bytes()).hexdigest(),
        'rendered_answer_key_sha256':sha256((ROOT/'private_answer_key_rendered.json').read_bytes()).hexdigest(),
        'note':'Raw reasoning-containing manifest and packs are local artifacts.'})
    return m


def check(m):
    if digest(m['design'])!=m['design_hash']:raise ValueError('Manifest mismatch')
    for p,h in m['design']['source_hashes'].items():
        if sha256((run.ROOT/p).read_bytes()).hexdigest()!=h:raise ValueError('Source changed')
    if m['design']['model']!=MODEL or m['design']['behavioural_reservation_usd']+m['design']['full_dispatch_reserve_usd']>25:raise ValueError('Model or budget mismatch')


async def execute(m,client,root=ROOT):
    check(m);d=m['design'];sink=ValiditySink(root/'records')
    if list(sink.read_all()) or list((root/'dispatches').glob('*.json')):raise ValueError('Existing attempts; no automatic resume')
    reserved=0.
    for j in d['jobs']:
        bound=reserve(j['messages'])
        if reserved+bound>d['full_dispatch_reserve_usd']+1e-9:raise ValueError('Pre-dispatch budget breach')
        save_new(root/'dispatches'/f"{j['item_id']}.json",{'item_id':j['item_id'],'design_hash':m['design_hash'],'reserved_usd':bound})
        reserved+=bound
        r=await client.complete([Message(**v) for v in j['messages']],temperature=1.,max_tokens=2000,seed=None)
        row={'item_id':j['item_id'],'record_key':j['item_id'],'design_hash':m['design_hash'],'model_version':r.model_version,
             'api_call_id':r.api_call_id,'timestamp_utc':r.timestamp_utc,'attempts':r.attempts,'request_messages':r.request_messages,
             'response_payload':r.raw_response,'raw_response':r.text,'parse_status':'ok','error_message':r.error,
             'provider':r.provider,'temperature':r.temperature,'max_tokens':r.max_tokens}
        try:
            if r.error or r.provider!='anthropic' or r.model_version!=MODEL or not r.api_call_id or r.attempts!=1 or r.request_messages!=j['messages'] or cost(row) is None or cost(row)>bound:raise ValueError('API/model/request/usage failure')
            payload=r.raw_response
            if payload['id']!=r.api_call_id or payload['model']!=MODEL or ''.join(v['text'] for v in payload['content'] if v['type']=='text')!=r.text:raise ValueError('Raw payload mismatch')
            row['estimates'],row['commentary']=parse_brief(r.text)
            row['commentary_word_count']=len(row['commentary'].split())
        except (ValueError,TypeError,KeyError) as exc:
            row['parse_status']='failed';row['validation_error']=str(exc)
        row['record_hash']=digest(row);sink.write(j['item_id'],row)
        print(f"Audit {len(list(sink.read_all()))}/200",flush=True)
        if row['parse_status']!='ok':sink.write_failure({'item_id':j['item_id'],'error':row.get('validation_error')});raise RuntimeError('Audit failure preserved; stopped')


def score(m):
    check(m);rows=list(ValiditySink(ROOT/'records').read_all());jobs={j['item_id']:j for j in m['design']['jobs']}
    for r in rows:
        if r['design_hash']!=m['design_hash'] or r['request_messages']!=jobs[r['item_id']]['messages']:raise ValueError('Audit provenance mismatch')
        if r['parse_status']=='ok' and parse_brief(r['raw_response'])[0]!=r['estimates']:raise ValueError('Reparsed coding mismatch')
    ids=[r['api_call_id'] for r in rows if r['parse_status']=='ok']
    if len(ids)!=len(set(ids)):raise ValueError('Duplicate audit API ID')
    key=json.loads((ROOT/'private_answer_key.json').read_bytes())
    if key['blind_pack_hash']!=m['design']['blind_pack_hash']:raise ValueError('Answer-key mismatch')
    report=score_audit(key,rows,permutations=1999);save_new(ROOT/'analysis'/f'audit_{digest(report)[:16]}.json',report)
    delivered_key=json.loads((ROOT/'private_answer_key_rendered.json').read_bytes())
    delivered=score_audit(delivered_key,rows,permutations=1999)
    save_new(ROOT/'analysis'/f'rendered_truth_sensitivity_{digest(delivered)[:16]}.json',delivered)
    by_id={r['item_id']:r for r in rows};unknown=0.;n=0
    for p in (ROOT/'dispatches').glob('*.json'):
        i=json.loads(p.read_bytes());n+=1
        if i['item_id'] not in by_id or cost(by_id[i['item_id']]) is None:unknown+=i['reserved_usd']
    save_new(ROOT/'budget_ledger.json',{'known_cost_usd':sum(cost(r) or 0 for r in rows),'unknown_usage_reserved_usd':unknown,'pending_requests':n-len(rows),
        'full_dispatch_reserve_usd':m['design']['full_dispatch_reserve_usd'],'provider_balance_verified':False})
    return report


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--prepare-only',action='store_true');parser.add_argument('--yes',action='store_true');a=parser.parse_args()
    if a.prepare_only:
        m=prepare();print(json.dumps({'planned_calls':200,'reserve_usd':m['design']['full_dispatch_reserve_usd']}));return
    if not a.yes or not os.environ.get('ANTHROPIC_API_KEY'):parser.error('Need --yes and configured key')
    m=json.loads((ROOT/'manifest.json').read_bytes());auth=json.loads((ROOT/'dispatch_authorization.json').read_bytes())
    if auth['design_hash']!=m['design_hash']:raise ValueError('Authorisation mismatch')
    from anthropic import AsyncAnthropic
    import msvcrt
    async def work():
        async with AsyncAnthropic(base_url='https://api.anthropic.com',max_retries=0,timeout=180) as sdk:
            client=LLMClient(MODEL,concurrency=1,max_retries=1,timeout_s=180);client._client=sdk
            await execute(m,client)
    lockpath=run.ROOT/'output/structural_encoding_audit.lock';lockpath.parent.mkdir(exist_ok=True)
    with lockpath.open('a+b') as lock:
        lock.write(b'0');lock.flush();lock.seek(0);msvcrt.locking(lock.fileno(),msvcrt.LK_NBLCK,1)
        try:asyncio.run(work())
        finally:
            try:report=score(m)
            finally:run.archive_support.archive(ROOT,m)
            print(json.dumps({'complete':report['complete'],'literal_spec_thresholds_met':report['literal_spec_thresholds_met']}))


if __name__=='__main__':main()
