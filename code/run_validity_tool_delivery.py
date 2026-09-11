"""Isolated, budget-bounded comparison of original and read-only tool delivery."""
import argparse
import asyncio
from copy import deepcopy
from hashlib import sha256
from itertools import combinations
import json
import logging
from pathlib import Path
import random
import time
import zipfile

import httpx
import numpy as np
import pandas as pd
import utils
from engine.llm_client import utc_now_iso
from engine.parsing import parse_decision
from engine.seeding import derive_seed
from engine.validity_sweep import digest, freeze, ValiditySink
from engine.validity_variants import load_reviewed_paraphrases, variant_prompt
from research_support.profile_delivery import (
    BRIDGE, Specification, FixedSpecificationProvider, tool_schema, decision_messages)
from run_validity_claude import save_new
import run_validity_evidence_screen as base

ROOT = base.ROOT
BASE = ROOT / 'experiments/phase1_5_encoding_validity'
SOURCE = BASE / 'option_c_20260909_restart/manifest.json'
PREVIOUS = BASE / 'joint_wording_20260911'
TEMPLATES = BASE / 'claude_paraphrases_20260909_theory_r5/paraphrases_approved.json'
WORDINGS = ('canonical', 'paraphrase_1', 'paraphrase_2', 'paraphrase_3')
DELIVERIES = ('system', 'tool')
PARAMETERS = ('MoR', 'PD')
N = 10
CAP = 3.50
SEED = 20260924
URL = 'https://api.openai.com/v1/chat/completions'


def payload(messages, seed, retrieve=False):
    result = {'model': base.MODEL, 'messages': deepcopy(messages), 'temperature': 1.,
              'max_completion_tokens': 128 if retrieve else 600, 'seed': seed}
    if retrieve:
        result.update(tools=[tool_schema()], parallel_tool_calls=False,
                      tool_choice={'type': 'function', 'function': {'name': 'read_agent_specification'}})
    return result


def initial(cell):
    if cell['delivery'] == 'system':
        return deepcopy(cell['messages'])
    return [{'role': 'system', 'content': BRIDGE}, *deepcopy(cell['messages'][1:])]


def provider(cell):
    text = cell['messages'][0]['content']
    return FixedSpecificationProvider(Specification(text, sha256(text.encode('utf-8')).hexdigest()))


def reserve(request):
    # UTF-8 byte upper bound plus 2,048 tokens for provider message/tool framing.
    size = len(json.dumps(request, ensure_ascii=False).encode('utf-8'))
    return ((size + 2048) * .75 + request['max_completion_tokens'] * 4.5) / 1e6


def cell_reserve(cell):
    first = payload(initial(cell), 4294967295, cell['delivery'] == 'tool')
    if cell['delivery'] == 'system':
        return reserve(first)
    # The adapter caps the serialized assistant call at 1024 UTF-8 bytes.
    # Extra 2048 bytes cover that turn plus the duplicated tool-call ID/framing.
    final = payload([*initial(cell), {'role': 'tool', 'content': provider(cell).read().text}], 4294967295)
    return reserve(first) + reserve(final) + 2048 * .75 / 1e6


def jobs(d):
    rng = random.Random(d['seed'])
    for i in range(1, d['n_per_cell'] + 1):
        order = list(d['cells']); rng.shuffle(order)
        for c in order:
            key = f"{c['id']}/decision_{i:04d}"
            yield key, c, i, derive_seed(d['seed'], c['id'], i)


