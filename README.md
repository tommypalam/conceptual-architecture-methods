# Concepts as Architecture

**A Probabilistic Framework for Encoding Political-Ethical Concepts in Normative AI Agents**

**Can explicit ethical parameters shape how an AI agent makes decisions, and where
does that shaping stop?**

Concepts as Architecture encodes five political-ethical concepts — freedom, justice, authority, care
and loyalty — as ten uncertainty-aware parameters, samples agents from their joint
distribution, and measures whether the resulting profiles change decisions in
fixed dilemmas.

**Author:** Tommaso Piero Palamenga, Bocconi University.
**Supervisor:** Prof. Arnaldo Camuffo.

> **The thesis is [`docs/thesis/LF3262767.pdf`](docs/thesis/LF3262767.pdf).**

**Two outputs, two branches:** the thesis is submitted and frozen; the paper is
live and may contradict it. See [docs/PROJECT_SPLIT.md](docs/PROJECT_SPLIT.md).
> It is the single canonical PDF, built from
> [`docs/thesis/thesis.md`](docs/thesis/thesis.md) by
> [`docs/thesis/build/build.ps1`](docs/thesis/build/build.ps1) and checked against the
> university's format rules by [`verify.py`](docs/thesis/build/verify.py). Its claim in
> one line: **Procedural Dependence is the only verified field effect;
> Internalisation Dependence is a candidate; Legitimacy Locus is withdrawn and
> unresolved; Affective Weighting was never independently pinned.**

New here? [`docs/README.md`](docs/README.md) is the map. Moving to another computer?
Start with the [desktop handoff](docs/handoffs/desktop_handoff.md).

---

## What the evidence shows

**Headline: a numeric parameter profile changes the deterministic good/bad
classification on two models from different providers. An explicit ethical
instruction, on the same items against the same baseline, does not.**

| Model | no profile | ethical guidance | **numeric profile** | paired E−G | Holm |
|---|---:|---:|---:|---:|---:|
| `claude-haiku-4-5` | 0.367 | 0.429 | **0.600** | +0.171 | 0.000112 |
| `gpt-5.4-mini` (calibration) | 0.395 | **0.378** | **0.606** | **+0.228** | **≈ 0** |

The guidance arm states the target behaviour in plain English — weigh everyone's
interests, avoid harm, deception, coercion and unequal treatment. **On the model
this project is calibrated on it lands *below* the unprofiled baseline**
(−0.017, p = 0.712) while a profile containing numbers and endpoint explanations moves the
headline by +0.21. This establishes no moral improvement or general superiority over verbal instructions.

Prespecified same-item subgroup, the five items dispersing on both models:
**+0.255, p < 10⁻⁷**.

Items were screened for dispersion **before any profiled call**, with payoffs
frozen identical across the whole pool, under a three-level authoring criterion
derived from five independent review stops and enforced in code.
→ [Phase 4B closure](experiments/phase4_coding/PHASE4B_CLOSURE_2026-09-16.md) ·
[calibration-model result](experiments/phase4_coding/phase4b_gpt_r2/ASSESSMENT.md) ·
[three-model screen](experiments/phase4_coding/phase4b_grand_r1/ASSESSMENT.md)

**One coordinate is causally load-bearing, and the direction was predicted from
theory.** Procedural Dependence is defined as 0 = outcome-dominant, 1 =
process-dominant. Pinning it to each endpoint while holding the other nine
identical — a one-line change to the prompt:

| Arm | Good-rate | vs no profile | p |
|---|---:|---:|---:|
| PD− (0.1, outcome-dominant) | 0.382 | −0.041 | 0.431 |
| no profile | 0.423 | — | — |
| **PD+ (0.9, process-dominant)** | **0.729** | **+0.306** | **< 10⁻⁸** |

Paired **+0.346**, pooled Holm ≈ 0, 6 of 7 items positive. **The prediction was
locked in source before collection**, derived from the coordinate's definition
rather than from any measured correlation — and PD's dominance, flagged as
post-hoc since Phase 2 and never prospectively tested in four attempts, is
no longer post-hoc.
→ [prospective PD test](experiments/phase5_analysis/pd_prospective_r1/ASSESSMENT.md) ·
[Phase 5 closure](experiments/phase5_analysis/PHASE5_CLOSURE_2026-09-16.md)

