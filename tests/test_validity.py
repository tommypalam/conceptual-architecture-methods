"""Meaningful regression checks for inference and experiment integrity; offline."""
import asyncio
import copy
import sys
from pathlib import Path

import numpy as np
import pytest
from scipy.special import expit

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'code'))
from engine.validity_analysis import logistic, analyze, VALUES
from engine.validity_sweep import build_design, freeze, execute, jobs, parse_output, ValiditySink
from engine.llm_client import MockClient
from engine.record_sink import MemorySink
from run_validity_sweep import mock_response


def cells(counts, n=100):
    return [{'value': v, 'n_valid': n, 'opt0_count': k} for v,k in zip(VALUES, counts)]


def test_logistic_recovers_known_curve_and_inverts_labels():
    data = cells([round(10000*expit(-2+4*x)) for x in VALUES], 10000)
    fit = logistic(data)
    inverse = logistic([{**c, 'opt0_count': c['n_valid']-c['opt0_count']} for c in data])
    assert fit['status'] == 'ok'
    assert fit['slope'] == pytest.approx(4, abs=.002)
    assert fit['ci95'][0] < 4 < fit['ci95'][1]
    assert inverse['slope'] == pytest.approx(-fit['slope'])
    assert inverse['p_value'] == pytest.approx(fit['p_value'])


def test_pinning_separation_and_null():
    assert logistic(cells([100]*5))['status'] == 'pinned'
    assert logistic(cells([0,0,0,100,100]))['status'] == 'separation'
    assert logistic(cells([0,0,50,100,100]))['status'] == 'separation'
    fit = logistic(cells([50]*5))
    assert fit['slope'] == pytest.approx(0, abs=1e-8)
    assert fit['p_value'] == pytest.approx(1)


def test_requested_bare_schema_is_valid_without_lenient_false_positives():
    assert parse_output('ADOPT', ['ADOPT','WAIT'], 'user_prefix_bare') == ('ADOPT','ok')
    assert parse_output('"WAIT".', ['ADOPT','WAIT'], 'user_prefix_bare') == ('WAIT','ok')
    assert parse_output('I might ADOPT or WAIT', ['ADOPT','WAIT'], 'user_prefix_bare')[1] != 'ok'
    assert parse_output('I think ADOPT', ['ADOPT','WAIT'], 'user_prefix_bare')[1] != 'ok'
    assert parse_output('ADOPT', ['ADOPT','WAIT'], 'full_harness')[1] != 'ok'


def design():
    return build_design(params=['RE'], problems=['S1','S3'], n=3, seed=42,
                        provider='mock', model='mock-model')


def test_delivery_content_and_schedule():
    d = design()
    schedule = jobs(d)
    assert len(schedule) == 60
    assert schedule == jobs(d)
    for a,b in zip(schedule[::2], schedule[1::2]):
        assert a[1]['arm'] != b[1]['arm']
        assert a[1]['profile'] == b[1]['profile']
        assert a[2] == b[2]
    for c in d['cells']:
        assert len(c['messages']) == (2 if c['arm']=='full_harness' else 1)
        prompt = '\n'.join(m['content'] for m in c['messages'])
        assert '[RE_VALUE]' not in prompt
        assert f"{c['value']:.2f}" in prompt
        assert ('Reply with only:' in prompt) == (c['arm']=='user_prefix_bare')


def test_freeze_detects_changes(tmp_path):
    path = tmp_path/'manifest.json'
    d = design()
    first = freeze(path,d)
    assert freeze(path,d) == first
    changed = copy.deepcopy(d)
    changed['n'] += 1
    with pytest.raises(ValueError, match='differs'):
        freeze(path,changed)


