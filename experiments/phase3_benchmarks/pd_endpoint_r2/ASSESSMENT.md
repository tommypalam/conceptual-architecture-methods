# pd_endpoint_r2: accepted review, saturated screen

**Outcome: screen_stop after an accepted design review. 151 paid calls,
150 valid screen decisions, zero participant decisions.** 14 September 2026.

This is the first PD designation to pass its review gate and collect data. The
data answers a real question, and the answer stopped the study.

## Result

| Item | Value |
|---|---|
| Review verdict | **accept**, zero blocking issues, zero limits |
| Screen decisions | 150 / 150 valid |
| Tasks usable | **0 of 6** |
| Participant decisions | 0 |
| Cost | $0.058536225 |
| Reservation released | $3.340646925; $3.282 not charged |
| Release | `dd79f15e…` |

Accounting: Claude $7.139674300/$15, OpenAI $1.443713700/$30, package
$31.489461025/$100. Usage estimates, not wallet balances.

## The measurement

Twenty-five unprofiled decisions per task, six tasks, through the production
harness at collection temperature.

| Task | Choice | n | Modal share | Unprofiled choice is |
|---|---|---:|---:|---|
| `permit_sequence` | ALPHA | 25/25 | 1.00 | departing |
| `tender_award` | ALPHA | 25/25 | 1.00 | procedure-respecting |
| `records_release` | ALPHA | 25/25 | 1.00 | departing |
| `inspection_backlog` | ALPHA | 25/25 | 1.00 | procedure-respecting |
| `roster_publication` | BETA | 25/25 | 1.00 | procedure-respecting |
| `grant_arithmetic` | ALPHA | 25/25 | 1.00 | procedure-respecting |

**Every task is perfectly deterministic.** All six fail the prespecified
saturation gate (modal share 1.00), so the participant stage did not run.

### It is not position bias

Presentation order alternates deterministically within each task. Reconstructing
the order from the frozen requests and comparing it to the choices:

**The first-shown option was chosen in 77 of 150 decisions (51.3%)** — 48% to 52%
per task. Order is irrelevant to the outcome. The unanimity is driven by task
content, not by where an option appears.

### The model is not uniformly rule-following

Four tasks resolved to the procedure-respecting option and two
(`permit_sequence`, `records_release`) resolved to departing from it —
100 of 150 decisions procedure-respecting overall. The unprofiled model has a
determinate answer for each of these situations, and that answer is
task-specific rather than a blanket policy of compliance.

## What this establishes

**A real measurement, prospectively gated.** The screen did exactly what the
[saturation diagnosis](../../phase5_analysis/reanalysis_20260914/ASSESSMENT.md)
proposed: it measured baseline dispersion before committing the participant
budget, and refused the expensive stage when there was no dispersion to work
with. 720 paired participant decisions were not collected, because on these
tasks they could not have discriminated anything.

**Direct confirmation of the saturation mechanism on fresh material.** The
reanalysis found four of six Phase 2 cells with deterministic unprofiled
baselines. Six of six here. Deterministic baselines are not an artefact of the
older Phase 2 dilemmas; they recur on new, deliberately ambiguous administrative
tasks written specifically to avoid an obvious answer.

**A sharpened statement of the design problem.** These tasks were built to be
ambiguous: no quantities, no comparison, nothing stating which option is better,
and a shared framing declaring both options fully within the role-holder's
discretion. An independent reviewer accepted them as genuine dilemmas with no
blocking issues. **The model still answered every one of them identically
25 times out of 25.** Ambiguity as judged by a reviewer does not produce
dispersion in the harness.

## What this does NOT establish

- **Nothing about Procedural Dependence.** No profiled decision was collected.
  The [Phase 5 reanalysis](../../phase5_analysis/reanalysis_20260914/ASSESSMENT.md)
  result stands exactly as recorded: post-hoc, on Phase 2 data, still awaiting a
  prospective test.
- **No claim that these tasks are unanswerable or that the model is correct.**
  A deterministic answer is not a right answer, and the 25 responses per cell
  are one model, one harness, one snapshot, one prompt form.
- **No general claim about administrative dilemmas.** Six tasks, one attempt.
- **No ethical understanding, human resemblance or moral quality.**
- The review's acceptance is one AI judgement, not human expert review or
  evidence that the tasks are well constructed.

## Where this leaves the approach

Four of the five recorded failure modes in this line of work are now
distinguished by evidence rather than argument:

| Attempt | Trade-off stated as | Failure |
|---|---|---|
| gradient r1 | Evaluative adjectives | Review: cued the answer |
| gradient r3 | Understated facts | Review: classes collapsed |
| gradient r4 | Stipulated totals | Review: revealed the answer |
| endpoint r1 | Absent; options read as unlawful | Review: not two permissible choices |
| **endpoint r2** | **Absent; both options permissible** | **Review accepted. Screen: no dispersion** |

The review objections are now resolved — r2 passed with zero blocking issues.
What remains is not a wording problem at all: **the harness returns a
determinate answer to these situations regardless of how carefully the trade-off
is concealed.** A profile manipulation cannot be detected on material where the
unprofiled model never varies.

Any continuation needs tasks selected for measured dispersion rather than for
judged ambiguity — which means screening candidate tasks first and building the
study only from those that vary. That is a different sequencing of the same
protocol, and it is not attempted here.

## Provenance

All 151 records are written once and preserved. Review response, all 150 screen
responses, the frozen release, requests and population remain unchanged. The
inherited `pd_gradient_r1/review/0` failure is carried forward untouched. No
parameter, marginal, correlation entry, locked question or societal axis
definition was altered.
