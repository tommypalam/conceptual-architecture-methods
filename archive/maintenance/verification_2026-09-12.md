# Archive cleanup verification

Date: 12 September 2026. Branch: `project-cleanup-20260912`.

## Completed checks

| Check | Result |
|---|---|
| Explicit source-to-destination moves | 34 |
| Relocated files | 26,462; 97,050,911 bytes |
| Relocated SHA-256/size comparison | Every destination matches its original bytes |
| Retained experiment/source files | 132,487; 1,116,059,065 bytes, all unchanged |
| Git content preservation | All 26,456 relocated tracked files retain their original blob IDs; four ignored generation responses remain ignored |
| Current documentation links | 622 checked; zero missing |
| Offline test suite | 149 passed, including eight archive safety tests |
| Archived link resolution | 183 references resolved; zero unresolved |
| Human-readable text audit | 384 Markdown/text files at scan time; 208 archived originals, 145 frozen/versioned sources, 31 current documents |
| Current stale-status scan | Zero matches for the audited obsolete Phase 1.5/baseline statements |
| Generated cache cleanup | 102 cache files removed; no research record deletion |

The text scan deliberately excludes raw response bodies. Historical and frozen
statements are preserved, not rewritten as current claims. The audit counts
precede this new verification page. Current link validation is recorded in
[current_links_2026-09-12.json](current_links_2026-09-12.json).

## What changed

The former Phase 0 question archive moved to `archive/phase0/question_revisions/`.
All 26,241 files in the former Phase 0b archive moved to `archive/phase0b/runs/`.
Retired candidate prompts, old execution guides, early paraphrase candidates,
abandoned confirmation drafts and historical decision snapshots were consolidated
under phase or shared folders. Full records remain preserved, including failures.

The active decision log, objective, baseline README and documentation indexes now
point to accepted current results. The broader programme and pre-analysis draft
have current status text; scientific hypotheses and locked definitions were not
revised. Two short redirect pages keep links from frozen reports working.

The only execution-source edits are archive/candidate paths in the non-frozen
`run_recalibrate.py` and `run_nulla_tasksweep.py` CLIs. The new offline maintenance
tool checks workspace containment, refuses collisions, detects source changes,
and verifies moved bytes. It has no model client. No API calls were made.

## Provenance

- [Migration plan](migration_plan_2026-09-12.json)
- [Per-file source/destination/hash inventory](migration_inventory_2026-09-12.json)
- [Retained-file verification](retained_verification_2026-09-12.json)
- [Text classification audit](text_audit_2026-09-12.json)
- [Compatibility redirects](compatibility_links_2026-09-12.json)
- [Historical reference resolution](historical_references_2026-09-12.json)
- [Cache cleanup](cache_cleanup_2026-09-12.json)

The full retained-file snapshot is local at
`output/cleanup_retained_inventory.json`; its SHA-256 is
`ca61f665da6486be5f4dd07dbe0127e5c00e0ac26bcd9e3340f33789a3816441`. It contains file metadata and hashes, not response
contents. The checks establish local byte preservation; they do not establish
an off-device backup or repair the missing responses from earlier runs.

No original experimental outcome, threshold or phase claim was revised by this
maintenance work. Phase 1.5 remains closed for the accepted limited objective;
the original full battery remains unmet.
