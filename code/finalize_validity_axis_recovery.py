"""Wait for a successful continuation, then archive, score, verify and render locally."""
import argparse
import json
import time
from pathlib import Path

from engine.llm_client import utc_now_iso
from engine.validity_sweep import digest
from prepare_validity_axis_revision import ROOT
from report_validity_axis_revision import render
from run_validity_axis_continuation import archive_snapshot,assemble
from verify_validity_axis_collection import verify


def finalize(source,continuation,destination,wait=False):
    logs=ROOT/'output'/destination.name;logs.mkdir(parents=True,exist_ok=True)
    def status(value):
        (logs/'status.json').write_text(json.dumps({'status':value,'timestamp_utc':utc_now_iso()},indent=2),encoding='utf-8')
    try:
        status('WAITING_FOR_COLLECTION')
        collection_status=ROOT/'output'/continuation.name/'status.json'
        while True:
            current=json.loads(collection_status.read_text(encoding='utf-8'))['status']
            if current=='CONTINUATION_COLLECTED':break
            if current!='RUNNING':raise RuntimeError('Collection did not complete: '+current)
            if not wait:raise RuntimeError('Collection is still running; use --wait')
            time.sleep(10)
        status('ARCHIVING_AND_SCORING')
        archive_snapshot(continuation)
        result=assemble(source,continuation,destination)
        status('VERIFYING')
        verify(destination)
        status('RENDERING')
        render(destination,destination/'analysis'/f'axis_pilot_{digest(result)[:16]}.json')
        status('REPORT_READY_RESEARCH_REVIEW_REQUIRED')
    except BaseException:
        status('STOPPED_WITH_ERROR');raise


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source-root',type=Path,required=True)
    p.add_argument('--continuation-root',type=Path,required=True)
    p.add_argument('--destination',type=Path,required=True)
    p.add_argument('--wait',action='store_true')
    a=p.parse_args()
    finalize(a.source_root.resolve(),a.continuation_root.resolve(),a.destination.resolve(),a.wait)
