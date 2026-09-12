# Revised Phase 2: encoding, social behaviour and ethical consequences

Prepared 12 September 2026 on `phase2-design-20260912`.
**Status: concrete design proposal; not preregistered or released for collection.**

The researcher requested a rigorous but expedited continuation and clarified
the thesis objective: establish whether AI can functionally use an ethical
encoding during decision generation, investigate resemblance to human behaviour,
and evaluate whether its actions and consequences are good or bad. Both the LPM
population design and Agents-of-Chaos-inspired group interaction remain central.
The researcher set a **$100 absolute API ceiling**, asking to spend as little
as feasibly possible. This is a ceiling for the new Phase 2 package, not a target,
not a renewal of the old Phase 1.5 allowance, and not permission to alter evidence.

## 1. The claim and its tests

Use “functional ethical understanding” as a research question with observable
requirements, not as a synonym for any changed answer. Pre-generation placement
of a profile is an application-level fact. Context-sensitive decisions, transfer,
robustness and interpretable failure patterns provide behavioural evidence about
using that representation. Neither placement nor verbal self-description reveals
a unique internal mechanism. Provider training and alignment remain in every arm.

| Question | Necessary evidence | What does not answer it |
|---|---|---|
| Does encoding participate in generation? | Frozen request contains the profile before the first decision; raw output retained; contemporaneous control without a profile; predicted profile sensitivity reported | Editing the answer after generation; an explanation that merely mentions ethics |
| Does it support broader functional use? | Effects tested in new contexts and genuinely new tasks, with predictions and representations frozen before collection | New profiles on old dilemmas; selecting the best wording after results |
| Does behaviour resemble humans? | Comparison with independent human measurements and experimental manipulations; report variation and effect patterns, not only average agreement | Plausible prose, arbitrary 50/50 targets, or one model judging another human-like |
| Are actions/outcomes good or bad? | Approved dual moral coding with human validation; consequences established by task facts or an explicit outcome model | Treating human-like, compliant, profile-consistent or consensus behaviour as inherently good |

Phase 1.5's accepted limited conclusion remains intact. All ten coordinates and
negative results remain visible. Phase 2 is not another attempt to pass its old
battery. No new parameter-to-action rule or preferred answer is specified here.

## 2. Scope and order

1. **Phase 2A: paired population study.** Retain N=200, all ten parameters,
   unchanged Beta marginals and R, all three locked simple dilemmas and ten
   environments. Add a matched context-only control. This tests behaviour beyond
   the neutral setting studied in the later Phase 1.5 work.
2. **Phase 2B: bounded group study.** Retain C1, C2 and C3, their agent counts,
   round structure, role rules, private evidence and per-round reinjection. Begin
   with the two existing anchor environments and matched no-profile controls.
   This is a limited comparison of whole environments, not five-axis validation.
3. **Transfer, human resemblance and moral evaluation.** Preserve the later
   programme explicitly. A separately frozen transfer suite is necessary before
   claiming unseen-task generalisation; Phase 3 supplies the existing five human
   benchmark families. Phase 4 supplies dual moral coding. Preparation of these
   components can occur offline while the Phase 2 implementation is checked.

Budget-based reductions are prospective proposals, not post-results exclusions.
Group expansion is not selected because initial effects look promising. Any
later expansion must have its own frozen scope and remain within the aggregate
budget; this document does not queue it. None of the six dilemmas or ten parameters
is removed from the research programme. The Appendix A minimum-thesis descope
route is not invoked.

## 3. Phase 2A conditions and population

**E — encoded:** canonical profile with all ten values supplied before generation,
plus the concrete social environment and locked dilemma. Preserve the generated
decision exactly; the application may parse it but may not replace it ethically.

**U — unencoded, context matched:** same environment, dilemma, model, format and
sampling settings, with no profile values, parameter names or endpoint definitions.
Use a self-contained task instruction that does not refer to a nonexistent
profile. The two exact prompts must be reviewed and frozen together. This estimates
the effect of the *whole profile-injection package*, including added text; it does
not by itself separate semantics from prompt length or isolate each coordinate.
The old naked Phase 0c baselines are historical context, not this control arm.

