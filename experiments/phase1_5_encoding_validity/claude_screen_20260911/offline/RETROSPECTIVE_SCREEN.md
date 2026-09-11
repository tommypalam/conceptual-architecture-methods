# A small screen applied to existing OpenAI data

This one retrospective worked example uses the first 20 call indices of each original baseline formulation: 80 existing responses, zero new API calls. The full-sample outcomes were already known. No alternative subsets, seeds or sample sizes were searched.

| Wording | ADOPT / valid | Rate | Pointwise Wilson 95% interval |
|---|---:|---:|---|
| canonical | 1/20 | 0.050 | 0.009 to 0.236 |
| paraphrase_1 | 6/20 | 0.300 | 0.145 to 0.519 |
| paraphrase_2 | 14/20 | 0.700 | 0.481 to 0.855 |
| paraphrase_3 | 2/20 | 0.100 | 0.028 to 0.301 |

P2 minus P3: 0.600; conservative exact interval 0.078 to 0.889.
The proposed gross-failure rule detects an effect beyond the .10 margin in this subset: **False**.

This illustrates the screening procedure on a known failure. It does not estimate general power, validate the chosen sample size or predict Claude performance. Failure to detect a gap in a future small sample would remain inconclusive, not evidence of equivalence.
Numerical evidence and all selected hashes: [retrospective_c0106a7dbff227b3.json](retrospective_c0106a7dbff227b3.json).
