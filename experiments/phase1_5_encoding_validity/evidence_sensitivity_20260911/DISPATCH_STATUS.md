# Dispatch status: complete

All 540 planned responses are valid, with zero terminal failures. Recorded
full-rate token estimate $0.650970, under the $4 cap. Combined new-budget estimate
is $1.1531925 of $9. All exact requests/profiles, approval, 540 unique API IDs,
single attempts, source hashes, reservations and raw ZIP bytes are verified.
No calls remain running and no automatic expansion is scheduled.
See [the report](analysis/SENSITIVITY_REPORT.md) and [interpretation](analysis/INTERPRETATION.md).

The researcher replied **"Approve 540 calls, $4 cap"** to the exact request.
The reply is saved in [dispatch_approved.json](dispatch_approved.json) against
the frozen design and message hashes. The unchanged launch passed automatic
review on resubmission and collection began.

## Preserved initial rejection

The frozen design is
`ce4176c96a31d7ad9d9cf29a5e6c0cf45cc87bca9ed3c2358acffcbe9fdd4651`.

The initial launch was rejected by automatic approval review before process
creation. No paid calls or dispatch reservations were made. The reviewer
required explicit approval of the new research payload, 540 calls and $4 cap;
the general "go for it" instruction did not meet that requirement.

A concrete approval request has been sent for [these exact messages](request_preview.json),
with the complete allocation and $4 maximum within the existing $9 allowance.
Two offline tests passed, including full mock collection/resume and failure
preservation. Original sources and meanings remain intact.

The exact reply was preserved in a separate design-linked record before
resubmitting the same launch. The preparatory authorization.json does not claim
an exact-message human signature and does not override the review rejection.
