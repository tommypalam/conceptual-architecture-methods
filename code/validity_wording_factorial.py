"""Offline planning and analysis for the exploratory PD/S3 wording factorial."""
from pathlib import Path
import numpy as np
from scipy.stats import beta

from engine.validity_variants import PARAMETER_RE

CONTRASTS={
    'PD_wording_P2_minus_P3':np.array([.5,-.5,.5,-.5]),
    'other_nine_P2_minus_P3':np.array([.5,.5,-.5,-.5]),
    'interaction_difference_in_differences':np.array([1.,-1.,-1.,1.]),
}


def mix_endpoints(pd_template,other_template):
    """Copy only PD's two endpoint strings into the other template; no new words."""
    pd=list(PARAMETER_RE.finditer(pd_template))[5]
    target=list(PARAMETER_RE.finditer(other_template))[5]
    result=other_template
    for group in (5,4):
        result=result[:target.start(group)]+pd[group]+result[target.end(group):]
    return result


def exact_table(n,alpha=.05):
    """Four simultaneous exact intervals; union-bound coverage >=1-alpha."""
    k=np.arange(n+1); tail=alpha/4/2
    low=np.zeros(n+1); high=np.ones(n+1)
    low[1:]=beta.ppf(tail,k[1:],n-k[1:]+1)
    high[:-1]=beta.ppf(1-tail,k[:-1]+1,n-k[:-1])
    return np.column_stack([low,high])


def interval_contrast(bounds,weights):
    weights=np.asarray(weights)
    lower=np.sum(np.where(weights>=0,bounds[...,0],bounds[...,1])*weights,axis=-1)
    upper=np.sum(np.where(weights>=0,bounds[...,1],bounds[...,0])*weights,axis=-1)
    return np.stack([lower,upper],axis=-1)


def analyze_counts(counts,totals,invalid):
    counts=np.asarray(counts); totals=np.asarray(totals); invalid=np.asarray(invalid)
    if counts.shape!=(4,) or totals.shape!=(4,) or invalid.shape!=(4,):
        raise ValueError('Need four conditions A,B,C,D')
    if np.any(totals<=0) or np.any(counts<0) or np.any(invalid<0) or np.any(counts+invalid>totals):
        raise ValueError('Invalid counts')
    bounds=np.array([[exact_table(int(n))[int(k),0],exact_table(int(n))[int(k+u),1]]
        for k,n,u in zip(counts,totals,invalid)])
    valid=totals-invalid
    rates=np.divide(counts,valid,out=np.full(4,np.nan),where=valid>0)
    result={}
    for name,w in CONTRASTS.items():
        ci=interval_contrast(bounds,w)
        result[name]={'estimate_valid_only':float(rates@w) if np.all(valid>0) else None,
            'simultaneous_ci95_unknowns_expanded':ci.tolist(),
            'excludes_zero':bool(ci[0]>0 or ci[1]<0)}
    return {'condition_bounds':bounds.tolist(),'contrasts':result}


def plan_power(seed=20260910,repetitions=20000,sizes=(100,200,300,400)):
    scenarios={
        'null_balanced':([.5,.5,.5,.5],None),
        'PD_main_20pp_balanced':([.6,.4,.6,.4],'PD_wording_P2_minus_P3'),
        'other_nine_main_20pp_balanced':([.6,.6,.4,.4],'other_nine_P2_minus_P3'),
        'interaction_40pp_balanced':([.6,.4,.4,.6],'interaction_difference_in_differences'),
        'PD_main_20pp_different_backgrounds':([.4,.2,.8,.6],'PD_wording_P2_minus_P3'),
        'PD_main_10pp_balanced':([.55,.45,.55,.45],'PD_wording_P2_minus_P3'),
        'interaction_20pp_balanced':([.55,.45,.45,.55],'interaction_difference_in_differences'),
    }
    rows=[]
    for n in sizes:
        table=exact_table(n)
        for index,(name,(probs,target)) in enumerate(scenarios.items()):
            rng=np.random.default_rng(np.random.SeedSequence([seed,n,index]))
            counts=rng.binomial(n,probs,size=(repetitions,4)); bounds=table[counts]
            powers={}; any_detection=np.zeros(repetitions,dtype=bool)
            for contrast,w in CONTRASTS.items():
                ci=interval_contrast(bounds,w); detected=(ci[:,0]>0)|(ci[:,1]<0)
                powers[contrast]=float(detected.mean()); any_detection |= detected
            rows.append({'n_per_condition':n,'scenario':name,'probabilities':probs,
                'target_contrast':target,'target_power':powers[target] if target else None,
                'detection_rates':powers,'any_detection_rate':float(any_detection.mean()),
                'repetitions':repetitions})
    return {'seed':seed,'repetitions':repetitions,'method':'Four Bonferroni exact rate intervals; weighted contrast bounds; no missing observations simulated',
            'targets':'At least 80% power for 20pp main effects and 40pp interaction in specified balanced scenarios; smaller effects explicitly underpowered',
            'rows':rows}
