# arXiv submission — what is ready and what you must do

**Rebuilt 23 September 2026** after a full revision (see the end of this file).
`preprint.pdf`, 19 pages including appendices, builds clean with a reference list.

## Files here

| File | Purpose |
|---|---|
| `preprint.pdf` | the compiled paper — what a reader sees |
| `preprint.tex` | TeX source; **arXiv wants this**, not the PDF alone |
| `references.bib` | 19 entries: 15 from the verified record, 4 added and verified 23 Sept (see `../citation_verification.md`) |
| `abstract.txt` | plain text for the submission form (limit 1,920 characters) |
| `preamble.tex`, `build.ps1`, `build.sh` | the toolchain; rebuild with `powershell -File docs/paper/arxiv/build.ps1` |
| `../figures/` | the two figures; **upload them with the TeX** (the TeX references `figures/fig1_forest.pdf` and `figures/fig2_items.pdf`) |

## Steps only you can do

1. **arXiv account and endorsement.** If you have never submitted to `cs.CL`,
   you will need an endorsement from an existing author in that category. This
   can take days, so start it before anything else. A supervisor is the obvious
   source.
2. **ORCID** — optional but worth having, and permanent.
3. **Categories.** Primary `cs.CL`; cross-list `cs.AI`. Consider `cs.HC` only if
   you want the persona-conditioning audience.
4. **Licence.** The default arXiv licence is fine for a preprint you may later
   submit to a conference. CC-BY is more permissive and some venues prefer it;
   either is compatible with an ACL/EMNLP submission.
5. **Upload.** Submit `preprint.tex` plus a `figures/` folder with both figure
   PDFs. The reference list is already rendered into the TeX, so no `.bib` is
   needed. arXiv compiles it itself; do not upload only the PDF unless the TeX
   fails to compile there.
6. **Make the repository public** (or remove the URL from the title footnote):
   the paper points readers to https://github.com/tommypalam/conceptual-architecture-methods.

## Before you press submit

**arXiv v1 is permanent.** Revisions are possible and visible; withdrawal is not
really. Three things in this paper are irreversible once posted and each is
correct, so read them once more and be sure you want them public:

- §5.2 reports that a field invented in an afternoon **outperforms** the
  encoding's verified parameter (+0.400 against +0.339).
- §5.3 reports that the parameter **does not behave as its name suggests**.
- The header states that the author's thesis is a **separate, frozen document**
  that this paper's later evidence constrains.

All three are defensible and all three are why the paper is credible. But they
are public statements about your own prior work, so they should be a decision
rather than an oversight.

## Known weaknesses a reviewer will raise

Stated here so they are not a surprise:

1. **One task family.** §7 says so; the attempted second family is reported.
2. **One model for the §5 identification.** Cross-provider work covers §4 only.
3. **No human comparison anywhere.**

None is fatal for a preprint. (1) and (2) are what would need addressing before
a main-conference submission.

## After posting

The arXiv identifier should be added to the repository README and to
`docs/PROJECT_SPLIT.md`, so the thesis and the paper can be told apart by anyone
who arrives at either.


## Revision of 23 September 2026

Rewritten around one claim — the definition carries the effect — with these changes:

- **Bibliography fixed.** The 22 Sept PDF had no reference list (citations were
  plain text, so citeproc rendered nothing). Citations are now `[@key]`.
- **Outcome stated plainly as keep-rate.** The frozen table labels keeping `good`;
  the paper reports the choice and attaches no moral reading.
- **§5.1 no longer claims "prose does not do what numbers do".** The instruction
  was not matched in meaning; §6.4's on-topic principle moves keep-rate as much as
  the block.
- **Item-level robustness for every contrast** (crossed agent × item bootstrap and
  item-level t-test; `docs/paper/analysis/`, zero API calls). The decisive
  estimand is now CANON − FLIP (−0.454, 7/7 items, robust); FLIP's own sign and
  the floor-lift dissociation are reported as unit-level only.
- **Models, temperature, output caps, agents and the full prompt** are stated;
  item texts and twin clauses in an appendix.
- **Two figures**, generated from the analysis JSON.
- Numbers checked by an independent pass against results.json / assessments; nine
  discrepancies found and corrected (e.g. two transport failures, not one; 17
  twin wordings, not eleven; review-instability counts attributed to the right
  pools; Worst-off Priority excluded from "follows its definition").
- **Known weaknesses unchanged:** one task family, one model for §6, no human
  comparison.
