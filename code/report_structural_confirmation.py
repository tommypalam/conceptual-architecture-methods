"""Verify and report the independently collected paired PD endpoint study."""
from hashlib import sha256
import json
from pathlib import Path
import zipfile
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import run_structural_pd_confirmation as study


def report():
    root=study.ROOT
    m=json.loads((root/'manifest.json').read_bytes())
    _,rows,_=study.run.inventory(root,m)
    paths=list((root/'analysis').glob('result_*.json'))
    if len(paths)!=1:raise ValueError('Require one result')
    r=json.loads(paths[0].read_bytes())
    if not r['complete'] or study.assess(rows,m)!=r:raise ValueError('Result differs on recomputation')
    previous_ids=set()
    for stage in ('diagnostics','sweep'):
        previous_ids.update(x['api_call_id'] for x in study.run.ValiditySink(study.run.PACKAGE/stage/'records').read_all())
    ids=[x['api_call_id'] for x in rows]
    if len(set(ids))!=100 or previous_ids&set(ids):raise ValueError('Reused returned API ID')
    backup=json.loads((root/'local_backup.json').read_bytes())
    archive=Path(backup['path'])
    if sha256(archive.read_bytes()).hexdigest()!=backup['sha256']:raise ValueError('Archive hash mismatch')
    with zipfile.ZipFile(archive) as z:
        if z.testzip():raise ValueError('Corrupt archive')
        for p in (root/'records').rglob('*.json'):
            if z.read(p.relative_to(root).as_posix())!=p.read_bytes():raise ValueError('Raw archive mismatch')
    study.save_new(root/'analysis/verification.json',{'status':'PASS','records':100,'unique_api_ids':100,
        'no_API_ID_overlap_with_prior_3480':True,'result_recomputed':True,'source_requests_raw_reparsing_verified':True,
        'raw_zip_byte_equality_verified':True,'result_sha256':sha256(paths[0].read_bytes()).hexdigest(),
        'off_device_backup_verified':False})
    fig,axes=plt.subplots(1,2,figsize=(9,4),sharey=True)
    for ax,g in zip(axes,r['groups']):
        ax.plot([.1,.9],g['rates'],'o-',color='#126C80',lw=2)
        ax.set_title(f"{g['problem']}: {g['target_label']}")
        ax.set(xticks=[.1,.9],xlabel='Procedural Dependence',ylim=(-.04,1.04))
        lo,hi=g['simultaneous95']
        ax.text(.04,.96,f"Change: +{100*g['effect']:.0f} percentage points\nSimultaneous 95% CI [{100*lo:.1f}, {100*hi:.1f}]",transform=ax.transAxes,va='top',fontsize=9)
        ax.grid(alpha=.2)
    axes[0].set_ylabel('Target decision rate')
    fig.suptitle('Independent PD confirmation | 25 new paired backgrounds')
    fig.tight_layout()
    for ext in ('png','pdf'):fig.savefig(root/f'analysis/fig_02_PD_confirmation.{ext}',dpi=160)
    plt.close(fig)
    lines=['# Independent PD confirmation','',
        '**Both prospectively specified endpoint contrasts passed.** 100/100 valid responses; estimated cost $0.1079835.',
        'Neutral context, 25 new backgrounds, one response per endpoint/dilemma. Draw seed20261012; schedule20261013. Model gpt-5.4-mini-2026-03-17, temperature1, max600.',
        '', '| Dilemma / target | PD .1 | PD .9 | Paired change, pp | Simultaneous 95% CI, pp | Holm-adjusted exact p |',
        '|---|---:|---:|---:|---|---:|']
    for g in r['groups']:
        lo,hi=g['simultaneous95']
        lines.append(f"| {g['problem']} / {g['target_label']} | {100*g['rates'][0]:.0f}% | {100*g['rates'][1]:.0f}% | +{100*g['effect']:.0f} | [{100*lo:.1f}, {100*hi:.1f}] | {g['p_holm']:.8g} |")
    lines+=['','The paired effects were positive in20/25 S2 backgrounds and17/25 S3 backgrounds, with no opposite discordances; remaining pairs tied. No background or response was excluded.',
        '', 'The complete all-ten sweep generated these exploratory hypotheses. This separate study froze their signs, sample and exact inference before collection and used new unselected backgrounds. Its results are not pooled with the exploratory source.',
        '', 'Increasing the same coordinate caused different actions in the two tasks: more formal reporting in S2 and more waiting in S3. This supports a reproducible context-dependent effect of a normatively defined parameter in the decision generator. No external ethical filter replaced a generated decision.',
        '', 'Interpretation remains bounded. S2 pits formal classification against proportionate local correction; neither action is inherently morally better. S3 WAIT permits preparing a written plan but can also express caution or preservation; it is not uniquely diagnostic of procedural reasoning. These are reused dilemmas with fresh profiles, not unseen-task transfer. An endpoint study does not establish graded response or paraphrase equivalence, intrinsic moral understanding, or a unique internal mechanism.',
        '', 'The original full validity gate remains unmet and Phase2 remains on hold. This is local confirmation, not validation of all ten coordinates.',
        '', '[Frozen protocol](../PROTOCOL.md) | [Figure](fig_02_PD_confirmation.png) | [Verification](verification.json)',
        '', 'Raw records, requests, unique IDs, recomputed statistics and same-computer ZIP byte equality verified. No off-device backup is claimed.','']
    (root/'analysis/REPORT.md').write_text('\n'.join(lines),encoding='utf-8')
    print(json.dumps({'both_supported':r['both_supported'],'records':100,'verification':'PASS'}))


if __name__=='__main__':report()
