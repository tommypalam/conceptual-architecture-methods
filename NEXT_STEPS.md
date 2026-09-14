# Current state and next steps

Updated 2026-09-13. Publication source: `phase3-preparation-20260913`.
The researcher authorised publishing the completed work and revised paper abstract
to `main`, preserving its previous tip as `backup-1` and retaining `backup`.
See the [publication record](docs/publication_20260913.md) for scope, branch targets
and verification. Continue future implementation on a development branch.

## Phase 3 closed for a scoped objective (14 September)

See the [closure record](experiments/phase3_benchmarks/PHASE3_CLOSURE_2026-09-14.md).
Phase 3 characterised the boundaries of the measurement approach rather than
delivering a benchmark pass. The original five-benchmark N200 study is not
released; Phase 3B human comparison was never attempted and is deferred as
infeasible. Neither is retrospectively passed.

**The decisive new evidence is [pd_endpoint_r2](experiments/phase3_benchmarks/pd_endpoint_r2/ASSESSMENT.md)** -
the first PD designation to pass its review gate and collect data. An
independent review accepted the design with zero blocking issues, and 150
unprofiled decisions were collected on six fresh administrative dilemmas written
without quantities, comparisons or any statement of which option is preferable.

All six tasks returned **modal share 1.00, 25/25 identical decisions**.
Presentation order was irrelevant (first-shown option chosen 51.3% of the time,
48-52% per task), so the unanimity is content-driven. Four tasks resolved to the
procedure-respecting option and two to departing, so it is not blanket
compliance. The screen refused the participant stage; 720 paired decisions were
not collected because they could not have discriminated anything.

This prospectively confirms the saturation mechanism on fresh material and
sharpens it: **ambiguity as judged by an independent reviewer does not produce
dispersion in the harness.** Five designs failed to produce a testable
process/outcome manipulation, and the obstacle is not wording - the harness
returns a determinate answer regardless of how carefully the trade-off is
concealed.

Accounting: Claude $7.139674300/$15, OpenAI $1.443713700/$30, package
$31.489461025/$100. The whole PD sequence spent $0.093134250 across six
designations against $16.829628 of reservations. No collector is running and no
paid batch is queued.

Next: Phase 4B remains the central moral experiment with the good/bad question
unchanged. Two requirements carry over - screen candidate tasks for dispersion
*before* building a study, and select moral tasks from those that actually vary.
A set assembled for theoretical interest and validated only by review will
reproduce consequence_rule_pilot_r1's 96/96 result at larger N.

## PD gradient sequence closed at review (14 September)

Four designations, three paid reviews, **zero screen calls and zero participant
decisions**. Total $0.032921625 against $10.312758 of reservations; the gates
prevented 99.7% of potential spend. See the
[r4 assessment](experiments/phase3_benchmarks/pd_gradient_r4/ASSESSMENT.md).

| Round | Verdict | Cost | Finding |
|---|---|---:|---|
| [r1](experiments/phase3_benchmarks/pd_gradient_r1/ASSESSMENT.md) | revise | $0.028867575 | Evaluative wording cued the answer; a rendered profile block leaked coordinate names to the reviewer |
| [r2](experiments/phase3_benchmarks/pd_gradient_r2/STATUS.md) | never dispatched | $0 | Re-designated after a post-freeze source correction |
| [r3](experiments/phase3_benchmarks/pd_gradient_r3/ASSESSMENT.md) | reject | $0.001966800 | Neutralised wording collapsed Class P into Class N |
| [r4](experiments/phase3_benchmarks/pd_gradient_r4/ASSESSMENT.md) | reject | $0.002087250 | Stipulated totals define the class but reveal the answer |

**The sequence is closed and no r5 should be prepared.** The three failures are
three positions on one axis: the information that defines the process/outcome
divergence is the same information that tells the participant which option
maximises the outcome. Hiding it cannot establish the class structure; showing
it hands over the answer. Escaping that needs a different measurement approach,
not another wording round.

Two of the six blocking findings were reviewer errors and are recorded as such
rather than deferred to. The r4 "class reversal" finding restates the design
specification and calls it a contradiction.

**The PD gradient remains untested.** The
[Phase 5 reanalysis](experiments/phase5_analysis/reanalysis_20260914/ASSESSMENT.md)
stands as recorded: post-hoc, on Phase 2 data, still awaiting prospective test.
What the sequence produced instead is a documented design constraint for
process/outcome manipulation in this harness, which belongs in the write-up
beside the saturation diagnosis.

