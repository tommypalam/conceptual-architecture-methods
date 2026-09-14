# crossmodel_pilot_r1: exploratory cost and feasibility probe

**Outcome: 32/32 probes succeeded, $0.067523500.** 15 September 2026.
Exploratory batch under a $1 ceiling, not a study. **No recognition claim is
made**: answers were saved and deliberately left uncoded, because the two-rater
coding step belongs to a properly designated study.

## Purpose

Two questions had to be answered by measurement before a real cross-model
recognition study could be sized:

1. What does a cross-model recognition probe actually cost?
2. Do the frozen `recognition_r1` stimuli work unchanged on models other than
   the single model that screen probed?

## What it cost, measured

Four text-only families, both forms, two models, two probes per cell.

| Family | Model | Input tokens | Output | $/probe |
|---|---|---:|---:|---:|
| `ultimatum` | haiku-4.5 | 1,010 | 101 | 0.001671 |
| `ultimatum` | gpt-5.4-mini | 902 | 40 | 0.000942 |
| `bystander` | haiku-4.5 | 1,291 | 106 | 0.002006 |
| `bystander` | gpt-5.4-mini | 1,194 | 46 | 0.001215 |
| `reactance` | haiku-4.5 | 2,416 | 121 | 0.003326 |
| `reactance` | gpt-5.4-mini | 2,091 | 41 | 0.001932 |
| `milgram` | haiku-4.5 | 2,676 | 124 | 0.003626 |
| `milgram` | gpt-5.4-mini | 2,404 | 36 | 0.002163 |

**Mean: $0.00266 per probe on haiku-4.5, $0.00156 on gpt-5.4-mini.** Every probe
terminated cleanly (16 `end_turn`, 16 `stop`); none hit the output limit.

This is roughly **five times cheaper than the estimate** used when the full
design was first attempted, because that attempt mis-sized the request rather
than because the models are cheap. Two corrections were needed:

- **Stimuli must be passed as content blocks**, as the frozen `probe_request`
  does, not JSON-dumped into a single string.
- **`max_tokens: 128` truncates these answers.** The frozen screen's 35-word
  answers fit; these models write longer. 256 is sufficient here.

`asch` was excluded from this batch and measured separately in
[crossmodel_pilot_asch_r1](../crossmodel_pilot_asch_r1/) after the same fix.

## Asch, measured separately

| Form | Model | Input tokens | $/probe | Named its family |
|---|---|---:|---:|---|
| canonical | haiku-4.5 | 7,251 | 0.008526 | yes |
| alternative | haiku-4.5 | 7,289 | 0.008474 | yes |
| canonical | gpt-5.4-mini | 2,309 | 0.002073 | yes |
| alternative | gpt-5.4-mini | 2,360 | 0.002130 | yes |

**$0.00530 per probe, about 2.5x the text-only families** - affordable, not
prohibitive. The 81,266-token figure from the failed attempt was entirely an
artefact of JSON-dumping the content blocks, not an inherent property of Asch.

**A real asymmetry to fix before any study.** The OpenAI request path in this
pilot flattens content to text and therefore **drops the 18 images**, which is
why gpt-5.4-mini sees 2,309 tokens where haiku sees 7,251. The two models are
not receiving the same stimulus for Asch. A cross-model comparison on this family
would be confounded until the OpenAI path carries the images, and that must be
fixed rather than disclosed.

## Descriptive observation, explicitly not a result

Whether each answer names its own family, by simple keyword match. **This is not
the frozen recognition rule**, which requires two independent raters to name the
family with neither flagging ambiguity or refusal. It is a sanity check on
whether the stimuli behave, nothing more.

| Form | haiku-4.5 | gpt-5.4-mini |
|---|---|---|
| canonical | 8/8 | 7/8 |
| alternative | 6/8 | 6/8 |

`milgram`, `ultimatum` and `bystander` alternatives were named by both models in
every probe. `reactance` alternatives were named by neither, and the misses are
near-misses rather than blanks: haiku called it "the Decoy Effect (or Attraction
Effect)"; gpt-5.4-mini called it "the framing/choice-reversal paradigm". Both
identified the option-restriction structure and attached a different label.

This is 2 probes per cell with an unvalidated keyword match. It cannot support
any rate, comparison or claim, and the reactance pattern in particular could be
a labelling artefact of the keyword list rather than a recognition failure.

## What it enables

A real cross-model study is now sizable from evidence rather than guesswork.
Measured per-probe costs give, for four text-only families across two models at
n per cell:

| n per cell | Probes | Estimated probe cost |
|---:|---:|---:|
| 10 | 160 | ~$0.34 |
| 25 | 400 | ~$0.84 |
| 50 | 800 | ~$1.69 |

Including `asch` adds roughly $0.0053 per probe per model.

Coding adds roughly two rater calls per ten probes. Adding `asch` or a third
model requires measuring those cells first.

## Limits

- **Exploratory, uncoded, 2 probes per cell.** No recognition rate is estimated
  and no model is compared to another.
- **Asch is not comparable across providers yet.** The OpenAI path drops its
  images, so the two models received different stimuli for that family.
- **Two models.** The original screen's probe target is not re-probed here.
- Costs are usage estimates from this harness at this moment, not quotes.
- Recognition, if later measured, still would not identify memorisation as
  against inference over shared structure, and would not establish behavioural
  imitation.

## Provenance

All 32 records written once and preserved. The stopped
`crossmodel_recognition_r1` attempt is the ledger parent; its failed Asch slot
is inherited by explicit name and carried forward untouched at full reservation
under the no-retry rule. Stimuli, system prompt and question are the frozen
`recognition_r1` text, reused unchanged.
