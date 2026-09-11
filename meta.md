# PARIA decision log

Current decisions are recorded here; [NEXT_STEPS.md](NEXT_STEPS.md) owns execution
status. The [earlier log](docs/archive/meta_through_2026-09-06.md) is preserved
byte-for-byte, including its original encoding defects and historical templates.

## 2026-09-11 - Numeric-axis candidate collected, verified and not promoted

Completed all 7,900 planned slots across the original segment and four disjoint
continuations. There are 7,890 valid responses, ten preserved API failures, zero
parsing failures and zero returned-model mismatches. Verified original request
messages/profiles, all 7,900 unique requested seeds, 7,890 unique successful API
IDs, record hashes, byte equality to source segments and every raw ZIP payload.
The original frozen design/scorer and the ten unknown decisions remain intact.

Revised canonical/P1/P2/P3 PD=.8/S3 ADOPT rates are .15125/.330413/.689223/.107769;
baseline rates are .1075/.2125/.796992/.109023. Each arm establishes only one of
six TOST pairs (canonical/P3), not the required all six; invalid-outcome sensitivity
also fails all-pair equivalence. No all-formulation saturation flag. Revised
PD/S1 slope is 4.0153 (95% interval .5460 to 7.4846), p=.007488, extreme h=.4949,
but observed rates .94/.92/.98/1/1 fail the required monotonicity. The baseline
is separated and ceiling-limited. PD/S2 and S3 remain descriptive. The conservative
API-error flag is retained, but both substantive local criteria independently
remain unmet. No between-arm improvement test or new directional claim is added.

Synthetic interpretation review: Linden distinguishes failure of this candidate
from impossibility of ethical-concept encoding; Osei retains the selected familiar
problem, interruptions and model-specific scope; Tanaka retains all-pair TOST,
unknown sensitivity and the prespecified monotonicity rule without claiming the
small observed reversal proves population nonmonotonicity; Renna keeps the broad
ethical-concept objective and Phase 2 gate; Okafor requires complete disjoint
allocation and verified immutable records. Resolution: do not promote the
candidate or automatically expand collection. Use the finished evidence packet
for spec 4.5 review before further lexical re-engineering, preserving theory and
the user's consultation requirement. No supervisor contact or descope is inferred.

Recorded token cost $8.8045695; additional-budget estimate remaining $39.881084
after the prior endpoint diagnostic. Taxes/provider-only charges remain external.
The numeric report and figures are saved with a separate interpretation and
recovery ledger under `axis_instruction_20260911_assembled/analysis`.

Postprocessing initially stopped while plotting because floating-point Wilson
bounds produced a tiny negative error-bar length at a boundary probability.
Only the renderer was repaired: display lengths within 1e-12 of zero are clipped;
larger inconsistencies still fail. Numerical intervals and the frozen scorer
are untouched. Both figures were checked visually. Report v2 displays tiny
p-values in scientific notation and marks non-prespecified criteria explicitly;
the earlier derived report is retained. No extra API calls were used for reporting.

## 2026-09-11 - Preserve the third timeout segment and finish unsent slots

The previous continuation stopped on September 10 at 10:17 UTC after 56
requests: 55 valid, one timeout in revision/PD/S3/.7/call_0048. Its finalizer
also stopped safely. Collection remained stopped overnight. Across all unique
slots there are now 4,940 records, 4,930 valid decisions and ten API failures;
recorded usage totals $5.5044945. No failures are replaced or pooled with older
studies. The collection-time gap is retained in timestamps and provenance.

On September 11, the authenticated model-list check returned HTTP 200 and four
concurrent generic-text completion-endpoint diagnostics reached the server.
Prepared `axis_instruction_20260911_continuation_r4` for only the 2,960 unsent
slots from a byte-identical combined snapshot. The already-tested transport
recovery preparer and frozen executor are reused without edits; all nine source
code hashes, exact approval, requests, requested seeds and the combined $12
guard remain enforced. The prior synthetic recovery review still applies.

## 2026-09-10 - Technical continuation of the approved numeric-axis pilot

**Attached continuation timeout:** `continuation_r2` stopped at 1,864 records
(1,863 valid, one `APITimeoutError: Request timed out.`, no non-API invalids).
Across segments: 4,884 recorded, 4,875 valid, nine API failures; recorded token
estimate $5.443323. The failed slot is revision/P1/PD=.8/S3, call 0235. The
automatic finalizer stopped without assembling an incomplete final result.
Concurrent generic-text endpoint probes subsequently reached the server.

Prepared a new snapshot and `continuation_r3` for 3,016 never-dispatched slots.
The new preparer admits request timeouts as well as connection errors; the
frozen executor, retry policy, prompts, seeds, model, N, analysis and combined
$12 guard are unchanged. No failed request is replaced. The behavioural test
verifies timeout reservation, unchanged allocation and executor compatibility,
and refusal of authentication errors. Existing snapshot/guard checks also pass.
This is transport recovery under the existing approval, not a theoretical or
statistical amendment. Synthetic review retains all five previously recorded
positions, with timeout-related unknown usage disclosed alongside connection
failures; no outcome-based recovery decision or phase pass is inferred.

**Second transport interruption:** the first continuation's initial four calls
also returned connection errors, with no reported usage. Those P2 slots (two
per arm) are preserved alongside the original four P3 failures. Python SDK GET,
invalid-model POST, detached POST and four concurrent generic-text POST probes
then reached the server. These diagnostics generate no model decisions. The
cause remains unconfirmed; neither invalid credentials nor background execution
has been established as the cause. Automatic approval review rejected sending
full study prompts to a nonexistent diagnostic model; the safer probe instead
sent only repeated generic text, with no research data.

Prepared a byte-identical 3,020-record recovery snapshot and a second linked
continuation for 4,880 never-dispatched slots, retaining all eight unknowns and
the same combined guard. An attached process is used to keep failures visible.
The behavioural test now additionally verifies snapshot union, reservation of
all keys, byte equality and refusal of a tampered parent inventory. It passed.
No endpoint, analysis, original runner or prior recovery source was changed.

The attached second continuation began returning responses successfully; at
600 new responses no further terminal error was recorded, with $4.0306 combined
usage. Recovery checkpoint committed locally as `2fdfdcd1`. A local postprocessor
now waits for the continuation's successful terminal status, then archives,
assembles, applies the frozen scorer, verifies every planned request/profile/
seed and source/ZIP bytes, and renders the report. A failed continuation blocks
finalization; no extra calls or favourable-outcome override is permitted.
Results and the final milestone commit remain pending collection and review.

