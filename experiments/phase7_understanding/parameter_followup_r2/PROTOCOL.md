# parameter_followup_r2 — protocol

**Status: prepared offline.** Programme: [../PROGRAMME.md](../PROGRAMME.md),
Stage 4a. Companion to
[parameter_followup_r1](../parameter_followup_r1/ASSESSMENT.md). Exploratory; not
part of the submitted thesis.

## Question

The sweep's two near-misses, at a sample size that can settle them.

| Code | Prior (sweep, 25 agents) | Holm | Status |
|---|---:|---:|---|
| **TfA** Tolerance for Asymmetry | −0.1029 | 0.111 | uncorrected interval excludes zero |
| **MoR** Mode of Response | −0.0971 | 0.069 | uncorrected interval excludes zero |

The thesis records both as "below the certified threshold", **not flat** — their
uncorrected intervals exclude zero but neither survived Holm. They are the last
unfinished business inside the ten.

## Run statement (rule 4)

| | |
|---|---|
| Model | `gpt-5.4-mini-2026-03-17`, temperature 1, reasoning disabled |
| Configuration | NEUTRAL on all five axes |
| Agents | **80**, independent Beta marginals, seed **2026092025** |
| Cells | 2 coordinates × 2 levels = 4; 7 items; **2,240 calls** |
| Seeds | population 2026092025, schedule 2026092035, analysis 2026092036 |
| Cost | $10.984 reserved worst case; about $1.67 expected |

Design content hash `3897b681466fdc673bd276b24917439441283ae6e3dc9331a3ab75cb91f03212`.

## Why 80 agents

Simulated against the measured gpt per-item baselines, Holm family 2, 20 seeds:
at |0.10| — where both coordinates sit — power is **9/20 at 40 agents** and
**18/20 at 80**. At 25 agents, where they were first measured, an effect of that
size was barely detectable. **A 40-agent re-test would have been a coin flip on
exactly the effects it was built to settle.**

## Design and analysis, fixed before collection

Identical to r1: each coordinate pinned to 0.10 and 0.90 with the other nine drawn
per agent and held byte-identical between levels. Verified for all 80 agents —
the two levels differ on exactly one line, at that coordinate's own entry, and are
equal in length. The seed was chosen before any call as the first with no
rendered-precision collision on either coordinate, the same check that blocked
r1's first seed.

- **Two-sided for both.** Neither has a theory-derived direction on these items;
  adopting the sweep's sign after seeing it would be post-hoc confirmation.
- Paired sign test, Holm over the family of **2**, 4-of-7 item consistency, a 95%
  unit-bootstrap interval and a 90% equivalence bound per coordinate.
- **No replication gate**: neither coordinate has an established effect to
  reproduce.
- No coordinate re-run with more agents after results are seen.

**A null bounds the effect below about 0.10 on these items; it does not establish
zero,** and the assessment must say so. Given the priors, the most likely outcome
is two tighter bounds rather than two effects — that is a useful result and will
be reported as one.

## What no outcome establishes

Understanding, or that any coordinate is understood as a concept. That a
coordinate which moves the outcome is a **label** effect — that needs a swap
control, which this designation does not run. Anything beyond `gpt-5.4-mini` and
these seven items. [probe_fields_r1](../probe_fields_r1/ASSESSMENT.md) bounds what
any such result would mean for the architecture: a glossed field moving choices
does not single out the ten parameters.
