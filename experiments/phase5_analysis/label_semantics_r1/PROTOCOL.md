# label_semantics_r1 — does the PD *label* carry the meaning?

**1,296 calls, worst case $14.354 against a $15.00 ceiling. Hard review gate,
then a screen gate.**

## The confound this resolves

`phase4b_permutation_r2` asked whether the profile is read as parameters or acts
as an elaborate formatting cue. It deranged **all ten** labels at once and got
E−P = +0.089, pooled Holm 0.084 — the prespecified rule failed and **the caveat
stands**.

A ten-binding derangement is a blunt instrument. It moves every coordinate
simultaneously, so the contrast is diluted across whatever fraction of the ten
actually carry signal. If one coordinate does most of the work and the
derangement happens to move it somewhere unimportant, a weak gap is exactly what
you would see.

`pd_prospective_r1` then located the signal: **PD moved the good-rate +0.346**
(pooled Holm ≈ 0, 6 of 7 items). That makes a far sharper control possible.

## The design — one binding, active against inert

Phase 5's integrated analysis measured **AW as the weakest coordinate** in both
gpt designations (r = −0.051 and −0.167, both Holm 1.000), found it inert, and
confirmed dropping it changes no conclusion. CLAUDE.md independently flags AW as
preliminary. It is the natural inert partner.

For each agent and each level L ∈ {0.1, 0.9}:

| Arm | PD field | AW field | other eight |
|---|---|---|---|
| **TRUE(L)** | **L** | drawn AW | drawn |
| **SWAP(L)** | drawn AW | **L** | drawn |

Both arms carry the multiset {L, drawn-AW} across those two fields, so **the
blocks are numeral-identical**: same length, same line count, same ten numbers,
same field order. Only which of the two labels holds L differs.

**Verified across all 40 agents before collection** — 80/80 arm pairs
numeral-identical, user text byte-identical, and the rendered diff confined to
exactly four lines in the two named fields:

```
- 6. Procedural Dependence: 0.90
+ 6. Procedural Dependence: 0.61
- 10. Affective Weighting: 0.61
+ 10. Affective Weighting: 0.90
```

**Disclosed:** the agent's drawn PD value is discarded in every arm. That is what
keeps TRUE and SWAP numeral-identical, and it means this designation tests **the
label binding at two fixed levels**, not the drawn PD distribution.

## Two contrasts

| Contrast | What it is |
|---|---|
| **TRUE(0.9) vs TRUE(0.1)** | replication check against `pd_prospective_r1` |
| **SWAP(0.9) vs SWAP(0.1)** | **the primary** — the same two numbers on the inert label |

## Locked prediction

**TRUE should reproduce +0.346.** If it does not, `pd_prospective_r1` failed to
replicate and the SWAP contrast is uninterpretable — so TRUE is a genuine gate on
the whole designation, not decoration.

**SWAP is not predicted directionally.** Its reading is prespecified:

| Outcome | Reading |
|---|---|
| SWAP ≈ 0 while TRUE is significant | the **label-to-value binding** carries the effect; the permutation caveat resolves in favour of the parameter reading |
| SWAP comparable to TRUE (≥ 75%) | the model responds to **numeric extremity**, not the field; the parameter reading is substantially weakened |
| SWAP significant but smaller | partial; reported as measured with neither reading claimed |

## Power, measured before collection

One contrast, Holm over the doubled 16-member family (both contrasts plus all
per-item tests), 16 seeds:

| True gap | Power |
|---:|---:|
| 0.10 | 7/16 |
| 0.15 | 14/16 |
| 0.20 | 16/16 |
| **0.35** (the PD effect) | **16/16** |
| 0 (null) | **0/16** |

Well powered for the effect TRUE is expected to show, and for any SWAP effect of
comparable size. **Underpowered only if SWAP is real but below ~0.12** — in which
case the correct reading is "smaller than TRUE", which the rule already handles.

## Why this beats the derangement

`permutation_r2` moved ten bindings and measured +0.089. This moves **one**
binding on a coordinate measured at **+0.346**, so the expected effect is large
and the same sample size is far better powered. The manipulation is also
interpretable: named coordinates, one binding, a directional prediction on the
replication arm.

## Failure is a result

If SWAP is statistically indistinguishable from TRUE, **the parameter reading is
weakened and reported as such, not reframed.**

## What this cannot establish

- **Not moral truth or improvement.** Deterministic classification under
  stipulated standards, never read from agent text.
- **Not a claim about the other eight coordinates**, untouched here.
- **Not that PD is understood as a concept**, only whether its label is
  load-bearing relative to an inert one.
- **Not cross-model.** `gpt-5.4-mini` only.
- **Not generalisation.** Seven items, n = 40 agents.
- **No human validation**; raters remain deferred.
