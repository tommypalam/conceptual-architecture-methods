# position_counterbalance_r1: the label carries it, not the line

**Outcome: complete. 2,241 calls, 2,240/2,240 valid, zero failures.**
18 September 2026. Review **accept**, zero blocking issues. Cost $1.656796
against a $25.223 reservation.

Ledger after this designation: Claude $22.247448300/$32, OpenAI $12.741596175/$40,
package $34.989044/$100. Usage estimates, not wallet balances.

**The effect is bound to the Procedural Dependence label, not to the line the
label occupies.** `label_semantics_r1`'s reading survives a control it could not
itself run, and the claim upgrades from *field-bound* to *label-bound*.

## The confound this closes

`label_semantics_r1` moved the level from the PD line to the AW line and the
effect vanished (TRUE +0.339, SWAP −0.036). But in the rendered block **PD is line
6 and AW is line 10**, so that swap moved the label *and its position together*. A
model weighting earlier lines more heavily — an ordinary primacy effect over a
numbered list — would have produced the entire published result with no label
reading at all.

That mechanism was not named in the paper until a reviewer identified it. It was a
genuine gap in our own claim, not a technicality.

## Result

40 agents × 7 items × 8 cells. Each cell's effect is the paired high-minus-low
contrast within that cell; Holm over all four cells as one family.

| Cell | Level on | At line | Effect | raw p | **Holm** | Items |
|---|---|---:|---:|---:|---:|---|
| **A** | **Procedural Dependence** | **6** | **+0.393** | ≈ 0 | **0.000000** | **7+/0−** |
| **C** | **Procedural Dependence** | **10** | **+0.271** | ≈ 0 | **0.000000** | 5+/1− |
| B | Affective Weighting | 10 | +0.061 | 0.0784 | 0.157 | 6+/1− |
| D | Affective Weighting | 6 | +0.004 | 1.000 | 1.000 | 3+/2− |

**The label factor, averaged over the two comparisons that isolate it: +0.300.**
The position factor is decomposed below rather than averaged, because averaging it
is misleading.

| Contrast | Holds fixed | Varies | Difference |
|---|---|---|---:|
| A vs D | position 6 | the label | **+0.389** |
| C vs B | position 10 | the label | **+0.211** |
| A vs C | label PD | position | +0.122 |
| B vs D | label AW | position | +0.057 |

**The prespecified rule fired:** cells A and C both clear Holm p < 0.05 with 4+ of
7 items consistent, while B and D do not. `label_carries = True`.

## Why cell D is the decisive cell

D puts `0.90` on **line 6** — the privileged position under any primacy account —
but on the Affective Weighting label. It gives **+0.004**. Essentially nothing.

If position carried the effect, D should have resembled A. It resembles noise. Put
the same numeral at the same line under a different label and the effect
disappears; keep the label and move it four lines down (cell C) and the effect
survives at +0.271.

Cell A is positive on **all seven items**, with `rest_break` at +0.750,
`storage_unit` +0.650 and `tool_library` +0.625.

## The position main effect is null; the interaction is not

An earlier version of this assessment reported "position +0.032, a modest
component". **That was the wrong summary and is corrected here.** Averaging
position across the two labels hides that it does opposite things on each: on PD
line 6 beats line 10 by +0.121; on AW line 6 *trails* line 10 by −0.057. The
average describes neither cell.

Decomposed properly, with 95% intervals from a paired bootstrap over all 280
agent-item units present in every cell:

| Term | Estimate | 95% CI | Includes zero |
|---|---:|---|---|
| Position **main effect** | +0.032 | [−0.025, +0.088] | **yes** |
| **Interaction** (position × label) | **+0.089** | **[+0.030, +0.150]** | no |
| Position on the PD label (A − C) | **+0.121** | **[+0.046, +0.200]** | no |

**There is no position main effect.** Cell D establishes that directly: the level
at the privileged line on the inert label yields +0.004, so position does not act
on the value independently of the label.

**What survives is an interaction** — position modulates the magnitude of an
already-present label effect. The label works somewhat better earlier in the
block, and does nothing at either position when it is the wrong label. The
interval is clear of zero, but the decomposition was **not prespecified** and
rests on one designation; it is a finding to replicate, not an established
magnitude.

## The inert partner is less inert than assumed

Every swap control in this project rests on Affective Weighting being inert. That
premise now has **two prospective manipulation estimates of the same nominal
condition** — the level on AW at line 10 — and they disagree in sign:

| Designation | Estimate | *p* | Consistency |
|---|---:|---:|---|
| `label_semantics_r1`, SWAP arm | **−0.036** | 0.260 | 27+/37− pairs |
| this designation, cell B | **+0.061** | 0.078 | **6 of 7 items positive** |

A swing of 0.096, both null. **Nothing here breaks**: every claim resting on AW's
inertness used a null, and both estimates are null.

