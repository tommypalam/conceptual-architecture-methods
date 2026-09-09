# Gradient extension — completed 2026-09-09

Collection and scoring are complete. The frozen retention criterion is met in
2 of 6 eligible comparisons. No eligible parameter/problem pair meets it in
both numeric-only and verbal-only representations. Phase 1.5 remains open.

Neutral configuration; root seed 20260604; exact model
`gpt-5.4-mini-2026-03-17`; temperature 1; output cap 600; concurrency 5.
Ten parameters x five values (.1, .3, .5, .7, .9) x three simple problems x
two representations x 50 calls per cell = 15,000 calls, across 300 cells.
The completed `option_c_20260909_restart` full-harness sweep is the hybrid
baseline. No historical September 6 responses were pooled.

## Completeness and provenance

- 15,000 unique records; 14,998 valid parses; two preserved parse failures;
  zero API failures or returned-model mismatches.
- All 300 cells have 50 records and at least 98% valid parses. The failures
  are verbal-only LL/S2 at .7 and numeric-only PD/S2 at .9 (49/50 valid each).
  Neither failure is in an eligible comparison below; neither was replaced.
- [Frozen analysis](cells_6f4ee2cee96409c4.json) contains all cell rates,
  Wilson 95% intervals, and all 60 gradient fits/comparisons.
- [Manifest](../manifest.json), [record inventory](../record_checksums.json),
  [usage](../token_usage.json), and [backup metadata](../local_backup.json)
  preserve the design and provenance. The ten-call checkpoint analysis is
  retained separately and is not the final result.
- Backup ZIP integrity was verified. It is on this computer under
  `output/validity_backups`, not an independent or off-device backup.
- Recorded usage: 11,389,500 input tokens, 1,333,082 output tokens, zero cached
  input tokens. At the previously checked $0.75/M input and $4.50/M output
  prices, the estimated token cost is **$14.54**, before taxes or other charges.
  This is below the pre-run $20–$55 estimate, not a billing reconciliation.

## Prespecified eligible comparisons

Eligibility requires that the original full-harness sweep met its complete
criterion. Retention requires complete data with at least 98% valid parses in
each cell, the predicted direction, and an absolute fitted logit-slope ratio
of at least .50 against that baseline. This is the existing point-estimate
rule; it is not a confidence-interval test of the slope ratio. The other 54
comparisons are not assessable under this rule, rather than 54 failures.

| Parameter/problem | Representation | Logit slope (Wald 95% CI) | Absolute slope ratio | Criterion |
|---|---|---|---|---|
| MoR / S3 | Numeric only | 2.271 (1.311, 3.231) | .454 | Not met |
| MoR / S3 | Verbal only | 2.811 (1.606, 4.017) | .562 | Met |
| PD / S1 | Numeric only | 6.988 (-1.763, 15.738) | .851 | Met |
| PD / S1 | Verbal only | Pinned: 250/250 chose A | Not estimable | Not met |
| MS / S2 | Numeric only | 2.181 (.592, 3.771) | .262 | Not met |
| MS / S2 | Verbal only | 2.421 (1.421, 3.421) | .290 | Not met |

All five estimable slopes above have the predicted positive direction. MoR and
MS retain detectable directional sensitivity, but several effects are smaller
than the specified retention threshold. Failure of that threshold does not
mean there is no parameter effect. For PD/S1, numeric-only first-option counts
are 48, 49, 50, 50, 50 out of 50 at increasing values: only three choices are B.
Its wide Wald interval includes zero despite the likelihood-ratio p=.022;
both diagnostics must be retained. The numeric criterion pass therefore does
not resolve the severe S1 ceiling limitation. Verbal-only PD/S1 is fully pinned.

These findings do not establish representation robustness for the full
ten-parameter architecture. No prompts, models, thresholds, sample sizes, or
accepted theory amendments were changed in response to the results. Reviewed
paraphrase equivalence and the final scientific gate review remain outstanding.
See the [updated evidence matrix](../../phase_review_20260909/evidence_7c6e7611aaf4b8b2.md).
