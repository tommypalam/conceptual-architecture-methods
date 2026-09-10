"""Combine interrupted collection segments without replacing any planned slot."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil

from engine.validity_sweep import ValiditySink,digest
from run_validity_claude import save_new
import run_validity_axis_continuation as recovery


def snapshot(source,continuation,destination):
    source,continuation,destination=map(lambda p:Path(p).resolve(),(source,continuation,destination))
    m=json.loads((source/'manifest.json').read_text(encoding='utf-8'))
    cm=json.loads((continuation/'manifest.json').read_text(encoding='utf-8'))
    cd=cm['design']
    if digest(m['design'])!=m['design_hash'] or digest(cd)!=cm['design_hash']:
        raise ValueError('Manifest integrity failure')
    if Path(cd['source_root'])!=source or cd['core_design_hash']!=m['design_hash']:
        raise ValueError('Wrong continuation parent')
    original=list(ValiditySink(source/'records').read_all())
    new=list(ValiditySink(continuation/'records').read_all())
    if {r['record_key']:r['record_hash'] for r in original}!=cd['reserved_source_records']:
        raise ValueError('Parent snapshot changed')
    keys=[r['record_key'] for r in original+new]
    if len(keys)!=len(set(keys)) or not set(keys)<={k for k,_,_ in recovery.core.jobs(m['design'])}:
        raise ValueError('Invalid or overlapping allocation')
    for r in new:
        if r['record_key'] not in cd['allocation'] or r.get('continuation_manifest_hash')!=cm['design_hash']:
            raise ValueError('Invalid child provenance')
        if r['design_hash']!=m['design_hash'] or r.get('model_version_mismatch'):
            raise ValueError('Child design/model mismatch')
    recovery.core.check_approval(m,source/'review_approved.json')
    save_new(destination/'manifest.json',m)
    save_new(destination/'recovery_snapshot.json',{
        'core_design_hash':m['design_hash'],'continuation_manifest_hash':cm['design_hash'],
        'source_root':str(source),'continuation_root':str(continuation),
        'source_records':len(original),'continuation_records':len(new),
        'preserved_api_failures':sum(bool(r.get('error_message')) for r in original+new),
        'preparer_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'note':'Incomplete byte-identical collection snapshot for a new continuation. No replacement or statistical override.'})
    excluded={'manifest.json','record_checksums.json','token_usage.json','local_backup.json','recovery_snapshot.json'}
    for p in source.iterdir():
        if p.is_file() and p.name not in excluded:
            target=destination/p.name
            if target.exists():
                if target.read_bytes()!=p.read_bytes():raise ValueError('Existing preparation differs')
            else:shutil.copyfile(p,target)
    for folder,rows in ((source,original),(continuation,new)):
        for r in rows:
            rel=Path('records')/(r['record_key']+'.json');target=(destination/rel).resolve()
            if not target.is_relative_to((destination/'records').resolve()):raise ValueError('Unsafe path')
            data=(folder/rel).read_bytes();target.parent.mkdir(parents=True,exist_ok=True)
            if target.exists():
                if target.read_bytes()!=data:raise ValueError('Existing record differs')
            else:
                with target.open('xb') as stream:stream.write(data)
    return destination


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source-root',type=Path,required=True)
    p.add_argument('--continuation-root',type=Path,required=True)
    p.add_argument('--snapshot-root',type=Path,required=True)
    a=p.parse_args();print(snapshot(a.source_root,a.continuation_root,a.snapshot_root))
