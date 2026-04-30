# PARIA â€” Pre-Analysis Plan

> This document is written BEFORE estimation. It is the commitment device.
> Deviations from this plan must be disclosed and logged in meta.md.
> Any analysis not described here requires explicit human approval before execution.

---

## Status

**Draft â€” not yet finalised.** This document is a placeholder updated to reflect Draft 0.5 scope. It must be completed and committed before Phase 5 (Evaluation) begins. Running any benchmark retrodiction test without a committed pre-analysis plan is not permitted.

---

## Research Question

Can canonical definitions of five political-ethical concepts â€” freedom, justice, authority, care, and loyalty â€” be encoded into uncertainty-aware parameter profiles that generate distinguishable and interpretable social dynamics in an agent-based simulation?

---

## Primary Hypotheses

**H1 (Authority / Milgram):** Agent populations placed in the Milgram-analogue configuration `00100` (F=0, J=0, A=1, C=0, L=0) will produce obedience rates in the range of 61â€“66%, replicating Milgram's (1974) baseline.

**H2 (Authority / contrast):** Agent populations placed in the inverse configuration will produce obedience rates significantly below the `00100` configuration.

**H3 (Loyalty / Asch):** Agent populations in a loyalty-high configuration will produce conformity rates of approximately 32â€“37% on critical trials, replicating Asch (1956).

**H4 (Justice / UG):** Agent populations in a justice-calibrated configuration will produce proposer offers clustering at 40â€“50% of stake, with rejection rates for 20% offers of approximately 40â€“50%, replicating Ultimatum Game norms (GÃ¼th et al. 1982; Oosterbeek et al. 2004 meta-analysis).

**H5 (Care / Bystander):** Agent populations in a care-high configuration will produce helping rates of approximately 75% alone and approximately 55% with three or more bystanders (Fischer et al. 2011 meta-analysis).

**H6 (Freedom / Reactance):** Agent populations in a freedom-low + authority-high configuration will produce option-attractiveness shifts of approximately 15â€“25% following removal, with Cohen's d â‰ˆ 0.45 (Rains 2013 meta-analysis).

**H7 (Cross-concept distinguishability):** The five concept encodings will produce statistically distinguishable behavioural profiles across configurations â€” i.e., the conceptual encoding layer does explanatory work beyond random variation.

---

## Phase 0 Calibration Requirement

Each experimental problem must produce an approximately 50/50 binary response distribution under gpt-5.4-mini baseline â€” before any parameter profile is injected.

**Calibration target:** 45/55 to 55/45. Problems outside 40/60â€“60/40 are rewritten or replaced before Phase 1.

See `experiments/phase0_baseline_calibration/` for protocol and results.

---

## Primary Outcome Measures

**Benchmark retrodictions (Phases 4â€“5):**
- Obedience rate per config (authority/Milgram): proportion of agents complying with authority directive
- Conformity rate per config (loyalty/Asch): proportion of agents conforming on critical trials
- UG offer distribution and rejection rate (justice)
- Helping rate by bystander count (care)
- Option attractiveness shift following removal (freedom)

All reported as point estimate with 95% CI across N=20 runs per configuration.

> NOTE: The precise operationalisation of several measures is not yet defined. This must be resolved before Phase 5 begins. See Limitation L1 in meta.md.

---

## Secondary Outcomes

*To be defined before Phase 5.*

- [ ] Welfare score (Limitation L1 â€” not yet formalised)
- [ ] Behavioural divergence across concept encodings (H7)
- [ ] Sensitivity of all metrics to R matrix regime (A vs. B vs. C)
- [ ] Within-configuration variance across parameter profiles

---

## Planned Specifications

### Primary Specification

- Configurations: defensible subset of 8â€“12 from 32 total, including Milgram-analogue `00100` and concept-isolation configurations
- N agents per run: 500
- N runs per configuration: 20
- Random seed: to be logged at runtime and recorded here before results are reported
- R matrix regime: Regime A (as specified in variables.json / utils.py)
- Agent sampling: Gaussian copula via utils.sample_agents()

### Phase 0 Specification

- Model: `gpt-5.4-mini`
- Temperature: 1.0
- System prompt: none (bare baseline)
- N calls per simple problem: 200
- N runs per complex problem: 20

### Robustness Checks (planned)

- [ ] Regime B: R with all |r| < 0.25 zeroed
- [ ] Regime C: R with all correlations inflated 20% (verify PSD first)
- [ ] Reduced N: 200 agents per config (test population size sensitivity â€” Limitation L6)
- [ ] t-copula replacement (Limitation L3 â€” flag if results differ qualitatively)
- [ ] AW parameter sensitivity: re-run with AW zeroed from all R entries (Limitation L7)

---

## Validation Benchmarks

| Concept | Benchmark | Primary source | Meta-analytic anchor | Retrodiction target |
|---------|-----------|----------------|---------------------|---------------------|
| Authority | Milgram obedience | Milgram (1974) | Haslam, Loughnan & Perry (2014) | 61â€“66% obedience in `00100` |
| Loyalty | Asch conformity | Asch (1956) | Bond & Smith (1996), 133 studies | ~32â€“37% conformity on critical trials |
| Justice | Ultimatum Game | GÃ¼th et al. (1982) | Oosterbeek, Sloof & van de Kuilen (2004) | Proposer offers 40â€“50%; ~40â€“50% rejection of 20% offers |
| Care | Bystander helping | LatanÃ© & Darley (1968, 1970) | Fischer et al. (2011), 53 studies | ~75% alone; ~55% with 3+ bystanders |
| Freedom | Reactance restoration | Worchel & Brehm (1970) | Rains (2013), 123 studies | ~15â€“25% shift; Cohen's d â‰ˆ 0.45 |

> **Stanford Prison Experiment: explicitly excluded.** No quantifiable retrodiction target. Documented methodological contamination. Role-transformation phenomenon addressed via C2 (Restructuring Board) in experimental problems.

---

## What Counts as Failure

- Config `00100` obedience rate outside [0.61, 0.66] â†’ R matrix requires recalibration (logged, panel review, not silent fix)
- Any benchmark retrodiction fails across all three R regimes â†’ corresponding concept encoding requires re-examination
- No statistically distinguishable difference across concept encodings â†’ conceptual encoding layer does not do explanatory work â†’ primary contribution fails
- Results sensitive to R regime and RT â†” MS is the driving correlation â†’ Limitation L2 is load-bearing â†’ direct empirical grounding required before publication
- Any Phase 0 calibration outside 40/60â€“60/40 â†’ problem must be rewritten before deployment

---

## Pre-Registration

*This document is not yet pre-registered. Pre-registration on OSF or equivalent is recommended before any results are reported externally.*

Pre-registration URL: `[TO BE ADDED]`

---

*Placeholder updated: 2026-04-21 (Draft 0.5 â€” five concepts, five benchmarks). Must be finalised and committed before Phase 5.*
