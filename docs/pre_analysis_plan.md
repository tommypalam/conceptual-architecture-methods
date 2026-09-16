# Concepts as Architecture — Pre-Analysis Plan

> This is a draft for future main-study estimation; it is not publicly preregistered.
> Deviations from this plan must be disclosed here, with a current pointer in NEXT_STEPS.md.
> The legacy hypotheses below are historical plans, not prerequisites for every new exploratory analysis.
> Current operational policy: [implementation v0.2](../Theory/implementation_specification_v0_2.md), alongside thesis v0.6 and unchanged v0.1 conventions.

---

## Status

13 September 2026: the researcher clarified that the thesis is exploratory and
authorised adapting its implementation while maintaining research discipline.
The central moral-outcome experiment remains a required contribution. Use the
[current amendment](../Theory/implementation_specification_v0_2.md) for prospective
batch definitions, transparent revisions and the distinction between exploration
and later confirmation. The statements below requiring this entire historical
plan before Phase 2 are superseded by the recorded study-specific protocols and
amendments. None of this changes earlier tests or retrospectively preregisters them.
No new coding manual or paid collection is approved by this status update.

Later 13 September amendment: the researcher ruled out human raters for budget
reasons. The [AI-assisted scope](../experiments/phase4_coding/AI_ONLY_SCOPE_20260913.md)
supersedes human-rating completion prerequisites. It keeps the central moral
experiment, prospective manual freezes, independent AI coding and factual checks;
human validation and human-consensus claims are deferred.

2026-09-12 continuation: the researcher authorised expedited Phase 2 design work
under a $100 absolute API cap. The [revised design proposal](../experiments/phase2_design_20260912/PROTOCOL_DRAFT.md)
specifies scope, matched controls, implementation findings and outstanding review.
The original broad-study hypotheses below remain preserved; the proposal is not
yet the final preregistered execution plan and introduces no retrospective pass.

Updated 2026-09-12: the hypotheses below retain the original broad-study draft.
They are not newly authorised by scoped Phase 1.5 closure. The concrete downstream
design remains to be settled. Only status text changed during cleanup; the
[previous draft](../archive/phase2/documents/pre_analysis_plan_before_cleanup_2026-09-12.md) is preserved.

**Draft — not yet finalised.** This placeholder is synced to thesis v0.6 / spec v0.1 (June 2026). It must be completed, pre-registered on OSF, and committed **before Phase 2 begins** (thesis §7.5.5: pre-registration covers primary contrasts, retrodiction bands, sample sizes, mixed-effects model specification, power analysis, and the coding manual). Running any Phase 2 or benchmark work without a committed, pre-registered plan is not permitted.

---

## Research Question

Can canonical definitions of five political-ethical concepts — freedom, justice, authority, care, and loyalty — be encoded into uncertainty-aware parameter profiles that generate distinguishable and interpretable social dynamics in an agent-based simulation?

---

## Gating Structure (must pass in order before any Phase 2 inference)

1. **Phase 0a–0c:** closed under the documented [July closure](../experiments/PHASE0_CLOSURE_2026-07-29.md).
   The tested harness was non-neutral; the holdout used naked delivery and
   established measured baselines with inference tiers. The original all-cells
   50/50 and null-B holdout specifications were not attained as written.
2. **Phase 1:** operational pilot passed on S3 and S2, N=50 each. This does not
   establish encoding validity.
3. **Phase 1.5:** closed for the researcher-accepted limited objective. Local
   normative parameterization is supported; the original full battery remains
   unmet. This does not validate the original full-architecture Phase 2 design.
   See the [accepted closure](../experiments/phase1_5_encoding_validity/ACCEPTED_CLOSURE_2026-09-12.md).
4. **Before Phase 2:** finalise and preregister this plan and the coding manual;
   define a downstream scope supported by the evidence and record accepted deviations.

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

Approximately 20 candidate primary contrasts to be finalised and preregistered across the six problems, tested as likelihood-ratio tests on nested mixed-effects models:

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
`logit P(y) = α + β_c·C + θ·γ + (C × θ)·δ + u_i`, agent-level random intercept for the paired-agent design. The intended primary fit is binomial mixed-effects logistic regression in R
(`lme4/glmer`). The Python cross-check remains to be specified: the older draft's
[`statsmodels MixedLM`](https://www.statsmodels.org/stable/generated/statsmodels.regression.mixed_linear_model.MixedLM.html) is a linear mixed-effects model, not a binomial-logit implementation, and must not be
treated as an equivalent estimator. Resolve and validate the cross-check before
preregistration; no main-study fit is implemented or claimed here. Pre-registered contrasts via LR tests on nested models. FDR control: Benjamini–Hochberg at q = 0.05 within each problem's pre-registered family. Power: simulation-based, K = 1,000 datasets per contrast, target ≥ 0.80; contrasts below 0.50 flagged as below resolution.

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

*Status reconciled 2026-09-06. Original hypotheses retained; no new preregistration or retrospective confirmation is claimed.*
