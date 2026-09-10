import asyncio
from copy import deepcopy
import json
from pathlib import Path
import sys
import pytest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'code'))
import run_validity_pd_endpoints as runner
from engine.llm_client import MockClient
from engine.validity_sweep import ValiditySink,digest
from engine.validity_variants import PARAMETER_RE

BASE=Path(__file__).resolve().parents[1]/'experiments/phase1_5_encoding_validity'


@pytest.fixture
def prepared(tmp_path):
    parent=BASE/'wording_factorial_20260910'
    bundle=BASE/'claude_paraphrases_20260909_theory_r5/paraphrases_approved.json'
    return runner.prepare(parent,bundle,tmp_path,n=2),tmp_path


def test_only_selected_pd_endpoint_changes(prepared):
    manifest,_=prepared
    cells=manifest['design']['cells']
    systems=[c['messages'][0]['content'] for c in cells]
    matches=[list(PARAMETER_RE.finditer(s))[5] for s in systems]
    assert [m[4] for m in matches]==[matches[0][4],matches[3][4],matches[0][4],matches[3][4]]
    assert [m[5] for m in matches]==[matches[0][5],matches[0][5],matches[3][5],matches[3][5]]
    def masked(s,m):
        for g in (5,4): s=s[:m.start(g)]+'ENDPOINT'+s[m.end(g):]
        return s
    assert len({masked(s,m) for s,m in zip(systems,matches)})==1
    assert all(c['profile']==cells[0]['profile'] and c['messages'][1]==cells[0]['messages'][1] for c in cells)
    parent=json.loads((BASE/'wording_factorial_20260910/manifest.json').read_text(encoding='utf-8'))
    assert cells[0]['messages']==parent['design']['cells'][0]['messages']
    assert cells[3]['messages']==parent['design']['cells'][1]['messages']


def test_real_review_is_pending_and_immutable(prepared):
    manifest,root=prepared
    with pytest.raises(ValueError,match='pending'):
        runner.require_approval(manifest,root/'review_pending.json')
    changed=deepcopy(manifest); changed['design']['seed']+=1
    from engine.validity_sweep import freeze
    with pytest.raises(ValueError,match='NEW run directory'): freeze(root/'manifest.json',changed['design'])


def test_mock_execution_resume_and_low_high_analysis(prepared,monkeypatch):
    manifest,root=prepared
    manifest=deepcopy(manifest); manifest['design'].update(provider='mock',model='mock-model')
    manifest['design_hash']=digest(manifest['design'])
    # Low-P2 cells A/C choose ADOPT; low-P3 cells B/D choose WAIT.
    p2low=list(PARAMETER_RE.finditer(manifest['design']['cells'][0]['messages'][0]['content']))[5][4]
    def responder(messages,seed):
        low=list(PARAMETER_RE.finditer(messages[0].content))[5][4]
        return 'DECISION: '+('ADOPT' if low==p2low else 'WAIT')+'\nREASONING: Mock only.'
    client=MockClient(responder=responder); sink=ValiditySink(root/'records')
    asyncio.run(runner.execute(manifest,client,sink))
    asyncio.run(runner.execute(manifest,client,sink))
    assert client.n_calls==8
    assert len({r['seed'] for r in sink.read_all()})==8
    monkeypatch.setattr(runner,'archive',lambda path:None)
    result=runner.score(root,manifest)
    assert result['seed']==20260912
    assert result['status']=='EXPLORATORY_DIAGNOSTIC_COMPLETE'
    contrasts=result['contrast_analysis']['contrasts']
    assert contrasts['low_endpoint_P2_minus_P3']['estimate_valid_only']==1
    assert contrasts['high_endpoint_P2_minus_P3']['estimate_valid_only']==0
    assert contrasts['endpoint_interaction_difference_in_differences']['estimate_valid_only']==0
