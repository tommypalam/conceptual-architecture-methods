# pd_crossmodel_r1 — does PD's endpoint effect exist outside the calibration model?

**481 calls, worst case computed from the job list. Review advisory.**

## The gap this closes

`pd_prospective_r1` pinned PD to its endpoints and measured **+0.346**, the
largest effect in the project, with the **direction locked from theory before
collection**. `label_semantics_r1` then showed the effect belongs to the PD
*label*: the same numerals on the inert AW label gave −0.036.

**Both ran on `gpt-5.4-mini` only.**

`id_crossmodel_r1` has since replicated ID on haiku (+0.075, p = 0.033, 4 of 6
items). That leaves an asymmetry worth removing: **ID currently has broader model
evidence than PD**, though PD's effect is roughly three times larger and is the
one coordinate whose direction follows from its definition.

## Design

For each of 40 agents, two arms:

```
PD-    the agent's drawn profile with PD pinned to 0.10   (outcome-dominant)
PD+    the agent's drawn profile with PD pinned to 0.90   (process-dominant)
```

Nine other coordinates drawn once per agent and held **identical** between arms.
System prompts differ by exactly one line; user text byte-identical. Paired
within agent and item.

**Model:** `claude-haiku-4-5-20251001`.
**Items:** haiku's six dispersing items (`phase4b_profiled_pool`).

## The prediction is ONE-SIDED, and its premise is re-verified here

This is the difference from `id_crossmodel_r1`, which had to be two-sided because
ID has no theory mapping onto these items.

**PD+ produces a HIGHER share of `good` decisions than PD−.**

The derivation: PD is defined 0 = outcome-dominant, 1 = process-dominant; every
item presents a claim under a stated arrangement; the option that **keeps** the
arrangement classifies `good`. That last step is a property of the *item set*,
not of the coordinate, so it does not automatically transfer from gpt's seven
items to haiku's six.

`verify_direction()` re-checks it at build time and **gates `prepare()`**. All six
pass:

| Item | Clean action | Classifies |
|---|---|---|
| `ward_transfer` | `leave_arrangement` | good |
| `weekend_rota` | `keep_saturday` | good |
| `desk_booking` | `keep_desk` | good |
| `tool_library` | `return_press` | good |
| `meeting_room` | `keep_slot` | good |
| `storage_unit` | `keep_lease` | good |

**Only the direction carries over from gpt, never the magnitude.** Importing
+0.346 as an expectation would be the post-hoc move this project keeps refusing.

**A significant effect in the wrong direction is a directional FAILURE**, reported
as such and not rescued by re-reading the test as two-sided afterwards. The
analysis computes both p-values and flags the case explicitly.

## Power — reported across the plausible range, not at one flattering point

**PD's effect size on haiku is unknown and is not assumed to be gpt's.** The
Phase 4B post-hoc correlation for PD on haiku was **+0.089** — near flat. So:

| True effect | Detected |
|---:|---|
| **+0.089** (haiku post-hoc, pessimistic) | **15/20** |
| +0.120 | 16/20 |
| +0.150 | 19/20 |
| +0.200 | 19/20 |
| **+0.346** (gpt's measured effect) | **20/20** |
| 0.000 | **1/20** false positive |

Simulated against haiku's **measured** per-item baselines from
`phase4b_profiled_r1`, 20 seeds — not a uniform effect, the error that killed
`phase4b_sonnet_r1`. Reproduce with `phase5_id_crossmodel_power.py`.

A null is therefore **strong evidence against a gpt-sized effect** and **weak
evidence against a small one**, and will be reported with both numbers.

60 agents was considered and rejected: it buys 20/20 at +0.120 and nothing
elsewhere in the range, for 50% more cost. 40 keeps symmetry with
`id_crossmodel_r1`.

## Decision rule, prespecified

PD is declared to move the outcome on haiku if the pooled **one-sided** p < 0.05
**in the predicted direction** AND the effect points that way in at least **4 of
6 items**. Both required. Verified against synthetic fixtures before collection:
5+/1− passes, 3+/3− fails, wrong-direction flags as a directional failure.

**A null is not re-run with more agents.**

### What each outcome licenses

| Outcome | Reading |
|---|---|
| **Moves, predicted direction** | PD's theory-derived direction holds on a second provider. Licenses *"PD moves the outcome on haiku too"* — **NOT** *"PD is verified cross-model"*, since verification on gpt required the swap control, not run here. |
| **Null** | PD's endpoint effect does not transfer to haiku on this item set. Given the +0.089 post-hoc correlation this is a live possibility, not a surprise. |
| **Opposite direction** | Directional failure of the prospective test on this model. Reported, not reframed. |

## A defect fixed at source rather than rescored again

`coordinate_sweep_r2` and `id_crossmodel_r1` both set `SCREEN_N = 0` and then had
`collect()` derive an empty usable-task list from the absent screen. Every
contrast returned `None`; both needed an offline rescore. The data were intact
both times, but the designation's own analysis was empty.

**This collector fixes it**: `declared_tasks()` supplies the pool's own
`TASK_IDS` whenever the screen is skipped, and `analyse()` falls back to it.
Verified against an empty `usable` list before collection. Carrying the defect a
third time and rescoring again would be knowingly shipping a broken analysis.

## Review is advisory

Under the 16 September amendment. These six items are byte-identical to material
`phase4b_profiled_r1` reviewed and accepted with zero blocking issues before
collecting 631 decisions on them, on this same model. No new participant-visible
text is introduced — only a different pinned coordinate. One review is dispatched
and whatever it returns is recorded.

## Build-time verification, before any call

- `verify_direction()` on all six items — gates `prepare()`.
- `verify_construction()` across all 40 agents — arms differ in the PD line
  alone, nine coordinates identical, arms never identical, **zero coincident
  draws**.
- Per-pair wire check across all **240 agent-item pairs**: exactly two diff
  lines, both the PD line at 0.10 and 0.90, byte-identical user text.
- One-sided statistics verified against synthetic fixtures in both directions.

## Accounting

Ledger before this designation: Claude $20.993885000/$32, OpenAI
$11.093290725/$40. Headroom $11.006. `id_crossmodel_r1`, the same shape, settled
at $1.266 against a $6.433 reservation. Usage estimates, not verified provider
balances.

## What this cannot establish

- **Not that PD is verified on haiku** even if positive — that needs the swap
  control, not run here.
- **Not moral truth or improvement.** Deterministic classification under
  stipulated standards, never read from agent text.
- **Not generalisation.** Six items, 40 agents, one harness, one snapshot.
- **No human validation**; raters remain deferred.
