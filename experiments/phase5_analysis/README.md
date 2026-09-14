# Phase 5: integrated analysis

Relates representations, behaviour and measurement across the completed phases.
Everything here is **offline reanalysis of already-collected, already-paid
records**: zero API calls, no budget change, no frozen record modified.

[Back to the evidence index](../README.md)

## Studies

| Study | What it found |
|---|---|
| [reanalysis_20260914](reanalysis_20260914/ASSESSMENT.md) | Within-arm analysis of the Phase 2 confirmation. The no-profile arm was deterministic in four of six cells (400/400 identical); Procedural Dependence shows a monotone dose-response on departure from that baseline and ranks first of ten parameters under multivariate control. Scores the nine directional signs locked in thesis §6.1.1. |
| [Saturation diagnosis](reanalysis_20260914/SATURATION_DIAGNOSIS.md) | Traces null contrasts in four studies across three phases to one cause — deterministic unprofiled baselines — and proposes a U-arm dispersion pre-screen as a required protocol field. |

## Reproduce

```powershell
py -3.11 -B code/phase5_reanalysis.py
```

Deterministic under seed 20260914 with 10,000 permutations per test. Writes
`reanalysis_20260914/dispersion_results.json`; verified byte-identical on rerun.

Inputs are read-only: the frozen `responses.csv` and the hash-locked
`population.json` (content hash `72ff60b5…f87363a`) from
[phase2_confirmation_20260913](../phase2_confirmation_20260913/).

## Status and limits

Phase 5 is **begun, not complete**. The specification's remaining Phase 5 scope —
broader sensitivity analysis, the AW on/off comparison, factor analysis of
parameter redundancy, and multi-model portability — has not been run.

The reanalysis is post-hoc exploratory with one qualification: the §6.1.1
directional signs were locked before Phase 2 collection, but this is their first
evaluation and the analysis choices were made after seeing the data. The strongest
single effect (PD on S2/S3) was **not** among the locked predictions and remains a
post-hoc discovery requiring a prospective test before any confirmatory language.

Nine of ten coordinates show no systematic effect here. No ethical understanding,
human resemblance, moral quality or institutional-axis identification is
established, and no completed phase outcome is altered.
