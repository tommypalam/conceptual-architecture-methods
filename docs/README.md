# Documents: the thesis, the paper and the project guides

[Back to the project](../README.md)

## Start here: the thesis

| | |
|---|---|
| **[thesis/LF3262767.pdf](thesis/LF3262767.pdf)** | **The thesis.** The single canonical PDF and the file uploaded to the university. The filename is the one the portal requires; the PDF itself carries no name or student number. |
| [thesis/thesis.md](thesis/thesis.md) | Its source. Edit this, never the PDF. |
| [thesis/abstract.txt](thesis/abstract.txt) | The abstract as pasted into the portal, which takes it separately and caps it at 4,000 characters. |
| [thesis/figures/](thesis/figures/) | The four figures, generated from the frozen records by [`code/phase6_thesis_figures.py`](../code/phase6_thesis_figures.py). |
| [thesis/build/](thesis/build/) | How the PDF is made and checked: [build.ps1](thesis/build/build.ps1), [preamble.tex](thesis/build/preamble.tex), [verify.py](thesis/build/verify.py), the [compliance note](thesis/build/COMPLIANCE.md) recording the university's rules, and the [last recorded verification](thesis/build/verification.json). |
| [thesis/history/](thesis/history/) | Superseded drafts kept because they exist nowhere else. Frozen; do not edit. |

**What the thesis claims, in one line.** Procedural Dependence is the only verified
field effect; Internalisation Dependence is a candidate; Legitimacy Locus is
withdrawn and unresolved; Affective Weighting was never independently pinned. It
establishes no semantic understanding, moral improvement or human resemblance.

**To rebuild**, from the repository root: `powershell -File docs/thesis/build/build.ps1`.
**To check** a build against the format rules: `python docs/thesis/build/verify.py`
(needs `pypdf` and `pdfplumber`). Rebuilding changes the PDF's bytes even when the
text is identical, so do not rebuild a copy that has already been submitted.

## The paper

The thesis is a condensed version of a longer paper with no page ceiling.

| | |
|---|---|
| [paper/paper_draft.md](paper/paper_draft.md) | *Which Parts of a Prompt Carry Behaviour?* — the full-length draft. |
| [paper/citation_verification.md](paper/citation_verification.md) | Every citation checked for existence and for making the claim attributed to it, with the two that failed. |

## Follow a result back to its evidence

- [Evidence index](../experiments/README.md) — every study, by phase.
- [Code guide](../code/README.md) — maps each thesis result to its design module,
  collector, evidence folder and offline analysis.
- [Phase 5 closure](../experiments/phase5_analysis/PHASE5_CLOSURE_2026-09-16.md) and
  [Phase 4B closure](../experiments/phase4_coding/PHASE4B_CLOSURE_2026-09-16.md) —
  what each phase did and did not establish.
- [Within-arm reanalysis](../experiments/phase5_analysis/reanalysis_20260914/ASSESSMENT.md)
  and [saturation diagnosis](../experiments/phase5_analysis/reanalysis_20260914/SATURATION_DIAGNOSIS.md) —
  why four early studies returned nulls, and the dispersion screen that followed.

## Reference documents

These stay at the top of `docs/` on purpose: frozen reports in `archive/` and
`experiments/` link to these exact paths, and frozen reports are never edited.

| Document | Use it for |
|---|---|
| [abstract.md](abstract.md) | The abstract with title and author, for reading. Must contain `thesis/abstract.txt` verbatim; `verify.py` checks that it does. |
| [variables.json](variables.json) | The codebook: exact parameter codes, endpoints and distributions. |
| [project_layout.md](project_layout.md) | Where files belong and how new work is named. |
| [pre_analysis_plan.md](pre_analysis_plan.md) | Historical hypotheses with current exploratory-policy guidance. |
| [phase1_5_results.md](phase1_5_results.md) | Phase 1.5 findings, uncertainty and limitations. |
| [research_programme.md](research_programme.md) | Researcher-supplied context beyond this thesis; not independently verified here. |
| [phase1_5_execution.md](phase1_5_execution.md), [phase1_5_followup.md](phase1_5_followup.md) | Two small redirect stubs. They exist only because frozen reports link to them; the originals are in the archive. |

Theory and specification live outside this folder, in [Theory/](../Theory/README.md).

## Records of what was published, and handoffs

| | |
|---|---|
| [publications/](publications/) | One dated record per publication to `main` (13–17 September): scope, branch targets and verification. Historical; their status statements are not current instructions. |
| [handoffs/](handoffs/) | [Desktop handoff](handoffs/desktop_handoff.md) for moving to another computer, its [transfer manifest](handoffs/desktop_transfer.json), and an earlier [chat handoff](handoffs/NEXT_CHAT_HANDOFF.md). |

## Current work

[NEXT_STEPS.md](../NEXT_STEPS.md) owns current status and remaining dependencies.
[CLAUDE.md](../CLAUDE.md) and [AGENTS.md](../AGENTS.md) hold the project rules and
the dated decision record. The [central archive](../archive/README.md) holds
historical documents by phase.
