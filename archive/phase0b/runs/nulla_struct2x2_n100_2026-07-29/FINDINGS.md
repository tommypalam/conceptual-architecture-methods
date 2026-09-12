# Phase 0b — null_a structural 2x2 (+ wording sweep), N=100, 2026-07-29

Goal: with spec fidelity, find the LEAST deviation from the spec's null_a
(system message + DECISION/REASONING + full scaffold text) that restores C2/C3 to
Wilson-CI-contains-50%. Wording held at w0 (spec original) for the 2x2.
Recalibrated dilemmas, prompts FROZEN.

## Wording sweep (system message + DECISION/REASONING, vary preamble/task wording)

w0_orig / w1_respondent / w2_balanced / w3_plain — ALL collapse C2 AND C3 to 100%.
=> Wording does not help under the spec-faithful config.

## Structural 2x2 (wording=w0; vary delivery x output format)

| corner | delivery | output | C2 | C3 |
|--------|----------|--------|----|----|
| sys_decision (spec) | system msg | DECISION+REASONING | 1.00 | 0.99 |
| sys_bare | system msg | bare label | 1.00 | 0.90 |
| user_decision | user prefix | DECISION+REASONING | 1.00 | 1.00 |
| user_bare | user prefix | bare label | 1.00 | 0.97 |

ALL FOUR corners collapse C2 to 100%. C3 collapses in all four too.

## Contradiction resolved

Earlier bare_nosys_all6_n100 measured a user_bare-style C2 at 69% (bistable).
Diff: that run had system_prompt = None (dilemma ONLY). This 2x2's user_bare
still PREPENDS the w0 scaffold text to the user turn. So the difference is the
PRESENCE of scaffold text, not delivery or format.

## Conclusion (C2 investigation exhausted)

Every C2 measurement:
- dilemma only, NO scaffold text (bare_nosys): 69% BISTABLE
- ANY scaffold text (w0-w3), ANY delivery, ANY output format: 100% collapsed
- even the single L1 preamble sentence alone: 96% collapsed

=> For C2 on this model, the mere PRESENCE of any "you are an agent / your task"
harness framing — even one neutral sentence — collapses it to 100% APPROVE. Only
a literally text-free harness preserves the coin-flip. This is not fixable by
wording, delivery, or output format. It is a property of C2 x this model:
the framing cues it to act as a decisive agent, and it decisively approves.

## Implication for Phase 0b
The spec's null_a (full scaffold, empty slots) CANNOT be made 50/50 for C2 by any
scaffold revision. The spec §2.1.5 remedy ("revise the template") is exhausted for
C2. Decision required: (a) accept C2 as a documented harness-fragile exception and
pass 0b on the other 5; (b) treat "harness present vs absent" as itself the
measured effect; (c) something else. S1/S3/C1 robustness + S2 behaviour still to be
re-confirmed under the chosen final harness.

## Prompts FROZEN. No dilemma text edited.
