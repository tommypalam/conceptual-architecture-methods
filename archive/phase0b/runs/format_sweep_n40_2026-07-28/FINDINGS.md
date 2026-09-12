# Phase 0b — Output-format breadth sweep (null_a, N=40, 2026-07-28)

5 format variants x {S2, C2, C3} (the format-fragile trio) x N=40, empty harness
(null_a), recalibrated dilemmas, prompts FROZEN. All 600 calls parsed (bare
variants parse as `ambiguous` = a valid recovered label; zero failures).

## Distance from 0.50 (lower = more balanced; 0.50 = collapsed to a pole)

| variant | C2 | C3 | S2 | mean |
|---------|----|----|----|------|
| canonical | 0.50 | 0.50 | 0.50 | 0.500 |
| decision_only | 0.50 | 0.50 | 0.50 | 0.500 |
| reasoning_first | 0.50 | 0.50 | 0.50 | 0.500 |
| bare_label | 0.50 | 0.42 | 0.42 | 0.450 |
| **bare_nosys** | **0.28** | **0.23** | **0.38** | **0.292** |

## Actual rates vs naked (opt0 = FORMAL_REPORT / APPROVE / CONTINUE)

bare_nosys (no system message + "Reply with only: X or Y"):
- C2: 78% (minority 22%) BISTABLE   [naked 64%]
- C3: 72% (minority 28%) BISTABLE   [naked 55%]
- S2: 12% still collapsed           [naked 34%]

bare_label (bare output but system message KEPT):
- C2: 100% collapsed; C3: 93%; S2: 7%. Barely helps -> the system message
  itself is part of C2's collapse, not just the DECISION token.

## Reading

- Only `bare_nosys` (the full naked envelope: no system message + bare label)
  moves the fragile problems off the pole. Removing reasoning (decision_only) or
  reordering (reasoning_first) does nothing.
- bare_nosys recovers 2/3: C2 and C3 become bistable. S2 stays collapsed (and
  even overshoots its own naked 34% toward LOCAL).
- Even for C2/C3, bare_nosys does not perfectly reproduce the naked split
  (78 vs 64, 72 vs 55) — shifted ~14-17pp toward the pole. N=40 CIs are wide
  (~+/-15pp), so part is noise, but the direction is consistent: a system-message
  harness, even empty, biases relative to the true naked measurement.

## Implication for the harness design

The closest-to-neutral Phase-0b delivery is the naked envelope (no system
message, bare label). It rescues C2/C3 but not S2. S2 remains the single most
harness-fragile problem, resistant to the format fix.

Next: confirm bare_nosys at higher N on the fragile trio; and separately decide
S2's fate (drop from the null-neutral set, or accept it as characterised
harness-fragile).

## Prompts FROZEN. No dilemma text edited.
