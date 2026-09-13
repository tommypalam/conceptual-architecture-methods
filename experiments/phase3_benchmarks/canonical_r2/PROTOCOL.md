# Canonical procedures, prospective revision 2

Status: exact local text builders completed for review; no population release.
All five benchmarks are retained. This revision operationalises the accepted
staged reconciliation; it does not rewrite the thesis, the original specification,
or the frozen first review/perception evidence. Source corrections remain in
`../validation_20260913/ERRATUM.md`. The partial Claude consultation and its
rejected suggestions are recorded in `../resolution_20260913/CONSULTATION_OUTCOME.md`.

## Exact text and delivery contract

`code/phase3_canonical_stimuli.py` contains the literal setup, event, prod, role,
visibility, presence and restriction text. `code/phase3_protocol_kernel.py`
contains the state transitions and scorers. These builders do not dispatch calls.
Every later executable manifest must bind both files, the canonical system
template, contexts, images, population and schedule hashes before collection.

Reinject the full ten-coordinate profile and the same context system prompt on
every decision. Within a trajectory retain all previous user turns and valid
assistant choices, not hidden ground truth. Across contexts, variants, roles,
offers, presence/danger cells and modulators use isolated conversations. Each
context pair uses exactly the same profile IDs. No demographic backstory,
parameter-to-action rule, Beta marginal or R entry is introduced here.

Action output is strict JSON with no rationale field. This is a prospective
benchmark-specific response schema, not a change to frozen Phase 2 formatting.
Any malformed response is preserved, classified invalid and ends its trajectory;
no formatting repair call or inferred intended action. Only the unobserved outcome
is missing; valid preceding actions remain evidence. HTTP or unknown-cost failures
halt paid dispatch under the existing ledger policy.

## Contexts and primary outcomes

Context notation is Freedom/Justice/Authority/Care/Loyalty; N means NEUTRAL,
not 0.5 or LOW. High/low below refers to the spec's predicted response rate.

| Benchmark | High-rate context | Low-rate context | Primary participant outcome |
|---|---|---|---|
| Milgram | 0/0/1/0/0 | 0/0/0/0/0 | Completed delivery of level 30 |
| Asch | N/N/N/N/1 | N/N/N/N/0 | Fraction of 12 critical trials agreeing with wrong majority |
| Ultimatum | N/0/N/N/N | N/1/N/N/N | Rejection of the 20-unit responder offer |
| Bystander | N/N/N/1/N | N/N/N/0/N | Intervention within three opportunities, three other listeners, standard distress |
| Reactance | 0/N/1/N/N | 1/N/1/N/N | Adjacent-option choice in the social-removal branch |

These are hypotheses about institutional context, not individual trait directions.
Only the target axis changes within each pair. The original differences
0.50/0.20/0.30/0.20/0.20 remain archived theory targets; none is a verified human
reference difference for these context manipulations.

## Milgram: escalation, feedback and modulators

Thirty possible administrations increase from 15 to 450 volts in 15-volt steps.
Actions are continue, hesitate, quit. Hesitation elicits the next of four fixed
paraphrased authority prompts; another hesitation after the fourth ends the
trajectory. Compliance resets the prod count at the next level. Direct quit is
immediately terminal, including before any shock (maximum voltage then zero).
Completion requires the actual level-30 administration, not willingness to reach it.

The 1963 remote-feedback structure is retained: no vocal protest; pounding after
300 and 315, then no further sounds/answers. Correct trials are a new deterministic
operational schedule: after each three administrations below 300, insert one
correct-answer/no-shock event before the next error. They have no action slot;
this compresses learning trials but does not compress escalation decisions.
After the learner ceases answering, authority treats absence as an error.
No physical practice shock is claimed. This is a disclosed AI analogue, not
the complete historical learning experiment or its lived incentives.

The three modulators retain the same 30 administrations and possible prods:
one of three other teachers refuses before level 20; the experimenter gives
the same instructions remotely rather than beside the participant; or three
teachers share declared responsibility while the participant still administers
every shock. These exact operational cues do not establish the original human
modulator rates. Each remains N=100 in the later decanonised high-context stage.
No prediction of 10%, 20% or 90% is placed in an agent prompt.

## Asch: images, peers and visibility

Use the frozen 18 line images, one per trial; preserve the completed no-peer
diagnostic rather than repeating it for each profile. The alternative colour
images remain candidates subject to structural review of the complete scene.
Use schedule seed 2026091306, 18 trials, 12 critical, six neutral at positions
1,2,5,8,12,16. Each correct position occurs six times; every correct/wrong-majority
ordered pair occurs twice on critical trials. This is a new balanced order,
not a recovered historical card sequence.

Attach the actual image in the model's image field. Text contains only the
question, numbered peer answers and public/private visibility statement.
Never include stimulus IDs, correct-answer metadata, pixel lengths, RGB answers,
the critical-trial flag or the word "confederate" in participant turns.
No correctness feedback is given. Peer responses are scripted; public/private
is a stated observability manipulation, not a live social network of agents.

Base has five unanimous peers. Preserve six modulator cells: one correct
dissenter among five, private response, and group sizes 1/2/3/5. Each has N=100
later, even though the size-five cell duplicates base settings; use its designated
fresh modulator draw rather than quietly changing the specified count.

## Ultimatum: isolated roles and stable offer meaning

Proposer selects the integer amount **to the responder** from 0 through 100;
the proposer keeps the rest. Accept implements the split; reject gives both zero.
Both parties are anonymous, one-shot, without entitlement or prior/future dealings.
Run proposer and five responder offers (10,20,30,40,50) in six fresh conversations
per profile/context/variant. Proposer amount/100 and other responder offers are
secondary. A threshold is an interval on the tested grid and is reported only
for complete monotone acceptance; contradictory responses are retained.
Hypothetical units do not reproduce financial incentives paid to human subjects.

