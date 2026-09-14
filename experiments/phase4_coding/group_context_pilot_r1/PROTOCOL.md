# Context and collective moral decisions: exploratory pilot r1

14 September 2026. Prospective implementation under the researcher's instruction
to continue the broad thesis within existing budgets. This new designation follows
the saturated finite individual pilot. Earlier participant records and failed
AI-rating screens remain unchanged; no positive effect is required for completion.

## Design and scope

Draw nine fresh profiles from the original ten-dimensional copula/Beta population,
seed 2026091400. Shuffle IDs with seed 2026091401 into three fixed groups of three.
Reuse those groups across all conditions. Study four partial configurations:
A0J0, A0J1, A1J0, A1J1. A is the original Authority axis and J the original Justice
axis, with the canonical LOW/HIGH meanings. Freedom, Care and Loyalty are NEUTRAL.
No societal-axis definition, parameter, marginal or correlation changes. This is
a prospective four-condition subset, not completion of all 32 configurations.

Two finite tasks: public versus protected truthful reporting, and equal receipts
versus increased production plus panel rewards. Full task facts and transitions
are in code/phase4_group_tasks.py. These introduce a real conflict between costs,
benefits and principles; changing the scenario from the saturated predecessor is
explicit exploratory development, not a held-out generalization claim.

Four arms: E numeric full profile; V exactly information-matched written percentages;
U identical harness without a profile; G U plus the previous concise ethical guidance.
All retain the same context and facts. U/G repeated groups have no supplied
personalities. Reinject the complete assigned system prompt every call. Agents
do not see other profiles or arm names, and have no memory across task/condition cells.

There are 3 groups x 4 contexts x 2 tasks x 4 arms = 96 group episodes.
In each, all three agents first recommend an action privately and give a brief
public reason. Only after all initial recommendations are saved does each receive
the same simultaneous board of that group's initial recommendations and reasons,
including its own, and independently cast one final vote with a reason. No final
vote can influence another final vote. Total: 288 initial + 288 final = 576 calls,
plus one Claude design/rule review. This is one bounded round of peer review,
not a multi-round open-ended society or a completed Agents-of-Chaos implementation.

The primary behavioral comparison is between randomized/matched representation
and context conditions. Initial-vote aggregate versus final aggregate is a
descriptive change after repetition plus peer information. There is no private
retest control, so do not claim a causal effect of deliberation alone, emergence,
or better decisions than independent aggregation in general.

Each majority requires at least two votes. Three different valid votes implement
hold, a pre-disclosed procedural fallback with real listed costs. Any invalid vote
makes the corresponding collective outcome missing and unexecuted, never hold by
imputation. Initial aggregates are counterfactual decisions without peer review;
only final aggregates execute state changes in their separate simulated episodes.
Individual recommendations are not separately executed or treated as moral actions.

## Moral measurement amendment

The [rule map](RULES.md) extends deterministic primary measurement specifically to
these six collective action outcomes. Group moral labels describe the jointly
implemented action, not the language, private intentions or character of members.
Recommendations receive only conditional action-outcome descriptions. The whole
panel is the acting unit. Its three members have explicitly consented in advance
to the voting rule and possible fees/rewards. Panel deltas are always reported;
the fixed harm indicator covers external recipients, consistent with the earlier
actor-cost/third-party distinction. This boundary is a disclosed normative
assumption, not evidence that groups may ignore harms to their members generally.

The director's recommendation does not change the recorded legal mandate.
The scenario facts constrain its scope; the contextual labels do not invent new
laws, payoffs, privacy prohibitions or waivers of equal claims. Fixed standards and
task rules stay identical across all four contexts and all representation arms.
Any relative/fixed divergence is interpreted under these stipulated rules only.

Peer reasons are untrusted simulated speech, shown verbatim with provenance and
bounded size. They may contain factual mistakes or persuasive claims. The scorer
does not infer honesty/deception of dialogue from action choice, and does not claim
that the group's communications were ethically validated. No message rewrites,
scoring feedback, action substitution or post-generation filter occurs.

One independent Claude review must accept the protocol, exact task/rule source,
six outcome vectors, prompt variants and group mechanism with zero blockers before
participant collection. Malformed/revise/reject stops the designation without an
automatic retry. Prior judge failures are separate preserved measurement evidence.
No human raters are required. AI approval and exhaustive tests do not establish
universal moral truth, human resemblance or intrinsic ethical understanding.

## Ordering, extraction and missingness

