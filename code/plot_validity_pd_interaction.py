"""Offline figure of fixed-text PD interaction rates; no API calls."""
import argparse
from hashlib import sha256
import json
import logging
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd

import run_validity_pd_interaction as run
import utils
from run_validity_claude import save_new


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run-root',type=Path,required=True)
    args=parser.parse_args();root=args.run_root.resolve()
    manifest=json.loads((root/'manifest.json').read_bytes())
    run.base.check(manifest)
    report=run.score(root,manifest)
    if report['n_records']!=run.PLANNED: raise ValueError('Wait for complete collection')
    rows=[{'arm':s['arm'],**c} for s in report['sweeps'] for c in s['cells']]
    logging.basicConfig(level=logging.INFO)
    utils.log_dataframe_summary(pd.DataFrame(rows),'All ten observed cells for figure',logging.getLogger('ablation-figure'))
    fig,ax=plt.subplots(figsize=(7.4,5.2),layout='constrained')
    for arm,label,color,offset in [('pd_low','PD = 0.1 (outcome-dominant)','#3569A7',-.007),
                                   ('pd_high','PD = 0.9 (process-dominant)','#CB6525',.007)]:
        cells=[r for r in rows if r['arm']==arm]
        valid=[c for c in cells if c['rate'] is not None]
        ax.errorbar([c['value']+offset for c in valid],[c['rate'] for c in valid],
                    yerr=[[max(0.,c['rate']-c['ci95'][0]) for c in valid],
                          [max(0.,c['ci95'][1]-c['rate']) for c in valid]],
                    color=color,marker='o',linestyle='none',capsize=4,label=label)
    ax.set(xlabel='Injected MoR value',ylabel='Observed probability of ADOPT',
           xticks=list(run.VALUES),ylim=(-.035,1.035),xlim=(.055,.945))
    ax.grid(axis='y',alpha=.2);ax.spines[['top','right']].set_visible(False)
    ax.legend(frameon=False,loc='center')
    ax.set_title('Does PD change the MoR response under the same text?',fontsize=12,pad=14)
    fig.get_layout_engine().set(rect=(0,.14,1,.86))
    fig.text(.05,.095,'N = 30 per cell; bars: Wilson 95% intervals. Points offset horizontally for visibility.',fontsize=8)
    fig.text(.05,.064,'GPT-5.4-mini-2026-03-17 | S3 | neutral context | root seed 20260922',fontsize=8)
    fig.text(.05,.033,'All ten entries retained; only PD differs between curves. Matched message byte lengths.',fontsize=8)
    directory=root/'analysis';directory.mkdir(exist_ok=True)
    files=[]
    for extension in ('png','pdf'):
        target=directory/f'fig_01_pd_interaction.{extension}'
        if target.exists():raise ValueError('Preserve existing scientific figure')
        fig.savefig(target,dpi=200)
        files.append({'path':target.name,'sha256':sha256(target.read_bytes()).hexdigest()})
    plt.close(fig)
    save_new(directory/'figure_provenance.json',{'design_hash':manifest['design_hash'],
             'analysis_digest':run.digest(report),'script_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
             'files':files,'all_ten_cells_retained':True,'curve_interpolation':False})


if __name__=='__main__':main()
