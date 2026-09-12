# Phase 2 behavioural confirmation: completed assessment

**The amended behavioural Phase 2 is complete. All six primary individual
profile-versus-context comparisons replicated on fresh profiles and passed the
prespecified adjusted exact tests. One of seven secondary group comparisons
also passed. This supports functional influence of the encoded profile package
on generated choices, not ethical understanding or validated moral quality.**

Completed 2026-09-13 on `phase2-design-20260912`; prospective freeze commit
`14349800`; root seed **2026091302**; pinned model
`gpt-5.4-mini-2026-03-17`. The [protocol](PROTOCOL.md), [manifest](manifest.json)
and [precollection verification](VERIFICATION.md) were fixed before paid calls.
This was a local prospective freeze, not public preregistration.

## Scope and execution

Four hundred fresh LPM profiles retained all ten parameters, original Beta
marginals and Gaussian copula R. Each profile faced all three individual tasks
in both existing anchors, with encoded E and context-only U conditions:
**4,800 individual responses**. Twenty matched groups per task faced the same
four conditions plus a balanced, profile-free neutral bridge: **300 group
runs**, based on 60 matched group memberships. Group trajectories reused the
matched membership, CEO, private-evidence assignments and tie seed across
conditions. The custom interaction engine is inspired by Agents of Chaos;
direct integration of an external framework is not claimed.

The study saved **11,005 API responses**: 4,800 individual and 6,205 group.
Early C1 consensus reduced the 12,700 maximum. All individual answers parsed;
6,202 group votes parsed and three intermediate duplicate-marker responses did
not. **All 300 final group outcomes are complete.** No failures were rerun,
answers substituted, or protocol changes made during collection.

Every generation finished with `stop`, used the pinned snapshot, and supplied
known usage. All 11,005 provider response IDs were unique. Reconstruction of
every exact request and group state passed with **zero new dispatches**; see
the [integrity audit](analysis/integrity_audit.json). Twenty confirmation tests,
five independent-parser tests and a full mock/replay passed before collection.

The researcher requested an individual-results update after all individual
responses had completed, while groups were still running. That complete subset
is preserved in [the interim record](analysis/individual_interim_20260913.json).
Its inspection did not change the sample, tests, prompts or stopping rules.

## Primary individual results

Counts are out of 400 per cell. Differences are E minus U in percentage points.
Intervals below are conservative simultaneous 95% intervals over all six
contrasts; the decision rule uses the separately prespecified Holm-adjusted
two-sided exact paired tests. No first label is classified as morally good.

| Task and first label | Context | E | U | Difference, pp | Simultaneous 95% CI, pp | Holm p |
|---|---|---:|---:|---:|---|---:|
| S1: candidate A | 00100 | 397 | 369 | +7.00 | [1.43, 12.28] | 0.00000153 |
| S1: candidate A | 11011 | 398 | 383 | +3.75 | [-0.65, 7.97] | 0.000729 |
| S2: formal report | 00100 | 113 | 0 | +28.25 | [20.50, 35.11] | 9.63e-34 |
| S2: formal report | 11011 | 38 | 0 | +9.50 | [4.25, 14.43] | 2.18e-11 |
| S3: adopt now | 00100 | 345 | 400 | -13.75 | [-19.33, -7.71] | 2.22e-16 |
| S3: adopt now | 11011 | 252 | 400 | -37.00 | [-44.19, -28.66] | 3.36e-44 |

All six directions reproduce the exploratory pilot in an independent sample.
The most informative changes are S2 and S3: profiles introduce meaningful
variation where the profile-free comparator is unanimous. S1 remains close to
ceiling, so its significant differences are comparatively small.

The interval method is deliberately conservative and is not an inversion of
the Holm test. Thus the S1/11011 simultaneous interval includes zero even though
its adjusted exact test rejects; its pointwise 95% interval is [0.29, 7.06] pp.
Both methods and their roles were fixed before collection, not selected after
seeing the results. Complete paired counts and both interval types are in
[summary.json](analysis/summary.json) and [RESULTS.md](analysis/RESULTS.md).

## Secondary group results

Every entry is the number of groups choosing the named final outcome, out of
20. These are paired group-level comparisons; individual votes and repeated
rounds do not increase the independent sample size.

| Task / outcome | 00100 E | 00100 U | 11011 E | 11011 U | Neutral B |
|---|---:|---:|---:|---:|---:|
| C1 / package A | 11 | 20 | 0 | 0 | 0 |
| C2 / approve | 20 | 20 | 19 | 16 | 19 |
| C3 / continue | 20 | 20 | 20 | 20 | 20 |

**C1 provides the strongest group finding.** In 00100, profile encoding reduced
package-A outcomes from 100% to 55%: paired difference -45 pp, pointwise 95% CI
[-71.19, -1.02], exact p=.00390625, Holm p=.02734375 across the seven secondary
contrasts. The very conservative simultaneous interval is [-77.22, 11.50] pp;
as above, interval and test procedures differ. The inverse and neutral groups
all chose B, showing how strongly context alone can structure collective choice.

