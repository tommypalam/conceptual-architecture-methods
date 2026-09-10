"""Verify a completed axis-pilot union against frozen requests and source bytes."""
import argparse
import hashlib
import json
from pathlib import Path
import zipfile

from engine.seeding import derive_seed
from engine.validity_sweep import ValiditySink,digest
from run_validity_claude import save_new
import run_validity_axis_revision as core


def verify(root):
    root=Path(root).resolve()
    m=json.loads((root/'manifest.json').read_text(encoding='utf-8'));d=m['design']
    if digest(d)!=m['design_hash']:raise ValueError('Design integrity failure')
    core.check_approval(m,root/'review_approved.json')
    for name,expected in d['source_hashes'].items():
        if hashlib.sha256((core.ROOT/name).read_bytes()).hexdigest()!=expected:
            raise ValueError('Frozen source changed: '+name)
    rows=list(ValiditySink(root/'records').read_all())
    jobs={key:(c,k) for key,c,k in core.jobs(d)}
    if len(rows)!=d['planned_calls'] or {r['record_key'] for r in rows}!=set(jobs):
        raise ValueError('Incomplete or duplicate collection')
    lineage=json.loads((root/'collection_manifest.json').read_text(encoding='utf-8'))
    source=Path(lineage['source_root']);child=Path(lineage['continuation_root'])
    original={r['record_key']:r for r in ValiditySink(source/'records').read_all()}
    continuation={r['record_key']:r for r in ValiditySink(child/'records').read_all()}
    if original.keys()&continuation.keys() or original.keys()|continuation.keys()!=set(jobs):
        raise ValueError('Collection origins overlap or omit slots')
    seeds=set();ids=set()
    for r in rows:
        key=r['record_key'];c,k=jobs[key]
        expected_seed=derive_seed(d['seed'],c['stage'],c['arm'],c['wording'],c['problem'],c['value'],k)
        if r['seed']!=expected_seed or r['seed'] in seeds:raise ValueError('Seed mismatch or collision')
        seeds.add(r['seed'])
        if r['design_hash']!=m['design_hash'] or r['request_messages']!=c['messages'] or r['agent_parameters']!=c['profile']:
            raise ValueError('Request/profile/design mismatch')
        if r['labels']!=c['labels'] or r['call_index']!=k:raise ValueError('Slot metadata mismatch')
        if r.get('model_version_mismatch'):raise ValueError('Model mismatch')
        if not r.get('error_message'):
            if r['model_version']!=d['model'] or not r['api_call_id'] or r['api_call_id'] in ids:
                raise ValueError('Successful model identity/call ID mismatch')
            ids.add(r['api_call_id'])
        origin=source if key in original else child
        relative=Path('records')/(key+'.json')
        if (root/relative).read_bytes()!=(origin/relative).read_bytes():
            raise ValueError('Raw bytes differ from source')
    backup=json.loads((root/'local_backup.json').read_text(encoding='utf-8'))
    archive=Path(backup['path'])
    if hashlib.sha256(archive.read_bytes()).hexdigest()!=backup['sha256']:raise ValueError('ZIP hash mismatch')
    with zipfile.ZipFile(archive) as z:
        if z.testzip():raise ValueError('Corrupt ZIP')
        members=[name for name in z.namelist() if name.startswith('records/') and name.endswith('.json')]
        if len(members)!=len(rows) or len(set(members))!=len(members):raise ValueError('ZIP record count mismatch')
        for r in rows:
            relative='records/'+r['record_key']+'.json'
            if z.read(relative)!=(root/relative).read_bytes():raise ValueError('ZIP payload mismatch')
    failures=[r['record_key'] for r in rows if r.get('error_message')]
    report={'design_hash':m['design_hash'],'n_records':len(rows),
        'n_valid':sum(r['parse_status']=='ok' for r in rows),
        'n_api_failures':len(failures),'api_failure_slots':failures,
        'n_non_api_invalid':sum(r['parse_status']!='ok' and not r.get('error_message') for r in rows),
        'n_unique_requested_seeds':len(seeds),'n_unique_successful_api_ids':len(ids),
        'recorded_token_estimate_usd':sum(core.cost(r) for r in rows),
        'additional_budget_remainder_estimate_usd':48.6856535-sum(core.cost(r) for r in rows),
        'exact_requests_profiles_source_bytes_and_zip_verified':True,
        'verifier_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'note':'Integrity verification only; no statistical override. Requested seeds do not guarantee provider determinism. ZIP is same-computer storage.'}
    save_new(root/'analysis/collection_verification.json',report)
    print(json.dumps({k:v for k,v in report.items() if k!='api_failure_slots'},indent=2))
    return report


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--run-root',type=Path,required=True)
    verify(p.parse_args().run_root)
