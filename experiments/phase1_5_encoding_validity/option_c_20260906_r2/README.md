# Option C — interrupted September run

Status verified 2026-09-06: **8,640/15,000 records; incomplete**.

The run stopped after a terminal HTTP 429 `credit_balance_exhausted` error.
There are 8,639 valid responses and one failed API observation; 6,360 planned
observations were not dispatched. Returned models on successful records match
`gpt-5.4-mini-2026-03-17`. Record integrity and frozen source hashes were verified.

The process has exited. No completed sweep or encoding-validity verdict follows
from this partial sample. Do not delete the failed record to resume. Restore
credits and document a continuation/restart protocol before further collection.

| Artifact | Purpose |
|---|---|
| [Manifest](manifest.json) | Frozen design, exact prompts, model, and source hashes |
| [Record checksums](record_checksums.json) | Integrity inventory of all 8,640 locally retained records |
| [Initial checkpoint](analysis/summary_cfcbd4c46056d445.md) | Ten-record operational checkpoint; not a validity test |
| [Partial report](analysis/summary_562653cd58340299.md) | Report generated when dispatch stopped |
| [Partial report data](analysis/summary_562653cd58340299.json) | Machine-readable missing/invalid accounting and partial estimates |

Raw request/response records and the failure log remain local under `records/`
and are excluded from Git. The checksums preserve their identities without
publishing the raw payloads. This designation follows the initial
invalid-credential attempt, with identical design hash; neither is overwritten.

See the [protocol](../../../docs/phase1_5_execution.md) and
[current project state](../../../NEXT_STEPS.md).
