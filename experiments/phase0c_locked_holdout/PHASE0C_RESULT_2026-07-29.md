# Phase 0c — Locked Holdout Result (2026-07-29)

## Protocol (as run)

- **Frozen set:** the recalibrated dilemmas at `experiments/phase0b_calibration/
  questions/`, SHA-256 hash-locked in `frozen_prompts/manifest.json`
  (frozen_at 2026-07-29T00:00:00Z). Lock verified intact after the run.
- **Delivery:** naked (no system message; "Reply with only: X or Y") — the
  validated-neutral condition. Deviation from spec §2.2.1's "null_b" is
  deliberate and documented: the Phase 0b finding (PHASE0B_RESULT_2026-07-29.md)
  proved the null_b/full-harness condition collapses S2/C2/C3, so a null_b
  holdout would re-measure the harness, not validate the dilemmas. The naked
  holdout tests 0c's actual purpose (§11.5 multi-iteration false-pass check).
- **N = 1000 per problem**, 6,000 calls, independent 0c seed. No edits permitted.

## Result (spec §2.2.2 tiers)

| prob | split (opt0/opt1) | rate | Wilson 95% CI | tier |
|------|-------------------|------|---------------|------|
| S3 | ADOPT 535 / WAIT 465 | 0.54 | [0.50, 0.57] | MODEST SHIFT (document) |
| S1 | A 413 / B 587 | 0.41 | [0.38, 0.44] | MODEST-OUTER (45-55 excl; within 40-60) |
| S2 | REPORT 187 / LOCAL 813 | 0.19 | [0.16, 0.21] | SUBSTANTIAL (retire) |
| C1 | A 723 / B 277 | 0.72 | [0.69, 0.75] | SUBSTANTIAL (retire) |
| C2 | APPROVE 735 / REJECT 265 | 0.73 | [0.71, 0.76] | SUBSTANTIAL (retire) |
| C3 | CONTINUE 698 / PIVOT 302 | 0.70 | [0.67, 0.73] | SUBSTANTIAL (retire) |

## Interpretation — 0c did its job (§11.5 false-pass check)

At the holdout N=1000, four problems (S2, C1, C2, C3) drift substantially out of
the 40-60 band; S1 sits just inside 40-60 but outside 45-55; only S3 lands
MODEST/near-balanced. Comparison to the recalibration splits (N=300):

| prob | recalib N=300 | holdout N=1000 | direction |
|------|---------------|----------------|-----------|
| S1 | 0.57 | 0.41 | flipped past 50 to the low side |
| S2 | 0.34 | 0.19 | further toward LOCAL |
| S3 | 0.61 | 0.54 | toward 50 (improved) |
| C1 | 0.66 | 0.72 | further toward A |
| C2 | 0.64 | 0.73 | further toward APPROVE |
| C3 | 0.55 | 0.70 | further toward CONTINUE |

The recalibration splits were partly SAMPLING LUCK at small N: the bistability
bar used (minority >=20%) is weak, and at N=1000 the true rates sit outside the
40-60 validation band for four problems. Every drift is in the SAME direction as
the original model-drift the recalibration fought — the nudges reduced the lean
at small N but did not overcome it. This is exactly the multi-iteration
false-pass §11.5 warned about, and Phase 0c caught it before Phase 2.

## Contingency (spec §2.2.3)

">= 3 Phase 0c failures across multiple problems": here four SUBSTANTIAL (S2, C1,
C2, C3). Per §2.2.3, three-or-more failures invokes the Appendix A descope path
(minimum-viable-thesis subset: simple problems plus Milgram and UG only). Note
the failures here are 1 simple (S2) + all 3 complex (C1/C2/C3); S1 marginal, S3
holds. Decision on scope is pending (recorded in session, not resolved here).

## What is NOT in question

- The dilemmas are still valid, balanced NAKED at the sample sizes originally
  used; the issue is that "balanced at N=100-300" did not survive N=1000 for four
  of them — a precision/false-pass problem, not a broken-dilemma problem.
- Prompts remained FROZEN and hash-locked throughout; no dilemma text was edited.
- The lock is intact; re-engineering any retired prompt requires a NEW freeze and
  a fresh Phase 0c for that prompt (spec §2.2.1 no-edit rule).

## Files
- Frozen manifest: frozen_prompts/manifest.json
- Raw records: results/ (6,000 JSON, write-once)
