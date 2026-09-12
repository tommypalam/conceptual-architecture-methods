"""Frozen 40-call canonical MS replay of two complete historical seed cohorts."""
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
from run_validity_original_expanded import intent, holm
from scipy.stats import binomtest

ROOT = base.ROOT
BASE = ROOT / 'experiments/phase1_5_encoding_validity'
PREVIOUS = BASE / 'ms_stanza_crossover_20260912'
N = 20
CALLS = 40
CAP = .30
SEED = 20260928
COHORTS = ('expanded', 'crossover')


def jobs(d):
    rng = random.Random(d['seed'])
    for index in range(1,N+1):
        order=list(d['cells']);rng.shuffle(order)
        for c in order:
            yield f"{c['id']}/call_{index:04d}",c,index,c['replay_sources'][index-1]['seed']


def prepare(root):
    ledger=json.loads((PREVIOUS/'budget_ledger.json').read_bytes())
    if ledger['pending_requests'] or ledger['cumulative_conservative_charge_usd']+CAP>9:
        raise ValueError('Cap not covered')
    from run_validity_original_expanded import inventory as source_inventory
    sources = (('expanded',BASE/'original_expanded_20260911','MS_S2/canonical/v0.9'),
               ('crossover',PREVIOUS,'MS_S2/background_canonical/ms_canonical/v0.9'))
    cells=[];paths=[Path(__file__),PREVIOUS/'budget_ledger.json'];common=None
    for cohort,prior,cell_id in sources:
        mp=prior/'manifest.json';m=json.loads(mp.read_bytes());_,rows,_=source_inventory(prior,m)
        c=next(c for c in m['design']['cells'] if c['id']==cell_id)
        group=sorted([r for r in rows if r['cell_id']==cell_id],key=lambda r:r['call_index'])
        if len(group)!=20 or any(r['terminal_failure'] for r in group):raise ValueError('Source cohort incomplete')
        signature=(c['messages'],c['profile'],c['labels'],m['design']['model'],m['design']['temperature'],m['design']['max_tokens'])
        if common is not None and common!=signature:raise ValueError('Cohort requests differ beyond seeds')
        common=signature;refs=[]
        for i,r in enumerate(group,1):
            if r['call_index']!=i or r['attempts']!=1:raise ValueError('Source allocation mismatch')
            p=prior/'records'/(r['record_key']+'.json');paths.append(p)
            refs.append({'path':p.relative_to(ROOT).as_posix(),'record_key':r['record_key'],'seed':r['seed'],
                         'source_decision':r['parsed_decision'],'source_api_id':r['api_call_id'],
                         'source_timestamp':r['timestamp_utc'],'sha256':sha256(p.read_bytes()).hexdigest()})
        cells.append({'id':f'MS_S2/{cohort}_seeds/v0.9','cohort':cohort,'parameter':'MS','problem':'S2',
            'value':.9,'profile':c['profile'],'labels':c['labels'],'messages':c['messages'],'n':N,'replay_sources':refs})
        paths.append(mp);paths += [ROOT/p for p in m['design']['source_hashes']]
    if len({ref['seed'] for c in cells for ref in c['replay_sources']})!=40:raise ValueError('Source seed overlap')
    d={'experiment':'ms_exact_request_seed_replay','configuration':'neutral','model':base.MODEL,'provider':'openai',
       'temperature':1.,'max_tokens':600,'seed':SEED,'seed_role':'Ordering only; each API request reuses its historical seed.',
       'planned_calls':CALLS,'n_per_cell':N,'cells':cells,'spending_ceiling_usd':CAP,'prior_ledger':ledger,
       'transport_timeout_seconds':180,'pricing':m['design']['pricing'],
       'source_hashes':{p.relative_to(ROOT).as_posix():sha256(p.read_bytes()).hexdigest() for p in paths},
       'primary':'For each complete historical20-seed cohort, compare each new binary decision to its own saved decision with identical prompt/model/temperature/token limit/seed. Exact two-sided McNemar (binomial .5 on discordant pairs), Holm correction across two cohorts, alpha.05. Report gain/loss counts and paired risk change with conservative nominal95 union bounds on the two discordance proportions.',
       'secondary':'Compare the two replay cohorts in the current interleaved collection using a two-sided Fisher test and conservative nominal95 risk-difference interval; descriptive, no extra significance rule. Report match fraction; exact reproduction is not assumed or required by the provider.',
       'selection':'Both entire20-seed cohorts selected by prior run, not individual outcomes. Prior results14/20 versus0/20 are known; this is an exploratory diagnosis, not blind confirmation. Request replays are intentional new calls, never replacement of old records.',
       'collection':'20 shuffled two-cohort blocks, concurrency3, one attempt per slot,40 unique seeds within this new run. Original exact system and user prompts, all ten values. Historical requested seeds deliberately reused. No new text, tool or parameter interpretation.',
       'interpretation':'Different outcomes for matched requests challenge stable reproduction for these seeds, but do not identify backend drift. Fresh cohort difference could support seed-set sensitivity without explaining general validity. No monotonicity, equivalence or internal-understanding claim; original gate unchanged.',
       'stop_rule':'Any API, model, usage, budget, parse or request mismatch stops after current batch. Preserve attempts, no retries or optional extension.',
       'budget':'$0.30 maximum pre-dispatch reserve inside remaining $3.79170675 tracked allowance.'}
    d['full_dispatch_reserve_usd']=sum(base.reserve(c,d)*N for c in cells)
    if d['full_dispatch_reserve_usd']>CAP:raise ValueError('Full reserve exceeds cap')
    m=freeze(root/'manifest.json',d)
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