def prepare(root):
    old = json.loads(SOURCE.read_bytes())
    if digest(old['design']) != old['design_hash']:
        raise ValueError('Original design mismatch')
    ledger = json.loads((PREVIOUS / 'budget_ledger.json').read_bytes())
    if ledger['pending_requests'] or ledger['cumulative_conservative_charge_usd'] + CAP > 9:
        raise ValueError('Allowance insufficient')
    templates = load_reviewed_paraphrases(TEMPLATES)
    cells = []
    for parameter in PARAMETERS:
        for value in (.1, .9):
            source = next(c for c in old['design']['cells'] if
                          (c['arm'], c['parameter'], c['problem'], c['value']) ==
                          ('full_harness', parameter, 'S3', value))
            canonical, provenance = variant_prompt(parameter, value, 'hybrid')
            if canonical != source['messages'][0]['content'] or provenance['parameter_values'] != source['profile']:
                raise ValueError('Original prompt reconstruction mismatch')
            for wording in WORDINGS:
                system, p = variant_prompt(parameter, value, 'hybrid', template=templates.get(wording))
                if p['parameter_values'] != source['profile']:
                    raise ValueError('Wording changed profile')
                for delivery in DELIVERIES:
                    messages = deepcopy(source['messages']); messages[0]['content'] = system
                    cells.append({'id': f'{delivery}/{parameter}_{value:.1f}/{wording}',
                                  'delivery': delivery, 'parameter': parameter, 'value': value,
                                  'wording': wording, 'problem': 'S3', 'labels': source['labels'],
                                  'profile': source['profile'], 'messages': messages})
    paths = [Path(__file__), ROOT / 'code/research_support/profile_delivery.py', SOURCE,
             TEMPLATES, PREVIOUS / 'budget_ledger.json', ROOT / 'code/engine/validity_variants.py',
             ROOT / 'code/engine/parsing.py', ROOT / 'code/engine/seeding.py',
             ROOT / 'code/engine/validity_sweep.py', ROOT / 'code/engine/record_sink.py',
             ROOT / 'code/run_validity_claude.py', ROOT / 'code/run_validity_evidence_screen.py',
             ROOT / 'code/engine/prompt_assembly.py', ROOT / 'code/engine/phase0b.py',
             ROOT / 'docs/variables.json']
    # The old manifest uses historical basename-only code hashes. Preserve it
    # unchanged as a hashed source; pin the actual current runner dependencies
    # with root-relative paths, rather than claiming that old code is executing.
    hashes = {p.relative_to(ROOT).as_posix(): sha256(p.read_bytes()).hexdigest() for p in paths}
    d = {'experiment': 'fixed_specification_tool_delivery_screen', 'configuration': 'neutral',
         'model': base.MODEL, 'seed': SEED, 'n_per_cell': N, 'cells': cells, 'source_hashes': hashes,
         'planned_decisions': len(cells) * N, 'maximum_api_calls': len(cells) * N * 3 // 2,
         'temperature': 1., 'final_max_tokens': 600, 'retrieval_max_tokens': 128,
         'spending_ceiling_usd': CAP, 'prior_ledger': ledger, 'bridge': BRIDGE, 'tool_schema': tool_schema(),
         'endpoint': URL, 'timeout_seconds': 180, 'concurrency': 3,
         'primary': 'Tool minus system mean pairwise squared wording difference, averaged equally over MoR/PD x .1/.9 and all six wording pairs. Unbiased binomial U-statistic; 10,000 stratified binomial bootstrap replicates, percentile95 interval, seed20260925. Negative favours tool delivery. Exploratory candidate screen, not equivalence.',
         'promotion_rule': 'Complete valid screen; primary bootstrap upper95 bound below zero; canonical tool MoR endpoint effect >=.20 and >=50% of positive concurrent canonical system effect; average tool MoR effect across all four wordings >=.20. Only warrants broader confirmation, never passes Phase1.5. Otherwise no automatic expansion.',
         'scope': 'MoR/S3 previously responsive; PD/S3 previously wording-sensitive. Selected development cases, not held-out validation. No new PD direction hypothesis. Two endpoints do not assess monotonicity. All ten parameters and original exact text retained.',
         'mechanism': 'Forced genuine function call, empty arguments, fixed assigned specification returned verbatim. No redrawing, answer scoring, trait weighting, text normalization, retrieval selection, feedback or correction.',
         'limitations': 'Delivery changes role, position, bridge instruction and number of turns together. Does not identify the mechanism of any improvement or show internal ethical understanding. Future null-harness, full curves, representation tests, independent coding and all30 equivalence cells remain required.',
         'stopping': 'One attempt per API slot, no retries. Any API, usage, model, tool-shape, wire, or parse failure stops after current batch and invalidates screen. No replacement, optional stopping on outcomes, pooling or automatic wider sweep.',
         'wire_policy': 'Store the exact serialized JSON request body before every send; compare decoded body to frozen request. No credentials or request headers stored. Final tool-call ID and arguments come from the actual model response.',
         'pricing': json.loads((PREVIOUS / 'manifest.json').read_bytes())['design']['pricing']}
    d['full_dispatch_reserve_usd'] = sum(cell_reserve(c) * N for c in cells)
    if d['full_dispatch_reserve_usd'] > CAP:
        raise ValueError(f"Reserve {d['full_dispatch_reserve_usd']:.6f} exceeds cap")
    m = freeze(root / 'manifest.json', d)
    save_new(root / 'request_preview.json', {'design_hash': m['design_hash'], 'bridge': BRIDGE,
             'tool_schema': tool_schema(), 'cells': cells,
             'dynamic_fields': 'The returned assistant tool call and ID are recorded verbatim before the final decision request. The tool content is exactly messages[0].content; no generated specification.'})
    return m


