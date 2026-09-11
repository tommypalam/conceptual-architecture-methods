# Concurrent comparison: repetition is not a repair candidate

All 720 approved attempt slots are accounted for: **719 valid responses and
one preserved timeout**. The timeout was never retried. The linked continuation
sent only the 381 previously unsent requests. Every parent byte and every raw
ZIP payload is verified; messages, profile values, seeds, model and cap stayed
unchanged. The collection had a documented transport pause.

**Formal status remains INVALID_SCREEN**, following the original rule that an
API failure invalidates this screen. The following are diagnostic contrasts,
not a clean confirmation or a phase pass. The failed response is included as
an unknown outcome in applicable conservative intervals, not silently dropped.

| Representation | Original .1 -> .9 ADOPT | Repeated .1 -> .9 ADOPT |
|---|---|---|
| Canonical hybrid | 18/60 -> 52/60 | 5/60 -> 5/60 |
| Numeric-only | 21/60 -> 47/59 valid; one unknown | 0/60 -> 1/60 |
| Verbal-only | 5/60 -> 37/60 | 0/60 -> 2/60 |

Primary verbal average difference (repeated minus original, equally weighting
endpoints) is **-.333**, conservative >=95% interval **[-.490,-.122]**.
These four primary cells contain no failed response, although the experiment's
overall invalidation rule still stands. The result points to lower ADOPT rates
with repetition under the tested setup, rather than merely a historical batch
comparison. It does not establish an internal mechanism or ethical correctness.

Original endpoint effects are +.567 for canonical (interval [.287,.772]),
+.447 among valid numeric responses (unknown-outcome envelope [.138,.685]),
and +.533 for verbal ([.265,.731]). Repeated endpoint effects are 0, +.017
and +.033 respectively, all with intervals including zero.

Direct repetition-minus-original changes in endpoint effects are -.567 for
canonical ([-.984,-.060]), -.430 for numeric ([-.787,.009]), and -.500 for
verbal ([-.827,-.092]). These secondary intervals are not family-adjusted.
They support a diagnostic concern about reduced sensitivity, distinct from
the primary average-rate shift. Numeric interaction uncertainty remains.

## Decision

Stop treating repetition as a repair to scale into the battery. The original
implementation remains the reference, with positive endpoint response in all
three representations in these diagnostic data. This does not erase its
original numeric slope-retention miss or the failed paraphrase battery.

A separately frozen, fresh **original full-curve representation confirmation**
is justified for MoR/S3: use all five values and contemporaneous canonical,
numeric and verbal conditions. The reference must qualify on its own; use the
original slope-retention rules and do not pool historical data. This addresses
one local representation question, not all ten parameters or all phase gates.
The pending design should report its selected scope explicitly.

Known token usage for this comparison is $0.7561365; the timeout has unknown
usage bounded by a $0.00496725 reservation. Cumulative known usage is
$2.7954015; conservative charge including the unknown is $2.80036875, leaving
approximately $6.20 of the previous $9 allowance. Provider balance is unverified.
No original definitions, theory, thresholds, agent integration or Phase 2
readiness changed. See [the detailed report](TIMEOUT_COLLECTION_REPORT.md).
