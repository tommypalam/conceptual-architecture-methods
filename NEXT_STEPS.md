# Current state and next steps

Updated 2026-09-06. Working branch: `phase1-5-validity`.
This file is the current operational status; historical records are evidence,
not competing task lists.

## Phase ledger

| Phase | Verified status | Evidence / next dependency |
|---|---|---|
| 0a–0c | Closed, with documented baseline and delivery deviations | [Phase 0 closure](experiments/PHASE0_CLOSURE_2026-07-29.md) |
| 1 | Operational pilot passed, S3 + S2, 100 calls | [Pilot result](experiments/phase1_pilot/PHASE1_PILOT_RESULT_2026-07-29.md) |
| 1.5 | Open; September sweep interrupted; follow-up tools offline-tested | [Execution protocol](docs/phase1_5_execution.md), [follow-up implementation](docs/phase1_5_followup.md) |
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

1. Restore API credit availability outside the repository. Before further calls,
   record a continuation/restart designation and how the interrupted sample will
   be handled. The existing runner intentionally refuses to resume across a
   terminal failure. A credit top-up alone does not resolve that provenance step.
   Preserve the snapshot, prompts, sample target, and all prior records.
2. Configure and verify `ANTHROPIC_API_KEY` outside chat/source. The user selected
   Claude for independent coding and paraphrase generation. At the last check the
   Windows User key was absent. Verify an explicit available Claude model ID;
   install its optional SDK in the project environment before real calls.
3. Generate three paraphrases, then obtain actual human semantic review of the
   exact template hashes. No generated paraphrase or human approval exists yet.
4. After the source sweep is complete under a documented protocol, prepare the
   blind 200-item reasoning audit and run the robustness comparisons. The
   six-level verbal mapping, equivalence tests, audit sampling, and prevalence
   caveats are fixed in the follow-up document.
5. Review the entire validity battery before authorising Phase 2. A single .8
   rotation does not estimate a gradient; the optional five-value extension adds
   15,000 calls and needs a deliberate execution/budget decision.

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
