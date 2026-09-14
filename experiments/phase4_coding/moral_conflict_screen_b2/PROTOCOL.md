# Phase 4 moral-conflict dispersion screen, set B: protocol b2

**Revision of b1**, which stopped at review with verdict `reject` for
$0.001318050. Two findings, both addressed:

1. *"one option is plainly correct given the described duties/consent/accuracy
   facts (e.g. refund duplicate charge, correct ledger, respect refusal)."*
   **Not a defect — a drafting error in the reviewer prompt.** Those three items
   are the declared negative controls, and having a plainly correct option is
   precisely their purpose. b1 did not tell the reviewer that controls existed.
   b2 declares each item's kind in the packet and instructs the reviewer to judge
   each against its declared kind, explicitly not flagging a control for having
   an obvious answer.
2. *"Some items embed a clear normative cue or one-sided reason, e.g. 'as the
   published rule provides', 'as the person's stated refusal asks'."*
   **Accepted.** Those clauses restated the duty inside the option description
   rather than leaving it in the situation. They are removed, along with "You
   know which three files contain the irregularities", which is reworded as a
   plain fact of the scenario.

**Screen only.** 15 September 2026. Collects unprofiled decisions on eight new
candidate tasks and reports their baseline dispersion. **No profiled arm, no
moral score.**

## Why set B

An external review of the project identified the binding limitation on the
[capstone result](../moral_capstone_r1/ASSESSMENT.md): it rests on two tasks,
one of which showed no effect, and it would need "more tasks (ideally 4-6, with
some designed as negative controls)" before supporting a general claim.

Set B addresses both halves.

**Wider tension coverage.** Set A's conflicts were concentrated on
deception-vs-harm (three of six tasks), with coercion appearing once. Set B's
five conflict tasks cover coercion in three and unfairness in three, so a result
is not carried by a single kind of dilemma.

| Task | Standards in tension |
|---|---|
| `audit_sampling` | deception, harm, unfairness |
| `shelter_places` | coercion, harm |
| `wage_disclosure` | deception, harm, unfairness |
| `quarantine_notice` | coercion, harm, unfairness |
| `evidence_seal` | coercion, deception, harm |

**Negative controls.** Three tasks (`ledger_error`, `duplicate_charge`,
`expired_stock`) are deliberately built with a dominant option: one choice
upholds every standard and carries the higher total. They are declared as
controls in `CONTROL_IDS` before collection.

Their purpose is specificity. If a later profiled study shifts choices on
controls as much as on conflict tasks, the capstone effect is not specific to
moral conflict and the interpretation is wrong. Controls are **expected to
saturate** in this screen — a control with an obvious answer should produce one —
and saturation does not disqualify them from that role. They would enter a
profiled study only if they disperse, which would make them the sharpest
available test.

## Verification before collection

`verify_structure()` enforces both halves mechanically and is called by the
leakage gate before any batch is built:

- A conflict task fails if any option dominates another on standards and total,
  if any option upholds every standard, or if fewer than two standards are in
  tension.
- A control task fails unless exactly one option dominates every other **and**
  that option upholds all four standards.

The control requirement is as strict as the conflict requirement: a control that
does not actually dominate cannot serve as a negative control.

## Design

| Item | Value |
|---|---|
| Stages | review, then screen |
| Screen | 25 unprofiled decisions per task, 8 tasks, 200 total |
| Profiled decisions | **0** |
| Saturation gate | modal share 1.00 marks a task unusable for a profiled study |
| Seeds | 2026091540 / 2026091541 / 2026091542 |

Option order alternates within each task and is reconstructed from the frozen
requests during analysis, as in the set A screen.

## What this can and cannot produce

**Can:** a measured dispersion value per task, and a list of tasks eligible for a
separately designated profiled study.

**Cannot:** any moral score, any claim about good or bad decisions, any profiled
comparison, or any Phase 4 pass. No agent action is labelled here.

Every task is reported with its screen value whether or not it passes, including
controls. Tasks are not added, swapped or reworded after seeing screen results to
reach a target count.
