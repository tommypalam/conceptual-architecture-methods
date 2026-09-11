# One-candidate numeric-axis revision: local PD pilot

Prepared September 10, 2026. No API calls have been made. The theory and original
Phase 1.5 gate are unchanged. The researcher authorised continuing toward a
theory-faithful encoding revision, with about $48.69 of the additional $50 budget
remaining. Exact review of this new instruction is still required.

## Problem and candidate

The previous endpoint experiment found substantial low- and high-end wording
effects under the fixed PD=.8/S3 profile. It did not establish a successful
replacement or show that one synonymous phrase is the correct encoding.

One candidate adds a shared instruction to read numerical values as continuous
positions along the axis defined jointly by both endpoints. It preserves every
endpoint string, parameter name/value, normative context, dilemma, label and
response schema. The exact block and four revised templates are in
[HUMAN_REVIEW.md](HUMAN_REVIEW.md). The existing canonical and three approved
Claude-generated endpoint versions remain unchanged beneath that addition.

The clarification is grounded in thesis 3.1's bounded continuous parameters,
the parameter-to-behaviour account in 4.2, and the specification's 4.1.3 discussion
of categorical collapse versus graded encoding. It introduces no linear utility
function, choice probability, numerical weight between traits, new normative
priority, cut-point or preferred action. It applies explicitly to numerical
values, preserving the accepted six-bin verbal-only convention for later work.
The proposal is assistant-authored shared task guidance, not a newly generated
independent paraphrase. Its own wording is not varied in this pilot; a result
would not establish robustness to paraphrasing the added instruction itself.

This is a proposed remedy for ambiguous application of endpoint positions, not
evidence that ambiguity caused the prior results. The instruction affects all
ten traits, but only PD is manipulated here. Findings remain local to a selected
parameter and familiar dilemmas. Fresh responses are not a new-problem holdout.

## Prespecified collection

| Component | Fresh baseline | Fresh revision | Total |
|---|---:|---:|---:|
| PD=.8/S3, canonical + P1/P2/P3, 800 per formulation | 3,200 | 3,200 | 6,400 |
| Canonical PD sweep, five values x S1/S2/S3 x 50 | 750 | 750 | 1,500 |
| Total | 3,950 | 3,950 | 7,900 |

One fixed profile per cell, other nine parameters at existing Beta means.
Neutral full harness; pinned `gpt-5.4-mini-2026-03-17`; temperature 1; cap 600
output tokens; root seed 20260913. The seed is an identifier, not a date.
Sweep values remain .1/.3/.5/.7/.9. PD/S1 retains its original positive
first-option hypothesis. PD/S2 and PD/S3 receive no invented directional sign.

Baseline messages match previous frozen designs exactly. All baseline and
revision responses are newly collected. Shuffle matched baseline/revision
request pairs across component/formulation/problem/value/repetition and randomise
submission order within pairs. Dispatch at most four requests concurrently;
each request gets a distinct seed including its arm and formulation. Requested
seeds and temporal pairing do not establish paired provider randomness. Inference
retains independent binomial-call assumptions and flags potential service drift.

The exact 38 cells and all messages are in [manifest.json](manifest.json).
Nine source files are hash-locked; no completed-run source is edited. Raw
responses remain write-once in ignored `records/`. A normal interruption resumes
undispatched keys. A terminal API/model error stops dispatch after the active
batch and prevents resuming over the preserved failure in place.

## Analysis and local decision rule

For each arm separately, use all six original constrained-score TOST comparisons
among four formulations, .10 margin and alpha .05. All six must establish
equivalence; the 98% parse floor must hold in every cell. Report baseline and
revision rates, intervals and every comparison. A baseline-fail/revision-pass
classification is not itself a formal between-arm improvement test.

Preserve invalid responses. Report the original valid-only TOST result plus an
exhaustive check over every possible ADOPT count among invalids for each eligible
pair at planned N. The local decision rule requires equivalence under every
binary completion as well. Incomplete or below-floor cells remain ineligible.
This added sensitivity safeguard does not retroactively change the original
battery's analysis or gate.

