# PARIA: From Political Concepts to Simulated Judgment

> **Status:** Early-stage working paper. Draft 0.5 â€” April 2026.
> Not for citation. All design decisions are provisional.
> Author: Tommaso Piero Palamenga â€” Bocconi University

---

## What This Project Does

PARIA tests whether canonical psychological definitions of **freedom**, **justice**, **authority**, **care**, and **loyalty** can be encoded as transparent, uncertainty-aware parameter distributions that produce distinguishable and interpretable social dynamics in an LLM-powered agent-based simulation.

Each concept is reduced to a single canonical definition grounded in the psychological literature. These definitions are encoded as Beta distributions over ten shared parameters. Agents are sampled from a ten-dimensional joint distribution via Gaussian copula, then placed into one of thirty-two societal configurations. The simulation is validated against five behavioural benchmarks â€” one per concept â€” drawn from canonical social psychology.

**The central claim:** structured conceptual encodings can do genuine explanatory work â€” not just serve as decorative philosophical preface.

---

## Research Question

> Can canonical definitions of five political-ethical concepts â€” freedom, justice, authority, care, and loyalty â€” be encoded into uncertainty-aware parameter profiles that generate distinguishable and interpretable social dynamics?

---

## Current Phase

| Phase | Description | Status |
|-------|-------------|--------|
| 0 | Baseline calibration â€” 50/50 RLHF check (gpt-5.4-mini) | **ACTIVE** |
| 1 | Foundations â€” 10 parameters + 5 canonical definitions | **Complete** |
| 2 | Distribution Modelling â€” Beta marginals + Gaussian copula | **Substantially complete** |
| 3 | System Architecture â€” tool-based injection mechanism | **Next** |
| 4 | Simulation â€” Mesa ABM interaction loop | Pending |
| 5 | Evaluation â€” benchmark retrodiction | Pending |
| 6 | Analysis and Writing | Pending |

---

## Data

- **Raw data:** `data/raw/` â€” NEVER modified by any script. Contains empirical calibration data from psychometric instruments.
- **Processed data:** `data/processed/` â€” generated reproducibly by pipeline scripts.
- **Target population:** Western democratic adults (US, UK, Western Europe, Scandinavia, Australia). Italian/Southern European data as primary calibration anchor where available.

---

## The Ten Agent Parameters

| Code | Parameter | Scale | Beta(Î±, Î²) | Proxy |
|------|-----------|-------|------------|-------|
| LL | Legitimacy Locus | 0=internal â†’ 1=external | Beta(3.5, 2.5) | GCOS |
| CS | Constraint Sensitivity | 0=low â†’ 1=high | Beta(2.5, 2.0) | HPRS |
| RT | Response Threshold | 0=tolerant â†’ 1=hair-trigger | Beta(2.5, 2.5) | UG rejection thresholds |
| MoR | Mode of Response | 0=internal â†’ 1=external | Beta(2.0, 2.5) | STAXI / Thomas-Kilmann / IRI |
| RE | Relational Embedding | 0=atomised â†’ 1=relational | Beta(2.0, 3.0) | Singelis SCS |
| PD | Procedural Dependence | 0=outcome â†’ 1=process | Beta(2.5, 2.0) | Colquitt (2001) |
| TfA | Tolerance for Asymmetry | 0=egalitarian â†’ 1=hierarchical | Beta(2.0, 3.5) | SDO7 |
| ID | Internalisation Dependence | 0=surface â†’ 1=endorsement | Beta(3.0, 2.0) | SRQ |
| MS | Moral Scope | 0=local â†’ 1=universal | Beta(1.8, 1.5) | MES (Crimston et al. 2016) |
| AW | Affective Weighting | 0=cognitive â†’ 1=affective | Beta(2.2, 2.5) | Davis IRI EC/PT ratio |

Joint distribution: Gaussian copula with empirically anchored 10Ã—10 correlation matrix R (verified PSD, min eigenvalue = 0.311).

> **Changes from Draft 0.4:** PLBâ†’LL, CATâ†’RT, SMGâ†’MS (anchor: MFQ-2â†’MES); TO (Temporal Orientation) dropped; AW (Affective Weighting) added.

---

## Five Canonical Definitions