def test_resume_and_missing_accounting(tmp_path):
    d = design()
    manifest = freeze(tmp_path/'manifest.json',d)
    sink = MemorySink()
    client = MockClient(responder=mock_response)
    asyncio.run(execute(manifest,client=client,sink=sink,limit=7))
    report = analyze(list(sink.read_all()),params=d['params'],problems=d['problems'],arms=d['arms'],n=d['n'])
    assert report['n_records'] == 7
    assert sum(c['n_missing'] for r in report['sweeps'] for c in r['cells']) == 53
    assert not any(r['criterion_met'] for r in report['sweeps'])
    original = copy.deepcopy(sink.records)
    asyncio.run(execute(manifest,client=client,sink=sink))
    assert client.n_calls == 60
    assert all(sink.records[k] == v for k,v in original.items())
    asyncio.run(execute(manifest,client=client,sink=sink))
    assert client.n_calls == 60
    assert all(r['parse_status']=='ok' for r in sink.read_all())


def test_fail_stop_and_resume_refusal(tmp_path):
    class FailingClient(MockClient):
        async def complete(self,*args,**kwargs):
            r = await super().complete(*args,**kwargs)
            r.error = 'test credential error'
            return r
    manifest = freeze(tmp_path/'manifest.json',design())
    sink = MemorySink()
    client = FailingClient(responder=mock_response)
    with pytest.raises(RuntimeError,match='stopped'):
        asyncio.run(execute(manifest,client=client,sink=sink,concurrency=3))
    assert client.n_calls == 3
    assert len(sink.failures) == 3
    with pytest.raises(ValueError,match='terminal failures'):
        asyncio.run(execute(manifest,client=client,sink=sink))


def test_wrong_direction_and_invalid_data_cannot_pass():
    records=[]
    for v,k in zip(VALUES,[10,30,50,70,90]):
        for i in range(100):
            records.append({'arm':'full_harness','swept_parameter':'RE','problem_id':'S3',
                            'sweep_value':v,'call_index':i+1,'labels':['ADOPT','WAIT'],
                            'parsed_decision':'ADOPT' if i<k else 'WAIT','parse_status':'ok'})
    row=analyze(records,params=['RE'],problems=['S3'],arms=['full_harness'],n=100)['sweeps'][0]
    assert row['fit']['p_value'] < .05
    assert row['direction_matches'] is False
    assert not row['criterion_met']
    for r in records:
        r['problem_id']='S1'
        if r['call_index']<=3:
            r['parse_status']='failed_api'
    row=analyze(records,params=['RE'],problems=['S1'],arms=['full_harness'],n=100)['sweeps'][0]
    assert row['direction_matches'] is True
    assert not row['parse_quality_98pct']
    assert not row['criterion_met']
    with pytest.raises(ValueError,match='Duplicate'):
        analyze(records+[records[0]],params=['RE'],problems=['S1'],arms=['full_harness'],n=100)


def test_modified_or_corrupt_records_refuse_resume(tmp_path):
    manifest = freeze(tmp_path/'manifest.json',design())
    sink = MemorySink()
    client = MockClient(responder=mock_response)
    asyncio.run(execute(manifest,client=client,sink=sink,limit=1))
    next(iter(sink.records.values()))['parsed_decision'] = 'corrupted'
    with pytest.raises(ValueError,match='integrity'):
        asyncio.run(execute(manifest,client=client,sink=sink))
    (tmp_path/'bad.json').write_text('{bad json',encoding='utf-8')
    with pytest.raises(ValueError):
        list(ValiditySink(tmp_path).read_all())


def test_boundary_contrast_interval_is_not_zero_width():
    records=[]
    for arm in ['full_harness','user_prefix_bare']:
        for value in VALUES:
            for i in range(50):
                records.append({'arm':arm,'swept_parameter':'RE','problem_id':'S1',
                                'sweep_value':value,'call_index':i+1,'labels':['A','B'],
                                'parsed_decision':'A','parse_status':'ok'})
    report=analyze(records,params=['RE'],problems=['S1'],arms=['full_harness','user_prefix_bare'],n=50)
    contrast=report['delivery_contrasts'][0]
    assert contrast['estimate']==0
    assert contrast['ci95_conservative'][0]<0<contrast['ci95_conservative'][1]
