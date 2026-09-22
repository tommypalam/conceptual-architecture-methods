# arXiv submission — what is ready and what you must do

**Built and verified 22 September 2026.** `preprint.pdf`, 12 pages, builds clean
with no missing characters.

## Files here

| File | Purpose |
|---|---|
| `preprint.pdf` | the compiled paper — what a reader sees |
| `preprint.tex` | TeX source; **arXiv wants this**, not the PDF alone |
| `references.bib` | 15 entries, all from the verified record |
| `abstract.txt` | 1,914 characters, plain text, for the submission form (limit 1,920) |
| `preamble.tex`, `build.ps1` | the toolchain; rebuild with `powershell -File docs/paper/arxiv/build.ps1` |

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
5. **Upload.** Submit `preprint.tex` plus `references.bib`. arXiv compiles it
   itself; do not upload only the PDF unless the TeX fails to compile there.

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