Each of 200 sampled profiles receives every environment and simple problem in
E, with one independent U response paired to the same experimental slot. U does
not see that slot's profile. Those are independent baseline replicates, not 200
different unencoded personalities. No pooling of old responses into this cohort.

One population is drawn, stored and hash-locked before collection. Keep the
existing unused `phase2_simple` root seed 20260605; freeze separately derived
schedule and analysis seeds. Randomise/interleave arm and environment order,
keeping fresh, isolated conversations. Different arms receive independently
derived call seeds. API seeds do not guarantee identical stochastic realizations.

Use the recalibrated locked question directory
`experiments/phase0b_calibration/questions` explicitly. Preserve its exact text
and historical filenames. Use `gpt-5.4-mini-2026-03-17`, temperature 1,
600 maximum output tokens and no model substitution. Record all effective
settings, including reasoning configuration and provider-supported seed behaviour.

**Allocation:** 200 profiles x 3 problems x 10 environments x 2 arms = **12,000
generation calls**. No live calls have been made under this design.

## 4. Environments: a verified identification problem

The existing draft has Freedom = Justice in all ten rows. Its intercept-plus-five-
axis design matrix has exact rank 5, not 6. Balanced marginal coverage alone does
not permit separate estimation of the two effects. This is a mathematical
limitation, not a disappointing behavioural result.

The offline preflight proposes replacing **00111 with 01111**, retaining the other
nine configurations, both anchors and at least three rows at each axis level.
Rank becomes 6. The proposal is selected without reading response outcomes:
exhaust all single non-anchor replacements, require full additive rank and the
existing coverage constraints, maximise entropy of pairwise Hamming distances,
then mean distance and lexicographic order. See [design checks](design_checks.json).

This is a minimal repair proposal. It does not prove global entropy optimality
over every possible subset, and it is not the same calculation as the existing
greedy farthest-point heuristic. Freedom/Justice separation would still depend
heavily on one environment. Consequently, primary analysis treats environments
as categorical packages; separate additive axis coefficients are exploratory.
Full rank does not establish power or identify all axis interactions.

Proposed codes, in inherited order:
`00100, 11011, 00001, 11110, 00010, 11101, 01111, 11000, 00000, 11111`.

Do not overwrite `config/configurations.json` on the strength of this proposal.
The final subset and its concrete descriptions need review together. Descriptions
must express the thesis's structural definitions; the fallback statement that
LOW axes are “penalised” is not a sufficient approved operationalisation.

## 5. Primary analysis to freeze before collection

The observational unit is a response; the independent sampling unit for population
uncertainty is the profile/paired slot, not every repeated response. The primary
analysis must preserve all arms and environments within each resampled profile.

For each problem, propose a binomial logistic mixed model with a profile random
intercept, categorical environment effects, E/U arm and arm-by-environment terms,
all ten centred parameter values, and arm-by-parameter terms. Values attached to
U are blinded slot attributes; their coefficients are negative-control quantities.
No automatic removal of parameters, stepwise search or best-sign selection.

The two proposed primary directional tests are the arm-by-PD terms in S2 and S3:
more PD-associated FORMAL_REPORT in S2 and WAIT in S3 when the profile is delivered.
These directions come from the independent PD confirmation, not a newly invented
mapping. Their extension across environments is a new hypothesis and may fail.
Use two-sided tests with Holm correction over the two tests; a significant wrong
sign is counterevidence. These are conditional population associations; correlated
free draws do not identify an isolated causal intervention on PD.

Report predicted probabilities and paired arm differences for every environment,
not just odds ratios. Environment-by-arm heterogeneity, S1, the original directional
predictions and all other parameter terms are secondary/exploratory, reported
completely with a prespecified multiplicity family. Do not use a failed average
PD effect to erase a real context reversal. Failure to reject is not equivalence.

