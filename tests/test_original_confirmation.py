import asyncio
from copy import deepcopy
from dataclasses import replace
import json
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'code'))
import run_validity_original_confirmation as probe
from engine.llm_client import MockClient
from engine.validity_sweep import digest


class Client(MockClient):
    async def complete(self, *args, **kwargs):
        result = await super().complete(*args, **kwargs)
        return replace(result, model_version=probe.base.MODEL, provider='openai',
                       raw_response={'usage': {'prompt_tokens': 1500, 'completion_tokens': 100}})


def test_exact_originals_balanced_unique_allocations_and_guarded_mock(tmp_path):
    m = probe.prepare(tmp_path); probe.base.check(m)
    canonical = json.loads((probe.SWEEP / 'manifest.json').read_bytes())['design']['cells']
    gradients = json.loads((probe.GRADIENTS / 'manifest.json').read_bytes())['design']['cells']
    for c in m['design']['cells']:
        source = next(x for x in (canonical if c['arm'] == 'full_harness' else gradients)
                      if (x.get('arm', x.get('variant')), x['parameter'], x['problem'], x['value']) ==
                      (c['arm'], 'MoR', 'S3', c['value']))
        assert c['messages'] == source['messages'] and c['profile'] == source['profile']
    jobs = list(probe.base.jobs(m['design']))
    assert len(jobs) == 900 and len({j[3] for j in jobs}) == 900
    for arm in probe.ARMS:
        for value in probe.VALUES:
            group = [j for j in jobs if (j[1]['arm'], j[1]['value']) == (arm, value)]
            assert sorted((c['allocation'] - 1) * 30 + k for _, c, k, _ in group) == list(range(1, 61))
    assert m['design']['full_dispatch_reserve_usd'] < probe.CAP
    assert m['design']['prior_conservative_charge_usd'] + probe.CAP < 9
    assert m['design']['prior_unknown_usage_reserved_usd'] > 0
    client = Client(responder=lambda messages, seed: 'DECISION: WAIT\nREASONING: Test.')
    blocked = deepcopy(m); blocked['design']['spending_ceiling_usd'] = 0
    blocked['design_hash'] = digest(blocked['design'])
    with pytest.raises(RuntimeError, match='spending guard'):
        asyncio.run(probe.base.execute(tmp_path, blocked, client))
    assert client.n_calls == 0 and probe.score(tmp_path, m)['status'] == 'INCOMPLETE'
    asyncio.run(probe.base.execute(tmp_path, m, client))
    asyncio.run(probe.base.execute(tmp_path, m, client))
    assert client.n_calls == 900
    r = probe.score(tmp_path, m)
    assert r['status'] == 'RETENTION_NOT_ASSESSABLE_CONTROL_CRITERION_NOT_MET'
    assert all(x['assessment'] == 'not_assessable' for x in r['retention'])


def evidence(counts):
    planned = {}; rows = []
    for arm in probe.ARMS:
        for value, k in zip(probe.VALUES, counts[arm]):
            for i in range(60):
                key = f'{arm}/{value}/{i}'
                planned[key] = ({'value': value, 'labels': ['ADOPT', 'WAIT'], 'allocation': i // 30 + 1}, i, i)
                rows.append({'record_key': key, 'arm': arm, 'problem_id': 'S3', 'call_index': i % 30 + 1,
                             'parse_status': 'ok', 'parsed_decision': 'ADOPT' if i < k else 'WAIT',
                             'terminal_failure': False,
                             'response_payload': {'usage': {'prompt_tokens': 100, 'completion_tokens': 10}}})
    return rows, planned


def test_original_rules_and_fresh_control_no_historical_rescue():
    counts = {'full_harness': [2, 10, 22, 40, 54], 'numeric_only': [16, 20, 22, 24, 28],
              'verbal_only': [2, 14, 28, 40, 54]}
    rows, planned = evidence(counts); r = probe.assess(rows, planned)
    by = {x['variant']: x for x in r['retention']}
    assert r['status'] == 'RETENTION_CRITERION_NOT_MET'
    assert by['numeric_only']['absolute_logit_slope_ratio'] < .5
    assert not by['numeric_only']['criterion_met'] and by['verbal_only']['criterion_met']
    counts['numeric_only'] = counts['verbal_only']
    rows, planned = evidence(counts)
    assert probe.assess(rows, planned)['status'] == 'BOTH_RETENTION_CHECKS_MET_NOT_VALIDATED'
    rows[0]['terminal_failure'] = True
    assert probe.assess(rows, planned)['status'] == 'INVALID_SCREEN'
    counts['full_harness'] = [2, 16, 10, 40, 54]
    rows, planned = evidence(counts); r = probe.assess(rows, planned)
    assert r['status'] == 'RETENTION_NOT_ASSESSABLE_CONTROL_CRITERION_NOT_MET'
    assert all(x['assessment'] == 'not_assessable' for x in r['retention'])


def test_transport_failure_preserved_and_not_retried(tmp_path):
    m = probe.prepare(tmp_path)
    class Failed(Client):
        async def complete(self, *args, **kwargs):
            return replace(await super().complete(*args, **kwargs), error='Test timeout')
    client = Failed(responder=lambda messages, seed: 'DECISION: WAIT\nREASONING: Test.')
    with pytest.raises(RuntimeError, match='Terminal failure'):
        asyncio.run(probe.base.execute(tmp_path, m, client))
    with pytest.raises(ValueError, match='Preserved terminal failure'):
        asyncio.run(probe.base.execute(tmp_path, m, client))
    _, rows, _ = probe.base.inventory(tmp_path, m)
    assert client.n_calls == len(rows) == 3 and all(r['terminal_failure'] for r in rows)
