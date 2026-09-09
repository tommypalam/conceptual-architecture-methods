"""Wait for the fresh sweep, then run authorised core follow-ups and archive records.

Run as a background process. No optional gradient extension or inferred human approval.
"""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import zipfile

from engine.llm_client import utc_now_iso
from engine.validity_sweep import ValiditySink, digest, jobs
from engine.validity_variants import load_reviewed_paraphrases
from run_validity_claude import save_new

ROOT = Path(__file__).resolve().parents[1]


def validate_source(source):
    manifest = json.loads((source/'manifest.json').read_text(encoding='utf-8'))
    if digest(manifest['design']) != manifest['design_hash']:
        raise ValueError('Source manifest integrity failure')
    rows = list(ValiditySink(source/'records').read_all())
    keys = [r['record_key'] for r in rows]
    expected = {k for k, _, _ in jobs(manifest['design'])}
    if len(keys) != len(set(keys)) or not set(keys) <= expected:
        raise ValueError('Unexpected or duplicate source observations')
    for row in rows:
        if (row['design_hash'] != manifest['design_hash'] or row.get('error_message')
                or row.get('model_version_mismatch') or
                row['model_version'] != manifest['design']['model']):
            raise ValueError('Source failure or model/design mismatch; dependent work stopped')
    return len(keys) == len(expected)


def archive(root):
    manifest = json.loads((root/'manifest.json').read_text(encoding='utf-8'))
    rows = list(ValiditySink(root/'records').read_all())
    if len(rows) != manifest['design']['planned_calls']:
        raise ValueError('Cannot archive an incomplete run as complete')
    index = [{'record_key': r['record_key'], 'record_hash': r['record_hash']} for r in rows]
    inventory = {'design_hash': manifest['design_hash'], 'n_records': len(rows),
                 'n_invalid': sum(r['parse_status'] != 'ok' for r in rows),
                 'n_api_failures': sum(bool(r.get('error_message')) for r in rows),
                 'models_returned': sorted({r['model_version'] for r in rows}), 'index': index}
    save_new(root/'record_checksums.json', inventory)
    usage = {'input_tokens': 0, 'output_tokens': 0, 'cached_input_tokens': 0}
    for row in rows:
        u = (row.get('response_payload') or {}).get('usage', {})
        usage['input_tokens'] += u.get('prompt_tokens', u.get('input_tokens', 0))
        usage['output_tokens'] += u.get('completion_tokens', u.get('output_tokens', 0))
        usage['cached_input_tokens'] += u.get('prompt_tokens_details', {}).get('cached_tokens', 0)
    save_new(root/'token_usage.json', usage)
    folder = ROOT/'output'/'validity_backups'
    folder.mkdir(parents=True, exist_ok=True)
    target = folder/f'{root.name}_{digest(inventory)[:16]}.zip'
    if not target.exists():
        temporary = target.with_suffix('.zip.tmp')
        with zipfile.ZipFile(temporary, 'x', compression=zipfile.ZIP_DEFLATED) as z:
            for p in sorted(root.rglob('*')):
                if p.is_file() and not p.name.endswith('.tmp'):
                    z.write(p, p.relative_to(root).as_posix())
        temporary.rename(target)
    with zipfile.ZipFile(target) as z:
        if z.testzip() is not None:
            raise ValueError('Archive integrity failure')
    save_new(root/'local_backup.json', {'path': str(target),
             'sha256': hashlib.sha256(target.read_bytes()).hexdigest(),
             'note': 'Local same-computer archive; not an off-device backup.'})


