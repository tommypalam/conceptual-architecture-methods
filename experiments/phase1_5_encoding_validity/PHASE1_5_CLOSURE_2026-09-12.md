# Phase 1.5 closure: parameter influence established locally; full validity gate unmet

Closed 12 September 2026 at the researcher's request. This closes collection and
evaluation of the implementation tested here. **It is not a validity pass or a
pass-with-revision. Phase 2 remains on hold.** No further API calls are queued.

## Scientific conclusion

The tested model responds to some numerical parameter interventions under fixed
canonical wording. The strongest follow-up evidence is transfer of MoR and MS
endpoint effects across prospectively sampled complete profile backgrounds.
However, the full ten-parameter architecture has not established the intended
combination of graded response, active-trait recoverability and robustness across
approved wordings and representations. Local behavioural control is evidence
toward encoding; it does not establish an internal understanding of ethics or
exclude alternative explanations based on prompt conditioning.

This outcome limits the tested implementation and the claims currently justified.
It does not show that ethics cannot be encoded, falsify the conceptual theory as
a whole, or show that every unsupported parameter has zero effect. Closure does
not change any original success threshold or retroactively designate exploratory
follow-ups as a confirmatory replacement battery.

## Original battery: retain the complete gate result

Neutral context; behavioural model `gpt-5.4-mini-2026-03-17`; root seed 20260604.
The independent audit used `claude-haiku-4-5-20251001`. The September 6 interrupted
sample was not pooled into the fresh September 9 battery.

| Component | Collection | Result relevant to the gate |
|---|---|---|
| Parameter sweep | 15,000 valid responses | Three of nine prespecified directional hypotheses meet the full-harness complete criterion: MoR/S3, PD/S1, MS/S2. This denominator is not the 30 parameter/problem cells. LL, CS and AW lack prespecified simple-problem directions and are not failures for that reason. |
| Representation rotations | 4,500 responses; 4,498 valid | Descriptive differences; these single-position comparisons do not establish gradient retention. |
| Numeric/verbal gradients | 15,000 responses; 14,998 valid | Two of six eligible retention comparisons pass: verbal MoR/S3 and numeric PD/S1. No eligible parameter/problem pair passes both representations. PD/S1 is severely ceiling-limited. |
| Blind reasoning audit | 200 valid coding records | Literal thresholds are met, but aggregate accuracy falls below empirical majority baselines; no active-parameter permutation p<.05. Only 20 active items per parameter limit sensitivity. Active-trait recovery is not established, and absence of recovery is not proved. |
| Approved paraphrases | 4,500 responses; 4,497 valid, with 1,500 canonical observations reused | **8/30** cells establish all-pair equivalence; **24** are required. One cell misses the parse floor. Limited equivalence power and substantial observed wording differences both matter. |

These four behavioural collections contain **39,000 unique responses, 38,993 valid
parses and seven preserved parsing failures**; the audit is separate. The reused
canonical observations are not additional calls. These are original-battery
counts, not a grand total including every subsequent diagnostic. Failure to
establish equivalence is not itself proof of a meaningful difference.

The [original assessment](phase_review_20260909/BATTERY_ASSESSMENT.md) and its
[hashed evidence matrix](phase_review_20260909/evidence_a8076369a0ab8aa4.json)
retain the criteria, underlying estimates and source reports.

## What the subsequent diagnostics added

The following studies were targeted development diagnostics. They provide
mechanism clues and boundaries; their local successes do not overwrite the
original gate or erase unsuccessful candidates.

| Diagnostic | Finding | Interpretation boundary |
|---|---|---|
| [Profile ablation](profile_ablation_20260911/analysis/INTERPRETATION.md), 300 responses | MoR-only slope 6.276 versus full-ten 2.831; difference +3.445, 95% interval [.827, 6.064]. | Removing nine parameters changes content, length and conditioning together. The isolated curve still misses observed monotonicity; presentation overload is not established as the sole explanation. |
| [PD interaction](pd_interaction_20260911/analysis/INTERPRETATION.md), 300 responses | High-PD versus low-PD MoR slope contrast +3.491, 95% interval [.479, 6.503]. | Supports context-dependent response under unchanged text; the contrast depends on the linear-logit model. The secondary risk-scale interaction interval includes zero. |
| [Expanded original-wording screen](original_expanded_20260911/analysis/INTERPRETATION.md), 640 responses | Four of eight primary directional comparisons supported after adjustment: three MoR wordings and canonical MS. | Selected-case evidence; MS did not transfer consistently across wordings. |
| [Tool delivery](tool_delivery_20260911/analysis/INTERPRETATION.md), 320 decisions from 480 API calls | This candidate did not meet the scale-up rule and attenuated MoR sensitivity. | A failed implementation of tool delivery, not a test of every possible tool architecture. |
| [Offline repeat stability](repeat_stability_20260912/INTERPRETATION.md) | Five adjusted detections among 139 between-run comparisons; three among 188 within-run comparisons. | Separate comparison families, selected historical records; non-detection is not equivalence. The analysis indexes existing data, not new responses. |
| [Exact-seed MS replay](ms_seed_replay_20260912/analysis/INTERPRETATION.md), 40 responses | One cohort reproduced 14/20; another changed from 0/20 to 9/20 under identical recorded request settings and seeds. | Seed-list changes alone cannot explain the discrepancy. Post-selection and stochastic responses remain; no backend cause was identified. |

