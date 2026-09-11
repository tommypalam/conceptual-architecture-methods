import asyncio
from copy import deepcopy
from dataclasses import replace
import json
from pathlib import Path
import sys

import pytest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'code'))
import run_validity_pd_interaction as probe
from engine.llm_client import MockClient
from engine.validity_sweep import digest


class Client(MockClient):
    async def complete(self,*args,**kwargs):
        r=await super().complete(*args,**kwargs)
        return replace(r,model_version=probe.base.MODEL,provider='openai',
                       raw_response={'usage':{'prompt_tokens':500,'completion_tokens':100}})


def test_exact_numeric_change_full_mock_budget_resume(tmp_path):
    m=probe.prepare(tmp_path);probe.base.check(m)
    source=json.loads((probe.SWEEP/'manifest.json').read_bytes())['design']['cells']
    for c in m['design']['cells']:
        old=next(x for x in source if (x['arm'],x['parameter'],x['problem'],x['value'])==('full_harness','MoR','S3',c['value']))
        pd_value=.1 if c['arm']=='pd_low' else .9
        assert c['messages'][1:]==old['messages'][1:]
        original=old['messages'][0]['content'];actual=c['messages'][0]['content']
        assert actual==original.replace(' 6. Procedural Dependence: 0.56',f' 6. Procedural Dependence: {pd_value:.2f}',1)
        assert len(actual.encode())==len(original.encode())
        assert c['profile']=={**old['profile'],'PD':pd_value}
        assert len(c['profile'])==10 and c['source_full_profile']==old['profile']
        counterpart=next(x for x in m['design']['cells'] if x['value']==c['value'] and x['arm']!=c['arm'])
        assert len(actual.encode())==len(counterpart['messages'][0]['content'].encode())
    jobs=list(probe.base.jobs(m['design']))
    assert len(jobs)==300 and len({j[3] for j in jobs})==300
    assert m['design']['full_dispatch_reserve_usd']<probe.CAP
    assert m['design']['prior_conservative_charge_usd']+probe.CAP<9
    client=Client(responder=lambda messages,seed:'DECISION: WAIT\nREASONING: Test.')
    blocked=deepcopy(m);blocked['design']['spending_ceiling_usd']=0;blocked['design_hash']=digest(blocked['design'])
    with pytest.raises(RuntimeError,match='spending guard'):
        asyncio.run(probe.base.execute(tmp_path,blocked,client))
    assert client.n_calls==0 and probe.score(tmp_path,m)['status']=='INCOMPLETE'
    asyncio.run(probe.base.execute(tmp_path,m,client));asyncio.run(probe.base.execute(tmp_path,m,client))
    assert client.n_calls==300
    assert probe.score(tmp_path,m)['status']=='SLOPE_DIFFERENCE_NOT_ESTIMABLE'


def evidence(full,solo):
    rows=[];planned={}
    for arm,counts in zip(probe.ARMS,(full,solo)):
        for value,k in zip(probe.VALUES,counts):
            for i in range(30):
                key=f'{arm}/{value}/{i}'
                planned[key]=({'value':value,'labels':['ADOPT','WAIT']},i,i)
                rows.append({'record_key':key,'arm':arm,'problem_id':'S3','call_index':i+1,
                             'parse_status':'ok','parsed_decision':'ADOPT' if i<k else 'WAIT',
                             'terminal_failure':False,'response_payload':{'usage':{'prompt_tokens':100,'completion_tokens':10}}})
    return rows,planned


def test_direct_slope_contrast_not_separate_significance_and_unknowns():
    shallow=[10,12,15,18,20];steep=[1,4,15,26,29]
    a=probe.assess(*evidence(shallow,steep));b=probe.assess(*evidence(steep,shallow))
    assert a['status']=='MORE_POSITIVE_MOR_SLOPE_AT_HIGH_PD'
    assert b['status']=='LESS_POSITIVE_MOR_SLOPE_AT_HIGH_PD'
    assert a['primary_slope_difference']['estimate']==pytest.approx(-b['primary_slope_difference']['estimate'])
    assert a['primary_slope_difference']['ci95'][0]==pytest.approx(-b['primary_slope_difference']['ci95'][1])
    assert probe.assess(*evidence(steep,steep))['status']=='SLOPE_DIFFERENCE_UNRESOLVED'
    rows,planned=evidence(shallow,steep);rows[0]['terminal_failure']=True
    assert probe.assess(rows,planned)['status']=='INVALID_SCREEN'
    result=probe.assess([],planned)
    assert result['secondary_endpoint_difference']['conservative_95_interval_unknown_envelope']==[-2,2]
    assert result['primary_slope_difference']['estimate'] is None


def test_terminal_failure_is_preserved_not_retried(tmp_path):
    m=probe.prepare(tmp_path)
    class Failed(Client):
        async def complete(self,*args,**kwargs):
            return replace(await super().complete(*args,**kwargs),error='Test timeout')
    client=Failed(responder=lambda messages,seed:'DECISION: WAIT\nREASONING: Test.')
    with pytest.raises(RuntimeError,match='Terminal failure'):
        asyncio.run(probe.base.execute(tmp_path,m,client))
    with pytest.raises(ValueError,match='Preserved terminal failure'):
        asyncio.run(probe.base.execute(tmp_path,m,client))
    assert client.n_calls==3
