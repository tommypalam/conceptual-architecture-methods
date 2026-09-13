# Phase 3: human-benchmark preparation

**All five canonical/alternative pairs passed independent structural review.**
Phase 3 remains open: recognition screening and agent population collection have
not started. The reviews assess operational text structure; they do not establish
human resemblance, equal perceptual difficulty or ethical understanding.

Start with the [checked assessment](variants_r3/ASSESSMENT.md), which records each
reviewer's caveats and our bounded interpretation. The current evidence is:

| Completed work | API calls | Conservative cost |
|---|---:|---:|
| Initial independent design review | 1 | $0.0793452 |
| No-peer perception checks (18/18 lines; 18/18 colours) | 36 | $0.010098 |
| Earlier truncated consultation, full reservation retained | 1 | $0.248127 |
| Five generated alternative candidates | 5 | $0.04751175 |
| Independent review of five repaired pairs | 5 | $0.031317 |
| **Total** | **48** | **$0.41639895** |

Generation plus the latest reviews cost $0.07882875. Provider totals are
$0.3587892 Claude and $0.05760975 OpenAI, leaving $14.6412108 and $29.94239025
under the researcher's separate $15/$30 caps. Package accounting, including
Phase 2, is $23.322471975 against $100. These are conservative usage estimates,
not verified invoices or provider balances. Existing validation-stage allocations
remain binding; no extra batch is queued by this checkpoint.

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

All 48 offline Phase 3 tests passed at candidate freeze. The newest verifier
reconstructs generation/review manifests, replays all ten responses without API
calls, checks derived results against raw records, and verifies historical
scientific inputs and archives. The current local archive has 145 JSON members:
`output/phase3_structural_review_20260913.zip`. Its checksum is in the checkpoint.
Raw records and archives are excluded from Git; off-device backup is unverified.
The historical failed consultation remains preserved and fully accounted.

## Next release work

Assemble the actual visual/sequential stimulus bundles and verify state, role,
action-schema and peer-schedule contracts offline. Recognition requests must
show actual task content while excluding answer keys, agent profiles, context
labels and identifying benchmark names.

Then freeze the specified 50 recognition responses per form across five pairs
(500 judge calls), two independent raters, disagreement adjudication, missingness
rules and the complete cost bound. More than 15 recognitions in 50 rejects an
alternative. Do not repeat accepted generation, structural reviews or perception
checks merely to resume; substantive changes need a linked prospective revision.

Population work remains downstream of recognition. All five families and ten
coordinates remain in scope, with high/low contexts, modulators and dependency
sensitivity still to be frozen for collection. Full D=100 replication and total
trajectory costs need a feasible budget resolution; neither a full Phase 3 pass
nor completion of omitted Phase 2 configurations is claimed.
