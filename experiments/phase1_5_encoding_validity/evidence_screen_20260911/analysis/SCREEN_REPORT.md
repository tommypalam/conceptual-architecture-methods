# S3 evidence screen result

Status: **NO_GROSS_FAILURE_DETECTED_NOT_VALIDATED**.

Collected 450/450, valid 450; terminal failures 0.
Recorded full-rate token estimate: **$0.502223**; screen cap $3, total new allowance $9.
Cached-input discounts are not subtracted. This is a token estimate, not a checked account balance.

| Arm | Profile wording | ADOPT / valid | Rate | Wilson 95% CI |
|---|---|---:|---:|---|
| original | canonical | 2/30 | 6.7% | [1.8%, 21.3%] |
| original | paraphrase_1 | 9/30 | 30.0% | [16.7%, 47.9%] |
| original | paraphrase_2 | 25/30 | 83.3% | [66.4%, 92.7%] |
| original | paraphrase_3 | 6/30 | 20.0% | [9.5%, 37.3%] |
| original | no_profile | 4/30 | 13.3% | [5.3%, 29.7%] |
| repetition | canonical | 0/30 | 0.0% | [0.0%, 11.4%] |
| repetition | paraphrase_1 | 9/30 | 30.0% | [16.7%, 47.9%] |
| repetition | paraphrase_2 | 0/30 | 0.0% | [0.0%, 11.4%] |
| repetition | paraphrase_3 | 1/30 | 3.3% | [0.6%, 16.7%] |
| repetition | no_profile | 9/30 | 30.0% | [16.7%, 47.9%] |
| grounding | canonical | 0/30 | 0.0% | [0.0%, 11.4%] |
| grounding | paraphrase_1 | 5/30 | 16.7% | [7.3%, 33.6%] |
| grounding | paraphrase_2 | 3/30 | 10.0% | [3.5%, 25.6%] |
| grounding | paraphrase_3 | 3/30 | 10.0% | [3.5%, 25.6%] |
| grounding | no_profile | 1/30 | 3.3% | [0.6%, 16.7%] |

## Primary remaining-wording-gap screen

- original: P2 minus P3 = +0.633; conservative >=95% interval [+0.215, +0.887].
- repetition: P2 minus P3 = -0.033; conservative >=95% interval [-0.195, +0.135].
- grounding: P2 minus P3 = +0.000; conservative >=95% interval [-0.274, +0.274].

Only the grounding gap is primary. An interval wholly outside +/-0.10 detects a gross remaining failure.
Failure to detect such a gap does not establish equivalence, improvement, or a phase pass.

## Exploratory contrasts

| Contrast | Difference | Conservative nominal >=95% CI |
|---|---:|---|
| grounding_minus_original_no_profile | -0.100 | [-0.332, +0.164] |
| grounding_minus_original_wording_gap | -0.633 | [-1.204, +0.133] |
| grounding_minus_repetition_no_profile | -0.267 | [-0.519, +0.063] |
| grounding_minus_repetition_wording_gap | +0.033 | [-0.456, +0.517] |
| repetition_minus_original_no_profile | +0.167 | [-0.201, +0.489] |
| repetition_minus_original_wording_gap | -0.667 | [-1.119, -0.012] |

Secondary intervals are not adjusted across contrasts. Null comparisons test added context under the shared
user schema, not equivalence to the naked Phase 0c baseline or a pure profile effect.
Known S3 was selected during development; these are not holdout results. No PD/S3 direction was invented.
The fixed profile cannot establish parameter responsiveness or replace the PD/S1 gradient.

## Integrity

All frozen sources, complete requests, profiles, seeds, approval, single-attempt identities,
dispatch reservations and all raw ZIP payload bytes verified. Same-computer backup only.
Model `gpt-5.4-mini-2026-03-17`, temperature 1, output cap 600, root seed 20260915.
Original prompts and theory are unchanged. Tool delivery remains inactive; Phase 1.5 remains open.
