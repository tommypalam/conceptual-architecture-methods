# MoR/S3 curve screen

Status: **CURVE_CRITERION_NOT_MET**.
300 calls; full-rate token estimate $0.373464; cumulative $1.526657.
Original allowance estimate remaining $7.473343; provider balance not checked.

| Arm | ADOPT counts /30 at .1/.3/.5/.7/.9 | Slope (95% CI) | LR p | h | Monotonic | Directional criterion |
|---|---|---|---|---|---|---|
| repetition | 0/1/1/5/12 | 6.188855325347497 ([3.1532420520986464, 9.224468598596347]) | 1.177427892629766e-07 | 1.369438406004566 | True | True |
| grounding | 4/9/5/11/19 | 2.6535590748751248 ([1.2862453444438473, 4.020872805306402]) | 5.3871097476476265e-05 | 1.0931447729592794 | False | False |

Direct endpoint-change contrast (grounding minus repetition):
```json
[
  {
    "parameter": "MoR",
    "problem": "S3",
    "contrast": "grounding endpoint change minus repetition endpoint change",
    "estimate": 0.09999999999999998,
    "ci95_conservative": [
      -0.6054367735758642,
      0.7757067708712586
    ],
    "inference": "Bonferroni-combined Clopper-Pearson endpoint intervals; independent binomial-call assumption"
  }
]
```

Primary: grounding directional criterion; repetition and arm contrast are secondary, not family-adjusted.
N=30 per cell; no historical pooling. Pinned/separated fits cannot satisfy the original criterion.
This tests one canonical parameter description on known S3. No representation retention, paraphrase
equivalence, reasoning faithfulness, internal understanding or phase-pass claim follows.
Model gpt-5.4-mini-2026-03-17; neutral; temperature 1; max output 600; root seed 20260917.
All exact requests, profiles, reservations and raw ZIP bytes verified. Backup is on the same computer.
