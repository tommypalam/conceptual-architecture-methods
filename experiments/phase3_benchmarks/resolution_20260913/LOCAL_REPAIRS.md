# Prospective Phase 3 implementation repairs

Continuation: the user approved disclosure and the Claude call returned a
truncated response. See [outcome and disposition](CONSULTATION_OUTCOME.md).
The fuller [canonical revision 2](../canonical_r2/PROTOCOL.md) now supplies exact
text, controls and paired inference; all 38 Phase 3 tests pass. The account below records the
earlier offline mechanics milestone and pre-approval state.

Status: offline mechanics implemented; stimulus and collection release pending.
This is a new revision, not an edit to the frozen first audit or perception check.
No new behavioural outcomes have been collected.

Verification: all 26 Phase 3 offline tests passed, including nine new mechanics
tests. The suite exercises prod exhaustion/reset, full and early termination,
truth/majority counterbalance, critical-trial denominators, missing paired IDs,
nonmonotone acceptance, impossible choices, and truncated observation windows.

## What is implemented

`code/phase3_protocol_kernel.py` supplies independently testable mechanics for
all five families. It cannot make API calls. It preserves all ten individual
coordinates and fills partial contexts without converting NEUTRAL into LOW.
The neutral wording says no institutional stance is specified; individual
characteristics and task facts still apply. This is a proposed Phase 3 assembly
extension, not a rewrite of the frozen canonical prompt.

| Family | Concrete repair | Remaining stimulus decision |
|---|---|---|
| Milgram | Immutable 30-level escalation; each delivery increments 15; four ordered prod opportunities; direct quit; continued compliance resets the prod count; terminal states cannot resume | Full event/script package, correct learning trials versus disclosed abstraction, and the three modulator scripts |
| Asch | 18 unique images, 12 critical trials; six correct positions each; all six truth/wrong-majority pairs occur twice on critical trials; neutral positions 1, 2, 5, 8, 12, 16; seeded order; peer sizes 1/2/3/5 and a correct dissenter | Public/private response script and independent review of the full colour-domain scene |
| Ultimatum | Five separate responder offers (10/20/30/40/50 of 100); conditional rejection at 20; a threshold interval only when complete responses are monotone | Isolated proposer prompt and review of the bonus-domain entitlements and anonymity |
| Bystander | Helping terminates the individual's trajectory; exhausted waiting counts as no intervention; incomplete windows remain missing | One selected emergency paradigm, exact event sequence, opportunity count and presence contrast |
| Reactance | Predeclared symmetric adjacency, full pre/post rankings, separate choice availability; impossible choices remain invalid; rank improvement and adjacent choice are distinct fields | Concrete option set/graph and matched restriction controls that separate social restriction from mechanical unavailability |

The Asch order above is an operational choice, not a recovered historical order.
The existing 18-per-family images are eligible inputs, but their prior no-peer
accuracy does not validate peer-pressure wording or variant equivalence.
Correct-answer keys belong only in the offline schedule; a future request builder
must exclude keys and descriptive filenames from participant/judge text.

Milgram's kernel represents the aversive decision points only. It does not pretend
that 30 decisions reproduce all learning trials. Its worst case is **150 model
decisions per trajectory**, because each level can involve an initial decision
and four prod responses. A response after the fourth prod can still continue;
persisting in hesitation then ends the trajectory. An explicit quit always ends
it immediately. The latter is a disclosed agency-preserving operational rule.

## Denominators and inference

Every assigned trial/profile must be present, including explicit missing or
invalid outcomes. Malformed responses are preserved by the collector before
being represented as missing in scoring; a malformed refusal is not silently
converted into a valid behavioural refusal. Terminal early stops are observed
data, not missing unvisited trials.

Binary outcomes include assigned count, valid count, invalid count, successes,
labelled complete-case rate, and worst-case identification bounds with invalid
outcomes set to zero or one. These bounds are **not confidence intervals**.
Paired contrasts match exact profile IDs and reject unequal sets; they never use
an inner join that silently discards a profile. Asch outcomes use 12 critical
trials per participant, not 18, and population inference must cluster by profile.

The forthcoming analysis freeze must add paired uncertainty and multiplicity
rules; the mechanics tests alone do not supply inferential validation. Original
rate bands remain documented hypotheses with source limitations, not human
reference rates repaired by adjusting the endpoint after data.

## Release and budget

Do not dispatch a population from these primitives. Complete the exact scripts,
independent variant review, 500 recognition probes and two-rater process first.
The proposed exploration uses fresh matched profiles and is separate from the
spec's N=200 confirmation. Cost full trajectories, all visual trials, isolated
roles and control branches before choosing its affordable sample size. The
spec's one-call-per-agent arithmetic is not a cost bound. Do not reduce the
100-matrix sensitivity study to one profile per matrix to fit tonight's cap.

The single Claude consultation packet is already frozen in consult_manifest.json.
Automatic approval review blocked its dispatch because the private specification,
protocols, template and completed-check summary would be disclosed to Anthropic
without sufficiently specific approval. No request was sent and no reservation
was created. Explicit approval for this exact disclosure is pending. Its reserved
maximum is $0.248127 within the existing structural-review allocation; there is
no automatic retry, alternate destination or provider substitution.

## Synthetic five-perspective review

Decision: implement testable mechanics while keeping scientific release separate.
Linden requires no new parameter-to-action rules or claims of ethical understanding.
Osei distinguishes the operational schedules from historical procedures and asks
for matched causal controls. Tanaka requires participant-level denominators,
paired IDs and missingness bounds. Renna preserves all ten coordinates and all
five benchmarks. Okafor requires explicit terminal states and budgeted call units.

Disagreement: exact historical scripts versus an executable AI analogue. Resolution:
implement reusable mechanics now, label new schedules, and require the full
stimulus/review freeze before making claims or collecting population responses.
These are written synthetic perspectives, not external expert or human approval.
