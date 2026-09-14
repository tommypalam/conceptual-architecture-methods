# moral_capstone_r2: stopped at review (reject)

**Outcome: review_stop. One paid call, zero participant decisions.**
15 September 2026. Superseded by [r3](../moral_capstone_r3/ASSESSMENT.md).

| Item | Value |
|---|---|
| Verdict | reject |
| Cost | $0.001994850 |

## Findings and disposition

**Finding 5 — accepted, and a real defect.** *"rule_map leaks intended
classifications ('good'/'not_good'), revealing a study hypothesis/answer key."*

The review packet included, for every action, its fixed-standard vector **and its
net-score headline**. That is an answer key: it tells the reviewer which option
the study will score as good before asking whether the item is balanced. r1 sent
the same structure and its reviewer did not catch it; this one did. r3 sends the
stipulated structure only — which standards each option upholds and its net
total — with no classification labels, and the packet allow-list is changed to
enforce it.

**Findings 1-4 — not accepted; contradicted by measurement.** The review states
that `witness_cost` has "no reasonable either-way choice" and that `safety_hold`,
`evidence_seal` and `wage_disclosure` have "one option plainly correct".

Those items had already been answered 25 times each with no profile:

| Task | Unprofiled split | Modal |
|---|---|---:|
| `witness_cost` | state_partially 19 / state_fully 6 | 0.76 |
| `safety_hold` | hold_shipment 18 / ship_as_promised 7 | 0.72 |
| `evidence_seal` | describe_vaguely 23 / break_seal 2 | 0.92 |
| `wage_disclosure` | disclose_both 24 / 1 invalid | 0.96 |

Every item drew both options. `witness_cost` additionally produced a 52-point
arm difference in [r1](../moral_capstone_r1/ASSESSMENT.md) (0.233 to 0.750, Holm
p = 0.0002), which a task with no either-way choice cannot do.

A reviewer reading item text alone cannot see this, which is why r3 supplies the
measured dispersion in the packet as evidence and instructs the reviewer not to
flag an item as one-sided when the measurement shows otherwise. The finding is
recorded as a reviewer error, not deferred to.

Nothing was collected under this designation. Its stop, findings and charge are
preserved unchanged.
