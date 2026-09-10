# PD low/high endpoint attribution: completed

All **1,200 responses are valid**, 300 per condition, with no terminal API errors
or model mismatches. Both the low and high PD endpoint formulations produce
large behavioural differences. The interaction estimate is uncertain. The
result supports revising and testing the encoding of the complete endpoint pair;
it does not identify a single word to replace or establish a valid replacement.

## Fixed design and observations

Neutral full harness; one fixed PD=.8/S3 profile, other nine parameters at their
existing Beta means and other-nine descriptions fixed to P2. Model
`gpt-5.4-mini-2026-03-17`, temperature 1, cap 600 output tokens; collection seed
20260912. The seed is an identifier, not the collection date. All four conditions
received fresh data in 300 randomized four-request blocks. Responses were saved
September 10, 01:43:43-02:12:53 UTC; completion status was written at 02:13:13 UTC.

| Condition | Low endpoint | High endpoint | ADOPT / valid N | ADOPT rate | Simultaneous rate interval |
|---|---|---|---:|---:|---:|
| A | P2 | P2 | 266 / 300 | 88.7% | 83.3% to 92.8% |
| B | P3 | P2 | 151 / 300 | 50.3% | 43.0% to 57.7% |
| C | P2 | P3 | 119 / 300 | 39.7% | 32.6% to 47.0% |
| D | P3 | P3 | 15 / 300 | 5.0% | 2.4% to 9.0% |

The rate intervals are the four prespecified Bonferroni Clopper-Pearson bounds,
with at least 95% simultaneous coverage under the binomial assumptions. The
machine-readable cell summaries additionally retain ordinary Wilson intervals;
those pointwise intervals are not used for the contrasts below. Every condition
meets the 98% parse floor, with zero invalid or missing responses.

## Prespecified contrasts

Effects are percentage points, P2 minus P3. Weighted extrema of the four rate
intervals provide the simultaneous contrast bounds.

| Contrast | Estimate | Simultaneous 95% interval | Finding |
|---|---:|---:|---|
| Low endpoint, averaged across high-end versions | +36.5 | +24.6 to +47.2 | Large low-end wording effect |
| High endpoint, averaged across low-end versions | +47.2 | +35.1 to +57.7 | Large high-end wording effect |
| Low-by-high interaction | +3.7 | -18.9 to +26.2 | Inconclusive interaction; absence not established |

Both main-effect intervals exclude zero and exceed the 20-point planning target
throughout. The larger high-end point estimate does not establish that its effect
is statistically larger than the low-end effect; that comparison was not one of
the three prespecified tests. Likewise, an interaction interval spanning zero
does not establish additivity or equivalence. The design has weak power for the
smaller interaction scenarios documented in the preparation protocol.

For interpretation, changing only the low-end wording shifts ADOPT by 38.3
points when high=P2 (A minus B) and 34.7 points when high=P3 (C minus D).
Changing only the high-end wording shifts ADOPT by 49.0 points when low=P2
(A minus C) and 45.3 points when low=P3 (B minus D). These are descriptive
decompositions of the planned contrasts, not additional hypothesis tests.

## Semantic review and scientific scope

The researcher explicitly approved B/C with the exact review file open. The
assistant separately assessed both as consistent with the intended endpoint
meanings: low gives outcomes priority while retaining meaningful procedural
value; high assigns independent worth to fair procedure. These judgments made
the variants suitable for testing. They did not guarantee model invariance.

The low and high pairs are both implicated. This experiment cannot isolate
particular words, determine an internal reasoning mechanism, or show whether an
alternative prompt would preserve meaning more reliably. It concerns a selected
PD=.8/S3 profile with P2 background descriptions. No inference about all ten
parameters or general ethical competence follows from this single profile.

The fresh unchanged controls A/D were 88.7%/5.0%; their corresponding prior
factorial controls A/B were 85%/15%. Their ordering persists, but their rates
are not identical across collections. No historical observations are pooled and
no formal cross-session equivalence claim is made. The model snapshot matches;
independent, stable within-condition Bernoulli responses remain an assumption.
Randomized blocks distribute temporal changes without proving independence.

The theory, original validity criteria and later LPM/simple and Agents of
Chaos-style/complex plans remain unchanged. Phase 1.5 is still open and its
current gate unmet. The next research decision should specify a theory-faithful
operational encoding revision addressing both endpoints, with review and fresh
validation against the applicable battery. Choosing a formulation because it
produces a preferred ADOPT rate is not an encoding-validity repair. No revision
or further paid study has been launched from these results.

## Integrity and budget

Exact frozen messages/profiles, model identity, seeds, unique record/API IDs,
record hashes, checksum inventory and analysis counts were verified for all
1,200 observations. The ZIP passes its integrity test and all 1,200 raw JSON
payloads are byte-identical to the local records. Four requests used two attempts
(1,204 recorded attempts total); every request ultimately succeeded. The local
same-computer ZIP is not an off-device backup.

Usage: 1,086,600 input tokens, 110,977 output tokens, zero cached tokens.
Estimated token cost **$1.3143465** from the official rates checked September 10:
$0.75/million input and $4.50/million output
([OpenAI model pricing](https://developers.openai.com/api/docs/models/gpt-5.4-mini)).
This is an estimate from returned usage, before taxes or any unreported retry
charges. Estimated remainder of the newly authorised $50: **$48.6856535**.
The earlier experiments predate this additional budget; the $5 preparation
reservation is released in favour of the recorded cost estimate.

Evidence: [numerical analysis](endpoints_b2ad447503a870bd.json),
[completion verification](../completion_verification.json),
[record inventory](../record_checksums.json), [backup metadata](../local_backup.json),
[usage](../token_usage.json), [approval](../review_approved.json), and the
[frozen protocol](../PROTOCOL.md). Preparation files retain their historical
pending status; the separate approval artifact records the subsequent approval.
