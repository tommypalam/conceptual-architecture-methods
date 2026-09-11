"""Offline verification, complete-cell figure and report for the frozen screen."""
from hashlib import sha256
import json
from pathlib import Path
import zipfile

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import run_validity_tool_delivery as run
from run_validity_claude import save_new


def main():
    root = run.BASE / 'tool_delivery_20260911'
    m = json.loads((root / 'manifest.json').read_bytes())
    result = run.score(root, m)
    if result['n_decisions'] != 320 or result['n_api_records'] != 480 or result['status'] == 'INCOMPLETE_OR_INVALID':
        raise ValueError('Complete valid allocation required for this report')
    approval = json.loads((root / 'dispatch_approved.json').read_bytes())
    if (approval['design_hash'] != m['design_hash'] or approval['request_preview_sha256'] !=
            sha256((root / 'request_preview.json').read_bytes()).hexdigest()
            or approval['maximum_api_calls'] != 480 or approval['spending_ceiling_usd'] != 3.5):
        raise ValueError('Approval scope mismatch')
    records = list(run.ValiditySink(root / 'records').read_all())
    decisions = list(run.ValiditySink(root / 'decisions').read_all())
    ids = [r['response_payload']['id'] for r in records]
    seeds = [r['request']['seed'] for r in records]
    if (len(set(ids)) != 480 or len(set(seeds)) != 480
            or any(not i or 'test-' in i or i.startswith('mock') for i in ids)):
        raise ValueError('API IDs or requested seeds invalid')
    backup = json.loads((root / 'local_backup.json').read_bytes())
    path = Path(backup['path'])
    if sha256(path.read_bytes()).hexdigest() != backup['sha256']:
        raise ValueError('Archive checksum mismatch')
    with zipfile.ZipFile(path) as z:
        if z.testzip(): raise ValueError('ZIP corrupt')
        for directory, rows in (('records', records), ('decisions', decisions)):
            for row in rows:
                name = directory + '/' + row['record_key'] + '.json'
                if z.read(name) != (root / name).read_bytes():
                    raise ValueError('Raw archive byte mismatch')
    save_new(root / 'analysis/verification.json', {
        'design_hash': m['design_hash'], 'approval_matches_exact_scope': True,
        'unique_real_api_ids': len(set(ids)), 'unique_requested_seeds': len(set(seeds)),
        'raw_api_and_decision_archive_bytes_verified': True,
        'api_records': 480, 'decisions': 320, 'unknown_usage_calls': result['unknown_usage_calls'],
        'frozen_sources_and_actual_wire_requests_verified': True})
    ledgers = [json.loads(p.read_bytes()) for p in (root / 'analysis').glob('budget_*.json')]
    ledger = next(x for x in ledgers if x['recorded_token_estimate_usd'] == result['known_cost_usd'])
    save_new(root / 'budget_ledger.json', ledger)
    lookup = {(c['delivery'], c['parameter'], c['value'], c['wording']): c for c in result['cells']}
    fig, axes = plt.subplots(2, 2, figsize=(8.6, 7.4), layout='constrained', sharey=True)
    for row, parameter in enumerate(run.PARAMETERS):
        for col, value in enumerate((.1, .9)):
            ax = axes[row, col]
            for delivery, shift, color, label in [('system', -.09, '#3266a5', 'Original system'),
                                                   ('tool', .09, '#c06024', 'Tool delivery')]:
                for j, wording in enumerate(run.WORDINGS):
                    c = lookup[delivery, parameter, value, wording]; lo, hi = c['wilson95']; p = c['rate']
                    ax.errorbar(j + shift, p, yerr=[[max(0, p-lo)], [max(0, hi-p)]],
                                fmt='o', color=color, capsize=3, label=label if j == 0 else None)
            ax.set(title=f'{parameter} = {value}',
                   xticks=range(4), xticklabels=['Canonical', 'P1', 'P2', 'P3'], ylim=(-.04, 1.04))
            ax.grid(axis='y', alpha=.2); ax.spines[['top', 'right']].set_visible(False)
            if col == 0: ax.set_ylabel('Observed probability of ADOPT')
    axes[0, 0].legend(loc='best', fontsize=8)
    fig.suptitle('Frozen specification: original versus tool delivery', fontsize=13)
    fig.get_layout_engine().set(rect=(0, .13, 1, .79))
    fig.text(.055, .09, 'All 32 conditions; N = 10 each; other nine parameters at original means.', fontsize=8)
    fig.text(.055, .06, 'Bars: marginal Wilson 95% intervals, not the primary bootstrap. Selected development cases.', fontsize=8)
    fig.text(.055, .03, 'GPT-5.4-mini-2026-03-17 | S3 | neutral | root seed 20260924', fontsize=8)
    files = []
    for extension in ('png', 'pdf'):
        target = root / 'analysis' / f'fig_01_tool_delivery.{extension}'
        if target.exists(): raise ValueError('Preserve existing figure')
        fig.savefig(target, dpi=200)
        files.append({'path': target.name, 'sha256': sha256(target.read_bytes()).hexdigest()})
    plt.close(fig)
    save_new(root / 'analysis/figure_provenance.json', {'design_hash': m['design_hash'],
             'analysis_digest': run.digest(result), 'script_sha256': sha256(Path(__file__).read_bytes()).hexdigest(),
             'all_32_cells_retained': True, 'files': files})
    effect = result['primary_tool_minus_system']; lo, hi = result['exploratory_bootstrap95']
    lines = ['# Fixed-specification tool delivery: result', '',
             f"Status: **{result['status']}**. 320/320 valid decisions; 480/480 valid API responses.",
             f"Known cost **${result['known_cost_usd']:.6f}**; remaining conservative allowance **${ledger['remaining_original_allowance_conservative_usd']:.6f}**.", '',
             '## Frozen primary', '',
             f'Tool minus original mean squared wording difference: **{effect:+.6f}**, exploratory bootstrap 95% interval **[{lo:+.6f}, {hi:+.6f}]**.',
             'Negative favours tool delivery. Units are squared probability differences, not percentage points.',
             f"Sensitivity safeguard: **{result['sensitivity_safeguard']}**.", '',
             '| MoR endpoint effect | Canonical | P1 | P2 | P3 |', '|---|---:|---:|---:|---:|']
    for delivery, effects in zip(run.DELIVERIES, result['mor_effects_by_delivery_and_wording']):
        lines.append('| ' + delivery + ' | ' + ' | '.join(f'{x:+.3f}' for x in effects) + ' |')
    lines += ['', '## Every condition', '', '| Parameter | Value | Wording | Original ADOPT / 10 | Tool ADOPT / 10 |', '|---|---:|---|---:|---:|']
    for parameter in run.PARAMETERS:
        for value in (.1, .9):
            for wording in run.WORDINGS:
                a = lookup['system', parameter, value, wording]; b = lookup['tool', parameter, value, wording]
                lines.append(f"| {parameter} | {value} | {wording} | {a['adopt']} | {b['adopt']} |")
    lines += ['', '![All conditions](fig_01_tool_delivery.png)', '',
              '## Scope and verification', '',
              'This selected N10 screen is not the 30-cell equivalence battery. The original 24/30 requirement and all other gate components remain unchanged.',
              'A favourable result warrants broader confirmation only. No-scale-up support does not prove every tool architecture fails.',
              'Bootstrap uncertainty is approximate and boundary cells can understate it. The two endpoints do not test monotonicity. The tool delivers text; it does not operationalise a new ethical decision algorithm.',
              'Role, position, bridge and turn count change together. All ten intended values, source descriptions and locked user messages are retained. All four reviewed wordings and all planned cells are reported.',
              'Sources, exact approval, wire payloads, provider payloads, reparsed decisions, unique IDs/seeds and raw ZIP bytes verified. No retries, replacements or pooling. The backup is on this computer.',
              'The earlier canonical 23/30 versus 8/30 repeat discrepancy remains unexplained. This run cannot identify its cause.', '',
              'Model gpt-5.4-mini-2026-03-17; neutral; temperature 1; final max600, retrieval max128; root seed20260924.', '']
    target = root / 'analysis/REPORT.md'
    if target.exists(): raise ValueError('Preserve existing report')
    target.write_bytes('\n'.join(lines).encode('utf-8'))
    print(json.dumps({'status': result['status'], 'report': str(target), 'ledger': ledger}, indent=2))


if __name__ == '__main__':
    main()
