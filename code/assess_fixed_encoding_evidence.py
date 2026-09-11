"""Join completed validity summaries without rerunning models or changing tests."""
from copy import deepcopy
from hashlib import sha256
import json
import logging
from pathlib import Path

import pandas as pd
import utils
from run_validity_claude import save_new

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'experiments/phase1_5_encoding_validity'
SOURCES = {
    'sweeps': BASE / 'option_c_20260909_restart/analysis/summary_8d2d0ab58fff59f9.json',
    'gradients': BASE / 'gradients_20260909_final/analysis/cells_6f4ee2cee96409c4.json',
    'paraphrases': BASE / 'paraphrases_20260909_final/analysis/cells_621833995ad959cd.json',
    'audit': BASE / 'claude_audit_20260909_brief_r3/analysis/audit_cc085a29d6576c92.json',
}
DESTINATION = BASE / 'fixed_encoding_assessment_20260911'


def index_unique(rows, fields):
    result = {}
    for row in rows:
        key = tuple(row[f] for f in fields)
        if key in result: raise ValueError('Duplicate evidence key: ' + str(key))
        result[key] = row
    return result


def build_matrix(sources):
    sweep, gradient, paraphrase, audit = (sources[k] for k in ('sweeps', 'gradients', 'paraphrases', 'audit'))
    if (sweep['n_records'] != sweep['n_expected'] or sweep['n_records'] != 15000
            or gradient['n_records'] != gradient['n_expected'] or gradient['n_records'] != 15000
            or paraphrase['n_records'] != paraphrase['n_expected'] or paraphrase['n_records'] != 4500
            or not audit['complete'] or audit['n_codings'] != 200):
        raise ValueError('Only completed final source summaries are eligible')
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger('encoding-assessment')
    utils.log_dataframe_summary(pd.DataFrame(sweep['sweeps']), 'All source sweeps before scope selection: 60', logger)
    canonical = [r for r in sweep['sweeps'] if r['arm'] == 'full_harness']
    utils.log_dataframe_summary(pd.DataFrame(canonical), 'Canonical scope: 60 -> 30; bare-delivery rows remain in source', logger)
    expected = {(p, q) for p in utils.PARAM_NAMES for q in ('S1', 'S2', 'S3')}
    s_index = index_unique(canonical, ('parameter', 'problem'))
    g_index = index_unique(gradient['gradients'], ('parameter', 'problem', 'variant'))
    p_index = index_unique(paraphrase['paraphrase_equivalence']['cells'], ('parameter', 'problem'))
    a_index = index_unique(audit['parameters'], ('parameter',))
    if (set(s_index) != expected or set(p_index) != expected
            or set(g_index) != {(p, q, v) for p, q in expected for v in ('numeric_only', 'verbal_only')}
            or set(a_index) != {(p,) for p in utils.PARAM_NAMES}):
        raise ValueError('Missing or unexpected evidence coverage; no silent join omissions')
    result = []
    for parameter in utils.PARAM_NAMES:
        for problem in ('S1', 'S2', 'S3'):
            s = s_index[parameter, problem]; p = p_index[parameter, problem]; a = a_index[parameter,]
            if [c['value'] for c in s['cells']] != [.1, .3, .5, .7, .9]:
                raise ValueError('Unexpected canonical value grid')
            direction = s['predicted_direction']
            row = {'parameter': parameter, 'problem': problem,
                   'canonical_cells': deepcopy(s['cells']), 'canonical_fit': deepcopy(s['fit']),
                   'canonical_criterion': 'not_prespecified' if direction is None else 'met' if s['criterion_met'] else 'not_met',
                   'prespecified_direction': direction, 'canonical_monotonic': s['monotonic'],
                   'canonical_cohens_h_extremes': s['cohens_h_extremes'],
                   'canonical_rate_range': max(c['rate'] for c in s['cells']) - min(c['rate'] for c in s['cells']),
                   'paraphrase_rotation_value': .8,
                   'paraphrase_all_pairs_equivalent': p['all_pairs_equivalent'], 'paraphrase_complete': p['complete'],
                   'active_audit_n_per_parameter_not_per_problem': a['active_parameter_items']['n'],
                   'active_audit_accuracy': a['active_parameter_items']['accuracy'],
                   'active_audit_majority_baseline': a['active_parameter_items']['majority_class_baseline'],
                   'active_audit_permutation_p': a['active_stratified_permutation_p']}
            for variant in ('numeric_only', 'verbal_only'):
                g = g_index[parameter, problem, variant]
                row[variant] = {'assessment': g['assessment'], 'criterion_met': g['criterion_met'],
                                'eligible_from_source': g['source_sweep_criterion_met'],
                                'slope_ratio': g['absolute_logit_slope_ratio'], 'fit': deepcopy(g['fit'])}
            result.append(row)
    utils.log_dataframe_summary(pd.DataFrame(result), 'Joined evidence: all 30 canonical parameter/problem rows retained', logger)
    return result


