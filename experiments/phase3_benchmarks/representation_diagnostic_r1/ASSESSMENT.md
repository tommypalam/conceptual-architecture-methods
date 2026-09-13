# Numeric versus prose profiles: completed exploratory comparison

Completed and verified 2026-09-13. **All 576 participant decisions were valid**;
review plus collection cost **$0.409685100**. The pilot establishes neither a
clear presentation effect nor equivalence between the two representations.
The confidence intervals allow material differences in either direction.

## Primary endpoint: rejection of the 20-unit offer

Twenty-four fresh profiles each received both representations, both Justice
contexts and all six isolated tasks. E is the structured decimal profile; V is
the prose profile with exactly the same positions expressed as written
percentages. Justice LOW/HIGH describes institutional context, not individual
trait values or moral quality. Other institutional axes were NEUTRAL.

| Representation | Justice LOW | Justice HIGH |
|---|---:|---:|
| E: structured numeric profile | 11/24 rejected (45.8%) | 7/24 rejected (29.2%) |
| V: exact-information prose | 7/24 rejected (29.2%) | 6/24 rejected (25.0%) |
| E minus V | +16.7 percentage points | +4.2 percentage points |

The difference between those E-minus-V contrasts was +12.5 percentage points.
All three prespecified primary bootstrap intervals include zero:

| Primary exploratory contrast | Estimate, percentage points | Paired bootstrap 95% interval | Conservative Hoeffding 95% interval |
|---|---:|---:|---:|
| E minus V, Justice LOW | +16.7 | [-12.5, +41.7] | [-38.8, +72.1] |
| E minus V, Justice HIGH | +4.2 | [-16.7, +25.0] | [-51.3, +59.6] |
| Interaction: LOW E-V minus HIGH E-V | +12.5 | [-29.2, +54.2] | [-98.4, +123.4] |

All 24 assigned profiles contribute to every contrast; there are no missing
blocks or degenerate bootstrap distributions. No significance, equivalence,
superiority or pass/fail test was specified or added. Similar point estimates
cannot establish interchangeability, and higher rejection is not a performance
advantage or moral score. The interaction can range from -200 to +200 points.

The secondary LOW-minus-HIGH context estimates were +16.7 points in E
(bootstrap [-8.3,+41.7]) and +4.2 in V ([-20.8,+29.2]). Those intervals also
include zero. This sample does not resolve the contextual mechanism question.

Intervals use 9,999 whole-profile bootstrap resamples and fixed analysis seeds
2026091322 through 2026091326. Whole-block resampling retains within-profile
pairing; it does not require independent decisions within a profile. Independence
between profile blocks and stationarity of the provider remain assumptions.
The review's dependence caution is retained in the raw response; it should not
be interpreted as the analysis having treated paired decisions as independent.
Hoeffding bounds are deliberately conservative. Saved identification intervals
refer to missingness bounds, not sampling confidence intervals.

## Full secondary task grid

Rejection counts out of 24 at each fixed offer:

| Representation and context | Offer 10 | Offer 20 | Offer 30 | Offer 40 | Offer 50 |
|---|---:|---:|---:|---:|---:|
| E, Justice LOW | 19 | 11 | 2 | 0 | 0 |
| V, Justice LOW | 18 | 7 | 3 | 0 | 0 |
| E, Justice HIGH | 19 | 7 | 1 | 0 | 0 |
| V, Justice HIGH | 17 | 6 | 4 | 0 | 0 |

Both representations rejected low offers more often than high offers in this
sample. Mean proposer offers to the other participant, out of 100, were:

| Representation | Justice LOW | Justice HIGH |
|---|---:|---:|
| E | 42.54 | 46.04 |
| V | 42.08 | 44.17 |

These are descriptive hypothetical-task outcomes, not a human-rate match.
All 96 five-offer grids were complete; six were nonmonotone (E/LOW 1, V/LOW 3,
E/HIGH 1, V/HIGH 1). They remain in the data. Each offer used a fresh conversation,
so stochastic choice can produce a nonmonotone grid without demonstrating a
stable preference inconsistency. No continuous threshold is inferred from one.

## What this means for the thesis

The previous E/U study identified an observed profile-package difference against
context-only prompts. This fresh E/V comparison does not demonstrate that the
structured numeric presentation is necessary or uniquely effective. Nor does it
establish equal behaviour under prose. The studies use different fresh profile
draws; their responses and effect estimates are not pooled. There is no fresh
context-only arm here, so a causal V-versus-U effect is not identified.

V retained the same quantitative information, trait names and endpoint wording.
The comparison concerns presentation, including layout, token length, introductory
clarification and decimal-versus-percentage framing. It is not a nonquantitative
personality-description control and does not isolate numeral syntax alone.
Literal translation fidelity is not psychometric equivalence or proof that the
model uses every coordinate as intended. No ten separate mechanisms, intrinsic
ethical understanding, human resemblance or moral quality are established.

