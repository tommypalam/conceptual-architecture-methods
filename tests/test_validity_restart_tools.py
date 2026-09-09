"""Offline checks for fresh-run gates, backups, and literal endpoint assembly."""
import json
import sys
import zipfile
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'code'))
import run_validity_restart_followups as pipeline
from engine.validity_sweep import build_design, digest, freeze, jobs, ValiditySink
from engine.validity_variants import PARAMETER_RE
from engine.prompt_assembly import load_template
from generate_validity_endpoint_paraphrases import assemble
import utils


def source(tmp_path, *, complete=True):
    root = tmp_path/'run'
    d = build_design(params=['RE'], problems=['S1'], n=1, seed=42,
                     provider='openai', model='test-model')
    manifest = freeze(root/'manifest.json', d)
    scheduled = jobs(d) if complete else jobs(d)[:2]
    for key, _, _ in scheduled:
        row = {'record_key': key, 'design_hash': manifest['design_hash'],
               'model_version': d['model'], 'parse_status': 'ok', 'error_message': None,
               'response_payload': {'usage': {'prompt_tokens': 100, 'completion_tokens': 10}}}
        row['record_hash'] = digest(row)
        ValiditySink(root/'records').write(key, row)
    return root


def test_dependent_work_requires_complete_valid_source(tmp_path):
    root = source(tmp_path, complete=False)
    assert pipeline.validate_source(root) is False
    path = next((root/'records').rglob('*.json'))
    row = json.loads(path.read_text())
    row['error_message'] = 'quota failure'
    row['record_hash'] = digest({k: v for k,v in row.items() if k != 'record_hash'})
    path.write_text(json.dumps(row))
    with pytest.raises(ValueError, match='Source failure'):
        pipeline.validate_source(root)


def test_archive_preserves_payloads_and_reports_usage(tmp_path, monkeypatch):
    root = source(tmp_path)
    monkeypatch.setattr(pipeline, 'ROOT', tmp_path)
    assert pipeline.validate_source(root)
    pipeline.archive(root)
    pipeline.archive(root)
    inventory = json.loads((root/'record_checksums.json').read_text())
    assert inventory['n_records'] == 10
    assert json.loads((root/'token_usage.json').read_text())['input_tokens'] == 1000
    backup = json.loads((root/'local_backup.json').read_text())
    with zipfile.ZipFile(backup['path']) as z:
        for p in (root/'records').rglob('*.json'):
            assert z.read(p.relative_to(root).as_posix()) == p.read_bytes()


def test_endpoint_assembly_preserves_everything_else():
    canonical = load_template()
    endpoints = {code: {'0': m[4], '1': m[5]}
                 for code,m in zip(utils.PARAM_NAMES, PARAMETER_RE.finditer(canonical))}
    assert assemble(endpoints, canonical) == canonical
    endpoints['LL']['0'] = 'A NEW ENDPOINT'
    actual = assemble(endpoints, canonical)
    first = next(PARAMETER_RE.finditer(canonical))
    assert actual == canonical[:first.start(4)]+'A NEW ENDPOINT'+canonical[first.end(4):]
    del endpoints['AW']
    with pytest.raises(ValueError, match='ten parameter'):
        assemble(endpoints, canonical)
