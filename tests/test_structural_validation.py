import asyncio
from copy import deepcopy
from dataclasses import replace
import json
from pathlib import Path
import sys

import pytest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'code'))
import run_structural_encoding_validation as run
from engine.llm_client import MockClient


class Client(MockClient):
    async def complete(self,*args,**kwargs):
        r=await super().complete(*args,**kwargs)
        return replace(r,model_version=run.base.MODEL,provider='openai',raw_response={
            'id':r.api_call_id,'model':run.base.MODEL,'choices':[{'message':{'content':r.text}}],
            'usage':{'prompt_tokens':1000,'completion_tokens':100}})


def test_exact_source_rendering_and_all_parameter_allocation():
    ds=[run.build(s) for s in ('diagnostics','sweep')]
    assert sum(d['full_dispatch_reserve_usd'] for d in ds)<22
    source=json.loads(run.SOURCE.read_bytes())['design']['cells']
    templates=run.load_reviewed_paraphrases(run.TEMPLATES)
    for p in run.utils.PARAM_NAMES:
        for v in run.VALUES:
            old=next(c for c in source if (c['arm'],c['parameter'],c['value'])==('full_harness',p,v))
            for variant in ('canonical',*templates,'numeric_only','verbal_only'):
                kind=variant if variant in ('numeric_only','verbal_only') else 'hybrid'
                expected,_=run.variant_prompt(p,v,kind,template=templates.get(variant))
                assert run.render(p,v,old['profile'],variant,templates)==expected
    for d in ds:
        jobs=list(run.jobs(d));assert len(jobs)==len({j[0] for j in jobs})==len({j[3] for j in jobs})==d['planned_calls']
        for c in d['cells']:
            bg=d['backgrounds'][c['background']]
            assert all(c['profile'][p]==(c['value'] if p==c['parameter'] else bg[p]) for p in bg)
            old=next(o for o in source if (o['arm'],o['parameter'],o['problem'],o['value'])==('full_harness',c['parameter'],c['problem'],c['value']))
            assert c['messages'][1:]==old['messages'][1:]
    assert {(c['parameter'],c['problem']) for c in ds[1]['cells']}=={(p,s) for p in run.utils.PARAM_NAMES for s in ('S1','S2','S3')}
    assert len({(c['parameter'],c['problem']) for c in ds[1]['cells'] if c['prespecified']})==9


def test_constant_mock_cannot_be_misclassified_and_raw_choice_preserved(tmp_path):
    d=run.build('diagnostics');m=run.freeze(tmp_path/'manifest.json',d)
    def response(messages,seed):
        label='FORMAL_REPORT' if 'FORMAL_REPORT' in messages[-1].content else 'ADOPT'
        return 'DECISION: '+label+'\nREASONING: Constant synthetic choice.'
    client=Client(responder=response)
    asyncio.run(run.execute(tmp_path,m,client))
    result=run.score(tmp_path,m)
    assert result['status']=='COMPLETE' and result['n_valid']==480
    assert all(g['endpoint_effect']==0 and not g['predicted_endpoint_supported'] for g in result['groups'])
    rows=list(run.ValiditySink(tmp_path/'records').read_all())
    assert all(r['parsed_decision'] in r['raw_response'] for r in rows)
    with pytest.raises(ValueError,match='Existing attempts'):asyncio.run(run.execute(tmp_path,m,client))


def test_signs_missing_outcomes_and_cluster_uncertainty():
    d=run.build('sweep');m={'design':d,'design_hash':run.digest(d)};rows=[]
    for _,c,i,_ in run.jobs(d):
        # Exactly half of backgrounds have effects; two values are interior.
        target=c['background']<10 and c['value']>=.7
        other=next(l for l in c['labels'] if l!=c['target_label'])
        rows.append({'cell_id':c['id'],'call_index':i,'terminal_failure':False,'parse_status':'ok',
            'parsed_decision':c['target_label'] if target else other,'response_payload':{'usage':{'prompt_tokens':1,'completion_tokens':1}}})
    result=run.assess(rows,m)
    assert result['status']=='COMPLETE' and len(result['groups'])==30
    for g in result['groups']:
        assert g['endpoint_effect']==.5 and g['interior_effect']==.5
        assert g['endpoint_nominal95']==[.3,.7]  # 20 backgrounds, not 3000 agents
        assert g['predicted_endpoint_supported'] is (True if g['prespecified'] else None)
    assert run.assess(rows[:-1],m)['status']=='INCOMPLETE_OR_INVALID'
    assert run.assess(rows[:-1],m)['groups']==[]


def test_cap_and_failure_stop_before_any_further_batch(tmp_path):
    d=run.build('diagnostics');d['spending_ceiling_usd']=0;m=run.freeze(tmp_path/'manifest.json',d)
    client=Client(responder=lambda messages,seed:'DECISION: ADOPT\nREASONING: Synthetic.')
    with pytest.raises(RuntimeError,match='spending guard'):asyncio.run(run.execute(tmp_path,m,client))
    assert client.n_calls==0
    d['spending_ceiling_usd']=4;m={'design':d,'design_hash':run.digest(d)}
    class Failed(Client):
        async def complete(self,*args,**kwargs):return replace(await super().complete(*args,**kwargs),error='Synthetic failure')
    failed=Failed(responder=lambda messages,seed:'DECISION: ADOPT\nREASONING: Synthetic.')
    with pytest.raises(RuntimeError,match='Terminal failure'):asyncio.run(run.execute(tmp_path,m,failed))
    assert failed.n_calls==3
    assert len(list(run.ValiditySink(tmp_path/'records').read_all()))==3
