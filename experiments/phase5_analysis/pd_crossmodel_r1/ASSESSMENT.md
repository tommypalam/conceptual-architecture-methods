# pd_crossmodel_r1: PD's directional prediction holds on a second provider

**Outcome: complete. 481 calls, 480/480 valid, zero failures.**
18 September 2026. Review **revise**, two blocking issues, both assessed below.
Cost $1.245072 against a $6.433 reservation.

Ledger after this designation: Claude $22.238957400/$32, OpenAI $11.093290725/$40.
Usage estimates, not wallet balances.

**PD moves the deterministic good/bad headline on `claude-haiku-4-5`, in the
direction locked from theory before collection.**

## Result

| Arm | Good-rate | n |
|---|---:|---:|
| PD− (0.10, outcome-dominant) | 0.617 | 240 |
| **PD+ (0.90, process-dominant)** | **0.750** | 240 |

**Paired +0.133, one-sided p = 0.00031, 240 pairs, 84 discordant (58 vs 26),
4 of 6 items in the predicted direction.** Both conditions of the prespecified
one-sided rule met.

| Item | Effect | one-sided p | Holm |
|---|---:|---:|---:|
| **`storage_unit`** | **+0.350** | **0.00129** | **0.0077** |
| `desk_booking` | +0.225 | 0.0112 | 0.0562 |
| `ward_transfer` | +0.150 | 0.143 | 0.453 |
| `weekend_rota` | +0.125 | 0.113 | 0.453 |
| `meeting_room` | +0.000 | 0.623 | 1.000 |
| `tool_library` | −0.050 | 0.855 | 1.000 |

## Why this is a stronger test than the ID replication

**The prediction was one-sided and derived, not two-sided and descriptive.**
`id_crossmodel_r1` had to be two-sided because ID has no theory mapping onto
these items. PD does: 0 = outcome-dominant, 1 = process-dominant, and on every
item the option that keeps the stated arrangement classifies `good`.

**That premise is a property of the item set, not of the coordinate**, so it does
not automatically transfer from gpt's seven items to haiku's six.
`verify_direction()` re-checked it against this item set at build time and
**gated `prepare()`**; all six passed. Only the direction carried over from gpt —
never the magnitude.

A significant effect in the wrong direction would have been recorded as a
directional failure; the analysis computes both p-values and flags that case
explicitly. It did not fire.

## Both load-bearing coordinates now have cross-provider evidence

| Coordinate | gpt | haiku | Direction |
|---|---:|---:|---|
| **PD** Procedural Dependence | **+0.346** | **+0.133** | one-sided, theory-derived |
| **ID** Internalisation Dependence | +0.111 | +0.075 | two-sided, descriptive |

**Both shrink on haiku** — PD to roughly 38% of its gpt effect, ID to 68%. **What
replicates is the direction and the decision rule, not the magnitude**, and
nothing here licenses a claim that effect sizes are stable across models.

## A correlation pointed at nothing, and the manipulation found something

PD's **post-hoc correlation on haiku was +0.089** — near flat, and the basis for
this project describing PD as "flat on haiku" before this designation. Pinning PD
to its endpoints gives **+0.133 at p = 0.0003**.

This is the LL lesson running the other way. LL's post-hoc correlation was
strongly positive (+0.271) and its manipulation was negative then null. PD's
post-hoc correlation on haiku was near zero and its manipulation is clearly
positive. **Correlations on unmanipulated coordinates mislead in both
directions**, which is the case for prospective manipulation rather than for
trusting any particular correlation's sign.

## The review returned *revise*, and both findings are assessed

Advisory under the 16 September amendment: these six items are byte-identical to
material `phase4b_profiled_r1` reviewed and **accepted with zero blocking
issues** before collecting 631 decisions on them, on this same model.

### Finding 1 — "tied payoffs mean the items do not test a real tradeoff"

> *"Both options produce the same aggregate net loss … not genuinely testing a
> tradeoff between aggregate welfare and individual rights."*

**This describes the design correctly and reads it as a defect.** The totals are
tied at −3 on every item **deliberately**, a property established in
`pd_discriminant_r2`, which refuted its own r1 welfare reading by tying totals
and finding the choices did not move.

Tying them is what makes welfare-maximisation, minimax and best-case seeking
**indifferent by construction**, so a PD+/PD− difference cannot be produced by any
of them. Generic compliance predicts no difference either, since both arms are
equally profiled and differ in one line. The contrast is within-profile, which is
the entire point.

**Not accepted as a defect.** The stipulation was declared before collection and
applies identically to both arms.

### Finding 2 — `tool_library` carries heavier normative weight

> *"Item 03 … describes retaining property against an owner's explicit withdrawal
> under stipulated contractual terms … a stronger deontological violation
> (property rights + contract) than the other items."*

