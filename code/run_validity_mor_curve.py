"""Focused MoR/S3 curve screen using unchanged, previously approved messages."""
import argparse
import asyncio
from copy import deepcopy
from hashlib import sha256
import json
import logging
import os
from pathlib import Path
import zipfile

import pandas as pd
import utils
from engine.llm_client import utc_now_iso
from engine.validity_analysis import analyze, VALUES
from engine.validity_sweep import digest, freeze
from run_validity_claude import save_new
import run_validity_evidence_screen as base

ROOT = base.ROOT
BASE = ROOT / 'experiments/phase1_5_encoding_validity'
PREVIOUS = BASE / 'evidence_sensitivity_20260911'
SCREEN = BASE / 'evidence_screen_20260911'
SWEEP = BASE / 'option_c_20260909_restart'
ARMS = ('repetition', 'grounding')


def prepare(root):
    previous = json.loads((PREVIOUS/'manifest.json').read_bytes()); base.check(previous)
    screen = json.loads((SCREEN/'manifest.json').read_bytes()); base.check(screen)
    source = json.loads((SWEEP/'manifest.json').read_bytes())
    if digest(source['design']) != source['design_hash']: raise ValueError('Source manifest damaged')
    budget = json.loads((PREVIOUS/'budget_ledger.json').read_bytes())
    if budget['pending_requests'] or budget['cumulative_token_estimate_usd'] + 2.4 > 9:
        raise ValueError('Previous spending not settled or original allowance exceeded')
    cells = []
    for arm in ARMS:
        user = next(c['messages'][-1] for c in screen['design']['cells'] if (c['arm'], c['wording']) == (arm, 'canonical'))
        for value in VALUES:
            originals = [c for c in source['design']['cells'] if
                         (c['arm'], c['parameter'], c['problem'], c['value']) == ('full_harness', 'MoR', 'S3', value)]
            if len(originals) != 1: raise ValueError('Canonical cell missing or duplicated')
            c = deepcopy(originals[0]); c['messages'][-1] = deepcopy(user)
            cells.append({'arm': arm, 'wording': f'MoR_canonical_v{value:.1f}'.replace('.', 'p'),
                          'parameter': 'MoR', 'value': value, 'problem': 'S3', 'n': base.N,
                          'labels': ['ADOPT', 'WAIT'], 'profile': c['profile'], 'messages': c['messages']})
    hashes = dict(previous['design']['source_hashes'])
    for path in (Path(__file__), PREVIOUS/'manifest.json', PREVIOUS/'budget_ledger.json',
                 ROOT/'code/engine/validity_analysis.py'):
        hashes[path.relative_to(ROOT).as_posix()] = sha256(path.read_bytes()).hexdigest()
    d = {'experiment': 'MoR_S3_grounding_repetition_five_value_screen', 'phase': 'phase1_5_encoding_validity',
         'configuration': 'neutral', 'model': base.MODEL, 'provider': 'openai',
         'temperature': 1., 'max_tokens': 600, 'seed': 20260917, 'planned_calls': 300,
         'cells': cells, 'source_hashes': hashes, 'pricing': previous['design']['pricing'],
         'spending_ceiling_usd': 2.4, 'prior_recorded_token_estimate_usd': budget['cumulative_token_estimate_usd'],
         'prior_reserved_usd': budget['cumulative_dispatched_reservations_usd'],
         'original_allowance_usd': 9.,
         'authorization_basis': 'Researcher: spend what you need, ill top up. This focused run remains inside the previous $9 allowance; no unlimited automatic expansion.',
         'primary': 'Grounding MoR/S3 original directional sweep criterion at N=30: complete, >=98% valid per cell, positive logistic slope LR p<.05, h>=.20, monotonic rates. Diagnostic only, not phase pass.',
         'secondary': 'Repetition curve and direct grounding-minus-repetition endpoint-change contrast, conservative >=95% interval. No significance-in-one-arm comparison. No equivalence or slope-retention claim.',
         'scope': 'All five values collected contemporaneously in two arms; earlier endpoints and canonical curve are historical context, not pooled. Known S3, one parameter, all other nine at source means.',
         'stop_rule': 'Fixed 300 calls; stop on API/model/usage/reservation failure. Preserve every attempt, no automatic retries, expansions, or outcome-based stopping.'}
    d['full_dispatch_reserve_usd'] = sum(base.reserve(c,d)*c['n'] for c in cells)
    if d['full_dispatch_reserve_usd'] > 2.4 or d['prior_reserved_usd'] + 2.4 > 9:
        raise ValueError('Conservative current/cumulative guard exceeded')
    m = freeze(root/'manifest.json', d)
    save_new(root/'request_preview.json', {'design_hash': m['design_hash'], 'cells': cells})
    return m


