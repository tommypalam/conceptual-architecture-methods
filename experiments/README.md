# Experimental evidence

Every completed study, in reading order, with what it established and where the
evidence stops. Status lines here are current; dated text *inside* frozen study
folders is historical evidence, not current instruction.

Current position: Phase 0 closed, Phase 1 passed operationally, Phase 1.5 closed
for the accepted limited objective, Phase 2 complete, **Phase 3 closed for a scoped
objective**, Phase 4 at pilot stage, Phase 5 reanalysis begun. The
original full encoding battery and formal benchmark battery remain unmet.

## Reading order

| # | Phase | Read this | What it establishes |
|---|---|---|---|
| 1 | 0 | [Calibration and holdout closure](PHASE0_CLOSURE_2026-07-29.md) | Baselines locked; harness is non-neutral |
| 2 | 0 baseline | [Locked original questions](phase0_baseline_calibration/README.md) | Immutable provenance; never edit |
| 3 | 0b | [Harness result](../archive/phase0b/runs/PHASE0B_RESULT_2026-07-29.md) | Harness effects measured |
| 4 | 0c | [Locked holdout result](phase0c_locked_holdout/PHASE0C_RESULT_2026-07-29.md) | Prompts frozen permanently |
| 5 | 1 | [Operational pilot](phase1_pilot/PHASE1_PILOT_RESULT_2026-07-29.md) | Engine runs end to end |
| 6 | 1.5 | [Encoding evidence index](phase1_5_encoding_validity/README.md) | Profiles influence generation; PD clearest. Original battery unmet |
| 7 | 2 pilot | [Exploratory assessment](phase2_exploratory_20260912/ASSESSMENT.md) | 2,180 responses; group format failures found and repaired prospectively |
| 8 | 2 confirmation | [Fresh-sample assessment](phase2_confirmation_20260913/ASSESSMENT.md) | 4,800 decisions, 300 group runs; six individual contrasts pass Holm |
| 9 | 5 reanalysis | [Within-arm reanalysis](phase5_analysis/reanalysis_20260914/ASSESSMENT.md) | **Where the Phase 2 effect actually lives**: PD dose-response, deterministic baselines |

## Phase 3 — closed for a scoped objective

See the [Phase 3 index](phase3_benchmarks/README.md) for the full set.

| Study | Outcome |
|---|---|
| [Recognition screen](phase3_benchmarks/recognition_r1/execution/transport_r1/ASSESSMENT.md) | 500 probes, 50/50 recognition in all ten cells. Alternatives rejected as controls — and that is itself a finding: see the [interpretation note](phase3_benchmarks/recognition_r1/FINDING_INTERPRETATION.md) |
| [E/U context diagnostic](phase3_benchmarks/context_diagnostic_r2/ASSESSMENT.md) | 576 decisions; +50-point profile-package difference at offer 20 |
| [E/V representation diagnostic](phase3_benchmarks/representation_diagnostic_r1/ASSESSMENT.md) | 576 decisions; neither a clear presentation effect nor equivalence |
| [Transfer pilot](phase3_benchmarks/transfer_pilot_r1/ASSESSMENT.md) | 448/448 valid; saturated — every response opposed the preferential procedure |

The original all-five-benchmark N200 study is **not** released. All ten
coordinates, five benchmark families and the original failed gates stay explicit.

## Phase 4 — moral measurement, pilot stage

See the [Phase 4 index](phase4_coding/README.md).

| Item | Outcome |
|---|---|
| [Manual draft](phase4_coding/manual_r1/MANUAL_DRAFT.md) | Twelve categories specified; structure tested, moral validity not established |
| [Rating screens r1](phase4_coding/consequence_pilot_r1/ASSESSMENT.md), [r2](phase4_coding/consequence_pilot_r2/ASSESSMENT.md), [r3](phase4_coding/consequence_pilot_r3/ASSESSMENT.md) | All three stopped by their own prospective gates; zero participants. Preserved deliberately |
| [Finite-rule pilot](phase4_coding/consequence_rule_pilot_r1/ASSESSMENT.md) | 96/96 valid choices, saturated across E/V/U/G; all contrasts zero |

Human raters are deferred by explicit instruction; AI agreement is never presented
as human validation. No moral scores are assigned to any agent action.

## Phase 5 — integrated analysis, begun

| Item | Outcome |
|---|---|
| [Within-arm reanalysis](phase5_analysis/reanalysis_20260914/ASSESSMENT.md) | PD monotone dose-response, ranked 1/10 under control; four of six baselines deterministic |
| [Saturation diagnosis](phase5_analysis/reanalysis_20260914/SATURATION_DIAGNOSIS.md) | Four nulls across three phases share one cause; proposes a U-arm dispersion pre-screen |

Both are offline reanalyses of already-paid records. Zero API calls.

## How to read a frozen study folder

Most study directories follow the same shape:

- `PROTOCOL.md` — what was frozen before collection, including stopping rules
- `ASSESSMENT.md` — what happened, with limits stated
- `CHECKPOINT.json` — verification, record counts, archive hashes
- `STATUS.md` — short current-state pointer, where present

A study whose protocol exists but whose assessment records zero participants was
stopped by its own gate. That is a designed outcome, not an incomplete folder.

## Conventions and cautions

Frozen packages keep their original paths because manifests, replay scripts and
source hashes depend on them; do not rename them for tidiness. Raw per-call
records are write-once. A directory's file count is not a count of independent
observations — snapshots may overlap. No record was deleted in any
reorganisation; checksums are in the
[archive migration inventory](../archive/maintenance/migration_inventory_2026-09-12.json).

The [central archive](../archive/README.md) holds retired question revisions,
historical Phase 0b records and superseded plans. For current work and open
dependencies, read [NEXT_STEPS.md](../NEXT_STEPS.md).
