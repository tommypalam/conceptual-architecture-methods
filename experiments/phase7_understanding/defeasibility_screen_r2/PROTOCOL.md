# defeasibility_screen_r2 — protocol

**Status: prepared offline.** A NEW designation on NEW wording.
[defeasibility_screen_r1](../defeasibility_screen_r1/ASSESSMENT.md) stands as
recorded: two usable twins of seven, a screen stop. Programme:
[../PROGRAMME.md](../PROGRAMME.md), Stage 3a. Exploratory; not part of the thesis.

## What changed, and why it is not a re-roll

r1's seven wordings gave a readable gradient. The two twins that stayed contested
describe a **timing or paperwork lapse**; the three that saturated to unanimous
override describe **taking a second share or being favoured by a person**; two were
presentation-order artefacts. The five unusable twins are re-authored under one
rule, enforced in `phase7_defeasibility_items_r2.verify_candidates`:

> Every provenance clause is a lapse in timing or form — the procedure exists and
> the holder's step through it was late or took the wrong form — and nobody else is
> named as passed over or as having done a favour.

Nothing from r1 is re-screened or re-reviewed. `desk_booking` and `weekend_rota`
keep their r1 twins byte for byte and their r1 results (keep 0.84, order gap 0.01;
keep 0.44, gap 0.04). Rewording after an unprofiled dispersion screen is this
project's established practice and selects on baseline dispersion only; no profiled
outcome exists to select on.

**Two candidates per re-authored item** (A: lateness; B: wrong channel), because r1
showed that a designer's sense of a clause's strength does not predict where the
model lands. Candidate content hash
`5cff813d69c3a1509795e1d8e73455d47ae5f7e2173554316f9fd3124985c74f`.

## Run statement

| | |
|---|---|
| Review | 1 call, `claude-sonnet-4-6`, all ten candidates. **Hard gate** (new material). Not re-run. |
| Screen | 10 candidates x 24 unprofiled decisions (12 per presentation order) = 240 calls, `gpt-5.4-mini-2026-03-17`, temperature 1, no profile block |
| Configuration | NEUTRAL on all five axes; no agents drawn, no seed |
| Cost | $0.919 reserved worst case; about $0.11 expected |

## Rules fixed before collection

- **Usable** = pooled keep-share in [0.10, 0.90] **and** keep-share gap between the
  two presentation orders at most 0.20. The second condition is the one r1 lacked;
  see [ORDER_DEPENDENCE.md](../ORDER_DEPENDENCE.md).
- **Selection, per item:** one usable candidate — take it; both — the one whose
  pooled keep-share is nearer 0.50, ties to A; neither — the item has no twin.
- **At least 4 twins in total** (so at least 2 of the 5 re-authored items) or the
  designation reports `screen_stop`.
- The rules were exercised offline on synthetic rows before release: an
  order-determined candidate and a saturated one are both rejected.
- No twin option is morally classified, here or later.

## What no outcome establishes

Anything about PD or any parameter. A pass shows only that enough twins disperse,
order-robustly, to carry the profiled study — which is the next designation and
needs its own authorisation.
