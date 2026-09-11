# Joint-profile wording screen

Status: **GROSS_LOCAL_WORDING_FAILURE_DETECTED**.
480 fresh calls;480 valid; known cost$0.515651.
Cumulative conservative charge$3.899548; remaining$5.100452.

| Wording | PD | MoR | ADOPT / valid | Wilson95% interval |
|---|---|---|---|---|
| canonical | 0.1 | 0.1 | 26/30 | [0.703186733179637, 0.9469034451594526] |
| canonical | 0.1 | 0.9 | 30/30 | [0.8864866068260312, 0.9999999999999999] |
| canonical | 0.9 | 0.1 | 2/30 | [0.018477023791270378, 0.2132345836261692] |
| canonical | 0.9 | 0.9 | 8/30 | [0.14182663319596317, 0.4444796169518888] |
| paraphrase_1 | 0.1 | 0.1 | 30/30 | [0.8864866068260312, 0.9999999999999999] |
| paraphrase_1 | 0.1 | 0.9 | 30/30 | [0.8864866068260312, 0.9999999999999999] |
| paraphrase_1 | 0.9 | 0.1 | 0/30 | [0.0, 0.11351339317396876] |
| paraphrase_1 | 0.9 | 0.9 | 21/30 | [0.5212421254128504, 0.8333525173175619] |
| paraphrase_2 | 0.1 | 0.1 | 20/30 | [0.4878005164454384, 0.8076950191632386] |
| paraphrase_2 | 0.1 | 0.9 | 30/30 | [0.8864866068260312, 0.9999999999999999] |
| paraphrase_2 | 0.9 | 0.1 | 4/30 | [0.053096554840547455, 0.296813266820363] |
| paraphrase_2 | 0.9 | 0.9 | 29/30 | [0.8332960900859082, 0.9940914096183874] |
| paraphrase_3 | 0.1 | 0.1 | 27/30 | [0.7437891742081593, 0.9654001112526658] |
| paraphrase_3 | 0.1 | 0.9 | 30/30 | [0.8864866068260312, 0.9999999999999999] |
| paraphrase_3 | 0.9 | 0.1 | 1/30 | [0.005908590381612455, 0.16670390991409173] |
| paraphrase_3 | 0.9 | 0.9 | 25/30 | [0.6643564949358398, 0.9266345762815145] |

