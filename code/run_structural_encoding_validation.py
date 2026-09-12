"""Staged structural encoding diagnostics and all-ten-parameter coverage."""
import argparse
import asyncio
from copy import deepcopy
from hashlib import sha256
from itertools import combinations
import json
import logging
import os
from pathlib import Path
import random

import pandas as pd
from scipy.stats import beta, fisher_exact
import utils
from engine.llm_client import Message
from engine.parsing import parse_decision, parse_reasoning
from engine.seeding import derive_seed
from engine.validity_sweep import digest, freeze, ValiditySink
from engine.validity_variants import load_reviewed_paraphrases, variant_prompt
from run_validity_claude import save_new
import run_validity_evidence_screen as base
import run_validity_tool_delivery as archive_support

from engine.validity_variants import PARAMETER_RE
from run_validity_original_expanded import intent
import numpy as np

ROOT=base.ROOT
BASE=ROOT/'experiments/phase1_5_encoding_validity'
SOURCE=BASE/'option_c_20260909_restart/manifest.json'
PREVIOUS=BASE/'profile_transfer_20260912'
PACKAGE=BASE/'structural_encoding_20260912'
PROTOCOL=PACKAGE/'PROTOCOL.md'
TEMPLATES=BASE/'claude_paraphrases_20260909_theory_r5/paraphrases_approved.json'
VALUES=(.1,.3,.5,.7,.9)
from engine.validity_analysis import DIRECTIONS
from engine.validity_variants import verbal_level
import re


def render(parameter,value,profile,variant,templates):
    template=templates.get(variant)
    kind=variant if variant in ('numeric_only','verbal_only') else 'hybrid'
    prompt,provenance=variant_prompt(parameter,value,kind,template=template)
    matches=list(re.finditer(r'(?m)^ (\d+)\. ([^:\n]+): ([^\n]+)',prompt))
    if len(matches)!=10:raise ValueError('Missing numbered profile values')
    for code,match in reversed(list(zip(utils.PARAM_NAMES,matches))):
        text=verbal_level(profile[code]) if kind=='verbal_only' else f'{profile[code]:.2f}'
        prompt=prompt[:match.start(3)]+text+prompt[match.end(3):]
    return prompt


def build(stage):
    if stage not in ('diagnostics','sweep'):raise ValueError('Unknown stage')
    source=json.loads(SOURCE.read_bytes());prior=json.loads((PREVIOUS/'manifest.json').read_bytes())
    if digest(source['design'])!=source['design_hash']:raise ValueError('Source hash mismatch')
    base.check(prior)
    templates=load_reviewed_paraphrases(TEMPLATES)
    if set(templates)!={'paraphrase_1','paraphrase_2','paraphrase_3'}:raise ValueError('Template names changed')
    diagnostic=stage=='diagnostics';nb=8 if diagnostic else 20;seed=20261005 if diagnostic else 20261008
    variants=('canonical',*templates,'numeric_only','verbal_only') if diagnostic else ('canonical',)
    cases=(('MoR','S3'),('MS','S2')) if diagnostic else tuple((p,s) for p in utils.PARAM_NAMES for s in ('S1','S2','S3'))
    eigenvalue=utils.verify_psd(utils.R);draws=utils.sample_agents(nb,seed=seed)
    backgrounds=[dict(zip(utils.PARAM_NAMES,map(float,row))) for row in draws]
    if draws.shape!=(nb,10) or not np.isfinite(draws).all():raise ValueError('Invalid backgrounds')
    logging.basicConfig(level=logging.INFO)
    utils.log_dataframe_summary(pd.DataFrame(backgrounds),f'All{nb} {stage} backgrounds; no selection',logging.getLogger('structural'))
    cells=[]
    for b,bg in enumerate(backgrounds):
        for p,s in cases:
            for variant in variants:
                for v in VALUES:
                    source_cell=next(c for c in source['design']['cells'] if (c['arm'],c['parameter'],c['problem'],c['value'])==('full_harness',p,s,v))
                    canonical,_=variant_prompt(p,v)
                    if canonical!=source_cell['messages'][0]['content']:raise ValueError('Canonical loader/source mismatch')
                    profile=dict(bg);profile[p]=v;messages=deepcopy(source_cell['messages'])
                    messages[0]['content']=render(p,v,profile,variant,templates)
                    sign=DIRECTIONS.get((p,s));target=source_cell['labels'][1] if sign==-1 else source_cell['labels'][0]
                    cells.append({'id':f'background_{b:02d}/{p}_{s}/{variant}/v{v:.1f}',
                        'background':b,'parameter':p,'problem':s,'variant':variant,'value':v,'profile':profile,
                        'rendered_profile':{k:(verbal_level(x) if variant=='verbal_only' else float(f'{x:.2f}')) for k,x in profile.items()},
                        'target_label':target,'prespecified':sign is not None,'messages':messages,'labels':source_cell['labels'],'n':1})
    expected=480 if diagnostic else 3000
    if len(cells)!=expected or len({c['id'] for c in cells})!=expected:raise ValueError('Allocation mismatch')
    # Verbal bins can intentionally coincide. Never deduplicate/reweight their slots.
    paths=[Path(__file__),PROTOCOL,SOURCE,TEMPLATES,PREVIOUS/'manifest.json',ROOT/'tests/test_structural_validation.py',ROOT/'code/engine/validity_variants.py',ROOT/'code/engine/validity_coherence.py']
    paths += [ROOT/p for p in prior['design']['source_hashes']]
    d={'stage':stage,'experiment':'structural_encoding_evaluation','configuration':'neutral','provider':'openai','model':base.MODEL,
       'temperature':1.,'max_tokens':600,'seed':seed+1,'draw_seed':seed,'analysis_seed':seed+2,
       'planned_calls':expected,'params':list(utils.PARAM_NAMES),'problems':['S1','S2','S3'],
       'n_backgrounds':nb,'backgrounds':backgrounds,'backgrounds_hash':digest(backgrounds),'R_min_eigenvalue':float(eigenvalue),
       'cells':cells,'pricing':prior['design']['pricing'],'total_package_cap_usd':25.,'bootstrap_draws':100000,
       'source_hashes':{p.relative_to(ROOT).as_posix():sha256(p.read_bytes()).hexdigest() for p in paths},
       'primary':'All group endpoint and intermediate contrasts, shared background bootstrap; Bonferroni across both contrasts in every group. Full frozen rules in protocol.',
       'phase_gate':'Original gate unchanged; structural mechanism triangulated, no proof of unique internal understanding or Phase2 release.'}
    d['full_dispatch_reserve_usd']=sum(base.reserve(c,d) for c in cells)
    d['spending_ceiling_usd']=d['full_dispatch_reserve_usd']+1e-8
    return d


