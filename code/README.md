# Code guide

Visual playback: [simulation theatre](../viewer/README.md), launched with
`py -3.11 -B code/serve_replay.py` from the repository root. It replays completed
Phase 2 records locally without API calls; `--verify-all` checks all 300 groups.

[Back to the project](../README.md)

## Understand the implementation

| Order | Component | Responsibility |
|---|---|---|
| 1 | [Population](engine/population.py) and [sampling utilities](utils.py) | Construct parameter profiles |
| 2 | [Questions](engine/questions.py) | Load the locked dilemma text |
| 3 | [Prompt assembly](engine/prompt_assembly.py) and [delivery](engine/delivery.py) | Assemble the model's inputs |
| 4 | [Model clients](engine/llm_client.py) | Handle provider requests and mock responses |
| 5 | [Parsing](engine/parsing.py) and [record sink](engine/record_sink.py) | Extract labels and preserve responses |
| 6 | [Simple runner](engine/simple_runner.py) and [complex runner](engine/complex_runner.py) | Coordinate the corresponding task types |

## Trace a thesis result to its code

Every result in the [thesis](../docs/thesis/LF3262767.pdf) follows one pattern:
a **design module** fixes the question, arms and locked prediction; a
**collector** named `<design>_rN.py` dispatches designation `rN` against the
write-once ledger; the evidence lands in `experiments/.../<designation>/`; and
any later analysis is a separate zero-call module that only reads frozen records.

| Thesis result | Design | Collector | Evidence | Offline analysis |
|---|---|---|---|---|
| Profile vs instruction, second model (§6) | [pool](phase4b_profiled_pool.py) | [profiled_r1](phase4b_profiled_r1.py) | [phase4b_profiled_r1](../experiments/phase4_coding/phase4b_profiled_r1/ASSESSMENT.md) | |
| Profile vs instruction, calibration model (§6) | [pool](phase4b_gpt_pool.py) | [gpt_r2](phase4b_gpt_r2.py) | [phase4b_gpt_r2](../experiments/phase4_coding/phase4b_gpt_r2/ASSESSMENT.md) | |
| Ten-label derangement control (§6) | [permutation](phase4b_permutation.py), [pool](phase4b_perm_pool.py) | [permutation_r2](phase4b_permutation_r2.py) | [phase4b_permutation_r2](../experiments/phase4_coding/phase4b_permutation_r2/ASSESSMENT.md) | |
| Three-model variance decomposition (§6) | [tasks](phase4b_tasks_r2.py) | [grand_r1](phase4b_grand_r1.py) | [phase4b_grand_r1](../experiments/phase4_coding/phase4b_grand_r1/ASSESSMENT.md) | |
| Prospective PD test (§7.1) | [pd_prospective](phase5_pd_prospective.py) | [r1](phase5_pd_prospective_r1.py) | [pd_prospective_r1](../experiments/phase5_analysis/pd_prospective_r1/ASSESSMENT.md) | |
| PD swap control (§7.2) | [label_semantics](phase5_label_semantics.py) | [r1](phase5_label_semantics_r1.py) | [label_semantics_r1](../experiments/phase5_analysis/label_semantics_r1/ASSESSMENT.md) | |
| Label vs line position, 2×2 (§7.3) | [counterbalance](phase5_position_counterbalance.py), [block reorderer](phase5_position_render.py) | [r1](phase5_position_counterbalance_r1.py) | [position_counterbalance_r1](../experiments/phase5_analysis/position_counterbalance_r1/ASSESSMENT.md) | |
| Eight-parameter sweep (§7.5) | [coordinate_sweep](phase5_coordinate_sweep.py) | [r2](phase5_coordinate_sweep_r2.py) | [coordinate_sweep_r2](../experiments/phase5_analysis/coordinate_sweep_r2/ASSESSMENT.md) | [rescore](phase5_sweep_rescore.py) |
| ID and LL swap controls; LL withdrawal (§7.6) | [label_semantics_multi](phase5_label_semantics_multi.py) | [r2](phase5_label_semantics_r2.py) | [label_semantics_r2](../experiments/phase5_analysis/label_semantics_r2/ASSESSMENT.md) | |
| PD on the second provider (§8) | [pd_crossmodel](phase5_pd_crossmodel.py) | [r1](phase5_pd_crossmodel_r1.py) | [pd_crossmodel_r1](../experiments/phase5_analysis/pd_crossmodel_r1/ASSESSMENT.md) | |
| ID on the second provider (§8) | [id_crossmodel](phase5_id_crossmodel.py) | [r1](phase5_id_crossmodel_r1.py) | [id_crossmodel_r1](../experiments/phase5_analysis/id_crossmodel_r1/ASSESSMENT.md) | [rescore](phase5_id_crossmodel_rescore.py), [power](phase5_id_crossmodel_power.py) |

