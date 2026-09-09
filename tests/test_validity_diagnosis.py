"""Check simultaneous bounds and missing-outcome sensitivity independently."""
import sys
from pathlib import Path

import pytest
from scipy.stats import beta

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'code'))
from diagnose_validity_paraphrases import exact_bounds,difference_bounds,equivalent_counts


def test_exact_intervals_match_beta_quantiles_and_endpoints():
    tail=.05/120/2
    assert exact_bounds(17,50)==pytest.approx([beta.ppf(tail,17,34),beta.ppf(1-tail,18,33)])
    assert exact_bounds(0,50)[0]==0
    assert exact_bounds(50,50)[1]==1
    with pytest.raises(ValueError): exact_bounds(49,50,2)


def test_unknown_outcomes_envelope_all_possible_completions():
    outer=exact_bounds(20,50,3)
    for k in range(20,24):
        inner=exact_bounds(k,50)
        assert outer[0]<=inner[0] and outer[1]>=inner[1]
    a=exact_bounds(40,50); b=exact_bounds(4,50)
    forward=difference_bounds(a,b); reverse=difference_bounds(b,a)
    assert forward==pytest.approx([-reverse[1],-reverse[0]])
    assert forward[0]>.1


def test_frozen_equivalence_rule_preserves_precision_limitation():
    assert not equivalent_counts(50,25,25)
    assert equivalent_counts(50,0,0)
    assert equivalent_counts(400,200,200)
    assert not equivalent_counts(400,40,300)