def prepare_package():
    designs=[build(s) for s in ('diagnostics','sweep')]
    total=sum(d['full_dispatch_reserve_usd'] for d in designs)
    if total>22:raise ValueError(f'Behavioural reservations {total} leave less than $3 for audit')
    if set(map(digest,designs[0]['backgrounds']))&set(map(digest,designs[1]['backgrounds'])):raise ValueError('Shared stage backgrounds')
    for d in designs:
        root=PACKAGE/d['stage'];m=freeze(root/'manifest.json',d)
        save_new(root/'request_preview.json',{'design_hash':m['design_hash'],'cells':d['cells']})
    save_new(PACKAGE/'allocation.json',{'cap_usd':25,'behavioural_reservation_usd':total,'audit_reservation_available_usd':25-total,
        'stages':{d['stage']:{'calls':d['planned_calls'],'reserve_usd':d['full_dispatch_reserve_usd']} for d in designs},
        'audit_calls':200,'audit_dispatch':'Exact blinded payloads must fit the remaining package reservation.'})
    return designs


def jobs(d):
    rng=random.Random(d['seed']);groups={}
    for c in d['cells']:groups.setdefault((c['background'],c['parameter'],c['problem'],c['variant']),[]).append(c)
    keys=list(groups);rng.shuffle(keys)
    for key in keys:
        cells=list(groups[key]);rng.shuffle(cells)
        for c in cells:yield f"{c['id']}/call_0001",c,1,derive_seed(d['seed'],c['id'],1)

def inventory(root, m):
    base.check(m)
    planned = {key: (c, i, seed) for key, c, i, seed in jobs(m['design'])}
    rows = list(ValiditySink(root / 'records').read_all()); seen = set()
    for r in rows:
        key = r['record_key']
        if key in seen or key not in planned: raise ValueError('Unexpected or duplicate record')
        c, i, seed = planned[key]; seen.add(key)
        if (r['design_hash'] != m['design_hash'] or r['cell_id'] != c['id'] or r['call_index'] != i
                or r['seed'] != seed or r['request_messages'] != c['messages']
                or r['agent_parameters'] != c['profile'] or r['problem_id'] != c['problem']):
            raise ValueError('Record provenance mismatch')
        if not r['terminal_failure']:
            payload = r['response_payload']
            if (payload['choices'][0]['message']['content'] != r['raw_response']
                    or payload['id'] != r['api_call_id'] or payload['model'] != base.MODEL
                    or parse_decision(r['raw_response'], tuple(c['labels'])) != (r['parsed_decision'], r['parse_status'])):
                raise ValueError('Raw response or reparsed decision mismatch')
    return planned, rows, seen


