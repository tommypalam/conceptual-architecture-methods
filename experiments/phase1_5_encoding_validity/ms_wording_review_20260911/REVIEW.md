# MS wording and reported explanations: offline review

The review identifies plausible interpretive differences and an attribution
problem. It does **not** identify a defective MS paraphrase, prove that P2
ignores MS, or repair the failed robustness evidence. No API calls, prompt
changes, new coding rules or gate revisions were made.

## Evidence and reading scope

All **240 MS/S2 records** from the completed 640-call replication were extracted
and checked against their immutable source files. The other 400 records remain
in the original analysis. Qualitative reading covered **104 explanations**:
all 80 at MS=.9, plus call indices 1-3 at .1 and .5 in each of four wordings.
The other 136 remain in the full local evidence pack.

This selection was fixed before reading the explanations, after inspecting the
aggregate results; it is therefore **post-result and unblinded**, not a registered
independent audit. No labels were selected for inclusion. Examples below were
chosen after reading to illustrate both interpretations and counterexamples;
they do not provide prevalence estimates. These are model-reported explanations,
not access to an internal decision process or proof of reasoning faithfulness.

## What the theory and question actually specify

[Thesis section 3.1](../../../Theory/concepts_as_architecture_thesis_v0_6.md)
defines MS through the breadth of application across persons and cases; Appendix A
includes both moral-circle breadth and universal application of principles.
The variable dictionary retains the same local-to-universal axis.

The high endpoint descriptions used in the experiment are:

| Wording | Exact high-MS endpoint |
|---|---|
| Canonical | universalised, generalisable, broadly applied |
| P1 | prescriptions extend across diverse contexts and persons through generalizable application |
| P2 | norms extend across situations and generalize to encompass diverse persons |
| P3 | principles apply broadly across situations and extend to diverse persons through generalization |

All four retain the intended broadening direction. The paraphrases make the
objects being generalised explicit as prescriptions, norms or principles.
That can change emphasis, but the thesis itself includes principles and cases;
the outcome difference alone does not establish semantic invalidity. There is
no observed endpoint reversal, missing MS value or obvious unique P2 defect.
Existing human approval is not retroactively revoked by an unfavourable result.

The theory separately predicts **higher MS -> more FORMAL_REPORT in S2** through
broader institutional-integrity obligations (section 6.1.1). That is a
probabilistic behavioural hypothesis, not the definition of moral scope itself.
It remains the prespecified hypothesis and is not being replaced in this review.

The [locked S2 dilemma](../../phase0_baseline_calibration/questions/S2_quiet_error.md)
deliberately says that classification is genuinely contestable. Formal reporting
adds independent compliance classification and maximal transparency; local
correction fixes the record, logs it and adds a preventive check, but leaves
classification outside independent compliance review. Neither option is defined
as concealment or indifference to everyone beyond the colleague.

Consequently, broad concern could be invoked to defend institutional oversight
or a generally applicable, proportionate correction policy. This is an
interpretive limitation of using the binary decision as a unique readout of MS,
not evidence that the original probabilistic prediction is untestable or should
be silently discarded.

## What the saved explanations show

Canonical high-MS reporting explanations often connect general standards with
independent institutional classification. For example,
[canonical .9, call 0007](../original_expanded_20260911/records/MS_S2/canonical/v0.9/call_0007.json)
mentions "broadly applicable standards" and then prefers compliance classification
over leaving the record formally unclassified.

P2 high-MS local-correction explanations can explicitly invoke the same broad
standards while choosing the other procedural path.
[P2 .9, call 0011](../original_expanded_20260911/records/MS_S2/paraphrase_2/v0.9/call_0011.json)
states "fair procedure, internalized standards, and generalizable norms" before
endorsing correction and a preventive check as proportionate.
[P2 .9, call 0001](../original_expanded_20260911/records/MS_S2/paraphrase_2/v0.9/call_0001.json)
explicitly mentions "high moral scope and procedural concern" while rejecting
formal review as potentially excessive. Merely naming MS does not demonstrate
that it caused the choice or that its numerical value was recovered accurately.

