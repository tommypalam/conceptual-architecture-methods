# Cross-model recognition screen: protocol r1

15 September 2026. Prospective. Extends the completed
[recognition screen](../recognition_r1/execution/transport_r1/ASSESSMENT.md)
from one probed model to three across two providers.

## 0. Why

The original screen found five decanonised social-psychology paradigms
identified 50/50 in every cell, with two cross-provider raters agreeing 500/500.
That is a strong result about **one model** and a weak one about the **method**.
A single probed model cannot distinguish

- *structure-preserving domain substitution does not conceal a paradigm*, from
- *this particular model happens to recognise these five*.

An external review of the project identified generalising this test across model
families as the most portable contribution in the work, and identified
single-model design as the ceiling on every thread. This designation addresses
both with one measurement.

## 1. Design

| Item | Value |
|---|---|
| Families | 5 (Milgram, Asch, Ultimatum, bystander, reactance) |
| Forms | 2 (canonical, decanonised alternative) |
| Probed models | 3 |
| Probes per cell | 10 |
| Total probes | **300** |
| Cells | 30 |

| Model | Provider | Role |
|---|---|---|
| `claude-sonnet-4-6` | anthropic | the model probed in the original screen |
| `claude-haiku-4-5-20251001` | anthropic | same family, smaller |
| `gpt-5.4-mini-2026-03-17` | openai | different family |

**Stimuli are reused unchanged.** Text, recognition question and system prompt
are imported from the frozen recognition modules. No stimulus is regenerated,
reworded or re-reviewed: reusing the exact frozen text is what makes a
cross-model comparison meaningful, and regenerating it would confound model
differences with stimulus differences.

## 1.1 Cost

The reservation is a worst-case bound, not expected spend: it charges the full
input bound plus full max output at output price, and `input_token_bound` counts
utf-8 bytes rather than tokens, over-counting input roughly fourfold. The Milgram
stimulus is about 8,000 characters, so the bound is large.

Prior studies in this project settled near 17% of reservation. Ten probes per
cell is chosen so the ceiling stays well inside remaining allowances while the
design keeps all three model arms under one protocol and one rubric.

## 1.2 Provider ceiling amendment

The recorded $15 Anthropic ceiling was reached as a binding constraint when this
designation was prepared: $7.139674300 was already spent and the full schedule
reserves $13.14 on the Anthropic side.

**The researcher stated on 15 September 2026 that the $15 figure was a
conservative planning estimate rather than a hard limit, and raised it for this
designation.** The ceiling used here is $25 Anthropic. This is recorded as an
explicit amendment, in the source and in this protocol, rather than applied
silently.

The $100 package cap is **unchanged** and still enforced. Reservation
$15.9859755 against it; expected settlement near $2.7 on the prior 17% ratio.
No other budget figure changes, and cumulative totals do not reset.

## 2. Coding

The established two-rater scheme with the frozen rubric. A probe counts as
recognised **only when both raters independently say so**, matching the original
screen's rule. Disagreements are reported, never resolved by majority or by one
rater.

Both raters code every model's answers, including their own. Excluding
self-coding would change the rater pair per cell and confound the model
comparison; the overlap is disclosed rather than avoided, and is a stated limit.

## 3. Estimands, fixed in advance

**Primary:** the recognition rate per family x form x model, and the
canonical-minus-alternative difference per model.

**Secondary:** mean alternative-form rate per model; rater disagreement count.

## 4. What a result would and would not mean

**If alternatives are recognised at canonical rates across all three models**,
the original finding generalises beyond one model, and the claim becomes one
about the method of decanonisation rather than about a model.

**If recognition varies substantially by model**, the original result is
model-specific, the generalisation fails, and that is the finding. It would also
qualify every other use of these stimuli in the project.

Either outcome is reported. **The sign of the result is not a success gate.**

## 5. What this cannot establish

- **Recognition is not contamination.** These probes cannot distinguish
  memorised training examples from inference over shared abstract structure.
  Either way a decanonised control fails, but the mechanism is unidentified.
- **Recognition is not behavioural imitation.** Naming a paradigm does not show
  that behaviour in it is copied.
- **Three models, two providers.** Not a survey of the field.
- **One frozen stimulus bundle per form.** A different decanonisation might
  succeed; this shows structural fidelity is not sufficient for concealment.
- **No ethical understanding, human resemblance or moral quality**, and no claim
  that any model is better than another.
- The raters are AI models and one rater shares a provider with two probe
  targets. Agreement is not human validation.
