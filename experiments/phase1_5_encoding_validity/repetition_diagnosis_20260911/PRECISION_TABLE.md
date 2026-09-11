# Sampling sensitivity of the observed-monotonicity check

Exact P(nondecreasing counts), conditional on specified independent-binomial probabilities.
This is not full-gate power, a probability that the fitted model is true, or a revised result.

| Assumed curve | N30 | N50 | N100 | N200 | N500 | N1000 |
|---|---|---|---|---|---|---|
| original_canonical | 86.4% | 94.9% | 99.5% | 100.0% | 100.0% | 100.0% |
| previous_repetition | 75.6% | 79.1% | 84.9% | 91.4% | 97.8% | 99.7% |
| previous_grounding | 49.2% | 63.5% | 83.5% | 96.1% | 99.9% | 100.0% |
| fresh_repetition | 30.4% | 39.8% | 58.6% | 79.8% | 97.0% | 99.8% |
| flat_half_counterexample | 2.1% | 1.7% | 1.4% | 1.2% | 1.1% | 1.0% |
| flat_verbal_floor_counterexample | 46.9% | 30.1% | 13.0% | 6.2% | 3.2% | 2.2% |

Positive curves use plug-in logistic fits to saved data; this smooth monotonic assumption is imposed, not established.
The two flat curves are counterexamples: ordering can occur without any parameter effect, especially through ties near a boundary.
Increasing N here is a hypothetical sensitivity calculation, not a sample-size recommendation or authorised allocation.
See precision_and_traces.json for fitted probabilities, expected counts, tie probabilities and exact source hashes.
