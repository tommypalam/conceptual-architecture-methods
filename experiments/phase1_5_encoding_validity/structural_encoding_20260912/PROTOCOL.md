# Structural encoding evaluation: diagnostics, all-parameter sweep and blind audit

Prepared 2026-09-12 following the researcher's instruction to follow the structural
objective, test the needed evidence, then sweep every parameter. This instruction
supersedes the spending pause. The authorised additional total remains $25,
including conservative reservations. No theory or locked prompt is edited.

## Theory alignment

Thesis v0.6 section 4 defines conceptual encodings as generative inputs; section
4.2 ties the ten coordinates to explicit behavioural tendencies; section 8.3
explicitly calls the central claim structural. This reasonably supports testing
whether normative representations participate in generating decisions, rather
than merely evaluating finished answers. Section 3.5 requires traceability from
definition through profile to output.

Sections 4.1 and 4.1.1 permit system-prompt injection and external state. They do
not require ethics to be learned in the model's weights or establish that the
model has an intrinsic moral understanding. The AGI ambition is the researcher's
broader programme, not an empirical claim established by this thesis. Architectural
causal influence, internal model mechanisms and moral quality remain distinct.
No theory update is necessary to investigate the architectural interpretation.

## Evidence requirements and coverage

| Requirement | Check |
|---|---|
| The normative representation reaches the decision generator | Offline request reconstruction: all ten values, correct endpoints, pre-decision system message, exact locked dilemma; raw decisions are parsed without an ethical replacement rule. |
| Responses depend on the intended coordinate | Paired-background numerical interventions, other nine coordinates held fixed; all original nine directional hypotheses retained. |
| Response is more than an extreme endpoint switch | Five levels .1/.3/.5/.7/.9, endpoint and interior (.7-.3) contrasts, every observed curve reported. |
| Effects survive alternative expressions | Independent diagnostic panel of canonical, three human-approved paraphrases, numeric-only and verbal-only variants for MoR/S3 and MS/S2 on fresh backgrounds. |
| Influence extends across the parameter set | Full canonical coverage of ten parameters x three locked dilemmas x five levels on 20 fresh backgrounds. Unpredicted signs remain exploratory. |
| Explanations contain recoverable profile information | After a complete sweep, prepare the existing 200-item blind quartile audit; retain active-trait, majority-baseline and literal-threshold analyses. Claude coding is independent of the behavioural model. |

These measures triangulate the structural interpretation; behavioural tests and
self-explanations cannot prove a unique internal mechanism. The existing failures
of paraphrase equivalence, retention and recoverability are not reset. A small
diagnostic panel is not a full 24/30 equivalence reassessment. No replacement gate
or automatic Phase 2 release is created. Report normative orientation rather than
labelling a particular S2 action morally better.

## Fixed collection sequence and budget

1. Offline integrity and mock execution tests; no paid calls.
2. Diagnostic panel: 8 new backgrounds x 2 parameter/problem pairs x 5 levels x
   6 representations = **480 calls**. Draw seed 20261005, schedule seed 20261006,
   analysis seed 20261007. All representations and backgrounds retained.
3. Full parameter sweep: 20 different new backgrounds x 10 parameters x 3 problems
   x 5 levels = **3,000 calls**, one response per background/condition. Draw seed
   20261008, schedule seed 20261009, analysis seed 20261010. This is complete
   parameter/problem/value coverage, not a rerun of the original 15,000-call
   two-delivery-arm allocation. Forty or fifty observations per cell are not claimed.
4. Independent 200-item audit selected using the existing stratification algorithm
   and seed 20261011, after all sweep outcomes exist. Render exact coding requests
   and verify their reservations against the remaining budget before dispatch.

The panel precedes the sweep. It is not a search that chooses the best representation:
the sweep stays canonical regardless of which representation looks strongest.
Valid negative diagnostic results remain reportable and do not cause selective
substitution, threshold relaxation or extra sampling. Technical/integrity failures
halt dispatch; resolve and document them before any subsequent stage. The full
sweep maps the scope of effects; it is not promised to pass the original battery.

Each stage's complete conservative reservation is checked before launch. Reserve
the panel and sweep jointly below $22, leaving at least $3 for the audit within
the $25 ceiling. The initial 600-call panel would reserve $22.22371875 jointly
with the sweep, leaving less than the planned $3 audit reserve. The panel was
reduced to eight backgrounds before collection; the full sweep remains 3,000.
This budget-based choice was made without observing any new model outcomes.
If exact audit payloads do not fit the remainder, do not dispatch
a partial audit or silently exceed the cap; report that constraint. The old $9
allowance is separate. No external provider balance has been verified.

Behavioural model gpt-5.4-mini-2026-03-17, temperature 1, max output 600, neutral
context, concurrency 3, one attempt per slot. Previously reviewed paraphrases and
the existing six-bin verbal mapping are used without new endpoint meanings.
The canonical source messages and question-loader output must match exactly when
rendered at original profiles. Only profile values change in the full sweep.

All backgrounds are unselected draws from the unchanged Beta/Gaussian-copula
sampler. Intervening on one coordinate produces counterfactual profiles, not an
unchanged sample from the joint population. Preserve all draws and rendered
values. No Phase 2 cohort is created. No adaptive sample size or rerolling.

## Analysis fixed before collection

For every parameter/problem/representation, report all five rates, the mean
background-level .9-.1 contrast and .7-.3 contrast, and nominal 95% plus
Bonferroni intervals controlling both contrasts across all groups in that stage.
Use 100,000 shared whole-background bootstrap resamples, NumPy linear quantiles.
Coverage is approximate, especially for the eight-background panel; one response
per background/condition limits precision. Calls are not independent sampled agents.
Report all contrasts, including those without prespecified directions.

Orient the nine thesis 6.1.1 predictions toward their predicted label. For the
other 21 parameter/problem pairs, report the first response label and label the
contrast exploratory; do not count absent hypotheses as failures. An adjusted
positive predicted contrast supports that endpoint effect locally, not the entire
architecture. Intermediate-range evidence also requires a positive adjusted
interior contrast and nondecreasing observed target rates across five levels.
Failure of observed ordering does not prove nonmonotonicity of the true curve.

Representation differences, slope-retention ratios and all-pair equivalence remain
diagnostics with their actual uncertainty; no N=8 non-significant difference is
called equivalence. The original battery's criteria and historical outcomes stay
unchanged. The interpretation report must distinguish endpoint influence, graded
response, representation dependence, recoverability and unresolved mechanism.

One immutable JSON and dispatch intent per call. Failures stop after their current
batch and remain archived. No automatic retry or in-place continuation. Missing
outcomes prevent complete-stage labels. Coder output never changes an agent's
decision. Retain source hashes, source model versions, request seeds, raw responses,
usage, timestamps and local backup checksums.
