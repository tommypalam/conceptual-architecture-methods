# Prospective PD gradient test: protocol r1

**Status: DRAFT. Not frozen, not authorised, no calls made.**
Requires researcher authorisation and one accepted independent review before any
paid call. 15 September 2026 designation; Phase 3A under implementation
specification v0.2.

## 1. Why this study exists

The [within-arm reanalysis](../../phase5_analysis/reanalysis_20260914/ASSESSMENT.md)
found that Procedural Dependence predicts which agents depart from the
unprofiled baseline, with a monotone dose-response and first rank of ten
coordinates under multivariate control, in four independent cells of n=400.

That finding is **post-hoc**. PD was predicted for S1 in thesis §6.1.1, where it
is null; its dominance on S2 and S3 was not predicted. A post-hoc discovery in
already-collected data cannot be called confirmed, and the project has correctly
refused to call it so.

This study converts it into a prospective test on fresh tasks, with the
direction, the shape, the discriminating contrast and the failure conditions
all fixed before collection.

## 2. Theoretical derivation of the prediction

The prediction is derived from existing theory, not invented for this study.

Thesis v0.6 §4.2 (line 368): *"Procedural Dependence shifts evaluation from
outcome-assessment to process-assessment."* PD's calibration anchor is
Colquitt's (2001) procedural-to-distributive justice sensitivity ratio, over the
Thibaut & Walker / Leventhal / Lind & Tyler tradition establishing that
procedural and distributive evaluations are psychologically separable with
different downstream predictive validity.

If that mapping is functional rather than decorative, then on a dilemma where
the process-respecting action and the outcome-maximising action **diverge**,
an agent's PD coordinate should govern which it selects. On a dilemma where the
two actions **coincide**, PD should not matter, because there is nothing for the
process/outcome axis to discriminate.

This yields a prediction that can fail in three distinct ways, stated in §5.

## 3. Design

### 3.1 Task classes

Six fresh tasks, none of them S1-S3, none a classic benchmark. Two classes,
three tasks each, assigned by the derivation above **before** any data:

- **Class P (process/outcome divergent), 3 tasks.** The procedurally correct
  action produces a worse total outcome; the outcome-maximising action requires
  bypassing or shortcutting a legitimate process. *Prediction: PD gradient present.*
- **Class N (process/outcome aligned), 3 tasks.** Following the process and
  maximising the outcome select the same action. *Prediction: PD gradient absent.*

Class N is the discriminating control. Without it, a PD gradient on Class P is
consistent with "PD is a general dissent dial." With it, a gradient on P and its
absence on N is evidence for the specific process/outcome mechanism the theory
asserts. **Class N is not padding and must not be dropped if budget tightens** —
a P-only study is not worth running.

Task authorship rule: each task is written to its class specification, then
the class assignment, predicted direction and the process-respecting label are
recorded in `code/phase3_pd_gradient_tasks.py` and covered by its content hash
before collection (see 3.4). No task may be reassigned between classes after any
response is seen.

### 3.2 Dispersion pre-screen (mandatory gate)

Per the [saturation diagnosis](../../phase5_analysis/reanalysis_20260914/SATURATION_DIAGNOSIS.md),
four prior studies returned uninformative nulls because their unprofiled baseline
was deterministic. This study screens first.

For each of the six tasks: **25 unprofiled (U-arm) calls** through the production
harness at collection temperature. Compute modal share *p*.

| Modal share | Disposition |
|---|---|
| *p* = 1.00 | **Reject the task.** Replace it before any profiled collection. |
| 0.85 ≤ *p* < 1.00 | Usable; the ceiling is recorded and reported with the result. |
| *p* < 0.85 | Usable. |

Screening is on **baseline dispersion only, never on outcomes**. The screen runs
before any profiled arm exists, so it cannot select for a desired effect. The
screen value for every task — including replaced ones — is reported.

