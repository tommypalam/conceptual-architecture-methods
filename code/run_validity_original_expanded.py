"""Frozen 640-call original-delivery comparison across two positive cases and PD stress."""
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

ROOT = base.ROOT
BASE = ROOT / 'experiments/phase1_5_encoding_validity'
SOURCE = BASE / 'option_c_20260909_restart/manifest.json'
TEMPLATES = BASE / 'claude_paraphrases_20260909_theory_r5/paraphrases_approved.json'
PREVIOUS = BASE / 'tool_delivery_20260911'
WORDINGS = ('canonical', 'paraphrase_1', 'paraphrase_2', 'paraphrase_3')
CASES = (('MoR', 'S3', (.1, .5, .9)), ('MS', 'S2', (.1, .5, .9)), ('PD', 'S3', (.1, .9)))
N = 20
CALLS = 640
CAP = 4.50
SEED = 20260926


def jobs(d):
    rng = random.Random(d['seed'])
    for index in range(1, N + 1):
        order = list(d['cells']); rng.shuffle(order)
        for c in order:
            key = f"{c['id']}/call_{index:04d}"
            yield key, c, index, derive_seed(d['seed'], c['id'], index)


def prepare(root):
    source = json.loads(SOURCE.read_bytes())
    if digest(source['design']) != source['design_hash']: raise ValueError('Source design mismatch')
    ledger = json.loads((PREVIOUS / 'budget_ledger.json').read_bytes())
    if ledger['pending_requests'] or ledger['cumulative_conservative_charge_usd'] + CAP > 9:
        raise ValueError('Prior allowance does not cover cap')
    templates = load_reviewed_paraphrases(TEMPLATES); cells = []
    for parameter, problem, values in CASES:
        for value in values:
            old = next(c for c in source['design']['cells'] if
                       (c['arm'], c['parameter'], c['problem'], c['value']) ==
                       ('full_harness', parameter, problem, value))
            canonical, provenance = variant_prompt(parameter, value, 'hybrid')
            if canonical != old['messages'][0]['content'] or provenance['parameter_values'] != old['profile']:
                raise ValueError('Canonical source reconstruction mismatch')
            for wording in WORDINGS:
                system, p = variant_prompt(parameter, value, 'hybrid', template=templates.get(wording))
                if p['parameter_values'] != old['profile']: raise ValueError('Profile changed')
                messages = deepcopy(old['messages']); messages[0]['content'] = system
                cells.append({'id': f'{parameter}_{problem}/{wording}/v{value:.1f}',
                              'parameter': parameter, 'problem': problem, 'value': value,
                              'wording': wording, 'profile': old['profile'], 'messages': messages,
                              'labels': old['labels'], 'n': N})
    paths = [Path(__file__), SOURCE, TEMPLATES, PREVIOUS / 'budget_ledger.json',
             ROOT / 'code/run_validity_evidence_screen.py', ROOT / 'code/run_validity_tool_delivery.py',
             ROOT / 'code/run_validity_claude.py', ROOT / 'code/engine/validity_variants.py',
             ROOT / 'code/engine/validity_sweep.py', ROOT / 'code/engine/record_sink.py',
             ROOT / 'code/engine/llm_client.py', ROOT / 'code/engine/seeding.py',
             ROOT / 'code/engine/parsing.py', ROOT / 'code/engine/prompt_assembly.py',
             ROOT / 'code/engine/phase0b.py', ROOT / 'docs/variables.json']
    d = {'experiment': 'original_delivery_expanded_selected_cases', 'configuration': 'neutral',
         'model': base.MODEL, 'provider': 'openai', 'temperature': 1., 'max_tokens': 600,
         'seed': SEED, 'planned_calls': CALLS, 'n_per_cell': N, 'cells': cells,
         'spending_ceiling_usd': CAP, 'prior_ledger': ledger, 'transport_timeout_seconds': 180,
         'source_hashes': {p.relative_to(ROOT).as_posix(): sha256(p.read_bytes()).hexdigest() for p in paths},
         'pricing': json.loads((PREVIOUS / 'manifest.json').read_bytes())['design']['pricing'],
         'primary': 'Eight high-minus-low endpoint effects: MoR/S3 and MS/S2 x all four wordings. One-sided Fisher exact tests for increased first-option probability; Holm adjustment across all eight, alpha.05. Positive directions come from existing prespecified hypotheses. Each effect also reports an exact conservative nominal95 interval; intervals are not Holm-adjusted.',
         'secondary': 'Within each of eight fixed parameter/value/problem contexts, all six wording differences.32 Bonferroni exact cell intervals give simultaneous>=95 coverage for all48 differences, including missing-outcome envelopes. Interval entirely outside[-.10,.10] identifies gross wording divergence. Failure to detect it is not equivalence. PD endpoint effects are two-sided descriptive contrasts, with no new directional hypothesis.',
         'midpoints': 'For MoR/MS report all three rates and observed order, including ties. Three points do not establish the original five-point monotonicity criterion; no separate midpoint significance test.',
         'interpretation': 'Report which of the eight directional hypotheses replicate and which wordings/cases limit transport. Completion is not validation. No new combined pass rule, alteration of original24/30 equivalence gate or automatic expansion.',
         'selection': 'MoR/S3 and MS/S2 selected from previously responsive cases; PD/S3 deliberately retained as known wording stress. Fresh selected-case replication, not held-out case selection, ten-parameter validation or full sweep.',
         'collection': '20 shuffled complete32-condition blocks, concurrency3, unique requested seeds, one attempt per slot. Original system-role delivery and SDK; no tools, bridge, prompt revisions, meaning changes or historical pooling.',
         'stop_rule': 'Any API/model/usage/reservation/parse failure stops after current batch; preserve all attempts and invalidate study. No retries, in-place replacement, optional sample extension or partial-run auto-recovery.',
         'budget': 'Reserve every batch at full token prices before sending. Prior conservative charge plus$4.50 cap below latest$9 allowance. Unknown usage retains reservation; provider balance unverified.'}
    if len(cells) * N != CALLS: raise ValueError('Allocation mismatch')
    d['full_dispatch_reserve_usd'] = sum(base.reserve(c, d) * N for c in cells)
    if d['full_dispatch_reserve_usd'] > CAP: raise ValueError('Full reserve exceeds cap')
    m = freeze(root / 'manifest.json', d)
    save_new(root / 'request_preview.json', {'design_hash': m['design_hash'], 'cells': cells})
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