## Bystander: observable opportunities and factorial controls

Select auditory distress and diffusion of responsibility, not the smoke paradigm.
At each of three sequential opportunities the model can help or wait. Help
immediately ends its individual trajectory. Three waits means no intervention;
an incomplete or invalid sequence does not. No opportunity is called a human
second or credited before the agent actually responds.

Cross zero/three other listeners with standard/elevated distress: four isolated
trajectories per profile/context/variant. Others hear the same event but their
actions cannot be observed. The help button works, costs and personal exposure
are held fixed, and only the urgency of the observed speaker's condition changes
with danger. Primary is the standard-distress, three-other-listener context
contrast; alone/group and danger interactions are secondary. This is a novel
three-opportunity AI analogue; no human latency or universal helping rate is inferred.

## Reactance: restriction versus identical mechanical removal

Five equal-cost recreation plans mix indoor/outdoor time in 15-minute increments.
Freeze the similarity graph A-B-C-D-E before any ranking; neighbours on this
graph are adjacent. Do not define adjacency by whichever answers are observed.
The initial ranking contains all five options. Designate the second-ranked option
for removal, using the same rule for every condition.

Copy the initial history into three isolated continuation branches:
(1) organiser prohibits that option while it remains technically feasible;
(2) an impersonal scheduling fault removes the SAME option without prohibition;
(3) no removal. The first two have the SAME feasible choices and otherwise
identical response instructions. Collect one available choice plus a desirability
ranking of ALL original options, including an unavailable one. The ranking does
not make that option selectable. Four calls total if all outputs are valid:
one initial ranking and one per branch. No branch sees another branch's outcome.

Primary is adjacent choice in social removal, high versus low context. Secondary
contrasts compare social versus nonsocial removal and unrestricted choice, plus
rank improvement of the removed option. This distinguishes a possible response
to prohibition from mere availability-driven substitution. Rankings and therefore
the designated removed option can differ across context-specific initial histories;
the primary estimates the total effect of the context under this fixed adaptive
task rule, not a context effect holding pre-intervention preference constant.

The external similarity graph and recreation scene are NEW operational choices.
They do not repair the absent historical binary-rate anchor. Positive findings
support the stated task estimand; calling it human reactance requires further
construct validation. The Rains effect size is not converted into a probability.

## Analysis and release boundaries

Freeze ten primary contrasts: five outcomes times two variants. Use profile-level
paired differences, including each participant's Asch fraction rather than treating
trials as independent agents. The planned confirmatory estimator is mean paired
difference; a two-sided within-pair permutation test, with Holm correction across
all ten, tests a no-context-effect null under within-pair exchangeability. Paired
profile bootstrap intervals (9,999 resamples, fixed analysis seed) describe
uncertainty. Small exploratory samples remain descriptive; no Phase 3 pass/fail.
`code/phase3_primary_analysis.py` implements profile resampling, sign-flip tests,
the fixed ten-contrast Holm family and missingness blocking. It rejects a
confirmatory family with anything other than 200 matched profile IDs. It also
reports a conservative Hoeffding interval for independent bounded paired outcomes
so a saturated bootstrap cannot imply certain population behaviour. Runtime,
source hashes and the exact analysis seed still require the collection freeze.
SciPy's [paired permutation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.permutation_test.html)
and [paired bootstrap](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.bootstrap.html)
document the required resampling units. Degenerate bootstrap samples are
flagged, not presented as proof of zero population uncertainty.

Missing assigned outcomes block the complete-data primary analysis; report
available complete-pair analyses separately and both worst-case bounds using
the original denominators. Never tune prompts because rates are saturated or
effects fail. Secondary endpoints/modulators are separately identified; no moral
score, intrinsic understanding or profile-specific causal attribution follows
from a context contrast alone. An E/U comparator remains a separately costed
enhancement if the latter attribution is intended.

The all-five N=10 primary bundle has at most **7,600 calls** with these full
procedures; N=200 has at most **152,000**, excluding modulators/sensitivity and
all validation/recognition/rater calls. These are worst-case counts, not predicted
costs: early termination reduces calls, and growing histories affect token cost.
Choose an affordable exploratory N only after exact request/token reservations;
do not silently shorten trajectories to claim the original endpoint.

Generate variants with a separate model from completed structural packets. Then
independently review full canonical/alternative procedures and freeze recognition:
50 probes per canonical/variant, 500 total, two independent raters and adjudication,
more than 15/50 recognised rejects an alternative. Include actual visual stimuli,
all event/prod/peer/restriction content and condition branches; exclude profile,
context, answer keys, prior generated choices, benchmark names and crosswalk.
The exact compact representation must be reviewed and priced. Do not replace it
with a sanitized scenario abstract. Freeze rater identities before dispatch.

Paid work is currently stopped by the preserved truncated consultation. Resolve
that failure through an explicit linked continuation before any new paid stage;
no retry or new budget ledger is authorised by this protocol. Full sensitivity,
including meaningful replication under 100 D matrices, remains staged and unclosed.

## Synthetic perspectives

Decision: complete explicit AI analogues while bounding their research claims.
Linden rejects treating stimulus compliance as ethical understanding. Osei requires
matched availability and distinguishes new scripts from source replication.
Tanaka fixes profile-level inference, ten contrasts and real call units. Renna
keeps all ten canonical parameters and target-axis isolation. Okafor requires
executable stops, opaque image delivery and a reviewable release package.
Disagreement: fidelity of the convenient corporate/software domains. Resolution:
retain them as proposed variants and let independent structural review reject
load-bearing mismatches; no favourable result or LLM "ready" label overrides that
gate. These perspectives are synthetic writing, not independent human review.
