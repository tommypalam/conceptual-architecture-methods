"""Run the frozen factorial with its Windows process lock outside the ZIP tree."""
import argparse
import asyncio
import hashlib
import json
import os
from pathlib import Path

from engine.llm_client import LLMClient, utc_now_iso
from engine.validity_sweep import ValiditySink, digest
from run_validity_claude import save_new
from run_validity_wording_factorial import ROOT, execute, require_approval, score


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run-root',type=Path,required=True)
    parser.add_argument('--approval',type=Path,required=True)
    parser.add_argument('--yes',action='store_true')
    args=parser.parse_args()
    if not args.yes or not os.environ.get('OPENAI_API_KEY'):
        parser.error('Real calls require --yes and a configured OPENAI_API_KEY')
    root=args.run_root.resolve()
    manifest=json.loads((root/'manifest.json').read_text(encoding='utf-8'))
    if digest(manifest['design'])!=manifest['design_hash']:
        raise ValueError('Manifest integrity failure')
    require_approval(manifest,args.approval)
    logs=ROOT/'output'/root.name
    logs.mkdir(parents=True,exist_ok=True)
    # A Windows byte-range lock inside the run directory may prevent ZIP reads.
    # Keep process-only state outside the immutable experiment archive.
    import msvcrt
    with (logs/'execution.lock').open('a+b') as lock:
        lock.write(b'0'); lock.flush(); lock.seek(0)
        msvcrt.locking(lock.fileno(),msvcrt.LK_NBLCK,1)
        save_new(root/'launcher_provenance.json',{
            'design_hash':manifest['design_hash'],
            'launcher_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'approval_sha256':hashlib.sha256(args.approval.read_bytes()).hexdigest(),
            'note':'Frozen execute/score functions unchanged; Windows process lock stored outside ZIP tree.'})
        def status(state):
            (logs/'status.json').write_text(json.dumps({
                'status':state,'timestamp_utc':utc_now_iso(),
                'design_hash':manifest['design_hash']},indent=2),encoding='utf-8')
        status('RUNNING')
        try:
            client=LLMClient(model=manifest['design']['model'],concurrency=4)
            try:
                asyncio.run(execute(manifest,client,ValiditySink(root/'records')))
            finally:
                result=score(root,manifest)
            status(result['status'])
        except BaseException:
            status('STOPPED_WITH_ERROR')
            raise


if __name__=='__main__':
    main()
