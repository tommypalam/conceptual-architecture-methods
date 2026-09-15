# id_crossmodel_r1: ID replicates on a second provider

**Outcome: complete. 481 calls, 480/480 valid, zero failures.**
18 September 2026. Review **accept**, zero blocking issues. Cost $1.265516
against a $6.433 reservation.

Ledger after this designation: Claude $20.993885000/$32, OpenAI $11.093290725/$40.
Usage estimates, not wallet balances.

**ID moves the deterministic good/bad headline on `claude-haiku-4-5`, in the same
direction as on the calibration model.** ID becomes the first coordinate in this
project with manipulated evidence on two providers.

## Result

| Arm | Good-rate | n |
|---|---:|---:|
| ID− (0.10) | 0.604 | 240 |
| **ID+ (0.90)** | **0.679** | 240 |

**Paired +0.075, p = 0.0328, 240 pairs, 64 discordant, 4 of 6 items positive.**
Both conditions of the prespecified two-sided rule met.

| Item | Effect | raw p | Holm |
|---|---:|---:|---:|
| **`desk_booking`** | **+0.225** | **0.0039** | **0.0234** |
| `storage_unit` | +0.175 | 0.143 | 0.574 |
| `weekend_rota` | +0.125 | 0.0625 | 0.313 |
| `tool_library` | +0.075 | 0.250 | 0.574 |
| `ward_transfer` | −0.025 | 1.000 | 1.000 |
| `meeting_room` | −0.125 | 0.180 | 0.574 |

One item survives Holm individually. The pooled contrast is the primary test and
the per-item tests are corrected among themselves; there is exactly one primary,
so it is reported uncorrected rather than given a fabricated family of one.

## ID across five measurements on two providers

| Measurement | Model | Effect |
|---|---|---:|
| post-hoc correlation (`integrated_20260916`, E arm) | gpt | +0.303 |
| `coordinate_sweep_r2`, 25 agents, pinned | gpt | +0.143 |
| `label_semantics_r2` TRUE, 40 agents, pinned | gpt | +0.111 |
| `label_semantics_r2` SWAP, same numerals on AW | gpt | +0.046 n.s. |
| **this designation, 40 agents, pinned** | **haiku** | **+0.075** |

**Same sign in all five**, four of them manipulations rather than correlations.

Set against LL, which was withdrawn two days ago: +0.271 post-hoc, −0.131 pinned
at 25 agents, −0.014 at 40 — three different answers on one model. ID's
consistency across a provider boundary is the contrast that makes the withdrawal
of LL look like a discriminating test rather than an accident.

## The effect is smaller on haiku, and that is stated rather than smoothed

**+0.075 against gpt's +0.111** — roughly two-thirds the magnitude, on a
partially different item set, clearing p < 0.05 without much room to spare.

**What replicated is the direction and the decision rule, not the magnitude.**
Nothing here licenses a claim that ID's effect size is stable across models.

## What this establishes

**ID's effect is not an artefact of the calibration model.** Every prior ID
measurement was `gpt-5.4-mini`; the coordinate-level claim now has evidence from
a second provider under the same pinning manipulation.

**It removes the sharpest scoping limitation on the coordinate result.** Before
this designation the verified map was "two of ten coordinates are label effects,
measured on one model". ID is no longer in that position.

## What this does NOT establish

- **NOT that ID is verified cross-model.** Verification on gpt required the
  numeral-identical swap control from `label_semantics_r2`, which shows the
  effect belongs to the *label* rather than to numeric extremity. **No swap
  control was run on haiku.** This designation licenses *"ID moves the outcome on
  haiku too"* and nothing stronger. The four-arm swap design was considered and
  rejected on measured power (14/20 against 16/20, because its Holm family is
  four times larger); an underpowered TRUE arm would have made the SWAP arms
  uninterpretable by construction, which is exactly what happened to LL.
- **Not the same item set as the gpt designation.** Four of six items overlap.
  `ward_transfer` is haiku-only; `on_call` and `rest_break` are gpt-only. That is
  forced rather than chosen: `haiku_screen_r4` measured six alternative items at
  modal share **1.00** — fully deterministic and unable to show any arm
  difference. This is ID tested on haiku's dispersing items.
- **Not a directional confirmation.** ID has no theory mapping onto these items,
  so the test was two-sided on both models and the shared sign is descriptive.
- **Not moral truth or improvement.** Deterministic classification under
  stipulated standards, computed from stipulated transitions, never read from
  agent text.
- **Not that ID is understood as a concept.**
- **Not generalisation.** Six items, 40 agents, one harness, one snapshot.
- **No human validation**; raters remain deferred.

## A defect that shipped twice

The designation collected all 480 decisions successfully and then produced an
**empty analysis**: `n = 0` in both arms, pooled contrast `None`.

**The cause is identical to `coordinate_sweep_r2`'s.** This designation drops the
U screen arm (`SCREEN_N = 0`), but `collect()` derives its task list from the
screen — `usable = [t for t, v in screen.items() if v["usable"]]`. With no screen
probes `usable` is empty and every contrast filters to nothing.

**That defect had already been diagnosed and written up** in
`code/phase5_sweep_rescore.py` two days earlier. This collector was adapted from
the one containing it and inherited it unfixed: the symptom was corrected there
with a rescore module and the lesson was not carried into the next collector
built on it.

**Nothing is wrong with the data**: 480 decisions, 240 per arm, 80 per item
across six items, 40 agents, zero invalid. Rescored offline in
`code/phase5_id_crossmodel_rescore.py`, which uses the designation's own declared
item set (`phase4b_profiled_pool.TASK_IDS` — the six the protocol names and the
review accepted), not a list chosen after seeing results. Zero API calls; results
in `rescored.json`. The collector is hash-pinned by its release and was not
edited.

**The fix now exists at source.** `pd_crossmodel_r1` carries a `declared_tasks()`
fallback and was verified against an empty `usable` list before collection.
Rescoring a third time would have been knowingly shipping a broken analysis.

## Provenance

Review returned **accept**, zero blocking issues. Advisory under the 16 September
amendment: these six items are byte-identical to material `phase4b_profiled_r1`
reviewed and accepted before collecting 631 decisions on them, on this same
model. One review was dispatched and its verdict recorded; no re-roll.

Build-time checks before any call: `verify_construction()` across all 40 agents,
and a per-pair wire check across all **240 agent-item pairs** confirming exactly
two diff lines — both the ID line at 0.10 and 0.90 — byte-identical user text,
and nine of ten coordinate lines identical.

Two agents (13 and 17) drew an ID coinciding with a pinned level at rendered
precision. **Verified harmless**: the drawn ID is overwritten in *both* arms, so
unlike the AW collision that forced a reseed in `label_semantics_r2` it cannot
make the arms identical. Recorded rather than silently dropped.

Power measured before collection against haiku's **measured** per-item baselines
from `phase4b_profiled_r1` — not a uniform effect, the error that caused
`phase4b_sonnet_r1` to report 8/8 when the true figure was ≤5/10. 20 seeds:
16/20 at ID's gpt effect of +0.111, 18/20 at +0.143, **1/20 false positive at
zero**. Reproducible via `code/phase5_id_crossmodel_power.py`.

481 calls dispatched, 480 valid, zero entries in `failures.jsonl` for this
designation. Failures from earlier designations remain preserved and unretried.
