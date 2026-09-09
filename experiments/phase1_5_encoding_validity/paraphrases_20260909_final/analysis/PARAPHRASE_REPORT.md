# Approved paraphrase experiment — completed 2026-09-09

**The prespecified equivalence criterion is not met: 8/30 parameter/problem
cells establish all-pair equivalence, against a requirement of at least 24/30.**
This completes the planned empirical battery. It does not pass the Phase 1.5 gate.

Neutral configuration; root seed 20260604; exact `gpt-5.4-mini-2026-03-17`;
temperature 1; cap 600; concurrency five. Ten parameter rotations at .8,
other parameters fixed at their means, three problems, three approved templates,
N=50 per cell: 4,500 new calls. The canonical arm reuses exactly 1,500 valid
hybrid responses from `rotations_20260909_restart`. Total compared observations:
6,000 recorded, 5,997 valid; the canonical baseline is not newly recollected.

Tommy approved all three exact templates before dispatch. The
[approval bundle](../../claude_paraphrases_20260909_theory_r5/paraphrases_approved.json)
records the statement, reviewer identity basis and template hashes. Templates
were not edited after approval. Generation was refined using semantic feedback,
with all drafts preserved and no behavioural results supplied to the generator.

## Completeness and cost

All 4,500 expected record keys are present and unique. There are 4,497 valid
parses, three preserved parsing failures, zero API failures and no returned-model
mismatches. No failed response was replaced. MoR/S2/paraphrase_3 has 48/50 valid
responses (96%), below the 98% floor; its six equivalence comparisons are not
assessed. PD/S2/paraphrase_1 has 49/50 valid (98%) and remains eligible.
The other 88 new cells have 50/50 valid responses.

Recorded tokens: 4,299,000 input, 406,843 output, zero cached input. At the
previously verified $0.75/M input and $4.50/M output rates, estimated token cost
is **$5.06**, before taxes or other charges. The preceding four Claude preparation
calls cost approximately $0.065 separately.

The record inventory, token usage and local backup metadata are in the run root.
ZIP integrity and its recorded SHA256 were verified. This is a same-computer
backup under `output/validity_backups`, not an off-device copy.

## Existing all-pair criterion

Each of 30 parameter/problem cells compares all six pairs among canonical and
three paraphrases. The unchanged test is constrained-binomial score TOST with
Miettinen–Nurminen correction, absolute rate-difference margin .10, alpha .05.
All six pairs must establish equivalence. Complete collection and at least 98%
valid responses per formulation are required. Thus 29 cells have six pair tests;
one is disqualified by parse validity. The gate requires at least 24 equivalent
cells and the stated data-quality conditions.

| Parameter | S1 | S2 | S3 |
|---|---|---|---|
| LL | Equivalent | Not established | Not established |
| CS | Equivalent | Not established | Not established |
| RT | Equivalent | Not established | Not established |
| MoR | Not established | Parse floor not met | Not established |
| RE | Equivalent | Equivalent | Not established |
| PD | Equivalent | Not established | Not established |
| TfA | Not established | Not established | Not established |
| ID | Equivalent | Not established | Not established |
| MS | Not established | Not established | Not established |
| AW | Equivalent | Not established | Not established |

The full [frozen report](cells_621833995ad959cd.json) includes individual rates,
Wilson 95% intervals, pair differences and TOST p-values. All eight successful
cells occur in highly concentrated response distributions. Equivalence at a
ceiling/floor does not by itself establish meaningful parameter encoding.

## Descriptive behaviour across formulations

Pooled first-option rates below summarize ten equally sampled parameter
rotations. They are descriptive, not substitutes for the prespecified cell tests
or new independent hypothesis tests. Valid denominators retain parse failures.

| Problem | Canonical | Paraphrase 1 | Paraphrase 2 | Paraphrase 3 |
|---|---|---|---|---|
| S1 | 498/500 (99.6%) | 498/500 (99.6%) | 497/500 (99.4%) | 495/500 (99.0%) |
| S2 | 86/500 (17.2%) | 92/499 (18.4%) | 61/500 (12.2%) | 174/498 (34.9%) |
| S3 | 254/500 (50.8%) | 360/500 (72.0%) | 389/500 (77.8%) | 275/500 (55.0%) |

For one concrete fixed profile, PD=.8 on S3, the first-option rates are 14%
canonical (95% CI 7.0–26.2%), 22% paraphrase 1 (12.8–35.2%), 64% paraphrase 2
(50.1–75.9%), and 4% paraphrase 3 (1.1–13.5%). The observed range is 60 percentage
points. This is a profile-level illustration; because all endpoint descriptions
change together, it cannot identify PD wording alone as the cause.

Failure to establish equivalence is not automatically evidence of a meaningful
difference: N=50 is too imprecise for a .10 equivalence margin near a 50/50 rate,
even when observed rates match. The large observed shifts on several S2/S3
profiles are a separate descriptive concern. Neither that limitation nor the
three parsing failures justifies changing thresholds or adding outcome-selected
calls after seeing results. Even if the one parse-disqualified cell passed,
the count would remain far below 24.

The human and assistant reviews judged the meanings acceptably consistent for
testing; the model nevertheless did not demonstrate the required behavioural
invariance. Semantic acceptability and empirical invariance are distinct.
No post-result template revision, new model, architecture change or Phase 2
launch is authorised by this report. See the
[full battery assessment](../../phase_review_20260909/BATTERY_ASSESSMENT.md).