**Which of the ten concept-parameters actually carry the behaviour? PD is verified; ID is a candidate after item-heterogeneity and direct binding checks.** Each coordinate was pinned to its endpoints with the other nine
held identical, Holm-corrected over all eight contrasts as one family. Every
survivor then had to pass a label-swap control at 40 agents:

| Coordinate | Pinned effect | Swap control | Verdict |
|---|---:|---|---|
| **Procedural Dependence** | **+0.339** | **−0.036**, n.s. | **verified label effect** |
| **Internalisation Dependence** | **+0.111 to +0.143** | binding difference +0.064, CI includes zero | **candidate; binding not established** |
| ~~Legitimacy Locus~~ | −0.131, then **−0.014** | uninterpretable | **did not replicate — withdrawn** |
| six others | −0.10 to +0.05 | — | unit-bootstrap bounds below 0.20 on tested items |
| AW | never independently pinned | partner estimates include zero | no effect detected at tested power |

The six equivalence bounds are post-hoc and conditional on the unit-bootstrap analysis and tested items; they are not universal or simultaneous guarantees. LL remains unresolved. AW was not independently pinned.
→ [coordinate sweep](experiments/phase5_analysis/coordinate_sweep_r2/ASSESSMENT.md) ·
[verification](experiments/phase5_analysis/label_semantics_r2/ASSESSMENT.md)

**Both coordinates move the outcome on a second provider under the prespecified tests.** Each coordinate was
pinned to its endpoints on `claude-haiku-4-5`, 40 agents, six items:

| Coordinate | gpt | haiku | p (haiku) | Prediction |
|---|---:|---:|---:|---|
| **Procedural Dependence** | +0.346 | **+0.133** | **0.0003** | **one-sided, from theory** |
| **Internalisation Dependence** | +0.111 | **+0.075** | **0.033** | two-sided |

PD's is the stronger test: its direction was locked one-sided from the
coordinate's definition before collection, and the derivation's premise was
re-verified against the new item set rather than assumed to transfer. Both
effects **shrink** on haiku — what replicates is the direction and the decision
rule, not the magnitude.

And a second correlation pointed the wrong way: PD's post-hoc correlation on
haiku was **+0.089**, near flat. Pinned, it gives **+0.133**. Legitimacy Locus
ran the opposite way — correlation +0.271, manipulation negative then null.
Post-hoc correlations mislead in *both* directions.
→ [PD cross-model](experiments/phase5_analysis/pd_crossmodel_r1/ASSESSMENT.md) ·
[ID cross-model](experiments/phase5_analysis/id_crossmodel_r1/ASSESSMENT.md)

**One of the three survivors did not survive replication, and the design caught
it.** Legitimacy Locus was measured three times and gave three different answers:
**+0.271** as a correlation across unmanipulated profiles, **−0.131** pinned at 25
agents, and **−0.014** (Holm 0.708) pinned at 40. Positive, negative, null.

This is not a power failure — it failed on the *larger* sample, where power was
17/20 at an effect of the size previously measured. It is a coordinate that
cleared a Holm-corrected bar in one well-powered designation and then vanished.
Legitimacy Locus is **unresolved, not inert**, and it is no longer claimed.

The swap control carries a TRUE arm precisely so that this is visible: had the
control been run alone, Legitimacy Locus's null swap would have been read as
evidence that its label carries the effect.

**The open question, now answered for the coordinate that carries the effect.**
Is the model reading the *parameters*, or does any structured numeric block do
similar work? A one-binding control moved the same number between two labels,
holding the block, its length and all ten numerals identical:

| Arm | `0.9` sits on | Good-rate |
|---|---|---:|
| **TRUE+** | **Procedural Dependence** | **0.729** |
| **TRUE−** (0.1 there instead) | Procedural Dependence | 0.389 |
| **SWAP+** | Affective Weighting | 0.557 |
| **SWAP−** (0.1 there instead) | Affective Weighting | 0.593 |

