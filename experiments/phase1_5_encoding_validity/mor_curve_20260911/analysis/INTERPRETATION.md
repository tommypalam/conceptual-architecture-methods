# Interpretation and next decision

**300/300 valid, no terminal or usage failures.** Estimated full-rate token cost
$0.373464; cumulative $1.5266565 across the three screens under the latest $9
allowance, leaving approximately $7.47 of that allowance. This is not the
provider account balance. No calls remain running or automatically scheduled.
See [the verified report](CURVE_REPORT.md) for estimates and provenance.

| Arm | ADOPT at MoR .1/.3/.5/.7/.9 (30 per value) | Existing directional criterion |
|---|---|---|
| Grounding, primary | 4/9/5/11/19 | Not met: rates are not monotonic |
| Repetition, secondary | 0/1/1/5/12 | Met in this screen |

Grounding has a positive overall fitted slope, 2.654 (95% Wald interval
[1.286,4.021], LR p=.0000539), and a large endpoint effect (h=1.093).
It fails because the observed rate falls from 9/30 at .3 to 5/30 at .5.
This is a failure of the frozen observed-monotonicity rule, not evidence that
the parameter has no effect. With N30 per cell it also does not establish that
the underlying response function truly declines there. Keep the outcome;
do not smooth the dip away, relax the rule, or repeatedly sample until it passes.

Repetition has a positive slope, 6.189 (95% Wald interval [3.153,9.224],
LR p=.000000118), h=1.369, and nondecreasing observed rates. It meets the
same directional rule as a secondary diagnostic. This is verbatim repetition
of scenario information, without the added grounding instruction. The result
does not show that repetition encodes ethics, is superior to grounding, or
repairs the other validity tests. The direct difference in endpoint changes
is +.100 for grounding minus repetition, with conservative 95% interval
[-.605,.776]; an arm difference is unresolved.

The previous endpoint screen had repetition 1/30 -> 3/30 and grounding
3/30 -> 23/30. This screen has repetition 0/30 -> 12/30 and grounding
4/30 -> 19/30. These are separate batches, not pooled observations. In
particular, the earlier weak repetition endpoint result warrants caution
about selecting it from this favourable secondary result. The original
canonical five-value curve also remains a separate implementation/batch;
no improvement over that implementation was established here.

## Decision

Do not scale grounding into a full battery on this result. It has failed this
screen's primary criterion, while retaining evidence of overall response.
Do not abandon the ten-parameter architecture or infer an unresolvable limit.

The next useful candidate test is a small, separately frozen repetition
representation check for MoR/S3: include a fresh canonical repetition control
beside numeric-only and verbal-only variants at the same values. This would
ask whether the existing representation gap persists under repetition and
provide a new contemporaneous canonical check. It should reuse approved
definitions and locked dilemma text, preserve all other parameter values,
and retain the existing retention rule. It is a recommendation, not a prepared
or authorised dispatch allocation; exact messages and cost must be reviewed
before launching. No further calls were made here.

Even a favourable representation check would leave paraphrase robustness,
the audit's interpretability problem, and independent confirmation unresolved.
No internal-understanding, ethical-correctness, AGI or Phase 1.5 pass claim is
supported by this screen alone. Original prompts, theory and thresholds remain
unchanged; the optional tool is inactive and Phase 2 remains on hold.