The original segment stopped after 3,016 records: 3,012 valid responses and
four preserved `APIConnectionError: Connection error.` records, all in P3
equivalence cells (two per arm). Recorded token estimate $3.360072. A read-only
authenticated model-list request subsequently returned HTTP 200. Recovery is
based on transport failure, not interim behavioural results.

Prepared a separate continuation for exactly 4,884 never-dispatched original
slots. Parent keys and hashes are reserved, including failures. Requests retain
the frozen original design, model, temperature, seeds and allocation order;
the continuation adds provenance only. Prior spending counts against the same
$12 guard. Original records remain unchanged and have a verified ZIP snapshot.
The user's exact pilot approval and instruction to continue cover these slots.

One behavioural integration test passed: excludes completed and failed slots,
resumes without extra calls, counts prior cost before dispatch, preserves source
bytes and assembles a complete allocation retaining the frozen scorer's terminal
failure flag. The storage adapter accommodates missing model identities on
connection failures; it does not change statistical analysis or gate decisions.

Synthetic review: Linden requires unchanged normative content; Osei notes the
collection interruption and forbids outcome-selected replacements; Tanaka keeps
the four unknown decisions and original sensitivity analysis; Renna preserves
the encoding objective; Okafor requires disjoint allocation, immutable hashes
and the combined guard. Resolution: resume only unsent slots under a linked
designation, disclose the interruption, retain the conservative failure flag,
and verify the byte-identical union before reporting.

## 2026-09-10 - One numeric-axis clarification candidate prepared

**Subsequent explicit approval:** the researcher answered "Approve the exact
revision" to the review request covering the added instruction, four exact
templates and 7,900-call pilot. Recorded the approval against all frozen hashes
and committed the preparation before outcomes (`6d6c81f8`). Launched the approved
pilot with the existing model, neutral context, seed 20260913 and $12 local
dispatch guard. No theoretical change or supervisor endorsement is inferred.

The researcher asked to continue after the endpoint result. Prepared one
theory-motivated operational candidate: a shared instruction to read both
endpoints jointly as an axis, interpret numerical positions continuously, retain
intermediate degree and apply all ten positions jointly. All definitions,
endpoint strings, parameter values, context, dilemma text and output schema
remain unchanged; no desired answer, arithmetic utility/probability mapping,
new trait hierarchy or new categorical cut-point is introduced. Its explicit
numerical scope preserves the accepted six-bin verbal convention. This is an
assistant-authored task instruction, not a newly independent Claude paraphrase.
The old reviewed Claude endpoint paraphrases remain the lexical manipulations.

Rationale: thesis 3.1/4.2 defines continuous axes and graded consequences; spec
4.1.3 calls for continuous rather than bucket-collapsed encoding. The prior
diagnostics implicate both endpoints, but do not prove that interpretation of
numeric positions caused the failure. This is a candidate hypothesis, not an
identified cure, and it affects all ten fixed positions although only PD is
manipulated in the pilot. One candidate is fixed before new outcomes; no
automatic search for wording yielding favourable ADOPT rates.

Design: 6,400 fresh PD=.8/S3 observations, canonical plus three previously
approved formulations, N=800 per formulation in baseline/revision arms. Add
1,500 fresh canonical PD sweep observations: both arms, all three simple
problems, five original values, N=50. Total 7,900; neutral context, same pinned
model/temperature/cap, seed 20260913. Matched baseline/revision job pairs are
randomised across the two components and within pairs; requested seeds differ.
Previous observations are not pooled and familiar scenarios are not called
held-out problems. Endpoint messages in the fresh baseline match frozen sources.

N=800 uses the saved equal-rate six-pair TOST precision simulation, approximately
91% success at true common p=.5, rather than claiming N=50 supplies adequate
equivalence power there. The old simulation and source hash are retained, not
rerun or mislabelled as predicted candidate success. Sweeps retain the original
N=50 and its known PD/S1 ceiling/power limitations. All six TOST pairs are
reported per arm; eligible invalid outcomes additionally undergo exhaustive
binary-completion sensitivity. Separate local progression requires revised
equivalence with that sensitivity, the original PD/S1 sweep criterion and no
all-formulation <=5%/>=95% saturation flag. This is a local screen, not a
replacement gate. No new PD/S2 or PD/S3 directional prediction is supplied.
Baseline-fail/revision-pass does not by itself test between-arm improvement.

Synthetic review: Linden supports clarifying the existing numeric axis without
changing endpoints, but requires review of the exact task instruction. Osei
requires fresh controls, forbids preferred-answer selection, and notes the
selected-PD scope and familiar tasks. Tanaka supports better-powered local
equivalence and unknown-outcome sensitivity; keeps the weak sweep and broader
budget/precision limits visible. Renna requires both stability and a graded
response, preserving the broader conceptual programme. Okafor requires frozen
sources, distinct seeds, immutable records, resumability and a spending guard.
Disagreement: a generic instruction may leave the underlying lexical dependence
unchanged and a conservative local screen may be inconclusive. Resolution:
test one candidate once, publish every outcome, and avoid automatic expansion.

Five focused tests passed, including exact-only insertion, balanced cells,
1,516 mocked calls with correct component scoring, distinct seeds and no-call
resume, saturation/invalid sensitivity, approval refusal, a pre-dispatch budget
stop and preserved terminal-failure refusal. Frozen plan, exact review and
protocol are under `axis_instruction_20260910`; no paid calls. Expected cost
about $9, $12 recorded-usage dispatch guard, approximately $48.69 available.
Taxes/provider-only retry charges remain outside exact local accounting.

Exact researcher review of the added instruction and four revised templates
has been requested. Spec 4.5 calls for supervisor discussion before re-attempting
the full Phase 1.5 battery after severe paraphrase failure. The protocol flags
that future review point; no supervisor contact or endorsement is implied.
The local pilot cannot establish all-parameter gradients, audit recoverability,
representation robustness or 24/30 equivalence. A full revised battery still
needs an explicit precision/budget plan; neither deadline nor budget authorises
a silent theory departure or gate relaxation.

## 2026-09-10 - Return to endpoint diagnosis within Phase 1.5