A task replaced at screening gets a new task, one new screen, and an explicit
record. At most **two** replacement rounds; if six qualifying tasks cannot be
found in two rounds, the designation stops and reports that outcome.

### 3.3 Participants

120 fresh profiles per task, drawn from the unchanged ten-dimensional
copula/Beta population. Seed `2026091501` for the draw, `2026091502` for
task assignment. Profiles are hash-locked before collection.

Six tasks × 120 = **720 participant decisions**. Each agent receives the full
ten-coordinate numeric profile (the E arm). The U-arm screen supplies the
baseline; no separate large U arm is collected, because the screen already
establishes the baseline distribution and the within-arm gradient is the estimand.

No parameter, marginal, correlation matrix entry, locked question or societal
axis definition changes. AW remains included, as in all prior studies.


### 3.4 The task set (authored, hashed, not yet reviewed)

Six tasks are authored in `code/phase3_pd_gradient_tasks.py`. Content hash
`1f42b1b16af7bd81d2edb023061b8d0edec8684c93d2122635469b319fe63aff` covers all task text, the counterbalance map and the
predictions; it is recomputed and checked before launch.

| Task | Class | Process label | Outcome label | PD predicted to favour |
|---|---|---|---|---|
| `permit_sequence` | P | BETA | ALPHA | BETA |
| `tender_award` | P | ALPHA | BETA | ALPHA |
| `records_release` | P | BETA | ALPHA | BETA |
| `inspection_backlog` | N | ALPHA | same | none (control) |
| `roster_publication` | N | BETA | same | none (control) |
| `grant_arithmetic` | N | ALPHA | same | none (control) |

Class P tasks place a legitimate published procedure against a materially better
outcome: a permit needing a survey sign-off, a late tender bid that is the best
on the merits, and an outbreak dataset awaiting board approval. Class N tasks
pair the same procedural structure with evidence that following the procedure
also produces the better outcome, so the axis has nothing to separate.

**Counterbalancing.** Options are stored by role (`process_text` /
`outcome_text`) and labelled at assembly. The process-respecting option carries
label ALPHA in three tasks and BETA in three, and neither class is
label-constant. A fixed label, or a general pro-rule bias, therefore cannot
reproduce the predicted P-versus-N pattern.

**Leakage.** An automated audit checks that no participant-visible text contains
any parameter name, the class assignment, the predicted answer, or the name of
any classic paradigm. The audit currently reports zero forbidden terms across
all six tasks, and includes a planted-term check so it cannot pass vacuously.
Participant text is 134-152 words across tasks, so length is not a confound.

Offline checks for all of the above are in `tests/test_phase3_pd_gradient.py`
(35 tests, passing). They lock the design invariants; they do not establish
scientific validity.


### 3.5 Collector and stage gates (implemented, not run)

`code/phase3_pd_gradient.py` implements the three stages, each gated on the one
before. Zero calls have been made; `run` additionally requires an explicit
`--yes` flag.

1. **Review.** One independent design review of the full task set. Any verdict
   other than `accept` writes a `review_stop` result with zero screen and zero
   participant calls.
2. **Screen.** 150 unprofiled calls. The unprofiled arm is constructed by
   building the prompt from a placeholder profile and stripping the block
   entirely, so no placeholder value reaches the model. Any task at modal
   share 1.00 writes a `screen_stop` result with zero participant calls, and
   replacement requires a new linked designation rather than an in-place retry.
3. **Participants.** 720 profiled decisions, shuffled within each agent's block.

Inherited safety machinery is unchanged: write-once records, a strict parser
that rejects unknown labels, duplicate JSON keys and extra fields, per-call cost
reservation with replay verification, source-hash freezing, and a guard that
refuses to dispatch anything not in the frozen manifest. Two additional guards
are specific to this study: a leakage gate that refuses to build a batch whose
participant text contains a forbidden term or whose counterbalance is broken,
and a check that the task content hash still matches the release at collection
time.

