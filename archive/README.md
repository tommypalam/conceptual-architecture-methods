# Central project archive

Historical artifacts are grouped by phase. This archive preserves past wording,
records and failed or superseded approaches. Its contents are evidence and history,
not current run instructions. Read [NEXT_STEPS.md](../NEXT_STEPS.md) for active work.

| Folder | Purpose | Relocated files |
|---|---|---:|
| [phase0](phase0/README.md) | Original calibration and retired question revisions | 155 |
| [phase0b](phase0b/README.md) | Harness diagnostics and candidate recalibration | 26,256 |
| [phase0c](phase0c/README.md) | Locked holdout | 0 |
| [phase1](phase1/README.md) | Operational pilot | 0 |
| [phase1_5](phase1_5/README.md) | Encoding validity history and superseded drafts | 46 |
| [phase2](phase2/README.md) | Main-study preparation | 1 |
| [phase3](phase3/README.md) | Behavioural benchmarks | 0 |
| [phase4](phase4/README.md) | Coding and validation | 0 |
| [phase5](phase5/README.md) | Sensitivity and analysis | 0 |
| [phase6](phase6/README.md) | Reporting and release | 0 |
| [shared](shared/README.md) | Cross-phase decision and programme history | 4 |

## Preservation and navigation

- All 26,462 relocated files retain their original SHA-256 and byte size.
- The existing Phase 0 question archive and all historical Phase 0b files were moved intact.
- Complete frozen Phase 1.5 packages stay at stable experiment paths. They remain reproducibility dependencies, not disposable clutter.
- Earlier candidate generation records are retained with their candidate packages; ignored raw records remain local and ignored.
- Historical filenames stay unchanged when they identify an existing record. New folder names follow the [layout policy](../docs/project_layout.md).
- Old relative links inside archived documents preserve historical bytes; use the [resolved-reference index](historical_references.md) for navigation.

[Migration plan](maintenance/migration_plan_2026-09-12.json) | [Per-file checksums](maintenance/migration_inventory_2026-09-12.json) | [Verification report](maintenance/verification_2026-09-12.md)

This is an archive on the same computer, not an off-device backup. No raw API
payload is newly published by this cleanup.
