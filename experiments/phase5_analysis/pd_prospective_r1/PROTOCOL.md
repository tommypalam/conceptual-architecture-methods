# pd_prospective_r1 — the first prospective PD test

**736 calls, worst case $8.060 against a $10.00 ceiling. Hard review gate, then
a screen gate.**

## Why this designation exists

Procedural Dependence is the one coordinate this project keeps finding, and it
has never been tested prospectively.

- The **Phase 2 within-arm reanalysis** ranked PD first of ten under
  multivariate control, and recorded the binding caveat: a **post-hoc**
  discovery *"requiring prospective test before any confirmatory language."*
- The **Phase 5 integrated analysis** found PD top-ranked in both gpt
  designations (r = +0.406 and **+0.522**, the latter surviving Holm) — also
  post-hoc, on partially shared items, and **absent on haiku** (r = +0.089).

**Four prior attempts reached the profiled stage zero times.** `pd_endpoint_r2`
and `pd_gradient_r1`–`r5` were stopped by dispersion screens. `pd_discriminant_r1`
and `r2` cleared review with zero blocking issues and were stopped by their own
screens. The obstacle was never wording or magnitude — no item set both dispersed
unprofiled and could carry a PD contrast.

**Phase 4B produced one.** The seven-item gpt set cleared an independent review
with **zero blocking issues** in `phase4b_permutation_r2`, all seven disperse on
`gpt-5.4-mini` (mean headroom **0.331**), and their baselines are measured on
three models.

## Design

Two arms, identical in every respect but one number:

| Arm | Content |
|---|---|
| **PD−** | full ten-coordinate profile, **PD pinned to 0.1** (outcome-dominant) |
| **PD+** | full ten-coordinate profile, **PD pinned to 0.9** (process-dominant) |

Plus **U** (no profile, 175 calls) as a fresh baseline and screen.

40 agents × 7 items × 2 arms = 560 paired profiled decisions.

**Verified across all 40 agents before collection:** the system prompts differ by
**exactly two diff lines** —

```
- 6. Procedural Dependence: 0.10
+ 6. Procedural Dependence: 0.90
```

— and the user text is byte-identical. The nine other coordinates are drawn once
per agent and held identical between arms. Both arms are equally profiled, so the
contrast cannot be a profile-presence effect, a verbosity effect, or a demand
characteristic of being profiled at all.

## The locked prediction — DIRECTIONAL, derived from theory

> **PD+ produces a HIGHER share of decisions classifying `good` than PD−.**

CLAUDE.md defines PD as **0 = outcome-dominant** (results matter, methods
secondary), **1 = process-dominant** (fair procedure matters independently).

Every item presents someone holding a claim under a **stated arrangement** — a
desk booking, a lease, a loan with withdrawal rights, an off-rota night, a held
slot, a mandatory rest break, a requested day off. The option that **keeps** the
arrangement classifies `good`; the option that overrides it classifies
`not_good`. **Verified on all seven items** in `verify_design()`, not assumed.

Process-dominance therefore predicts keeping the arrangement, and a higher
good-rate under PD+.

**This direction follows from the coordinate's definition and would have been
predicted without seeing the Phase 2 or Phase 5 results.** It is not read off the
correlation.

## Power, measured against the screened baselines

40 agents × 7 items, 16 seeds:

| True PD gap | Power |
|---:|---:|
| 0.10 | 8/16 |
| **0.15** | **15/16** |
| **0.20** | **16/16** |
| 0.25 | 16/16 |
| 0 (null) | **0/16** |

PD is drawn Beta(2.5, 2.0), sd ≈ 0.19. This designation pins it at 0.1 and 0.9 —
a spread of roughly 4.2 sd of the natural draw. Correlations of +0.41 and +0.52
over the natural range imply an endpoint gap comfortably above 0.15.

**The design is adequate for the effect the correlations imply, and underpowered
only if the true endpoint gap is below ~0.12.** That limitation is recorded now,
not after seeing the result.

## Decision rule

Declared only if **both**: pooled Holm p < 0.05, **and** the effect points the
same direction in ≥ 4 of 7 items.

## Failure is a result

**If PD+ and PD− do not differ, the prospective PD test fails on the first item
set ever built that could run it**, and the Phase 2 and Phase 5 findings remain
post-hoc indefinitely. That is reported as a failure, not reframed.

Three prior locked predictions in this project are recorded as **untested**
because their collections never reached the profiled stage. This designation
reaches it or reports why not.

## What this cannot establish

- **Not moral truth or moral improvement.** Deterministic classification under
  stipulated standards, computed from stipulated transitions, never read from
  agent text.
- **Not a claim about the other nine coordinates**, which are held constant
  rather than tested.
- **Not cross-model.** `gpt-5.4-mini` only — the model where the association was
  observed. PD was absent on haiku (r = +0.089), so no transfer is assumed.
- **Not generalisation.** Seven items, n = 40 agents, one harness, one snapshot.
- **No human validation**; human raters remain deferred.
