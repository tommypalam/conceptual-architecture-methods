# PD process/outcome pilot r1

Prospective exploratory protocol, 13 September 2026. No moral scores or original
Phase 3 gate pass. Implementation: code/phase3_transfer_pilot.py.

## Question and design

Does PD change the relative influence of procedure and outcome when evaluating
a completed selection? This first pilot measures expressed overall support, not
consequential choice, willingness to pay, human resemblance or ethical understanding.
Eight newly drawn backgrounds/sampling blocks face workshop-grant and facility-
maintenance settings. These are two closely related allocation settings, not a
broad test of cross-domain generalization. Root seeds: population 2026091340,
schedule 2026091341, analysis 2026091342.

Cross adherence to a prior equal-chance draw versus an undisclosed preferential
override with a realised net gain versus loss of 40 units of public access. Outcome
was unknowable when selected; participants see the complete audit now. Thus the
outcome manipulation concerns retrospective evaluation and may engage outcome bias;
it does not show whether a decision was reasonable given its original information.
Process is a bundle (draw adherence, consistency, favoritism and concealment), not
an isolated procedural-justice facet. No official/peer endorsement or personal
stakes are manipulated. No claim to isolate deference, private self-interest,
deception avoidance or all competing dispositions is made.

Every case has support/oppose options and the same JSON-choice schema. Choices have
no subsequent consequences in this pilot; the later moral experiment supplies
state-changing actions. Option mapping is balanced across the eight blocks and
held fixed within every arm/PD comparison. Each response is a fresh conversation;
all 56 cells within each block are shuffled. No common provider sampling seed is
claimed. The secondary outcome label is access gain/loss, not a moral rating.

## Profiles and controls

Retain the ten-coordinate Gaussian-copula/Beta draw with original R. Save each draw
unchanged. For E, V and S intervene on PD at 0.1 and 0.9. E and V retain all other
coordinates; S retains only PD's value and endpoint meanings. These intervention
rows are not natural joint-population draws. E uses the existing numerical profile;
V expresses the same values/endpoints as written percentages; S uses only the
corresponding PD sentence. U has no profile. E/V numerical information is identical,
but length, wording and presentation differ. S is an information ablation, not a
pure formatting control. Repeated S/U requests are sampling blocks, not distinct
personalities. All institutional axes are explicitly NEUTRAL; this is not a new
binary societal configuration. The nonprofile task instruction is common across
all arms and does not refer to absent profile information in U.

Full schedule: 8 blocks x 2 settings x 4 procedure/outcome cells x
(2 E + 2 V + 2 S + 1 U) = 448 participant calls, plus one Claude design review.
The earlier 12-block/672-call draft was only a sizing example. Eight blocks reduce
worst-case byte-based reservations within the $2 ceiling before any responses.
This sample is for exploration; no adequate power or conclusive test is claimed.

## Review, spending and transport

One independent Sonnet 4.6 review receives this protocol, all eight task cells and
the seven profile/control renderings for the first background. It must accept with
no blocking issues before participant collection. Revise/reject stops; no automatic
rewrite, replacement review or changed stimulus is permitted within r1. Review is
AI methodological screening, not human task validation or a moral judgment.

Participant: gpt-5.4-mini-2026-03-17, temperature 1, reasoning none, default service,
JSON-object mode, maximum 64 output tokens. Reviewer: claude-sonnet-4-6, thinking
disabled, temperature 1, maximum 1024 output tokens. Official model pages accessed
13 September list $0.75/$4.50 and $3/$15 per million input/output tokens respectively:
[OpenAI](https://developers.openai.com/api/docs/models/gpt-5.4-mini),
[Anthropic](https://platform.claude.com/docs/en/models/sonnet-4-6/overview).
Each request reserves decoded UTF-8 content bytes + 1024 input tokens plus maximum
output, with the existing 10% accounting margin. No caching discount assumed.
Complete reservation must fit $2 and leave at least $4 Claude/$10 OpenAI under the
existing provider caps for the moral experiment. This is not a wallet-balance check.

Reuse the shared write-once ledger with all 1,814 previous records and the parent
archive preserved. Unknown charges retain full reservations. No failed slot is
overwritten or retried. Strictly parse choice A/B, reject duplicate keys/extra
fields, and preserve malformed actions as missing. A transport/parser termination
failure stops; an invalid decision schema remains a scored missing action.

## Analysis fixed before collection

Report every cell's assigned, valid and support counts. For each setting and each
E/V/S arm report T = support(high PD,P+O-) - support(high PD,P-O+)
- support(low PD,P+O-) + support(low PD,P-O+). The candidate expectation T>0 is
derived now from thesis Appendix A's process/outcome distinction; it is not claimed
as the researcher's original hypothesis. No significance, equivalence or pass/fail
test is specified. Report component cells alongside T; a positive interaction alone
does not prove two opposite signed action effects.

Use 9,999 whole-block bootstrap resamples plus conservative Hoeffding intervals
from the existing contrast function. They are marginal, conditional on these two
settings, not simultaneous intervals or uncertainty over a population of domains.
With missing blocks retain assigned-denominator identification bounds and a clearly
labelled complete-block supplement; do not report the complete-data interval.
U has no PD contrast. S and U repetitions reflect model sampling, not variability
in their unprovided coordinates. No pooling with earlier studies or held-out
confirmation designation. Preserve all outcomes, including flat/contrary effects.

After collection verify exact request reconstruction, source hashes, scoring,
costs, old archives and a new full archive with zero API calls. Interpret feasibility
and alternative explanations before any separately designated next study.