Accounting: Claude $7.139674300/$15, OpenAI $1.383501075/$30, package
$31.429248400/$100. No collector is running and no paid batch is queued.

## Proposed next study: prospective PD gradient test (15 September)

**DRAFT, not authorised, no calls made.** The
[pd_gradient_r1 protocol](experiments/phase3_benchmarks/pd_gradient_r1/PROTOCOL.md)
converts the post-hoc PD finding into a prospective test. Six fresh tasks in two
classes: Class P where the process-respecting and outcome-maximising actions
diverge (PD gradient predicted), Class N where they coincide (no gradient
predicted). Class N is the discriminating control that separates a
process/outcome mechanism from a general dissent dial; it must not be dropped.

A mandatory U-arm dispersion pre-screen (25 calls per task, reject at modal
share 1.00, at most two replacement rounds) implements the saturation
diagnosis before any profiled collection. Screening is on baseline dispersion
only, never on outcomes.

Design: 120 profiles per task, 720 participant decisions, power 0.932 against
the *weakest* cell observed in the reanalysis; flat-task false-positive rate
0.040. PD's maximum correlation with any other coordinate in R is 0.200, so the
effect is separable by multivariate control. Reproduce the sizing with
`py -3.11 -B code/phase3_pd_gradient_power.py` (seed 20260915, zero API calls).

Projected cost $0.637132 for 871 calls, reservation $0.891985 with headroom,
based on the observed transfer_pilot_r1 rate of $0.00067486 per decision.
Remaining allowances: Claude $7.860326/$15, OpenAI $28.649421/$30, package
$68.603673/$100. Budgets do not reset with a new designation.

Three prespecified failure conditions are recorded in the protocol, any of which
is a publishable outcome. The sign of the result is not a success gate.

Gates before any paid call: researcher authorisation; tasks authored, classed
and hashed; one accepted independent review; offline tests passing; frozen
manifest and cost bound. **Awaiting researcher authorisation.**

## Latest completed step: offline reanalysis and gap repair (14 September)

No API calls, no budget change, no frozen record modified. Cumulative accounting
is unchanged at Claude $7.139674300/$15, OpenAI $1.350579450/$30, package
$31.396326775/$100. Reproduce with `py -3.11 -B code/phase5_reanalysis.py`.

Three documents were added, and they change how the completed evidence is read:

1. [Phase 2 within-arm reanalysis](experiments/phase5_analysis/reanalysis_20260914/ASSESSMENT.md).
   The unprofiled arm was **perfectly deterministic in four of six cells** (400/400
   identical choices on S2 and S3), so the six passing Phase 2 contrasts measure
   variance creation from a deterministic baseline, not distribution shift. Within
   the encoded arm, **Procedural Dependence shows a monotone dose-response** on
   departure from that baseline (quintile spread 35.0-62.5 points, permutation
   p<0.0001 in all four non-degenerate cells) and ranks **first of ten parameters**
   under multivariate control in every one. Nine of ten coordinates show no
   systematic effect. The thesis section 6.1.1 directional signs, locked before
   collection and never previously evaluated, score **5 supported, 4 null, 0 wrong
   sign** - descriptive and uncorrected. The S3 sign reversal is explained as a
   label-ordering artefact, not an effect reversal. PD's dominance on S2/S3 was
   *not* among the locked predictions and remains a post-hoc discovery.
2. [Recognition finding interpretation](experiments/phase3_benchmarks/recognition_r1/FINDING_INTERPRETATION.md).
   The 500-probe screen is filed as a failed gate; the operational verdict stands,
   but the measurement is also a substantive result - cross-provider raters agreed
   500/500 that all five decanonised variants were identifiable at the canonical
   rate. Structure-preserving domain substitution does not conceal a classic
   paradigm. This closes the alternative to the configuration counterfactual and
   raises the priority of one-bit context contrasts.
3. [Cross-phase saturation diagnosis](experiments/phase5_analysis/reanalysis_20260914/SATURATION_DIAGNOSIS.md).
   Four studies across three phases (Phase 2 S2/S3, transfer_pilot_r1 448/448,
   representation_diagnostic_r1, consequence_rule_pilot_r1 96/96) returned nulls
   from one cause: deterministic unprofiled baselines cannot discriminate arm
   contrasts. Proposes a **U-arm dispersion pre-screen** (n approx 20-30,
   modal-share bands) as a required protocol field before any multi-arm budget is
   committed. Screening is on baseline dispersion only, never on outcomes.

