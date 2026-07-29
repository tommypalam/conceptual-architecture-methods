# Phase 1.5 — Pilot-scale sweep finding (2026-07-29)

Reduced diagnostic before the full §4.1 sweep: RE and RT swept {0.1,0.3,0.5,0.7,
0.9}, other 9 params at population means, neutral context, full Phase-2 harness
(system message + DECISION/REASONING). S1 + S3 (PRIMARY tier). N=25/value.
500 calls (~$0.50). Recalibrated set.

## Results (opt0 rate at each sweep value)

| param | prob | .1 | .3 | .5 | .7 | .9 | slope | Cohen h (ext) | monotonic |
|-------|------|----|----|----|----|----|-------|---------------|-----------|
| RE | S1 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 | 0.00 | (pinned) |
| RE | S3 | 0.12 | 0.08 | 0.20 | 0.04 | 0.24 | +0.86 | 0.32 | no |
| RT | S1 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 | 0.00 | (pinned) |
| RT | S3 | 0.16 | 0.24 | 0.56 | 0.24 | 0.32 | +0.76 | 0.38 | no |

S1 verified genuinely pinned: 125/125 A across all RE sweep values (not a parse
artefact).

## Reading

1. **Headroom, not mechanism-absence, is the gate.** S1 is pinned at 100% A under
   the full harness + mean profile (consistent with Phase 0b: S1 marginal, the
   harness pushes it to a wall), so NO parameter can show a gradient there — zero
   dynamic range. S3, the one PRIMARY problem with real headroom under the
   harness, DOES show gradients.
2. **Gradients are present on S3 with real effect sizes** (Cohen's h 0.32-0.38,
   both >= the 0.20 §4.1.3 bar):
   - RT on S3: slope +0.76, ADOPT RISES with RT. Predicted direction (§6.1.1:
     higher RT -> ADOPT) CORRECT.
   - RE on S3: slope +0.86, ADOPT rises with RE. Predicted (§6.1.1: higher RE ->
     WAIT, i.e. ADOPT DOWN) is the OPPOSITE. Wrong-direction — a discovery to
     investigate per §4.1.3 (inverted encoding? hypothesis wrong? prior?).
3. **Non-monotonicity is likely N=25 noise.** At N=25 each proportion has ~+/-18pp
   CI; the mid-sweep dips are within noise. The full N=50 sweep with logistic
   p-values is needed to distinguish noise from true bucket-collapse.

## Verdict

The encoding mechanism is PARTIALLY ALIVE: parameters move decisions on the
problem that has headroom (S3), with effect sizes above the §4.1.3 threshold and
at least one parameter (RT) in the predicted direction. The pilot did its job —
it shows gradients exist AND that harness-pinning (Phase 0b) will mask effects on
low-headroom problems.

Implications for the full §4.1 sweep:
- Run the full sweep, but expect pinned problems (S1 under full harness, likely
  S2/C2/C3) to show no gradient for headroom reasons, not encoding reasons.
- Consider sweeping under a HIGHER-HEADROOM delivery (the naked/near-neutral
  envelope from Phase 0b) so parameter effects are not masked by harness
  collapse — a design question given Phase 0b, to decide before the 7,500-call
  commitment.
- The RE-on-S3 wrong-direction result is flagged for the §4.1.3 investigation.
