# Original delivery: expanded selected-case replication

Frozen before collection on 2026-09-11. The researcher approved the proposed
640-call allocation with "go", then "continue" after the $4.50 cap was stated.
This follows the original implementation; the failed tool candidate is inactive.
No source prompt, approved meaning, response format or phase gate is revised.

## Allocation

| Case | Values | Wordings | Calls per condition | Total |
|---|---|---|---:|---:|
| MoR / S3 | .1, .5, .9 | Canonical and all three approved r5 paraphrases | 20 | 240 |
| MS / S2 | .1, .5, .9 | Same four | 20 | 240 |
| PD / S3 | .1, .9 | Same four | 20 | 160 |

Total **640 fresh calls, 32 conditions**, all ten parameters retained; the nine
non-swept parameters remain at their original means. MoR/S3 and MS/S2 were
selected because they previously responded; PD/S3 deliberately retains a
known wording-sensitive case. This is selected-case replication, not held-out
case selection or evidence that all ten axes work across all dilemmas.

Configuration neutral. Model `gpt-5.4-mini-2026-03-17`, temperature 1, maximum
600 tokens. Root seed **20260926**. Twenty shuffled complete blocks of 32,
concurrency 3, distinct requested seeds. No deterministic-output claim.
The original OpenAI SDK client sends the unchanged system/user message pair;
no tool call, bridge, added instruction, evidence overlay or rewritten dilemma.
Canonical messages match the original source manifest exactly; the approved
template loader checks review hashes for all three paraphrases. S2 and S3 retain
their own labels; the generic helper field `adopt` means first-option count and
is explicitly labelled FORMAL_REPORT for S2 in substantive output.

Exact messages are in [request_preview.json](request_preview.json). Frozen source
hashes, profiles, schedule and analysis commitments are in [manifest.json](manifest.json).
No old responses are pooled. The paused 900-call study is not resumed.

## Primary: eight directional endpoint comparisons

For MoR/S3 and MS/S2 under each of four wordings, estimate the high-minus-low
first-option probability difference. Positive directions are the existing
prespecified MoR/S3 ADOPT and MS/S2 FORMAL_REPORT hypotheses, not newly inferred
PD mappings. Test each with a one-sided Fisher exact test (high > low), then
**Holm-adjust all eight together**, alpha .05. Report every effect, raw and
adjusted p-value; no selection of the best wording or pair after collection.

Also report conservative exact nominal 95% effect intervals, constructed using
Bonferroni bounds on the two binomial cells within each contrast. These intervals
are **not adjusted across the eight comparisons**; Holm applies to the tests.
Missing/invalid outcomes receive an unknown-outcome envelope and invalidate the
study; primary p-values are withheld until the complete allocation is valid.

The number of significant directional effects is a result of this replication,
not a replacement pass count for the original Phase 1.5 battery. No new combined
"successful encoding" criterion is introduced.

## Secondary: wording stress and intermediate values

Construct 32 simultaneous exact binomial cell intervals with per-tail probability
.05/(2 x 32), yielding at least 95% joint coverage. Propagate these bounds into
all six pairwise wording differences at each of the eight fixed contexts:
**48 contrasts in total**. A propagated interval entirely outside [-.10, .10]
detects a gross local wording discrepancy. All other contrasts remain unresolved
for this screening purpose; absence of detection is not equivalence.

PD/S3 endpoint effects are reported as two-sided descriptive contrasts without
a new directional hypothesis. For MoR and MS, report all three observed rates
and whether they are nondecreasing, including ties. This is descriptive ordering;
three points do not establish the original five-point monotonicity criterion.
No retrospective midpoint hypothesis, model choice or sample extension.

## Budget, collection and provenance

Cap **$4.50**, full-dispatch reserve **$4.06452** using the existing conservative
UTF-8-byte plus framing bound and full token rates. Prior conservative charge
$4.31127825; cap plus that charge is below the latest $9 allowance. Provider
balance unverified. No cached-token discount assumed. Rates remain the recorded
September 11 $0.75/M input and $4.50/M output prices.

Reservations are written before each batch. Every provider call has one immutable
record with exact request messages, intended profile, seed, model, API ID,
timestamp, usage, raw provider payload, raw text and parsed output. Credentials
are not recorded. Unknown usage retains its reserved charge. API, model, usage,
reservation, request or parse failures stop after the current batch, are retained
in failure logs and invalidate the study. No failed slot is retried or replaced;
there is no automatic partial-run recovery or outcome-dependent extension.

The runner passed three tests before freezing, including all 640 mocked calls,
exact prompt/profile/label preservation, complete-block randomisation, distinct
seeds, known Holm/Fisher outcomes, gross wording contrasts, incomplete-sample
handling, budget blocking and terminal-failure preservation.

## Interpretation boundaries

More observations can clarify uncertain effects; they cannot repair a genuine
wording discrepancy. Positive endpoint effects establish directional behavioural
influence within these selected cases. They do not establish equivalence,
representation retention, active-trait recoverability or internal understanding.
Neither 50/50 nor 70/30 response balance is a pass requirement for parameterised
profiles. The original 24/30 equivalence gate and remaining battery are unchanged.
No automatic full sweep or Phase 2 launch follows completion. All outcomes,
including unsuccessful replications and the known stress case, will be reported.