Use the original sweep analysis for both arms: grouped binomial logistic fit,
likelihood-ratio slope test, confidence interval, extreme-value Cohen's h,
monotonicity, separation/pinning flags and prespecified direction. Only PD/S1
can meet a theory-specified PD directional criterion. All other curves are
reported descriptively. The N=50 sweep follows the existing operational design;
it has no new claim of adequate power, and PD/S1's known ceiling limitation
can make this local screen inconclusive even if wording becomes stable.

Consider broader revalidation only if the revised arm establishes local
equivalence including invalid-outcome sensitivity, meets the existing PD/S1
sweep criterion, and avoids the supplementary saturation flag: all four
formulations at or below 5% ADOPT, or all four at or above 95%. This is a
conservative local screening rule, not a new phase pass criterion. It guards
against calling a nearly fixed answer an encoding repair. Even a local screen
success does not establish all-trait effects, independent reasoning recovery,
representation robustness or 24/30-cell equivalence. An unmet screen is reported
without changing N, replacing the candidate or searching for favourable answers.

## Precision justification

N=800 for equivalence uses the already completed equal-rate simulation in
[equivalence_precision_reference.json](equivalence_precision_reference.json),
with original source hash and full result preserved. At a common true rate .5,
the original six-pair rule succeeded in approximately 91% of 10,000 simulated
experiments at N=800, versus about 35% at N=400. This is sampling precision under
actual equality, not the probability this candidate works. Invalid decisions
can reduce sensitivity further. No new power simulation is claimed.

The N increase is a prospective local measurement choice responding to the
documented precision limitation. It does not amend the original N=50 global
battery. A full revalidation's precision, budget and scope must be resolved
explicitly; this pilot does not promise that all remaining validation fits the
current budget or deadline.

## Review, budget and stopping

Human review applies to the exact added block and revised template/message
hashes. The prior endpoint approvals remain provenance, not approval of this new
instruction. The code refuses dispatch without the matching new approval record.

Implementation specification 4.5 says severe paraphrase failure calls for
lexically transparent re-engineering and discussion with the supervisor before
re-attempting Phase 1.5. This packet makes that discussion concrete; the pilot
does not close or replace the battery. Supervisor discussion remains a recorded
review point before any full revised-battery rerun. No message to a supervisor
has been sent, and no endorsement is implied.

Expected token cost about $9, based on recent observed usage with additional
input text. The pilot dispatch guard is $12: before each batch it checks recorded
token cost plus a conservative input-byte/output-cap reservation. Prices used
are the already verified September 10 rates, $0.75/million input and $4.50/million
output, without cache discounts. Provider billing, taxes and unreported retry
charges are not fully captured by this local estimate. Reaching the guard stops
dispatch and leaves an explicitly incomplete sample; it is not outcome-based
stopping. About $36.69 remains unreserved after the $12 planning allocation.
The reservation is not spend; no calls have been made.

No automatic new candidate, sample-size increase, full battery, theory change,
parameter deletion or main-phase run follows this pilot. Keep all outcomes.
On full collection, generate analysis, usage, inventory and verified same-computer
ZIP. The ZIP is not off-device storage; no remote publication is authorised here.

Validation: five focused offline tests passed, including exact-only insertion,
all unchanged endpoint stanzas and original control messages, balanced 38-cell
design, a 1,516-call mock, distinct seeds, no-call resume, correctly separated
sweep/equivalence analysis, saturation/invalid-outcome checks, pending approval
refusal, spending guard before dispatch and preserved terminal failure refusal.

## Execution after exact review

```powershell
python -u -B code/run_validity_axis_revision.py --run-root experiments/phase1_5_encoding_validity/axis_instruction_20260910 --approval experiments/phase1_5_encoding_validity/axis_instruction_20260910/review_approved.json --yes
```

Credentials stay in the process environment. `--score-only` analyses existing
data offline. No credential or paid access was used during preparation.
