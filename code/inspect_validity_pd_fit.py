"""Post-score descriptive residual check; does not change the frozen analysis."""
import json
import logging
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.optimize import brentq
from scipy.special import expit

import run_validity_pd_interaction as run
from run_validity_claude import save_new
import utils


def main():
    root=run.curve.BASE/'pd_interaction_20260911'
    m=json.loads((root/'manifest.json').read_bytes())
    result=run.score(root,m)
    if result['n_records']!=300:raise ValueError('Complete collection required')
    rows=[]
    for sweep in result['sweeps']:
        if sweep['fit']['status']!='ok':raise ValueError('No finite frozen fit')
        cells=sweep['cells'];slope=sweep['fit']['slope']
        x=np.array([c['value'] for c in cells]);n=np.array([c['n_valid'] for c in cells])
        k=np.array([c['opt0_count'] for c in cells])
        # Recover the intercept from its score equation at the already frozen slope.
        intercept=brentq(lambda b:float(np.sum(n*expit(b+slope*x)-k)),-100,100)
        fitted=expit(intercept+slope*x)
        assert abs(float(np.sum(x*(n*fitted-k))))<1e-4
        for c,p in zip(cells,fitted):
            rows.append({'arm':sweep['arm'],'value':c['value'],'observed_rate':c['rate'],
                         'fitted_rate':float(p),'observed_minus_fitted':c['rate']-float(p)})
    logging.basicConfig(level=logging.INFO)
    utils.log_dataframe_summary(pd.DataFrame(rows),'All ten cells in post-score descriptive fit check',logging.getLogger('fit-check'))
    save_new(root/'analysis/descriptive_fit_check.json',{'design_hash':m['design_hash'],
             'analysis_digest':run.digest(result),'script_sha256':run.sha256(Path(__file__).read_bytes()).hexdigest(),
             'purpose':'Post-score descriptive check motivated by sharp observed high-PD jump. Not a preregistered test, alternative primary or replacement inference.',
             'rows':rows,'primary_result_unchanged':True})
    print(json.dumps(rows,indent=2))


if __name__=='__main__':main()
