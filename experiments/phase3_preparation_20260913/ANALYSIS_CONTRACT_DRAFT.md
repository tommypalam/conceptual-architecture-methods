# Draft Phase 3 analysis and recording contract

Status: proposed operational contract; not a pre-registration or collection release.

## Units and contrasts

Keep profile identity fixed across each predeclared paired high/low comparison;
use isolated conversations across contexts. Repeated trials or steps within a
benchmark stay clustered by profile; neither becomes an extra independent agent.
Under sensitivity, define whether common random numbers or fresh draws are used
before freezing. Reusing a seed does not create provider determinism.

Each benchmark requires its own measure: trajectory completion, trial conformity,
proposer offer and conditional responder rejection, timed/help-intent event, or
preference restoration. Freeze units, invalid-response handling, primary direction,
reference data and effect-size target before looking at generated outcomes.

Report effect estimates and uncertainty, both absolute benchmark behaviour and
high/low contrasts. Declare a multiple-testing family before collection. A
significant contrast is distinct from satisfying a specified minimum effect or
matching a human reference interval. Do not transplant Phase 2 tests to nonbinary,
repeated-trial or multivariate outcomes without checking their assumptions.

The spec's numeric contrast thresholds are retained as unverified proposed targets
in the registry, not used as executable pass/fail rules. Behavioural predictions,
human rate matching, recognition screening and moral coding are separate claims.
An E/U arm is a proposed addition if profile-specific attribution is required.

## Independent variant and recognition procedure

Separate generation from benchmark execution. Use the reviewed structural packet,
not the human target rate, to generate candidate variants. Save generation provenance.
Independent reviewers bind their decision to exact canonical, variant and structure
hashes. A changed variant invalidates its prior review and recognition results.

The judge sees only scenario content. N=50 per scenario/variant; two independent
classifications per judge response with preserved originals and adjudication.
More than 15 recognised outputs out of 50 exceeds the specified 30% threshold.
Track refusals, ambiguous answers and missing calls separately; freeze how they
affect the denominator. Canonical recognition is expected and not a release failure.
A decanonised version cannot be promoted from an incomplete or unreviewed probe.
Freeze a maximum revision count and budget; the original spec does not bound it.

## Required record and release artefacts

Before collection: reviewed protocol and amendments; exact prompts/stimuli and
hashes; context definitions; population/matrix hashes and seeds; model snapshots;
judge identity; complete schedule; pricing and reservation rules; analysis plan;
review/recognition decisions; frozen source and runtime; offline checks.

Per call: phase/stage, benchmark, variant, context, regime/matrix, profile, role,
trial/step, exact request, prior-state hash, unique slot and provider ID, complete
raw output, parsing diagnostics, timestamps, termination reason, usage and cost.
Write once; retain failures and valid records. Any retry uses a separately linked
attempt. Never repair a response by overwriting it or silently substitute an answer.

The future transport must reserve all in-flight calls against the shared cap,
including judge and generator costs. Unknown usage retains its conservative
reservation. Preflight account room is not provider balance or authorization to
consume it. The current preparation tools have no paid transport implementation.
