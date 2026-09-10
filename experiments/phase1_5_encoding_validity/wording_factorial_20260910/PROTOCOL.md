# Exploratory PD/S3 wording attribution experiment

Prepared 2026-09-10 after the researcher's instruction to proceed. No calls
have been made in this designation. The two new combinations B/C await exact
template review in [HUMAN_REVIEW.md](HUMAN_REVIEW.md). A/D retain their original
approval. The existing theory and Phase 1.5 gate are unchanged.

## Question and scope

Does the previously observed P2/P3 difference for PD=.8/S3 follow the PD
endpoint descriptions, the other nine endpoint descriptions, or their
interaction? The old whole-template comparison could not separate these
contributions. This control changes presentation without changing definitions.

| Condition | PD endpoints | Other nine endpoint pairs |
|---|---|---|
| A | P2 | P2 |
| B | P3 | P2 |
| C | P2 | P3 |
| D | P3 | P3 |

The PD low endpoints both retain substantive procedural value subordinate to
outcomes. Both high endpoints give fair procedure independent normative value.
The mixtures copy these endpoint strings verbatim; no new descriptor is
introduced. Automated comparisons confirm identical numeric profiles, context,
dilemma, response instruction, and all non-PD text within A/B and D/C. A and D
are byte-identical request messages to the original approved P2/P3 PD/S3 cells.
This is the assistant's consistency assessment, not a substitute for the
remaining exact-combination human review.

The original 32/50 versus 2/50 ADOPT rates selected this profile and pair after
observing outcomes. All four conditions therefore collect fresh observations;
no old outcomes are pooled. Results are exploratory and specific to this
profile, dilemma and snapshot. They cannot establish general encoding validity
or identify which of the other nine descriptions is individually responsible.

## Frozen collection

- Configuration: neutral full harness, matching the source; no binary societal
  configuration is substituted.
- Profile: PD=.8, all other parameters at their existing fixed Beta means,
  with the original rendered precision. One fixed profile, no sampled population.
- Model: `gpt-5.4-mini-2026-03-17`, temperature 1, output cap 600 tokens.
- N: 300 independent requests per condition, 1,200 total, one fixed run.
- Root seed: 20260910. Each of 300 blocks dispatches one request per condition
  in a seeded shuffled order, with concurrency four. Requested seeds include
  condition and block; seeds do not guarantee independent or reproducible
  provider sampling. Provider scheduling does not guarantee completion order.
- All responses, including invalid parses and terminal failures, are retained.
  Resume skips already recorded requests; it never replaces them. A terminal
  API error or wrong returned model stops dispatch after the current block.
  Resuming a designation containing such a terminal failure is refused.
- Stop at fixed N regardless of interim outcomes. Progress counts may be
  monitored; no outcome-based early stopping or adaptive sample expansion.
- Exact messages, code hashes, source provenance, power-plan hash and design
  hash are in [manifest.json](manifest.json). Changes require a new designation.

## Estimands and analysis fixed before collection

Let pA,...,pD be each condition's probability of ADOPT, the unchanged first
option. Report all four valid-only rates, recorded/valid/invalid/missing counts,
and these three probability-scale contrasts:

| Contrast | Weights on A, B, C, D | Interpretation |
|---|---|---|
| PD wording P2 minus P3 | .5, -.5, .5, -.5 | Average PD wording effect across backgrounds |
| Other nine P2 minus P3 | .5, .5, -.5, -.5 | Average background wording effect across PD wordings |
| Interaction | 1, -1, -1, 1 | PD effect under P2 background minus PD effect under P3 background |

Construct four Clopper-Pearson rate intervals with per-rate alpha .05/4.
The union bound supplies at least 95% simultaneous coverage under the binomial
model; weighted extrema give simultaneous intervals for the three contrasts.
This method is conservative. An interval excluding zero supports a directional
effect; compare its width and magnitude with the planning targets rather than
treating a significance result as sufficient practical importance. Report all
three contrasts regardless of results. No equivalence test or revised phase
pass threshold is introduced.

