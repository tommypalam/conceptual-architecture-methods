"""Fixed, budget-bounded S3 grounding screen; separate from frozen experiments."""
import argparse
import asyncio
from copy import deepcopy
from hashlib import sha256
import json
import logging
import os
from pathlib import Path
import random
import zipfile

import pandas as pd
from scipy.stats import beta
import utils
from engine.llm_client import LLMClient, Message, utc_now_iso
from engine.parsing import parse_decision, parse_reasoning
from engine.seeding import derive_seed
from engine.validity_analysis import wilson
from engine.validity_sweep import ValiditySink, digest, freeze
from research_support.evidence import EvidenceCard, GROUNDING_NOTE, render_evidence_card
from run_validity_claude import save_new
from run_validity_axis_revision import check_approval

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'experiments/phase1_5_encoding_validity/axis_instruction_20260910'
CANDIDATE = ROOT / 'experiments/phase1_5_encoding_validity/evidence_candidate_20260911'
MODEL = 'gpt-5.4-mini-2026-03-17'
N = 30
ARMS = ('original', 'repetition', 'grounding')


def reserve(cell, d):
    # UTF-8 byte bound with ample message-framing allowance; no cache discount.
    return ((sum(len(v['content'].encode('utf-8')) for v in cell['messages']) + 512)
            * .75 + d['max_tokens'] * 4.5) / 1e6


def cost(row):
    u = (row.get('response_payload') or {}).get('usage', {})
    if not all(isinstance(u.get(k), int) and u[k] >= 0
               for k in ('prompt_tokens', 'completion_tokens')):
        return None
    return (u['prompt_tokens'] * .75 + u['completion_tokens'] * 4.5) / 1e6