**Completed endpoint result:** all 1,200 responses are valid (300 per condition),
with no terminal API or model errors. ADOPT counts A/B/C/D are 266/151/119/15;
rates .8867/.5033/.3967/.0500. Prespecified simultaneous contrasts: low endpoint
+.3650 [.2464,.4721], high endpoint +.4717 [.3514,.5771], interaction +.0367
[-.1894,.2619]. Both main-effect intervals exceed the .20 planning target.
The interaction is unresolved; no additivity/equivalence claim is made. The
higher high-end estimate is not a tested claim of a larger effect than low-end.

Interpretation review (synthetic): Linden separates accepted intended meanings
from demonstrated model stability. Osei restricts inference to the selected
PD=.8/S3 and P2 background, and retains differing fresh control rates as a
cross-session limitation. Tanaka retains the frozen contrasts, simultaneous
bounds and small-interaction power caveat. Renna identifies both endpoints as
targets for a reviewed encoding revision rather than preferred-answer tuning.
Okafor verifies exact requests/profiles/model, unique keys/API IDs/seeds, all
hashes, analysis counts and byte-identical ZIP payloads. Resolution: report the
two large endpoint effects; keep the theory, original gate and Phase 2 hold;
no additional experiment or encoding revision has been launched.

First/last saved responses: 01:43:43/02:12:53 UTC, September 10. Root seed
20260912; neutral context; completion status 02:13:13 UTC. Four requests needed
two attempts, with all ultimately successful. Usage: 1,086,600 input and 110,977
output tokens, no cache; estimated cost $1.3143465 before taxes/unreported retry
charges. Estimated additional-budget remainder $48.6856535. The preparation
reservation and pending-review artifact remain historical; exact approval,
completion verification and the [report](experiments/phase1_5_encoding_validity/pd_endpoints_20260910/analysis/ENDPOINT_REPORT.md)
record the final state. Same-computer ZIP verified; no remote publication.

**Subsequent approval and launch:** with the exact endpoint review file open,
the researcher said "approved, do you also approve". Recorded human approval
against the frozen hashes and the separate assistant semantic assessment. The
assistant finds both mixed pairs preserve the accepted meanings/directions;
this does not establish behavioural robustness. All preparation artifact and
source hashes were verified before the 1,200-call launch. No frozen prompts,
model settings or analysis code changed. Collection remains within the additional
$50 budget and fixed stopping rule; actual token usage will be recorded at completion.

The researcher clarified that later simple problems should use LPMs and complex
problems an Agents of Chaos-style build, with the validity battery completed
first. They then explicitly instructed continuing the proposal made before the
"fire"/deadline discussion. This supersedes immediate prioritisation of the
alternative injection architecture in the earlier clarification below. The
objective of encoding the five concepts and following the theory is unchanged.

Prepared `pd_endpoints_20260910`: PD=.8/S3, other-nine P2 descriptions fixed,
four low/high PD combinations, N=300 each, pinned model/temperature/context,
root seed 20260912. Original factorial A and B become new A and D controls;
new B/C mix the low/high strings independently. All four collect fresh data.
No original experimental artifact or frozen source was changed. The executor
and exact-bound functions are reused; factor names and the seed are explicitly
updated in the new scorer. Nine offline tests passed, including endpoint-only
differences, control identity, exact-review refusal, immutable design, mocked
execution/resume and low/high scoring orientation.

The existing 20,000-repetition power plan is relabelled with its source hash:
the probability scenarios/weights are mathematically identical. N=300 retains
approximately 97% balanced-scenario power for 20-point main effects/40-point
interaction, and weak power for smaller effects. No new power simulation is
claimed. Four Bonferroni exact intervals supply simultaneous contrast bounds;
unknown decisions are expanded over binary completions; the 98% parse floor
and fixed stopping remain. Selection of PD/S3 and P2 background is post-hoc,
with restricted generalisation and no new ADOPT-direction hypothesis.

Synthetic review: Linden finds both mixed pairs preserve the already accepted
endpoint meanings, subject to exact human review. Osei retains fresh controls
and identifies post-hoc P2-background selection as a scope limitation. Tanaka
accepts reusing the identical mathematical power scenarios, with explicit weak
small-effect power. Renna keeps this diagnostic subordinate to the full battery
and original conceptual objective. Okafor favours the verified immutable runner
and distinct score labels over changing completed-run code. Resolution: proceed
with the authorised local diagnosis; do not select future encodings by preferred
decision rates or treat this result as a global battery pass.

The additional API budget is $50. Reserve $5 for planning this experiment
(expected approximately $1.35), with zero incurred spend at preparation. Exact
B/C review is requested after prompts, protocol, runner and checks are ready,
as required by `docs/phase1_5_followup.md`. Original A/D approvals are retained.
No further theoretical change or architecture switch is requested or implemented.

## 2026-09-10 - Research objective reaffirmed under deadline and budget

The researcher approved up to $50 additional API spending and specified a
submission-ready thesis in ten days, then clarified that the original purpose
must remain: implement the theoretical encoding of ethical concepts and test
whether it is possible. Deadline-driven conversion to a wording-only methods
study is not authorised. A final submission date of September 20 was an assistant
planning assumption, not a researcher-confirmed timestamp. No new calls have
been made against this additional budget at the time of this clarification.

Read thesis 4.1/8.2 and implementation specification 4.5. The theory explicitly
positions system-prompt delivery as the baseline and tool-based injection as
the target subsequent architecture; the decision tree names that route when
encoding fails. The spec also calls for lexically transparent prompt revision
and supervisor discussion after severe paraphrase failure. The next step must
connect the measured failure to that architectural route rather than continue
local wording investigations without a construct-encoding plan. No architecture
change, new theoretical mapping, gate relaxation or Appendix A descope was
implemented in this clarification. No supervisor message was sent.

Synthetic review: Linden preserves all five concept definitions and accepted
theoretical commitments. Osei requires the revised mechanism to earn behavioural
validity rather than treating a structured tool response as evidence. Tanaka
keeps the original gate and fresh-data distinction intact. Renna reconnects
the diagnostic work to the planned construct-injection architecture. Okafor
requires a concrete mapping to the existing sampler, persistent profile and
context interfaces before paid execution. Resolution: prioritise the specified
architecture and its falsifiable assessment; keep diagnostics subordinate to
that aim and consult the researcher on substantive departures. Budget and time
constraints are recorded, not used to silently narrow the research claim.

## 2026-09-10 - Four-condition wording diagnostic completed

