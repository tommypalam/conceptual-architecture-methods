# defeasibility_screen_r1 — assessment

**Review gate PASSED (`accept`, zero blocking issues). Dispersion screen STOPPED
the designation.** 176 calls, 176/176 valid, zero failures, $0.081790.
`claude-sonnet-4-6` review + `gpt-5.4-mini-2026-03-17` screen, 20 September 2026.
Protocol: [PROTOCOL.md](PROTOCOL.md). Programme: [../PROGRAMME.md](../PROGRAMME.md).

**The profiled Stage 3a study does NOT run on these twins.** Two of seven are
usable against a prespecified minimum of four.

## What was measured

25 unprofiled decisions per twin, no profile block, presentation order alternating.
Outcome: share choosing the base item's KEEP option.

| Item | Twin keep | Base keep | Keep listed 1st | Override 1st | Order gap | Verdict |
|---|---:|---:|---:|---:|---:|---|
| desk_booking | 0.84 | 0.52 | 0.85 | 0.83 | **0.01** | **usable** |
| weekend_rota | 0.44 | 0.76 | 0.46 | 0.42 | **0.04** | **usable** |
| on_call | 0.52 | 0.32 | **1.00** | **0.00** | **1.00** | order artefact |
| meeting_room | 0.52 | 0.24 | **1.00** | **0.00** | **1.00** | order artefact |
| storage_unit | 0.00 | 0.40 | 0.00 | 0.00 | 0.00 | saturated |
| tool_library | 0.00 | 0.40 | 0.00 | 0.00 | 0.00 | saturated |
| rest_break | 0.00 | 0.24 | 0.00 | 0.00 | 0.00 | saturated |

## The collector said `screen_pass`. It was wrong, and the rule is at fault

`screen_outcome()` applied the prespecified band [0.10, 0.90] to the POOLED keep
share and returned four usable twins. An order-dependence check run afterwards
shows two of those four are artefacts: on `on_call` and `meeting_room` the model
chose whichever option was printed first, 25 times out of 25 in both directions.
Their 0.52 is the design's alternating order averaging two deterministic
responses, not a contested item.

**The stop is recorded against the corrected count of two.** The recorded
`results.json` keeps `screen_pass` exactly as the frozen collector produced it —
it is not edited — and this assessment supersedes its decision. The usability rule
was underspecified, not misapplied.

**Rule for every future dispersion screen: a twin is usable only if the pooled
share is inside the band AND the keep-share gap between presentation orders is
below 0.20.** Pooled dispersion can be a perfectly order-determined item in
disguise. `pd_endpoint_r2` checked order and found it irrelevant (51.3% first-shown)
so the check lapsed; it does not transfer to new items and must be run on every one.

## Three substantive findings, none of them the one the design wanted

**1. Three twins saturated to unanimous override.** `storage_unit`, `tool_library`
and `rest_break` returned 0.00 keep, 25/25. These are the three whose provenance
clause is most damning: a unit handed over ahead of a waiting list by an
acquaintance; an owner withdrawing a press two weeks inside fixed loan terms; a
worker claiming a second rest slot after taking their own. **A 0.00 baseline cannot
show a downward effect**, which is the direction the PROCESS reading of PD
predicts, so these items are unusable in the direction that matters. The reviewer
anticipated exactly this in its second limit.

**2. Three twins moved the OPPOSITE way: the arrangement is kept MORE when it was
obtained outside the procedure.** desk_booking 0.52 to 0.84, meeting_room 0.24 to
0.52, on_call 0.32 to 0.52. Neither locked reading predicted this and **no
explanation is offered** — the two order-artefact items cannot support one at all,
and desk_booking alone is a single item. The descriptive statement is that adding a
procedure clause raised the keep-rate on three of seven items and lowered it on
four. Anyone wanting a mechanism must test one.

**3. The provenance clause has a large effect on baseline behaviour in both
directions** — +0.32 to −0.40 across the seven. It is not inert wording. That is
worth knowing and is not what was being asked.

## What this costs the programme

**Stage 3a is the critical path and it is now blocked**, not abandoned. It was the
only stage where "respects fair process" and "keeps what exists" come apart, and so
the only stage that could tell whether PD is a status-quo dial — the live worry
raised by [probe_fields_r1](../probe_fields_r1/ASSESSMENT.md), where an invented
"existing arrangements stand" field matched PD's effect.

**Two usable twins cannot carry it.** The project's 4-of-7 item-consistency rule
is unreachable, and a two-item study would be exactly the underpowered design that
produced the Legitimacy Locus mess.

**What a second attempt would need**, and it is a real design problem rather than a
rewording pass:

  - **Milder provenance** on the three saturated items — enough that the procedure
    is unmet, not enough to make override unanimous. The gradient between "name
    written three days early" (0.84 keep) and "given it ahead of the waiting list"
    (0.00) is steep and this screen gives two points on it, not a curve.
  - **Order-robustness by construction** for the two artefact items, which failed
    before any profile was applied and would have failed as base items too.
  - **More items**, since the seven-item pool is exhausted: four of seven twins are
    unusable and authoring new base items is its own screened designation.

That is a bigger undertaking than this designation, needs its own reservation and
review, and should not be attempted as a patch. **Five earlier designs in this
project died at this same gate; this is the sixth.** The gate works, and the
$0.08 it cost to learn this is the point of running it before the $1.70 study.

## What no reading of this establishes

Nothing about PD, Procedural Dependence, or any parameter. No profile was rendered
and no parameter manipulated. No moral label was assigned to any twin option; the
pool's `good` classification was stipulated for the base items and deliberately not
applied here. The three saturated twins are not evidence that the model "recognises
unfair procedure" — an unprofiled model choosing override unanimously is consistent
with many accounts, including simple salience of the added clause.

## Accounting

OpenAI $16.087575 → $16.160016/$40 (screen). Anthropic $22.247448 → $22.256757/$32
(review). Package ≈ $38.417/$100. Usage estimates, not verified provider balances.
