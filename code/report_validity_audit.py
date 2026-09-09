"""Score a completed blind audit and write a provenance-aware human-readable report."""
import argparse
import json
import logging
from pathlib import Path
from statistics import median

import pandas as pd
import utils

from engine.validity_coherence import score_audit
from engine.validity_sweep import ValiditySink, digest, verify_record
from run_validity_continuation import preserve
from run_validity_claude import save_new
from run_validity_restart_followups import archive


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run-root', type=Path, required=True)
    parser.add_argument('--answer-key', type=Path, required=True)
    args = parser.parse_args()
    root = args.run_root.resolve()
    key = json.loads(args.answer_key.read_text(encoding='utf-8'))
    manifest = json.loads((root/'manifest.json').read_text(encoding='utf-8'))
    if digest(manifest['design']) != manifest['design_hash'] or manifest['design']['blind_pack_hash'] != key['blind_pack_hash']:
        raise ValueError('Manifest or answer-key pairing mismatch')
    rows = list(ValiditySink(root/'records').read_all())
    if len(rows) != 200 or any(r['design_hash'] != manifest['design_hash'] or r['parse_status'] != 'ok' for r in rows):
        raise ValueError('Require a complete, valid 200-item audit')
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    frame = pd.DataFrame([{p: row['estimates'][p]['quartile'] for p in utils.PARAM_NAMES} for row in rows])
    utils.log_dataframe_summary(frame, 'Audit quartiles (null means abstention; retained)', logging.getLogger('audit'))
    report = score_audit(key, rows)
    if not report['complete']:
        raise ValueError('Audit is not complete')
    save_new(root/'analysis'/f'audit_{digest(report)[:16]}.json', report)
    words = [r.get('commentary_word_count', 0) for r in rows]
    details = {'n_codings': len(rows), 'n_estimates': len(rows)*10,
               'model': manifest['design']['model'], 'blind_pack_hash': key['blind_pack_hash'],
               'source_design_hash': key['source_design_hash'], 'audit_seed': key['audit_seed'],
               'configuration': 'neutral', 'commentary_word_median': median(words),
               'commentary_word_max': max(words), 'commentary_over_15_words': sum(n > 15 for n in words),
               'n_parameters_above_035': sum(p['literal_spec_above_035'] for p in report['parameters']),
               'n_parameters_at_least_050': sum(p['literal_spec_at_least_050'] for p in report['parameters']),
               'literal_spec_thresholds_met': report['literal_spec_thresholds_met']}
    ledger_path = root/'continuation.json'
    if ledger_path.exists():
        ledger = json.loads(ledger_path.read_text(encoding='utf-8'))
        if ledger['design_hash'] != manifest['design_hash']:
            raise ValueError('Continuation design mismatch')
        for entry in ledger['preserved_failed_attempts']:
            data = Path(entry['source_path']).read_bytes()
            attempt = json.loads(data)
            verify_record(attempt)
            if attempt['record_hash'] != entry['record_hash']:
                raise ValueError('Preserved failed-attempt mismatch')
            preserve(root/'preserved_attempts'/f'{entry["item_id"]}.json', data)
        details['continuation_reused_records'] = len(ledger['reused'])
        details['additional_preserved_failed_attempts'] = len(ledger['preserved_failed_attempts'])
    save_new(root/'analysis'/'execution_summary.json', details)
    pct = lambda x: f'{100*x:.1f}%'
    lines = ['# Completed independent Claude reasoning audit', '',
             f'Model: `{details["model"]}`. Configuration: neutral. Audit sampling seed: {key["audit_seed"]}.',
             '200 blind reasoning items, 2,000 quartile estimates. All 200 responses parsed successfully.',
             'This format revision repeats all 200 selected items; the earlier failed-format attempt is preserved separately and not pooled.',
             'The private answer key was used only for local scoring; provider requests contained definitions and reasoning only.', '',
             f'Additional malformed attempts under the brief prompt: {details.get("additional_preserved_failed_attempts", 0)}. '
             f'Unchanged valid observations reused in this continuation: {details.get("continuation_reused_records", 0)}. '
             'Failed attempts are preserved outside the effective records directory and included in the local backup.', '',
             f'Literal specification thresholds met: **{report["literal_spec_thresholds_met"]}**.',
             f'Parameters above 35% with p<.05 against .25: {details["n_parameters_above_035"]}/10 (required: 6).',
             f'Parameters at or above 50%: {details["n_parameters_at_least_050"]}/10 (required: 4).', '',
             '| Parameter | All-item accuracy (95% Wilson CI) | Majority baseline | Active-only accuracy | Active balanced accuracy | Stratified permutation p |',
             '|---|---|---|---|---|---|']
    for p in report['parameters']:
        all_items, active = p['all_items'], p['active_parameter_items']
        low, high = all_items['ci95']
        lines.append(f'| {p["parameter"]} | {pct(all_items["accuracy"])} ({pct(low)}–{pct(high)}) | '
                     f'{pct(all_items["majority_class_baseline"])} | {pct(active["accuracy"])} | '
                     f'{pct(active["balanced_accuracy"])} | {p["active_stratified_permutation_p"]:.4f} |')
    lines.extend(['', '## Interpretation limits', '',
                  'Nine traits are held at their means in each source sweep. Aggregate accuracy against a uniform 25% chance baseline can therefore be misleading; compare it with the empirical majority baseline and the 20 active-parameter items per trait.',
                  'Active-only estimates have small samples. Permutation tests use 1,999 resamples within problem strata and are unadjusted diagnostics, not multiplicity-corrected confirmation.',
                  f'{report["n_decimal_literal_traces"]} selected reasoning traces contain decimal literals; these were retained as prespecified.',
                  'Literal audit thresholds do not establish the whole Phase 1.5 gate. Paraphrase testing and the remaining combined scientific review are still pending.', '',
                  '## Response brevity', '',
                  f'Explanatory commentary: median {median(words):g} words; maximum {max(words)}; {sum(n>15 for n in words)} responses exceeded the requested 15-word limit.',
                  'All commentary is preserved. Verbosity does not filter estimates or change scoring.', ''])
    target = root/'analysis'/'AUDIT_REPORT.md'
    content = '\n'.join(lines)
    if target.exists() and target.read_text(encoding='utf-8') != content:
        raise ValueError('Existing report differs')
    if not target.exists():
        target.write_text(content, encoding='utf-8')
    archive(root)
    print(json.dumps(details, indent=2))
    print(f'Report and verified local backup completed: {target}')


if __name__ == '__main__':
    main()
