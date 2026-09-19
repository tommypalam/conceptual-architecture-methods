# probe_fields_r1 — protocol

**Status: prepared offline.** Programme context: [../PROGRAMME.md](../PROGRAMME.md)
(Stage 4b, including its five-perspective review). Follows
[semantics_r1](../semantics_r1/ASSESSMENT.md). Exploratory; not part of the
submitted thesis.

## Question

`semantics_r1` showed the PD effect follows the stated meaning of the PD scale. Is
that special to the framework's parameter, or does *any* on-topic field carrying an
explanation move choices as it says — including one whose meaning points the
other way?

## Run statement (rule 4)

| | |
|---|---|
| Model | `gpt-5.4-mini-2026-03-17`, temperature 1, reasoning disabled |
| Configuration | NEUTRAL on all five axes |
| Agents | 40, independent Beta marginals, seed **2026092001** |
| Items | the seven screened gpt items, byte-identical |
| Cells | 4 probe fields × 2 levels = 8; **2,240 calls**, one run |
| Seeds | population 2026092001, schedule 2026092002, analysis 2026092003 |
| Cost | $11.012 reserved worst case; about $1.67 expected at settlement |

## Design

Each probe replaces the name and both endpoint texts of entry 10 (Affective
Weighting's slot) and is pinned to 0.10 and 0.90. The slot was chosen because
`position_counterbalance_r1` measured an extreme numeral there at +0.061 and
+0.004. PD and the eight other entries keep the agent's drawn values.

| Code | Field | 0 = | 1 = | Predicted |
|---|---|---|---|---|
| SQ | Status-quo Preference | existing arrangements carry no special weight | existing arrangements stand unless there is strong reason to change them | + |
| SW | Stated-Wish Deference | a stated wish is one input among many | a person's stated wish about their own arrangement is decisive | + |
| WO | Worst-off Priority | total benefit matters however it is spread | whoever would lose most matters most | + |
| **NC** | **Numbers Count** | claims are weighed regardless of how many hold them | the option helping more people is favoured | **negative** |

Signs are derived from each gloss and a property of the item set: on every item
one party holds an arrangement, has said they want to keep it, and loses 5 if
overridden against 4 lost on the other side if kept; keeping classifies `good` on
all seven. **NC's prediction is weaker by construction** — only some items put a
countable larger group on the overriding side — so per-item effects are reported.

Verified for all 40 agents before any call: every cell differs from the agent's
canonical block on entry 10's three lines only; within a probe the two levels
differ in one numeral and are equal in length; "Affective Weighting" appears
nowhere; the eight cells are eight distinct blocks.

**These are probe fields, not parameters.** Nothing here amends the ten.

## Analysis, fixed before collection

Design content hash `25b23a16057afebd3df102a23d03905b56a371a982921fc618a99be039a9d032`.

1. Each within-field effect (printed 0.90 minus 0.10, paired by agent and item)
   with a 95% unit-bootstrap interval (10,000 draws, units complete in all eight
   cells). Two-sided sign tests, Holm over the four. No gate: no probe has a prior
   effect to replicate.
2. **Readings.** *Generic cue*: all four share a sign, intervals excluding zero.
   *Meaning-general*: NC negative, interval excluding zero, and at least two of
   SQ/SW/WO positive likewise. *PD-special*: every interval inside (−0.15, +0.15).
   *Mixed*: anything else, reported field by field.
3. Reference for magnitude: PD CANON +0.3393 (`semantics_r1`). Comparing a probe to
   PD is descriptive — different slot, different population draw.
4. All seven items primary; none dropped after results; no cell re-run.

Power (measured baselines, Holm family 4, 40 agents): 18/20 at |0.15|, 20/20 at
|0.20|, 8/20 at |0.10|. **A screen, not a settlement**; a surviving field gets a
larger follow-up before anything is claimed about its size.

## Disclosed choices (as `semantics_r1`)

256-token output cap; no review call — items are byte-identical to accepted
material and the parent verdict is read from the ledger; fresh population seed.
**The probe entries are new material no reviewer has seen.** They rest on the
byte-level construction checks and the researcher's direction to proceed under
the programme's protocol (20 September).

## What no outcome establishes

That any probe is or should be a framework parameter; understanding, or a
difference between reading an explanation and following an instruction phrased as
one; anything beyond this model and these seven items. *Meaning-general* would cap
what the ten parameters can claim — the programme's criterion for PD being special
is then defeasibility (Stage 3a), not effect size.
