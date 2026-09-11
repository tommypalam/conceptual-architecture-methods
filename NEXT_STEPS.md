# Current state and next steps

Updated 2026-09-11. Working branch: `phase1-5-validity`.
This file is the current operational status; historical records are evidence,
not competing task lists.

The user authorised a fresh Phase 1.5 restart on September 9. The active source
is `option_c_20260909_restart`: 15,000 new calls, without reusing the old sample.
See [live restart instructions](docs/phase1_5_restart_20260909.md).

### Active execution

**Latest completion - paid screen within $9:** the researcher explicitly renewed
OpenAI spending for bounded exploration, with a $9 total new ceiling. The
[450-call evidence screen](experiments/phase1_5_encoding_validity/evidence_screen_20260911/PROTOCOL.md)
allocates at most $3 (full conservative schedule reservation $2.867265).
Same pinned GPT model; original/repetition/grounding arms with four unchanged
profile formulations and matched no-profile controls, 30 calls per cell.
Eleven offline tests pass, including cost guards, crash reservations, source
preservation and failure handling. **450/450 valid, collection complete:** after the initial
automatic-review rejection, the researcher explicitly replied "Approve 450
calls, $3 cap". That exact approval is saved against the frozen design, and
dispatch completed with zero API/model/usage errors and one attempt per call.
Estimated full-rate token cost **$0.5022225**; approximately **$8.50 remains of
the new allowance**, not a verified account balance. All request/profile/source
hashes, 450 unique API IDs, reservations and raw backup bytes are verified.
No automatic expansion is scheduled.
This authority supersedes the older spending stop below for this work only;
it does not authorise a full sweep or closing the gate on a small screen.

The observed P2/P3 gap changed from +.633 original to -.033 repetition alone
and .000 grounding. The primary grounding interval [-.274, +.274] is too wide
for equivalence: **NO_GROSS_FAILURE_DETECTED_NOT_VALIDATED**. Repetition also
narrows the gap, and grounding favours WAIT (canonical/P1/P2/P3 ADOPT counts
0/5/3/3 out of 30; no-profile 1/30). No distinct grounding benefit or preserved
parameter sensitivity is established. See the
[verified report](experiments/phase1_5_encoding_validity/evidence_screen_20260911/analysis/SCREEN_REPORT.md)
and [interpretation and next check](experiments/phase1_5_encoding_validity/evidence_screen_20260911/analysis/INTERPRETATION.md).
Next: prepare a small sensitivity/headroom check before considering any full
sweep, keeping repetition as a control and the original hypotheses intact.

**Current direction - offline grounding candidate:** the researcher selected
careful preparation of a fact-only evidence reference, with an optional tool
scaffold kept outside the experiment. The experimental model remains
`gpt-5.4-mini-2026-03-17`; Claude is a research helper, not its replacement.
The [S3 exact candidate review](experiments/phase1_5_encoding_validity/evidence_candidate_20260911/HUMAN_REVIEW.md)
preserves all six source paragraphs verbatim, with a separately identified new
grounding instruction. The original candidate manifest records its draft status
at preparation; the separately designated screen above now has exact dispatch
approval. Original prompts, theory, prior raw records and existing runners are unchanged.
The [optional read-only evidence interface](experiments/phase1_5_encoding_validity/evidence_candidate_20260911/PROTOCOL.md)
passes four offline tests, including shared provider substitution contracts.
It is not registered with an LLM or integrated into the validity battery.
Preparation made no paid calls. Phase 1.5 remains open; Phase 2 remains on hold.
The researcher subsequently authorised exploration within the Phase 0a/0b/0c
closure. All six Phase 0c source hashes were verified intact. The candidate
protocol now explicitly requires separating added-context effects from profile
effects and fresh validation from development screens. Existing naked-prompt
baselines cannot automatically validate an evidence overlay or tool delivery.

**Earlier spending constraint (superseded by the $9 authority above):** the researcher reports $12 left
in the OpenAI account and instructs us not to spend any more of it on Phase 1.5.
No further OpenAI calls are authorised for this phase. The researcher has since
explicitly authorised using remaining Claude API usage, with original prompts
unchanged. This is new provider-specific authority, not a workaround for the
OpenAI spending stop. The earlier $50 allowance does not authorise new OpenAI
spending. The researcher explicitly approved the exact 80-call Claude screen
and $0.75 cap. This is its entire current paid scope; no automatic expansion.

