# pd_gradient_r1: stopped at review

**Outcome: review_stop. One paid call, zero screen calls, zero participant
decisions.** 14 September 2026. This designation is closed and is not reopened;
the revision is separately designated `pd_gradient_r2`.

## What happened

The independent design review returned **`revise`**, not `accept`. Under the
protocol's stage gate, a non-accept verdict stops the designation before any
screen or participant call. That gate fired as written.

A harness defect meant the collector also raised on the response before the
verdict could be recorded in `results.json`. Both facts are preserved here.

| Item | Value |
|---|---|
| Calls made | 1 (review) |
| Screen calls | 0 |
| Participant decisions | 0 |
| Cost | $0.028867575, preserved at full reservation |
| Reservation released | $3.4501302; unspent remainder not charged |
| Failed slot | `pd_gradient_r1/review/0` |
| Record | `c396f99f…` in the ledger, immutable |
| Failure log | third entry in `failures.jsonl` |

## The review's findings

Verdict `revise`, three blocking issues, quoted exactly:

1. *"Multiple tasks reveal the preferred action via wording: P tasks say the
   outcome-maximising option is superior; N tasks say both options are same or
   better outcome, making the answer obvious."*
2. *"Several task texts are recognisable classic paradigms or near-paradigms
   (grant, inspection, roster, tender; procedural fairness/justice framing)."*
3. *"Forbidden psychological parameter names appear in the system_example,
   including Procedural Dependence and other axis labels."*

Stated limits: *"Need genuinely neutral phrasing with no outcome hints. Need
less paradigm-recognisable, more bespoke scenarios. Keep class labels and
predicted option hidden from participant-visible text."*

### Assessment of each finding

**Finding 3 is a genuine leak that the local gate missed.** The
`leakage_gate` audits participant-visible task text only. The review packet
additionally contained a rendered `system_example`, which necessarily includes
all ten coordinate names. That example was never shown to a participant, so no
collected data could have been contaminated by it — but the local gate did not
catch it, and the design was described as leak-clean before this review. The
gate was too narrow.

**Finding 1 is partly by construction and partly a real defect.** Class N tasks
state that following the procedure also produces the better outcome; that is
what makes them aligned controls, and it is the property the dispersion screen
exists to measure. The reviewer is nevertheless right that the wording makes the
answer obvious, which would likely have produced a modal share at or near 1.00
and a `screen_stop`. For Class P, phrases such as "substantially stronger on the
merits" and "the best available on the merits" state the trade-off but also
editorialise toward one option. That is a real defect.

**Finding 2 is not accepted as stated.** The six scenarios are original and none
is a decanonised classic benchmark. What the reviewer identifies is the shared
procedural-justice *framing*, which is intrinsic to testing a process/outcome
axis and cannot be removed without removing the construct. It is recorded as a
limit rather than repaired. Note the separate, established result that
structure-preserving domain substitution does not conceal a paradigm from a
frontier model; see the
[recognition finding](../recognition_r1/FINDING_INTERPRETATION.md).

## The harness defect

The shared `parse()` in `code/phase3_recognition_run.py` returns response text
verbatim only when `job["kind"] == "probe"`. Every other kind falls through to a
`{"ratings": [...]}` coding-schema check. Every prior collector tags its jobs
`kind: "probe"`. This collector introduced `"review"`, `"screen"` and
`"participant"` for readability, so the review response — which was well-formed
and parsed correctly by `review_value` — was rejected with
`ValueError: Invalid coding schema`, and the ledger preserved the slot as failed
at full reservation with no retry.

The model's output was not at fault. The write-once and no-retry rules behaved
exactly as specified: the failed slot and its full charge are retained.

## What this cost and what it saved

$0.028867575 spent. The screen and participant stages never launched, so
$3.42 of the reservation was not charged. The review gate did the job it was
designed to do: it stopped a study whose task wording would likely have produced
a saturated screen, before the expensive stages.

## Carried into r2

1. Neutral task wording with the trade-off stated as fact and no evaluative
   comparison; no phrase asserting that one option is superior.
2. A review packet containing no rendered profile block, and a widened leakage
   gate that audits the review packet as well as participant text.
3. `kind: "probe"` on every job, matching the harness contract.
4. Finding 2 recorded as a stated limit, not repaired.

Cumulative accounting after this stop: Claude $7.139674300/$15, OpenAI
$1.379447025/$30, package $31.425194350/$100. These are usage estimates, not
wallet balances. No task, parameter, marginal, correlation entry, locked
question or societal axis definition was changed by this designation, and no
prior result was altered.
