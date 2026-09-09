"""Link an unchanged brief-audit design after a malformed provider response."""
import argparse
import hashlib
import json
from pathlib import Path

from engine.validity_sweep import digest, verify_record
from run_validity_continuation import preserve
from run_validity_audit_brief import parse_brief


def prepare(source, target):
    source, target = source.resolve(), target.resolve()
    if source == target or source in target.parents or target in source.parents:
        raise ValueError('Require separate run directories')
    manifest_bytes = (source/'manifest.json').read_bytes()
    manifest = json.loads(manifest_bytes)
    design = manifest['design']
    if digest(design) != manifest['design_hash'] or design.get('format_version') != 'compact_json_optional_15_word_note_v1':
        raise ValueError('Require the frozen brief-audit design')
    expected = {j['item_id']: j['messages'] for j in design['jobs']}
    reused, failed, seen, payloads = [], [], set(), {}
    for path in sorted((source/'records').glob('*.json')):
        data = path.read_bytes()
        row = json.loads(data)
        verify_record(row)
        ident = row['item_id']
        if (ident not in expected or ident in seen or path.stem != ident or row['record_key'] != ident
                or row['design_hash'] != manifest['design_hash'] or row['request_messages'] != expected[ident]):
            raise ValueError('Unexpected or incompatible source record')
        seen.add(ident)
        entry = {'item_id': ident, 'record_hash': row['record_hash'],
                 'file_sha256': hashlib.sha256(data).hexdigest(), 'source_path': str(path)}
        if row['parse_status'] != 'ok':
            failed.append({**entry, 'validation_error': row.get('validation_error')})
        else:
            if row['model_version'] != design['model'] or row.get('error_message'):
                raise ValueError('Invalid model or provider result')
            estimates, commentary = parse_brief(row['raw_response'])
            if estimates != row['estimates'] or commentary != row['commentary']:
                raise ValueError('Stored parse differs from frozen parser')
            reused.append(entry)
            payloads[ident] = data
    ledger = {'design_hash': manifest['design_hash'], 'source_root': str(source),
              'source_manifest_sha256': hashlib.sha256(manifest_bytes).hexdigest(),
              'reused': reused, 'preserved_failed_attempts': failed,
              'remaining': len(expected)-len(reused),
              'rule': 'Reuse every valid response without outcome-based selection. Preserve failed source '
                      'responses separately and link new attempts; unchanged prompt/model/sample/scoring.'}
    if target.exists() and any(target.iterdir()) and not (target/'continuation.json').exists():
        raise ValueError('Destination is not a recognised continuation')
    preserve(target/'continuation.json', json.dumps(ledger, indent=2).encode())
    preserve(target/'manifest.json', manifest_bytes)
    for ident, data in payloads.items():
        preserve(target/'records'/f'{ident}.json', data)
    print(f'Copied unchanged: {len(reused)} | preserved failed attempts: {len(failed)} | remaining: {ledger["remaining"]}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-root', type=Path, required=True)
    parser.add_argument('--run-root', type=Path, required=True)
    args = parser.parse_args()
    prepare(args.source_root, args.run_root)
