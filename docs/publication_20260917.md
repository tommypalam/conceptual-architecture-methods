# Publication record, 17 September 2026

The researcher authorised publishing the Phase 4B and Phase 5 closures, the
cross-model result and the prospective PD test to `main`, preserving the previous
published `main` as `backup-5`.

## Branch targets

| Branch | Commit | Meaning |
|---|---|---|
| `backup` | `c8e7aa0b` | Original published main; retained unchanged |
| `backup-1` | `aaed0a8d` | Second published main; retained unchanged |
| `backup-2` | `470d5cb6` | Third published main; retained unchanged |
| `backup-3` | `674e76d1` | Fourth published main; retained unchanged |
| `backup-4` | `d8cae32a` | Fifth published main; retained unchanged |
| `backup-5` | `f8d52c97` | **New.** The published main immediately before this release |
| `main` | fast-forwarded | Now carries both closures, the cross-model result and the PD test |
| `research-transfer-design-20260913` | development | Source branch; pushed for continuity |

`main` was an ancestor of the development branch, so the update is a
fast-forward. No history was rewritten, force-pushed or reset.

---

## Two phases closed

### Phase 4B — [closure record](../experiments/phase4_coding/PHASE4B_CLOSURE_2026-09-16.md)

**Parameter profiles change the deterministic good/bad classification on two
models from different providers. An explicit ethical instruction does not.**

| Model | U | G | E | paired E−G | Holm |
|---|---:|---:|---:|---:|---:|
| `claude-haiku-4-5` | 0.367 | 0.429 | 0.600 | +0.171 | 0.000112 |
| **`gpt-5.4-mini`** (calibration) | 0.395 | **0.378** | **0.606** | **+0.228** | **≈ 0** |

The G arm states the target behaviour in plain English — weigh everyone's
interests, avoid harm, deception, coercion and unequal treatment — and **on the
calibration model lands below the unprofiled baseline** (−0.017, p = 0.712).
Prespecified same-item subgroup across both models: **+0.255, p < 10⁻⁷**.

### Phase 5 — [closure record](../experiments/phase5_analysis/PHASE5_CLOSURE_2026-09-16.md)

**Closed for a scoped objective.** Three of four spec deliverables met; **human
resemblance is NOT met** and is not retrospectively passed.

---

## The headline addition: the prospective PD test passed

[`pd_prospective_r1`](../experiments/phase5_analysis/pd_prospective_r1/ASSESSMENT.md)
— 736 calls, 736/736 valid, zero failures.

| Arm | Good-rate | n | vs U | p |
|---|---:|---:|---:|---:|
| **PD−** (0.1, outcome-dominant) | 0.382 | 280 | −0.041 | 0.431 |
| **U** (no profile) | 0.423 | 175 | — | — |
| **PD+** (0.9, process-dominant) | **0.729** | 280 | **+0.306** | **< 10⁻⁸** |

Paired **+0.346**, pooled Holm ≈ 0, **6 of 7 items positive**, five surviving
individual correction.

**The entire manipulation is one line:**

```
- 6. Procedural Dependence: 0.10
+ 6. Procedural Dependence: 0.90
```

Verified across all 40 agents: exactly two diff lines, nine other coordinates
identical, user text byte-identical.

**The direction was locked from theory before any call**, derived from the
coordinate's definition rather than from a measured correlation. PD's dominance
has been flagged **post-hoc** since the Phase 2 reanalysis, which recorded that
it required *"prospective test before any confirmatory language"*. Four prior
attempts reached the profiled stage zero times. **It is no longer post-hoc**, and
at +0.346 it is the largest effect the project has measured.

---

## Also published

**[Three-model variance decomposition](../experiments/phase4_coding/phase4b_grand_r1/ASSESSMENT.md)**
— 901 calls, payoff structure frozen identical in all 36 cells. Good-rate
variance: items 44.4%, models 32.1%, interaction 23.5%.