async def execute(root, m, client):
    planned, rows, seen = inventory(root, m); d = m['design']; allocation = list(jobs(d))
    if rows or any((root / 'dispatches').rglob('*.json')):
        raise ValueError('Existing attempts or unresolved intents; no automatic rerun')
    if len({seed for _, _, _, seed in allocation}) != d['planned_calls']: raise ValueError('Seed collision')
    reserved = 0.; sink = ValiditySink(root / 'records')
    async def one(job):
        key, c, i, seed = job
        result = await client.complete([Message(**v) for v in c['messages']],
                                      temperature=d['temperature'], max_tokens=d['max_tokens'], seed=seed)
        decision, parse = parse_decision(result.text, tuple(c['labels']))
        r = {'record_key': key, 'design_hash': m['design_hash'], 'cell_id': c['id'],
             'call_index': i, 'seed': seed, 'arm':'full_harness', 'swept_parameter':c['parameter'], 'sweep_value':c['value'], 'problem_id': c['problem'], 'agent_parameters': c['profile'],
             'request_messages': result.request_messages, 'response_payload': result.raw_response,
             'raw_response': result.text, 'parsed_decision': decision, 'parsed_reasoning': parse_reasoning(result.text),
             'parse_status': parse, 'api_call_id': result.api_call_id, 'model_version': result.model_version,
             'provider': result.provider, 'attempts': result.attempts, 'error_message': result.error,
             'timestamp_utc': result.timestamp_utc, 'temperature': result.temperature, 'max_tokens': result.max_tokens}
        cost = base.cost(r)
        r['terminal_failure'] = bool(result.error or result.model_version != base.MODEL or result.provider != 'openai'
            or result.attempts != 1 or not result.api_call_id or cost is None or cost > base.reserve(c, d)
            or parse != 'ok' or result.request_messages != c['messages'])
        r['record_hash'] = digest(r); sink.write(key, r)
        if r['terminal_failure']: sink.write_failure({'record_key': key, 'error': result.error, 'parse_status': parse})
        return r
    for start in range(0, d['planned_calls'], 3):
        batch = allocation[start:start + 3]; bound = sum(base.reserve(c, d) for _, c, _, _ in batch)
        if reserved + bound > d['spending_ceiling_usd']: raise RuntimeError('Pre-dispatch spending guard')
        for key, c, _, _ in batch: save_new(root / 'dispatches' / (key + '.json'), intent(key, c, m))
        reserved += bound
        new = await asyncio.gather(*(one(j) for j in batch)); rows.extend(new)
        if len(rows) % 30 == 0 or len(rows) in (3, d['planned_calls']):
            print(f"{len(rows)}/{d['planned_calls']}; known cost ${sum(base.cost(r) or 0 for r in rows):.5f}", flush=True)
        if any(r['terminal_failure'] for r in new): raise RuntimeError('Terminal failure preserved; stopped')


def assess(rows,m):
    d=m['design'];lookup={(r['cell_id'],r['call_index']):r for r in rows}
    complete=len(rows)==d['planned_calls'] and len(lookup)==len(rows) and all(not r['terminal_failure'] and r['parse_status']=='ok' for r in rows)
    keys=list(dict.fromkeys((c['parameter'],c['problem'],c['variant']) for c in d['cells']))
    tensor=np.full((d['n_backgrounds'],len(keys),5),np.nan)
    for c in d['cells']:
        r=lookup.get((c['id'],1))
        if r and not r['terminal_failure'] and r['parse_status']=='ok':
            tensor[c['background'],keys.index((c['parameter'],c['problem'],c['variant'])),VALUES.index(c['value'])]=int(r['parsed_decision']==c['target_label'])
    complete=complete and bool(np.isfinite(tensor).all());groups=[]
    if complete:
        effects=np.concatenate((tensor[:,:,-1]-tensor[:,:,0],tensor[:,:,3]-tensor[:,:,1]),axis=1)
        rng=np.random.default_rng(d['analysis_seed']);indices=rng.integers(0,len(tensor),size=(d['bootstrap_draws'],len(tensor)))
        boot=np.column_stack([effects[:,j][indices].mean(axis=1) for j in range(effects.shape[1])])
        alpha=.05/(2*effects.shape[1]);adj=np.quantile(boot,[alpha,1-alpha],axis=0);nom=np.quantile(boot,[.025,.975],axis=0)
        for j,(p,s,v) in enumerate(keys):
            rates=tensor[:,j,:].mean(axis=0).tolist();known=(p,s) in DIRECTIONS
            groups.append({'parameter':p,'problem':s,'variant':v,'prespecified':known,'rates':rates,'n_per_level':len(tensor),
                'endpoint_effect':float(effects[:,j].mean()),'endpoint_nominal95':nom[:,j].tolist(),'endpoint_adjusted':adj[:,j].tolist(),
                'interior_effect':float(effects[:,j+len(keys)].mean()),'interior_nominal95':nom[:,j+len(keys)].tolist(),'interior_adjusted':adj[:,j+len(keys)].tolist(),
                'observed_ordered':bool(np.all(np.diff(rates)>=0)),
                'predicted_endpoint_supported':bool(adj[0,j]>0) if known else None,
                'background_endpoint_effects':effects[:,j].tolist(),'background_interior_effects':effects[:,j+len(keys)].tolist()})
        logging.basicConfig(level=logging.INFO)
        utils.log_dataframe_summary(pd.DataFrame(groups),f'All{len(rows)} responses ->{len(groups)} curves, no exclusions',logging.getLogger('structural'))
    return {'design_hash':m['design_hash'],'status':'COMPLETE' if complete else 'INCOMPLETE_OR_INVALID',
        'n_records':len(rows),'n_valid':sum(r['parse_status']=='ok' and not r['terminal_failure'] for r in rows),
        'groups':groups,'known_cost_usd':sum(base.cost(r) or 0 for r in rows),'phase_gate':d['phase_gate']}


