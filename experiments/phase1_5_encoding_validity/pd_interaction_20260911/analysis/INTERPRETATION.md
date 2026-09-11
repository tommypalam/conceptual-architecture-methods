# Background values matter under fixed descriptions

**300/300 valid responses; no API, model or usage failures.** The approved
fixed allocation completed without retries. Estimated cost$0.313056.
All ten profile entries and descriptions remained present in both arms.
At matched MoR, only the PD number differed; message byte lengths were equal.

| MoR | ADOPT /30 at PD=.1 | ADOPT /30 at PD=.9 |
|---|---|---|
| .1 | 25 | 3 |
| .3 | 25 | 1 |
| .5 | 27 | 2 |
| .7 | 27 | 4 |
| .9 | 30 | 23 |

The prespecified primary fitted MoR slope difference, high-PD minus low-PD,
is **+3.491**, Wald95% interval **[+.479,+6.503]**, two-sided **p=.0231**.
The slopes are2.255 and5.746 respectively. This is a local exploratory result,
selected from previous development evidence and analysed using the frozen
linear-logit model. It supports background-value dependence of the fitted
response under the tested descriptions. It is not a new whole-phase pass.

## The shape matters as much as the fitted contrast

At low PD, adoption is already83% at low MoR and reaches100%; little upward
range remains. At high PD, adoption stays between3% and13% through MoR=.7,
then reaches77% at.9. Much of that arm's response is an extreme-end jump,
not demonstrated gradual responsiveness throughout the intermediate values.

High-PD counts also dip from3 to1 between the first two points. Its legacy
directional criterion is not met; low-PD meets the descriptive legacy rule.
Monotonicity was explicitly secondary for this interaction test and remains
required where specified by the original phase gate. We neither waive the dip
nor infer that the underlying response must be nonmonotone from N30 samples.

The primary Wald inference assumes a suitable linear-logit model. A clearly
labelled post-score descriptive check illustrates the approximation: at high
PD, the fitted ADOPT rates at MoR=.7/.9 are31.7%/59.5%, compared with observed
13.3%/76.7%. This is not a formal lack-of-fit test or a replacement primary;
it is a reason to avoid presenting a smooth fitted slope as a complete account
of the response. See [all observed/fitted rates](descriptive_fit_check.json).

The prespecified secondary difference in endpoint probability changes is+.500,
with conservative95% interval[-.183,+1.027]. It includes zero, so this less
model-dependent contrast does not independently resolve an endpoint interaction.
The wide bound is retained as computed; this contrast can range from-2 to+2.
See [full numerical report](INTERACTION_REPORT.md) and
[observed-rate figure](fig_01_pd_interaction.png).

## What the result narrows down

Prompt length does not differ between these two arms. Their different response
patterns therefore cannot be attributed to a difference in total byte length
between these arms. The content of the injected numerical profile matters;
the nine background values cannot simply be treated as absent or neutral.

This strengthens the case for studying conditional parameter behaviour, while
keeping explanations open. Numeric cueing, inferred task priorities and intended
trait interaction are not distinguished here. Nor does this test establish how
much of the earlier deletion effect comes from PD, or rule out presentation
effects in that earlier experiment. A smaller fitted MoR slope in a joint
profile is not inherently a defect: other dispositions may legitimately
change decisions or leave less probability range available.

The theory motivated selecting PD but did not predict this interaction's sign.
The observed ADOPT/WAIT patterns must not be backfilled into a supposedly
pre-existing theoretical rule. Neither label is being scored as morally better.

## Decision

Bank this scoped fixed-text result alongside the deletion diagnostic, including
their limitations. Do not treat steeper slopes as an automatic repair target.
The outstanding questions are whether the observed joint dependence has the
intended meaning and whether it is sufficiently graded, interpretable and
robust. These require distinct evidence; another slope test alone would not
close them. The original8/30 paraphrase-equivalence outcome, audit interpretation
and Phase2 hold remain unchanged. All five concepts and ten parameters remain.

No new experiment is automatically queued. The900-call representation
confirmation remains stopped. Any subsequent graded-response or wording check
must be frozen prospectively, with its actual scope and limits made explicit.

Cumulative known usage$3.378930; conservative charge including the earlier
unknown timeout reservation$3.38389725, leaving$5.61610275 from the latest$9
allowance. No pending calls; provider balance unverified. Raw records are
write-once and backed up locally with checksums; same-computer ZIP verification
does not establish an off-device backup.
