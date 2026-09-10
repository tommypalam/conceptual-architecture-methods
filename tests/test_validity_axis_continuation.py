import asyncio
from copy import deepcopy
from dataclasses import replace
import json
from pathlib import Path
import sys
import pytest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'code'))
from prepare_validity_axis_revision import prepare,INSTRUCTION
from engine.llm_client import MockClient
from engine.validity_sweep import ValiditySink,digest
from run_validity_claude import save_new
from run_validity_sweep import mock_response
import run_validity_axis_revision as core
import run_validity_axis_continuation as recovery
from prepare_validity_axis_recovery_snapshot import snapshot


def test_recovery_never_repeats_failed_or_successful_slots_and_preserves_bytes(tmp_path,monkeypatch):
    prepared=prepare(tmp_path/'preparation');m=deepcopy(prepared);d=m['design']
    d.update(provider='mock',model='mock-model');d['cells']=d['cells'][:2]
    for c in d['cells']:c['n']=3
    d['planned_calls']=6;m['design_hash']=digest(d)
    source=tmp_path/'original';save_new(source/'manifest.json',m)
    save_new(source/'review_approved.json',{'approved':True,'reviewer':'TEST ONLY','proposal_hash':m['design_hash'],
        'instruction_hash':digest(INSTRUCTION),'template_hashes':d['template_hashes'],'exact_messages_hash':digest([c['messages'] for c in d['cells']])})
    (source/'PROTOCOL.md').write_text('TEST PROTOCOL',encoding='utf-8')
    (source/'HUMAN_REVIEW.md').write_text('TEST REVIEW',encoding='utf-8')
    class Failing(MockClient):
        async def complete(self,*args,**kwargs):
            result=await super().complete(*args,**kwargs)
            return replace(result,error='APIConnectionError: test',text=None,model_version=None) if self.n_calls==1 else result
    with pytest.raises(RuntimeError,match='Terminal failure'):
        asyncio.run(core.execute(m,Failing(responder=mock_response),ValiditySink(source/'records')))
    original=list(ValiditySink(source/'records').read_all());assert len(original)==4
    original_bytes={r['record_key']:(source/'records'/(r['record_key']+'.json')).read_bytes() for r in original}
    shard=tmp_path/'continuation';cm=recovery.prepare(source,shard)
    assert cm['design']['planned_calls']==2 and len(cm['design']['preserved_failures'])==1
    assert set(cm['design']['allocation']).isdisjoint(original_bytes)
    client=MockClient(responder=mock_response)
    capped=deepcopy(cm);capped['design']['prior_recorded_cost_usd']=13
    capped['design_hash']=digest(capped['design'])
    with pytest.raises(RuntimeError,match='budget guard'): asyncio.run(recovery.execute(capped,client,shard))
    assert client.n_calls==0
    asyncio.run(recovery.execute(cm,client,shard));asyncio.run(recovery.execute(cm,client,shard))
    assert client.n_calls==2
    assembled=tmp_path/'assembled';monkeypatch.setattr(recovery,'archive_snapshot',lambda root:None)
    result=recovery.assemble(source,shard,assembled)
    rows=list(ValiditySink(assembled/'records').read_all())
    assert len(rows)==6 and sum(bool(r['error_message']) for r in rows)==1
    for key,data in original_bytes.items():
        assert (source/'records'/(key+'.json')).read_bytes()==data
        assert (assembled/'records'/(key+'.json')).read_bytes()==data
    assert result['status']=='LOCAL_SCREEN_NOT_MET_OR_INCOMPLETE'
    assert result['recorded_token_estimate_usd']==0
    # A snapshot of both segments reserves every original key, even a failure.
    combined=snapshot(source,shard,tmp_path/'snapshot')
    assert {r['record_key'] for r in ValiditySink(combined/'records').read_all()}=={r['record_key'] for r in rows}
    for r in rows:
        relative=Path('records')/(r['record_key']+'.json')
        assert (combined/relative).read_bytes()==(assembled/relative).read_bytes()
    with pytest.raises(ValueError,match='No undispatched'):
        recovery.prepare(combined,tmp_path/'empty')
    changed=deepcopy(cm);changed['design']['reserved_source_records']={};changed['design_hash']=digest(changed['design'])
    (shard/'manifest.json').write_text(json.dumps(changed),encoding='utf-8')
    with pytest.raises(ValueError,match='Parent snapshot changed'):
        snapshot(source,shard,tmp_path/'tampered')
