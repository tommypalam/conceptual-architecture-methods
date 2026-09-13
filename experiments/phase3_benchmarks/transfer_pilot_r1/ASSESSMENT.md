# PD process/outcome pilot r1: completed exploratory result

13 September 2026 · Prelaunch commit `f749a393` · No confirmation or Phase 3 pass

## Verdict

The pilot completed all 448 participant responses with no invalid decisions after
one accepted independent Claude design review. It does **not** establish a
consistent full-profile process/outcome trade-off across these two settings. The
PD-only instruction shows larger descriptive shifts, which merit interpretation
but do not establish superiority or general transfer. No moral scores were assigned.

The key diagnostic is saturation: every response opposed the secretly preferential
procedure, whether its realised access effect was beneficial or harmful. Thus one
side of the intended process/outcome contrast was flat. Increasing N on this exact
packet would not repair its limited ability to distinguish competing explanations.

## What was tested

Eight fresh background/sampling blocks; two related allocation settings; procedure
adherence/secret favoritism crossed with net public-access gain/loss; E full numeric
profile, V information-matched written percentages, S PD-only sentence, U no profile.
E/V/S intervene on PD at 0.1/0.9; other E/V coordinates stay fixed. U has no PD value.
Each cell has eight responses. S/U replicate the same information across sampling
blocks, not eight provided personalities. See the [protocol](PROTOCOL.md).

Responses are retrospective support/oppose evaluations. They do not change state,
reveal willingness to sacrifice, measure human resemblance or evaluate moral quality.
The two settings are not independently sampled representatives of a domain population.
The legacy JSON key `independent_domains: 2` counts the two distinct settings only;
it must not be interpreted as a statistical claim of independent domain sampling.

## Complete cell counts

Each entry is support / 8 assigned responses. P+ follows the announced draw;
P- secretly substitutes an associate's project. O+ is net access gain, O- net loss.
All denominators are also valid-response denominators; none are missing.

| Setting / arm / PD | P-O- | P-O+ | P+O- | P+O+ |
|---|---:|---:|---:|---:|
| Workshop E low | 0 | 0 | 0 | 8 |
| Workshop E high | 0 | 0 | 2 | 8 |
| Workshop V low | 0 | 0 | 3 | 8 |
| Workshop V high | 0 | 0 | 2 | 6 |
| Workshop S low | 0 | 0 | 4 | 8 |
| Workshop S high | 0 | 0 | 8 | 7 |
| Workshop U | 0 | 0 | 2 | 8 |
| Maintenance E low | 0 | 0 | 3 | 8 |
| Maintenance E high | 0 | 0 | 3 | 8 |
| Maintenance V low | 0 | 0 | 4 | 7 |
| Maintenance V high | 0 | 0 | 4 | 8 |
| Maintenance S low | 0 | 0 | 5 | 8 |
| Maintenance S high | 0 | 0 | 8 | 8 |
| Maintenance U | 0 | 0 | 0 | 8 |

## Prespecified exploratory contrasts

T = high-PD support(P+O-) minus support(P-O+), minus the corresponding low-PD
difference. T ranges from -2 to 2. Values below are percentage points, including
differences of differences; their range is therefore -200 to +200 points.

| Setting / arm | T | Marginal bootstrap 95% interval | Conservative Hoeffding 95% interval |
|---|---:|---:|---:|
| Workshop E | +25.0 | [0.0, +62.5] | [-167.1, +200.0] |
| Workshop V | -12.5 | [-50.0, +25.0] | [-200.0, +179.6] |
| Workshop S | +50.0 | [+12.5, +87.5] | [-142.1, +200.0] |
| Maintenance E | 0.0 | [-50.0, +50.0] | [-192.1, +192.1] |
| Maintenance V | 0.0 | [-37.5, +37.5] | [-192.1, +192.1] |
| Maintenance S | +37.5 | [0.0, +75.0] | [-154.6, +200.0] |

