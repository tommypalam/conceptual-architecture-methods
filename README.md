# PARIA / Concepts as Architecture: From Political Concepts to Simulated Judgment

> **Status:** Thesis draft v0.6 + Implementation Specification v0.1 (May 2026).
> Not for citation. All design decisions are provisional until empirically validated.
> Author: Tommaso Piero Palamenga — Bocconi University
> Supervisor: Dr. Abhinav · Co-supervisor: Prof. Arnaldo Camuffo

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
| 0 | Naked-prompt 50/50 baseline calibration (gpt-5.4-mini) | **COMPLETE** — all 6 problems locked 2026-05-02 |
| 0b | Harness-neutral baseline (3 null conditions × 6 problems × N=500) | **NEXT** — required gating |
| 0c | Locked holdout (frozen prompts, N=1000/problem) | Pending |
| 1 | Pilot (S2, one configuration, N=50) | Pending |
| 1.5 | Encoding-validity battery (~10k calls) — **hard gate** | Pending |
| 2 | Full experimental runs (paired-agent simple + orchestrated complex + bridge) | Pending |
| 3 | Benchmarks under contamination protocol | Pending |
| 4 | Moral coding (LLM-rater + human gold subset) | Pending |
| 5 | Analysis (mixed-effects primary, sensitivity, multi-model) | Pending |
| 6 | Reporting, OSF compliance, open-artefact release | Pending |

OSF pre-registration is required before Phase 2 (see [`docs/pre_analysis_plan.md`](docs/pre_analysis_plan.md)).

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

## Experimental Problems (Phase 0 locked 2026-05-02)

| ID | Name | Type | Labels | Phase 0 split |
|----|------|------|--------|----------------|
| S1 | The Promotion Decision | Simple binary | A / B | 53 / 47 |
| S2 | The Quiet Error | Simple binary | FORMAL_REPORT / LOCAL_CORRECTION | 51 / 49 |
| S3 | The Department Reorganisation | Simple binary | ADOPT / WAIT | 50 / 50 |
| C1 | The Resource Council | Complex multi-agent | PACKAGE_A / PACKAGE_B | 51.5 / 48.5 |
| C2 | The Restructuring Board | Complex multi-agent (Milgram analogue) | APPROVE / REJECT | 50 / 50 |
| C3 | The Scientific-Approach Dilemma | Complex multi-agent (epistemic) | CONTINUE / PIVOT | 51 / 49 |

Locked prompts, retired-variant archive, and raw per-call results live under `experiments/phase0_baseline_calibration/` — **immutable, never modified by any script or session**. (The S3 question file keeps its legacy `strategic_pivot` filename but contains the accepted Department Reorganisation prompt.)

---

## Folder Structure

```
conceptual-architecture-methods/
│
├── Theory/
│   ├── concepts_as_architecture_thesis_v0_6.md       # Thesis v0.6 (canonical, architecture)
│   └── implementation_specification_v0_1.md          # Spec v0.1 (canonical, operations)
│
├── code/
│   ├── utils.py                      # R matrix, Beta marginals, config space, copula sampling, PSD check, logging
│   ├── phase0_run_simple.py          # Phase 0 runner, S1–S3 (provenance — do not alter)
│   ├── phase0_run_complex_direct.py  # Phase 0 runner, C1–C3 direct calls (provenance)
│   ├── phase0_run_complex.py         # compatibility wrapper (provenance)
│   ├── phase0_score_simple.py        # Phase 0 scoring, S1–S3 (provenance)
│   ├── phase0_score_complex_direct.py# Phase 0 scoring, C1–C3 (provenance)
│   └── phase0_score_complex.py       # compatibility wrapper (provenance)
│
├── experiments/
│   └── phase0_baseline_calibration/  # IMMUTABLE. Locked prompts, archive, raw per-call JSONs, scoring.
│       ├── README.md
│       ├── questions/                # S1–S3, C1–C3 locked prompts + archive/ of retired variants
│       └── results/raw/evals/        # One JSON per call — anti-anchoring isolation
│
├── docs/
│   ├── variables.json                # Variable codebook v2.1 (synced to thesis v0.6)
│   ├── pre_analysis_plan.md          # Hypotheses + acceptance criteria (pre-register before Phase 2)
│   └── novelty_assessment.md         # L1 diagnosis — where AI assistance is and is not reliable
│
├── CLAUDE.md                         # Project constitution (read every session)
├── meta.md                           # Living log of decisions, limitations, rule changes
├── .gitignore
└── README.md
```

Future phase directories (`phase0b_harness_neutral/`, `phase0c_locked_holdout/`, `phase1_pilot/`, `phase1_5_encoding_validity/`, `phase2_*/`, `phase3_benchmarks/`, `phase4_coding/`, `phase5_analysis/`) and shared `config/` + `prompts/` artefacts are created as their phases begin, following spec §1.2.

---

## Running What Exists Today

The pipeline scripts for Phases 0b onward have not been written yet (the spec is the blueprint; code is generated against it phase by phase). What runs today:

```bash
# Verify the copula layer: PSD check + marginal-preserving sampling
python -c "import sys; sys.path.insert(0, 'code'); import utils; \
  a = utils.sample_agents(1000, seed=42); print(a.shape, a.mean(axis=0).round(3))"
```

The Phase 0 runners/scorers in `code/` are kept as the executable provenance of the locked Phase 0 results (thesis §11.4); they are not part of the forward pipeline.

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
