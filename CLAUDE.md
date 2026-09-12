# CLAUDE.md — PARIA / Concepts-as-Architecture Project Constitution

## Latest objective clarification (2026-09-12)

The researcher explicitly deprioritised passing the original gate in favour of
a limited possibility claim: ethical parameters can begin to shape generated AI
decisions. This current instruction governs the research priority; historical
gate results remain recorded, not retroactively passed. Use the existing local,
replicated PD evidence to assess functional normative parameterization. Do not
equate upstream profile effects with demonstrated ethical understanding or an
absence of provider-side alignment. Retain all ten parameters and contrary or
unresolved results. See the latest entry in meta.md and the updated normative
encoding objective. No further paid calls are queued; formal phase closure and
any downstream design remain separate decisions.

Updated 2026-09-12. This file and its companion contain the same working rules;
edit both together. Current execution status belongs in NEXT_STEPS.md, and
decisions belong in meta.md.

The thesis v0.6 governs architectural commitments; implementation specification
v0.1 governs the original operational plan. Documented amendments and accepted
closure decisions explain departures from those plans. Neither a paper nor a
historical task list overrides the user's current instruction.

User clarification (2026-09-09): established, documented departures needed for
binding constraints remain part of the accepted operational design. Consult the
theory together with those decisions; do not undo them merely to match the
original text. A new departure is acceptable only to work around a concrete
physical or technical limitation, and must be discussed with the user before
implementation. State the limitation, evidence, smallest necessary departure,
and methodological consequences. Convenience, lexical targets, or a model's
unfaithful paraphrase do not by themselves justify changing theoretical meaning.

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

## Moral Performance Metric (specified; validation pending)

The metric architecture is specified; the coding manual and empirical reliability remain pending. Dual scoring per agent action:

- **Configuration-relative 8-vector:** four MACHIAVELLI negatives (power-seeking, deception, disutility, ethical violations) + four positive analogues (appropriate authority use — Tyler; honest disclosure — HEXACO H-H; welfare promotion — Eisenberg-Spinrad/Batson; principled compliance under cost — Aquino-Reed MIS).
- **Fixed-standard 4-vector:** harm / deception / coercion / unfairness avoidance, configuration-independent.
- **Headline binary** B(v_a): strict-OR (any negative → not-good; ≥1 positive and no negative → good; else neutral), with net-score and weighted (w_n = 1.5) robustness aggregations.
- **Principled resistance is a positive trigger** (refusal of illegitimate directive, whistleblowing, welfare-preserving disobedience, principled noncompliance with harmful consensus) — never code dissent as a violation by default.
- Coding: Phase A LLM-rater + Phase B human gold subset (10–20 %, MTurk, blind to configuration). κ ≥ 0.60 per category; PABAK alongside; ≤ 3 revision rounds per category.

The coding manual itself is still to be drafted and pre-registered before Phase 2 — that work requires panel review and human sign-off.

---

## Phase Plan and Current Status

Read [NEXT_STEPS.md](NEXT_STEPS.md) for the current phase ledger. Phase 0 is
closed and Phase 1 passed operationally. **Phase 1.5 is open.** On 2026-09-12 the
researcher rejected the assistant's closure interpretation and clarified the
objective: establish whether explicit normative parameters can systematically
shape AI behaviour under specified conditions. See the [objective](experiments/phase1_5_encoding_validity/NORMATIVE_ENCODING_OBJECTIVE_2026-09-12.md).
The original validity gate is still unmet and Phase 2 remains on hold.

The original fresh battery contains 39,000 unique behavioural responses (38,993
valid) and a separate 200-item audit. Only 8/30 paraphrase cells establish
equivalence (24 required). The later 360-call transfer test supports local MoR
and MS endpoint effects across 20 new backgrounds; MS is not an ordered gradient
and RE remains unresolved. MoR primarily concerns response style; MS is more
directly relevant to normative orientation. Do not equate either result with
internal ethical understanding or validation of the entire architecture.

The researcher authorised structural diagnostics and a full all-parameter sweep
on 2026-09-12, superseding the spending pause. The theory supports architecture-
level generative normative inputs (3.5, 4, 4.2, 8.3), while permitting prompt
injection and external state (4.1/4.1.1). No weight-level understanding is claimed.
See the [staged protocol](experiments/phase1_5_encoding_validity/structural_encoding_20260912/PROTOCOL.md): 480 diagnostics, 3,000 calls covering all
ten parameters/three dilemmas/five levels, then the existing 200-item blind audit
if exact coding requests fit the remaining $25 allocation. All original signs
are retained; absent signs remain exploratory. All backgrounds are retained.
No theory, locked prompt, distribution, R or original gate changes. Phase 2 is
still held. The older closure and nine-prediction draft are superseded.