**Latest completed diagnostic:** `claude_screen_20260911` collected all 80 valid
responses with the exact four approved baseline formulations at PD=.8/S3,
20 per formulation. No original prompt was changed. Canonical/P1/P2/P3 ADOPT
counts are 13/14/19/6 out of 20: 65% / 70% / 95% / 30%. The prespecified P2-minus-P3
gap is 65 points, with conservative exact >=95% interval [14.7, 89.7] points.
Its lower bound exceeds the .10 margin: **gross wording failure detected**.
The tested Haiku/provider switch does not repair this known local problem.
This is an early screen, not a full sweep or phase-pass test.

Recorded cost **$0.156395**, within the explicitly approved $0.75 cap; zero
OpenAI calls, zero API/model failures, one attempt per call. All requests,
profiles, IDs, frozen sources and raw ZIP payloads are verified. No collection
remains running and no further paid study is automatically authorised. See the
[screen report](experiments/phase1_5_encoding_validity/claude_screen_20260911/analysis/SCREEN_REPORT.md),
[fixed protocol](experiments/phase1_5_encoding_validity/claude_screen_20260911/PROTOCOL.md)
and [illustrative reasoning notes](experiments/phase1_5_encoding_validity/claude_screen_20260911/analysis/QUALITATIVE_NOTES.md).
The notes identify a tentative mechanism: answers supply different implicit
procedural details for ADOPT versus WAIT. This is an unblinded 12-response
inspection, not a causal finding or validated coding instrument. The next
offline review should distinguish stated facts from added assumptions and
their links to PD; original prompts and theory remain unchanged.

An [offline worked example](experiments/phase1_5_encoding_validity/claude_screen_20260911/offline/RETROSPECTIVE_SCREEN.md)
used only the first 20 stored call indices per original OpenAI formulation.
Its P2/P3 gap is .60, with conservative interval [.078, .889]: too wide to
establish a gap beyond .10 under this screen's rule. This single retrospective
subset is not a power estimate or evidence about Claude; no subsets were searched.

New approaches must be screened before any full sweep: inspect known failure
cases, check exact theoretical mappings and use local mocks for implementation
correctness. If empirical testing is later explicitly funded, propose a small,
fixed, targeted screening study with a stopping rule before dispatch. Screening
can reject weak candidates; a promising small sample or an offline check does
not establish equivalence or close the validity gate. A full battery requires
its own justified validation plan and renewed spending authorisation.

**Latest completion - numeric-axis pilot:** all 7,900 planned slots are recorded
in `axis_instruction_20260911_assembled`: 7,890 valid responses, ten preserved
API failures, no parsing failures and no returned-model mismatches. No paid
collection remains running. Neutral context, model `gpt-5.4-mini-2026-03-17`,
seed 20260913, temperature 1, output cap 600. Exact requests, profiles, unique
requested seeds/API IDs, source bytes and all ZIP record payloads are verified.

The approved shared instruction **did not meet the local screen**. Revised
canonical/P1/P2/P3 ADOPT rates at PD=.8/S3 are 15.1% / 33.0% / 68.9% / 10.8%.
Only canonical/P3 establishes equivalence: one of six pairs in each arm, where
all six are required. Unknown-decision sensitivity does not establish all-pair
equivalence. Neither arm has the all-formulation saturation flag. Revised PD/S1
has a positive fitted slope (p=.00749, extreme h=.495), but its observed
94%/92%/98%/100%/100% sequence fails the prespecified monotonicity check. The
baseline is ceiling-limited with separation. S2/S3 remain descriptive because
they have no prespecified PD directional hypothesis. The retained API-failure
flag is not the sole reason the local screen is unmet.

See the [interpretation and next dependency](experiments/phase1_5_encoding_validity/axis_instruction_20260911_assembled/analysis/INTERPRETATION.md),
[full report and figures](experiments/phase1_5_encoding_validity/axis_instruction_20260911_assembled/analysis/AXIS_PILOT_REPORT_v2.md),
and [recovery ledger](experiments/phase1_5_encoding_validity/axis_instruction_20260911_assembled/analysis/RECOVERY_LEDGER.md).
The original approved design is `axis_instruction_20260910`; four linked
continuations collected only unsent slots. All failures and the overnight gap
remain documented. No old-study responses were pooled or failures replaced.

