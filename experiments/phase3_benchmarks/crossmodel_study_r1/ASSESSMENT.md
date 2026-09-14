# crossmodel_study_r1: 1000 probes collected, coding stage failed by design error

**Outcome: incomplete. 1000/1000 probes collected and preserved. All 200 coding
calls refused before dispatch. No recognition rate is estimated.**
15 September 2026.

**The 0.00 rates in `results.json` are the absence of coding data, not a
finding.** They must not be read as "no model recognised anything". Every
recognition cell is uncoded.

## Result

| Item | Value |
|---|---|
| Probes collected | **1000 / 1000**, all preserved |
| Coding calls dispatched | **0 / 200** |
| Coding calls refused | 200, all with `Slot outside complete reservation` |
| Recognition rates | **none; every cell is uncoded** |
| Cost | $3.091415800 (probes only; no coding money was spent) |
| Calls | 1000 |

Accounting: Claude $9.504403700/$32, OpenAI $3.642239700/$30, package
$35.783528825/$100. Usage estimates, not wallet balances.

## Cause: a design error in how the release was frozen

The ledger refuses any dispatch whose request does not match its frozen
reservation exactly — model, token bound, kind, max output, **and request
hash**. That guard is correct and did its job.

Coding requests cannot be known before the probes run: each batch packages ten
real answers. This study froze the coding slots against a **placeholder** answer
(`"x" * 1024`), then rebuilt them from the real answers at collection time. The
rebuilt requests necessarily differ from the placeholders in both content hash
and token bound, so all 200 were refused.

`recognition_r1` did not have this problem because it reserved coding by
**model and bound only**, without a per-request hash, and treated coding as a
separate stage. Freezing a content-dependent stage against fabricated content in
a single release cannot work, and the guard correctly says so.

**No coding call reached a provider**, so the failure cost nothing beyond the
probes, which are intact and reusable.

## What is preserved and reusable

All 1000 probe answers are saved in `answers.json` and `probe_rows.json`, with
their per-call records written once in the ledger:

| Family | Form | haiku-4.5 | gpt-5.4-mini |
|---|---|---:|---:|
| each of 5 | canonical | 50 | 50 |
| each of 5 | alternative | 50 | 50 |

Stimuli were the frozen `recognition_r1` text, reused unchanged, with the
repaired provider-symmetric image path so both models received the same 18 Asch
images. `max_tokens` was 256 and no probe was truncated.

**A continuation needs only the coding stage**, dispatched as a separately
designated release that reserves by model and bound rather than by request hash.
The probes must not be re-collected: they are complete, paid for, and frozen.

## What this does and does not establish

**Does:** that 1000 cross-model probes can be collected cleanly on the repaired
request path for $3.09, and that the ledger's reservation guard blocks a
content-dependent stage frozen against fabricated content.

**Does not:** any recognition rate, any cross-model comparison, any claim about
whether the single-model `recognition_r1` finding generalises. That question
remains exactly as open as it was before this run.

The exploratory pilots' descriptive observation — that milgram, ultimatum and
bystander alternatives were named by both models while reactance was not —
stands as it was: 2 probes per cell, keyword-matched, supporting nothing.

## Provenance

All 1000 records written once and preserved. The inherited
`crossmodel_recognition_r1` failed slot is carried forward untouched. No
stimulus, rubric, parameter or frozen result was altered. A duplicate launch
attempt during this run was correctly refused by the ledger's exclusive lock
(`FileExistsError: execution.lock`), so only one collector ever wrote.
