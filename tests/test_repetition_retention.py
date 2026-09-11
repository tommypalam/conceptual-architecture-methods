import asyncio
from copy import deepcopy
from dataclasses import replace
import json
from pathlib import Path
import sys

import pytest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'code'))
import run_validity_repetition_retention as probe
from engine.llm_client import MockClient
from engine.validity_sweep import digest


def test_frozen_sources_and_complete_guarded_mock(tmp_path):
    m=probe.prepare(tmp_path); probe.base.check(m)
    old=json.loads((probe.PREVIOUS/'manifest.json').read_bytes())['design']['cells']
    gradients=json.loads((probe.GRADIENTS/'manifest.json').read_bytes())['design']['cells']
    for c in m['design']['cells']:
        original=next(x for x in old if x['arm']=='repetition' and x['value']==c['value'])
        variant=original if c['arm']=='full_harness' else next(x for x in gradients if
            (x['variant'],x['parameter'],x['problem'],x['value'])==(c['arm'],'MoR','S3',c['value']))
        assert c['profile']==original['profile']==variant['profile']
        assert c['messages'][0]==variant['messages'][0]
        assert c['messages'][-1]==original['messages'][-1]
    jobs=list(probe.base.jobs(m['design']))
    assert len(jobs)==450 and len({j[3] for j in jobs})==450
    assert m['design']['full_dispatch_reserve_usd']<3
    assert m['design']['prior_settled_token_estimate_usd']+3<9
    class Client(MockClient):
        async def complete(self,*args,**kwargs):
            r=await super().complete(*args,**kwargs)
            return replace(r,model_version=probe.base.MODEL,provider='openai',
                raw_response={'usage':{'prompt_tokens':1500,'completion_tokens':100}})
    client=Client(responder=lambda messages,seed:'DECISION: WAIT\nREASONING: Test.')
    blocked=deepcopy(m); blocked['design']['spending_ceiling_usd']=0; blocked['design_hash']=digest(blocked['design'])
    with pytest.raises(RuntimeError,match='spending guard'):
        asyncio.run(probe.base.execute(tmp_path,blocked,client))
    assert client.n_calls==0 and probe.score(tmp_path,m)['status']=='INCOMPLETE'
    asyncio.run(probe.base.execute(tmp_path,m,client)); asyncio.run(probe.base.execute(tmp_path,m,client))
    assert client.n_calls==450
    r=probe.score(tmp_path,m)
    assert r['status']=='RETENTION_NOT_ASSESSABLE_CONTROL_CRITERION_NOT_MET'
    assert all(x['assessment']=='not_assessable' for x in r['retention'])


def evidence(counts):
    planned={};rows=[]
    for arm in probe.ARMS:
        for value,k in zip(probe.VALUES,counts[arm]):
            for i in range(30):
                key=f'{arm}/{value}/{i}'
                planned[key]=({'value':value,'labels':['ADOPT','WAIT']},i,i)
                rows.append({'record_key':key,'arm':arm,'problem_id':'S3','call_index':i+1,
                             'parse_status':'ok','parsed_decision':'ADOPT' if i<k else 'WAIT',
                             'terminal_failure':False,'response_payload':{'usage':{'prompt_tokens':100,'completion_tokens':10}}})
    return rows,planned


def test_fresh_control_and_original_half_slope_rule():
    counts={'full_harness':[1,5,11,20,27],'numeric_only':[8,10,11,12,14],'verbal_only':[1,7,14,20,27]}
    rows,planned=evidence(counts); r=probe.assess(rows,planned)
    by={x['variant']:x for x in r['retention']}
    assert r['status']=='RETENTION_CRITERION_NOT_MET'
    assert by['numeric_only']['absolute_logit_slope_ratio']<.5 and not by['numeric_only']['criterion_met']
    assert by['verbal_only']['criterion_met']
    counts['numeric_only']=counts['verbal_only']
    rows,planned=evidence(counts)
    assert probe.assess(rows,planned)['status']=='BOTH_RETENTION_CHECKS_MET_NOT_VALIDATED'
    counts['full_harness']=[1,8,5,20,27]  # Positive slope, failed observed monotonicity.
    rows,planned=evidence(counts); r=probe.assess(rows,planned)
    assert r['status']=='RETENTION_NOT_ASSESSABLE_CONTROL_CRITERION_NOT_MET'
    assert all(not x['criterion_met'] and x['assessment']=='not_assessable' for x in r['retention'])
