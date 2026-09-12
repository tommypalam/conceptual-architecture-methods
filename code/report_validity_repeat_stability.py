"""Report the complete offline repeat-stability family and fixed reference prompts."""
import json
from pathlib import Path
from hashlib import sha256
from run_validity_claude import save_new
import audit_validity_repeat_stability as audit


def main():
    root=audit.OUT;r=json.loads((root/'results.json').read_bytes())
    pairs=r['between_run_comparisons'];within=r['within_run_halves']
    lines=['# Offline repeated-prompt stability audit','',
        f"**{r['valid_records']:,} valid records**, {len(r['scope'])} source studies; **$0 new API spending**.",
        f"{r['repeated_prompt_groups']} exact-prompt/settings groups recur with N>=20 in at least two runs.",
        f"**{r['between_run_detections']}/{len(pairs)} between-run comparisons** differ after Holm correction; **{r['within_run_detections']}/{len(within)} chronological-halves checks** differ in their separate Holm family.",
        'These are exploratory diagnostics, not encoding-validity passes. Non-detection is not equivalence.', '',
        '## Fixed reference prompts','',
        'Canonical MS/S2 and MoR/S3 endpoints selected in the protocol before this audit. Rates count FORMAL_REPORT for MS and ADOPT for MoR. All matching run summaries shown; seeds may differ.', '',
        '| Parameter/value | Run | First-option count | Wilson 95% CI | Earliest UTC |',
        '|---|---|---:|---|---|']
    for a in r['anchors']:
        for s in a['runs']:
            lo,hi=s['wilson95']
            lines.append(f"| {a['parameter']} {a['value']} | {s['run']} | {s['first_count']}/{s['n']} | [{lo:.3f}, {hi:.3f}] | {s['start']} |")
    lines+=['','## Largest observed shifts','',
        'The twelve largest absolute differences, selected descriptively after analysis. The JSON retains every comparison, including all non-detections. Later minus earlier; intervals are conservative nominal95, not family-adjusted.', '',
        '| Problem / prompt hash prefix | Earlier run: count/N | Later run: count/N | Difference | Nominal conservative 95% CI | Holm p |',
        '|---|---|---|---:|---|---:|']
    for p in sorted(pairs,key=lambda p:abs(p['effect']['difference']),reverse=True)[:12]:
        lo,hi=p['effect']['conservative_95_interval_unknown_envelope']
        lines.append(f"| {p['problem']} / {p['prompt_key'][:12]} | {p['earlier']}: {p['earlier_count']}/{p['earlier_n']} | {p['later']}: {p['later_count']}/{p['later_n']} | {p['effect']['difference']:+.3f} | [{lo:+.3f}, {hi:+.3f}] | {p['holm_p']:.5g} |")
    lines+=['','## Inventory and exclusions','',
        '| Source | Archived files | Valid retained | Invalid/failure | Different tool protocol | Successful multi-attempt records |',
        '|---|---:|---:|---:|---:|---:|']
    for s in r['scope']:
        lines.append(f"| {s['run']} | {s['files']} | {s.get('valid_retained',0)} | {s.get('excluded_invalid_or_failure',0)} | {s.get('excluded_tool_protocol_calls',0)} | {s.get('successful_records_with_multiple_attempts',0)} |")
    lines+=['',f"Unique retained API IDs: {r['unique_api_ids']:,}. Same-prompt/same-seed repeated groups: {len(r['same_prompt_and_seed_repeats'])}. Backend fingerprint counts: {r['fingerprints']}.", '',
        '## Interpretation boundaries','',r['limits'],
        'Full per-run summaries retain profile hashes, token/cache metadata, backend fingerprints, response-text uniqueness and chronological halves. Identical text is not proof of copied responses or dependent calls; these are indicators for further investigation.',
        'Archived records were read from checksum-verified ZIPs. Current filename inventories and manifest bytes match archives; each archived record hash and each manifest design hash verified. This audit does not claim a fresh byte comparison against every current loose record. Payload text and recorded decisions reparse consistently under their original parser. Legacy bare-label responses retain their original scoring; API failures retain explicit exclusions.',
        'Older successful multi-attempt records are counted, not silently removed. Assembled recovery allocations included once; prior copies and independent Claude studies excluded by declared scope. Historical September6 responses remain separate. No new retries, paid calls or raw-data edits.',
        'All per-record checksums/normalized metadata are preserved locally in record_index.json and the audit ZIP. Original gate unchanged; Phase1.5 open, Phase2 held. Spending balance remains $3.79170675, provider balance unverified.', '',
        '[Complete results](results.json) | [Protocol](PROTOCOL.md)', '']
    target=root/'REPORT.md'
    if target.exists():raise ValueError('Preserve existing report')
    target.write_text('\n'.join(lines),encoding='utf-8')
    save_new(root/'report_provenance.json',{'results_sha256':sha256((root/'results.json').read_bytes()).hexdigest(),
        'script_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),'report_sha256':sha256(target.read_bytes()).hexdigest()})


if __name__=='__main__':main()
