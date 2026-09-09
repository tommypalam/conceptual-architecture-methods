# Current state and next steps

Updated 2026-09-09. Working branch: `phase1-5-validity`.
This file is the current operational status; historical records are evidence,
not competing task lists.

The user authorised a fresh Phase 1.5 restart on September 9. The active source
is `option_c_20260909_restart`: 15,000 new calls, without reusing the old sample.
See [live restart instructions](docs/phase1_5_restart_20260909.md).

### Active execution

**Latest verified status (after background completion):** the source sweep has
15,000/15,000 valid records, zero API failures. Rotations have 4,500/4,500 records,
4,498 valid parses and two parse failures, zero API failures. Both completed runs
have checksum inventories and local ZIP backups in `output/validity_backups`.
Combined OpenAI token cost is approximately $17.92 before taxes. The independent
Claude audit is now complete in `claude_audit_20260909_brief_r3`: 200 valid coding
records, 2,000 estimates including two abstentions. The user approved optional
concise commentary. The revised prompt requests at most 15 explanatory words;
observed median 21, maximum 66; verbosity did not filter outcomes. All records,
failed attempts and the continuation ledger are preserved and locally backed up.
The audit meets literal numerical thresholds (7 above the 35% criterion, 6 at
least 50%), but no active-parameter permutation diagnostic has p<.05 and every
aggregate accuracy is below its empirical majority baseline. No phase pass is
claimed. See [audit report](experiments/phase1_5_encoding_validity/claude_audit_20260909_brief_r3/analysis/AUDIT_REPORT.md).
Audit token cost across 202 unique attempts: approximately $0.436. The authorised
gradient extension is complete in `gradients_20260909_final`: 15,000 records,
14,998 valid parses, two preserved parsing failures and zero API failures.
Checksums, a verified local ZIP and the updated evidence matrix are saved.
Estimated gradient token cost: $14.54. Two of six eligible comparisons meet
the existing retention criterion (verbal MoR/S3 and numeric PD/S1); no eligible
pair meets it in both representations. PD/S1 remains severely ceiling-limited.
The other 54 comparisons are not assessable under the prespecified source gate.
See the [gradient report](experiments/phase1_5_encoding_validity/gradients_20260909_final/analysis/GRADIENT_REPORT.md).
Terminal job status: `output/validity_gradients_20260909/status.json`.
Earlier audit failures were
preserved separately; the completed audit uses the unchanged 200-item blind pack.
Corrected paraphrases are generated and assistant-reviewed in
`claude_paraphrases_20260909_theory_r5`; exact-template human approval and
the 4,500-call equivalence experiment remain pending as described below.
Earlier progress counts below are historical checkpoints.

**Historical launch notes:** the user instructed rerunning Phase 1.5 from scratch. The source
designation is now `option_c_20260909_restart`, targeting 15,000 fresh calls under
the unchanged scientific design. Claude Haiku 4.5, pinned to
`claude-haiku-4-5-20251001`, is selected for paraphrases and the independent audit.
Both model IDs were accessible. The ten-call checkpoint passed. At the latest
integrity check, 1,795 new records were valid with no API failures, using about
$1.60 in OpenAI tokens. The sweep continues; this count is a dated checkpoint,
not a live total. `output/validity_restart_20260909/status.json` is updated by the
background supervisor (PID 5336 at launch), which waits for source completion
before running 4,500 rotations and the 200-item Claude audit.
The prepared shard below is inactive and will not be used for this restart.

Earlier, the user confirmed that the original raw records are on another computer and
authorised collecting the remainder here for a later merge. The prepared
`option_c_20260909_shard` reserves all 8,640 inventoried keys and schedules only
the 6,360 never-dispatched slots. It has made no API calls. The failed original slot cannot be
identified from the inventory alone and awaits recovery of its original record.
That recovery path requires the original payloads; the fresh restart does not.
See [cross-computer continuation](docs/phase1_5_continuation.md).

## Phase ledger