def check(m):
    base.check(m)
    if m['design']['bridge'] != BRIDGE or m['design']['tool_schema'] != tool_schema():
        raise ValueError('Delivery contract changed')


async def api_call(client, root, m, key, request):
    intent_path = root / 'dispatches' / (key + '.json')
    if intent_path.exists():
        raise ValueError('Existing API intent; never retry in place')
    wire = client.build_request('POST', URL, json=request)
    body = wire.content.decode('utf-8')
    if json.loads(body) != request:
        raise ValueError('Serialized request mismatch')
    bound = reserve(request)
    save_new(intent_path, {'key': key, 'design_hash': m['design_hash'], 'request': request,
                          'wire_body': body, 'reserved_usd': bound})
    started = time.monotonic(); response = None; data = None; error = None
    try:
        response = await client.send(wire)
        data = response.json()
        response.raise_for_status()
        if data.get('model') != base.MODEL or not data.get('id'):
            raise ValueError('Model or API ID mismatch')
        usage = base.cost({'response_payload': data})
        if usage is None or usage > bound:
            raise ValueError('Missing usage or reservation exceeded')
    except Exception as exc:
        error = f'{type(exc).__name__}: {exc}'
    r = {'record_key': key, 'design_hash': m['design_hash'], 'request': request,
         'wire_body': body, 'response_payload': data, 'error': error, 'attempts': 1,
         'timestamp_utc': utc_now_iso(), 'latency_s': time.monotonic() - started,
         'http_status': response.status_code if response is not None else None,
         'request_id': response.headers.get('x-request-id') if response is not None else None,
         'response_text': response.text if response is not None else None}
    r['record_hash'] = digest(r)
    sink = ValiditySink(root / 'records'); sink.write(key, r)
    if error:
        sink.write_failure({'record_key': key, 'error': error})
        raise RuntimeError('API failure preserved; stop')
    return data