Invalid/missing decisions remain unknown. For k known ADOPT and u unknown
among the planned N, extend each interval from the exact lower bound at k to
the exact upper bound at k+u. This covers every binary completion without
assuming missing at random. The original 98% parse floor applies separately
to each condition (at least 294 valid of 300); below it, or if incomplete or
containing terminal failures, findings remain descriptive/incomplete.

Inference and power assume independent Bernoulli responses with a stable
probability within each condition. Randomized blocks distribute temporal changes
across conditions but do not prove this assumption or model correlated service
effects. Report any observed service/model changes and collection interruption.

## Offline power and sample-size selection

Seed 20260910; 20,000 independent simulated experiments per scenario and N;
no API calls. [power_plan.json](power_plan.json) records every scenario and all
three contrast detection rates. Candidate N was 100, 200, 300, 400 per cell;
choose the smallest reaching 80% for both 20-point main effects and a 40-point
interaction in the specified balanced scenarios. N=300 meets that target.
These effect sizes are diagnostic planning targets, not changes to the original
10-point equivalence margin or guarantees of detecting every meaningful effect.

| Scenario | True probabilities A/B/C/D | Approximate power at N=300 |
|---|---|---:|
| PD main effect 20 points | .6/.4/.6/.4 | 97% |
| Other-nine main effect 20 points | .6/.6/.4/.4 | 97% |
| Interaction 40 points | .6/.4/.4/.6 | 97% |
| PD main effect 20 points, different backgrounds | .4/.2/.8/.6 | 99.5% |
| PD main effect 10 points | .55/.45/.55/.45 | 5% |
| Interaction 20 points | .55/.45/.45/.55 | 5% |

The balanced null produced no false detections in 20,000 simulations at each
candidate N; this does not claim a mathematically zero false-positive rate.
Monte Carlo standard error near 97% is about .12 percentage points. Invalid
responses were not simulated and can reduce power. A null result cannot rule
out smaller effects, particularly interaction: these require much more data.

## Budget and records

Official [OpenAI GPT-5.4-mini pricing](https://developers.openai.com/api/docs/models/gpt-5.4-mini),
checked 2026-09-10: $0.75/million input tokens and $4.50/million output tokens.
Historical token lengths from the 100 P2/P3 PD/S3 responses average 897.5 input
and 92 output tokens. Applying those lengths to 1,200 fresh requests estimates
$1.30455 before taxes. At the historical maximum 904 input tokens and the full
600-token output cap, the estimate is $4.0536. Allow roughly $5 planning room;
this is not an enforced billing cap. Mixed input lengths, retries and service
charges can change actual cost. Caching would reduce input cost; no cache
discount is assumed. No new Claude calls are required.

Raw records stay under this directory's ignored `records/`. On completion,
the runner writes analysis, a tracked checksum inventory and token usage,
and a verified same-computer ZIP in `output/validity_backups`. The ZIP is
not an off-device backup. Approval must match both template and exact-message
hashes. The pending approval artifact remains preserved.

Offline validation: six focused tests passed, covering exact confidence bounds,
contrast orientation and unknown handling, endpoint-only mixing, unchanged
original A/D messages, approval hash checks, eight-call mock collection with
balanced blocks/distinct seeds, no-call resume, scoring, and terminal failure
preservation with resume refusal. Tests use no credentials or real API calls.

## Commands

After the researcher's exact B/C approval is recorded separately:

```powershell
python -u -B code/run_validity_wording_factorial.py --run-root experiments/phase1_5_encoding_validity/wording_factorial_20260910 --approval experiments/phase1_5_encoding_validity/wording_factorial_20260910/review_approved.json --yes
```

Credentials must already be configured in the process environment. For an
offline analysis of recorded data, use the same run root and `--score-only`.
No credential or approval is required for that read-only collection analysis.
