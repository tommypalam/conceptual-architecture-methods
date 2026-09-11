# Focused MoR curve screen

Prepared 2026-09-11 after the complete unblinded MoR audit error review.
Purpose: test whether the grounding candidate preserves response across five
values, alongside the repetition control. This is exploratory development on
known S3, not a holdout, a full sweep, or a phase-validity decision.

- Model: `gpt-5.4-mini-2026-03-17`, temperature 1, output cap 600 tokens.
- Neutral configuration, one parameter (MoR), one dilemma (S3).
- Values .1/.3/.5/.7/.9; all other nine parameters at original source means.
- Two arms: previously approved verbatim repetition and fact-grounding text.
- 30 calls per cell, 10 cells, **300 calls**; root seed **20260917**.
- Thirty shuffled complete ten-cell blocks, concurrency three, independent
  model calls. Shared schedule blocks do not make outcomes statistically paired.
- **$2.40 enforced dispatch cap**; conservative full reservation **$2.0572875**.
  Earlier settled token estimate $1.1531925. Even accumulated conservative
  reservations remain below the previous $9 allowance; top-up not required
  by the dispatch budget. This is not a checked provider account balance.

Exact messages and source hashes are frozen in `manifest.json` and displayed
in `request_preview.json`. System profiles are copied exactly from each
original canonical MoR cell. User messages are copied exactly from the approved
repetition/grounding screen. No new wording, numeric-axis convention, desired
answer, moral scoring rule, or tool invocation is added. Prior endpoints are
not pooled; fresh endpoints make the five-value comparison contemporaneous.
The original canonical curve remains historical context, so this diagnostic
cannot establish a causal advantage over the original arm.

Primary: grounding evaluated with the existing directional sweep rule:
complete allocation, >=98% valid per cell, positive fitted logistic slope
(likelihood-ratio p<.05), endpoint Cohen's h>=.20, monotonic observed rates.
Only this grounding criterion is primary. At N=30, the quality rule requires
30 valid responses per cell. Report cell counts/Wilson intervals, slope and
Wald interval, LR p, h, monotonicity, and estimator failures separately.
Pinned, separated or failed fits do not pass. No new threshold is substituted.

Secondary: the repetition curve and direct grounding-minus-repetition
endpoint-change contrast, using conservative >=95% exact-binomial bounds.
No claim that arms differ merely because their separate tests differ in
significance. Secondary results are not adjusted across a testing family.

Do not expand on the basis of interim outcomes. Stop dispatch on any API,
model, usage, attempt-count or spending failure; retain all records and
pre-call reservations. No automatic retry or in-place replacement of failures.
The frozen evidence-screen transport handles immutable records and backup.
Report verification checks every request/profile, source hash, unique real
API ID, reservation and raw ZIP payload. Same-computer backup only.

If the primary criterion is unmet, do not automatically commission a larger
grounding battery. If met, interpretation, numeric/verbal retention and
paraphrase robustness remain unresolved; select a next diagnostic explicitly.
All five concepts and ten parameters remain in the architecture. Phase 2
remains on hold. Broad renewed spending authority is recorded verbatim in
`dispatch_authorization.json`; preparation does not claim an exact-payload
user signature that has not occurred.
