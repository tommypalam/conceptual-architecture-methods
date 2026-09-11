"""Verify the completed evidence screen and render its frozen analysis."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import zipfile

from engine.validity_sweep import digest
from run_validity_claude import save_new
import run_validity_evidence_screen as screen


def report(root):
    m = json.loads((root / 'manifest.json').read_text(encoding='utf-8'))
    planned, rows, seen = screen.inventory(root, m)
    if len(rows) != m['design']['planned_calls'] or seen != set(planned):
        raise ValueError('Incomplete allocation; use the frozen partial scorer')
    approval = json.loads((root / 'dispatch_approved.json').read_text(encoding='utf-8'))
    if (not approval['approved'] or approval['design_hash'] != m['design_hash']
            or approval['exact_messages_hash'] != digest([c['messages'] for c in m['design']['cells']])):
        raise ValueError('Approval mismatch')
    ids = [r['api_call_id'] for r in rows]
    if len(set(ids)) != len(rows) or any(not v or v.startswith('mock-') for v in ids):
        raise ValueError('API IDs missing, duplicated or mocked')
    if any(r['terminal_failure'] or r['attempts'] != 1 or r['model_version'] != screen.MODEL
           or r['provider'] != 'openai' for r in rows):
        raise ValueError('Unresolved API/model/usage failure')
    intents = {}
    for p in (root / 'dispatches').rglob('*.json'):
        r = json.loads(p.read_text(encoding='utf-8')); key = r['record_key']
        if key not in planned or key in intents or r != screen.dispatch_intent(key, planned[key][0], m):
            raise ValueError('Invalid dispatch ledger')
        intents[key] = r
    if set(intents) != seen:
        raise ValueError('Dispatch/response keys differ')
    reserved = sum(r['reserved_usd'] for r in intents.values())
    if reserved > m['design']['spending_ceiling_usd']:
        raise ValueError('Reservation guard exceeded')
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
    result = screen.score(root, m)
    verification = {'design_hash': m['design_hash'], 'n_records': len(rows), 'n_unique_api_ids': len(set(ids)),
                    'n_unique_requested_seeds': len({r['seed'] for r in rows}),
                    'exact_requests_profiles_and_approval': True, 'all_single_attempt_expected_model': True,
                    'all_reservations_matched': True, 'reserved_usd': reserved,
                    'all_raw_zip_bytes_verified': True, 'source_hashes_verified': True}
    save_new(root / 'analysis/verification.json', verification)
    lines = ['# S3 evidence screen result', '', f"Status: **{result['status']}**.", '',
             f"Collected {result['n_records']}/450, valid {result['n_valid']}; terminal failures {result['n_terminal_failures']}.",
             f"Recorded full-rate token estimate: **${result['recorded_token_estimate_usd']:.6f}**; screen cap $3, total new allowance $9.",
             'Cached-input discounts are not subtracted. This is a token estimate, not a checked account balance.', '',
             '| Arm | Profile wording | ADOPT / valid | Rate | Wilson 95% CI |', '|---|---|---:|---:|---|']
    for c in result['cells']:
        lo, hi = c['ci95']; rate = f"{c['rate']:.1%}" if c['rate'] is not None else 'N/A'
        lines.append(f"| {c['arm']} | {c['wording']} | {c['adopt']}/{c['n_valid']} | {rate} | [{lo:.1%}, {hi:.1%}] |")
    lines += ['', '## Primary remaining-wording-gap screen', '']
    for arm, v in result['wording_gaps'].items():
        lo, hi = v['conservative_95_interval_unknown_envelope']
        lines.append(f"- {arm}: P2 minus P3 = {v['difference']:+.3f}; conservative >=95% interval [{lo:+.3f}, {hi:+.3f}].")
    lines += ['', 'Only the grounding gap is primary. An interval wholly outside +/-0.10 detects a gross remaining failure.',
              'Failure to detect such a gap does not establish equivalence, improvement, or a phase pass.', '',
              '## Exploratory contrasts', '', '| Contrast | Difference | Conservative nominal >=95% CI |', '|---|---:|---|']
    for name, v in result['secondary_nominal_not_studywise_adjusted'].items():
        lo, hi = v['conservative_95_interval_unknown_envelope']
        lines.append(f"| {name} | {v['difference']:+.3f} | [{lo:+.3f}, {hi:+.3f}] |")
    lines += ['', 'Secondary intervals are not adjusted across contrasts. Null comparisons test added context under the shared',
              'user schema, not equivalence to the naked Phase 0c baseline or a pure profile effect.',
              'Known S3 was selected during development; these are not holdout results. No PD/S3 direction was invented.',
              'The fixed profile cannot establish parameter responsiveness or replace the PD/S1 gradient.', '',
              '## Integrity', '', 'All frozen sources, complete requests, profiles, seeds, approval, single-attempt identities,',
              'dispatch reservations and all raw ZIP payload bytes verified. Same-computer backup only.',
              f"Model `{screen.MODEL}`, temperature 1, output cap 600, root seed 20260915.",
              'Original prompts and theory are unchanged. Tool delivery remains inactive; Phase 1.5 remains open.', '']
    target = root / 'analysis/SCREEN_REPORT.md'; raw = '\n'.join(lines).encode('utf-8')
    if target.exists() and target.read_bytes() != raw:
        raise ValueError('Existing report differs; preserve it and use a new designation')
    if not target.exists(): target.write_bytes(raw)
    print(json.dumps({'status': result['status'], 'n_valid': result['n_valid'],
                      'cost_estimate_usd': result['recorded_token_estimate_usd'], 'report': str(target)}, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run-root', type=Path, required=True)
    report(parser.parse_args().run_root.resolve())
