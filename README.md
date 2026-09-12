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

**Phase 0 is closed; Phase 1 passed operationally; Phase 1.5 is closed for the
researcher-accepted limited encoding objective.** The original full validity gate
remains unmet. The broader Phase 2 design has not been released or run.
[Accepted closure](experiments/phase1_5_encoding_validity/ACCEPTED_CLOSURE_2026-09-12.md).

The evidence supports initial functional normative parameterization: explicit
profiles can systematically influence generated decisions in the tested model,
harness and dilemmas. Procedural Dependence has independent endpoint confirmation
and later canonical/verbal effects. Ethical understanding and complete ten-parameter
validity remain unestablished. All ten parameters and mixed findings stay reported.

The structural package contains 3,580 valid behavioural responses and 200 valid
blind codings. Its all-ten follow-up dispatched 17,250 requests, saving 17,247
records, 17,234 valid. Missingness and failures remain explicit. The earlier
39,000-response battery remains separate; its 8/30 paraphrase result did not
meet the original 24/30 criterion. No original result or threshold is revised.
[Complete all-ten assessment](experiments/phase1_5_encoding_validity/all_ten_assessment_20260912/ASSESSMENT.md).

The researcher accepted a limited possibility claim after seeing the results.
This is a disclosed scope decision, not a retrospective battery pass. The
[results draft](docs/phase1_5_results.md) and [abstract](docs/abstract.md) state
that conclusion and its limits. [NEXT_STEPS.md](NEXT_STEPS.md) owns the current
ledger. No further paid Phase 1.5 run is queued.

Locked Phase 0 calibration exposed substantial harness effects; its measured,
problem-specific baselines remain in force. Theory, parameter meanings, Beta
marginals, correlations and locked questions are unchanged.

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
