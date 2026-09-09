"""Recover an interrupted sweep into a separate, provenance-linked designation."""
from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import os
from pathlib import Path

from engine.validity_sweep import build_design, digest, execute, jobs, verify_record, ValiditySink
from engine.llm_client import LLMClient, MockClient
from run_validity_sweep import mock_response, score


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'))


def sha(data):
    return hashlib.sha256(data).hexdigest()


def preserve(path, data):
    if path.exists():
        if path.read_bytes() != data:
            raise ValueError(f'Existing continuation artifact differs: {path}')
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as stream:
        stream.write(data)


def prepare_shard(source, target):
    """Reserve all inventoried slots without pretending their responses are local."""
    source, target = Path(source).resolve(), Path(target).resolve()
    if source == target or source in target.parents or target in source.parents:
        raise ValueError('Source and shard must be separate directories')
    manifest = read_json(source/'manifest.json')
    d = manifest['design']
    current = build_design(params=d['params'], problems=d['problems'], n=d['n'],
                           seed=d['root_seed'], provider=d['provider'], model=d['model'])
    if digest(d) != manifest['design_hash'] or digest(current) != manifest['design_hash']:
        raise ValueError('Frozen design or source files differ from this checkout')
    inventory_bytes = (source/'record_checksums.json').read_bytes()
    inventory = json.loads(inventory_bytes)
    keys = [entry['record_key'] for entry in inventory['index']]
    expected = {key for key, _, _ in jobs(d)}
    if (inventory['design_hash'] != manifest['design_hash'] or
            len(keys) != len(set(keys)) or len(keys) != inventory['n_records'] or
            not set(keys) <= expected):
        raise ValueError('Invalid checksum inventory')
    ledger = {'schema_version': '1.0', 'mode': 'missing_records_shard',
              'source_root': str(source), 'design_hash': manifest['design_hash'],
              'source_inventory_sha256': sha(inventory_bytes),
              'wrapper_sha256': sha(Path(__file__).read_bytes()),
              'reserved_source_keys': keys, 'planned_new_calls': len(expected)-len(keys),
              'source_api_failures_pending_recovery': inventory['n_api_failures'],
              'rule': 'Collect only never-inventoried slots. Original payloads are absent; '
                      'no pooled analysis or retry of an unidentified failure. Verify originals before merging.'}
    if target.exists() and any(target.iterdir()) and not (target/'continuation.json').exists():
        raise ValueError('Destination is not a recognised continuation')
    preserve(target/'continuation.json', json.dumps(ledger, indent=2).encode())
    preserve(target/'manifest.json', (source/'manifest.json').read_bytes())
    preserve(target/'source_record_checksums.json', inventory_bytes)
    print(f'Configuration neutral | N={d["n"]}/cell | seed={d["root_seed"]} | '
          f'new slots={ledger["planned_new_calls"]} | absent source records={len(keys)}', flush=True)
    return manifest, set(keys)


class ShardSink(ValiditySink):
    def __init__(self, root, reserved):
        super().__init__(root)
        self.reserved = reserved

    def exists(self, key):
        return key in self.reserved or super().exists(key)

    def write(self, key, record):
        if key in self.reserved:
            raise ValueError('Cannot overwrite a reserved original slot')
        super().write(key, record)

    def read_all(self):
        for record in super().read_all():
            if record['record_key'] in self.reserved:
                raise ValueError('Shard contains a reserved original slot')
            yield record