**Analyses over the frozen records, all zero API calls:**

| Module | What it computes |
|---|---|
| [phase5_integrated.py](phase5_integrated.py) | Parameter separability, AW sensitivity, coordinate ordering across designations |
| [phase5_mixed_effects.py](phase5_mixed_effects.py), [phase5_refit_primary.py](phase5_refit_primary.py) | Crossed random-intercept logistic model; refit of every primary contrast |
| [phase6_mixed_slopes.py](phase6_mixed_slopes.py) | The same with a random slope of condition by item |
| [phase6_review_tests.py](phase6_review_tests.py) | Direct TRUE−SWAP difference tests and the other reviewer-requested analyses |
| [phase6_thesis_intervals.py](phase6_thesis_intervals.py) | Paired and item-cluster bootstrap intervals; equivalence bounds for the sweep |
| [phase6_thesis_figures.py](phase6_thesis_figures.py) | The four thesis figures, written to `docs/thesis/figures/` |

**Two things that will otherwise mislead you.**

*Do not trust the first docstring line of a collector.* Several collectors
(`phase5_coordinate_sweep_r2.py`, `phase5_label_semantics_r1.py` and `_r2.py`,
`phase5_pd_prospective_r1.py`) open with "Prospective PD discriminant test on
crossed no-clean-hands dilemmas" — a header inherited from the module they were
adapted from. It is wrong for all of them and **cannot be corrected**: each file
is hash-pinned by its own release, and editing it would break verification for
every designation that inherits from it. The file *name* and its design module are
authoritative.

*Do not rename or move anything in this folder.* 109 of the 271 modules here are
pinned by SHA-256 in the frozen release chain, and they import one another by
flat module name. That is why this directory is flat and long, and why the
19 September reorganisation restructured `docs/` but added only this guide here.

## Find an entry point

| Task | Files |
|---|---|
| Fresh Phase 2 confirmation | [Collector](run_phase2_confirmation.py), [analysis](analyze_phase2_confirmation.py), [read-only audit](audit_phase2_confirmation.py), [diagnostics](diagnose_phase2_confirmation.py), [archive verification](archive_phase2_confirmation.py) |
| Frozen exploratory Phase 2 | [Collector](run_phase2_pilot.py), [analysis](analyze_phase2_pilot.py), [read-only audit](audit_phase2_pilot.py) |
| Pilot-to-confirmation methods | [Diagnostics](diagnose_phase2_pilot.py), [prospective parser](phase2_group_fields_v2.py), [exact power scenarios](phase2_confirmation_power.py) |
| Phase 5 within-arm reanalysis | [Offline reanalysis, zero API calls](phase5_reanalysis.py) |
| PD gradient power simulation | [Sizing and calibration, zero API calls](phase3_pd_gradient_power.py) |
| PD gradient task set | [Six tasks, counterbalanced, leakage-audited](phase3_pd_gradient_tasks.py) |
| PD gradient collector | [Three-stage collector, DRAFT and unauthorised](phase3_pd_gradient.py) |
| Basic simulation CLI | [Run](run_engine.py), [score](score_engine.py) |
| Configuration generation | [Build configuration](build_config.py) |
| Final all-ten assessment | [Reproduce the assessment](report_all_ten_final.py) |
| Independent PD confirmation | [Reproduce the confirmation report](report_structural_confirmation.py) |
| Structural package summary | [Reproduce the package report](report_structural_package.py) |
| Optional research assistance | [Research-support adapters](research_support/) |
| Archive maintenance | [Checksum-verified relocation tool](maintenance/archive_project.py) |

Historical calibration and validation scripts remain beside these entry points
because imports and frozen source hashes depend on their names. Their prefixes
identify their purpose: `run_` executes, `prepare_` prepares, `report_` reports,
and `verify_` checks. Consult each script and its frozen protocol before use;
a historical runner is not a queued or newly authorised experiment.

## Verify offline

Run from the repository root in the existing Python environment:

```powershell
python -B -m pytest tests -q -p no:cacheprovider
```

No paid Phase 1.5 job is queued. The never-dispatched final-confirmation draft is
in the [archive](../archive/phase1_5/unexecuted_drafts/). Current research work is
listed in [NEXT_STEPS.md](../NEXT_STEPS.md).
