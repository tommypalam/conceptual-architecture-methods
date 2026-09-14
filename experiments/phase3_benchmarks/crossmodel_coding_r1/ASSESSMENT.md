# crossmodel_coding_r1: stopped after one call (double-parse)

**Outcome: stopped. 1 of 200 coding calls dispatched.** 15 September 2026.
Superseded by [r2](../crossmodel_coding_r2/ASSESSMENT.md), which completed all
200 with the repair.

## Cause

`phase3_recognition_run.parse` recognises `kind == "coding"`, validates the
frozen rubric schema and id order itself, and returns `value["ratings"]` — a
list. This module then treated that return value as raw text and called
`.strip()` on it, raising `AttributeError: 'list' object has no attribute
'strip'` on the second call.

The repair is to validate the list the shared parser returns rather than
re-parsing it. It lives in a separate r2 module because this module's hash is
pinned by this release; the file was restored byte-exact against that pin rather
than edited in place.

One paid call is preserved at full reservation under the no-retry rule and is
inherited by r2. No probe was affected.
