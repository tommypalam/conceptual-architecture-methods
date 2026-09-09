# Completed independent Claude reasoning audit

Model: `claude-haiku-4-5-20251001`. Configuration: neutral. Audit sampling seed: 20260604.
200 blind reasoning items, 2,000 quartile estimates. All 200 responses parsed successfully.
This format revision repeats all 200 selected items; the earlier failed-format attempt is preserved separately and not pooled.
The private answer key was used only for local scoring; provider requests contained definitions and reasoning only.

Additional malformed attempts under the brief prompt: 1. Unchanged valid observations reused in this continuation: 173. Failed attempts are preserved outside the effective records directory and included in the local backup.

Literal specification thresholds met: **True**.
Parameters above 35% with p<.05 against .25: 7/10 (required: 6).
Parameters at or above 50%: 6/10 (required: 4).

| Parameter | All-item accuracy (95% Wilson CI) | Majority baseline | Active-only accuracy | Active balanced accuracy | Stratified permutation p |
|---|---|---|---|---|---|
| LL | 7.5% (4.6%–12.0%) | 94.0% | 25.0% | 28.1% | 0.5005 |
| CS | 38.0% (31.6%–44.9%) | 94.0% | 25.0% | 28.1% | 0.3045 |
| RT | 15.0% (10.7%–20.6%) | 94.0% | 20.0% | 25.0% | 0.4840 |
| MoR | 75.0% (68.6%–80.5%) | 92.0% | 20.0% | 25.0% | 0.7235 |
| RE | 6.5% (3.8%–10.8%) | 92.0% | 45.0% | 31.2% | 0.2840 |
| PD | 50.0% (43.1%–56.9%) | 94.0% | 40.0% | 37.5% | 0.1045 |
| TfA | 76.0% (69.6%–81.4%) | 92.0% | 30.0% | 34.4% | 0.1360 |
| ID | 78.5% (72.3%–83.6%) | 94.0% | 35.0% | 28.1% | 0.2360 |
| MS | 52.0% (45.1%–58.8%) | 94.0% | 30.0% | 31.2% | 0.2220 |
| AW | 86.5% (81.1%–90.6%) | 92.0% | 25.0% | 31.2% | 0.1620 |

## Interpretation limits

Nine traits are held at their means in each source sweep. Aggregate accuracy against a uniform 25% chance baseline can therefore be misleading; compare it with the empirical majority baseline and the 20 active-parameter items per trait.
Active-only estimates have small samples. Permutation tests use 1,999 resamples within problem strata and are unadjusted diagnostics, not multiplicity-corrected confirmation.
0 selected reasoning traces contain decimal literals; these were retained as prespecified.
Literal audit thresholds do not establish the whole Phase 1.5 gate. Paraphrase testing and the remaining combined scientific review are still pending.

## Response brevity

Explanatory commentary: median 21 words; maximum 66; 186 responses exceeded the requested 15-word limit.
All commentary is preserved. Verbosity does not filter estimates or change scoring.
