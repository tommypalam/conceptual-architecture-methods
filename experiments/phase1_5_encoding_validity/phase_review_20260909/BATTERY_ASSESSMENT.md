# Phase 1.5 — empirical battery complete, current gate not met

Assessment date: 2026-09-09. Neutral context, root seed 20260604. Behavioural
model: `gpt-5.4-mini-2026-03-17`; independent coding/generation model:
`claude-haiku-4-5-20251001`. No historical September 6 sample was pooled.

**The existing full ten-parameter system-prompt implementation is not cleared
for Phase 2.** All authorised battery collection is complete. A full pass is
ruled out by the measured results. No architectural revision, parameter removal,
new hypothesis, model swap or main-study launch is made here.

| Evidence | Completed collection | What it establishes and limits |
|---|---|---|
| Single-parameter sweep | 15,000 valid responses | Full-harness complete criterion met for MoR/S3, PD/S1, MS/S2; bare delivery only MS/S2. LL/CS/AW lack prespecified simple-problem directions and are not labelled failures for that reason. |
| Representation rotations | 4,500 records; 4,498 valid | Large descriptive representation differences; one .8 rotation per parameter does not measure slopes. |
| Numeric/verbal gradients | 15,000 records; 14,998 valid | Two of six eligible retention comparisons meet the existing rule: verbal MoR/S3 and numeric PD/S1. Numeric MoR and MS fall below .50 of their hybrid slopes. PD/S1 is severely ceiling-limited. |
| Blind reasoning audit | 200 valid coding records | Literal thresholds met, but all aggregate accuracies lie below empirical majority baselines; no active-parameter permutation p<.05. Twenty active items per parameter limit sensitivity; this is not proof of no recoverability. |
| Approved paraphrases | 4,500 records; 4,497 valid, plus 1,500 reused canonical observations | 8/30 cells establish all-pair equivalence, versus 24 required. One cell misses the parse floor. Large observed S2/S3 differences coexist with limited equivalence power at N=50. |

There are 39,000 unique behavioural responses in the fresh source and follow-ups,
38,993 valid parses and seven preserved parsing failures, with zero terminal API
failures in those four behavioural runs. The audit has its separately documented
preserved malformed attempts and continuation; these are not erased or pooled
into the effective 200-item coding sample. Raw records are local with committed
checksum inventories and integrity-checked same-computer ZIPs. No off-device
backup or GitHub push is claimed.

The [combined evidence matrix](evidence_a8076369a0ab8aa4.json) links all source
reports and their hashes. Its machine-generated status is
SCIENTIFIC_REVIEW_REQUIRED: supplying every report does not make a scientific
gate pass. Individual run reports retain confidence intervals and exact criteria.
The [paraphrase report](../paraphrases_20260909_final/analysis/PARAPHRASE_REPORT.md)
documents the final experiment in detail.

## Interpretation and next decision

The evidence supports some parameter sensitivity, especially MoR and MS, but
does not support the intended combination of broad graded encoding, recoverable
reasoning, and robustness across semantically reviewed wordings. S1's near-fixed
choices can make agreement look strong while offering little discriminating
information. The audit's class-prevalence imbalance prevents its literal
threshold pass from resolving interpretability. Paraphrase non-equivalence
alone must not be equated with proven difference, but large observed rate shifts
and reduced numeric gradients are substantive reasons to withhold readiness.

Under thesis section 8.2, full pass requires all subtests. The partial-pass path
requires an explicit revised architecture and revised hypotheses; it is not
permission to proceed with unchanged ten-parameter claims. The fail branch names
alternative injection mechanisms as possible future research. These observations
do not establish which redesign would work, nor that the underlying conceptual
theory is false. Final classification and the smallest defensible next study
must be discussed with the researcher before implementation.

The user's binding-constraint rule remains controlling: existing documented
amendments are preserved; any new theoretical departure needs a concrete physical
or technical limitation, evidence, and prior consultation. Weak results alone
are not permission to redefine constructs, remove inconvenient parameters,
increase sample sizes selectively or alter locked dilemmas to obtain a pass.

Synthetic five-perspective review: Linden separates conceptual coherence from
successful operational encoding. Osei treats ceiling effects and task coverage as
measurement constraints without claiming all parameters are ineffective. Tanaka
retains failed criteria while distinguishing low-power equivalence and active-
audit diagnostics from proof of absence. Renna sees delivery/representation
dependence as an unresolved mechanism problem. Okafor confirms the completed,
recoverable empirical record and recommends a concrete next-study proposal
before more spending. Resolution: battery collection complete; gate not met;
hold Phase 2 and consult on the next research decision, without silently choosing
a partial-pass redesign or abandoning the theory.
