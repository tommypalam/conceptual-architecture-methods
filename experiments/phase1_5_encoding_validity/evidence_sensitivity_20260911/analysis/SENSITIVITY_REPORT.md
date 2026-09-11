# S3 endpoint sensitivity result

Status: **POSITIVE_RESPONSE_DETECTED_NOT_VALIDATED**.

Collected 540/540; valid 540; terminal failures 0.
Recorded full-rate token estimate **$0.650970**; cumulative new-budget estimate **$1.153193**.
Estimated allowance remaining **$7.846807** of $9; not a checked account balance.
Cached-input discounts are not subtracted. Screen cap $4; no automatic expansion.

| Arm | Parameter | Wording | Value | ADOPT / valid | Rate | Wilson 95% CI |
|---|---|---|---:|---:|---:|---|
| original | PD | paraphrase_2 | 0.1 | 23/30 | 76.7% | [59.1%, 88.2%] |
| original | PD | paraphrase_2 | 0.9 | 27/30 | 90.0% | [74.4%, 96.5%] |
| original | PD | paraphrase_3 | 0.1 | 29/30 | 96.7% | [83.3%, 99.4%] |
| original | PD | paraphrase_3 | 0.9 | 6/30 | 20.0% | [9.5%, 37.3%] |
| original | MoR | canonical | 0.1 | 8/30 | 26.7% | [14.2%, 44.4%] |
| original | MoR | canonical | 0.9 | 26/30 | 86.7% | [70.3%, 94.7%] |
| repetition | PD | paraphrase_2 | 0.1 | 4/30 | 13.3% | [5.3%, 29.7%] |
| repetition | PD | paraphrase_2 | 0.9 | 7/30 | 23.3% | [11.8%, 40.9%] |
| repetition | PD | paraphrase_3 | 0.1 | 7/30 | 23.3% | [11.8%, 40.9%] |
| repetition | PD | paraphrase_3 | 0.9 | 1/30 | 3.3% | [0.6%, 16.7%] |
| repetition | MoR | canonical | 0.1 | 1/30 | 3.3% | [0.6%, 16.7%] |
| repetition | MoR | canonical | 0.9 | 3/30 | 10.0% | [3.5%, 25.6%] |
| grounding | PD | paraphrase_2 | 0.1 | 27/30 | 90.0% | [74.4%, 96.5%] |
| grounding | PD | paraphrase_2 | 0.9 | 7/30 | 23.3% | [11.8%, 40.9%] |
| grounding | PD | paraphrase_3 | 0.1 | 14/30 | 46.7% | [30.2%, 63.9%] |
| grounding | PD | paraphrase_3 | 0.9 | 9/30 | 30.0% | [16.7%, 47.9%] |
| grounding | MoR | canonical | 0.1 | 3/30 | 10.0% | [3.5%, 25.6%] |
| grounding | MoR | canonical | 0.9 | 23/30 | 76.7% | [59.1%, 88.2%] |

## Endpoint response

All differences are .9 minus .1. Only grounding/MoR/canonical is primary.

| Arm / parameter / wording | Difference | Conservative >=95% interval |
|---|---:|---|
| original/MoR/canonical | +0.600 | [+0.183, +0.861] |
| original/PD/paraphrase_2 | +0.133 | [-0.203, +0.433] |
| original/PD/paraphrase_3 | -0.767 | [-0.933, -0.394] |
| repetition/MoR/canonical | +0.067 | [-0.178, +0.290] |
| repetition/PD/paraphrase_2 | +0.100 | [-0.246, +0.418] |
| repetition/PD/paraphrase_3 | -0.200 | [-0.448, +0.108] |
| grounding/MoR/canonical | +0.667 | [+0.261, +0.897] |
| grounding/PD/paraphrase_2 | -0.667 | [-0.897, -0.261] |
| grounding/PD/paraphrase_3 | -0.167 | [-0.548, +0.258] |

## Descriptive PD wording gaps

| Arm / PD value | P2 minus P3 | Conservative >=95% interval |
|---|---:|---|
| original/PD/0.1 | -0.200 | [-0.448, +0.108] |
| original/PD/0.9 | +0.700 | [+0.298, +0.918] |
| repetition/PD/0.1 | -0.100 | [-0.418, +0.246] |
| repetition/PD/0.9 | +0.200 | [-0.108, +0.448] |
| grounding/PD/0.1 | +0.433 | [+0.030, +0.722] |
| grounding/PD/0.9 | -0.067 | [-0.433, +0.317] |

Secondary intervals are not adjusted across the family. Significance in one arm and its absence
in another is not evidence that the arms differ. PD/S3 has no prespecified direction.
Two endpoints do not establish monotonic gradients, slope retention, equivalence or joint encoding.
Known S3 was selected during development; these are not holdout results. No new null data were collected.

## Integrity

All frozen sources, full messages/profiles, seeds, approval, single-attempt identities,
current/cumulative reservations and all raw ZIP payload bytes verified. Same-computer backup only.
Model `gpt-5.4-mini-2026-03-17`, neutral context, temperature 1, output cap 600, root seed 20260916.
Original prompts and meanings are intact; tool delivery is inactive and Phase 1.5 remains open.