In C1/00100, consensus occurred in 14/20 E groups versus 20/20 U groups, with
mean duration 3.60 versus 1.25 rounds. The prespecified consensus contrast did
**not** survive correction (Holm p=.1875; simultaneous CI [-64.49, 20.23] pp).
It is not a confirmed reduction in consensus. No other group contrast passed
the seven-test correction. C2/11011 approval differed by +15 pp, but Holm p=1
and its simultaneous CI [-25.90, 48.84] is wide.

**C2 and C3 remain limited instruments here.** C2 approved in 94/100 runs;
only nine amendment IDs were adopted across all C2 runs. C3 continued in all
100 runs. Mean public authenticated evidence counts ranged from 16.60 to 18.10
of 24 across conditions. Those are descriptive ID counts, not semantic accuracy,
optimal evidence use or evidence of no encoding effect. N=20 has low power for
modest group differences; non-rejection does not establish equivalence.

## Implementation and qualitative findings

The [fixed review](QUALITATIVE_REVIEW.md) covers 120 individual and 320 group
responses plus all three parser failures. It is an unblinded assistant review,
not a human gold set or validated moral coding. The [diagnostics](analysis/diagnostics.json)
preserve remaining limitations rather than editing the answers.

- The prospective parser reads 51 fresh votes that the old strict parser would
  reject. It also rejects three duplicate-marker responses the old parser would
  accept. All three are intermediate C3 responses and have valid final votes.
  Two retain authenticated evidence citations independently of vote validity.
- No C3 evidence-ID provenance violation was found, but this does not validate
  the semantic claims attached to the citations or guarantee full disclosure.
- The fixed C2 sample correctly distinguishes actual adoption from discussion,
  including a real neutral-group CEO adoption. Remaining interface limitations
  include 26 amendment-text responses without ACTION: amend, five bare-reference
  proposals rejected, two missing ADOPT fields, and 25 duplicate proposal-text
  IDs. Proposal counts must not be read as counts of distinct substantive ideas.
- Explanations sometimes add unsupported assumptions or describe intended
  safeguards. Generated reasons are self-reports, and proposed mitigations are
  not realised benefits. No automatic moral or deception labels are assigned.

The group harness changed prospectively after the pilot's specific failures,
so group outcomes are not pooled across studies. Individual prompts were
unchanged. Historical naked-choice calibration rates do not automatically apply
to role-bearing, multi-round tasks with additional private evidence.

## Cost and preservation

Estimated provider token cost at published global rates: **$17.05021125**;
conservative accounting using uncached rates plus 10%: **$18.755232375 / $30**.
Pricing was verified before collection against the
[official model page](https://developers.openai.com/api/docs/models/gpt-5.4-mini).
Invoices and provider credit balance were not verified.

Including the completed exploratory pilot's $4.15084065, combined Phase 2
accounting is **$22.906073025 / $100**. Remaining cap room is not a provider
balance or an instruction to spend it. All paid Phase 2 calls have stopped.
Raw requests/responses, group states and review packs remain under ignored
`data/raw/phase2_confirmation_20260913`. The [local archive](analysis/raw_archive.json)
contains 22,312 files (53,581,434 compressed bytes); every member CRC and source
SHA-256 was verified. Archive SHA-256:
`791b8635f9d3458c9713f9d06f858e40eb8eedf613d813ca4366175790b2a112`.
An off-device backup is not established.

## Conclusion and next phases

This completes the researcher-authorised **two-anchor behavioural Phase 2**.
It does not complete the original ten-environment design or retrospectively
pass the original Phase 1.5 validity battery. The two anchors change all five
societal bits together, and the E/U comparison changes the full profile prompt,
including information and length. Neither individual parameter meanings nor
the causal contribution of peer exposure versus repeated sampling are isolated.

The application supplies profiles before generation and retains the model's
answers without ethical substitution. The evidence therefore supports a
functional encoding intervention. It does not establish intrinsic understanding,
human resemblance, improved moral performance, superiority to a postfilter,
unseen-task transfer, or the full architecture. The underlying model's existing
training and alignment are not removed by this experiment.

Phase 3 is the planned human-benchmark comparison with canonical/decanonised
scenarios and contamination controls. Phase 4 supplies human-validated dual moral
scoring; the coding manual still needs the required human review before use.
Phase 5 handles broader sensitivity/analysis and Phase 6 reporting. No downstream
paid experiment or moral-scoring run is queued by this completion.

## Synthetic closure review

Decision: close the amended behavioural collection and analysis, preserving the
scope limits and outstanding human/moral validation.

- Vera Linden: the evidence supports generated-choice influence; ethical
  understanding and moral labels remain unestablished.
- Marcus Osei: independent individual replication is a substantive gain;
  saturated group tasks and absent human benchmarks limit external validity.
- Yuki Tanaka: retain all six primary and seven secondary tests, their separate
  multiplicity families, wide group intervals and explicit non-rejections.
- Sofia Renna: expose unsupported assumptions and interface losses; a coherent
  explanation and a legal evidence ID are not measures of internal understanding.
- James Okafor: full request/state replay and preserved records support closure
  of this run; any further harness repair must be prospective.

Resolution: the original full-battery meaning of complete remains unmet, while
the revised behavioural study is complete and informative. These are synthetic
perspectives, not external expert review or human approval.
