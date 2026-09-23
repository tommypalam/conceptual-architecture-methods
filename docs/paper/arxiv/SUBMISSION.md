# Publication package

Revised 23 September 2026 on `paper-20260922`.

**Title:** Which Part of a Prompt Carries Behaviour?

**Subtitle:** Separating Names, Numbers, and Definitions in Structured Prompts

**Author:** Tommaso Piero Palamenga, Bocconi University.

The paper is prepared locally. It has not been submitted or posted by this
revision. The submitted thesis is a separate, unchanged document.

## Files

- `preprint.pdf`: the revised reading copy.
- `preprint.tex`: generated LaTeX with the rendered reference list.
- `abstract.txt`: the same abstract as the paper, in plain text.
- `references.bib`: the 19 cited references; verification is recorded in
  [citation_verification.md](../citation_verification.md).
- `preamble.tex`, `build.ps1`, `build.sh`: build configuration.
- `../figures/fig1_forest.pdf`, `../figures/fig2_items.pdf`: required figures.
- `../../../output/pdf/Palamenga_Prompt_Field_Controls_source.zip`: upload archive
  containing only the generated TeX and the two required figure PDFs.

## Build and reproduce

From the repository root:

```powershell
python docs/paper/analysis/paper_item_robustness.py experiments tmp/pdfs/recomputed_robustness.json
powershell -File docs/paper/arxiv/build.ps1
```

The analysis requires NumPy and SciPy. Building requires Pandoc, XeLaTeX, and
the TeX packages used by `preamble.tex`. The source uses TeX Live font filenames
instead of operating-system font names, following arXiv's font-loading guidance.
These commands do not collect responses.

## Submit the prepared version

For an arXiv preprint, the suggested primary category is `cs.CL`; `cs.AI` is a
possible cross-list. Upload the source ZIP, select XeLaTeX, and inspect the PDF
produced by arXiv. The archive has its figures at the paths referenced by the
TeX and already contains the rendered bibliography, so it needs no separate
BibTeX run. Local compilation is checked; arXiv's server compilation still needs
checking during submission.

Use the title, subtitle if desired in the title field, author details, and
`abstract.txt` consistently. Account access, any endorsement requested by arXiv,
category, licence, and final submission remain author choices. Repository
visibility and access to supporting records should be checked from a signed-out
browser before posting; this revision did not establish anonymous access to the
GitHub repository. No licence was selected on the author's behalf.

Official instructions checked for this package:
[submission overview](https://info.arxiv.org/help/submit/index.html),
[TeX uploads](https://info.arxiv.org/help/submit_tex.html), and
[XeLaTeX and font loading](https://info.arxiv.org/help/faq/texlive.html).

## Scope of the revision

The paper distinguishes a verified contribution from one field from a
decomposition of the entire profile effect; restores the prespecified status
of CANON-minus-FLIP; corrects payoff, replication, multiple-testing, and
presentation-order claims; and reports the mixed floor-lift evidence without
assigning PD an established status-quo interpretation. All nine base stimuli,
seven twin scenarios, the full central prompt, and complete probe definitions
are included. The main limitation remains one task family and one model for
the full identification sequence.

See [REVISION_20260923.md](../REVISION_20260923.md) for evidence and validation.
No new experiment is required to present the completed work at its stated scope.
