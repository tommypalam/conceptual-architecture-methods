import asyncio
from dataclasses import replace
import json
from pathlib import Path
import sys

import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'code'))
import run_structural_encoding_audit as audit
from engine.llm_client import MockClient


def test_blind_messages_exclude_private_profile_and_request_bounded():
    pack={'parameter_definitions':{'MS':{'endpoint_0':'local','endpoint_1':'universal'}},
          'quartile_definitions':{'1':'low','4':'high'},'private_answer_key':'SECRET_PROFILE_VALUES'}
    item={'item_id':'opaque','reasoning':'I weighed broader obligations.'}
    messages=[vars(m) for m in audit.brief_messages(pack,item)]
    assert 'SECRET_PROFILE_VALUES' not in json.dumps(messages)
    assert 'private_answer_key' not in json.dumps(messages)
    assert audit.reserve(messages)>2000*5/1e6


def test_single_attempt_failure_preserved_and_no_resume(tmp_path):
    messages=[{'role':'system','content':'Synthetic coder'},{'role':'user','content':'Synthetic reasoning'}]
    d={'model':audit.MODEL,'behavioural_reservation_usd':21.,'full_dispatch_reserve_usd':audit.reserve(messages),
       'source_hashes':{},'jobs':[{'item_id':'one','messages':messages}]}
    m={'design':d,'design_hash':audit.digest(d)}
    class Client(MockClient):
        async def complete(self,*args,**kwargs):
            r=await super().complete(*args,**kwargs)
            return replace(r,model_version=audit.MODEL,error='Synthetic timeout',raw_response=None)
    client=Client(responder=lambda messages,seed:'{}')
    with pytest.raises(RuntimeError,match='failure preserved'):asyncio.run(audit.execute(m,client,tmp_path))
    assert client.n_calls==1
    assert len(list(audit.ValiditySink(tmp_path/'records').read_all()))==1
    with pytest.raises(ValueError,match='Existing attempts'):asyncio.run(audit.execute(m,client,tmp_path))
    assert client.n_calls==1
    bad={'design':dict(d,behavioural_reservation_usd=25.),'design_hash':''};bad['design_hash']=audit.digest(bad['design'])
    with pytest.raises(ValueError,match='budget mismatch'):audit.check(bad)


def test_valid_coding_retains_brief_commentary_and_usage(tmp_path):
    messages=[{'role':'system','content':'Synthetic coder'},{'role':'user','content':'Synthetic reasoning'}]
    d={'model':audit.MODEL,'behavioural_reservation_usd':21.,'full_dispatch_reserve_usd':audit.reserve(messages),
       'source_hashes':{},'jobs':[{'item_id':'one','messages':messages}]}
    m={'design':d,'design_hash':audit.digest(d)}
    answer=json.dumps({'estimates':{p:{'quartile':None,'confidence':0.} for p in audit.run.utils.PARAM_NAMES}})+' Insufficient evidence.'
    class Client(MockClient):
        async def complete(self,*args,**kwargs):
            r=await super().complete(*args,**kwargs)
            return replace(r,model_version=audit.MODEL,provider='anthropic',raw_response={
                'id':r.api_call_id,'model':audit.MODEL,'content':[{'type':'text','text':r.text}],
                'usage':{'input_tokens':100,'output_tokens':100}})
    asyncio.run(audit.execute(m,Client(responder=lambda messages,seed:answer),tmp_path))
    row=next(audit.ValiditySink(tmp_path/'records').read_all())
    assert row['parse_status']=='ok' and row['commentary']=='Insufficient evidence.'
    assert row['commentary_word_count']==2 and audit.cost(row)==.0006
