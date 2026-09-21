# precipitation_r3 — assessment

**Complete. 1,680 calls, 1,680/1,680 valid, zero failures, $0.764479.**
`gpt-5.4-mini-2026-03-17`, 40 agents, 7 twins, 3 arms, both presentation orders,
22 September 2026. Protocol: [PROTOCOL.md](PROTOCOL.md). Design hash
`b75a407e…6146e11`, unchanged since r1.

**The confound is fixed and the secondary is readable. The slope appeared in the
arm that can respond and vanished from the arm that cannot — but it is carried by
seven agents and does not survive their removal.**

## Result

560 units complete in all three arms (agent × item × order):

| Arm | Keep-rate | 95% CI |
|---|---:|---|
| NEITHER (bare item) | 0.3054 | [0.2661, 0.3429] |
| **INSTANCES** (the agent's own five prior decisions) | **0.7339** | [0.6964, 0.7696] |
| **RULE** (the principle stated) | **0.7679** | [0.7339, 0.8018] |

| Contrast | Estimate | 95% CI |
|---|---:|---|
| INSTANCES − NEITHER | **+0.4286** | [+0.3839, +0.4732] |
| RULE − NEITHER | **+0.4625** | [+0.4179, +0.5071] |
| INSTANCES − RULE | **−0.0339** | [−0.0643, −0.0036] |

All reproduce r2 closely (+0.396, +0.500, −0.104), on a design where order is
balanced rather than confounded. **The primary result is now measured twice.**

## The secondary, which is what this designation was for

| Arm | Dose-response slope on exemplar keep-count | 95% CI | |
|---|---:|---|---|
| **INSTANCES** | **+0.0804** | [+0.0180, +0.1366] | excludes zero |
| RULE | −0.0111 | [−0.0439, +0.0253] | flat |

**This is the inverse of r2**, where the slope sat in RULE (−0.083, excluding
zero) and INSTANCES was flat. Crossing order with the covariate moved it to the
only arm that can carry it: RULE's text is byte-identical for every agent and
*cannot* respond to exemplar content, so its flatness is the control working.

It holds within each order separately, so it is not an artefact of pooling:

| Order | k=1 | k=2 | k=3 | k=4 |
|---|---:|---:|---:|---:|
| INSTANCES−NEITHER, keep first | +0.095 | +0.107 | +0.277 | +0.277 |
| INSTANCES−NEITHER, override first | +0.238 | +0.536 | +0.664 | +0.643 |
| RULE−NEITHER, keep first | +0.381 | +0.250 | +0.286 | +0.277 |
| RULE−NEITHER, override first | +0.667 | +0.643 | +0.630 | +0.643 |

## Why the slope is not claimed

**It is carried by seven agents.** The exemplar keep-counts inherited from the
frozen transcripts are badly unbalanced — 3 agents at k=1, 4 at k=2, 17 at k=3,
16 at k=4 — and restricting to the well-populated cells destroys it:

| Subset | Slope | 95% CI |
|---|---:|---|
| All 40 agents | +0.0804 | [+0.0117, +0.1351] |
| **k ≥ 3 (33 agents)** | **−0.0108** | **[−0.0659, +0.0460]** |
| k ≥ 2 (37 agents) | +0.0418 | [−0.0329, +0.1107] |

Between k=3 and k=4 — where 33 of 40 agents sit — **there is no dose-response at
all.** What the pooled slope describes is a step between a sparse low group and
everything else, not a graded response to exemplar content. A graded response is
what a fitted boundary predicts; a step on seven agents is what a small-sample
artefact also predicts, and this designation cannot separate them.

The protocol's decision rule returned `boundary_precipitates_differently`. **That
decision is recorded and not claimed**, for this reason.

## What is established

1. **Showing an agent its own five prior decisions shifts behaviour by +0.43** on
   items those decisions never covered, in a direction they never state. Measured
   twice, order-balanced.
2. **Stating the principle shifts it slightly more** (+0.46), and the difference
   is small but excludes zero (−0.034). Examples nearly reproduce the rule.
3. **The confound diagnosis from r2 was correct.** Crossing order moved the slope
   from the impossible arm to the possible one, which is what the diagnosis
   predicted and is the cleanest confirmation available that r2's void was read
   correctly.

## What is not established

Precipitation. A fitted boundary predicts a *graded* response to exemplar content,
and the graded part of the evidence lives in seven agents. The mundane reading —
relevant context shifts behaviour, an explicit principle marginally more — remains
unexcluded, and is if anything strengthened by INSTANCES and RULE landing within
0.034 of each other.

Understanding, or that the model holds a concept. Survival under decay, the second
half of Conjecture 1, untouched. Anything beyond this model, these seven twins and
these exemplars.

## What would settle it

**Exemplar keep-count must be balanced by construction, not inherited.** The
frozen transcripts supply what they supply; a successor should *select or
construct* exemplar sets to populate k=0…5 evenly — selection on a property of the
exemplars, not on any outcome, so it is not outcome-driven. With ~8 agents per
level the slope would be readable across its whole range rather than resting on
its tails. That is the third circularity control of the original protocol
(no idealised exemplars) in tension with statistical balance, and the tension
should be resolved explicitly rather than by inheritance.

## Accounting

OpenAI $21.879964 → **$22.644443**/$40. Anthropic unchanged $22.268707/$32.
Package ≈ $44.913/$100. Usage estimates, not verified provider balances.
