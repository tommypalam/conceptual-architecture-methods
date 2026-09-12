import asyncio
from copy import deepcopy
from dataclasses import replace
import json
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'code'))
import run_validity_ms_stanza_crossover as run
from engine.llm_client import MockClient


class Client(MockClient):
    async def complete(self, *args, **kwargs):
        r = await super().complete(*args, **kwargs)
        return replace(r, model_version=run.base.MODEL, provider='openai', raw_response={
            'id': r.api_call_id, 'model': run.base.MODEL,
            'choices': [{'message': {'content': r.text}}],
            'usage': {'prompt_tokens': 1000, 'completion_tokens': 100}})


def test_complete_mock_exact_swaps_and_allocation(tmp_path):
    m = run.prepare(tmp_path); run.base.check(m)
    source = json.loads(run.SOURCE.read_bytes())['design']['cells']
    for c in m['design']['cells']:
        bg = next(x for x in source if (x['parameter'], x['value'], x['wording']) == ('MS', c['value'], c['background']))
        ms = next(x for x in source if (x['parameter'], x['value'], x['wording']) == ('MS', c['value'], c['ms_stanza']))
        assert c['profile'] == bg['profile'] == ms['profile'] and len(c['profile']) == 10
        assert c['messages'][1:] == bg['messages'][1:] == ms['messages'][1:]
        before = list(run.PARAMETER_RE.finditer(bg['messages'][0]['content']))
        donor = list(run.PARAMETER_RE.finditer(ms['messages'][0]['content']))
        after = list(run.PARAMETER_RE.finditer(c['messages'][0]['content']))
        assert len(after) == 10
        for i in range(10): assert after[i].group(0) == (donor if i == 8 else before)[i].group(0)
        if c['background'] == c['ms_stanza']: assert c['messages'] == bg['messages']
    jobs = list(run.jobs(m['design']))
    assert len(jobs) == len({j[0] for j in jobs}) == len({j[3] for j in jobs}) == 160
    for i in range(0, 160, 8): assert len({j[1]['id'] for j in jobs[i:i+8]}) == 8
    client = Client(responder=lambda messages, seed: 'DECISION: FORMAL_REPORT\nREASONING: Synthetic test.')
    asyncio.run(run.execute(tmp_path, m, client)); result = run.score(tmp_path, m)
    assert client.n_calls == result['n_valid'] == 160
    assert result['status'] == 'COMPLETE_CROSSOVER'
    assert all(p['holm_p'] == 1 and not p['difference_detected'] for p in result['primary_four_comparisons'])
    assert m['design']['full_dispatch_reserve_usd'] < run.CAP
    with pytest.raises(ValueError, match='Existing attempts'): asyncio.run(run.execute(tmp_path, m, client))
    assert client.n_calls == 160


def test_stanza_effect_and_missing_do_not_masquerade_as_background(tmp_path):
    m = run.prepare(tmp_path); rows = []
    for c in m['design']['cells']:
        for i in range(20):
            positive = c['ms_stanza'] == 'canonical' and c['value'] == .9
            rows.append({'cell_id': c['id'], 'terminal_failure': False, 'parse_status': 'ok',
                         'parsed_decision': 'FORMAL_REPORT' if positive else 'LOCAL_CORRECTION',
                         'response_payload': {'usage': {'prompt_tokens': 100, 'completion_tokens': 10}}})
    result = run.assess(rows, m)
    for p in result['primary_four_comparisons']:
        assert p['difference_detected'] == (p['varied_component'] == 'ms_stanza')
        assert p['effect_p2_minus_canonical']['difference'] == (-1 if p['varied_component'] == 'ms_stanza' else 0)
    assert result['secondary_high_value_interaction']['difference'] == 0
    missing = run.assess(rows[:-1], m)
    assert missing['status'] == 'INCOMPLETE_OR_INVALID'
    assert all(p['holm_p'] is None for p in missing['primary_four_comparisons'])
    empty = run.assess([], m)
    assert all(p['effect_p2_minus_canonical']['conservative_95_interval_unknown_envelope'] == [-1, 1] for p in empty['primary_four_comparisons'])


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
