import asyncio
from copy import deepcopy
from dataclasses import replace
import json
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'code'))
import run_validity_evidence_sensitivity as probe
from engine.llm_client import MockClient
from engine.validity_sweep import digest


class Client(MockClient):
    async def complete(self, *args, **kwargs):
        r = await super().complete(*args, **kwargs)
        return replace(r, model_version=probe.base.MODEL, provider='openai',
                       raw_response={'usage': {'prompt_tokens': 1600, 'completion_tokens': 100}})


def test_frozen_executor_accepts_exact_endpoint_design_and_preserves_sources(tmp_path):
    old_path = probe.PREVIOUS / 'manifest.json'; original = old_path.read_bytes()
    m = probe.prepare(tmp_path); d = m['design']; probe.base.check(m)
    jobs = list(probe.base.jobs(d))
    assert len(jobs) == 540 and len({j[0] for j in jobs}) == 540 and len({j[3] for j in jobs}) == 540
    for start in range(0, 540, 18):
        assert len({(c['arm'], c['wording']) for _, c, _, _ in jobs[start:start + 18]}) == 18
    old = {(c['arm'], c['wording']): c for c in json.loads(original)['design']['cells']}
    source = json.loads((probe.SWEEP / 'manifest.json').read_text(encoding='utf-8'))['design']['cells']
    for c in d['cells']:
        assert c['messages'][-1] == old[c['arm'], 'canonical']['messages'][-1]
        assert c['profile'][c['parameter']] == c['value']
        if c['parameter'] == 'PD':
            prior = old['original', c['template_wording']]
            assert c['messages'][0]['content'].replace(f" 6. Procedural Dependence: {c['value']:.2f}", ' 6. Procedural Dependence: 0.80', 1) == prior['messages'][0]['content']
            assert {k:v for k,v in c['profile'].items() if k != 'PD'} == {k:v for k,v in prior['profile'].items() if k != 'PD'}
        else:
            historical = next(s for s in source if s['parameter'] == 'MoR' and s['value'] == c['value'] and s['problem'] == 'S3' and s['arm'] == 'full_harness')
            assert c['messages'][0] == historical['messages'][0] and c['profile'] == historical['profile']
    assert d['prior_reserved_usd'] + d['spending_ceiling_usd'] < 9
    assert d['full_dispatch_reserve_usd'] < 4
    def response(messages, seed):
        decision = 'ADOPT' if ' 4. Mode of Response: 0.90' in messages[0].content else 'WAIT'
        return f'DECISION: {decision}\nREASONING: Test only.'
    client = Client(responder=response)
    zero = deepcopy(m); zero['design']['spending_ceiling_usd'] = 0; zero['design_hash'] = digest(zero['design'])
    with pytest.raises(RuntimeError, match='spending guard'):
        asyncio.run(probe.base.execute(tmp_path, zero, client))
    assert client.n_calls == 0
    asyncio.run(probe.base.execute(tmp_path, m, client))
    asyncio.run(probe.base.execute(tmp_path, m, client))
    assert client.n_calls == 540
    result = probe.score(tmp_path, m)
    assert result['n_valid'] == 540 and result['status'] == 'POSITIVE_RESPONSE_DETECTED_NOT_VALIDATED'
    assert result['endpoint_effects']['grounding/MoR/canonical']['conservative_95_interval_unknown_envelope'][0] > 0
    assert result['endpoint_effects']['grounding/PD/paraphrase_2']['difference'] == 0
    assert old_path.read_bytes() == original


def test_partial_failure_is_preserved_and_not_interpreted_as_no_effect(tmp_path):
    m = probe.prepare(tmp_path)
    class Failed(Client):
        async def complete(self, *args, **kwargs):
            r = await super().complete(*args, **kwargs)
            return replace(r, error='APIConnectionError: TEST', text=None)
    client = Failed()
    with pytest.raises(RuntimeError, match='Terminal failure'):
        asyncio.run(probe.base.execute(tmp_path, m, client))
    with pytest.raises(ValueError, match='Preserved terminal failure'):
        asyncio.run(probe.base.execute(tmp_path, m, client))
    assert client.n_calls == 3
    result = probe.score(tmp_path, m)
    assert result['status'] == 'INCOMPLETE' and result['n_terminal_failures'] == 3
    assert result['endpoint_effects']['grounding/MoR/canonical']['difference'] is None
