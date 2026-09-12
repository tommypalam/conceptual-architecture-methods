# Structural encoding: diagnostics

**480/480 valid responses; token estimate $0.515599.**
Neutral context; 8 unselected backgrounds; draw seed 20261005, schedule 20261006, analysis 20261007.
Model gpt-5.4-mini-2026-03-17, temperature 1, maximum 600. One observation per background/condition.
All displayed rates use the target label shown; unpredicted contrasts use the first response label and remain exploratory. No background removed.

| Parameter | Problem | Representation | Target | Rates .1/.3/.5/.7/.9 | Endpoint (adjusted interval) | Interior (adjusted interval) | Ordered | Predicted endpoint supported |
|---|---|---|---|---|---|---|---|---|
| MoR | S3 | canonical | ADOPT | 37.5%/37.5%/50.0%/75.0%/75.0% | +0.375 [+0.000, +0.875] | +0.375 [-0.625, +1.000] | True | False |
| MoR | S3 | paraphrase_1 | ADOPT | 62.5%/75.0%/87.5%/100.0%/100.0% | +0.375 [+0.000, +0.875] | +0.250 [+0.000, +0.750] | True | False |
| MoR | S3 | paraphrase_2 | ADOPT | 50.0%/75.0%/62.5%/100.0%/100.0% | +0.500 [+0.000, +1.000] | +0.250 [+0.000, +0.750] | False | False |
| MoR | S3 | paraphrase_3 | ADOPT | 37.5%/62.5%/62.5%/87.5%/100.0% | +0.625 [+0.125, +1.000] | +0.250 [-0.500, +0.875] | True | True |
| MoR | S3 | numeric_only | ADOPT | 50.0%/50.0%/75.0%/62.5%/75.0% | +0.250 [-0.500, +0.875] | +0.125 [+0.000, +0.625] | False | False |
| MoR | S3 | verbal_only | ADOPT | 25.0%/12.5%/50.0%/50.0%/50.0% | +0.250 [-0.500, +0.875] | +0.375 [+0.000, +0.875] | False | False |
| MS | S2 | canonical | FORMAL_REPORT | 37.5%/12.5%/25.0%/12.5%/50.0% | +0.125 [-0.500, +0.750] | +0.000 [-0.500, +0.500] | False | False |
| MS | S2 | paraphrase_1 | FORMAL_REPORT | 25.0%/12.5%/37.5%/37.5%/37.5% | +0.125 [+0.000, +0.625] | +0.250 [-0.500, +0.875] | False | False |
| MS | S2 | paraphrase_2 | FORMAL_REPORT | 12.5%/25.0%/12.5%/37.5%/37.5% | +0.250 [+0.000, +0.750] | +0.125 [-0.500, +0.750] | False | False |
| MS | S2 | paraphrase_3 | FORMAL_REPORT | 37.5%/50.0%/50.0%/25.0%/50.0% | +0.125 [+0.000, +0.625] | -0.250 [-0.750, +0.000] | False | False |
| MS | S2 | numeric_only | FORMAL_REPORT | 37.5%/25.0%/12.5%/12.5%/12.5% | -0.250 [-0.750, +0.000] | -0.125 [-0.625, +0.000] | False | False |
| MS | S2 | verbal_only | FORMAL_REPORT | 37.5%/50.0%/62.5%/62.5%/62.5% | +0.250 [+0.000, +0.750] | +0.125 [+0.000, +0.625] | True | False |

[All curves](fig_01_all_curves.png) · [PDF](fig_01_all_curves.pdf)

Adjusted intervals protect both contrasts across 12 groups: 24 comparisons. Nominal 95% intervals and every background effect remain in [result_313c5ea5a071ca14.json](result_313c5ea5a071ca14.json).
Bootstrap coverage is approximate. Observed ordering is not proof of population monotonicity; lack of significance is not equivalence. An endpoint difference alone is not graded encoding.
These rates do not constitute a fresh original-battery pass, a moral-performance score, or evidence identifying a unique internal LLM mechanism.
The diagnostic panel is small and tests previously selected MoR/MS cases. The full sweep includes all thirty parameter/problem pairs; absent directional hypotheses are not counted as failures.

Exact requests, settings, unique returned IDs, raw reparsing and archive byte equality verified. No retries or replacements. No off-device backup claimed.