These are the six prospectively specified marginal exploratory intervals, with
9,999 whole-block bootstrap resamples, seed 2026091342. They are not simultaneous
intervals or significance tests. The one bootstrap interval excluding zero does
not turn this pilot into confirmation; conservative intervals are very wide.
No interval estimates uncertainty over a population of unfamiliar task domains.

Because P-O+ support is zero in every arm, every observed T here equals the
high-minus-low PD shift in P+O- support alone. This is not the hoped-for two-sided
reversal. E is positive in one setting and flat in the other; V is negative/flat;
S is positive in both. No planned between-arm superiority test was conducted.
The full profiles contain nine extra dispositions; E/S differences can reflect
their content, interactions, attention or wording. They do not identify which
explanation is responsible. Numerical encoding is not shown necessary or superior.

## Independent review and accounting

Claude accepted before participant collection with no blocking issues. It flagged
the bundled procedure manipulation, related settings, small sample, S information
ablation, sampling interpretation and retrospective-evaluation limits. Its phrase
"outcome-bias interpretation is post-hoc" is preserved verbatim in the raw review;
the frozen protocol already mentioned outcome bias before participant collection.
We therefore treat it as a limitation warning, not an accurate chronology claim.

| Item | Accounted USD |
|---|---:|
| Claude design review | 0.027366900 |
| OpenAI participant responses | 0.274972500 |
| This pilot | **0.302339400** |
| Reserved maximum / study ceiling | 1.785316500 / 2.000000000 |
| Cumulative Claude / cap | 6.056865100 / 15.00 |
| Cumulative OpenAI / cap | 1.103860725 / 30.00 |
| Cumulative Phase 3 allocation | 7.160725825 |
| Phase 2+3 package / absolute cap | 30.066798850 / 100.00 |

These are conservative usage-based accounting amounts, not invoices or verified
wallet balances. Remaining provider-cap room is $8.943134900 Claude and
$28.896139275 OpenAI; the $4/$10 moral-study planning reserve remains protected.
Changing phase labels does not reset any counter.

## Interpretation and next decision

Do not launch an enlarged confirmation of these exact stimuli. Preserve this
negative/mixed evidence and move the next development packet toward choices that
actually change state, with procedure and expected outcomes crossed without
bundling the procedure violation with secret personal favoritism. This is a
post-pilot redesign proposal, not a preregistered prediction or released study.

Retain useful full-profile, matched-prose, concise and profile-free controls. Do
not select only settings where S or E looked favorable. A subsequent task-validity
check must establish that the options implement the intended trade-off, including
cases where the outcome-focused choice reverses, before any large collection.
Reducing a deception floor must not mean excluding honest failures from the paper.

The central moral experiment remains required under the amended scope. Its
[manual draft](../../phase4_coding/manual_r1/MANUAL_DRAFT.md) is prepared in parallel;
the researcher has explicitly deferred human raters. AI-assisted moral judgments
will be reported separately from factual simulated consequences and are not human
validation. Formal Phase 3 and its original recognition failures remain unresolved.

Five synthetic perspectives reviewed this interpretation: Linden rejects equating
procedural support with goodness; Osei highlights the uniform rejection floor and
retrospective-task limit; Tanaka rejects superiority or confirmation claims from
eight blocks; Renna treats full/concise divergence as an open explanatory question;
Okafor recommends preserving the completed records and repairing the next task
before spending on sample expansion. Resolution: no automatic confirmatory sweep;
continue consequential-task and measurement development. These are internal roles,
not external expert validation.

## Evidence and verification

[Results](results.json), [scored rows](scored_rows.json), [release](release.json),
[execution manifest](execution_manifest.json) and [checkpoint](CHECKPOINT.json)
provide exact counts, uncertainty, requests/source hashes, costs and archive
integrity. Raw provider records remain locally archived and excluded from Git.
The checkpoint records the zero-call verification outcome and preserved prior
evidence. Off-device backup is not verified by this study.

Verification completed with zero new calls: all 1,814 inherited records were
preserved, the ledger contains 2,263 paid records, and all 6,791 archive members
passed CRC and SHA-256 checks. [Report checks](REPORT_CHECKS.json) separately verify
the displayed counts, six contrast intervals and cumulative accounting.
