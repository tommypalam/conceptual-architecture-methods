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

## Find an entry point

| Task | Files |
|---|---|
| Fresh Phase 2 confirmation | [Collector](run_phase2_confirmation.py), [analysis](analyze_phase2_confirmation.py), [read-only audit](audit_phase2_confirmation.py), [diagnostics](diagnose_phase2_confirmation.py), [archive verification](archive_phase2_confirmation.py) |
| Frozen exploratory Phase 2 | [Collector](run_phase2_pilot.py), [analysis](analyze_phase2_pilot.py), [read-only audit](audit_phase2_pilot.py) |
| Pilot-to-confirmation methods | [Diagnostics](diagnose_phase2_pilot.py), [prospective parser](phase2_group_fields_v2.py), [exact power scenarios](phase2_confirmation_power.py) |
| Phase 5 within-arm reanalysis | [Offline reanalysis, zero API calls](phase5_reanalysis.py) |
| PD gradient power simulation | [Sizing and calibration, zero API calls](phase3_pd_gradient_power.py) |
| PD gradient task set | [Six tasks, counterbalanced, leakage-audited](phase3_pd_gradient_tasks.py) |
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
