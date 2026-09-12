# PARIA: handoff to Codex on the desktop

Prepared 12 September 2026 for Tommaso Piero Palamenga.

## Message for the next Codex chat

Continue work on `tommypalam/conceptual-architecture-methods` from the current
GitHub `main` branch. Read this handoff, `README.md`, `NEXT_STEPS.md`, `AGENTS.md`
and `docs/variables.json` before making changes. Check Git status and use a new
development branch. Treat this as continuation of the existing project.

The researcher accepted Phase 1.5 closure around a limited positive conclusion:
**explicit normative profiles can systematically shape generated AI decisions
under the tested conditions, with replicated Procedural Dependence effects
providing the strongest evidence.** The original full battery remains unmet.
This is a disclosed post-results scope decision, not a retrospective gate pass.
Ethical understanding, all-ten robustness, persistent internalization, improved
moral performance and AGI have not been established.

Do not restart Phase 1.5 collection or try to optimise another sweep to pass its
original gate. No paid job is queued. Continue with thesis integration and a
concrete downstream design appropriate to the supported evidence. The original
full-architecture Phase 2 study has not been released. New coding rules, substantive
theoretical departures and new empirical protocols still require the relevant review.

The researcher intentionally removed `meta.md`; do not recreate it. Put current
work and decision pointers in `NEXT_STEPS.md`, and substantive decisions in their
phase documents. Preserve the gentle, human-readable layout and every raw record.

## Git branches and backup

- `main`: the current version, including the cleanup and this desktop handoff.
- `backup`: the previous GitHub `main`, commit
  `c8e7aa0bde3ce17bb8e36f367a2e15950aa6cd2d`.
- `project-cleanup-20260912`: the development history used to prepare publication.

The backup preserves the previous published version. It is not a backup of
ignored local response files. No force-push or history rewrite is required.
Verify the actual remote branch tips on arrival; future commits may follow this handoff.

Use a fresh checkout if the desktop already contains an older experiment copy.
Keep that older copy intact: it may contain responses that were never transferred
from the original computer.

```powershell
git clone --branch main https://github.com/tommypalam/conceptual-architecture-methods.git conceptual-architecture-methods-desktop
Set-Location conceptual-architecture-methods-desktop
git status --short --branch
git switch -c desktop-work
```

## Transfer the local research data separately

GitHub contains code, current documents, protocols, results and checksum inventories,
plus historical files that were already tracked. Recent response payloads, dispatch
records, some large exact request bundles and local ZIP backups are intentionally
ignored. **A Git clone alone is not the complete research dataset.**

On the originating computer, copy these two files to the desktop:

```text
C:\Users\tommy\Downloads\conceptual-architecture-methods-main (1)\output\desktop_transfer_20260912\paria_desktop_data_20260912.zip
C:\Users\tommy\Downloads\conceptual-architecture-methods-main (1)\output\desktop_transfer_20260912\desktop_data_manifest.json
```

The bundle contains locally ignored research artifacts, the existing ZIP backups
and cleanup verification inventories. It excludes credentials, `.git`, virtual
environments and caches. See [desktop_transfer.json](desktop_transfer.json) for
the ZIP SHA-256, byte size, file count and verification result.

Place both files beside the fresh checkout, then run from the checkout root:

```powershell
Get-FileHash -Algorithm SHA256 -LiteralPath ..\paria_desktop_data_20260912.zip
```

Compare that result with `bundle_sha256` in `docs/desktop_transfer.json` before
extracting. Extract only into the fresh checkout. Do not overwrite existing
research records or use `-Force` to conceal a collision.

```powershell
Expand-Archive -LiteralPath ..\paria_desktop_data_20260912.zip -DestinationPath .
python -B code/maintenance/verify_desktop_data.py ..\desktop_data_manifest.json --root .
```

The verifier requires Python 3.11 or newer and uses only the standard library.
It reads files without modifying them and must report `all_verified: true`.
If the bundle is unavailable, manuscript and code review can continue, but do
not claim that all records are present or rerun analyses requiring absent data.

