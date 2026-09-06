# PARIA / Concepts as Architecture: From Political Concepts to Simulated Judgment

> **Execution update (2026-09-06):** Phase 1.5 Option-C runner implemented and
> tested offline; full 15,000-call protocol frozen, real execution awaiting access
> to the configured API credential. No new empirical validity result is claimed.
> See [`docs/phase1_5_execution.md`](docs/phase1_5_execution.md) for commands,
> safeguards, analysis, and remaining battery work. July status below is retained
> as the last empirical milestone.

> **Status (2026-07-29):** Phase 0 CLOSED (0a/0b/0c); Phase 1 pilot PASSED;
> Phase 1.5 (encoding-validity) in progress. Thesis v0.6 + Implementation Spec
> v0.1. Not for citation; design decisions provisional until validated.
> Author: Tommaso Piero Palamenga — Bocconi University
> Supervisor: Dr. Abhinav · Co-supervisor: Prof. Arnaldo Camuffo
>
> **Headline empirical results so far:**
> - The six dilemmas calibrate ~50/50 **naked** (Phase 0a, locked; recalibrated
>   for model drift and re-locked, see `experiments/phase0b_calibration/`).
> - The Phase-2 **agent-framing harness is NOT behaviourally neutral** on
>   gpt-5.4-mini-2026-03-17: any scaffold text collapses S2/C2/C3 toward a pole.
>   Diagnosed to the "decision-making simulation" preamble; not fixable by
>   template revision (Phase 0b — a substantive methodological finding).
> - Phase 0c locked holdout (N=1000) confirmed baselines; problems are used at
>   their **0c-measured baselines**, tiered PRIMARY (S1/S3) / SECONDARY
>   (C1/C2/C3) / LOW-POWER (S2), not assumed 50/50.
> - See `experiments/PHASE0_CLOSURE_2026-07-29.md` for the full closure verdict.

---

## What This Project Does

PARIA tests whether canonical psychological definitions of **freedom**, **justice**, **authority**, **care**, and **loyalty** can be encoded as transparent, uncertainty-aware parameter distributions that produce distinguishable and interpretable social dynamics in an LLM-powered agent-based simulation.

Each concept is reduced to a single canonical definition grounded in the psychological literature. These definitions are encoded as Beta distributions over ten shared parameters. Agents are sampled from a ten-dimensional joint distribution via Gaussian copula, then placed into one of thirty-two societal configurations. The simulation is validated against five behavioural benchmarks — one per concept — under a training-data contamination protocol, and exercised through six 50/50-calibrated experimental problems. Moral performance is scored with a dual configuration-relative + fixed-standard extended-MACHIAVELLI metric.

**The central claim:** structured conceptual encodings can do genuine explanatory work — not just serve as decorative philosophical preface.

---

## Source of Truth

| Document | Role |
|----------|------|
| [`Theory/concepts_as_architecture_thesis_v0_6.md`](Theory/concepts_as_architecture_thesis_v0_6.md) | Thesis v0.6 — canonical for **architectural commitments** (concepts, parameters, distributions, benchmarks, metric, gates) |
| [`Theory/implementation_specification_v0_1.md`](Theory/implementation_specification_v0_1.md) | Spec v0.1 — canonical for **operational realisation** (sequencing, pass/fail criteria, call budgets, schemas, contingency trees) |
| [`CLAUDE.md`](CLAUDE.md) | Project constitution — read every session |
| [`meta.md`](meta.md) | Living decision log |
| [`docs/variables.json`](docs/variables.json) | Variable codebook (v2.1, synced to v0.6) |

Where thesis and spec disagree: thesis wins on architecture, spec wins on operations.

---

## Research Question

> Can canonical definitions of five political-ethical concepts — freedom, justice, authority, care, and loyalty — be encoded into uncertainty-aware parameter profiles that generate distinguishable and interpretable social dynamics?

---

## Phase Plan and Status (v0.6 sequence)