The [abstract](docs/abstract.md) was rewritten around these findings. No phase is
reopened, no completed result is altered, and no new hypothesis is presented as
having preceded existing responses.

Next: the three proposals in the saturation diagnosis and reanalysis section 6 -
dispersion pre-screen adoption, a prospective PD dose-response test on fresh
process/outcome tasks, and one-bit configuration contrasts. None is frozen,
costed or authorised. Phase 3 remains open; Phase 4B remains the central moral
experiment under implementation specification v0.2, with the good/bad decision
question unchanged and its tasks now required to be contested in the U arm.

## Preceding paid step: finite-rule moral pilot (14 September)

The [finite-rule pilot assessment](experiments/phase4_coding/consequence_rule_pilot_r1/ASSESSMENT.md)
records one accepted independent review and 96/96 valid individual choices, frozen
at db754fee. Every E/V/U/G condition chose accurate reporting and equal allocation.
All planned credit and fixed-good contrasts are zero; bootstrap intervals are
degenerate and conservative bounds remain wide. There is no observed encoding
advantage, and equivalence is not established. Fixed-standard good covers all
96 choices; the relative strict rule labels the 24 high-cost reports not_good.
The difference was specified prospectively. Human validation and full Phase 4
are not complete.

This run cost $0.111206700; all moral development, including failed screens, totals
$1.329527925/$4. Current cumulative accounting is Claude $7.139674300/$15,
OpenAI $1.350579450/$30 and package $31.396326775/$100. Zero-call replay preserved
2,338 inherited records; the ledger now has 2,435 and the verified archive 7,307
members. Raw evidence remains local, with off-device backup unverified.
No collector is running or further paid batch queued.

Next: prepare a separate contextual/group moral pilot with meaningful competing
duties and recorded consequences. Do not scale the saturated cells or select only
tasks where encoding wins. Retain simpler controls, fixed cross-condition moral
standards, all candidate failures and a reviewed transition map. Human raters stay
deferred. Keep the central good/bad question; the result sign is not a success gate.

## Finite-rule pilot preparation record

The [new finite-rule protocol](experiments/phase4_coding/consequence_rule_pilot_r1/PROTOCOL.md)
prospectively replaces generative primary labels for twelve fully specified actions
with explicit deterministic classifications. It requires independent AI review of
the rule map before 96 participant choices. See the [scope amendment](experiments/phase4_coding/DETERMINISTIC_SCOPE_20260914.md).
This does not repair any failed screen or establish universal moral truth.
Full reservation $0.584697300 plus all prior screening charges $1.218321225 gives
$1.803018525 within the original $4 ceiling. No human raters are required.

R3 is now stopped after 41 calls and four failed measurement checks, with zero
participants. Its [assessment](experiments/phase4_coding/consequence_pilot_r3/ASSESSMENT.md)
records the failures, $0.667539675 cost, zero-call replay and 7,016-member archive.
Current prelaunch accounting: Claude $7.094015500/$15, OpenAI $1.285031550/$30,
package $31.285120075/$100. These are usage estimates, not wallet balances.
The unused first offline manifest is preserved under prelaunch_attempt_01;
source-hash guards caught its outdated review packet before any paid launch.

## Prior design and screening chronology: a stronger paper contribution

Current continuation is the separately designated
[consequential moral pilot r3](experiments/phase4_coding/consequence_pilot_r3/PROTOCOL.md).
R2 stopped at independent review after one $0.038352600 call, without coding or
participants; see its [assessment](experiments/phase4_coding/consequence_pilot_r2/ASSESSMENT.md).
R3 formalizes the paired estimands, action-rating attribution and exact blocking
criteria, and retests all original r1 cases alongside the newer checks. Forty
ratings plus one review precede 96 conditional participant calls. Full r3
reservation $2.647544625 plus r1+r2 charges $0.550781550 totals $3.198326175 within
the unchanged $4 development ceiling. The 14 September continuation does not
reset the provider/package budgets; original source/date labels stay preserved.
The [r1 assessment](experiments/phase4_coding/consequence_pilot_r1/ASSESSMENT.md)
records a failed measurement gate after 33 calls ($0.512428950), with zero
participant decisions. Its 13 check failures include numeric labels contradicting
their own evidence and an uncertainty error. All r1 ratings remain unchanged.
R2 uses one named label per category, deterministic conversion to the same vectors,
explicit missing-fact logic and new development checks. The measurement threshold
is unchanged. Its $2.185882875 full reservation plus r1 cost totals $2.698311825,
within the shared $4 ceiling. No participant run is released by a failed check.

