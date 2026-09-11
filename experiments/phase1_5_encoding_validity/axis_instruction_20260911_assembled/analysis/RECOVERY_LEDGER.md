# Numeric-axis pilot: collection recovery ledger

One approved 7,900-slot design was collected across five segments. Every
previously dispatched key was reserved, including failures. Subsequent segments
collected only never-dispatched keys from the original randomised schedule.
No failed slot was replaced and no historical experiment was pooled.

| Segment | Recorded | Valid | API failures | Reported-token cost (USD) |
|---|---:|---:|---:|---:|
| axis_instruction_20260910 | 3,016 | 3,012 | 4 connection errors | 3.3600720 |
| axis_instruction_20260910_continuation | 4 | 0 | 4 connection errors | 0.0000000 |
| axis_instruction_20260910_continuation_r2 | 1,864 | 1,863 | 1 timeout | 2.0832510 |
| axis_instruction_20260910_continuation_r3 | 56 | 55 | 1 timeout | 0.0611715 |
| axis_instruction_20260911_continuation_r4 | 2,960 | 2,960 | 0 | 3.3000750 |
| **Total** | **7,900** | **7,890** | **10** | **8.8045695** |

There are no parsing failures or returned-model mismatches. Failure records
have no returned model identity or reported usage. Provider-only retry charges
and taxes are not captured by these token estimates. The combined $12 dispatch
guard was retained across segments, not renewed for each continuation.
Approximately $39.881084 remains from the additional $50 after this pilot and
the preceding $1.3143465 endpoint diagnostic, subject to actual provider billing.

The first eight failures affect the P2/P3 equivalence cells (two per wording
per arm); the ninth affects revision/P1 equivalence; the tenth affects the
revision PD/S3=.7 sweep. Failed decisions remain unknown. The frozen equivalence
analysis reports valid-only results and exhaustive binary-completion sensitivity.
The original sweep criterion is retained, including its 98% valid-response floor.

The frozen overall local-screen flag disallows terminal API errors. That flag
is retained without override; the report separately shows whether equivalence,
saturation and the prespecified PD/S1 sweep criteria were met. Collection
completion does not imply scientific success or permission to start Phase 2.

Connection checks used read-only model-list requests and non-inference
completion-endpoint probes containing generic text. The cause of the transient
failures is not established. Collection was stopped overnight between September
10 and 11; original per-record timestamps preserve the gap. Randomised matched
baseline/revision scheduling was retained, but does not remove every possible
collection-time effect.

Original prompts, endpoint definitions, model, temperature, output cap, seed
derivation, planned N and statistical analysis stayed unchanged. New linked
manifests describe recovery allocation and inherited exact human approval.
The transport preparer was extended to admit timeouts; the frozen request
executor and retry policy were reused unchanged.

Nested snapshots preserve the earlier source directories and manifest hashes.
See [collection provenance](../collection_manifest.json),
[snapshot lineage](../recovery_snapshot.json),
[collection verification](collection_verification.json),
[final report](AXIS_PILOT_REPORT_v2.md), and
[ZIP metadata](../local_backup.json). Original raw records and ZIPs remain local;
same-computer copies are not off-device backups.
