# crossmodel_pilot_asch_r1: Asch cost cell

**Outcome: 4/4 probes succeeded, $0.021203875.** 15 September 2026. Exploratory,
uncoded, no recognition claim. Companion to
[crossmodel_pilot_r1](../crossmodel_pilot_r1/ASSESSMENT.md), which measured the
four text-only families.

| Form | Model | Input tokens | Output | $/probe |
|---|---|---:|---:|---:|
| canonical | haiku-4.5 | 7,251 | 100 | 0.008526 |
| alternative | haiku-4.5 | 7,289 | 83 | 0.008474 |
| canonical | gpt-5.4-mini | 2,309 | 34 | 0.002073 |
| alternative | gpt-5.4-mini | 2,360 | 37 | 0.002130 |

**Mean $0.00530 per probe, about 2.5x the text-only families.** Affordable.

The 81,266-token Asch probe in the failed `crossmodel_recognition_r1` attempt
was an artefact of JSON-dumping the content blocks into a single string, not a
property of the stimulus. Passed as content blocks, Asch costs about four cents
for eight probes across both models.

## A confound that must be fixed, not disclosed

The OpenAI request path in this pilot flattens content to text, which **drops
Asch's 18 image blocks**. That is why gpt-5.4-mini sees 2,309 input tokens where
haiku-4.5 sees 7,251: the two models are not receiving the same stimulus.

Any cross-model comparison on Asch is confounded until the OpenAI path carries
the images. This is a repair required before a study, not a limitation to be
noted in a results section.

Descriptively, all four answers named Asch or conformity, including both
alternatives. That is 1 probe per cell with a keyword match and supports nothing.