**Completed outcome:** all 1,200 calls are valid, 300 per condition, with no API
errors, model mismatches, missing observations or retries. ADOPT counts A/B/C/D
are 255/45/161/25, hence rates .8500/.1500/.5367/.0833. Frozen simultaneous
contrasts: PD main +.5767 [.4574,.6780]; other-nine main +.1900 [.0767,.2973];
interaction +.2467 [.0223,.4635]. All intervals exclude zero. The PD effect
exceeds the .20 planning target throughout its interval; practical sizes of
the background and interaction effects remain less precisely resolved.

Interpretation review (synthetic): Linden retains the human-approved endpoint
meanings and treats this as a presentation sensitivity, without redefining PD.
Osei notes the selected profile and differing fresh A/D rates limit transport
and exact cross-session replication. Tanaka endorses the frozen simultaneous
bounds, while noting the wide interaction interval and no attribution between
the jointly changed low/high endpoints. Renna sees a concrete encoding target
and keeps global validity unresolved. Okafor verifies all frozen request messages,
profiles, model identities, unique keys/seeds/API IDs, checksums and byte-identical
archived raw files. Resolution: report all three effects and their limits;
retain the unmet gate and Phase 2 hold. No theory, gate or prompt revision and
no additional paid experiment is authorised by these outcomes.

Collection ran 00:47:01-00:56:44 UTC, neutral configuration, fixed PD=.8 profile,
root seed 20260910. Usage is 1,077,000 input and 109,683 output tokens, zero
cached tokens; estimated cost $1.3013235 before taxes. The verified ZIP is a
same-computer backup. All 1,200 raw records remain local and excluded from Git;
summaries, inventories, provenance and the
[report](experiments/phase1_5_encoding_validity/wording_factorial_20260910/analysis/FACTORIAL_REPORT.md)
are reviewable project artifacts. Historical preparation and approval below
remain preserved in order to distinguish pre-collection choices from outcomes.

**Subsequent approval and launch:** the user replied "go for it" directly to
the exact-combination B/C review request. Recorded this explicit approval with
the frozen template/message hashes in `review_approved.json`; retained the
original pending artifact and preparation checksum inventory. Started the
1,200-call experiment at 00:47 UTC with all model, prompt, design and analysis
hashes unchanged. A thin operational launcher calls the frozen execute/score
functions, placing the Windows byte-range process lock in ignored `output/`
so the lock cannot obstruct reading experiment files into the final ZIP.
Launcher source and approval hashes are recorded separately in provenance.
No scientific protocol change, additional export or theory amendment occurred.

The researcher said "go for it" following the proposed PD/S3 wording attribution
test. Prepared the concrete design, exact prompts, executable runner, analysis,
budget and offline power calculation. No real calls were made. The prior
proposal explicitly requires exact-template review of the new mixtures B/C;
those combinations are now reviewable. Earlier human approval of P2/P3 is
retained for unchanged A/D. No theoretical departure or new export permission
is requested. No new words were generated: only PD endpoint strings are copied
between the already approved P2/P3 templates.

Decision: 300 fresh calls per condition (1,200 total), fixed PD=.8/S3, neutral
full harness, pinned gpt-5.4-mini-2026-03-17, temperature 1, cap 600, root seed
20260910. Randomized four-request blocks distribute temporal drift; seeds
include condition and block. Three prespecified probability-scale contrasts
use simultaneous bounds derived from four Bonferroni exact rate intervals.
Unknown decisions expand intervals over all binary completions; the 98% parse
floor remains separate. No old outcomes are pooled and no phase gate changes.

Power: 20,000 offline simulations per scenario and N=100/200/300/400. N=300 is
the smallest grid value above 80% for both 20-point main effects and a 40-point
interaction in the balanced scenarios (approximately 97% each). Power is only
about 5% for the illustrated 10-point main effect and 20-point interaction.
These limits prevent interpreting a null as absence of wording sensitivity.
The binomial assumptions require stable independent within-condition responses;
blocking alone does not establish independence. Profile/pair selection was
post-hoc, so this remains exploratory and cannot establish global validity.

Synthetic five-perspective review: Linden finds no endpoint-direction change
in copying the two approved PD strings, while retaining exact-combination human
review. Osei supports fresh A/D controls and temporal balancing, with restricted
generalisation from the selected profile. Tanaka supports simultaneous exact
bounds and unknown-outcome sensitivity but flags severe conservatism and low
small-interaction power. Renna distinguishes presentation attribution from
theory revision or repair of the original gate. Okafor requires frozen source
hashes, write-once records, deterministic resume and terminal-failure refusal.
Disagreement: a larger study would identify smaller effects more reliably but
would exceed the intended small diagnostic. Resolution: retain 1,200 calls,
publish all interval widths, explicitly leave small effects unresolved, and do
not authorise adaptive extension based on outcomes. No constitution rule changes.

Validation: six focused offline tests passed, including unchanged A/D exact
messages, endpoint-only mixing, independent confidence-bound verification,
contrast/unknown handling, approval hashes, eight-call mock collection and
idempotent resume, scoring, and preserved terminal failure. Separate comparison
confirmed all four profiles/user messages identical and only PD endpoints
differ within A/B and D/C. Expected cost $1.30455 based on historical PD/S3 token
lengths and official prices checked September 10; output-cap estimate $4.0536
before taxes/retries. No new Claude calls. See the
[frozen protocol](experiments/phase1_5_encoding_validity/wording_factorial_20260910/PROTOCOL.md)
and its exact-template review. All original records and frozen code are intact.

## 2026-09-09 — Offline diagnosis authorised, theory held fixed

The user asked what could be done while leaving the theory alone, then accepted
the proposed offline diagnosis. No API calls or theory, source prompt, model,
criterion, or recorded observation changes were made. New diagnostic code and
artifacts are separate from the frozen analysis.

Exploratory method: simultaneous Clopper–Pearson intervals over all 120 binomial
rates, Bonferroni alpha .05, expanded over every possible binary completion of
invalid parses. Interval subtraction bounds all 180 rate differences. Categories
and a .95/.05 saturation flag are explicitly post-collection diagnostics. The
original all-pair TOST and parse floor remain unchanged. Three focused tests
passed against independent beta-quantile bounds, unknown-outcome envelopes,
interval symmetry, and the frozen equivalence precision behaviour.

