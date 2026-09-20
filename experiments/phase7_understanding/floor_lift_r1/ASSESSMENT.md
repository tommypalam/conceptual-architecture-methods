# floor_lift_r1 — assessment

**Complete. 2,240 calls, 2,240/2,240 valid, zero failures, $1.687996.**
`gpt-5.4-mini-2026-03-17`, 40 agents (seed 2026092011), seven items in two
versions, eight cells, 20 September 2026. Protocol: [PROTOCOL.md](PROTOCOL.md).
Design hash `6031a0f8…7e49bfad`.

**Gate PASSED. Decision: `mixed` — neither locked reading holds, and the result
runs opposite to the one this designation was built to look for.**

## Headline numbers

Gate (all seven items, both versions):

| Arm | Effect | Holm | Expected |
|---|---:|---:|---|
| PD:BASE | **+0.3500** | ~0 | +0.3393 ✓ |
| SQ:BASE | **+0.3571** | ~0 | +0.4000 ✓ |
| PD:TWIN | +0.3286 | ~0 | — |
| SQ:TWIN | +0.3143 | ~0 | — |

Lift on the three floored twins, 120 complete units:

| Quantity | Estimate | 95% CI |
|---|---:|---|
| L(PD) | **+0.3833** | [+0.2917, +0.4750] |
| L(SQ) | **+0.1333** | [+0.0583, +0.2083] |
| **L(SQ) − L(PD)** | **−0.2500** | **[−0.3583, −0.1417]** |

**PD lifts the floored twins roughly three times as hard as the pure status-quo
field.** The locked rule anticipated only SQ ≥ PD and correctly returned `mixed`
rather than forcing a reading.

## The cell-level table, which qualifies the headline

Keep-rate per cell (n = 40 each):

| Item | Field | BASE lo | BASE hi | TWIN lo | TWIN hi |
|---|---|---:|---:|---:|---:|
| rest_break | PD | 0.100 | 0.925 | 0.100 | **0.775** |
| rest_break | SQ | 0.650 | 0.725 | 0.425 | **0.775** |
| tool_library | PD | 0.375 | 0.975 | 0.200 | **0.675** |
| tool_library | SQ | 0.575 | 0.950 | 0.400 | **0.450** |
| storage_unit | PD | 0.475 | 0.900 | **0.000** | **0.000** |
| storage_unit | SQ | 0.575 | 0.950 | **0.000** | **0.000** |

Three things this shows that the pooled lift hides:

**1. The "floor" was not a floor under profile.** Unprofiled, these twins sat at
0.00–0.04. Under a profile they are mobile: PD-high reaches 0.775 and 0.675 on two
of them. **An unprofiled baseline does not predict the profiled range** — a
finding in its own right, and a caution for every screen this project runs.

**2. Part of PD's larger lift is a LOWER low arm, not a higher high arm.** On
`rest_break` both fields reach 0.775 when high; PD starts at 0.100 and SQ at 0.425.
PD's +0.675 against SQ's +0.350 on that item is mostly the starting point. On
`tool_library` the ceilings do differ (0.675 vs 0.450), so this does not explain
everything.

**3. `storage_unit` is 0.000 in all four twin cells** and contributes nothing but
dilution to both estimates. It is retained — dropping an item after seeing results
is the outcome-driven selection this project forbids — but the two informative
items are `rest_break` and `tool_library`.

## What actually happened, stated against the prediction

The protocol predicted that a process-dominant agent would have **no reason** to
protect an arrangement that bypassed its procedure, so PD's keep-rate would stay
on the floor while a status-quo field lifted it. **The opposite occurred.**

Comparing each field's high arm across versions — how much the procedural lapse
deters an agent already set to that field's maximum:

| Item | PD high: BASE → TWIN | SQ high: BASE → TWIN |
|---|---|---|
| rest_break | 0.925 → 0.775 (**−0.15**) | 0.725 → 0.775 (+0.05) |
| tool_library | 0.975 → 0.675 (**−0.30**) | 0.950 → 0.450 (**−0.50**) |
| storage_unit | 0.900 → 0.000 (−0.90) | 0.950 → 0.000 (−0.95) |

**A high-PD agent is LESS deterred by the procedural lapse than a high-SQ agent**
on `tool_library` (−0.30 vs −0.50), and no more deterred on `rest_break`. Whatever
"Procedural Dependence: 0.90" does to this model, it is not "care that the
procedure was followed by the holder".

## What this means for the status-quo-dial question

**The dial hypothesis is not confirmed, and it is not refuted.** The two fields
demonstrably behave *differently* — the difference −0.250 [−0.358, −0.142] is the
cleanest dissociation between PD and a pure status-quo field this project has
produced, and it is a genuine answer to `probe_fields_r1`'s worry: **PD is not
interchangeable with a status-quo field.**

But the dissociation runs the wrong way for the framework's story. PD does not
behave like "procedure matters"; it behaves like a **stronger, more indiscriminate
keep-the-arrangement pressure than an explicit keep-the-arrangement field** —
larger range on the base items, and less sensitive to the arrangement's provenance.
A plausible description is that PD's gloss ("fair procedure matters independently")
is read as weighting *the holder's established claim*, with the question of whether
the holder honoured the procedure carrying little weight. That is a hypothesis
generated after seeing the data and is **not tested here**.

**Nothing licenses calling this procedural justice**, and §7 of the thesis should
not be strengthened on this result. If anything it narrows what PD's verified
effect can be said to be.

## Limits

- Three items carry the test, one of which (`storage_unit`) is degenerate. Two
  informative items is thin, and the per-item spread is wide (PD:TWIN +0.675,
  0.000, +0.475).
- The floored-twin comparison is between fields in **different slots** (PD entry 6,
  SQ entry 10). `position_counterbalance_r1` measured entry 10 as near-neutral for
  an extreme numeral, but the slots are not proven equivalent for a *glossed* field.
- Power bounds a null below ~0.10; no null is being read here, so this does not
  bite, but the reverse-direction finding rests on two items.
- One model, one item family, one presentation of each item.
- No twin option is morally classified. The `good` classification is the base
  items' stipulation and is deliberately not applied to twins; the outcome here is
  the share choosing the base item's KEEP option, nothing more.

## Accounting

OpenAI $16.259575 → **$17.947571**/$40. Anthropic unchanged $22.268707/$32.
Package ≈ $40.216/$100. Usage estimates, not verified provider balances.
