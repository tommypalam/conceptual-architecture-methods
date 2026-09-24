# Current state

**24 September 2026.** The project has two outputs, governed separately; see
[docs/PROJECT_SPLIT.md](docs/PROJECT_SPLIT.md) before editing either.

| | Where | Status |
|---|---|---|
| **Thesis** | `docs/thesis/LF3262767.pdf`, branch `thesis-final-20260919` | **submitted and frozen** — never rebuilt, never edited |
| **Paper** | `docs/paper/paper_draft.md` → `docs/paper/arxiv/preprint.pdf`, branch `paper-20260922` | **arXiv-ready**; not yet posted |

## What is pending, and who can do it

Only the author can do these:

1. **arXiv endorsement for `cs.CL`** — can take days; start first.
2. Read the three permanent statements in
   [docs/paper/arxiv/SUBMISSION.md](docs/paper/arxiv/SUBMISSION.md) once more
   before v1, then upload `preprint.tex` and `references.bib`.
3. After posting, add the arXiv identifier to `README.md` and `PROJECT_SPLIT.md`.

No paid collection is authorised. No collector is running.

## What is settled

56 designations, 35,879 frozen calls, $45.05 accounted. Every figure in the
paper is verified against its frozen `results.json`; all 36 robustness contrasts
reproduce exactly offline. Phase 7's findings are summarised in
[experiments/phase7_understanding/FINDINGS.md](experiments/phase7_understanding/FINDINGS.md).

## The next project, if taken up

The understanding question is structurally closed on the input side: reading a
definition and following an instruction phrased as one make identical
predictions on every test this harness can build. Progress needs open weights —
find a direction, ablate it, inject it. Hardware on hand: a 6700XT with 32 GB
DDR4, so prototype on CPU with a 1B model and rent a GPU only if the gate passes.
The gate is whether a small open model shows any field effect at all; zero cost,
one afternoon, and it either opens the project or closes it cleanly.

## The log

The running record of every phase, decision and result from 12 to 23 September
is preserved at
[archive/shared/documents/NEXT_STEPS_through_20260923.md](archive/shared/documents/NEXT_STEPS_through_20260923.md).
Decisions belong with their phase document; this file holds current state only.
