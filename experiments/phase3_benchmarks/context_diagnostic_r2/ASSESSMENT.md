# Canonical context diagnostic: profile-package difference, unresolved context interaction

Completed and verified 2026-09-13. **All 576 participant decisions were valid.**
The full profile package changed the observed rejection rate substantially at
the prespecified 20-unit offer, but did not increase the observed context effect.
This is a useful exploratory result; the original Phase 3 gate remains unmet.

## Main result

There were 24 matched profiles/replicate blocks, two justice contexts, two arms
and six isolated tasks. E includes the full ten-coordinate profile; U includes
context only. Other context axes were NEUTRAL. Context LOW/HIGH below means the
institutional Justice setting, not a trait value, observed moral quality or
human-population classification.

| At the prespecified 20-unit offer | Justice LOW | Justice HIGH |
|---|---:|---:|
| E: full profile and context | 12/24 rejected (50.0%) | 13/24 rejected (54.2%) |
| U: context only | 0/24 rejected (0.0%) | 1/24 rejected (4.2%) |
| E minus U | +50.0 percentage points | +50.0 percentage points |

The existing hypothesis predicted more rejection in Justice LOW than HIGH.
The observed LOW-minus-HIGH difference was -4.2 percentage points in each arm.
Their interaction was therefore zero. The predicted direction was not observed
at this endpoint; uncertainty does not establish either equivalence or a reversal.

| Prespecified exploratory contrast | Estimate, percentage points | Paired bootstrap 95% interval | Conservative Hoeffding 95% interval |
|---|---:|---:|---:|
| E: Justice LOW minus HIGH | -4.2 | [-29.2, +20.8] | [-59.6, +51.3] |
| U: Justice LOW minus HIGH | -4.2 | [-12.5, 0.0] | [-59.6, +51.3] |
| Interaction: E context effect minus U context effect | 0.0 | [-20.8, +20.8] | [-110.9, +110.9] |

The prespecified secondary E-minus-U contrast was +50.0 points in each context:
bootstrap interval [+29.2, +70.8] and conservative interval [-5.4, +100.0] for
each. The broader interval includes zero. These are exploratory descriptive
estimates from 24 blocks, without significance tests, multiplicity-adjusted
claims or promotion to confirmation. The interaction is a difference of two
differences and can range from -200 to +200 percentage points.

All primary and secondary contrasts retained all 24 assigned blocks. There
were no missing outcomes or degenerate bootstrap distributions for these five
contrasts. Bootstrap intervals use 9,999 block resamples with seeds 2026091315
through 2026091319. The machine-readable identification intervals describe
missingness bounds, not sampling confidence intervals. Hoeffding intervals
assume independent bounded blocks; stationarity and provider dependence remain
limitations. U block IDs label stochastic repetitions, not distinct profiles.

## All secondary task results

Rejection counts out of 24 for every fixed offer:

| Arm and context | Offer 10 | Offer 20 | Offer 30 | Offer 40 | Offer 50 |
|---|---:|---:|---:|---:|---:|
| E, Justice LOW | 21 | 12 | 8 | 0 | 0 |
| U, Justice LOW | 19 | 0 | 0 | 0 | 0 |
| E, Justice HIGH | 18 | 13 | 5 | 0 | 0 |
| U, Justice HIGH | 0 | 1 | 0 | 0 | 0 |

Context-only rejection at offer 10 differed markedly (19/24 versus 0/24).
Thus the small contrast at offer 20 is not evidence that context never matters.
Offer 10 remains secondary; it does not replace the frozen primary endpoint.
The change in the E-U difference across offers also argues against describing
one simple, universal profile effect from this small task grid.

Mean proposer offers to the other participant, out of 100:

| Arm | Justice LOW | Justice HIGH |
|---|---:|---:|
| E | 42.29 | 46.67 |
| U | 50.00 | 50.00 |

Every context-only proposer offered 50. No human-rate match or equivalence is
inferred from these values. The task is hypothetical, canonical and recognisable;
its context manipulation is not a matched human experiment.

All 96 five-offer grids were complete. Five were nonmonotone: two E/LOW,
two E/HIGH and one U/HIGH. These observations are retained. Because each offer
was sampled in a fresh conversation, a nonmonotone grid can reflect stochastic
choice rather than a stable preference violation. No continuous rejection
threshold is inferred from such grids.

## What this supports and what comes next

