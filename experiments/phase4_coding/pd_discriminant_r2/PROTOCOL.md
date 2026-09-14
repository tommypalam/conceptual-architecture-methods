# pd_discriminant_r2 — welfare tied, so the procedure term can express

**421 calls, worst case $3.737 against an $11.00 ceiling. Hard review gate.**

## What r1 measured

`pd_discriminant_r1` passed its review with zero blocking issues and was stopped
by its own screen: three of four items returned modal share 1.00, and in every
saturated cell the unprofiled model chose the **higher-total** option — holding
where holding paid (+4, +3), overriding where overriding paid (+5). The crossing
worked. Welfare simply dominated at total-differences of 4, 6 and 10 units.

r1's locked prediction is recorded as **untested**, not failed. This designation
is a fresh test, not a continuation.

## What r2 changes: only the magnitudes

Every item is now built so the three simple drives are **tied by construction**:

| Item | Hold (total / worst / best) | Override (total / worst / best) |
|---|---|---|
| `rota_swap` | 1 / −4 / +5 | 1 / −4 / +5 |
| `grant_deadline` | 1 / −4 / +5 | 1 / −4 / +5 |
| `consent_form` | 1 / −4 / +5 | 1 / −4 / +5 |
| `appeal_window` | 1 / −4 / +5 | 1 / −4 / +5 |

- **Welfare-maximisation** is indifferent — totals are equal.
- **Minimax / worst-case avoidance** is indifferent — worst losses are equal.
- **Best-case seeking** is indifferent — best gains are equal.

The remaining asymmetry between the two options is which one keeps the
stipulated procedure. That is the signal PD is supposed to move.

`verify_symmetry()` enforces all three ties at build time.

## An honest correction

An earlier reading held that r1's one dispersing item (`appeal_window`, 0.52)
dispersed because welfare and harm-avoidance conflicted there. **Checked against
the numbers, that is wrong** — welfare and minimax point the same way in all four
r1 items. Why that item dispersed is unexplained. r2 does not rely on the
explanation; its magnitudes come from the tie construction, not from imitating
`appeal_window`.

## Locked prediction

> **PD+ chooses the procedure-holding option more often than PD−, pooled across
> the four items.**

Arms: **U** (unprofiled), **PD−** (0.1), **PD+** (0.9). 40 agents × 2 profiled
arms × 4 items = 320 profiled calls, plus 100 screen. The nine non-PD coordinates
are drawn once per agent and held identical between the profiled arms — verified
to differ by exactly the PD line for all 40 agents, with byte-identical user text.

## Prespecified decision rule

A PD effect is declared only if **both** hold:

1. pooled Holm p < 0.05, **and**
2. the effect points the same direction in ≥ 3 of 4 items.

**Measured error rate, simulated before collection over 8 seeds:**

| Simulated world | Declared a PD effect |
|---|---|
| true PD effect | **8/8** |
| pure compliance (holds 85%, ignores PD) | **1/8** |
| null | **0/8** |

**The compliance false positive is not eliminated and this is stated plainly.**
A chance tilt large enough to reach pooled significance usually shows across
items too, so the consistency requirement does not screen it out. At n = 40 the
combined rule cannot do better. A positive result here is **evidence, not
proof**; replication on fresh agents is the remedy and is not performed in this
designation.

## Failure is a result

If PD− and PD+ do not differ under the rule above, the prospective PD test fails
on this item set and is reported as a failure, not reframed.

## Gates

**Screen gate.** U arm first; any item at modal 1.00 is dropped as saturated. If
fewer than 3 survive, the profiled stage does not run.

**Hard review gate.** New magnitudes are new materials.

## What this cannot establish

- Not a moral claim; deterministic choice counts under stipulated standards.
- Not generalisation: four items, one model, one harness.
- Nothing about the other nine coordinates, held constant rather than tested.
- No human validation.