Recorded pilot token estimate: **$8.8045695**, under the shared $12 dispatch
guard. The earlier **$39.881084** figure was arithmetic against the proposed
additional $50 allowance, not a checked provider-account balance. It is not
current spending authority; the researcher's reported $12 balance and no-spend
instruction above govern further work.
Checksums and verified same-computer ZIPs are saved; off-device backup is not
claimed. The final report's chart-roundoff formatting repair changed no numerical
analysis. Collection is complete; the original Phase 1.5 gate remains unmet and
Phase 2 remains on hold. The candidate is not promoted to a full revised battery.
The completed evidence packet supports the spec 4.5 research/supervisor review
before choosing further lexical re-engineering. Theory and scope are unchanged.

**Latest completion - PD endpoints:** all 1,200 responses are valid, 300 per
condition, with zero terminal API/model failures. Fixed PD=.8/S3, P2 background,
neutral context, collection seed 20260912. ADOPT rates A/B/C/D: 88.7% / 50.3% /
39.7% / 5.0%. Low-end wording effect +36.5 points (simultaneous interval +24.6
to +47.2); high-end +47.2 (+35.1 to +57.7); interaction +3.7 (-18.9 to +26.2).
Both endpoints matter; interaction remains unresolved. Exact messages, hashes,
analysis counts and byte equality of all 1,200 archived records are verified.
See the [endpoint report](experiments/phase1_5_encoding_validity/pd_endpoints_20260910/analysis/ENDPOINT_REPORT.md).
Estimated token cost $1.3143465; approximately $48.69 remained from the additional
$50 immediately after this diagnostic, before the axis pilot and provider-only charges. Collection is complete; status is
under `output/pd_endpoints_20260910`. Phase 1.5 remains open. Later simple problems
use LPMs and complex problems an Agents of Chaos-style build.

**September 10 diagnostic complete:** all 1,200 PD/S3 factorial responses are
valid (300 per condition), with zero API/model errors, seed 20260910. The user
approved exact B/C combinations; A/D retain prior approval. ADOPT rates A/B/C/D
are 85.0% / 15.0% / 53.7% / 8.3%. The PD wording effect is +57.7 points
(simultaneous interval +45.7 to +67.8); other-nine wording +19.0 (+7.7 to +29.7);
interaction +24.7 (+2.2 to +46.4). All three exclude zero under the frozen
analysis. This localises a large presentation sensitivity to PD wording, with
additional background and interaction effects. Theory and the gate are unchanged.
See the [result report](experiments/phase1_5_encoding_validity/wording_factorial_20260910/analysis/FACTORIAL_REPORT.md).
Recorded token cost estimate: $1.3013235 before taxes. Exact messages/profiles,
all record hashes and the byte equality of all 1,200 ZIP payloads are verified.
Status/logs: `output/wording_factorial_20260910`. No collection is still running.

**Latest verified status (after background completion):** the source sweep has
15,000/15,000 valid records, zero API failures. Rotations have 4,500/4,500 records,
4,498 valid parses and two parse failures, zero API failures. Both completed runs
have checksum inventories and local ZIP backups in `output/validity_backups`.
Source-plus-rotations OpenAI token cost is approximately $17.92 before taxes. The independent
Claude audit is now complete in `claude_audit_20260909_brief_r3`: 200 valid coding
records, 2,000 estimates including two abstentions. The user approved optional
concise commentary. The revised prompt requests at most 15 explanatory words;
observed median 21, maximum 66; verbosity did not filter outcomes. All records,
failed attempts and the continuation ledger are preserved and locally backed up.
The audit meets literal numerical thresholds (7 above the 35% criterion, 6 at
least 50%), but no active-parameter permutation diagnostic has p<.05 and every
aggregate accuracy is below its empirical majority baseline. No phase pass is
claimed. See [audit report](experiments/phase1_5_encoding_validity/claude_audit_20260909_brief_r3/analysis/AUDIT_REPORT.md).
Audit token cost across 202 unique attempts: approximately $0.436. The authorised
gradient extension is complete in `gradients_20260909_final`: 15,000 records,
14,998 valid parses, two preserved parsing failures and zero API failures.
Checksums, a verified local ZIP and the updated evidence matrix are saved.
Estimated gradient token cost: $14.54. Two of six eligible comparisons meet
the existing retention criterion (verbal MoR/S3 and numeric PD/S1); no eligible
pair meets it in both representations. PD/S1 remains severely ceiling-limited.
The other 54 comparisons are not assessable under the prespecified source gate.
See the [gradient report](experiments/phase1_5_encoding_validity/gradients_20260909_final/analysis/GRADIENT_REPORT.md).
Terminal job status: `output/validity_gradients_20260909/status.json`.
Earlier audit failures were
preserved separately; the completed audit uses the unchanged 200-item blind pack.
Corrected paraphrases in `claude_paraphrases_20260909_theory_r5` are now
human-approved by Tommy (project owner), with unchanged exact template hashes.
The 4,500-call equivalence experiment is complete in `paraphrases_20260909_final`:
4,497 valid parses, three preserved parsing failures, zero API failures, estimated
token cost $5.06. Only 8/30 cells establish all-pair equivalence (24 required);
one cell also misses the parse floor. Checksums and the local ZIP are verified.
All authorised empirical battery collection is complete. The current architecture
does not meet the gate; Phase 2 remains on hold. See the
[battery assessment](experiments/phase1_5_encoding_validity/phase_review_20260909/BATTERY_ASSESSMENT.md).
Terminal status: `output/validity_paraphrases_20260909/status.json`.
Earlier progress counts below are historical checkpoints.

