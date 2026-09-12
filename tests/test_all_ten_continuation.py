import asyncio
from pathlib import Path
import sys
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'code'))
import run_all_ten_continuation as cont
from test_all_ten_followup import Client, design


def partial_parent(root,m,mode='unknown'):
    client=Client(mode)
    assert asyncio.run(cont.original.execute(root,m,client))=='TECHNICAL_STOP'
    return cont.segment_inventory(root,m)


def test_continuation_preserves_seeds_order_and_failed_slots(tmp_path):
    m=design(9);m['design']['prior_accounted_usd']=20.;m['design_hash']=cont.digest(m['design'])
    parent=tmp_path/'parent';child=tmp_path/'child';before=partial_parent(parent,m)
    raw={p:p.read_bytes() for p in parent.rglob('*.json')}
    expected=[j for j in cont.old.jobs(m['design']) if j[0] not in before['intents']]
    client=Client()
    assert asyncio.run(cont.execute(child,m,client,parent))=='COLLECTED'
    after=cont.segment_inventory(child,m)
    assert len(after['rows'])==6 and client.n_calls==6
    assert set(after['intents']).isdisjoint(before['intents'])
    assert {r['seed'] for r in after['rows']}=={j[3] for j in expected}
    assert all(p.read_bytes()==v for p,v in raw.items())
    assert before['unknown']>0
    with pytest.raises(ValueError,match='Existing attempts'):
        asyncio.run(cont.execute(child,m,Client(),parent))


def test_parent_unknown_reservation_prevents_overspend(tmp_path):
    m=design(9);parent=tmp_path/'parent'
    m['design']['prior_accounted_usd']=24.985;m['design_hash']=cont.digest(m['design'])
    partial_parent(parent,m)
    client=Client();child=tmp_path/'child'
    assert asyncio.run(cont.execute(child,m,client,parent))=='BUDGET_STOP'
    assert client.n_calls==0


def test_new_failure_stops_without_retry(tmp_path):
    m=design(9);m['design']['prior_accounted_usd']=20.;m['design_hash']=cont.digest(m['design'])
    parent=tmp_path/'parent';partial_parent(parent,m)
    client=Client('unknown');child=tmp_path/'child'
    assert asyncio.run(cont.execute(child,m,client,parent))=='TECHNICAL_STOP'
    assert client.n_calls==3
    assert cont.segment_inventory(child,m)['unknown']>0


def test_live_parent_exclusion_is_exact_prefix():
    import json
    m=json.loads((cont.PARENT/'manifest.json').read_bytes())
    parent=cont.segment_inventory(cont.PARENT,m)
    schedule=list(cont.old.jobs(m['design']))
    assert len(parent['rows'])==1941 and parent['pending']==0
    assert set(parent['intents'])=={j[0] for j in schedule[:1941]}
    remaining=[j for j in schedule if j[0] not in parent['intents']]
    assert remaining==schedule[1941:] and len(remaining)==15309
    assert abs(parent['unknown']-.019947)<1e-10
