# MoR reasoning review: diagnostic, unblinded

All 20 existing active-MoR audit items were inspected, including successes,
errors and minority decisions. No new coder was called and no blind labels were
changed. [The inventory](TRACE_INVENTORY.md) links every item to its source;
the JSON pins the exact source, audit and reasoning hashes.

Claude assigned quartile 2 to 19 items and quartile 1 to one, with no abstentions.
The four exact matches are all true-quartile-2 items. This near-constant coding
does not discriminate the manipulated values; it does not by itself tell us
whether the generator, its short explanation, the coder, or several components
are responsible. Original accuracy remains 4/20 and the original audit stands.

## Comparison with intended meaning

[Thesis 3.1 and 4.2](../../../Theory/concepts_as_architecture_thesis_v0_6.md)
define MoR as internal/reflective self-adjustment versus external/behavioural
response. The implementation endpoints specify internal, reflective,
self-adjusting versus external, behavioural, confrontational. Internal
endorsement is not synonymous with internal response: LL and ID also concern
endorsement. Fair procedure belongs to PD. A rationale citing these other
dimensions may be legitimate joint-profile reasoning, but is weak evidence
from which to recover MoR's exact quartile.

The following notes are qualitative observations, not new gold labels or a
replacement scoring rule. Full IDs, values and decisions are in the inventory.

| Item prefix | Observation from the saved rationale |
|---|---|
| 3ba475 | Promotion justified through fairness, reliability and readiness; response mode not explained. |
| 9dadf5 | Promotion justified through procedure and internal endorsement; endorsement is not MoR evidence alone. |
| 3c182c | Local correction, logging and prevention proposed; local action does not uniquely identify a quartile. |
| bad5cf | WAIT justified through process, staff harm and mixed evidence; continuity is compatible with low MoR but nonspecific. |
| 5cd3fd | Promotion justified through trust, reliability and procedural fairness. |
| 5a74df | Local correction justified through proportionality, trust and accountability. |
| 5ca201 | Local correction justified as proportionate; inferred response mode overlaps with procedural interpretation. |
| b6386c | WAIT justified through procedure, endorsement and disruption; conditional under-delivery is mentioned. |
| 190e10 | Promotion justified through fairness and readiness despite the higher MoR value. |
| 709518 | Promotion rationale again centres on fairness, reliability and readiness. |
| 840095 | Promotion rationale centres on collaboration, stability and readiness. |
| 117746 | Formal reporting justified through independent review and legitimacy; external action receives quartile-2 coding. |
| 5aa891 | Local correction is called genuine internal correction; Claude assigns quartile 1 to true quartile 3. |
| 27baee | WAIT justified by uncertainty, procedural fairness and endorsement, despite value .7. |
| 597309 | WAIT rationale calls the productivity dip real without retaining its explicit under-delivery condition in that phrase. |
| dac6db | ADOPT justified through peer uptake and future positioning, with proposed transparent reassignment. |
| 2ecf76 | Promotion justified through balanced criteria and process, despite value .9. |
| b4182b | Formal disclosure justified through procedure and internalisation; Claude still assigns quartile 2. |
| c30b42 | Local correction preferred at .9 to avoid disproportionate harm; high MoR does not force one action. |
| 06cf52 | WAIT at .9 justified by uncertainty and staff disruption, retaining the under-delivery condition. |

These patterns suggest two diagnostic questions: does the short explanation
expose response-mode reasoning, and does the coder distinguish it from
endorsement/procedure? They do not establish a semantic inversion or justify
rewriting definitions. The S3 subset has only six items; its selected .9 item
is WAIT, one of the minority responses in the original 50-call cell. Do not
use this small subset to contradict the complete canonical decision curve.

## Consequence for the next test

Fact grounding remains a coherent, limited candidate for preserving conditional
scenario information. This review does not demonstrate that it repairs MoR
interpretation. The next focused screen compares grounding and repetition at
all five MoR values, including fresh endpoints in the same collection batch.
This avoids attributing cross-batch endpoint differences to the overlay and
tests whether response survives at intermediate values. It is not a full battery.

If the curve is flat, reversed, pinned or fails the existing directional rule,
do not scale that candidate automatically. If promising, reasoning and
representation checks still remain before independent battery confirmation.
No trait-specific hints, desired decisions, altered original prompts, corrected
audit labels or integration of the optional tool are introduced by this review.