Counterexamples matter. [Canonical .9, call 0015](../original_expanded_20260911/records/MS_S2/canonical/v0.9/call_0015.json)
also invokes moral scope while choosing local correction.
[P2 .9, call 0017](../original_expanded_20260911/records/MS_S2/paraphrase_2/v0.9/call_0017.json)
chooses formal reporting and describes independent classification as protecting
institutional trust and the colleague from ad hoc handling. The explanations
therefore do not sort perfectly by template or action.

There are also factual-framing concerns on both sides. In
[canonical .9, call 0010](../original_expanded_20260911/records/MS_S2/canonical/v0.9/call_0010.json),
contestability is treated as a reason to escalate whenever classification is
uncertain, although the question supplies no general ambiguity-must-be-reported
rule. In [P2 .9, call 0014](../original_expanded_20260911/records/MS_S2/paraphrase_2/v0.9/call_0014.json),
the response says the case already fits the minor-error criteria despite the
explicit contestability. These could express adopted classifications or overstate
what the question establishes; the wording should not be treated as demonstrated
faithful premise use. No new quantitative factuality score is assigned.

## Why MS wording alone cannot yet be blamed

The programmatic comparison verifies that **all ten endpoint descriptions change
in each paraphrase**. All ten numbers, the user dilemma, preamble, normative
context and task block remain identical at a fixed MS value.
See [exact comparison](wording_comparison.json).

Other changed descriptions are relevant to the reported choices. For example,
P2's low-MoR endpoint specifies "private reassessment and self-modification",
where canonical uses "internal, reflective, self-adjusting". P2's low-RT endpoint
mentions "significant breaches or egregious failures", where canonical says
"only major violations activate response". These are plausible sources of
changed emphasis, not established causes or grounds for revoking approval.
PD and ID are also named in explanations under both action labels.

The design can establish that the **full wording condition** changes responses.
It cannot isolate the contribution of the MS stanza, the other nine descriptions,
or their interaction. We should not diagnose a specific lexical repair from
the current comparisons, nor assume more sampling alone would remove the gap.

## What remains established

- Canonical MS/S2 replicated a strong response: FORMAL_REPORT 0/20/70% at
  .1/.5/.9, endpoint +.70 with the previously reported adjusted test.
- P2 remained 5/5/5%. Its coherent explanations do not turn a flat observed
  choice curve into positive encoding evidence.
- Broad concern is not synonymous with automatic escalation. A single action
  label and a plausible rationale do not by themselves identify encoded MS.
- The review offers hypotheses about interpretation and identifies an unresolved
  attribution problem. It provides no causal mechanism proof or active-trait
  recovery result. Original gate results remain unchanged.

## Smallest useful next diagnostic, if pursued

Use a fresh concurrent **2 x 2 wording decomposition**: MS stanza from canonical
or P2, crossed with the other nine stanzas from canonical or P2, at MS=.1/.9.
All ten descriptions are present, every retained stanza is verbatim, the values
are unchanged, and S2 stays locked. At N20 this would be eight conditions and
160 calls, including both original full-template controls collected anew.

This would distinguish the MS-stanza contribution from the rest-of-profile
wording contribution and possible interaction. It would not isolate semantics
from wording length, or guarantee improved encoding. The mixed compositions
would be new experimental prompts and need an exact frozen protocol, reviewable
preview and applicable dispatch approval before use. No runner, frozen paid
allocation, approval request or API call for this suggestion has been made.

No theoretical meaning, benchmark, scoring manual, parameter set, distribution
or pass threshold was changed. Phase 1.5 remains open. The positive canonical
replication is retained, as are all unfavourable results. Spending for this
review is **$0**; approximately **$3.98** remains in the tracked allowance.
