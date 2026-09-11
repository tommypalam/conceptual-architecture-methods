import asyncio
from copy import deepcopy
from dataclasses import replace
import json
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'code'))
import run_validity_original_expanded as run
from engine.llm_client import MockClient


class Client(MockClient):
    async def complete(self, *args, **kwargs):
        r = await super().complete(*args, **kwargs)
        return replace(r, model_version=run.base.MODEL, provider='openai', raw_response={
            'id': r.api_call_id, 'model': run.base.MODEL,
            'choices': [{'message': {'content': r.text}}],
            'usage': {'prompt_tokens': 1000, 'completion_tokens': 100}})


def test_complete_mock_preserves_all_prompts_labels_profiles_and_allocation(tmp_path):
    m = run.prepare(tmp_path); run.base.check(m)
    assert m['design']['full_dispatch_reserve_usd'] < run.CAP
    assert m['design']['prior_ledger']['cumulative_conservative_charge_usd'] + run.CAP < 9
    source = json.loads(run.SOURCE.read_bytes())['design']['cells']
    templates = run.load_reviewed_paraphrases(run.TEMPLATES)
    for c in m['design']['cells']:
        old = next(o for o in source if (o['arm'], o['parameter'], o['problem'], o['value']) ==
                   ('full_harness', c['parameter'], c['problem'], c['value']))
        assert c['profile'] == old['profile'] and len(c['profile']) == 10
        assert c['messages'][1:] == old['messages'][1:] and c['labels'] == old['labels']
        text, _ = run.variant_prompt(c['parameter'], c['value'], 'hybrid', template=templates.get(c['wording']))
        assert c['messages'][0]['content'] == text
        if c['wording'] == 'canonical': assert c['messages'] == old['messages']
    jobs = list(run.jobs(m['design']))
    assert len(jobs) == len({j[0] for j in jobs}) == len({j[3] for j in jobs}) == 640
    for i in range(0, 640, 32): assert len({j[1]['id'] for j in jobs[i:i+32]}) == 32
    def answer(messages, seed):
        first = 'FORMAL_REPORT' if 'FORMAL_REPORT' in messages[-1].content else 'ADOPT'
        return f'DECISION: {first}\nREASONING: Synthetic test.'
    client = Client(responder=answer)
    asyncio.run(run.execute(tmp_path, m, client))
    result = run.score(tmp_path, m)
    assert client.n_calls == 640 and result['n_valid'] == 640
    assert result['status'] == 'COMPLETE_SELECTED_CASE_REPLICATION'
    assert result['n_positive_directions_established'] == 0  # constant output gives no encoding effect
    assert len(result['secondary_wording_pairs']) == 48
    assert {x['first_option'] for x in result['primary_eight_endpoint_effects']} == {'FORMAL_REPORT', 'ADOPT'}
    with pytest.raises(ValueError, match='Existing attempts'): asyncio.run(run.execute(tmp_path, m, client))
    assert client.n_calls == 640


def test_known_effects_holm_family_stress_and_missing(tmp_path):
    m = run.prepare(tmp_path); rows = []
    for c in m['design']['cells']:
        for i in range(20):
            if c['parameter'] in ('MoR', 'MS'):
                positive = c['value'] == .9 or (c['value'] == .5 and i < 10)
            else:
                positive = c['wording'] == 'paraphrase_3'
            rows.append({'cell_id': c['id'], 'terminal_failure': False, 'parse_status': 'ok',
                         'parsed_decision': c['labels'][0 if positive else 1],
                         'response_payload': {'usage': {'prompt_tokens': 100, 'completion_tokens': 10}}})
    result = run.assess(rows, m)
    assert result['n_positive_directions_established'] == 8
    assert all(x['observed_nondecreasing'] for x in result['primary_eight_endpoint_effects'])
    assert result['n_gross_wording_differences'] == 6
    assert run.holm([.04, .01, .02]) == [.04, .03, .04]
    missing = run.assess(rows[:-1], m)
    assert missing['status'] == 'INCOMPLETE_OR_INVALID'
    assert all(x['holm_p'] is None for x in missing['primary_eight_endpoint_effects'])
    empty = run.assess([], m)
    assert all(x['simultaneous95_interval_unknown_envelope'] == [-1., 1.] for x in empty['secondary_wording_pairs'])


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
