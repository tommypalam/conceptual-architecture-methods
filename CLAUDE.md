# CLAUDE.md â€” PARIA Project Constitution

> Read this at the start of every session. Every line constrains behavior.
> Source of truth: `Theory/conceptual_architecture_methods_paper_v0_5_with_graphs.pdf` (Draft 0.5, April 2026).

---

## Purpose

PARIA tests whether canonical psychological definitions of five political-ethical concepts â€” freedom, justice, authority, care, and loyalty â€” can be encoded as uncertainty-aware parameter distributions that generate **distinguishable and interpretable** social dynamics in an LLM-powered agent-based simulation.

This is a **proof-of-concept thesis**, not a completed methodology. All design decisions are provisional until empirically validated. Claims are candidates for development, not established results.

---

## Unit of Analysis

Individual agents sampled from a 10-dimensional joint distribution, placed into one of 32 societal configurations (2âµ grid). One agent = one draw from the Gaussian copula over 10 Beta-marginal parameters.

---

## The Ten Agent Parameters

Every agent is a vector x = (xâ‚, ..., xâ‚â‚€), each xáµ¢ âˆˆ [0, 1].

| Code | Parameter | 0-endpoint | 1-endpoint | Beta(Î±, Î²) | Proxy Instrument |
|------|-----------|------------|------------|------------|-----------------|
| LL | Legitimacy Locus | internal endorsement | external/institutional | Beta(3.5, 2.5) | GCOS |
| CS | Constraint Sensitivity | low (influence = environment) | high (nudges = coercion) | Beta(2.5, 2.0) | HPRS |
| RT | Response Threshold | tolerant (reacts only to major violations) | hair-trigger | Beta(2.5, 2.5) | UG rejection thresholds |
| MoR | Mode of Response | internal/reflective adjustment | external/confrontational | Beta(2.0, 2.5) | STAXI / Thomas-Kilmann / IRI |
| RE | Relational Embedding | atomised, abstract-person | role-sensitive, socially embedded | Beta(2.0, 3.0) | Singelis SCS |
| PD | Procedural Dependence | outcome-dominant | process-dominant | Beta(2.5, 2.0) | Colquitt (2001) |
| TfA | Tolerance for Asymmetry | egalitarian (asymmetry suspect) | hierarchical (asymmetry accepted) | Beta(2.0, 3.5) | SDO7 |
| ID | Internalisation Dependence | surface compliance sufficient | requires genuine endorsement | Beta(3.0, 2.0) | SRQ |
| MS | Moral Scope | local / role-bound | universalised / broadly applied | Beta(1.8, 1.5) | MES (Crimston et al. 2016) / IWAH |
| AW | Affective Weighting | cognitive / deliberative / reasoned | affective / intuitive / felt | Beta(2.2, 2.5) | Davis IRI â€” EC/PT ratio |

> **Draft 0.5 parameter changes from v0.4:**
> - PLB renamed â†’ **LL** (Legitimacy Locus)
> - CAT renamed â†’ **RT** (Response Threshold)
> - SMG renamed â†’ **MS** (Moral Scope); primary anchor changed from MFQ-2 to MES
> - TO (Temporal Orientation) **dropped**; replaced by **AW** (Affective Weighting), Beta(2.2, 2.5)

---

## Canonical Concept Definitions

**Freedom** â€” subjective experience of volitional agency (SDT: autonomy, competence, relatedness) coupled with motivational disposition to resist perceived threats to agency (Psychological Reactance Theory, Brehm 1966).

**Justice** â€” cognitive-affective appraisal of proportionality between contributions and outcomes, evaluated through social comparison, sensitive to distributional AND procedural dimensions, generating corrective motivation when imbalance exceeds subjective threshold (Equity Theory + organisational justice framework).