| Phase | Description | Status |
|-------|-------------|--------|
| 0a | Naked-prompt 50/50 baseline calibration (gpt-5.4-mini) | **COMPLETE** — locked 2026-05-02; recalibrated for drift + re-locked 2026-07-28 |
| 0b | Harness-neutral baseline (3 null conditions × 6 problems) | **COMPLETE 2026-07-29** — harness found non-neutral; documented, not forced to pass (see closure) |
| 0c | Locked holdout (frozen prompts, N=1000/problem, naked delivery) | **COMPLETE 2026-07-29** — hash-locked; baselines measured + tiered |
| 1 | Pilot (S3 + S2, config 10011, N=50) | **PASS 2026-07-29** — pipeline verified end-to-end |
| 1.5 | Encoding-validity battery (~10k+ calls) — **hard gate** | **IN PROGRESS** — pilot sweep done (mechanism partially alive); full sweep = Option C (see NEXT_STEPS) |
| 2 | Full experimental runs (paired-agent simple + orchestrated complex + bridge) | Pending |
| 3 | Benchmarks under contamination protocol | Pending |
| 4 | Moral coding (LLM-rater + human gold subset) | Pending |
| 5 | Analysis (mixed-effects primary, sensitivity, multi-model) | Pending |
| 6 | Reporting, OSF compliance, open-artefact release | Pending |

OSF pre-registration is required before Phase 2 (see [`docs/pre_analysis_plan.md`](docs/pre_analysis_plan.md)).
Current working state and the next concrete step: [`NEXT_STEPS.md`](NEXT_STEPS.md).

---

## The Ten Agent Parameters

| Code | Parameter | Scale | Beta(α, β) | Proxy |
|------|-----------|-------|------------|-------|
| LL | Legitimacy Locus | 0=external → 1=internal | Beta(3.5, 2.5) | GCOS |
| CS | Constraint Sensitivity | 0=low → 1=high | Beta(2.5, 2.0) | HPRS |
| RT | Response Threshold | 0=tolerant → 1=hair-trigger | Beta(2.5, 2.5) | UG rejection thresholds |
| MoR | Mode of Response | 0=internal → 1=external | Beta(2.0, 2.5) | STAXI / Thomas-Kilmann / IRI |
| RE | Relational Embedding | 0=atomised → 1=relational | Beta(2.0, 3.0) | Singelis SCS |
| PD | Procedural Dependence | 0=outcome → 1=process | Beta(2.5, 2.0) | Colquitt (2001) |
| TfA | Tolerance for Asymmetry | 0=egalitarian → 1=hierarchical | Beta(2.0, 3.5) | SDO7 |
| ID | Internalisation Dependence | 0=surface → 1=endorsement | Beta(3.0, 2.0) | SRQ |
| MS | Moral Scope | 0=local → 1=universal | Beta(1.8, 1.5) | MES (Crimston et al. 2016) |
| AW | Affective Weighting | 0=cognitive → 1=affective | Beta(2.2, 2.5) | Davis IRI EC/PT ratio |

Joint distribution: Gaussian copula with empirically anchored 10×10 correlation matrix R (verified PSD, min eigenvalue = 0.311). Implemented in [`code/utils.py`](code/utils.py).

> **Note (v0.6):** the LL axis runs **0=external, 1=internal** — corrected from the inverted pre-v0.6 convention. AW remains preliminary.

---

## Societal Configurations

32 configurations from the 2⁵ grid of (Freedom, Justice, Authority, Care, Loyalty) ∈ {0,1}⁵. The proof-of-concept tests a defensible subset of **8–12 configurations** selected by per-axis coverage + anchor inclusion + max-entropy spread (thesis §4.3).

**Anchors:** Milgram-analogue `00100` (F=0, J=0, A=1, C=0, L=0) and its inverse `11011`.

---

## Behavioural Benchmarks (modernised v0.6 bands, under contamination protocol)