async def execute(root, m, client):
    check(m); d = m['design']; allocation = list(jobs(d))
    # This design deliberately has no automatic partial-run recovery.
    if any((root / 'dispatches').rglob('*.json')) or any((root / 'decisions').rglob('*.json')):
        raise ValueError('Existing allocation; inspect it rather than rerunning')
    if sum(cell_reserve(c) for _, c, _, _ in allocation) > d['spending_ceiling_usd']:
        raise ValueError('Pre-dispatch spending guard')
    all_seeds = [derive_seed(seed, stage) for _, c, _, seed in allocation
                 for stage in (('retrieve', 'decision') if c['delivery'] == 'tool' else ('decision',))]
    if len(set(all_seeds)) != len(all_seeds):
        raise ValueError('Seed collision')
    async def one(job):
        key, cell, i, seed = job
        messages = initial(cell); spent_reserve = 0.; stages = []; error = None; text = None
        try:
            if cell['delivery'] == 'tool':
                request = payload(messages, derive_seed(seed, 'retrieve'), True)
                spent_reserve += reserve(request); stages.append(key + '/retrieve')
                data = await api_call(client, root, m, stages[-1], request)
                if data['choices'][0]['finish_reason'] != 'tool_calls':
                    raise ValueError('Retrieval did not finish with a tool call')
                messages = decision_messages(messages, data['choices'][0]['message'], provider(cell))
            request = payload(messages, derive_seed(seed, 'decision'))
            if spent_reserve + reserve(request) > cell_reserve(cell):
                raise ValueError('Final dynamic request exceeds frozen cell reservation')
            stages.append(key + '/decision')
            data = await api_call(client, root, m, stages[-1], request)
            message = data['choices'][0]['message']; text = message.get('content')
            if message.get('tool_calls') or data['choices'][0]['finish_reason'] != 'stop':
                raise ValueError('Invalid final response shape')
            decision, parse = parse_decision(text, tuple(cell['labels']))
            if parse != 'ok':
                raise ValueError('Final decision parse failed')
        except Exception as exc:
            error = f'{type(exc).__name__}: {exc}'; decision = None; parse = 'failed'
        r = {'record_key': key, 'design_hash': m['design_hash'], 'cell_id': cell['id'],
             'index': i, 'seed': seed, 'api_stages': stages, 'raw_response': text,
             'parsed_decision': decision, 'parse_status': parse, 'error': error}
        r['record_hash'] = digest(r); ValiditySink(root / 'decisions').write(key, r)
        if error:
            ValiditySink(root / 'decisions').write_failure({'record_key': key, 'error': error})
        return r
    completed = 0
    for start in range(0, len(allocation), 3):
        batch = await asyncio.gather(*(one(j) for j in allocation[start:start + 3]))
        completed += len(batch)
        if completed % 15 == 0 or completed == 3 or completed == len(allocation):
            print(f'{completed}/{len(allocation)} decisions saved', flush=True)
        if any(r['error'] for r in batch):
            raise RuntimeError('Failure preserved; screen stopped after current batch')


def wording_stat(counts, n):
    """Shape (..., delivery, parameter, endpoint, wording). Do not clip negatives."""
    p = counts / n
    unbiased_square = counts * (counts - 1) / (n * (n - 1))
    terms = [unbiased_square[..., a] + unbiased_square[..., b] - 2 * p[..., a] * p[..., b]
             for a, b in combinations(range(4), 2)]
    return np.mean(np.stack(terms, axis=-1), axis=(-3, -2, -1))


def verify_inventory(root, m, records, rows):
    planned = {key: (c, i, seed) for key, c, i, seed in jobs(m['design'])}
    api = {r['record_key']: r for r in records}
    if len(api) != len(records): raise ValueError('Duplicate API records')
    intents = {}
    for path in (root / 'dispatches').rglob('*.json'):
        intent = json.loads(path.read_bytes()); key = intent['key']
        if key in intents: raise ValueError('Duplicate intents')
        decision_key, stage = key.rsplit('/', 1)
        if decision_key not in planned or stage not in ('retrieve', 'decision'):
            raise ValueError('Unexpected API allocation')
        cell, _, seed = planned[decision_key]; messages = initial(cell)
        if stage == 'retrieve' and cell['delivery'] != 'tool':
            raise ValueError('System arm unexpectedly called tool')
        if stage == 'decision' and cell['delivery'] == 'tool':
            retrieved = api[decision_key + '/retrieve']['response_payload']
            messages = decision_messages(messages, retrieved['choices'][0]['message'], provider(cell))
        expected = payload(messages, derive_seed(seed, stage), stage == 'retrieve')
        if (intent['design_hash'] != m['design_hash'] or intent['request'] != expected
                or json.loads(intent['wire_body']) != expected or intent['reserved_usd'] != reserve(expected)):
            raise ValueError('Frozen request or wire mismatch')
        intents[key] = intent
    ids = []
    for key, r in api.items():
        if key not in intents or r['design_hash'] != m['design_hash'] or r['attempts'] != 1:
            raise ValueError('API provenance mismatch')
        if r['request'] != intents[key]['request'] or r['wire_body'] != intents[key]['wire_body']:
            raise ValueError('Recorded request differs from intent')
        if not r['error']:
            data = r['response_payload']; ids.append(data['id'])
            if data['model'] != base.MODEL or json.loads(r['response_text']) != data:
                raise ValueError('Raw provider payload mismatch')
    if len(set(ids)) != len(ids): raise ValueError('Duplicate API response IDs')
    for r in rows:
        c, i, seed = planned[r['record_key']]
        if (r['cell_id'], r['index'], r['seed']) != (c['id'], i, seed):
            raise ValueError('Decision assignment mismatch')
        if not r['error']:
            final = api[r['record_key'] + '/decision']['response_payload']['choices'][0]['message']['content']
            if final != r['raw_response'] or parse_decision(final, tuple(c['labels'])) != (r['parsed_decision'], r['parse_status']):
                raise ValueError('Reparsed decision mismatch')
    reserved = sum(i['reserved_usd'] for i in intents.values())
    if reserved > m['design']['spending_ceiling_usd']:
        raise ValueError('Total reservations exceed cap')
    return intents


