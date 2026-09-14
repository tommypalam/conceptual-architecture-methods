# pd_gradient_r3: stopped at review (reject)

**Outcome: review_stop. One paid call, zero screen calls, zero participant
decisions.** 14 September 2026. This designation is closed. No replacement is
queued, and none should be prepared without first resolving section 3.

## Result

| Item | Value |
|---|---|
| Verdict | **reject** |
| Calls made | 1 (review) |
| Screen / participant calls | 0 / 0 |
| Cost | $0.001966800 |
| Reservation released | $3.38861325; $3.3866 not charged |
| Release | `abd6183a…` |

Cumulative across the whole PD gradient attempt (r1 + r3): **$0.030834375**.
Cumulative accounting: Claude $7.139674300/$15, OpenAI $1.381413825/$30,
package $31.427294350/$100. These are usage estimates, not wallet balances.

## The review's findings, quoted

1. *"Task labels don't reliably match class rule: several P tasks present a
   materially better outcome as the same action as the procedure (e.g.,
   records_release, permit_sequence), violating the class distinction."*
2. *"Multiple items are recognisable as classic paradigms/counterparts (deadline
   exclusion, inspection backlog, roster notice, grant recheck), risking cueing."*
3. *"Some stems effectively reveal the preferred answer via outcome framing
   (e.g., explicit harms of deviation and benefits of compliance)."*

Limits: *"Could not validate all class assignments independently from the text
alone. Need de-classicized, neutral wording and balanced option framing before
acceptance."*

## Assessment

**Finding 1 is the serious one, and it is accepted.** The r2/r3 neutralisation
was applied to remove evaluative language, and in doing so it weakened the very
property that defines Class P. `permit_sequence` now says only that the work is
deferred seven months and the road "remains in its current condition";
`records_release` says the team "states the dataset informs decisions" within
nine days. Neither any longer establishes that departing from the procedure
produces a materially better outcome. A reader can plausibly conclude that
waiting is both procedurally correct and not worse — which collapses Class P
into Class N and destroys the contrast the study exists to measure.

This is a real design defect, not a reviewer misreading. The r1 → r2 repair
traded one failure mode for another: r1 stated the trade-off too strongly and
cued the answer; r2/r3 stated it so weakly that the class distinction no longer
holds. **The correct fix is not a third round of wording adjustment.** The
trade-off magnitude has to be carried by something other than adjectives —
explicit stipulated quantities on both sides, in the manner of the Phase 4
finite-rule tasks, so that "materially better outcome" is a stated fact rather
than a matter of tone.

**Finding 3 is partly accepted.** Class N stems give base rates showing that
departure causes rework, absence or clawback. That is what makes them aligned
controls, but it does make the answer evident from the stem. The dispersion
pre-screen exists precisely to measure that, and would likely have rejected
those tasks as saturated. The screen never ran, so this remains a prediction.

**Finding 2 is recorded, not accepted.** The six scenarios are original, and
"deadline exclusion" and "inspection backlog" are ordinary administrative
situations rather than classic paradigms. What the reviewer is detecting is the
procedural-justice framing, which cannot be removed without removing the
construct under test. The separately established
[recognition result](../recognition_r1/FINDING_INTERPRETATION.md) — 500/500
identification of structure-preserving variants — indicates that this class of
objection is not repairable by re-skinning, and should be carried as a limit.

## What the two review stops establish

The gates work. Two independent reviews, on two versions of the task set,
stopped the study before the screen and participant stages in both cases. Total
exposure across both attempts was **$0.0308** against a **$3.39** reservation:
the design gate prevented 99.1% of the potential spend.

That is the intended behaviour of a prospective protocol, and it is worth
reporting as such. It is not a scientific result, and it says nothing about
whether the PD gradient generalises.

## What is NOT established

- **The PD finding is untested.** No screen and no participant decision was
  collected in any round. The
  [Phase 5 reanalysis](../../phase5_analysis/reanalysis_20260914/ASSESSMENT.md)
  result stands exactly as recorded: post-hoc, on Phase 2 data, awaiting
  prospective test.
- **No task saturation measurement exists** for these six tasks.
- **No conclusion about task classes, transfer, or the process/outcome axis.**
- Two AI design reviews are not human expert review, and their agreement on
  overlapping findings is not independent confirmation.

## Requirements for any future designation

1. Class P must carry explicit stipulated quantities on both sides of the
   trade-off, so class membership is verifiable from the text without relying on
   evaluative wording. Neither r1's adjectives nor r3's understatement qualifies.
2. Class N must be constructed so the aligned outcome is a stated consequence
   rather than a conclusion the stem argues for, and must still pass the
   dispersion screen.
3. The procedural-justice framing objection should be carried as a stated limit
   rather than chased through further rewrites.
4. Any future round is a new designation with its own review. r1's and r3's
   stops, findings, failed slot and charges are preserved unchanged.

Do not prepare a fourth round as a wording edit. The defect identified in
finding 1 is structural.
