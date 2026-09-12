# Reporting returned under identical requested seeds

**40/40 valid replays, cost$0.0452325**, no failed or unresolved requests.
The researcher explicitly approved the frozen40-call/$0.30 scope before dispatch.

| Historical seed cohort | Historical FORMAL_REPORT | Replay FORMAL_REPORT | Same individual decisions |
|---|---:|---:|---:|
| Expanded original run | 14/20 | 14/20 | 16/20 |
| MS crossover run | 0/20 | 9/20 | 11/20 |

Every replay matches its source model, role/content messages, temperature,
completion-token limit and requested seed. All ten parameter values match.
The two source cohorts contain the same canonical high-MS prompt and differ
in their seeds. Both complete cohorts were intermixed in the new collection.
All40 new IDs are unique and distinct from all40 source IDs; source hashes,
new record provenance, response parses and raw archive bytes verified.

## What this resolves

The seed set associated with the all-local0/20 result now produces9/20 formal
reports without changing the prompt or seed list. A different seed list alone
therefore cannot explain the earlier discrepancy. Canonical high-MS reporting
has not remained uniformly absent. The expanded cohort's rate returns at14/20,
but four individual choices change: two gains and two losses. Matching an
aggregate rate is not identical per-request reproduction.

For the crossover cohort, all nine discordant pairs change from local correction
to formal reporting: paired change+0.45, conservative nominal95 interval
[+0.010,+0.712], exact McNemar p=.00390625, Holm-two p=.0078125. Expanded cohort
paired change0, interval[-0.340,+0.340], Holm p=1. These are the frozen paired
comparisons; the intervals are not family-adjusted.

The fresh crossover-seed cohort is25pp below the expanded-seed cohort, with
conservative nominal95 interval[-0.691,+0.286] and descriptive Fisher p=.2003.
That does not establish either a seed effect or equivalence of seed sets.

## What it does not resolve

Same-seed sampling can remain stochastic. The result does not identify backend
drift, a particular source of randomness, or a stable response probability.
The new responses were collected08:37:36-08:37:55 UTC September12; source
cohorts were collected the previous evening and around00:17 UTC. Time and other
unobserved conditions differ. All returned backend fingerprints remain absent.

Cohorts were selected after observing an unusually large discrepancy. Using
all their seeds avoids cherry-picking individual outputs, but does not remove
selection of the discrepant cohorts or regression-to-the-mean concerns. Treat
the paired tests as exploratory diagnostic evidence, not confirmatory population
proof that server behaviour changed. No provider-level deterministic guarantee
is assumed.

Only MS=.9 was replayed. There is no concurrent low-MS control in this probe,
so this is not a fresh endpoint-sensitivity or gradient pass. Earlier positive
and negative studies remain intact. The original24/30 equivalence requirement,
audit recovery question and Phase1.5 gate are unchanged; Phase2 remains held.

## Next useful design

Before a full sweep or further wording changes, use short repeated blocks of
the same fixed request panel, including low/high canonical MS and low/high
canonical MoR as a positive comparison. Separate repeated-seed variation from
between-block variation and retain concurrent controls. Freeze block count,
spacing, analysis and spending before collection; do not stop when a favourable
block appears. No such additional run is launched or allocated here.

Remaining conservative tracked allowance **$3.74647425**; provider balance
unverified. No pending requests. Sources and new archives remain separate;
the verified ZIP backup is on this computer, not an off-device backup.

[Full report](REPORT.md) | [All40 matched pairs](replay_verification.json)
