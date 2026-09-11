"""Offline, reproducible evidence extraction; no model calls or new coding rules."""
from hashlib import sha256
import json
import logging
from pathlib import Path

import pandas as pd
import utils
import run_validity_original_expanded as run
from run_validity_claude import save_new


def main():
    source = run.BASE / 'original_expanded_20260911'
    target = run.BASE / 'ms_wording_review_20260911'
    m = json.loads((source / 'manifest.json').read_bytes())
    planned, rows, _ = run.inventory(source, m)
    if len(rows) != 640 or any(r['terminal_failure'] for r in rows):
        raise ValueError('Expected completed valid source')
    selected = [r for r in rows if planned[r['record_key']][0]['parameter'] == 'MS']
    selected.sort(key=lambda r: (planned[r['record_key']][0]['wording'],
                                planned[r['record_key']][0]['value'], r['call_index']))
    if len(selected) != 240: raise ValueError('Unexpected MS allocation')
    print('Source selection:640 records ->240 MS/S2 records; other400 remain in source analyses.')
    evidence = []
    for r in selected:
        c = planned[r['record_key']][0]
        evidence.append({'source_record_key': r['record_key'],
                         'source_file_sha256': sha256((source / 'records' / (r['record_key'] + '.json')).read_bytes()).hexdigest(),
                         'wording': c['wording'], 'value': c['value'], 'call_index': r['call_index'],
                         'decision': r['parsed_decision'], 'reasoning': r['parsed_reasoning'],
                         'profile': c['profile'],
                         'qualitative_reading_subset': c['value'] == .9 or r['call_index'] <= 3})
    logger = logging.getLogger('MS-wording-review'); logging.basicConfig(level=logging.INFO)
    utils.log_dataframe_summary(pd.DataFrame(evidence), 'All240 MS/S2 explanations extracted unchanged', logger)
    reading = [r for r in evidence if r['qualitative_reading_subset']]
    if len(reading) != 104: raise ValueError('Reading subset mismatch')
    print('Qualitative reading selection:240 ->104 (all80 high-MS plus first3 at low/middle in each wording); other136 retained in complete pack.')
    utils.log_dataframe_summary(pd.DataFrame(reading), 'Fixed104-item qualitative reading subset; post-result and unblinded', logger)
    cells = [c for c in m['design']['cells'] if c['parameter'] == 'MS']
    paths = [Path(__file__), source / 'manifest.json', run.ROOT / 'Theory/concepts_as_architecture_thesis_v0_6.md',
             run.ROOT / 'docs/variables.json', run.TEMPLATES]
    save_new(target / 'manifest.json', {'source_design_hash': m['design_hash'],
        'source_file_hashes': {p.relative_to(run.ROOT).as_posix(): sha256(p.read_bytes()).hexdigest() for p in paths},
        'source_records': 640, 'MS_records': 240, 'reading_subset': 104,
        'selection': 'All .9 MS records; call indices1-3 at .1 and.5 for each of four wordings. Selection fixed before reading these explanations, after inspecting aggregate outcomes. No outcome-label selection.',
        'scope': 'Post-result, unblinded qualitative review of reported explanations, not formal coding, causal identification, active-trait recovery, human semantic reapproval or access to internal reasoning.',
        'all_MS_records': evidence, 'templates_and_profiles': cells})
    for wording in run.WORDINGS:
        lines = [f'# MS/S2 reported explanations: {wording}', '',
                 'Full source records retained. [READ] marks the fixed qualitative subset.', '']
        for r in evidence:
            if r['wording'] != wording: continue
            lines += [f"## MS={r['value']} / call {r['call_index']:04d} / {r['decision']}" + (' [READ]' if r['qualitative_reading_subset'] else ''),
                      '', r['reasoning'] or '(missing explanation)', '', f"Source: `{r['source_record_key']}`", '']
        path = target / f'{wording}_EXPLANATIONS.md'
        data = '\n'.join(lines).encode('utf-8')
        if path.exists() and path.read_bytes() != data: raise ValueError('Preserve existing extraction')
        if not path.exists(): path.write_bytes(data)
    print(json.dumps({'output': str(target), 'all_records': len(evidence), 'reading_subset': len(reading), 'api_calls': 0}))


if __name__ == '__main__': main()