def prepare(source, target):
    source, target = Path(source).resolve(), Path(target).resolve()
    if source == target or source in target.parents or target in source.parents:
        raise ValueError('Source and continuation must be separate directories')
    manifest = read_json(source/'manifest.json')
    d = manifest['design']
    if digest(d) != manifest['design_hash']:
        raise ValueError('Manifest integrity failure')
    current = build_design(params=d['params'], problems=d['problems'], n=d['n'],
                           seed=d['root_seed'], provider=d['provider'], model=d['model'])
    if digest(current) != manifest['design_hash']:
        raise ValueError('Frozen design or source files differ from this checkout')
    inventory_bytes = (source/'record_checksums.json').read_bytes()
    inventory = json.loads(inventory_bytes)
    entries = inventory['index']
    indexed = {e['record_key']: e['record_hash'] for e in entries}
    if (inventory['design_hash'] != manifest['design_hash'] or
            len(indexed) != len(entries) or len(entries) != inventory['n_records']):
        raise ValueError('Invalid checksum inventory')
    schedule = {key: (cell, k) for key, cell, k in jobs(d)}
    found, reused, failures = {}, [], []
    from engine.seeding import derive_seed
    for path in sorted((source/'records').rglob('*.json')):
        data = path.read_bytes()
        r = json.loads(data)
        verify_record(r)
        key = r['record_key']
        if (key not in schedule or key in found or indexed.get(key) != r['record_hash']
                or r['design_hash'] != manifest['design_hash']
                or path.relative_to(source/'records').as_posix() != key+'.json'):
            raise ValueError('Unexpected, duplicate, misplaced, or mixed-design record')
        cell, k = schedule[key]
        expected = {'arm': cell['arm'], 'swept_parameter': cell['parameter'],
                    'sweep_value': cell['value'], 'problem_id': cell['problem'],
                    'call_index': k, 'agent_parameters': cell['profile'],
                    'labels': cell['labels'], 'request_messages': cell['messages'],
                    'seed': derive_seed(d['root_seed'], cell['parameter'], cell['value'], cell['problem'], k),
                    'temperature': d['temperature'], 'max_tokens': d['max_tokens']}
        if any(r.get(name) != value for name, value in expected.items()):
            raise ValueError(f'Record does not match scheduled request: {key}')
        found[key] = data
        entry = {'record_key': key, 'record_hash': r['record_hash'],
                 'source_path': str(path), 'file_sha256': sha(data)}
        if r.get('model_version_mismatch'):
            raise ValueError('Model mismatch requires scientific review')
        if r.get('error_message'):
            failures.append(entry)
        else:
            version = d['model']+'-mock' if d['provider'] == 'mock' else d['model']
            if r['model_version'] != version:
                raise ValueError('Returned model identity differs')
            # Reuse all returned observations, including parse failures; no outcome selection.
            reused.append(entry)
    if set(found) != set(indexed):
        raise ValueError(f'Missing source records: found {len(found)}; inventory requires {len(indexed)}')
    if len(failures) != inventory['n_api_failures']:
        raise ValueError('Failure count differs from inventory')
    ledger = {'schema_version': '1.0', 'source_root': str(source),
              'design_hash': manifest['design_hash'],
              'source_inventory_sha256': sha(inventory_bytes),
              'wrapper_sha256': sha(Path(__file__).read_bytes()),
              'reused': reused, 'preserved_failed_attempts': failures,
              'planned': d['planned_calls'], 'remaining': d['planned_calls']-len(reused),
              'rule': 'Reuse every nonterminal observation unchanged; fill only unfilled slots. '
                      'Original failures remain in source; collection gap must be disclosed.'}
    ledger_bytes = json.dumps(ledger, indent=2, ensure_ascii=False).encode('utf-8')
    if target.exists() and any(target.iterdir()) and not (target/'continuation.json').exists():
        raise ValueError('Destination is not a recognised continuation')
    # Write ledger first so an interrupted copy can be resumed and checked.
    preserve(target/'continuation.json', ledger_bytes)
    preserve(target/'manifest.json', (source/'manifest.json').read_bytes())
    for entry in reused:
        key = entry['record_key']
        preserve(target/'records'/f'{key}.json', found[key])
    print(f'Configuration neutral | N={d["n"]}/cell | seed={d["root_seed"]} | '
          f'planned={d["planned_calls"]} | reused={len(reused)} | remaining={ledger["remaining"]}', flush=True)
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-root', type=Path, required=True)
    parser.add_argument('--run-root', type=Path, required=True)
    parser.add_argument('--execute', action='store_true', help='Dispatch paid calls for an OpenAI source')
    parser.add_argument('--missing-only', action='store_true',
                        help='Collect never-inventoried slots while original payloads are on another computer')
    parser.add_argument('--limit', type=int)
    parser.add_argument('--concurrency', type=int, choices=range(1, 6), default=5)
    args = parser.parse_args()
    if args.limit is not None and args.limit <= 0:
        parser.error('limit must be positive')
    if args.missing_only:
        manifest, reserved = prepare_shard(args.source_root, args.run_root)
        sink = ShardSink(args.run_root/'records', reserved)
    else:
        manifest = prepare(args.source_root, args.run_root)
        sink = ValiditySink(args.run_root/'records')
    if not args.execute:
        print('Prepared only; no API calls made.')
        return
    d = manifest['design']
    if d['provider'] == 'openai':
        if not os.environ.get('OPENAI_API_KEY'):
            parser.error('Configure OPENAI_API_KEY outside chat/source before execution')
        client = LLMClient(model=d['model'], concurrency=args.concurrency)
    elif d['provider'] == 'mock':
        client = MockClient(responder=mock_response, concurrency=args.concurrency)
    else:
        parser.error('Unsupported source provider')
    try:
        asyncio.run(execute(manifest, client=client, sink=sink,
                            concurrency=args.concurrency, limit=args.limit))
    finally:
        score(args.run_root)
        if args.missing_only:
            print('SHARD ONLY: original responses remain absent; this is not the completed source sweep.')


if __name__ == '__main__':
    main()