Results: 8/30 equivalent and saturated; 4/30 within-margin observed ranges but
equivalence not established; 17/30 larger observed ranges with inconclusive
conservative bounds; 1/30 with a difference beyond .10 supported by those bounds.
The latter is PD=.8/S3, paraphrase 2 versus 3: 32/50 vs 2/50, observed difference
.60, simultaneous interval [.1488,.8495]. The 17 include the parse-disqualified
MoR/S2 cell, whose status remains explicit. Conservative inconclusiveness is not
evidence of no effect, and saturation agreement does not establish encoding.

Offline simulation, seed 20260909, 10,000 repetitions per hypothetical scenario,
used the exact existing six-pair rule for four truly equal probabilities. At
p=.50, all-pair success was 0/10,000 for N=50 and N=100, .0175 at N=200, .3506 at
N=400. An explicitly labelled planning extension to N=800/1200 gave .9113/.9942.
Monte Carlo intervals and five rate scenarios per N are saved. These values
describe sampling precision under equality, not observed model reliability or
a revised gate. No repeated real-data collection is licensed by the simulation.

Synthetic review: Linden keeps concepts fixed and distinguishes human semantic
consistency from model invariance. Osei requires fresh observations for any
post-hoc-selected diagnostic profile. Tanaka requires family-wide uncertainty,
explicit invalid-response sensitivity, and separating simulated precision from
real-data evidence. Renna identifies whole-template manipulation as an attribution
limitation. Okafor recommends isolating one parameter's wording from the other
nine before more expensive battery runs. Resolution: preserve the unmet original
gate, qualify the interpretation with the demonstrated precision limitation,
and propose a two-by-two exploratory PD/S3 wording study for discussion only.
No sample size, mixed-template human approval, spending or dispatch is assumed.

Artifacts: experiments/phase1_5_encoding_validity/offline_diagnosis_20260909/,
including a rate heatmap, all profiles/pair bounds, simulation data, and the
plain-language FINDINGS_AND_NEXT_STEP.md. No theoretical departure implemented.

## 2026-09-09 — Paraphrases complete; empirical battery gate not met

Completed all 4,500 approved paraphrase calls: 4,497 valid parses, three preserved
parsing failures, no API failures or model mismatches. MoR/S2/paraphrase_3 has
48/50 valid and misses the 98% parse floor; PD/S2/paraphrase_1 has 49/50 and
remains eligible. Eight of 30 cells establish all-pair TOST equivalence, versus
24 required: seven S1 cells and RE/S2. No S3 cell establishes equivalence.
The protocol, approved templates and fixed N were not changed after results.
Estimated token cost $5.055; checksums, local ZIP and combined evidence saved.

Descriptive pooled first-option rates on S3 are 50.8%, 72.0%, 77.8%, 55.0%
for canonical and paraphrases 1–3. The fixed PD=.8/S3 profile ranges from 4%
to 64% across formulations. These are observed profile-level differences, not
causal attribution to any individual endpoint wording. Low equivalence power at
N=50 near .5 and S1 ceiling effects remain explicit limitations. Semantic human
approval does not ensure the model's behavioural invariance.

All authorised empirical battery collection is complete: 39,000 unique fresh
behavioural responses, 38,993 valid, plus the independent audit and generation
records. Full pass is ruled out. The existing ten-parameter system-prompt
implementation is not cleared for Phase 2; the final research decision between
diagnostic follow-up and a revised architecture remains for consultation.
No automatic partial-pass descope, new theoretical departure, or model switch.

The five synthetic perspectives and resolution are recorded in
experiments/phase1_5_encoding_validity/phase_review_20260909/BATTERY_ASSESSMENT.md:
conceptual coherence is not operational validity; task saturation and audit
prevalence limit inference; failed equivalence is not automatically proven
difference; representation dependence needs investigation; all provenance is
preserved. The current gate is not met, while the underlying theory is not
declared false. All backups remain on this computer; nothing is pushed remotely.

## 2026-09-09 — Human paraphrase approval and behavioural run

With HUMAN_REVIEW.md open, the user approved all three variants and requested
another assistant assessment. Reviewer recorded as Tommy (project owner), based
on this conversation and established project identity. The verbatim approval and
all three exact hashes are preserved in a separate paraphrases_approved.json;
the original unapproved bundle and raw generation records remain unchanged.

Final assistant assessment agrees these are suitable for testing: endpoint
directions, secondary procedure value, genuine endorsement, broad moral scope
and the accepted canonical scaffold are preserved. Stylistic differences may
still change emphasis; semantic approval is not proof of behavioural equivalence.
No revisions were made after approval. The earlier synthetic review applies.

Launched paraphrases_20260909_final: neutral configuration, seed 20260604,
ten parameters at .8 with remaining parameters at their fixed means, three
problems, three approved paraphrases, 50 calls per cell, 4,500 total. Model
gpt-5.4-mini-2026-03-17, temperature 1, cap 600, concurrency five. The canonical
baseline is 1,500 valid hybrid observations from the completed rotations run.
Source/design hashes and baseline compatibility passed before dispatch.

Hidden supervisor PID 20056 updates output/validity_paraphrases_20260909/status.json,
then verifies expected record keys, uses unchanged all-pair TOST scoring, creates
a local backup, and updates the combined evidence matrix. Fixed N and fail-stop
rules remain unchanged; Phase 1.5 still needs final scientific review.

## 2026-09-09 — Thesis disclosure approved; final paraphrases prepared

After the explicit disclosure question and explanation of Anthropic API data
terms, the user replied "approval given". Retried the previously rejected exact
request through approval review; execution was allowed. This resolves the prior
disclosure block. It does not supply prospective human approval of new wording.

Four preserved Haiku calls (theory_r2–r5) generated and refined the endpoints.
The first two rounds still changed conceptual meanings; targeted semantic
feedback corrected those defects without supplying replacement text or any
behavioural outcomes. The r4 guard stopped on three unrequested edits, all
subsequently inspected and disclosed. Two remaining CS defects were corrected
in r5. Its response used corrected_variants rather than variants; offline
extraction verified that only the two requested endpoints changed and preserved
all generated text. No frozen generator or scientific source was edited.

All three final templates pass structure and per-parameter lexical targets.
Assistant semantic review recommends them for human review against the thesis
and accepted implementation. See docs/phase1_5_paraphrase_final_review_20260909.md
for the parameter-by-parameter and synthetic five-perspective assessment.
The final exact templates and hashes are in theory_r5/HUMAN_REVIEW.md.
All human approval fields remain false and no paraphrase behavioural calls
have started. No theoretical departure, model swap, or phase pass is claimed.

