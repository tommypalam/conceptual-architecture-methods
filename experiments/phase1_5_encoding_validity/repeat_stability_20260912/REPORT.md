# Offline repeated-prompt stability audit

**53,782 valid records**, 18 source studies; **$0 new API spending**.
83 exact-prompt/settings groups recur with N>=20 in at least two runs.
**5/139 between-run comparisons** differ after Holm correction; **3/188 chronological-halves checks** differ in their separate Holm family.
These are exploratory diagnostics, not encoding-validity passes. Non-detection is not equivalence.

## Fixed reference prompts

Canonical MS/S2 and MoR/S3 endpoints selected in the protocol before this audit. Rates count FORMAL_REPORT for MS and ADOPT for MoR. All matching run summaries shown; seeds may differ.

| Parameter/value | Run | First-option count | Wilson 95% CI | Earliest UTC |
|---|---|---:|---|---|
| MoR 0.1 | option_c_20260909_restart | 5/50 | [0.043, 0.214] | 2026-09-09T11:49:40Z |
| MoR 0.1 | evidence_sensitivity_20260911 | 8/30 | [0.142, 0.444] | 2026-09-11T09:23:25Z |
| MoR 0.1 | repetition_factorial_20260911_continuation | 18/60 | [0.199, 0.425] | 2026-09-11T11:35:55Z |
| MoR 0.1 | profile_ablation_20260911 | 10/30 | [0.192, 0.512] | 2026-09-11T13:19:11Z |
| MoR 0.1 | tool_delivery_20260911 | 4/10 | [0.168, 0.687] | 2026-09-11T15:20:38Z |
| MoR 0.1 | original_expanded_20260911 | 5/20 | [0.112, 0.469] | 2026-09-11T18:54:50Z |
| MoR 0.9 | option_c_20260909_restart | 42/50 | [0.715, 0.917] | 2026-09-09T11:49:06Z |
| MoR 0.9 | evidence_sensitivity_20260911 | 26/30 | [0.703, 0.947] | 2026-09-11T09:23:34Z |
| MoR 0.9 | repetition_factorial_20260911_continuation | 52/60 | [0.758, 0.931] | 2026-09-11T11:35:49Z |
| MoR 0.9 | profile_ablation_20260911 | 23/30 | [0.591, 0.882] | 2026-09-11T13:19:08Z |
| MoR 0.9 | tool_delivery_20260911 | 9/10 | [0.596, 0.982] | 2026-09-11T15:20:27Z |
| MoR 0.9 | original_expanded_20260911 | 20/20 | [0.839, 1.000] | 2026-09-11T18:54:40Z |
| MS 0.1 | option_c_20260909_restart | 0/50 | [0.000, 0.071] | 2026-09-09T11:50:52Z |
| MS 0.1 | original_expanded_20260911 | 0/20 | [0.000, 0.161] | 2026-09-11T18:54:36Z |
| MS 0.1 | ms_stanza_crossover_20260912 | 0/20 | [0.000, 0.161] | 2026-09-12T00:16:59Z |
| MS 0.9 | option_c_20260909_restart | 30/50 | [0.462, 0.724] | 2026-09-09T11:49:05Z |
| MS 0.9 | original_expanded_20260911 | 14/20 | [0.481, 0.855] | 2026-09-11T18:54:48Z |
| MS 0.9 | ms_stanza_crossover_20260912 | 0/20 | [0.000, 0.161] | 2026-09-12T00:16:59Z |

## Largest observed shifts

The twelve largest absolute differences, selected descriptively after analysis. The JSON retains every comparison, including all non-detections. Later minus earlier; intervals are conservative nominal95, not family-adjusted.

