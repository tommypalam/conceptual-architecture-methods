# phase4b_permutation_r2 — is the profile read as parameters, or as a cue?

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