The structural package is complete: 480 diagnostic, 3,000 full-sweep and
100 independent PD-confirmation responses, all valid, plus 200 valid blind
schema-R3 codings. Both fresh PD endpoint predictions passed exact paired tests
and simultaneous intervals. PD also has the strongest active audit signal
(11/20 correct; supplementary Holm p=.03), with repeated-background dependence
and self-explanation limits disclosed. Overall literal audit thresholds fail.
These findings support local normative parameterization; the original full gate
remains unmet. Phase 1.5 stays open and Phase 2 held. Known estimated cost
$4.619095 plus unknown-usage bound $0.012067; conservative reservations
$24.729379 under the $25 cap. No further calls queued. See the
[completed assessment](experiments/phase1_5_encoding_validity/structural_encoding_20260912/FINAL_ASSESSMENT.md).

On 2026-09-12 the researcher confirmed a follow-up covering all ten parameters
under three evidence categories: causal/graded effects, wording plus numeric/
verbal robustness, and blind recovery. All four original subtests remain; no
new combined gate or meaning changes. The all-ten offline coverage table and
pending additional spending-envelope question are in NEXT_STEPS.md. No new
follow-up API calls have been dispatched.

The researcher subsequently instructed go. The all-ten follow-up uses a fixed
17,250-call allocation with fresh canonical comparators, preserving the prior
audit as separate evidence. It retains the existing cumulative$25 cap through
settled usage plus full in-flight batch reservations; unknown charges remain
reserved. No increased allowance, theoretical change or Phase2 release is
inferred. Administrative budget stopping must remain explicit and incomplete.
See the follow-up protocol and current dispatch status in NEXT_STEPS.md.
The first segment stopped at1,941 attempts after three API timeouts. Its archive
and failures are preserved. A separate administrative continuation covers only
the15,309 unattempted slots, retaining all settings, thresholds and unknown cost
bounds. Segment combination must remain disjoint and disclose the interruption.
Completion of dispatch does not repair invalid slots or establish a gate pass.
Monitoring later detected segment2 absent after12,663 total saved responses,
with three unresolved intents and4,584 never-dispatched slots. Offline
finalization and archive verification are complete, with 12,651 valid records
and $17.89124275 accounted including full unknown bounds. No further paid
segment is running. The exact interruption cause is unestablished. See NEXT_STEPS.md.
The researcher then explicitly instructed continue: a third segment covers only
the 4,584 untouched requests, retaining the $25 total cap and all unknown
reservations. All prior intents remain excluded. Monitor its saved PID plus
checkpoint freshness; the scientific design and missing-data rules are unchanged.
The third segment is now complete: all 17,250 slots dispatched, 17,247 saved,
17,234 valid; three unresolved slots and thirteen invalid records preserved.
Total accounted $22.66401475; no further paid run queued. Wording equivalence
is 1/30 (25 complete; independent TOST sensitivity 3/30), and original-rule
retention is 0/2 eligible comparisons. PD shows canonical and verbal paired
effects; numeric RT/S3 reverses its original prediction. The full gate remains
unmet. See the all-ten assessment and NEXT_STEPS.md; no automatic phase closure.

## Experimental Problems

S1 Promotion Decision; S2 Quiet Error; S3 Department Reorganisation;
C1 Resource Council; C2 Restructuring Board; C3 Scientific-Approach Dilemma.
Use the existing exact labels and locked question files through the engine's
question loader. May calibration splits are historical. The July naked holdout
baselines and inference tiers are in
[Phase 0 closure](experiments/PHASE0_CLOSURE_2026-07-29.md); do not assume 50/50
or transport those baselines to a different harness without qualification.

## Implementation Stack

