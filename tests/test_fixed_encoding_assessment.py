from copy import deepcopy
import json
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'code'))
import assess_fixed_encoding_evidence as assessment


def sources():
    return {name: json.loads(path.read_bytes()) for name, path in assessment.SOURCES.items()}


def test_join_preserves_inference_scope_and_original_estimates():
    inputs = sources()
    before = deepcopy(inputs)
    rows = assessment.build_matrix(inputs)
    assert inputs == before
    assert len(rows) == 30
    by_key = {(r['parameter'], r['problem']): r for r in rows}
    mor = by_key['MoR', 'S3']
    original = next(r for r in inputs['sweeps']['sweeps']
                    if (r['arm'], r['parameter'], r['problem']) == ('full_harness', 'MoR', 'S3'))
    assert mor['canonical_cells'] == original['cells']
    assert mor['canonical_fit'] == original['fit']
    assert [c['rate'] for c in mor['canonical_cells']] == [.10, .26, .42, .76, .84]
    assert mor['canonical_criterion'] == 'met'
    assert not mor['numeric_only']['criterion_met']
    assert mor['verbal_only']['criterion_met']
    assert by_key['PD', 'S3']['canonical_criterion'] == 'not_prespecified'
    assert by_key['RT', 'S3']['canonical_criterion'] == 'not_met'
    # Trait-level audit evidence is referenced, never multiplied into 600 items.
    audit_by_trait = {r['parameter']: r for r in inputs['audit']['parameters']}
    assert sum(a['active_parameter_items']['n'] for a in audit_by_trait.values()) == 200
    for row in rows:
        a = audit_by_trait[row['parameter']]
        assert row['active_audit_n_per_parameter_not_per_problem'] == a['active_parameter_items']['n']
        assert row['active_audit_permutation_p'] == a['active_stratified_permutation_p']
    mor['canonical_cells'][0]['rate'] = -1
    assert inputs == before  # Report consumers cannot mutate the loaded source.


@pytest.mark.parametrize('fault', ['missing_gradient', 'duplicate_paraphrase', 'unfinished_audit', 'wrong_grid'])
def test_incomplete_or_ambiguous_evidence_is_rejected(fault):
    inputs = sources()
    if fault == 'missing_gradient':
        inputs['gradients']['gradients'].pop()
    elif fault == 'duplicate_paraphrase':
        rows = inputs['paraphrases']['paraphrase_equivalence']['cells']
        rows.append(deepcopy(rows[0]))
    elif fault == 'unfinished_audit':
        inputs['audit']['complete'] = False
    else:
        row = next(r for r in inputs['sweeps']['sweeps'] if r['arm'] == 'full_harness')
        row['cells'][0]['value'] = .2
    with pytest.raises(ValueError):
        assessment.build_matrix(inputs)