Before release: implement this exact estimator, specify its convergence/failure
handling and contrast definitions, and simulate null calibration and power on
at least 1,000 synthetic datasets per declared scenario. Include small/moderate
effects, near-ceiling S1/S2 cases, between-profile dependence and no profile effect.
Do not power the design only at the unusually large earlier PD endpoints. N=200
is inherited and provisional until this check; no power result is claimed now.
If the model fails on a real dataset, preserve that failure; a predeclared simpler
paired analysis is sensitivity evidence, not a silent substitute primary result.

All planned slots stay in the allocation table. Report missing, API-failed,
unparseable and refused responses by arm/environment. Do not code them as morally
bad, silently retry them, or hide them in a complete-case denominator. Report
complete-pair results with denominators and worst-case binary missingness bounds.
Final inferential rules must be frozen before dispatch, not after missingness occurs.

## 6. Phase 2B: Agents-of-Chaos-inspired interaction

Retain the custom interaction architecture, not only independent questionnaire
answers. This repository labels its own population runner “LPM” and orchestrator
“Agents-of-Chaos-style”; direct reuse of AgentTorch or the original Agents of Chaos
source has not been established. Describe implementation lineage accurately.

| Task | Preserved design |
|---|---|
| C1 | Five members, up to five rounds, unanimous early termination or final binding vote |
| C2 | Six members including a CEO, five rounds, amendments affecting the working plan, final five non-CEO votes |
| C3 | Four founders, six rounds, asymmetric evidence and legitimate sharing, seeded 2-2 tie-break |

Propose **10 matched groups per problem**, each exposed to both anchors `00100`
and `11011`, under E and U. Fix group membership, CEO seat and exogenous evidence
assignment across those four conditions; conversations develop independently.
Maintain the original separate neutral no-profile bridge, 10 groups per problem.
Ten groups is an exploratory feasibility-scale allocation, not a claim of adequate
confirmatory power. Show group-level intervals and full trajectories.

At maximum round counts: each group consumes 25 C1 + 30 C2 + 24 C3 = 79 calls
across the three tasks. Ten groups x (2 environments x 2 arms + 1 neutral bridge)
x 79 = **3,950 calls**. These counts exclude postfiltering, coding and failures.
For C2/C3 the ceiling is fixed; C1 may finish early under its existing rule.

Report whole-environment effects and paired E/U differences. Do not infer an
individual authority or justice effect from the two anchors, which differ on all
five axes. Interacting outcomes are clustered by group. If profiles are reused
across groups, report overlap and account for that dependence; calls and seats
must not be treated as independent human subjects.

Implementation findings to resolve before group collection:

- `bridge_neutral` currently renders as `00000`; introduce an explicit neutral
  context using the established neutral definition, not an all-low surrogate.
- The bridge prompt currently omits the CEO role note as well as the profile.
  Keep role and interaction instructions equivalent across arms.
- Current group selection depends on configuration, so groups are not presently
  matched across environments. The revised matched design needs its own manifest.
- C3 evidence content is marked placeholder in `problems.py`. Author and review
  the actual evidence before freezing; labels/polarities cannot stand in for facts.
- The current per-round sharing set is mutated while calls complete, so leakage
  classification can depend on completion order. Use a frozen prior-round view;
  make newly shared content available only at the specified next-round boundary.
- Private evidence is logged as held but only newly delivered evidence is rendered.
  Verify that earlier private information remains accessible, and that legitimately
  shared content is actually visible rather than just its ID.
- Verify executable amendment adoption and working-plan state in C2. The action
  label alone does not implement a changed plan.
- Persist complete per-call requests, responses, model settings, token usage,
  seeds and dispatch intents during each round; a summary written at run end is
  insufficient for interrupted-run recovery and budget accounting.

These are readiness findings, not completed repairs. Use versioned prospective
components and tests; preserve frozen historical code packages and records.

## 7. Postfilter comparison and human resemblance

