# PARIA — Pre-Analysis Plan

> This document is written BEFORE estimation. It is the commitment device.
> Deviations from this plan must be disclosed and logged in meta.md.
> Any analysis not described here requires explicit human approval before execution.
> Source of truth: `Theory/concepts_as_architecture_thesis_v0_6.md` (thesis v0.6) and `Theory/implementation_specification_v0_1.md` (spec v0.1).

---

## Status

**Draft — not yet finalised.** This placeholder is synced to thesis v0.6 / spec v0.1 (June 2026). It must be completed, pre-registered on OSF, and committed **before Phase 2 begins** (thesis §7.5.5: pre-registration covers primary contrasts, retrodiction bands, sample sizes, mixed-effects model specification, power analysis, and the coding manual). Running any Phase 2 or benchmark work without a committed, pre-registered plan is not permitted.

---

## Research Question

Can canonical definitions of five political-ethical concepts — freedom, justice, authority, care, and loyalty — be encoded into uncertainty-aware parameter profiles that generate distinguishable and interpretable social dynamics in an agent-based simulation?

---

## Gating Structure (must pass in order before any Phase 2 inference)

1. **Phase 0** — naked-prompt 50/50 calibration: **COMPLETE** (2026-05-02, all six problems passed; thesis Ch. 11).
2. **Phase 0b** — harness-neutral baseline: three null conditions (empty harness / population means at neutral config / sham profile) × six problems × N = 500. Pass: Wilson 95 % CI contains 50 % in all 18 cells (spec §2.1).
3. **Phase 0c** — locked holdout: prompts hash-frozen, N = 1000 per problem under null condition B, no-edit rule (spec §2.2).
4. **Phase 1** — pilot: S2, authority-low/justice-low config, N = 50; five diagnostics (spec Part 3).
5. **Phase 1.5** — encoding-validity battery: sweeps, coherence audit, paraphrase robustness, numeric/verbal variants; pass/partial/fail decision tree (thesis Ch. 8, spec Part 4). **Hard gate** — Phase 2 does not proceed on fail.

---

## Primary Hypotheses

### Benchmark retrodiction (Phase 3; thesis Ch. 5)

**H1 (Authority / Milgram):** populations in the Milgram-analogue configuration `00100` (F=0, J=0, A=1, C=0, L=0) produce maximum-voltage obedience of 61–66 % (Haslam, Loughnan & Perry 2014).

**H2 (Authority / configuration counterfactual — PRIMARY contamination diagnostic):** the authority-low counterfactual produces obedience substantially below `00100`; the high-vs-low difference (predicted ≈ 0.50), not the absolute rate, is the primary success criterion (thesis §5.3.3). The same counterfactual logic applies to all five benchmarks.

**H3 (Loyalty / Asch):** loyalty-high configurations produce 25–30 % critical-trial conformity (Bond & Smith 1996 modernised band; the original 32–37 % is superseded per thesis §5.1.2). Modulators: unanimity-breaking → 5–10 %; private response → 10–15 %; group-size plateau at N = 3.

**H4 (Justice / UG):** proposer offers cluster at 45–50 % of stake (modernised band per thesis §5.1.3); rejection of 20 %-offers ≈ 40–50 %; rejection-threshold mean ≈ 30–33 %.

**H5 (Care / Bystander):** care-high configurations produce ≈ 75 % alone-condition helping, ≈ 55 % with 3+ bystanders; dangerous-emergency condition attenuates or reverses the effect (Fischer et al. 2011).

