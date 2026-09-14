# crossmodel_probe_images_r1: provider image asymmetry repaired

**Outcome: 2/2 probes succeeded, $0.014012075.** 15 September 2026. Exploratory
verification of a defect repair, not a study. No recognition claim.

## The defect

[crossmodel_pilot_asch_r1](../crossmodel_pilot_asch_r1/ASSESSMENT.md) recorded
that the OpenAI request path flattened content to text and therefore **dropped
Asch's 18 image blocks**, so the two providers were not receiving the same
stimulus. Any cross-model comparison on that family would have been confounded.

## The repair, verified

`code/phase3_crossmodel_probe.py` translates Anthropic base64 image blocks into
OpenAI `image_url` parts. Both providers now receive 21 text blocks and 18
images.

| Model | Input tokens before | After |
|---|---:|---:|
| `claude-haiku-4-5-20251001` | 7,289 | 7,289 |
| `gpt-5.4-mini-2026-03-17` | 2,360 | **6,501** |

**Provider token ratio 0.89, previously 0.32.** The residual gap is tokeniser
and image-encoding difference between providers, not dropped content.

Cost with images carried: $0.005527 per OpenAI Asch probe, against $0.002130
when images were being discarded. Asch remains affordable.

Both answers named Asch. That is one probe per model with no coding and supports
nothing beyond the repair working.

## Provenance

`code/phase3_crossmodel_pilot.py` is **byte-unchanged**. It is frozen by the
releases of the two completed pilots, and its source hash is verified at every
dispatch; the repair was therefore made in a new module rather than by editing
frozen source. An attempt to edit it in place was correctly refused by the
source-hash guard with "Frozen continuation source changed", and the file was
restored from HEAD before proceeding.

The inherited `crossmodel_recognition_r1` failed slot is carried forward
untouched at full reservation.
