# Offline wording-sensitivity diagnosis

**Exploratory diagnosis only. Original gate, theory, prompts and saved observations are unchanged.**
Neutral context; original study seed 20260604; diagnostic simulation seed 20260909.

## Main results

- equivalent_saturated: 8/30 profiles.
- large_difference_supported: 1/30 profiles.
- observed_large_difference_uncertain: 17/30 profiles.
- within_margin_observed_but_not_established: 4/30 profiles.

The original result remains 8/30 equivalent. Categories below are explanatory,
not replacement gates. Parse eligibility is retained separately; one profile is below the original floor.

| Profile | Observed range (pp) | All four near same boundary? | Original equivalent? | Parse eligible? | Exploratory category |
|---|---|---|---|---|---|
| LL/S1 | 2.0 | True | True | True | equivalent_saturated |
| LL/S2 | 30.0 | False | False | True | observed_large_difference_uncertain |
| LL/S3 | 32.0 | False | False | True | observed_large_difference_uncertain |
| CS/S1 | 0.0 | True | True | True | equivalent_saturated |
| CS/S2 | 20.0 | False | False | True | observed_large_difference_uncertain |
| CS/S3 | 30.0 | False | False | True | observed_large_difference_uncertain |
| RT/S1 | 2.0 | True | True | True | equivalent_saturated |
| RT/S2 | 6.0 | False | False | True | within_margin_observed_but_not_established |
| RT/S3 | 14.0 | False | False | True | observed_large_difference_uncertain |
| MoR/S1 | 4.0 | True | False | True | within_margin_observed_but_not_established |
| MoR/S2 | 49.4 | False | False | False | observed_large_difference_uncertain |
| MoR/S3 | 24.0 | False | False | True | observed_large_difference_uncertain |
| RE/S1 | 0.0 | True | True | True | equivalent_saturated |
| RE/S2 | 0.0 | True | True | True | equivalent_saturated |
| RE/S3 | 50.0 | False | False | True | observed_large_difference_uncertain |
| PD/S1 | 0.0 | True | True | True | equivalent_saturated |
| PD/S2 | 28.0 | False | False | True | observed_large_difference_uncertain |
| PD/S3 | 60.0 | False | False | True | large_difference_supported |
| TfA/S1 | 4.0 | True | False | True | within_margin_observed_but_not_established |
| TfA/S2 | 12.0 | False | False | True | observed_large_difference_uncertain |
| TfA/S3 | 14.0 | False | False | True | observed_large_difference_uncertain |
| ID/S1 | 0.0 | True | True | True | equivalent_saturated |
| ID/S2 | 46.0 | False | False | True | observed_large_difference_uncertain |
| ID/S3 | 48.0 | False | False | True | observed_large_difference_uncertain |
| MS/S1 | 4.0 | True | False | True | within_margin_observed_but_not_established |
| MS/S2 | 40.0 | False | False | True | observed_large_difference_uncertain |
| MS/S3 | 28.0 | False | False | True | observed_large_difference_uncertain |
| AW/S1 | 2.0 | True | True | True | equivalent_saturated |
| AW/S2 | 18.0 | False | False | True | observed_large_difference_uncertain |
| AW/S3 | 40.0 | False | False | True | observed_large_difference_uncertain |

## Uncertainty and missing decisions

Construct exact Clopper–Pearson intervals for all 120 unique binomial rates, each at
confidence 1−.05/120. Bonferroni gives at least 95% simultaneous coverage under the
binomial sampling assumptions. Subtract interval endpoints to bound all 180 pair
differences simultaneously; no extra correction for overlapping pairs is needed.
For invalid parses, expand each rate interval over every possible allocation of those
unknown decisions, using the full 50-call denominator. This assumes each unparsed
response could correspond to either binary choice; it does not assign or repair it.
The bounds are deliberately conservative. Not exceeding the margin with these bounds
does not show equivalence or absence of a difference. Both saturation (.95/.05) and
the diagnostic categories are post-collection descriptive choices.

Method references: [SciPy exact binomial intervals](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.binomtest.html),
[NIST Bonferroni simultaneous coverage](https://www.itl.nist.gov/div898/handbook/prc/section4/prc473.htm).

## Precision simulation under true equality

All four true probabilities are identical within each simulation scenario. Trials
are independent binomial draws, with no missing responses. Every replicate uses the
unchanged six-pair TOST rule. These are simulated sampling properties, not extra API
observations, estimated real-world power, or authority to enlarge the completed study.
Intervals quantify Monte Carlo error only. Saturated probabilities and .50 are
hypothetical sensitivity scenarios, not fitted values chosen to justify a gate pass.

| N per formulation | True common rate | One-pair success | All-six success | MC 95% interval |
|---|---|---|---|---|
| 50 | 0.02 | 71.3% | 36.2% | 35.3%–37.2% |
| 50 | 0.10 | 6.6% | 0.1% | 0.1%–0.2% |
| 50 | 0.50 | 0.0% | 0.0% | 0.0%–0.0% |
| 50 | 0.90 | 6.5% | 0.2% | 0.1%–0.3% |
| 50 | 0.98 | 72.1% | 36.8% | 35.9%–37.8% |
| 100 | 0.02 | 98.5% | 94.9% | 94.5%–95.3% |
| 100 | 0.10 | 47.6% | 9.7% | 9.1%–10.3% |
| 100 | 0.50 | 0.0% | 0.0% | 0.0%–0.0% |
| 100 | 0.90 | 48.5% | 9.6% | 9.1%–10.2% |
| 100 | 0.98 | 98.4% | 94.9% | 94.4%–95.3% |
| 200 | 0.02 | 100.0% | 100.0% | 99.9%–100.0% |
| 200 | 0.10 | 89.8% | 64.3% | 63.4%–65.2% |
| 200 | 0.50 | 26.7% | 1.8% | 1.5%–2.0% |
| 200 | 0.90 | 89.1% | 64.7% | 63.7%–65.6% |
| 200 | 0.98 | 100.0% | 100.0% | 99.9%–100.0% |
| 400 | 0.02 | 100.0% | 100.0% | 100.0%–100.0% |
| 400 | 0.10 | 99.7% | 98.6% | 98.3%–98.8% |
| 400 | 0.50 | 74.9% | 35.1% | 34.1%–36.0% |
| 400 | 0.90 | 99.7% | 98.5% | 98.2%–98.7% |
| 400 | 0.98 | 100.0% | 100.0% | 100.0%–100.0% |

## Attribution limits

Each formulation rewrites all ten endpoint pairs simultaneously. A sensitive PD=.8
profile therefore does not identify PD wording as the cause. Formulation-wide
shifts, altered salience, response-format compliance, and interactions with the
fixed dilemma remain competing explanations. S1 agreement near a fixed choice
is not evidence that the parameters control that choice. The existing reasoning
audit also cannot resolve this because nine fixed means dominate aggregate accuracy.

No new data collection or theory revision is authorised by this analysis.
