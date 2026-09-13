# Recognition screening, prospective round 1

Status: preparation under the researcher's instruction to proceed. No population
release. Freeze the complete priced manifest and pass offline tests before any
paid call. The earlier five structural accepts remain limited to their reviewed
wording. This file and new adapters supplement, rather than edit, frozen inputs.

## What is being tested

Can an independent model identify the famous paradigm from the actual task
content? Use all five accepted canonical/alternative pairs, 50 fresh calls per
form: 500 probe outputs, zero sampled agents, no configuration. Claude Sonnet 4.6
is the recognition judge, distinct from GPT-5.4 mini benchmark execution. This
is repeated sampling from one model, not 50 independent human judges. No model
swap, sample reduction or automatic candidate revision follows from the results.

The specification's question is retained verbatim. The system prompt asks for
at most 35 words: name and briefly explain a resemblance, or state no match.
Maximum output 128 tokens, temperature 1, thinking disabled, no tools/cache.
This length limit preserves the requested name plus explanation while bounding
coding cost. Truncated, empty or over-1,024-byte outputs are invalid, never silently
shortened or coded as nonrecognition. Missing/invalid outputs block release.

## Exact content and representation

`code/phase3_recognition_stimuli.py` assembles both forms using canonical r2,
accepted alternative r3 and the existing 36 images. The exact image schedule
uses seed 2026091306. Images are sent as image blocks, without file names,
RGB/length measurements, correct labels or critical-trial flags in text.

For escalation, a lossless dictionary and indexed replacement table reconstruct
all 30 levels x 5 hesitation states x 4 conditions per form. For perception,
literal-line dictionaries reconstruct all 108 turns across six distinct cells
(size5 base also supplies the size5 modulator). All 18 images are included.
The remaining tasks include six isolated allocation roles/offers, all four
presence/danger cases and their three events, and every possible second-ranked
removed label across all three restriction branches. No participant choice is
fabricated or sent. No profile, normative context, source, benchmark identity,
crosswalk, target rate or outcome scoring rule goes to the recognition judge.

Only repeated strings are compressed; the exact wording is recoverable. Offline
tests compare every reconstructed escalation turn and every perception turn to
the corresponding builder. A compact recipe is not a naturalistic conversation;
its presentation may influence recognition. Canonical results are positive
controls, and low canonical recognition must be investigated before treating low
alternative recognition as informative. No new numerical positive-control pass
threshold is invented after outcomes. Domain/stakes limits remain in the prior
structural assessment. Later population requests must use these exact adapters
and isolation contracts or acquire a separately linked validation revision.

## Two independent AI classifications

Proposed rater identities: Claude Haiku 4.5 (pinned 20251001) and GPT-5.4 mini
(pinned 2026-03-17), in fresh isolated calls. The user was offered human raters;
absent a different preference, use AI coding explicitly, not human validation.
Neither rater sees the scenario, form, true family, other rating or judge identity.
They see only the original short answer and the same all-five classification
rubric. Ten opaque-ID answers per call, independently shuffled for each rater
with seeds 2026091307/2026091308: 50 calls per rater, 100 total. No deduplication
or voting across answers; each of 500 outputs receives two separate labels.
Batch-level contextual dependence is a limitation, despite fresh independent calls.

Count explicit names and unambiguous defining structures, as the specification
requires. Generic authority, fairness, group pressure, helping or preference
language alone is insufficient. Record all named/defined families, ambiguity
and refusal separately. Naming a different experiment is not target recognition.
Uncertainty words alone do not erase a specific identification. A bare inability
or refusal to assess is missing, not zero. The frozen rubric contains edge cases.

For every disagreement, preserve both originals and produce a local Codex
adjudication record with the response hash, decision and rationale. This is a
third AI assessment (current Codex GPT-6 session), not independent human
discussion; it is a disclosed operational limitation of AI-only screening.
Unresolved ambiguity/refusal blocks a complete release. No paid adjudication
calls or automatic debate loop are authorised. Human review can later audit
these decisions without rewriting the original records.

## Decision and reporting

Report each form's target-recognised count /50, Wilson 95% interval, raw rater
agreement and disagreements. More than 15/50 rejects an alternative. Exactly
15 does not exceed the specified threshold. Canonical recognition is descriptive,
not a reason to remove a benchmark. An incomplete sample cannot pass. Preserve
worst-case recognition bounds for unresolved items. Alternative acceptance here
means only passing this screen; it does not prove absence of training-data
influence, behavioural human resemblance, moral quality or ethical understanding.
No new candidate is automatically generated after a rejection.

## Cost and preservation

One shared ledger, with all 48 earlier records and the historical failure kept
byte-for-byte. No failure reset, overwrite or in-place retry. New slots are
`recognition_r1/` only. Reservations include all remaining probes AND all 100
coding calls at their maximum valid input and output limits before first spend.
The existing $7 recognition/$10 validation allocations and $15 Claude/$30 OpenAI
provider caps remain binding, alongside the $100 package cap. If the full bound
does not fit, do not dispatch a partial paid screen.

Ten token-count requests may quote the exact private probe payloads using the
free Anthropic count endpoint; preserve its outputs separately. Reserve each
quote plus 10% input-token margin and 1,024 framing tokens, as well as the maximum
output, then the existing additional 10% monetary allowance. Count estimates
are not a guarantee: actual usage must stay within assumptions or the run stops
and retains the full reservation. No automatic retry on HTTP, parse or cost
failure. All restarts verify hashes, exact requests and completed response links.

Standard global prices verified 2026-09-13: Sonnet4.6 $3/$15 per million
input/output tokens; Haiku4.5 $1/$5; GPT-5.4 mini $0.75/$4.50. No cache/batch
discounts assumed. Sources: [Anthropic pricing](https://platform.claude.com/docs/en/about-claude/pricing),
[Haiku identity](https://platform.claude.com/docs/en/models/haiku-4-5/overview),
[GPT-5.4 mini](https://developers.openai.com/api/docs/models/gpt-5.4-mini),
[token counting](https://platform.claude.com/docs/en/build-with-claude/token-counting),
[vision](https://platform.claude.com/docs/en/build-with-claude/vision).

## Synthetic perspectives

Linden separates recognition from understanding. Osei retains changed stakes
and all sequential cues. Tanaka preserves fixed N, invalids and coding disagreement,
and flags shared-model and batch dependence. Renna retains all five families and
ten coordinates without injecting profiles into the screen. Okafor requires
lossless reconstruction and complete reservations before paying. Resolution:
prepare the full screen without simplifying stimuli to force a favourable score;
AI-only coding and compact presentation remain disclosed limits. These are
written perspectives, not a human panel or the two independent raters.
