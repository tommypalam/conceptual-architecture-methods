# From behavioural influence to transferable normative dispositions

Prepared 13 September 2026 on `research-transfer-design-20260913`.
Status: research strategy and candidate design, not a frozen protocol or paid release.

Researcher clarification incorporated: the thesis is exploratory and its central
culminating experiment investigates good/bad decisions and consequences. Read
[implementation v0.2](../../../Theory/implementation_specification_v0_2.md) and the
[moral capstone brief](../../phase4_coding/CAPSTONE_DESIGN_DRAFT_20260913.md). Transfer
and prediction support that contribution; they do not replace it. Directional
expectations below are candidate deductions for future studies, not hypotheses
that the researcher is claimed to have held before the thesis began.

## Research objective

The researcher wants a distinctive, strong paper rather than incremental increases
in response counts. The proposed central question is:

> Can an explicit normative representation predict and control an agent's trade-offs
> across unfamiliar situations, including cases where the same disposition calls
> for opposite overt actions?

Success would support transferable functional normative representation under the
tested intervention. It would not establish weight-level encoding, intrinsic
ethical understanding, persistent internalization, human equivalence or moral
superiority. The profile remains a generation-time prompt intervention.

The paper's potential contribution is a validated connection between a specified
disposition, its selective response to circumstances and its usefulness for
predicting behaviour. Numerical notation need not outperform equivalent prose.
Publication strength and novelty are not guaranteed by completing this design.

## Why this direction

The existing studies already establish replicated whole-profile effects, a narrower
Procedural Dependence (PD) effect, and limits to wording and benchmark validation.
They provide development evidence, not the confirmation data for this study.

A preliminary literature scan shows substantial neighbouring work. This is a
scoping comparison based on accessible abstracts, not a systematic novelty review:

| Primary source | Existing contribution | Implication for PARIA |
|---|---|---|
| [Castricato et al., PERSONA, COLING 2025](https://aclanthology.org/2025.coling-main.752/) | A reproducible pluralistic-alignment testbed with synthetic personas and human evaluation | Persona diversity and a simulator alone are insufficient novelty claims. |
| [Moore et al., Findings of EMNLP 2024](https://aclanthology.org/2024.findings-emnlp.891/) | Value consistency across paraphrases, topics, answer formats and languages | Consistency alone is already studied; test selective, theory-derived changes as well as invariance. |
| [Wu et al., NAACL 2024](https://arxiv.org/abs/2307.02477) | Counterfactual task variants reveal limits to transfer beyond familiar task assumptions | Adapt the diagnostic principle to normative decisions; these authors did not validate PARIA or moral understanding. |
| [Tan et al., ACL 2026](https://aclanthology.org/2026.acl-long.1127/) | Subgroup value emulation, structured-preference fine-tuning and transfer evaluation | Structured numerical preferences and value transfer are not themselves new; their training intervention differs from our prompt intervention. |

Read the full methods and closest additional papers before finalizing novelty,
baselines or a target venue. Do not claim that no existing study tests this question.

The local theoretical anchor is thesis v0.6 section 2.2 and Appendix A, PD row:
process-dominant agents give greater weight to how an outcome is produced, including
acceptance of unfavourable outcomes from fair procedures. The distinction between
procedural and distributive justice is grounded in the organizational-justice
literature, including [Colquitt (2001)](https://pubmed.ncbi.nlm.nih.gov/11419799/).
Human construct validation does not validate our numerical axis or predict an
effect size in an LLM. The operational contrasts below are proposed deductions
from the thesis, not claims that these sources establish a particular AI response.

## The decisive first study

Begin with PD because it has the strongest existing evidence. This is an explicit
post-results choice of research focus. All ten coordinates remain in the framework,
and earlier contrary findings remain reported. This study does not validate them all.

Use newly authored administrative/resource-allocation settings outside the six
locked dilemmas. Cross procedure quality and outcome desirability independently:

| Proposed decision | Outcome more desirable | Outcome less desirable |
|---|---|---|
| Procedure meets stated impartiality criteria | Aligned positive case | Process/outcome conflict |
| Procedure violates those criteria | Process/outcome conflict | Aligned negative case |

Candidate factual procedure features are consistent eligibility, an opportunity
to correct factual errors and the absence of preferential overrides. The final
design must distinguish these features from mere official endorsement. Outcome
desirability must have an explicit, independently reviewed meaning: who benefits,
what is lost and what remains constant. Private advantage, distributive equality
and aggregate welfare are not interchangeable manipulations. No moral-quality
scores follow from these stimulus labels.

Keep available actions, stakes, evidence completeness, timing and action costs
matched. Describe concrete facts without calling the procedure "fair" or telling
the participant which action follows from its profile. Avoid reproducing PD's
definition verbatim in the task. Randomize option order and response labels, and
balance whether accepting or challenging requires action. Include paraphrases and
cases where all relevant information is already available: waiting cannot explain
every process-sensitive response. A later authority-endorsement manipulation is
needed to discriminate deference fully; it is not identified by this 2x2 alone.

### Candidate primary estimand

For each arm, compare acceptance of the process-positive/outcome-negative proposal
with acceptance of the process-negative/outcome-positive proposal. Then compare
that trade-off between PD=0.9 and PD=0.1:

`T = [Pr(accept | high PD, P+ O-) - Pr(accept | high PD, P- O+)]`
`  - [Pr(accept | low PD,  P+ O-) - Pr(accept | low PD,  P- O+)]`.

The theory-derived candidate prediction is `T > 0`. This is a difference in
trade-offs, not a requirement that all high-PD agents always choose one action,
nor a guarantee that each individual contrast reverses sign. Report the component
contrasts and aligned cases, so a favourable aggregate cannot conceal a different
response pattern. A strong reversal claim requires evidence for both relevant
directions, not just a positive aggregate interaction.

### Simultaneous controls

| Arm | Content | Identified comparison |
|---|---|---|
| E | Full numerical LPM profile | Proposed implementation |
| V | All the same profile information in prose, preserving values and endpoints | Representation package: layout, wording and numerical framing |
| S | A concise PD-only disposition description, with the same PD level information and no task-specific action instruction | Whether the rest of the full profile is needed for this effect |
| U | Identical task/context without a disposition profile | Model/harness baseline |

S is deliberately simpler and removes other information; E-S is not a pure
formatting contrast. S at a given PD level and U do not vary with the other nine
coordinates. Their repetitions are sampling blocks, not different simulated
personalities. Equal E and S performance would support a simpler implementation
for this task, not automatically validate the full architecture. A wide interval
would establish neither equivalence nor superiority.

Draw fresh ten-coordinate backgrounds from the existing Beta marginals and copula.
Save the original draws unchanged, then create linked PD endpoint interventions
holding the other nine values fixed. The intervened profiles are experimental
counterfactuals and are not unmodified draws from the original joint distribution.
Do not change the marginals or R to make them appear naturally sampled.

## Transfer, specificity and practical contribution

Separate pilot settings from confirmation settings by domain and substantive
decision structure, not just names. Candidate domains include access to shared
facilities, grants, public-service scheduling and organizational appeals. Two
pilot domains and at least six fresh confirmation settings are a planning target,
not a sufficient basis for claiming all-domain generalization. Freeze all held-out
texts and analysis choices before obtaining any confirmation-model decisions.
No domain may be silently discarded because its outcomes are inconvenient.

The intended paper builds four connected layers of evidence:

1. **Selective control:** PD changes sensitivity to procedure/outcome conflicts,
   survives label/order changes and is not explained solely by inaction or
   official endorsement. Unrelated-detail invariance needs an equivalence margin
   and adequate precision; a nonsignificant difference is not evidence of invariance.
2. **Prediction:** predeclare effect directions on untouched tasks. If numerical
   probability forecasts are reported, fit on development data only and compare
   held-out calibration/Brier scores against prespecified simple predictors
   (including task-feature and task-feature-plus-PD models). Do not retrofit a
   regression after seeing the held-out decisions and call it prediction.
3. **Use in groups:** after individual validation, test whether measured dispositions
   help predict a predeclared group outcome beyond independent votes or majority
   aggregation. Add a matched no-discussion comparison if claiming an interaction
   mechanism. The existing Phase 2 data motivates this; it is not a fresh group
   transfer test. The replay viewer can make this result inspectable.
4. **Moral decisions and consequences:** a central fresh experiment tests helpful
   and harmful actions, their costs and simulated outcomes under the existing dual
   moral standard. Prepare measurement in parallel with transfer; retain human
   validation and examine active good as well as avoidance of violations.

A second theoretically distinct coordinate and joint interventions would strengthen
an architectural claim. Select it prospectively using theory and the complete
existing evidence, including failures. Do not pick the winner of an undisclosed
multi-coordinate pilot. No new coordinate-to-action mapping is frozen here.

Cross-model replication is a separate stage. Use a fresh second-provider sample
with comparable tasks/settings, report model-specific estimates and do not infer
cross-model equivalence from two nonsignificant differences. Provider selection
requires a current quote and feasible bounds, not an assumption of spare credit.

## Human resemblance and moral consequences

The original five benchmark families and failed recognition controls remain in
scope and explicitly unresolved. This document proposes a supplement; it does not
amend their thresholds or declare formal Phase 3 closed. Any eventual replacement
of the formal validation route requires a separately documented scope decision.

Newly authored stimuli reduce direct reuse of exact experimental items but do not
prove absence from training data or absence of learned conceptual templates.
Record recognition as an ancillary diagnostic, not as proof of memorization.

For human resemblance, obtain comparable human responses under a separate protocol
or justify a precise match to existing human conditions. AI reviewers can flag
task ambiguity; they cannot establish human construct validity. Recruitment,
appropriate institutional review and participant compensation need a separate
plan. A small convenience sample would be exploratory, not human validation of
the entire architecture. No participants are contacted by this proposal.

For the central good/bad experiment, retain the Phase 4 human-reviewed coding requirement.
Neither procedural fidelity nor profile fidelity is automatically morally good.
If later simulations have explicit state transitions and payoffs, report the
defined outcomes directly and distinguish them from morally weighted judgments.

## Expedited execution and spending discipline

No paid API calls were made for this strategy. The current cumulative Phase 3
ledger estimates Claude $6.029498200 / $15 and OpenAI $0.828888225 / $30;
Phase 2+3 accounting is $29.764459450 / $100. These are conservative records,
not checked provider wallet balances or a new allocation to exhaust.

| Stage | Concrete deliverable | Proposed additional API ceiling |
|---|---|---:|
| Offline design | Source-to-prediction table, stimuli, task-validity rubric, baseline templates and competing predictions | $0 |
| Small pilot | Two new settings; 12 fresh background/sampling blocks; full 2x2 conditions and E/V/S/U | $2 total, including review |
| Fresh confirmation | Held-out settings and fresh blocks; sample chosen by prospective precision/power simulation | Up to $8, only if a defensible design fits |
| Moral capstone preparation | Manual, human validation plan and matched consequential scenarios, developed alongside transfer | Protect $4 Claude/$10 OpenAI within existing allowances; exact costs unresolved |
| Additional validation | Targeted second-model, specificity or group test chosen by the remaining claim gap | Separate proposal that preserves the moral-study reserve |

Pilot arithmetic: `12 blocks x 2 settings x 4 P/O cells x (2 E + 2 V + 2 S + 1 U)
= 672 participant calls`, excluding separately capped reviewer calls. This is a
design size, not a power calculation or cost quote. A 48-block, six-setting
confirmation with the same cells would require 8,064 calls; it is only a sizing
example, not the selected N. Additional label/authority/invariance variants must
be explicitly counted and cannot be added silently under these numbers.

Check exact token bounds, current provider rates, failure reservations and both
provider caps before release. If the proposed size cannot fit the ceiling, revise
the design prospectively or keep its conclusion exploratory; do not shrink N
after inspecting results or label an underpowered run conclusive. No budget
increase is requested here, and no collector or model request manifest is queued.

The pilot assesses comprehension, feasible intervention strength, floor/ceiling
patterns and whether task facts actually separate the proposed explanations.
Report all pilot cells. Do not keep generating candidates until one is significant.
Specify any bounded revision allowance before the pilot; every revision gets a
new designation. A null pilot with wide intervals is uncertainty, not equivalence.

Before confirmation, freeze a smallest practically informative effect, the
primary contrast family, multiplicity treatment, missing-data policy, domain and
profile dependence handling, sample size and stopping rules. Simulate precision
under plausible null and alternative effects rather than powering from the largest
observed pilot effect. Repeated responses do not create new independent domains.
Preserve all failures and unknown charges using the existing write-once workflow.

## Five-perspective design review

Decision evaluated: prioritize a theory-derived PD trade-off/transfer supplement
with simpler controls before further familiar-benchmark scaling. These are
synthetic review perspectives, not external expert approval.

- **Linden (philosophy):** The trade-off follows the thesis's process/outcome
  distinction, but outcome desirability requires an explicit normative referent.
  No behavioural pattern warrants an intrinsic-understanding claim.
- **Osei (psychology):** Manipulate procedure separately from outcome and official
  endorsement; hold comprehension and action cost constant. Human resemblance
  needs comparable human evidence, and six settings do not represent all domains.
- **Tanaka (statistics):** Treat PD edits as interventions, preserve paired blocks,
  and avoid treating repeated U/S prompts as distinct profiles. Freeze a primary
  estimand and dependence-aware power/precision plan before confirmation.
- **Renna (AI/cognitive science):** The novelty candidate is selective transfer and
  prediction under controlled intervention. Compare with both exact-information
  prose and a useful simpler baseline; numeric superiority is optional.
- **Okafor (simulation):** Start with a bounded individual study using existing
  transport safeguards. Add group interaction only when it tests a specific
  prediction beyond independent votes, not merely to create a larger simulation.

Principal disagreement: a fuller factorial with authority, action-cost and a
second coordinate would be more discriminating but would inflate the pilot.
Resolution: the first 2x2 pilot measures the process/outcome trade-off only;
deference, generality and architectural composition are not declared resolved.
Record and cost the necessary additional controls before a confirmatory claim.

## Completion boundary for this draft

This draft establishes a research direction, candidate estimand, control logic,
scoped literature comparison, stage budgets and explicit inference limits.
It does not freeze task text, a moral rubric, a new benchmark or a paid study.
Next deliverable is the exact pilot packet with independently reviewed task facts,
alternative-explanation predictions, exact quote and offline verification. Prepare
the moral measurement and capstone packet in parallel. The overall thesis remains
exploratory; a fresh confirmation stage is required only for claims presented as
confirmed, not as a prerequisite to asking every new research question.

Initial draft verification: 42 local links across this strategy, current status
and the Phase 3 index resolve; companion constitutions match except for their
filename headings; pilot/confirmation example arithmetic gives 672/8,064 calls;
`git diff --check` passes. No experiment code or frozen records were changed.