def intent(key, cell, m):
    return {'record_key': key, 'design_hash': m['design_hash'], 'messages_hash': digest(cell['messages']),
            'reserved_usd': base.reserve(cell, m['design'])}


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


def holm(pvalues):
    order = sorted(range(len(pvalues)), key=pvalues.__getitem__); result = [None] * len(pvalues); previous = 0.
    for rank, i in enumerate(order):
        previous = max(previous, min(1., (len(pvalues) - rank) * pvalues[i])); result[i] = previous
    return result


def assess(rows, m):
    cells = []
    for c in m['design']['cells']:
        group = [r for r in rows if r['cell_id'] == c['id']]
        valid = [r for r in group if not r['terminal_failure'] and r['parse_status'] == 'ok']
        count = sum(r['parsed_decision'] == c['labels'][0] for r in valid); unknown = N - len(valid)
        tail = .05 / (2 * 32)
        ci = [0. if count == 0 else float(beta.ppf(tail, count, N-count+1)),
              1. if count+unknown == N else float(beta.ppf(1-tail, count+unknown+1, N-count-unknown))]
        cells.append({k: c[k] for k in ('id', 'parameter', 'problem', 'value', 'wording', 'labels')} | {
            'n_expected': N, 'n_recorded': len(group), 'n_valid': len(valid), 'n_missing': N-len(group),
            'n_invalid': len(group)-len(valid), 'adopt': count, 'first_option_count': count,
            'rate': count/len(valid) if valid else None, 'wilson95': base.wilson(count, len(valid)),
            'simultaneous95_cell_interval_unknown_envelope': ci})
    logging.basicConfig(level=logging.INFO)
    utils.log_dataframe_summary(pd.DataFrame(cells), 'All32 conditions retained; first-option count called adopt only for compatibility with exact-contrast helper', logging.getLogger('original-expanded'))
    lookup = {(c['parameter'], c['wording'], c['value']): c for c in cells}
    complete = len(rows) == CALLS and all(c['n_valid'] == N for c in cells)
    primary = []
    for parameter in ('MoR', 'MS'):
        for wording in WORDINGS:
            lo, mid, hi = [lookup[parameter, wording, v] for v in (.1, .5, .9)]
            p = float(fisher_exact([[hi['adopt'], N-hi['adopt']], [lo['adopt'], N-lo['adopt']]], alternative='greater').pvalue) if complete else None
            primary.append({'parameter': parameter, 'problem': lo['problem'], 'wording': wording,
                'first_option': lo['labels'][0], 'endpoint_effect': base.contrast([(hi, 1), (lo, -1)]),
                'one_sided_fisher_p': p, 'three_observed_rates': [c['rate'] for c in (lo, mid, hi)],
                'observed_nondecreasing': bool(lo['rate'] <= mid['rate'] <= hi['rate']) if complete else None})
    adjusted = holm([p['one_sided_fisher_p'] for p in primary]) if complete else [None] * 8
    for p, adj in zip(primary, adjusted):
        p['holm_p'] = adj; p['positive_direction_established'] = adj < .05 if adj is not None else None
    pairs = []
    for parameter, problem, values in CASES:
        for value in values:
            for a, b in combinations(WORDINGS, 2):
                ca, cb = lookup[parameter, a, value], lookup[parameter, b, value]
                la, ha = ca['simultaneous95_cell_interval_unknown_envelope']; lb, hb = cb['simultaneous95_cell_interval_unknown_envelope']
                ci = [lb-ha, hb-la]
                pairs.append({'parameter': parameter, 'problem': problem, 'value': value, 'a': a, 'b': b,
                    'difference_b_minus_a': cb['rate']-ca['rate'] if ca['rate'] is not None and cb['rate'] is not None else None,
                    'simultaneous95_interval_unknown_envelope': ci, 'gross_difference_over_10pp': ci[0] > .1 or ci[1] < -.1})
    result = {'design_hash': m['design_hash'], 'status': 'COMPLETE_SELECTED_CASE_REPLICATION' if complete else 'INCOMPLETE_OR_INVALID',
              'n_records': len(rows), 'n_valid': sum(c['n_valid'] for c in cells), 'cells': cells,
              'primary_eight_endpoint_effects': primary, 'n_positive_directions_established': sum(p['positive_direction_established'] is True for p in primary),
              'secondary_wording_pairs': pairs, 'n_gross_wording_differences': sum(p['gross_difference_over_10pp'] for p in pairs),
              'secondary_pd_endpoint_effects': {w: base.contrast([(lookup['PD', w, .9], 1), (lookup['PD', w, .1], -1)]) for w in WORDINGS},
              'known_cost_usd': sum(base.cost(r) or 0 for r in rows), 'unknown_usage_calls': sum(base.cost(r) is None for r in rows),
              'phase_gate': 'Unchanged. Completion and positive endpoint effects do not establish equivalence, five-point gradients, representation retention or active-trait recoverability.'}
    return result


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
            print(json.dumps({k: v for k, v in result.items() if k not in ('cells', 'secondary_wording_pairs', 'primary_eight_endpoint_effects', 'secondary_pd_endpoint_effects')}, indent=2))


if __name__ == '__main__': main()