def score(root, m):
    check(m); d = m['design']
    records = list(ValiditySink(root / 'records').read_all())
    rows = list(ValiditySink(root / 'decisions').read_all())
    expected = {key: c for key, c, _, _ in jobs(d)}
    if len({r['record_key'] for r in rows}) != len(rows) or any(r['record_key'] not in expected or r['design_hash'] != m['design_hash'] for r in rows):
        raise ValueError('Unexpected decision provenance')
    intents = verify_inventory(root, m, records, rows)
    cells = []; counts = np.zeros((2, 2, 2, 4), dtype=int)
    for c in d['cells']:
        group = [r for r in rows if r['cell_id'] == c['id']]
        valid = [r for r in group if not r['error'] and r['parse_status'] == 'ok']
        k = sum(r['parsed_decision'] == 'ADOPT' for r in valid)
        ix = (DELIVERIES.index(c['delivery']), PARAMETERS.index(c['parameter']), (0 if c['value'] == .1 else 1), WORDINGS.index(c['wording']))
        counts[ix] = k
        cells.append({k_: c[k_] for k_ in ('id', 'delivery', 'parameter', 'value', 'wording')} | {
            'n_expected': N, 'n_recorded': len(group), 'n_valid': len(valid), 'adopt': k,
            'rate': k / len(valid) if valid else None, 'wilson95': base.wilson(k, len(valid))})
    logging.basicConfig(level=logging.INFO)
    utils.log_dataframe_summary(pd.DataFrame(cells), 'All32 planned cells retained; invalid and missing slots counted', logging.getLogger('tool-delivery'))
    complete = (len(rows) == d['planned_decisions'] and all(c['n_valid'] == N for c in cells)
                and len(records) == len(intents) == d['maximum_api_calls'] and not any(r['error'] for r in records))
    result = {'design_hash': m['design_hash'], 'n_decisions': len(rows), 'n_api_records': len(records),
              'status': 'INCOMPLETE_OR_INVALID', 'cells': cells,
              'known_cost_usd': sum(base.cost(r) or 0 for r in records),
              'unknown_usage_calls': sum(base.cost(r) is None for r in records),
              'unresolved_dispatches': len(intents) - len(records),
              'exact_requests_wire_profiles_raw_payloads_and_parses_verified': True,
              'phase_gate': 'Unchanged and unmet. This selected screen cannot validate the architecture.'}
    if complete:
        point = wording_stat(counts, N)
        rng = np.random.default_rng(SEED + 1)
        simulations = rng.binomial(N, counts / N, size=(10000, *counts.shape))
        boot = wording_stat(simulations, N)
        interval = np.quantile(boot[:, 1] - boot[:, 0], [.025, .975]).tolist()
        mor_effects = (counts[:, 0, 1, :] - counts[:, 0, 0, :]) / N
        safeguard = (mor_effects[0, 0] > 0 and mor_effects[1, 0] >= .2
                     and mor_effects[1, 0] >= .5 * mor_effects[0, 0]
                     and mor_effects[1].mean() >= .2)
        result.update(primary_tool_minus_system=float(point[1] - point[0]),
                      exploratory_bootstrap95=interval, mor_effects_by_delivery_and_wording=mor_effects.tolist(),
                      sensitivity_safeguard=bool(safeguard),
                      status='CANDIDATE_FOR_BROADER_CONFIRMATION' if interval[1] < 0 and safeguard else 'NO_SCALE_UP_SUPPORT')
    save_new(root / 'analysis' / f'screen_{digest(result)[:16]}.json', result)
    known = result['known_cost_usd']; record_by_key = {r['record_key']: r for r in records}
    unknown = sum(i['reserved_usd'] for k, i in intents.items()
                  if k not in record_by_key or base.cost(record_by_key[k]) is None)
    prior = d['prior_ledger']
    conservative = prior['cumulative_conservative_charge_usd'] + known + unknown
    ledger = {'original_allowance_usd': 9, 'recorded_token_estimate_usd': known,
              'cumulative_token_estimate_usd': prior['cumulative_token_estimate_usd'] + known,
              'unknown_usage_reserved_usd': prior['unknown_timeout_reserved_usd'] + unknown,
              'cumulative_conservative_charge_usd': conservative,
              'remaining_original_allowance_conservative_usd': 9 - conservative,
              'pending_requests': result['unresolved_dispatches'], 'provider_balance_verified': False}
    save_new(root / 'analysis' / f'budget_{digest(ledger)[:16]}.json', ledger)
    return result


