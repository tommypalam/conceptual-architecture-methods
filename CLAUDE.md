# CLAUDE.md — PARIA / Concepts-as-Architecture Project Constitution

> **Execution update (2026-09-06):** The older phase-status table below is
> historical. Phase 0 is CLOSED and Phase 1 PASSED per their July closure records.
> Phase 1.5 remains open. The Option-C comparison now has a separate tested runner
> and frozen 15,000-call design; real `_r2` execution started after 10/10 valid
> checkpoint responses from the exact pinned model. No full gate verdict yet.
> Read `NEXT_STEPS.md` and `docs/phase1_5_execution.md` for current execution,
> credential availability, and remaining battery work. Original pilot code and
> records are preserved. Source decision: meta.md 2026-09-06.

> Read this at the start of every session. Every line constrains behavior.
> Source of truth: `Theory/concepts_as_architecture_thesis_v0_6.md` (thesis v0.6, May 2026 — canonical for architectural commitments) and `Theory/implementation_specification_v0_1.md` (spec v0.1, May 2026 — canonical for operational realisation).
> Where the two disagree: thesis wins on architecture, spec wins on operations.

---

## Purpose

PARIA tests whether canonical psychological definitions of five political-ethical concepts — freedom, justice, authority, care, and loyalty — can be encoded as uncertainty-aware parameter distributions that generate **distinguishable and interpretable** social dynamics in an LLM-powered agent-based simulation.

This is a **proof-of-concept thesis**, not a completed methodology. All design decisions are provisional until empirically validated. Claims are candidates for development, not established results.

---

## Unit of Analysis

Individual agents sampled from a 10-dimensional joint distribution (Gaussian copula over 10 Beta marginals), placed into one of 32 societal configurations (2⁵ grid). One agent = one draw. Phase 2 uses a **paired-agent design**: a single population of 200 profiles is drawn once, hash-locked, and exposed to every configuration (within-subjects).

---

## The Ten Agent Parameters

Every agent is a vector x = (x₁, ..., x₁₀), each xᵢ ∈ [0, 1].

| Code | Parameter | 0-endpoint | 1-endpoint | Beta(α, β) | Proxy Instrument |
|------|-----------|------------|------------|------------|------------------|
| LL | Legitimacy Locus | **external/institutional warrant** | **internal endorsement** | Beta(3.5, 2.5) | GCOS |
| CS | Constraint Sensitivity | low (influence = environment) | high (nudges = coercion) | Beta(2.5, 2.0) | HPRS |
| RT | Response Threshold | tolerant (reacts only to major violations) | hair-trigger | Beta(2.5, 2.5) | UG rejection thresholds |
| MoR | Mode of Response | internal/reflective adjustment | external/confrontational | Beta(2.0, 2.5) | STAXI / Thomas-Kilmann / IRI |
| RE | Relational Embedding | atomised, abstract-person | role-sensitive, socially embedded | Beta(2.0, 3.0) | Singelis SCS |
| PD | Procedural Dependence | outcome-dominant | process-dominant | Beta(2.5, 2.0) | Colquitt (2001) |
| TfA | Tolerance for Asymmetry | egalitarian (asymmetry suspect) | hierarchical (asymmetry accepted) | Beta(2.0, 3.5) | SDO7 |
| ID | Internalisation Dependence | surface compliance sufficient | requires genuine endorsement | Beta(3.0, 2.0) | SRQ |
| MS | Moral Scope | local / role-bound | universalised / broadly applied | Beta(1.8, 1.5) | MES (Crimston et al. 2016) |
| AW | Affective Weighting | cognitive / deliberative | affective / intuitive | Beta(2.2, 2.5) | Davis IRI EC/PT ratio |

> **⚠ LL convention (v0.6 fix):** the axis runs **0 = external, 1 = internal** (thesis §3.1). Pre-v0.6 repo docs had this inverted. Beta(3.5, 2.5), mean 0.583, reads as autonomy/internal-leaning — matching GCOS population data. Never reintroduce the old convention.
> AW remains **preliminary** (Beta calibration and R-row not directly anchored; subject to AW on/off sensitivity in Phase 5).

