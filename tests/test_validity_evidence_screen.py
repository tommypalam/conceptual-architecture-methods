import asyncio
from copy import deepcopy
from dataclasses import replace
import json
from pathlib import Path
import sys
from types import SimpleNamespace

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'code'))
import run_validity_evidence_screen as screen
from engine.llm_client import MockClient, Message
from engine.validity_sweep import ValiditySink, digest
from run_validity_claude import save_new


class Client(MockClient):
    async def complete(self, *args, **kwargs):
        result = await super().complete(*args, **kwargs)
        return replace(result, model_version=screen.MODEL, provider='openai',
                       raw_response={'usage': {'prompt_tokens': 1500, 'completion_tokens': 90}})


def test_exact_sources_balanced_schedule_guard_and_no_call_resume(tmp_path):
    original = (screen.SOURCE / 'manifest.json').read_bytes()
    m = screen.prepare(tmp_path); d = m['design']; jobs = list(screen.jobs(d))
    screen.check(m)
    assert len(jobs) == 450 and len({j[0] for j in jobs}) == 450
    assert len({j[3] for j in jobs}) == 450
    for start in range(0, 450, 15):
        assert len({(c['arm'], c['wording']) for _, c, _, _ in jobs[start:start + 15]}) == 15
    source = json.loads(original)
    old = {c['wording']: c for c in source['design']['cells'] if c['stage'] == 'equivalence' and c['arm'] == 'baseline'}
    for c in d['cells']:
        if c['wording'] == 'no_profile':
            assert c['profile'] is None and [v['role'] for v in c['messages']] == ['user']
        else:
            assert c['profile'] == old[c['wording']]['profile']
            assert c['messages'][0] == old[c['wording']]['messages'][0]
            if c['arm'] == 'original': assert c['messages'] == old[c['wording']]['messages']
        content = c['messages'][-1]['content']
        assert (screen.GROUNDING_NOTE in content) == (c['arm'] == 'grounding')
        assert 'ADOPT = outcome-dominant' not in content
        assert content.endswith(old['canonical']['messages'][1]['content'].split('Respond in exactly this format:')[1])
    client = Client()
    capped = deepcopy(m); capped['design']['spending_ceiling_usd'] = 0; capped['design_hash'] = digest(capped['design'])
    with pytest.raises(RuntimeError, match='spending guard'):
        asyncio.run(screen.execute(tmp_path, capped, client))
    assert client.n_calls == 0
    asyncio.run(screen.execute(tmp_path, m, client))
    asyncio.run(screen.execute(tmp_path, m, client))
    assert client.n_calls == 450
    rows = list(ValiditySink(tmp_path / 'records').read_all())
    assert len(rows) == 450 and len({r['api_call_id'] for r in rows}) == 450
    assert screen.score(tmp_path, m)['n_valid'] == 450
    assert sum(screen.reserve(c, d) for _, c, _, _ in jobs) < 3
    assert (screen.SOURCE / 'manifest.json').read_bytes() == original


@pytest.mark.parametrize('fault', ['api_error', 'missing_usage', 'model_mismatch'])
def test_failure_stops_batch_and_cannot_be_replaced(tmp_path, fault):
    m = screen.prepare(tmp_path)
    class Failed(Client):
        async def complete(self, *args, **kwargs):
            r = await super().complete(*args, **kwargs)
            if fault == 'api_error': return replace(r, error='APIConnectionError: TEST', text=None)
            if fault == 'missing_usage': return replace(r, raw_response={})
            return replace(r, model_version='wrong-model')
    client = Failed()
    with pytest.raises(RuntimeError, match='Terminal failure'):
        asyncio.run(screen.execute(tmp_path, m, client))
    assert client.n_calls == 3
    with pytest.raises(ValueError, match='Preserved terminal failure'):
        asyncio.run(screen.execute(tmp_path, m, client))
    assert client.n_calls == 3
    result = screen.score(tmp_path, m)
    assert result['status'] == 'INCOMPLETE' and result['n_terminal_failures'] == 3


def test_crash_reservation_prevents_duplicate_dispatch(tmp_path):
    m = screen.prepare(tmp_path)
    key, c, _, _ = next(screen.jobs(m['design']))
    save_new(tmp_path / 'dispatches' / (key + '.json'), screen.dispatch_intent(key, c, m))
    client = Client()
    with pytest.raises(ValueError, match='Unresolved dispatch reservation'):
        asyncio.run(screen.execute(tmp_path, m, client))
    assert client.n_calls == 0


def test_gross_failure_rule_and_unknown_envelope(tmp_path):
    m = screen.prepare(tmp_path)
    texts = {c['messages'][0]['content']: c['wording'] for c in m['design']['cells'] if c['wording'] != 'no_profile'}
    def response(messages, seed):
        choice = 'ADOPT' if texts.get(messages[0].content) == 'paraphrase_2' else 'WAIT'
        return f'DECISION: {choice}\nREASONING: Test only.'
    client = Client(responder=response)
    asyncio.run(screen.execute(tmp_path, m, client))
    result = screen.score(tmp_path, m)
    assert result['status'] == 'GROSS_WORDING_FAILURE_DETECTED'
    assert result['wording_gaps']['grounding']['conservative_95_interval_unknown_envelope'][0] > .1
    missing = {'adopt': 0, 'n_expected': 30, 'n_valid': 0, 'rate': None}
    assert screen.contrast([(missing, 1), (missing, -1)]) == {
        'difference': None, 'conservative_95_interval_unknown_envelope': [-1., 1.]}


def test_transport_never_retries_rejected_parameter():
    calls = []
    async def create(**kwargs):
        calls.append(kwargs)
        raise RuntimeError('seed not supported; max_completion_tokens use max_tokens')
    client = screen.SingleAttemptOpenAI(screen.MODEL, max_retries=1)
    client._client = SimpleNamespace(chat=SimpleNamespace(completions=SimpleNamespace(create=create)))
    result = asyncio.run(client.complete([Message('user', 'test')], temperature=1, max_tokens=600, seed=42))
    assert len(calls) == 1 and result.attempts == 1 and result.error
    assert calls[0]['seed'] == 42 and calls[0]['max_completion_tokens'] == 600
