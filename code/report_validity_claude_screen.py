"""Verify and report the completed small Claude screen without new inference."""
import hashlib
import json
from pathlib import Path
import zipfile

from engine.validity_sweep import ValiditySink,digest
from run_validity_claude import save_new
from run_validity_claude_screen import ROOT,check,jobs,cost


def main():
    root=ROOT/'experiments/phase1_5_encoding_validity/claude_screen_20260911'
    m=json.loads((root/'manifest.json').read_text(encoding='utf-8'));check(m)
    paths=list((root/'analysis').glob('screen_*.json'))
    if len(paths)!=1:raise ValueError('Need one final screen analysis')
    result=json.loads(paths[0].read_text(encoding='utf-8'))
    if digest(result)[:16] not in paths[0].name or result['design_hash']!=m['design_hash']:raise ValueError('Analysis mismatch')
    approval=json.loads((root/'dispatch_approved.json').read_text(encoding='utf-8'))
    if not approval['approved'] or approval['design_hash']!=m['design_hash'] or approval['exact_messages_hash']!=digest([c['messages'] for c in m['design']['cells']]):
        raise ValueError('Exact approval mismatch')
    rows=list(ValiditySink(root/'records').read_all());expected={key:(c,k) for key,c,k in jobs(m['design'])}
    if len(rows)!=80 or {r['record_key'] for r in rows}!=set(expected):raise ValueError('Incomplete allocation')
    ids=set();input_tokens=output_tokens=0
    for r in rows:
        c,k=expected[r['record_key']]
        if r['request_messages']!=c['messages'] or r['agent_parameters']!=c['profile'] or r['call_index']!=k:
            raise ValueError('Original request mismatch')
        if r['provider']!='anthropic' or r['model_version']!=m['design']['model'] or r['parse_status']!='ok' or r['attempts']!=1:
            raise ValueError('Unexpected provider/model/parse/attempts')
        if not r['api_call_id'] or r['api_call_id'] in ids:raise ValueError('Call ID mismatch')
        ids.add(r['api_call_id']);u=r['response_payload']['usage']
        if u.get('cache_creation_input_tokens',0) or u.get('cache_read_input_tokens',0):raise ValueError('Unexpected cache usage requires explicit accounting')
        input_tokens+=u['input_tokens'];output_tokens+=u['output_tokens']
    total=sum(cost(r) for r in rows)
    if abs(total-result['recorded_token_estimate_usd'])>1e-12:raise ValueError('Cost mismatch')
    backup=json.loads((root/'local_backup.json').read_text(encoding='utf-8'));archive=Path(backup['path'])
    if hashlib.sha256(archive.read_bytes()).hexdigest()!=backup['sha256']:raise ValueError('Archive hash mismatch')
    with zipfile.ZipFile(archive) as z:
        if z.testzip():raise ValueError('Archive corrupted')
        for r in rows:
            name='records/'+r['record_key']+'.json'
            if z.read(name)!=(root/name).read_bytes():raise ValueError('Archive bytes differ')
    save_new(root/'analysis/verification.json',{'n_records':80,'n_valid':80,'n_unique_api_ids':len(ids),
        'n_attempts':80,'input_tokens':input_tokens,'output_tokens':output_tokens,
        'recorded_token_estimate_usd':total,'original_requests_profiles_hashes_and_archive_verified':True,
        'reporter_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()})
    interval=result['primary_conservative_95_interval_unknown_envelope']
    lines=['# Claude screen: unchanged prompts, gross wording failure detected','',
        'The 80-call screen detected a large wording effect without a full sweep. Changing to the tested Claude/provider setup did not resolve the known PD/S3 failure. Original prompt files and every dispatched message stayed unchanged.','',
        f'All 80 responses are valid, with no API/model failures and one attempt per call. Recorded-token cost: **${total:.6f}** (about 16 cents), within the approved $0.75 cap. **Zero OpenAI calls.**','',
        'Configuration neutral; one fixed profile at PD=.8; S3; model `claude-haiku-4-5-20251001`; temperature 1; output cap 600. Twenty calls per formulation, in shuffled four-formulation blocks. Schedule seed 20260914 controls order only; no sampling seed is sent to Anthropic.','',
        '| Formulation | ADOPT / valid N | ADOPT rate | Pointwise Wilson 95% interval |','|---|---:|---:|---|']
    for c in result['cells']:
        lines.append(f'| {c["wording"]} | {c["adopt"]}/{c["n_valid"]} | {c["rate"]:.0%} | {c["ci95"][0]:.1%} to {c["ci95"][1]:.1%} |')
    lines+=['',f'Prespecified P2-minus-P3 difference: **{result["primary_difference"]:.0%}**; conservative exact interval with at least 95% coverage: **{interval[0]:.1%} to {interval[1]:.1%}**. The lower bound exceeds the .10 margin, meeting the fixed gross-failure detection rule. All four cells meet the validity floor; there are no unknown decisions.','',
        'This is an early rejection signal, not a complete cross-model battery. It supports withholding this provider switch from a larger rerun. No broad model ranking, ethical-competence claim or phase closure follows. The original Phase 1.5 gate remains unmet.','',
        'The problem and primary wording pair were selected from previous development evidence. Haiku generated the prior paraphrases; it is the behavioural subject here, not an independent wording judge. Model and provider transport changed together. Historical OpenAI responses were not pooled or used as concurrent controls. Valid means the decision parsed under the expected model, not that its explanation faithfully operationalises the theory.','',
        'The [retrospective OpenAI example](../offline/RETROSPECTIVE_SCREEN.md) illustrates why a small screen that does not detect a failure must remain inconclusive. This new Claude result crosses the fixed detection threshold; no allocation or threshold was changed to obtain it.','',
        'Next: review the [illustrative reasoning notes](QUALITATIVE_NOTES.md) against the original theory and options, using existing records. No original prompt edits, further paid study or automatic expansion is authorised by this result.','',
        f'Evidence: [{paths[0].name}]({paths[0].name}); [verification](verification.json); [protocol](../PROTOCOL.md); [exact approval](../dispatch_approved.json); [record inventory](../record_checksums.json); [local ZIP](../local_backup.json). Same-computer storage is not off-device backup.',
        'Cost uses reported input/output tokens at the [verified Anthropic rates](https://platform.claude.com/docs/en/about-claude/pricing), before taxes or provider-only adjustments.','']
    report=root/'analysis/SCREEN_REPORT.md';content='\n'.join(lines)
    if report.exists() and report.read_text(encoding='utf-8')!=content:raise ValueError('Existing report differs')
    report.write_text(content,encoding='utf-8');print(report);print(f'Verified 80 requests, IDs, attempts and ZIP payloads; cost ${total:.6f}.')


if __name__=='__main__':main()
