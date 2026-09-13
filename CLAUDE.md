# CLAUDE.md — PARIA / Concepts-as-Architecture Project Constitution

## Phase 2 behavioural study complete (2026-09-13)

The researcher-authorised exploratory-first sequence is complete for the amended
two-anchor behavioural study. See
experiments/phase2_confirmation_20260913/ASSESSMENT.md. Fresh confirmation used
400 profiles, 4,800 individual responses and 300 matched-condition group runs;
11,005 API responses in total. All six primary individual contrasts and one of
seven secondary group contrasts passed their respective Holm corrections.
All final outcomes are complete; three intermediate C3 duplicate-marker votes
remain invalid. Full request/state replay passed with zero new API calls.

Follow-up conservative accounting is $18.755232375; pilot plus follow-up totals
$22.906073025 against the absolute $100 new-package cap. No paid run is active
or queued. Preserve the frozen source, raw records and local verified archives.
The original ten-environment Phase 2 design is not claimed complete. Human
benchmarking is Phase 3 and human-validated moral scoring is Phase 4; the coding
manual still needs the required human review. Ethical understanding, human
resemblance and moral quality are not established. C2 interface limitations and
C3 outcome saturation remain documented; any repair must be prospective.

## Visual replay viewer (2026-09-13)

The researcher requested a game-like view of interactions. The read-only
simulation theatre is documented in viewer/README.md, including its design
review. Launch code/serve_replay.py to inspect all 300 completed Phase 2 group
runs. All 6,205 responses passed state reconstruction; desktop/mobile browser
checks passed. Frozen sources and raw records remain unchanged. Visual seating
and animation are schematic, rounds are simultaneous, and choices carry no
moral scoring. The viewer makes no API calls; live support is future work.

## Exploratory Phase 2 authorisation (2026-09-12)

The researcher explicitly instructed: run the small exploratory Phase 2 test,
assess it, then conduct a separately designed confirmatory study. This supersedes
the earlier preparation-only restriction for this pilot. The pilot has 50 fresh
profiles, both existing anchors, encoded/context-only arms and five matched groups
per task plus neutral bridges; at most 2,575 calls, $10 operational ceiling within
the $100 absolute new-package API cap. See
experiments/phase2_exploratory_20260912/PROTOCOL.md. Preserve the separate future
confirmatory freeze and fresh sample. No original full-battery pass is implied.
The exploratory-first instruction amends the original sequencing: moral coding
and its required human sign-off remain pending; no moral scores or human-validity
claims are produced by this behavioural pilot. Historical raw data and question
bodies remain immutable. The pilot is now complete: 2,180 responses, 75 group
runs, $4.15084065 conservative accounting. See its ASSESSMENT.md for useful
individual contrasts, 25 group format failures and state-adherence problems.
At pilot closure no confirmatory run was queued; the repaired fresh study above supersedes that status. Preserve its
frozen source and raw responses. Current execution status belongs in NEXT_STEPS.md.

## Desktop continuation (2026-09-12)

Phase 2 continuation: the researcher requested rigorous, expedited design work
on generation-time ethical encoding, human resemblance and moral consequences,
preserving LPM and Agents-of-Chaos-inspired interaction. The new package has a
$100 absolute API cap; spend as little as feasible. See the revised proposal in
experiments/phase2_design_20260912/PROTOCOL_DRAFT.md and NEXT_STEPS.md. Preparation
does not itself approve a new configuration subset, coding scheme or live run.

The researcher authorised publication to main with the previous published main
preserved as backup. Use docs/desktop_handoff.md on the desktop. Recent ignored
research data transfers separately; a Git clone alone is incomplete. No new paid
run or Phase 2 release follows from publication. Work on a development branch.

## Human-readable navigation (2026-09-12)

The researcher requested a gentle organisation pass and intentionally removed
meta.md. Do not recreate a separate root decision log. Current work and decision
pointers belong in NEXT_STEPS.md; substantive decisions belong with their phase
protocol or assessment. Existing archived chronologies remain historical evidence.
Use descriptive README links and reading order rather than renaming frozen files.
The Phase 1.5 evidence index groups every retained study by purpose. No scientific
meaning, record, executable source or run setting changes in this pass.