def prepare(root):
    source = json.loads((SOURCE / 'manifest.json').read_text(encoding='utf-8'))
    if digest(source['design']) != source['design_hash']:
        raise ValueError('Source design damaged')
    check_approval(source, SOURCE / 'review_approved.json')
    cm = json.loads((CANDIDATE / 'manifest.json').read_text(encoding='utf-8'))
    for name, expected in cm['artifact_sha256'].items():
        if sha256((CANDIDATE / name).read_bytes()).hexdigest() != expected:
            raise ValueError('Candidate artifact changed')
    card = EvidenceCard.from_json((CANDIDATE / 'S3.evidence.json').read_text(encoding='utf-8'))
    lock = json.loads((ROOT / 'experiments/phase0c_locked_holdout/frozen_prompts/manifest.json').read_text(encoding='utf-8'))
    if sha256((ROOT / card.source_path).read_bytes()).hexdigest() != lock['hashes']['S3']:
        raise ValueError('Phase 0c source lock changed')
    overlay = render_evidence_card(card)
    if overlay + '\n' != (CANDIDATE / 'S3_OVERLAY_DRAFT.txt').read_text(encoding='utf-8'):
        raise ValueError('Renderer differs from prepared candidate')
    repeated = overlay.replace(GROUNDING_NOTE + '\n\n', '', 1)
    baseline = [c for c in source['design']['cells']
                if c['stage'] == 'equivalence' and c['arm'] == 'baseline']
    assert [c['wording'] for c in baseline] == ['canonical', 'paraphrase_1', 'paraphrase_2', 'paraphrase_3']
    assert all(c['messages'][1] == baseline[0]['messages'][1] for c in baseline)
    # Null isolates the added-context effect WITHOUT supplying a parameter profile.
    # It keeps the exact same user turn/schema; it is not the Phase 0c naked prompt.
    null = dict(baseline[0], wording='no_profile', profile=None,
                messages=[deepcopy(baseline[0]['messages'][1])])
    cells = []
    for arm in ARMS:
        for old in baseline + [null]:
            messages = deepcopy(old['messages'])
            if arm != 'original':
                addition = repeated if arm == 'repetition' else overlay
                prefix, suffix = messages[-1]['content'].split('\n\nRespond in exactly this format:', 1)
                messages[-1]['content'] = prefix + '\n\n' + addition + '\n\nRespond in exactly this format:' + suffix
            cells.append({'arm': arm, 'wording': old['wording'], 'profile': old['profile'],
                          'problem': 'S3', 'labels': ['ADOPT', 'WAIT'], 'n': N, 'messages': messages})
    hashes = dict(source['design']['source_hashes'])
    for path in [Path(__file__), ROOT / 'code/research_support/evidence.py',
                 ROOT / 'code/run_validity_axis_revision.py', ROOT / 'code/run_validity_claude.py',
                 ROOT / 'code/engine/validity_sweep.py', ROOT / 'code/engine/llm_client.py',
                 ROOT / 'code/engine/parsing.py', ROOT / 'code/engine/seeding.py',
                 ROOT / 'code/engine/record_sink.py', ROOT / 'code/engine/validity_analysis.py',
                 SOURCE / 'manifest.json', SOURCE / 'review_approved.json',
                 CANDIDATE / 'manifest.json', CANDIDATE / 'S3.evidence.json',
                 CANDIDATE / 'S3_OVERLAY_DRAFT.txt', ROOT / card.source_path,
                 ROOT / 'experiments/phase0c_locked_holdout/frozen_prompts/manifest.json']:
        hashes[path.relative_to(ROOT).as_posix()] = sha256(path.read_bytes()).hexdigest()
    d = {'phase': 'phase1_5_encoding_validity', 'experiment': 'S3_evidence_grounding_development_screen',
         'model': MODEL, 'provider': 'openai', 'configuration': 'neutral for profile cells; unspecified in no-profile cells',
         'temperature': 1., 'max_tokens': 600, 'seed': 20260915,
         'planned_calls': len(cells) * N, 'cells': cells, 'source_hashes': hashes,
         'spending_ceiling_usd': 3., 'total_new_user_budget_usd': 9.,
         'pricing': {'input_per_million': .75, 'output_per_million': 4.5,
                     'source': 'https://developers.openai.com/api/docs/models/gpt-5.4-mini', 'checked': '2026-09-11'},
         'primary': 'Grounding P2 minus P3; conservative >=95% exact interval outside +/-.10 rejects gross stability. No pass claim.',
         'secondary': 'Other contrasts are exploratory, nominal >=95% each, not adjusted across contrasts. No-profile overlay effects do not prove neutrality or identify pure parameter effects.',
         'collection': '30 shuffled complete 15-cell blocks; concurrency 3; unique requested seeds; one HTTP attempt per slot; no retries or parameter fallback; persistent pre-dispatch reservations; stop on API/model/provenance/usage failure.',
         'selection': 'Known S3 failure; not a holdout. No sample expansion or outcome-based selection within this run.',
         'authorization_basis': 'Researcher authorised exploration within Phase 0 closure, then instructed paid exploration with total $9 ceiling. No claim of a separate exact-message human signature.'}
    d['full_dispatch_reserve_usd'] = sum(reserve(c, d) * N for c in cells)
    if d['full_dispatch_reserve_usd'] > d['spending_ceiling_usd']:
        raise ValueError('Entire fixed design exceeds conservative reservation cap')
    m = freeze(root / 'manifest.json', d)
    save_new(root / 'request_preview.json', {'design_hash': m['design_hash'], 'cells': cells})
    return m


def jobs(d):
    rng = random.Random(d['seed'])
    for k in range(1, N + 1):
        block = list(d['cells']); rng.shuffle(block)
        for c in block:
            key = f"{c['arm']}/{c['wording']}/call_{k:04d}"
            yield key, c, k, derive_seed(d['seed'], c['arm'], c['wording'], k)


def check(m):
    d = m['design']
    if digest(d) != m['design_hash'] or d['model'] != MODEL:
        raise ValueError('Frozen design mismatch')
    for path, expected in d['source_hashes'].items():
        if sha256((ROOT / path).read_bytes()).hexdigest() != expected:
            raise ValueError('Frozen source changed: ' + path)