The original [r1 protocol](experiments/phase4_coding/consequence_pilot_r1/PROTOCOL.md)
and scoped manual remain frozen historical evidence.
Its scoped manual and explicit transition model cover costly disclosure and
equal-receipt/total-output trade-offs. Six fresh backgrounds, four tasks and E/V/U/G
arms give 96 participant choices. One Claude review and 32 independent coding calls
precede participant collection; rejected review or failed measurement checks stop
the designation. Exact full reservation is $2.049750450, within the $4 study ceiling
and existing cumulative caps. No participant run is authorized by a failed check.
Five offline tests passed, including full mocked collection, zero-call replay,
historical preservation, measurement/review stops and provider/size guards. A
1 KB inherited transport limit was caught and corrected before spending; the new
separate transport supports evidence-backed ratings and keeps the old audit and
no-retry behavior. Unused prelaunch artifacts are preserved in the pilot folder.
R1 was frozen at `fe2a44bc`, reviewed, screened out and archived. Zero-call replay
preserved its 2,263 inherited records; the ledger now has 2,296 records and 6,890
archive members. Current accounting: Claude $6.489798700/$15; OpenAI
$1.183356075/$30; package $30.579227800/$100. These are usage estimates, not balances.
R2 passed six offline tests and was frozen at `4527dcfd`, then stopped at review.
R3 must pass its expanded offline checks and independent gates before participants.
No round completes full Phase 4 or human validation merely by passing its pilot.

The researcher subsequently clarified that good/bad decisions and consequences
must remain central, and authorised an adaptive exploratory implementation.
[Implementation v0.2](Theory/implementation_specification_v0_2.md) now governs this
forward-looking policy, preserving v0.1 and all frozen studies. The
[central moral experiment brief](experiments/phase4_coding/CAPSTONE_DESIGN_DRAFT_20260913.md)
retains the eight-category relative and four-category fixed-standard evaluation,
adds prospective consequential-choice collection, and now defers human raters
under the researcher's explicit no-budget instruction. See the
[AI-only amendment](experiments/phase4_coding/AI_ONLY_SCOPE_20260913.md).
Prepare the versioned manual and independent AI measurement checks alongside
the transfer packet. Protect a planning reserve of $4 Claude and $10 OpenAI within
existing allowances for this capstone; this is not a quote or extra funding.
Human participation is outside current scope. No moral scores have been assigned.
The thesis may develop hypotheses during exploration; confirmation
claims still require separately planned fresh tests.

On `research-transfer-design-20260913`, the researcher requested a more ambitious,
scientifically distinctive direction. The [transfer strategy draft](experiments/phase3_benchmarks/transfer_design_20260913/STRATEGY_DRAFT.md)
proposes selective process/outcome trade-offs, prediction on held-out situations
and subsequent group validation, grounded in the existing PD theory and a scoped
literature comparison. It includes E/V/S/U controls, candidate estimand, a
672-decision pilot sizing example and a proposed $2 pilot ceiling. The exact
[r1 protocol](experiments/phase3_benchmarks/transfer_pilot_r1/PROTOCOL.md) now freezes
eight blocks, 448 participant calls and one Claude review at a maximum $1.7853165.
Four offline tests passed; prelaunch freeze is `f749a393`. The pilot is now complete:
one accepted Claude review, 448/448 valid participant decisions, $0.302339400.
See the [assessment](experiments/phase3_benchmarks/transfer_pilot_r1/ASSESSMENT.md).
Every response opposed the secretly preferential procedure. Full-profile trade-off
effects were inconsistent across the two settings; PD-only shifts were descriptively
larger. This is not confirmation, numerical superiority or a formal Phase 3 pass.
All ten coordinates and original benchmark failures remain in the record; no
formal Phase 3 replacement is implied. Zero-call replay preserved all 1,814 earlier
records; the ledger now has 2,263 records and all 6,791 archive members passed checks.
No collector is running or paid follow-up queued. The original task should not be
scaled automatically: its saturation limits discrimination of competing explanations.

