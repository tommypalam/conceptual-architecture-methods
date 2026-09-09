"""Continuation preserves outcomes and avoids duplicate billing across computers."""
import asyncio
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'code'))
from engine.llm_client import MockClient
from engine.validity_sweep import build_design, freeze, execute, ValiditySink, digest
from run_validity_sweep import mock_response
from run_validity_continuation import prepare, prepare_shard, ShardSink


def source_run(tmp_path):
    source = tmp_path/'source'
    d = build_design(params=['RE'], problems=['S1'], n=1, seed=42,
                     provider='mock', model='mock-model')
    manifest = freeze(source/'manifest.json', d)
    sink = ValiditySink(source/'records')
    asyncio.run(execute(manifest, client=MockClient(responder=mock_response), sink=sink, limit=3))
    records = list(sink.read_all())
    failed = records[0]
    failed['error_message'] = 'quota exhausted'
    failed['parse_status'] = 'failed_api'
    failed['record_hash'] = digest({k:v for k,v in failed.items() if k != 'record_hash'})
    (sink.root/(failed['record_key']+'.json')).write_text(json.dumps(failed), encoding='utf-8')
    inventory = {'design_hash': manifest['design_hash'], 'n_records': 3, 'n_api_failures': 1,
                 'index': [{'record_key': r['record_key'], 'record_hash': r['record_hash']} for r in records]}
    (source/'record_checksums.json').write_text(json.dumps(inventory), encoding='utf-8')
    return source, manifest


def test_recovery_retains_bytes_and_fills_only_unfilled_slots(tmp_path):
    source, manifest = source_run(tmp_path)
    before = {str(p): p.read_bytes() for p in source.rglob('*') if p.is_file()}
    target = tmp_path/'continuation'
    prepare(source, target)
    assert len(list(ValiditySink(target/'records').read_all())) == 2
    client = MockClient(responder=mock_response)
    asyncio.run(execute(manifest, client=client, sink=ValiditySink(target/'records'), limit=2))
    prepare(source, target)
    asyncio.run(execute(manifest, client=client, sink=ValiditySink(target/'records')))
    assert client.n_calls == 8
    assert len(list(ValiditySink(target/'records').read_all())) == 10
    assert before == {str(p):p.read_bytes() for p in source.rglob('*') if p.is_file()}


def test_shard_does_not_require_payloads_or_repeat_reserved_slots(tmp_path):
    source, manifest = source_run(tmp_path)
    for p in (source/'records').rglob('*.json'):
        p.unlink()
    target = tmp_path/'shard'
    _, reserved = prepare_shard(source, target)
    sink = ShardSink(target/'records', reserved)
    client = MockClient(responder=mock_response)
    asyncio.run(execute(manifest, client=client, sink=sink, limit=2))
    prepare_shard(source, target)
    asyncio.run(execute(manifest, client=client, sink=sink))
    asyncio.run(execute(manifest, client=client, sink=sink))
    assert client.n_calls == 7
    assert not reserved.intersection(r['record_key'] for r in sink.read_all())
    with pytest.raises(ValueError, match='Missing source records'):
        prepare(source, tmp_path/'bad')


def test_corrupt_source_rejected_before_target_created(tmp_path):
    source, _ = source_run(tmp_path)
    path = next((source/'records').rglob('*.json'))
    path.write_text('{}')
    with pytest.raises(ValueError, match='integrity'):
        prepare(source, tmp_path/'bad')
    assert not (tmp_path/'bad').exists()


def test_inventory_tampering_and_wrapper_changes_rejected(tmp_path):
    source, _ = source_run(tmp_path)
    target = tmp_path/'shard'
    prepare_shard(source, target)
    path = source/'record_checksums.json'
    inventory = json.loads(path.read_text())
    inventory['index'][0]['record_hash'] = 'changed'
    path.write_text(json.dumps(inventory))
    with pytest.raises(ValueError, match='differs'):
        prepare_shard(source, target)
