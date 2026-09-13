# Phase 3: recognition probes complete; coding stopped

The approved screening saved **500 recognition probes**, then stopped after
28 valid Haiku coding batches when the next response changed one character in
an answer ID. The strict parser rejected that batch; no retry occurred.
OpenAI coding and discussion have not started. **No formal recognition verdict
exists; Phase 3 remains open and population collection is not released.**

Read the [current assessment](recognition_r1/execution/ASSESSMENT.md),
[verified checkpoint](recognition_r1/execution/CHECKPOINT.json) and
[continuation handoff](recognition_r1/execution/CONTINUATION.md).

| Work preserved | API calls | Conservative cost |
|---|---:|---:|
| Earlier design, perception, generation and structural review, including failed consultation | 48 | $0.416398950 |
| Recognition probes, all ten cells complete | 500 | $5.337931500 |
| Valid initial coding batches | 28 | $0.112679600 |
| Failed coding batch, full reservation retained | 1 | $0.031920900 |
| **Total** | **577** | **$5.898930950** |

This screening attempt used $5.482532000 of its $14.06743250 maximum. Provider
totals are $5.841321200 Claude and $0.057609750 OpenAI, within $15/$30 caps.
Package accounting including Phase 2 is $28.805003975 under $100. These are
conservative estimates, not verified balances. No paid call is queued.

All five pairs previously received independent structural text acceptance;
that does not establish low recognition, human resemblance, equal perceptual
difficulty or ethical understanding. Their domain caveats remain in the
[structural assessment](variants_r3/ASSESSMENT.md).

## Read the evidence

1. [Structural assessment and next gate](variants_r3/ASSESSMENT.md).
2. [Exact repaired candidates](variants_r3/candidates.json) and
   [tracked repair rationale](variants_r3/REPAIRS.md); generated originals remain
   in [generation results](variants_r2/generation_result.json).
3. [Canonical operational protocol](canonical_r2/PROTOCOL.md) and
   [frozen review manifest](variants_r3/review_manifest.json).
4. [Five review verdicts](variants_r3/review_result.json) and
   [48-call verification checkpoint](variants_r3/REVIEW_CHECKPOINT.json).
5. [Budget amendment](PROVIDER_BUDGET_20260913.md),
   [linked continuation](variants_r2/PROTOCOL.md), and
   [preserved reconciliation](variants_r2/reconciliation.json).
6. Historical [staged protocol](validation_20260913/PROTOCOL.md),
   [source erratum](validation_20260913/ERRATUM.md), and
   [truncated consultation disposition](resolution_20260913/CONSULTATION_OUTCOME.md).

The 65 offline tests passed before launch. After the stop, the local verifier
checked exact request and cost links, successful parser replay, frozen sources,
historical evidence and all 1,733 archive members with zero additional API calls.
The archive is `output/phase3_recognition_r1_20260913.zip`; its SHA256 is in the
current checkpoint. Raw records and archives are excluded from Git. Off-device
backup is unverified; both historical failures remain immutable and accounted.

## Next release work

Prepare the linked coding recovery described in the handoff. Reuse all 500
probes and 28 valid coding batches. Do not restart the failed runner or overwrite
its records. The original release excludes retries; a replacement requires an
explicit linked, costed and tested continuation. Complete two-rater coding and
bounded discussion before applying the fixed-denominator recognition gate.
More than 15 recognitions in 50 rejects an alternative; missing outcomes block
passing. No automatic new candidates or population collection follow.

All five families and ten coordinates remain in scope, with high/low contexts,
modulators and dependency sensitivity still to be frozen for collection. Full
D=100 replication and trajectory costs require a feasible budget resolution.
Phase 3 does not retrospectively complete omitted Phase 2 configurations.