## 2026-09-09 — Gradient extension completed and reviewed

Completed the authorised 15,000-call extension, neutral configuration, N=50 per
cell, seed 20260604, exact gpt-5.4-mini-2026-03-17 snapshot and unchanged frozen
settings. There are 14,998 valid parses, two preserved parsing failures, zero
API failures, and no missing or duplicate records. All cells meet the 98% parse
floor. Scoring, record checksums and the integrity-tested local ZIP completed.
Recorded token cost is approximately $14.54 at the previously checked rates.
The backup is on this computer only. The evidence matrix now includes gradients.

Decision: retain the measured mixed result and keep the Phase 1.5 gate open.
Two of six eligible comparisons meet the existing slope-retention rule:
verbal MoR/S3 (ratio .562) and numeric PD/S1 (.851). Numeric MoR/S3 (.454),
numeric MS/S2 (.262), and verbal MS/S2 (.290) retain the predicted direction
but fall below .50. Verbal PD/S1 is pinned at 250/250 A decisions. No eligible
pair meets the criterion in both representations; 54 other comparisons remain
not assessable because their source sweep did not qualify.

Synthetic review: Linden rejects treating partial sensitivity as validation of
all conceptual distinctions. Osei flags S1 saturation: numeric PD/S1 has only
three B choices in 250 observations. Tanaka retains the point-estimate rule
while reporting PD's wide Wald interval and its different likelihood-ratio
diagnostic; a ratio below .50 does not prove no effect. Renna sees representation
dependence as a measured limitation that must accompany downstream claims.
Okafor confirms completed operational collection and local provenance, while
requiring the outstanding paraphrases and scientific review before closure.
Resolution: report every eligible result and non-assessable comparison without
retuning the design. No new theory departure or Phase 2 authorisation is inferred.
The separate private-thesis disclosure to Anthropic remains unapproved.

## 2026-09-09 — Gradient extension authorised

The user explicitly instructed running the gradient extension. The prepared
`gradients_20260909_final` design is authorised for its full 15,000 calls:
ten parameters, five values, three problems, N=50, numeric-only and verbal-only;
neutral configuration, seed 20260604, exact gpt-5.4-mini-2026-03-17 snapshot,
temperature 1, 600-token cap, concurrency five. Frozen code hashes match, and
the run has no existing records at launch. The completed hybrid source is reused
only as its exact-protocol baseline. This approval does not authorise sending
the separate thesis-containing paraphrase request to Anthropic. An operational
checkpoint precedes sustained dispatch; failures remain preserved.

The checkpoint returned ten valid responses with the exact snapshot and no API
failures. Launched a hidden background job, PID 23588, for the remaining 14,990
calls. The separate operational wrapper leaves frozen scientific files unchanged,
uses an OS-held lock against duplicate jobs, updates status every 20 seconds,
and will score, verify, archive and refresh the phase evidence matrix on completion.
Status/logs are under `output/validity_gradients_20260909`. No gradient outcome
or phase pass is claimed at launch. The paraphrase disclosure remains unapproved.

## 2026-09-09 — Remaining phase work prepared

The user asked to finish Phase 1.5 strongly. Prepared the existing five-value
numeric/verbal gradient design in `gradients_20260909_final` (15,000 calls;
same source snapshot, profiles, settings, seed and existing analysis). No calls
were made because this extension had been explicitly excluded from the earlier
restart. Requested the concrete budget/execution decision and, separately,
explicit approval for sending the already-prepared private theory excerpt to
Anthropic after its automatic approval-review rejection. Replies are pending.

Created a versioned parameter-by-test evidence matrix from the completed source
and audit reports, retaining confidence intervals, majority baselines and active
diagnostics. It records remaining tests as pending and is not a scientific closure
verdict. No completed observation, criterion or theory commitment was changed.

## 2026-09-09 — Project-health assessment requested by user

Provisional assessment, not a phase-gate verdict or permission to redesign:
execution and provenance now support a serious validation study, while the full
ten-parameter interpretability/reliability claim remains unsupported. In the
full-harness sweep, MoR/S3, PD/S1 and MS/S2 meet the complete prespecified cell
criterion; in the bare delivery only MS/S2 does. Other statistically detectable
effects must not be confused with complete criterion success, nor strict
monotonicity failures with proof of no effect. LL/CS/AW lack prespecified signs.
S1 saturation leaves little room to distinguish most profiles. Representation
comparisons show substantial differences on S2/S3; the one-value rotations do
not establish within-parameter gradients. The audit's literal threshold pass
does not overcome its majority-baseline and active-stratum limitations.

Synthetic review: Linden requires distinct, interpretable conceptual effects;
Osei recognises real parameter sensitivity but flags saturation and harness
dependence; Tanaka distinguishes inconclusive small active strata from proof of
no recoverability; Renna treats model/coder/measurement limitations as competing
explanations; Okafor finds the operational records useful but notes that local
ZIP files are not independent backups. Resolution: continue evaluating the
frozen design, finish the reviewed paraphrase test, discuss the outstanding
gradient criterion before additional collection, and withhold Phase 2 readiness.
No parameter, prompt, benchmark, scope, or accepted historical amendment changes.
Any new departure requires the user's stipulated constraint evidence and prior
consultation. An informative mixed or negative thesis result remains possible;
no publication outcome or successful full architecture is promised.

## 2026-09-09 — Completed independent audit and interpretation

The effective r3 audit has 200 valid records and 2,000 estimates (two legitimate
abstentions retained as incorrect for accuracy). All 173 reused r2 records were
byte-preserved; r3 collected 27 new responses with the identical frozen design.
The malformed r2 response is preserved separately inside the final local backup.
Together with the older strict-format attempt there were 202 unique paid audit
attempts, approximately $0.435918 at Haiku's $1/$5 token rates.

Model: claude-haiku-4-5-20251001; neutral context; sampling seed 20260604. Literal
thresholds are met: seven parameters exceed .35 with binomial p<.05 against .25;
six reach .50. However, all aggregate accuracies fall below their 92–94% empirical
majority baselines. None of the ten active-parameter permutation tests reaches
p<.05 (1,999 resamples, unadjusted). Active strata contain only 20 observations
per trait. No claim of established recoverability or overall phase pass follows.
The complete table reports Wilson confidence intervals and both accuracy views.

