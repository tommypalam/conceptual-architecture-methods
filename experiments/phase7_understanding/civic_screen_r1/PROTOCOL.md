# civic_screen_r1 — protocol

**Status: prepared offline.** Steps 2 and 3 of
[SECOND_FAMILY.md](../SECOND_FAMILY.md), the plan for blocker 2 of
[PROJECT_SPLIT.md](../../../docs/PROJECT_SPLIT.md). Exploratory; not part of the
submitted thesis.

## Question

Every result in the paper comes from one schema: a workplace resource, an
incumbent party holding it and saying they want to keep it, payoffs frozen at
`[1, -4]` against `[2, -5]`. A reviewer will say the effect may be a property of
that schema. **This designation asks whether a second schema can be built at
all** — the step at which seventeen earlier wordings died.

## The candidates

Fourteen civic allocations (`phase7_civic_items`, content hash
`d2e5a95d…8cd7`). What changes, and it is the pair that makes this a second
family rather than a redecoration:

- **No incumbent.** Nobody holds the thing yet; these are prospective allocations
  among parties with equal standing, so a "keep what exists" disposition has
  nothing to attach to.
- **A published criterion, not a stated wish.** The expectation is a rule the body
  announced in advance — an order of application, a stated basis, a rota. The
  clean option follows it; the other sets it aside for a better immediate result.

What is held, because relaxing any of it breaks comparability with §5–§6: totals
tied at −3; one clean and one single-violation option; the three-level authoring
criterion, run through the base pool's own expressions; deterministic
classification from the action identifier.

Two family-specific checks were added and pass: no situation carries an incumbent
holder or a stated wish to keep.

**The one-sided direction premise was re-derived on these items, not inherited.**
On all 14 the criterion-following option is the clean one, so PD+ predicts more
`good` decisions. `gate()` re-checks this before any call.

## Run statement (rule 4)

| | |
|---|---|
| Review | 1 call, `claude-sonnet-4-6`, all 14 candidates. **Hard gate** (new material); not re-run |
| Screen | 14 × 24 unprofiled decisions, 12 per presentation order = **336 calls**, `gpt-5.4-mini-2026-03-17`, no profile block |
| Configuration | NEUTRAL on all five axes; no agents drawn |
| Cost | $1.240 reserved worst case; about $0.19 expected |

**337 calls total.**

## Rules fixed before collection

- **Usable** = pooled criterion-following share in [0.10, 0.90] **and** a
  presentation-order gap of at most 0.20. The order condition is
  [ORDER_DEPENDENCE](../ORDER_DEPENDENCE.md) rule 1, and it is what
  `defeasibility_screen_r1` lacked when it passed two items that were following
  position rather than choosing.
- **At least 6 usable** or the designation reports `screen_stop` and the second
  family is not built. Six keeps the project's 4-of-7 consistency rule reachable.
- Every usable candidate is taken; no outcome is consulted in selection.
- Screening is on baseline dispersion only. No candidate is reworded and
  re-screened inside this designation.

The selection rules were exercised offline on synthetic rows: a saturated
candidate and an order-determined candidate were both correctly rejected.

## What no outcome establishes

Anything about PD or any parameter — no profile is rendered. A pass shows only
that enough civic candidates disperse, order-robustly, to carry a profiled study;
that study is the next designation and needs its own authorisation.

**The null reading is already fixed** (`phase7_civic_items.LOCKED_PREDICTION`): if
the profiled study later fails to replicate the effect here, §5 and §6 are
**bounded to the workplace-resource schema** and reported as such.