**H6 (Freedom / Reactance):** freedom-low + authority-high configurations produce a between-subjects removed-adjacent-option shift of ≈ 15–25 pp (Cohen's d ≈ 0.45; Rains 2013), reformulated as a between-subjects rate per thesis §5.1.5.

**H7 (Cross-concept distinguishability):** the five concept encodings produce statistically distinguishable behavioural profiles across configurations — the conceptual encoding layer does explanatory work beyond random variation.

### Experimental-problem directional hypotheses (Phase 2; thesis §6.1.1)

Approximately 20 pre-registered primary contrasts across the six problems, tested as likelihood-ratio tests on nested mixed-effects models:

- **S1 Promotion Decision:** higher RE → A; higher TfA → A; higher PD → A.
- **S2 Quiet Error:** higher ID → FORMAL_REPORT; higher TfA → LOCAL_CORRECTION; higher MS → FORMAL_REPORT.
- **S3 Department Reorganisation:** higher RT → ADOPT; higher MoR → ADOPT; higher RE → WAIT.
- **C1 Resource Council:** higher TfA → PACKAGE_A; higher MS → PACKAGE_B; higher PD → longer time-to-consensus.
- **C2 Restructuring Board:** higher ID → REJECT; higher TfA → APPROVE; higher AW → more amendment-moves in rounds 1–4.
- **C3 Scientific-Approach Dilemma:** higher RT → CONTINUE; higher ID → higher information-sharing rate; higher AW → greater attention to disconfirming evidence.

---

## Primary Outcome Measures

- **Phase 2 simple:** per-problem binary decision under the paired-agent design (N = 200 profiles × 8–12 configurations, within-subjects).
- **Phase 2 complex:** C1 final package + time-to-consensus; C2 round-5 approval rate + amendment patterns; C3 round-6 vote + information-sharing/updating signatures. 20 runs per configuration; bridge-calibration (no-parameter) baselines reported alongside.
- **Phase 3 benchmarks:** retrodiction rates per configuration, canonical and decanonised variants, with the configuration-counterfactual difference as primary.
- **Phase 4 moral coding:** configuration-relative 8-vector and fixed-standard 4-vector per action (thesis Ch. 7); headline B(v_a) under strict-OR with net-score and weighted (w_n = 1.5) robustness aggregations.

---

## Planned Specifications

### Primary inference (thesis §7.5.5, spec §9.1)

Mixed-effects logistic regression per problem:
`logit P(y) = α + β_c·C + θ·γ + (C × θ)·δ + u_i`, agent-level random intercept for the paired-agent design. Fit in R (lme4/glmer), cross-checked in Python (statsmodels MixedLM). Pre-registered contrasts via LR tests on nested models. FDR control: Benjamini–Hochberg at q = 0.05 within each problem's pre-registered family. Power: simulation-based, K = 1,000 datasets per contrast, target ≥ 0.80; contrasts below 0.50 flagged as below resolution.

### Secondary descriptive analyses

Mann–Whitney U with Cohen's h (pairwise), Kruskal–Wallis H with η²_H (omnibus), Wilson 95 % CIs, non-parametric bootstrap (10,000 resamples). Mixed-effects results take precedence on disagreement.

### Robustness checks

- R-matrix regimes B (weak zeroed), C (+20 %), D (weak-joint perturbation, 100 matrices, 95-percentile band)
- t-copula df ∈ {4, 8, 16}
- AW on/off (9- vs 10-parameter sensitivity)
- Multi-model robustness: Phase 0 + one full S2 run replicated on a second model (≈ 3,200 calls)
- Behavioural separability: exploratory factor analysis on Phase 2 agent-level decision matrices
- Fixed-standard vs configuration-relative ranking comparison (divergence is itself a finding)

---

## What Counts as Failure

- Configuration-counterfactual difference absent (canonical rate reproduced regardless of configuration) → benchmark contaminated; per-concept calibration unverified (thesis §5.3).
- Config `00100` obedience outside [0.61, 0.66] under Regime A → recalibration of primary parameters, logged, panel-reviewed, never silent.
- Any benchmark fails across all R regimes → corresponding concept encoding re-examined.
- Phase 1.5 sweep test fails → Phase 2 does not proceed under system-prompt injection; tool-based injection path (spec §4.5).
- No statistically distinguishable difference across concept encodings → the conceptual encoding layer does not do explanatory work → primary contribution fails.
- Phase 0b/0c failures → contingency trees of spec §2.1.5/§2.2.2/§2.3 (including the Appendix A descope path).

---

## Pre-Registration

*Not yet pre-registered.* OSF pre-registration is **required before Phase 2** and follows the seven-section template of spec §10.2 (hypotheses, methods, analysis plan, coding manual hash, sensitivity, stopping rules, post-experiment compliance report).

Pre-registration URL: `[TO BE ADDED]`

---

*Synced to thesis v0.6 / spec v0.1: 2026-06-11. Must be finalised, pre-registered, and committed before Phase 2.*