Some frozen backup metadata contains absolute paths from the originating computer.
Copying the ZIP backups preserves their bytes but does not make those old absolute
paths valid. In particular, `code/report_all_ten_final.py` reads those paths.
Do not rewrite frozen metadata to fix this; use the portable transfer verifier
first and assess a separate path-resolution adapter before replaying such reports.

## Python environment for code work

The originating environment uses Python 3.11. The dependency snapshot in
[requirements-desktop.txt](../requirements-desktop.txt) records its installed
direct packages. A clean installation of those pins on the desktop still needs
verification; the existing-machine test result is not a fresh-environment claim.

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-desktop.txt
.\.venv\Scripts\python.exe -B -m pytest tests -q -p no:cacheprovider
```

No API key is needed for the offline tests or checksum verifier. Keys are not in
the handoff or transfer bundle. Configure credentials privately only if later
authorised work actually needs them. Do not paste keys into chat.

## Evidence to preserve in the thesis

| Evidence | Current interpretation |
|---|---|
| Independent PD confirmation | 100 valid responses across 25 new backgrounds. PD .1 to .9 increased S2 FORMAL_REPORT by 80 percentage points, simultaneous 95% CI [35.4, 95.2], and S3 WAIT by 68 points, CI [22.9, 88.2]. Both prospectively specified contrasts passed adjusted exact tests. |
| Later all-ten follow-up | 17,250 requests dispatched; 17,247 saved, 17,234 valid. The complete-data primary bootstrap is unavailable. The planned paired sensitivity retains all 180 contrasts, with eight incomplete contrasts assigned p=1; eight contrasts survive Holm correction. |
| PD across representations | Canonical endpoint effects and verbal endpoint/interior effects survive correction in both dilemmas. Observed canonical curves are ordered. Original simple-task PD signs began as exploratory; the independent confirmation remains a separate prospective test. |
| Other results | MoR has a canonical endpoint effect but primarily concerns response style. Numeric RT/S3 reverses its original prediction. MS is not an ordered canonical gradient. Keep all ten outcomes. |
| Robustness and explanations | Broad wording/representation robustness and aggregate audit thresholds remain insufficient. PD's separate active audit signal is 11/20, supplementary Holm10 p=.03, with dependence and self-explanation limitations. |

The original 39,000-response battery remains separate. Its 8/30 paraphrase result
and the newer 1/30 conservative paired result use different estimands/methods;
do not present them as a simple worsening trend. Failure to establish equivalence
is not automatically proof of non-equivalence. New backgrounds are not new dilemmas.

Ten parsing failures, three recorded API failures and three further unresolved
dispatches remain explicit in the final allocation. Nothing should be silently
retried or replaced. Latest tracked package accounting is $22.66401475 / $25,
including unknown-charge bounds; this is not lifetime spending or verified credit.

The earlier interrupted September 6 run's approximately 8,639 saved responses
were on another computer and were not recovered in this workspace. Its inventories
are not substitute payloads. If those records exist on the desktop, preserve and
inventory them separately before considering any disjoint merge.

## Reading order and next actions

1. [Abstract](abstract.md) and [results draft](phase1_5_results.md).
2. [Accepted closure](../experiments/phase1_5_encoding_validity/ACCEPTED_CLOSURE_2026-09-12.md).
3. [Complete all-ten assessment](../experiments/phase1_5_encoding_validity/all_ten_assessment_20260912/ASSESSMENT.md).
4. [Independent confirmation](../experiments/phase1_5_encoding_validity/structural_encoding_20260912/pd_confirmation/analysis/REPORT.md).
5. [Evidence index](../experiments/phase1_5_encoding_validity/evidence_index.md), [layout guide](project_layout.md) and [next steps](../NEXT_STEPS.md).

First verify the checkout, data availability and local environment. Then continue
integrating the completed findings into a submission-ready thesis. Prepare any
downstream design offline, keeping its hypotheses within the evidence's limits.
No new criterion, parameter removal, configuration selection, prompt change or
moral-coding scheme follows automatically from this handoff.
