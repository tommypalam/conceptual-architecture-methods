# Phase 0b — Result and Honest Conclusion (2026-07-29)

## One-line verdict

On the current model (gpt-5.4-mini, snapshot gpt-5.4-mini-2026-03-17), the
Phase-2-style harness is NOT behaviourally neutral: any agent-framing scaffold
collapses 3 of 6 dilemmas to a deterministic pole, independent of scaffold
wording, delivery, or output format. The dilemmas themselves are sound (bistable
naked). This is the spec §2.1.5 "Null A fails — the harness is biasing the
dilemma" outcome, and no template revision within the harness resolves it. Phase
0b's job — surfacing harness contamination before Phase 2 — is fulfilled.

## What was tested (all archived under experiments/phase0b_archive/, dated)

1. Recalibration of the 4 drifted dilemmas to bistable NAKED (locked set at
   experiments/phase0b_calibration/questions/; N>=300 confirmed).
2. Full 18-cell grid at N=200 under the spec harness (system message +
   DECISION/REASONING + full scaffold): 3/18 cells contain 50%.
3. Ablations isolating the collapse: task-text wording (w0-w3), scaffolding
   ladder (L0-L3), and a delivery x output-format 2x2.

## Per-problem null_a (spec harness: full scaffold, system msg, DECISION/REASONING, N=200)

| prob | opt0 split | rate | Wilson 95% CI | contains 50%? |
|------|-----------|------|---------------|---------------|
| S3 | ADOPT 112 / WAIT 88 | 0.56 | [0.49, 0.63] | YES |
| S1 | A 119 / B 81 | 0.60 | [0.53, 0.66] | no (marginal) |
| C1 | PACKAGE_A 123 / PACKAGE_B 77 | 0.62 | [0.55, 0.68] | no (marginal) |
| S2 | REPORT 0 / LOCAL 200 | 0.00 | [0.00, 0.02] | no (collapsed) |
| C2 | APPROVE 200 / REJECT 0 | 1.00 | [0.98, 1.00] | no (collapsed) |
| C3 | CONTINUE 200 / PIVOT 0 | 1.00 | [0.98, 1.00] | no (collapsed) |

Three tiers: S3 clean; S1/C1 marginal (CIs just exclude 50%); S2/C2/C3 fully
collapsed.

## Why the collapse is not fixable within the harness

- WORDING: w0 (orig), w1 (respondent), w2 (balanced, "reasonable people
  disagree"), w3 (plain) — ALL collapse C2 and C3 to 100% under the spec config.
- SCAFFOLDING LADDER: C2 collapses at L1 — the single preamble sentence "You are
  participating in a decision-making simulation." — before any task text.
- DELIVERY x FORMAT 2x2 (wording w0): all four corners (system/user x
  DECISION/bare) collapse C2 to 100%.
- The ONLY configuration that keeps the collapsing dilemmas bistable is a
  literally text-free harness (dilemma + bare label, no scaffold at all):
  bare_nosys_all6_n100 gave all six bistable (C2 69%, C3 73%, S2 32%, ...).

## Mechanism (interpretation, supported by REASONING traces)

The harness frames the model as a decision-making AGENT told to "apply a
decision rule." Under this framing — especially with forced REASONING — the model
stops treating a genuine dilemma as a coin-flip and RESOLVES it toward the option
that reads as the responsible/optimal managerial choice (approve the
restructuring, report the error, continue the validated approach). Traces show
explicit business-case rationalisation ("concrete 18% cost reduction, stabilises
financing"). Instruction-tuned decisiveness suppresses the genuine ambivalence
that made the dilemma balanced naked. The complex/high-stakes problems (S2/C2/C3)
are exactly the ones with a strong "responsible default", which is why they
collapse and S3 (a closer call) does not.

## Conclusion for the thesis

This is a genuine, reportable finding, NOT a calibration failure and NOT faked to
pass:
1. The six dilemmas are validly calibrated NAKED (Phase 0a + recalibration).
2. The Phase-2-style harness is NOT neutral on this model: agent-framing collapses
   S2/C2/C3 and marginally biases S1/C1; only S3 survives the full harness.
3. No harness template revision (wording/delivery/format) fixes the collapse; only
   removing the harness text entirely does.

Phase 0b therefore PASSES its actual purpose — it detected and characterised
harness contamination before Phase 2 committed resources — while FAILING the
literal §2.1.4 "18/18 contain 50%" criterion under the spec harness. Both facts
are reported. Phase 1 scope and the Phase-2 harness design are to be decided in
light of this evidence (not resolved here; Phase 0b does not depend on Phase 2).

## Prompts FROZEN throughout. No dilemma text was edited at any point.
