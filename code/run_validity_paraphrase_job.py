"""Run approved paraphrases with durable status, existing scoring, and local backup."""
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
from engine.validity_variants import load_reviewed_paraphrases
from run_validity_restart_followups import archive

ROOT=Path(__file__).resolve().parents[1]


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source-root',type=Path,required=True)
    p.add_argument('--run-root',type=Path,required=True)
    p.add_argument('--baseline-root',type=Path,required=True)
    p.add_argument('--review-bundle',type=Path,required=True)
    p.add_argument('--yes',action='store_true',required=True)
    a=p.parse_args()
    if not os.environ.get('OPENAI_API_KEY'):
        p.error('Require configured OPENAI_API_KEY')
    root=a.run_root.resolve()
    manifest=json.loads((root/'manifest.json').read_text(encoding='utf-8')); d=manifest['design']
    if digest(d)!=manifest['design_hash'] or d['experiment']!='paraphrases':
        raise ValueError('Require frozen paraphrase design')
    load_reviewed_paraphrases(a.review_bundle)
    logs=ROOT/'output'/'validity_paraphrases_20260909'; logs.mkdir(parents=True,exist_ok=True)
    lock=(logs/'job.lock').open('a+b'); lock.write(b'0'); lock.flush(); lock.seek(0)
    msvcrt.locking(lock.fileno(),msvcrt.LK_NBLCK,1)

    def status(stage,**extra):
        payload={'updated_at':utc_now_iso(),'stage':stage,'pid':os.getpid(),
            'run_root':str(root),'planned':d['planned_calls'],
            'records':sum(1 for _ in (root/'records').rglob('*.json')),'phase_status':'OPEN',**extra}
        temp=logs/'status.tmp'; temp.write_text(json.dumps(payload,indent=2),encoding='utf-8')
        temp.replace(logs/'status.json'); print(json.dumps(payload),flush=True)

    try:
        command=[sys.executable,'-u','-B',str(ROOT/'code/run_validity_followup.py'),
            '--source-root',str(a.source_root.resolve()),'--run-root',str(root),
            '--baseline-root',str(a.baseline_root.resolve()),'--paraphrases',str(a.review_bundle.resolve()),
            '--experiment','paraphrases','--provider','openai','--n',str(d['n']),'--yes']
        with (logs/'run.log').open('a',encoding='utf-8') as stream:
            child=subprocess.Popen(command,cwd=ROOT,stdout=stream,stderr=subprocess.STDOUT)
            while child.poll() is None:
                status('running',child_pid=child.pid); time.sleep(20)
        if child.returncode:
            raise RuntimeError(f'Paraphrase runner exited {child.returncode}; inspect run.log; attempts preserved')
        rows=list(ValiditySink(root/'records').read_all())
        keys=[r['record_key'] for r in rows]
        expected={f"{c['variant']}/{c['parameter']}/{c['problem']}/{c['value']:.1f}/call_{k:04d}"
            for c in d['cells'] for k in range(1,d['n']+1)}
        if len(keys)!=d['planned_calls'] or len(set(keys))!=len(keys) or set(keys)!=expected:
            raise ValueError('Missing, duplicate or unexpected observations')
        if any(r['design_hash']!=manifest['design_hash'] or r.get('error_message') or
               r['model_version']!=d['model'] for r in rows):
            raise ValueError('Design/model/API failure')
        reports=[]
        for path in (root/'analysis').glob('cells_*.json'):
            report=json.loads(path.read_text(encoding='utf-8'))
            if 'paraphrase_equivalence' in report and sum(c['n_recorded'] for c in report['cells'])==d['planned_calls']:
                reports.append(path)
        if len(reports)!=1:
            raise ValueError('Expected one complete equivalence report')
        status('creating_backup'); archive(root)
        subprocess.run([sys.executable,'-B',str(ROOT/'code/report_validity_phase.py'),
            '--sweep-report',str(a.source_root.resolve()/'analysis/summary_8d2d0ab58fff59f9.json'),
            '--audit-report',str(root.parent/'claude_audit_20260909_brief_r3/analysis/audit_cc085a29d6576c92.json'),
            '--gradient-report',str(root.parent/'gradients_20260909_final/analysis/cells_6f4ee2cee96409c4.json'),
            '--paraphrase-report',str(reports[0]),'--out',str(root.parent/'phase_review_20260909')],cwd=ROOT,check=True)
        status('complete',paraphrase_report=str(reports[0]),note='Battery collected; scientific review still required')
    except Exception as exc:
        status('stopped_error',error=str(exc)); raise


if __name__=='__main__':
    main()