## Archive organisation (2026-09-12)

The researcher authorised central archive consolidation and current-document
cleanup. The existing Phase 0 question archive is in
`archive/phase0/question_revisions/`; historical Phase 0b records are in
`archive/phase0b/runs/`. This administrative relocation preserves all original
bytes. Locked questions and raw records remain immutable. The historical Phase 0
README and long decision log are archived; concise current entry points replace
them. Use archive/README.md, docs/project_layout.md and the migration inventory
for locations. Frozen source packages retain their existing paths. This explicit
cleanup authorisation is not permission to edit scientific content or rerun phases.

## Accepted Phase 1.5 closure (2026-09-12)

The researcher accepted the limited normative-encoding results and instructed
proceed. Phase 1.5 is closed for that revised objective; the original full battery
remains unmet and is not retrospectively passed. This post-results scope decision
supersedes earlier OPEN status and does not claim a section 8.2 full/partial pass.
Explicit profiles can influence decision generation, with local replicated PD
evidence strongest. Ethical understanding and all-ten robustness are unestablished.
Retain all ten coordinates and contrary or unresolved findings. No further paid
Phase 1.5 calls are queued. The original full-architecture Phase 2 design is not
released by this closure; prepare downstream scope and prerequisites offline.
See NEXT_STEPS.md and experiments/phase1_5_encoding_validity/ACCEPTED_CLOSURE_2026-09-12.md.

Updated 2026-09-13. This file and its companion contain the same working rules;
edit both together. Current execution status belongs in NEXT_STEPS.md, and
decisions belong in the relevant phase document, with current pointers in NEXT_STEPS.md.

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

Read [NEXT_STEPS.md](NEXT_STEPS.md) for the current ledger. Phase 0 is closed and
Phase 1 passed operationally. **Phase 1.5 is closed for the researcher-accepted
limited objective**, with evidence of functional normative parameterization.
This is an explicit post-results scope decision. The original gate is still
unmet; neither full nor partial passage of the original battery is claimed.

See the [accepted closure](experiments/phase1_5_encoding_validity/ACCEPTED_CLOSURE_2026-09-12.md)
and [all-ten assessment](experiments/phase1_5_encoding_validity/all_ten_assessment_20260912/ASSESSMENT.md).
PD has independent confirmation and later canonical/verbal effects. All ten
parameters remain reported, including numeric RT counterevidence and unresolved
MS gradients. Broad wording/representation robustness and aggregate explanation
recovery remain insufficient. No intrinsic understanding or AGI is established.

The prior structural package saved 3,580 valid behavioural responses and 200 valid
blind codings. The follow-up dispatched 17,250 requests, saved 17,247 records
and obtained 17,234 valid responses. Missing/invalid slots, disjoint segments,
unknown costs and unavailable complete-data primary analysis remain explicit.
Prespecified paired sensitivity results do not silently replace the primary.
Latest tracked cumulative accounting is $22.66401475 against $25; no further paid
calls queued. This is not total lifetime spending. Raw archives are local with
verified checksums; off-device backup is not established.

The original full-architecture Phase 2 study is not released. Next work is thesis
integration and a concrete downstream scope with its own analysis and required
coding review. No parameter removal, theory amendment, locked-prompt edit or new
parameter-to-behaviour mapping follows from accepting the limited conclusion.

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
disagreements, and resolution in the relevant phase document. These are structured review roles,
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
4. Record the resolution in the relevant phase document and link it from NEXT_STEPS.md.
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
- Never commit directly to main during active development. Documentation-only changes (AGENTS.md, CLAUDE.md, NEXT_STEPS.md, README) are the only exception.

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

This file is updated after every session where a significant decision was made, a limitation was discovered, or a mistake was corrected. Updates are sourced from the relevant phase documents and NEXT_STEPS.md. A significant decision is recorded with the phase it affects, with a current pointer in NEXT_STEPS.md.

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
