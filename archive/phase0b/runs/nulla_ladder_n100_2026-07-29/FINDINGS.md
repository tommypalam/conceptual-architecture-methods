# Phase 0b — null_a scaffolding ladder (N=100, 2026-07-29)

Additive scaffolding ladder x {C2, C3} x N=100, neutral envelope (user_prefix +
bare_label, max_tokens 30). Each level adds ONE piece to the fully-naked base.
Recalibrated dilemmas. Prompts FROZEN. (Runner "ok 0" = all parsed as `ambiguous`
bare labels, which the scorer counts — not failures.)

## Results (opt0 rate; bistable = minority >= 20%)

| level | added piece | C2 | C3 |
|-------|-------------|----|----|
| L0_naked | (nothing — dilemma + bare label only) | 0.71 BISTABLE | 0.67 BISTABLE |
| L1_preamble | "You are participating in a decision-making simulation." | 0.96 collapse | 0.69 BISTABLE |
| L2_task | + "# Your task … consider … choose one option …" | 0.94 collapse | 0.99 collapse |
| L3_identity | + "Do not infer demographic identity …" | 1.00 collapse | 0.56 BISTABLE |

## Finding: C2 collapses at L1 — the PREAMBLE SENTENCE ALONE

Adding only "You are participating in a decision-making simulation." takes C2
from 71% (bistable) to 96% (collapsed). No task text, no identity clause — just
that one framing sentence. So for C2 there is NO scaffolding middle ground: any
preamble collapses it.

C3 is non-monotonic (tolerates L1 and L3, breaks at L2) — consistent with its
known steep/idiosyncratic surface — but C2 is the binding constraint.

## Conclusion (final for the null_a design)

The ONLY null_a configuration neutral across all six problems is **L0 — fully
naked**: dilemma + "Reply with only: X or Y", with NO preamble and NO task block.
The "decision-making simulation" framing sentence is itself a collapsing cue for
C2. Confirmed consistent with bare_nosys_all6_n100 (all six bistable naked).

## Forced design implication

null_a's neutrality is only achievable fully-naked. The preamble + task block
(which Phase 2 uses to introduce the profile) is a measurable behavioural cue,
not inert scaffolding. Therefore the Phase-0b neutrality guarantee and the
Phase-2 harness structure cannot both use the "simulation / # Your task"
framing if absolute per-cell neutrality is required. Decision options recorded
in the session; leading candidate: adopt L0-naked null_a as the neutrality
baseline and treat null_b/null_c (which necessarily carry a profile) on a
CONTRAST basis (do they move the split relative to L0 in hypothesized
directions?) rather than requiring each to sit at 50/50.

## Prompts FROZEN. No dilemma text edited.
