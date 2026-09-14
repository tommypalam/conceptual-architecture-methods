# pd_discriminant_r1 — prospective PD test on crossed no-clean-hands dilemmas

**421 calls, worst case $3.737 against an $11.00 ceiling. Hard review gate.**

## The question

Not *do profiles change decisions* — that has evidence. The question is whether
the **intended concept** explains **which** decisions change.

PD's dominance on S2/S3 was a post-hoc discovery in the Phase 5 reanalysis,
explicitly flagged as requiring prospective test before any confirmatory
language. Five prior designs failed to build that test, each foundering on the
same constraint: stating a process/outcome trade-off explicitly enough to define
the contrast also reveals the answer.

**These items solve that.** No trade-off is stated. Both options set aside
something binding, so the responder must reveal a ranking to answer at all.

## Design

Four items crossing **procedure-respect × outcome direction**:

| Item | Procedure | Hold total | Override total | Procedure |
|---|---|---:|---:|---|
| `rota_swap` | published rotation | +4 | −2 | **helps** |
| `consent_form` | approved re-consent | +3 | −1 | **helps** |
| `grant_deadline` | stated closing time | −5 | +5 | **harms** |
| `appeal_window` | stated appeal window | −5 | +5 | **harms** |

Three arms: **U** (unprofiled), **PD−** (PD = 0.1), **PD+** (PD = 0.9).
40 agents × 2 profiled arms × 4 items = 320 profiled calls, plus 100 screen.

**The nine non-PD coordinates are drawn once per agent and held identical
between PD− and PD+.** Verified: the two system prompts differ by exactly two
lines — `Procedural Dependence: 0.10` versus `0.90` — for all 40 agents.

## Locked prediction

Fixed in `phase4_pd_discriminant_tasks.LOCKED_PREDICTION` before any call:

> **PD+ chooses the procedure-holding option more often than PD−, in BOTH the
> helps-cell and the harms-cell.**

**Primary test: the harms-cell, Holm-corrected.** There, holding costs 10
stipulated units and does *more* third-party harm.

## Why this discriminates

| Account | helps | harms | PD− vs PD+ difference? |
|---|---|---|---|
| **PD (process-dominant)** | hold | **hold** | **yes** |
| welfare-maximisation | hold | override | no — constant across arms |
| prosociality | hold | override | no — constant across arms |
| harm-avoidance | hold | override | no — constant across arms |
| generic compliance | hold | hold | no — both arms equally instructed |

Every competing account is **constant across the two profiled arms**, because
the arms differ only in one number. A PD+ shift toward holding in the harms-cell
cannot be produced by any of them. Generic compliance predicts holding in both
cells but predicts **no PD−/PD+ difference**.

## Failure is a result

If PD− and PD+ do not differ in the harms-cell, **the prospective PD test fails
on this item set and is reported as a failure, not reframed.** This is stated in
`LOCKED_PREDICTION.failure_condition` before collection.

## Gates

**Screen gate.** The U arm runs first. Any item at modal share 1.00 is dropped as
saturated. If fewer than 3 items survive, the profiled stage does not run and the
designation reports the screen and stops.

**Hard review gate.** New items, so the advisory amendment does not apply. The
reviewer prompt asks explicitly whether either option's description **or
consequence text** labels it with a norm violation its pair does not carry — the
criterion that stopped `breadth_focus_r1` and `closeout_r1`.

## Authoring criterion, enforced at build time

From `closeout_r1`: paired options must match in the **presence and weight** of
non-unit text, not merely avoid evaluative vocabulary. `verify_symmetry()`
enforces:

- both options violate a fixed standard (no clean exit);
- **equal violation counts** — caught `rota_swap` carrying 2 against 1 before
  collection;
- exactly one closing sentence per option, parallel in form, within 3 words in
  length, neither characterising the act as improper;
- balanced crossing (2 helps, 2 harms), with declared direction matching computed
  totals.

## What this cannot establish

- **Not a moral claim.** Deterministic choice counts under stipulated standards;
  no moral label is assigned and no moral quality measured.
- **Not generalisation.** Four items, one model, one harness. Repeated responses
  on a handful of dilemmas are limited evidence about generalisation, and more
  calls do not substitute for more independent situations.
- **Not a claim about the other nine coordinates**, which are held constant
  rather than tested.
- **Not human-validated**; human raters remain deferred.

## Verification before collection

- `verify_symmetry()` passes on all four items.
- Leakage audit: zero hits.
- PD− and PD+ system prompts differ by exactly the PD line, all 40 agents; user
  text byte-identical.
- U arm carries no profile block.
- Full 421-call schedule simulated against a fake responder: 421/421 parsed.
- **Analysis validated against three simulated worlds**, 6 seeds each:
  a true PD effect is detected in the harms-cell in **6/6** seeds; a pure
  welfare-drive world yields **0/6**; a null world yields **0/6**. Holm
  correction over a 6-member family was added after an uncorrected null run
  produced a spurious p = 0.014.
