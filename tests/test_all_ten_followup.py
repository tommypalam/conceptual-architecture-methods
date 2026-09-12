import asyncio
from copy import deepcopy
from dataclasses import replace
from pathlib import Path
import sys
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'code'))
import run_all_ten_followup as run
from engine.llm_client import MockClient


def design(n=6):
    cells=[]
    for i in range(n):
        cells.append({'id':f'b{i}','background':i,'parameter':'PD','problem':'S2','phase':'gradients','variant':'canonical','value':.1,'profile':{'PD':.1},
            'messages':[{'role':'user','content':'Synthetic task'}],'labels':['A','B'],'target_label':'A','n':1})
    d={'source_hashes':{},'cells':cells,'seed':20261021,'planned_calls':n,'max_tokens':600,'prior_accounted_usd':24.97,
        'total_package_cap_usd':25.,'spending_ceiling_usd':.03,'model':run.old.base.MODEL}
    return {'design':d,'design_hash':run.digest(d)}


class Client(MockClient):
    def __init__(self,mode='ok'):
        super().__init__(responder=lambda messages,seed:'DECISION: A\nREASONING: Synthetic.');self.mode=mode
    async def complete(self,*args,**kwargs):
        r=await super().complete(*args,**kwargs)
        payload={'id':r.api_call_id,'model':run.old.base.MODEL,'choices':[{'message':{'content':r.text}}],
            'usage':{'prompt_tokens':100,'completion_tokens':100}}
        if self.mode=='unknown':payload.pop('usage')
        if self.mode=='invalid':
            r=replace(r,text='Unparseable');payload['choices'][0]['message']['content']=r.text
        return replace(r,model_version=run.old.base.MODEL,provider='openai',raw_response=payload)


def test_batch_bounds_and_settlement(tmp_path):
    m=design(12);client=Client()
    # All12 worst-case reservations exceed available .03, but settled usage
    # plus each full next-batch reservation fits. No cap increase is needed.
    assert sum(run.old.base.reserve(c,m['design']) for c in m['design']['cells'])>.03
    assert asyncio.run(run.execute(tmp_path,m,client))=='COLLECTED'
    assert client.n_calls==12
    _,rows,_=run.old.inventory(tmp_path,m);assert len(rows)==12
    with pytest.raises(ValueError,match='Existing attempts'):asyncio.run(run.execute(tmp_path,m,client))


def test_budget_stops_before_any_unaffordable_dispatch(tmp_path):
    m=design();m['design']['prior_accounted_usd']=24.999;m['design_hash']=run.digest(m['design'])
    client=Client();assert asyncio.run(run.execute(tmp_path,m,client))=='BUDGET_STOP'
    assert client.n_calls==0 and not list((tmp_path/'dispatches').rglob('*.json'))


def test_unknown_usage_stops_and_invalid_parse_is_not_retried(tmp_path):
    m=design();client=Client('unknown')
    assert asyncio.run(run.execute(tmp_path/'unknown',m,client))=='TECHNICAL_STOP'
    assert client.n_calls==3
    client=Client('invalid')
    assert asyncio.run(run.execute(tmp_path/'invalid',m,client))=='COLLECTED'
    _,rows,_=run.old.inventory(tmp_path/'invalid',m)
    assert len(rows)==6 and all(r['parse_status']!='ok' for r in rows)
    assert client.n_calls==6


def test_paired_equivalence_does_not_use_degenerate_zero_width():
    equal=run.paired_interval([0]*50)
    assert -.1<equal['ci90_conservative'][0]<0<equal['ci90_conservative'][1]<.1
    assert run.paired_interval([0]*20)['ci90_conservative'][1]>.1
    assert run.paired_interval([1]*50)['ci90_conservative'][0]>.1


def test_allocation_and_source_prompt_integrity():
    d=run.build()
    assert len(d['cells'])==17250
    assert sum(c['phase']=='gradients' for c in d['cells'])==11250
    assert sum(c['phase']=='wording' for c in d['cells'])==6000
    assert len(set(c['parameter'] for c in d['cells']))==10
    assert len({j[3] for j in run.old.jobs(d)})==17250
    for phase,variants in [('gradients',3),('wording',4)]:
        by={}
        for c in d['cells']:
            if c['phase']==phase:by.setdefault((c['background'],c['parameter'],c['problem'],c['value']),[]).append(c)
        for group in by.values():
            assert len(group)==variants
            assert len({run.digest(c['profile']) for c in group})==1
            assert len({run.digest(c['messages'][1:]) for c in group})==1


def test_complete_scoring_keeps_all_tests_and_invalid_cells_visible():
    d=run.build();d['bootstrap_draws']=1000
    m={'design':d,'design_hash':run.digest(d)};rows=[]
    for c in d['cells']:
        label=c['target_label'] if c['value']>=.5 else next(v for v in c['labels'] if v!=c['target_label'])
        rows.append({'cell_id':c['id'],'phase':c['phase'],'call_index':1,'arm':'full_harness',
            'swept_parameter':c['parameter'],'sweep_value':c['value'],'problem_id':c['problem'],
            'parse_status':'ok','parsed_decision':label,'terminal_failure':False})
    report=run.assess(rows,m)
    assert report['all_planned_recorded']
    assert len(report['gradient_analysis']['groups'])==90
    assert len(report['gradient_sensitivity']['representation_retention_diagnostic'])==60
    assert len(report['gradient_sensitivity']['exact_paired_180_comparisons'])==180
    assert len(report['wording_analysis'])==30
    assert all(r['all_pairs_equivalent'] for r in report['wording_analysis'])
    assert not report['original_gate_passed']
    # An invalid wording response is retained, not replaced or counted equivalent.
    target=next(r for r in rows if r['phase']=='wording');target['parse_status']='invalid';target['parsed_decision']=None
    report=run.assess(rows,m)
    assert report['n_records']==17250 and report['n_parse_invalid']==1
    assert sum(r['all_pairs_equivalent'] for r in report['wording_analysis'])==29
