# Repeatability problems are concentrated, not universal

The offline audit checked 54,120 archived files from18 behavioural studies:
53,782 valid final responses retained,18 failures/invalid records excluded,
and320 calls from the different tool-assisted protocol excluded. All retained
provider IDs are unique. No new API calls or spending.

83 identical-prompt/settings groups recur with at least20 valid observations
in each of two runs. Five of139 between-run comparisons differ after Holm
correction; three of188 chronological-halves checks differ in a separate family.
These counts are not pass percentages: non-detection does not establish stability.

## A positive signal that does recur

Canonical MoR/S3 shows the same endpoint direction in all six available studies:

| Study | ADOPT at MoR=.1 | ADOPT at MoR=.9 |
|---|---:|---:|
| September9 source | 5/50 | 42/50 |
| Evidence sensitivity | 8/30 | 26/30 |
| Repetition factorial, original arm | 18/60 | 52/60 |
| Profile ablation, full profile | 10/30 | 23/30 |
| Tool screen, original system arm | 4/10 | 9/10 |
| Expanded original replication | 5/20 | 20/20 |

These are matching original prompts/settings, with different seeds. The N10
tool-screen reference is shown descriptively but excluded from the N>=20 test
family. This recurring direction supports a limited parameter-response finding.
It does not establish exact probabilities, all-trait encoding, equivalence,
internal understanding or a passed phase gate. No new combined endpoint test
was added after seeing this pattern.

## Where repeatability breaks

Canonical MS=.9 yielded30/50, then14/20, then0/20. Both comparisons against
the latest run remain significant in the full139-comparison family (Holm
p=.000178 and .000461). Low-MS canonical controls remain0/50,0/20,0/20.
The high-MS shift is therefore not merely a low-powered failure to reproduce a
small previously observed effect.

The other detected between-run discrepancies concern PD/S3 contexts: the known
PD=.9/MoR=.9 canonical corner23/30 ->8/30, and two PD=.8 wording conditions.
All three detected within-run shifts occur in the assembled axis pilot's
unchanged baseline paraphrases at PD=.8: P1 rises50/400 ->120/400; P2 falls
355/399 ->281/399; P3 rises21/399 ->66/399. The halves are chronological
completion halves, not randomized treatments. The pilot contains interruptions
and continuations; time, seed allocation and collection segment are confounded.
Opposing directions across wordings do not support a simple uniform shift
in willingness to select ADOPT.

## What remains untested

There are **zero same-prompt/same-seed repetitions** in the retained corpus.
Identical prompt text plus recorded model/settings is not a completely identical
request when its seed changes. All53,782 returned fingerprints are missing;
recorded cache hits are zero. Neither absence identifies the cause.

The next small probe should replay the entire canonical MS=.9 request,
including each recorded seed, for all20 old-expanded and20 recent-crossover
records, intermixed in one fresh run. Select cohorts by prior run, not by which
individual responses were favourable. This tests whether the earlier seed set
still differs and whether matched request outcomes change over collection time.
A replay can be stochastic even with the same seed; it cannot by itself identify
backend drift or prove deterministic reproduction. Freeze the comparisons and
spending guard before dispatch. No broader sweep is justified by this audit.

All original findings and gates retained. Canonical MoR's recurring direction
is worth preserving while MS and some procedural contexts require a narrower
reproducibility claim. Phase1.5 remains open; Phase2 held. Remaining tracked
allowance$3.79170675 before any new paid probe.

[All comparisons, intervals and exclusions](REPORT.md) | [Protocol](PROTOCOL.md)
