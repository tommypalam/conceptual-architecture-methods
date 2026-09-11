"""Offline observed rates for all sixteen wording/profile cells."""
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import run_validity_joint_wording as run
from run_validity_claude import save_new


def main():
    root=run.curve.BASE/'joint_wording_20260911'
    m=json.loads((root/'manifest.json').read_bytes())
    result=run.score(root,m)  # Logs all sixteen cells and missing values.
    if result['n_records']!=480:raise ValueError('Wait for complete collection')
    fig,axes=plt.subplots(2,2,figsize=(8.2,6.8),layout='constrained',sharey=True)
    colors=('#3569A7','#9467BD','#CB6525','#398568')
    for row,pd in enumerate((.1,.9)):
        for col,mor in enumerate((.1,.9)):
            ax=axes[row,col]
            cells=[next(c for c in result['cells'] if (c['arm'],c['pd_value'],c['mor_value'])==(arm,pd,mor)) for arm in run.ARMS]
            for x,(c,color) in enumerate(zip(cells,colors)):
                if c['rate'] is None:continue
                lo,hi=c['wilson95'];p=c['rate']
                ax.errorbar(x,p,yerr=[[max(0,p-lo)],[max(0,hi-p)]],fmt='o',color=color,capsize=4)
            ax.set(title=f'PD = {pd}, MoR = {mor}',xticks=range(4),
                   xticklabels=['Canonical','P1','P2','P3'],ylim=(-.04,1.04),xlim=(-.5,3.5))
            ax.tick_params(axis='x',labelsize=9)
            ax.grid(axis='y',alpha=.2);ax.spines[['top','right']].set_visible(False)
            if col==0:ax.set_ylabel('Observed probability of ADOPT')
    fig.suptitle('Does the same joint profile survive approved rewording?',fontsize=13)
    fig.get_layout_engine().set(rect=(0,.12,1,.88))
    fig.text(.05,.082,'N = 30 per cell. Bars: marginal Wilson 95% intervals.',fontsize=8)
    fig.text(.05,.055,'Primary decisions use simultaneous exact bounds across all sixteen cells, not these marginal bars.',fontsize=8)
    fig.text(.05,.028,'GPT-5.4-mini-2026-03-17 | S3 | neutral context | root seed 20260923',fontsize=8)
    directory=root/'analysis';files=[]
    for extension in ('png','pdf'):
        target=directory/f'fig_01_joint_wording.{extension}'
        if target.exists():raise ValueError('Preserve existing figure')
        fig.savefig(target,dpi=200)
        files.append({'path':target.name,'sha256':run.sha256(target.read_bytes()).hexdigest()})
    plt.close(fig)
    save_new(directory/'figure_provenance.json',{'design_hash':m['design_hash'],
             'analysis_digest':run.digest(result),'script_sha256':run.sha256(Path(__file__).read_bytes()).hexdigest(),
             'all_sixteen_cells_retained':True,'files':files,'intervals':'Marginal Wilson95; primary uses simultaneous exact cell bounds.'})


if __name__=='__main__':main()