| Concept | Definition source |
|---------|------------------|
| Freedom | SDT (Ryan & Deci 1985, 2000) + Psychological Reactance Theory (Brehm 1966) |
| Justice | Equity Theory (Adams 1963) + Organisational Justice Framework (Colquitt 2001; Thibaut & Walker 1975) |
| Authority | Milgram (1963, 1974) + Kelman's three-process model (1958, 1974) |
| Care | Davis IRI (1983) + Batson empathy-altruism hypothesis (1981, 2011) + MES (Crimston et al. 2016) |
| Loyalty | Identity fusion theory (Swann et al. 2012) + Kelman complianceâ€“identificationâ€“internalisation framework |

---

## Societal Configurations

32 configurations from the 2âµ grid of (Freedom, Justice, Authority, Care, Loyalty) âˆˆ {0,1}âµ.

The proof-of-concept tests a defensible subset of **8â€“12 configurations** spanning the most antagonistic combinations.

**Primary validation target:** Config `00100` (Milgram-analogue: F=0, J=0, A=1, C=0, L=0) should produce obedience rates of 61â€“66%.

---

## Behavioural Benchmarks

| Concept | Benchmark | Target |
|---------|-----------|--------|
| Authority | Milgram (1974) obedience | 61â€“66% obedience in `00100` |
| Loyalty | Asch (1956) conformity | ~32â€“37% critical-trial conformity |
| Justice | Ultimatum Game (GÃ¼th et al. 1982) | Proposer offers 40â€“50%; ~40â€“50% rejection of 20% offers |
| Care | Bystander helping (LatanÃ© & Darley 1968) | ~75% alone; ~55% with 3+ bystanders |
| Freedom | Reactance restoration (Worchel & Brehm 1970) | ~15â€“25% option-attractiveness shift; Cohen's d â‰ˆ 0.45 |

---

## Experimental Problems (Phase 0 calibration active)

Six problems calibrated against gpt-5.4-mini baseline to confirm ~50/50 response distribution before parameter injection. See `experiments/phase0_baseline_calibration/`.

| ID | Name | Type |
|----|------|------|
| S1 | The Promotion Decision | Simple binary |
| S2 | The Quiet Error | Simple binary |
| S3 | The Strategic Pivot | Simple binary |
| C1 | The Resource Council | Complex multi-agent |
| C2 | The Restructuring Board | Complex multi-agent (Milgram analogue) |
| C3 | The Scientific-Approach Dilemma | Complex multi-agent |

---

## How to Run the Full Pipeline

```bash
# Entry point â€” available from Phase 4 onward
python code/run_all.py
```

Each script can also be run independently in order:

```bash
python code/01_intake.py
python code/02_distributions.py
python code/03_encode.py
python code/04_agents.py
python code/05_simulate.py
python code/06_evaluate.py
python code/07_output.py
```

---

## Folder Structure

```
PARIA/
â”‚
â”œâ”€â”€ data/
â”‚   â”œâ”€â”€ raw/               # IMMUTABLE. Empirical calibration data. Never touched by scripts.
â”‚   â””â”€â”€ processed/         # Reproducibly generated. Safe to delete and rebuild.
â”‚
â”œâ”€â”€ code/
â”‚   â”œâ”€â”€ 01_intake.py           # Load and validate raw calibration data
â”‚   â”œâ”€â”€ 02_distributions.py    # Beta marginal fitting + Gaussian copula construction
â”‚   â”œâ”€â”€ 03_encode.py           # Concept encoding (five concept priors via PyMC)
â”‚   â”œâ”€â”€ 04_agents.py           # Agent population sampling from joint distribution
â”‚   â”œâ”€â”€ 05_simulate.py         # Mesa ABM â€” interaction loop across societal configurations
â”‚   â”œâ”€â”€ 06_evaluate.py         # Validation: five benchmark retrodictions
â”‚   â”œâ”€â”€ 07_output.py           # Tables, figures, comparative dashboard (Plotly)
â”‚   â”œâ”€â”€ utils.py               # Shared helpers (copula sampling, PSD check, logging)
â”‚   â””â”€â”€ run_all.py             # Master entry point
â”‚
â”œâ”€â”€ output/
â”‚   â”œâ”€â”€ tables/
â”‚   â”œâ”€â”€ figures/
â”‚   â””â”€â”€ logs/
â”‚
â”œâ”€â”€ experiments/
â”‚   â””â”€â”€ phase0_baseline_calibration/   # 50/50 RLHF check via gpt-5.4-mini
â”‚       â”œâ”€â”€ README.md
â”‚       â”œâ”€â”€ questions/         # S1â€“S3 (simple), C1â€“C3 (complex) problem prompts
â”‚       â””â”€â”€ results/
â”‚           â”œâ”€â”€ raw/
â”‚           â”‚   â””â”€â”€ evals/     # One file per call/run â€” anti-anchoring isolation
â”‚           â”‚       â”œâ”€â”€ README.md
â”‚           â”‚       â”œâ”€â”€ S1_promotion_decision/    # N=200 per-call JSONs
â”‚           â”‚       â”œâ”€â”€ S2_quiet_error/           # N=200 per-call JSONs
â”‚           â”‚       â”œâ”€â”€ S3_strategic_pivot/       # N=200 per-call JSONs
â”‚           â”‚       â”œâ”€â”€ C1_resource_council/      # N=20 per-run transcripts
â”‚           â”‚       â”œâ”€â”€ C2_restructuring_board/   # N=20 per-run transcripts
â”‚           â”‚       â””â”€â”€ C3_scientific_approach/   # N=20 per-run transcripts
â”‚           â””â”€â”€ processed/     # Aggregated calibration results
â”‚
â”œâ”€â”€ notebooks/             # EXPLORATORY ONLY. Not authoritative.
â”‚
â”œâ”€â”€ docs/
â”‚   â”œâ”€â”€ variables.json         # Complete variable codebook (v2.0, Draft 0.5)
â”‚   â”œâ”€â”€ novelty_assessment.md  # L1 diagnosis
â”‚   â”œâ”€â”€ pre_analysis_plan.md   # Hypotheses and acceptance criteria
â”‚   â””â”€â”€ handoff/               # Session-ending handoff notes
â”‚
â”œâ”€â”€ tests/
â”œâ”€â”€ Theory/
â”‚   â””â”€â”€ conceptual_architecture_methods_paper_v0_5_with_graphs.pdf
â”‚
â”œâ”€â”€ CLAUDE.md                  # Project constitution (read every session)
â”œâ”€â”€ meta.md                    # Living log of decisions, limitations, and rule changes
â”œâ”€â”€ research-os-template.md
â”œâ”€â”€ .gitignore
â””â”€â”€ README.md
```

