# floor_lift_r1 — protocol

**Status: prepared offline.** Programme: [../PROGRAMME.md](../PROGRAMME.md),
Stage 3a, one-directional. Exploratory; not part of the submitted thesis.

## Question

[probe_fields_r1](../probe_fields_r1/ASSESSMENT.md) showed an invented
"Status-quo Preference" field (+0.400) matching Procedural Dependence (+0.339), so
**PD may be a status-quo dial**. Two screens failed to build twins the model
splits on ([r1](../defeasibility_screen_r1/ASSESSMENT.md),
[r2](../defeasibility_screen_r2/ASSESSMENT.md)): eleven wordings put three items on
a floor of 0.00–0.04 unprofiled keep.

**The floor is the instrument.** On a floored twin the two readings differ:

- **DIAL** — "PD high → keep what exists": raising PD **lifts** the keep-rate, as
  raising Status-quo Preference does.
- **PROCESS** — a process-dominant agent has no reason to protect an arrangement
  that went around its own procedure: the keep-rate **stays on the floor**.

## Run statement (rule 4)

| | |
|---|---|
| Model | `gpt-5.4-mini-2026-03-17`, temperature 1, reasoning disabled |
| Configuration | NEUTRAL on all five axes |
| Agents | 40, independent Beta marginals, seed **2026092011** |
| Cells | 2 fields x 2 levels x 2 item versions = 8; **2,240 calls** |
| Items | the seven screened items (BASE) and their r1 twins (TWIN) |
| Seeds | population 2026092011, schedule 2026092012, analysis 2026092013 |
| Cost | $11.117 reserved worst case; about $1.67 expected |

Design content hash `6031a0f8b6e83facba6bbba14f2be909bf60a455d93afb06f48a5c2e7e49bfad`.

## Design

PD is pinned at entry 6 with its canonical gloss; Status-quo Preference replaces
entry 10 (AW's slot, near-neutral by `position_counterbalance_r1`). Verified for
all 40 agents: within a field the two levels differ on one line and are equal in
length; PD and SQ move different entries and neither touches the other; BASE and
TWIN differ only in the situation paragraph.

**The three floored twins carry the test** — `rest_break`, `storage_unit`,
`tool_library` (unprofiled keep 0.04, 0.00, 0.00). They are also the three where
PD's BASE effect is **largest** (+0.800, +0.675, +0.400 in `semantics_r1`), so the
design asks whether the field that moves these items most on the base version
moves them at all once the arrangement bypassed its procedure.

## Analysis, fixed before collection

1. **Gate.** Both BASE arms must reproduce their known effects (PD ≈ +0.34,
   SQ ≈ +0.40; one-sided, Holm over the four base contrasts, 4+ of 7 items
   positive). If either fails, the twin arms are not interpreted.
2. **Primary: L(SQ) − L(PD)** on the floored twins — a within-unit difference with
   a 95% unit-bootstrap interval. **Not** one arm clearing a threshold while the
   other does not; that inference was withdrawn over ID.
3. **Locked readings.** *PD is not a dial*: SQ lifts, PD does not, difference
   excludes zero. *PD is a dial*: both lift, difference includes zero.
   *Uninformative*: SQ does not lift either — no field tested can move the floor,
   so PD's null says nothing. *Mixed*: anything else, reported as such.
4. All seven items primary; no cell re-run; no twin option morally classified.

**Power** (simulated at a 0.02 floor, 40 agents x 3 items, Holm over 4): +0.20
lift 200/200, +0.15 194/200, +0.10 148/200, **+0.05 44/200**, zero false positives.
**A null therefore bounds the lift below about 0.10 and does not establish zero**,
and the assessment must say so.

The decision rule was exercised offline on planted data for all three readings
before release.

## Disclosed choices

256-token output cap; no review call — **two** inherited verdicts are recorded and
not re-dispatched: `position_counterbalance_r1/review/0` (base items, accept) and
`defeasibility_screen_r1/review/0` (twins, accept); fresh population seed.

## What no outcome establishes

Understanding; that PD encodes procedural justice; anything about other models or
items. *PD is not a dial* would establish a **dissociation** between PD and a pure
status-quo field on items where an arrangement bypassed its procedure — stronger
than anything in the thesis, and still not understanding.