Synthetic review: Linden separates literal thresholds from the conceptual claim;
Osei notes the missing evidence of manipulated-trait recovery; Tanaka emphasises
class imbalance and low active-stratum precision; Renna rejects treating audit
completion as phase closure; Okafor confirms traceable records and backups.
Resolution: audit collection/scoring complete, scientific result mixed and not
sufficient to establish validity; remaining battery decisions stay open.

The prompt requested at most 15 commentary words; observed median 21, maximum
66, with 186/200 above the requested limit. This limitation is disclosed and did
not cause response selection. The report and all 200 records have a checksum
inventory and verified local ZIP backup. Two new offline audit-format/resume
tests passed; frozen source sweep and original audit modules remain unchanged.

## 2026-09-09 — Brief-audit malformed-response continuation

Brief audit r2 stopped at item 174: the response supplied null for both ID quartile
and confidence, although the frozen schema requires numeric confidence even for
abstention. The preceding 173 records parsed successfully. No scoring results
were inspected to select reuse. A linked r3 designation copies all 173 valid
records byte-for-byte and retains r2's malformed attempt in place, with its hash
and reason recorded in a continuation ledger. The remaining schedule contains
27 calls: a new attempt for that malformed item and 26 undispatched items.
The prompt, model, blind pack, confidence schema, token cap and scoring remain
identical. This is operational recovery within the authorised 200-item audit,
not a theoretical departure or a relaxed parser. Both failed attempt and final
effective observation counts must be disclosed in the completed report.

## 2026-09-09 — User-approved concise audit format

The user explicitly authorised completing the Claude audit with extra commentary
allowed, while instructing Claude to use as few words as possible without losing
explanatory ability. A separate CLI now requests compact estimates JSON followed
by at most one 15-word explanatory sentence. It accepts trailing prose and stores
it unchanged, recording word count separately; verbosity never selects outcomes.
Invalid quartiles/confidence, duplicate JSON keys and multiple structured answers
are still rejected. The original frozen audit/scoring modules remain unchanged.

New designation: `claude_audit_20260909_brief_r2`. The same 200-item blind pack,
Claude snapshot, temperature, token cap and analysis are retained. All 200 items
receive the revised prompt; the one earlier failed-format response remains in
its original designation and is not pooled. No private answer key is sent.
Two offline tests passed, covering commentary handling, ambiguity/schema rejection,
blinding, checkpoint resumption and exactly-once item collection.

Synthetic review: Linden retains evidence-based interpretation and abstention;
Osei requires identical item selection across the revision; Tanaka separates
format compliance from statistical inclusion; Renna discloses the prompt revision;
Okafor preserves original failures and tests resume behaviour. Resolution: apply
the user's approved operational format change in a new designation and score the
complete new audit without changing the scientific thresholds.

## 2026-09-09 — Background collection completed; audit format stop

On the user's return, verified committed-format checksum inventories and local
backup manifests: source 15,000 records, all valid; rotations 4,500 records,
4,498 valid parses and two parse failures; no API failures in either run.
Both same-computer ZIP archives exist. Recorded token usage gives $13.380867 for
the source and $4.5390015 for rotations at standard rates, $17.9198685 combined.
The supervisor exited at 13:50:09 UTC after rotations finished because the
independent audit's first response failed strict parsing. Haiku returned its
ten estimates in a fenced JSON object followed by prose, triggering Extra data.
This was a format failure, not a credential or quota error. The one audit record
is preserved and 199 items remain undispatched. No parser/prompt/model change or
new audit designation has been made; consultation is required under the user's
new-departure rule. Phase 1.5 remains open, with paraphrases also pending.

## 2026-09-09 — Constraints and consultation clarified

The user clarified that earlier departures from the original theory were made
for necessary binding constraints and remain accepted. The theory should still
guide review, read together with documented operational amendments. A new
departure requires a concrete physical or technical limitation and consultation
with the user before implementation; theoretical fidelity is not relaxed for
convenience. Record the evidence, minimal proposed workaround and consequences.
This rule is now in both project constitutions. It does not reverse historical
phase closures or authorise changing the running frozen sweep. The first Claude
candidates' semantic drift has no demonstrated physical necessity. No new
departure is approved by this clarification, and disclosure approval for the
prepared theory-containing Anthropic request remains pending.

## 2026-09-09 — User-authorised fresh Phase 1.5 restart

After reviewing recovery dependencies and API cost estimates, the user explicitly
requested a complete restart and delegated selection of a Claude model similar
to GPT-5.4 mini. The new source designation is `option_c_20260909_restart`;
all 15,000 slots will be newly collected, with no reuse or pooling of the earlier
sample. Historical evidence and the unused shard preparation remain provenance.
This supersedes the continuation plan as the active execution path.

Claude Haiku 4.5 (`claude-haiku-4-5-20251001`) is selected for independent
paraphrase generation and blind audit. Official provider documentation positions
it as the lightweight high-throughput model, with $1/$5 per million input/output
tokens, close to GPT-5.4 mini's $0.75/$4.50 tier. This is an approximate capability
tier match, not demonstrated equal research-task performance. No behavioural
model substitution is made. Sources: https://platform.claude.com/docs/en/models/overview
and https://developers.openai.com/api/docs/models/gpt-5.4-mini.

Synthetic review: Linden rejects claiming model equivalence from pricing; Osei
requires a fresh designation with unchanged prompts and allocation; Tanaka keeps
all new outcomes and discloses the restart, without pooling historical data;
Renna retains the independent-coder limitation and human semantic-review gate;
Okafor requires an operational checkpoint before sustained dispatch. Resolution:
fresh fixed-N sweep, pinned Claude snapshot, then the 200-item audit and 9,000
robustness calls; no optional 15,000-call gradient extension automatically added.
Both model IDs were accessible. The ten-call OpenAI checkpoint passed all parsing
and model checks (8,959 input and 499 output tokens); the fresh sweep then started.
Claude returned three candidates but violated literal labels. Mechanical label
restoration produced structurally valid candidates; the user's requested theory
comparison then found semantic drift and rejected all three for behavioural use.
See [semantic review](docs/phase1_5_paraphrase_review_20260909.md). A new generation
will vary endpoint descriptions only, holding all other template text literal,
before any paraphrase behavioural calls. Human sign-off remains pending.

