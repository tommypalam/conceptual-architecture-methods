import asyncio
import json
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'code'))
import utils
from engine.llm_client import CallResult
from engine.validity_sweep import ValiditySink
from run_validity_audit_brief import brief_messages, parse_brief, execute


def answer():
    return json.dumps({'estimates': {p: {'quartile': None, 'confidence': 0} for p in utils.PARAM_NAMES}})


def test_prose_does_not_change_estimates_and_ambiguous_json_rejected():
    expected = json.loads(answer())['estimates']
    for text in [answer(), answer()+'\nInsufficient trait evidence.', '```json\n'+answer()+'\n```\nInsufficient trait evidence.']:
        assert parse_brief(text)[0] == expected
    for text in [answer()+answer(), 'Preface '+answer(), '```json\n'+answer(),
                 '{"estimates":{},"estimates":{}}']:
        with pytest.raises(ValueError):
            parse_brief(text)
    invalid = json.loads(answer())
    invalid['estimates']['LL']['quartile'] = True
    with pytest.raises(ValueError):
        parse_brief(json.dumps(invalid))


def test_checkpoint_resume_preserves_records_and_blinding(tmp_path):
    pack = {'parameter_definitions': {}, 'quartile_definitions': {},
            'items': [{'item_id': str(i), 'reasoning': 'trace'} for i in range(200)]}
    assert set(json.loads(brief_messages(pack, pack['items'][0])[1].content)) == {'definitions','quartiles','reasoning'}
    class Fake:
        n = 0
        async def complete(self, messages, **kwargs):
            self.n += 1
            return CallResult(text=answer()+'\nInsufficient evidence.', model='claude-test',
                model_version='claude-test', provider='anthropic', api_call_id=str(self.n),
                timestamp_utc='test', temperature=1, max_tokens=2000, seed=None,
                latency_s=0, attempts=1, request_messages=[vars(m) for m in messages])
    client = Fake()
    asyncio.run(execute(tmp_path, pack, 'claude-test', client=client, limit=2))
    first = {r['record_key']: r['record_hash'] for r in ValiditySink(tmp_path/'records').read_all()}
    asyncio.run(execute(tmp_path, pack, 'claude-test', client=client))
    asyncio.run(execute(tmp_path, pack, 'claude-test', client=client))
    rows = list(ValiditySink(tmp_path/'records').read_all())
    assert client.n == len(rows) == 200
    assert all(r['record_hash'] == first[r['record_key']] for r in rows if r['record_key'] in first)
    assert all(r['commentary_word_count'] == 2 for r in rows)
