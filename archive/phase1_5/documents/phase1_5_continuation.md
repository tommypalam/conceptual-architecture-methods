# Phase 1.5 cross-computer continuation

2026-09-09. Branch: `phase1-5-validity`. No new paid calls have been made.

The user authorised collecting the unfinished sweep on this computer and merging
later. Original response payloads remain on another computer; Git includes only
their inventory. Never fabricate responses from checksums or count absent payloads
as locally available observations.

`code/run_validity_continuation.py` is a separate wrapper; the scientific runner
and its frozen source hashes remain unchanged. Its default is preparation only.
The prepared `experiments/phase1_5_encoding_validity/option_c_20260909_shard`
retains the original manifest, source inventory, and a wrapper provenance ledger.
All 8,640 inventoried keys are reserved, including the unidentified failed call.
Only the 6,360 never-inventoried slots can be dispatched now. The failed slot
requires its original payload before a separately linked replacement attempt.

After configuring the OpenAI key, run an operational checkpoint:

```powershell
$env:OPENAI_API_KEY = [Environment]::GetEnvironmentVariable('OPENAI_API_KEY', 'User')
python -B code/run_validity_continuation.py --source-root experiments/phase1_5_encoding_validity/option_c_20260906_r2 --run-root experiments/phase1_5_encoding_validity/option_c_20260909_shard --missing-only --execute --limit 10
```

Remove `--limit 10` after checking credentials, exact model identity, and record
integrity to resume the remaining shard slots. Configuration is neutral, N=50
per cell, ten parameters, five values, three problems, two deliveries; original
target 15,000; seed 20260604; snapshot gpt-5.4-mini-2026-03-17; temperature 1;
output cap 600; concurrency at most five. No outcome-based stopping or selection.
New terminal failures stop dispatch and remain preserved.

The shard's analysis is partial and cannot close the source sweep or Phase 1.5.
Raw records remain in the project's ignored `records/` directory: they need a
separate backup, since pushing Git does not back them up.

Recovery mode (omit `--missing-only`) requires every source payload and verifies
the inventory, design, request fields, model identities and record hashes before
creating a separate continuation. It copies every nonterminal response byte for
byte, including parse failures, and preserves original failures in their source.
Before combining the shard with that continuation, verify shard records against
the same deterministic schedule, reject overlapping keys, and record byte hashes
and both collection periods in the merge ledger. A merge has not yet occurred.

Verification: 19 existing validity tests and four continuation tests passed.
Coverage includes interrupted copy/checkpoint resumption, no duplicate dispatch,
source preservation, absent-source sharding, corruption and inventory-change
rejection. Both production source hashes and the rebuilt design match the frozen
manifest. Claude generation/audit and human paraphrase review remain pending.