def main():
    raw = {name: path.read_bytes() for name, path in SOURCES.items()}
    sources = {name: json.loads(value.decode('utf-8')) for name, value in raw.items()}
    rows = build_matrix(sources)
    result = {'scope': 'Original canonical implementation, 30 parameter/problem rows; no new composite pass rule.',
              'source_sha256': {SOURCES[name].relative_to(ROOT).as_posix(): sha256(value).hexdigest() for name, value in raw.items()},
              'analysis_source_sha256': sha256(Path(__file__).read_bytes()).hexdigest(),
              'selection': '60 source sweeps -> 30 full_harness sweeps. Bare-delivery evidence is preserved in source, not reclassified.',
              'audit_scope': '20 active items per parameter, shared reference across three problem rows; not 20 new audit items per row.',
              'paraphrase_scope': 'Fixed .8 rotations, not a robustness test of the complete five-value response curve.',
              'inference': 'Existing estimates/tests copied, not refitted. Prior p-values remain unadjusted. Missing directions are not failures.',
              'source_records_not_reverified': 'This join verifies final-summary coverage and pins their bytes; it does not re-audit every raw historical API record.',
              'rows': rows}
    save_new(DESTINATION / 'evidence_matrix.json', result)
    lines = ['# Fixed-implementation evidence map', '', 'Offline join of completed summaries; no new model calls or gate changes.',
             'Canonical first-option rates are ordered by parameter values .1/.3/.5/.7/.9; 50 responses per point.',
             'The source JSON retains original cell CIs, fitted slopes and CIs, effect sizes, and test diagnostics.', '',
             '| Parameter | Problem | Canonical rates (%) | Original directional criterion | Numeric retention | Verbal retention | Paraphrases equivalent at .8 |',
             '|---|---|---|---|---|---|---|']
    for r in rows:
        rates = '/'.join(f"{c['rate']*100:.0f}" for c in r['canonical_cells'])
        def retention(variant):
            v = r[variant]
            if not v['eligible_from_source']: return 'not assessable'
            ratio = 'not estimable' if v['slope_ratio'] is None else f"ratio {v['slope_ratio']:.3f}"
            return ('met; ' if v['criterion_met'] else 'not met; ') + ratio
        lines.append(f"| {r['parameter']} | {r['problem']} | {rates} | {r['canonical_criterion']} | {retention('numeric_only')} | {retention('verbal_only')} | {'yes' if r['paraphrase_all_pairs_equivalent'] else 'not established'} |")
    lines += ['', 'All 30 rows retained. A missing directional hypothesis is not a failed prediction.',
              'The audit references 20 active items per parameter, not a separate audit for each problem.',
              'No parameter has active-audit permutation p<.05; small N does not establish zero recoverability.',
              'Equivalence not established is not proof of a meaningful difference. Near-fixed decisions can make agreement easy.',
              'The rotation-at-.8 result does not establish robustness of a full response curve.',
              'These columns are different tests with different scopes; no new combined pass rule is introduced.', '']
    target = DESTINATION / 'EVIDENCE_MAP.md'; output = '\n'.join(lines).encode('utf-8')
    if target.exists() and target.read_bytes() != output: raise ValueError('Preserve differing existing map')
    if not target.exists(): target.write_bytes(output)
    assert all(path.read_bytes() == raw[name] for name, path in SOURCES.items())
    print(json.dumps({'rows': len(rows), 'canonical_criterion_met': [[r['parameter'], r['problem']] for r in rows if r['canonical_criterion'] == 'met'],
                      'map': str(target)}, indent=2))


if __name__ == '__main__': main()
