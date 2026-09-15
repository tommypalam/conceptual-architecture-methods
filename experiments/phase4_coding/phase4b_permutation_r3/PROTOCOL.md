# phase4b_permutation_r3 — the same test, re-powered on the observed effect

## Why r3 exists

`phase4b_permutation_r2` ran this design at 40 agents and **failed its
prespecified rule**: paired E−P = +0.089, raw p = 0.0105, **pooled Holm 0.084**,
5 of 7 items positive. Consistency passed; significance did not.

That null was uninterpretable **by design, not by surprise**. r2's protocol
recorded a power table before collection putting 40 agents at **7/12 for a gap of
0.10**, and stated: *"well powered for a large effect and underpowered for a small
one."* The observed gap landed almost exactly there.

**r3 changes one thing: the number of agents.** Items, arms, derangement,
analysis and decision rule are unchanged and already validated.

## Re-powered on the observed effect

Simulated at the measured gap of 0.089, against each item's screened baseline:

| Agents | Pairs | Power |
|---:|---:|---:|
| 40 (r2) | 280 | 5/16 |
| 80 | 560 | 10/16 |
| 100 | 700 | 13/20 |
| **120** | **840** | **16/16** |
| 160 | 1120 | 16/16 |

False positive at gap 0, 160 agents: **0/16**.

120 is the first adequately powered point. 140+ would reserve over $20 of the
$24.50 OpenAI headroom with phases 5 and 6 still to run.

**The screen arm shrinks to 15 probes** so the profiled design stays intact at
120 agents. These seven items have been screened three times on gpt already
(`grand_r1`, `gpt_r2`, `permutation_r2`, all n = 25, consistent), so this arm
re-confirms dispersion rather than establishing it.

**1,786 calls, worst case $19.960 against a $20.00 ceiling.** Prior runs settle
near 17% of reservation, so realistic spend is ~$3.4.

## What r2 already showed

| Arm | Good-rate | vs U | p |
|---|---:|---:|---:|
| U no block | 0.400 | — | — |
| P scrambled labels | 0.475 | +0.075 | 0.122 |
| E correct labels | 0.564 | **+0.164** | **0.00074** |

A scrambled block did not clear baseline; the correctly-labelled block did. The
difference between them is what r3 is powered to resolve.

**The direction is not predicted** and the null remains a real possible outcome.
If E and P do not differ at 840 pairs, that is strong evidence the block works
largely as a presentation cue, and it will be reported as such.

---

## Original protocol (unchanged except agent count and screen size)

## One item excluded on review

`phase4b_permutation_r1` stopped at its hard gate on **`revise`**, flagging a
single item: `sample_draw`, where one option takes a bodily sample from a person
who has explicitly refused. The reviewer judged that a legal/ethical absolute the
stipulated unit framework cannot neutralise, making the item leading rather than
balanced — and **explicitly cleared the other seven** as "structurally parallel
and balanced", downgrading `rest_break` to a limit rather than a blocker.

**This is the second independent reviewer to name `sample_draw`**, and the first
to narrow to it alone. The finding is specific, it is about that item, and it is
correct. r2 drops it and runs on the remaining seven.

**The exclusion is not outcome-driven.** It was made on a review finding, before
any profiled call in this designation, and it does not rescue a result — the
`phase4b_gpt_r2` effect is **larger** without `sample_draw` (+0.228 → +0.243,
p = 3×10⁻¹⁰), and larger still without all three items any reviewer has flagged
(+0.255, p = 9×10⁻⁹).

Seven items retain all four claim families, all five items shared with haiku, and
a mean headroom of 0.331. The consistency rule becomes ≥ 4 of 7.

---

## Original protocol (unchanged except item count)

**736 calls, worst case $8.060 against a $10.00 ceiling. Hard review gate, then a
screen gate.**

## The caveat this settles

Every Phase 4B assessment carries the same limitation:

> "A shift under a numeric block is consistent with the block acting as an
> elaborate context cue."