| Concept | Benchmark | Target |
|---------|-----------|--------|
| Authority | Milgram (1974) | 61–66 % obedience in `00100`; modulator fingerprint secondary |
| Loyalty | Asch (1956) / Bond & Smith (1996) | 25–30 % critical-trial conformity (modernised) |
| Justice | Ultimatum Game (Güth et al. 1982) | Proposer offers 45–50 %; ~40–50 % rejection of 20 % offers |
| Care | Bystander helping (Latané & Darley 1968) | ~75 % alone; ~55 % with 3+ bystanders |
| Freedom | Reactance restoration (Worchel & Brehm 1970) | Δ ≈ 15–25 pp between-subjects; Cohen's d ≈ 0.45 |

Every benchmark runs canonical + decanonised variants under predicted-high AND predicted-low configurations; the **configuration-counterfactual difference** is the primary success criterion (thesis §5.3). SPE is explicitly rejected as a benchmark.

---

## Experimental Problems — calibration timeline

| ID | Name | Labels | 0a split (May 2026) | 0c naked N=1000 (2026-07-29) | tier |
|----|------|--------|--------------------|------------------------------|------|
| S1 | The Promotion Decision | A / B | 53 / 47 | 41 / 59 | PRIMARY |
| S2 | The Quiet Error | FORMAL_REPORT / LOCAL_CORRECTION | 51 / 49 | 19 / 81 | LOW-POWER |
| S3 | The Department Reorganisation | ADOPT / WAIT | 50 / 50 | 54 / 46 | PRIMARY |
| C1 | The Resource Council | PACKAGE_A / PACKAGE_B | 51.5 / 48.5 | 72 / 28 | SECONDARY |
| C2 | The Restructuring Board (Milgram analogue) | APPROVE / REJECT | 50 / 50 | 73 / 27 | SECONDARY |
| C3 | The Scientific-Approach Dilemma | CONTINUE / PIVOT | 51 / 49 | 70 / 30 | SECONDARY |

The **0a** column is the original May-2026 naked calibration (locked, immutable in
`experiments/phase0_baseline_calibration/`). Four problems (S2/S3/C1/C2) drifted
on the current model and were **recalibrated to bistable naked** and re-locked in
`experiments/phase0b_calibration/questions/` (0a stays frozen). The **0c** column
is the fresh hash-locked holdout at N=1000 — it revealed that small-N recalibration
splits were partly sampling luck, so problems are used at these **0c-measured
baselines** (Phase 2 effects interpreted relative to them), tiered by headroom.
Full reasoning: `experiments/PHASE0_CLOSURE_2026-07-29.md`.

---

## Folder Structure

```
conceptual-architecture-methods/
│
├── Theory/                           # Thesis v0.6 + Implementation Spec v0.1 (canonical)
│
├── code/
│   ├── utils.py                      # R matrix, Beta marginals, config space, copula sampling, PSD check
│   ├── engine/                       # SOLID-decomposed LLM simulation engine (protocols + DI)
│   │   ├── llm_client.py             #   provider-agnostic async call layer (SupportsComplete)
│   │   ├── record_sink.py            #   write-once record storage (RecordSink protocol)
│   │   ├── questions.py              #   read locked dilemma bodies (0a frozen | 0b recalibrated)
│   │   ├── prompt_assembly.py        #   full-harness system-prompt population
│   │   ├── population.py             #   Gaussian-copula paired-agent draw
│   │   ├── delivery.py / framing.py  #   swappable message-shape + task-framing seams
│   │   ├── phase0b.py                #   null-condition + sweep assemblers (one Protocol)
│   │   ├── simple_runner.py          #   agent × config × problem grid runner
│   │   ├── recalibrate.py            #   naked-prompt recalibration rig
│   │   ├── scoring.py / parsing.py / seeding.py
│   │   └── selftest.py               #   29 offline invariance checks
│   ├── run_phase0b.py                # composition roots (CLIs) — one per phase step
│   ├── run_phase0c.py  run_phase1_pilot.py  run_phase1_5_sweep.py
│   ├── run_recalibrate.py  run_ablation.py  run_nulla_tasksweep.py
│   └── phase0_*.py                   # frozen provenance of the May-2026 0a runs (do not alter)
│
├── experiments/
│   ├── phase0_baseline_calibration/  # IMMUTABLE — May-2026 0a locked prompts + raw evals
│   ├── phase0b_calibration/questions/# RECALIBRATED locked set (used by 0b/0c/1+)
│   ├── phase0b_archive/              # dated harness-investigation runs + FINDINGS/RESULT md
│   ├── phase0c_locked_holdout/       # hash-locked holdout: frozen_prompts/manifest.json + results/
│   ├── phase1_pilot/                 # Phase 1 pilot runs + result
│   ├── phase1_5_encoding_validity/   # sweep pilot + (in progress) full battery
│   └── PHASE0_CLOSURE_2026-07-29.md  # the Phase 0 closure verdict
│
├── prompts/                          # system_prompt_template.md + recalibration candidate drafts
├── config/                           # seeds.json, configurations.json
├── docs/                             # variables.json, pre_analysis_plan.md, novelty_assessment.md
├── CLAUDE.md   meta.md   NEXT_STEPS.md   .gitignore   .gitattributes   README.md
```

