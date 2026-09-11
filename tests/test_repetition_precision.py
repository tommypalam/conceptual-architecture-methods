from itertools import product
from pathlib import Path
import sys

import pytest
from scipy.stats import binom

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'code'))
from diagnose_repetition_precision import ordered_probability, fitted_probabilities


def test_dynamic_program_matches_exhaustive_binomial_sum():
    p=[.1,.3,.4,.8,.9]; n=3
    expected=sum(__import__('math').prod(binom.pmf(k,n,q) for k,q in zip(ks,p))
                 for ks in product(range(n+1),repeat=5) if list(ks)==sorted(ks))
    assert ordered_probability(p,n)['nondecreasing_probability']==pytest.approx(expected,abs=1e-12)
    assert ordered_probability([0]*5,30)=={'nondecreasing_probability':1.,'all_equal_counts_probability':1.}
    assert ordered_probability([1,0,0,0,0],30)['nondecreasing_probability']==0


def test_fit_reconstruction_and_invalid_inputs():
    from scipy.special import expit
    p=expit(-2+3*__import__('numpy').array([.1,.3,.5,.7,.9]))
    s={'fit':{'status':'ok','slope':3},'cells':[{'value':x,'n_valid':100,'opt0_count':100*q} for x,q in zip([.1,.3,.5,.7,.9],p)]}
    r=fitted_probabilities(s)
    assert r['intercept']==pytest.approx(-2,abs=1e-10)
    assert r['probabilities']==pytest.approx(p)
    for bad in [[.5]*4,[.5,.5,.5,.5,float('nan')],[.5,.5,.5,.5,1.1]]:
        with pytest.raises(ValueError):ordered_probability(bad,30)
    with pytest.raises(ValueError):ordered_probability([.5]*5,0)
