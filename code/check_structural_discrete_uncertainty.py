"""Post-primary exact-pair sensitivity check; never changes frozen stage results."""
import argparse
from pathlib import Path
import json

from scipy.stats import binomtest
from run_validity_claude import save_new


def holm(values):
    order=sorted(range(len(values)),key=lambda i:values[i]);result=[0.]*len(values);previous=0.
    for k,i in enumerate(order):
        previous=max(previous,min(1.,values[i]*(len(values)-k)));result[i]=previous
    return result


def check(root):
    files=list((root/'analysis').glob('result_*.json'))
    if len(files)!=1:raise ValueError('Need one completed primary report')
    r=json.loads(files[0].read_bytes())
    if r['status']!='COMPLETE':raise ValueError('No complete-stage inference')
    rows=[]
    for g in r['groups']:
        for name in ('endpoint','interior'):
            effects=g[f'background_{name}_effects']
            if any(x not in (-1,0,1) for x in effects):raise ValueError('Exact matched binary check requires one response per condition/background')
            positive=sum(x==1 for x in effects);negative=sum(x==-1 for x in effects)
            p=binomtest(positive,positive+negative,.5).pvalue if positive+negative else 1.
            rows.append({'parameter':g['parameter'],'problem':g['problem'],'variant':g['variant'],'contrast':name,
                'n_backgrounds':len(effects),'positive_discordant':positive,'negative_discordant':negative,
                'p_exact_two_sided':p,'prespecified_direction':g['prespecified'],'effect':g[f'{name}_effect']})
    adjusted=holm([x['p_exact_two_sided'] for x in rows])
    for row,p in zip(rows,adjusted):row['p_holm']=p
    report={'status':'SUPPLEMENTARY_NOT_FROZEN_PRIMARY','primary_design_hash':r['design_hash'],
        'rationale':'Small discrete samples can make percentile-bootstrap tail intervals anti-conservative; exact paired-binomial tests use discordant outcomes. Family includes both contrasts for all groups.',
        'timing':'Supplement specified after diagnostic outcomes; preserve this development timing and do not relabel as an original preregistered gate.',
        'limits':'Conditional on independent sampled backgrounds and paired binary outcomes; provider/time dependence remains possible. Exact non-detection does not prove zero effect.',
        'primary_unchanged':True,'comparisons':rows}
    save_new(root/'analysis/discrete_uncertainty_sensitivity.json',report)
    print(json.dumps({'comparisons':len(rows),'holm_below_005':int(sum(x['p_holm']<.05 for x in rows)),'primary_unchanged':True}))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--run-root',type=Path,required=True);a=p.parse_args();check(a.run_root)
