# Phase 0 — Closure Verdict (2026-07-29)

Phase 0 (0a calibration, 0b harness-neutrality, 0c locked holdout) is COMPLETE.
This document is the formal closure record and the foundation Phase 1 builds on.
Prompts remained FROZEN throughout; no dilemma text was edited at any point.

## The three phases and what each established

- **0a (May 2026, locked):** the six dilemmas are genuine ~50/50 coin-flips under
  the naked prompt. Frozen at `experiments/phase0_baseline_calibration/`.
- **0b (2026-07-28/29):** the Phase-2-style agent-framing harness is NOT
  behaviourally neutral on the current model (gpt-5.4-mini-2026-03-17). Any
  scaffold text collapses S2/C2/C3 toward a pole and marginally biases S1/C1;
  only S3 survives the full harness. Not fixable by template revision. This is a
  substantive methodological finding (protects Phase 2 from a harness confound),
  documented in `phase0b_archive/PHASE0B_RESULT_2026-07-29.md`.
- **0c (2026-07-29):** fresh, hash-locked, no-edit holdout at N=1000 under the
  validated-neutral naked delivery. It caught that four recalibrated splits were
  partly small-N sampling luck. Documented in
  `phase0c_locked_holdout/PHASE0C_RESULT_2026-07-29.md`.

## The locked baselines (Phase 0c, N=1000, naked — the reference for Phase 2)

| prob | opt0 rate | Wilson 95% CI | tier | Phase-2 usability |
|------|-----------|---------------|------|-------------------|
| S3 | 0.54 (ADOPT) | [0.50, 0.57] | balanced | PRIMARY — full headroom |
| S1 | 0.41 (A) | [0.38, 0.44] | near-balanced | PRIMARY — good headroom |
| C1 | 0.72 (PACKAGE_A) | [0.69, 0.75] | off-centre | SECONDARY — moderate headroom |
| C2 | 0.73 (APPROVE) | [0.71, 0.76] | off-centre | SECONDARY — moderate headroom |
| C3 | 0.70 (CONTINUE) | [0.67, 0.73] | off-centre | SECONDARY — moderate headroom |
| S2 | 0.19 (FORMAL_REPORT) | [0.16, 0.21] | near a wall | LOW-POWER — caveated, not load-bearing |

## Closure decision (the "most solid but useful" path)

Requiring a literal 50/50 baseline is neither necessary nor achievable on this
model (0c proved the target moves with sampling and model drift). What Phase 2
needs is a TRUSTWORTHY, PRECISELY-MEASURED baseline per problem, which 0c
provides (each known to ~+/-3% on a locked no-edit sample). Therefore:

1. **Keep all six problems.** Interpret Phase 2 configuration effects RELATIVE to
   the 0c-measured baseline above, not against an idealised 50/50. This extends
   spec §2.2.2's "modest shift -> interpret relative to measured baseline" logic
   to the off-centre problems as well.
2. **Tiering for inference weight:**
   - PRIMARY (S1, S3): near-balanced, full detection power both directions —
     the load-bearing problems for the parameters->behaviour claim.
   - SECONDARY (C1, C2, C3): usable with moderate headroom; parameter effects are
     detectable, with reduced power toward the majority pole. Report with the
     baseline caveat.
   - LOW-POWER (S2): baseline near a wall (0.19); reported for completeness but
     NOT relied on for primary inference. Effects toward LOCAL would be hard to
     detect; effects toward REPORT remain detectable.
3. **No re-recalibration, no descope.** Re-recalibrating chases a luck-driven
   moving target (wasted budget fighting model drift); descoping discards three
   usable problems. The measured-baseline approach is more honest and retains
   scope.

## Documented deviations (flag to supervisor after Phase 0/1 per the standing rule)

- **Recalibrated dilemma set** used for 0b/0c instead of the drifted 0a originals
  (0a frozen and untouched). Justified by measured model drift.
- **0c delivery = naked**, not spec §2.2.1's null_b, because 0b proved null_b/full
  harness collapses the dilemmas and would not validate them. The naked holdout
  serves 0c's actual §11.5 purpose.
- **Measured-baseline interpretation extended to substantial-shift problems**
  (§2.2.2 formally blesses this only for modest shifts; here applied to C1/C2/C3
  with the tiering caveat rather than retiring them).

## Status: PHASE 0 CLOSED. Cleared for Phase 1 (pilot).

Phase 1 (spec Part 3) is an OPERATIONAL pilot: one simple problem, one
configuration, verify the pipeline runs end-to-end (system-prompt assembly, API
infra, paired-agent orchestration, basic graded behaviour). S1 or S3 (PRIMARY
tier) is the natural pilot problem.
