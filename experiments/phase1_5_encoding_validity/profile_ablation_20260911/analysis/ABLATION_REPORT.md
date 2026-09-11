# Background-profile ablation diagnostic

Status: **MORE_POSITIVE_SLOPE_UNDER_DELETION**.
300 fresh calls; known cost $0.270473; cumulative known $3.065874.
Conservative charge including prior unknown timeout $3.070841; original allowance remaining $5.929159.

| Arm | ADOPT counts /30 at .1/.3/.5/.7/.9 | Slope (95% CI) | Original directional criterion, descriptive |
|---|---|---|---|
| full_harness | 10/10/11/23/23 | 2.831164499915256 ([1.5449206309849945, 4.117408368845518]) | True |
| mor_only | 8/22/28/26/30 | 6.276293099928861 ([3.9955091764704034, 8.557077023387318]) | False |

Primary slope difference, MoR-only minus full-ten:
```json
{
  "status": "estimated",
  "estimate": 3.4451286000136045,
  "ci95": [
    0.8266560307725941,
    6.063601169254615
  ],
  "p_two_sided": 0.009916489550058027,
  "method": "Independent-arm grouped-binomial logistic slope difference; Wald approximation, logit linearity and independent calls assumed",
  "se": 1.3359799414148363
}
```

Secondary direct difference in endpoint probability changes:
```json
{
  "difference": 0.3,
  "conservative_95_interval_unknown_envelope": [
    -0.44706211481886204,
    0.9527220868389555
  ]
}
```

The primary assumes linear logits and independent binomial calls; counts and endpoint intervals retain a less model-dependent description.
A slope difference is not a pure parameter-count or bandwidth effect: deletion changes conditioning, semantic content and length together.
Unspecified background parameters are not zero or neutral. No paraphrase robustness, ethical understanding, reduced architecture or phase pass is established.
Model gpt-5.4-mini-2026-03-17; neutral context; temperature1; output cap600; N30 each; root seed20260921.
Fixed300 calls, all responses fresh, exact retained text and requests verified, one attempt per slot.
Raw ZIP bytes verified. Backup is on the same computer. No automatic further experiment.