Current cumulative accounting: Claude $6.056865100/$15; OpenAI $1.103860725/$30;
Phase 2+3 package $30.066798850/$100. These are usage estimates, not wallet balances.
The moral-study reserve remains intact. Raw archives are local; off-device backup
is unverified.

The [moral manual draft](experiments/phase4_coding/manual_r1/MANUAL_DRAFT.md) now
specifies all twelve categories, evidence rules, harmful omissions, mixed cases,
unknowns and independent-judge disagreement. Offline schema/aggregation code in
`code/phase4_moral_schema.py` passed four tests. It validates structure and evidence
references, not factual truth or moral validity; no agent actions have been morally
scored. Next: complete explicit consequential-task rule maps and independent AI
manual review, then freeze a small moral pilot with exact costs and measurement
stopping rules. Human raters are outside the current scope and are not a blocker.

## Phase 2 behavioural study complete (2026-09-13)

The researcher-authorised exploratory-first sequence is complete for the amended
two-anchor behavioural study. See
experiments/phase2_confirmation_20260913/ASSESSMENT.md. Fresh confirmation used
400 profiles, 4,800 individual responses and 300 matched-condition group runs;
11,005 API responses in total. All six primary individual contrasts and one of
seven secondary group contrasts passed their respective Holm corrections.
All final outcomes are complete; three intermediate C3 duplicate-marker votes
remain invalid. Full request/state replay passed with zero new API calls.

Follow-up conservative accounting is $18.755232375; pilot plus follow-up totals
$22.906073025 against the absolute $100 new-package cap. No paid run is active
or queued. Preserve the frozen source, raw records and local verified archives.
The original ten-environment Phase 2 design is not claimed complete. Human
benchmarking is Phase 3 and human-validated moral scoring is Phase 4; the coding
manual still needs the required human review. Ethical understanding, human
resemblance and moral quality are not established. C2 interface limitations and
C3 outcome saturation remain documented; any repair must be prospective.

Read the [completed assessment](experiments/phase2_confirmation_20260913/ASSESSMENT.md),
[full results](experiments/phase2_confirmation_20260913/analysis/RESULTS.md),
[qualitative review](experiments/phase2_confirmation_20260913/QUALITATIVE_REVIEW.md),
and [integrity audit](experiments/phase2_confirmation_20260913/analysis/integrity_audit.json).
The prospective freeze is commit `14349800`, root seed 2026091302. All ten LPM
coordinates, distributions and locked dilemmas remain unchanged. The group
engine preserves Agents-of-Chaos-inspired interaction without claiming direct
integration of the external framework.

The [exploratory pilot](experiments/phase2_exploratory_20260912/ASSESSMENT.md)
remains immutable: 2,180 responses, 75 group runs, $4.15084065 accounted.
Fresh confirmation cost $18.755232375 conservatively (estimated provider token
charge $17.05021125). These are usage-based estimates, not invoice or balance
verification. The $100 cap is not a spending target or downstream authorisation.

## Visual replay available (2026-09-13)

The researcher requested a game-like view of agent interactions. The
[simulation theatre](viewer/README.md) is implemented as a separate read-only
viewer: all 300 confirmation groups and 6,205 responses passed reconstruction;
desktop/mobile browser checks passed. It preserves simultaneous rounds, CEO
vote exclusion, amendment adoption and evidence visibility. No research records
or frozen sources changed, and no API calls were made. Run
`py -3.11 -B code/serve_replay.py`, then open http://127.0.0.1:8765.
Future live/final-simulation support needs a new adapter; the current viewer
replays completed Phase 2 only. Design review and checks are in its README.

The 3D upgrade is complete at `/lab`: three Blender rooms, selectable figures,
recorded vote/disclosure effects and synchronised matched-condition playback.
Both browser suites passed on the upgraded server; all 300 runs / 6,205 rows
passed a fresh offline reconstruction. Mobile label collisions were corrected;
idle rendering, reduced motion and asset-failure fallback were checked. See
[3D design and review](viewer/DESIGN_3D.md) and [usage](viewer/README.md).
The current desktop server is http://127.0.0.1:8766/lab. Generated GLBs and their
checksums are versioned; the editable Blender project remains under `output/`.
The research claims and paid-study status above are unchanged.
The requested desktop UI restyle adds local game-style fonts, tactile controls,
fixed playback and inspector tabs, and full-screen mode. Desktop layout checks
and the existing 3D browser suite passed; rendering and research data are unchanged.

