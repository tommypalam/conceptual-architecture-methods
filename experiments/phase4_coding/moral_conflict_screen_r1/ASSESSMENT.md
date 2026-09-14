# moral_conflict_screen_r1: stopped at review (reject)

**Outcome: review_stop. One paid call, zero screen decisions.** 15 September
2026. Superseded by [r2](../moral_conflict_screen_r2/ASSESSMENT.md), which was
accepted and collected 150 decisions.

| Item | Value |
|---|---|
| Verdict | reject |
| Cost | $0.001999800 |
| Release | `23f59a13…` |

## Cause: a drafting error in the reviewer instruction

r1 reused the Phase 3 reviewer prompt, which requires "no quantities attached to
options". Phase 4 moral tasks **require** stipulated consequences — the numbers
state what each option causes and are the substance of the item. The reviewer
was asked to enforce a constraint that contradicts the design, and applied it
correctly. The finding was mine, not the reviewer's.

## Findings and disposition

1. *"one option is framed with explicit rule/consent duties or deception
   issues (data_consent, safety_hold, witness_cost)."* **Not accepted.** Those
   duties are what create the moral conflict; removing them removes the dilemma.
   The r2 instruction states this explicitly.
2. *"Some options use comparative or outcome-cueing language, including totals
   and wording like 'best', 'otherwise recommend', 'full allocation'."*
   **Partly accepted.** The totals are intended and necessary. The two wording
   cues are fair hits and were neutralised in r2, along with renaming the action
   id `serve_by_need` to `serve_other_first`.
3. *"At least one item appears to name or imply a moral/psychological construct
   via framing (e.g., refusal, need, best)."* **Not accepted.** "Refusal"
   describes the stipulated fact of the scenario, not a construct.

Nothing was collected under this designation. Its stop, findings and charge are
preserved unchanged.
