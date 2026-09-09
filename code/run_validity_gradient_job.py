"""Run the authorised gradient extension with durable status, scoring and backup."""
import argparse
import json
import msvcrt
import os
from pathlib import Path
import subprocess
import sys
import time

from engine.llm_client import utc_now_iso
from engine.validity_sweep import ValiditySink, digest
from run_validity_restart_followups import archive

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-root', type=Path, required=True)
    parser.add_argument('--run-root', type=Path, required=True)
    parser.add_argument('--yes', action='store_true')
    args = parser.parse_args()
    if not args.yes or not os.environ.get('OPENAI_API_KEY'):
        parser.error('Require --yes and configured OPENAI_API_KEY')
    root = args.run_root.resolve()
    manifest = json.loads((root/'manifest.json').read_text(encoding='utf-8'))
    design = manifest['design']
    if digest(design) != manifest['design_hash'] or design['experiment'] != 'gradients':
        raise ValueError('Require a valid frozen gradient design')
    if Path(design['source_root']).resolve() != args.source_root.resolve():
        raise ValueError('Source path differs from frozen design')
    logs = ROOT/'output'/'validity_gradients_20260909'
    logs.mkdir(parents=True, exist_ok=True)
    lock = (logs/'job.lock').open('a+b')
    lock.write(b'0'); lock.flush(); lock.seek(0)
    msvcrt.locking(lock.fileno(), msvcrt.LK_NBLCK, 1)

    def status(stage, **details):
        payload = {'updated_at': utc_now_iso(), 'stage': stage, 'pid': os.getpid(),
                   'run_root': str(root), 'planned': design['planned_calls'],
                   'records': sum(1 for _ in (root/'records').rglob('*.json')),
                   'phase_status': 'OPEN', **details}
        temporary = logs/'status.tmp'
        temporary.write_text(json.dumps(payload, indent=2), encoding='utf-8')
        temporary.replace(logs/'status.json')
        print(json.dumps(payload), flush=True)

    try:
        command = [sys.executable, '-u', '-B', str(ROOT/'code'/'run_validity_followup.py'),
                   '--source-root', str(args.source_root.resolve()), '--run-root', str(root),
                   '--experiment', 'gradients', '--provider', 'openai', '--n', str(design['n']), '--yes']
        with (logs/'run.log').open('a', encoding='utf-8') as stream:
            child = subprocess.Popen(command, cwd=ROOT, stdout=stream, stderr=subprocess.STDOUT)
            while child.poll() is None:
                status('running', child_pid=child.pid)
                time.sleep(20)
        if child.returncode:
            raise RuntimeError(f'Gradient runner exited {child.returncode}; inspect run.log; attempts preserved')
        rows = list(ValiditySink(root/'records').read_all())
        keys = [r['record_key'] for r in rows]
        if len(rows) != design['planned_calls'] or len(set(keys)) != len(rows):
            raise ValueError('Incomplete or duplicate gradient observations')
        if any(r['design_hash'] != manifest['design_hash'] or r.get('error_message') or
               r['model_version'] != design['model'] for r in rows):
            raise ValueError('Gradient design/model/API failure')
        status('creating_backup')
        archive(root)
        reports = []
        for path in (root/'analysis').glob('cells_*.json'):
            report = json.loads(path.read_text(encoding='utf-8'))
            if 'gradients' in report and sum(c['n_recorded'] for c in report['cells']) == design['planned_calls']:
                reports.append(path)
        if len(reports) != 1:
            raise ValueError('Expected one complete gradient analysis')
        gradient_report = reports[0]
        report_command = [sys.executable, '-B', str(ROOT/'code'/'report_validity_phase.py'),
            '--sweep-report', str(args.source_root.resolve()/'analysis'/'summary_8d2d0ab58fff59f9.json'),
            '--audit-report', str(root.parent/'claude_audit_20260909_brief_r3'/'analysis'/'audit_cc085a29d6576c92.json'),
            '--gradient-report', str(gradient_report), '--out', str(root.parent/'phase_review_20260909')]
        subprocess.run(report_command, cwd=ROOT, check=True)
        status('complete', gradient_report=str(gradient_report),
               note='Collection/scoring complete; phase still requires paraphrases and scientific review')
    except Exception as exc:
        status('stopped_error', error=str(exc))
        raise


if __name__ == '__main__':
    main()
