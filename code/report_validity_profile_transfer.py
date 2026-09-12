"""Verify and report every condition in the frozen 360-call replication."""
import numpy as np
from hashlib import sha256
import json
from pathlib import Path
import zipfile

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import run_validity_profile_transfer as run
from run_validity_claude import save_new


def main():
    root = run.BASE / 'profile_transfer_20260912'
    m = json.loads((root / 'manifest.json').read_bytes()); r = run.score(root, m)
    if r['status'] != 'COMPLETE_TRANSFER_SCREEN' or r['unresolved_dispatches']:
        raise ValueError('Wait for complete valid collection')
    planned, rows, seen = run.inventory(root, m)
    ids = [x['api_call_id'] for x in rows]; seeds = [x['seed'] for x in rows]
    if (len(set(ids)) != 360 or len(set(seeds)) != 360 or any(not i or i.startswith('mock') for i in ids)
            or any(x['attempts'] != 1 or x['provider'] != 'openai' or x['model_version'] != run.base.MODEL
                   or x['temperature'] != 1 or x['max_tokens'] != 600 for x in rows)):
        raise ValueError('API provenance/settings mismatch')
    auth = json.loads((root / 'dispatch_authorization.json').read_bytes())
    if (auth['design_hash'] != m['design_hash'] or auth['request_preview_sha256'] !=
            sha256((root / 'request_preview.json').read_bytes()).hexdigest()
            or auth['planned_calls'] != 360 or auth['spending_ceiling_usd'] != 2.5):
        raise ValueError('Authorization mismatch')
    backup = json.loads((root / 'local_backup.json').read_bytes()); archive = Path(backup['path'])
    if sha256(archive.read_bytes()).hexdigest() != backup['sha256']: raise ValueError('ZIP checksum mismatch')
    with zipfile.ZipFile(archive) as z:
        if z.testzip(): raise ValueError('ZIP corrupt')
        for key in seen:
            name = 'records/' + key + '.json'
            if z.read(name) != (root / name).read_bytes(): raise ValueError('Raw ZIP bytes differ')
    save_new(root / 'analysis/verification.json', {'design_hash': m['design_hash'],
             'unique_real_api_ids': 360, 'unique_requested_seeds': 360,
             'raw_record_archive_bytes_verified': True, 'sources_messages_profiles_labels_and_parses_verified': True,
             'authorization_matches': True, 'no_retries_or_pooling': True,
             'all_settings_pinned': True, 'pending_requests': 0})
    ledger = next(json.loads(p.read_bytes()) for p in (root / 'analysis').glob('budget_*.json')
                  if json.loads(p.read_bytes())['recorded_token_estimate_usd'] == r['known_cost_usd'])
    save_new(root / 'budget_ledger.json', ledger)
    d=m['design']
    sampled=[dict(zip(run.utils.PARAM_NAMES,map(float,row))) for row in run.utils.sample_agents(20,seed=d['draw_seed'])]
    if sampled!=d['backgrounds'] or run.digest(sampled)!=d['backgrounds_hash']:raise ValueError('Background draw changed')
    source=json.loads(run.SOURCE.read_bytes())['design']['cells']
    def mask(text):
        for match in reversed(list(run.PARAMETER_RE.finditer(text))):text=text[:match.start(3)]+'VALUE'+text[match.end(3):]
        return text
    for c in d['cells']:
        bg=sampled[c['background']]
        if any(c['profile'][k]!=(c['value'] if k==c['parameter'] else bg[k]) for k in bg):raise ValueError('Counterfactual changed wrong coordinate')
        old=next(o for o in source if (o['arm'],o['parameter'],o['problem'],o['value'])==('full_harness',c['parameter'],c['problem'],.1))
        if c['messages'][1:]!=old['messages'][1:] or mask(c['messages'][0]['content'])!=mask(old['messages'][0]['content']):raise ValueError('Non-numeric text change')
    save_new(root/'analysis/profile_verification.json',{'draw_seed':d['draw_seed'],'backgrounds_hash':d['backgrounds_hash'],
        'all20_draws_reproduced_and_retained':True,'all180_conditions_change_only_numeric_values':True,
        'other_nine_values_fixed_within_each_triplet':True,'source_user_messages_and_definitions_exact':True,
        'R_and_Beta_source_hashes_unchanged':True,'no_historical_outcomes_pooled':True})
    lookup={(c['background'],c['parameter'],c['value']):c for c in r['cells']}
    rng=np.random.default_rng(d['analysis_seed']);indices=rng.integers(0,20,size=(50000,20))
    fig,axes=plt.subplots(1,3,figsize=(10,4.8),layout='constrained',sharey=True)
    for ax,(parameter,problem,target),color in zip(axes,run.CASES,('#3266a5','#bd582c','#348254')):
        curves=np.array([[lookup[b,parameter,v]['rate'] for v in run.VALUES] for b in range(20)])
        means=curves.mean(axis=0);boot=curves[indices].mean(axis=1)
        lo,hi=np.quantile(boot,[.025,.975],axis=0,method='linear')
        for curve in curves:ax.plot(run.VALUES,curve,color=color,alpha=.09,linewidth=.8)
        ax.errorbar(run.VALUES,means,yerr=[means-lo,hi-means],fmt='o-',color=color,linewidth=2,capsize=3)
        ax.set(title=f'{parameter} / {problem}',xlabel=f'{parameter} value',ylabel=f'{target} probability',
               xticks=run.VALUES,xlim=(0,1),ylim=(-.04,1.04))
        ax.grid(axis='y',alpha=.15);ax.spines[['top','right']].set_visible(False)
    fig.suptitle('Parameter effects across 20 new complete profile backgrounds',fontsize=12)
    fig.get_layout_engine().set(rect=(0,.18,1,.71))
    fig.text(.03,.115,'Thick lines: means. Faint lines: all 20 backgrounds, two responses per point; individual curves are noisy.',fontsize=8)
    fig.text(.03,.070,'Bars: approximate marginal 95% background-bootstrap intervals. Primary decisions use adjusted effect intervals.',fontsize=8)
    fig.text(.03,.025,'Neutral | GPT-5.4-mini-2026-03-17 | draw 20260929 | schedule 20260930 | analysis 20261001',fontsize=8)
    files=[]
    for ext in ('png','pdf'):
        p=root/'analysis'/f'fig_01_profile_transfer.{ext}'
        if p.exists():raise ValueError('Preserve existing figure')
        fig.savefig(p,dpi=200);files.append({'path':p.name,'sha256':sha256(p.read_bytes()).hexdigest()})
    plt.close(fig)
    save_new(root/'analysis/figure_provenance.json',{'design_hash':m['design_hash'],'analysis_digest':run.digest(r),
        'script_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),'all20_backgrounds_retained':True,'files':files})
    lines=['# Three-parameter profile transfer','',
        f"**360/360 valid responses**, estimated token cost **${r['known_cost_usd']:.6f}**.",
        '20 sampled backgrounds x3 separate parameter interventions x3 levels x2 complete blocks. Neutral context; draw20260929, schedule20260930, analysis20261001.', '',
        '## Three prespecified local comparisons','',
        '| Parameter / target | Counts at .1 / .5 / .9 (each/40) | High-low effect | Nominal95 interval | Adjusted98.333% interval | Block1 / block2 effects | Local support |',
        '|---|---|---:|---|---|---|---|']
    for p in r['primary']:
        counts=[sum(lookup[b,p['parameter'],v]['target_count'] for b in range(20)) for v in run.VALUES]
        nlo,nhi=p['nominal95'];alo,ahi=p['bonferroni983333'];b1,b2=p['block_effects']
        lines.append(f"| {p['parameter']} / {p['target_label']} | {' / '.join(map(str,counts))} | {p['mean_high_minus_low']:+.3f} | [{nlo:+.3f},{nhi:+.3f}] | [{alo:+.3f},{ahi:+.3f}] | {b1:+.3f} / {b2:+.3f} | {p['local_transfer_supported']} |")
    lines+=['','50000 shared whole-background percentile resamples. Adjusted intervals use Bonferroni across three comparisons; coverage remains approximate with20 backgrounds. Local support requires adjusted lower bound>0 and positive effects in both blocks. No global architecture pass.', '',
        '![All backgrounds and aggregate curves](fig_01_profile_transfer.png)','',
        '## All background effects','',
        'High-minus-low target probability, averaged across two blocks. Do not classify individual backgrounds as reliable passes/fails from two responses per level.', '',
        '| Background | MoR ADOPT | MS FORMAL_REPORT | RE WAIT |','|---|---:|---:|---:|']
    effects={(e['background'],e['parameter']):e['effect'] for e in r['background_effects']}
    for b in range(20):lines.append(f"| {b:02d} | {effects[b,'MoR']:+.2f} | {effects[b,'MS']:+.2f} | {effects[b,'RE']:+.2f} |")
    lines+=['','## Scope and provenance','',
        'All20 backgrounds retained, with unchanged Beta/R sampling. Copies intervene on one coordinate and are not unmodified joint-population draws. Other nine coordinates remain fixed within each triplet. The three coordinates are tested separately; interactions are not identified.',
        'Source definitions, non-profile text and locked S2/S3 user messages match exactly. No answer targets are injected. RE is scored toward WAIT under its original hypothesis; ADOPT remains the first literal option in S3.',
        'All360 provider IDs and request seeds unique; no retries, missing outcomes or unresolved requests. Source hashes, exact messages/profiles/labels/parses and raw ZIP bytes verified. All20 sampled profiles reproduced from the fixed seed. Local archive is on this computer, not off-device storage.',
        'No historical outcomes pooled. Cases were selected from development evidence. Fixed wording and familiar dilemmas limit transfer claims. Three levels do not replace five-point gradients; midpoint order is descriptive. No interpretation/recovery, paraphrase or representation gate is passed by this result alone. Phase1.5 remains open and Phase2 held.',
        f"Remaining tracked allowance **${ledger['remaining_original_allowance_conservative_usd']:.6f}**; provider balance unverified. No automatic additional calls.", '']
    target=root/'analysis/REPORT.md'
    if target.exists():raise ValueError('Preserve existing report')
    target.write_text('\n'.join(lines),encoding='utf-8')
    print(json.dumps({'primary':r['primary'],'ledger':ledger},indent=2))


if __name__=='__main__':main()
