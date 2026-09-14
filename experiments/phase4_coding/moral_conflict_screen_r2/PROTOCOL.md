# Phase 4 moral-conflict dispersion screen: protocol r2

**Revision of r1**, which stopped at review with verdict `reject` for
$0.001999800. The primary cause was a drafting error on my part: r1 reused the
Phase 3 reviewer instruction, which demands "no quantities attached to options".
Phase 4 moral tasks *require* stipulated consequences, so the reviewer was asked
to enforce a constraint that contradicts the design and applied it correctly.

r2 sends an instruction written for this phase: stipulated consequences are an
intended and necessary part of each item, duties and consent on one side are the
substance of the conflict rather than a flaw, and an item is flagged only if one
option is clearly correct on every consideration at once, if the text implies
what ought to be chosen, or if it names a construct.

Two wording cues the r1 review named are accepted and neutralised: "the service
you would otherwise recommend" and "full allocation" are reworded, and the
action id `serve_by_need` is renamed `serve_other_first`. The objection that
consent and disclosure duties disqualify an item is not accepted; those duties
are what create the conflict.

**Screen only.** 15 September 2026. This designation collects unprofiled
decisions on six candidate moral-conflict tasks and reports their baseline
dispersion. **It runs no profiled arm and assigns no moral score.**

## Why a screen first

Phase 3 closed on a measured requirement: screen candidate tasks for dispersion
*before* building a study, because judged ambiguity does not predict dispersion
in this harness.

- [consequence_rule_pilot_r1](../consequence_rule_pilot_r1/ASSESSMENT.md):
  96/96 identical choices across E/V/U/G.
- [pd_endpoint_r2](../../phase3_benchmarks/pd_endpoint_r2/ASSESSMENT.md):
  modal share 1.00 on all six tasks, *after* an independent review accepted them
  with zero blocking issues.

A task set that does not vary unprofiled cannot discriminate any arm contrast,
whatever its moral content. Spending a participant budget before measuring
dispersion is what produced both results above.

## What changed in the tasks

`consequence_rule_pilot_r1` saturated because its tasks had a dominant option:
truthful reporting was both the honest action and the one that helped the third
party, so honesty and welfare pointed the same way.

These six tasks are constructed so the four fixed standards **oppose** each
other. Every option upholds at least one and violates at least one; no option is
clean on all four; and each task puts at least two different standards in
tension. In every task the option that upholds deception-avoidance has the
*lower* stipulated total, so honesty is never also the welfare-maximising choice.

| Task | Tension |
|---|---|
| `witness_cost` | honesty vs. harm to an identified person |
| `quota_shortfall` | fairness vs. aggregate welfare |
| `safety_hold` | harm avoidance vs. honouring a written commitment |
| `referral_fee` | honesty vs. loyalty to a colleague |
| `triage_override` | fairness vs. a legitimate published rule |
| `data_consent` | welfare vs. respecting a stated refusal |

`verify_conflict()` checks this mechanically before any batch is built: it
rejects a task if any option dominates another on standards and total, if any
option upholds every standard, or if fewer than two standards are in tension.
Three drafts were rejected by that check during authoring and repaired.

## Design

| Item | Value |
|---|---|
| Stages | review, then screen |
| Screen | 25 unprofiled decisions per task, 6 tasks, 150 total |
| Profiled decisions | **0** |
| Saturation gate | modal share 1.00 marks a task unusable |
| Seeds | 2026091520 / 2026091521 / 2026091522 |

Option order alternates deterministically within each task, so presentation
cannot drive the result. Order is reconstructed from the frozen requests during
analysis, as in pd_endpoint_r2.

Three audits run before any batch is built: no forbidden term in participant
text or review packet, no comparative or evaluative language, and the conflict
verification above.

## What this can and cannot produce

**Can:** a measured dispersion value per task, and a list of tasks eligible for a
separately designated study.

**Cannot:** any moral score, any claim about good or bad decisions, any profiled
comparison, or any Phase 4 pass. No agent action is labelled here. Human raters
remain deferred.

A task that saturates is reported as saturated. A task that varies is reported
as eligible and nothing more. The result is not a success gate in either
direction.
