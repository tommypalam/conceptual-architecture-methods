# Offline repeat-stability audit

2026-09-12; no new model calls or spending. Phase1.5 diagnostic; original gates
and all raw data remain unchanged. This is post-result exploratory analysis.

Scope: the 18 behavioural source designations enumerated in
`code/audit_validity_repeat_stability.py`, covering the fresh September9 battery,
subsequent endpoint/wording screens, assembled axis pilot, completed repetition
allocation, later diagnostics and latest MS crossover. Assembled axis and
repetition directories represent their respective allocations once; recovery
snapshots and original partial copies are excluded to avoid double counting.
Claude coding/generation and interrupted September6 data are separate studies.
Only original system-delivery calls from the tool study enter these comparisons;
tool retrieval and tool-assisted final calls have different protocols.

Read from checksum-verified local ZIPs; verify current filename inventories and
manifest bytes against archives. This does not reverify every current loose file
against its ZIP. Verify every archived record hash and each manifest design hash;
reparse payload text using its original parser, including the source sweep
bare-label arm; verify provider IDs are unique across included valid
responses. Report invalid/failure exclusions explicitly. Retain full source
checksum and normalized metadata inventories locally. Do not alter archives.

Group exact role/content strings plus returned model, temperature, token limit
and label set. No whitespace normalization. **Seeds are not part of this key:**
this tests repeated prompts/settings, not identical complete requests. Inspect
same-prompt/same-seed coincidences separately. Include every prompt key with
N>=20 valid observations in each of at least two runs, and all eligible run
pairs. Within-run identical prompt occurrences are aggregated descriptively;
no cross-run pooling to claim a validation pass. All other groups are retained
in the full inventory. Profile hashes, timestamps, cache/token metadata and
backend fingerprints are reported without treating association as mechanism.

All between-run pairs: two-sided Fisher tests, Holm correction over the complete
family. Report differences and conservative nominal95 exact intervals; these
intervals are not family-adjusted. A separate family compares first versus
second chronological halves within every eligible prompt/run group. No
outcome-dependent cut point or prompt selection for the test families.

Report four named reference prompts regardless of outcome: canonical MS/S2 and
MoR/S3, each .1/.9, from the recent original expanded manifest. Also report the
largest absolute differences transparently as selected descriptive examples,
with the complete corrected family available. No significance means no resolved
difference, not equivalence. Fisher's fixed-probability/independence assumptions
may fail; discrepancies flag instability under that model without identifying
its cause. Run time, seed allocation, implementation and server state are not
randomized independently. Missing fingerprints cannot establish backend drift.

Use results to choose the next diagnostic, not select favourable past results
or weaken the phase gate. No new paid allocation is made by this audit.

Successful records from historical runners with multiple attempts remain included
and explicitly counted; their final recorded decision is the observation. This
audit does not claim the older battery used the later single-attempt policy.
