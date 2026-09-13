# PARIA - Concepts as Architecture

Moving to another computer? Start with the [desktop handoff](docs/desktop_handoff.md).

Can explicit ethical parameters shape how an AI agent makes decisions?
PARIA studies this using ten normatively motivated parameters and fixed dilemmas.

**Author:** Tommaso Piero Palamenga, Bocconi University.

**Supervisor:** Dr. Abhinav. **Co-supervisor:** Prof. Arnaldo Camuffo.

## Start here

| Order | Read | What you will learn |
|---|---|---|
| 1 | [Abstract](docs/abstract.md) | The research question and main contribution |
| 2 | [Results and interpretation](docs/phase1_5_results.md) | What the completed experiments show and where the evidence stops |
| 3 | [Current status and next steps](NEXT_STEPS.md) | What is finished and what comes next |
| 4 | [Theory and specification](Theory/README.md) | The original argument and operational design |
| 5 | [Experimental evidence](experiments/README.md) | Reports, protocols and supporting studies |

## Current position

Phase 0 is closed and Phase 1 passed operationally. **Phase 1.5 is closed for the
accepted limited objective:** explicit normative profiles can systematically
influence generated decisions under the tested conditions, with replicated
Procedural Dependence effects providing the strongest evidence.

The original full validity battery remains unmet. Ethical understanding and
validation of the complete ten-parameter architecture are not established.
The narrower conclusion was accepted after observing the results; this is
recorded in the [closure decision](experiments/phase1_5_encoding_validity/ACCEPTED_CLOSURE_2026-09-12.md).
The amended **Phase 2 behavioural study is complete** after an exploratory pilot
and independent confirmation: 400 fresh profiles, 4,800 individual responses,
300 group runs and 11,005 confirmation responses in total. All six primary
individual profile/context contrasts and one of seven secondary group contrasts
passed their respective multiple-test corrections. Read the
[Phase 2 assessment](experiments/phase2_confirmation_20260913/ASSESSMENT.md).
Combined pilot-plus-confirmation accounting is $22.91, below the $100 cap.
Human benchmarking and validated moral scoring remain Phases 3 and 4. The
original full ten-environment Phase 2 design is not claimed complete.

## Watch the agents interact

The [simulation theatre](viewer/README.md) replays all 300 completed Phase 2
group runs with a visual table, round controls, full responses, agent profiles,
amendments and evidence sharing. Run `py -3.11 -B code/serve_replay.py` and open
http://127.0.0.1:8765. It reads your local records and makes no API calls.

## Find your way around

| Area | Contents |
|---|---|
| [Writing and planning](docs/README.md) | Manuscript drafts, research plan and project guides |
| [Theory](Theory/README.md) | Versioned thesis and implementation specification |
| [Experiments](experiments/README.md) | Locked questions, completed studies and original records |
| [Code](code/README.md) | Engine, entry points and reproducibility tools |
| [Configuration](config/README.md) | Parameters, correlations, contexts and seeds |
| [Prompts](prompts/README.md) | Canonical template and links to approved variants |
| [Archive](archive/README.md) | Historical material organised by phase |

The [layout and naming guide](docs/project_layout.md) explains folder conventions.
[AGENTS.md](AGENTS.md) and [CLAUDE.md](CLAUDE.md) contain the matching working rules.
Existing study names and frozen paths remain stable for reproducibility.

The wider [Cognitive Hexagon programme](docs/research_programme.md) supplies context;
this repository's empirical claims concern PARIA only.