def score(root, m):
    planned, rows, _ = base.inventory(root,m)
    converted = []
    for r in rows:
        c = planned[r['record_key']][0]
        converted.append({**r, 'swept_parameter': 'MoR', 'sweep_value': c['value'], 'labels': c['labels']})
    logging.basicConfig(level=logging.INFO)
    utils.log_dataframe_summary(pd.DataFrame([{k:r[k] for k in ('arm','sweep_value','parse_status','parsed_decision')} for r in converted]),
                                'All collected MoR records retained for original analyzer', logging.getLogger('mor-curve'))
    result = analyze(converted, params=['MoR'], problems=['S3'], arms=list(ARMS), n=base.N)
    ground = next(s for s in result['sweeps'] if s['arm'] == 'grounding')
    terminal = sum(r['terminal_failure'] for r in rows)
    status = ('INCOMPLETE' if len(rows) != 300 else 'INVALID_SCREEN' if terminal or not ground['parse_quality_98pct']
              else 'DIRECTIONAL_CURVE_CRITERION_MET_NOT_VALIDATED' if ground['criterion_met'] else 'CURVE_CRITERION_NOT_MET')
    result.update({'design_hash':m['design_hash'], 'status':status, 'n_terminal_failures':terminal,
                   'n_missing_usage':sum(base.cost(r) is None for r in rows),
                   'recorded_token_estimate_usd':sum(base.cost(r) or 0 for r in rows),
                   'historical_records_pooled':False})
    save_new(root/'analysis'/f'curve_{digest(result)[:16]}.json',result)
    return result


def verify_and_report(root, m):
    planned, rows, seen = base.inventory(root,m)
    if len(rows) != 300 or seen != set(planned): raise ValueError('Incomplete collection')
    ids = [r['api_call_id'] for r in rows]
    if len(set(ids)) != 300 or any(not i or i.startswith('mock-') for i in ids): raise ValueError('Invalid API IDs')
    if any(r['terminal_failure'] or r['attempts'] != 1 or r['provider'] != 'openai'
           or r['model_version'] != base.MODEL for r in rows): raise ValueError('Unresolved response failure')
    auth = json.loads((root/'dispatch_authorization.json').read_bytes())
    if auth['design_hash'] != m['design_hash'] or auth['exact_messages_hash'] != digest([c['messages'] for c in m['design']['cells']]):
        raise ValueError('Authorization scope mismatch')
    intents = [json.loads(p.read_bytes()) for p in (root/'dispatches').rglob('*.json')]
    if len(intents) != 300 or {i['record_key'] for i in intents} != seen: raise ValueError('Dispatch mismatch')
    for i in intents:
        if i != base.dispatch_intent(i['record_key'], planned[i['record_key']][0], m): raise ValueError('Reservation mismatch')
    reserved = sum(i['reserved_usd'] for i in intents)
    if reserved > 2.4 or reserved + m['design']['prior_reserved_usd'] > 9: raise ValueError('Budget mismatch')
    backup = json.loads((root/'local_backup.json').read_bytes()); archive = Path(backup['path'])
    if sha256(archive.read_bytes()).hexdigest() != backup['sha256']: raise ValueError('ZIP checksum mismatch')
    with zipfile.ZipFile(archive) as z:
        if z.testzip(): raise ValueError('ZIP corruption')
        for key in seen:
            rel = 'records/'+key+'.json'
            if z.read(rel) != (root/rel).read_bytes(): raise ValueError('ZIP payload mismatch')
    result = score(root,m)
    current = result['recorded_token_estimate_usd']; cumulative = current + m['design']['prior_recorded_token_estimate_usd']
    save_new(root/'analysis/verification.json', {'design_hash':m['design_hash'],'unique_real_api_ids':300,
             'unique_seeds':len({r['seed'] for r in rows}), 'source_request_profile_hashes_verified':True,
             'all_raw_zip_bytes_verified':True, 'reserved_usd':reserved})
    save_new(root/'budget_ledger.json', {'original_allowance_usd':9,'screen_cap_usd':2.4,
             'recorded_token_estimate_usd':current, 'cumulative_token_estimate_usd':cumulative,
             'remaining_original_allowance_estimate_usd':9-cumulative, 'pending_requests':0,
             'cumulative_dispatched_reservations_usd':reserved+m['design']['prior_reserved_usd'],
             'provider_balance_verified':False,'automatic_expansion':False})
    lines = ['# MoR/S3 curve screen', '', f"Status: **{result['status']}**.",
             f'300 calls; full-rate token estimate ${current:.6f}; cumulative ${cumulative:.6f}.',
             f'Original allowance estimate remaining ${9-cumulative:.6f}; provider balance not checked.', '',
             '| Arm | ADOPT counts /30 at .1/.3/.5/.7/.9 | Slope (95% CI) | LR p | h | Monotonic | Directional criterion |',
             '|---|---|---|---|---|---|---|']
    for s in result['sweeps']:
        f=s['fit']; counts='/'.join(str(c['opt0_count']) for c in s['cells'])
        lines.append(f"| {s['arm']} | {counts} | {f.get('slope')} ({f.get('ci95')}) | {f.get('p_value')} | {s['cohens_h_extremes']} | {s['monotonic']} | {s['criterion_met']} |")
    lines += ['', 'Direct endpoint-change contrast (grounding minus repetition):',
              '```json', json.dumps(result['delivery_contrasts'],indent=2),'```', '',
              'Primary: grounding directional criterion; repetition and arm contrast are secondary, not family-adjusted.',
              'N=30 per cell; no historical pooling. Pinned/separated fits cannot satisfy the original criterion.',
              'This tests one canonical parameter description on known S3. No representation retention, paraphrase',
              'equivalence, reasoning faithfulness, internal understanding or phase-pass claim follows.',
              f'Model {base.MODEL}; neutral; temperature 1; max output 600; root seed 20260917.',
              'All exact requests, profiles, reservations and raw ZIP bytes verified. Backup is on the same computer.', '']
    target=root/'analysis/CURVE_REPORT.md'; data='\n'.join(lines).encode('utf-8')
    if target.exists() and target.read_bytes()!=data: raise ValueError('Preserve previous report')
    if not target.exists(): target.write_bytes(data)
    print(json.dumps({'status':result['status'],'cost_usd':current,'report':str(target)}))