| Phase | Verified status | Evidence / next dependency |
|---|---|---|
| 0a–0c | Closed, with documented baseline and delivery deviations | [Phase 0 closure](experiments/PHASE0_CLOSURE_2026-07-29.md) |
| 1 | Operational pilot passed, S3 + S2, 100 calls | [Pilot result](experiments/phase1_pilot/PHASE1_PILOT_RESULT_2026-07-29.md) |
| 1.5 | Open; source, rotations, audit and gradients complete; paraphrases pending | [Gradient results](experiments/phase1_5_encoding_validity/gradients_20260909_final/analysis/GRADIENT_REPORT.md), [follow-up implementation](docs/phase1_5_followup.md) |
| 2 | Pending; encoding-validity gate and preregistration required | Paired-agent individual and collective experiments |
| 3 | Pending | Five behavioural benchmark families and contamination diagnostics |
| 4 | Pending | Reviewed moral-coding manual and human validation |
| 5 | Pending | Main inference, dependency/distribution sensitivity, model robustness |
| 6 | Pending | Final reporting, compliance record, open-artifact release |

## Interrupted Option-C experiment

- Run: `experiments/phase1_5_encoding_validity/option_c_20260906_r2`.
- Exact model: `gpt-5.4-mini-2026-03-17`; temperature 1; output cap 600;
  seed 20260604; concurrency 5.
- Target: ten parameters × five values × three simple problems × N=50 ×
  two deliveries = **15,000 calls**.
- Preserved total: **8,640 records**, including one terminal API failure;
  **6,360 planned observations were not dispatched**.
- Stop reason: HTTP 429, `insufficient_quota` / `credit_balance_exhausted`.
  The process exited; it is not running in the background.
- Final partial report: [8,640-record summary](experiments/phase1_5_encoding_validity/option_c_20260906_r2/analysis/summary_562653cd58340299.md).
  Its partial estimates are not a completed sweep verdict.
- Earlier designation `option_c_20260906` contains five invalid-credential
  failures and no model output. Both designations retain the same design hash.

The two arms jointly vary message role and requested output format. The
alternative retains scaffold text; it is not an established neutral treatment.
The stored failures must not be deleted or replaced to make the run resumable.

## Next actions

1. Source sweep, rotations and independent audit are collected and scored. Do
   not rerun these completed samples merely to improve their results.
2. The user explicitly approved the previously blocked thesis disclosure to
   Anthropic. Four preserved Haiku generation/correction calls (r2–r5) produced
   final candidates with no changes to the canonical theory or scaffold.
3. The final three candidates pass structural/lexical checks and assistant
   semantic review. Review the [exact templates](experiments/phase1_5_encoding_validity/claude_paraphrases_20260909_theory_r5/HUMAN_REVIEW.md)
   and [review findings](docs/phase1_5_paraphrase_final_review_20260909.md).
   Human approval against their exact hashes remains required before the
   4,500 paraphrase behaviour calls. All approval fields remain false.
4. Completed runs have checksum inventories and ZIP backups under
   `output/validity_backups` (same machine, not off-device). The old supervisor
   is stopped; do not relaunch it against the obsolete failed audit designation.
5. Review the entire validity battery before authorising Phase 2. A single .8
   rotation does not estimate a gradient; the now-authorised five-value extension
   collected 15,000 calls and is complete. Do not rerun it to improve results.

The final gradient design is frozen in `gradients_20260909_final/manifest.json`.
The user approved its 15,000 calls (estimated $20–$55; actual token estimate
$14.54) and subsequently approved the thesis-containing paraphrase disclosure.
Human semantic approval of the final wording remains pending. The current
[evidence matrix](experiments/phase1_5_encoding_validity/phase_review_20260909/evidence_7c6e7611aaf4b8b2.md)
keeps completed evidence and unresolved criteria distinct; it is not a gate verdict.

## Supervisor handoff

The supervisor can review `code/engine/` and the validity CLI entry points now.
There is no requirement to delay code review until the empirical battery closes.
The latest implementation verification comprises ten sweep tests and nine
follow-up tests, plus the earlier 29 engine checks. Offline verification is
evidence about code, not a scientific phase pass.

Keep the documented RE-on-S3 pilot direction reversal as an open hypothesis
check, not a reason to retune a frozen prompt. LL, CS, and AW lack prespecified
simple-problem directional contrasts; do not manufacture pass/fail directions.

## Retained decisions

The original Phase 0a archive stays immutable. The recalibrated July question set
is the locked working set. The naked holdout replaces the originally planned
null-B holdout, and effects are interpreted against measured baselines with
problem-specific headroom caveats. Phase 1 used S3 plus S2. These are documented
decisions, not unfinished corrections. See the closure records and [decision log](meta.md).