The approved [axis-instruction pilot](axis_instruction_20260911_assembled/analysis/INTERPRETATION.md),
[joint-wording test](joint_wording_20260911/analysis/INTERPRETATION.md) and
[MS stanza crossover](ms_stanza_crossover_20260912/analysis/INTERPRETATION.md)
also remain part of the contrary or inconclusive evidence. Exact wording controls
one source of variation; fixing wording does not by itself establish that numerical
parameters have the intended graded and interpretable effects.

## Final transfer test: preserve positives and limits together

The [360-response transfer study](profile_transfer_20260912/analysis/INTERPRETATION.md)
used all 20 prospectively sampled backgrounds, three separately varied parameters,
three values (.1/.5/.9) and two complete blocks. Other-nine values, canonical
descriptions and locked dilemmas were held fixed within each triplet. There were
no failures, missing outcomes, replacements or historical pooling.

| Parameter / target | Target counts at .1 / .5 / .9, each out of 40 | Mean high-minus-low effect | Adjusted interval | Block effects | Frozen local criterion |
|---|---|---:|---|---|---|
| MoR / S3 ADOPT | 9 / 16 / 32 | +57.5 percentage points | [40.0, 75.0] pp | +60 / +55 pp | Met |
| MS / S2 FORMAL_REPORT | 3 / 1 / 14 | +27.5 percentage points | [10.0, 45.0] pp | +35 / +20 pp | Met |
| RE / S3 WAIT | 20 / 22 / 22 | +5.0 percentage points | [-15.0, 27.5] pp | +20 / -10 pp | Not established |

Intervals are individual 98.333% percentile-bootstrap intervals, Bonferroni-adjusted
across three primary comparisons, with 50,000 shared whole-background resamples.
The uncertainty units are **20 backgrounds**, not 360 independent agents; coverage
is approximate. The local rule also required positive effects in both blocks.
Neutral context; draw seed 20260929, ordering seed 20260930, analysis seed 20261001;
model `gpt-5.4-mini-2026-03-17`, temperature 1, maximum output 600 tokens.

**MS is not an ordered gradient:** 7.5%, 2.5%, 35%. Its endpoint result does not
resolve graded encoding. MoR is ordered at these three levels (22.5%, 40%, 80%),
which does not replace the original five-point test. RE's interval and opposite
block signs leave its predicted effect unresolved rather than disproved.
These are new backgrounds but familiar dilemmas selected after earlier evidence.
Intervening on one coordinate creates counterfactual profiles, not untouched draws
from the joint population. No interaction model or new wording/recovery battery
was tested. [All background results and figure](profile_transfer_20260912/analysis/REPORT.md)
are retained without selecting favourable backgrounds.

## Closure decision and operational handoff

The current implementation **does not pass the original validity gate**. Under
thesis section 8.2, proceeding with a revised architecture would require an explicit
revision and justified validation; local positive results do not automatically
constitute that pathway. No pass-with-revision, parameter descope, Appendix A MVT,
or new architecture is invoked here. Phase 2 remains blocked by encoding validity.

Collection and routine probing for this evaluated implementation stop here. The
prepared but unexecuted 900-call `original_confirmation_20260911` protocol remains
an historical proposal, not a queue. Earlier proposed studies in the archived
ledger are also not instructions to execute. Reopening experimental work requires
a new scoped decision; any theoretical departure still requires consultation.

All ten parameter definitions, Beta marginals, R, original prompts, Phase 0
provenance and recorded criteria remain unchanged. This closure neither merges
nor deletes earlier runs, and does not alter immutable raw records or runners.
The [previous operational ledger](../../docs/archive/NEXT_STEPS_before_closure_2026-09-12.md)
is preserved byte-for-byte; its original relative links use the repository root
as their base. Historical reports retain their as-of-date status.

No API calls or new charges were incurred for this closure. The last transfer run
cost an estimated $0.389088. The latest $9 allowance has a conservative tracked
remainder of **$3.35738625**, with zero pending requests; this is not a verified
provider balance or a lifetime project-spending total. See its
[budget ledger](profile_transfer_20260912/budget_ledger.json).

Raw archives remain on this computer with checksum inventories and previously
verified ZIPs. No off-device backup or remote push is claimed. The closure
[evidence manifest](closure_20260912/evidence_manifest.json) hashes the selected
reports and handoff documents; it is not a new verification of every raw response.

## Thesis-ready finding

Across the original encoding-validity battery and subsequent targeted diagnostics,
PARIA demonstrated partial behavioural parameterisation in the tested model, but
did not meet its prespecified validity gate. A final prospective profile-transfer
test found positive average endpoint effects for Mode of Response and Moral Scope
across 20 complete backgrounds, while Relational Embedding remained unresolved.
Moral Scope did not exhibit an ordered three-level response, and representation
dependence, paraphrase robustness and active-trait recoverability remained
unresolved or insufficient. These findings support a limited claim of numerical
influence under specified prompting conditions, rather than validated ethical
understanding or a broadly reliable ten-parameter encoding architecture. Main-study
simulation was therefore withheld, preserving the distinction between a promising
operational mechanism and its successful validation.