def inventory(root, m):
    check(m)
    planned = {key: (c, k, seed) for key, c, k, seed in jobs(m['design'])}
    rows = list(ValiditySink(root / 'records').read_all())
    seen = set()
    for r in rows:
        key = r['record_key']
        if key in seen or key not in planned:
            raise ValueError('Duplicate or unexpected record')
        seen.add(key); c, k, seed = planned[key]
        if (r['design_hash'] != m['design_hash'] or r['request_messages'] != c['messages']
                or r['agent_parameters'] != c['profile'] or r['seed'] != seed
                or r['arm'] != c['arm'] or r['wording'] != c['wording'] or r['call_index'] != k):
            raise ValueError('Record provenance mismatch')
    return planned, rows, seen


async def execute(root, m, client):
    planned, rows, seen = inventory(root, m); d = m['design']
    intents = {}
    for path in (root / 'dispatches').rglob('*.json'):
        intent = json.loads(path.read_text(encoding='utf-8')); key = intent['record_key']
        if key not in planned or key in intents or intent != dispatch_intent(key, planned[key][0], m):
            raise ValueError('Invalid dispatch reservation')
        intents[key] = intent
    if set(intents) != seen:
        raise ValueError('Unresolved dispatch reservation; no automatic retry')
    if any(r['terminal_failure'] for r in rows):
        raise ValueError('Preserved terminal failure; no in-place resume')
    reserved = sum(v['reserved_usd'] for v in intents.values())
    pending = [j for j in jobs(d) if j[0] not in seen]
    sink = ValiditySink(root / 'records')
    async def one(job):
        key, c, k, seed = job
        result = await client.complete([Message(**v) for v in c['messages']],
                                      temperature=d['temperature'], max_tokens=d['max_tokens'], seed=seed)
        decision, parse = parse_decision(result.text, tuple(c['labels']))
        mismatch = bool(result.ok and (result.model_version != MODEL or result.provider != 'openai'))
        r = {'record_key': key, 'design_hash': m['design_hash'], 'arm': c['arm'], 'wording': c['wording'],
             'problem_id': 'S3', 'agent_parameters': c['profile'], 'call_index': k, 'seed': seed,
             'schedule_seed': d['seed'], 'timestamp_utc': result.timestamp_utc, 'provider': result.provider,
             'model_version': result.model_version, 'model_version_mismatch': mismatch,
             'api_call_id': result.api_call_id, 'attempts': result.attempts,
             'request_messages': result.request_messages, 'response_payload': result.raw_response,
             'raw_response': result.text, 'parsed_decision': decision, 'parsed_reasoning': parse_reasoning(result.text),
             'error_message': result.error, 'parse_status': 'failed_api' if result.error else 'model_mismatch' if mismatch else parse}
        estimate = cost(r)
        r['terminal_failure'] = bool(result.error or mismatch or estimate is None
                                     or estimate > reserve(c, d) or result.attempts != 1
                                     or not result.api_call_id or result.request_messages != c['messages'])
        r['record_hash'] = digest(r); sink.write(key, r)
        if r['terminal_failure']:
            sink.write_failure({'record_key': key, 'error': result.error, 'terminal_failure': True})
        return r
    for start in range(0, len(pending), 3):
        batch = pending[start:start + 3]
        bound = sum(reserve(c, d) for _, c, _, _ in batch)
        if reserved + bound > d['spending_ceiling_usd']:
            raise RuntimeError('Pre-dispatch spending guard reached')
        for key, c, _, _ in batch:
            save_new(root / 'dispatches' / (key + '.json'), dispatch_intent(key, c, m))
        reserved += bound
        new = await asyncio.gather(*(one(j) for j in batch)); rows.extend(new)
        if len(rows) % 15 == 0 or len(rows) == 3:
            print(f"{len(rows)}/{d['planned_calls']}; token estimate ${sum(cost(r) or 0 for r in rows):.5f}; reserved ${reserved:.4f}", flush=True)
        if any(r['terminal_failure'] for r in new):
            raise RuntimeError('Terminal failure preserved; collection stopped')


