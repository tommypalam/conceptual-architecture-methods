# Offline evidence candidate and optional retrieval scaffold

Prepared 2026-09-11 on `phase1-5-validity`. No paid calls, prompt edits, runner
integration or Phase 2 activity. Phase 1.5 remains open with its gates unmet.

## Scope and rationale

Testable idea: some wording sensitivity may reflect varying assumptions about
the dilemma's procedures. The existing twelve-response Claude inspection
suggests this possibility, but cannot establish causality or explain GPT's
internal reasoning. This candidate exposes a complete, traceable evidence
reference without assigning a preferred decision. S3 is selected because it
already has a documented large wording effect; it is not a fresh holdout.

The sheet reproduces the entire locked loader body in paragraph order. It uses
no model-generated paraphrase and no selective list of missing procedural facts.
A generic instruction distinguishes unspecified details from established facts
and permits proposed procedures if explicitly identified as proposals. This
instruction is a new experimental intervention requiring exact review, not a
claim that the effective prompt has stayed unchanged.

## Phase 0 boundaries for exploration

The researcher authorises exploration within the purpose and accepted closure
of Phases 0a, 0b and 0c. The governing interpretation is the
[Phase 0 closure](../../PHASE0_CLOSURE_2026-07-29.md), including its documented
measured-baseline and inference-tier decisions, rather than superseded demands
to rebalance every dilemma to 50/50 or automatically descope.

- **0a: preserve the calibrated problems.** Keep both the archived originals
  and the accepted recalibrated set unchanged. No answer cues, altered stakes,
  new factual assumptions or outcome-driven re-recalibration.
- **0b: isolate delivery effects.** An evidence sheet or tool response is added
  context even if the source files are unchanged. A future candidate comparison
  must include matched no-profile controls with and without that addition, as
  well as the parameterised comparison and repetition control. Otherwise an
  overlay-induced default cannot be distinguished from parameter influence.
  The neutral-valued ten-parameter profile is not a no-profile control.
- **0c: separate exploration from validation.** Keep a record of every candidate
  and failed screen. Freeze the selected complete condition and analysis before
  fresh confirmatory sampling; never promote development responses to holdout
  evidence. The existing naked-prompt holdout remains valid for its recorded
  condition, not automatically for the new delivery. A new condition needs its
  own measured baseline and independent validation before substantive use.

Offline verification on September 11 confirmed all six working source files
match the original Phase 0c manifest; the candidate's S3 source hash matches
that lock too. This establishes source preservation, not harness neutrality.
Exploration authority does not change the OpenAI spending stop, activate the
optional tool, weaken Phase 1.5 gates or authorise a theoretical departure.

## Optional architecture

Implementation: `code/research_support/evidence.py`.

- `EvidenceCard` is immutable and checks that its paragraphs reconstruct its
  pinned body hash. Preparation uses the existing question loader explicitly
  pointed at the working Phase 0b dilemma, not its historical Phase 0a default.
- `EvidenceProvider` specifies stable lookup by scenario ID. Memory and JSON
  implementations return identical cards or `UnknownScenarioError(id)`.
- Both providers hold snapshots. JSON construction validates a caller-supplied
  artifact hash and schema before serving; later file changes cannot silently
  alter a running lookup. To use a revision, construct a new provider.
- `EvidenceTool` depends on the provider protocol, not either implementation.
  Its sole operation reads the rendered reference for a catalogue ID. No model
  argument becomes a filesystem path. It cannot draw profiles, change state,
  rank actions, or dispatch calls.
- `render_evidence_card` is shared by the local facade and direct text preview.
  Matching returned bytes establish software substitution, not equivalence
  between tool delivery and prompt delivery in an LLM.

This applies single responsibility, interface segregation and dependency
inversion with a small contract. An additional provider can implement that
contract without modifying the consumer. Liskov substitution is checked through
shared behavioural tests: equal content, errors, immutability and snapshot
semantics. Invalid catalogue construction can fail before either is used.

No existing engine module imports this package. The one-way preparation import
uses the existing question loader. The entire optional package can be omitted
without changing the active runner. There is no SDK tool registration, routing
framework or provider dependency.

Thesis section 4.1 describes a future tool that runs the encoding algorithm and
draws profiles. This evidence facade does **not** implement that theoretical
tool; it prepares a reusable retrieval boundary only. Sampling, parameter
reinjection and the later complex-agent architecture remain separate decisions.

## Reproduction and checks

From the repository root:

```text
python code/prepare_validity_evidence_candidate.py
python -m pytest tests/test_research_evidence.py -q
```

Preparation writes only new artifacts and refuses differing existing bytes.
Four test cases cover both adapters' lookup contracts, complete source coverage,
absence of calibration-note leakage, source preservation, tampering and
conflicting-artifact refusal. These are software checks, not scientific results.

The manifest records source and artifact hashes. Pinning validates provenance
against those supplied hashes; it does not certify the grounding instruction's
meaning or authorise use. Only trusted application code supplies catalogue paths.

## Future empirical comparison, not scheduled or authorised

If the text and later spending are approved, use GPT's same pinned model and a
small fixed screen before any full sweep. Original, previously approved
formulations must stay distinct; no canonicalisation of all four inputs.

A defensible comparison should distinguish the original input, a repetition
control (same repeated source and labels without the grounding instruction),
and the complete candidate. Otherwise a change cannot be attributed to the
grounding instruction rather than repetition or context length. Tool delivery
should remain outside that first screen to avoid another simultaneous change.
Exact placement and all complete messages must be frozen before collection.

Predetermine allocations, gross-failure stopping criteria, uncertainty handling
and cost cap; do not expand a favourable subset after inspecting outcomes.
Reduction of the known S3 gap would be exploratory local evidence. Lack of a
significant gap at small N would not establish equivalence. Saturation or loss
of parameter responsiveness would not count as success. PD/S1 retains its
prespecified directional role; S3 has no newly invented PD directional target.
No candidate closes Phase 1.5 without the required validity battery.

Current next step: review the prepared exact text and perform further offline
inspection if needed. OpenAI calls remain prohibited by the researcher's
spending instruction. The completed 80-call Claude authorisation does not
automatically fund new helper calls.
