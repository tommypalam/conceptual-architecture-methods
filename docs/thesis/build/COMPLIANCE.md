# Bocconi final-paper submission — 19 September 2026

The researcher authorised factual corrections, improved presentation and a
Bocconi-compliant PDF, and confirmed Prof. Arnaldo Camuffo as the sole supervisor.
The student number was supplied for the upload filename only.

## Sources and scope

- Researcher's supplied *Guide to Writing the Final Paper — Bachelor of Science
  Programs*, filename `GUIDE_TO_WRITING_THE_FINAL_PAPER20160712152429.pdf`:
  empirical structure, professional language, bibliography and in-text citations.
- [Bocconi 2025–26 undergraduate student guide, §§10.1–10.3](https://didattica.unibocconi.eu/tsg/testo.php?comando=Base&edizione=2026&idAnt=26757&volume=N3),
  checked on 19 September 2026. The supplied PDF itself refers readers to the
  student guide for the technical format specifications.

The sources determine document conventions. They do not authorise uploading,
contacting the supervisor, requesting institutional approval or changing the
research. No such action was taken. This check covers the supplied guide and
public 2025–26 requirements; any additional private programme/supervisor
instructions remain the researcher's responsibility to supply.

## Deliverables and build

- `../LF3262767.pdf`: final upload copy, and the single canonical thesis PDF. The
  former byte-identical convenience copy `docs/thesis.pdf` was removed in the
  19 September reorganisation so that there is exactly one thesis file.
- `../thesis.md`: authoritative revised manuscript.
- `../abstract.txt`: separate portal abstract, under 4,000 characters.
- `../../abstract.md`: current abstract with project metadata for local reading. It
  stays at `docs/abstract.md` because frozen reports link to that path, and
  `verify.py` now asserts it contains the portal abstract verbatim.

Run `powershell -File docs/thesis/build/build.ps1` from the repository root.
The script produces both PDF names and prints the location of its temporary
LaTeX diagnostics. It checks process exit codes and only replaces output files
after a successful build. It uses the installed Pandoc, XeLaTeX and fonts.
It makes no experimental API calls. Run `python docs/thesis/build/verify.py`
with pypdf and pdfplumber installed for the read-only artifact checks.

## Format implemented

| Requirement | Implementation |
|---|---|
| Single PDF, maximum 10 MB | One upload PDF; verified below the limit |
| Filename LF + student number | LF3262767.pdf |
| No student name or number in content | Removed from body and PDF author metadata |
| Four opening pages | Four genuinely blank, unnumbered pages; no dedication requested |
| No title page or abstract in upload | Both omitted; the portal supplies these separately |
| A4 | 210 × 297 mm; the guide's “29 × 21 (A4)” is interpreted as standard A4 |
| Left/right margins 2.5 cm | Geometry set explicitly; character bounds checked |
| 12-point body, recommended Arial/Tahoma/Verdana | Arial, 12 TeX points, embedded |
| 26–30 lines per full prose page | 1.65 line spacing, approximately 29 available body lines; headings and partial pages naturally contain fewer |
| Page numbering after four opening pages | Arabic 1 begins with the contents; centred footer |
| No university seal | No logo or seal used |
| Tables/figures/materials | Compact readable table/caption/verbatim typography; the 12-point requirement is applied to body prose |
| Citations | All authors at first mention, subsequent et al. italicised; alphabetical references; matching citation years and preprint versions |

The public guide describes approximately 30 pages as a general expectation, not
a fixed upload-page ceiling. The researcher's 30-page body-and-appendix ceiling
is checked separately, excluding contents, references and the four required
blank pages. Actual counts and the final file hash are in `verification.json`.

## Editorial and factual corrections

- The GPT E/G/U comparison uses eight items and 320 E/G pairs. Subsequent GPT
  coordinate studies use seven; haiku uses six. The union is nine, now including
  `sample_draw` in Appendix B with its designation-specific scope.
- PD's original swap contained TRUE arms. Removed the contrary historical claim.
- Retained PD as the only verified field effect, ID as a candidate, LL as
  withdrawn and unresolved, six conditional bounds, and AW as never independently
  pinned. Removed obsolete blanket claims that seven or nine parameters do nothing.
- Corrected the independent-sampling rationale: paired backgrounds control arm
  composition, but do not establish robustness to another background distribution.
- Replaced power guarantees with conditional interpretations. Additional ID
  collection needs an item-sensitive power analysis, not a fixed agent multiplier.
- Equivalence bounds are post-hoc individual unit-bootstrap bounds conditional on
  the tested items, not simultaneous or universally robust guarantees. TfA's
  wider item-bootstrap interval is disclosed.
- The full slope analysis has 16 fits, 15 usable standard errors and two ID
  disagreements. The failed PD swap TRUE slope fit is an exception, not a pass.
- Shortened repeated argument and historical commentary while preserving the
  main numeric tables, all four figures, limits, full prompt and item materials.
- Removed uncited bibliography entries. Completed Min, Rao and Yoo conference
  page ranges using their official ACL Anthology records. Lu and Sclar retain
  their preprint citation years and are consistently listed as those versions.

No frozen experiment, collection or analysis code, raw record, result file,
configuration or figure was changed. The figures are the existing frozen-data
exports. No new experiment was run.

## Verification

`verify.py` checks opening blanks, numbered pages, anonymous content and metadata,
A4 size, side margins, embedded page fonts, Arial body size and baseline spacing,
page budget, abstract length, retained key evidence, and identical PDF copies.
The final PDF was also rendered and visually reviewed for table/figure legibility,
clipping and pagination. `verification.json` records measured results; the build
log is checked for missing glyphs and overfull boxes.

Before uploading, enter the title, abstract and tutor information separately in
yoU@B as required by the guide. The PDF deliberately has no supervisor/title
page; this is not a removal of Camuffo from the project. No upload was performed.
