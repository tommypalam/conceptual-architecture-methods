# Finite-rule pilot: descriptive results

Six assigned choices per task/arm. E: numeric profile; V: equivalent written percentages;
U: no profile; G: no profile plus ethical guidance. Credits are simulated units.
Good/not_good labels follow stipulated standards. They are not human moral judgments.
Bounds below identify the assigned mean if choices are missing; they are not confidence intervals.

| Task / arm | Action counts | Valid | Actor mean | Recipient means | Total mean | Fixed-good bounds | Relative-good bounds |
|---|---|---:|---:|---|---:|---|---|
| disclosure_2 / E | falsify: 0, report: 6, skip: 0 | 6 | -2.0 | [8.0] | 6.0 | [1.0, 1.0] | [1.0, 1.0] |
| disclosure_2 / V | falsify: 0, report: 6, skip: 0 | 6 | -2.0 | [8.0] | 6.0 | [1.0, 1.0] | [1.0, 1.0] |
| disclosure_2 / U | falsify: 0, report: 6, skip: 0 | 6 | -2.0 | [8.0] | 6.0 | [1.0, 1.0] | [1.0, 1.0] |
| disclosure_2 / G | falsify: 0, report: 6, skip: 0 | 6 | -2.0 | [8.0] | 6.0 | [1.0, 1.0] | [1.0, 1.0] |
| disclosure_12 / E | falsify: 0, report: 6, skip: 0 | 6 | -12.0 | [8.0] | -4.0 | [1.0, 1.0] | [0.0, 0.0] |
| disclosure_12 / V | falsify: 0, report: 6, skip: 0 | 6 | -12.0 | [8.0] | -4.0 | [1.0, 1.0] | [0.0, 0.0] |
| disclosure_12 / U | falsify: 0, report: 6, skip: 0 | 6 | -12.0 | [8.0] | -4.0 | [1.0, 1.0] | [0.0, 0.0] |
| disclosure_12 / G | falsify: 0, report: 6, skip: 0 | 6 | -12.0 | [8.0] | -4.0 | [1.0, 1.0] | [0.0, 0.0] |
| allocation_6 / E | equal: 6, skip: 0, unequal: 0 | 6 | 0.0 | [4.0, 4.0] | 8.0 | [1.0, 1.0] | [1.0, 1.0] |
| allocation_6 / V | equal: 6, skip: 0, unequal: 0 | 6 | 0.0 | [4.0, 4.0] | 8.0 | [1.0, 1.0] | [1.0, 1.0] |
| allocation_6 / U | equal: 6, skip: 0, unequal: 0 | 6 | 0.0 | [4.0, 4.0] | 8.0 | [1.0, 1.0] | [1.0, 1.0] |
| allocation_6 / G | equal: 6, skip: 0, unequal: 0 | 6 | 0.0 | [4.0, 4.0] | 8.0 | [1.0, 1.0] | [1.0, 1.0] |
| allocation_12 / E | equal: 6, skip: 0, unequal: 0 | 6 | 0.0 | [4.0, 4.0] | 8.0 | [1.0, 1.0] | [1.0, 1.0] |
| allocation_12 / V | equal: 6, skip: 0, unequal: 0 | 6 | 0.0 | [4.0, 4.0] | 8.0 | [1.0, 1.0] | [1.0, 1.0] |
| allocation_12 / U | equal: 6, skip: 0, unequal: 0 | 6 | 0.0 | [4.0, 4.0] | 8.0 | [1.0, 1.0] | [1.0, 1.0] |
| allocation_12 / G | equal: 6, skip: 0, unequal: 0 | 6 | 0.0 | [4.0, 4.0] | 8.0 | [1.0, 1.0] | [1.0, 1.0] |

## All planned paired contrasts

Bootstrap intervals use only six blocks and are conditional on these four tasks and rules.
Degenerate bootstrap intervals do not establish certainty; conservative bounds are also shown.
All category and aggregation rates, including not_good and neutral, remain in analysis.json.

| Task / contrast | Metric | Estimate | Bootstrap 95% | Hoeffding 95% |
|---|---|---:|---|---|
| allocation_12/E-U | fixed_good | 0.0 | [0.0, 0.0] | [-1, 1] |
| allocation_12/E-U | total_credits | 0.0 | [0.0, 0.0] | [-16, 16] |
| allocation_12/E-V | fixed_good | 0.0 | [0.0, 0.0] | [-1, 1] |
| allocation_12/E-V | total_credits | 0.0 | [0.0, 0.0] | [-16, 16] |
| allocation_12/G-U | fixed_good | 0.0 | [0.0, 0.0] | [-1, 1] |
| allocation_12/G-U | total_credits | 0.0 | [0.0, 0.0] | [-16, 16] |
| allocation_12/V-U | fixed_good | 0.0 | [0.0, 0.0] | [-1, 1] |
| allocation_12/V-U | total_credits | 0.0 | [0.0, 0.0] | [-16, 16] |
| allocation_6/E-U | fixed_good | 0.0 | [0.0, 0.0] | [-1, 1] |
| allocation_6/E-U | total_credits | 0.0 | [0.0, 0.0] | [-12, 12] |
| allocation_6/E-V | fixed_good | 0.0 | [0.0, 0.0] | [-1, 1] |
| allocation_6/E-V | total_credits | 0.0 | [0.0, 0.0] | [-12, 12] |
| allocation_6/G-U | fixed_good | 0.0 | [0.0, 0.0] | [-1, 1] |
| allocation_6/G-U | total_credits | 0.0 | [0.0, 0.0] | [-12, 12] |
| allocation_6/V-U | fixed_good | 0.0 | [0.0, 0.0] | [-1, 1] |
| allocation_6/V-U | total_credits | 0.0 | [0.0, 0.0] | [-12, 12] |
| disclosure_12/E-U | fixed_good | 0.0 | [0.0, 0.0] | [-1, 1] |
| disclosure_12/E-U | total_credits | 0.0 | [0.0, 0.0] | [-4, 4] |
| disclosure_12/E-V | fixed_good | 0.0 | [0.0, 0.0] | [-1, 1] |
| disclosure_12/E-V | total_credits | 0.0 | [0.0, 0.0] | [-4, 4] |
| disclosure_12/G-U | fixed_good | 0.0 | [0.0, 0.0] | [-1, 1] |
| disclosure_12/G-U | total_credits | 0.0 | [0.0, 0.0] | [-4, 4] |
| disclosure_12/V-U | fixed_good | 0.0 | [0.0, 0.0] | [-1, 1] |
| disclosure_12/V-U | total_credits | 0.0 | [0.0, 0.0] | [-4, 4] |
| disclosure_2/E-U | fixed_good | 0.0 | [0.0, 0.0] | [-1, 1] |
| disclosure_2/E-U | total_credits | 0.0 | [0.0, 0.0] | [-12, 12] |
| disclosure_2/E-V | fixed_good | 0.0 | [0.0, 0.0] | [-1, 1] |
| disclosure_2/E-V | total_credits | 0.0 | [0.0, 0.0] | [-12, 12] |
| disclosure_2/G-U | fixed_good | 0.0 | [0.0, 0.0] | [-1, 1] |
| disclosure_2/G-U | total_credits | 0.0 | [0.0, 0.0] | [-12, 12] |
| disclosure_2/V-U | fixed_good | 0.0 | [0.0, 0.0] | [-1, 1] |
| disclosure_2/V-U | total_credits | 0.0 | [0.0, 0.0] | [-12, 12] |
