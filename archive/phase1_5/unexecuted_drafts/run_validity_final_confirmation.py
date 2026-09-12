"""Final confirmation: nine theory predictions,40 new backgrounds,3600 calls."""
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
PROPOSAL=BASE/'final_confirmation_20260912/PROTOCOL.md'
CASES=(('RE','S1','A'),('TfA','S1','A'),('PD','S1','A'),('ID','S2','FORMAL_REPORT'),('TfA','S2','LOCAL_CORRECTION'),('MS','S2','FORMAL_REPORT'),('RT','S3','ADOPT'),('MoR','S3','ADOPT'),('RE','S3','WAIT'))
VALUES=(.1,.3,.5,.7,.9)
N=2
BACKGROUNDS=40
CALLS=3600
CAP=25.
DRAW_SEED=20261002
SEED=20261003
ANALYSIS_SEED=20261004


def replace_values(system,profile):
    matches=list(PARAMETER_RE.finditer(system))
    if len(matches)!=10 or list(profile)!=list(utils.PARAM_NAMES):raise ValueError('Parameter layout mismatch')
    result=system
    for match,name in reversed(list(zip(matches,utils.PARAM_NAMES))):
        result=result[:match.start(3)]+f"{profile[name]:.2f}"+result[match.end(3):]
    after=list(PARAMETER_RE.finditer(result))
    if [m.group(1,2,4,5) for m in matches]!=[m.group(1,2,4,5) for m in after]:raise ValueError('Definitions changed')
    return result


def jobs(d):
    rng=random.Random(d['seed'])
    lookup={(c['background'],c['parameter'],c['problem'],c['value']):c for c in d['cells']}
    for block in (1,2):
        comparisons=[(b,p,s) for b in range(BACKGROUNDS) for p,s,_ in CASES]
        rng.shuffle(comparisons)
        for b,p,s in comparisons:
            levels=list(VALUES);rng.shuffle(levels)
            for v in levels:
                c=lookup[b,p,s,v]
                yield f"{c['id']}/call_{block:04d}",c,block,derive_seed(d['seed'],c['id'],block)