def archive(root, m):
    files = {p.relative_to(root).as_posix(): p.read_bytes() for p in root.rglob('*')
             if p.is_file() and p.name != 'local_backup.json'}
    hashes = {name: sha256(raw).hexdigest() for name, raw in files.items()}
    target = ROOT / 'output/validity_backups' / f'{root.name}_{digest(hashes)[:16]}.zip'
    target.parent.mkdir(parents=True, exist_ok=True)
    if not target.exists():
        with zipfile.ZipFile(target, 'x', compression=zipfile.ZIP_DEFLATED) as z:
            for name, raw in files.items(): z.writestr(name, raw)
    with zipfile.ZipFile(target) as z:
        if z.testzip() or any(z.read(k) != v for k, v in files.items()):
            raise ValueError('Archive mismatch')
    save_new(root / 'local_backup.json', {'path': str(target), 'sha256': sha256(target.read_bytes()).hexdigest(),
             'file_sha256': hashes, 'note': 'Verified same-computer archive, not off-device backup.'})


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--run-root', required=True, type=Path)
    p.add_argument('--prepare-only', action='store_true'); p.add_argument('--yes', action='store_true')
    a = p.parse_args(); root = a.run_root.resolve()
    if a.prepare_only:
        m = prepare(root)
        print(json.dumps({k: m['design'][k] for k in ('planned_decisions', 'maximum_api_calls', 'full_dispatch_reserve_usd', 'spending_ceiling_usd')}))
        return
    import os
    import msvcrt
    if not a.yes or not os.environ.get('OPENAI_API_KEY'):
        p.error('Need --yes and configured key')
    m = json.loads((root / 'manifest.json').read_bytes()); check(m)
    auth = json.loads((root / 'dispatch_authorization.json').read_bytes())
    if auth['design_hash'] != m['design_hash'] or auth['request_preview_sha256'] != sha256((root / 'request_preview.json').read_bytes()).hexdigest():
        raise ValueError('Dispatch authorization scope mismatch')
    async def run():
        async with httpx.AsyncClient(headers={'Authorization': 'Bearer ' + os.environ['OPENAI_API_KEY']},
                                    timeout=m['design']['timeout_seconds'], follow_redirects=False) as client:
            await execute(root, m, client)
    logs = ROOT / 'output' / root.name; logs.mkdir(parents=True, exist_ok=True)
    with (logs / 'execution.lock').open('a+b') as lock:
        lock.write(b'0'); lock.flush(); lock.seek(0); msvcrt.locking(lock.fileno(), msvcrt.LK_NBLCK, 1)
        try:
            asyncio.run(run())
        finally:
            try:
                result = score(root, m)
            finally:
                archive(root, m)
            print(json.dumps({k: v for k, v in result.items() if k != 'cells'}, indent=2), flush=True)


if __name__ == '__main__':
    main()