## Phase 3: E/V representation comparison complete; inference remains exploratory (2026-09-13)

The approved representation_diagnostic_r1 completed one accepted Claude review
and all 576 participant decisions, with zero invalid actions. There were 24 fresh
matched profiles, both justice contexts, numeric E/prose V representations and
six isolated ultimatum tasks. See
experiments/phase3_benchmarks/representation_diagnostic_r1/ASSESSMENT.md and CHECKPOINT.json.

At the primary 20-unit offer, Justice LOW rejection was E 11/24 (45.8%) versus
V 7/24 (29.2%); Justice HIGH was E 7/24 (29.2%) versus V 6/24 (25.0%). E-V
differences were +16.7 and +4.2 percentage points, with bootstrap 95% intervals
[-12.5,+41.7] and [-16.7,+25.0]. Their interaction was +12.5 points
[-29.2,+54.2]. Every primary interval includes zero and conservative bounds
are wider. Neither a clear presentation effect nor equivalence is established.
No significance, superiority, human-rate or moral-performance claim is made.

V preserves every rendered value, trait name and endpoint meaning; written
percentages retain quantitative information. The comparison bundles layout,
length, introductory clarification and decimal/percentage framing. It is not
a wholly nonquantitative control or a test of numeral syntax alone. All 96
response grids were complete; six nonmonotone grids are retained. The earlier
E/U result and this fresh E/V sample are not pooled; this study has no U arm.

The run cost $0.409685100 against the $4.200345600 reservation/$4.30 ceiling.
Phase 3 accounting is $6.858386425: Claude $6.029498200 and OpenAI $0.828888225.
Remaining room under the $15/$30 caps is $8.970501800/$29.171111775. Package
accounting including Phase 2 is $29.764459450 under $100. These are conservative
estimates, not provider balances. Specific disclosure approval was received and
the launch block resolved. No collector is running, further paid call queued or
approval pending for this completed run.

Five prelaunch tests passed. Final replay made zero new calls, verified every
request/translation/score/cost and all 1,237 inherited records plus the prior
archive. The ledger now contains 1,814 records; all 5,444 new archive members
passed CRC and SHA-256 checks. Independent integer-total report checks passed.
Tiny floating-point roundoff in three proposer mean-bound pairs is documented
in REPORT_CHECKS.json; binary primary estimates are unaffected. Do not modify
frozen results or source to clean it up retrospectively. Raw data and archives
remain excluded from Git; off-device backup is unverified.

The preceding E/U diagnostic remains complete: 576 valid decisions, +50-point
profile-package difference at offer 20 in both contexts, and zero primary context
interaction with wide uncertainty. All earlier recognition failures also remain:
five alternatives failed >15/50 and the later allocation candidate was discarded
after 5/5 recognition. The original all-five N200 Phase 3 study is not released.
All five benchmark families, ten coordinates, Beta marginals and R stay in scope.
No ethical understanding, human resemblance or moral quality is established.

Next: prepare a theory-grounded unfamiliar-task transfer proposal with matched
prose controls, specifying predicted concept changes and independent task-validity
checks before collection. Derive predictions from existing theory; do not invent
new trait-action mappings, equate wide intervals with equivalence or require
numerical notation to be uniquely effective. Such a supplement cannot silently
replace the original failed recognition controls or formal benchmark requirements.
No follow-up is frozen or queued by this assessment.

## Next work

1. Phase 3: use the [completed representation comparison](experiments/phase3_benchmarks/representation_diagnostic_r1/ASSESSMENT.md)
   to prepare a theory-grounded transfer proposal with matched prose controls.
   Freeze task validity, predicted directions and analysis before any new sample.
   The pilot establishes neither presentation equivalence nor a clear difference;
   preserve the original failed recognition gates and all-five requirements.
2. Phase 4: draft and review the dual moral-coding manual and human gold/reliability
   plan. Obtain the required human review before moral scores are assigned.
   Dissent is not automatically bad; proposed safeguards are not realised welfare.
