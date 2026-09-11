"""Small endpoint sensitivity probe using the frozen evidence-screen transport."""
import argparse
import asyncio
from copy import deepcopy
from hashlib import sha256
import json
import logging
import os
from pathlib import Path

import pandas as pd
import utils
from engine.llm_client import utc_now_iso
from engine.validity_analysis import DIRECTIONS, wilson
from engine.validity_sweep import digest, freeze
from run_validity_claude import save_new
import run_validity_evidence_screen as base

ROOT = base.ROOT
PREVIOUS = ROOT / 'experiments/phase1_5_encoding_validity/evidence_screen_20260911'
SWEEP = ROOT / 'experiments/phase1_5_encoding_validity/option_c_20260909_restart'
VALUES = (.1, .9)


def prepare(root):
    previous = json.loads((PREVIOUS / 'manifest.json').read_text(encoding='utf-8'))
    base.check(previous)
    source = json.loads((SWEEP / 'manifest.json').read_text(encoding='utf-8'))
    if digest(source['design']) != source['design_hash']:
        raise ValueError('Historical sweep manifest damaged')
    budget = json.loads((PREVIOUS / 'budget_ledger.json').read_text(encoding='utf-8'))
    if budget['pending_requests'] != 0 or budget['total_new_authorised_usd'] != 9:
        raise ValueError('Previous budget not reconciled')
    old = {(c['arm'], c['wording']): c for c in previous['design']['cells']}
    cells = []
    for arm in base.ARMS:
        for param, wordings in (('PD', ('paraphrase_2', 'paraphrase_3')), ('MoR', ('canonical',))):
            for wording in wordings:
                for value in VALUES:
                    if param == 'PD':
                        origin = deepcopy(old['original', wording])
                        before = ' 6. Procedural Dependence: 0.80'
                        after = f' 6. Procedural Dependence: {value:.2f}'
                        if origin['messages'][0]['content'].count(before) != 1:
                            raise ValueError('Expected exact parameter line not found')
                        origin['messages'][0]['content'] = origin['messages'][0]['content'].replace(before, after, 1)
                        origin['profile']['PD'] = value
                    else:
                        matches = [c for c in source['design']['cells'] if c['parameter'] == 'MoR'
                                   and c['value'] == value and c['problem'] == 'S3' and c['arm'] == 'full_harness']
                        if len(matches) != 1: raise ValueError('Historical MoR control missing')
                        origin = deepcopy(matches[0])
                    if origin['messages'][-1] != old['original', 'canonical']['messages'][-1]:
                        raise ValueError('Dilemma/schema differs from the completed evidence screen')
                    origin['messages'][-1] = deepcopy(old[arm, 'canonical']['messages'][-1])
                    cell_id = f'{param}_{wording}_v{value:.1f}'.replace('.', 'p')
                    cells.append({'arm': arm, 'wording': cell_id, 'template_wording': wording,
                                  'parameter': param, 'value': value, 'problem': 'S3',
                                  'labels': ['ADOPT', 'WAIT'], 'n': base.N,
                                  'profile': origin['profile'], 'messages': origin['messages']})
    assert DIRECTIONS['MoR', 'S3'] == 1 and ('PD', 'S3') not in DIRECTIONS
    hashes = dict(previous['design']['source_hashes'])
    for path in (Path(__file__), SWEEP / 'manifest.json', PREVIOUS / 'manifest.json',
                 PREVIOUS / 'budget_ledger.json', ROOT / 'code/run_validity_evidence_screen.py'):
        hashes[path.relative_to(ROOT).as_posix()] = sha256(path.read_bytes()).hexdigest()
    d = {'phase': 'phase1_5_encoding_validity', 'experiment': 'S3_evidence_endpoint_sensitivity_screen',
         'model': base.MODEL, 'provider': 'openai', 'configuration': 'neutral',
         'temperature': 1., 'max_tokens': 600, 'seed': 20260916, 'planned_calls': len(cells) * base.N,
         'cells': cells, 'source_hashes': hashes, 'spending_ceiling_usd': 4.,
         'total_new_user_budget_usd': 9., 'prior_recorded_token_estimate_usd': budget['recorded_full_rate_token_estimate_usd'],
         'prior_reserved_usd': budget['conservative_dispatched_reservations_usd'],
         'pricing': previous['design']['pricing'],
         'primary': 'Grounding canonical MoR .9-minus-.1 ADOPT difference, conservative >=95% exact interval. Existing positive direction; no slope, retention or phase-pass claim.',
         'secondary': 'Original/repetition MoR controls; PD within-wording endpoint differences and P2/P3 gaps at each value, descriptive/no PD direction; secondary intervals nominal, not family-adjusted.',
         'collection': '30 shuffled complete 18-cell blocks, concurrency 3; same frozen single-attempt transport, pre-dispatch reservations, source checks and immutable records as prior screen.',
         'scope': 'Two endpoints of two parameters on known S3. Other nine parameters at source means in each sweep. No new no-profile collection, four-wording equivalence, full gradient, or holdout claim.',
         'authorization_basis': 'Researcher said go for it after recommendation of a small sensitivity check, retaining the $9 total ceiling; no separate exact-payload signature claimed by preparation.'}
    d['full_dispatch_reserve_usd'] = sum(base.reserve(c, d) * c['n'] for c in cells)
    if d['full_dispatch_reserve_usd'] > d['spending_ceiling_usd'] or d['prior_reserved_usd'] + d['spending_ceiling_usd'] > 9:
        raise ValueError('Current or cumulative conservative budget exceeded')
    m = freeze(root / 'manifest.json', d)
    save_new(root / 'request_preview.json', {'design_hash': m['design_hash'], 'cells': cells})
    return m


