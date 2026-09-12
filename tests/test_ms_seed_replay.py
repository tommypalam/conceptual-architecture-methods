import asyncio
from copy import deepcopy
from dataclasses import replace
import json
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'code'))
import run_validity_ms_seed_replay as run
from engine.llm_client import MockClient


class Client(MockClient):
    async def complete(self, *args, **kwargs):
        r = await super().complete(*args, **kwargs)
        return replace(r, model_version=run.base.MODEL, provider='openai', raw_response={
            'id': r.api_call_id, 'model': run.base.MODEL,
            'choices': [{'message': {'content': r.text}}],
            'usage': {'prompt_tokens': 1000, 'completion_tokens': 100}})


def test_exact_seed_replay_and_paired_identity(tmp_path):
    m=run.prepare(tmp_path);run.base.check(m)
    allocation=list(run.jobs(m['design']))
    assert len(allocation)==len({j[3] for j in allocation})==40
    answers={}
    for key,c,index,seed in allocation:
        ref=c['replay_sources'][index-1];source=json.loads((run.ROOT/ref['path']).read_bytes())
        assert c['messages']==source['request_messages'] and c['profile']==source['agent_parameters']
        assert seed==source['seed'] and m['design']['temperature']==source['temperature']
        assert m['design']['max_tokens']==source['max_tokens']
        answers[seed]=source['parsed_decision']
    client=Client(responder=lambda messages,seed:'DECISION: '+answers[seed]+'\nREASONING: Synthetic replay.')
    asyncio.run(run.execute(tmp_path,m,client));r=run.score(tmp_path,m)
    assert r['status']=='COMPLETE_SEED_REPLAY' and r['n_valid']==40
    assert all(c['matches']==20 for c in r['cells'])
    assert all(p['holm_p']==1 and p['paired_change']['difference']==0 for p in r['primary_paired_comparisons'])
    assert m['design']['full_dispatch_reserve_usd']<.30
    with pytest.raises(ValueError,match='Existing attempts'):asyncio.run(run.execute(tmp_path,m,client))
    assert client.n_calls==40


def test_all_local_replay_detects_old_cohort_change_only(tmp_path):
    m=run.prepare(tmp_path);rows=[]
    for _,c,index,seed in run.jobs(m['design']):
        rows.append({'cell_id':c['id'],'call_index':index,'terminal_failure':False,'parse_status':'ok',
            'parsed_decision':'LOCAL_CORRECTION','response_payload':{'usage':{'prompt_tokens':100,'completion_tokens':10}}})
    r=run.assess(rows,m);a,b=r['primary_paired_comparisons']
    assert a['losses']==14 and a['gains']==0 and a['paired_change_detected']
    assert a['paired_change']['difference']==-.7
    assert b['losses']==b['gains']==0 and not b['paired_change_detected']
    assert r['secondary_current_cohort_comparison']['descriptive_fisher_p']==1
    assert all(p['holm_p'] is None for p in run.assess(rows[:-1],m)['primary_paired_comparisons'])


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
