# precipitation_r2 — assessment

**Complete. 840 calls, 840/840 valid, zero failures, $0.382414.**
`gpt-5.4-mini-2026-03-17`, 40 agents, 7 twins, 3 arms, 22 September 2026.
A re-designation of [precipitation_r1](../precipitation_r1/ASSESSMENT.md), which
halted on a transport timeout; none of its records are used here. Protocol:
[PROTOCOL.md](PROTOCOL.md). Design hash `b75a407e…6146e11`.

**Both arms shift behaviour and they differ. The pre-registered secondary that
would have made this a precipitation result is VOID, by its own stated criterion.**

## Result

Keep-rate on the queue-jumped twins, 280 units complete in all three arms:

| Arm | Keep-rate | 95% CI |
|---|---:|---|
| NEITHER (bare item) | 0.3071 | [0.2536, 0.3643] |
| **INSTANCES** (the agent's own five prior decisions) | **0.7036** | [0.6500, 0.7571] |
| **RULE** (the principle stated) | **0.8071** | [0.7607, 0.8500] |

| Contrast | Estimate | 95% CI |
|---|---:|---|
| INSTANCES − NEITHER | **+0.3964** | [+0.3321, +0.4607] |
| RULE − NEITHER | **+0.5000** | [+0.4393, +0.5607] |
| INSTANCES − RULE | **−0.1036** | [−0.1607, −0.0464] |

All three exclude zero. The collector's decision rule returned
`boundary_precipitates_differently`.

## The secondary is void, and that governs the reading

The design's discriminating test was a dose-response: if a boundary is *fitted* to
instances, the shift should track how keep-leaning each agent's five exemplars
were. The protocol stated in advance that **the RULE arm cannot produce such a
slope** — its text is byte-identical for every agent — and that a slope there
would mean the exemplar count is proxying something else, voiding the secondary.

| Arm | Slope on exemplar keep-count | 95% CI |
|---|---:|---|
| INSTANCES | −0.026 | [−0.110, +0.037] |
| **RULE** | **−0.083** | **[−0.139, −0.040]** |

**The RULE slope excludes zero. The secondary is void.**

The cause, found by follow-up: **exemplar keep-count is confounded with agent
parity, and parity sets presentation order.**

| Exemplar keeps | Even agents (keep shown first) | Odd agents |
|---|---:|---:|
| 1 | 0 | 3 |
| 2 | 1 | 3 |
| 3 | 5 | 12 |
| **4** | **14** | **2** |

And presentation order matters enormously on the bare item: NEITHER gives 0.436
keep when keep is listed first against 0.179 when it is not. The "dose-response"
was reading order, not exemplars. **This is the order-dependence defect of
[ORDER_DEPENDENCE.md](../ORDER_DEPENDENCE.md) reappearing in a third form** —
after the base items, after the inverse-inference prompt, now in a covariate.

Note what did *not* happen: the INSTANCES slope is flat. There is no evidence the
shift tracks the exemplars at all, which is the opposite of what precipitation
predicts. Had only the INSTANCES slope been significant I would have had a
positive result; instead the arm that *cannot* respond is the one that did.

## What survives, and what does not

**The primary contrasts survive the confound**, because every one is paired within
agent-item with presentation order held fixed inside the pair. Split by order:

| Contrast | Keep first | Override first |
|---|---:|---:|
| INSTANCES − NEITHER | +0.2714 | +0.5214 |
| RULE − NEITHER | +0.3929 | +0.6071 |
| INSTANCES − RULE | −0.1214 | −0.0857 |

Every sign holds in both orders. So these three facts stand:

1. **Showing an agent its own five prior decisions shifts behaviour substantially**
   (+0.396) on items the decisions never covered, in a direction the decisions
   never state.
2. **Stating the principle shifts it more** (+0.500).
3. **The two differ** (−0.104): exemplars do not fully reproduce what the stated
   rule does.

**What does NOT survive is the inference from those facts to precipitation.** With
the dose-response void, nothing distinguishes "a boundary was fitted to the
instances" from "additional relevant context shifts behaviour, and an explicit
principle shifts it more than examples do." The second is the mundane reading and
this designation cannot exclude it. **The `boundary_precipitates_differently`
decision is recorded but not claimed.**

## What would settle it

The confound is fixable and cheap. Presentation order must be **crossed with**
exemplar keep-count rather than left to correlate with agent index — each
agent-item shown in both orders, 1,680 calls, about $0.77. That is the design
[ORDER_DEPENDENCE.md](../ORDER_DEPENDENCE.md) rule 1b already requires for forced
choices, and I did not apply it to a covariate. A successor would also want
exemplar sets balanced across keep-count by construction rather than inherited
from whatever the frozen transcripts happened to contain.

## What no reading of this establishes

Understanding, or that the model holds a concept. Precipitation: the primary
contrasts are consistent with it and do not evidence it, and the test that would
have is void. Survival under decay, which is the second half of Conjecture 1 and
untouched here. Anything beyond `gpt-5.4-mini`, these seven twins, and these
exemplars.

## Accounting

OpenAI $21.497550 → **$21.879964**/$40. Anthropic unchanged $22.268707/$32.
Package ≈ $44.149/$100. Usage estimates, not verified provider balances.
