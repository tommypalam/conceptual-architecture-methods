# Project layout and naming

Updated 12 September 2026. Current cleanup branch: `project-cleanup-20260912`.

## Where things belong

| Location | Purpose |
|---|---|
| `README.md` | Short project introduction and current scientific status |
| `NEXT_STEPS.md` | Current work and remaining dependencies; no stale running-job narrative |
| `meta.md` | Active decision index, with links to full archived chronologies |
| `AGENTS.md`, `CLAUDE.md` | Matching project rules |
| `docs/` | Current manuscript drafts, plan, codebook and documentation |
| `Theory/` | Versioned theoretical sources; historical statements are interpreted through accepted amendments |
| `code/engine/` | Reusable simulation, provider, parsing and analysis components |
| `code/` | Existing CLI and reproducibility scripts; frozen source names stay stable |
| `code/maintenance/` | Offline project maintenance tools |
| `tests/` | Offline tests for implementation and provenance safeguards |
| `config/` | Parameter distributions, correlations, configurations and seeds |
| `prompts/` | Current prompt templates |
| `experiments/` | Locked questions and complete evidence packages at stable reproducibility paths |
| `archive/` | Historical archives, superseded guidance and unused drafts, grouped by phase |
| `output/` | Ignored local runtime output, backups and verification working files |

## Naming for new work

- Use lowercase `snake_case` for new folders, Python modules and ordinary document names.
- New dated study directories use `study_name_YYYYMMDD`; dated narrative snapshots use `description_YYYY-MM-DD.md`. Retain an existing study's designation exactly.
- Use `README.md` for a directory's entry point. The existing root governance filenames remain unchanged.
- Keep the ten parameter codes exactly: LL, CS, RT, MoR, RE, PD, TfA, ID, MS, AW. Do not rename them for stylistic consistency.
- Keep existing per-call names and request keys. New runs follow the applicable frozen record schema; figure/table artifacts use the project's `fig_XX_description` / `table_XX_description` convention.
- Do not cosmetically rename hash-locked source files, approved templates, locked questions or recorded study identifiers. Their stable names are part of reproducibility.

## Archive policy

The top-level archive has `phase0`, `phase0b`, `phase0c`, `phase1`, `phase1_5`,
`phase2`, `phase3`, `phase4`, `phase5`, and `phase6` folders. `shared` contains
cross-phase history; `maintenance` contains relocation manifests and verification.
Folders with no historical material say so explicitly.

Archive a document when its operational instructions or draft have been
superseded. A completed result is still evidence: preserve its complete package
with the source hashes and records it needs. Frozen Phase 1.5 packages remain
under `experiments/phase1_5_encoding_validity/`; the phase README identifies the
current findings and the historical supporting studies. Old timestamps and
OPEN/RUNNING statements inside frozen evidence are historical observations.

The existing Phase 0 question archive is now under `archive/phase0/question_revisions/`.
The former `experiments/phase0b_archive/` is under `archive/phase0b/runs/`.
All relocated bytes are verified using the [migration inventory](../archive/maintenance/migration_inventory_2026-09-12.json).
The [archive index](../archive/README.md) and migration plan map old paths to new
paths. Historical documents retain their original bytes, including old relative
links; use the archive's resolved-reference index for those links. Small redirect
pages may remain where frozen documents link to a former documentation path.

Raw response content, failure records and immutable manifests are never rewritten
to modernise a status message. Archive relocation does not change scientific
criteria, parameters or accepted phase outcomes. Raw artifacts that were ignored
before migration remain ignored; previously tracked historical files retain their
tracking status when relocated. No new raw payload is published by cleanup.
