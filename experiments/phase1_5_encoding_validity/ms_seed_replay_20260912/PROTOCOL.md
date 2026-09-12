# Canonical MS exact-request seed replay

2026-09-12, frozen before new responses. Neutral context; canonical MS=.9,
S2 locked dilemma, all ten original values/descriptions. Model
`gpt-5.4-mini-2026-03-17`; temperature1; maximum600 completion tokens.
40 new calls: all20 seeds from original_expanded and all20 from ms_stanza_crossover.
Ordering seed20260928; each API seed is replayed from its own source record.

The user requested continued probing; prior spending authority persists.
This bounded probe follows the offline audit finding zero same-prompt/same-seed
repetitions. Both complete cohorts are used; none selected by favourable outcome.
Prior source counts14/20 and0/20 are known, so interpretation is exploratory.

## Exact requests and allocation

[Full preview](request_preview.json) contains exact messages and all40 source
references/seeds. Replay original model, role/content messages, temperature,
max_completion_tokens and seed. No additional text, tools, memory or response
from a previous call is sent. Source responses in provenance are used only for
offline paired scoring. All40 source bytes are hash-locked in the manifest.
20 randomized complete two-cohort blocks, concurrency3, one attempt per slot.
40 unique requested seeds within this run; they intentionally match history.
These new research calls do not replace or retry any historical record.

## Prespecified analysis

Primary family: two exact two-sided McNemar tests, one per historical cohort,
comparing each seed's original binary decision with its replay. Use binomial
probability .5 among discordant pairs; no discordant pairs gives p=1. Holm
correction across both, alpha.05. Report formal-report gains and losses, match
counts and paired probability change. Conservative nominal95 bounds combine
Bonferroni exact intervals for gain/loss proportions; they are not Holm-adjusted.

Secondary descriptive comparison: new responses for crossover seeds minus new
responses for expanded seeds, with conservative nominal95 interval and two-sided
Fisher p. No additional significance or expansion decision. No gate-pass rule.

A matched request need not produce identical responses. A changed response
frequency with the same requested seeds means changing the seed list is not a
sufficient explanation for that observed shift. It does not prove backend drift,
determinism, internal understanding or failure of ethical encoding in principle.
A difference between the fresh cohorts may indicate seed-set sensitivity, but
these are fixed historical cohorts and small samples. Selection after earlier
results and possible dependence across time remain limitations.

## Stops, preservation and spending

Any API, parse, model, request, usage or reservation failure stops after current
batch. Preserve every attempt; no retries, optional extension or automatic
restart. Exact-prompt and seed checks precede scoring; all source and new API IDs
must remain distinct. ZIP verification and source-paired audit after collection.

**$0.30 maximum dispatch cap**, inside remaining tracked$3.79170675. Full
conservative reservation is recorded in the manifest; provider balance is
unverified. No Claude calls or larger sweep. Phase1.5 remains open;Phase2 held.
