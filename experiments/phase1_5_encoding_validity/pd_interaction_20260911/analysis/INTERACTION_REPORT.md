# Fixed-text PD background interaction diagnostic

Status: **MORE_POSITIVE_MOR_SLOPE_AT_HIGH_PD**.
300 fresh calls; known cost $0.313056; cumulative known $3.378930.
Conservative charge including prior unknown timeout $3.383897; original allowance remaining $5.616103.

| Arm | ADOPT counts /30 at .1/.3/.5/.7/.9 | Slope (95% CI) | Legacy directional criterion, descriptive only |
|---|---|---|---|
| pd_low | 25/25/27/27/30 | 2.2547264876432687 ([0.2130170095610584, 4.296435965725479]) | True |
| pd_high | 3/1/2/4/23 | 5.746135853153931 ([3.5318123057807456, 7.960459400527117]) | False |

Primary slope difference, PD=.9 minus PD=.1:
```json
{
  "status": "estimated",
  "estimate": 3.4914093655106626,
  "ci95": [
    0.4794654142820547,
    6.50335331673927
  ],
  "p_two_sided": 0.023088516633877083,
  "method": "Independent-arm grouped-binomial logistic slope difference; Wald approximation, logit linearity and independent calls assumed",
  "se": 1.5367343354196494
}
```

Secondary direct difference in endpoint probability changes:
```json
{
  "difference": 0.5000000000000001,
  "conservative_95_interval_unknown_envelope": [
    -0.18251089121489839,
    1.0272054948178297
  ]
}
```

The primary assumes linear logits and independent binomial calls; counts and endpoint intervals retain a less model-dependent description.
All ten entries, exact text and matched UTF8 message lengths stay fixed; only PD background value differs between arms.
A background-value effect is not proof of faithful psychological interaction or an explanation of the entire deletion effect. No paraphrase, capacity or phase-pass claim.
Model gpt-5.4-mini-2026-03-17; neutral context; temperature1; output cap600; N30 each; root seed20260922.
Fixed300 calls, all responses fresh, exact retained text and requests verified, one attempt per slot.
Raw ZIP bytes verified. Backup is on the same computer. No automatic further experiment.
