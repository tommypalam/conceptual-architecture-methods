# Phase 3: concrete issues to reconcile before collection

The full five-benchmark scope is retained. Following the spec requires resolving
its internal inconsistencies; this document proposes decisions, it does not amend
the frozen theory or authorize a narrower experiment. No paid call has been made.

## 1. The dependence-sensitivity budget has two incompatible readings

Sections 7.6-7.7 require 100 weak-R perturbations, but budget D as if it were
one N=100 regime. A percentile band of rates across matrices needs a rate estimate
for each matrix. Assigning one agent to each matrix gives 100 binary outcomes,
not 100 useful matrix-specific rate estimates.

The offline planner includes all five benchmarks, 500 recognition probes,
4,000 primary slots, all nine explicitly listed modulator cells (900 calls),
B/C and the three t-copula regimes. It reuses the primary A sample instead of
billing A twice. Nominal counts under alternative D allocations are:

| Profiles per D matrix, per benchmark/context | Nominal calls | Benchmark-only cost illustration |
|---|---:|---:|
| 1 | 11,400 | $21.58 |
| 10 | 20,400 | $39.40 |
| 100 | 110,400 | $217.60 |

Costs assume 1,500 input and 150 output tokens per benchmark call, the verified
$0.75/$4.50 per million standard global rates, and 10% allowance. They EXCLUDE
judge/generation/rater costs and extra role, trial or trajectory calls. They are
not quotes or hard upper bounds. At 600 output tokens the same cases become
$45.86, $83.73 and $462.40 before those exclusions. See preflight_report.json.
The carried-forward $100 cap has $77.093926975 remaining accounting room after
Phase 2; this is not a verified provider balance.

Recommendation: do not select the one-agent interpretation to make the budget
appear compliant. Prepare Phase 3 in separately frozen stages: scenario validation,
then all-five primary and modulator collection, then the complete sensitivity
stage once an explicit D precision/cost allocation is reviewed. No Phase 3 closure
or full sensitivity pass is claimed while that last stage is outstanding. A
reduced per-matrix sample would be a documented amendment, not the literal N=100
interpretation. No option is selected and no spending is authorized by this table.

Price source, checked 2026-09-13:
https://developers.openai.com/api/docs/models/gpt-5.4-mini

## 2. Human reference targets need source-matched outcomes

The source audit found at least one concrete bibliographic error: the thesis
calls Rains (2013) a 123-study synthesis, while the publication reports 20 studies
and 4,942 participants. It studies models of reactance involving anger and
counterarguments. Its abstract does not validate the proposed adjacent-option
binary rate or a universal d=.45 to probability-difference=.20 conversion.

The Bystander paper cited as a meta-analytic anchor reports standardized g=-.35
and moderator dependence; that alone does not establish a universal 75%-to-55%
helping pair for the proposed software-incident task. The smoke study and seizure
study must not be combined as if they used the same procedure and denominator.

Recommendation: correct the source facts in a prospective erratum and specify
which human outcome matches each task before freezing thresholds. Preserve any
additional theory-derived prediction, but label it as a prediction rather than
an established human rate. See SOURCE_AUDIT.md for the inspected sources and limits.

## 3. The nominal call unit does not define the actual benchmark procedure

- Milgram's maximum-step outcome requires a specified escalation/stop procedure;
  answering one final-step vignette is not the same measure.
- Asch uses critical perceptual trials. Freeze stimuli, number of trials and the
  participant-level denominator; do not tell the model which answer is correct.
- Ultimatum needs separate proposer offers and responder decisions, including
  stated offer levels. A single 20% responder question cannot measure both roles.
- Bystander needs alone/group and danger conditions, a time window and a clear
  individual-versus-group helping denominator.
- Reactance needs a defined threat/control contrast and preference measurement.
  A ranking change and a binary adjacent-choice rate are not interchangeable.

Recommendation: write the five operational protocols around those measurements
before emitting a paid schedule. Do not shrink the procedures to one API request
per agent merely to match the budget paragraph. Scenario equivalents require the
separate-model generation and independent reader review in section 7.2.1.

## 4. Contexts, inference and recognition require explicit definitions

The draft registry preserves the spec's neutral off-target axes. NEUTRAL is not
silently mapped to binary 0 and is not a new LPM coordinate. The low-rate settings
are marked as proposed or unresolved. Ultimatum's high-rejection context direction
must be settled before labels such as high_rate can be assigned honestly.

The spec's configuration-counterfactual is useful evidence, but a context-only
model could also reproduce a high/low pattern. The existing primary prescription
has no context-only execution arm. Add an explicitly costed E/U comparator as a
prospective enhancement if whole-profile attribution is the intended Phase 3
claim; otherwise restrict inference to the encoded system's overall benchmark
behaviour. This addition is proposed, not assumed or counted in the nominal table.

Recognition failures and modulator failures warrant different labels. Recognition
below 30% does not prove absence of training-data contamination. A failed modulator
prediction can also be a model/measurement failure, so it must not automatically
be explained away as contamination. Keep the spec's required checks while making
these inferential limits explicit.

## Proposed next approval

Approve a spec-reconciliation pass that preserves all five benchmarks and all
planned sensitivity components, corrects source mismatches, defines the procedures
and contexts, and prepares separate freezes for the validation, primary/modulator,
and sensitivity stages. Keep the $100 hard cap; present the final priced schedule
and any per-matrix sample amendment before paid release. This is a request to
resolve methodological choices, not a request to repeat authorization to start
Phase 3 preparation.

AGENTS.md requires discussing a new methodological departure before implementation.
The original spec and completed Phase 2 records have therefore not been rewritten.

## Synthetic review of this proposal

Linden: defend behavioural comparability without promoting recognition tests to
proof of understanding. Osei: procedure, stakes and trial denominators must survive
variant generation. Tanaka: one observation per matrix cannot estimate the requested
matrix-level rate distribution; propagate both sampling and matrix uncertainty.
Renna: retain all five concepts, ten coordinates and every planned dependence
regime; neutral benchmark contexts need their own representation. Okafor: staged
release makes the study reviewable under a hard cap without pretending all stages
are complete. Disagreement concerns extra controls and feasible D replication;
resolution is to present these as prospective choices, not execute them silently.
These are synthetic perspectives, not the independent review required by section 7.2.
