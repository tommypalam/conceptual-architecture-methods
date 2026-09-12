"""Frozen MS stanza/background crossover: eight conditions, 160 calls."""
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
from run_validity_original_expanded import jobs, inventory, intent, holm

ROOT = base.ROOT
BASE = ROOT / 'experiments/phase1_5_encoding_validity'
PREVIOUS = BASE / 'original_expanded_20260911'
SOURCE = PREVIOUS / 'manifest.json'
N = 20
CALLS = 160
CAP = 1.20
SEED = 20260927
WORDINGS = ('canonical', 'paraphrase_2')


def swap_ms(background, donor):
    b, s = list(PARAMETER_RE.finditer(background)), list(PARAMETER_RE.finditer(donor))
    if len(b) != 10 or len(s) != 10: raise ValueError('Expected ten stanzas')
    if any(x.group(1, 2, 3) != y.group(1, 2, 3) for x, y in zip(b, s)):
        raise ValueError('Names, order or values differ')
    if b[8].group(1, 2) != ('9', 'Moral Scope'): raise ValueError('MS position mismatch')
    result = background[:b[8].start()] + s[8].group(0) + background[b[8].end():]
    after = list(PARAMETER_RE.finditer(result))
    if any(after[i].group(0) != (s if i == 8 else b)[i].group(0) for i in range(10)):
        raise ValueError('Unexpected stanza change')
    if PARAMETER_RE.sub('', background) != PARAMETER_RE.sub('', result):
        raise ValueError('Non-profile text changed')
    return result


def prepare(root):
    source = json.loads(SOURCE.read_bytes()); base.check(source)
    ledger = json.loads((PREVIOUS / 'budget_ledger.json').read_bytes())
    if ledger['pending_requests'] or ledger['cumulative_conservative_charge_usd'] + CAP > 9:
        raise ValueError('Prior allowance does not cover cap')
    cells = []
    for value in (.1, .9):
        originals = {w: next(c for c in source['design']['cells'] if
                     (c['parameter'], c['problem'], c['value'], c['wording']) == ('MS', 'S2', value, w)) for w in WORDINGS}
        a, b = originals.values()
        if a['profile'] != b['profile'] or a['messages'][1:] != b['messages'][1:]:
            raise ValueError('Source conditions differ outside wording')
        if PARAMETER_RE.sub('', a['messages'][0]['content']) != PARAMETER_RE.sub('', b['messages'][0]['content']):
            raise ValueError('Source non-profile text differs')
        for background in WORDINGS:
            for stanza in WORDINGS:
                original = originals[background]; messages = deepcopy(original['messages'])
                messages[0]['content'] = swap_ms(messages[0]['content'], originals[stanza]['messages'][0]['content'])
                if background == stanza and messages != original['messages']: raise ValueError('Control changed')
                cells.append({'id': f'MS_S2/background_{background}/ms_{stanza}/v{value:.1f}',
                    'parameter': 'MS', 'problem': 'S2', 'value': value, 'background': background,
                    'ms_stanza': stanza, 'profile': original['profile'], 'messages': messages,
                    'labels': original['labels'], 'n': N})
    paths = [Path(__file__), SOURCE, PREVIOUS / 'budget_ledger.json',
             ROOT / 'code/run_validity_original_expanded.py']
    paths += [ROOT / name for name in source['design']['source_hashes']]
    d = {'experiment': 'ms_stanza_background_crossover', 'configuration': 'neutral',
         'model': base.MODEL, 'provider': 'openai', 'temperature': 1., 'max_tokens': 600,
         'seed': SEED, 'planned_calls': CALLS, 'n_per_cell': N, 'cells': cells,
         'spending_ceiling_usd': CAP, 'prior_ledger': ledger, 'transport_timeout_seconds': 180,
         'source_hashes': {p.relative_to(ROOT).as_posix(): sha256(p.read_bytes()).hexdigest() for p in paths},
         'pricing': source['design']['pricing'],
         'primary': 'At MS=.9: four two-sided Fisher exact tests, Holm family alpha .05. P2-minus-canonical MS stanza within each fixed background; P2-minus-canonical background within each fixed MS stanza. Report risk differences and nominal conservative exact95 intervals. High value chosen because prior divergence was at .9, before these responses exist.',
         'secondary': 'Four high-minus-low MS endpoint effects and high-value difference-of-differences, descriptive with conservative nominal95 intervals. No additional significance decisions. No monotonicity claim from two levels.',
         'selection': 'Exploratory attribution after observed canonical/P2 MS/S2 divergence. Fresh concurrent full-template controls; no historical pooling. Fixed other-nine values are a specific mean profile, not absent traits.',
         'interpretation': 'No overall pass or repair rule. Isolates effects of wording blocks conditional on counterpart; does not isolate semantic content from lexical emphasis or length. Non-detection is not invariance. No replacement of original gate, active-trait recovery or internal understanding claim.',
         'collection': '20 shuffled eight-condition blocks, concurrency3, unique seeds, original system delivery, one attempt per slot. All ten descriptions verbatim; only approved MS stanza recombined with approved background. Locked S2 and numeric profiles unchanged.',
         'stop_rule': 'Any API/model/usage/reservation/parse failure stops after current batch. Preserve all attempts. No retries, replacement, optional extension or automatic recovery.',
         'budget': 'Full-price pre-dispatch reservations, $1.20 cap inside remaining tracked allowance. Provider balance unverified.'}
    if len(cells)*N != CALLS: raise ValueError('Allocation mismatch')
    d['full_dispatch_reserve_usd'] = sum(base.reserve(c, d)*N for c in cells)
    if d['full_dispatch_reserve_usd'] > CAP: raise ValueError('Full reserve exceeds cap')
    m = freeze(root / 'manifest.json', d)
    save_new(root / 'request_preview.json', {'design_hash': m['design_hash'], 'cells': cells})
    return m


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


