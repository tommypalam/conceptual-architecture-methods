# capstone_model2_r1: stopped on the first participant call (truncation)

**Outcome: review accepted, then stopped on participant call 1 of 960.**
16 September 2026. Superseded by [r2](../capstone_model2_r2/ASSESSMENT.md).

| Item | Value |
|---|---|
| Review verdict | **accept**, zero blocking issues |
| Participant calls | 1 of 960 |
| Failed slot | `capstone_model2_r1/participant/1/witness_cost/E` |
| Cost of the failed call | $0.005258000 |

## Cause: a real model difference, not a defect

`max_tokens` was 64, inherited from `moral_capstone_r3`, where the participant
model is `gpt-5.4-mini` and returns bare JSON in a handful of tokens.

`claude-haiku-4-5-20251001` writes its reasoning first:

> *"I need to work through my decision profile against this situation.
> **Key profile characteristics affecting this decision:** 1. **Legitimacy Locus
> (0.41)**: Moderate-low. I lean slightly toward institutional warrant..."*

It hit `stop_reason: max_tokens` at 64 output tokens before reaching the JSON
object, and the strict parser correctly rejected the truncated text.

Neither model is at fault and neither is behaving incorrectly. A 64-token output
budget simply encodes an assumption about one model's response style.

## The repair, and what was deliberately NOT changed

r2 raises `max_tokens` to 512. **Nothing else changes.**

An earlier draft also added "with no preamble, explanation or reasoning before
it" to the task instruction. That was reverted: it would have made the prompt
differ from `moral_capstone_r3`, and a cross-model comparison whose prompts
differ tests the prompt as much as the model. The prompts are now verified
identical across all four arms; only the output budget differs, and that
difference is disclosed as a necessary accommodation.

The review's acceptance of the task set carries forward on its merits; r2 seeks
its own review under the same instruction.

One paid call is preserved at full reservation under the no-retry rule and is
inherited by r2 by explicit name.
