# Canonical ultimatum context/encoding diagnostic, revision 2

Prospective exploratory supplement, 2026-09-13. The researcher authorised
continued useful work within the existing budgets after the clarified candidate
was discarded. This supplement has a $4.30 maximum, including one independent
Claude review. Provider cumulative caps remain Claude $15 / OpenAI $30, and
package accounting including Phase 2 must remain below $100. No automatic retry,
repeat sample, alternative generation or larger confirmation is released.

## Prelaunch serialization correction

Revision 1 made no API calls. Its offline round-trip audit found that the
review packet's JSON object key order changed when population metadata was
loaded from the canonical saved file. The decoded reviewer content was identical
and all 576 participant requests matched. Revision 2 serializes the review
packet with sorted keys, adds a real saved-file round-trip test, and uses new
slot/release/source identities. The original frozen source, protocol and requests
remain preserved. No scientific design, population draw, participant wording,
analysis or budget changes. Exact review text also includes this revision note.

## Why this step

Implementation specification sections 7.3-7.4 distinguish recognition screening
from the configuration counterfactual, its primary behavioural diagnostic.
The five alternatives failed screening; the later allocation candidate was
recognised 5/5. Repeated surface changes have not produced a usable control.
Recognition of a shared rule cannot identify whether an answer was memorised.
Nor does a context effect alone prove independence from training-data knowledge:
a model can recognise a task and also follow contextual instructions.

This is an explicit sequencing amendment: collect a small canonical-only
diagnostic while the formal low-recognition alternative gate remains unmet.
It is not the original all-five N200 primary family, an Appendix A descope,
a substitute for the rejected alternatives or permission to claim a Phase 3 pass.
All five benchmark families, all ten coordinates, Beta marginals and R remain
in scope. The original specification, gates and frozen evidence stay unchanged.
The immediate purpose is to distinguish a fixed canonical response from context
sensitivity, and to estimate the incremental effect of the complete profile block.

## Design and exact requests

Draw 24 fresh profiles with the existing Gaussian copula and Beta marginals,
population seed 2026091313. Retain all ten coordinates. Existing canonical
rendering rounds prompt coordinates to two decimal places; retain four-decimal
draws and both representations through saved requests. No selection by values
or outcomes. Each profile/block gets all 24 combinations below:

- Two contexts from canonical_r2: N/0/N/N/N (predicted high rejection) and
  N/1/N/N/N (predicted low rejection), axes Freedom/Justice/Authority/Care/Loyalty.
- Two arms: E, the canonical full profile/context system prompt;
  U, context only with the complete profile block removed and task instructions
  consistently referring only to context. U is not an all-0.5 profile.
- Six independent tasks: integer proposer offer to the other participant 0..100,
  and responder accept/reject for offers 10,20,30,40,50 of 100.

Use the exact canonical `ultimatum_turn` builder. Append the same formatting
sentence to both system arms: "Return a JSON object matching the requested
schema." The shared suffix supports API JSON mode; the canonical source is
unchanged. Each response has a fresh
conversation: one system message and one user message, no previous answer.
Within each profile/block shuffle all 24 cells using seed 2026091314 plus block
ID, keeping blocks contiguous to limit timing imbalance. In U, block IDs are
matched stochastic replicate IDs, not visible or meaningful profiles. No
demographic identities, predicted actions or target rates enter participant text.

Model: gpt-5.4-mini-2026-03-17, temperature 1, reasoning none, default service,
JSON-object response mode, 64 output tokens. No provider seed or common random
numbers are claimed. At most 576 participant calls. Exact requests, profile draw,
schedule, source hashes, parser, analysis and price bounds are frozen before
review/collection. Reviewer gets this protocol, all six task texts and all four
system-text conditions for the first profile, plus the population summary and
rendering contract. Reviewer does not receive credentials or previous raw outputs.
Participant requests send synthetic profiles, context and task text to OpenAI.