def assess(rows,m):
    cells=[];primary=[];complete=len(rows)==CALLS and all(not r['terminal_failure'] and r['parse_status']=='ok' for r in rows)
    for c in m['design']['cells']:
        group=[r for r in rows if r['cell_id']==c['id']]
        valid=[r for r in group if not r['terminal_failure'] and r['parse_status']=='ok']
        count=sum(r['parsed_decision']=='FORMAL_REPORT' for r in valid)
        old_count=sum(s['source_decision']=='FORMAL_REPORT' for s in c['replay_sources'])
        gains=losses=0
        for r in valid:
            prior=c['replay_sources'][r['call_index']-1]['source_decision']=='FORMAL_REPORT'
            now=r['parsed_decision']=='FORMAL_REPORT';gains+=int(now and not prior);losses+=int(prior and not now)
        s={'id':c['id'],'cohort':c['cohort'],'n_expected':N,'n_recorded':len(group),'n_valid':len(valid),
           'n_missing':N-len(group),'n_invalid':len(group)-len(valid),'adopt':count,'formal_report_count':count,
           'source_formal_report_count':old_count,'rate':count/len(valid) if valid else None,
           'wilson95':base.wilson(count,len(valid)),'gains':gains,'losses':losses,'matches':len(valid)-gains-losses}
        cells.append(s)
        terms=[({'adopt':k,'n_expected':N,'n_valid':len(valid),'rate':k/len(valid) if valid else None},weight)
               for k,weight in ((gains,1),(losses,-1))]
        p=float(binomtest(gains,gains+losses,.5,alternative='two-sided').pvalue) if gains+losses else 1.
        primary.append({'cohort':c['cohort'],'gains':gains,'losses':losses,'paired_change':base.contrast(terms),
                        'mcnemar_exact_p':p if complete and len(valid)==20 else None})
    complete=complete and all(c['n_valid']==20 for c in cells)
    for p,adj in zip(primary,holm([p['mcnemar_exact_p'] for p in primary]) if complete else [None,None]):
        p['holm_p']=adj;p['paired_change_detected']=adj<.05 if adj is not None else None
    a,b=cells
    secondary={'crossover_minus_expanded':base.contrast([(b,1),(a,-1)]),
        'descriptive_fisher_p':float(fisher_exact([[b['adopt'],20-b['adopt']],[a['adopt'],20-a['adopt']]]).pvalue) if complete else None}
    logging.basicConfig(level=logging.INFO)
    utils.log_dataframe_summary(pd.DataFrame(cells),f'All{len(rows)} records retained; source-paired valid counts explicitly shown',logging.getLogger('ms-seed-replay'))
    return {'design_hash':m['design_hash'],'status':'COMPLETE_SEED_REPLAY' if complete else 'INCOMPLETE_OR_INVALID',
            'n_records':len(rows),'n_valid':sum(c['n_valid'] for c in cells),'cells':cells,
            'primary_paired_comparisons':primary,'secondary_current_cohort_comparison':secondary,
            'known_cost_usd':sum(base.cost(r) or 0 for r in rows),'unknown_usage_calls':sum(base.cost(r) is None for r in rows),
            'phase_gate':'Unchanged; exact-request replay is a reproducibility diagnostic, not encoding validation.'}


def score(root, m):
    planned, rows, seen = inventory(root, m)
    intents = {}; row_map = {r['record_key']: r for r in rows}
    for path in (root / 'dispatches').rglob('*.json'):
        obj = json.loads(path.read_bytes()); key = obj['record_key']
        if key not in planned or key in intents or obj != intent(key, planned[key][0], m): raise ValueError('Intent mismatch')
        intents[key] = obj
    if not seen.issubset(intents): raise ValueError('Record without intent')
    reserved = sum(i['reserved_usd'] for i in intents.values())
    if reserved > CAP: raise ValueError('Reservations exceed cap')
    result = assess(rows, m)
    result['unresolved_dispatches'] = len(intents)-len(rows)
    save_new(root / 'analysis' / f'result_{digest(result)[:16]}.json', result)
    unknown = sum(i['reserved_usd'] for k, i in intents.items() if k not in row_map or base.cost(row_map[k]) is None)
    prior = m['design']['prior_ledger']; known = result['known_cost_usd']
    charge = prior['cumulative_conservative_charge_usd'] + known + unknown
    ledger = {'original_allowance_usd': 9, 'recorded_token_estimate_usd': known,
              'cumulative_token_estimate_usd': prior['cumulative_token_estimate_usd']+known,
              'unknown_usage_reserved_usd': prior['unknown_usage_reserved_usd']+unknown,
              'cumulative_conservative_charge_usd': charge, 'remaining_original_allowance_conservative_usd': 9-charge,
              'pending_requests': result['unresolved_dispatches'], 'provider_balance_verified': False}
    save_new(root / 'analysis' / f'budget_{digest(ledger)[:16]}.json', ledger)
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
            print(json.dumps({k: v for k, v in result.items() if k not in ('cells',)}, indent=2))


if __name__ == '__main__': main()