The background follow-up supervisor (PID 5336 at launch) queues rotations and
blind coding after complete source verification, then checks recorded human
paraphrase approvals before further dispatch. It creates checksum inventories
and same-computer ZIP backups. Three restart-tool tests passed in addition to
the 19 baseline and four continuation tests. At a subsequent checkpoint all
1,795 newly collected responses were valid, with approximately $1.60 token cost.

Automatic approval review rejected the new theory-grounded generation request
because sending private thesis text and derived feedback to Anthropic required
explicit disclosure approval. The request is frozen locally and was not sent;
the user has been asked for that specific permission. Other authorised work
continues. See [restart operations](docs/phase1_5_restart_20260909.md).

## 2026-09-09 — Cross-computer continuation preparation

The user requested completion of Phase 1.5, confirmed original responses remain
on another computer, and authorised collecting remaining slots here for a later
merge. Neither provider key is configured yet. A separate tested wrapper now
supports full-source recovery and inventory-only sharding, without modifying the
frozen scientific runner. The prepared September 9 shard schedules 6,360 new
slots; the unidentified original failed slot awaits payload recovery.

Synthetic review: Linden requires honest separation of absent and observed data;
Osei supports the fixed allocation without outcome selection; Tanaka requires
disjoint keys and verified pooling; Renna flags the collection gap and dependent
audit prerequisites; Okafor requires fail-stop execution and local backup.
Resolution: preserve the full target and snapshot, reserve every inventoried key,
collect only never-dispatched slots, and withhold pooled claims until recovery.
All 19 existing tests and four new continuation tests passed. No paid calls or
merge occurred. See [continuation instructions](docs/phase1_5_continuation.md).

## 2026-09-07 — Sample recovery handoff

The user asked whether topping up credits permits retaining the interrupted
sample, requested a Markdown handoff, and authorised pushing all changes including
the abstract. The handoff distinguishes 8,639 reusable valid responses from the
one failed attempt: completing the fixed design needs 6,361 further successful
responses, not a fresh 15,000-call experiment. This is a proposed continuation,
not an implemented or executed resume command.

Synthetic review: Linden and Osei favour preserving the fixed design and avoiding
outcome-selected reuse; Tanaka requires one effective response per planned slot
with all failed attempts disclosed; Renna flags collection-time comparability;
Okafor requires a separately tested continuation ledger and unchanged originals.
Resolution: document a new linked designation, reuse every valid original record,
fill only unfilled slots, and retain the failure in the source archive. No paid
calls or frozen-code edits were made. See
[HANDOFF_2026-09-07.md](docs/HANDOFF_2026-09-07.md).

## 2026-09-06 — Documentation consolidation and provisional abstract

**User request:** clean up Markdown, update/remove redundant documents, create
AGENTS.md using the CLAUDE.md formula, push the project, and write a rigorous
provisional abstract including unfinished work.

**Decision:** README is the project introduction; NEXT_STEPS is the current
operational ledger; docs/README is the document map. AGENTS.md and CLAUDE.md share
the same constitution body, updated from the existing formula. Scientific
commitments and approval rules remain explicit. The five review roles are
labelled synthetic perspectives, not external reviewers or automatic delegation.
The user's communication preferences are included.

**Concise synthetic review:** Linden: distinguish proposed normative architecture
from demonstrated understanding. Osei: separate pilot functionality from validity.
Tanaka: keep incomplete samples incomplete and do not claim future statistical
results. Renna: distinguish PARIA from the wider Hexagon programme. Okafor:
consolidate navigation while preserving frozen evidence. Resolution: a separate
provisional abstract, current status reconciliation, and unchanged source papers,
prompts, experiment records, and frozen runner code.

Moved the wider-programme OVERVIEW to docs/research_programme.md, retaining its
scope while correcting PARIA overclaims. Archived the old meta log and June
novelty assessment. Removed redundant active copies and stale task lists; Git
history retains the previous README/CLAUDE/NEXT_STEPS versions. The main-study
plan remains a draft; its proposed Python mixed-model cross-check is explicitly
unresolved rather than presented as an implemented binomial estimator.

The user explicitly authorised pushing all project changes to the existing
GitHub remote. This supersedes the earlier lack of publication authorisation.
Raw per-call artifacts and credentials remain excluded from the push.

**Verification:** active Markdown links resolve; AGENTS.md and CLAUDE.md match
apart from their titles; archived documents match their pre-cleanup bytes.
No code, test, source paper, locked prompt, or historical phase evidence changed.
All 8,640 interrupted-run records passed their integrity checks: 8,639 valid,
one API failure, and exact returned model identity on successful calls. Both
September designations now have checksum inventories for publication; raw
payloads remain local.

## 2026-09-06 — Source sweep interrupted by API credit exhaustion

Observed process exit after 8,640/15,000 records in option_c_20260906_r2.
One terminal HTTP 429 reported insufficient_quota / credit_balance_exhausted;
the runner stopped after its current batch and emitted the partial report.
There was no outcome-based stopping decision. The failed record remains stored;
the 6,360 undispatched observations remain missing. No resumption or new paid
run was initiated during documentation cleanup. Funding and an explicit
continuation/restart protocol are required before further source collection.

## Retained methodological decisions

- [Phase 0 closure](experiments/PHASE0_CLOSURE_2026-07-29.md): locked recalibrated
  dilemmas, naked holdout, measured baselines, and headroom tiers.
- [Phase 1 result](experiments/phase1_pilot/PHASE1_PILOT_RESULT_2026-07-29.md):
  S3 plus S2 operational pilot; validity still requires Phase 1.5.
- [Option-C protocol](docs/phase1_5_execution.md): exact snapshot, fixed N,
  joint role/format contrast, immutable records, fail-stop execution.
- [Follow-up protocol](docs/phase1_5_followup.md): independent Claude route;
  200-item blind audit with prevalence-aware diagnostics; six verbal bins;
  human-reviewed paraphrases and all-pair equivalence; optional gradient extension.
- [Historical log](docs/archive/meta_through_2026-09-06.md): original discussions,
  implementation verification, credential-only restart, and earlier decisions.

## Recording future decisions

Add dated entries with the user's objective, concrete decision, evidence,
limitations/deviations, and affected artifacts. Record synthetic review only
where substantive judgment warrants it. Never rewrite historical evidence to
make an experiment appear complete or a planned validation appear passed.
