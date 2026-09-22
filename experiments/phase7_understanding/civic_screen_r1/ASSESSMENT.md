# civic_screen_r1 — assessment

**Review gate PASSED (`accept`, zero blocking issues). Screen STOPPED the
designation: 3 usable candidates of 14, against 6 required.**
337 calls, 337/337 valid, zero failures, $0.130501. `claude-sonnet-4-6` review,
`gpt-5.4-mini-2026-03-17` screen, 22 September 2026. Protocol:
[PROTOCOL.md](PROTOCOL.md). Candidate hash `d2e5a95d…8cd7`.

**The second item family is not built.** The paper's single-schema limitation
stands as stated.

## Result

Criterion-following share, 24 unprofiled decisions per candidate, 12 per order:

| Item | Family | Follow | Criterion 1st | Override 1st | Gap | Usable |
|---|---|---:|---:|---:|---:|---|
| kiln_access | property | 0.875 | 0.833 | 0.917 | **0.083** | **yes** |
| grazing_licence | property | 0.583 | 0.583 | 0.583 | **0.000** | **yes** |
| dental_slot | bodily | 0.167 | 0.250 | 0.083 | **0.167** | **yes** |
| market_stall | property | 0.125 | 0.000 | 0.250 | 0.250 | no |
| allotment_plot | allocative | 0.292 | 0.167 | 0.417 | 0.250 | no |
| transport_seat | bodily | 0.333 | 0.667 | 0.000 | 0.667 | no |
| hearing_slot | scheduling | 0.375 | 0.667 | 0.083 | 0.583 | no |
| bursary_award | allocative | 0.583 | 0.167 | **1.000** | 0.833 | no |
| inspection_order | scheduling | 0.583 | 0.917 | 0.250 | 0.667 | no |
| rehab_place | bodily | 0.708 | 0.500 | 0.917 | 0.417 | no |
| clinic_list | allocative | 0.792 | 0.583 | 1.000 | 0.417 | no |
| repair_queue | scheduling | 0.917 | 0.917 | 0.917 | 0.000 | no (band) |
| pitch_booking | allocative | 1.000 | 1.000 | 1.000 | 0.000 | no (band) |
| respite_night | bodily | 0.083 | 0.083 | 0.083 | 0.000 | no (band) |

## The failure is not the one that killed the previous seventeen wordings

| Condition | Passed |
|---|---:|
| Dispersion band [0.10, 0.90] | **11 of 14** |
| Order gap ≤ 0.20 | **6 of 14** |
| **Both** | **3** |

**Eleven of fourteen disperse.** Only three are order-robust. Eight candidates
pass the band and fail on order alone — `bursary_award` swings 0.167 → 1.000
across presentation orders, `inspection_order` 0.917 → 0.250, `transport_seat`
0.667 → 0.000.

This matters for how the result is read. The seventeen wordings of
`defeasibility_screen_r1` and `_r2` died of **saturation**: the model answered
unanimously and there was nothing to measure. These candidates do not saturate.
They are contested, and the contest is settled by which option is printed first.

**Eight of these would have passed the screen rule this project used three days
ago.** `defeasibility_screen_r1` passed 4 of 7 under the band alone and two of
those four were subsequently found to be order artefacts. The order condition of
[ORDER_DEPENDENCE](../ORDER_DEPENDENCE.md) rule 1 is doing exactly the work it
was added for, and it is the reason this designation stops honestly rather than
proceeding to a profiled study on items that are not choosing.

## What this costs the paper

**The single-schema limitation stands.** Every result in §5 and §6 remains from
workplace-resource vignettes with an incumbent holder, a stated wish to keep and
payoffs frozen at one pair. §9 says so and continues to.

**It is not evidence that a second schema is impossible.** Three candidates are
usable, which is a materially better yield than the previous attempts produced,
and the failure mode is now specific and named: civic allocations in this format
are *order-sensitive* rather than saturated. That is a different obstacle from the
one that blocked the defeasibility items, and it is one the authoring can address
— the previous obstacle was not.

## The reviewer's three limits, assessed

The review accepted with zero blocking issues and recorded three limits. Two
describe the design correctly and are intended; one is a real catch.

1. **Shared asymmetric payoff structure.** Describes the design. The totals are
   tied at −3 deliberately so welfare-maximisation, minimax and best-case are
   indifferent by construction; that is what makes the parameter rather than the
   arithmetic operative. Same finding as the `pd_crossmodel_r1` review, same
   answer.
2. **`respite_night`'s rota position confers a prior entitlement**, inconsistent
   with the design note's claim that nobody holds the thing. **This is correct.**
   A carer whose turn the rota has reached does hold something like an incumbent
   claim, which is the property the family was built to remove. The item scored
   0.083 — near-unanimous override — and would have been excluded anyway, but the
   reviewer identified a genuine authoring error, not a stylistic one. Any second
   attempt must screen for implicit incumbency, not merely for the phrases
   `verify_items` forbids.
3. **Unit framing makes consequentialist reasoning salient**, possibly suppressing
   procedural responses. Applies equally to every item in the project including
   the original seven, so it does not distinguish this family; recorded as a
   standing limitation of the harness rather than of these items.

## What a second attempt would need

Not more wordings of the same shape. The diagnosis is specific:

- **Order-robustness must be designed in, not discovered.** Eight candidates were
  contested but position-driven. Whatever makes an option "first" carry the choice
  here is a property of how the two options are phrased relative to one another,
  and authoring did not control it.
- **Implicit incumbency must be screened**, per the reviewer's second limit. A
  rota position, a place in a queue, or an existing application can all confer a
  claim without using any forbidden phrase.
- **The three usable candidates are kept** (`kiln_access`, `grazing_licence`,
  `dental_slot`) and are not re-screened. They are not reworded inside this
  designation and no candidate is dropped or amended after seeing these results.

Whether that attempt is worth about $0.20 is a judgement for the researcher. The
honest position is that this one failed for a reason that can be addressed, which
was not true of the seventeen before it.

## Accounting

OpenAI $22.644443 → **$22.775960**/$40. Anthropic $22.268707 → $22.278... (one
review call). Package ≈ $45.05/$100. Usage estimates, not verified provider
balances.