**TRUE +0.339 (Holm ≈ 0). SWAP −0.036 (Holm 1.000).** Move the identical number
from one line to another and the effect vanishes. That rules out a formatting
cue, a verbosity effect and a response to numeric extremity — extremity was held
constant and moved.
→ [label-semantics control](experiments/phase5_analysis/label_semantics_r1/ASSESSMENT.md)

The same control was then run for the other two survivors. **Internalisation
Dependence did not establish a field binding.** Its TRUE arm replicated (+0.111,
Holm 0.0047) and its SWAP arm was not significant (+0.046) — but a significant
arm beside a non-significant one is not a test of the *difference* between them.
Tested directly, the TRUE-minus-SWAP difference is **+0.064, 95% interval
[−0.014, +0.146]**, which includes zero; for PD the same difference is +0.375
[+0.286, +0.464]. ID is therefore a **candidate**, not a verified field effect,
and an earlier reading here that it "passed" is withdrawn.
**Legitimacy Locus failed the replication gate** and nothing is claimed for it.

An earlier control that deranged **all ten** labels at once measured only +0.089
and [failed its rule](experiments/phase4_coding/phase4b_permutation_r2/ASSESSMENT.md);
the dilution explanation is now confirmed. The caveat is answered for one
coordinate, PD, not retired for all ten — and the swap's partner field, Affective
Weighting, was never independently pinned, so its neutrality is an estimate with
its own uncertainty rather than an established property.

**Boundaries, stated plainly.** This establishes no moral truth and no moral
improvement: every label is a deterministic classification under stipulated
standards, never read from agent text. It does not show the profile is
*understood* — see the open question above. A third model, `claude-sonnet-4-6`,
is one where the question **cannot be asked with these items** at all: every item
that disperses there sits within 0.12 of a bound, and that designation was
[abandoned on a power analysis](experiments/phase4_coding/phase4b_sonnet_r1/ASSESSMENT.md)
rather than run underpowered. Six to eight items is six to eight situations, and
no human has validated any of it.

---

Three further findings, each with its boundary stated.

**1. Profiles change decisions — and they create variance rather than shift it.**
A fresh-sample confirmation ran 400 hash-locked profiles through 4,800 individual
decisions and 300 group simulations. All six prespecified individual contrasts
survived Holm correction. Within-arm reanalysis then showed *why*: in four of six
cells the no-profile model chose the same option in **400/400 calls**, so profiles
introduced behavioural variance where none existed.
→ [Phase 2 assessment](experiments/phase2_confirmation_20260913/ASSESSMENT.md) ·
[within-arm reanalysis](experiments/phase5_analysis/reanalysis_20260914/ASSESSMENT.md)

**2. One parameter carries the effect, and theory named it in advance.**
Procedural Dependence — the outcome-versus-process axis — shows a monotone
dose-response on departure from the baseline choice (35 to 62 percentage points
across its quintiles, permutation p<0.0001) and ranks **first of ten parameters**
under multivariate control in every non-degenerate cell. Nine of ten coordinates
show no systematic effect. Of nine directional signs locked before collection,
five were supported and none pointed the wrong way.
→ [reanalysis](experiments/phase5_analysis/reanalysis_20260914/ASSESSMENT.md)

**3. You cannot hide a famous benchmark by re-skinning it.**
A 500-probe screen, dual-coded by raters from two different providers with
**500/500 exact agreement**, identified all five decanonised benchmark variants at
the same rate as their canonical originals. Structure-preserving domain
substitution does not conceal a classic paradigm — closing a contamination control
that is usually assumed rather than tested.
→ [recognition finding](experiments/phase3_benchmarks/recognition_r1/FINDING_INTERPRETATION.md)

**And a methodological result that explains four nulls at once.** Studies across
three phases returned null contrasts traceable to one cause: a task whose
unprofiled answer is deterministic cannot discriminate any arm comparison. The fix
is a baseline-dispersion pre-screen before committing any multi-arm budget.
→ [saturation diagnosis](experiments/phase5_analysis/reanalysis_20260914/SATURATION_DIAGNOSIS.md)

