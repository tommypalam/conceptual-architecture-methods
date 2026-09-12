# Concepts as Architecture

## A Probabilistic Framework for Encoding Political-Ethical Concepts in LLM-Based Agents

**Tommaso Piero Palamenga — Bocconi University**
**Provisional abstract · 12 September 2026**

Political-ethical concepts offer a possible organising structure for artificial
agents' judgments, but their translation into computational representations
requires evidence that the resulting behaviour is systematic, interpretable,
and robust to how those representations are expressed. This paper develops
PARIA, a probabilistic framework for investigating whether psychologically
grounded definitions of freedom, justice, authority, care, and loyalty can
generate distinguishable patterns of individual and collective decision-making
in large-language-model-based agents. The architecture represents individual
heterogeneity through ten bounded parameters with Beta marginals linked by a
Gaussian copula, and varies normative context across a five-axis configuration
space. Its distributional assumptions and concept-to-parameter mappings remain
explicit, revisable modelling commitments.

The evaluation programme separates operational feasibility from encoding,
behavioural, and moral validity. Completed calibration and locked-holdout studies
across six managerial dilemmas revealed substantial sensitivity to agent-framing
scaffolds and unequal decision baselines; an operational pilot established
end-to-end pipeline functionality. These findings motivate interpretation
against measured baselines rather than assumed neutrality. The completed original
encoding-validity battery collected 39,000 behavioural
responses and a separate 200-item reasoning audit. Only 8 of 30 paraphrase cells
established equivalence against 24 required; representation retention and active-
trait recovery were insufficient to clear the gate. Subsequent diagnostics
identified local parameter influence. In a final 360-response test across 20 new
complete profile backgrounds, Mode of Response and Moral Scope produced positive
average endpoint effects, while Relational Embedding remained unresolved. Moral
Scope did not exhibit an ordered three-level response. Evaluation therefore
closed with evidence of partial behavioural parameterisation and the full validity
gate unmet. Conditional on this validity gate,
the planned main study compares a shared agent population across selected
societal configurations in individual dilemmas and multi-round collective tasks.
Further evaluation will examine obedience, conformity, bargaining, helping,
and reactance using canonical and decanonised scenarios and configuration
counterfactuals to probe possible benchmark contamination. A proposed dual
moral metric combines configuration-relative judgments with fixed-standard
assessment, subject to human coding validation. Prespecified mixed-effects
analyses and sensitivity checks will assess dependence on parameterisation,
distributional structure, and model choice.

The intended contribution is an auditable method for testing the explanatory
value and limits of explicit conceptual encodings. Evidence of human behavioural
validity, conceptual understanding, or improved moral performance is not yet
established.

**Keywords:** normative AI; political-ethical concepts; agent-based simulation;
probabilistic modelling; encoding validity; behavioural validation.

## Editorial status — outside the abstract

This is an abstract for the complete **PARIA / Concepts as Architecture** paper,
not the entire Cognitive Hexagon programme. It deliberately uses prospective
language for unfinished work and makes no claim that the main study is already
preregistered. Completed encoding results and their limits are documented in the
[Phase 1.5 closure](../experiments/phase1_5_encoding_validity/PHASE1_5_CLOSURE_2026-09-12.md);
its local transfer study does not validate the full architecture. Phase 2 remains
on hold. Earlier completed-work statements are grounded in the
[Phase 0 closure](../experiments/PHASE0_CLOSURE_2026-07-29.md) and
[Phase 1 operational pilot](../experiments/phase1_pilot/PHASE1_PILOT_RESULT_2026-07-29.md).

Planned methods derive from the [thesis](../Theory/concepts_as_architecture_thesis_v0_6.md),
[implementation specification](../Theory/implementation_specification_v0_1.md),
and recorded validity protocols. Replace the prospective sections with actual
sample sizes, effect estimates, uncertainty, and limitations only after those
studies are completed. No favourable result is presupposed.
