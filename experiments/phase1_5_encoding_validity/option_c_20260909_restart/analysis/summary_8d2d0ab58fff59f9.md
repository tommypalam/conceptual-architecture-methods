# Phase 1.5 delivery comparison

NOT CLOSED: coherence, paraphrase and numeric/verbal tests also required

Records: 15000 / 15000. Missing and invalid calls are retained in the JSON accounting.

| Delivery | Parameter | Problem | Rates (.1/.3/.5/.7/.9) | Slope p | h | Monotonic | Direction | Sweep criterion |
|---|---|---|---|---|---|---|---|---|---|
| full_harness | LL | S1 | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 | pinned | 0.000 | True | not pre-specified | not assessable (no predicted sign) |
| full_harness | LL | S2 | 0.44 / 0.02 / 0.02 / 0.04 / 0.14 | 8.499e-05 | 0.684 | False | not pre-specified | not assessable (no predicted sign) |
| full_harness | LL | S3 | 0.40 / 0.68 / 0.42 / 0.58 / 0.92 | 1.423e-05 | 1.199 | False | not pre-specified | not assessable (no predicted sign) |
| full_harness | CS | S1 | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 | pinned | 0.000 | True | not pre-specified | not assessable (no predicted sign) |
| full_harness | CS | S2 | 0.00 / 0.04 / 0.02 / 0.04 / 0.08 | 0.04923 | 0.574 | False | not pre-specified | not assessable (no predicted sign) |
| full_harness | CS | S3 | 0.90 / 0.60 / 0.70 / 0.44 / 0.58 | 0.0001627 | 0.767 | False | not pre-specified | not assessable (no predicted sign) |
| full_harness | RT | S1 | 1.00 / 1.00 / 1.00 / 1.00 / 0.98 | separation | 0.284 | True | not pre-specified | not assessable (no predicted sign) |
| full_harness | RT | S2 | 0.10 / 0.12 / 0.06 / 0.00 / 0.08 | 0.1639 | 0.070 | False | not pre-specified | not assessable (no predicted sign) |
| full_harness | RT | S3 | 0.72 / 0.40 / 0.36 / 0.44 / 0.44 | 0.01947 | 0.576 | False | False | not met |
| full_harness | MoR | S1 | 1.00 / 0.98 / 1.00 / 1.00 / 0.98 | 0.6132 | 0.284 | False | not pre-specified | not assessable (no predicted sign) |
| full_harness | MoR | S2 | 0.02 / 0.18 / 0.04 / 0.32 / 0.42 | 4.354e-08 | 1.126 | False | not pre-specified | not assessable (no predicted sign) |
| full_harness | MoR | S3 | 0.10 / 0.26 / 0.42 / 0.76 / 0.84 | 8.476e-21 | 1.675 | True | True | met |
| full_harness | RE | S1 | 0.96 / 1.00 / 1.00 / 1.00 / 1.00 | separation | 0.403 | True | None | not met |
| full_harness | RE | S2 | 0.02 / 0.08 / 0.04 / 0.02 / 0.00 | 0.1989 | 0.284 | False | not pre-specified | not assessable (no predicted sign) |
| full_harness | RE | S3 | 0.74 / 0.48 / 0.30 / 0.68 / 0.28 | 0.001198 | 0.956 | False | True | not met |
| full_harness | PD | S1 | 0.94 / 0.98 / 1.00 / 1.00 / 1.00 | 0.004608 | 0.495 | True | True | met |
| full_harness | PD | S2 | 0.00 / 0.00 / 0.00 / 0.64 / 0.86 | 4.259e-42 | 2.375 | True | not pre-specified | not assessable (no predicted sign) |
| full_harness | PD | S3 | 0.86 / 0.70 / 0.66 / 0.22 / 0.08 | 4.376e-22 | 1.801 | True | not pre-specified | not assessable (no predicted sign) |
| full_harness | TfA | S1 | 1.00 / 1.00 / 0.98 / 0.98 / 1.00 | 0.6132 | 0.000 | False | False | not met |
| full_harness | TfA | S2 | 0.18 / 0.04 / 0.02 / 0.02 / 0.06 | 0.01538 | 0.381 | False | True | not met |
| full_harness | TfA | S3 | 0.40 / 0.22 / 0.50 / 0.60 / 0.72 | 3.848e-06 | 0.657 | False | not pre-specified | not assessable (no predicted sign) |
| full_harness | ID | S1 | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 | pinned | 0.000 | True | not pre-specified | not assessable (no predicted sign) |
| full_harness | ID | S2 | 0.02 / 0.08 / 0.00 / 0.08 / 0.06 | 0.4012 | 0.211 | False | True | not met |
| full_harness | ID | S3 | 0.40 / 0.22 / 0.40 / 0.16 / 0.62 | 0.0761 | 0.444 | False | not pre-specified | not assessable (no predicted sign) |
| full_harness | MS | S1 | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 | pinned | 0.000 | True | not pre-specified | not assessable (no predicted sign) |
| full_harness | MS | S2 | 0.00 / 0.02 / 0.06 / 0.14 / 0.60 | 2.929e-19 | 1.772 | True | True | met |
| full_harness | MS | S3 | 0.26 / 0.28 / 0.38 / 0.32 / 0.58 | 0.001469 | 0.661 | False | not pre-specified | not assessable (no predicted sign) |
| full_harness | AW | S1 | 1.00 / 1.00 / 1.00 / 0.98 / 1.00 | 0.4653 | 0.000 | False | not pre-specified | not assessable (no predicted sign) |
| full_harness | AW | S2 | 0.18 / 0.10 / 0.08 / 0.08 / 0.08 | 0.1052 | 0.303 | True | not pre-specified | not assessable (no predicted sign) |
| full_harness | AW | S3 | 0.20 / 0.60 / 0.22 / 0.36 / 0.72 | 0.0002588 | 1.099 | False | not pre-specified | not assessable (no predicted sign) |
| user_prefix_bare | LL | S1 | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 | pinned | 0.000 | True | not pre-specified | not assessable (no predicted sign) |
| user_prefix_bare | LL | S2 | 0.38 / 0.04 / 0.00 / 0.00 / 0.00 | 6.47e-15 | 1.328 | True | not pre-specified | not assessable (no predicted sign) |
| user_prefix_bare | LL | S3 | 0.04 / 0.14 / 0.12 / 0.38 / 0.12 | 0.01392 | 0.305 | False | not pre-specified | not assessable (no predicted sign) |
| user_prefix_bare | CS | S1 | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 | pinned | 0.000 | True | not pre-specified | not assessable (no predicted sign) |
| user_prefix_bare | CS | S2 | 0.00 / 0.00 / 0.00 / 0.00 / 0.12 | separation | 0.707 | True | not pre-specified | not assessable (no predicted sign) |
| user_prefix_bare | CS | S3 | 0.16 / 0.10 / 0.08 / 0.20 / 0.00 | 0.1112 | 0.823 | False | not pre-specified | not assessable (no predicted sign) |
| user_prefix_bare | RT | S1 | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 | pinned | 0.000 | True | not pre-specified | not assessable (no predicted sign) |
| user_prefix_bare | RT | S2 | 0.00 / 0.02 / 0.04 / 0.06 / 0.02 | 0.2738 | 0.284 | False | not pre-specified | not assessable (no predicted sign) |
| user_prefix_bare | RT | S3 | 0.14 / 0.14 / 0.10 / 0.16 / 0.10 | 0.6879 | 0.123 | False | False | not met |
| user_prefix_bare | MoR | S1 | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 | pinned | 0.000 | True | not pre-specified | not assessable (no predicted sign) |
| user_prefix_bare | MoR | S2 | 0.00 / 0.00 / 0.06 / 0.86 / 0.88 | 6.144e-47 | 2.434 | True | not pre-specified | not assessable (no predicted sign) |
| user_prefix_bare | MoR | S3 | 0.04 / 0.02 / 0.20 / 0.54 / 0.74 | 6.648e-24 | 1.669 | False | True | not met |
| user_prefix_bare | RE | S1 | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 | pinned | 0.000 | True | None | not met |
| user_prefix_bare | RE | S2 | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | pinned | 0.000 | True | not pre-specified | not assessable (no predicted sign) |
| user_prefix_bare | RE | S3 | 0.06 / 0.16 / 0.08 / 0.28 / 0.18 | 0.02394 | 0.381 | False | False | not met |
| user_prefix_bare | PD | S1 | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 | pinned | 0.000 | True | None | not met |
| user_prefix_bare | PD | S2 | 0.00 / 0.00 / 0.00 / 0.40 / 1.00 | separation | 3.142 | True | not pre-specified | not assessable (no predicted sign) |
| user_prefix_bare | PD | S3 | 0.72 / 0.36 / 0.46 / 0.02 / 0.00 | 4.912e-20 | 2.026 | False | not pre-specified | not assessable (no predicted sign) |
| user_prefix_bare | TfA | S1 | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 | pinned | 0.000 | True | None | not met |
| user_prefix_bare | TfA | S2 | 0.02 / 0.00 / 0.02 / 0.00 / 0.00 | 0.3008 | 0.284 | False | True | not met |
| user_prefix_bare | TfA | S3 | 0.08 / 0.06 / 0.30 / 0.32 / 0.58 | 4.141e-11 | 1.158 | False | not pre-specified | not assessable (no predicted sign) |
| user_prefix_bare | ID | S1 | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 | pinned | 0.000 | True | not pre-specified | not assessable (no predicted sign) |
| user_prefix_bare | ID | S2 | 0.00 / 0.00 / 0.02 / 0.00 / 0.02 | 0.3008 | 0.284 | False | True | not met |
| user_prefix_bare | ID | S3 | 0.20 / 0.18 / 0.12 / 0.10 / 0.06 | 0.01638 | 0.432 | True | not pre-specified | not assessable (no predicted sign) |
| user_prefix_bare | MS | S1 | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 | pinned | 0.000 | True | not pre-specified | not assessable (no predicted sign) |
| user_prefix_bare | MS | S2 | 0.00 / 0.00 / 0.00 / 0.08 / 0.20 | 1.29e-07 | 0.927 | True | True | met |
| user_prefix_bare | MS | S3 | 0.14 / 0.12 / 0.18 / 0.22 / 0.24 | 0.07971 | 0.257 | False | not pre-specified | not assessable (no predicted sign) |
| user_prefix_bare | AW | S1 | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 | pinned | 0.000 | True | not pre-specified | not assessable (no predicted sign) |
| user_prefix_bare | AW | S2 | 0.00 / 0.00 / 0.00 / 0.04 / 0.00 | 0.3008 | 0.000 | False | not pre-specified | not assessable (no predicted sign) |
| user_prefix_bare | AW | S3 | 0.02 / 0.04 / 0.14 / 0.08 / 0.30 | 1.411e-05 | 0.875 | False | not pre-specified | not assessable (no predicted sign) |

Unadjusted p<0.05 follows spec 4.1; no new directional hypotheses inferred.

The alternative delivery retains the profile and scaffold. Headroom is measured, not assumed. The two arms jointly vary message role and requested response format; this is a delivery-package contrast, not attribution to either component alone.
