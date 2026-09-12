"""Verify and report every condition in the frozen 160-call replication."""
from hashlib import sha256
import json
from pathlib import Path
import zipfile

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import run_validity_ms_stanza_crossover as run
from run_validity_claude import save_new


def main():
    root = run.BASE / 'ms_stanza_crossover_20260912'
    m = json.loads((root / 'manifest.json').read_bytes()); r = run.score(root, m)
    if r['status'] != 'COMPLETE_CROSSOVER' or r['unresolved_dispatches']:
        raise ValueError('Wait for complete valid collection')
    planned, rows, seen = run.inventory(root, m)
    ids = [x['api_call_id'] for x in rows]; seeds = [x['seed'] for x in rows]
    if (len(set(ids)) != 160 or len(set(seeds)) != 160 or any(not i or i.startswith('mock') for i in ids)
            or any(x['attempts'] != 1 or x['provider'] != 'openai' or x['model_version'] != run.base.MODEL
                   or x['temperature'] != 1 or x['max_tokens'] != 600 for x in rows)):
        raise ValueError('API provenance/settings mismatch')
    auth = json.loads((root / 'dispatch_authorization.json').read_bytes())
    if (auth['design_hash'] != m['design_hash'] or auth['request_preview_sha256'] !=
            sha256((root / 'request_preview.json').read_bytes()).hexdigest()
            or auth['planned_calls'] != 160 or auth['spending_ceiling_usd'] != 1.2):
        raise ValueError('Authorization mismatch')
    backup = json.loads((root / 'local_backup.json').read_bytes()); archive = Path(backup['path'])
    if sha256(archive.read_bytes()).hexdigest() != backup['sha256']: raise ValueError('ZIP checksum mismatch')
    with zipfile.ZipFile(archive) as z:
        if z.testzip(): raise ValueError('ZIP corrupt')
        for key in seen:
            name = 'records/' + key + '.json'
            if z.read(name) != (root / name).read_bytes(): raise ValueError('Raw ZIP bytes differ')
    save_new(root / 'analysis/verification.json', {'design_hash': m['design_hash'],
             'unique_real_api_ids': 160, 'unique_requested_seeds': 160,
             'raw_record_archive_bytes_verified': True, 'sources_messages_profiles_labels_and_parses_verified': True,
             'authorization_matches': True, 'no_retries_or_pooling': True,
             'all_settings_pinned': True, 'pending_requests': 0})
    ledger = next(json.loads(p.read_bytes()) for p in (root / 'analysis').glob('budget_*.json')
                  if json.loads(p.read_bytes())['recorded_token_estimate_usd'] == r['known_cost_usd'])
    save_new(root / 'budget_ledger.json', ledger)
    lookup = {(c['background'], c['ms_stanza'], c['value']): c for c in r['cells']}
    fig, axes = plt.subplots(1, 2, figsize=(8, 4.8), layout='constrained', sharey=True)
    for ax, bg in zip(axes, run.WORDINGS):
        for j, (ms, color) in enumerate(zip(run.WORDINGS, ('#3266a5', '#bd582c'))):
            cells = [lookup[bg, ms, v] for v in (.1, .9)]
            ax.errorbar([.1+j*.01, .9+j*.01], [c['rate'] for c in cells],
                yerr=[[max(0, c['rate']-c['wilson95'][0]) for c in cells],
                      [max(0, c['wilson95'][1]-c['rate']) for c in cells]],
                fmt='o-', color=color, capsize=3, label=('Canonical' if j == 0 else 'P2')+' MS stanza')
        ax.set(title=('Canonical' if bg == 'canonical' else 'P2')+' other-nine descriptions',
               xlabel='MS value', xticks=[.1,.9], xlim=(0,1), ylim=(-.04,1.04))
        ax.grid(axis='y', alpha=.2); ax.spines[['top','right']].set_visible(False)
        ax.legend(fontsize=8, loc='best')
    axes[0].set_ylabel('FORMAL_REPORT probability')
    fig.suptitle('MS / S2: verbatim stanza crossover', fontsize=13)
    fig.get_layout_engine().set(rect=(0,.17,1,.73))
    fig.text(.04,.10,'All eight conditions, N = 20 each. Bars: marginal Wilson 95% intervals.',fontsize=8)
    fig.text(.04,.06,'Lines connect endpoints; two levels do not establish a gradient or monotonicity.',fontsize=8)
    fig.text(.04,.02,'GPT-5.4-mini-2026-03-17 | neutral | seed 20260927 | other values at original means',fontsize=8)
    figure_files=[]
    for ext in ('png','pdf'):
        target=root/'analysis'/f'fig_01_ms_crossover.{ext}'
        if target.exists(): raise ValueError('Preserve existing figure')
        fig.savefig(target,dpi=200)
        figure_files.append({'path':target.name,'sha256':sha256(target.read_bytes()).hexdigest()})
    plt.close(fig)
    save_new(root/'analysis/figure_provenance.json',{'design_hash':m['design_hash'],
        'analysis_digest':run.digest(r),'script_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
        'all_eight_conditions_retained':True,'files':figure_files})
    lines=['# MS stanza/background crossover','',
        f"**160/160 valid**, estimated token cost **${r['known_cost_usd']:.6f}**.",
        'Configuration neutral; seed20260927; pinned GPT-5.4 mini; N20 per condition.', '',
        '## All conditions','',
        '| Other-nine wording | MS wording | FORMAL_REPORT at .1 | At .9 | High-low | Nominal conservative 95% CI |',
        '|---|---|---:|---:|---:|---|']
    for e in r['secondary_endpoint_effects']:
        bg,ms=e['background'],e['ms_stanza']; a,b=lookup[bg,ms,.1],lookup[bg,ms,.9]
        effect=e['high_minus_low']; lo,hi=effect['conservative_95_interval_unknown_envelope']
        lines.append(f"| {bg} | {ms} | {a['formal_report_count']}/20 | {b['formal_report_count']}/20 | {effect['difference']:+.3f} | [{lo:+.3f}, {hi:+.3f}] |")
    lines += ['', '## Prespecified primary family at MS=.9','',
        'P2 minus canonical for the varied block; the counterpart is fixed. Two-sided Fisher tests, Holm correction across all four. Intervals are conservative nominal 95%, not family-adjusted.', '',
        '| Varied block | Fixed counterpart | Difference | Nominal conservative 95% CI | Holm p | Detected |',
        '|---|---|---:|---|---:|---|']
    for p in r['primary_four_comparisons']:
        e=p['effect_p2_minus_canonical']; lo,hi=e['conservative_95_interval_unknown_envelope']
        lines.append(f"| {p['varied_component']} | {p['fixed_counterpart']} | {e['difference']:+.3f} | [{lo:+.3f}, {hi:+.3f}] | {p['holm_p']:.5g} | {p['difference_detected']} |")
    e=r['secondary_high_value_interaction'];lo,hi=e['conservative_95_interval_unknown_envelope']
    lines += ['',f"Secondary high-value interaction (P2/P2 - P2/C - C/P2 + C/C; background first): {e['difference']:+.3f}, conservative nominal95 interval [{lo:+.3f}, {hi:+.3f}]. Descriptive; no secondary significance decision.", '',
        '![All eight conditions](fig_01_ms_crossover.png)','',
        '## Scope and verification','',
        'This exploratory attribution test followed earlier observed divergence. All ten stanzas are verbatim; all numeric values, locked S2 and non-profile text unchanged. Concurrent full-template controls exactly reproduce prior messages. No historical records pooled.',
        'Non-detection is not invariance. Effects of wording blocks do not isolate semantics from lexical emphasis or length, establish internal understanding, or replace the original 24/30 equivalence requirement. Two endpoints do not establish monotonicity. Phase1.5 remains open; Phase2 held.',
        'All160 real API IDs and requested seeds unique; source hashes, exact requests/profiles, returned model/settings, provider payloads and reparsed labels verified. Raw ZIP bytes verified. Backup is on this computer; no off-device backup claim. No retries, replacement or pending requests.',
        f"Conservative cumulative charge ${ledger['cumulative_conservative_charge_usd']:.6f}; remaining tracked allowance ${ledger['remaining_original_allowance_conservative_usd']:.6f}. Provider balance unverified. No automatic expansion.", '']
    target=root/'analysis/REPORT.md'
    if target.exists(): raise ValueError('Preserve existing report')
    target.write_bytes('\n'.join(lines).encode('utf-8'))
    print(json.dumps({'primary':r['primary_four_comparisons'],'cells':r['cells'],'ledger':ledger},indent=2))


if __name__ == '__main__': main()