def prepare(root):
    source=json.loads(SOURCE.read_bytes())
    if digest(source['design'])!=source['design_hash']:raise ValueError('Source manifest mismatch')
    prior=json.loads((PREVIOUS/'manifest.json').read_bytes());base.check(prior)
    ledger=json.loads((PREVIOUS/'budget_ledger.json').read_bytes())
    if ledger['pending_requests']:raise ValueError('Prior unresolved usage')
    min_eigenvalue=utils.verify_psd(utils.R)
    draws=utils.sample_agents(BACKGROUNDS,seed=DRAW_SEED)
    if draws.shape!=(BACKGROUNDS,10) or not np.isfinite(draws).all() or np.any((draws<0)|(draws>1)):raise ValueError('Invalid sample')
    backgrounds=[dict(zip(utils.PARAM_NAMES,map(float,row))) for row in draws]
    logging.basicConfig(level=logging.INFO)
    utils.log_dataframe_summary(pd.DataFrame(backgrounds),'All40 new backgrounds retained; no selection',logging.getLogger('confirmation'))
    cells=[]
    for b,bg in enumerate(backgrounds):
        for parameter,problem,target in CASES:
            old=next(c for c in source['design']['cells'] if (c['arm'],c['parameter'],c['problem'],c['value'])==('full_harness',parameter,problem,.1))
            if target not in old['labels']:raise ValueError('Unknown target label')
            for value in VALUES:
                profile=dict(bg);profile[parameter]=value;messages=deepcopy(old['messages'])
                messages[0]['content']=replace_values(messages[0]['content'],profile)
                cells.append({'id':f'background_{b:02d}/{parameter}_{problem}/v{value:.1f}',
                    'background':b,'parameter':parameter,'problem':problem,'target_label':target,'value':value,
                    'profile':profile,'rendered_profile':{k:float(f'{v:.2f}') for k,v in profile.items()},
                    'messages':messages,'labels':old['labels'],'n':2})
    if len(cells)!=1800 or len({digest(c['messages']) for c in cells})!=1800:raise ValueError('Duplicate conditions; review without rerolling')
    old_backgrounds=prior['design']['backgrounds']
    if {digest(b) for b in backgrounds}&{digest(b) for b in old_backgrounds}:raise ValueError('Background reused')
    paths=[Path(__file__),SOURCE,PROPOSAL,PREVIOUS/'manifest.json',PREVIOUS/'budget_ledger.json',
           ROOT/'code/utils.py',ROOT/'code/run_validity_original_expanded.py',ROOT/'tests/test_final_confirmation.py',
           ROOT/'Theory/concepts_as_architecture_thesis_v0_6.md']
    paths += [ROOT/p for p in prior['design']['source_hashes']]
    d={'experiment':'final_numeric_confirmation','configuration':'neutral','model':base.MODEL,'provider':'openai',
       'temperature':1.,'max_tokens':600,'seed':SEED,'draw_seed':DRAW_SEED,'analysis_seed':ANALYSIS_SEED,
       'planned_calls':CALLS,'n_per_cell':2,'n_backgrounds':BACKGROUNDS,'backgrounds':backgrounds,
       'backgrounds_hash':digest(backgrounds),'R_min_eigenvalue':float(min_eigenvalue),'cells':cells,
       'spending_ceiling_usd':CAP,'prior_ledger':ledger,'budget_scope':'New separate $25 allocation; do not add old remaining allowance.',
       'pricing':prior['design']['pricing'],'pricing_verified_url':'https://developers.openai.com/api/docs/models/gpt-5.4-mini',
       'source_hashes':{p.relative_to(ROOT).as_posix():sha256(p.read_bytes()).hexdigest() for p in paths},
       'bootstrap_draws':100000,'bootstrap_quantile_method':'linear','family_contrasts':18,'transport_timeout_seconds':180,
       'primary':'Nine oriented endpoint contrasts; nine prespecified intermediate contrasts. Shared100000 whole-background bootstrap draws, nominal95 and Bonferroni18 adjusted99.722222% intervals. Full rules in hashed PROTOCOL.md.',
       'local_decision':'Endpoint: adjusted lower>0 and both block effects>0. Intermediate-range support additionally requires adjusted intermediate lower>0 and five nondecreasing observed rates. No labels for incomplete data.',
       'selection':'All nine original simple-problem directional hypotheses; all40 new backgrounds retained. Development-informed design with fresh data, not external preregistration.',
       'intervention':'Only profile numbers change. One coordinate varied per comparison, other nine fixed. No Beta/R/definition/dilemma changes.',
       'collection':'Two complete1800-call blocks; shuffled comparisons and levels. Concurrency3, distinct requested seeds, one attempt per slot.',
       'stop_rule':'Any terminal failure stops after current batch; no automatic continuation or replacement.',
       'phase_gate':'Phase1.5 open. Conditional behavioural encoding is the target claim; original full battery unchanged and Phase2 held.'}
    d['full_dispatch_reserve_usd']=sum(base.reserve(c,d)*2 for c in cells)
    if d['full_dispatch_reserve_usd']>CAP:raise ValueError('Full reserve exceeds cap')
    m=freeze(root/'manifest.json',d)
    save_new(root/'backgrounds.json',{'draw_seed':DRAW_SEED,'backgrounds_hash':d['backgrounds_hash'],'backgrounds':backgrounds})
    save_new(root/'request_preview.json',{'design_hash':m['design_hash'],'cells':cells})
    return m


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
    if len({seed for _, _, _, seed in allocation}) != CALLS: raise ValueError('Seed collision')
    reserved = 0.; sink = ValiditySink(root / 'records')
    async def one(job):
        key, c, i, seed = job
        result = await client.complete([Message(**v) for v in c['messages']],
                                      temperature=d['temperature'], max_tokens=d['max_tokens'], seed=seed)
        decision, parse = parse_decision(result.text, tuple(c['labels']))
        r = {'record_key': key, 'design_hash': m['design_hash'], 'cell_id': c['id'],
             'call_index': i, 'seed': seed, 'problem_id': c['problem'], 'agent_parameters': c['profile'],
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
    for start in range(0, CALLS, 3):
        batch = allocation[start:start + 3]; bound = sum(base.reserve(c, d) for _, c, _, _ in batch)
        if reserved + bound > d['spending_ceiling_usd']: raise RuntimeError('Pre-dispatch spending guard')
        for key, c, _, _ in batch: save_new(root / 'dispatches' / (key + '.json'), intent(key, c, m))
        reserved += bound
        new = await asyncio.gather(*(one(j) for j in batch)); rows.extend(new)
        if len(rows) % 30 == 0 or len(rows) in (3, CALLS):
            print(f'{len(rows)}/{CALLS}; known cost ${sum(base.cost(r) or 0 for r in rows):.5f}', flush=True)
        if any(r['terminal_failure'] for r in new): raise RuntimeError('Terminal failure preserved; stopped')


def analyse_tensor(tensor,d):
    # Shape backgrounds x nine predictions x five levels x two blocks.
    expected=(BACKGROUNDS,len(CASES),len(VALUES),N)
    if tensor.shape!=expected or not np.isfinite(tensor).all():raise ValueError('Incomplete outcome tensor')
    deltas=tensor[:,:,-1,:]-tensor[:,:,0,:]
    interior=tensor[:,:,3,:]-tensor[:,:,1,:]
    effects=np.concatenate((deltas.mean(axis=2),interior.mean(axis=2)),axis=1)
    rng=np.random.default_rng(d['analysis_seed'])
    indices=rng.integers(0,BACKGROUNDS,size=(d['bootstrap_draws'],BACKGROUNDS))
    # Bound working memory; use the same resamples for every contrast.
    boot=np.column_stack([effects[:,j][indices].mean(axis=1) for j in range(18)])
    adjusted=np.quantile(boot,[.05/(2*18),1-.05/(2*18)],axis=0,method='linear')
    nominal=np.quantile(boot,[.025,.975],axis=0,method='linear')
    primary=[];background_effects=[]
    for j,(p,s,t) in enumerate(CASES):
        rates=tensor[:,j,:,:].mean(axis=(0,2)).tolist()
        blocks=deltas[:,j,:].mean(axis=0).tolist()
        endpoint=bool(adjusted[0,j]>0 and all(v>0 for v in blocks))
        ordered=bool(np.all(np.diff(rates)>=0))
        primary.append({'parameter':p,'problem':s,'target_label':t,'five_target_rates':rates,
            'endpoint_effect':float(effects[:,j].mean()),'endpoint_nominal95':nominal[:,j].tolist(),
            'endpoint_adjusted':adjusted[:,j].tolist(),'block_endpoint_effects':blocks,
            'intermediate_effect':float(effects[:,j+9].mean()),'intermediate_nominal95':nominal[:,j+9].tolist(),
            'intermediate_adjusted':adjusted[:,j+9].tolist(),'block_intermediate_effects':interior[:,j,:].mean(axis=0).tolist(),
            'observed_five_levels_ordered':ordered,'endpoint_confirmed':endpoint,
            'intermediate_range_supported':bool(endpoint and ordered and adjusted[0,j+9]>0)})
        for b in range(BACKGROUNDS):
            background_effects.append({'background':b,'parameter':p,'problem':s,
                'endpoint_effect':float(effects[b,j]),'intermediate_effect':float(effects[b,j+9]),
                'block1_endpoint':float(deltas[b,j,0]),'block2_endpoint':float(deltas[b,j,1])})
    return primary,background_effects


def assess(rows,m):
    lookup={(r['cell_id'],r['call_index']):r for r in rows}
    complete=len(rows)==CALLS and len(lookup)==CALLS and all(not r['terminal_failure'] and r['parse_status']=='ok' for r in rows)
    tensor=np.full((BACKGROUNDS,len(CASES),len(VALUES),N),np.nan);cells=[]
    for c in m['design']['cells']:
        valid=[];recorded=0
        for block in (1,2):
            r=lookup.get((c['id'],block))
            if r is None:continue
            recorded+=1
            if r['terminal_failure'] or r['parse_status']!='ok':continue
            y=int(r['parsed_decision']==c['target_label']);valid.append(y)
            j=CASES.index((c['parameter'],c['problem'],c['target_label']))
            tensor[c['background'],j,VALUES.index(c['value']),block-1]=y
        cells.append({k:c[k] for k in ('id','background','parameter','problem','value','target_label')}|{
            'n_expected':N,'n_recorded':recorded,'n_valid':len(valid),'n_missing':N-recorded,
            'n_invalid':recorded-len(valid),'target_count':sum(valid),'rate':sum(valid)/len(valid) if valid else None})
    complete=complete and bool(np.isfinite(tensor).all())
    logging.basicConfig(level=logging.INFO);logger=logging.getLogger('confirmation')
    utils.log_dataframe_summary(pd.DataFrame(cells),f'All{len(rows)} records ->1800 cells; no silent exclusions',logger)
    primary,effects=analyse_tensor(tensor,m['design']) if complete else ([],[])
    if effects:utils.log_dataframe_summary(pd.DataFrame(effects),'All40 backgrounds x9 contrasts; no filtering',logger)
    return {'design_hash':m['design_hash'],'status':'COMPLETE_CONFIRMATION' if complete else 'INCOMPLETE_OR_INVALID',
        'n_records':len(rows),'n_valid':sum(c['n_valid'] for c in cells),'cells':cells,'primary':primary,
        'background_effects':effects,'known_cost_usd':sum(base.cost(r) or 0 for r in rows),
        'unknown_usage_calls':sum(base.cost(r) is None for r in rows),'phase_gate':m['design']['phase_gate']}


def score(root,m):
    planned,rows,seen=inventory(root,m);intents={};row_map={r['record_key']:r for r in rows}
    for path in (root/'dispatches').rglob('*.json'):
        obj=json.loads(path.read_bytes());key=obj['record_key']
        if key not in planned or key in intents or obj!=intent(key,planned[key][0],m):raise ValueError('Intent mismatch')
        intents[key]=obj
    if not seen.issubset(intents):raise ValueError('Record without intent')
    reserved=sum(i['reserved_usd'] for i in intents.values())
    if reserved>CAP:raise ValueError('Reservation exceeds authorised cap')
    result=assess(rows,m);result['unresolved_dispatches']=len(intents)-len(rows)
    save_new(root/'analysis'/f"result_{digest(result)[:16]}.json",result)
    unknown=sum(i['reserved_usd'] for k,i in intents.items() if k not in row_map or base.cost(row_map[k]) is None)
    ledger={'allocation_usd':CAP,'recorded_token_estimate_usd':result['known_cost_usd'],
        'unknown_usage_reserved_usd':unknown,'conservative_charge_usd':result['known_cost_usd']+unknown,
        'remaining_allocation_conservative_usd':CAP-result['known_cost_usd']-unknown,
        'full_dispatch_reserve_usd':m['design']['full_dispatch_reserve_usd'],
        'dispatched_reserve_usd':reserved,'pending_requests':result['unresolved_dispatches'],
        'provider_balance_verified':False,'scope':'New separate $25 allowance; older ledgers preserved separately.'}
    save_new(root/'analysis'/f"budget_{digest(ledger)[:16]}.json",ledger)
    return result


def main():
    p = argparse.ArgumentParser(description=__doc__); p.add_argument('--run-root', type=Path, required=True)
    p.add_argument('--prepare-only', action='store_true'); p.add_argument('--yes', action='store_true')
    a = p.parse_args(); root = a.run_root.resolve()
    if a.prepare_only:
        m = prepare(root); print(json.dumps({k: m['design'][k] for k in ('planned_calls', 'full_dispatch_reserve_usd', 'spending_ceiling_usd')})); return
    m = json.loads((root / 'manifest.json').read_bytes()); base.check(m)
    auth = json.loads((root / 'dispatch_authorization.json').read_bytes())
    if auth['design_hash'] != m['design_hash'] or auth['request_preview_sha256'] != sha256((root / 'request_preview.json').read_bytes()).hexdigest():
        raise ValueError('Authorization scope mismatch')
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
