import asyncio
from copy import deepcopy
from dataclasses import replace
import json
from pathlib import Path
import sys

import pytest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'code'))
import run_validity_joint_wording as probe
from engine.llm_client import MockClient
from engine.validity_sweep import digest


class Client(MockClient):
    async def complete(self,*args,**kwargs):
        r=await super().complete(*args,**kwargs)
        return replace(r,model_version=probe.base.MODEL,provider='openai',
                       raw_response={'usage':{'prompt_tokens':1000,'completion_tokens':100}})


def test_approved_templates_exact_profile_and_full_mock(tmp_path):
    m=probe.prepare(tmp_path);probe.base.check(m)
    templates=probe.load_reviewed_paraphrases(probe.PARAPHRASES)
    prior=json.loads((probe.PREVIOUS/'manifest.json').read_bytes())
    for c in m['design']['cells']:
        system,p=probe.variant_prompt('MoR',c['value'],'hybrid',template=templates.get(c['arm']))
        assert c['messages'][0]['content']==probe.previous_run.replace_pd(system,c['pd_value'])
        assert c['profile']=={**p['parameter_values'],'PD':c['pd_value']}
        assert len(c['profile'])==10
        old=next(x for x in prior['design']['cells'] if x['value']==c['value'] and x['background_value']==c['pd_value'])
        assert c['messages'][1:]==old['messages'][1:]
        if c['arm']=='canonical':assert c['messages']==old['messages']
    jobs=list(probe.base.jobs(m['design']))
    assert len(jobs)==480 and len({j[3] for j in jobs})==480
    assert m['design']['full_dispatch_reserve_usd']<=probe.CAP
    assert m['design']['prior_conservative_charge_usd']+probe.CAP<9
    client=Client(responder=lambda messages,seed:'DECISION: WAIT\nREASONING: Test.')
    blocked=deepcopy(m);blocked['design']['spending_ceiling_usd']=0;blocked['design_hash']=digest(blocked['design'])
    with pytest.raises(RuntimeError,match='spending guard'):
        asyncio.run(probe.base.execute(tmp_path,blocked,client))
    assert client.n_calls==0 and probe.score(tmp_path,m)['status']=='INCOMPLETE'
    asyncio.run(probe.base.execute(tmp_path,m,client));asyncio.run(probe.base.execute(tmp_path,m,client))
    assert client.n_calls==480
    result=probe.score(tmp_path,m)
    assert result['status']=='NO_GROSS_DIFFERENCE_DETECTED_NOT_VALIDATED'
    assert len(result['wording_pair_contrasts'])==24


def evidence(different=False):
    rows=[];planned={}
    for arm in probe.ARMS:
        for pd in (.1,.9):
            for mor in (.1,.9):
                for i in range(30):
                    key=f'{arm}/{pd}/{mor}/{i}'
                    planned[key]=({'pd_value':pd,'value':mor},i,i)
                    yes=different and arm=='paraphrase_3' and pd==.9 and mor==.9
                    rows.append({'record_key':key,'arm':arm,'parse_status':'ok','parsed_decision':'ADOPT' if yes else 'WAIT',
                                 'terminal_failure':False,'response_payload':{'usage':{'prompt_tokens':100,'completion_tokens':10}}})
    return rows,planned


def test_family_intervals_missing_and_failure_not_hidden():
    rows,planned=evidence(True);result=probe.assess(rows,planned)
    assert result['status']=='GROSS_LOCAL_WORDING_FAILURE_DETECTED'
    assert result['n_pairs_detecting_gross_difference']==3
    assert all(p['pd_value']==.9 and p['mor_value']==.9 for p in result['wording_pair_contrasts'] if p['gross_difference_over_10pp'])
    for p in result['wording_pair_contrasts']:
        if p['gross_difference_over_10pp']:
            assert p['difference']==1 and .1<p['simultaneous95_interval_unknown_envelope'][0]<1
    empty=probe.assess([],planned)
    assert empty['status']=='INCOMPLETE'
    assert all(p['simultaneous95_interval_unknown_envelope']==[-1,1] for p in empty['wording_pair_contrasts'])
    rows[0]['terminal_failure']=True
    assert probe.assess(rows,planned)['status']=='INVALID_SCREEN'


def test_failure_stops_and_preserves_no_retry(tmp_path):
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