Phase 4B showed that a numeric profile moves the deterministic good/bad headline
(+0.211 on gpt, p = 0.0000038) where an explicit ethical instruction does not
(−0.017, p = 0.712). What it could not show is whether the model reads the
*parameters*, or whether any plausible structured numeric block would do the same
work.

## The manipulation

For each agent, the ten drawn coordinates are **permuted across the ten labels**.

| Arm | Content |
|---|---|
| **E** | the agent's values against their **correct** labels |
| **P** | the **same ten numbers** against **deranged** labels |

```
E    LL 0.41   CS 0.83   RT 0.19   ...   PD 0.22   ...
P    LL 0.22   CS 0.41   RT 0.83   ...   PD 0.19   ...
```

**Verified across all 40 agents, before collection:** identical user turns,
identical system-prompt length, identical multiset of rendered numerals, and
E ≠ P for every agent. The permutation is a fixed 10-cycle derangement, seeded
and declared in source, so **no label keeps its own value** and no two labels
merely swap.

This is the tightest control the project can build: the two arms are matched on
every quantity a "structured numbers" account could appeal to — mean, variance,
extremes, digit patterns, block length, field order, token count. **Only the
label-to-value assignment differs.**

Why not a fixed or random profile: a constant profile changes the numeric
content, and a fresh draw changes the distribution. Permutation holds the agent's
own values exactly and moves only the assignment.

## Arms

| Arm | n |
|---|---:|
| **U** no profile — fresh baseline | 200 |
| **E** drawn values, correct labels | 320 |
| **P** same values, deranged labels | 320 |

40 agents × 8 items × 2 profiled arms, paired within agent and item. The **G arm
is not carried**: its question was answered in `phase4b_gpt_r2`, and this
designation spends its calls on the contrast that answers a different one.

Model: `gpt-5.4-mini-2026-03-17`, the calibration model, where the Phase 4B
effect was strongest (+0.228 paired, Holm ≈ 0).

## Locked prediction

> **E differs from P** on the share of decisions classifying `good`.

**Direction is not predicted.** A permuted profile is not a *worse* profile — it
is a different one — so there is no principled basis for predicting which way it
moves the headline.

| Outcome | Reading |
|---|---|
| **E ≠ P** | the label-to-value mapping carries the effect; the cue reading is ruled out and **the caveat is retired** |
| **E ≈ P** | the block works regardless of where the numbers sit; the effect is a presentation artefact and **the caveat stands** |

Both outcomes are publishable. The second would cost the project its central
interpretation, which is what makes this a real test.

## Power, measured before collection

Paired E vs P, 40 agents × 8 items, 12 seeds:

| True E−P gap | Power |
|---:|---:|
| 0.21 (permutation fully destroys the effect) | **12/12** |
| 0.15 | 10/12 |
| 0.10 | 7/12 |
| 0.05 | 3/12 |
| 0 (null) | 1/12 false positive |

**Stated plainly: this design is well powered for a large effect and
underpowered for a small one.** If permuting labels merely dents the effect
rather than destroying it, a null here would be weak evidence. That limitation is
recorded now, not after seeing the result.

## Decision rule

Declared only if **both**: pooled Holm p < 0.05, **and** the effect points the
same direction in ≥ 4 of 8 items.

## Failure is a result

If E and P do not differ under that rule, **the profile is not shown to be read
as parameters**, and every Phase 4B claim must be reported under that
limitation. Reported as a failure, not reframed.

## What this cannot establish

- **Not moral truth or moral improvement.** Deterministic classification under
  stipulated standards, never read from agent text.
- **Not that the model "understands" the parameters** even if E ≠ P. It would
  show the label-to-value mapping is load-bearing, which is weaker than
  comprehension and stronger than a formatting cue.
- **Not the thesis §5.3 configuration counterfactual**, which varies the five
  societal axes and tests the *context* block. That remains unrun.
- **Not generalisation.** Eight items, one model, n = 40 agents.
- **No human validation**; human raters remain deferred.
