"""Export checked, local-only research summaries for the educational viewer."""
import hashlib
import json
from pathlib import Path
import phase4_conflict_tasks as tasks

ROOT=Path(__file__).resolve().parents[1]

def checked(path):
    envelope=json.loads(path.read_text(encoding='utf-8'))
    raw=json.dumps(envelope['payload'],sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
    if hashlib.sha256(raw).hexdigest()!=envelope['sha256']:raise ValueError('Changed source artifact')
    return envelope['payload']

def build():
    path=ROOT/'experiments/phase4_coding/moral_capstone_r1/results.json'
    result=checked(path)
    parameters=json.loads((ROOT/'docs/variables.json').read_text(encoding='utf-8'))['variables']
    data={'study':'moral_capstone_r1','date':'15 September 2026','source_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
        'cells':result['cells'],'tasks':{t:tasks.task(t) for t in ('witness_cost','safety_hold')},
        'framing':tasks.COMMON_FRAMING,
        'parameters':[{k:v[k] for k in ('name','label','endpoint_0','endpoint_1')} for v in parameters if v.get('role')=='agent_parameter']}
    replication=ROOT/'experiments/phase4_coding/moral_capstone_r3/results.json'
    data['replication_cells']=checked(replication)['cells']
    latest=ROOT/'experiments/phase4_coding/phase4b_profiled_r1/results.json'
    data['latest']=checked(latest)['analysis']
    data['source_hashes']={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (path,replication,latest)}
    data['date']='16 September 2026'
    (ROOT/'viewer/thesis-evidence.json').write_bytes((json.dumps(data,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
    print('Exported original and replication cells, Phase 4B analysis and 10 parameter definitions; no API calls.')

if __name__=='__main__':build()
