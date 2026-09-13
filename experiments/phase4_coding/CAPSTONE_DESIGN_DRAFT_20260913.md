# Moral decisions and consequences: central experiment

13 September 2026 · Design brief, not a frozen paid protocol

Current amendment: human raters are deferred at the researcher's explicit request.
This brief now describes AI-assisted moral evaluation. See the
[scope record](AI_ONLY_SCOPE_20260913.md) and [draft manual](manual_r1/MANUAL_DRAFT.md).

14 September measurement amendment: the finite individual pilot now uses
deterministic rule-derived primary classifications after independent AI review.
See [the scoped change](DETERMINISTIC_SCOPE_20260914.md). The earlier generative
rating screens remain failed reliability audits. This route is limited to fully
specified task/action pairs; it does not authorize applying the finite scorer
to arbitrary group dialogue or silently substituting rules for general coding.
Any group extension needs its own state transitions, rule map and prospective review.

## Purpose

The thesis culminates in investigating whether different normative representations
produce good or bad individual and collective decisions, under explicit standards,
when principles conflict with incentives, authority or group pressure. The desired
result is an informative map of benefits, harms and trade-offs; encoded agents are
not presumed to improve moral outcomes.

This is central under [implementation v0.2](../../Theory/implementation_specification_v0_2.md).
The transfer study supplies evidence about what the profiles control. Its success
does not replace this experiment, and its failure would inform a narrower capstone
interpretation rather than remove moral evaluation from the research question.

## Candidate experimental structure

Use matched initial situations, available actions, evidence, incentives and
exogenous randomness across conditions. Keep the original profile/context
definitions unless a separately justified change is documented. Choose a feasible
context subset prospectively, recording precisely which contrasts it identifies;
two bundled contexts cannot identify five separate societal-axis effects.

Candidate families are honest disclosure versus concealment under personal cost;
legitimate versus harmful directives; and group resource decisions with visible
effects on differently situated recipients. These are design domains, not fixed
action-to-moral-label mappings. Include easy aligned cases, genuine trade-offs and
cases where principled dissent prevents harm. Do not construct only situations in
which the supposedly ethical option is also the easiest or most rewarded.

Each scenario should support an explicit transition table or state model specifying
what each permitted action changes. Hold opportunity to help/harm constant across
conditions. Track personal payoff, third-party effects, task completion and costs
separately. Include the consequences of inaction; a policy that avoids every task
must not appear successful solely because it avoids direct harmful acts.

For uncertainty, distinguish expected consequences given the agent's available
information from realised simulated outcomes. An unlucky outcome does not by
itself show that the original decision was unreasonable. For deception, distinguish
what the agent knew from what was true; explanations alone cannot establish intent.

## Candidate comparison arms

| Arm | Main question |
|---|---|
| Full LPM encoding | What moral choices and consequences result from specified dispositions? |
| Information-matched prose | Do these outcomes depend on the representation format? |
| Context-only baseline | What changes relative to the same model/harness without the profile? |
| Concise ethical instruction baseline | What does the architecture add beyond an ordinary instruction to act ethically? |

The last baseline must be useful and neutrally designed; it cannot be deliberately
vague or weak to make PARIA win. Freeze its normative information and acknowledge
information differences. A task-specific answer instruction is not an appropriate
baseline for a transferable disposition claim.

A post-generation filter/comparator is a valuable optional extension for the
researcher's encoding-versus-filter question. Its access to information, handling
of blocked actions, opportunity to revise and total model-call budget must be
specified and matched fairly. Without that comparison, report generation-time
intervention placement but make no claim of outperforming filtering. Final arms,
sample sizes and resources depend on the exact quote and AI measurement scope.

Include matched individual and group conditions where feasible. Independent votes
versus deliberation can test whether discussion changes harmful or helpful
outcomes; calling a group effect "emergent" requires specifying what simpler
aggregation predicts and comparing against it. Use cluster-aware inference and
do not count all rounds of one group as independent groups.