def run_cli(logs, label, script, *args):
    log = logs/f'{label}.log'
    with log.open('a', encoding='utf-8') as stream:
        result = subprocess.run([sys.executable, '-u', '-B', str(ROOT/'code'/script),
                                 *map(str, args)], cwd=ROOT, stdout=stream, stderr=subprocess.STDOUT)
    if result.returncode:
        raise RuntimeError(f'{label} failed; see {log}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-root', type=Path, required=True)
    parser.add_argument('--claude-model', required=True)
    parser.add_argument('--review-bundle', type=Path, required=True)
    parser.add_argument('--yes', action='store_true')
    args = parser.parse_args()
    if not args.yes or not all(os.environ.get(k) for k in ('OPENAI_API_KEY', 'ANTHROPIC_API_KEY')):
        parser.error('Requires --yes and configured provider credentials')
    source = args.source_root.resolve()
    base = source.parent
    logs = ROOT/'output'/'validity_restart_20260909'
    logs.mkdir(parents=True, exist_ok=True)
    # OS-held lock releases on process exit, including crashes; avoid duplicate dispatch.
    import msvcrt
    lock_stream = (logs/'pipeline.lock').open('a+b')
    lock_stream.write(b'0')
    lock_stream.flush()
    lock_stream.seek(0)
    try:
        msvcrt.locking(lock_stream.fileno(), msvcrt.LK_NBLCK, 1)
    except OSError:
        parser.error('Another restart follow-up process already holds the execution lock')
    status_path = logs/'status.json'

    def status(stage, **details):
        payload = {'updated_at': utc_now_iso(), 'pid': os.getpid(), 'stage': stage,
                   'source_root': str(source), 'phase_status': 'OPEN', **details}
        temporary = status_path.with_suffix('.tmp')
        temporary.write_text(json.dumps(payload, indent=2), encoding='utf-8')
        temporary.replace(status_path)
        print(json.dumps(payload), flush=True)

    try:
        last_count, last_progress = -1, time.monotonic()
        while True:
            count = sum(1 for _ in (source/'records').rglob('*.json'))
            if count != last_count:
                last_count, last_progress = count, time.monotonic()
            status('waiting_for_source', records=count, target=15000)
            if (source/'records'/'failures.jsonl').exists():
                raise RuntimeError('Source failure log exists; dependent work stopped')
            if count >= 15000:
                if not validate_source(source):
                    raise ValueError('Source is incomplete')
                # Let the source CLI finish its final analysis before taking a backup.
                time.sleep(30)
                break
            if time.monotonic()-last_progress > 900:
                raise RuntimeError('Source made no progress for 15 minutes; inspect source process before resuming')
            time.sleep(30)
        archive(source)
        rotations = base/'rotations_20260909_restart'
        audit = base/'claude_audit_20260909_restart'
        pack = ROOT/'output'/'validity_audit_20260909_restart'

        def run_rotations():
            common = ('--source-root', source, '--run-root', rotations,
                      '--experiment', 'rotations', '--provider', 'openai', '--yes')
            run_cli(logs, 'rotations_checkpoint', 'run_validity_followup.py', *common, '--limit', 10)
            run_cli(logs, 'rotations', 'run_validity_followup.py', *common)
            archive(rotations)

        def run_audit():
            run_cli(logs, 'audit_prepare', 'run_validity_claude.py', 'prepare-audit',
                    '--source-root', source, '--out', pack)
            common = ('run', '--task', 'audit', '--model', args.claude_model,
                      '--blind-pack', pack/'blind_pack.json', '--run-root', audit, '--yes')
            run_cli(logs, 'audit_checkpoint', 'run_validity_claude.py', *common, '--limit', 1)
            run_cli(logs, 'audit', 'run_validity_claude.py', *common)
            run_cli(logs, 'audit_score', 'run_validity_claude.py', 'score-audit',
                    '--answer-key', pack/'private_answer_key.json', '--run-root', audit)
            archive(audit)

        status('running_rotations_and_audit', rotations_target=4500, audit_target=200)
        with ThreadPoolExecutor(max_workers=2) as pool:
            futures = [pool.submit(run_rotations), pool.submit(run_audit)]
            failures = []
            for future in futures:
                try:
                    future.result()
                except Exception as exc:
                    failures.append(str(exc))
        if failures:
            raise RuntimeError('; '.join(failures))
        try:
            load_reviewed_paraphrases(args.review_bundle)
        except (ValueError, FileNotFoundError):
            status('waiting_for_human_paraphrase_review', review_bundle=str(args.review_bundle),
                   source_complete=True, rotations_complete=True, audit_complete=True)
            return
        paraphrases = base/'paraphrases_20260909_restart'
        status('running_reviewed_paraphrases', target=4500)
        common = ('--source-root', source, '--run-root', paraphrases, '--experiment', 'paraphrases',
                  '--paraphrases', args.review_bundle, '--baseline-root', rotations,
                  '--provider', 'openai', '--yes')
        run_cli(logs, 'paraphrases_checkpoint', 'run_validity_followup.py', *common, '--limit', 10)
        run_cli(logs, 'paraphrases', 'run_validity_followup.py', *common)
        archive(paraphrases)
        status('core_collection_complete_scientific_review_required')
    except Exception as exc:
        status('stopped_error', error=str(exc))
        raise


if __name__ == '__main__':
    main()