def main():
    p=argparse.ArgumentParser(description=__doc__); p.add_argument('--run-root',type=Path,required=True)
    p.add_argument('--prepare-only',action='store_true'); p.add_argument('--report-only',action='store_true'); p.add_argument('--yes',action='store_true')
    args=p.parse_args(); root=args.run_root.resolve()
    if args.prepare_only:
        m=prepare(root); print(json.dumps({k:m['design'][k] for k in ('planned_calls','spending_ceiling_usd','full_dispatch_reserve_usd')})); return
    m=json.loads((root/'manifest.json').read_bytes()); base.check(m)
    if args.report_only: verify_and_report(root,m); return
    if not args.yes or not os.environ.get('OPENAI_API_KEY'): p.error('Need --yes and configured key')
    auth=json.loads((root/'dispatch_authorization.json').read_bytes())
    if auth['design_hash']!=m['design_hash'] or auth['exact_messages_hash']!=digest([c['messages'] for c in m['design']['cells']]):
        raise ValueError('Authorization scope mismatch')
    import msvcrt
    from openai import AsyncOpenAI
    logs=ROOT/'output'/root.name; logs.mkdir(parents=True,exist_ok=True)
    async def run():
        client=base.SingleAttemptOpenAI(base.MODEL,concurrency=3,max_retries=1,timeout_s=90)
        async with AsyncOpenAI(base_url='https://api.openai.com/v1',max_retries=0,timeout=90) as sdk:
            client._client=sdk; await base.execute(root,m,client)
    with (logs/'execution.lock').open('a+b') as lock:
        lock.write(b'0'); lock.flush(); lock.seek(0); msvcrt.locking(lock.fileno(),msvcrt.LK_NBLCK,1)
        try: asyncio.run(run())
        finally:
            result=score(root,m); base.archive(root,m)
            (logs/'status.json').write_text(json.dumps({'status':result['status'],'timestamp_utc':utc_now_iso()}),encoding='utf-8')
        verify_and_report(root,m)


if __name__ == '__main__': main()
