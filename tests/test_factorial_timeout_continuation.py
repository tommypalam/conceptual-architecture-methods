import asyncio
from dataclasses import replace
from pathlib import Path
import sys

import pytest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'code'))
import continue_repetition_factorial as resume
from engine.llm_client import MockClient

SOURCE=resume.probe.BASE/'repetition_factorial_20260911'


class Client(MockClient):
    async def complete(self,*args,**kwargs):
        r=await super().complete(*args,**kwargs)
        return replace(r,model_version=resume.base.MODEL,provider='openai',
                       raw_response={'usage':{'prompt_tokens':1500,'completion_tokens':100}})


def test_only_unsent_requests_collected_and_parent_timeout_unchanged(tmp_path):
    target=tmp_path/'continuation';m=resume.prepare(SOURCE,target)
    _,old,_=resume.base.inventory(SOURCE,m);old_seeds={r['seed'] for r in old}
    sent=[]
    def respond(messages,seed):
        assert seed not in old_seeds
        sent.append(seed)
        return 'DECISION: WAIT\nREASONING: Test.'
    client=Client(responder=respond)
    asyncio.run(resume.execute(target,m,client));asyncio.run(resume.execute(target,m,client))
    assert client.n_calls==381 and len(set(sent))==381
    resume.verify_parent(target,m)
    _,rows,_=resume.base.inventory(target,m)
    assert len(rows)==720 and sum(r['terminal_failure'] for r in rows)==1
    assert resume.probe.score(target,m)['status']=='INVALID_SCREEN'


def test_new_failure_stops_without_revisiting_parent_timeout(tmp_path):
    target=tmp_path/'continuation';m=resume.prepare(SOURCE,target)
    class Failed(Client):
        async def complete(self,*args,**kwargs):
            return replace(await super().complete(*args,**kwargs),error='Test new timeout')
    client=Failed(responder=lambda messages,seed:'DECISION: WAIT\nREASONING: Test.')
    with pytest.raises(RuntimeError,match='New failure'):
        asyncio.run(resume.execute(target,m,client))
    with pytest.raises(ValueError,match='New failure'):
        asyncio.run(resume.execute(target,m,client))
    assert client.n_calls==3
    resume.verify_parent(target,m)