**Historical launch notes:** the user instructed rerunning Phase 1.5 from scratch. The source
designation is now `option_c_20260909_restart`, targeting 15,000 fresh calls under
the unchanged scientific design. Claude Haiku 4.5, pinned to
`claude-haiku-4-5-20251001`, is selected for paraphrases and the independent audit.
Both model IDs were accessible. The ten-call checkpoint passed. At the latest
integrity check, 1,795 new records were valid with no API failures, using about
$1.60 in OpenAI tokens. The sweep continues; this count is a dated checkpoint,
not a live total. `output/validity_restart_20260909/status.json` is updated by the
background supervisor (PID 5336 at launch), which waits for source completion
before running 4,500 rotations and the 200-item Claude audit.
The prepared shard below is inactive and will not be used for this restart.

Earlier, the user confirmed that the original raw records are on another computer and
authorised collecting the remainder here for a later merge. The prepared
`option_c_20260909_shard` reserves all 8,640 inventoried keys and schedules only
the 6,360 never-dispatched slots. It has made no API calls. The failed original slot cannot be
identified from the inventory alone and awaits recovery of its original record.
That recovery path requires the original payloads; the fresh restart does not.
See [cross-computer continuation](docs/phase1_5_continuation.md).

## Phase ledger

| Phase | Verified status | Evidence / next dependency |
|---|---|---|
| 0a–0c | Closed, with documented baseline and delivery deviations | [Phase 0 closure](experiments/PHASE0_CLOSURE_2026-07-29.md) |
| 1 | Operational pilot passed, S3 + S2, 100 calls | [Pilot result](experiments/phase1_pilot/PHASE1_PILOT_RESULT_2026-07-29.md) |
| 1.5 | Empirical battery complete; current gate not met; next research decision pending | [Battery assessment](experiments/phase1_5_encoding_validity/phase_review_20260909/BATTERY_ASSESSMENT.md) |
| 2 | Pending; encoding-validity gate and preregistration required | Paired-agent individual and collective experiments |
| 3 | Pending | Five behavioural benchmark families and contamination diagnostics |
| 4 | Pending | Reviewed moral-coding manual and human validation |
| 5 | Pending | Main inference, dependency/distribution sensitivity, model robustness |
| 6 | Pending | Final reporting, compliance record, open-artifact release |

## Interrupted Option-C experiment

- Run: `experiments/phase1_5_encoding_validity/option_c_20260906_r2`.
- Exact model: `gpt-5.4-mini-2026-03-17`; temperature 1; output cap 600;
  seed 20260604; concurrency 5.
- Target: ten parameters × five values × three simple problems × N=50 ×
  two deliveries = **15,000 calls**.
- Preserved total: **8,640 records**, including one terminal API failure;
  **6,360 planned observations were not dispatched**.
- Stop reason: HTTP 429, `insufficient_quota` / `credit_balance_exhausted`.
  The process exited; it is not running in the background.
- Final partial report: [8,640-record summary](experiments/phase1_5_encoding_validity/option_c_20260906_r2/analysis/summary_562653cd58340299.md).
  Its partial estimates are not a completed sweep verdict.
- Earlier designation `option_c_20260906` contains five invalid-credential
  failures and no model output. Both designations retain the same design hash.

The two arms jointly vary message role and requested output format. The
alternative retains scaffold text; it is not an established neutral treatment.
The stored failures must not be deleted or replaced to make the run resumable.

## Next actions

**Researcher clarification, September 10 (budget superseded September 11):** the objective remains implementing
and testing the theory's ethical-concept encoding, not replacing that objective
with a stand-alone wording study to meet the deadline. The researcher authorised
up to $50 additional API expenditure and wants a submission-ready thesis in ten
days. These constraints do not authorise lowering the validity gate, removing
concepts/parameters, invoking the descope path, or departing from theoretical
meaning. Existing accepted binding-constraint amendments remain in force.

