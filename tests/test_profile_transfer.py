import asyncio
from copy import deepcopy
from dataclasses import replace
import json
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'code'))
import run_validity_profile_transfer as run
from engine.llm_client import MockClient


class Client(MockClient):
    async def complete(self, *args, **kwargs):
        r = await super().complete(*args, **kwargs)
        return replace(r, model_version=run.base.MODEL, provider='openai', raw_response={
            'id': r.api_call_id, 'model': run.base.MODEL,
            'choices': [{'message': {'content': r.text}}],
            'usage': {'prompt_tokens': 1000, 'completion_tokens': 100}})


def test_frozen_backgrounds_numeric_only_and_full_mock(tmp_path):
    m=run.prepare(tmp_path);run.base.check(m)
    assert len(m['design']['backgrounds'])==20
    source=json.loads(run.SOURCE.read_bytes())['design']['cells']
    for c in m['design']['cells']:
        bg=m['design']['backgrounds'][c['background']]
        assert all(c['profile'][k]==(c['value'] if k==c['parameter'] else bg[k]) for k in bg)
        old=next(o for o in source if (o['arm'],o['parameter'],o['problem'],o['value'])==('full_harness',c['parameter'],c['problem'],.1))
        assert c['messages'][1:]==old['messages'][1:]
        before=old['messages'][0]['content'];after=c['messages'][0]['content']
        def mask(text):
            for match in reversed(list(run.PARAMETER_RE.finditer(text))):text=text[:match.start(3)]+'VALUE'+text[match.end(3):]
            return text
        assert mask(before)==mask(after)
        assert [float(x.group(3)) for x in run.PARAMETER_RE.finditer(after)]==list(c['rendered_profile'].values())
    allocation=list(run.jobs(m['design']))
    assert len(allocation)==len({j[0] for j in allocation})==len({j[3] for j in allocation})==360
    assert all(j[2]==1 for j in allocation[:180]) and all(j[2]==2 for j in allocation[180:])
    for i in range(0,360,3):
        assert len({(j[1]['background'],j[1]['parameter']) for j in allocation[i:i+3]})==1
        assert {j[1]['value'] for j in allocation[i:i+3]}=={.1,.5,.9}
    def response(messages,seed):
        label='FORMAL_REPORT' if 'FORMAL_REPORT' in messages[-1].content else 'ADOPT'
        return 'DECISION: '+label+'\nREASONING: Synthetic constant.'
    client=Client(responder=response);asyncio.run(run.execute(tmp_path,m,client));r=run.score(tmp_path,m)
    assert r['n_valid']==360 and r['status']=='COMPLETE_TRANSFER_SCREEN'
    assert all(not p['local_transfer_supported'] and p['mean_high_minus_low']==0 for p in r['primary'])
    assert m['design']['full_dispatch_reserve_usd']<2.5
    with pytest.raises(ValueError,match='Existing attempts'):asyncio.run(run.execute(tmp_path,m,client))


def test_direction_orientation_shared_clusters_and_missing(tmp_path):
    m=run.prepare(tmp_path);rows=[]
    for _,c,block,_ in run.jobs(m['design']):
        target=c['value']==.9 or (c['value']==.5 and block==1)
        other=next(l for l in c['labels'] if l!=c['target_label'])
        rows.append({'cell_id':c['id'],'call_index':block,'terminal_failure':False,'parse_status':'ok',
            'parsed_decision':c['target_label'] if target else other,
            'response_payload':{'usage':{'prompt_tokens':100,'completion_tokens':10}}})
    r=run.assess(rows,m)
    assert all(p['mean_high_minus_low']==1 and p['local_transfer_supported'] for p in r['primary'])
    assert all(p['three_target_rates']==[0,.5,1] and p['bonferroni983333']==[1,1] for p in r['primary'])
    assert r['primary'][2]['target_label']=='WAIT'
    assert all(p['local_transfer_supported'] is None for p in run.assess(rows[:-1],m)['primary'])
    # Opposite block effects must not advance even with positive average point estimate.
    for row in rows:
        if row['call_index']==2:row['parsed_decision']='WAIT' if row['parsed_decision']=='ADOPT' else ('ADOPT' if row['parsed_decision']=='WAIT' else ('LOCAL_CORRECTION' if row['parsed_decision']=='FORMAL_REPORT' else 'FORMAL_REPORT'))
    r=run.assess(rows,m)
    assert all(not p['local_transfer_supported'] for p in r['primary'])


def test_budget_and_terminal_failures_preserved(tmp_path):
    m = run.prepare(tmp_path)
    class Failed(Client):
        async def complete(self, *args, **kwargs):
            return replace(await super().complete(*args, **kwargs), error='Synthetic timeout')
    client = Failed(responder=lambda messages, seed: 'DECISION: ADOPT\nREASONING: Test.')
    blocked = deepcopy(m); blocked['design']['spending_ceiling_usd'] = 0
    blocked['design_hash'] = run.digest(blocked['design'])
    with pytest.raises(RuntimeError, match='spending guard'): asyncio.run(run.execute(tmp_path, blocked, client))
    assert client.n_calls == 0
    with pytest.raises(RuntimeError, match='Terminal failure'): asyncio.run(run.execute(tmp_path, m, client))
    assert client.n_calls == 3
    assert all(r['terminal_failure'] for r in run.ValiditySink(tmp_path / 'records').read_all())
    with pytest.raises(ValueError, match='Existing attempts'): asyncio.run(run.execute(tmp_path, m, client))
    assert client.n_calls == 3
