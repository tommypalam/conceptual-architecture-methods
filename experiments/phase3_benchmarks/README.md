# Phase 3: benchmarks and diagnostics — open

Four studies are complete; the formal benchmark battery is not. Recognition
screening is finished and all five decanonised alternatives were rejected as
low-recognition controls. That operational verdict stands, and the measurement
behind it is also a substantive result in its own right — see the
[finding interpretation](recognition_r1/FINDING_INTERPRETATION.md).

| Study | Result |
|---|---|
| [Recognition screen](recognition_r1/execution/transport_r1/ASSESSMENT.md) | 500 probes; 50/50 recognition in all ten cells; all alternatives rejected |
| [E/U context diagnostic](context_diagnostic_r2/ASSESSMENT.md) | 576 decisions; +50-point profile-package difference at offer 20 |
| [E/V representation diagnostic](representation_diagnostic_r1/ASSESSMENT.md) | 576 decisions; neither presentation effect nor equivalence established |
| [Transfer pilot](transfer_pilot_r1/ASSESSMENT.md) | 448/448 valid; saturated, one side of the contrast flat |
| [PD gradient r1 - review stop](pd_gradient_r1/ASSESSMENT.md) | Prospective test of the PD dose-response. Review returned `revise`; 1 call, $0.028867575, zero participants |
| [PD gradient r2 - frozen, never dispatched](pd_gradient_r2/STATUS.md) | Re-designated after a post-freeze source correction; $0 |
| [PD gradient r3 - review stop](pd_gradient_r3/ASSESSMENT.md) | Same design as r2. Review returned `reject` on a real class-definition defect; 1 call, $0.001966800, zero participants |
| [PD gradient r4 - review stop, sequence closed](pd_gradient_r4/ASSESSMENT.md) | Trade-off restated as stipulated quantities. Review returned `reject`; the accepted finding is structural and closes the sequence. 1 call, $0.002087250, zero participants |

The transfer pilot's saturation and three other nulls share one cause; see the
[cross-phase saturation diagnosis](../phase5_analysis/reanalysis_20260914/SATURATION_DIAGNOSIS.md)
and its proposed dispersion pre-screen before designing further packets.

The original all-five-benchmark N200 study is not released. All ten coordinates,
five benchmark families, Beta marginals and R remain in scope.

## Recognition screen detail

Current [implementation v0.2](../../Theory/implementation_specification_v0_2.md)
keeps the thesis exploratory and the [moral capstone](../phase4_coding/CAPSTONE_DESIGN_DRAFT_20260913.md)
central. Transfer work supports that experiment; original recognition results and
human-behaviour validation requirements remain explicit.

New research direction: [theory-grounded transfer strategy draft](transfer_design_20260913/STRATEGY_DRAFT.md).
Candidate process/outcome trade-offs, held-out prediction and simpler controls;
no paid release, finalized pilot packet or formal Phase 3 amendment. The proposed
pilot ceiling is $2, subject to exact costing. No new calls have been made.

Latest representation comparison: [E/V diagnostic complete and verified](representation_diagnostic_r1/ASSESSMENT.md). All 576 decisions valid; numeric-minus-prose rejection differences at offer 20 were +16.7/+4.2 points with wide intervals including zero. Neither a clear presentation effect nor equivalence is established. Cost $0.409685100; 1,814 records preserved; no further paid work queued.

Earlier E/U diagnostic: [canonical E/U diagnostic complete](context_diagnostic_r2/ASSESSMENT.md). All 576 decisions valid; profile-package difference +50 points at offer 20 in both contexts, primary context interaction zero with wide uncertainty. Cost $0.304161000; zero-call verification passed and 1,237 records are preserved. Original recognition gates remain unmet. No further paid work is queued.

Clarified pilot: [completed and discarded after 5/5 recognition](design_pilot_r2/ASSESSMENT.md). Structural review accepted; both raters agreed. Eight calls cost $0.036588750, or $0.040948875 including the stopped pilot. Zero-call verification passed; 660 records are preserved. No further paid work is queued.

