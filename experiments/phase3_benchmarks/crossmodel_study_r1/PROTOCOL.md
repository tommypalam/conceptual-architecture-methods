# Cross-model recognition study: protocol r1

15 September 2026. Prospective. Extends the completed
[recognition screen](../recognition_r1/execution/transport_r1/ASSESSMENT.md)
from one probed model to two across two providers.

## 0. Why

The original screen found five decanonised paradigms identified 50/50 in every
cell, two cross-provider raters agreeing 500/500. That is strong evidence about
**one model** and weak evidence about the **method**. A single probed model
cannot separate

- *structure-preserving domain substitution does not conceal a paradigm*, from
- *this particular model happens to recognise these five*.

An external review identified generalising this test across model families as
the most portable contribution in the project, and single-model design as the
ceiling on every thread.

## 1. Design

| Item | Value |
|---|---|
| Families | 5 (Milgram, Asch, Ultimatum, bystander, reactance) |
| Forms | 2 (canonical, decanonised alternative) |
| Probed models | 2 (`claude-haiku-4-5-20251001`, `gpt-5.4-mini-2026-03-17`) |
| Probes per cell | **50** |
| Total probes | **1000** |
| Coding calls | 200 (2 raters x 100 batches of 10) |
| Seeds | 2026091570 / 2026091571 / 2026091572 |

**Stimuli are reused unchanged.** Text, recognition question, system prompt and
coding rubric are imported from the frozen recognition modules. Regenerating
them would confound model differences with stimulus differences.

## 1.1 Two defects repaired before this study

Both were found by exploratory probing, not assumed away:

- **`max_tokens: 128` truncated answers.** The frozen screen capped answers at
  35 words; these models write longer. Raised to 256, verified on 36 probes with
  zero truncations.
- **The OpenAI path dropped Asch's 18 images**, so providers saw different
  stimuli. Anthropic image blocks are now translated to OpenAI `image_url`
  parts. Verified in
  [crossmodel_probe_images_r1](../crossmodel_probe_images_r1/ASSESSMENT.md):
  gpt-5.4-mini went 2,360 to 6,501 input tokens on Asch, provider token ratio
  0.89 from 0.32.

## 2. Coding

The frozen two-rater scheme and rubric. A probe counts as recognised **only when
both raters independently name the family**. Disagreements are counted and
reported, never resolved by majority or by one rater.

Both raters code every model's answers, including answers from a model that
shares their provider. Excluding self-provider coding would change the rater
pair per cell and confound the model comparison. The overlap is disclosed, not
avoided.

A failed rater batch is preserved and never retried; its items stay uncoded and
count as missing rather than being guessed.

## 3. Estimands, fixed in advance

**Primary:** recognition rate per family x form x model, with Wilson 95%
intervals, and the canonical-minus-alternative difference per model.

**Secondary:** per-family rate spread across models; rater disagreement count;
answers flagged ambiguous or refusal.

## 4. What a result would mean

**If alternatives are recognised at canonical rates on both models**, the
original finding generalises beyond one model and the claim becomes one about
the method of decanonisation rather than about a model.

**If recognition varies substantially by model**, the original result is
model-specific, the generalisation fails, and that is the finding. It would also
qualify every other use of these stimuli in this project.

Either outcome is reported. **The sign of the result is not a success gate.**

## 5. Cost

Measured, not estimated. Per-probe costs from
[crossmodel_pilot_r1](../crossmodel_pilot_r1/ASSESSMENT.md) and its Asch
companion give roughly **$2.75 in probes and $0.57 in coding, about $3.32
expected**. The reservation is a worst-case bytes-based bound and is far higher;
the ceiling is $20.

Against a $32 Anthropic ceiling (researcher amendment, 15 September 2026), a $30
OpenAI ceiling and the unchanged $100 package cap.

## 6. What this cannot establish

- **Recognition is not contamination.** These probes cannot separate memorised
  training examples from inference over shared abstract structure. Either way a
  decanonised control fails, but the mechanism is unidentified.
- **Recognition is not behavioural imitation.** Naming a paradigm does not show
  behaviour in it is copied.
- **Two models, two providers.** Not a survey of the field, and the original
  screen's probe target is not re-probed here.
- **One frozen stimulus bundle per form.** A different decanonisation might
  succeed; this tests whether structural fidelity suffices for concealment.
- **No ethical understanding, human resemblance or moral quality**, and no claim
  that any model is better than another.
- Raters are AI models and one shares a provider with one probe target.
  Agreement is not human validation.
