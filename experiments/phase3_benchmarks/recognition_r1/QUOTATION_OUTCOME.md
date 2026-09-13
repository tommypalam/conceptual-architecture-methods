# Free quotation complete; paid screening not released

The researcher explicitly approved disclosure of the ten frozen recognition
bundles and 36 original images to Anthropic for token counting. All ten free
requests completed successfully. Their exact response/request links are saved
under `quotes/`; no recognition output or paid API call was generated.

| Family | Canonical input tokens | Alternative input tokens |
|---|---:|---:|
| Authority | 2,787 | 2,568 |
| Perception | 7,252 | 7,290 |
| Allocation | 844 | 1,179 |
| Helping | 1,173 | 1,411 |
| Restriction | 2,213 | 2,621 |

The original [cost plan](cost_plan.json) reserves **$10.90678875** for 500 probes
and 100 initial coding calls. It excludes disagreement discussion and therefore
cannot be called the complete specification-compliant screening budget.

The [complete prospective bound](discussion_cost_plan.json) includes a further
maximum of 100 discussion calls and totals **$14.06743250**:

| Component | Conservative maximum |
|---|---:|
| 500 Sonnet4.6 recognition probes | $8.07147000 |
| 100 initial coding calls, two independent raters | $2.83531875 |
| Up to 100 discussion calls, same two raters | $3.16064375 |
| **Total** | **$14.06743250** |

These are reservations using the frozen plan's prices, full output limits,
worst-case valid coding inputs, input/framing margins and the additional 10%
monetary allowance. They are not measured screening costs, price quotations
from a provider's billing system, or a prediction that every response disagrees.
Token counting estimates input usage; it does not verify balances or prices.

Provider maximums are **$11.44946000 Claude / $2.61797250 OpenAI**. Including
prior Phase 3 spending would bring them to $11.80824920/$2.67558225, within
the researcher's $15/$30 hard caps. Package accounting would be at most
$37.389904475 within $100. However, both the original $7 screening and $10
validation allocations would be exceeded. Their existing ledger guards remain
unchanged: no partial batch, silent allocation increase or new budget ledger.

## Prospective correction to disagreement handling

This corrects the proposed third-AI-only adjudication in PROTOCOL.md before any
paid screening. Retain the two independently generated original ratings. For
each disagreement (including uncertainty/refusal flags), the SAME two raters
receive the original answer and both original labels, with own/other identity
made explicit. Each independently reconsiders and returns a classification and
a brief reason. Thus the second round exchanges the raters' original positions;
it does not substitute the local Codex agent as a third deciding vote.

Use one bounded exchange only, at most ten unresolved answers per request,
at most 50 requests per rater if all 500 outputs disagree. The two discussion
responses are compared after both are preserved. Any remaining disagreement,
ambiguity or refusal stays unresolved and blocks a complete release decision;
there is no forced consensus, third-model tie-break, majority vote or automatic
extra paid round. Report agreement before and after discussion separately.
This is an AI discussion protocol, not independent human validation. The exact
output parser, response ordering, fixed-denominator analysis and linked paid
runtime still require implementation and testing before release.

The offline builder `code/phase3_recognition_discussion.py` defines exact request
construction and conservative bounds. Three new tests verify preservation of
both positions, opaque-ID/duplicate/label/length guards, partial batches and
separate rater identities. No new endpoint call follows from these tests.

Synthetic perspectives: Linden keeps recognition separate from understanding;
Osei retains the full stimuli; Tanaka requires unresolved disagreements to remain
missing rather than force consensus; Renna retains all five families; Okafor
requires the entire worst-case workload and historical spend to fit before any
dispatch. Resolution: preserve the completed quotes and resolve economical
delivery, allocation and runtime offline; do not reduce N or weaken stimuli to
fit the original rough allowance. These are written perspectives.

## Current status and next work

The token-count disclosure block is resolved. Ten quote records exist and are
reused on resume; all 48 paid historical records remain unchanged. Phase 3
spending is still **$0.41639895**, package $23.322471975.

Next, assess a cheaper delivery method for the SAME requests, or prospectively
allocate within the existing provider caps, then implement and freeze the linked
collector, parsers, discussion, analysis and all-call budget guard. A provider
cap fitting the proposal is not itself a release of the frozen $7 allocation.
No new paid screening is running or queued. No further token-count approval is
needed for these exact already-approved requests.
