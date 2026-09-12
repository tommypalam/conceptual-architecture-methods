import asyncio
from pathlib import Path
import sys
import pytest
from dataclasses import replace
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'code'))
import run_all_ten_segment3 as run
from test_all_ten_followup import Client as BaseClient, design


class Client(BaseClient):
    def __init__(self,mode='ok'):
        super().__init__(mode);self.requested_seeds=[]

    async def complete(self,*args,**kwargs):
        self.requested_seeds.append(kwargs['seed'])
        r=await super().complete(*args,**kwargs)
        identity=f"mock_seed_{kwargs['seed']}"
        return replace(r,api_call_id=identity,raw_response=dict(r.raw_response,id=identity))


def interrupted_parents(tmp_path,m):
    a=tmp_path/'a';b=tmp_path/'b'
    assert asyncio.run(run.original.execute(a,m,Client('unknown')))=='TECHNICAL_STOP'
    prior=run.segment_inventory(a,m)
    remaining=[j for j in run.old.jobs(m['design']) if j[0] not in prior['intents']]
    for key,c,_,_ in remaining[:3]:
        run.save_new(b/'dispatches'/(key+'.json'),run.old.intent(key,c,m))
    return a,b


def test_unresolved_intents_are_excluded_and_order_seeds_preserved(tmp_path):
    m=design(12);m['design']['prior_accounted_usd']=20.;m['design_hash']=run.digest(m['design'])
    parents=interrupted_parents(tmp_path,m);before=run.combined_inventory(parents,m)
    files={p:p.read_bytes() for root in parents for p in root.rglob('*.json')}
    client=Client();out=tmp_path/'new'
    assert asyncio.run(run.execute(out,m,client,parents))=='DISPATCH_COMPLETE_WITH_MISSING_RESPONSES'
    combined=run.combined_inventory((*parents,out),m)
    assert len(combined['rows'])==9 and len(combined['intents'])==12 and combined['pending']==3
    assert combined['unknown']==before['unknown'] and client.n_calls==6
    assert all(p.read_bytes()==v for p,v in files.items())
    expected=[j for j in run.old.jobs(m['design']) if j[0] not in before['intents']]
    assert client.requested_seeds==[j[3] for j in expected]
    new=run.segment_inventory(out,m)
    assert {r['seed'] for r in new['rows']}=={j[3] for j in expected}
    with pytest.raises(ValueError,match='Existing attempts'):
        asyncio.run(run.execute(out,m,Client(),parents))


def test_unresolved_parent_bounds_block_unaffordable_batch(tmp_path):
    m=design(12);m['design']['prior_accounted_usd']=24.975;m['design_hash']=run.digest(m['design'])
    parents=interrupted_parents(tmp_path,m);client=Client()
    assert asyncio.run(run.execute(tmp_path/'new',m,client,parents))=='BUDGET_STOP'
    assert client.n_calls==0


def test_duplicate_parent_dispatches_are_rejected(tmp_path):
    m=design(12);parents=interrupted_parents(tmp_path,m)
    with pytest.raises(ValueError,match='Overlapping'):
        run.combined_inventory((parents[0],parents[0]),m)


def test_new_unknown_usage_stops_after_one_batch(tmp_path):
    m=design(12);m['design']['prior_accounted_usd']=20.;m['design_hash']=run.digest(m['design'])
    parents=interrupted_parents(tmp_path,m);client=Client('unknown');out=tmp_path/'new'
    assert asyncio.run(run.execute(out,m,client,parents))=='TECHNICAL_STOP'
    assert client.n_calls==3
    combined=run.combined_inventory((*parents,out),m)
    assert combined['unknown']>run.combined_inventory(parents,m)['unknown']