Primary:24 wording-pair contrasts, with simultaneous>=95% intervals from16 exact cell bounds.
Pairs with interval entirely outside+/-.10: 1.
```json
[
  {
    "pd_value": 0.1,
    "mor_value": 0.1,
    "a": "canonical",
    "b": "paraphrase_1",
    "contrast": "b minus a",
    "difference": 0.1333333333333333,
    "simultaneous95_interval_unknown_envelope": [
      -0.17689859456119417,
      0.39900489710184117
    ],
    "gross_difference_over_10pp": false
  },
  {
    "pd_value": 0.1,
    "mor_value": 0.1,
    "a": "canonical",
    "b": "paraphrase_2",
    "contrast": "b minus a",
    "difference": -0.20000000000000007,
    "simultaneous95_interval_unknown_envelope": [
      -0.5997566446651815,
      0.2819975355608759
    ],
    "gross_difference_over_10pp": false
  },
  {
    "pd_value": 0.1,
    "mor_value": 0.1,
    "a": "canonical",
    "b": "paraphrase_3",
    "contrast": "b minus a",
    "difference": 0.033333333333333326,
    "simultaneous95_interval_unknown_envelope": [
      -0.33880625968536027,
      0.39134598414258615
    ],
    "gross_difference_over_10pp": false
  },
  {
    "pd_value": 0.1,
    "mor_value": 0.1,
    "a": "paraphrase_1",
    "b": "paraphrase_2",
    "contrast": "b minus a",
    "difference": -0.33333333333333337,
    "simultaneous95_interval_unknown_envelope": [
      -0.6166248696523762,
      0.07675945800742356
    ],
    "gross_difference_over_10pp": false
  },
  {
    "pd_value": 0.1,
    "mor_value": 0.1,
    "a": "paraphrase_1",
    "b": "paraphrase_3",
    "contrast": "b minus a",
    "difference": -0.09999999999999998,
    "simultaneous95_interval_unknown_envelope": [
      -0.3556744846725549,
      0.1861079065891338
    ],
    "gross_difference_over_10pp": false
  },
  {
    "pd_value": 0.1,
    "mor_value": 0.1,
    "a": "paraphrase_2",
    "b": "paraphrase_3",
    "contrast": "b minus a",
    "difference": 0.2333333333333334,
    "simultaneous95_interval_unknown_envelope": [
      -0.23866712313158966,
      0.6089659566931211
    ],
    "gross_difference_over_10pp": false
  },
  {
    "pd_value": 0.1,
    "mor_value": 0.9,
    "a": "canonical",
    "b": "paraphrase_1",
    "contrast": "b minus a",
    "difference": 0.0,
    "simultaneous95_interval_unknown_envelope": [
      -0.1937668195483888,
      0.1937668195483888
    ],
    "gross_difference_over_10pp": false
  },
  {
    "pd_value": 0.1,
    "mor_value": 0.9,
    "a": "canonical",
    "b": "paraphrase_2",
    "contrast": "b minus a",
    "difference": 0.0,
    "simultaneous95_interval_unknown_envelope": [
      -0.1937668195483888,
      0.1937668195483888
    ],
    "gross_difference_over_10pp": false
  },
  {
    "pd_value": 0.1,
    "mor_value": 0.9,
    "a": "canonical",
    "b": "paraphrase_3",
    "contrast": "b minus a",
    "difference": 0.0,
    "simultaneous95_interval_unknown_envelope": [
      -0.1937668195483888,
      0.1937668195483888
    ],
    "gross_difference_over_10pp": false
  },
  {
    "pd_value": 0.1,
    "mor_value": 0.9,
    "a": "paraphrase_1",
    "b": "paraphrase_2",
    "contrast": "b minus a",
    "difference": 0.0,
    "simultaneous95_interval_unknown_envelope": [
      -0.1937668195483888,
      0.1937668195483888
    ],
    "gross_difference_over_10pp": false
  },
  {
    "pd_value": 0.1,
    "mor_value": 0.9,
    "a": "paraphrase_1",
    "b": "paraphrase_3",
    "contrast": "b minus a",
    "difference": 0.0,
    "simultaneous95_interval_unknown_envelope": [
      -0.1937668195483888,
      0.1937668195483888
    ],
    "gross_difference_over_10pp": false
  },
  {
    "pd_value": 0.1,
    "mor_value": 0.9,
    "a": "paraphrase_2",
    "b": "paraphrase_3",
    "contrast": "b minus a",
    "difference": 0.0,
    "simultaneous95_interval_unknown_envelope": [
      -0.1937668195483888,
      0.1937668195483888
    ],
    "gross_difference_over_10pp": false
  },
  {
    "pd_value": 0.9,
    "mor_value": 0.1,
    "a": "canonical",
    "b": "paraphrase_1",
    "contrast": "b minus a",
    "difference": -0.06666666666666667,
    "simultaneous95_interval_unknown_envelope": [
      -0.3087724538343892,
      0.19183718544098435
    ],
    "gross_difference_over_10pp": false
  },
  {
    "pd_value": 0.9,
    "mor_value": 0.1,
    "a": "canonical",
    "b": "paraphrase_2",
    "contrast": "b minus a",
    "difference": 0.06666666666666667,
    "simultaneous95_interval_unknown_envelope": [
      -0.2919042288471947,
      0.39707526299443674
    ],
    "gross_difference_over_10pp": false
  },
  {
    "pd_value": 0.9,
    "mor_value": 0.1,
    "a": "canonical",
    "b": "paraphrase_3",
    "contrast": "b minus a",
    "difference": -0.03333333333333333,
    "simultaneous95_interval_unknown_envelope": [
      -0.30872033112695196,
      0.2545440457299861
    ],
    "gross_difference_over_10pp": false
  },
  {
    "pd_value": 0.9,
    "mor_value": 0.1,
    "a": "paraphrase_1",
    "b": "paraphrase_2",
    "contrast": "b minus a",
    "difference": 0.13333333333333333,
    "simultaneous95_interval_unknown_envelope": [
      -0.1768985945611938,
      0.3990048971018407
    ],
    "gross_difference_over_10pp": false
  },
  {
    "pd_value": 0.9,
    "mor_value": 0.1,
    "a": "paraphrase_1",
    "b": "paraphrase_3",
    "contrast": "b minus a",
    "difference": 0.03333333333333333,
    "simultaneous95_interval_unknown_envelope": [
      -0.19371469684095113,
      0.2564736798373901
    ],
    "gross_difference_over_10pp": false
  },
  {
    "pd_value": 0.9,
    "mor_value": 0.1,
    "a": "paraphrase_2",
    "b": "paraphrase_3",
    "contrast": "b minus a",
    "difference": -0.1,
    "simultaneous95_interval_unknown_envelope": [
      -0.39895277439440346,
      0.23960545485019555
    ],
    "gross_difference_over_10pp": false
  },
  {
    "pd_value": 0.9,
    "mor_value": 0.9,
    "a": "canonical",
    "b": "paraphrase_1",
    "contrast": "b minus a",
    "difference": 0.4333333333333333,
    "simultaneous95_interval_unknown_envelope": [
      -0.13426056684936083,
      0.8264664394432516
    ],
    "gross_difference_over_10pp": false
  },
  {
    "pd_value": 0.9,
    "mor_value": 0.9,
    "a": "canonical",
    "b": "paraphrase_2",
    "contrast": "b minus a",
    "difference": 0.7,
    "simultaneous95_interval_unknown_envelope": [
      0.19331489544397473,
      0.9228204850963164
    ],
    "gross_difference_over_10pp": true
  },
  {
    "pd_value": 0.9,
    "mor_value": 0.9,
    "a": "canonical",
    "b": "paraphrase_3",
    "contrast": "b minus a",
    "difference": 0.5666666666666667,
    "simultaneous95_interval_unknown_envelope": [
      0.01011162825123324,
      0.8940055137409226
    ],
    "gross_difference_over_10pp": false
  },
  {
    "pd_value": 0.9,
    "mor_value": 0.9,
    "a": "paraphrase_1",
    "b": "paraphrase_2",
    "contrast": "b minus a",
    "difference": 0.2666666666666667,
    "simultaneous95_interval_unknown_envelope": [
      -0.16006751147688847,
      0.5839970194232889
    ],
    "gross_difference_over_10pp": false
  },
  {
    "pd_value": 0.9,
    "mor_value": 0.9,
    "a": "paraphrase_1",
    "b": "paraphrase_3",
    "contrast": "b minus a",
    "difference": 0.13333333333333341,
    "simultaneous95_interval_unknown_envelope": [
      -0.34327077866962996,
      0.5551820480678951
    ],
    "gross_difference_over_10pp": false
  },
  {
    "pd_value": 0.9,
    "mor_value": 0.9,
    "a": "paraphrase_2",
    "b": "paraphrase_3",
    "contrast": "b minus a",
    "difference": -0.1333333333333333,
    "simultaneous95_interval_unknown_envelope": [
      -0.4396248243226948,
      0.2276065857745595
    ],
    "gross_difference_over_10pp": false
  }
]
```

