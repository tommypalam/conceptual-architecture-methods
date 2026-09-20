# defeasibility_screen_r2 — assessment

**Review gate PASSED (`accept`, zero blocking issues). Screen STOPPED: none of the
ten re-authored candidates is usable.** 241 calls, 241/241 valid, zero failures,
about $0.11 (OpenAI $16.160016 → $16.259575; Anthropic $22.256757 → $22.268707).
20 September 2026. Protocol: [PROTOCOL.md](PROTOCOL.md).

The twin set stays at the two carried from r1. **A two-directional profiled study
on twins does not run.**

## Result

| Candidate | Keep | Keep shown 1st | Override 1st | Order gap | Fails on |
|---|---:|---:|---:|---:|---|
| storage_unit/A (form a week late) | 0.21 | 0.42 | 0.00 | 0.42 | order |
| storage_unit/B (agreed by phone, unsigned) | **0.00** | 0.00 | 0.00 | 0.00 | floor |
| tool_library/A (4 days' notice of 14) | **0.00** | 0.00 | 0.00 | 0.00 | floor |
| tool_library/B (notice spoken, not written) | 0.04 | 0.08 | 0.00 | 0.08 | floor |
| rest_break/A (name up an hour late) | 0.04 | 0.08 | 0.00 | 0.08 | floor |
| rest_break/B (asked in person, board unsigned) | **0.00** | 0.00 | 0.00 | 0.00 | floor |
| on_call/A (swap logged late) | 0.75 | 0.92 | 0.58 | 0.33 | order |
| on_call/B (one signature of two) | 0.38 | 0.75 | 0.00 | 0.75 | order |
| meeting_room/A (form a week late) | 0.17 | 0.33 | 0.00 | 0.33 | order |
| meeting_room/B (email, no form) | 0.83 | 1.00 | 0.67 | 0.33 | order |

## What it shows

**1. Milder wording did not lift the floor. That is the finding.** On
`storage_unit`, `tool_library` and `rest_break` the unprofiled model keeps the
arrangement 24–40% of the time when nothing is said about how it arose, and
**0–4% of the time once ANY lapse is mentioned** — a form a week late, notice given
aloud, a name on the board an hour after the cut-off. Eleven wordings across two
designations, from blatant to trivial, all land on the floor. The r1 hypothesis
that blatancy caused the saturation is **refuted**: on these items the unprofiled
model treats a procedural lapse by the holder as close to decisive, however small.

**2. The order rule was too strict for its sample, and it is NOT relaxed.** With 12
decisions per order the standard error of a gap is about 0.18, so a 0.20 ceiling
rejects items that may be order-robust: three candidates failed at a gap of exactly
0.33. Under a looser ceiling `on_call/A` and `meeting_room/B` would have passed and
the twin set would have reached four. **The rule was fixed before collection and
is applied as written.** Loosening it now, knowing which candidates it admits,
would be selection after the fact. The error is in the design of the screen (too
few decisions per order for the threshold chosen) and is recorded as mine.

**3. The review accepted again**, with three limits: the shared payoff structure
(deliberate — totals are tied so welfare rules are indifferent), that paired
wordings could reveal the hypothesis (not applicable: each call sees one item
once), and that `rest_break` may trigger labour-law intuitions the credit
stipulation does not control — a fair point, and consistent with that item sitting
on the floor in every version.

## What this does to Stage 3a

The two-directional design is dead on this item pool: three sessions of authoring
have produced two usable twins. **It is not pursued further.**

But the floor itself suggests a different, one-directional test, in this project's
own words: a deterministic baseline makes detection one-directional, not
impossible. On a twin sitting at 0.00 keep, the two readings of PD still differ:

    DIAL      "PD high -> keep what exists": raising PD should LIFT the keep-rate
              off the floor, as raising Status-quo Preference should
    PROCESS   a process-dominant agent has no reason to protect an arrangement
              that went around its process: the keep-rate STAYS on the floor

Status-quo Preference is the positive control that the floor can be lifted at all.
And the three floored items are exactly the three where PD's effect on the BASE
item is largest (`rest_break` +0.800, `tool_library` +0.675, `storage_unit` +0.400
in `semantics_r1`). If PD moves those base items by that much and leaves their
twins on the floor while Status-quo Preference lifts them, **PD is not a status-quo
dial**. If PD lifts the twins as it lifts the bases, it is one. Both outcomes are
informative; only "neither field lifts the twins" is not.

That is a separate designation on the r1 twins (already reviewed and accepted),
with its own protocol and authorisation.

## What this does not establish

Anything about PD or any parameter; no profile was rendered. That the model
"understands procedure": an unprofiled floor is consistent with simple salience of
the added clause. No twin option is morally classified.

## Accounting

OpenAI $16.259575/$40. Anthropic $22.268707/$32. Package ≈ $38.528/$100. Usage
estimates, not verified provider balances.