Next-candidate pilot: [stopped at structural review](design_pilot_r1/ASSESSMENT.md); two calls cost $0.004360125. No recognition calls ran. The earlier approval block is resolved; the original recognition results below remain unchanged.

All500 recognition responses are dual-coded. Haiku and GPT-5.4 mini agreed on
all500 answers, with no missing outcomes. Every canonical and alternative form
was recognised50/50 times. **All five alternatives fail the >15/50 recognition
gate.** No discussion was needed. This screen is complete; Phase3 remains open
and population collection is not released.

Read the [final assessment](recognition_r1/execution/transport_r1/ASSESSMENT.md),
[results](recognition_r1/execution/transport_r1/results.json) and
[verification checkpoint](recognition_r1/execution/transport_r1/CHECKPOINT.json).

| Benchmark | Canonical recognised | Alternative recognised | Alternative gate |
|---|---:|---:|---|
| Milgram | 50/50 | 50/50 | Reject |
| Asch | 50/50 | 50/50 | Reject |
| Ultimatum | 50/50 | 50/50 | Reject |
| Bystander | 50/50 | 50/50 | Reject |
| Reactance | 50/50 | 50/50 | Reject |

Earlier independent [structural acceptance](variants_r3/ASSESSMENT.md) assessed
operational text structure. It did not establish low recognition. Recognising a
shared structure does not by itself demonstrate memorisation, human resemblance,
moral quality or ethical understanding. The main thesis questions remain separate.

The complete screen cost $5.687192500 conservatively; the final CONTINUE turn
added $0.204660500. All Phase 3 accounting including both behavioural diagnostics is $6.858386425:
Claude $6.029498200, OpenAI $0.828888225, within the separate $15/$30 caps. Package accounting including
Phase 2 is $29.764459450 under $100. These are estimates, not provider balances.

The original500 probes and28 valid coding batches were reused. An exact replacement
reproduced an invalid long ID, so a [prospective format amendment](recognition_r1/execution/transport_r1/PROTOCOL.md)
used short opaque IDs for the remaining72 calls, mapped exactly back to original
records. Both failures remain immutable and fully accounted. The mixed coding
formats and AI-only raters are explicit limitations; no rubric or answer text changed.

Seven recovery/transport tests and seven existing runtime/analysis checks passed.
Final real-data replay made zero API calls, reproduced results, checked all frozen
sources and historical evidence, and verified the1,952-member local archive:
`output/phase3_recognition_transport_r1_20260913.zip`. The original650 records remain intact; the design pilots and behavioural diagnostics bring the ledger to 1,814. Raw data and archives are excluded from Git; off-device backup is unverified.

## Evidence and next work

- [Completed recognition assessment and next decision](recognition_r1/execution/transport_r1/ASSESSMENT.md).
- [Original stopped screen](recognition_r1/execution/ASSESSMENT.md) and
  [exact replacement checkpoint](recognition_r1/execution/recovery_r1/CHECKPOINT.json).
- [Accepted structural reviews and limitations](variants_r3/ASSESSMENT.md),
  [repaired candidates](variants_r3/candidates.json), and
  [canonical protocol](canonical_r2/PROTOCOL.md).
- [Original quotation and discussion design](recognition_r1/QUOTATION_OUTCOME.md),
  [first paid release](recognition_r1/execution/RELEASE.md), and
  [provider budget](PROVIDER_BUDGET_20260913.md).

Review alternative-scenario design offline before any new candidate round. Do
not loosen the threshold, hide these rejections, or launch population simulations
using rejected low-recognition controls. An exploratory pilot may cheaply reject
future candidates, but does not replace the specified N50 acceptance screen.
No new generation, screening or population calls are running or queued.

All five benchmark families, ten LPM coordinates, Beta distributions and R remain
in scope. High/low contexts, modulators, dependency sensitivity and full D=100
trajectory costs still need their collection freeze and feasible budget resolution.
Phase3 does not retrospectively fill omitted Phase2 configurations.