**This has a real point.** `tool_library` states the member *owns* the press and
lent it "under terms letting them withdraw it" — ownership plus contract —
whereas `desk_booking` describes a person who *booked* a desk. Those are not
equal normative weight, and the item set is not perfectly parallel on that
dimension.

**The data settle its direction.** `tool_library` is the single item with a
**negative** effect (−0.050) — it works *against* the result:

| Set | Effect | one-sided p |
|---|---:|---:|
| **all six items (primary)** | **+0.133** | **0.00031** |
| without `tool_library` (sensitivity) | +0.170 | 0.00006 |

If the concern is valid, the reported +0.133 is **conservative**.

**All six items are reported as primary.** Dropping an item after seeing results
would be outcome-driven selection, which this project forbids and which the 17
September ceiling amendment explicitly refused when it cost 40% of a budget. The
six-item figure stands and the sensitivity check is recorded as a check, not as
the headline.

### The methods finding gains a fifth data point

These items have now been reviewed by five designations. Four accepted them with
zero blocking issues — `phase4b_grand_r1`, `phase4b_screen_r2`,
`phase4b_sonnet_r1`, `phase4b_profiled_r1`, the last of which then collected 631
decisions on them — and this one returned revise with two blocking issues.

**An AI review's verdict is not a stable property of the material.** That was the
evidence behind the 16 September amendment and this designation reproduces it on
byte-identical items. No review was re-run to obtain a different verdict; one was
dispatched and its verdict is recorded in full.

## What this establishes

**PD's endpoint effect is not specific to the calibration model**, and its
theory-derived direction holds on a second provider under a one-sided test whose
premise was re-verified against the new item set.

**Together with `id_crossmodel_r1`, both load-bearing coordinates are now
cross-provider**, which removes the sharpest scoping limitation on the coordinate
result.

## What this does NOT establish

- **NOT that PD is verified cross-model.** Verification on gpt required the
  numeral-identical swap control from `label_semantics_r1`, which showed the
  effect belongs to the PD *label* rather than to numeric extremity. **No swap
  control was run on haiku**, for the same power reason it was not run for ID: a
  four-arm design quadruples the Holm family. This licenses *"PD moves the
  outcome on haiku too"* and nothing stronger.
- **Not the same item set.** Four of six overlap with gpt's seven;
  `ward_transfer` is haiku-only, `on_call` and `rest_break` are gpt-only. Forced,
  not chosen: `haiku_screen_r4`'s six alternatives all returned modal share 1.00.
- **Not magnitude stability.** +0.133 against gpt's +0.346.
- **Not moral truth or improvement.** Deterministic classification under
  stipulated standards, computed from stipulated transitions, never read from
  agent text.
- **Not that PD is understood as a concept.**
- **Not generalisation.** Six items, 40 agents, one harness, one snapshot.
- **No human validation**; raters remain deferred.

## The empty-analysis defect is fixed at source

`coordinate_sweep_r2` and `id_crossmodel_r1` both set `SCREEN_N = 0` and then had
`collect()` derive an empty usable-task list from the absent screen, so every
contrast returned `None` and both needed an offline rescore. The data were intact
both times; the designations' own analyses were not.

**This collector fixes it.** `declared_tasks()` supplies the pool's own
`TASK_IDS` whenever the screen is skipped, and `analyse()` falls back to it,
verified against an empty `usable` list before collection. The results record
confirms it fired: `task_list_source` reads *"declared_tasks() — the pool's own
TASK_IDS, because this designation skips the screen"*. **This designation produced
its own analysis and needed no rescore.**

## Provenance

Build-time checks before any call:

- `verify_direction()` on all six items, **gating `prepare()`** — the one-sided
  prediction's premise re-verified against this item set.
- `verify_construction()` across all 40 agents — arms differ in the PD line
  alone, nine coordinates identical, **zero coincident draws**.
- A per-pair wire check across all **240 agent-item pairs**: exactly two diff
  lines, both the PD line at 0.10 and 0.90, byte-identical user text.
- One-sided statistics verified against synthetic fixtures in both directions
  before collection: strongly-predicted gives p = 0.000011, strongly-wrong gives
  p = 0.999998 and raises the directional-failure flag, and a 3+/3− split fails
  the consistency rule.

Power measured before collection against haiku's **measured** per-item baselines
from `phase4b_profiled_r1`, 20 seeds — not a uniform effect, the error that
caused `phase4b_sonnet_r1` to report 8/8 when the true figure was ≤5/10. Reported
across the plausible range rather than at one flattering point: **15/20** at
haiku's post-hoc +0.089, 19/20 at +0.150, **20/20** at gpt's +0.346, and **1/20
false positive at zero**. Reproducible via `code/phase5_id_crossmodel_power.py`.

481 calls dispatched, 480 valid, zero entries in `failures.jsonl` for this
designation. Failures from earlier designations remain preserved and unretried.
