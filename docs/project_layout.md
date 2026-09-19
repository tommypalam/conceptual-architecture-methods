# Project layout and naming

Updated 14 September 2026. Published version: `main`; use a development branch for new work.

## Where things belong

| Location | Purpose |
|---|---|
| `README.md` | Short project introduction and current scientific status |
| `NEXT_STEPS.md` | Current work, remaining dependencies and links to accepted decisions |
| `AGENTS.md`, `CLAUDE.md` | Matching project rules |
| `docs/` | Documentation; see its [README](README.md). Reference documents that frozen reports link to stay at this level |
| `docs/thesis/` | **The thesis**: `LF3262767.pdf` (the single canonical PDF), its source `thesis.md`, the portal `abstract.txt`, `figures/`, the `build/` toolchain and verifier, and frozen `history/` |
| `docs/paper/` | The full-length paper draft and its citation verification |
| `docs/publications/` | Dated records of each publication to `main` |
| `docs/handoffs/` | Machine and session handoffs |
| `Theory/` | Versioned theoretical sources; historical statements are interpreted through accepted amendments |
| `code/engine/` | Reusable simulation, provider, parsing and analysis components |
| `code/` | CLI, collectors and offline analyses. **Flat by necessity**: 109 of its modules are SHA-256-pinned by the frozen release chain and import one another by name, so nothing here is renamed or moved. Its [README](../code/README.md) maps each thesis result to its modules |
| `code/maintenance/` | Offline project maintenance tools |
| `tests/` | Offline tests for implementation and provenance safeguards; see its [README](../tests/README.md) |
| `config/` | Parameter distributions, correlations, configurations and seeds |
| `prompts/` | Current prompt templates |
| `experiments/` | Locked questions and complete evidence packages at stable reproducibility paths |
| `archive/` | Historical archives, superseded guidance and unused drafts, grouped by phase |
| `output/` | Ignored local runtime output, backups and verification working files |

## Reading order and labels

Start at the root README: abstract, results, next steps, theory, then evidence.
Each main area has a README with descriptive links. The detailed Phase 1.5
[evidence index](../experiments/phase1_5_encoding_validity/evidence_index.md)
groups studies by purpose and retains the exact directory names beside them.

Use plain-language titles for navigation, such as "Independent PD confirmation".
Keep actual source filenames stable. No numbered folder prefixes, symbolic-link
aliases or duplicate copies are needed just to control the reading order.

The researcher retired the separate root decision log. Record a substantive
decision in the phase document it affects and link it from NEXT_STEPS.md. Existing
archived chronologies remain available; do not create a replacement parallel log.

## Navigation layer (2026-09-14)

Every top-level area has a `README.md` acting as its entry point, and each one
links back to the root. The intended path for a new reader is:

    README.md  ->  docs/abstract.md  ->  experiments/README.md  ->  NEXT_STEPS.md

The root README states the findings and, immediately after, what is *not*
established. Keep that pairing: a finding and its boundary belong together, and
a reader who sees only the first half has been misled.

[experiments/README.md](../experiments/README.md) is the evidence index: every
study in reading order with its outcome, plus a short guide to the shape of a
frozen study folder (`PROTOCOL.md`, `ASSESSMENT.md`, `CHECKPOINT.json`,
`STATUS.md`). A study whose protocol exists but whose assessment records zero
participants was stopped by its own gate; that is a designed outcome, not an
incomplete folder, and the navigation must not present it as a gap.

When a result is filed under an operational verdict that understates it, add a
sibling interpretation note rather than rewriting the frozen assessment. The
[recognition finding note](../experiments/phase3_benchmarks/recognition_r1/FINDING_INTERPRETATION.md)
is the worked example: the failed-gate verdict stands, and the measurement is
reported as a finding beside it.

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
