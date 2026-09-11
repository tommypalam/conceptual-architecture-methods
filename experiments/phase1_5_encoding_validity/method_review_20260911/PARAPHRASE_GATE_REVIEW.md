# What the paraphrase gate establishes

Reviewed September 11 against the thesis, implementation specification, accepted
Phase 0 closure and completed evidence. This is a methodological review, not a
protocol amendment, gate waiver, authorisation for Phase 2 or new experiment.
No API calls, source-prompt edits or theory changes were made.

## Finding and correction

### Subsequent researcher clarification: sufficient, bounded encoding

The objective is to establish whether ethics can be encoded into agents to a
defensible extent, with Phase 1.5 supplying the evidence for that eventual
claim. It does not demand perfect robustness to all wording. The existing
operational criterion already reflects tolerance: at least 24/30 cells must
establish equivalence within ten percentage points across the four reviewed
formulations. Six cells may remain outside the equivalence-established set;
that is not a declaration that six demonstrated divergences are harmless.

Interpret "encoding rather than manipulation" operationally as evidence that
the specified ethical parameters exert interpretable behavioural control that
survives the prespecified representation checks, rather than a preferred answer
being produced by incidental phrasing or near-fixed default behaviour. All
prompt-based implementations influence outputs through text; these tests do
not prove a unique internal mechanism or confer moral correctness on decisions.

Sufficient evidence must combine parameter sensitivity, the intended meaning
and direction where prespecified, recoverability assessed against appropriate
baselines, robustness and decision headroom. Success on one dimension is not
automatically success on the others. Claims can describe demonstrated effects
at their actual scope while keeping unvalidated parts of the wider framework
explicit. A selectively chosen successful subset is developmental evidence
until independently validated; it does not silently redefine the original gate.

This clarification affirms the empirical objective and the existing tolerance.
It is not a new margin, altered parameter set, gate waiver or approval of a
reduced-scope Phase 2. No additional API spending follows from recording it.

### Original review finding

The current project makes paraphrase robustness part of its central encoding
claim. It is not currently an optional portability check. The assistant's earlier
suggestion that it could simply become a limitation of an otherwise validated
fixed implementation was too permissive for this specification.

There is nevertheless a legitimate distinction between demonstrating an effect
within a fixed implementation and demonstrating the stronger robustness claim.
Both deserve separate reporting. The distinction does not retroactively change
what this project's pre-existing gate requires.

## What the governing documents say

| Source | Commitment | Consequence |
|---|---|---|
| [Thesis 8.1.3](../../../Theory/concepts_as_architecture_thesis_v0_6.md) | Same numeric profile and semantically reviewed definitions; decision distributions equivalent within .10 across template paraphrases | Approximate distributional robustness, not identical individual responses or invariance to arbitrary text changes |
| [Specification 4.3.3](../../../Theory/implementation_specification_v0_1.md) | At least 80% of the 30 rotation/problem cells establish equivalence across all four versions | The operational target is 24/30; it is not a requirement that every possible wording produce identical behaviour |
| [Thesis 8.2 and 8.3](../../../Theory/concepts_as_architecture_thesis_v0_6.md) | Full pass needs all four subtests; large paraphrase divergence blocks Phase 2 under the current mechanism | Robustness is a prerequisite for the documented central claim |
| [Specification 4.5](../../../Theory/implementation_specification_v0_1.md) | Severe paraphrase failure requires substantive revision and supervisor discussion before re-attempting Phase 1.5 | Calling it an expected property of LLMs does not itself clear the gate |
| [Phase 0 closure](../../PHASE0_CLOSURE_2026-07-29.md) | Keep locked dilemmas, measured naked baselines and inference tiers; recognise the demonstrated harness effect | Preserve exact wording for reproduction, and do not transport naked baselines to modified delivery without qualification |
| [Recorded follow-up implementation](../../../docs/phase1_5_followup.md) | All-pair equivalence, complete sampling and parse-quality requirements | Preserve the executed rule and its historical results |

Two short statements make the thesis's intended scope explicit. Section 8.1.3
says that "the language is supposed to be a transparent vehicle"; section 8.2
requires that "behaviour is robust to lexical paraphrase" for a full pass.
The review does not endorse every causal interpretation in those sections as
proved by the tests; it identifies the project's stated commitments.

## Phase 0 and Phase 1.5 ask different questions

Phase 0a/calibration selected and measured dilemma formulations. The accepted
later closure preserved the recalibrated set, found substantial harness effects
in 0b, and retained the independent naked holdout in 0c with measured baselines.
Fixing those exact strings prevents hidden stimulus changes and makes the
recorded condition reproducible. It does not assert that any new wrapper,
response schema or agent profile preserves the same baseline.

