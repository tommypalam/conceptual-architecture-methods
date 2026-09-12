# Canonical MS exact-request replay

**40/40 valid**, estimated token cost **$0.045233**.
Neutral context; canonical MS=.9/S2; all ten original values. GPT-5.4-mini-2026-03-17, temperature1, max600. Ordering seed20260928; API seeds replay history.

## Prespecified paired comparisons

| Source cohort | Source FORMAL_REPORT | Replay FORMAL_REPORT | Matched decisions | Gains / losses | Paired change | Nominal conservative 95% CI | Holm p |
|---|---:|---:|---:|---:|---:|---|---:|
| expanded | 14/20 | 14/20 | 16/20 | 2 / 2 | +0.000 | [-0.340, +0.340] | 1 |
| crossover | 0/20 | 9/20 | 11/20 | 9 / 0 | +0.450 | [+0.010, +0.712] | 0.0078125 |

Two-sided exact McNemar tests, Holm across two cohorts. Intervals combine exact gain/loss proportion bounds and are nominal, not Holm-adjusted. All source/new pairs retained in replay_verification.json. No missing or invalid outcomes.

## Secondary fresh-cohort comparison

Crossover-seed minus expanded-seed report probability: -0.250, conservative nominal95 interval [-0.691, +0.286]; descriptive two-sided Fisher p=0.200287. No additional significance or expansion rule.

## Verification and limits

Every new request matches its historical messages, model, temperature, completion-token limit and requested seed, with identical ten-parameter values. All40 source record hashes verified, all40 new provider IDs unique and separate from40 historical IDs. Raw ZIP bytes verified; no retries, replacements or pooling.
Historical cohorts were selected after seeing the discrepancy, but all20 seeds from each cohort were included regardless of individual outcome. Same-seed requests need not return identical decisions. Changes cannot alone identify backend drift or establish failure of ethical encoding in principle. Fixed cohorts, timing, possible dependence and the small sample limit inference.
This is a paired reproducibility diagnostic, not monotonicity, equivalence, internal understanding or a Phase1.5 pass. Original gate unchanged; Phase2 held. No automatic additional calls.
Remaining tracked allowance **$3.746474**; provider balance unverified. Local verified archive remains on this computer.
