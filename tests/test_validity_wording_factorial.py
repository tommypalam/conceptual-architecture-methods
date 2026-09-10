import sys
from pathlib import Path
import numpy as np
import pytest
from scipy.stats import binomtest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'code'))
from validity_wording_factorial import exact_table,interval_contrast,CONTRASTS,analyze_counts,mix_endpoints
from engine.prompt_assembly import load_template


def test_rate_bounds_match_independent_scipy_exact_method():
    table=exact_table(100)
    for k in (0,1,40,50,99,100):
        ci=binomtest(k,100).proportion_ci(confidence_level=1-.05/4,method='exact')
        assert table[k]==pytest.approx([ci.low,ci.high])


def test_contrast_signs_and_missing_outcome_sensitivity():
    p=np.array([.6,.4,.6,.4])
    assert p@CONTRASTS['PD_wording_P2_minus_P3']==pytest.approx(.2)
    assert p@CONTRASTS['other_nine_P2_minus_P3']==pytest.approx(0)
    assert np.array([.6,.4,.4,.6])@CONTRASTS['interaction_difference_in_differences']==pytest.approx(.4)
    a=analyze_counts([60,40,60,40],[100]*4,[0]*4)
    b=analyze_counts([60,40,60,40],[100]*4,[2]*4)
    for name in CONTRASTS:
        old=a['contrasts'][name]['simultaneous_ci95_unknowns_expanded']
        new=b['contrasts'][name]['simultaneous_ci95_unknowns_expanded']
        assert new[0]<=old[0] and new[1]>=old[1]
    with pytest.raises(ValueError): analyze_counts([100]*4,[100]*4,[1]*4)


def test_mixing_is_identity_when_sources_match_and_only_replaces_pd():
    original=load_template()
    assert mix_endpoints(original,original)==original
    changed=original.replace('results matter, methods are secondary','RESULTS WORDING')
    assert mix_endpoints(changed,original)==changed
    unrelated=changed.replace('even soft pressure registers','A DIFFERENT CS PHRASE registers')
    assert mix_endpoints(unrelated,original)==changed


@pytest.fixture
def prepared(tmp_path):
    import json
    from run_validity_wording_factorial import prepare
    base=Path(__file__).resolve().parents[1]/'experiments/phase1_5_encoding_validity'
    (tmp_path/'power_plan.json').write_text('{}',encoding='utf-8')
    manifest=prepare(base/'option_c_20260909_restart',
        base/'claude_paraphrases_20260909_theory_r5/paraphrases_approved.json',tmp_path,n=2)
    old=json.loads((base/'paraphrases_20260909_final/manifest.json').read_text(encoding='utf-8'))
    for name,variant in [('A','paraphrase_2'),('D','paraphrase_3')]:
        original=next(c for c in old['design']['cells'] if c['parameter']=='PD' and c['problem']=='S3' and c['variant']==variant)
        current=next(c for c in manifest['design']['cells'] if c['variant']==name)
        assert current['messages']==original['messages']
        assert current['profile']==original['profile']
    return manifest,tmp_path


def test_review_requires_exact_messages_and_explicit_reviewer(prepared):
    import json
    from run_validity_wording_factorial import require_approval
    manifest,root=prepared
    pending=root/'review_pending.json'
    with pytest.raises(ValueError,match='pending'): require_approval(manifest,pending)
    review=json.loads(pending.read_text(encoding='utf-8'))
    review.update(approved=True,reviewer='TEST REVIEWER ONLY')
    approved=root/'test_review.json'
    approved.write_text(json.dumps(review),encoding='utf-8')
    require_approval(manifest,approved)
    review['condition_messages_hashes']['B']='wrong'
    approved.write_text(json.dumps(review),encoding='utf-8')
    with pytest.raises(ValueError,match='does not match'): require_approval(manifest,approved)


def mock_manifest(manifest):
    from copy import deepcopy
    from engine.validity_sweep import digest
    mock=deepcopy(manifest)
    mock['design'].update(provider='mock',model='mock-model')
    mock['design_hash']=digest(mock['design'])
    return mock


def test_balanced_blocks_unique_seeds_resume_and_score(prepared,monkeypatch):
    import asyncio
    from engine.llm_client import MockClient
    from engine.validity_sweep import ValiditySink
    from run_validity_sweep import mock_response
    import run_validity_wording_factorial as runner
    manifest,root=prepared; manifest=mock_manifest(manifest)
    client=MockClient(responder=mock_response,concurrency=4); sink=ValiditySink(root/'records')
    asyncio.run(runner.execute(manifest,client,sink))
    rows=list(sink.read_all())
    assert len(rows)==client.n_calls==8
    assert len({r['seed'] for r in rows})==8
    assert all(r['parse_status']=='ok' for r in rows)
    for k in (1,2): assert {r['variant'] for r in rows if r['randomized_block']==k}==set('ABCD')
    before={r['record_key']:r['record_hash'] for r in rows}
    asyncio.run(runner.execute(manifest,client,sink))
    assert client.n_calls==8
    assert before=={r['record_key']:r['record_hash'] for r in sink.read_all()}
    monkeypatch.setattr(runner,'archive',lambda path: None)
    result=runner.score(root,manifest)
    assert result['status']=='EXPLORATORY_DIAGNOSTIC_COMPLETE'
    assert all(c['n_valid']==2 for c in result['cells'])


def test_terminal_failure_preserved_and_resume_refused(prepared):
    import asyncio
    from dataclasses import replace
    from engine.llm_client import MockClient
    from engine.validity_sweep import ValiditySink
    from run_validity_sweep import mock_response
    from run_validity_wording_factorial import execute
    class FailingClient(MockClient):
        async def complete(self,*args,**kwargs):
            result=await super().complete(*args,**kwargs)
            return replace(result,error='TEST FAILURE',text=None) if self.n_calls==1 else result
    manifest,root=prepared; manifest=mock_manifest(manifest)
    sink=ValiditySink(root/'records'); client=FailingClient(responder=mock_response)
    with pytest.raises(RuntimeError,match='stopped after block'): asyncio.run(execute(manifest,client,sink))
    rows=list(sink.read_all())
    assert len(rows)==client.n_calls==4
    assert sum(bool(r['error_message']) for r in rows)==1
    with pytest.raises(ValueError,match='terminal failure'): asyncio.run(execute(manifest,client,sink))
    assert client.n_calls==4
