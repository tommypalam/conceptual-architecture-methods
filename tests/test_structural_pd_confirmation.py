import asyncio
from dataclasses import replace
from pathlib import Path
import sys
import numpy as np

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'code'))
import run_structural_pd_confirmation as pd_run
from engine.llm_client import MockClient


def test_allocation_preserves_source_and_separates_backgrounds():
    d=pd_run.build()
    assert len(d['cells'])==100 and d['n_backgrounds']==25
    assert d['other_package_reserved_usd']+d['full_dispatch_reserve_usd']<25
    for b in range(25):
        cells=[c for c in d['cells'] if c['background']==b]
        assert len(cells)==4
        for p in pd_run.run.utils.PARAM_NAMES:
            if p!='PD':assert len({c['profile'][p] for c in cells})==1
        assert {c['target_label'] for c in cells}=={'WAIT','FORMAL_REPORT'}
    assert len({j[3] for j in pd_run.run.jobs(d)})==100


def test_exact_interval_and_test_handle_ties_and_discordance():
    tie=pd_run.exact_effect(np.zeros(25))
    assert tie['p_two_sided']==1 and tie['simultaneous95'][0]<0<tie['simultaneous95'][1]
    result=pd_run.exact_effect([1]*5+[0]*20)
    assert result['p_two_sided']==.0625
    positive=pd_run.exact_effect([1]*25)
    negative=pd_run.exact_effect([-1]*25)
    assert positive['simultaneous95'][0]>0
    assert np.allclose(positive['simultaneous95'],[-x for x in negative['simultaneous95'][::-1]])


def test_full_mock_exec_and_exact_joint_assessment(tmp_path):
    d=pd_run.build();m={'design':d,'design_hash':pd_run.digest(d)}
    by_messages={pd_run.digest(c['messages']):c for c in d['cells']}
    class Client(MockClient):
        async def complete(self,messages,**kwargs):
            c=by_messages[pd_run.digest([vars(v) for v in messages])]
            label=c['target_label'] if c['value']==.9 else next(v for v in c['labels'] if v!=c['target_label'])
            self._responder=lambda messages,seed:f'DECISION: {label}\nREASONING: Synthetic control.'
            r=await super().complete(messages,**kwargs)
            return replace(r,model_version=pd_run.run.base.MODEL,provider='openai',raw_response={
                'id':r.api_call_id,'model':pd_run.run.base.MODEL,'choices':[{'message':{'content':r.text}}],
                'usage':{'prompt_tokens':100,'completion_tokens':50}})
    asyncio.run(pd_run.run.execute(tmp_path,m,Client()))
    _,rows,_=pd_run.run.inventory(tmp_path,m)
    result=pd_run.assess(rows,m)
    assert result['complete'] and result['both_supported'] and len(rows)==100
    assert all(g['effect']==1 for g in result['groups'])
