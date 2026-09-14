# haiku_screen_r3 — per-model dispersion screen on claude-haiku-4-5

**Screen only. No profiled arm, no participant decisions, no moral score.**

## Question

Which of the eleven Phase 4 conflict tasks show baseline dispersion on
`claude-haiku-4-5-20251001`?

This is a measurement of task behaviour on a model, not a test of any hypothesis
about profiles. Nothing here bears on whether parameter profiles move decisions;
that requires a separately designated profiled study on whatever survives.

## Why

`capstone_model2_r4` ran the gpt-screened four-task pool on haiku. Three tasks
returned 1.000 in the unprofiled arm and one returned 0.000. Every cell was at a
ceiling or a floor, so its three null contrasts had no room to show an effect in
the direction one would appear, and measured nothing about the estimand. The one
cell with headroom moved: +0.133 (Holm 0.0276), G−U +0.200 (p = 0.0005).

Phase 3 established the requirement to screen for dispersion before building a
study. That requirement was met on `gpt-5.4-mini` and not repeated when the model
changed. This designation repeats it.

Seven conflict tasks have never been screened on any model but `gpt-5.4-mini`,
including `referral_fee` and `audit_sampling`, excluded there for saturation on
that model. Those exclusions carry no information about haiku.

## Prespecification

| Item | Value |
|---|---|
| Model | `claude-haiku-4-5-20251001` |
| Tasks | 6 — the conflict tasks whose net primary can discriminate |
| Probes | 25 unprofiled per task, 150 total |
| Review | 1 call, advisory (16 Sept amendment; materials previously accepted) |
| Total calls | 151 |
| Worst-case reservation | $1.108789 |
| Ceiling | $3.50 |
| Seeds | population 2026091646, schedule 2026091647, analysis 2026091648 |

**Tasks screened:** `witness_cost`, `safety_hold`, `referral_fee`,
`audit_sampling`, `wage_disclosure`, `evidence_seal`.

Task inclusion is fixed by `primary_discriminates()`, a model-independent
property of the deterministic rule map: a task whose net primary is constant
across its options cannot show an arm difference on any model. It is computed
before collection and is not an outcome.

## Gate

A task with **modal share = 1.00** is rejected as saturated: a deterministic
baseline cannot discriminate any arm contrast. The threshold is fixed in source
before collection. Tasks at ≥ 0.85 are flagged `near_ceiling` and reported, not
rejected.

**Screening is on baseline dispersion only, never on outcomes.** The screen runs
with no profile, before any profiled call exists. Every task's result is reported
whether it survives or not. Which option a task resolves to is not a criterion.

## What this cannot establish

- Nothing about whether profiles move decisions, on any model. No profiled call.
- No moral label, score or claim. No classification is computed here.
- Surviving the screen makes a task *eligible*, not validated.
- A model-specific measurement of where baselines sit, from one snapshot.

## Prior designations

r1 and r2 both stopped at the review call with zero screen probes, each having
fixed one half of a two-part routing problem. Their failures are preserved at
full reservation under the no-retry rule and inherited by name.

| | Fault | Cost |
|---|---|---|
| r1 | probes on the agnostic dispatcher, review on the shared parser (1024-byte cap); haiku returned a complete 1,592-byte fenced verdict | $0.014644300 |
| r2 | review on the agnostic dispatcher, which then had only a choice parser and rejected a verdict for not being an action id | $0.014644300 |

r3 fixes the cause. `phase4_crossmodel_dispatch` now offers two contracts a job
declares explicitly and exclusively — `valid_actions` for a task choice,
`raw_text` for a complete reply — sharing one usage guard, stop-reason check and
truncation rule. A job declaring both or neither raises. Every call in this
module goes through that one dispatcher, so no routing split remains.

## Verification before collection

- Choice path replayed against all 960 stored `capstone_model2_r4` decisions:
  **960 identical, 0 differences**.
- `read_review` tested against every observed and anticipated reply shape,
  including the fenced per-task object haiku actually sent r1: 12/12.
- Saturation gate verified to fire at modal 1.00 and to flag at 0.96.
- Reviewer prompt diffed against packet contents: all six items are conflict
  items, all declared `conflict`, none has a dominant option. The inherited
  control-item clause was removed as it described a kind not present.
- Full 151-call schedule simulated end to end against a fake haiku-style
  responder: 151/151 parsed, zero errors, zero network calls.