Secondary nominal endpoint effects and their PD contrasts:
```json
[
  {
    "arm": "canonical",
    "mor_endpoint_effects_by_pd": {
      "0.1": {
        "difference": 0.1333333333333333,
        "conservative_95_interval_unknown_envelope": [
          -0.10546361327647413,
          0.33256506312506784
        ]
      },
      "0.9": {
        "difference": 0.2,
        "conservative_95_interval_unknown_envelope": [
          -0.1360692703420858,
          0.4791838992694477
        ]
      }
    },
    "high_pd_minus_low_pd_endpoint_effect": {
      "difference": 0.06666666666666665,
      "conservative_95_interval_unknown_envelope": [
        -0.5267424610238756,
        0.6352643933241011
      ]
    }
  },
  {
    "arm": "paraphrase_1",
    "mor_endpoint_effects_by_pd": {
      "0.1": {
        "difference": 0.0,
        "conservative_95_interval_unknown_envelope": [
          -0.13590067257572858,
          0.13590067257572858
        ]
      },
      "0.9": {
        "difference": 0.7,
        "conservative_95_interval_unknown_envelope": [
          0.34439771781425144,
          0.8684535138469454
        ]
      }
    },
    "high_pd_minus_low_pd_endpoint_effect": {
      "difference": 0.7,
      "conservative_95_interval_unknown_envelope": [
        0.14571740781577291,
        1.0375213833053434
      ]
    }
  },
  {
    "arm": "paraphrase_2",
    "mor_endpoint_effects_by_pd": {
      "0.1": {
        "difference": 0.33333333333333337,
        "conservative_95_interval_unknown_envelope": [
          0.019822568577692712,
          0.553554856334588
        ]
      },
      "0.9": {
        "difference": 0.8333333333333334,
        "conservative_95_interval_unknown_envelope": [
          0.4728482160746335,
          0.9691437358514334
        ]
      }
    },
    "high_pd_minus_low_pd_endpoint_effect": {
      "difference": 0.5,
      "conservative_95_interval_unknown_envelope": [
        -0.14863593307237727,
        0.9895351153702133
      ]
    }
  },
  {
    "arm": "paraphrase_3",
    "mor_endpoint_effects_by_pd": {
      "0.1": {
        "difference": 0.09999999999999998,
        "conservative_95_interval_unknown_envelope": [
          -0.11967820922378924,
          0.29001030865973576
        ]
      },
      "0.9": {
        "difference": 0.8,
        "conservative_95_interval_unknown_envelope": [
          0.43245788578467137,
          0.9523154016887435
        ]
      }
    },
    "high_pd_minus_low_pd_endpoint_effect": {
      "difference": 0.7000000000000001,
      "conservative_95_interval_unknown_envelope": [
        0.07408296781966506,
        1.102970081191411
      ]
    }
  }
]
```

No detected difference is not equivalence. This small local screen cannot pass the full paraphrase battery.
All three previously approved paraphrases used; exact retained meanings not revised. All ten values and original user message retained.
Model gpt-5.4-mini-2026-03-17; neutral; temperature1; max600;N30 per cell;seed20260923.
Exact requests, approval provenance, unique API IDs, reservations and raw ZIP bytes verified. Same-computer archive. No automatic expansion.
