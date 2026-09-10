# PD endpoint decomposition - Phase 1.5 diagnostic

Prepared September 10, 2026 under the user's instruction to continue the plan
proposed before the deadline discussion. This experiment separates PD's low and
high endpoint wording. It does not change the concept definitions, injection
architecture, parameter values, dilemma, model or original phase gate.
The later plan remains LPMs for simple problems and an Agents of Chaos-style
build for complex problems; Phase 1.5 comes first.

## Design

Fixed profile: PD=.8, other nine parameters at their existing Beta means.
Fixed other-nine descriptions: P2. Neutral full harness and locked S3 dilemma.
Model `gpt-5.4-mini-2026-03-17`, temperature 1, cap 600 output tokens.
One fixed profile, 300 requests per condition, 1,200 fresh observations total.
Root collection seed 20260912 (a seed identifier, not the collection date).

| Condition | PD low endpoint source | PD high endpoint source | Relationship to previous run |
|---|---|---|---|
| A | P2 | P2 | Identical to prior factorial A |
| B | P3 | P2 | New mixed pair |
| C | P2 | P3 | New mixed pair |
| D | P3 | P3 | Identical to prior factorial B |

Condition letters are local to this designation. The previous run's C/D used
P3 background descriptions, which are not used here. All four conditions collect
fresh responses; previous outcomes are never pooled. Profile, pair and P2
background were selected after seeing earlier results, so this is exploratory
mechanism diagnosis, not independent confirmation of general encoding validity.

The full messages and endpoint table are in [HUMAN_REVIEW.md](HUMAN_REVIEW.md).
All wording is copied verbatim from the human-approved P2/P3 templates. Assistant
review finds that both low descriptions retain outcome dominance with substantive
secondary procedural value, and both high descriptions assign independent worth
to fair procedure. Their new low/high combinations B/C still require exact human
semantic review under [the recorded protocol](../../../docs/phase1_5_followup.md).
This is separate from the already authorised study and additional $50 budget.

## Inference and power

The outcome is ADOPT, the unchanged first option. In order A/B/C/D:

| Prespecified contrast | Weights | Interpretation |
|---|---|---|
| Low endpoint P2 minus P3 | .5, -.5, .5, -.5 | Average low-end wording effect across both high-end wordings |
| High endpoint P2 minus P3 | .5, .5, -.5, -.5 | Average high-end wording effect across both low-end wordings |
| Interaction | 1, -1, -1, 1 | Low-end effect at high-P2 minus low-end effect at high-P3 |

Use four Bonferroni Clopper-Pearson intervals, per-rate alpha .05/4; weighted
extrema provide at least 95% simultaneous contrast coverage under independent,
stable within-condition Bernoulli sampling. Report every contrast and interval.
No theory-based ADOPT direction is invented for PD/S3. A wording effect in either
direction diagnoses presentation sensitivity; preferred decisions are not a
criterion for selecting a future encoding.

The mathematical four-cell design, weights and power scenarios are identical to
the preceding factorial, so [power_plan.json](power_plan.json) transparently
relabels that offline simulation and records its source hash. It is not a new
simulation or new empirical evidence. Planning seed 20260910, 20,000 simulations
per scenario, candidate N=100/200/300/400. N=300 is the smallest candidate meeting
80% for balanced 20-point main effects and 40-point interactions (approximately
97% power each). Power is only about 5% for the illustrated 10-point main and
20-point interaction effects. These are planning targets, not the original
equivalence margin; a null result will not demonstrate equivalence or absence.

Preserve every malformed or missing response. Expand exact rate bounds from k
known ADOPT through k+u possible ADOPT for u unknowns among planned N. Report
valid-only estimates alongside the expanded bounds. Each condition needs at
least 294/300 valid parses (98%); incomplete collection, terminal failure or a
parse-floor miss prevents a completed diagnostic verdict. No failed record is
replaced. The original battery gate remains unchanged regardless of this result.

## Collection, stopping and provenance

Use 300 blocks with one request per condition, seeded shuffled submission order,
concurrency four and distinct condition/block requested seeds. Provider seeds
do not guarantee independent or reproducible sampling. Blocking distributes
temporal changes but does not establish independence or model service drift.
Keep fixed N regardless of results. Stop after the active block on terminal API
error or model mismatch; preserve those records and refuse in-place resumption
over terminal failures. A normal interruption resumes only undispatched keys.
No mid-run prompt, model, temperature, analysis or sample-size changes.

The new runner reuses the frozen, tested factorial executor and exact-bound
functions. It explicitly relabels the factors in analysis and records the new
seed, so the prior PD/background interpretation cannot silently carry forward.
Its source, prior sources, exact messages and power-plan contents are hash-locked
in [manifest.json](manifest.json). Prior experiment code and artifacts are intact.
Windows execution locks are outside the archived experiment directory.

On completion, raw records remain under ignored `records/`; tracked outputs
include numerical analysis, token usage, checksum inventory and local ZIP metadata.
The ZIP is a same-computer backup, not off-device storage. No remote publication
is part of this instruction.

## Budget and next decision

Expected token cost about $1.35, using the preceding run's observed approximately
$1.30 per 1,200 requests and nearly identical message lengths. Reserve $5 of the
user's additional $50 budget for planning, including output-length uncertainty;
this is not an enforced provider billing cap or money already spent. No paid
calls have been made at preparation. Record actual usage before authorising any
subsequent study against the remaining budget. No new Claude calls are needed.

After collection, use the endpoint effects and uncertainty to justify a concrete,
theory-faithful encoding revision if warranted. Do not automatically choose the
wording yielding a desired ADOPT rate, delete a parameter, or declare the whole
battery passed. A substantive revision requires researcher review and the
applicable specification review; validation must address the original battery's
remaining failures, not merely this selected profile. LPM/complex-agent work
remains downstream of Phase 1.5.

Validation before preparation: nine offline tests passed across the endpoint
and preceding factorial modules. Checks include exact endpoint isolation, fixed
profiles/user text, identity of previously reviewed control messages, pending
review refusal, immutable manifests, eight-call mock collection, resume without
extra calls, distinct seeds, factor orientation and correctly labelled scoring.
The reused executor's terminal-failure and uncertainty tests also passed.

## Execution after exact B/C review

```powershell
python -u -B code/run_validity_pd_endpoints.py --run-root experiments/phase1_5_encoding_validity/pd_endpoints_20260910 --approval experiments/phase1_5_encoding_validity/pd_endpoints_20260910/review_approved.json --yes
```

The configured API key belongs in the process environment, never in this file.
`--score-only` analyses existing records without API access.
