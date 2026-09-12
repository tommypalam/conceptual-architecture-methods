"""Local completion worker: verify, summarize and save an already-authorized run."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import time
import zipfile
import run_all_ten_followup as run


def finish():
    root=run.ROOT;m=json.loads((root/'manifest.json').read_bytes());run.old.base.check(m)
    _,rows,_=run.old.inventory(root,m)
    paths=list((root/'analysis').glob('result_*.json'))
    if len(paths)!=1:raise ValueError('Expected one terminal result')
    result=json.loads(paths[0].read_bytes());ledger=json.loads((root/'budget_ledger.json').read_bytes())
    if result!=run.assess(rows,m):raise ValueError('Result differs on independent recomputation')
    if len(rows)!=ledger['n_records'] or ledger['total_accounted_usd']>25:raise ValueError('Count/budget mismatch')
    backup=json.loads((root/'local_backup.json').read_bytes());p=Path(backup['path'])
    if sha256(p.read_bytes()).hexdigest()!=backup['sha256']:raise ValueError('Backup hash mismatch')
    with zipfile.ZipFile(p) as z:
        if z.testzip():raise ValueError('Corrupt archive')
        for name,h in backup['file_sha256'].items():
            raw=(root/name).read_bytes()
            if sha256(raw).hexdigest()!=h or z.read(name)!=raw:raise ValueError('Archived file differs')
    ids=[r['api_call_id'] for r in rows if r['api_call_id']]
    if len(ids)!=len(set(ids)):raise ValueError('Duplicate provider IDs')
    audit=json.loads((run.old.PACKAGE/'audit_schema_r3/analysis/prevalence_summary.json').read_bytes())['parameters']
    exact=result['gradient_sensitivity']['exact_paired_180_comparisons']
    retention=result['gradient_sensitivity']['representation_retention_diagnostic']
    lines=['# All-ten follow-up: completed collection assessment','',
        f"Collection status: **{ledger['status']}**. Recorded **{len(rows):,}/{m['design']['planned_calls']:,}**; parse-invalid {result['n_parse_invalid']}; terminal API/integrity failures {result['n_terminal_failures']}.",
        'A stopped/incomplete allocation is not a completed fixed-N study. No records were replaced. Original Phase1.5 gate remains unmet and Phase2 remains on hold.',
        '', 'Neutral configuration; 50 new sampled backgrounds, first25 for gradients. One response per condition. Draw/schedule/analysis seeds20261020/20261021/20261022. Fixed gpt-5.4-mini-2026-03-17, temperature1, max600.',
        '', '| Parameter | Canonical paired endpoint/interior signals, Holm180 | Numeric retention diagnostic | Verbal retention diagnostic | Wording equivalent cells /3 | Prior active audit accuracy; Holm10 p |',
        '|---|---|---|---|---|---|']
    for parameter in m['design']['params']:
        effects=[f"{x['problem']} {x['contrast']} ({x['effect']:+.2f})" for x in exact if x['parameter']==parameter and x['variant']=='canonical' and x['complete_pairs'] and x['p_holm']<.05]
        def retained(variant):
            eligible=[x for x in retention if x['parameter']==parameter and x['variant']==variant and x['assessment']=='eligible']
            if not eligible:return 'Not assessable under legacy eligibility'
            passed=[x['problem'] for x in eligible if x['criterion_met']]
            return ', '.join(passed) if passed else 'Not established'
        word=[w for w in result['wording_analysis'] if w['parameter']==parameter]
        a=next(a for a in audit if a['parameter']==parameter)
        lines.append(f"| {parameter} | {'; '.join(effects) or 'None established'} | {retained('numeric_only')} | {retained('verbal_only')} | {sum(w['all_pairs_equivalent'] for w in word)}/3; {sum(w['complete'] for w in word)}/3 complete | {a['active_accuracy']:.0%}; {a['active_p_holm_supplement']:.3f} |")
    lines+=['', 'The exact gradient sensitivity reports endpoint and interior effects separately; a positive endpoint is not a full graded-response pass. All90 response curves, confidence intervals where estimable and all180 paired comparisons are in the machine-readable result. Signs lacking original theoretical predictions remain exploratory.',
        '', 'Retention columns reproduce legacy eligibility and slope-ratio calculations for comparison. Their independent-call fits ignore repeated backgrounds; do not promote these diagnostic flags to new validity passes. Paired effects and original bootstrap diagnostics must be considered together.',
        '', 'Wording tests concern the average difference across50 paired backgrounds at .8, using conservative90% paired intervals and the unchanged +/-0.10 margin. Every one of six wording pairs must establish equivalence for a cell. Both directions of discordance are retained to expose cancellation. This is not per-profile invariance or the original fixed-mean equivalence experiment. Independent original TOST results are retained as a sensitivity.',
        '', 'Audit evidence is the completed separate prior-cohort200-item audit, not a new audit of these responses. It cannot by itself explain this entire new dataset. The original aggregate audit failed; short self-explanations and repeated-background dependence limit recovery claims.',
        '', f"New known usage estimate ${ledger['known_cost_usd']:.6f}; new unknown bound ${ledger['unknown_usage_reserved_usd']:.6f}; cumulative accounted ${ledger['total_accounted_usd']:.6f} under the $25 ceiling. Pending requests: {ledger['pending_requests']}. Provider invoice/balance not verified.",
        '', 'Frozen sources, raw hashes, exact requests, returned IDs, recomputed statistics and archive bytes verified. No off-device backup is claimed. This report records the prespecified calculations; it does not enact a methodological revision or Phase2 release.',
        '', f"[Full result]({paths[0].name}) | [Verification](verification.json) | [Protocol](../PROTOCOL.md) | [Prior audit](../../structural_encoding_20260912/audit_schema_r3/analysis/REPORT.md)",'']
    (root/'analysis/REPORT.md').write_text('\n'.join(lines),encoding='utf-8')
    run.save_new(root/'analysis/verification.json',{'status':'PASS','recorded':len(rows),'all_planned_recorded':result['all_planned_recorded'],
        'unique_provider_ids':len(ids),'raw_requests_and_hashes_verified':True,'terminal_results_recomputed':True,'archive_bytes_verified':True,
        'result_sha256':sha256(paths[0].read_bytes()).hexdigest(),'off_device_backup_verified':False})
    (root/'STATUS.md').write_text(f"# Follow-up status\n\nCollection: {ledger['status']}. {len(rows):,}/{m['design']['planned_calls']:,} responses.\n\nVerification completed; [assessment](analysis/REPORT.md). Phase1.5 remains open.\n",encoding='utf-8')
    # Never include unrelated staged work or commit on a branch switched by the user.
    cwd=run.old.ROOT
    branch=subprocess.check_output(['git','branch','--show-current'],cwd=cwd,text=True).strip()
    staged=subprocess.check_output(['git','diff','--cached','--name-only'],cwd=cwd,text=True).strip()
    if branch=='phase1-5-all-ten-criteria' and not staged:
        targets=[root/'analysis',root/'budget_ledger.json',root/'local_backup.json',root/'STATUS.md']
        subprocess.run(['git','add',*[str(p.relative_to(cwd)) for p in targets]],cwd=cwd,check=True)
        subprocess.run(['git','-c','core.whitespace=blank-at-eol,blank-at-eof,space-before-tab,cr-at-eol','diff','--cached','--check'],cwd=cwd,check=True)
        subprocess.run(['git','-c','user.name=tommypalam','-c','user.email=tpalamenga@gmail.com','commit','-m',
            f"Verify all-ten follow-up: {len(rows)} records, {ledger['status']}; preserve unchanged gate"],cwd=cwd,check=True)
    else:print('Verified files saved; commit deferred because branch/index changed.',flush=True)


def main():
    p=argparse.ArgumentParser();p.add_argument('--wait',action='store_true');args=p.parse_args()
    if args.wait:
        deadline=time.monotonic()+12*3600
        while not ((run.ROOT/'local_backup.json').exists() and (run.ROOT/'budget_ledger.json').exists()):
            if time.monotonic()>deadline:raise TimeoutError('No terminal archive after12 hours; inspect running process; no success claimed')
            time.sleep(30)
    finish()


if __name__=='__main__':main()