**But the pattern is the one this project withdrew a coordinate for.** The decision
rule used throughout pairs statistical significance with directional consistency.
Cell B has the consistency without the significance — six of seven items the same
way, pooled test not clearing. LL went positive, negative, null across three
measurements and was withdrawn; AW has now gone −0.036, +0.061 across two, while
carrying the premise that makes every swap control interpretable.

**AW's inertness accurately stated** rests on three post-hoc correlations, all
non-significant after correction, plus two prospective estimates that agree in
being null and disagree in sign. Earlier documents in this project described it as
"measured inert by two independent methods"; that is weaker than it sounded, and
this is the more accurate description.

This does not license discarding the swap controls — a partner null in both
estimates still supports the inference they draw. It does mean the inertness
premise is an empirical claim with its own uncertainty rather than a design
constant. A designation pinning AW as a coordinate in its own right, at adequate
power, is the way to settle it. It has not been run.

## What this establishes

**The PD effect belongs to the PD label string, not to a line of the block.** This
was the strongest remaining alternative explanation for this project's central
control, and it is now excluded by a design that held the numeral multiset, block
length and line count identical across all four arms while crossing binding with
position.

**Three of four candidate mechanisms are now excluded.** Block presence and
verbosity were excluded by construction; free-floating numeric extremity by the
original swap; position by this designation.

## What this does NOT establish

- **NOT semantic understanding.** The effect is bound to a label *string*. A model
  that had learned a purely associative mapping from the characters `Procedural
  Dependence` to a behavioural disposition, with no conceptual content, would
  produce every result here. This distinction is the paper's §1.3 and it is
  unchanged.
- **Field-weighted extremity is still not excluded.** A model weighting an extreme
  value by the salience of the field holding it remains consistent with these
  data. This designation addresses position, not salience, and no design in this
  project separates salience from label semantics.
- **NOT cross-model.** `gpt-5.4-mini` only. The cross-provider designations
  (`pd_crossmodel_r1`, `id_crossmodel_r1`) ran no counterbalance, so their claims
  remain at *field-bound* — label-plus-position — and must not silently inherit
  this upgrade. That is a smaller residual gap than the one closed here, but it is
  real.
- **NOT ID.** Only the PD label was counterbalanced. ID's swap control
  (`label_semantics_r2`) carries the same position confound, unaddressed.
- **Not generalisation.** Seven items, 40 agents, one model, one harness.
- **No human validation**; raters remain deferred.

## A bug the identity invariant caught

Realising the EXCHANGED order meant reordering entries in a rendered string — each
a numbered line plus a two-line gloss — and renumbering. This is exactly the kind
of surgery that corrupts silently.

`phase5_position_render.verify_render()` therefore carries an invariant stronger
than any property check: **reordering by the identity permutation must return the
input byte-for-byte.** It failed on the first version. The template pads *every*
entry with a leading space, including entry 10, so that the periods align; the
first implementation stripped it from 10. Numeral multiset, line count, value
preservation and gloss preservation all passed — only the identity test caught it.

Fixed before any call. The invariant is retained in source.

## A provenance guard that fired, and was obeyed

`prepare()` initially refused with **"Frozen continuation source changed"**. The
cause was ours: the 18 September removal of the retired project name had edited
one docstring line in `code/utils.py`, which is pinned by every release built on
it.

**The pinned bytes were restored rather than the check loosened.** The guard cannot
distinguish a comment from a logic change, which is what makes it worth having,
and deciding that one's own change is harmless enough to wave through is precisely
what it exists to prevent. `code/utils.py` therefore retains the retired name in
one docstring, now a deliberate exception on the same footing as the frozen
archive files.

## Provenance

Review returned **accept**, zero blocking issues.

Build-time checks before any call:

- `verify_construction()` across all 40 agents at both levels — the exchange is a
  permutation moving exactly the two named lines; all four arms carry the identical
  numeral multiset; the level sits on the declared label at the declared position;
  the eight other parameters never move in value *or* position; the four arms are
  four distinct blocks. **Zero degenerate agents.**
- `verify_render()` including the identity invariant described above.
- A per-group wire check across all **560 agent-item-level groups**: byte-identical
  user text, identical system-prompt length, identical numeral multiset, and the
  correct label at lines 6 and 10. **560/560 clean.**

Power measured before collection against the **measured** per-item baselines from
`phase4b_gpt_r2`'s E arm, 20 seeds, Holm family of 4: **20/20** at PD's measured
+0.339, 19/20 at +0.150, **0/20 false positives**.

The analysis used `declared_tasks()` — the fix carried forward from
`pd_crossmodel_r1` — and produced its own analysis without offline rescoring.

2,241 calls dispatched, 2,240 valid, 280 in each of eight cells, zero entries in
`failures.jsonl` for this designation.