Under these prompts, adding the full profile package produced a substantial
observed behavioural difference at offer 20. This motivates further study of
the package's contribution beyond context alone. It does not isolate the ten
numeric values from their semantic definitions, instruction wording or length;
nor does it establish ten separate trait effects, ethical understanding,
human resemblance or good/bad outcomes. More rejection is not itself a moral score.

The primary context interaction provides no positive evidence here that profile
encoding strengthens sensitivity to the Justice context. A zero point estimate
with these wide intervals does not establish absence of that effect.
Recognising a task and following profile/context instructions can coexist;
canonical-only behaviour does not resolve training-data contamination.

The most informative next design is a separately specified representation control:
compare the current profile package with a matched ordinary-language description
of the same values, with context and tasks fixed. It needs an explicit translation
contract and independent fidelity check before collection; no new trait-action
mapping or unvalidated binning follows from this result. A larger context-effect
confirmation alone would not resolve the semantic-instruction confound.
This is a recommendation, not a frozen or queued follow-up sample.

Keep all five benchmark families and the original low-recognition requirement
in the formal Phase 3 plan. The original alternatives remain rejected, and the
earlier N5 allocation candidate remains discarded. This supplement is not pooled
with recognition data and does not release the original all-five N200 study.

## Review, costs and verification

The researcher supplied explicit payload/destination approval before launch.
Sonnet 4.6 accepted the design with no blocking issues. It noted the E/U prompt
package confound, small interaction sample, unresolved recognition gate and
inability to independently verify the proposed participant model identity.
The runtime verified returned provider model identifiers against the frozen
requests; that is a transport check, not independent validation of model behaviour.

The run used 577 calls: one Claude review plus 576 GPT-5.4 mini decisions.
Review cost was $0.018932100; participant accounting was $0.285228900;
total **$0.304161000**, versus a $4.200345600 worst-case reservation and $4.30
local ceiling. Phase 3 accounting is now $6.448701325: Claude $6.007318900 and
OpenAI $0.441382425. Remaining room under their $15/$30 caps is $8.992681100
and $29.558617575. Package accounting including Phase 2 is $29.354774350 under
$100. These are conservative usage estimates, not provider invoices or balances.

Four offline tests passed before collection. The source and exact request freeze
were committed before launch (`a46be276`); release SHA-256 is
`96abf1505662916c36f960ec34f263df29ce43fabffc90f473f2a7e18f180c91`.
Population seed 2026091313; within-block schedule seed 2026091314 plus block ID.
All ten existing Beta marginals and R were retained. No provider sampling seed
was set. Profile values retain four decimals in the draw and two in the prompts.

Final real-data replay made **zero additional API calls**, reproduced requests,
scores, estimates and costs, and verified all 660 inherited records and the
previous archive. The ledger now contains 1,237 paid records. The new archive
`output/phase3_context_diagnostic_r2_20260913.zip` has 3,713 members, each checked
for membership, CRC and source SHA-256 equality. Archive SHA-256:
`073659c2be0d5072c5f3f3ae356610d466c968ef0ec35955612491159e9e97a3`.
Raw data and archives remain excluded from Git; off-device backup is unverified.

The first no-spend diagnostic freeze, its JSON-order reconstruction defect and
the prospective revision remain documented without overwriting frozen files.
No malformed action, retry, replacement or mid-run protocol change occurred.
No collector is running, no further paid call is queued and no approval is pending.

See [protocol](PROTOCOL.md), [results](results.json), [scored rows](scored_rows.json)
and [verification checkpoint](CHECKPOINT.json).

## Five-perspective interpretation review

Decision: retain the profile-package finding and unresolved primary context
interaction, and design a representation control before a larger claim.
These are synthetic perspectives, not external expert reviews or extra API calls.

- Linden: higher rejection is neither ethical understanding nor automatically good.
- Osei: a matched semantic comparator is needed; hypothetical canonical tasks
  cannot establish human resemblance.
- Tanaka: preserve the primary offer, wide intervals, all assigned blocks and
  nonmonotone grids; do not convert secondary differences into confirmation.
- Renna: connect the finding to testing what the profile representation adds,
  while retaining the full benchmark programme and contamination limitation.
- Okafor: the complete valid run and zero-call audit support a reliable pipeline;
  retain every record and avoid repeat collection without a new discriminating design.

The tension is a large observed secondary package effect alongside an unresolved
primary interaction. Resolution: report both plainly, retain exploratory status
and target the representation confound in the next prospective design.
