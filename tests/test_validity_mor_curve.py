import asyncio
from copy import deepcopy
from dataclasses import replace
import json
from pathlib import Path
import random
import sys

import pytest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'code'))
import run_validity_mor_curve as probe
from engine.llm_client import MockClient
from engine.validity_sweep import digest


class Client(MockClient):
    async def complete(self,*args,**kwargs):
        r=await super().complete(*args,**kwargs)
        return replace(r,model_version=probe.base.MODEL,provider='openai',
                       raw_response={'usage':{'prompt_tokens':1800,'completion_tokens':100}})


def test_exact_profiles_messages_and_guarded_complete_mock_run(tmp_path):
    m=probe.prepare(tmp_path); probe.base.check(m)
    source=json.loads((probe.SWEEP/'manifest.json').read_bytes())['design']['cells']
    old=json.loads((probe.SCREEN/'manifest.json').read_bytes())['design']['cells']
    jobs=list(probe.base.jobs(m['design']))
    assert len(jobs)==300 and len({j[3] for j in jobs})==300
    assert m['design']['prior_reserved_usd']+m['design']['spending_ceiling_usd']<9
    for c in m['design']['cells']:
        origin=next(s for s in source if (s['arm'],s['parameter'],s['problem'],s['value'])==('full_harness','MoR','S3',c['value']))
        overlay=next(s for s in old if (s['arm'],s['wording'])==(c['arm'],'canonical'))
        assert c['profile']==origin['profile'] and c['messages'][0]==origin['messages'][0]
        assert c['messages'][-1]==overlay['messages'][-1]
    def response(messages,seed):
        line=next(s for s in messages[0].content.splitlines() if ' 4. Mode of Response:' in s)
        value=float(line.split(':')[-1])
        return 'DECISION: '+('ADOPT' if random.Random(seed).random()<value else 'WAIT')+'\nREASONING: Test.'
    client=Client(responder=response)
    zero=deepcopy(m); zero['design']['spending_ceiling_usd']=0; zero['design_hash']=digest(zero['design'])
    with pytest.raises(RuntimeError,match='spending guard'):
        asyncio.run(probe.base.execute(tmp_path,zero,client))
    assert client.n_calls==0
    partial=probe.score(tmp_path,m)
    assert partial['status']=='INCOMPLETE' and all(not s['criterion_met'] for s in partial['sweeps'])
    asyncio.run(probe.base.execute(tmp_path,m,client))
    asyncio.run(probe.base.execute(tmp_path,m,client))
    assert client.n_calls==300
    result=probe.score(tmp_path,m)
    assert result['n_records']==300 and result['n_missing_usage']==0
    assert all(len(s['cells'])==5 and s['complete'] for s in result['sweeps'])
    assert len(result['delivery_contrasts'])==1 and not result['historical_records_pooled']


def test_terminal_failure_cannot_be_resumed_or_declared_complete(tmp_path):
    m=probe.prepare(tmp_path)
    class Failed(Client):
        async def complete(self,*args,**kwargs):
            return replace(await super().complete(*args,**kwargs),error='Test failure')
    client=Failed(responder=lambda messages,seed:'DECISION: WAIT\nREASONING: Test.')
    with pytest.raises(RuntimeError,match='Terminal failure'):
        asyncio.run(probe.base.execute(tmp_path,m,client))
    before={p:p.read_bytes() for p in (tmp_path/'records').rglob('*.json')}
    with pytest.raises(ValueError,match='Preserved terminal failure'):
        asyncio.run(probe.base.execute(tmp_path,m,client))
    assert client.n_calls==3 and all(p.read_bytes()==b for p,b in before.items())
    assert probe.score(tmp_path,m)['status']=='INCOMPLETE'