---

## Expected Outputs

| Artifact | Location | Description |
|----------|----------|-------------|
| `fig_01_parameter_distributions.html` | `output/figures/` | 10 Beta distribution plots |
| `fig_02_copula_sample.html` | `output/figures/` | 2D projections of agent population |
| `fig_03_obedience_by_config.html` | `output/figures/` | Obedience rates across configurations |
| `fig_04_benchmark_retrodictions.html` | `output/figures/` | Simulated vs. empirical for all 5 benchmarks |
| `table_01_parameter_summary.tex` | `output/tables/` | Summary statistics for 10 parameters |
| `table_02_config_results.tex` | `output/tables/` | Simulation results per configuration |
| `pipeline.log` | `output/logs/` | Full pipeline run log |
| `calibration_summary.csv` | `experiments/phase0_baseline_calibration/results/processed/` | Phase 0 baseline split per problem |

---

## Requirements

```
python >= 3.10
pymc >= 5.0
numpy >= 1.24
scipy >= 1.10
pandas >= 2.0
mesa >= 2.0
plotly >= 5.0
pyarrow >= 12.0
openai >= 1.0   # Phase 0 calibration only
```

---

## Key References

- Milgram (1974). *Obedience to Authority.* â€” Authority benchmark.
- Asch (1956). Conformity studies. â€” Loyalty benchmark.
- GÃ¼th, Schmittberger & Schwarze (1982). Ultimatum Game. â€” Justice benchmark.
- LatanÃ© & Darley (1968, 1970). Bystander intervention. â€” Care benchmark.
- Worchel & Brehm (1970). Reactance restoration. â€” Freedom benchmark.
- Ryan & Deci (2000). Self-Determination Theory. â€” Freedom definition.
- Adams (1963, 1965). Equity Theory. â€” Justice definition.
- Kelman (1958, 1974). Compliance, Identification, Internalisation. â€” Authority + Loyalty definitions.
- Davis (1983). Interpersonal Reactivity Index. â€” Care + AW parameter.
- Swann et al. (2012). Identity fusion theory. â€” Loyalty definition.
- Crimston et al. (2016). Moral Expansiveness Scale. â€” MS parameter anchor.
- Shapira & Bau et al. (2026). Agents of Chaos. arXiv:2602.20021. â€” Simulation methodology template.
- Full bibliography: `Theory/conceptual_architecture_methods_paper_v0_5_with_graphs.pdf`, references section.

---

## Contact

- **Author:** Tommaso Piero Palamenga â€” Bocconi University
- **Status:** Early-stage working paper, not for citation.
