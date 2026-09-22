# Two outputs, two branches, two sets of rules

This repository produces **two separate documents** from one body of evidence.
They have different audiences, different claims and different freeze status, and
conflating them is the main way this project could go wrong from here.

| | **The thesis** | **The paper** |
|---|---|---|
| Artefact | `docs/thesis/LF3262767.pdf` | `docs/paper/paper_draft.md` (long-form record: `paper_full_record.md`) |
| Branch | `thesis-final-20260919` | `paper-20260922` |
| Status | **SUBMITTED AND FROZEN** | in preparation |
| Audience | Bocconi examiners | interpretability / evaluation venue |
| Scope | the ten-parameter framework and what it established | one identification result and its controls |
| Evidence | phases 1–6, to 18 September 2026 | phases 1–7, including everything after |
| May change | **no** | yes |

## The thesis is closed

`docs/thesis/LF3262767.pdf` was submitted. Its SHA-256 is
`52df1c5aa6201cc12a53f06a7dd868826c4367b36b530228efa36a16119ff1a3` and it must
stay byte-identical: rebuilding changes the bytes even when the text does not, so
**a submitted PDF is never rebuilt**. Its branch is not developed further.

**Phase 7 is not in the thesis and is not added to it.** Some Phase 7 results
would strengthen it — field-weighted extremity is excluded, the partner field is
directly pinned — and some would weaken it: an invented field outperforms the
verified parameter, and that parameter does not behave as its name suggests. None
of that is retrofitted. The thesis stands as the document that was examined, and
its stated boundary is the one it was submitted with:

> PD verified, ID candidate, LL withdrawn and unresolved, AW never pinned.

If a reader needs the later evidence, they are pointed at the paper, not given a
revised thesis.

## The paper is the live document

The paper is **not a longer thesis**. It makes one claim — that behaviour tracks
the stated meaning of a prompt field, established by controls that exclude the
alternatives — and reports the evidence bounding that claim, including the
results that constrain the framework the thesis is about.

Consequences of the split, which are easy to get wrong:

- **The paper may contradict the thesis, and does.** The thesis leaves
  field-weighted extremity open; the paper closes it. The thesis treats the ten
  parameters as the object of study; the paper shows an invented field
  outperforming one of them. Both statements are correct about their own
  evidence, at their own dates. Neither document is edited to agree with the
  other.
- **The paper inherits the thesis's discipline, not its scope.** Frozen records,
  hash-pinned releases, preserved failures and prespecified analysis all carry
  over. The ten-parameter architecture does not: in the paper it is context for
  an identification method, not the subject.
- **Phase 7 belongs to the paper alone.** Its assessments live in
  `experiments/phase7_understanding/`, summarised in
  [FINDINGS.md](../experiments/phase7_understanding/FINDINGS.md).

## Branch rules

- `thesis-final-20260919` — frozen. No commits. Preserves the submitted state.
- `paper-20260922` — active. Paper work happens here.
- `understanding-programme-20260919` — Phase 7 collection, complete. Preserved as
  the record of how that evidence was produced; its history is the paper's
  provenance and is not rewritten.
- `main`, `backup-*` — publication and history as before.

## What blocks the paper, as of 22 September 2026

**Two cleared, one attempted and stopped. The paper is submittable; the
remaining limitation is stated rather than fixed.**

1. ~~Citations unverified.~~ **Done, 22 September.** All rows checked against
   source; two supplied citations did not exist and were removed rather than
   replaced; four entries corrected. The banner is off and §10 states verified
   status. Record: `docs/paper/citation_verification.md`.
2. **One item family.** Every result comes from seven workplace-resource
   vignettes with tied payoffs. The objection is not the count — the seven span
   four families — but that the *situation type* never varies: a workplace
   resource, an incumbent holder, a stated wish to keep, payoffs frozen at the
   same pair. It cannot be answered from existing data, and it is the same wall
   that blocked the understanding markers.
   **Attempted 22 September and stopped at the screen.**
   [civic_screen_r1](../experiments/phase7_understanding/civic_screen_r1/ASSESSMENT.md):
   14 civic candidates authored, review accepted with zero blocking issues,
   **3 usable of 14 against 6 required**. The failure is *not* the saturation
   that killed the previous seventeen wordings — 11 of 14 disperse — but
   presentation-order sensitivity: only 6 pass the order gap and 8 would have
   passed the screen rule this project used three days ago. The limitation
   therefore stands, with a **specific and addressable** diagnosis rather than a
   general one. Plan and rationale: [SECOND_FAMILY.md](../experiments/phase7_understanding/SECOND_FAMILY.md).
3. ~~Framing.~~ **Done, 22 September.** Restructured around one claim: 1,390
   lines to 664. The ten-field encoding is now context for an identification
   method rather than the subject, the claim sits at §5, and §8 Related work is
   written out rather than deferred. The long-form draft is preserved as
   `docs/paper/paper_full_record.md` — it holds the full coordinate map, the
   review-instability finding and the complete defect record, which are worth
   keeping but do not belong in a focused paper.

## What is settled and needs no further work

The identification result, its controls, and the scale of the record: 55
designations, 35,542 frozen calls, $44.91 accounted. Every figure in the paper has
been verified against its frozen `results.json`. One call is a preserved transport
failure, never retried, and the designation it halted was closed and
re-designated rather than resumed.