---

## Canonical Concept Definitions

**Freedom** — experiential and behavioural manifestation of agency under constraint; felt and observable reaction to perceived restriction, asymmetric influence, or normative pressure, mediated by relational and structural context (SDT + Psychological Reactance Theory).

**Justice** — cognitive-affective appraisal of proportionality between contributions and outcomes, evaluated through social comparison, sensitive to distributional AND procedural dimensions, generating corrective motivation when imbalance exceeds a subjective threshold (Equity Theory + organisational justice framework).

**Authority** — perceived legitimacy of asymmetric social influence mediated by compliance (instrumental), identification (relational), and internalisation (value-congruent), modulated by expertise, institutional role, and proximity (Milgram + Kelman's three-process model).

**Care** — other-oriented concern for the welfare of those perceived as morally considerable, extended through affective and cognitive mechanisms, activated by cues of suffering or need, modulated by breadth of the moral circle and social-relational embedding (Davis IRI + Batson empathy-altruism + MES).

**Loyalty** — sustained in-group commitment beyond instrumental calculation; pro-group behaviour at personal cost, mediated by identification and, at its extreme, identity fusion; modulated by in-group legitimacy, ritual enactment, and perceived group threat (Swann et al. identity fusion + Kelman).

---

## Societal Configurations (2⁵ grid)

Each configuration is (Freedom, Justice, Authority, Care, Loyalty) ∈ {0, 1}⁵. The proof-of-concept tests a **defensible subset of 8–12 configurations** selected under the formal three-part criterion of thesis §4.3: (1) per-axis coverage ≥ 3 configs at each level of each axis; (2) anchor inclusion — the Milgram-analogue `00100` (F=0, J=0, A=1, C=0, L=0) and its inverse `11011`; (3) max-entropy Hamming spread on remaining slots. The full 32-space is reserved for later work.

---

## Behavioural Benchmarks — One Per Concept (v0.6 modernised bands)

| Concept | Benchmark | Retrodiction target |
|---------|-----------|---------------------|
| Authority | Milgram (1974) | 61–66 % max-voltage obedience in `00100`; modulators: peer rebellion ~10 %, experimenter absence ~20 %, diffused responsibility ~90 % |
| Loyalty | Asch (1956) / Bond & Smith (1996) | **25–30 %** critical-trial conformity (modernised band; the original 32–37 % is superseded) |
| Justice | Ultimatum Game (Güth et al. 1982) | Proposer offers **45–50 %** (modernised); rejection of 20 %-offers ≈ 40–50 %; threshold ≈ 30–33 % |
| Care | Bystander helping (Latané & Darley 1968) | ~75 % alone → ~55 % with 3+ bystanders; danger condition attenuates/reverses |
| Freedom | Reactance restoration (Worchel & Brehm 1970) | Between-subjects rate Δ ≈ 15–25 pp; Cohen's d ≈ 0.45 |

> **Contamination protocol is mandatory (thesis §5.3):** every benchmark runs canonical + decanonised variants, under predicted-high AND predicted-low configurations. The **configuration-counterfactual difference is the primary success criterion**, not the absolute rate. Scenario-recognition probe threshold: 30 %. Modulator-structure retrodiction (Milgram, Asch) on decanonised variants is the strongest discriminator.
> **Stanford Prison Experiment: explicitly rejected** as benchmark (Le Texier 2018; Carnahan & McFarland 2007; no quantified target). Role transformation is addressed via C2.

---

## Moral Performance Metric (CLOSED — thesis Chapter 7)

The previous "hardest open problem" is now specified. Dual scoring per agent action:

- **Configuration-relative 8-vector:** four MACHIAVELLI negatives (power-seeking, deception, disutility, ethical violations) + four positive analogues (appropriate authority use — Tyler; honest disclosure — HEXACO H-H; welfare promotion — Eisenberg-Spinrad/Batson; principled compliance under cost — Aquino-Reed MIS).
- **Fixed-standard 4-vector:** harm / deception / coercion / unfairness avoidance, configuration-independent.
- **Headline binary** B(v_a): strict-OR (any negative → not-good; ≥1 positive and no negative → good; else neutral), with net-score and weighted (w_n = 1.5) robustness aggregations.
- **Principled resistance is a positive trigger** (refusal of illegitimate directive, whistleblowing, welfare-preserving disobedience, principled noncompliance with harmful consensus) — never code dissent as a violation by default.
- Coding: Phase A LLM-rater + Phase B human gold subset (10–20 %, MTurk, blind to configuration). κ ≥ 0.60 per category; PABAK alongside; ≤ 3 revision rounds per category.

The coding manual itself is still to be drafted and pre-registered before Phase 2 — that work requires panel review and human sign-off.

---

## Phase Plan and Current Status (v0.6 sequence)

| Phase | Description | Status |
|-------|-------------|--------|
| 0 | Naked-prompt 50/50 baseline calibration (gpt-5.4-mini) | **COMPLETE** (2026-05-02, all 6 problems locked) |
| 0b | Harness-neutral baseline — 3 null conditions × 6 problems × N=500 | **NEXT — required gating** |
| 0c | Locked holdout — frozen prompts, N=1000/problem, no-edit rule | Pending (after 0b) |
| 1 | Pilot — S2, one config, N=50, five diagnostics | Pending |
| 1.5 | Encoding-validity battery (~10k calls) — **HARD GATE** | Pending |
| 2 | Full experimental runs — simple (paired-agent) + complex (orchestrator, per-round reinjection, bridge calibration) | Pending |
| 3 | Benchmarks under contamination protocol | Pending |
| 4 | Moral coding — Phase A LLM-rater + Phase B human gold | Pending |
| 5 | Analysis — mixed-effects primary, sensitivity regimes, multi-model robustness | Pending |
| 6 | Reporting, OSF compliance, open-artefact release | Pending |

OSF pre-registration (hypotheses, analysis plan, coding manual, power analysis, stopping rules) is **required before Phase 2 begins**.

---

## Experimental Problems (Phase 0 locked 2026-05-02)

| ID | Name | Labels | Phase 0 split |
|----|------|--------|----------------|
| S1 | The Promotion Decision | A / B | 53 / 47 |
| S2 | The Quiet Error | FORMAL_REPORT / LOCAL_CORRECTION | 51 / 49 |
| S3 | **The Department Reorganisation** | ADOPT / WAIT | 50 / 50 |
| C1 | The Resource Council | PACKAGE_A / PACKAGE_B | 51.5 / 48.5 |
| C2 | The Restructuring Board | APPROVE / REJECT | 50 / 50 |
| C3 | The Scientific-Approach Dilemma | CONTINUE / PIVOT | 51 / 49 |

> The original S3 (Strategic Pivot) was **retired** after ~20 variants; the locked file `S3_strategic_pivot.md` in the questions folder contains the accepted Department Reorganisation prompt (ADOPT/WAIT) under the legacy filename. The questions folder is immutable — do not rename it; treat the thesis Appendix C text as authoritative for content.

---

## Implementation Stack

| Layer | Tool |
|-------|------|
| Joint distribution sampling | NumPy (`multivariate_normal`) + SciPy (`norm.cdf`, `beta.ppf`) — implemented in `code/utils.py` |
| Bayesian encoding | PyMC |
| Agent-based simulation | Mesa |
| Multi-agent orchestration | Custom orchestrator adapted from Agents of Chaos (per-round reinjection is load-bearing) |
| Statistical analysis | statsmodels (MixedLM, multipletests) + R lme4/glmer cross-check; SciPy |
| Inter-rater agreement | statsmodels Fleiss κ; custom PABAK, Krippendorff's α |
| Visualisation | Plotly (dashboards), Matplotlib (publication statics) |
| LLM access | OpenAI SDK (gpt-5.4-mini primary); Anthropic / Google SDKs for cross-validation and robustness |

---

## Naming Conventions

- Variables: `snake_case`
- Outputs: `[table/fig]_[number]_[description].[ext]`
- Agent draws: `.parquet` with columns named by parameter code (LL, CS, RT, MoR, RE, PD, TfA, ID, MS, AW)
- Per-call records: one immutable JSON per API call, schema per spec Appendix C
- Phase 0 artefacts: `experiments/phase0_baseline_calibration/` (legacy name for spec's `experiments/phase0/` — immutable)
- New phase directories follow spec §1.2 (`phase0b_harness_neutral/`, `phase0c_locked_holdout/`, `phase1_pilot/`, `phase1_5_encoding_validity/`, `phase2_simple/`, `phase2_complex/`, `phase3_benchmarks/`, `phase4_coding/`, `phase5_analysis/`)

---

## Non-Negotiable Rules

1. **Never touch `experiments/phase0_baseline_calibration/`** — prompts, archive, and results are immutable provenance. Raw API-call records anywhere are write-once; failures go to `failures.jsonl`, never retried in place.
2. Never rename parameter codes (LL, CS, RT, MoR, RE, PD, TfA, ID, MS, AW) without updating `docs/variables.json` and this file simultaneously.
3. After every transformation, print: row count, column names, missing value summary (`utils.log_dataframe_summary`).
4. For simulation runs: state configuration code, N agents, N runs, and random seed BEFORE execution. Seeds map phase-name → root seed (config/seeds.json once created).
5. If uncertain about any parameter-to-behaviour mapping, STOP and reference thesis §4.2 / Appendix A. Do not invent rules.
6. Never silently drop agents. Log every filter with before/after counts.
7. Every simulation result must report: config code, primary metric, confidence interval, and seed.
8. The correlation matrix R must remain positive semi-definite (min eigenvalue currently 0.311). `utils.verify_psd` runs at import; re-verify after any modification.
9. Phase 0-style calibration target: 45/55 to 55/45; outside 40/60–60/40 → rewrite before deployment.
10. Mid-run protocol edits are forbidden (spec §5.4.3): no prompt edits, model swaps, or temperature changes once a phase run starts. A full rerun gets a new designation (Phase 2.1, …).
11. Phase 1.5 is a **hard gate**: Phase 2 does not begin until the encoding-validity battery passes (or passes-with-revision per the decision tree, thesis §8.2).
12. Per-round parameter reinjection for C1/C2/C3 is load-bearing (thesis §4.1.1) — never rely on the model retaining the profile across rounds.

---

## Things Requiring Human Approval

- Changing any Beta(α, β) parameters in the marginal distributions
- Modifying entries in the correlation matrix R
- Altering societal configuration definitions or the selected 8–12 subset
- Adding new parameters beyond the current 10
- Drafting or revising the moral-coding manual (metric is specified; manual operationalisation needs sign-off)
- Switching from static to dynamic parameter drift during simulation
- Changing the primary validation benchmarks or their retrodiction bands
- Editing any Phase 0-locked prompt (Phase 0c freezes them permanently)
- Invoking the Appendix A descope path (MVT: simple problems + Milgram + UG)

---

## Critical Open Problems (v0.6 — do not paper over these)

1. **Encoding validity** — does the LLM operate as a parameterised agent? Phase 1.5 tests this; it is the primary remaining open question.
2. **Training-data contamination** — all five benchmarks are famous; the configuration counterfactual is the discriminator.
3. **Phase 0b/0c** — the full harness has not yet been validated; naked-prompt balance ≠ harness balance.
4. **Positive-side inter-rater agreement** — κ on positive categories expected lower than negative; gap size determines metric reliability.
5. **R dependency structure** — weak entries and the AW row are the least anchored; regimes B/C/D + t-copula test load-bearing-ness. RT ↔ MS (r = 0.35) is the least-anchored strong entry.
6. **Parameter redundancy** — Phase 1.5 sweeps + Phase 5 factor analysis test empirical separability.
7. **Static vs. dynamic distributions** — static for the proof-of-concept; drift is future work.
8. **Multi-model dependency** — all calibration is on gpt-5.4-mini; portability tested in Phase 5.
9. **Configuration subset adequacy** — 8–12 of 32; missing regimes are an acknowledged constraint.
10. **Cross-cultural generalisation** — Western-democratic scope only; everything else requires instrument revalidation.

---

## The Five-Agent Review Protocol

**Before committing to any non-trivial coding decision or conceptual judgment**, convene the following synthetic panel. Each speaks in character. Their discussion is logged in `meta.md` and any binding rule changes are propagated back to this file.

| Agent | Role | Personality |
|-------|------|-------------|
| **Prof. Vera Linden** | Philosophy Professor (political theory, normativity) | Precise, adversarial, intolerant of conceptual slippage. Pushes back hard on operationalisation choices. |
| **Prof. Marcus Osei** | Psychology Professor (social & experimental) | Empirically demanding, skeptical of theory-first reasoning. Catches ecological validity problems. |
| **Dr. Yuki Tanaka** | Postdoc in Statistics (Bayesian methods, copulas) | Technically exacting. Flags PSD violations, distributional assumptions, numerical instability first. |
| **Dr. Sofia Renna** | Senior Researcher — Interdisciplinary (AI + cognitive science) | Integrative bridger. Asks "how does this choice propagate downstream?" |
| **Dr. James Okafor** | Senior Researcher — Interdisciplinary (sociology + simulation) | Pragmatic, implementation-focused. Pushes for testability and clean failure modes. |

### Protocol

1. State the decision or judgment being evaluated in one sentence.
2. Each panel member gives their position (1–3 sentences, in character).
3. Identify any point of genuine disagreement — these are the load-bearing risks.
4. Record the resolution and any rule changes in `meta.md`.
5. If the panel reaches consensus that a rule in this file needs updating, update it immediately and note the date.

### Trigger conditions (when to convene)

- Any proposed change to the 10-parameter set or its Beta distributions
- Any proposed change to the correlation matrix R
- Drafting the moral-coding manual or any coding rule
- Any parameter-to-behaviour mapping rule being written for the first time
- Any structural change to the orchestrator or simulation interaction loop
- Any decision about tool-based injection vs. system-prompt injection
- Selecting the 8–12 configuration subset
- Interpreting Phase 0b/0c/1/1.5 pass-fail outcomes at the margins

---

## Git Protocol

**Before any session work:** run `git status` and confirm the branch (initialise the repo if not yet under git — it currently is not). State the branch in your first response.

**Branch discipline:**
- `main` is the stable, verified truth.
- Create a branch before any risky, experimental, or exploratory work.
- Merge back to main only after the work has been verified.
- Never commit directly to main during active development. Documentation-only changes (CLAUDE.md, meta.md, README) are the only exception.

**When to commit (PARIA-specific):**
1. Config artefacts created or changed (parameters.json, correlation_matrix_R.json, configurations.json, seeds.json)
2. Beta marginals or R confirmed against proxy instruments (with PSD re-verification)
3. Phase gate passed or failed — logged with numbers, never silently
4. Agent population generated (hash-locked) with plausible summary stats
5. Any run completed with full provenance (config, N, runs, seed, CI)
6. Benchmark retrodiction result logged — pass or fail
7. Any output table or figure intended for citation

**Before committing:** run `git diff --stat`, inspect pipeline diagnostics; the commit message describes *what was verified*, not just what was done.

**Push discipline:** push after every major phase milestone and at end of session. Never force-push, hard-reset, rebase, or delete a branch without explicit human approval.

**What is never committed:** `data/raw/`, `data/processed/`, `output/`, `.claude/`; raw per-call JSON archives are stored as artefacts with checksums committed instead (spec §1.4).

---

## Living Document Rule

This file is updated after every session where a significant decision was made, a limitation was discovered, or a mistake was corrected. Updates are sourced from `meta.md`. No decision made in session is considered settled until it appears here or in `meta.md`.

---

## Starter Prompt for Every Session

> Read README.md, CLAUDE.md, and docs/variables.json. Orient to the project: summarise the current phase, identify the specific session goal, and state what the expected output artifact is. Do not write code yet. Produce a stepwise plan with explicit verification after each step. During execution: never touch the Phase 0 archive, never rename parameter codes without approval, print agent counts and parameter summary stats after every transformation, and confirm R remains PSD after any modification. If uncertain about any parameter-to-behaviour mapping, stop and ask.