The researcher subsequently clarified the sequence: finish Phase 1.5 using the
previously proposed endpoint diagnosis and reviewed encoding work before moving
to the LPM/simple and Agents of Chaos-style/complex implementations. The theory's
alternative injection route remains documented; it is not the immediate authorised
replacement task. No decision algorithm that hard-codes preferred answers is
permitted without a justified theoretical mapping. Revised encoding still needs
the original validity assessment before Phase 2, followed by configuration
comparisons, benchmarks and validated moral scoring for those respective claims.

The [offline diagnosis](experiments/phase1_5_encoding_validity/offline_diagnosis_20260909/FINDINGS_AND_NEXT_STEP.md)
is complete with no API calls or theory changes. Eight equivalent profiles are
saturated; four other profiles have observed ranges within .10 but do not establish
equivalence; 17 have larger observed ranges with inconclusive conservative bounds;
PD/S3 supports a difference beyond .10 under simultaneous exact uncertainty bounds.
Simulated true-equality success for the existing all-six-pair test at p=.50 is
0/10,000 at N=50, about 35% at N=400 and 91% at N=800. These are planning
diagnostics, not new observations or replacement gate criteria.

The recommended two-by-two attribution experiment is now complete and supports
PD wording, background wording and interaction effects; see the latest status
above. The low/high PD endpoint diagnostic is also complete and supports large
effects from both endpoint descriptions. One operational numeric-axis revision
was approved and its fresh local validation pilot is complete; it did not meet
the local screen. The interpretation and review packet above provide the next
research-decision evidence.
The full revised battery is not prepared or authorised for automatic launch.
Increasing N alone cannot remove the wording
effect demonstrated here. The theory remains unchanged and Phase 2 is on hold.

1. Source sweep, rotations, gradients, independent audit and approved paraphrases
   are collected and scored. Review the battery assessment with the researcher;
   do not rerun completed samples merely to improve their results.
2. The user explicitly approved the previously blocked thesis disclosure to
   Anthropic. Four preserved Haiku generation/correction calls (r2–r5) produced
   final candidates with no changes to the canonical theory or scaffold.
3. The final three candidates pass structural/lexical checks and assistant
   semantic review. Review the [exact templates](experiments/phase1_5_encoding_validity/claude_paraphrases_20260909_theory_r5/HUMAN_REVIEW.md)
   and [review findings](docs/phase1_5_paraphrase_final_review_20260909.md).
   Tommy approved all three exact templates. `paraphrases_approved.json` records
   that approval separately from the preserved unapproved preparation bundle.
   The 4,500-call run is complete; the equivalence criterion was not met.
4. Completed runs have checksum inventories and ZIP backups under
   `output/validity_backups` (same machine, not off-device). The old supervisor
   is stopped; do not relaunch it against the obsolete failed audit designation.
5. Hold Phase 2. Discuss a concrete next-study proposal and any demonstrated
   implementation limitations with the researcher before changing architecture,
   scope, hypotheses, or locked prompts. No revised partial-pass path is assumed.

The final gradient design is frozen in `gradients_20260909_final/manifest.json`.
The user approved its 15,000 calls (estimated $20–$55; actual token estimate
$14.54) and subsequently approved the thesis-containing paraphrase disclosure.
Human semantic approval of the final wording and the completed paraphrase
results are recorded. The current
[evidence matrix](experiments/phase1_5_encoding_validity/phase_review_20260909/evidence_a8076369a0ab8aa4.md)
keeps completed evidence and unresolved criteria distinct; it is not a gate verdict.

## Supervisor handoff

The supervisor can review `code/engine/` and the validity CLI entry points now.
There is no requirement to delay code review until the empirical battery closes.
The latest implementation verification comprises ten sweep tests and nine
follow-up tests, plus the earlier 29 engine checks. Offline verification is
evidence about code, not a scientific phase pass.

Keep the documented RE-on-S3 pilot direction reversal as an open hypothesis
check, not a reason to retune a frozen prompt. LL, CS, and AW lack prespecified
simple-problem directional contrasts; do not manufacture pass/fail directions.

## Retained decisions

The original Phase 0a archive stays immutable. The recalibrated July question set
is the locked working set. The naked holdout replaces the originally planned
null-B holdout, and effects are interpreted against measured baselines with
problem-specific headroom caveats. Phase 1 used S3 plus S2. These are documented
decisions, not unfinished corrections. See the closure records and [decision log](meta.md).