def score(root,m):
    planned,rows,seen=inventory(root,m);intents={};by_key={r['record_key']:r for r in rows}
    for p in (root/'dispatches').rglob('*.json'):
        obj=json.loads(p.read_bytes());key=obj['record_key']
        if key not in planned or key in intents or obj!=intent(key,planned[key][0],m):raise ValueError('Intent mismatch')
        intents[key]=obj
    if not seen.issubset(intents):raise ValueError('Missing intents')
    reserved=sum(x['reserved_usd'] for x in intents.values())
    if reserved>m['design']['spending_ceiling_usd']:raise ValueError('Reservation breach')
    result=assess(rows,m);result['pending_requests']=len(intents)-len(rows)
    unknown=sum(x['reserved_usd'] for k,x in intents.items() if k not in by_key or base.cost(by_key[k]) is None)
    save_new(root/'analysis'/f'result_{digest(result)[:16]}.json',result)
    save_new(root/'budget_ledger.json',{'stage':m['design']['stage'],'reserved_usd':reserved,'known_cost_usd':result['known_cost_usd'],
        'unknown_usage_reserved_usd':unknown,'pending_requests':result['pending_requests'],'package_cap_usd':25,'provider_balance_verified':False})
    return result

def main():
    p = argparse.ArgumentParser(description=__doc__); p.add_argument('--run-root', type=Path, required=True)
    p.add_argument('--prepare-only', action='store_true'); p.add_argument('--yes', action='store_true')
    a = p.parse_args(); root = a.run_root.resolve()
    if a.prepare_only:
        designs=prepare_package(); m=json.loads((root/'manifest.json').read_bytes()); print(json.dumps({k: m['design'][k] for k in ('planned_calls', 'full_dispatch_reserve_usd', 'spending_ceiling_usd')})); return
    m = json.loads((root / 'manifest.json').read_bytes()); base.check(m)
    auth = json.loads((root / 'dispatch_authorization.json').read_bytes())
    if auth['design_hash'] != m['design_hash'] or auth['request_preview_sha256'] != sha256((root / 'request_preview.json').read_bytes()).hexdigest():
        raise ValueError('Authorization scope mismatch')
    if m['design']['stage']=='sweep':
        diagnostics=list((PACKAGE/'diagnostics/analysis').glob('result_*.json'))
        if len(diagnostics)!=1 or json.loads(diagnostics[0].read_bytes())['status']!='COMPLETE':raise ValueError('Diagnostics must complete first')
    if not a.yes or not os.environ.get('OPENAI_API_KEY'): p.error('Need --yes and configured key')
    from openai import AsyncOpenAI
    import msvcrt
    async def run():
        client = base.SingleAttemptOpenAI(base.MODEL, concurrency=3, max_retries=1, timeout_s=180)
        async with AsyncOpenAI(base_url='https://api.openai.com/v1', max_retries=0, timeout=180) as sdk:
            client._client = sdk; await execute(root, m, client)
    logs = ROOT / 'output' / root.name; logs.mkdir(parents=True, exist_ok=True)
    with (logs / 'execution.lock').open('a+b') as lock:
        lock.write(b'0'); lock.flush(); lock.seek(0); msvcrt.locking(lock.fileno(), msvcrt.LK_NBLCK, 1)
        try: asyncio.run(run())
        finally:
            try: result = score(root, m)
            finally: archive_support.archive(root, m)
            print(json.dumps({k: v for k, v in result.items() if k not in ('cells','background_effects')}, indent=2))


if __name__ == '__main__': main()
