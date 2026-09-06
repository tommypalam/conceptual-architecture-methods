"""Frozen, resumable Option-C sweep. Clients and record sinks are injected."""
from __future__ import annotations

import asyncio
import hashlib
import json
import random
import re
from pathlib import Path

from .delivery import SystemRoleDelivery, UserPrefixDelivery
from .llm_client import Message, utc_now_iso
from .parsing import parse_decision, parse_reasoning
from .phase0b import SweepProfile
from .phase0b_runner import PROBLEMS
from .prompt_assembly import load_template, build_simple_user_turn
from .questions import PHASE0B_QUESTIONS, load_dilemma_body
from .seeding import derive_seed
from .validity_analysis import VALUES
from .record_sink import JsonFileSink

ARMS = ('full_harness', 'user_prefix_bare')


class ValiditySink(JsonFileSink):
    """Reject damaged records rather than silently excluding them from a run."""

    def read_all(self):
        for path in sorted(self.root.rglob('*.json')):
            record = json.loads(path.read_text(encoding='utf-8'))
            verify_record(record)
            yield record


def verify_record(record):
    payload = {k: v for k,v in record.items() if k != 'record_hash'}
    if record.get('record_hash') != digest(payload):
        raise ValueError('Record integrity failure; preserve original and investigate')


def parse_output(text, labels, arm):
    # Bare-label is the requested schema in arm B, not a lenient recovery.
    # Do not change the legacy parser or any previous run's scoring.
    if arm == 'user_prefix_bare' and text is not None:
        options = '|'.join(re.escape(label) for label in labels)
        match = re.fullmatch(rf'\s*[\"\'\[]?\s*({options})\s*[\"\'\]]?\s*\.?\s*',
                             text, flags=re.IGNORECASE)
        if match:
            return next(label for label in labels if label.upper() == match[1].upper()), 'ok'
    return parse_decision(text, tuple(labels))


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':'),
                                     ensure_ascii=False, allow_nan=False).encode()).hexdigest()


def build_design(*, params, problems, n, seed, provider, model):
    template = load_template()
    cells = []
    for param in params:
        for value in VALUES:
            harness, provenance = SweepProfile(param, value).build(template, seed=seed)
            for problem in PROBLEMS:
                if problem.short_id not in problems:
                    continue
                body = load_dilemma_body(problem.question_file, PHASE0B_QUESTIONS)
                for arm in ARMS:
                    bare = arm == 'user_prefix_bare'
                    delivery = UserPrefixDelivery() if bare else SystemRoleDelivery()
                    user = build_simple_user_turn(body, problem.labels, bare_label=bare)
                    cells.append({'arm': arm, 'parameter': param, 'value': value,
                                  'problem': problem.short_id, 'labels': list(problem.labels),
                                  'profile': provenance['parameter_values'],
                                  'messages': [{'role': m.role, 'content': m.content}
                                               for m in delivery.messages(harness, user)],
                                  'dilemma_sha256': hashlib.sha256(body.encode()).hexdigest()})
    # Includes analysis sources: resume refuses silent changes to the frozen method.
    source_files = ('validity_sweep.py', 'validity_analysis.py', 'llm_client.py',
                    'parsing.py', 'seeding.py')
    hashes = {name: hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest()
              for name in source_files}
    return {'schema_version': '1.0', 'phase': 'phase1_5_encoding_validity',
            'subtest': 'option_c_sweep', 'provider': provider, 'model': model,
            'params': list(params), 'problems': list(problems), 'arms': list(ARMS),
            'values': list(VALUES), 'n': n, 'root_seed': seed,
            'temperature': 1.0, 'max_tokens': 600, 'source_hashes': hashes,
            'configuration': 'neutral', 'cells': cells,
            'planned_calls': len(cells)*n,
            'schedule': 'seeded shuffled base jobs; alternating arm order per job',
            'seed_note': 'same requested seed across arms; not a guarantee of paired random draws',
            'stopping_rule': 'fixed N; stop dispatch on terminal API failure or model-version mismatch',
            'missing_rule': 'never overwrite or replace failed observations; disclose all missing/invalid calls'}


def freeze(path, design):
    """Exclusive creation. Existing design must match byte-independent content hash."""
    path = Path(path)
    if path.exists():
        old = json.loads(path.read_text(encoding='utf-8'))
        if old.get('design_hash') != digest(old['design']):
            raise ValueError('Manifest integrity failure')
        if old['design_hash'] != digest(design):
            raise ValueError('Frozen design differs: use a NEW run directory; never mix protocols')
        return old
    path.parent.mkdir(parents=True, exist_ok=True)
    manifest = {'frozen_at': utc_now_iso(), 'design_hash': digest(design), 'design': design}
    with path.open('x', encoding='utf-8') as stream:
        json.dump(manifest, stream, indent=2, ensure_ascii=False, allow_nan=False)
    return manifest


