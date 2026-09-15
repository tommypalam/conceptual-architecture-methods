# coordinate_sweep_r2 — which of the ten coordinates are load-bearing?

## Why r2 exists

`coordinate_sweep_r1` halted at **689 of 2,801 calls** on a network
**TimeoutError**. No response was received, so nothing was measured — this is a
transport failure, not a model or parser failure. The no-retry rule charged the
full reservation ($0.011256300) and preserved the slot.

**The failed slot is NOT retried.** `coordinate_sweep_r1/profiled/CS_lo/6/tool_library`
stays unresolved permanently and is named as inherited, so a *new* unresolved
dispatch still stops the run. The rule is applied, not reinterpreted.

r2 re-runs the full 2,801-call schedule with **nothing changed** — same items,
same coordinates, same agents, same levels, same analysis. r1's 689 collected
calls are preserved as evidence of the halt and are not reused.

The halt was uniform across coordinates (84–98 of 350 each), so no coordinate was
advantaged or starved by where it stopped.

---

## Original protocol (unchanged)

**2,801 calls, worst case $31.517 against a $32.00 ceiling. Hard review gate.**

## Why now

`pd_prospective_r1` showed PD moves the deterministic good/bad headline by
**+0.346** when pinned to its endpoints. `label_semantics_r1` then showed the
effect belongs to the PD **label**: the same numerals on the inert AW label give
**−0.036**.

Together those establish a **validated method** — pin one coordinate to 0.1 and
0.9, hold the other nine identical, measure the paired contrast. This applies it
to the remaining eight.

## The eight

| | | |
|---|---|---|
| LL Legitimacy Locus | CS Constraint Sensitivity | RT Response Threshold |
| MoR Mode of Response | RE Relational Embedding | TfA Tolerance for Asymmetry |
| ID Internalisation Dependence | MS Moral Scope | |

**PD and AW are excluded**, both tested at 40 agents in `label_semantics_r1`:
PD +0.339 (Holm ≈ 0, load-bearing), AW −0.036 (Holm 1.000, inert). Re-testing
would spend budget re-deriving known results.

## Design

For each coordinate C and each agent: **C−** pins it to 0.1, **C+** pins it to
0.9, and the nine other coordinates are drawn once per agent and held identical.
25 agents × 8 coordinates × 2 arms × 7 items = **2,800 profiled decisions**.

**Verified across all 200 agent-coordinate pairs before collection:** the system
prompts differ by **exactly two diff lines** and the user text is byte-identical.

```
- 9. Moral Scope: 0.10
+ 9. Moral Scope: 0.90
```

## No directional prediction

The PD direction was derivable because every item presents a claim under a stated
arrangement, mapping onto PD's process/outcome definition. **No comparable
mapping exists for these eight** — nothing in these items is specifically about
legitimacy locus or moral scope. Predicting directions without grounds would be
decoration, so the test is **two-sided** and the rule requires only a difference.

## Decision rule

A coordinate is declared load-bearing if **both**: its pooled Holm p < 0.05 with
Holm correction over **all eight contrasts as one family**, **and** its effect
points the same direction in ≥ 4 of 7 items.

Running them together rather than one at a time means a survivor has cleared a
genuinely multiple-comparison-corrected test.

## Power, measured before collection

Per coordinate, Holm over the 8-contrast family, 24 seeds:

| True gap | Power |
|---:|---:|
| 0.15 | 17/24 |
| **0.20** | **24/24** |
| 0.25 | 24/24 |
| 0.35 (the PD effect) | 24/24 |
| 0 (null) | **0/24** |

Fully powered at d ≥ 0.20 and underpowered below ~0.15 — stated now, not after.

## What a survivor means, and does not

A survivor shows that **pinning the coordinate on its own label moves the
outcome**. It does **not** yet show the **label** carries it rather than the
numeral — that needs the swap control `label_semantics_r1` ran for PD, which is
the correct follow-up for coordinates that survive and is deliberately not run
for all eight in advance.

## Expected outcome

Phase 5's post-hoc correlations found no coordinate besides PD surviving Holm in
any designation, and no stable ordering across designations. **A null across all
eight is plausible and informative**: it would establish PD as the only
load-bearing coordinate of the ten under this method, on this item set and model.

## Optimisations applied, and one refused

Recorded in the 17 September ceiling amendment:

- PD and AW excluded — already tested at 40 agents.
- **The U screen arm is dropped.** These seven items have been screened four
  times on gpt with consistent results; re-screening confirms rather than
  establishes. The review call is kept.
- No per-coordinate swap control — the correct follow-up for survivors.
- 25 agents, not 30: re-measured power is materially identical (24/24 at d ≥ 0.20
  for both), and 30 does not fit the ceiling.

**REFUSED:** three of the seven items showed small effects under the PD
manipulation. Cutting them would save ~40% and would be **outcome-driven
selection**, biasing the sweep toward coordinates that behave like PD. All seven
are retained.

## What this cannot establish

- **Not moral truth or improvement.** Deterministic classification under
  stipulated standards, never read from agent text.
- **Not that any survivor's label carries the effect** — that is the follow-up.
- **Not cross-model.** `gpt-5.4-mini` only.
- **Not generalisation.** Seven items, n = 25 agents.
- **No human validation**; raters remain deferred.
