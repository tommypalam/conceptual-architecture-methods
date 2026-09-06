"""Offline checks of variant isolation, inference, blinding, and resumable execution."""
import asyncio
import copy
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'code'))
import utils
from engine.phase0b import SweepProfile, split_blocks
from engine.prompt_assembly import load_template
from engine.validity_variants import variant_prompt, verbal_level, validate_paraphrase, load_reviewed_paraphrases
from engine.validity_equivalence import tost
from engine.validity_coherence import prepare_audit, parse_coding, coding_messages, quartile, score_audit
from engine.validity_followup import comparison_design, execute_comparison, summarize_cells, load_source
from engine.validity_sweep import build_design, freeze, digest, ValiditySink, execute
from engine.llm_client import MockClient, CallResult
from run_validity_sweep import mock_response
from run_validity_claude import execute as execute_claude


def source(tmp_path,n=2,complete=False):
    root=tmp_path/'source'
    manifest=freeze(root/'manifest.json',build_design(params=list(utils.PARAM_NAMES),problems=['S1','S2','S3'],
                   n=n,seed=20260604,provider='mock',model='mock-model'))
    if complete:
        asyncio.run(execute(manifest,client=MockClient(responder=mock_response),sink=ValiditySink(root/'records')))
    return root


def test_variants_preserve_context_task_and_original_hybrid():
    canonical,provenance=SweepProfile('RE',.8).build(load_template(),seed=0)
    assert variant_prompt('RE',.8)[0]==canonical
    for variant in ('numeric_only','verbal_only'):
        prompt,meta=variant_prompt('RE',.8,variant)
        before,after=split_blocks(canonical),split_blocks(prompt)
        assert all(before[k]==after[k] for k in ('preamble','context','task'))
        assert meta['parameter_values']==provenance['parameter_values']
    assert '(0 =' not in variant_prompt('RE',.8,'numeric_only')[0]
    assert ': 0.80' not in variant_prompt('RE',.8,'verbal_only')[0]


def test_six_verbal_bands_and_four_audit_quartiles():
    assert len({verbal_level((i+.5)/6) for i in range(6)})==6
    assert verbal_level(1)=='very high'
    assert [quartile(x) for x in (0,.25,.5,.75,1)]==[1,2,3,4,4]
    with pytest.raises(ValueError): verbal_level(float('nan'))


def test_paraphrase_structure_and_human_review_are_required(tmp_path):
    template=load_template()
    assert not validate_paraphrase(template)['lexical_target_met']
    with pytest.raises(ValueError): validate_paraphrase(template.replace('[LL_VALUE]','0.8'))
    path=tmp_path/'bundle.json'
    path.write_text(json.dumps({'variants':[{'template':template,'generator_model':'claude-example'}]*3}))
    with pytest.raises(ValueError,match='human semantic review'): load_reviewed_paraphrases(path)


def test_equivalence_requires_precision_not_just_identical_rates():
    assert not tost(25,50,25,50)['equivalent']
    assert tost(500,1000,500,1000)['equivalent']
    assert not tost(700,1000,500,1000)['equivalent']
    assert tost(0,50,0,50)['equivalent']
    a,b=tost(12,80,28,100),tost(28,100,12,80)
    assert a['p_value']==pytest.approx(b['p_value'],abs=1e-7)
    assert a['difference']==pytest.approx(-b['difference'])


def test_comparison_checkpoint_resume_and_corruption(tmp_path):
    root=source(tmp_path); out=tmp_path/'followup'
    manifest=freeze(out/'manifest.json',comparison_design(root,'rotations',n=1))
    sink=ValiditySink(out/'records'); client=MockClient(responder=mock_response)
    asyncio.run(execute_comparison(manifest,client=client,sink=sink,limit=4))
    first={r['record_key']:r['record_hash'] for r in sink.read_all()}
    assert len(first)==4
    asyncio.run(execute_comparison(manifest,client=client,sink=sink))
    rows=list(sink.read_all())
    assert len(rows)==90 and all(r['record_hash']==first[r['record_key']] for r in rows if r['record_key'] in first)
    assert all(c['n_valid']==1 for c in summarize_cells(manifest,rows)['cells'])
    with pytest.raises(ValueError): summarize_cells(manifest,rows+[rows[0]])
    rows[0]['parsed_decision']='tampered'
    with pytest.raises(ValueError): summarize_cells(manifest,rows)


def test_dependent_live_run_waits_for_source(tmp_path):
    root=source(tmp_path)
    with pytest.raises(ValueError,match='complete source'): load_source(root,require_complete=True)
    d=comparison_design(root,'gradients',n=50)
    assert d['planned_calls']==15000


def test_blind_selection_is_deterministic_stratified_and_separate(tmp_path):
    root=source(tmp_path,complete=True)
    pack,key=prepare_audit(root)
    assert (pack,key)==prepare_audit(root)
    assert len(pack['items'])==200
    assert all(set(item)=={'item_id','reasoning'} for item in pack['items'])
    for param in utils.PARAM_NAMES:
        assert sum(r['swept_parameter']==param for r in key['items'])==20
    messages=coding_messages(pack,pack['items'][0])
    payload=json.loads(messages[-1].content)
    assert set(payload)=={'definitions','quartiles','reasoning'}
    assert 'true_quartiles' not in messages[-1].content
    # Perfect coding should recover both the aggregate and manipulated quartiles.
    codings=[{'item_id':r['item_id'],'parse_status':'ok','estimates':{
        p:{'quartile':q,'confidence':1} for p,q in r['true_quartiles'].items()}} for r in key['items']]
    report=score_audit(key,codings,permutations=19)
    assert report['complete'] and report['literal_spec_thresholds_met']
    assert all(r['active_parameter_items']['balanced_accuracy']==1 for r in report['parameters'])
    assert report['status'].startswith('REVIEW REQUIRED')
    assert not score_audit(key,codings[:-1],permutations=1)['complete']


def test_coder_schema_rejects_invalid_confidence_and_boolean_quartile():
    estimates={p:{'quartile':None,'confidence':0} for p in utils.PARAM_NAMES}
    assert parse_coding(json.dumps({'estimates':estimates}))==estimates
    estimates['LL']['quartile']=True
    with pytest.raises(ValueError): parse_coding(json.dumps({'estimates':estimates}))


def test_claude_failures_preserved_and_no_resume_over_failure(tmp_path):
    class Fake:
        async def complete(self,messages,**kwargs):
            return CallResult(text='bad JSON',model='claude-test',model_version='claude-test',provider='anthropic',
                api_call_id='fake',timestamp_utc='test',temperature=1,max_tokens=12000,seed=None,latency_s=0,attempts=1,
                request_messages=[vars(m) for m in messages])
    root=tmp_path/'claude'
    with pytest.raises(RuntimeError):
        asyncio.run(execute_claude(root,'paraphrases','claude-test',client=Fake()))
    row=next(iter(ValiditySink(root/'records').read_all()))
    assert row['raw_response']=='bad JSON' and row['parse_status']=='failed'
    with pytest.raises(ValueError,match='Preserved failure'):
        asyncio.run(execute_claude(root,'paraphrases','claude-test',client=Fake()))
