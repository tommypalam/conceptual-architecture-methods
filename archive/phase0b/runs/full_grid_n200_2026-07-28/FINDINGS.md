# Phase 0b — Definitive 18-cell grid (N=200, recalibrated set, 2026-07-28)

3 null conditions x 6 problems x N=200. Current canonical harness (system
message + `DECISION: [X | Y]` + REASONING, max_tokens 600). Recalibrated
(bistable-naked) dilemmas. Prompts FROZEN.

OVERALL: 3/18 cells balanced (Wilson 95% CI contains 50%).

## opt0 rate per cell (opt0 = A / FORMAL_REPORT / ADOPT / PACKAGE_A / APPROVE / CONTINUE)

| prob | naked | null_a | null_b | null_c |
|------|-------|--------|--------|--------|
| S1 | 0.57 | 0.59 | 1.00 | 0.89 |
| S2 | 0.34 | 0.00 | 0.04 | 0.09 |
| S3 | 0.61 | 0.56 | 0.49 | 0.86 |
| C1 | 0.66 | 0.61 | 0.71 | 0.53 |
| C2 | 0.64 | 1.00 | 0.00 | 0.96 |
| C3 | 0.55 | 1.00 | 0.96 | 0.80 |

Balanced cells (PASS): null_a/S3, null_b/S3, null_c/C1.

## Decomposition — two separable, independently measured harness effects

### Finding 1: the output-FORMAT scaffold collapses some dilemmas
Measured as |null_a - naked|. null_a is the EMPTY harness (no profile content),
so any deviation from the naked split is caused by the format/framing scaffold
alone (`DECISION: [X | Y]` + REASONING).

- Format-robust (deviation <= 0.05): S1 (0.03), S3 (0.05), C1 (0.05)
- Format-fragile (collapses to a pole): S2 (0.34), C2 (0.36), C3 (0.45)

### Finding 2: the "null" PROFILES are not behaviourally neutral
Measured as |null_b - null_a| and |null_c - null_a|. A neutral profile should
leave the split at its null_a (empty-harness) value. It does not:

- S1: null_b moves it 0.41, null_c 0.30 (a robust dilemma driven to ~100% A)
- C2: null_b moves it 1.00 (APPROVE -> REJECT, a complete flip)
- S3: null_c moves it 0.30
- C3: null_c moves it 0.20

null_b (population means at neutral config) and null_c (sham profile) each impose
their own directional bias on top of the format effect.

## Interpretation (a real result, not a calibration failure)

On the current model (gpt-5.4-mini-2026-03-17), the Phase-0b null harness is NOT
behaviourally neutral. Two distinct confounds are present and measured:
1. the structured output format over-determines format-fragile dilemmas even
   with an empty profile;
2. the "neutral" parameter profiles themselves steer the decision.

This is precisely the confound Phase 0b exists to detect before Phase 2. Three
problems (S1, S3, C1) are format-robust; the profiles still bias them, so no
problem is fully condition-invariant under the current harness.

## Data quality note
Non-trivial unparsed/api/refusal counts in null_b/null_c cells (5-17 per cell),
likely max_tokens/format interactions at N=200. Rates above are over parsed
decisions (n_ok). Worth checking if a format change is pursued.

## Prompts FROZEN throughout. No dilemma text was edited for this grid.
