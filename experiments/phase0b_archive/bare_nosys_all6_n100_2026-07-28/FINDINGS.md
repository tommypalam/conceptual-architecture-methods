# Phase 0b — Naked-envelope delivery, all six problems (null_a, N=100, 2026-07-28)

bare_nosys framing (NO system message + "Reply with only: X or Y" bare label)
x all 6 problems x N=100, empty harness (null_a), recalibrated dilemmas.
Prompts FROZEN. All 600 calls parsed (bare label = `ambiguous`, valid).

## Result: ALL SIX BISTABLE (minority >= 20%), splits track the naked ground truth

| prob | naked-envelope split | rate | naked truth | minority | Wilson CI | bistable |
|------|----------------------|------|-------------|----------|-----------|----------|
| S1 | A 60 / B 40 | 0.60 | 0.57 | 40% | [0.50,0.69] | YES |
| S2 | REPORT 32 / LOCAL 68 | 0.32 | 0.34 | 32% | [0.24,0.42] | YES |
| S3 | ADOPT 60 / WAIT 40 | 0.60 | 0.61 | 40% | [0.50,0.69] | YES |
| C1 | A 49 / B 51 | 0.49 | 0.66 | 49% | [0.39,0.59] | YES |
| C2 | APPROVE 69 / REJECT 31 | 0.69 | 0.64 | 31% | [0.59,0.77] | YES |
| C3 | CONTINUE 73 / PIVOT 27 | 0.73 | 0.55 | 27% | [0.64,0.81] | YES |

## Conclusion

The canonical Phase-0b harness (system message + `DECISION: [X | Y]` + REASONING,
max_tokens 600) is what collapsed the dilemmas in the N=200 grid (3/18 balanced).
The naked-envelope delivery (no system message, bare label) restores ALL SIX to
their bistable naked splits under the empty harness. The splits closely track the
naked ground truth (S2 0.32 vs 0.34, S3 0.60 vs 0.61, S1 0.60 vs 0.57, C2 0.69 vs
0.64); C1 and C3 differ more but remain comfortably bistable.

The earlier N=40 sweep showing S2 collapsed at 12% was sampling noise; at N=100
S2 lands on its naked value (32%).

## What this fixes and what it does NOT

- FIXES Finding 1 (the output-format scaffold collapse), completely, for null_a.
- Does NOT by itself address Finding 2 (null_b "neutral means" and null_c "sham"
  profiles were not behaviourally neutral in the N=200 grid). Those conditions
  carry a system-message profile by construction; the naked-envelope result here
  is null_a (empty harness) only. The next step is to re-run null_b/null_c under
  the naked-envelope delivery and see whether the profile bias persists when the
  profile is delivered in the bare envelope rather than as a DECISION-format
  system message.

## Prompts FROZEN. No dilemma text edited.