The inexpensive existence claim needs proof that E's first decision contains the
encoding and is not replaced by an application filter. This is distinct from
claiming superiority over a postfilter. For that stronger comparative question,
propose a **separate optional anchor-only arm F**: take each already-saved U draft
and let one later call review it using the same normative profile and context.
Preserve both versions and their linkage. There are 1,200 additional calls for all
200 profiles x 3 tasks x 2 anchors, with no duplicate base generation.

F is a particular post-generation editor, not every possible safety filter. It
has two calls versus E's one, so report cost, latency and revision rates; do not
claim compute-matched superiority. A quality comparison additionally needs the
approved moral manual. F is optional and **not in the default allocation**;
priority under the cap goes to the population study, group study and validation.

For human resemblance, retain all five thesis benchmark families and the canonical/
decanonised and counterfactual requirements. Phase 2's bespoke dilemmas have no
verified human reference sample here. Published benchmark agreement would support
limited retrodiction, not full human fidelity. New human participants require a
separate recruitment/consent and cost plan; none are enrolled by this document.
Do not substitute synthetic human responses for that missing reference.

Methodological context: [Aher et al. (2023)](https://proceedings.mlr.press/v202/aher23a.html)
show both replicated experimental patterns and distortions in simulated human
behaviour. [Bisbee et al. (2024)](https://doi.org/10.1017/pan.2024.5) show that matching
survey averages can coexist with incorrect variation and relationships. These
motivate checking effect structure and heterogeneity, not mean resemblance alone.

## 8. Moral assessment without building the answer into the generator

Retain the thesis's eight configuration-relative categories and four fixed-standard
categories; raters evaluate saved actions separately from generation. Do not tell
the behavioural model the score it should achieve. Freeze the manual before Phase 2,
as the existing specification requires. This proposal does not waive that timing.

Keep good, neutral, bad and unassessable evidence distinguishable. A binary action
label alone is insufficient where the current dilemma leaves consequences or
proportionality contestable. In particular, FORMAL_REPORT and WAIT are not globally
“good” answers. Distinguish stated intentions, enacted simulation events and merely
hypothetical downstream consequences. No claim of realised welfare follows from
an LLM's promise to protect staff without an implemented transition/outcome model.

Human raters should be blind to arm, profile and model identity. Fixed-standard
judgments use the same task facts across environments; configuration-relative
judgments necessarily require the relevant local institutional facts. Concealing
the arbitrary configuration code is compatible with supplying those facts.
An LLM agreement score alone does not establish human validity. The original
human-coding plan costs far more than $100; human labour is a separate feasibility
constraint. Do not silently replace it with synthetic “expert” ratings.

The category definitions, worked examples, handling of ambiguity, rater sample,
reliability targets and external review remain concrete launch prerequisites.
No moral-coding rules or human sign-off are claimed as completed here.

## 9. Budget and stopping

**Default allocation:** 12,000 simple + up to 3,950 group calls = **15,950**.
Optional F adds 1,200, giving 17,150; it is not automatically funded or dispatched.
Human benchmarks, transfer items and moral ratings have separate allocations;
any API work for this Phase 2 package shares the same absolute $100 ceiling.

Verified 12 September 2026: standard GPT-5.4-mini text pricing is $0.75 per million
input tokens and $4.50 per million output tokens; regional processing can add 10%.
[Official model documentation](https://developers.openai.com/api/docs/models/gpt-5.4-mini).
Pin the snapshot; price verification does not verify account access or balance.

For planning only, at 1,000 input + 150 output tokens per simple call, the simple
study costs $17.10 before any regional uplift. At an illustrative 2,000 input +
200 output tokens per group call, 3,950 group calls cost $9.48. **About $27 is an
illustrative generation estimate, not a reserved amount or a promise.** Longer
transcripts, rater prompts and the full 600-token output cap change the bound.
No batching/caching discount is assumed and no model is switched to save money.

Plan for generation within **$60** and total package API charges within **$90**,
leaving $10 unused margin under the absolute cap. These are planning allocations,
not new spending permissions. If the worst-case reservation cannot fit, reduce
or defer a complete prospective module before collection and disclose the change;
do not relax output settings or discard observations mid-run.

Before each batch, atomically reserve the full uncached input bound plus maximum
output cost for every in-flight request. Reconcile known usage; keep unknown-charge
requests at their full reservation. Disable hidden SDK retries. Any later explicit
retry is a new linked record with a new reservation, never an overwrite. All
providers, evaluator calls and recovery segments share one ledger. Stop before
exceeding the stage allocation or $90 operational ceiling; never rely on unused
provider credit or anticipated cache savings. Exact prompt/transcript bounds and
the tested spending guard are required before any launch.

No outcome-dependent stopping, selective extension, prompt optimisation or sample
rerolling. A technical or budget stop preserves every response and dispatch intent
and is reported as incomplete. The fact that $100 is authorised does not resolve
the remaining protocol, coding or configuration decisions.

## 10. Required review and next executable work

The scope adjustment is the authorised task. Adoption of the proposed configuration,
new comparator prompts and changed group allocation is distinct from implementing
their drafts. New interpretations must be reviewed before research execution.

1. Review this concrete scope, including the single-environment repair, E/U arms,
   smaller anchor-only group comparison and optional status of F.
2. Prepare/freeze exact descriptions and control prompts; complete the moral manual
   and required review; implement analysis and offline null/power checks.
3. Repair and test the identified group behaviours in a prospective version. Render
   complete request manifests, verify live model access without an experiment,
   and compute the full reservation against the shared cap.
4. Finalise the preregistration packet and commit verified artifacts. Public OSF
   registration remains required by the current protocol and is not claimed done.
5. Dispatch only the released allocation, preserving all negative and incomplete
   results; assess the three research questions separately.

### Five synthetic review perspectives

Decision under review: preserve the thesis objective and both simulation designs
while making Phase 2 a bounded comparative study under the new budget.

- **Linden:** pre-generation ethical representation is substantively relevant,
  but “understanding” needs context-sensitive use, transfer and stated limits.
  Neither conformity nor one preferred decision defines ethical success.
- **Osei:** retain a matched control and real human reference evidence. Small
  group counts give exploratory evidence; plausible dialogue is not human validation.
- **Tanaka:** repair exact axis aliasing, account for repeated profiles/groups,
  preserve correlated-coordinate caveats and simulate power before freezing N.
- **Renna:** keep population and interaction layers connected; a static questionnaire
  alone would leave the intended social and ethical consequences untested.
- **Okafor:** fix bridge neutrality, evidence flow and per-call recoverability
  before group spending; a working mock loop is not sufficient execution readiness.

Disagreement: maximise breadth versus spend on a direct postfilter comparator and
independent validation. Proposed resolution: retain all parameters and problems,
use matched E/U as core, restrict initial group environments, keep F optional,
and do not spend the validation allowance on an extra sweep. These are internal
synthetic perspectives, not external expert endorsement or human approval.

## Sources and verification

- [Original operational specification](../../Theory/implementation_specification_v0_1.md), Parts 5–9.
- [Accepted closure](../phase1_5_encoding_validity/ACCEPTED_CLOSURE_2026-09-12.md).
- [Independent PD confirmation](../phase1_5_encoding_validity/structural_encoding_20260912/pd_confirmation/analysis/REPORT.md).
- [Original main-study plan](../../docs/pre_analysis_plan.md), retained as historical scope.
- [Offline preflight](../../code/phase2_design_preflight.py) and [regression tests](../../tests/test_phase2_design_preflight.py).
- [LPM source](https://arxiv.org/abs/2507.09901) and [Agents of Chaos](https://arxiv.org/abs/2602.20021): methodological sources, not proof of direct library integration.

No raw response, frozen question, distribution, correlation matrix, existing
configuration file or production runner was changed. The newly added preflight
only computes design arithmetic. No paid calls or fresh-environment full-test
pass are claimed. The separate desktop response-data transfer remains unverified.