---

## Running What Exists Today

The LLM engine and per-phase CLIs are implemented. All calls default to a mock
provider (offline); real runs use `--provider openai` and print a cost estimate +
confirmation. Records are write-once JSON, one file per call (anti-anchoring).

```bash
# Offline engine self-test (29 invariance checks)
python code/engine/selftest.py

# Verify the copula layer: PSD check + marginal-preserving sampling
python -c "import sys; sys.path.insert(0,'code'); import utils; \
  a = utils.sample_agents(1000, seed=42); print(a.shape, a.mean(axis=0).round(3))"

# Re-score an existing archived run (no API calls)
python code/run_phase0c.py --score-only

# Dry-run a harness assembly (prints prompts, no API, nothing written)
python code/run_phase0b.py --questions-set phase0b --problems C2 --conditions null_a --dry-run
```

The `code/phase0_*.py` runners/scorers are kept as executable provenance of the
locked May-2026 0a results (thesis §11.4); the forward pipeline is `code/engine/`
+ the `code/run_*.py` composition roots.

---

## Requirements

```
python >= 3.11
numpy >= 1.26
scipy >= 1.11
pandas >= 2.0
pymc >= 5.0          # Phase 3 (system architecture) onward
mesa >= 2.0          # Phase 2 complex onward
statsmodels >= 0.14  # Phase 5
plotly >= 5.0
matplotlib >= 3.8
pyarrow >= 12.0
openai >= 1.0        # gpt-5.4-mini calls
```

R with lme4/glmer is used as the cross-check for the Phase 5 mixed-effects models.

---

## Key References

- Milgram (1974). *Obedience to Authority.* — Authority benchmark.
- Asch (1956) + Bond & Smith (1996). — Loyalty benchmark (modernised band).
- Güth, Schmittberger & Schwarze (1982) + Oosterbeek et al. (2004). — Justice benchmark.
- Latané & Darley (1968, 1970) + Fischer et al. (2011). — Care benchmark.
- Worchel & Brehm (1970) + Rains (2013). — Freedom benchmark.
- Pan et al. (2023). MACHIAVELLI Benchmark, ICML. — Negative-valence moral taxonomy.
- Tyler (2006); Lee & Ashton (2004/2018); Eisenberg & Spinrad (2014); Aquino & Reed (2002). — Positive-valence anchors.
- Ryan & Deci (2000); Adams (1963); Kelman (1958, 1974); Davis (1983); Swann et al. (2012); Crimston et al. (2016). — Concept definitions and parameter anchors.
- Shapira & Bau et al. (2026). Agents of Chaos. arXiv:2602.20021. — Orchestration template.
- Full bibliography: `Theory/concepts_as_architecture_thesis_v0_6.md`, References section.

---

## Contact

- **Author:** Tommaso Piero Palamenga — Bocconi University
- **Status:** Thesis draft v0.6 / Implementation Spec v0.1 — not for citation.