This result does not require numerical notation to outperform prose for the
broader generation-time encoding idea to remain viable. A more useful next
research question is whether changing an encoded concept produces a predicted
change on an unfamiliar task, with matched prose controls. Prepare that transfer
design offline, derive predictions from existing theory, and freeze task validity,
comparison conditions and analysis before collecting. Do not invent new
trait-action mappings or infer equivalence from this pilot to justify the next run.

The original five alternatives still fail the recognition gate; the subsequent
allocation candidate remains discarded. This canonical-only supplement does
not replace those controls or release the original all-five N200 Phase 3 study.
All five benchmark families, all ten coordinates, Beta marginals and R remain
in scope. A transfer proposal would supplement the evidence, not silently pass
or replace the original benchmark requirements. No follow-up sample is queued.

## Independent review, budget and provenance

The researcher supplied specific Anthropic/OpenAI payload approval before launch.
Claude Sonnet 4.6 accepted with no blocking issues, noting unmatched length,
unit framing and dependence/stationarity concerns. The protocol and exact
requests were frozen in commit `707ee797` before collection; release SHA-256:
`2285c8a6748bc8e0147cc54e3a79c3c34fab9dcb85bfe4c93cc7210247c0e115`.

Five prelaunch tests passed, including all 101 integer percentages, exact
forward/inverse translation, saved-file reconstruction, full mock/replay and
preserved transport failure/no retry. The real fidelity audit checked all ten
values, names and endpoints for every profile in both contexts. Nonprofile
instructions and paired task texts match exactly. Population seed 2026091320;
within-profile order seed 2026091321 plus profile ID. Four-decimal draws render
to two-decimal values in E and precisely matching written percentages in V.
No provider sampling seed was set.

One review cost $0.022179300; 576 GPT-5.4 mini decisions cost $0.387505800.
Total accounting is $0.409685100 against the $4.200345600 reservation and $4.30
ceiling. Phase 3 accounting is now $6.858386425: Claude $6.029498200 and OpenAI
$0.828888225. Remaining room under the $15/$30 provider caps is $8.970501800
and $29.171111775. Package accounting including Phase 2 is $29.764459450 under
$100. These are conservative usage estimates, not invoices or provider balances.

Full real-data replay made zero additional API calls and reproduced exact
requests, translations, responses, scores and accounting. All 1,237 inherited
records and the preceding archive remain intact. The ledger now contains 1,814
paid records. The new local archive has 5,444 members, each checked for CRC,
membership and source SHA-256 equality:
`output/phase3_representation_diagnostic_r1_20260913.zip`.
Archive SHA-256:
`30721acc1c89536d821fbd0e2a7a2286074e7da09bfcf1068fdd242a82aee90f`.
Raw data and archives are excluded from Git; off-device backup is unverified.

An independent integer-total report check reproduced all counts and proposer
means. Three saved proposer mean-identification intervals have reversed endpoints
by at most 1.67e-16 from floating-point arithmetic on complete data. The report
uses integer-derived means; this has no effect on binary primary contrasts or
their intervals. Frozen results and analysis remain unchanged; any arithmetic
cleanup must be prospective. See [REPORT_CHECKS.json](REPORT_CHECKS.json).

No API failure, invalid participant action, retry, replacement or mid-run
protocol change occurred. The original prelaunch approval block is resolved
and preserved as history. No collector is running or approval pending.

See [protocol](PROTOCOL.md), [results](results.json), [scored rows](scored_rows.json)
and [verification checkpoint](CHECKPOINT.json).

## Five-perspective interpretation review

Decision: retain the inconclusive presentation comparison and prepare a
theory-grounded transfer proposal without claiming equivalence or numeric superiority.
These are synthetic perspectives, not external expert reviews or extra API calls.

- Linden: notation need not be uniquely effective for generation-time encoding;
  neither arm demonstrates intrinsic understanding or moral superiority.
- Osei: the quantitative prose control is narrower than a naturalistic description;
  transfer and human comparability remain separate requirements.
- Tanaka: wide intervals allow meaningful effects; maintain the fixed endpoint,
  paired blocks, missingness rules and exploratory status.
- Renna: use the comparison to sharpen the next mechanism question while
  preserving all-five benchmark scope and the contamination limitation.
- Okafor: retain the complete validated run and exact translation evidence;
  avoid new collection until the next discriminating design is concrete.

The tension is wanting a strong claim from a cheap pilot versus the uncertainty
and bundled format differences. Resolution: report both effect estimates and
limits, preserve all results, and make no larger-study release from this outcome.
