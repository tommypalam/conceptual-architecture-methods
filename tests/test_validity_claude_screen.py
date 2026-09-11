import asyncio
from copy import deepcopy
from dataclasses import replace
from pathlib import Path
import sys

import pytest
from scipy.stats import beta

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'code'))
import run_validity_claude_screen as screen
from engine.llm_client import MockClient
from engine.validity_sweep import ValiditySink,digest


def test_unchanged_requests_fixed_screen_no_call_resume_and_budget(tmp_path):
    original=(screen.SOURCE/'manifest.json').read_bytes()
    m=screen.prepare(tmp_path);calls=screen.jobs(m['design'])
    assert len(calls)==80 and len({k for k,_,_ in calls})==80
    for i in range(0,80,4):assert len({c['wording'] for _,c,_ in calls[i:i+4]})==4
    lookup={c['messages'][0]['content']:c['wording'] for c in m['design']['cells']}
    class Client(MockClient):
        async def complete(self,*args,**kwargs):
            assert kwargs['seed'] is None
            r=await super().complete(*args,**kwargs)
            return replace(r,model_version=screen.MODEL)
    def response(messages,seed):
        choice='ADOPT' if lookup[messages[0].content]=='paraphrase_2' else 'WAIT'
        return f'DECISION: {choice}\nREASONING: Mock only.'
    client=Client(responder=response)
    capped=deepcopy(m);capped['design']['spending_ceiling_usd']=0;capped['design_hash']=digest(capped['design'])
    with pytest.raises(RuntimeError,match='guard'):asyncio.run(screen.execute(tmp_path,capped,client))
    assert client.n_calls==0
    asyncio.run(screen.execute(tmp_path,m,client));asyncio.run(screen.execute(tmp_path,m,client))
    assert client.n_calls==80
    result=screen.score(tmp_path,m)
    assert result['status']=='GROSS_WORDING_FAILURE_DETECTED' and result['n_valid']==80
    assert result['primary_conservative_95_interval_unknown_envelope'][0]>.1
    assert (screen.SOURCE/'manifest.json').read_bytes()==original
    rows=list(ValiditySink(tmp_path/'records').read_all())
    assert len({r['api_call_id'] for r in rows})==80
    assert all(r['seed'] is None for r in rows)


def test_failure_reserved_and_interval_unknown_envelope(tmp_path):
    m=screen.prepare(tmp_path)
    class Failed(MockClient):
        async def complete(self,*args,**kwargs):
            r=await super().complete(*args,**kwargs)
            return replace(r,error='APIConnectionError: TEST',text=None,model_version=None)
    client=Failed()
    with pytest.raises(RuntimeError,match='Terminal'):asyncio.run(screen.execute(tmp_path,m,client))
    assert client.n_calls==2
    with pytest.raises(ValueError,match='Preserved'):asyncio.run(screen.execute(tmp_path,m,client))
    assert client.n_calls==2
    assert screen.score(tmp_path,m)['status']=='INCOMPLETE'
    assert screen.exact(4,20)==pytest.approx([beta.ppf(.0125,4,17),beta.ppf(.9875,5,16)])
    outer=screen.exact(4,20,2)
    for k in range(4,7):
        lo,hi=screen.exact(k,20)
        assert outer[0]<=lo and outer[1]>=hi
