# position_counterbalance_r1 — the label, or the line it sits on?

**2,241 calls on `gpt-5.4-mini`. Review advisory. This designation can refute
this project's own published finding.**

## The confound

`label_semantics_r1` moved the level from the Procedural Dependence line to the
Affective Weighting line and the effect vanished — TRUE +0.339, SWAP −0.036. That
was reported as showing the effect belongs to the PD **label**.

**It does not show that.** In the rendered block PD is **line 6** and AW is
**line 10**. The swap therefore moved the label *and its position together*:

```
TRUE+     6. Procedural Dependence: 0.90   ...  10. Affective Weighting: 0.50
SWAP+     6. Procedural Dependence: 0.50   ...  10. Affective Weighting: 0.90
```

A model weighting earlier lines more heavily — an ordinary primacy effect over a
numbered list — would produce that entire result with **no label reading
whatsoever**. Position is a third unexcluded mechanism alongside field-weighted
extremity, and the paper did not name it until now.

## Design: a 2×2 crossing binding with position

The block is rendered in two orders. **NORMAL** is canonical, as every prior
designation used it. In **EXCHANGED**, the PD and AW entries swap line positions —
AW printed at line 6, PD at line 10 — while the other eight entries stay put,
each carrying its own gloss and value.

| Arm | Binding | Order | Level sits on | At line |
|---|---|---|---|---:|
| **A** | TRUE | normal | Procedural Dependence | 6 |
| **B** | SWAP | normal | Affective Weighting | 10 |
| **C** | TRUE | exchanged | Procedural Dependence | 10 |
| **D** | SWAP | exchanged | Affective Weighting | 6 |

Each arm runs at both levels (0.90 and 0.10), giving eight cells. 40 agents ×
7 items × 8 cells = 2,240 profiled calls, plus one review.

### The two orthogonal contrasts

```
LABEL, position held fixed      A vs D    both carry the level at line 6
                                C vs B    both carry it at line 10

POSITION, label held fixed      A vs C    both put it on Procedural Dependence
                                B vs D    both put it on Affective Weighting
```

## Competing predictions, locked before collection

These are genuinely competing. The result is not predetermined.

| If | Then | Consequence |
|---|---|---|
| **the label carries it** | A > D and C > B, with A ≈ C | `label_semantics_r1` survives and is **strengthened**: position excluded, claim upgrades from field-bound to label-bound |
| **position carries it** | A > C and D > B, with A ≈ D | `label_semantics_r1` is **refuted**; its effect is attributable to line 6, not to the PD label |
| **both contribute** | both contrasts non-zero | the effect decomposes and is reported as decomposed |

**Decision rule.** The label binding is declared load-bearing if cells **A and C**
— both holding the level on PD, at lines 6 and 10 respectively — each clear Holm
p < 0.05 with the effect in the same direction in at least 4 of 7 items, **while
cells B and D do not**. Holm is applied over all four within-cell contrasts as one
family.

**Failure condition, stated in source.** If the LABEL contrast is null while the
POSITION contrast is significant, this **refutes this project's own published
label-semantics finding**. It is reported as a refutation, `label_semantics_r1` is
marked superseded with its data intact, and the paper's central claim is restated
as a position effect. It is not reframed.

## Power

Simulated against the **measured** per-item baselines from `phase4b_gpt_r2`'s E
arm across all seven items, 20 seeds, Holm family of 4:

| True effect | Detected |
|---:|---|
| **+0.339** (PD's measured TRUE effect) | **20/20** |
| +0.250 | 20/20 |
| +0.200 | 19/20 |
| +0.150 | 19/20 |
| 0.000 | **0/20** false positive |

Unlike the cross-model designations this is not marginal: PD's effect is the
largest in the project, so a null here would be informative rather than
ambiguous.

## Construction, verified before any call

**`verify_construction()`** checks, for every agent at both levels: that the
exchange is a permutation moving exactly the two named lines; that all four arms
carry the identical numeral multiset; that the level sits on the declared label at
the declared position; that the eight other parameters never move in value *or*
position; and that the four arms are four distinct blocks. It carries forward the
rendered-precision degeneracy check from `label_semantics_r2`. **Zero degenerate
agents** under the chosen seed.

**`phase5_position_render.verify_render()`** checks the reordering itself. Its
strongest invariant: **reordering by the identity permutation must return the
input byte-for-byte.** That test caught a real bug — the renderer pads *every*
entry with a leading space, including entry 10, so that the periods align, and an
earlier version stripped it from 10. The property checks alone would have missed
it.

**A per-group wire check across all 560 agent-item-level groups** confirms the
four arms have byte-identical user text, identical system-prompt length, identical
numeral multiset, and the correct label at lines 6 and 10. **560/560 clean.**

## Accounting

Ledger before: Claude $22.238957400/$32, OpenAI $11.093290725/$40. This runs on
OpenAI with $28.907 of headroom. `label_semantics_r2`, the same shape and size,
settled at $1.656 against a $25.223 reservation.

## What this cannot establish

- **Not semantic understanding.** Even a clean label result shows the effect is
  bound to a label string, not that the model represents the concept it names.
- **Not field-weighted extremity excluded.** That mechanism remains, and this
  design does not address it.
- **Not generalisation.** Seven items, 40 agents, one model.
- **No human validation**; raters remain deferred.