Offline verification in `tests/test_phase3_pd_gradient_collector.py` (40 tests)
covers the parser, both stage gates, the unprofiled prompt construction, and the
analysis. The analysis was checked against synthetic data in both directions: it
recovers a planted Class P gradient (contrast +0.36) and reports no effect when
none is present (contrast -0.06). Together with the 35 design tests and the
21 reanalysis tests, 96 offline checks pass.

## 4. Estimands and analysis, fixed in advance

**Primary estimand.** Per task, the point-biserial correlation between the PD
coordinate and choice of the **process-respecting option**, identified by role
rather than by label (labels are counterbalanced per 3.4), with a two-sided
permutation p (10,000 shuffles of the choice labels against fixed parameter
values, seed `2026091503`). The prediction is a POSITIVE correlation on Class P
and no correlation on Class N.

**Primary contrast.** Mean PD correlation across Class P tasks minus mean across
Class N tasks. This single number is the study's headline; it is positive only
if PD operates on the process/outcome axis specifically.

**Secondary, prespecified.**
1. PD quintile dissent rates per task, reported as the five-point profile.
2. Multivariate logistic regression on all ten standardised coordinates per
   task; PD's rank by coefficient magnitude.
3. Per-task Holm correction across the six primary tests.

**Reporting rule.** Every task's result is reported whether or not it matches
prediction, including replaced tasks and their screen values. Effect sizes and
uncertainty accompany every estimate. Wide intervals are not equivalence.

## 5. Prespecified failure conditions

The prediction fails, and the failure is reported as the result, if:

1. **No gradient on Class P.** Fewer than 2 of 3 Class P tasks show a positive
   PD correlation surviving Holm. → The reanalysis finding does not generalise
   beyond S2/S3 and is plausibly task-specific.
2. **Gradient present on Class N.** 2 or more Class N tasks show a PD gradient
   of comparable magnitude. → PD is a general dissent/deviation dial, not a
   process/outcome mechanism. The theoretical mapping is wrong even though the
   statistical effect is real.
3. **PD not dominant.** PD fails to rank first under multivariate control in a
   majority of Class P tasks. → The effect is not PD-specific.

Any of these is a publishable, informative outcome. None is grounds for
re-running, re-labelling, adding tasks, or reassigning classes. **The sign of
the result is not a success gate.**

Exploratory analyses beyond this section are permitted and must be labelled
post-hoc.

## 6. Power

Simulated under PD ~ Beta(2.5, 2.0), using the **weakest** observed cell from
the reanalysis (S3 `00100`, Q1 = 2.5%, Q5 = 37.5%) as the planning effect —
deliberately conservative, since three of four observed cells were larger.

| n per task | Power (permutation, α = .05) |
|---:|---:|
| 40 | 0.50 |
| 60 | 0.62 |
| 80 | 0.82 |
| 100 | 0.88 |
| **120** | **0.93** |

False-positive rate on a simulated flat (PD-irrelevant) task at n=120: **0.040**
(400 sizing trials, 300 flat trials, seed 20260915). Nominal alpha is 0.05; the
simulated rate is within Monte-Carlo error of nominal at 300 trials
(95% binomial interval roughly 0.022-0.068), so Class N can support its
intended null role without an inflated false-positive rate.

PD's maximum absolute correlation with any other coordinate in R is **0.20**
(PD–MS), so a PD-specific effect is separable by multivariate control rather
than being a proxy for a correlated coordinate.

Reproduce every figure in this section with:

```powershell
py -3.11 -B code/phase3_pd_gradient_power.py
```

Deterministic under seed 20260915. Zero API calls.

## 7. Cost

Empirical basis: `transfer_pilot_r1` cost $0.302339400 for 448 participant
calls = $0.00067486 per decision, same harness and comparable prompt length.

