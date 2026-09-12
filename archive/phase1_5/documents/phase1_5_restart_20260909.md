# Fresh Phase 1.5 restart — September 9

The user authorised a full restart after reviewing recovery options and costs.
Branch: `phase1-5-validity`. No earlier response is reused in the fresh sample.
Phases 0 and 1 remain closed; this instruction restarts Phase 1.5 only.

**Current status:** source and rotations are complete. The original supervisor
exited after a strict-format audit failure. The user then approved brief optional
commentary; the completed effective audit is `claude_audit_20260909_brief_r3`.
See its [report](../experiments/phase1_5_encoding_validity/claude_audit_20260909_brief_r3/analysis/AUDIT_REPORT.md)
and [NEXT_STEPS](../NEXT_STEPS.md). Do not relaunch the old supervisor against the
failed audit designation. The launch details below are historical provenance.

## Execution

- Source: `experiments/phase1_5_encoding_validity/option_c_20260909_restart`.
- Snapshot: `gpt-5.4-mini-2026-03-17`, temperature 1, output cap 600.
- Neutral context; ten parameters × five values × three problems × 50 calls ×
  two deliveries = 15,000 calls; root seed 20260604; concurrency five.
- Same frozen design hash as the earlier source, new run designation and dates.
- Ten-call checkpoint: ten valid responses, exact snapshot, no API failures;
  8,959 input tokens and 499 output tokens, approximately $0.00896 at list price.
- Later verified checkpoint: 1,795 valid records, no API failures, approximately
  $1.60 in tokens. Collection continues; check live status for current counts.

Claude selection is pinned to `claude-haiku-4-5-20251001`, an approximate
lightweight/high-throughput tier match, not evidence of equivalent capability.
Both models' access was verified. Credentials are loaded from Windows user
environment variables, never written into project source or command arguments.

`code/run_validity_restart_followups.py` runs as a hidden background supervisor,
PID 5336 at launch. It waits for complete, unique source observations with valid
hashes and the exact model identity. Then it launches the 4,500-call
numeric/verbal/hybrid rotations and 200-item independent Claude audit, with
operational checkpoints. It stops dependent dispatch on failures. An OS-held
execution lock prevents duplicate supervisors. It stops waiting if the source
makes no progress for 15 minutes.

Status and logs: `output/validity_restart_20260909/`. Inspect `status.json`,
`pipeline.log`, `pipeline_errors.log` and per-stage logs. These are local files.
Do not launch another source process while the current source is active.

## Paraphrases

The first Claude generation is preserved in
`claude_paraphrases_20260909_restart/records/generation.json`. It returned the
right model but violated fixed labels. A mechanically restored review copy
passed structural/lexical checks, but all three candidates were rejected in an
assistant theory review for semantic drift. See
[the findings](phase1_5_paraphrase_review_20260909.md).

The corrected generation request under `claude_paraphrases_20260909_theory_r2`
is prepared but unsent. Automatic approval review rejected sending private
thesis section 3.1 and theory-derived feedback to Anthropic without explicit
disclosure approval. The user has been asked. Do not indirectly execute or
otherwise bypass that rejection.

The supervisor reads that corrected run's `paraphrases_for_review.json` only
after rotations/audit finish, and dispatches the 4,500 paraphrase calls only if
the existing validator finds three exact hashes with actual human approvals.
Assistant review is not recorded as human approval. If reviews are unavailable,
the supervisor records `waiting_for_human_paraphrase_review` and exits safely.

## Records and limits

Every response is saved immediately in its run's ignored `records/` directory.
Completed runs receive checksum inventories and token-usage totals plus tested
ZIP archives under `output/validity_backups`. Those archives are on the same
computer; Git pushes do not back up raw responses and no off-device backup is
claimed. The original sample remains separate historical evidence.

The optional 15,000-call gradient extension is not queued. The current single
rotation does not establish a within-parameter gradient. Collection completion
does not automatically close Phase 1.5: combined scientific review and any
unassessable criteria must be reported explicitly.

Verification: 19 existing validity tests, four continuation tests, and three
restart-tool tests passed. New checks cover complete-source gating, source
failure rejection, archive byte preservation, token accounting, and exact
preservation of all non-endpoint template text. Frozen source files unchanged.