**Authority** â€” perceived legitimacy of asymmetric social influence mediated by compliance (instrumental), identification (relational), and internalisation (value-congruent), modulated by expertise, institutional role, and proximity (Milgram + Kelman's three-process model).

**Care** â€” other-oriented concern for the welfare of those perceived as morally considerable, extended through affective mechanisms (empathic concern, felt compassion) and cognitive mechanisms (perspective-taking, reasoned beneficence), activated by cues of suffering or need, modulated by the perceived breadth of the moral circle and social-relational embedding (Davis IRI + Batson empathy-altruism hypothesis + MES).

**Loyalty** â€” sustained in-group commitment extending beyond instrumental calculation; disposition to maintain pro-group behaviour at personal cost, mediated by identification with group identity and, at its extreme, by fusion of personal and social identities; modulated by contextual cues of in-group legitimacy, ritual enactment, and perceived threat to the group (Swann et al. identity fusion theory + Kelman's three-process model).

---

## Thirty-Two Societal Configurations (2âµ grid)

Each configuration is (Freedom, Justice, Authority, Care, Loyalty) âˆˆ {0, 1}âµ.

The proof-of-concept tests a **defensible subset of 8â€“12 configurations** spanning the most antagonistic combinations, including the Milgram-analogue configuration (F=0, J=0, A=1, C=0, L=0 = `00100`) and its inverse, plus configurations that isolate each concept's effect.

> **Note:** The full 32-configuration space is reserved for later work.

**Primary validation target:** Configuration `00100` (Milgram-analogue) must produce obedience rates of 61â€“66%.

---

## Behavioural Benchmarks â€” One Per Concept

| Concept | Benchmark | Retrodiction target |
|---------|-----------|---------------------|
| Authority | Milgram (1974) obedience paradigm | 61â€“66% maximum-voltage obedience in authority-high config |
| Loyalty | Asch (1956) conformity paradigm | ~32â€“37% conformity on critical trials in loyalty-high config |
| Justice | Ultimatum Game (GÃ¼th et al. 1982) | Proposer offers 40â€“50%; rejection rate for 20% offers ~40â€“50% |
| Care | Bystander helping paradigm (LatanÃ© & Darley 1968) | ~75% helping alone; ~55% with 3+ bystanders in care-high config |
| Freedom | Reactance restoration (Worchel & Brehm 1970) | Option-attractiveness shift ~15â€“25% following removal; Cohen's d â‰ˆ 0.45 |

> **Stanford Prison Experiment: explicitly rejected** as benchmark. Qualitative pattern only, no quantifiable retrodiction target, documented methodological contamination. Role-transformation phenomenon addressed through C2 (Restructuring Board) instead.

---

## Implementation Stack

| Layer | Tool |
|-------|------|
| Bayesian encoding | PyMC |
| Joint distribution sampling | NumPy (`multivariate_normal`) + SciPy (`norm.cdf`, `beta.ppf`) |
| Agent-based simulation | Mesa |
| Data / aggregation | Python, pandas, NumPy |
| Visualisation | Plotly |
| Bayesian network (if needed) | pgmpy |
| Baseline calibration | OpenAI API (`gpt-5.4-mini`) |

---

## Current Phase Status

- Phase 0 â€” Baseline calibration (50/50 RLHF check via gpt-5.4-mini): **ACTIVE**
- Phase 1 â€” Foundations: **COMPLETE** (10 parameters + 5 canonical definitions)
- Phase 2 â€” Distribution Modelling: **SUBSTANTIALLY COMPLETE** (Beta marginals + copula R matrix)
- Phase 3 â€” System Architecture: **NEXT** (tool-based injection mechanism)
- Phase 4 â€” Simulation: pending
- Phase 5 â€” Evaluation: pending
- Phase 6 â€” Analysis and Writing: pending

---

## Naming Conventions

- Variables: `snake_case`
- Files: `[NN]_[verb]_[noun].py` (e.g., `02_distributions.py`)
- Outputs: `[table/fig]_[number]_[description].[ext]`
- Agent draws: saved as `.parquet` with columns named by parameter code (LL, CS, RT, MoR, RE, PD, TfA, ID, MS, AW)
- Experiment results: `experiments/phase0_baseline_calibration/results/`

---

## Non-Negotiable Rules

1. Never modify files in `data/raw/`.
2. Never rename parameter codes (LL, CS, RT, MoR, RE, PD, TfA, ID, MS, AW) without updating `docs/variables.json` and this file simultaneously.
3. After every transformation, print: row count, column names, missing value summary.
4. For simulation runs: state configuration code, N agents, N runs, and random seed BEFORE execution.
5. If uncertain about any parameter-to-behaviour mapping, STOP and reference Section 4.2 of the methods paper. Do not invent rules.
6. Never silently drop agents. Log every filter with before/after counts.
7. Every simulation result must report: config code, obedience rate (or relevant metric), confidence interval, and seed.
8. The correlation matrix R must remain positive semi-definite. Verify after any modification via eigendecomposition. Min eigenvalue must stay above 0 (currently 0.311).
9. Phase 0 calibration target: 45/55 to 55/45 split. Problems outside 40/60â€“60/40 must be rewritten before deployment.

---

## Things Requiring Human Approval

- Changing any Beta(Î±, Î²) parameters in the marginal distributions
- Modifying entries in the correlation matrix R
- Altering societal configuration definitions
- Adding new parameters beyond the current 10
- Defining "morally good decision" â€” this is the critical open question; no code for it without explicit sign-off
- Switching from static to dynamic parameter drift during simulation
- Changing the primary validation benchmarks (Milgram, Asch, UG, Bystander, Reactance)
- Rewriting or replacing any Phase 0 experimental problem

---

## Critical Open Problems (do not paper over these)

1. **Performance metric** â€” "morally good decisions" is not yet formalised. This is the hardest open question.
2. **Tool-based injection mechanism** â€” not yet built.
3. **Dynamic vs. static distributions** â€” unresolved.
4. **Minimum population size** â€” 200â€“500 per config is hypothesised, not tested.
5. **Empirical redundancy** â€” whether 10 parameters collapse under factor analysis is untested.
6. **RT â†” MS correlation** (r = 0.35) â€” theoretically motivated but least empirically anchored.
7. **AW calibration** â€” Beta(2.2, 2.5) is preliminary; R row for AW contains theoretically motivated rather than empirically direct values. Explicit targets for refinement.
8. **32-configuration space** â€” proof-of-concept tests only 8â€“12. Full exploration reserved for later work.

---

## The Five-Agent Review Protocol

**Before committing to any non-trivial coding decision or conceptual judgment**, convene the following synthetic panel. Each speaks in character. Their discussion is logged in `meta.md` and any binding rule changes are propagated back to this file.

### The Panel

| Agent | Role | Personality |
|-------|------|-------------|
| **Prof. Vera Linden** | Philosophy Professor (political theory, normativity) | Precise, adversarial, intolerant of conceptual slippage. Pushes back hard on operationalisation choices. Will not let a loose definition slide. |
| **Prof. Marcus Osei** | Psychology Professor (social & experimental) | Empirically demanding, skeptical of theory-first reasoning. Asks "what does the data actually show?" Catches ecological validity problems. |
| **Dr. Yuki Tanaka** | Postdoc in Statistics (Bayesian methods, copulas) | Technically exacting, worried about identification. Flags PSD violations, distributional assumptions, and numerical instability before anyone else notices. |
| **Dr. Sofia Renna** | Senior Researcher â€” Interdisciplinary (AI + cognitive science) | Integrative thinker, bridger. Connects layers of the architecture that others treat as independent. Asks "how does this choice propagate downstream?" |
| **Dr. James Okafor** | Senior Researcher â€” Interdisciplinary (sociology + simulation) | Pragmatic, implementation-focused. Has been burned by beautiful models that break in code. Pushes for testability and clean failure modes over theoretical elegance. |

### Protocol

1. State the decision or judgment being evaluated in one sentence.
2. Each panel member gives their position (1â€“3 sentences, in character).
3. Identify any point of genuine disagreement â€” these are the load-bearing risks.
4. Record the resolution and any rule changes in `meta.md`.
5. If the panel reaches consensus that a rule in this file needs updating, update it immediately and note the date.

### Trigger conditions (when to convene)

- Any proposed change to the 10-parameter set or its Beta distributions
- Any proposed change to the correlation matrix R
- The first attempt to define the performance metric
- Any parameter-to-behaviour mapping rule being written for the first time
- Any structural change to the simulation interaction loop
- Any decision about tool-based injection vs. system-prompt injection
- Any rewrite of a Phase 0 experimental problem

---

## Git Protocol

**Before any session work:** run `git status` and confirm the branch. State the branch in your first response. Never assume you are on main.

**Branch discipline:**
- `main` is the stable, verified truth.
- Create a branch before any risky, experimental, or exploratory work.
- Merge back to main only after the work has been verified.
- Never commit directly to main during active development. Documentation-only changes (CLAUDE.md, meta.md, README) are the only exception.

**When to commit (PARIA-specific):**
1. Raw calibration data loaded and validated
2. Beta marginals fitted and parameter distributions confirmed against proxy instruments
3. Gaussian copula sampled and PSD re-verified
4. Concept encoding finalised via PyMC and spot-checked
5. Agent population generated and parameter summary stats plausible
6. Simulation run completed and primary metric reported with config code, N, runs, seed, CI
7. Milestone benchmark retrodiction result logged â€” pass or fail, with numbers
8. Any output table or figure intended for citation

**Before committing:**
- Run `git diff --stat`
- Print and inspect pipeline diagnostics
- Commit message describes *what was verified*, not just what was done

**Push discipline:** push after every major phase milestone and at end of session. Never force-push, hard-reset, rebase, or delete a branch without explicit human approval.

**What is never committed:** `data/raw/`, `data/processed/`, `output/`, `.claude/`

---

## Living Document Rule

This file is updated after every session where a significant decision was made, a limitation was discovered, or a mistake was corrected. Updates are sourced from `meta.md`. No decision made in session is considered settled until it appears here or in `meta.md`.

---

## Starter Prompt for Every Session

> Read README.md, CLAUDE.md, and docs/variables.json. Orient to the project: summarise the current phase, identify the specific session goal, and state what the expected output artifact is. Do not write code yet. Produce a stepwise plan with explicit verification after each step. During execution: never modify raw data, never rename parameter codes without approval, print agent counts and parameter summary stats after every transformation, and confirm the correlation matrix R remains PSD after any modification. If uncertain about any parameter-to-behaviour mapping, stop and ask.