| Item | Calls | Projected |
|---|---:|---:|
| Dispersion pre-screen | 150 | $0.101230 |
| Participant decisions | 720 | $0.485903 |
| Independent review | 1 | ~$0.050000 |
| **Projected total** | **871** | **$0.637132** |
| **Reservation with 40% headroom** | | **$0.891985** |

Against remaining allowances: Claude $7.860326 of $15, OpenAI $28.649421 of $30,
package $68.603673 of $100. Replacement screening rounds, if triggered, are
counted against the same reservation and cannot exceed it.

Budgets do not reset with a new designation. A new date or phase label never
resets a counter.

## 8. Gates before any paid call

1. Researcher authorisation of this protocol and its reservation.
2. Tasks authored, classes assigned, predicted directions and process-respecting
   labels recorded and hashed in `TASKS.md`.
3. One accepted independent AI review of the task set, confirming each task
   instantiates its assigned class and that no task leaks its predicted answer,
   its class, the parameter names, or any benchmark identity.
4. Offline tests passing: parser, both stage gates, unprofiled prompt
   construction, analysis in both directions, budget and size guards, and the
   source-hash guard. 96 checks currently pass.
5. Exact frozen manifest and cost bound.

A rejected review or a failed offline test stops this designation. No rewritten
in-place retry; a revision gets a new linked designation.

## 9. What this study cannot establish

- **No ethical understanding.** A behavioural gradient on a process/outcome axis
  is not comprehension of procedural justice.
- **No human resemblance.** No human comparison is collected.
- **No moral quality.** No action is morally scored here; that is Phase 4.
- **No validity for the other nine coordinates.** This tests PD only.
- **No institutional-axis identification.** Context is held fixed; the confounded
  anchor problem is untouched and remains open.
- **One model, one harness, one snapshot.** Portability remains untested.
- **No completed original battery.** The Phase 1.5 full encoding battery and the
  formal five-benchmark Phase 3 study remain unmet and are not repaired by this.

A successful result licenses exactly one claim: *on fresh process/outcome
dilemmas, the Procedural Dependence coordinate prospectively predicts which
action a profiled agent selects, and does not do so where the axis is
irrelevant.* That is the strongest claim the design supports.

## 10. Five-perspective review

Decision: run a prospective, theory-derived test of the PD gradient with an
aligned-task control class and a mandatory dispersion pre-screen.

- **Linden:** the Class N control is what separates a claim about the
  process/outcome axis from a claim about generic deviation. Without it the
  study would restate the post-hoc finding in new clothes. Keep the derivation
  in §2 explicit so the prediction is visibly theory-driven, not curve-fitted.
- **Osei:** the pre-screen must run through the production harness at collection
  temperature, and every screen value must be reported, including for rejected
  tasks — otherwise task replacement becomes silent selection. Six tasks is thin
  for a task-class generalisation; say so as a limit rather than widening scope.
- **Tanaka:** power is adequate at n=120 against the weakest observed cell, and
  the flat-task false-positive rate is calibrated at 0.040, within Monte-Carlo
  error of nominal. Insist on
  Holm across the six primaries and on reporting the Class P minus Class N
  contrast with an interval, not just its sign.
- **Renna:** this feeds Phase 4 directly — whichever Class P tasks show the
  gradient are the natural substrate for contested moral dilemmas, since they are
  demonstrably non-saturated and have a live mechanism.
- **Okafor:** the three failure conditions in §5 are concrete and checkable
  before launch, which is what makes this worth running. Require the two-round
  replacement cap in code, not just in prose, so screening cannot drift.

Genuine disagreement: Osei holds that six tasks cannot support a claim about
task *classes* and would prefer more tasks per class over more agents per task;
Tanaka holds that per-task power is the binding constraint and prefers n=120.
Resolution: keep n=120 with three tasks per class for adequate per-task power,
and state the narrow task base as an explicit limit in §9 rather than claiming
class-level generality. Revisit task count only in a separately designated
follow-up. These are structured review roles, not external expert review or
human approval.
