# capstone_model2: the harness cannot run a second model unchanged

**Outcome: blocked, not run. Zero usable participant decisions.**
16 September 2026.

Two failed participant calls ($0.011462000, preserved at full reservation under
the no-retry rule) plus two accepted review calls. Ledger totals after this
designation: Claude $9.894610000/$32, OpenAI $4.251449400/$30, package
$37.052132425/$100. Usage estimates, not wallet balances.

This designation set out to repeat `moral_capstone_r3` on
`claude-haiku-4-5-20251001`, changing nothing but the participant model. It
cannot be done in this harness without changing something that would invalidate
the comparison. That constraint is the result, and it is reported rather than
worked around.

## What happened, in order

| Attempt | Change | Outcome |
|---|---|---|
| r1 | model only, `max_tokens: 64` inherited | Review **accepted**; first participant call truncated at `stop_reason: max_tokens` |
| r2 | `max_tokens: 512` | Worst-case reservation rose to $6.69, above the ceiling |
| sizing | 2 agents, measure real output | Response **completed** at 424 tokens, then rejected: 1,750 bytes against a 1,024-byte cap |

## The constraint

`gpt-5.4-mini` answers these tasks with bare JSON in a handful of tokens.
`claude-haiku-4-5` writes its reasoning first and then the JSON:

> *"I need to work through my decision profile against this situation. **Key
> profile characteristics affecting this decision:** 1. **Legitimacy Locus
> (0.41)**: Moderate-low. I lean slightly toward institutional warrant..."*

and ends `...```json\n{"choice":"DESCRIBE_VAGUELY"}\n``` `. The content is
correct and the JSON is present. The harness rejects it anyway.

`phase3_recognition_run.parse` offers exactly two response contracts:

| `kind` | Contract | Haiku's response |
|---|---|---|
| `probe` | raw text, **max 1024 bytes** | rejected: 1,750 bytes |
| anything else | strict `{"ratings": [...]}` schema | rejected: wrong shape |

Neither fits a model that reasons before answering. The 1,024-byte cap lives in
`phase3_recognition.py`, whose hash is pinned by the releases of the recognition
screen, the cross-model study and every Phase 4 collector. It is frozen
machinery, not a tunable.

## Why the available workarounds were refused

**Instructing brevity.** Adding "return the JSON with no preamble or reasoning"
makes Haiku fit. It was drafted and reverted: the prompt would then differ from
`moral_capstone_r3`, and a cross-model comparison whose prompts differ tests the
prompt as much as the model. The prompts were verified identical across all four
arms before launch, and that property is worth more than the run.

**Raising the byte cap.** This would edit shared frozen source that every
completed study depends on, at the end of a long session, to unblock one
designation. Rule 10 and the write-once discipline both point the other way.

**Truncating or salvaging the response.** The JSON is recoverable by regex from
the rejected text. Doing so would mean accepting responses this project's parser
rejects, silently, for one model only.

## What this establishes

**A measured, reportable constraint on single-model experimental designs.**

This harness was built and frozen around one model's response style: short,
bare-JSON answers. That assumption is invisible while only that model is used,
and it is not recorded anywhere as a design decision — it is implicit in a
1,024-byte constant and a 64-token output budget.

A second model, from a different provider, producing **correct answers in a
different format**, cannot be run through it. Not because the model is worse or
the task is harder, but because the harness encodes one model's conventions as
validity rules.

The external review identified single-model design as the ceiling on every
thread in this project. This is a concrete instance of *why* that ceiling is
hard to lift after the fact: portability has to be designed in, not retrofitted.

## What this does NOT establish

- **Nothing about whether the capstone effect generalises.** No usable profiled
  decision was collected on the second model. `moral_capstone_r3` remains a
  single-model result and must be reported as one.
- **Nothing about either model's ability.** Haiku's responses were correct and
  complete; they were rejected on format, at a stop reason of `end_turn`.
- **No claim that the cap is wrong.** A 1,024-byte limit on a 35-word recognition
  answer is a reasonable guard. The defect is that it silently became a
  cross-cutting validity rule for every later study.

## What a future portability run would need

1. A response contract that accepts reasoning followed by a delimited answer, or
   a per-study parser rather than one shared cap.
2. Output budgets set per model from measurement, not inherited.
3. Both decided **before** collection, in a designation whose purpose is
   portability, so the prompt can stay fixed across models.

None of that is attempted here.

## Provenance

Two failed participant calls preserved at full reservation under the no-retry
rule: `capstone_model2_r1/participant/1/witness_cost/E` ($0.005258000) and
`capstone_model2_sizing/participant/1/evidence_seal/G` ($0.006204000). The
r1 review verdict was **accept** with zero blocking issues; the task set was
never in question.

No shared source was edited. `phase4_capstone_specificity_r2.py` was restored
byte-exact against its release pin after an earlier post-run correction, and that
correction lives in `phase4_specificity_rescore.py`.