**4. Normative profiles change which moral standard gets sacrificed.**
On tasks built so the four fixed standards cannot all be satisfied, an explicit
profile moved the net-score good rate from 0.233 (no profile) to 0.750 (numeric)
and 0.900 (matched prose) on `witness_cost` - a paired within-agent difference of
+0.517, Holm-corrected p = 0.0002, with 34 agents switching toward the accurate
option and 3 away. Profiled arms deceived far less and accepted more harm, so the
profiles changed *which* standard was given up, not how many. A second task
showed no effect, and explicit ethical guidance underperformed the profiles.
Labels are deterministic classifications under stipulated standards, never AI or
human ratings.
-> [moral capstone](experiments/phase4_coding/moral_capstone_r1/ASSESSMENT.md) ·
[task screen](experiments/phase4_coding/moral_conflict_screen_r2/ASSESSMENT.md)

## What is *not* established

Stated plainly, because the project's value depends on the distinction:

- **No intrinsic ethical understanding.** Behavioural influence is not comprehension.
- **No human resemblance.** Human behavioural comparison (Phase 3B) is unresolved.
- **No moral truth.** Moral labels are deterministic classifications under
  standards this project stipulated, computed from stipulated transitions and
  never from agent text. A higher good rate is not evidence an agent is
  morally better. No AI or human rater assigns them.
  Human raters are deferred; AI agreement is never presented as human validation.
- **No validity for nine of ten parameters.** Only PD has a demonstrated mechanism.
- **No institutional-axis identification.** Both context anchors flip all five
  societal bits together, so single axes are confounded by design.
- **No completed original battery.** Phase 1.5's full encoding battery and the
  formal five-benchmark Phase 3 study remain unmet and are not retrospectively passed.
- **One model, one harness, one snapshot.** Portability is untested.

## Start here

| Order | Read | What you will learn |
|---|---|---|
| 1 | [Abstract](docs/abstract.md) | The research question and contribution |
| 2 | [Experimental evidence](experiments/README.md) | Every study, in reading order, with its limits |
| 3 | [Current status and next steps](NEXT_STEPS.md) | What is finished, what is open, what is proposed |
| 4 | [Theory and specification](Theory/README.md) | The argument and the operational plan |

## Watch the agents interact

The [simulation theatre](viewer/README.md) replays all 300 completed group runs in
explorable 3D rooms, with matched comparison, round controls, full responses,
profiles, amendments and evidence sharing.

```
py -3.11 -B code/serve_replay.py     # then open http://127.0.0.1:8765/lab
```

It reads local records and makes no API calls. The classic 2D viewer is at `/`.

## Reproduce the analysis

```
py -3.11 -B code/phase5_reanalysis.py    # within-arm reanalysis, zero API calls
```

Deterministic under seed 20260914; writes
`experiments/phase5_analysis/reanalysis_20260914/dispersion_results.json`.

## Find your way around

| Area | Contents |
|---|---|
| [Writing and planning](docs/README.md) | Abstract, plan and project guides |
| [Theory](Theory/README.md) | Versioned thesis and implementation specification |
| [Experiments](experiments/README.md) | Locked questions, completed studies, original records |
| [Code](code/README.md) | Engine, entry points and reproducibility tools |
| [Configuration](config/README.md) | Parameters, correlations, contexts and seeds |
| [Prompts](prompts/README.md) | Canonical template and approved variants |
| [Archive](archive/README.md) | Historical material organised by phase |

## Conventions

The [layout and naming guide](docs/project_layout.md) explains folder conventions.
[AGENTS.md](AGENTS.md) and [CLAUDE.md](CLAUDE.md) carry the matching working rules.

Frozen study paths, locked prompts and per-call record names are **never renamed** —
manifests, replay scripts and source hashes depend on them. Raw per-call records
are write-once. Raw data and archives are excluded from Git, so a clone is not the
dataset; off-device backup is unverified.

The wider [Cognitive Hexagon programme](docs/research_programme.md) supplies
context; this repository's empirical claims concern Concepts as Architecture only.
