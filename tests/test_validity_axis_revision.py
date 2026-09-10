import sys
from pathlib import Path
import pytest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'code'))
from prepare_validity_axis_revision import prepare,revise,INSTRUCTION
from engine.validity_variants import PARAMETER_RE


def test_only_new_shared_instruction_changes_and_all_pairs_balanced(tmp_path):
    manifest=prepare(tmp_path);d=manifest['design']
    assert len(d['cells'])==38 and d['planned_calls']==7900
    assert sum(c['n'] for c in d['cells'] if c['stage']=='equivalence')==6400
    assert sum(c['n'] for c in d['cells'] if c['stage']=='sweep')==1500
    paired={}
    for c in d['cells']:
        key=(c['stage'],c['wording'],c['problem'],c['value'])
        paired.setdefault(key,{})[c['arm']]=c
    for arms in paired.values():
        a,b=arms['baseline'],arms['revision']
        assert a['n']==b['n'] and a['profile']==b['profile']
        assert a['messages'][1:]==b['messages'][1:]
        old,new=a['messages'][0]['content'],b['messages'][0]['content']
        assert new==revise(old)
        assert new.replace('# Reading the parameter values\n\n'+INSTRUCTION+'\n\n','')==old
        assert [m[0] for m in PARAMETER_RE.finditer(old)]==[m[0] for m in PARAMETER_RE.finditer(new)]
    assert {(c['problem'],c['value']) for c in d['cells'] if c['stage']=='sweep'}=={
        (p,v) for p in ('S1','S2','S3') for v in (.1,.3,.5,.7,.9)}


def test_revision_rejects_duplicate_application_and_missing_marker():
    with pytest.raises(ValueError): revise('no context marker')
    with pytest.raises(ValueError): revise(revise('# Your normative context'))


def test_mock_execution_distinct_seeds_resume_scoring_and_budget_guard(tmp_path,monkeypatch):
    import asyncio
    from copy import deepcopy
    from engine.llm_client import MockClient
    from engine.validity_sweep import ValiditySink,digest
    from run_validity_sweep import mock_response
    import run_validity_axis_revision as runner
    m=deepcopy(prepare(tmp_path));d=m['design']
    d.update(provider='mock',model='mock-model')
    for c in d['cells']:
        if c['stage']=='equivalence': c['n']=2
    d['planned_calls']=sum(c['n'] for c in d['cells']);m['design_hash']=digest(d)
    planned=runner.jobs(d)
    assert len(planned)==1516
    for a,b in zip(planned[::2],planned[1::2]):
        assert {a[1]['arm'],b[1]['arm']}=={'baseline','revision'}
        assert a[2]==b[2]
        assert all(a[1][k]==b[1][k] for k in ('stage','wording','problem','value'))
    client=MockClient(responder=mock_response);sink=ValiditySink(tmp_path/'records')
    capped=deepcopy(m);capped['design']['collection']['spending_ceiling_usd']=0
    capped['design_hash']=digest(capped['design'])
    with pytest.raises(RuntimeError,match='spending ceiling'): asyncio.run(runner.execute(capped,client,sink))
    assert client.n_calls==0
    asyncio.run(runner.execute(m,client,sink));asyncio.run(runner.execute(m,client,sink))
    rows=list(sink.read_all())
    assert len(rows)==client.n_calls==1516
    assert len({r['seed'] for r in rows})==1516
    monkeypatch.setattr(runner,'archive',lambda path:None)
    result=runner.score(tmp_path,m)
    assert len(result['cells'])==38 and result['sweeps']['n_records']==1500
    assert all(c['n_recorded']==c['n_expected'] for c in result['cells'])
    assert result['phase_gate'].startswith('Unchanged')


def test_equivalence_saturation_and_missing_sensitivity():
    from run_validity_axis_revision import equivalence
    def cells(k,nvalid=800):
        return [{'wording':str(i),'n_recorded':800,'n_expected':800,'n_valid':nvalid,
            'opt0_count':k,'n_invalid':800-nvalid,'rate':k/nvalid} for i in range(4)]
    balanced=equivalence(cells(400,799))
    assert balanced['all_pairs_equivalent'] and balanced['all_unknown_completions_equivalent']
    assert not balanced['saturated_all_formulations']
    assert equivalence(cells(800))['saturated_all_formulations']
    assert not equivalence(cells(400,780))['eligible']


def test_candidate_review_and_terminal_failure_are_not_bypassed(tmp_path):
    import asyncio
    from copy import deepcopy
    from dataclasses import replace
    from engine.llm_client import MockClient
    from engine.validity_sweep import ValiditySink,digest
    from run_validity_sweep import mock_response
    import run_validity_axis_revision as runner
    m=deepcopy(prepare(tmp_path))
    with pytest.raises(ValueError,match='pending'): runner.check_approval(m,tmp_path/'review_pending.json')
    m['design'].update(provider='mock',model='mock-model');m['design_hash']=digest(m['design'])
    class Failing(MockClient):
        async def complete(self,*args,**kwargs):
            result=await super().complete(*args,**kwargs)
            return replace(result,error='TEST FAILURE',text=None) if self.n_calls==1 else result
    client=Failing(responder=mock_response);sink=ValiditySink(tmp_path/'records')
    with pytest.raises(RuntimeError,match='Terminal failure'): asyncio.run(runner.execute(m,client,sink))
    assert client.n_calls==4 and len(list(sink.read_all()))==4
    with pytest.raises(ValueError,match='terminal failure'): asyncio.run(runner.execute(m,client,sink))
    assert client.n_calls==4
