# What the offline diagnosis changes

The theory is unchanged. No new API calls were made. The original result is
still 8/30 equivalent cells and the Phase 1.5 gate remains unmet. This analysis
explains why that count alone is an inadequate account of what happened.

## Two distinct problems

| Diagnostic finding | Profiles out of 30 | Interpretation |
|---|---:|---|
| Original equivalence established; all formulations near the same boundary | 8 | Consistency near a nearly fixed choice, with little discrimination. |
| Observed spread no larger than 10 percentage points, but equivalence not established | 4 | Consistent with a precision limitation; not demonstrated equivalence. |
| Observed spread above 10 points, conservative bounds inconclusive about exceeding 10 | 17 | Wording-sensitivity candidates needing targeted follow-up; not 17 proven effects. |
| Difference above 10 points supported by conservative simultaneous bounds | 1 | PD=.8/S3: a large difference remains after strong uncertainty protection. |

The 17 uncertain profiles include MoR/S2, whose original equivalence test was
disqualified by two invalid parses. The categories retain that status separately.
The conservative analysis expands bounds over all possible assignments of the
three unparsed decisions; it does not repair responses or assume random missingness.

For PD=.8/S3, paraphrases 2 and 3 produced 32/50 versus 2/50 first-option choices:
an observed difference of 60 percentage points. Its simultaneous difference
interval is **14.9 to 84.9 points**, constructed from Bonferroni-adjusted exact
intervals covering all 120 formulation rates. It remains above the 10-point
margin. This conservative check supports at least one substantial discrepancy;
it is not an efficient estimator of how many discrepancies exist.

See [the rate map](wording_rates.png), [all 30 profile diagnoses](profile_diagnostics.csv),
and [all 180 pair bounds](pair_diagnostics.csv). The calculation and assumptions
are documented in [DIAGNOSIS.md](DIAGNOSIS.md).

## The equivalence design is demanding near balanced choices

We simulated 10,000 independent repetitions per scenario using the existing
six-pair TOST rule. In these scenarios all four formulations have exactly the
same true probability, .50. The simulations contain no language-model calls
and make no assumption that actual wording effects are zero.

| Responses per formulation | Chance all six pairs establish equivalence, simulated |
|---|---:|
| 50 | 0 successes in 10,000 |
| 100 | 0 successes in 10,000 |
| 200 | About 2% |
| 400 | About 35% |
| 800 | About 91% |
| 1,200 | About 99% |

The JSON artifacts give exact simulation fractions and Monte Carlo intervals.
Zero simulated successes is not a claim of mathematically zero probability.
The 800/1,200 scenarios were an explicit planning extension after seeing low
simulated success at 400; they are not changes to the completed study. Scenario
seed is 20260909, independent of the original study seed 20260604.

This is a real measurement limitation: the original N=50 design could easily
miss genuine equivalence away from response boundaries. Increasing N could
resolve that uncertainty, but would not eliminate actual wording sensitivity.
At N=800, a fresh complete 30-profile, four-formulation experiment would require
96,000 calls. That is a planning illustration, not a recommendation or an
authorised budget. A small diagnostic experiment should come first.

## Recommended next experiment: isolate the wording source

Start with the fixed PD=.8/S3 profile, where the strongest discrepancy survives
the conservative check. Compare a two-by-two combination of already reviewed
wording from paraphrases 2 and 3:

| Condition | PD endpoint pair | Other nine endpoint pairs |
|---|---|---|
| A | Paraphrase 2 | Paraphrase 2 |
| B | Paraphrase 3 | Paraphrase 2 |
| C | Paraphrase 2 | Paraphrase 3 |
| D | Paraphrase 3 | Paraphrase 3 |

Keep numerical values, model snapshot, dilemma, context, response format and
all other scaffold text fixed. This separates the PD wording contribution from
the contribution of the other nine descriptions, and permits an interaction
check. It does not presuppose that PD wording is responsible for the original
effect. New combinations B/C still need exact-template review before use.

This profile and wording pair were selected after observing their large
difference, so the experiment would be exploratory mechanism diagnosis, with
independent fresh observations in all four conditions. Earlier observations
would not become confirmatory evidence or be silently pooled. A null interaction
would not prove no interaction unless its uncertainty were suitably narrow.

Before spending: specify contrasts, a practically meaningful effect size,
contrast-specific power and sample size, randomisation, missing-response handling,
fixed stopping, exact template review and a budget. The equal-rate equivalence
simulation above is not a power calculation for this factorial experiment.
No such experiment was prepared for dispatch or launched in this diagnosis.

The concrete limitation being addressed is inability to attribute whole-template
wording changes to any one parameter. The proposed control isolates presentation
without redefining the theory. It does not authorise parameter removal, prompt
redefinition, a different model or Phase 2. Discuss this design with the researcher
before implementation.