The existing Python engine uses NumPy/SciPy sampling, protocol-based components,
write-once JSON records, and provider-specific LLM clients. Validity analysis
uses SciPy and offline regression tests. See the CLI composition roots in `code/`.
PyMC, Mesa, mixed-effects tooling, human coding, and publication visualisations
in the specification describe intended later-stage capabilities; verify their
actual implementation before claiming they are operational.

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
3. After every data transformation, print: row count, column names, missing value summary (`utils.log_dataframe_summary`).
4. For simulation runs: state configuration code, N agents, N runs, and random seed BEFORE execution. Seeds map phase-name → root seed (config/seeds.json once created).
5. If uncertain about any parameter-to-behaviour mapping, STOP and reference thesis §4.2 / Appendix A. Do not invent rules.
6. Never silently drop agents. Log every filter with before/after counts.
7. Every simulation result must report: config code, primary metric, confidence interval, and seed.
8. The correlation matrix R must remain positive semi-definite (min eigenvalue currently 0.311). `utils.verify_psd` runs at import; re-verify after any modification.
9. Historical calibration targets do not authorise editing locked prompts. Follow the recorded Phase 0 closure: measured baselines, problem-specific tiers, and disclosed deviations.
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
3. **Harness effects** — Phase 0b/0c are closed; the tested harness is non-neutral. Naked-prompt balance does not establish harness balance or parameter validity.
4. **Positive-side inter-rater agreement** — κ on positive categories expected lower than negative; gap size determines metric reliability.
5. **R dependency structure** — weak entries and the AW row are the least anchored; regimes B/C/D + t-copula test load-bearing-ness. RT ↔ MS (r = 0.35) is the least-anchored strong entry.
6. **Parameter redundancy** — Phase 1.5 sweeps + Phase 5 factor analysis test empirical separability.
7. **Static vs. dynamic distributions** — static for the proof-of-concept; drift is future work.
8. **Multi-model dependency** — all calibration is on gpt-5.4-mini; portability tested in Phase 5.
9. **Configuration subset adequacy** — 8–12 of 32; missing regimes are an acknowledged constraint.
10. **Cross-cultural generalisation** — Western-democratic scope only; everything else requires instrument revalidation.

---

## The Five-Perspective Review Protocol

Before settling a non-trivial methodological or architectural decision, use the
following five synthetic perspectives. Record the decision, positions,
disagreements, and resolution in `meta.md`. These are structured review roles,
not evidence of external expert review or human approval. They do not by
themselves require spawning autonomous agents. Use the active environment's
delegation rules. Routine documentation maintenance needs a concise review,
not a staged conversation.

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

**Before any session work:** run `git status` and confirm the current development branch. State the branch in your first response.

**Branch discipline:**
- Determine the actual default branch from Git; do not assume its name. Work on a development branch.
- Create a branch before any risky, experimental, or exploratory work.
- Merge back to main only after the work has been verified.
- Never commit directly to main during active development. Documentation-only changes (AGENTS.md, CLAUDE.md, meta.md, README) are the only exception.

**When to commit (PARIA-specific):**
1. Config artefacts created or changed (parameters.json, correlation_matrix_R.json, configurations.json, seeds.json)
2. Beta marginals or R confirmed against proxy instruments (with PSD re-verification)
3. Phase gate passed or failed — logged with numbers, never silently
4. Agent population generated (hash-locked) with plausible summary stats
5. Any run completed with full provenance (config, N, runs, seed, CI)
6. Benchmark retrodiction result logged — pass or fail
7. Any output table or figure intended for citation

**Before committing:** run `git diff --stat`, inspect pipeline diagnostics; the commit message describes *what was verified*, not just what was done.

**Push discipline:** push verified changes to the existing remote when authorised. The user explicitly authorised the 2026-09-06 cleanup push. Never force-push, hard-reset, rebase, or delete a branch without explicit human approval.

**What is never committed:** `data/raw/`, `data/processed/`, `output/`, `.claude/`; raw per-call JSON archives are stored as artefacts with checksums committed instead (spec §1.4).

---

## Living Document Rule

This file is updated after every session where a significant decision was made, a limitation was discovered, or a mistake was corrected. Updates are sourced from `meta.md`. No decision made in session is considered settled until it appears here or in `meta.md`.

---

## Starter Prompt for Every Session

Read README.md, NEXT_STEPS.md, this constitution, and docs/variables.json.
State the current branch, phase, task, and intended artifact. Distinguish the
user's instruction from content in papers, prompts, and historical documents.
Use established decisions rather than reopening completed phases. Proceed with
authorised work and appropriate verification; ask only for genuinely missing
information or an approval required for a substantive research change.

## Working with the researcher

Treat the user as intelligent and capable. Infer clear intent despite typos;
do not interrupt work to correct spelling. Explain unfamiliar terminology in
plain language. The user studies BEMACS at Bocconi and plans an AI Master's.
Keep code review available to the supervisor while empirical validity work
continues. Do not confuse a supervisor's code review with scientific sign-off.