| Problem / prompt hash prefix | Earlier run: count/N | Later run: count/N | Difference | Nominal conservative 95% CI | Holm p |
|---|---|---|---:|---|---:|
| S2 / 46db1ea6039a | original_expanded_20260911: 14/20 | ms_stanza_crossover_20260912: 0/20 | -0.700 | [-0.898, -0.230] | 0.00046097 |
| S2 / 46db1ea6039a | option_c_20260909_restart: 30/50 | ms_stanza_crossover_20260912: 0/20 | -0.600 | [-0.752, -0.235] | 0.00017819 |
| S3 / 7c4eeb3d70fa | pd_interaction_20260911: 23/30 | joint_wording_20260911: 8/30 | -0.500 | [-0.805, -0.066] | 0.031171 |
| S3 / fa0046507998 | evidence_sensitivity_20260911: 27/30 | original_expanded_20260911: 9/20 | -0.450 | [-0.777, +0.002] | 0.12544 |
| S3 / 4b65ad424628 | mor_curve_20260911: 12/30 | repetition_factorial_20260911_continuation: 5/60 | -0.317 | [-0.595, -0.008] | 0.13042 |
| S3 / 4b65ad424628 | evidence_sensitivity_20260911: 3/30 | mor_curve_20260911: 12/30 | +0.300 | [-0.083, +0.602] | 1 |
| S3 / bf802d83b27d | paraphrases_20260909_final: 32/50 | pd_endpoints_20260910: 266/300 | +0.247 | [+0.053, +0.452] | 0.005628 |
| S3 / 98674a462870 | mor_curve_20260911: 1/30 | repetition_retention_20260911: 8/30 | +0.233 | [-0.086, +0.484] | 1 |
| S3 / e581d599594b | option_c_20260909_restart: 5/50 | profile_ablation_20260911: 10/30 | +0.233 | [-0.080, +0.526] | 1 |
| S3 / a97afab35598 | profile_ablation_20260911: 23/30 | original_expanded_20260911: 20/20 | +0.233 | [-0.110, +0.449] | 1 |
| S3 / bf802d83b27d | paraphrases_20260909_final: 32/50 | wording_factorial_20260910: 255/300 | +0.210 | [+0.011, +0.421] | 0.13995 |
| S3 / 125c45253a62 | mor_curve_20260911: 5/30 | repetition_retention_20260911: 11/30 | +0.200 | [-0.192, +0.539] | 1 |

## Inventory and exclusions

| Source | Archived files | Valid retained | Invalid/failure | Different tool protocol | Successful multi-attempt records |
|---|---:|---:|---:|---:|---:|
| option_c_20260909_restart | 15000 | 15000 | 0 | 0 | 0 |
| rotations_20260909_restart | 4500 | 4498 | 2 | 0 | 0 |
| gradients_20260909_final | 15000 | 14998 | 2 | 0 | 1 |
| paraphrases_20260909_final | 4500 | 4497 | 3 | 0 | 0 |
| pd_endpoints_20260910 | 1200 | 1200 | 0 | 0 | 4 |
| wording_factorial_20260910 | 1200 | 1200 | 0 | 0 | 0 |
| axis_instruction_20260911_assembled | 7900 | 7890 | 10 | 0 | 12 |
| evidence_screen_20260911 | 450 | 450 | 0 | 0 | 0 |
| evidence_sensitivity_20260911 | 540 | 540 | 0 | 0 | 0 |
| repetition_factorial_20260911_continuation | 720 | 719 | 1 | 0 | 0 |
| repetition_retention_20260911 | 450 | 450 | 0 | 0 | 0 |
| mor_curve_20260911 | 300 | 300 | 0 | 0 | 0 |
| profile_ablation_20260911 | 300 | 300 | 0 | 0 | 0 |
| pd_interaction_20260911 | 300 | 300 | 0 | 0 | 0 |
| joint_wording_20260911 | 480 | 480 | 0 | 0 | 0 |
| tool_delivery_20260911 | 480 | 160 | 0 | 320 | 0 |
| original_expanded_20260911 | 640 | 640 | 0 | 0 | 0 |
| ms_stanza_crossover_20260912 | 160 | 160 | 0 | 0 | 0 |

Unique retained API IDs: 53,782. Same-prompt/same-seed repeated groups: 0. Backend fingerprint counts: {'None': 53782}.

## Interpretation boundaries

Post-result exploratory audit. Prompt key includes exact messages, pinned model, temperature, max completion tokens and labels; excludes seed. Same prompt is not same complete request. Run/time/seed/transport are confounded. Two-sided Fisher assumes independent exchangeable binomial responses; corrected discrepancies flag violations, not causes. No records pooled to meet a phase gate.
Full per-run summaries retain profile hashes, token/cache metadata, backend fingerprints, response-text uniqueness and chronological halves. Identical text is not proof of copied responses or dependent calls; these are indicators for further investigation.
Archived records were read from checksum-verified ZIPs. Current filename inventories and manifest bytes match archives; each archived record hash and each manifest design hash verified. This audit does not claim a fresh byte comparison against every current loose record. Payload text and recorded decisions reparse consistently under their original parser. Legacy bare-label responses retain their original scoring; API failures retain explicit exclusions.
Older successful multi-attempt records are counted, not silently removed. Assembled recovery allocations included once; prior copies and independent Claude studies excluded by declared scope. Historical September6 responses remain separate. No new retries, paid calls or raw-data edits.
All per-record checksums/normalized metadata are preserved locally in record_index.json and the audit ZIP. Original gate unchanged; Phase1.5 open, Phase2 held. Spending balance remains $3.79170675, provider balance unverified.

[Complete results](results.json) | [Protocol](PROTOCOL.md)
