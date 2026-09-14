# capstone_specificity_r1: stopped at review (reject)

**Outcome: review_stop. One paid call, zero participant decisions.**
16 September 2026. Superseded by [r2](../capstone_specificity_r2/ASSESSMENT.md).

| Item | Value |
|---|---|
| Verdict | reject |
| Cost | $0.001498200 |

## Cause: a drafting error in the reviewer instruction

r1 reused the capstone's reviewer prompt, which states *"Each item must be a
conflict in which no option upholds every one of harm avoidance, deception
avoidance, coercion avoidance and unfairness avoidance."*

These three items are **negative controls**. They are built so that exactly one
option upholds all four standards and carries the higher total, and that
one-sidedness is their entire purpose. The reviewer was asked to enforce a
criterion that the design deliberately violates, and applied it correctly:

> *"duplicate_charge/refund_duplicate and ledger_error/correct_entry uphold all
> four standards, so these are not valid conflicts."*

The finding is mine, not the reviewer's. This is the same class of error as
`moral_conflict_screen_b1`, where controls were flagged for having the property
they were built to have.

r2 sends an instruction written for controls: it states that they are negative
controls, that one-sidedness is intended, that they must not be judged as
conflicts, and that an item should be flagged only if **no** option is clearly
correct — the inverse criterion. Each item's kind is also declared in the packet.

Nothing was collected under this designation. Its stop, findings and charge are
preserved unchanged.
