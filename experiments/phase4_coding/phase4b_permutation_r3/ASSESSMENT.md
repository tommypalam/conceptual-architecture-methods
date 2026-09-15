# phase4b_permutation_r3: stopped at review, and the stop is the finding

**Outcome: stopped at the hard gate. One review call, $0.007863, zero probes.**
16 September 2026. Verdict **revise**.

Ledger after this designation: Claude $19.684017100/$32, OpenAI $5.497067400/$30.
Usage estimates, not wallet balances.

## What happened

r3 re-powered the permutation control on the effect r2 actually measured:
120 agents, 840 paired decisions, 16/16 simulated power at a gap of 0.089
against r2's 5/16. Items, arms, derangement, analysis and decision rule were
unchanged and already validated.

The review returned **`revise`**, blocking on `on_call` and `rest_break`:

> "ASSIGN_ON_CALL forces someone off an approved rest rotation; REASSIGN_REST
> reassigns a 'mandatory rest slot' to a different worker… Both option labels
> carry an implicit norm violation (overriding a protected entitlement) that the
> paired option does not."

**`phase4b_permutation_r2` reviewed the byte-identical seven-item packet and
returned `accept` with zero blocking issues**, explicitly calling `rest_break`
"a limit rather than a blocker" and describing the set as "structurally parallel
and balanced".

## The review record on identical materials

| Designation | Packet | Verdict | Finding |
|---|---|---|---|
| `phase4b_grand_r1` | 12 items | **accept** | zero blocking |
| `phase4b_screen_r2` | 12 items | **accept** | zero blocking |
| `phase4b_gpt_r1` | 8 items | revise | `sample_draw`, `on_call`, `rest_break` |
| `phase4b_gpt_r2` | 8 items, advisory | revise | inherited and recorded |
| `phase4b_permutation_r1` | 8 items | revise | **`sample_draw` alone**; explicitly cleared the other seven |
| `phase4b_permutation_r2` | **7 items** | **accept** | zero blocking; `rest_break` a limit, not a blocker |
| `phase4b_permutation_r3` | **7 items** | revise | **`on_call` + `rest_break`** — the two r2 cleared |

r2 and r3 saw the same seven items, the same text, the same reviewer prompt. One
accepted with zero blocking issues; the other blocked on two items the first had
named and dismissed.

## Why I stopped rather than proceeding

The 16 September amendment would permit continuing: these seven items were
reviewed and accepted by `phase4b_permutation_r2`, so a later review of the same
materials is advisory.

**Invoking it here would be selective.** `permutation_r1`'s reject is exactly
what caused `sample_draw` to be dropped and r2 to exist. Treating a reject as
binding when it produces a change I agree with, and as advisory when it blocks a
result I want, is not a rule — it is a preference wearing a rule's clothing.

The amendment's own text forbids the adjacent move: *"Re-running a review to
obtain a different verdict on the same materials remains forbidden."* Proceeding
after r2's accept and r3's reject would not be re-running, but it would be
selecting between two verdicts on identical materials on the basis of which one
lets the study run.

**The permutation question stays open, and r2's null stands as the answer of
record.**

## What this establishes

**A controlled demonstration of review-instrument instability.** The amendment
was written from evidence across *different* designations on shared material.
This is the tighter case: two designations, identical packets, identical prompts,
opposite verdicts, days apart. That is a concrete measurement of how far an AI
design review can be trusted as a gate, and it belongs in the methods section
rather than in a footnote.

**The three-level authoring criterion is not the issue.** All seven items pass
every level — no violation label, no asymmetric modal, no closing sentence on
either option. Both objections concern **world knowledge**: that a mandatory rest
slot or an approved rota carries real-world normative weight the stipulated units
cannot neutralise. That objection is partly correct, applies to every moral
dilemma in the project, and is already recorded as a design-level caveat.

## What this does NOT establish

- **Nothing new about the permutation question.** Zero probes. `r2`'s result —
  E−P +0.089, pooled Holm 0.084, rule not met — remains the state of the
  evidence, with its own power limitation intact.
- **Not that the flagged items are defective.** Two reviewers cleared them and
  two flagged them. The disagreement is the datum.
- **Not a reason to doubt any collected result.** `phase4b_profiled_r1`,
  `phase4b_gpt_r2` and `phase4b_permutation_r2` are untouched.

## Where this leaves the caveat

**The Phase 4B caveat stands and should be published standing.** The best
available evidence on it is r2's:

| Arm | Good-rate | vs U | p |
|---|---:|---:|---:|
| U no block | 0.400 | — | — |
| P scrambled labels | 0.475 | +0.075 | 0.122 |
| E correct labels | 0.564 | **+0.164** | **0.00074** |

A scrambled block does not clear baseline; a correctly-labelled one does; the
difference between them is +0.089 and fails correction at n = 280.

The honest statement for the paper is that the effect **appears split** between
block-presence and label-mapping, and that resolving the split requires ~840
pairs which this project attempted and could not gate through.

## What a future attempt needs

Not more power — r3 had it, at 16/16. **A review protocol that does not flip on
identical materials.** Options, none authorised here:

1. Multiple independent reviews with a declared aggregation rule fixed in
   advance, so a single draw cannot gate a study.
2. A human adjudicator for blocking issues, which the 13 September no-budget
   instruction currently defers.
3. Items rebuilt to carry no real-world entitlement at all — which may not be
   possible while remaining moral dilemmas, and is itself the open question both
   objections point at.

## Provenance

One review call, $0.007863, dispatched and recorded. The verdict stands as
returned and **was not re-run**. No probes were collected, no frozen source
edited, and the two inherited failures remain preserved and unretried.

The control was verified exact across all 120 agents before the review: identical
user turns, identical system-prompt length, identical multiset of rendered
numerals, E ≠ P for every agent, a 10-cycle derangement with no fixed point, and
zero agents with tied values. That verification is retained for any future
attempt.
