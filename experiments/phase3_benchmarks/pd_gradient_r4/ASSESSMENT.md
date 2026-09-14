# pd_gradient_r4: stopped at review (reject)

**Outcome: review_stop. One paid call, zero screen calls, zero participant
decisions.** 14 September 2026. This designation is closed. **No r5 should be
prepared** — see section 4.

## Result

| Item | Value |
|---|---|
| Verdict | **reject** |
| Calls made | 1 (review) |
| Screen / participant calls | 0 / 0 |
| Cost | $0.002087250 |
| Reservation released | $3.474014775; $3.472 not charged |
| Release | `20a51f75…` |

Cumulative across all PD gradient attempts (r1 + r3 + r4): **$0.032921625**.
Accounting: Claude $7.139674300/$15, OpenAI $1.383501075/$30, package
$31.429248400/$100. Usage estimates, not wallet balances.

## The review's findings, quoted

1. *"Several claimed classes are reversed by the stipulated totals:
   grant_arithmetic, inspection_backlog, roster_publication are N but departing
   yields lower totals; permit_sequence, records_release, tender_award are P but
   following yields lower totals."*
2. *"Tasks are recognisable variants of classic paradigms and directly reveal the
   preferable answer via the stated totals/options."*

Limit: *"No psychological parameter named; otherwise structurally clear."*

## Assessment

**Finding 1 is not accepted. It restates the design specification and labels it
a contradiction.** Class P is *defined* as departing yielding the higher total;
Class N is *defined* as following yielding the higher total. The reviewer's
sentence describes exactly that arrangement and calls it a reversal. The
executable check `verify_classes()` recomputes membership from the same numbers
and passes, and a test confirms it fails when the relation is actually broken.
This finding is a reviewer error, not a design defect.

**Finding 2 is accepted, and it is fatal to this design approach.** The
r4 repair made the trade-off explicit in stipulated quantities so that class
membership would be verifiable. That necessarily makes the higher-total option
visible to the participant as well. The quantities cannot simultaneously be
explicit enough to define the class and implicit enough not to signal an answer.

This is the third distinct failure mode in the same place:

| Round | Trade-off stated as | Failure |
|---|---|---|
| r1 | Evaluative adjectives | Cued the preferred action |
| r3 | Understated facts | Class P collapsed into Class N |
| r4 | Explicit stipulated totals | Reveals the higher-total option directly |

These are not three fixable bugs. They are three positions on one axis, and the
axis has no viable point: **the information that defines the process/outcome
divergence is the same information that tells the participant which option
maximises the outcome.** A design that hides it cannot establish its own class
structure; a design that shows it hands over the answer.

## 4. Why no r5 should be prepared

A fourth wording round would occupy some position on the same axis and fail for
one of the same three reasons. The obstacle is structural, not editorial.

Escaping it requires a different measurement approach, not a different
phrasing — for example, deriving the outcome magnitude from state the agent must
compute rather than from a stated total, or measuring the process/outcome axis
through something other than a forced binary choice between two described
options. Either is a new design, and neither is a revision of this one.

That work is not attempted here, and this designation does not propose it.

## 5. What the four rounds established

**Nothing about the PD gradient.** No screen and no participant decision was
collected in any round. The
[Phase 5 reanalysis](../../phase5_analysis/reanalysis_20260914/ASSESSMENT.md)
result stands exactly as recorded: post-hoc, on Phase 2 data, awaiting a
prospective test that this designation did not deliver.

**A methodological result that is reportable.** Three independent design
reviews, on three versions of a task set, stopped the study before any
collection. Total exposure **$0.032921625** against reservations totalling
**$10.312758**: the gates prevented 99.7% of potential spend, and no saturated or
answer-cueing task set reached a participant.

Two of the six blocking findings across r3 and r4 were reviewer errors, recorded
as such rather than deferred to. The gate is useful without being authoritative,
and its output requires assessment rather than compliance.

**A documented design constraint** for anyone attempting a process/outcome
manipulation in this harness: the trade-off magnitude cannot be made explicit
enough to define the contrast without also revealing the outcome-maximising
option. This constraint is the substantive finding of the r1-r4 sequence and
belongs in the write-up alongside the saturation diagnosis.

## 6. What is NOT established

- No task saturation measurement exists for these six tasks in any round.
- No conclusion about task classes, transfer, or the process/outcome axis.
- Three AI design reviews are not human expert review, their overlapping
  findings are not independent confirmation, and two of their findings were
  wrong.
- The recurring "recognisable as classic paradigms" objection remains recorded
  as a stated limit, consistent with the recognition screen's 500/500
  identification of structure-preserving variants. It was never repaired.

All r1, r3 and r4 stops, findings, the preserved failed slot and all charges
remain unchanged. No parameter, marginal, correlation entry, locked question or
societal axis definition was altered by any round.
