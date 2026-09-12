"""Render frozen structural-stage estimates and independently verify raw records."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import zipfile

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

import run_structural_encoding_validation as run


def report(root):
    m=json.loads((root/'manifest.json').read_bytes())
    files=list((root/'analysis').glob('result_*.json'))
    if len(files)!=1:raise ValueError('Require one completed frozen result')
    r=json.loads(files[0].read_bytes());_,rows,_=run.inventory(root,m)
    if r['status']!='COMPLETE' or len(rows)!=r['n_records']:raise ValueError('Stage incomplete')
    ids=[v['api_call_id'] for v in rows]
    if len(set(ids))!=len(ids):raise ValueError('Duplicate returned API ID')
    by_cell={c['id']:c for c in m['design']['cells']}
    for row in rows:
        c=by_cell[row['cell_id']]
        if row['model_version']!=m['design']['model'] or row['temperature']!=1 or row['max_tokens']!=600 or row['attempts']!=1:raise ValueError('Settings changed')
        if row['agent_parameters']!=c['profile'] or row['request_messages']!=c['messages']:raise ValueError('Profile/request mismatch')
        if row['parsed_decision'] not in c['labels']:raise ValueError('Invalid decision')
    backup=json.loads((root/'local_backup.json').read_bytes());zpath=Path(backup['path'])
    if sha256(zpath.read_bytes()).hexdigest()!=backup['sha256']:raise ValueError('ZIP hash mismatch')
    with zipfile.ZipFile(zpath) as z:
        if z.testzip():raise ValueError('Corrupt archive')
        for p in (root/'records').rglob('*.json'):
            if z.read(p.relative_to(root).as_posix())!=p.read_bytes():raise ValueError('Archived record differs')
    verified={'status':'PASS','n_records':len(rows),'unique_api_ids':len(set(ids)),
        'source_hashes_and_exact_requests_verified':True,'raw_reparse_verified':True,
        'same_computer_zip_matches_all_current_raw_records':True,'result_sha256':sha256(files[0].read_bytes()).hexdigest(),
        'note':'No off-device backup or unique internal-mechanism inference.'}
    run.save_new(root/'analysis/verification.json',verified)
    groups=r['groups'];diagnostic=m['design']['stage']=='diagnostics'
    nrows,ncols=(2,6) if diagnostic else (10,3)
    fig,axes=plt.subplots(nrows,ncols,figsize=(18,7) if diagnostic else (12,27),squeeze=False,sharex=True,sharey=True)
    for ax,g in zip(axes.flat,groups):
        c=next(c for c in m['design']['cells'] if (c['parameter'],c['problem'],c['variant'])==(g['parameter'],g['problem'],g['variant']))
        ax.plot(run.VALUES,g['rates'],'o-',color='#126C80',lw=1.7,ms=4)
        ax.set_title(f"{g['parameter']} / {g['problem']} | {g['variant']}\n{c['target_label']}",fontsize=9)
        ax.set_ylim(-.03,1.03);ax.set_xticks(run.VALUES);ax.grid(alpha=.18)
        ax.text(.02,.96,f"endpoint {g['endpoint_effect']:+.2f}\nadj [{g['endpoint_adjusted'][0]:+.2f}, {g['endpoint_adjusted'][1]:+.2f}]",transform=ax.transAxes,va='top',fontsize=8)
    fig.suptitle(f"Structural encoding: {m['design']['stage']} | all {len(groups)} curves\nObserved rates; endpoint intervals use whole-background bootstrap and stage-wide Bonferroni correction",fontsize=13)
    fig.supxlabel('Varied parameter value');fig.supylabel('Target choice rate')
    fig.tight_layout(rect=(.025,.025,1,.96));stem=root/'analysis/fig_01_all_curves'
    fig.savefig(stem.with_suffix('.png'),dpi=140);fig.savefig(stem.with_suffix('.pdf'));plt.close(fig)
    lines=[f"# Structural encoding: {m['design']['stage']}",'',
        f"**{r['n_valid']}/{m['design']['planned_calls']} valid responses; token estimate ${r['known_cost_usd']:.6f}.**",
        f"Neutral context; {m['design']['n_backgrounds']} unselected backgrounds; draw seed {m['design']['draw_seed']}, schedule {m['design']['seed']}, analysis {m['design']['analysis_seed']}.",
        'Model gpt-5.4-mini-2026-03-17, temperature 1, maximum 600. One observation per background/condition.',
        'All displayed rates use the target label shown; unpredicted contrasts use the first response label and remain exploratory. No background removed.',
        '', '| Parameter | Problem | Representation | Target | Rates .1/.3/.5/.7/.9 | Endpoint (adjusted interval) | Interior (adjusted interval) | Ordered | Predicted endpoint supported |',
        '|---|---|---|---|---|---|---|---|---|']
    for g in groups:
        c=next(c for c in m['design']['cells'] if (c['parameter'],c['problem'],c['variant'])==(g['parameter'],g['problem'],g['variant']))
        fmt=lambda xs:'/'.join(f'{100*x:.1f}%' for x in xs)
        interval=lambda x:'['+', '.join(f'{a:+.3f}' for a in x)+']'
        lines.append(f"| {g['parameter']} | {g['problem']} | {g['variant']} | {c['target_label']} | {fmt(g['rates'])} | {g['endpoint_effect']:+.3f} {interval(g['endpoint_adjusted'])} | {g['interior_effect']:+.3f} {interval(g['interior_adjusted'])} | {g['observed_ordered']} | {g['predicted_endpoint_supported'] if g['prespecified'] else 'Exploratory'} |")
    lines+=['','[All curves](fig_01_all_curves.png) · [PDF](fig_01_all_curves.pdf)','',
        f"Adjusted intervals protect both contrasts across {len(groups)} groups: {2*len(groups)} comparisons. Nominal 95% intervals and every background effect remain in [{files[0].name}]({files[0].name}).",
        'Bootstrap coverage is approximate. Observed ordering is not proof of population monotonicity; lack of significance is not equivalence. An endpoint difference alone is not graded encoding.',
        'These rates do not constitute a fresh original-battery pass, a moral-performance score, or evidence identifying a unique internal LLM mechanism.',
        'The diagnostic panel is small and tests previously selected MoR/MS cases. The full sweep includes all thirty parameter/problem pairs; absent directional hypotheses are not counted as failures.',
        '', 'Exact requests, settings, unique returned IDs, raw reparsing and archive byte equality verified. No retries or replacements. No off-device backup claimed.','']
    target=root/'analysis/REPORT.md'
    if target.exists():raise ValueError('Preserve prior report')
    target.write_text('\n'.join(lines),encoding='utf-8')
    print(json.dumps({'verification':verified,'cost':r['known_cost_usd'],'supported':[f"{g['parameter']}/{g['problem']}/{g['variant']}" for g in groups if g['predicted_endpoint_supported']]}))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--run-root',type=Path,required=True);a=p.parse_args();report(a.run_root)
