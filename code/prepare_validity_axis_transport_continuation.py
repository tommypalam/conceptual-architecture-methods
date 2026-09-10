"""Prepare unsent slots after connection errors or timeouts; frozen executor unchanged."""
import argparse
import hashlib
import json
from pathlib import Path

from engine.validity_sweep import ValiditySink,digest,freeze
from prepare_validity_axis_revision import ROOT
from run_validity_claude import save_new
import run_validity_axis_revision as core


def prepare(source,root):
    source,root=Path(source).resolve(),Path(root).resolve()
    m=json.loads((source/'manifest.json').read_text(encoding='utf-8'));d=m['design']
    if digest(d)!=m['design_hash']:raise ValueError('Core design damaged')
    core.check_approval(m,source/'review_approved.json')
    rows=list(ValiditySink(source/'records').read_all());planned=core.jobs(d)
    seen={r['record_key'] for r in rows}
    if len(seen)!=len(rows) or not seen<={k for k,_,_ in planned}:raise ValueError('Invalid source allocation')
    if any(r['design_hash']!=m['design_hash'] or r.get('model_version_mismatch') for r in rows):
        raise ValueError('Source model/design mismatch')
    failures=[r for r in rows if r.get('error_message')]
    if not failures or any(not r['error_message'].startswith(('APIConnectionError:','APITimeoutError:')) for r in failures):
        raise ValueError('Recovery limited to connection errors and request timeouts')
    allocation=[key for key,_,_ in planned if key not in seen]
    if not allocation:raise ValueError('No undispatched slots')
    sources=dict(d['source_hashes'])
    for name in ('code/run_validity_axis_continuation.py','code/prepare_validity_axis_transport_continuation.py'):
        sources[name]=hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
    cm=freeze(root/'manifest.json',{
        'phase':d['phase'],'experiment':'axis_instruction_transport_continuation',
        'source_root':str(source),'core_design_hash':m['design_hash'],
        'planned_calls':len(allocation),'allocation':allocation,
        'reserved_source_records':{r['record_key']:r['record_hash'] for r in rows},
        'preserved_failures':[r['record_key'] for r in failures],
        'prior_recorded_cost_usd':sum(core.cost(r) for r in rows),
        'total_pilot_dispatch_guard_usd':d['collection']['spending_ceiling_usd'],
        'source_hashes':sources,
        'rule':'Only never-dispatched original slots. All failures reserved. Frozen transport, prompts, settings, seeds, N and statistical analysis unchanged.'})
    save_new(root/'authorization.json',{
        'source_approval_sha256':hashlib.sha256((source/'review_approved.json').read_bytes()).hexdigest(),
        'basis':'Existing exact pilot approval and instruction to continue; technical recovery only, no failed request repeated.'})
    return cm


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source-root',type=Path,required=True);p.add_argument('--run-root',type=Path,required=True)
    a=p.parse_args();print('Prepared never-dispatched slots:',prepare(a.source_root,a.run_root)['design']['planned_calls'])