def assess(rows, m):
    cells = []
    for c in m['design']['cells']:
        group = [r for r in rows if r['cell_id'] == c['id']]
        valid = [r for r in group if not r['terminal_failure'] and r['parse_status'] == 'ok']
        count = sum(r['parsed_decision'] == 'FORMAL_REPORT' for r in valid)
        cells.append({k: c[k] for k in ('id', 'value', 'background', 'ms_stanza')} | {
            'n_expected': N, 'n_recorded': len(group), 'n_valid': len(valid),
            'n_missing': N-len(group), 'n_invalid': len(group)-len(valid),
            'adopt': count, 'formal_report_count': count,
            'rate': count/len(valid) if valid else None, 'wilson95': base.wilson(count, len(valid))})
    logging.basicConfig(level=logging.INFO)
    utils.log_dataframe_summary(pd.DataFrame(cells),
        f'All {len(rows)} recorded responses retained; eight groups; valid counts shown before/after filtering. adopt means FORMAL_REPORT for helper compatibility.', logging.getLogger('ms-crossover'))
    lookup = {(c['background'], c['ms_stanza'], c['value']): c for c in cells}
    complete = len(rows) == CALLS and all(c['n_valid'] == N for c in cells)
    primary = []
    for component in ('ms_stanza', 'background'):
        for fixed in WORDINGS:
            a, b = [lookup[(fixed, w, .9) if component == 'ms_stanza' else (w, fixed, .9)] for w in WORDINGS]
            p = float(fisher_exact([[b['adopt'], N-b['adopt']], [a['adopt'], N-a['adopt']]], alternative='two-sided').pvalue) if complete else None
            primary.append({'varied_component': component, 'fixed_counterpart': fixed,
                'effect_p2_minus_canonical': base.contrast([(b, 1), (a, -1)]), 'two_sided_fisher_p': p})
    for p, adj in zip(primary, holm([p['two_sided_fisher_p'] for p in primary]) if complete else [None]*4):
        p['holm_p'] = adj; p['difference_detected'] = adj < .05 if adj is not None else None
    endpoints = [{'background': bg, 'ms_stanza': ms, 'high_minus_low': base.contrast([
        (lookup[bg, ms, .9], 1), (lookup[bg, ms, .1], -1)])} for bg in WORDINGS for ms in WORDINGS]
    c, p = WORDINGS
    interaction = base.contrast([(lookup[p,p,.9], 1), (lookup[p,c,.9], -1),
                                (lookup[c,p,.9], -1), (lookup[c,c,.9], 1)])
    return {'design_hash': m['design_hash'], 'status': 'COMPLETE_CROSSOVER' if complete else 'INCOMPLETE_OR_INVALID',
            'n_records': len(rows), 'n_valid': sum(c['n_valid'] for c in cells), 'cells': cells,
            'primary_four_comparisons': primary, 'secondary_endpoint_effects': endpoints,
            'secondary_high_value_interaction': interaction,
            'known_cost_usd': sum(base.cost(r) or 0 for r in rows),
            'unknown_usage_calls': sum(base.cost(r) is None for r in rows),
            'phase_gate': 'Unchanged; diagnostic attribution is not validation or internal understanding.'}


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
            print(json.dumps({k: v for k, v in result.items() if k not in ('cells', 'primary_four_comparisons', 'secondary_endpoint_effects')}, indent=2))


if __name__ == '__main__': main()
