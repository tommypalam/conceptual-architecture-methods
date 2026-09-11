"""Trace all 20 existing active MoR audit items; unblinded diagnosis, no recoding."""
from collections import Counter
from hashlib import sha256
import json
import logging
from pathlib import Path

import pandas as pd
import utils
from engine.validity_sweep import digest, verify_record
from run_validity_claude import save_new

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'experiments/phase1_5_encoding_validity'
AUDIT = BASE / 'claude_audit_20260909_brief_r3'
PACK = ROOT / 'output/validity_audit_20260909_restart'
DEST = BASE / 'mor_reasoning_review_20260911'


def main():
    paths = [PACK/'private_answer_key.json', PACK/'blind_pack.json', AUDIT/'manifest.json']
    raw = {p: p.read_bytes() for p in paths}
    key, pack, manifest = [json.loads(raw[p]) for p in paths]
    assert digest(pack) == key['blind_pack_hash'] == manifest['design']['blind_pack_hash']
    assert digest(manifest['design']) == manifest['design_hash']
    selected = [i for i in key['items'] if i['swept_parameter'] == 'MoR']
    assert len(key['items']) == 200 and len(selected) == 20
    public = {i['item_id']: i for i in pack['items']}
    jobs = {i['item_id']: i for i in manifest['design']['jobs']}
    rows = []
    for i in sorted(selected, key=lambda x: x['source_record_key']):
        sp = BASE/'option_c_20260909_restart/records'/(i['source_record_key']+'.json')
        ap = AUDIT/'records'/(i['item_id']+'.json')
        raw[sp] = sp.read_bytes(); raw[ap] = ap.read_bytes()
        source, audit = json.loads(raw[sp]), json.loads(raw[ap])
        verify_record(source); verify_record(audit)
        assert source['record_hash'] == i['source_record_hash']
        assert source['design_hash'] == key['source_design_hash']
        assert audit['design_hash'] == manifest['design_hash'] and audit['parse_status'] == 'ok'
        reasoning = public[i['item_id']]['reasoning']
        assert reasoning == source['parsed_reasoning'] == json.loads(jobs[i['item_id']]['messages'][1]['content'])['reasoning']
        rows.append({'item_id': i['item_id'], 'source_record_key': i['source_record_key'],
                     'problem': i['problem_id'], 'value': source['sweep_value'],
                     'decision': source['parsed_decision'], 'true_quartile': i['true_quartiles']['MoR'],
                     'estimated_quartile': audit['estimates']['MoR']['quartile'],
                     'confidence': audit['estimates']['MoR']['confidence'],
                     'reasoning_sha256': sha256(reasoning.encode('utf-8')).hexdigest()})
    logging.basicConfig(level=logging.INFO)
    utils.log_dataframe_summary(pd.DataFrame(rows), 'Audit selection: 200 -> all 20 active MoR items; no outcome selection', logging.getLogger('review'))
    result = {'scope': 'Unblinded descriptive inspection; original blind labels and scores unchanged.',
              'source_sha256': {p.relative_to(ROOT).as_posix(): sha256(b).hexdigest() for p,b in raw.items()},
              'analysis_source_sha256': sha256(Path(__file__).read_bytes()).hexdigest(),
              'rows': rows, 'estimated_quartile_counts': dict(Counter(str(r['estimated_quartile']) for r in rows)),
              'exact_matches': sum(r['true_quartile'] == r['estimated_quartile'] for r in rows)}
    save_new(DEST/'trace_inventory.json', result)
    lines = ['# MoR audit trace inventory', '', 'All 20 active MoR items, selected before this review. Original labels retained.',
             'Rationales remain in the original raw records and local blind pack; hashes link exact text.', '',
             '| Item | Source record | Decision | True quartile | Claude quartile | Confidence |', '|---|---|---|---:|---:|---:|']
    for r in rows:
        lines.append(f"| {r['item_id']} | {r['source_record_key']} | {r['decision']} | {r['true_quartile']} | {r['estimated_quartile']} | {r['confidence']} |")
    out = ('\n'.join(lines)+'\n').encode('utf-8'); target = DEST/'TRACE_INVENTORY.md'
    if target.exists() and target.read_bytes() != out: raise ValueError('Preserve previous inventory')
    if not target.exists(): target.write_bytes(out)
    assert all(p.read_bytes() == b for p,b in raw.items())
    print(json.dumps({k:result[k] for k in ('estimated_quartile_counts','exact_matches')}))


if __name__ == '__main__': main()