One Sonnet 4.6 independent methodological review (up to 1024 output tokens;
request below 900 UTF-8 bytes and 100 words to fit the inherited text parser) must
return accept with no blocking issues before any participant request. Review
can accept the bounded diagnostic, not certify validity or override gates. A
revise/reject verdict stops the run. No automatic corrective consultation loop.
The review accepts bare JSON or one complete JSON fence, then strict schema.

## Outcomes and analysis

Primary exploratory endpoint is rejection at offer 20. Predeclare three
descriptive contrasts: E high-minus-low, U high-minus-low, and their interaction
(E high-minus-low) minus (U high-minus-low). The first two differences are in
[-1,1], the interaction in [-2,2]. No significance test, pass threshold or
post-results promotion to confirmation. The context direction is the existing
specification hypothesis, not a human reference effect or a new trait-action rule.

Report all four cell rejection rates, all 24 assigned paired blocks, complete
blocks, missingness identification bounds, paired-block percentile bootstrap
95% intervals (9999 resamples, analysis seed 2026091315), and conservative
Hoeffding 95% intervals for independent bounded blocks. Degenerate bootstrap
intervals are flagged; they do not prove population certainty. Missing outcomes
block the complete-data contrast; complete-block estimates remain labelled
supplementary. Independent-block/stationary-model assumptions are limitations.

Secondary descriptive summaries: proposer offers and rejection rates for all
five offers, E-U differences at each context, and complete-grid monotonicity.
Acceptance is expected to be nondecreasing with offer for the monotonicity
summary; violations are retained, never repaired. Do not infer a continuous
threshold from an incomplete or nonmonotone grid. No human-rate equivalence test,
normative good/bad score or ten individual trait effects are estimated.

E-U isolates the full profile-prompt package, including definitions, numeric
values, task wording and length. It cannot distinguish numerical encoding from
ordinary semantic instructions. The interaction asks if that package changes
context sensitivity, not if intrinsic ethical understanding has been achieved.
Rater calls are unnecessary: syntactically valid closed actions are scored by
deterministic rules. No human validation is implied by machine-readable output.

## Integrity and stop rules

Strict participant JSON: exactly offer_to_other with integer 0..100, or exactly
action with accept/reject. No fences, extra fields, booleans as numbers, duplicate
keys or inferred intended actions. Invalid action text remains an invalid
observation; independent later cells continue. API failures, truncation, missing
usage or accounting/source mismatches stop dispatch and preserve reservations.
Never retry or replace a record in place. All 660 earlier ledger records and
the previous archive remain byte-linked. Archive and replay after completion
make no new API calls. Raw data and archives remain outside Git.

The inherited ledger calls the transport stage `recognition` and stores raw
text jobs as `probe`. These are legacy accounting/parser labels only; the new
slots and analysis explicitly identify participant behaviour. No recognition
observations or recognition gate decisions are generated by this supplement.

## Five-perspective review

Decision: use a bounded canonical E/U diagnostic while leaving the formal gate open.
These are synthetic perspectives, not external reviewers or extra API calls.

- Linden: an encoding-package effect is not ethical understanding or moral quality.
- Osei: hypothetical stakes and institutional wording limit human comparison;
  the U baseline is needed before attributing context shifts to the architecture.
- Tanaka: 24 blocks support exploration; keep all assigned outcomes, bounded
  interaction uncertainty and saturation limitations explicit.
- Renna: canonical-only evidence cannot replace the all-five contamination
  programme; it can identify whether the next investment should target context,
  profile specificity or task transfer.
- Okafor: reuse frozen task/state components and ledger protection; bind every
  static request and stop on a review objection or transport failure.

The disagreement is whether to defer all behaviour until a low-recognition
alternative exists. Resolution under the user's broad continuation approval:
allow this separately labelled, small supplement without granting any original
gate passage. Stop after one sample and assess before specifying further work.
