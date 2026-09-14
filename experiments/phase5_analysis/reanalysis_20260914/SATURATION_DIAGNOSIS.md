# Cross-phase saturation diagnosis and proposed task-screening rule

14 September 2026. Offline synthesis of already-recorded results. **No new
collection, no record modification, no budget change.** This document proposes a
protocol rule for future designations; it authorises nothing.

## The pattern

Four independently designed studies, across three phases, produced nulls with the
same structural cause. Each was recorded separately; none was previously connected
to the others.

| Study | Design | Outcome as recorded | Baseline dispersion |
|---|---|---|---|
| [Phase 2 confirmation](../../phase2_confirmation_20260913/ASSESSMENT.md) S2, S3 | 400 profiles × 2 anchors | Six contrasts passed Holm | **U arm 400/400 identical** in all four cells |
| [transfer_pilot_r1](../../phase3_benchmarks/transfer_pilot_r1/ASSESSMENT.md) | 448 responses, E/V/S/U, PD 0.1/0.9 | Inconsistent trade-off; "key diagnostic is saturation" | **448/448 opposed** the preferential procedure |
| [representation_diagnostic_r1](../../phase3_benchmarks/representation_diagnostic_r1/ASSESSMENT.md) | 576 decisions, E vs V | All intervals include zero | Partially saturated at non-primary offers |
| [consequence_rule_pilot_r1](../../phase4_coding/consequence_rule_pilot_r1/ASSESSMENT.md) | 96 choices, E/V/U/G | All contrasts exactly zero; degenerate bootstrap | **96/96 identical** across all four arms |

In every case the recorded interpretation was cautious and correct in isolation.
Taken together they identify one mechanism: **when the unprofiled model's answer
to a task is deterministic, no arm comparison on that task can discriminate any
hypothesis.** The measurement has no room to move, so a null is guaranteed
regardless of whether encoding works.

This is not a claim that the nulls are artefacts to be discarded. It is a claim
that they are uninformative about encoding, and highly informative about task
selection.

## Why it kept happening

The protocols selected tasks for **theoretical interest** — process/outcome
tension, competing duties, costly disclosure — and verified them with structural
review (does this task instantiate the intended construct?) and offline schema
tests (does the pipeline handle it?). Neither check measures whether the model
actually varies on the task. A task can be perfectly constructed, perfectly
reviewed, and still have a 100% modal unprofiled response.

The [Phase 2 reanalysis](ASSESSMENT.md) makes this measurable: in S2 and S3 the
unprofiled arm chose one option in 400/400 calls, while S1 — the only task with
non-degenerate baseline — was also the only task where PD showed no effect and
profiles moved behaviour *toward* the mode rather than away. Dispersion and
discriminability are tightly coupled, and neither was screened for.

## Proposed rule: dispersion pre-screen

Before committing any multi-arm budget to a task, measure the unprofiled response
distribution on that task.

1. **Probe.** Run the task in the U arm only, n ≈ 20–30, no profile, at the
   collection temperature and through the production harness.
2. **Compute** the modal share *p* of the most-chosen option.
3. **Classify.**
   - *p* = 1.00 — **deterministic.** Cannot discriminate any arm contrast.
     Reject, or redesign the task, before spending on arms.
   - 0.85 ≤ *p* < 1.00 — **near-ceiling.** Usable only for hypotheses predicting
     movement *off* the mode, with the ceiling stated as a limit. Report the
     screen value alongside the result.
   - 0.55 ≤ *p* < 0.85 — **usable.** Room to move in both directions.
   - *p* < 0.55 — **contested.** Maximum discriminability; preferred for any
     contrast whose direction is uncertain.
4. **Record** the screen value in the protocol before freezing, and report it with
   the result so a null can be read against the room that existed for an effect.

The screen is cheap relative to what it protects. At observed per-decision rates,
25 unprofiled probes cost a small fraction of a multi-arm packet, and the four
studies above committed roughly 1,500 paid participant decisions to tasks whose
discriminating capacity was never measured.

### What the rule does not do

It does not guarantee an effect, and it must not be used to select tasks *because*
they produce a desired result. The screen runs on the **U arm only**, before any
profiled arm is collected, and it measures dispersion, not effect direction. A
task that passes the screen and then shows no arm difference is an informative
null — that is the point of screening. Screening on outcomes rather than baseline
dispersion would be outcome-driven selection, which implementation
specification v0.2 forbids and this rule must not become.

It also does not retroactively repair any completed study. The four results above
stand as recorded, with their existing interpretations and limits.

## Reinterpreting the existing nulls

With the mechanism identified, three recorded nulls can be stated more precisely
without changing any number:

- **consequence_rule_pilot_r1's zero contrasts** are not evidence that encoding
  fails to affect moral choice. They are evidence that the four stylized tasks had
  an obvious answer that every arm found, including the no-profile arm. The
  degenerate bootstrap is a symptom of identical outcomes, as its assessment
  already states.
- **transfer_pilot_r1's flat side** means the intended process/outcome contrast
  had only one live arm, so the "inconsistent transfer" verdict is
  underdetermined rather than negative.
- **Phase 2's six passing contrasts** are, in four of six cells, measurements of
  variance *creation* from a deterministic baseline rather than distribution shift
  — a stronger and more specific claim than the arm-level table conveys, and one
  the [reanalysis](ASSESSMENT.md) quantifies.

## Consequence for Phase 4

Phase 4B remains the central moral experiment under implementation specification
v0.2, and the good/bad decision question remains its core. The diagnosis changes
how its tasks must be chosen, not what it asks:

- Moral tasks must be **genuinely contested in the U arm**, or the capstone will
  reproduce r1's 96/96 result at larger N.
- Given the reanalysis, **process-versus-outcome moral dilemmas** are the best
  available candidates: PD is the one coordinate with a demonstrated monotone
  dose-response, so a moral task built on that axis has a known live mechanism.
- Contested moral tasks mean cases where competent, well-intentioned actors
  disagree — competing duties with real costs on both sides — not cases where the
  right answer is obvious and the question is whether the agent finds it.

## Five-perspective review

Decision: adopt a U-arm dispersion pre-screen as a design requirement for future
task selection, and reinterpret four existing nulls as saturation-driven.

- **Linden:** a task with an obvious answer tests compliance, not normative
  judgement. Contested tasks are required for the moral question to be meaningful
  at all, independently of statistical discriminability.
- **Osei:** this is standard pilot practice and should have preceded every packet.
  Insist the screen runs through the production harness at collection
  temperature — dispersion is a property of the harness, not the text.
- **Tanaka:** screening on baseline dispersion is legitimate; screening on
  outcomes is not, and the distinction must be explicit in every protocol that
  adopts this. A deterministic cell has zero Fisher information for any arm
  contrast, so the rule is a power requirement, not a preference.
- **Renna:** the PD result and this diagnosis point the same way — build the
  capstone on the process/outcome axis where a live mechanism is demonstrated.
- **Okafor:** make the screen value a required protocol field with a recorded
  number, so a future reader can tell a real null from a saturated one.

Genuine disagreement: Linden treats contestedness as a conceptual requirement for
the moral claim, while Tanaka treats it as a statistical power condition; these
motivate the same rule but differ on whether a near-ceiling task is ever
acceptable. Resolution: permit the 0.85–1.00 band only for hypotheses about
movement off the mode, with the screen value reported. Structured review roles,
not external expert review or human approval.