def dispatch_intent(key, c, m):
    return {'record_key': key, 'design_hash': m['design_hash'],
            'messages_hash': digest(c['messages']), 'reserved_usd': reserve(c, m['design'])}


def contrast(terms):
    # Bonferroni over the cells WITHIN this single contrast. Unknowns include missing.
    alpha = .05 / len(terms); lower = upper = point = 0.
    for c, weight in terms:
        k, n, unknown = c['adopt'], c['n_expected'], c['n_expected'] - c['n_valid']
        lo = 0. if k == 0 else float(beta.ppf(alpha / 2, k, n - k + 1))
        hi = 1. if k + unknown == n else float(beta.ppf(1 - alpha / 2, k + unknown + 1, n - k - unknown))
        lower += weight * (lo if weight > 0 else hi)
        upper += weight * (hi if weight > 0 else lo)
        point += weight * (c['rate'] if c['rate'] is not None else 0.)
    return {'difference': point if all(c['rate'] is not None for c, _ in terms) else None,
            'conservative_95_interval_unknown_envelope': [lower, upper]}


def score(root, m):
    _, rows, _ = inventory(root, m); cells = []
    for c in m['design']['cells']:
        group = [r for r in rows if (r['arm'], r['wording']) == (c['arm'], c['wording'])]
        valid = [r for r in group if r['parse_status'] == 'ok' and not r['terminal_failure']]
        k = sum(r['parsed_decision'] == 'ADOPT' for r in valid)
        cells.append({'arm': c['arm'], 'wording': c['wording'], 'n_expected': N,
                      'n_recorded': len(group), 'n_valid': len(valid), 'n_invalid': len(group) - len(valid),
                      'n_missing': N - len(group), 'adopt': k, 'rate': k / len(valid) if valid else None,
                      'ci95': wilson(k, len(valid))})
    logging.basicConfig(level=logging.INFO)
    utils.log_dataframe_summary(pd.DataFrame(cells), 'All 15 evidence cells; missing and invalid retained', logging.getLogger('evidence'))
    lookup = {(c['arm'], c['wording']): c for c in cells}
    gaps = {a: contrast([(lookup[a, 'paraphrase_2'], 1), (lookup[a, 'paraphrase_3'], -1)]) for a in ARMS}
    primary = gaps['grounding']; lo, hi = primary['conservative_95_interval_unknown_envelope']
    complete = len(rows) == m['design']['planned_calls']
    quality = all(c['n_valid'] / N >= .98 for c in cells)
    saturated = all(lookup['grounding', w]['rate'] is not None for w in ('canonical', 'paraphrase_1', 'paraphrase_2', 'paraphrase_3')) and (
        all(lookup['grounding', w]['rate'] <= .05 for w in ('canonical', 'paraphrase_1', 'paraphrase_2', 'paraphrase_3')) or
        all(lookup['grounding', w]['rate'] >= .95 for w in ('canonical', 'paraphrase_1', 'paraphrase_2', 'paraphrase_3')))
    status = ('INCOMPLETE' if not complete else 'INVALID_OUTPUT_SCREEN_NOT_INFORMATIVE' if not quality
              else 'GROSS_WORDING_FAILURE_DETECTED' if lo > .10 or hi < -.10
              else 'SATURATED_SCREEN_NOT_INFORMATIVE' if saturated else 'NO_GROSS_FAILURE_DETECTED_NOT_VALIDATED')
    secondary = {}
    for a, b in (('grounding', 'original'), ('grounding', 'repetition'), ('repetition', 'original')):
        secondary[a + '_minus_' + b + '_no_profile'] = contrast([(lookup[a, 'no_profile'], 1), (lookup[b, 'no_profile'], -1)])
        secondary[a + '_minus_' + b + '_wording_gap'] = contrast([
            (lookup[a, 'paraphrase_2'], 1), (lookup[a, 'paraphrase_3'], -1),
            (lookup[b, 'paraphrase_2'], -1), (lookup[b, 'paraphrase_3'], 1)])
    result = {'design_hash': m['design_hash'], 'status': status, 'cells': cells, 'wording_gaps': gaps,
              'secondary_nominal_not_studywise_adjusted': secondary, 'n_records': len(rows),
              'n_valid': sum(c['n_valid'] for c in cells), 'n_terminal_failures': sum(r['terminal_failure'] for r in rows),
              'recorded_token_estimate_usd': sum(cost(r) or 0 for r in rows),
              'n_missing_usage': sum(cost(r) is None for r in rows), 'phase_gate': 'Unchanged; no pass claim'}
    save_new(root / 'analysis' / f"screen_{digest(result)[:16]}.json", result)
    return result


