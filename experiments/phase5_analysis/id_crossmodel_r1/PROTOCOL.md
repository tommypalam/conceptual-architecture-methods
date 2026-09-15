# id_crossmodel_r1 — does ID's effect exist outside the calibration model?

**481 calls, worst case $6.433 against a $12.00 ceiling. Review advisory.**

## The gap this closes

`label_semantics_r2` verified **ID** as a label effect: pinned +0.111
(Holm 0.00467), with the same numerals on the inert AW label giving +0.046 (n.s.).
That made ID the second of ten coordinates whose label carries its effect.

**Every ID measurement in this project is `gpt-5.4-mini`.**

| Measurement | ID | Model |
|---|---:|---|
| post-hoc correlation (`integrated_20260916`, E arm) | +0.303 | gpt |
| `coordinate_sweep_r2`, 25 agents, pinned | +0.143 | gpt |
| `label_semantics_r2` TRUE, 40 agents, pinned | +0.111 | gpt |
| `label_semantics_r2` SWAP, same numerals on AW | +0.046 n.s. | gpt |

The **architecture-level** result is already two-provider — `phase4b_profiled_r1`
on haiku (+0.171, Holm 0.000112) and `phase4b_gpt_r2` on gpt (+0.228, Holm ≈ 0).
The **coordinate-level** result is not. This designation tests whether it is.

## Design

For each of 40 agents, two arms:

```
ID-    the agent's drawn profile with ID pinned to 0.10
ID+    the agent's drawn profile with ID pinned to 0.90
```

The nine other coordinates are drawn once per agent and held **identical**
between the arms. The system prompts differ by exactly one line; the user text is
byte-identical. Paired within agent and item.

**Model:** `claude-haiku-4-5-20251001` — the point of the designation.

**Items:** haiku's six dispersing items (`phase4b_profiled_pool`): `ward_transfer`,
`weekend_rota`, `desk_booking`, `tool_library`, `meeting_room`, `storage_unit`.

## The item set is haiku's, and that is a real limitation

These are **not** gpt's seven items. Four overlap; `ward_transfer` is haiku-only;
`on_call` and `rest_break` are gpt-only.

That is forced, not chosen. `haiku_screen_r4` measured six alternative items on
haiku and **all six returned modal share 1.00** — deterministic, unable to show
any arm difference. gpt's `on_call` and `rest_break` were never screened usable
on haiku. Dispatching them would spend on items that cannot move.

So this is **ID tested on haiku's dispersing items**, not a byte-identical
repetition of the gpt designation, and the assessment reports it that way.

## No screen arm

These six were screened on haiku in `phase4b_profiled_r1` (modal shares
0.52–0.96, all usable) and 631 profiled decisions were collected on them there.
Re-screening would confirm rather than establish.

## Endpoints only — a power decision, not a saving

A four-arm TRUE/SWAP design was considered and **rejected on measured power**.
Against haiku's own per-item baselines at 40 agents, the swap design gives
**14/20** at ID's gpt effect versus **16/20** for the two-arm design, because the
Holm family is four times larger.

A TRUE arm that fails leaves the SWAP arms uninterpretable — **exactly what
happened to LL in `label_semantics_r2`**. Running an underpowered swap would
manufacture that outcome by design. This designation asks the prior question
only: does ID move the outcome on haiku at all? A swap control on haiku is the
correct follow-up *if* this succeeds, and is deliberately not run in advance.

## Power, measured before collection, against haiku's own baselines

Simulated over the six items using the **measured** per-item good-rates from
`phase4b_profiled_r1`'s E arm — not a uniform effect. That shortcut is the error
made for `phase4b_sonnet_r1`, which reported 8/8 when the true figure was ≤ 5/10;
that designation was abandoned on the corrected analysis rather than run.

| True effect | Detected |
|---:|---|
| +0.080 | 14/20 |
| **+0.111** (ID's measured gpt effect) | **16/20** |
| +0.143 | 18/20 |
| +0.200 | 19/20 |
| 0.000 | **1/20** false positive |

**16/20 is 80%.** A null from this designation is therefore a **weak null** and
will be reported with that number in the same sentence.

Two of six items sit near a bound in one arm (`tool_library` 0.90 in E,
`storage_unit` 0.04 in U), which compresses the detectable range. **More agents
does not fix that**, which is why 60 agents was not chosen instead.

## Locked prediction

**No direction is predicted. The test is two-sided.**

ID had no theory-derived direction on gpt either — the sweep was two-sided and
its observed sign is descriptive. Importing gpt's sign to set expectations here
would convert a fresh test into a confirmation, which is precisely the post-hoc
move this project keeps refusing.

**Decision rule, prespecified:** ID is declared to move the outcome on haiku if
the pooled paired p < 0.05 **AND** the effect points the same direction in at
least 4 of 6 items. Both required.

**Correction:** there is exactly one primary test, so the pooled p is reported
uncorrected. Per-item tests are Holm-corrected among themselves. Inventing a
family of one would be theatre; hiding that the per-item tests are multiple would
not be.

### What each outcome licenses

| Outcome | Reading |
|---|---|
| **Moves, same sign** | ID's effect is not specific to the calibration model. Licenses *"ID moves the outcome on haiku too"* — **NOT** *"ID is verified cross-model"*, since verification on gpt required a null swap control that this designation does not run. |
| **Null** | ID's effect is specific to the calibration model **at 80% power**. The verified map is "two of ten, on one model" and the paper scopes its coordinate claims to gpt. |
| **Opposite sign** | Reported as measured, not reframed — exactly as LL's sign reversal was. A cross-model sign reversal on a manipulated coordinate would be a stronger version of the LL finding and must not be smoothed. |

**A null is not re-run with more agents.** That is the re-roll this project
forbids. The null stands with its power stated.

## Review is advisory

Under the 16 September amendment. These six items are byte-identical to material
`phase4b_profiled_r1` reviewed and **accepted with zero blocking issues** before
collecting 631 decisions on them, on this same model. This designation introduces
no new participant-visible text — only a different pinned coordinate.

One review is dispatched and whatever it returns is recorded. Re-running a review
to obtain a different verdict remains forbidden and is not done.

## Build-time verification, before any call

Run and passed offline:

- `verify_construction()` across all 40 agents — each agent's two arms differ in
  the ID line alone, nine other coordinates identical, arms never identical.
- A per-pair wire check across all **240 agent-item pairs**: exactly two diff
  lines, both the ID line at 0.10 and 0.90, byte-identical user text, and 9 of 10
  coordinate lines identical.
- Two agents (13 and 17) drew an ID coinciding with a pinned level at rendered
  precision. **Harmless here and verified so**: the drawn ID is overwritten in
  *both* arms, so unlike the AW collision in `label_semantics_r2` it cannot make
  the arms identical. Recorded rather than silently dropped.

## Accounting

Reservation **$6.432751** computed from the actual job list, summing each item's
own byte bound. Anthropic headroom at designation time is $32.00 − $19.728 =
**$12.271**. Prior runs settle near 17% of reservation, so the realistic figure
is **~$1.10**.

Ledger before this designation: Claude $19.728369100/$32, OpenAI
$11.093290725/$40. Usage estimates, not verified provider balances.

## What this cannot establish

- **Not moral truth or improvement.** Deterministic classification under
  stipulated standards, never read from agent text.
- **Not that ID is verified on haiku** even if positive — that needs the swap
  control, not run here.
- **Not generalisation.** Six items, 40 agents, one harness, one snapshot.
- **Not a claim about the other coordinates**, untouched here.
- **No human validation**; raters remain deferred.
