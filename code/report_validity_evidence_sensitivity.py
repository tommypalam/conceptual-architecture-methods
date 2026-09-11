"""Verify completed endpoint sensitivity records and render the frozen analysis."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import zipfile

from engine.validity_sweep import digest
from run_validity_claude import save_new
import run_validity_evidence_sensitivity as probe


def report(root):
    m = json.loads((root / 'manifest.json').read_text(encoding='utf-8'))
    planned, rows, seen = probe.base.inventory(root, m)
    if len(rows) != m['design']['planned_calls'] or seen != set(planned):
        raise ValueError('Incomplete allocation; use the frozen partial scorer')
    approval = json.loads((root / 'dispatch_approved.json').read_text(encoding='utf-8'))
    if (not approval['approved'] or approval['design_hash'] != m['design_hash']
            or approval['exact_messages_hash'] != digest([c['messages'] for c in m['design']['cells']])):
        raise ValueError('Approval mismatch')
    ids = [r['api_call_id'] for r in rows]
    if len(set(ids)) != len(rows) or any(not v or v.startswith('mock-') for v in ids):
        raise ValueError('API IDs missing, duplicated or mocked')
    if any(r['terminal_failure'] or r['attempts'] != 1 or r['model_version'] != probe.base.MODEL
           or r['provider'] != 'openai' for r in rows):
        raise ValueError('Unresolved API/model/usage failure')
    intents = {}
    for p in (root / 'dispatches').rglob('*.json'):
        r = json.loads(p.read_text(encoding='utf-8')); key = r['record_key']
        if key not in planned or key in intents or r != probe.base.dispatch_intent(key, planned[key][0], m):
            raise ValueError('Invalid dispatch ledger')
        intents[key] = r
    if set(intents) != seen: raise ValueError('Dispatch/response keys differ')
    reserved = sum(r['reserved_usd'] for r in intents.values())
    if reserved > m['design']['spending_ceiling_usd'] or reserved + m['design']['prior_reserved_usd'] > 9:
        raise ValueError('Current or cumulative reservation guard exceeded')
    backup = json.loads((root / 'local_backup.json').read_text(encoding='utf-8'))
    archive = Path(backup['path'])
    if sha256(archive.read_bytes()).hexdigest() != backup['sha256']:
        raise ValueError('Backup checksum mismatch')
    with zipfile.ZipFile(archive) as z:
        if z.testzip(): raise ValueError('Corrupt backup ZIP')
        for key in seen:
            relative = 'records/' + key + '.json'
            if z.read(relative) != (root / relative).read_bytes():
                raise ValueError('Raw ZIP payload mismatch')
    result = probe.score(root, m)
    verification = {'design_hash': m['design_hash'], 'n_records': len(rows), 'n_unique_api_ids': len(set(ids)),
                    'n_unique_requested_seeds': len({r['seed'] for r in rows}),
                    'exact_requests_profiles_and_approval': True, 'all_single_attempt_expected_model': True,
                    'all_reservations_matched': True, 'reserved_usd': reserved,
                    'all_raw_zip_bytes_verified': True, 'source_hashes_verified': True}
    save_new(root / 'analysis/verification.json', verification)
    current = result['recorded_token_estimate_usd']; cumulative = current + m['design']['prior_recorded_token_estimate_usd']
    save_new(root / 'budget_ledger.json', {'total_new_authorised_usd': 9, 'screen_allocation_usd': 4,
             'recorded_full_rate_token_estimate_usd': current, 'cumulative_token_estimate_usd': cumulative,
             'remaining_allowance_estimate_usd': 9 - cumulative, 'pending_requests': 0,
             'conservative_dispatched_reservations_usd': reserved,
             'cumulative_dispatched_reservations_usd': reserved + m['design']['prior_reserved_usd'],
             'provider_account_balance_verified': False, 'automatic_expansion': False})
    lines = ['# S3 endpoint sensitivity result', '', f"Status: **{result['status']}**.", '',
             f"Collected {result['n_records']}/540; valid {result['n_valid']}; terminal failures {result['n_terminal_failures']}.",
             f"Recorded full-rate token estimate **${current:.6f}**; cumulative new-budget estimate **${cumulative:.6f}**.",
             f"Estimated allowance remaining **${9-cumulative:.6f}** of $9; not a checked account balance.",
             'Cached-input discounts are not subtracted. Screen cap $4; no automatic expansion.', '',
             '| Arm | Parameter | Wording | Value | ADOPT / valid | Rate | Wilson 95% CI |',
             '|---|---|---|---:|---:|---:|---|']
    for c in result['cells']:
        lo, hi = c['ci95']; rate = f"{c['rate']:.1%}" if c['rate'] is not None else 'N/A'
        lines.append(f"| {c['arm']} | {c['parameter']} | {c['template_wording']} | {c['value']:.1f} | {c['adopt']}/{c['n_valid']} | {rate} | [{lo:.1%}, {hi:.1%}] |")
    lines += ['', '## Endpoint response', '', 'All differences are .9 minus .1. Only grounding/MoR/canonical is primary.', '',
              '| Arm / parameter / wording | Difference | Conservative >=95% interval |', '|---|---:|---|']
    for name, v in result['endpoint_effects'].items():
        lo, hi = v['conservative_95_interval_unknown_envelope']
        lines.append(f"| {name} | {v['difference']:+.3f} | [{lo:+.3f}, {hi:+.3f}] |")
    lines += ['', '## Descriptive PD wording gaps', '', '| Arm / PD value | P2 minus P3 | Conservative >=95% interval |', '|---|---:|---|']
    for name, v in result['PD_wording_gaps'].items():
        lo, hi = v['conservative_95_interval_unknown_envelope']
        lines.append(f"| {name} | {v['difference']:+.3f} | [{lo:+.3f}, {hi:+.3f}] |")
    lines += ['', 'Secondary intervals are not adjusted across the family. Significance in one arm and its absence',
              'in another is not evidence that the arms differ. PD/S3 has no prespecified direction.',
              'Two endpoints do not establish monotonic gradients, slope retention, equivalence or joint encoding.',
              'Known S3 was selected during development; these are not holdout results. No new null data were collected.', '',
              '## Integrity', '', 'All frozen sources, full messages/profiles, seeds, approval, single-attempt identities,',
              'current/cumulative reservations and all raw ZIP payload bytes verified. Same-computer backup only.',
              f"Model `{probe.base.MODEL}`, neutral context, temperature 1, output cap 600, root seed 20260916.",
              'Original prompts and meanings are intact; tool delivery is inactive and Phase 1.5 remains open.', '']
    target = root / 'analysis/SENSITIVITY_REPORT.md'; raw = '\n'.join(lines).encode('utf-8')
    if target.exists() and target.read_bytes() != raw: raise ValueError('Preserve differing existing report')
    if not target.exists(): target.write_bytes(raw)
    print(json.dumps({'status': result['status'], 'n_valid': result['n_valid'], 'cost_estimate_usd': current,
                      'cumulative_estimate_usd': cumulative, 'report': str(target)}, indent=2))


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__); p.add_argument('--run-root', type=Path, required=True)
    report(p.parse_args().run_root.resolve())