**[Integrated analysis](../experiments/phase5_analysis/integrated_20260916/ASSESSMENT.md)**
— zero API calls. Addresses critical open problem 6 (the ten coordinates are
separable **as sampled**: 9 of 10 components for 90% of variance, min eigenvalue
0.621) and problem 8 (**no stable coordinate ordering**, even within a model),
and runs the **AW sensitivity check** CLAUDE.md asked for — AW is inert and not
load-bearing for any result.

**[A third model where the question cannot be asked](../experiments/phase4_coding/phase4b_sonnet_r1/ASSESSMENT.md)**
— on `claude-sonnet-4-6` every dispersing item sits within 0.12 of a bound (mean
headroom 0.080 against haiku's 0.293). Abandoned on a power analysis rather than
run underpowered.

**[The permutation control](../experiments/phase4_coding/phase4b_permutation_r2/ASSESSMENT.md)**
— same ten numbers deranged across labels. U 0.400, P 0.475, E 0.564. A scrambled
block does not clear baseline (p = 0.122); a correctly-labelled one does
(p = 0.00074); the difference is +0.089 at pooled Holm 0.084 and **fails the
prespecified rule**. The caveat stands, published standing.

**A three-level authoring criterion** derived from five review stops and enforced
in code, and **screen-before-profiling applied per model prospectively** — gate
and screen stops cost roughly $0.55 and prevented on the order of 2,000 calls on
cued or saturated stimuli.

---

## An unplanned methods finding

**AI design review returned opposite verdicts on byte-identical material.**

`phase4b_permutation_r2` and `r3` reviewed the identical seven-item packet with
the identical prompt. r2: **accept**, zero blocking issues, `rest_break`
explicitly "a limit rather than a blocker". r3: **revise**, blocking on
`rest_break` and `on_call`. `pd_prospective_r1` then accepted the same packet
again.

Across the item set: eight reviews, **four accepts and four revises**, on
overlapping and in places identical material.

The 16 September amendment was written from evidence across *different*
designations. This is the tighter demonstration, and `permutation_r3` was
**stopped rather than pushed through** — invoking the advisory amendment there
would have been selective, since an earlier reject is what caused an item to be
dropped.

---

## What is explicitly NOT established

- **No human resemblance.** No human data exists. Raters deferred by the
  13 September instruction. Phase 5's fourth deliverable is **unmet**.
- **No moral truth and no moral improvement.** Every label is a deterministic
  classification under stipulated standards, computed from stipulated
  transitions and never read from agent text.
- **Not that the profile is understood.** The permutation control did not clear
  this; the effect appears split between block-presence and label-mapping. The PD
  result pressures the cue account without retiring it.
- **Not that PD is understood as a concept**, only that its value in a labelled
  field moves behaviour in the predicted direction.
- **Nothing about the other nine coordinates**, held constant in the PD test.
- **PD is not cross-model** — flat on haiku (r = +0.089).
- **Not generalisation.** Six to eight items per designation, 40 agents per arm.
- **Concept separability is untested**; only sampler separability is shown.
- **`on_call` ran negative** in the PD test (−0.150) and is reported rather than
  smoothed.

## Accounting

**Claude $19.692970000/$32, OpenAI $5.977333725/$30.** Usage estimates, not
verified provider balances. The $100 package cap is unchanged.

Three preserved failures across these designations, none retried:
`phase4b_screen_r2/screen/tool_library/5`,
`phase4b_sonnet_r1/profiled/E/17/ward_transfer`, and one inherited from
`capstone_model2`.

## Not published

The thesis explorer UI (`viewer/explore.*`, `viewer/thesis-evidence.json`,
`code/build_thesis_explorer.py`, `tests/check_thesis_explorer.cjs`) remains
untracked. Its evidence file predates this session's work and would ship stale
evidence. It is held locally until regenerated.

Raw per-call records and archives remain excluded from Git as usual; checksums
are committed with each release.

## Next

**Phase 6 — paper and release.** Nothing in this publication authorises a new
paid run.
