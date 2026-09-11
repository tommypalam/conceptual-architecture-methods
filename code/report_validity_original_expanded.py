"""Verify and report every condition in the frozen 640-call replication."""
from hashlib import sha256
import json
from pathlib import Path
import zipfile

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import run_validity_original_expanded as run
from run_validity_claude import save_new


def main():
    root = run.BASE / 'original_expanded_20260911'
    m = json.loads((root / 'manifest.json').read_bytes()); r = run.score(root, m)
    if r['status'] != 'COMPLETE_SELECTED_CASE_REPLICATION' or r['unresolved_dispatches']:
        raise ValueError('Wait for complete valid collection')
    planned, rows, seen = run.inventory(root, m)
    ids = [x['api_call_id'] for x in rows]; seeds = [x['seed'] for x in rows]
    if (len(set(ids)) != 640 or len(set(seeds)) != 640 or any(not i or i.startswith('mock') for i in ids)
            or any(x['attempts'] != 1 or x['provider'] != 'openai' or x['model_version'] != run.base.MODEL
                   or x['temperature'] != 1 or x['max_tokens'] != 600 for x in rows)):
        raise ValueError('API provenance/settings mismatch')
    auth = json.loads((root / 'dispatch_authorization.json').read_bytes())
    if (auth['design_hash'] != m['design_hash'] or auth['request_preview_sha256'] !=
            sha256((root / 'request_preview.json').read_bytes()).hexdigest()
            or auth['planned_calls'] != 640 or auth['spending_ceiling_usd'] != 4.5):
        raise ValueError('Authorization mismatch')
    backup = json.loads((root / 'local_backup.json').read_bytes()); archive = Path(backup['path'])
    if sha256(archive.read_bytes()).hexdigest() != backup['sha256']: raise ValueError('ZIP checksum mismatch')
    with zipfile.ZipFile(archive) as z:
        if z.testzip(): raise ValueError('ZIP corrupt')
        for key in seen:
            name = 'records/' + key + '.json'
            if z.read(name) != (root / name).read_bytes(): raise ValueError('Raw ZIP bytes differ')
    save_new(root / 'analysis/verification.json', {'design_hash': m['design_hash'],
             'unique_real_api_ids': 640, 'unique_requested_seeds': 640,
             'raw_record_archive_bytes_verified': True, 'sources_messages_profiles_labels_and_parses_verified': True,
             'authorization_matches': True, 'no_retries_or_pooling': True,
             'all_settings_pinned': True, 'pending_requests': 0})
    ledger = next(json.loads(p.read_bytes()) for p in (root / 'analysis').glob('budget_*.json')
                  if json.loads(p.read_bytes())['recorded_token_estimate_usd'] == r['known_cost_usd'])
    save_new(root / 'budget_ledger.json', ledger)
    lookup = {(c['parameter'], c['wording'], c['value']): c for c in r['cells']}
    fig, axes = plt.subplots(1, 3, figsize=(10, 4.8), layout='constrained', sharey=True)
    colors = ('#3266a5', '#bd582c', '#348254', '#8a5bad')
    for ax, (parameter, problem, values) in zip(axes, run.CASES):
        for j, (wording, color) in enumerate(zip(run.WORDINGS, colors)):
            cells = [lookup[parameter, wording, value] for value in values]
            rates = [c['rate'] for c in cells]
            xx = [v + (j-1.5)*.012 for v in values]
            ax.errorbar(xx, rates, yerr=[[max(0, c['rate']-c['wilson95'][0]) for c in cells],
                                       [max(0, c['wilson95'][1]-c['rate']) for c in cells]],
                        fmt='o-', color=color, markersize=4, linewidth=1, capsize=2,
                        label='Canonical' if j == 0 else f'P{j}')
        ax.set(title=f'{parameter} / {problem}', xlabel=f'{parameter} value',
               xticks=values, xlim=(0, 1), ylim=(-.04, 1.04))
        ax.grid(axis='y', alpha=.2); ax.spines[['top', 'right']].set_visible(False)
        ax.set_ylabel('FORMAL_REPORT probability' if problem == 'S2' else 'ADOPT probability')
    axes[2].legend(fontsize=8, loc='best')
    fig.suptitle('Original delivery: selected-case replication across approved wordings', fontsize=12)
    fig.get_layout_engine().set(rect=(0, .18, 1, .71))
    fig.text(.035, .115, 'All 32 conditions, N = 20 each; other nine parameters at original means. Bars: marginal Wilson 95% intervals.', fontsize=8)
    fig.text(.035, .070, 'Lines connect observed rates; three points do not establish the original five-point gradient criterion.', fontsize=8)
    fig.text(.035, .025, 'GPT-5.4-mini-2026-03-17 | neutral context | root seed 20260926 | selected cases, not held-out selection', fontsize=8)
    figure_files = []
    for ext in ('png', 'pdf'):
        target = root / 'analysis' / f'fig_01_original_expanded.{ext}'
        if target.exists(): raise ValueError('Preserve existing derived figure')
        fig.savefig(target, dpi=200); figure_files.append({'path': target.name, 'sha256': sha256(target.read_bytes()).hexdigest()})
    plt.close(fig)
    save_new(root / 'analysis/figure_provenance.json', {'design_hash': m['design_hash'],
             'analysis_digest': run.digest(r), 'script_sha256': sha256(Path(__file__).read_bytes()).hexdigest(),
             'all_32_conditions_retained': True, 'files': figure_files})
    lines = ['# Original-delivery selected-case replication', '',
             f"**640/640 valid calls**, cost **${r['known_cost_usd']:.6f}**.",
             f"**{r['n_positive_directions_established']}/8 directional endpoint comparisons** meet Holm-adjusted p<.05.",
             f"**{r['n_gross_wording_differences']}/48 wording pairs** establish a difference beyond .10 using simultaneous exact bounds.",
             'These are different diagnostic counts; neither is the original 24/30 equivalence gate.', '',
             '## Eight primary comparisons', '',
             '| Case | Wording | Rates at .1 / .5 / .9 | High-low effect | Nominal conservative 95% CI | Holm p |',
             '|---|---|---|---:|---|---:|']
    for p in r['primary_eight_endpoint_effects']:
        e = p['endpoint_effect']; lo, hi = e['conservative_95_interval_unknown_envelope']
        rates = ' / '.join(f'{v:.0%}' for v in p['three_observed_rates'])
        lines.append(f"| {p['parameter']}/{p['problem']} | {p['wording']} | {rates} | {e['difference']:+.3f} | [{lo:+.3f}, {hi:+.3f}] | {p['holm_p']:.5g} |")
    lines += ['', 'Directions concern ADOPT for MoR/S3 and FORMAL_REPORT for MS/S2. Effect intervals are nominal across comparisons; Holm corrects the eight one-sided tests.', '',
              '## Retained PD/S3 stress case', '', '| Wording | ADOPT .1 | ADOPT .9 | High-low effect | Nominal conservative 95% CI |', '|---|---:|---:|---:|---|']
    for w in run.WORDINGS:
        a, b = lookup['PD', w, .1], lookup['PD', w, .9]; e = r['secondary_pd_endpoint_effects'][w]
        lo, hi = e['conservative_95_interval_unknown_envelope']
        lines.append(f"| {w} | {a['first_option_count']}/20 | {b['first_option_count']}/20 | {e['difference']:+.3f} | [{lo:+.3f}, {hi:+.3f}] |")
    lines += ['', 'No new directional PD hypothesis or significance claim is introduced.', '', '## Gross wording differences', '']
    hits = [p for p in r['secondary_wording_pairs'] if p['gross_difference_over_10pp']]
    for p in hits:
        lo, hi = p['simultaneous95_interval_unknown_envelope']
        lines.append(f"- {p['parameter']}/{p['problem']} at {p['value']}: {p['b']} minus {p['a']} = {p['difference_b_minus_a']:+.3f}, simultaneous 95% interval [{lo:+.3f}, {hi:+.3f}].")
    if not hits: lines.append('No gross discrepancy established at this precision. This does not establish equivalence.')
    lines += ['', 'All 48 contrasts, including non-detections and unknown-outcome bounds, are retained in the analysis JSON.', '',
              '![All selected conditions](fig_01_original_expanded.png)', '', '## Interpretation limits and verification', '',
              'Selection used prior evidence: two responsive cases plus a known stress case. Fresh observations replicate selected effects, not the full architecture or unseen dilemmas. N20 and three levels do not replace the original five-level gradients or equivalence battery.',
              'All ten parameters, original system-role delivery, approved wording, user prompts and labels retained. No baseline 50/50 or 70/30 requirement was added for profiled responses.',
              'Positive endpoint effects do not establish internal understanding, wording equivalence, representation retention or active-trait recoverability. The original Phase1.5 gate remains unchanged; Phase2 is not authorised by this result.',
              'All640 real API IDs and requested seeds unique; exact sources/messages/profiles, provider payload text and reparsed labels verified. Raw ZIP contents verified byte-for-byte; local backup remains on this computer. No retries, replacement, pooling or pending calls.',
              f"Conservative cumulative charge ${ledger['cumulative_conservative_charge_usd']:.6f}; remaining allowance ${ledger['remaining_original_allowance_conservative_usd']:.6f}. Provider balance unverified.",
              'Model gpt-5.4-mini-2026-03-17; neutral; temperature1;max600;seed20260926. No automatic follow-up allocation.', '']
    target = root / 'analysis/REPORT.md'
    if target.exists(): raise ValueError('Preserve existing report')
    target.write_bytes('\n'.join(lines).encode('utf-8'))
    print(json.dumps({'report': str(target), 'positive_comparisons': r['n_positive_directions_established'],
                     'gross_wording_differences': r['n_gross_wording_differences'], 'ledger': ledger}, indent=2))


if __name__ == '__main__': main()