3. Carry the C2 action/amendment mismatch and C3 saturation into later sensitivity
   design. Do not alter or rerun completed Phase 2 records. Null group tests do
   not establish equivalence; isolated parameter meaning and peer-exposure effects
   were not identified by this package.
4. Continue thesis integration, broader sensitivity/analysis in Phase 5 and
   reporting in Phase 6. Keep the original full-battery shortfalls explicit.
5. Verify an off-device copy of the new raw archive before final research delivery.
   The local confirmation archive has 22,312 files, every member CRC and source
   SHA-256 checked; see [archive verification](experiments/phase2_confirmation_20260913/analysis/raw_archive.json).
   Git alone excludes the raw data. No new paid study is queued.

## Earlier Phase 2 design decisions

The [earlier broad proposal](experiments/phase2_design_20260912/PROTOCOL_DRAFT.md)
was superseded for this run by the exploratory-first two-anchor follow-up.
Its ten-context subset, optional postfilter comparator and proposed configuration
repair were not silently implemented. The two current anchors identify combined
context packages rather than separate societal-axis effects. Group prompts were
repaired prospectively after the pilot; pilot and confirmation groups are not
pooled. Public preregistration has not been performed.

## Earlier accepted Phase 1.5 result

Explicit normative profiles can systematically influence generated decisions in
the tested model, harness and dilemmas. Replicated Procedural Dependence effects
provide the clearest evidence for initial functional normative parameterization.
The application does not substitute an ethically preferred answer after model
generation. Understanding and broad ten-parameter validity are not established.

- [Accepted closure, evidence and limits](experiments/phase1_5_encoding_validity/ACCEPTED_CLOSURE_2026-09-12.md)
- [Thesis results and interpretation](docs/phase1_5_results.md)
- [Updated abstract](docs/abstract.md)
- [Complete all-ten assessment](experiments/phase1_5_encoding_validity/all_ten_assessment_20260912/ASSESSMENT.md)

This is a disclosed change in the conclusion's scope after observing results.
It is not an original section 8.2 pass or a new numerical gate. All ten parameters,
negative findings, frozen criteria, raw responses and original theory are retained.

## Earlier Phase 1.5 execution and cost

The prior structural package saved 3,580 valid behavioural responses and 200 valid
blind codings. The follow-up dispatched all 17,250 requests: 17,247 saved records,
17,234 valid, ten parse failures, three recorded API failures and three unresolved
dispatches. The complete-data primary bootstrap is unavailable. The prespecified
paired sensitivity retains all 180 contrasts, including incomplete contrasts at p=1.
See the complete assessment for uncertainty and multiplicity correction.

Latest tracked package accounting: $22.66401475 / $25, including unknown-charge
bounds. This is not lifetime project spending or a verified provider balance.
No retries, replacement records or additional paid runs are queued. Local archive
verification is complete; off-device backup remains unverified.

## Project organisation

The [central archive](archive/README.md) groups historical material by phase.
The [layout guide](docs/project_layout.md) defines naming and stable provenance
paths. The [previous execution ledger](archive/phase1_5/documents/NEXT_STEPS_before_accepted_closure_2026-09-12.md)
is preserved byte-for-byte. Historical commands and OPEN/RUNNING text are superseded.

The unused nine-prediction protocol and runner are now in
[unexecuted drafts](archive/phase1_5/unexecuted_drafts/). They are not queued or
supported execution entry points. No response record was discarded in cleanup.

The root README now provides the reading order; the Phase 1.5
[evidence index](experiments/phase1_5_encoding_validity/evidence_index.md) groups
all 54 retained study folders by purpose. The researcher intentionally removed
the separate root decision log. Future decisions belong in the relevant phase
document, with current pointers here. Earlier chronologies remain in the archive.

Readability review: meanings and results are unchanged; all study folders remain
listed; descriptive labels preserve their exact source paths. This administrative
change introduces no new analysis, architecture decision or paid run.
Verification: all 54 study folders appear once in the index, and all 171 local
links in the changed documentation resolve. Only Markdown files changed.

## Desktop handoff and publication

The researcher authorised publishing this version to GitHub main and preserving
the previous published main as backup. The [desktop handoff](docs/desktop_handoff.md)
contains continuation context, setup and separate local-data transfer steps.
Recent ignored records require the transfer bundle; Git alone is not the dataset.
Do not recreate meta.md or restart Phase 1.5.