def score(root, m):
    _, rows, _ = base.inventory(root, m); cells = []
    for c in m['design']['cells']:
        group = [r for r in rows if (r['arm'], r['wording']) == (c['arm'], c['wording'])]
        good = [r for r in group if r['parse_status'] == 'ok' and not r['terminal_failure']]
        k = sum(r['parsed_decision'] == 'ADOPT' for r in good)
        cells.append({**{name: c[name] for name in ('arm', 'wording', 'template_wording', 'parameter', 'value')},
                      'n_expected': c['n'], 'n_recorded': len(group), 'n_valid': len(good),
                      'n_invalid': len(group) - len(good), 'n_missing': c['n'] - len(group),
                      'adopt': k, 'rate': k / len(good) if good else None, 'ci95': wilson(k, len(good))})
    logging.basicConfig(level=logging.INFO)
    utils.log_dataframe_summary(pd.DataFrame(cells), 'All 18 sensitivity cells, missing/invalid retained', logging.getLogger('sensitivity'))
    lookup = {(c['arm'], c['parameter'], c['template_wording'], c['value']): c for c in cells}
    effects = {}
    gaps = {}
    for arm in base.ARMS:
        for param, wording in (('MoR', 'canonical'), ('PD', 'paraphrase_2'), ('PD', 'paraphrase_3')):
            effects[f'{arm}/{param}/{wording}'] = base.contrast([
                (lookup[arm, param, wording, .9], 1), (lookup[arm, param, wording, .1], -1)])
        for value in VALUES:
            gaps[f'{arm}/PD/{value:.1f}'] = base.contrast([
                (lookup[arm, 'PD', 'paraphrase_2', value], 1), (lookup[arm, 'PD', 'paraphrase_3', value], -1)])
    primary = effects['grounding/MoR/canonical']
    lo, hi = primary['conservative_95_interval_unknown_envelope']
    complete = len(rows) == m['design']['planned_calls']
    quality = all(c['n_valid'] / c['n_expected'] >= .98 for c in cells)
    status = ('INCOMPLETE' if not complete else 'INVALID_OUTPUT_SCREEN_NOT_INFORMATIVE' if not quality
              else 'POSITIVE_RESPONSE_DETECTED_NOT_VALIDATED' if lo > 0
              else 'OPPOSITE_RESPONSE_DETECTED_NOT_VALIDATED' if hi < 0
              else 'SENSITIVITY_UNRESOLVED_NOT_VALIDATED')
    result = {'design_hash': m['design_hash'], 'status': status, 'cells': cells, 'endpoint_effects': effects,
              'PD_wording_gaps': gaps, 'primary': 'grounding/MoR/canonical',
              'n_records': len(rows), 'n_valid': sum(c['n_valid'] for c in cells),
              'n_terminal_failures': sum(r['terminal_failure'] for r in rows),
              'n_missing_usage': sum(base.cost(r) is None for r in rows),
              'recorded_token_estimate_usd': sum(base.cost(r) or 0 for r in rows),
              'phase_gate': 'Unchanged; no continuous gradient, retention, equivalence, or hard-cap claim'}
    save_new(root / 'analysis' / f'sensitivity_{digest(result)[:16]}.json', result)
    return result


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--run-root', type=Path, required=True)
    p.add_argument('--prepare-only', action='store_true'); p.add_argument('--yes', action='store_true')
    args = p.parse_args(); root = args.run_root.resolve()
    if args.prepare_only:
        m = prepare(root); print(json.dumps({k: m['design'][k] for k in ('planned_calls', 'full_dispatch_reserve_usd', 'spending_ceiling_usd')}, indent=2)); return
    if not args.yes or not os.environ.get('OPENAI_API_KEY'): p.error('Need --yes and a configured key')
    m = json.loads((root / 'manifest.json').read_text(encoding='utf-8')); base.check(m)
    import msvcrt
    from openai import AsyncOpenAI
    logs = ROOT / 'output' / root.name; logs.mkdir(parents=True, exist_ok=True)
    def status(v): (logs / 'status.json').write_text(json.dumps({'status': v, 'timestamp_utc': utc_now_iso()}), encoding='utf-8')
    async def run():
        client = base.SingleAttemptOpenAI(base.MODEL, concurrency=3, max_retries=1, timeout_s=90)
        async with AsyncOpenAI(base_url='https://api.openai.com/v1', max_retries=0, timeout=90) as sdk:
            client._client = sdk
            await base.execute(root, m, client)
    with (logs / 'execution.lock').open('a+b') as lock:
        lock.write(b'0'); lock.flush(); lock.seek(0); msvcrt.locking(lock.fileno(), msvcrt.LK_NBLCK, 1)
        status('RUNNING')
        try:
            try: asyncio.run(run())
            finally:
                result = score(root, m); base.archive(root, m)
                print(json.dumps(result, indent=2), flush=True)
            status(result['status'])
        except BaseException:
            status('STOPPED_WITH_ERROR'); raise


if __name__ == '__main__': main()
