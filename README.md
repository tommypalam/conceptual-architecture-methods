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

**Phase 0 is closed; the Phase 1 operational pilot passed; Phase 1.5 validity
remains open.** The original September delivery comparison stopped at
**8,640/15,000 records** after an API credit-balance error. A user-authorised
[fresh September 9 restart](docs/phase1_5_restart_20260909.md) now has all 15,000
source calls, 4,500 representation comparisons and the 200-item independent audit
collected and scored. The earlier sample remains separate; paraphrases and the
combined scientific assessment are pending. Audit numerical thresholds alone do
not establish recovery of manipulated traits.
The remaining validity tools are implemented and offline-tested; their empirical
tests have not passed. [NEXT_STEPS.md](NEXT_STEPS.md) owns the detailed current
status, blockers, and next actions.

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
