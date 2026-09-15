# coordinate_sweep_r2: three of ten coordinates are load-bearing

**Outcome: complete. 2,801 calls, 2,800/2,800 decisions valid, zero failures.**
17 September 2026. Review **accept**, zero blocking issues. Cost $2.069183
against a $31.517 reservation.

Ledger after this designation: Claude $19.719300700/$32, OpenAI $9.446089125/$40.
Usage estimates, not wallet balances.

## Result

Each coordinate pinned to 0.1 and 0.9 with the other nine drawn and held
identical, 25 agents × 7 items, Holm-corrected over all eight contrasts as one
family.

| Coordinate | Effect | Pairs | raw p | **Holm** | Items | Load-bearing |
|---|---:|---:|---:|---:|---|---|
| **ID** Internalisation Dependence | **+0.143** | 175 | 0.000070 | **0.00056** | 6+/1− | **YES** |
| **LL** Legitimacy Locus | **−0.131** | 175 | 0.000117 | **0.00082** | **0+/6−** | **YES** |
| TfA Tolerance for Asymmetry | −0.103 | 175 | 0.0222 | 0.111 | 2+/5− | no |
| MoR Mode of Response | −0.097 | 175 | 0.0115 | 0.069 | 1+/6− | no |
| MS Moral Scope | −0.069 | 175 | 0.0730 | 0.292 | 2+/5− | no |
| RE Relational Embedding | +0.046 | 175 | 0.302 | 0.906 | 4+/2− | no |
| RT Response Threshold | −0.023 | 175 | 0.572 | 1.000 | 3+/3− | no |
| CS Constraint Sensitivity | −0.017 | 175 | 0.749 | 1.000 | 3+/3− | no |

With the two already tested in `label_semantics_r1` at 40 agents:

| Coordinate | Effect | Holm | Verdict |
|---|---:|---:|---|
| **PD** Procedural Dependence | **+0.339** | ≈ 0 | **load-bearing** |
| AW Affective Weighting | −0.036 | 1.000 | inert |

**Three of ten are load-bearing: PD, ID, LL. Seven are not.**

## What each survivor looks like

**PD +0.339** — by far the largest, and the only one with a direction predicted
from theory before collection. Six of seven items positive.

**ID +0.143** — Internalisation Dependence, 0 = surface compliance sufficient,
1 = requires genuine endorsement. Six of seven items positive, strongest on
`storage_unit` and `on_call` (+0.280 each).

**LL −0.131** — Legitimacy Locus, 0 = external/institutional warrant,
1 = internal endorsement. **Negative in 6 of 6 items with any effect and zero
positive** — the most directionally consistent result in the sweep. Higher
internal endorsement produces *fewer* `good` classifications on these items.

## A finding about method, not just coordinates

**LL's post-hoc correlation and its manipulated effect have opposite signs.**

| Source | LL |
|---|---:|
| Phase 5 integrated analysis, post-hoc on the E arm (`gpt_r2`) | **+0.271** |
| This sweep, LL pinned to endpoints | **−0.131** |

ID agrees in sign (+0.303 post-hoc, +0.143 manipulated); **LL reverses**.

That is a concrete demonstration of why the Phase 2 reanalysis insisted a
post-hoc coordinate finding needs prospective test before confirmatory language.
On unmanipulated coordinates that vary together by draw, a correlation can point
the wrong way. Here one did.

## What this establishes

**A map of which coordinates carry the behaviour**, by a method validated in two
steps: `pd_prospective_r1` showed pinning PD moves the outcome, and
`label_semantics_r1` showed the effect belongs to the PD *label* rather than to
numeric extremity.

**Seven coordinates are not load-bearing on this item set.** That is a
Holm-corrected null across eight contrasts at adequate power (24/24 simulated at
d ≥ 0.20, 0/24 false positives), not an absence of evidence. TfA and MoR sit
just outside correction and would be the first candidates for a larger n.

**PD remains dominant by a wide margin** — +0.339 against ID's +0.143 and LL's
−0.131, roughly 2.4× the next largest.

## What this does NOT establish

- **Not that ID's or LL's LABEL carries their effect.** This shows pinning the
  coordinate moves the outcome. Proving the label carries it rather than the
  numeral needs the swap control `label_semantics_r1` ran for PD. **That is the
  required follow-up for both survivors and has not been run.** Until it is, ID
  and LL are load-bearing *coordinates*, not demonstrated *label* effects.
- **Not moral truth or improvement.** Every label is a deterministic
  classification under stipulated standards, computed from stipulated
  transitions, never read from agent text.
- **Not a direction predicted in advance.** Unlike PD, neither ID nor LL had a
  theory mapping onto these items, so the test was two-sided and the observed
  signs are descriptive, not confirmed predictions.
- **Not cross-model.** `gpt-5.4-mini` only.
- **Not generalisation.** Seven items, 25 agents, one harness, one snapshot.
- **Not a claim that the seven nulls are inert in general** — only that they do
  not move this outcome on this item set at this n.
- **No human validation**; raters remain deferred.

## A correction: the collector's analysis was empty and was rescored offline

`coordinate_sweep_r2` collected all 2,800 decisions successfully and then
produced an **empty analysis**: every contrast `None`, Holm family size 0.

**The cause.** This designation drops the U screen arm (`SCREEN_N = 0`), because
its seven items had been screened four times on gpt with consistent results. But
`collect()` derives its task list from the screen — `usable = [t for t, v in
screen.items() if v["usable"]]`. With no screen probes, `usable` was empty and
`analyse()` filtered every contrast to an empty task list.

**Nothing is wrong with the data**: 2,800 decisions, 175 per arm across 16 arms,
400 per item across seven items, zero failures.

The correction lives in `code/phase5_sweep_rescore.py` rather than in the
collector, which is hash-pinned by its release — editing it in place would break
`verify()` for every designation inheriting from it, exactly as an earlier
in-place edit did for `phase4_capstone_specificity_r2`.

**The rescore uses the designation's own declared item set** (`phase4b_perm_pool.TASK_IDS`
— the seven the protocol names and the review accepted), which is the list
`usable` would have held had the screen run. It is not a list chosen after seeing
results. Zero API calls; results in `rescored.json`.

## Provenance

Review returned **accept**, zero blocking issues, three non-blocking limits.

Build-time checks before any call: `verify_sweep()` confirming each coordinate's
two arms differ in that coordinate and nothing else; a per-pair wire check across
all **200 agent-coordinate pairs** confirming the system prompts differ by exactly
two diff lines with byte-identical user text.

This designation continues `coordinate_sweep_r1`, which halted at 689/2,801 on a
network **TimeoutError** — no response received, so nothing was measured. That
slot is **preserved unresolved and never retried**, named as inherited alongside
two earlier failures. r1's 689 calls ($0.55) are preserved as evidence of the
halt and were not reused. The no-retry rule was applied, not reinterpreted.

2,801 calls dispatched, zero entries in `failures.jsonl` for this designation.
