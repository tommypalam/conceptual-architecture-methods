"""Verify and report every condition in the frozen 40-call replication."""
from hashlib import sha256
import json
from pathlib import Path
import zipfile

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import run_validity_ms_seed_replay as run
from run_validity_claude import save_new


def main():
    root = run.BASE / 'ms_seed_replay_20260912'
    m = json.loads((root / 'manifest.json').read_bytes()); r = run.score(root, m)
    if r['status'] != 'COMPLETE_SEED_REPLAY' or r['unresolved_dispatches']:
        raise ValueError('Wait for complete valid collection')
    planned, rows, seen = run.inventory(root, m)
    ids = [x['api_call_id'] for x in rows]; seeds = [x['seed'] for x in rows]
    if (len(set(ids)) != 40 or len(set(seeds)) != 40 or any(not i or i.startswith('mock') for i in ids)
            or any(x['attempts'] != 1 or x['provider'] != 'openai' or x['model_version'] != run.base.MODEL
                   or x['temperature'] != 1 or x['max_tokens'] != 600 for x in rows)):
        raise ValueError('API provenance/settings mismatch')
    auth = json.loads((root / 'dispatch_authorization.json').read_bytes())
    if (auth['design_hash'] != m['design_hash'] or auth['request_preview_sha256'] !=
            sha256((root / 'request_preview.json').read_bytes()).hexdigest()
            or auth['planned_calls'] != 40 or auth['spending_ceiling_usd'] != .3):
        raise ValueError('Authorization mismatch')
    backup = json.loads((root / 'local_backup.json').read_bytes()); archive = Path(backup['path'])
    if sha256(archive.read_bytes()).hexdigest() != backup['sha256']: raise ValueError('ZIP checksum mismatch')
    with zipfile.ZipFile(archive) as z:
        if z.testzip(): raise ValueError('ZIP corrupt')
        for key in seen:
            name = 'records/' + key + '.json'
            if z.read(name) != (root / name).read_bytes(): raise ValueError('Raw ZIP bytes differ')
    save_new(root / 'analysis/basic_verification.json', {'design_hash': m['design_hash'],
             'unique_real_api_ids': 40, 'unique_requested_seeds': 40,
             'raw_record_archive_bytes_verified': True, 'sources_messages_profiles_labels_and_parses_verified': True,
             'authorization_matches': True, 'no_retries_or_pooling': True,
             'all_settings_pinned': True, 'pending_requests': 0})
    ledger = next(json.loads(p.read_bytes()) for p in (root / 'analysis').glob('budget_*.json')
                  if json.loads(p.read_bytes())['recorded_token_estimate_usd'] == r['known_cost_usd'])
    save_new(root / 'budget_ledger.json', ledger)
    pair_rows=[];source_ids=set()
    for row in rows:
        c,index,seed=planned[row['record_key']]
        ref=c['replay_sources'][index-1];source_path=run.ROOT/ref['path']
        source=json.loads(source_path.read_bytes())
        if sha256(source_path.read_bytes()).hexdigest()!=ref['sha256']:raise ValueError('Source bytes changed')
        if any(row[k]!=source[k] for k in ('request_messages','seed','temperature','max_tokens','model_version','agent_parameters')):
            raise ValueError('Replay differs from source request/settings')
        if row['api_call_id']==source['api_call_id']:raise ValueError('Reused provider response')
        source_ids.add(source['api_call_id'])
        pair_rows.append({'cohort':c['cohort'],'index':index,'seed':seed,'source_path':ref['path'],
            'source_sha256':ref['sha256'],'new_record_key':row['record_key'],
            'new_sha256':sha256((root/'records'/(row['record_key']+'.json')).read_bytes()).hexdigest(),
            'source_decision':source['parsed_decision'],'new_decision':row['parsed_decision'],
            'match':source['parsed_decision']==row['parsed_decision'],
            'source_timestamp':source['timestamp_utc'],'new_timestamp':row['timestamp_utc'],
            'source_fingerprint':source['response_payload'].get('system_fingerprint'),
            'new_fingerprint':row['response_payload'].get('system_fingerprint')})
    if len(source_ids)!=40 or source_ids.intersection(ids):raise ValueError('Historical/current ID overlap')
    if not auth.get('explicit_approval'):raise ValueError('Missing explicit approval record')
    save_new(root/'analysis/replay_verification.json',{'design_hash':m['design_hash'],
        'all40_requests_match_historical_messages_model_temperature_tokens_and_seed':True,
        'all40_profiles_and_source_record_hashes_match':True,'unique_new_ids':40,'unique_historical_ids':40,
        'no_provider_id_overlap_with_sources':True,'historical_seed_reuse_intentional':True,
        'explicit_approval_verified':True,'pairs':sorted(pair_rows,key=lambda p:(p['cohort'],p['index']))})
    lines=['# Canonical MS exact-request replay','',
        f"**40/40 valid**, estimated token cost **${r['known_cost_usd']:.6f}**.",
        'Neutral context; canonical MS=.9/S2; all ten original values. GPT-5.4-mini-2026-03-17, temperature1, max600. Ordering seed20260928; API seeds replay history.', '',
        '## Prespecified paired comparisons','',
        '| Source cohort | Source FORMAL_REPORT | Replay FORMAL_REPORT | Matched decisions | Gains / losses | Paired change | Nominal conservative 95% CI | Holm p |',
        '|---|---:|---:|---:|---:|---:|---|---:|']
    for c,p in zip(r['cells'],r['primary_paired_comparisons']):
        e=p['paired_change'];lo,hi=e['conservative_95_interval_unknown_envelope']
        lines.append(f"| {c['cohort']} | {c['source_formal_report_count']}/20 | {c['formal_report_count']}/20 | {c['matches']}/20 | {c['gains']} / {c['losses']} | {e['difference']:+.3f} | [{lo:+.3f}, {hi:+.3f}] | {p['holm_p']:.6g} |")
    lines+=['','Two-sided exact McNemar tests, Holm across two cohorts. Intervals combine exact gain/loss proportion bounds and are nominal, not Holm-adjusted. All source/new pairs retained in replay_verification.json. No missing or invalid outcomes.', '']
    sec=r['secondary_current_cohort_comparison'];e=sec['crossover_minus_expanded'];lo,hi=e['conservative_95_interval_unknown_envelope']
    lines += ['## Secondary fresh-cohort comparison','',
        f"Crossover-seed minus expanded-seed report probability: {e['difference']:+.3f}, conservative nominal95 interval [{lo:+.3f}, {hi:+.3f}]; descriptive two-sided Fisher p={sec['descriptive_fisher_p']:.6g}. No additional significance or expansion rule.", '',
        '## Verification and limits','',
        'Every new request matches its historical messages, model, temperature, completion-token limit and requested seed, with identical ten-parameter values. All40 source record hashes verified, all40 new provider IDs unique and separate from40 historical IDs. Raw ZIP bytes verified; no retries, replacements or pooling.',
        'Historical cohorts were selected after seeing the discrepancy, but all20 seeds from each cohort were included regardless of individual outcome. Same-seed requests need not return identical decisions. Changes cannot alone identify backend drift or establish failure of ethical encoding in principle. Fixed cohorts, timing, possible dependence and the small sample limit inference.',
        'This is a paired reproducibility diagnostic, not monotonicity, equivalence, internal understanding or a Phase1.5 pass. Original gate unchanged; Phase2 held. No automatic additional calls.',
        f"Remaining tracked allowance **${ledger['remaining_original_allowance_conservative_usd']:.6f}**; provider balance unverified. Local verified archive remains on this computer.", '']
    target=root/'analysis/REPORT.md'
    if target.exists():raise ValueError('Preserve existing report')
    target.write_text('\n'.join(lines),encoding='utf-8')
    save_new(root/'analysis/report_provenance.json',{'design_hash':m['design_hash'],
        'results_digest':run.digest(r),'script_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
        'report_sha256':sha256(target.read_bytes()).hexdigest()})
    print(json.dumps({'cells':r['cells'],'primary':r['primary_paired_comparisons'],'secondary':sec,'ledger':ledger},indent=2))


if __name__=='__main__':main()