## What good/bad means here

Retain thesis v0.6 Chapter 7's eight-category configuration-relative vector:
power-seeking, deception, disutility, ethical violations, appropriate authority use,
honest disclosure, welfare promotion and principled compliance under cost. Also
retain the four fixed-standard categories: harm, deception, coercion and unfairness
avoidance. Full definitions, evidence rules and edge cases belong in the future
versioned coding manual, not in this design brief.

Report both vectors and their original headline aggregations separately. The
fixed-standard all-four-upheld headline measures avoiding specified violations;
it is not the same as demonstrating active virtue. Preserve positive actions,
negative actions, mixed cases and uncertainty in the detailed record. The
configuration-relative good/not-good/neutral classification must not be collapsed
into a claim that every non-good or unscorable action is bad.

Especially informative is divergence: a society may produce agents that behave
coherently by its own norms yet harm outsiders under the fixed standard. Conversely,
dissent may improve consequences. These are possible discoveries, not assumptions
used to set scoring rules or select favourable cases.

The original MACHIAVELLI work investigates reward/ethical-behaviour trade-offs;
that motivates assessing task achievement alongside ethical costs. PARIA's positive
extensions and dual scoring are its own proposed measurement construction and
remain to be validated. [Pan et al., 2023](https://arxiv.org/abs/2304.03279)

## Independent measurement

Draft, independently AI-review and freeze the manual before the new capstone responses are collected.
Use authored or explicitly designated development examples for rubric calibration.
If older Phase 2 responses are used, record that exposure and exclude those items
from any claimed held-out validation of the developed rubric.

Blind raters to arm, profile values, model identity and expected results. Supply
the relevant task facts, action, known information and consequences. Relative
scoring requires the applicable institutional facts even when the configuration
ID is hidden; fixed-standard raters must use the same standards across conditions.
Do not remove factual context so aggressively that the action becomes unjudgeable.

Use two independently prompted provider judges; human validation is deferred.
Report category prevalence, agreement and uncertainty, positive and negative
agreement where useful, and each judge's disagreements with recorded facts. Freeze the reliability
criterion and escalation rules before validation; do not lower them after failure.
Do not repeatedly revise the manual on the held-out items and call the same items
an untouched gold set. Disagreement and unscorable outcomes remain visible.

Human raters evaluating agent decisions do not establish that humans would make
the same decisions. A human behavioural comparison remains a separate protocol.
No moral labels, weights or approved manual are created by this draft.

## Analysis and stopping

The overall study is exploratory. Report the complete prespecified comparison
grid, rates of positive action and violations, task achievement, third-party effects,
and distributional differences. Inspect relationships with profiles, context and
group interaction, while disclosing exploratory selection and multiplicity.
Freeze measurement and batch stopping before responses, even when no direction is
predicted. Any subsequently selected central effect gets fresh confirmation if
presented as confirmed. Stronger moral outcomes are not a required result for an
informative thesis; clear evidence of harm or a competence/morality trade-off matters.

The amended capstone is complete only when the scoped collection, AI measurement checks,
all-results report, uncertainty analysis and reproducible archive are complete.
Report it as an exploratory AI-assisted moral study with no human validation.
Completing this amended scope does not establish human moral consensus or validate
the taxonomy merely through AI agreement. Do not reopen the deferred human gate.

## Next deliverables

1. Trace the proposed categories to the actual source instruments and distinguish
   their validated constructs from our new action-coding uses.
2. Prepare the versioned manual, calibration/held-out check split and independent
   AI coding plan with exact costs and factual consistency checks.
3. Build fresh task states, candidate actions, transition rules and matched arms.
4. Freeze a small pilot with exact API costs, preserving the capstone
   reserve specified in implementation v0.2. No current paid release exists.

The synthetic five-perspective reviews in implementation v0.2 and the scope record
cover this design brief. Neither constitutes external expert or human validation.
