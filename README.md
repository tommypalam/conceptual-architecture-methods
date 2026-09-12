# Concepts as Architecture / PARIA

A probabilistic framework for testing whether explicit political-ethical concepts
can shape distinguishable, interpretable behaviour in LLM-based agents.

**Author:** Tommaso Piero Palamenga, Bocconi University.
**Supervisor:** Dr. Abhinav. **Co-supervisor:** Prof. Arnaldo Camuffo.
**Research in progress:** thesis v0.6 and implementation specification v0.1.

## Research question

Can psychologically grounded definitions of **freedom, justice, authority, care,
and loyalty** be encoded into uncertainty-aware parameter profiles that generate
systematic differences in individual decisions and collective outcomes?

The architecture represents agents with ten parameters on [0,1], Beta marginals,
and a Gaussian copula. Societal contexts occupy a five-axis binary configuration
space. The planned proof-of-concept compares a fixed population across 8–12 of
32 configurations, using three individual dilemmas and three collective tasks.
Conceptual mappings, distributional assumptions, and normative scoring are
hypotheses to evaluate, not established properties of human or artificial minds.

## Current state

**Phase 0 is closed; Phase 1 passed operationally; Phase 1.5 is open and the
full validity gate remains unmet. Phase 2 remains on hold.** The researcher
rejected the earlier closure interpretation and clarified the goal: determine
whether normative parameters systematically shape AI decisions under specified
conditions. See the [current objective](experiments/phase1_5_encoding_validity/NORMATIVE_ENCODING_OBJECTIVE_2026-09-12.md).
The researcher has authorised [structural diagnostics and an all-parameter sweep](experiments/phase1_5_encoding_validity/structural_encoding_20260912/PROTOCOL.md)
within a $25 reservation cap. The theory remains unchanged.

The original battery collected 39,000 unique behavioural responses (38,993 valid)
and a separate 200-item audit. Only 8/30 paraphrase cells establish equivalence
(24 required); representation retention and active-trait recovery remain
insufficient. Later targeted studies establish useful local parameter influence:
a final 360-response test supports MoR and MS endpoint effects across 20 new
complete backgrounds. MS does not show an ordered gradient, and RE remains
unresolved. These findings do not establish internal ethical understanding or
validate the complete ten-parameter architecture.

[NEXT_STEPS.md](NEXT_STEPS.md) owns current execution status;
all positive, negative and inconclusive evidence is retained. The interrupted
September 6 sample remains separate from the fresh battery.

Completed calibration exposed substantial prompt-harness effects on the tested
model. The locked holdout therefore supplies measured, problem-specific naked
baselines, rather than an assumed 50/50 reference. These findings and the
operational pilot do not yet establish encoding validity, human behavioural
validity, or moral competence.

## Read in this order

| Document | Purpose |
|---|---|
| [Provisional paper abstract](docs/abstract.md) | Concise account of the complete research programme, with completed and planned work distinguished |
| [Current status and next steps](NEXT_STEPS.md) | Phase ledger, interrupted run, and actionable dependencies |
| [AGENTS.md](AGENTS.md) / [CLAUDE.md](CLAUDE.md) | Matching project constitutions and working rules |
| [Documentation index](docs/README.md) | Theory, protocols, evidence, archives, and wider programme |
| [Decision log](meta.md) | Current decisions and pointers to historical records |

## Methods and planned evaluation

- **Encoding validity:** parameter sweeps, independent blind reasoning coding,
  paraphrase equivalence, and numeric/verbal/hybrid prompt comparisons.
- **Main experiments:** paired-agent individual decisions and multi-round
  collective tasks with explicit parameter reinjection.
- **Behavioural benchmarks:** obedience, conformity, ultimatum bargaining,
  bystander helping, and reactance; canonical and decanonised scenarios with
  predicted-high versus predicted-low configuration contrasts.
- **Moral evaluation:** an extended-MACHIAVELLI configuration-relative taxonomy
  alongside a fixed-standard score, subject to a reviewed coding manual and
  independent rater validation.
- **Inference:** prespecified mixed-effects comparisons, multiplicity control,
  and sensitivity to distributions, dependencies, and model choice.

Phases 2–6 remain pending. The main-study analysis plan and coding manual must
be finalised and preregistered before Phase 2. No preregistration is claimed.

## Code and verification

`code/engine/` contains the simulation components and validity modules;
`code/run_*.py` contains the command-line entry points. Historical calibration
scripts remain executable provenance. `experiments/` holds locked prompts,
manifests, and evidence; raw call artifacts remain local and are not part of
the new Git publication.

Run from this repository root in the existing Python environment:

```powershell
python -B -m pytest tests/test_validity.py tests/test_validity_followup.py -q -p no:cacheprovider
```

For exact execution commands and dependencies, see the
[delivery protocol](docs/phase1_5_execution.md) and
[follow-up tools](docs/phase1_5_followup.md). Real API calls require credentials
in environment variables. Mock execution is the default. Never change the model,
prompts, or sampling plan inside a frozen run.

## Scope and sources

The [thesis](Theory/concepts_as_architecture_thesis_v0_6.md) defines the architecture;
the [implementation specification](Theory/implementation_specification_v0_1.md)
defines the original operational plan. Recorded amendments and phase closure
decisions govern what was actually executed. Versioned source documents are
retained rather than rewritten to imply that their planned studies occurred.

PARIA belongs to the wider [Cognitive Hexagon programme](docs/research_programme.md).
This repository's empirical claims concern PARIA only.
