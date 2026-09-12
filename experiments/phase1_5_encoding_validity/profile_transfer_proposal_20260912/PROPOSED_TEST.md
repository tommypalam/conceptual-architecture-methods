# Proposed test: three parameter effects across unfamiliar complete profiles

Draft revised for discussion, 2026-09-12, following the researcher's request to
include at least two more parameters. No profiles sampled, prompts frozen,
runner implemented or new API calls authorised/launched by this document.

## The three predictions

Use three existing directional hypotheses from thesis6.1.1:

| Parameter | Locked dilemma | Predicted effect of increasing the parameter | Reason for inclusion |
|---|---|---|---|
| MoR ? Mode of Response | S3, department reorganisation | More ADOPT | Strongest recurring directional effect; positive reference |
| MS ? Moral Scope | S2, quiet error | More FORMAL_REPORT | Positive original evidence followed by instability and partial replay recovery |
| RE ? Relational Embedding | S3, department reorganisation | More WAIT | Opposite prediction to MoR in the same dilemma; challenges trait-specific influence |

RE is a deliberately demanding inclusion: its original S3 rates were
ADOPT74/48/30/68/28% at .1/.3/.5/.7/.9 and it did not meet the original full
sweep criterion. It is not already validated. New backgrounds may clarify how
widely the directional effect holds, but do not guarantee a better result.
Opposite MoR/RE effects would be more informative than a generic tendency to
choose ADOPT whenever a displayed number rises. They would not alone prove
semantic understanding or exclude every competing explanation.

PD remains relevant. Its theory-prespecified S1 comparison has a near-ceiling
original curve (94/98/100/100/100% A), while its informative S3 effects are
exploratory under the existing directional list. RE offers an already specified
opposite-sign S3 comparison. This is a reason for choosing RE in this bounded
three-parameter draft, not a rejection of later PD testing.

## Question and scope

Do these directional parameter effects transfer to previously untested complete
profile backgrounds? Most recent replications used a fixed background or a
narrow PD contrast. Use new backgrounds to test the breadth of parameter
influence while retaining canonical wording and the familiar locked dilemmas.
This is not unseen-scenario generalisation or a test of a new encoding interface.

## Exact proposed allocation

Draw20 backgrounds using the existing Gaussian-copula/Beta sampler, unchanged
marginals and R. Proposed draw seed20260929. Keep every draw, including ones
that might produce floor/ceiling responses. Hash-lock the full draws and rendered
values before calls. These are diagnostic fixtures, not the Phase2 population.

For each of the SAME20 background draws, construct three separate triplets:

- MoR=.10/.50/.90, other nine values fixed, use S3.
- MS=.10/.50/.90, other nine values fixed, use S2.
- RE=.10/.50/.90, other nine values fixed, use S3.

Each triplet changes only its named parameter. In particular, the RE value in
the MoR triplet remains the original sampled RE value, and vice versa. This is
not a joint3x3x3 factorial or an estimate of all interactions. Sharing the
background draws supports comparison without inventing new behavioural rules.

**20 backgrounds x3 parameters x3 levels x2 complete blocks =360 calls.**
There are180 conditions per complete block and two observations per condition.
Randomize background/parameter triplet order and level order within each
triplet; proposed schedule seed20260930. Complete both blocks with fresh
concurrent controls and fixed requested seeds before interpreting results.
No outcome-dependent stopping, rerolled backgrounds or extra calls to rescue a
comparison. Report block timestamps; two blocks are not long-term stability.

Pinned GPT-5.4-mini-2026-03-17, temperature1, max600, original neutral context.
Keep all ten definitions, order, formatting, wrapper and exact S2/S3 user text.
Only numeric profile values vary. No target answer, action-scoring tool or
post-decision replacement is introduced.

Setting one value is a controlled intervention. The counterfactual copies are
not untouched samples from the original joint population: the intervention
breaks that parameter's natural association with its background. Neither the
population calibration nor R is changed by this diagnostic design.

## Primary analysis and multiplicity

There are THREE primary effects, all oriented in the predicted direction:
MoR high-minus-low ADOPT; MS high-minus-low FORMAL_REPORT; RE high-minus-low WAIT.

For each parameter, first calculate the high-minus-low rate within each
background, averaging across the two complete blocks. Then average equally
across all20 backgrounds. Retain the20 background effects and both aggregate
block effects. The same backgrounds are the unit of uncertainty across all
three comparisons; do not treat360 calls as360 independent sampled profiles.

Propose50,000 cluster-bootstrap resamples, analysis seed20261001. Resample whole
backgrounds, retaining all their parameters/levels/repetitions; use the same
resample indices for all three effects. Report ordinary nominal95% intervals
for estimation plus **98.333...% individual intervals** (Bonferroni over three)
for the proposed family-level decision. These bootstrap intervals are approximate,
particularly with20 backgrounds, not exact family-coverage guarantees.

Proposed local decision for each parameter: adjusted interval lower bound>0 and
positive aggregate effect in both blocks. Report all three decisions, including
inconclusive or contrary results. Do not declare a new overall architecture pass
from a favourable subset. This local exploratory screen does not replace any
original battery criterion. The multiplicity adjustment is introduced BEFORE
collection, rather than applying the previous single-comparison rule three times.

Secondary: all low/middle/high aggregate rates and background-specific effects.
Midpoint ordering is descriptive, not the original five-level monotonicity test.
Two observations per level cannot reliably classify each background as passed
or failed. Do not filter saturated or contrary backgrounds. Cross-parameter
interactions and faithful psychological mechanisms are not identified here.

Preserve all outcomes and failures. Terminal API/parse/request/model failure
stops after its current batch and prevents a complete-study claim; no retries
in place or silent exclusions. After design agreement, freeze the exact manifest,
profiles, messages, source hashes, analysis and verified budget guard before any
request is sent. No new rater coding manual is introduced.

## What a positive result supports

A scoped conclusion about each supported contrast: changing that parameter
has the predicted average behavioural effect across these new complete
background profiles under this fixed wording/model/dilemma. Opposing MoR and
RE effects in S3 would additionally support differential responsiveness to the
two parameter interventions, subject to uncertainty and background moderation.

This does not establish conscious ethical understanding, every internal
mechanism, validity of all ten parameters, paraphrase/representation/recovery
passes, a new population calibration or permission to start Phase2. The
original Phase1.5 requirements remain unchanged, including the unmet gate.

## Budget and status

Expected token cost approximately$0.40-$0.50 based on recent canonical runs;
this is an estimate, not a quote. Propose a **$2.50 maximum dispatch cap** inside
remaining tracked$3.74647425, subject to exact request reservation checks.
The cap is not the expected charge. No call allocation is active yet.

This is the expanded draft requested by the researcher. Prior proposals for
120 calls/$1 are superseded in this document; neither allocation was launched.
The requested pause on automatic probing remains in force while design is
settled. No profiles drawn, prompt edits, API calls or additional spending.