def jobs(design):
    by_cell = {(c['parameter'], c['value'], c['problem'], c['arm']): c
               for c in design['cells']}
    base = [(p, v, q, k) for p in design['params'] for v in VALUES
            for q in design['problems'] for k in range(1, design['n']+1)]
    random.Random(design['root_seed']).shuffle(base)
    result = []
    for index, (p, v, q, k) in enumerate(base):
        for arm in (ARMS if index % 2 == 0 else ARMS[::-1]):
            key = f'{arm}/{p}/{q}/{v:.1f}/call_{k:04d}'
            result.append((key, by_cell[p, v, q, arm], k))
    return result


async def execute(manifest, *, client, sink, concurrency=5, limit=None):
    if not 1 <= concurrency <= 5:
        raise ValueError('Concurrency must be between 1 and 5')
    design = manifest['design']
    expected_hash = manifest['design_hash']
    if digest(design) != expected_hash:
        raise ValueError('Manifest integrity failure')
    all_jobs = jobs(design)
    expected_keys = {j[0] for j in all_jobs}
    existing = list(sink.read_all())
    seen = set()
    for record in existing:
        verify_record(record)
        key = record.get('record_key')
        if key not in expected_keys or key in seen or record.get('design_hash') != expected_hash:
            raise ValueError('Unexpected, duplicate, or incompatible existing record')
        seen.add(key)
        if record.get('error_message') or record.get('model_version_mismatch'):
            raise ValueError('Run contains terminal failures: preserve records and review before a new designation')
    pending = [j for j in all_jobs if not sink.exists(j[0])]
    if limit is not None:
        pending = pending[:limit]
    completed = 0

    async def one(job):
        key, cell, k = job
        seed = derive_seed(design['root_seed'], cell['parameter'], cell['value'], cell['problem'], k)
        messages = [Message(**m) for m in cell['messages']]
        result = await client.complete(messages, temperature=design['temperature'],
                                       max_tokens=design['max_tokens'], seed=seed)
        decision, status = parse_output(result.text, cell['labels'], cell['arm'])
        expected_version = design['model'] + '-mock' if design['provider'] == 'mock' else design['model']
        mismatch = result.ok and result.model_version != expected_version
        record = {'schema_version': '1.0', 'phase': design['phase'], 'subtest': design['subtest'],
                  'record_key': key, 'design_hash': expected_hash, 'arm': cell['arm'],
                  'swept_parameter': cell['parameter'], 'sweep_value': cell['value'],
                  'problem_id': cell['problem'], 'call_index': k, 'labels': cell['labels'],
                  'agent_parameters': cell['profile'], 'configuration_id': 'neutral',
                  'model_name': result.model, 'model_version': result.model_version,
                  'model_version_mismatch': bool(mismatch), 'provider': result.provider,
                  'timestamp_utc': result.timestamp_utc, 'seed': seed,
                  'temperature': result.temperature, 'max_tokens': result.max_tokens,
                  'api_call_id': result.api_call_id, 'attempts': result.attempts,
                  'latency_s': result.latency_s,
                  'request_messages': result.request_messages,
                  'response_payload': result.raw_response, 'raw_response': result.text,
                  'parsed_decision': decision, 'parsed_reasoning': parse_reasoning(result.text),
                  'parse_status': 'failed_api' if result.error else ('model_mismatch' if mismatch else status),
                  'error_message': result.error}
        record['record_hash'] = digest(record)
        sink.write(key, record)
        if result.error or mismatch:
            sink.write_failure({'record_key': key, 'error': result.error,
                                'model_version_mismatch': bool(mismatch)})
        return not (result.error or mismatch)

    # Bound both dispatch and in-flight calls. A failed credential cannot create
    # thousands of failed records, and both arms are spread across run time.
    for start in range(0, len(pending), concurrency):
        outcomes = await asyncio.gather(*(one(j) for j in pending[start:start+concurrency]))
        completed += len(outcomes)
        if start == 0 or completed % 50 == 0 or completed == len(pending):
            print(f'Option C: {len(existing)+completed}/{design["planned_calls"]} records', flush=True)
        if not all(outcomes):
            raise RuntimeError('Dispatch stopped after terminal API failure or model-version mismatch; records preserved')
    return {'planned': design['planned_calls'], 'previous': len(existing), 'executed': completed}
