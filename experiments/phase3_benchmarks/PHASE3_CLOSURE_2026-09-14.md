# Phase 3 closure for a scoped objective

14 September 2026. This closes Phase 3 for a stated limited objective, in the
manner of the accepted
[Phase 1.5 closure](../phase1_5_encoding_validity/ACCEPTED_CLOSURE_2026-09-12.md).

**The original Phase 3 battery is not met and is not retrospectively passed.**
The five-benchmark N200 study was never released, and Phase 3B human
behavioural comparison was never attempted. Nothing here claims otherwise.

## What Phase 3 set out to do

Implementation specification v0.2 splits the phase:

- **Phase 3A — transfer and interpretation.** New situations, competing
  explanations, simpler controls, held-out prediction where justified.
- **Phase 3B — human behavioural comparison.** Comparable human evidence against
  the five benchmark families.

## What Phase 3 established

### 1. Benchmark decanonisation does not work

A 500-probe recognition screen, dual-coded by raters from two different
providers with **500/500 exact agreement**, identified all five decanonised
variants at the same rate as their canonical originals — 50/50 in every one of
ten cells, Wilson 95% interval 92.87%–100%.

Structure-preserving domain substitution does not conceal a classic paradigm
from a frontier model. This closes a contamination control the literature
commonly assumes rather than tests, and it makes the configuration
counterfactual the only available discriminator.
→ [screen](recognition_r1/execution/transport_r1/ASSESSMENT.md) ·
[interpretation](recognition_r1/FINDING_INTERPRETATION.md)

### 2. Profile packages change behaviour; presentation format does not

| Study | Result |
|---|---|
| [E/U context diagnostic](context_diagnostic_r2/ASSESSMENT.md) | 576 valid decisions; +50-point profile-package difference at offer 20 in both justice contexts; primary context interaction zero with wide uncertainty |
| [E/V representation diagnostic](representation_diagnostic_r1/ASSESSMENT.md) | 576 valid decisions; numeric-minus-prose differences +16.7 and +4.2 points, every interval including zero. Neither a presentation effect nor equivalence established |

### 3. Saturation is the binding constraint on this design space

Four studies across three phases returned nulls traceable to one cause:
a task whose unprofiled answer is deterministic cannot discriminate any arm
contrast. The [saturation diagnosis](../phase5_analysis/reanalysis_20260914/SATURATION_DIAGNOSIS.md)
identified the mechanism and proposed a U-arm dispersion pre-screen.

**Phase 3 then tested that proposal prospectively and confirmed it.**
[pd_endpoint_r2](pd_endpoint_r2/ASSESSMENT.md) passed an independent design
review with zero blocking issues and ran 150 unprofiled decisions on six fresh
administrative dilemmas, deliberately written without quantities, comparisons or
any statement of which option is preferable.

**All six tasks returned modal share 1.00 — 25/25 identical decisions each.**
Presentation order was irrelevant: the first-shown option was chosen in 77 of
150 decisions (51.3%), 48–52% per task. Four tasks resolved to the
procedure-respecting option and two to departing, so the determinacy is
task-specific rather than a blanket compliance policy.

The screen refused the participant stage and 720 paired decisions were not
collected, because on these tasks they could not have discriminated anything.

### 4. A documented design constraint

Five successive designs failed to produce a testable process/outcome
manipulation, and the failures are distinguishable:

| Attempt | Trade-off stated as | Outcome |
|---|---|---|
| [gradient r1](pd_gradient_r1/ASSESSMENT.md) | Evaluative adjectives | Review: cued the answer |
| [gradient r3](pd_gradient_r3/ASSESSMENT.md) | Understated facts | Review: task classes collapsed |
| [gradient r4](pd_gradient_r4/ASSESSMENT.md) | Stipulated totals | Review: revealed the answer |
| [endpoint r1](pd_endpoint_r1/ASSESSMENT.md) | Absent; options read as unlawful | Review: not two permissible choices |
| [endpoint r2](pd_endpoint_r2/ASSESSMENT.md) | Absent; both permissible | **Review accepted**; screen: no dispersion |

The review objections were eventually resolved. What remained was not a wording
problem: **the harness returns a determinate answer to these situations
regardless of how carefully the trade-off is concealed.** Ambiguity as judged by
an independent reviewer does not produce dispersion in the harness.

This is a reportable constraint on the design space, established by measurement
rather than argument.

## What Phase 3 did not establish

- **Phase 3B is not attempted.** No human behavioural comparison exists. It was
  deferred as infeasible under the researcher's explicit no-budget instruction,
  not silently replaced by an AI substitute.
- **The original five-benchmark N200 study is not released.** All ten
  coordinates, five benchmark families, Beta marginals and R remain in scope and
  unvalidated by this phase.
- **The PD gradient remains untested prospectively.** The
  [Phase 5 reanalysis](../phase5_analysis/reanalysis_20260914/ASSESSMENT.md)
  finding stands exactly as recorded: post-hoc, on Phase 2 data. Five
  designations attempted a prospective test and none collected a profiled
  decision.
- **No ethical understanding, human resemblance or moral quality.**
- All results are one model, one harness, one snapshot. Portability is untested.

## Accepted scoped conclusion

Phase 3 is closed for this objective: **it characterised the boundaries of the
measurement approach rather than delivering a benchmark pass.** Specifically, it
established that benchmark familiarity cannot be removed by domain substitution,
that profile packages shift behaviour while presentation format does not, and
that deterministic unprofiled baselines — not effect size — are the binding
constraint on detecting normative parameterisation in this harness.

This is an explicit post-results scope decision, recorded as such. It is not a
section 8.2 pass, not a partial pass, and not a replacement gate.

## Accounting

Phase 3 total including all PD designations: Claude $7.139674300/$15, OpenAI
$1.443713700/$30, package $31.489461025/$100. The PD sequence spent $0.093134250
across six designations against $16.829628 of reservations, collecting 150 screen
decisions and zero participant decisions. Usage estimates, not wallet balances.

No collector is running and no paid batch is queued. Raw records and archives
remain local; off-device backup is unverified.

## Carried into Phase 4

Phase 4B remains the central moral experiment under implementation specification
v0.2, with the good/bad decision question unchanged. Two requirements follow
directly from this phase:

1. **Screen candidate tasks for dispersion before building a study**, not after.
   Both the Phase 2 reanalysis and pd_endpoint_r2 show that judged ambiguity
   does not predict measured dispersion; only measurement does.
2. **Select moral tasks from those that vary.** A task set assembled for
   theoretical interest and validated only by review will reproduce
   consequence_rule_pilot_r1's 96/96 result at larger N.
