# Code entry points

Current work is offline thesis integration and downstream planning. No paid
Phase 1.5 job is queued. See [current status](../NEXT_STEPS.md).

| Area | Entry points and purpose |
|---|---|
| Reusable engine | `engine/`: profiles, question loading, delivery, providers, immutable record sinks and analysis |
| Basic execution | `run_engine.py`, `score_engine.py`: existing simulation CLI composition |
| Configuration | `build_config.py`, `utils.py`: configuration generation, sampling and PSD checks |
| Current evidence reporting | `report_all_ten_final.py`, `report_structural_confirmation.py`, `report_structural_package.py`: reproduce completed assessments with their frozen inputs |
| Phase 0 history | `phase0_*.py`, `run_phase0b.py`, `run_phase0c.py`, `run_recalibrate.py`, `run_nulla_tasksweep.py`: preserved calibration and harness tools |
| Phase 1 history | `run_phase1_pilot.py`: operational pilot |
| Phase 1.5 history | `run_validity_*.py`, `run_structural_*.py`, `run_all_ten_*.py` and associated preparation/report scripts: frozen study reproduction, not queued future runs |
| Optional research assistance | `research_support/`: evidence adapters, separate from behavioural decisions |
| Maintenance | `maintenance/archive_project.py`: explicit, checksum-verified archive migration; no API client |

Historical script names stay stable when imports or frozen source hashes depend
on them. The abandoned, never-dispatched final-confirmation runner is preserved
under `archive/phase1_5/unexecuted_drafts/`; it is not a supported command.

Run offline verification from the repository root:

```powershell
python -B -m pytest tests -q -p no:cacheprovider
```

For any new empirical run, prepare a new protocol and designation. Do not reuse
historical execute commands merely because they appear in an archived handoff.
Existing raw records remain write-once, including failures.
