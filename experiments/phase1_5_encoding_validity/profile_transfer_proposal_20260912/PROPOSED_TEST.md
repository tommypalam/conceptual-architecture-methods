# Proposed test: does MoR transfer to unfamiliar complete profiles?

Draft for discussion, 2026-09-12. No profiles sampled, prompts frozen, new code
implemented or API calls authorised/launched by this document.

## The question

Does changing Mode of Response produce the predicted average change in S3
choices when the other nine parameters vary across previously untested,
complete profiles? This moves beyond another repetition at the same mean-valued
background. It tests transfer of an already observed effect to new backgrounds.
The dilemma remains familiar and locked; this is not unseen-scenario validation.

Existing support: canonical MoR/S3 shows an original graded curve and the same
endpoint direction across six studies. Profile ablation and PD interaction
show that background matters, while repeat audits warn against using historical
controls. These motivate this test; they do not guarantee a favourable result.

## Small, concrete allocation

Use the existing Gaussian-copula/Beta sampler to draw20 background profiles,
with all existing calibration and R entries unchanged. Proposed draw seed20260929.
Keep every draw; no selecting profiles for expected effect or dropping saturated
ones. Hash-lock draws before API collection. These are diagnostic fixtures,
not the Phase2 paired-agent population.

For each draw, construct three counterfactual copies:

| Copy | MoR | Other nine values | Text and dilemma |
|---|---:|---|---|
| Low | .10 | Identical within this background | Exact canonical wording / locked S3 |
| Middle | .50 | Identical within this background | Exact canonical wording / locked S3 |
| High | .90 | Identical within this background | Exact canonical wording / locked S3 |

Run the complete60-condition panel twice: **120 calls**, two observations per
background/level. Randomize order within complete triplets and background order
within each full block; proposed schedule seed20260930. All controls collected
fresh in both blocks. New request seeds fixed before execution; no seed selected
from prior favourable outcomes. Record block/time and run to the fixed count,
without waiting for or extending toward a favourable result.

Pinned GPT-5.4-mini-2026-03-17, temperature1, max600, original neutral context.
All ten meanings, ordering, formatting, wrapper and user message remain intact.
Only numeric profile values vary. No action label is supplied as a target and
no tool or post-decision filter chooses or replaces an answer.

The copied MoR value is an intervention, not an unmodified copula draw.
Holding the other nine fixed deliberately breaks the natural MoR/background
association in the counterfactual copies. Do not report the resulting60 profiles
as samples from the original joint population or claim calibration changed.
This is a controlled sensitivity experiment over sampled backgrounds.

## Prediction and proposed analysis

The direction is inherited from thesis6.1.1: higher MoR predicts more ADOPT in
S3. No new directional PD, MS or interaction hypothesis is introduced.

Primary estimate: for each background, high-MoR ADOPT rate minus low-MoR ADOPT
rate, averaged equally across all20 backgrounds. Average within background
across the two blocks first. Report an approximate95% cluster-bootstrap interval,
resampling entire backgrounds with all their levels and repetitions together;
10,000 draws, proposed analysis seed20261001. Twenty backgrounds provide limited
precision; a pilot bootstrap interval is not an exact or universal guarantee.
Keep the20 background effects and both block-level effects visible.

Proposed development decision: evidence of transfer if the primary interval's
lower bound is above zero and the aggregate high-minus-low effect is positive
in both complete blocks. This is a new, disclosed local pilot criterion, not a
replacement for any original battery gate. Otherwise report inconclusive or
contradictory evidence, with its interval; do not reroll profiles or add calls.

Secondary: all three aggregate rates, intermediate placement of .50, and the
distribution of background-specific effects. Midpoint ordering is descriptive,
not a three-point substitute for the five-point monotonicity criterion. Two
observations per level cannot classify each background as a reliable pass/fail.
Background moderation and ceiling/floor effects should be shown, not filtered.

Preserve every response and every failure. A terminal API/parse/request/model
failure stops after its current dispatch batch and prevents a complete-study
claim. No retry in place or silent removal. Freeze the exact analysis, manifest,
source hashes, request preview and spending guard after the design is agreed.

## What a positive result would buy

A scoped claim: a prespecified parameter intervention changes choices in the
predicted direction on average across new complete profile backgrounds in this
dilemma, under fixed wording and model. It would make testing wider parameter
combinations more justified than optimising one handpicked cell.

It would not establish conscious ethical understanding, distinguish every
possible internal computation from instruction following, validate all ten
parameters, pass paraphrase/representation/recovery tests, recalibrate the Beta
marginals, or open Phase2. Those original requirements remain visible.

## Budget and status

Expected token cost is roughly$0.15 based on recent canonical runs, not a
provider quote or guaranteed charge. Propose a$1 maximum dispatch cap inside
remaining tracked$3.74647425, subject to exact request reservation checks.
No full sweep, profile draw, pending call or additional spending is created here.
This draft answers the researcher's request to think through a test; the earlier
request to pause automatic probing remains in force.