The Phase 1.5 paraphrases concern the descriptions of agent parameters in the
system template. They do not rewrite the locked dilemma. They deliberately
test whether a reviewed alternative description is behaviourally substitutable
at the same parameter values and context.

A conceptual distinction helps:

- **Within-template response:** does varying a numeric parameter change the
  decision distribution while the rest of that implementation stays fixed?
- **Across-template robustness:** does the distribution stay sufficiently close
  when the reviewed description changes while parameter values stay fixed?

The first can hold when the second does not. Neither alone demonstrates ethical
correctness, faithful internal reasoning, continuous joint encoding of all ten
parameters, or the framework's complete central claim. An implementation can
be reproducible and parameter-sensitive while remaining description-dependent.

## What the evidence actually supports

The [original battery assessment](../phase_review_20260909/BATTERY_ASSESSMENT.md)
records within-template complete sweep criteria for MoR/S3, PD/S1 and MS/S2 in
the full harness. It also records unresolved broader gradient and reasoning
recoverability issues. Removing the paraphrase requirement would therefore not
automatically validate the entire remaining architecture.

The original paraphrase result is 8/30 equivalent cells, against 24 required.
This does **not** mean that 22 cells have proved meaningful wording effects.
The [offline diagnosis](../offline_diagnosis_20260909/FINDINGS_AND_NEXT_STEP.md)
separates equivalence, imprecision and demonstrable divergence. Its simulations
found zero all-pair equivalence successes in 10,000 trials at N=50 when all four
true probabilities were .5. That is a documented precision limitation, not a
mathematical assertion that success is impossible. The eight original equivalent
cells were near common response boundaries, limiting their discrimination.

Separately, the original PD=.8/S3 P2/P3 gap survived conservative simultaneous
bounds across the full set of formulation rates. Increasing precision cannot
be assumed to make an actual discrepancy disappear. Thus low power is a reason
to qualify inconclusive cells, not a reason to erase the demonstrated effect.

The [latest sensitivity diagnostic](../evidence_sensitivity_20260911/analysis/INTERPRETATION.md)
finds a grounding-arm MoR endpoint response of +.667, conservative >=95%
interval [.261,.897]. It also finds a low-PD P2/P3 observed gap of +.433 with
nominal interval [.030,.722]. The latter is secondary and not family-adjusted;
it does not establish a lower bound above .10. Local response is supported,
uniform wording robustness is not established, and no fundamental hard cap
follows. These selected developmental results do not replace the original battery.

Nor does wording dependence by itself prove a unique internal mechanism such
as stereotype activation. Imperfect operational equivalence of descriptions,
underspecified procedures and interactions among descriptions are possible
explanations to investigate, not excuses established by this review. Human
semantic approval is important provenance; it is not behavioural validation or
direct access to the model's reasoning process.

## Recommended decision

1. **Retain the original gate and its outcome.** Phase 1.5 remains open and
   Phase 2 remains on hold. No automatic descope, parameter removal, threshold
   relaxation or designation of partial pass.
2. **Report distinct findings separately:** effects within the exact canonical
   implementation; robustness of reviewed alternatives; precision limitations;
   remaining gradient/interpretability limitations. Do not call them all one gap.
3. **Stop treating smaller wording gaps as the optimisation objective.** A
   candidate must preserve interpretable parameter response and decision
   headroom as well as address robustness. A nearly fixed answer is not a repair.
4. **Use existing canonical evidence before further spending.** The original
   five-value sweeps already address much of the fixed-template question. Any
   new diagnostic should name the missing inference it resolves, keep meanings
   fixed, and leave fresh confirmation separate from development.

For now this is an interpretation and research-priority decision, not a change
to the architecture. Downgrading paraphrase robustness to an optional limitation
would amend the stated theory/protocol and narrow the claim. It would require
explicit discussion and approval, preservation of the original outcome, and a
defensible rationale beyond having observed an inconvenient result. The user's
binding-constraint rule still applies; no demonstrated physical or technical
impossibility of robustness has been established here. Do not implement that
amendment automatically.

## A defensible current-results paragraph

Under fixed prompt implementations, selected parameter manipulations produced
behavioural differences. The planned validity battery did not establish the
broader combination of graded encoding, active-parameter recoverability and
robustness across reviewed descriptions. Paraphrase results contain both a
demonstrated large discrepancy and substantial uncertainty from a low-powered
equivalence design. Subsequent controlled development screens support local
parameter response under an evidence-grounding addition, while description
dependence remains unresolved across tested values. These findings characterise
the tested implementation and do not establish either general ethical encoding
or a fundamental impossibility of achieving it.

This paragraph is proposed reporting language, not an edit to the source thesis.
No new money was spent. The latest recorded estimate leaves approximately
$7.85 of the $9 allowance; it is not a verified account balance.
