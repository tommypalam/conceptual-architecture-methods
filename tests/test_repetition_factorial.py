import asyncio
from copy import deepcopy
from dataclasses import replace
import json
from pathlib import Path
import sys

import pytest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'code'))
import run_validity_repetition_factorial as probe
from engine.llm_client import MockClient
from engine.validity_sweep import digest


def test_exact_source_messages_balanced_allocations_and_full_mock(tmp_path):
    m=probe.prepare(tmp_path);probe.base.check(m)
    jobs=list(probe.base.jobs(m['design']))
    assert len(jobs)==720 and len({j[3] for j in jobs})==720
    assert m['design']['full_dispatch_reserve_usd']<4.5
    source=json.loads((probe.SWEEP/'manifest.json').read_bytes())['design']['cells']
    gradient=json.loads((probe.GRADIENTS/'manifest.json').read_bytes())['design']['cells']
    prior=json.loads((probe.PREVIOUS/'manifest.json').read_bytes())['design']['cells']
    for c in m['design']['cells']:
        if c['arm']=='repetition':
            original=next(s for s in prior if (s['arm'],s['value'])==(c['representation'],c['value']))
        elif c['representation']=='full_harness':
            original=next(s for s in source if (s['arm'],s['parameter'],s['problem'],s['value'])==('full_harness','MoR','S3',c['value']))
        else:
            original=next(s for s in gradient if (s['variant'],s['parameter'],s['problem'],s['value'])==(c['representation'],'MoR','S3',c['value']))
        assert c['messages']==original['messages'] and c['profile']==original['profile']
    for start in range(0,720,24):
        assert len({(c['arm'],c['representation'],c['value'],c['allocation']) for _,c,_,_ in jobs[start:start+24]})==24
    originals={c['messages'][-1]['content'] for c in m['design']['cells'] if c['arm']=='original'}
    class Client(MockClient):
        async def complete(self,*args,**kwargs):
            r=await super().complete(*args,**kwargs)
            return replace(r,model_version=probe.base.MODEL,provider='openai',raw_response={'usage':{'prompt_tokens':1500,'completion_tokens':100}})
    client=Client(responder=lambda messages,seed:'DECISION: '+('ADOPT' if messages[-1].content in originals else 'WAIT')+'\nREASONING: Test.')
    blocked=deepcopy(m);blocked['design']['spending_ceiling_usd']=0;blocked['design_hash']=digest(blocked['design'])
    with pytest.raises(RuntimeError,match='spending guard'):asyncio.run(probe.base.execute(tmp_path,blocked,client))
    assert client.n_calls==0
    assert probe.score(tmp_path,m)['status']=='INCOMPLETE'
    asyncio.run(probe.base.execute(tmp_path,m,client));asyncio.run(probe.base.execute(tmp_path,m,client))
    assert client.n_calls==720
    r=probe.score(tmp_path,m)
    assert r['n_valid']==720 and all(c['n_recorded']==60 for c in r['cells'])
    assert r['status']=='VERBAL_SUPPRESSION_DETECTED_NOT_VALIDATED'
    assert r['primary_verbal_average_difference']['difference']==-1
    # Average suppression need not mean changed endpoint sensitivity.
    assert all(c['difference']==0 for c in r['endpoint_effect_interactions'].values())


def test_missing_data_cannot_be_a_suppression_result(tmp_path):
    m=probe.prepare(tmp_path)
    planned={key:(c,i,seed) for key,c,i,seed in probe.base.jobs(m['design'])}
    r=probe.assess([],planned)
    assert r['status']=='INCOMPLETE' and r['primary_verbal_average_difference']['difference'] is None
    assert r['primary_verbal_average_difference']['conservative_95_interval_unknown_envelope']==[-1,1]
