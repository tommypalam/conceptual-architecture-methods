"""Assemble existing Phase 1.5 evidence without inferring an automatic gate pass."""
import argparse
import json
from pathlib import Path

import utils
from engine.validity_sweep import digest
from run_validity_claude import save_new


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--sweep-report', type=Path, required=True)
    parser.add_argument('--audit-report', type=Path, required=True)
    parser.add_argument('--gradient-report', type=Path)
    parser.add_argument('--paraphrase-report', type=Path)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    sweep, audit = read(args.sweep_report), read(args.audit_report)
    gradient = read(args.gradient_report) if args.gradient_report else None
    paraphrase = read(args.paraphrase_report) if args.paraphrase_report else None
    rows = []
    for param in utils.PARAM_NAMES:
        full = [r for r in sweep['sweeps'] if r['parameter'] == param and r['arm'] == 'full_harness']
        bare = [r for r in sweep['sweeps'] if r['parameter'] == param and r['arm'] == 'user_prefix_bare']
        coder = next(r for r in audit['parameters'] if r['parameter'] == param)
        eligible = [r for r in full if r['predicted_direction'] is not None]
        row = {'parameter': param, 'full_harness_qualifying_problems': [r['problem'] for r in full if r['criterion_met']],
               'bare_qualifying_problems': [r['problem'] for r in bare if r['criterion_met']],
               'full_harness_sweep_status': 'not_assessable_no_prespecified_direction' if not eligible else
                   ('criterion_met' if any(r['criterion_met'] for r in full) else 'criterion_not_met'),
               'audit_accuracy': coder['all_items']['accuracy'],
               'audit_accuracy_ci95': coder['all_items']['ci95'],
               'audit_majority_baseline': coder['all_items']['majority_class_baseline'],
               'audit_active_balanced_accuracy': coder['active_parameter_items']['balanced_accuracy'],
               'audit_active_permutation_p': coder['active_stratified_permutation_p'],
               'gradients': [r for r in gradient['gradients'] if r['parameter'] == param] if gradient else None,
               'paraphrases': [r for r in paraphrase['paraphrase_equivalence']['cells'] if r['parameter'] == param] if paraphrase else None}
        rows.append(row)
    report = {'phase': '1.5', 'configuration': 'neutral', 'seed': 20260604,
              'status': 'SCIENTIFIC_REVIEW_REQUIRED' if gradient and paraphrase else 'INCOMPLETE_BATTERY',
              'audit_literal_thresholds_met': audit['literal_spec_thresholds_met'],
              'source_reports': {name: str(getattr(args, name).resolve()) if getattr(args, name) else None
                                 for name in ('sweep_report','audit_report','gradient_report','paraphrase_report')},
              'source_report_hashes': {'sweep': digest(sweep), 'audit': digest(audit),
                                       'gradient': digest(gradient) if gradient else None,
                                       'paraphrase': digest(paraphrase) if paraphrase else None},
              'parameters': rows}
    version = digest(report)[:16]
    save_new(args.out/f'evidence_{version}.json', report)
    lines = ['# Phase 1.5 evidence matrix', '',
             f'Status: **{report["status"]}**. Neutral configuration; root/audit sampling seed 20260604.',
             'This is an evidence inventory, not a phase-pass declaration or authorisation to revise the architecture.', '',
             '| Parameter | Full-harness qualifying problems | Bare qualifying problems | Audit accuracy (95% CI) | Majority baseline | Active balanced accuracy | Active permutation p |',
             '|---|---|---|---|---|---|---|']
    for row in rows:
        full = ', '.join(row['full_harness_qualifying_problems']) or ('No prespecified direction' if row['full_harness_sweep_status'].startswith('not_assessable') else 'None')
        low, high = row['audit_accuracy_ci95']
        lines.append(f'| {row["parameter"]} | {full} | {", ".join(row["bare_qualifying_problems"]) or "None"} | '
                     f'{row["audit_accuracy"]:.1%} ({low:.1%}–{high:.1%}) | {row["audit_majority_baseline"]:.1%} | '
                     f'{row["audit_active_balanced_accuracy"]:.1%} | {row["audit_active_permutation_p"]:.4f} |')
    lines.extend(['', '## Outstanding decisions and interpretation', '',
                  '- Gradient comparison: '+('report supplied' if gradient else 'pending; one .8 rotation cannot estimate a within-parameter slope')+'.',
                  '- Reviewed-paraphrase equivalence: '+('report supplied' if paraphrase else 'pending; no empirical equivalence claim')+'.',
                  '- Audit numerical thresholds and empirical-class-baseline diagnostics must both be reported.',
                  '- Do not convert absent directional hypotheses into failures or post-hoc predictions.',
                  '- Do not equate failure to establish equivalence with evidence of a meaningful difference.',
                  '- Any new theoretical departure requires a demonstrated binding limitation and prior user consultation.',
                  '- Original failed attempts, collection dates, raw records and backup limitations remain part of provenance.', ''])
    target = args.out/f'evidence_{version}.md'
    if not target.exists():
        target.write_text('\n'.join(lines), encoding='utf-8')
    print(target)


if __name__ == '__main__':
    main()
