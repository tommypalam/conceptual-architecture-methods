import asyncio
from copy import deepcopy
from dataclasses import asdict
from hashlib import sha256
import json
from pathlib import Path
import sys

import httpx
import numpy as np
from openai import AsyncOpenAI
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'code'))
import run_validity_tool_delivery as probe
from research_support.profile_delivery import (
    Specification, FixedSpecificationProvider, JsonSpecificationProvider,
    tool_result, decision_messages)


def test_provider_substitution_and_no_mutation(tmp_path):
    text = 'Ten fixed traits: \u2014 unchanged.'
    s = Specification(text, sha256(text.encode()).hexdigest())
    path = tmp_path / 'spec.json'; path.write_bytes(json.dumps(asdict(s)).encode())
    sources = [FixedSpecificationProvider(s), JsonSpecificationProvider(path, sha256(path.read_bytes()).hexdigest())]
    path.write_bytes(b'changed after snapshot')
    for provider in sources:
        assert provider.read() == s
        assert tool_result(provider, 'read_agent_specification', '{}') == text
        assert tool_result(provider, 'read_agent_specification', '{}') == text
        for name, arguments in [('other', '{}'), ('read_agent_specification', '{"PD":0.9}')]:
            with pytest.raises(ValueError): tool_result(provider, name, arguments)
    with pytest.raises(ValueError): Specification(text, '0' * 64)


class Server:
    def __init__(self, failure=False, bad_tool=False):
        self.requests = []; self.failure = failure; self.bad_tool = bad_tool

    def __call__(self, request):
        body = json.loads(request.content); self.requests.append(body)
        if self.failure:
            return httpx.Response(429, json={'error': {'message': 'Synthetic rate limit'}})
        if body.get('tools'):
            message = {'role': 'assistant', 'content': None, 'tool_calls': [{
                'id': 'call_' + str(body['seed']), 'type': 'function',
                'function': {'name': 'read_agent_specification', 'arguments': '{"PD":0.9}' if self.bad_tool else '{}'}}]}
            finish = 'tool_calls'
        else:
            message = {'role': 'assistant', 'content': 'DECISION: WAIT\nREASONING: Synthetic fixture.'}
            finish = 'stop'
        return httpx.Response(200, json={'id': 'chatcmpl-test-' + str(len(self.requests)),
            'model': probe.base.MODEL, 'object': 'chat.completion', 'created': 1,
            'choices': [{'index': 0, 'message': message, 'finish_reason': finish}],
            'usage': {'prompt_tokens': 100, 'completion_tokens': 10, 'total_tokens': 110}})


def run_mock(root, manifest, server):
    async def run():
        async with httpx.AsyncClient(transport=httpx.MockTransport(server), headers={'Authorization': 'Bearer fake-test-only'}) as client:
            await probe.execute(root, manifest, client)
    return asyncio.run(run())


def test_allocation_wire_equivalence_full_flow_and_no_retry(tmp_path):
    m = probe.prepare(tmp_path)
    assert len(m['design']['cells']) == 32
    assert m['design']['full_dispatch_reserve_usd'] < probe.CAP
    old = json.loads(probe.SOURCE.read_bytes())['design']['cells']
    for c in m['design']['cells']:
        original = next(o for o in old if (o['arm'], o['parameter'], o['value'], o['problem']) ==
                        ('full_harness', c['parameter'], c['value'], 'S3'))
        assert c['profile'] == original['profile'] and len(c['profile']) == 10
        assert c['messages'][1:] == original['messages'][1:]
        if c['wording'] == 'canonical': assert c['messages'] == original['messages']
        assert probe.provider(c).read().text == c['messages'][0]['content']
    # The direct transport sends the SAME canonical JSON fields as the existing
    # SDK method, including model, temperature, max_completion_tokens and seed.
    sdk_server = Server(); request = probe.payload(m['design']['cells'][0]['messages'], 1234)
    async def sdk():
        async with AsyncOpenAI(api_key='fake-test-only', max_retries=0,
                               http_client=httpx.AsyncClient(transport=httpx.MockTransport(sdk_server))) as client:
            await client.chat.completions.create(**request)
    asyncio.run(sdk())
    assert sdk_server.requests == [request]
    server = Server(); run_mock(tmp_path, m, server)
    assert len(server.requests) == 480
    assert len({r['seed'] for r in server.requests}) == 480
    records = list(probe.ValiditySink(tmp_path / 'records').read_all())
    assert len(records) == 480
    for r in records:
        assert json.loads(r['wire_body']) == r['request']
        assert 'fake-test-only' not in json.dumps(r)
        messages = r['request']['messages']
        if messages[-1]['role'] == 'tool':
            assert messages[-1]['tool_call_id'] == messages[-2]['tool_calls'][0]['id']
            assert messages[-1]['content'] in {c['messages'][0]['content'] for c in m['design']['cells']}
    result = probe.score(tmp_path, m)
    assert result['status'] == 'NO_SCALE_UP_SUPPORT'  # flat agreement cannot pass
    assert not result['sensitivity_safeguard']
    with pytest.raises(ValueError, match='Existing allocation'): run_mock(tmp_path, m, server)
    assert len(server.requests) == 480


def test_failure_preserved_and_budget_blocks_before_calls(tmp_path):
    m = probe.prepare(tmp_path); server = Server(failure=True)
    blocked = deepcopy(m); blocked['design']['spending_ceiling_usd'] = 0
    blocked['design_hash'] = probe.digest(blocked['design'])
    with pytest.raises(ValueError, match='spending guard'): run_mock(tmp_path, blocked, server)
    assert not server.requests
    with pytest.raises(RuntimeError, match='Failure preserved'): run_mock(tmp_path, m, server)
    assert len(server.requests) == 3
    assert len(list(probe.ValiditySink(tmp_path / 'records').read_all())) == 3
    with pytest.raises(ValueError, match='Existing allocation'): run_mock(tmp_path, m, server)
    assert len(server.requests) == 3


def test_bad_tool_no_profile_change_or_second_call(tmp_path):
    m = probe.prepare(tmp_path); server = Server(bad_tool=True)
    with pytest.raises(RuntimeError, match='Failure preserved'): run_mock(tmp_path, m, server)
    assert all(r['messages'][-1]['role'] != 'tool' for r in server.requests)
    assert any(r['error'] for r in probe.ValiditySink(tmp_path / 'decisions').read_all())


def test_unbiased_wording_stat_shape_and_known_extremes():
    counts = np.zeros((2, 2, 2, 4), dtype=int)
    counts[0, ..., 0] = 10
    scores = probe.wording_stat(counts, 10)
    assert scores.shape == (2,) and scores.tolist() == [.5, 0.]
    assert probe.wording_stat(np.stack([counts] * 5), 10).shape == (5, 2)
    # Equal observed interior counts have a negative unbiased estimate; clipping
    # would reintroduce sample-size-dependent bias and alter the primary.
    assert np.all(probe.wording_stat(np.full_like(counts, 5), 10) < 0)
