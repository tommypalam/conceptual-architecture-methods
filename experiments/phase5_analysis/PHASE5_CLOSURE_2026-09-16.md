# Phase 5 closure — 16 September 2026

Phase 5 is closed **for a scoped objective**, in the manner of the accepted Phase
1.5 and Phase 3 closures. Three of its four specified deliverables are met. The
fourth — **human resemblance** — is not met and is not retrospectively passed.

Spec §1.2: *"Relate representations, behaviour, human resemblance and moral
outcomes; report sensitivity and failure cases. Follows available evidence."*

| Deliverable | Status |
|---|---|
| representations ↔ behaviour | **met** |
| behaviour ↔ moral outcomes | **met** |
| **human resemblance** | **NOT MET** — no human data exists |
| sensitivity and failure cases | **met** |

---

## The headline: the prospective PD test passed

[`pd_prospective_r1`](pd_prospective_r1/ASSESSMENT.md) — 736 calls, 736/736
valid, zero failures, $0.489219.

| Arm | Good-rate | n | vs U | p |
|---|---:|---:|---:|---:|
| **PD−** (0.1, outcome-dominant) | 0.382 | 280 | −0.041 | 0.431 |
| **U** (no profile) | 0.423 | 175 | — | — |
| **PD+** (0.9, process-dominant) | **0.729** | 280 | **+0.306** | **< 10⁻⁸** |

Paired PD+ vs PD−: **+0.346**, 280 pairs, 113 against 16 discordant, **pooled
Holm ≈ 0**, **6 of 7 items positive** with five surviving individual correction.

**The entire manipulation:**

```
- 6. Procedural Dependence: 0.10
+ 6. Procedural Dependence: 0.90
```

Verified across all 40 agents: exactly two diff lines, nine other coordinates
identical, user text byte-identical.

**The direction was locked from theory, not read off a correlation.** CLAUDE.md
defines PD as 0 = outcome-dominant, 1 = process-dominant. Every item presents a
claim under a stated arrangement, and the option keeping it classifies `good` on
all seven — verified in `verify_design()`, not assumed. Process-dominance
predicts a higher good-rate, and that was recorded in source before any call.

### Why this matters beyond its size

**PD's dominance is no longer post-hoc.** The Phase 2 within-arm reanalysis
ranked PD first of ten under multivariate control and recorded the binding
caveat: a post-hoc discovery *"requiring prospective test before any confirmatory
language."* This designation is that test.

**Four prior attempts reached the profiled stage zero times** — `pd_endpoint_r2`,
`pd_gradient_r1`–`r5`, `pd_discriminant_r1` and `r2` — all stopped by dispersion
screens. The obstacle was that no item set both dispersed unprofiled and could
carry a PD contrast. Phase 4B produced one.

**It is the largest effect the project has measured:**

| Contrast | Paired effect |
|---|---:|
| Permutation E vs P (failed its rule) | +0.089 |
| Phase 4B haiku, E vs G | +0.171 |
| Phase 4B gpt, E vs G | +0.228 |
| **PD+ vs PD−** | **+0.346** |

---

## The integrated analysis

[`integrated_20260916`](integrated_20260916/ASSESSMENT.md) — **zero API calls**,
offline over 2,205 collected decisions across two models and three independent
population draws.

**Q1 Coordinate association.** PD ranks first in both gpt designations
(r = +0.406, **+0.522 surviving Holm**), matching Phase 2. Qualified: the two gpt
runs share 7 of 8 items, so it is a partial replication across *agents*; and on
haiku PD is essentially zero (r = +0.089).

**Q2 Parameter redundancy — critical open problem 6.** Across 120 agents: no pair
reaches |r| ≥ 0.4, **9 of 10 components** are needed for 90% of variance, minimum
eigenvalue **0.621**. The ten coordinates are empirically separable **as
sampled**. This tests the copula, not the concepts, and says so.

**Q3 AW sensitivity — the check CLAUDE.md asked for.** AW is inert in all three
designations (r = +0.016, −0.051, −0.167; all Holm 1.000) and dropping it changes
no conclusion anywhere. **AW remains preliminary**; its inclusion is not
load-bearing for any reported result.

**Q4 Portability — critical open problem 8.** **No stable coordinate ordering.**
Two designations on the *same model* agree no better than chance (rank
correlation −0.054); one cross-model pair is negatively correlated (−0.406).

---

## What Phase 5 establishes

**One coordinate is causally load-bearing, prospectively.** Changing a single
number in a single line moves the deterministic good/bad classification by 35
percentage points, in the theory-predicted direction, on the calibration model.

**The ten coordinates are separable as sampled**, and AW's inclusion changes
nothing.

**Coordinate-level structure is not resolved at n = 40.** Rank orderings do not
agree even within a model. The **arm-level** effect is robust and replicates
across models; the **coordinate-level** story does not, PD excepted and only on
gpt.

**It pressures the permutation caveat without retiring it.** A cue account must
now explain why the identical block reading `0.90` behaves differently from the
identical block reading `0.10`. Evidence, not proof — the permutation control
failed its own rule and that caveat stands.

## What Phase 5 does NOT establish

- **Human resemblance is not addressed.** No human data exists. Human raters were
  deferred by the researcher's 13 September no-budget instruction, which stands.
  This deliverable is **unmet, not passed**.
- **Not moral truth or moral improvement.** Every label is a deterministic
  classification under stipulated standards, computed from stipulated
  transitions, never read from agent text.
- **Not that PD is understood as a concept.** The model responds to a value in a
  labelled field in the predicted direction. Whether that constitutes
  representing "procedural dependence" is untested.
- **Not a claim about the other nine coordinates.** They were held constant in
  the PD test precisely so they could not contribute.
- **Not cross-model for PD.** `gpt-5.4-mini` only; PD was flat on haiku.
- **Not separability of the concepts**, only of the sampler.
- **Not generalisation.** Seven items, 40 agents per arm, one harness, one
  snapshot.
- **`on_call` ran negative** (−0.150, Holm 0.180). One of seven does not follow
  the pattern, and it is reported rather than smoothed.

---

## Designation record

| Designation | Outcome | Calls |
|---|---|---:|
| [reanalysis_20260914](reanalysis_20260914/ASSESSMENT.md) | Phase 2 within-arm reanalysis; PD post-hoc | 0 |
| [integrated_20260916](integrated_20260916/ASSESSMENT.md) | redundancy, AW sensitivity, portability | 0 |
| [pd_prospective_r1](pd_prospective_r1/ASSESSMENT.md) | **prospective PD test PASSED** | 736 |

**Accounting at closure: Claude $19.692970000/$32, OpenAI $5.977333725/$30.**
Usage estimates, not verified provider balances. The $100 package cap is
unchanged.

---

## What is NOT closed

- **Human resemblance** — the unmet deliverable, deferred by instruction.
- **PD cross-model** — flat on haiku; a haiku PD test would need items that
  disperse there, which exist (the six-item haiku set) but were not run.
- **The permutation question** — r2's null stands; needs ~840 pairs and a review
  protocol that does not flip on identical materials.
- **The other nine coordinates** — none manipulated; no prospective test exists
  for any of them.
- **The thesis §5.3 configuration counterfactual** — never run in Phase 4 or 5.
- **Concept separability** as opposed to sampler separability.

No phase is reopened and no completed result is altered by this closure. The
original Phase 5 ambition — a full integrated analysis including human
behavioural comparison — is **not** claimed complete. This closes Phase 5 for the
stated scope, with its unmet deliverable named.
