# inverse_inference_r1 — protocol

**Status: prepared offline.** Programme: [../PROGRAMME.md](../PROGRAMME.md),
marker 4 (bidirectionality). Exploratory; not part of the submitted thesis.

## Question

Every result in this project runs one way: a value is placed in a field and the
model acts on it. [semantics_r1](../semantics_r1/ASSESSMENT.md) showed the action
follows what the gloss *says*; [probe_fields_r1](../probe_fields_r1/ASSESSMENT.md)
showed the same for invented fields. **Neither separates reading an explanation
from following an instruction phrased as one** — the live deflationary rival.

Inference runs the other way. The model sees only a transcript of choices and is
asked which agent had Procedural Dependence set high. There is no field in the
prompt to follow. An instruction-follower has no particular reason to succeed.

## Run statement (rule 4)

| | |
|---|---|
| Model | `gpt-5.4-mini-2026-03-17`, temperature 1, reasoning disabled |
| Materials | the frozen `pd_prospective_r1` archive — **no new participant data** |
| Trials | 40 paired trials x 3 conditions = **120 calls** |
| Seeds | A/B order 2026092131, analysis 2026092132 |
| Cost | $0.487 reserved worst case; about $0.09 expected |

Design content hash `01dbadd6fcef57b6f03766b21bffb3d32ede9e8847eb0b3e4027fffd538abe6e`.

## Design

Each trial shows **two transcripts from the same agent** — one produced at PD 0.10,
one at 0.90 — in a randomised A/B order, and asks which had the setting high.
Chance is exactly 0.50 and needs no baseline estimate.

**Why paired.** Singly, the best keep-count threshold separates the arms at only
0.875, so a single-transcript design would confound the model's ability with an
unavoidable ceiling. As pairs the arms separate at 36/40 with 4 ties.

| Condition | What the model is told differed |
|---|---|
| GLOSSED | the name *Procedural Dependence* **and** its two-line gloss |
| NAMED | the name only |
| **BLIND** | **that one unnamed numeric setting differed** |

**BLIND is the control that matters.** If accuracy there matches GLOSSED, the model
is counting which transcript keeps more arrangements and nothing about the field is
being recovered.

Verified before release: the A/B key is fixed in the release, no prompt contains
"PD", "0.10" or "0.90", BLIND names and glosses nothing, NAMED is name-only, and
the judge's system prompt carries no profile block.

## Locked predictions

| Reading | GLOSSED | NAMED | BLIND |
|---|---|---|---|
| surface statistic | high | high | high |
| **field recovery** | high | high | **lower** |
| no inference | chance | chance | chance |

## Analysis, fixed before collection

1. Accuracy per condition with a 95% interval, against chance at alpha/3.
2. **Primary: the paired within-trial difference GLOSSED − BLIND** with its own
   interval — not one condition clearing chance while another does not.
3. **The ceiling is measured, not assumed**: a keep-count rule reaches 36/40
   (0.90 counting ties wrong, 0.95 counting them half). Model accuracy is reported
   against that as well as against chance. **Exceeding it is not expected and is
   not the test**; matching it under GLOSSED while BLIND falls short is.
4. No condition re-run with more trials after results are seen.

The decision rule was exercised offline on planted data for all three readings.

## What no outcome establishes

Understanding, or that the field is represented conceptually. That inference and
action share a mechanism — only that both are present. Anything about fields other
than PD, models other than this one, or items outside these seven.
