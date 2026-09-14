# Publication record, 14 September 2026

The researcher authorised publishing the offline reanalysis and navigation
cleanup to `main`, preserving the previous published `main` as `backup-2`.

## Branch targets

| Branch | Commit | Meaning |
|---|---|---|
| `backup` | `c8e7aa0b` | Original published main; retained unchanged |
| `backup-1` | `aaed0a8d` | Second published main; retained unchanged |
| `backup-2` | `470d5cb6` | **New.** The published main immediately before this release |
| `main` | fast-forwarded | Now carries the nine frozen research commits plus this cleanup |
| `research-transfer-design-20260913` | development | Source branch; pushed for continuity |

`main` was an ancestor of the development branch, so the update is a
fast-forward. No history was rewritten, force-pushed or reset.

## What is published

**Offline reanalysis** of the completed Phase 2 confirmation records, with zero
API calls and no budget change. Cumulative accounting is unchanged at Claude
$7.139674300/$15, OpenAI $1.350579450/$30, package $31.396326775/$100.

- [Within-arm reanalysis](../experiments/phase5_analysis/reanalysis_20260914/ASSESSMENT.md)
  and [`code/phase5_reanalysis.py`](../code/phase5_reanalysis.py): the no-profile
  arm was deterministic in four of six cells; Procedural Dependence shows a
  monotone dose-response and ranks first of ten parameters under multivariate
  control in every non-degenerate cell. Scores the thesis §6.1.1 directional
  signs for the first time: 5 supported, 4 null, 0 wrong sign.
- [Saturation diagnosis](../experiments/phase5_analysis/reanalysis_20260914/SATURATION_DIAGNOSIS.md):
  four nulls across three phases share one cause; proposes a U-arm dispersion
  pre-screen as a required protocol field.
- [Recognition finding note](../experiments/phase3_benchmarks/recognition_r1/FINDING_INTERPRETATION.md):
  keeps the failed-gate verdict and records the substantive result beside it.
- [`tests/test_phase5_reanalysis.py`](../tests/test_phase5_reanalysis.py):
  21 offline checks, all passing.

**Navigation pass** over the root README, the evidence index, the Phase 3, 4 and
5 indexes, the docs and code guides, a new tests README and the layout guide.
Documentation only.

## Verification before release

| Check | Result |
|---|---|
| Reanalysis reproducibility | Byte-identical on rerun, seed 20260914 |
| New tests | 21/21 passing |
| Local documentation links | 229 checked, 0 broken |
| `CLAUDE.md` / `AGENTS.md` | Identical after the title line |
| `git diff --check` | Clean |
| Frozen study directories in diff | None |
| Secret scan on new files | No matches |
| Ignored data | `data/` and `output/` remain excluded |

## Test suite status, stated honestly

The full offline suite reports **6 failed, 230 passed, 10 skipped, 102 errors**.
Every one of these predates this work. Verified by running the suite on a clean
tree with all changes stashed: the failure/error pattern is character-for-character
identical over the compared span (E=30, F=3 across the first 144 tests), and no
failure or error references any file added here.

Two environment causes, neither in project code:

1. **205 `PermissionError`** — `%LOCALAPPDATA%\Temp\pytest-of-tpala` has broken
   ACLs on this machine, so pytest cannot create `tmp_path`. Removing that
   directory should clear most of these.
2. **12 `FileNotFoundError`**, plus assertion-level failures once temp is
   repaired — tests requiring gitignored raw per-call records that are absent
   from this machine. These need the local data transfer bundle, not a code fix.

There are **zero `AssertionError` results**: no test logic fails.

## Scope limits

Publication does not establish any scientific claim. The reanalysis is post-hoc
exploratory; the PD dominance on S2/S3 was not among the prospectively locked
predictions and requires a separate prospective test before any confirmatory
language. No phase is reopened, no completed result altered, no new hypothesis
presented as having preceded existing responses.

Phase 3 remains open. Phase 4B remains the central moral experiment under
implementation specification v0.2. Human raters remain deferred. No paid run is
queued or authorised by this release.

Raw per-call records and archives remain excluded from Git, so a clone is not the
dataset; off-device backup is still unverified. See the
[desktop handoff](desktop_handoff.md) for the separate data transfer.
