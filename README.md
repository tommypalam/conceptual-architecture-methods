# PARIA — Concepts as Architecture

**Can explicit ethical parameters shape how an AI agent makes decisions, and where
does that shaping stop?**

PARIA encodes five political-ethical concepts — freedom, justice, authority, care
and loyalty — as ten uncertainty-aware parameters, samples agents from their joint
distribution, and measures whether the resulting profiles change decisions in
fixed dilemmas.

**Author:** Tommaso Piero Palamenga, Bocconi University.
**Supervisor:** Dr. Abhinav. **Co-supervisor:** Prof. Arnaldo Camuffo.

Moving to another computer? Start with the [desktop handoff](docs/desktop_handoff.md).

---

## What the evidence shows

Three findings, each with its boundary stated.

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

## What is *not* established

Stated plainly, because the project's value depends on the distinction:

- **No intrinsic ethical understanding.** Behavioural influence is not comprehension.
- **No human resemblance.** Human behavioural comparison (Phase 3B) is unresolved.
- **No moral quality claim.** No agent action has been assigned a moral score.
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
context; this repository's empirical claims concern PARIA only.