Cell ordering is shuffled with seed 2026091402. Member request order is permuted
per cell; the initial board is sorted by local member ID. A/B/C labels rotate by
group and task, exactly once per semantic action/letter over the three groups,
and are matched across arms and contexts. The population grouping is immutable.
All initial calls precede all final calls. Every slot and dynamic-request template
is frozen before dispatch; final requests are reconstructed from retained initial
records and capped by a conservative byte bound, not invented during collection.

Require JSON with exactly choice (A/B/C) and reason (nonempty string, at most
240 UTF-8 bytes, no control characters). Prompt requests at most 120 ASCII
characters for the reason; no trimming or fixing invalid responses. Invalid
records remain missing and receive an explicit unavailable entry on the board.
Transport/model/usage/finish errors stop at the failed record under existing
no-retry rules. Content errors are retained while the fixed remaining batch runs.
Never drop a group because of its choices, agreement, missingness or effect sign.

## Prospective analysis

Unit for uncertainty is the matched group, not the 576 API responses. There are
only three independent profile groups; this is a small development pilot with
severe uncertainty. Context/task/arm repetitions are dependent within a group.
No power, significance, equivalence or confirmation claim is made.

For each of 32 task/context/arm cells report assigned/valid group counts,
initial/final action counts and transitions, ties and missingness, all three panel
deltas and each external recipient's delta, total credits, completion, all twelve
category rates and relative/fixed/net/weighted headline rates. Report individual
recommendation counts and changes descriptively, without treating them as extra
independent group observations or inventing individual executed moral outcomes.

Primary estimands: per task/context, final group recipient-total mean difference
and final fixed-good rate difference for E-U, V-U, G-U and E-V. Also report within
each task/arm the Authority difference at each Justice value and Justice difference
at each Authority value. These context comparisons retain the same scenario facts
and scoring rules. They test partial context prompts, not all institutional effects.

Secondary descriptive estimands: corresponding final-minus-initial aggregate
changes per task/context/arm for recipient total and fixed-good indicator. These
bundle repetition and peer exposure. No outcome pooling across task families is
primary. No data-dependent parameter regression or profile selection is planned.

Use 9,999 whole-group bootstrap resamples, seed 2026091403, and the existing
Hoeffding bounds for complete paired metrics. With only three groups intervals
will be coarse; a degenerate bootstrap is not certainty. Missing choices use the
full enumerated action bounds with assigned-group denominators; missing contrasts
have identification bounds and no imputed primary estimate. Report all specified
comparisons and no significance-based selection. Freeze a fresh follow-up before
any later confirmation; do not keep extending this sample until an effect appears.

## Budget, provenance and stopping

Models remain GPT-5.4-mini-2026-03-17 for participants (temperature 1, reasoning
none, JSON mode, 160 output tokens) and Claude Sonnet 4.6 for one review (temperature
0, thinking disabled, 2048 output tokens). Existing official prices and 10% margin
remain those documented on 14 September in the preceding pilot. The exact release
reserves every input/output including maximal group-board size before collection.

All $1.329527925 previous moral-development charges carry forward under the same
$4 ceiling. Reject preparation if the full new reservation would exceed the
remaining $2.670472075, the cumulative Claude $15/OpenAI $30/package $100 limits,
or protected later-study cap room of $4 Claude/$10 OpenAI. No budget/date reset.
These are accounting caps and usage estimates, not verified wallet balances.

Preserve all 2,435 existing paid records, archives and frozen sources. Commit
protocol, rule source, population, grouping, schedule and release before dispatch.
Offline tests must cover all outcomes, simultaneous boards, missing/duplicate
guards, majority ties, matched controls, full mocked run, zero-call replay and
historical preservation. Verify final analysis, integer costs and full archive
without any extra paid calls. Ignored raw data remains local; off-device backup
must not be claimed verified. Completing this pilot does not close the whole thesis.

## Five synthetic perspectives

- Linden: Keep the joint-actor boundary and equal-claim convention explicit;
  consent to a voting rule is not universal permission to discount member welfare.
- Osei: Stated fees and directives increase scenario trade-offs but cannot prove
  that simulated incentives equal human motivation. Only three groups limits scope.
- Tanaka: Preserve group dependence and all missing cells. Initial/final changes
  lack a retest control and cannot identify the effect of discussion alone.
- Renna: The old null and failed-rater results remain. Judge the batch by completion
  and interpretability, never by an encoding win or a desired amount of wrongdoing.
- Okafor: Bound and reconstruct every peer board; reinject profiles each round;
  retain raw speech but score only finite actions and their actual transitions.

Resolution: a four-context, two-task exploratory group pilot is the next scoped
implementation step. These are internal synthetic review roles, not human experts
or independent external validation. The listed limitations remain in final reporting.
