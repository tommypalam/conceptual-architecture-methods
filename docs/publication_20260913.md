# Publication and abstract revision — 13 September 2026

The researcher requested committing all completed work, publishing it to `main`,
preserving the previous `main` as an additional backup and retaining the original
backup. The publication source is `phase3-preparation-20260913`, including research
and viewer work through `9ba7dad2` and this documentation revision.

## Branch preservation

| Branch | Target |
|---|---|
| `backup` | Original backup, unchanged: `c8e7aa0bde3ce17bb8e36f367a2e15950aa6cd2d` |
| `backup-1` | Previous published main: `aaed0a8d6b2978b15bcc7e0253b7cdd63b56be9d` |
| `main` | The verified publication commit containing this record |

The fetched previous main is an ancestor of the publication source. Publication
uses a fast-forward with no force-push or history rewrite. The new backup is
published and checked before main is advanced; the original backup is checked
again afterward. This records the intended publication transaction; Git remote
refs are authoritative for its completion.

## Included work

- Completed amended Phase 2 pilot and confirmation, analyses and provenance.
- Read-only group replay viewer, Blender environments and desktop interface.
- Phase 3 protocols, recognition outcomes and completed E/U and E/V diagnostics.
- Current status, continuation guidance and a conventional paper abstract.

Ignored raw records, local archives and editable Blender output remain local.
The Git branches preserve versioned work, not a complete off-device research-data
backup. No frozen experiment source or raw response is changed by this revision.
No paid collection is launched or new Phase 3 validation amendment adopted.

## Abstract review

The revised [abstract](abstract.md) presents the research question, theoretical
representation, method, principal findings and contribution without phase labels,
execution history or editorial instructions. It describes completed evidence in
paper style and does not invent results for unfinished studies. Detailed scope
amendments remain in [current status](../NEXT_STEPS.md), the
[accepted encoding closure](../experiments/phase1_5_encoding_validity/ACCEPTED_CLOSURE_2026-09-12.md)
and the individual study reports.

Concise review: conceptual framing distinguishes prompt-level normative influence
from intrinsic understanding; psychological interpretation does not equate AI
choices with human behaviour; statistical wording retains the six primary and
one-of-seven secondary corrected findings and the inconclusive prose comparison;
architectural scope retains all ten coordinates without claiming full validity;
reproducibility language is supported by saved protocols, records and replay tools.
The review is editorial, not independent expert or human validation.

## Verification before publication

- The initial offline Phase 2/3 suite ran 145 tests: 144 passed and one old
  recognition mock test failed because it rebuilt an early release against the
  expanded current ledger, which now contains later model types and studies.
- The test now loads the original frozen release and its 48-record archive,
  checking the archive hash, historical records, preserved files and source hashes.
  Frozen production code, releases, records and results remain unchanged.
- All eight tests in the affected recognition module then passed, including its
  610-response mock pipeline and zero-call replay. All 145 tests are thus covered
  by passing results across the initial run and focused rerun. Test charges and
  responses are synthetic; no paid API collection occurred.
- The abstract has 266 words. All 36 local links checked across the abstract,
  publication record, handoff and current-status document resolve. The companion
  constitutions match apart from their title filenames; `git diff --check` passes.
- Remote `backup-1` was verified at the previous main tip before publication,
  and `backup` was verified unchanged. Remote tips are checked again after push.