class SingleAttemptOpenAI(LLMClient):
    async def _raw_call(self, messages, temperature, max_tokens, seed):
        self._ensure_client()
        resp = await self._client.chat.completions.create(
            model=self.model, messages=[{'role': v.role, 'content': v.content} for v in messages],
            temperature=temperature, max_completion_tokens=max_tokens, seed=seed)
        return resp.choices[0].message.content, resp.id, resp.model, resp.model_dump()


def archive(root, m):
    _, rows, _ = inventory(root, m)
    save_new(root / 'record_checksums.json', {'design_hash': m['design_hash'],
             'records': {r['record_key']: r['record_hash'] for r in rows}})
    payloads = {p.relative_to(root).as_posix(): p.read_bytes() for p in root.rglob('*')
                if p.is_file() and p.name != 'local_backup.json'}
    tag = digest({name: sha256(raw).hexdigest() for name, raw in payloads.items()})[:16]
    target = ROOT / 'output/validity_backups' / f'{root.name}_{tag}.zip'
    target.parent.mkdir(parents=True, exist_ok=True)
    if not target.exists():
        with zipfile.ZipFile(target, 'x', compression=zipfile.ZIP_DEFLATED) as z:
            for name, raw in payloads.items(): z.writestr(name, raw)
    with zipfile.ZipFile(target) as z:
        if z.testzip() or any(z.read(name) != raw for name, raw in payloads.items()):
            raise ValueError('Backup verification failed')
    save_new(root / 'local_backup.json', {'path': str(target), 'sha256': sha256(target.read_bytes()).hexdigest(),
             'n_records': len(rows), 'note': 'Verified byte-for-byte; same-computer backup only.'})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run-root', type=Path, required=True)
    parser.add_argument('--prepare-only', action='store_true')
    parser.add_argument('--yes', action='store_true')
    args = parser.parse_args(); root = args.run_root.resolve()
    if args.prepare_only:
        m = prepare(root)
        print(json.dumps({k: m['design'][k] for k in ('planned_calls', 'full_dispatch_reserve_usd', 'spending_ceiling_usd')}, indent=2)); return
    if not args.yes or not os.environ.get('OPENAI_API_KEY'):
        parser.error('Need --yes and a configured key')
    m = json.loads((root / 'manifest.json').read_text(encoding='utf-8')); check(m)
    import msvcrt
    from openai import AsyncOpenAI
    logs = ROOT / 'output' / root.name; logs.mkdir(parents=True, exist_ok=True)
    def status(v):
        (logs / 'status.json').write_text(json.dumps({'status': v, 'timestamp_utc': utc_now_iso()}), encoding='utf-8')
    async def run():
        client = SingleAttemptOpenAI(MODEL, concurrency=3, max_retries=1, timeout_s=90)
        async with AsyncOpenAI(base_url='https://api.openai.com/v1', max_retries=0, timeout=90) as sdk:
            client._client = sdk
            await execute(root, m, client)
    with (logs / 'execution.lock').open('a+b') as lock:
        lock.write(b'0'); lock.flush(); lock.seek(0); msvcrt.locking(lock.fileno(), msvcrt.LK_NBLCK, 1)
        status('RUNNING')
        try:
            try: asyncio.run(run())
            finally:
                result = score(root, m); archive(root, m)
                print(json.dumps(result, indent=2), flush=True)
            status(result['status'])
        except BaseException:
            status('STOPPED_WITH_ERROR'); raise


if __name__ == '__main__':
    main()
