# Phase 5 integrated analysis — 16 September 2026

**Zero API calls. No budget change. No frozen record altered. Accounting
unchanged.** Reproduce via `code/phase5_integrated.py`.

Spec §1.2 defines Phase 5 as: *"Relate representations, behaviour, human
resemblance and moral outcomes; report sensitivity and failure cases. Follows
available evidence."*

## What this reads

The three Phase 4B designations carrying agent-level coordinates alongside
decisions — two models, three **independent** population draws:

| Designation | Model | Agents | E-arm decisions |
|---|---|---:|---:|
| `phase4b_profiled_r1` | `claude-haiku-4-5` | 40 | 240 |
| `phase4b_gpt_r2` | `gpt-5.4-mini` | 40 | 320 |
| `phase4b_permutation_r2` | `gpt-5.4-mini` | 40 | 280 |

840 profiled decisions with known ten-coordinate vectors, plus their U, G and P
comparison arms — 2,205 decisions in total.

## EVERYTHING HERE IS POST-HOC AND EXPLORATORY

These data were collected to answer the Phase 4B **arm** question. **No
coordinate was manipulated**; all ten varied freely by draw. Nothing in this
analysis can confirm a hypothesis, and at n = 40 agents per designation a null
across the ten is the expected result.

The Phase 2 reanalysis set this precedent and its warning: PD's dominance there
was a post-hoc discovery *"requiring prospective test before any confirmatory
language."* **That rule binds everything below.**

---

## Q1 — Coordinate association

Correlation between each coordinate and the agent's E-arm good-rate,
Holm-corrected within each family of ten.

| Designation | Top coordinate | r | Holm | Survives |
|---|---|---:|---:|---|
| `phase4b_profiled_r1` (haiku) | MS | −0.381 | 0.152 | **none** |
| `phase4b_gpt_r2` | **PD** | **+0.406** | 0.094 | none |
| `phase4b_permutation_r2` | **PD** | **+0.522** | **0.005** | **PD** |

**PD is the top-ranked coordinate in both gpt designations**, and survives Holm
correction in one of them. That is the same parameter the Phase 2 reanalysis
found ranking first of ten under multivariate control.

### The qualification that matters

`phase4b_gpt_r2` and `phase4b_permutation_r2` use **independent agent draws**
(seeds 2026091687 and 2026091693) but **overlapping item sets** — 7 of 8 items
shared, `sample_draw` excluded from the second on review.

So this is a **partial replication across agents, not two independent
observations.** The agents differ; the items largely do not.

**And on haiku, PD is essentially zero: r = +0.089, Holm 1.000.** Whatever this
is, it is not a model-general coordinate effect.

**Pooling does not help.** The pooled family survives nothing, which is expected:
the three designations differ in model, item set and arm structure, so pooling
mixes incomparable cells rather than adding power.

---

## Q2 — Parameter redundancy (critical open problem 6)

*"Phase 1.5 sweeps + Phase 5 factor analysis test empirical separability."*

Across all 120 drawn agents:

- **No pair reaches |r| ≥ 0.4.** The strongest pairwise correlations in the
  realised draws are weak.
- **9 of 10 principal components are needed for 90% of variance.**
- **Minimum eigenvalue 0.621**, comfortably positive-definite.

**The ten coordinates are empirically separable in these draws.** They do not
collapse onto a smaller set.

**Boundary:** this tests the *sampler*, not the *concepts*. It shows the Gaussian
copula over ten Beta marginals produces near-independent draws — which is what it
was built to do. It does **not** show the ten concepts are distinct in the
model's behaviour, which would need coordinate-level manipulation.

---

## Q3 — AW sensitivity

CLAUDE.md flags AW as **preliminary**: *"Beta calibration and R-row not directly
anchored; subject to AW on/off sensitivity in Phase 5."* This is that check.

| Designation | AW r | AW Holm | Conclusions changed by dropping AW |
|---|---:|---:|---|
| `phase4b_profiled_r1` | +0.016 | 1.000 | none |
| `phase4b_gpt_r2` | −0.051 | 1.000 | none |
| `phase4b_permutation_r2` | −0.167 | 1.000 | none |

**AW is inert in all three, and removing it changes no conclusion.** Its weakest
association is −0.167 and none approaches significance.

This neither vindicates nor condemns AW. It shows that in these data AW carries
no detectable association with the moral headline, and that the other nine
coordinates' results do not depend on its inclusion. **AW remains preliminary.**

---

## Q4 — Portability (critical open problem 8)

*"All calibration is on gpt-5.4-mini; portability tested in Phase 5."*

Rank agreement between designations, ordering the ten coordinates by |r|:

| Pair | Rank correlation | Top-3 overlap |
|---|---:|---:|
| `gpt_r2` ~ `profiled_r1` (cross-model) | +0.430 | 2/3 |
| `gpt_r2` ~ `permutation_r2` (same model) | −0.054 | 1/3 |
| `permutation_r2` ~ `profiled_r1` (cross-model) | −0.406 | 0/3 |

**There is no stable coordinate ordering.** Two designations on the *same model*
agree no better than chance (−0.054), and one cross-model pair is *negatively*
correlated.

**This is the expected result** at n = 40 agents with no manipulation, and it is
the clearest statement available of what these data can and cannot support: the
arm-level effect is robust and replicates across models, while the
**coordinate-level structure is not resolved at this sample size.**

---

## What this establishes

**The ten coordinates are empirically separable as sampled** — problem 6 is
addressed for the sampler, not for the concepts.

**AW's inclusion is not load-bearing for any result reported** — the sensitivity
check CLAUDE.md asked for, answered.

**No coordinate-level claim is supportable at this n.** Rank orderings do not
agree even within a model. Any coordinate story told from these data would be
noise-fitting.

**PD is the one coordinate worth a prospective test.** It ranks first in both gpt
designations, survives correction in one, and matches the Phase 2 reanalysis
finding — but on partially shared items, and absent on haiku.

## What this does NOT establish

- **No confirmed coordinate effect.** Post-hoc, uncorrected across designations,
  with no coordinate manipulated. PD included.
- **Not a test of the concepts' separability**, only of the sampler's.
- **Not human resemblance.** Spec §1.2 names it; no human data exists and human
  raters remain deferred.
- **Not moral truth or moral quality.** Every label is a deterministic
  classification under stipulated standards.
- **Not generalisation.** Three designations, two models, 120 agents, six to
  eight items each.

## What a prospective PD test would need

The project has attempted this four times —
[`pd_endpoint_r2`](../../phase3_benchmarks/), `pd_gradient_r1`–`r5`,
[`pd_discriminant_r1`](../../phase4_coding/pd_discriminant_r1/ASSESSMENT.md) and
[`r2`](../../phase4_coding/pd_discriminant_r2/ASSESSMENT.md) — and reached the
profiled stage **zero times**, stopped each time by its own dispersion screen.

What is new since those attempts: **Phase 4B produced an item set that disperses
and is review-cleared**, and `phase4b_grand_r1` measured baselines for it on three
models. A PD-manipulated arm on that item set — PD pinned high against PD pinned
low, nine coordinates held identical, on the six items that disperse on haiku or
the seven on gpt — is the design the earlier attempts could not build.

The prediction remains **untested, not failed**. Nothing here authorises the run.
