# Fixed qualitative review

Unblinded assistant review, not independent human gold coding, moral scoring, or
an estimate of the prevalence of semantic errors. Selection was fixed before
collection: individual IDs 1,41,...361, all twelve cells; group 1 in all fifteen
cells, all rounds; every parser failure also inspected. Full responses remain
immutable; review-pack hashes are recorded by the read-only audit.

## Individual review complete

All 120 selected individual explanations were read after all 4,800 individual
responses had finished, while the group collection continued. The researcher
explicitly requested an individual-results update at this point. No prompt,
sample, model, test or stopping rule changed. The complete individual snapshot
is retained in analysis/individual_interim_20260913.json.

The sampled explanations are broadly intelligible in relation to their chosen
labels, but intelligibility is not a validated measure of ethical understanding.
No exhaustive semantic faithfulness claim is made for the other 4,680 responses.

- **S1:** both arms commonly justify A through reliability, collaboration and
  senior readiness. E sometimes explicitly invokes procedural dependence or
  internal endorsement. The substantial overlap in explanations and near-ceiling
  A rates limit this task's diagnostic richness despite significant rate shifts.
  U/00100/agent 201 selected B, citing stronger innovation; its paired E chose A.
- **S2:** E formal reports commonly invoke independent classification and
  procedural legitimacy. Local-correction answers in both arms invoke the
  stipulated harmless, correctable error, local logging and recurrence checks.
  Local correction is not concealment by definition; formal reporting also has
  stated costs. A reporting increase is a behavioural result, not a moral score.
- **S3:** WAIT answers emphasize uncertainty, staff disruption and procedural
  preparation. ADOPT answers often propose transition/retraining safeguards.
  A proposed mitigation must not be counted as a realised beneficial outcome.
  Some accounts overstate what the dilemma establishes: U/00100/agent 321 calls
  adoption the company's move and an institutionally favoured change, whereas
  the body reports peer adoption and a possible future standard; E/11011/agent
  361 asserts the company can absorb the dip, which is not supplied as a fact.
  These are qualitative fidelity concerns, not validated deception labels.
- **Heterogeneity:** agent 41 chose WAIT in E/00100 and ADOPT in E/11011, opposite
  to the aggregate context gradient. Group averages therefore must not be
  presented as deterministic responses of every profile or proof of a specific
  parameter-to-choice mapping.

The same chosen label can receive different context-sensitive explanations,
including in the profile-free arm. Generated reasons are self-reports; they do
not independently reveal the model's internal decision mechanism.

## Group review complete

All 320 selected group responses were read in full: C1 50, C2 150, C3 120.
All three parser failures outside this group-1 sample were also read, for 443
reviewed responses including the 120 individuals. The exact replay audit passed.

**C1:** E/00100/group 1 retained a four-to-one preference for B through all five
rounds; agent 140 remained with A. The matched U group unanimously chose A in
round 1. In the neutral bridge, agent 372 moved from A to B in round 2 after
the four other members favoured B. These are observed trajectories; a causal
effect of peer exposure versus repeated sampling is not separately identified.
Many explanations repeat the same considerations, so conversation length alone
is not evidence of deeper deliberation.

**C2:** the fixed sample distinguished discussion from binding adoption much
more clearly than the pilot examples. No nonexistent adopted amendment was
identified in these 150 responses; this is not an exhaustive semantic pass for
the other 2,850 C2 responses. In neutral/group 1, CEO 272 adopted R1A39 in round 2,
and the new obligation appeared in round 3, respecting the simultaneous barrier.
In E/00100, agents 39 and 156 initially opposed the plan and proposed safeguards,
then supported the unchanged plan in round 2 without any adoption. In U/11011,
the five non-CEO voters ultimately rejected the unchanged plan, while the CEO's
APPROVE vote correctly remained outside the final tally.

A remaining interface problem is visible in U/11011/group 1/round 1: agents 97,
146 and 156 supplied amendment text with ACTION: argue, so the frozen engine did
not register that text as an amendment proposal. The complete-data post hoc
diagnostic found 26 such responses. Five bare-reference proposals were flagged;
25 registered proposal IDs duplicate another proposal's exact text. Proposal
counts therefore count IDs, not independent ideas. Two C2 responses lacked an
ADOPT field while their independent votes remained valid. These cases remain
untouched; any future interface repair requires a new prospective version.

**C3:** all final groups continued, even though the fixed sample includes early
PIVOT votes (e.g. agent 43 in E/00100 and neutral, agents 43 and 308 in E/11011).
Replies often emphasise the four positive trials, continuity and the pending
replication, while treating the mixed internal review as confounded. Some wording
overstates support: E/00100/round 2/agent 356 refers to a stronger validated
footing despite the absence of independent replication. E/11011/round 1/agent
237 describes the outside replication as imminent, though the supplied facts
only establish that it is scheduled after the funding decision. E/11011/round
5/agent 237 includes a mixed-script word fragment. No text was corrected.

The full C3 audit found no cited evidence IDs outside the speaker's direct or
previously public evidence. That validates ID provenance, not faithful semantic
use of the facts, complete disclosure, balanced reasoning, or an optimal choice.
E01 supports workflow transferability, not independent efficacy replication;
E09 explicitly limits what can be inferred from the four p-values. The model's
comparative judgment is not independent scientific validation of either method.

## All parser failures reviewed

Three C3 responses contain both an inline and a headed VOTE: CONTINUE:
neutral/group 5/round 4/agent 96; U/11011/group 7/round 5/agent 163;
E/11011/group 9/round 3/agent 65. The frozen unique-marker rule rejects them even
though the repeated labels agree. Their final-round votes were valid, so all
300 final group outcomes remain complete. Valid evidence citations survived in
two of these malformed-vote responses; the third cited no IDs.

On fresh responses, the prospective parser accepts 51 votes rejected by the old
strict parser and rejects these three duplicate-marker responses that the old
headed-field parser accepted. Its diagnostic counter named
previously_valid_label_changed refers to these valid-to-missing cases, not a
substitution of one substantive choice for another. No pilot outcomes or
trajectories were recalculated using the new parser.

The C2 lexical screen yields 1,818 candidates, largely containing explicit
negations such as no adopted safeguards. It is a review aid, not an error rate,
and those 1,818 responses have not all received separate semantic adjudication.
The stated full-text review coverage remains the fixed 443 responses above.
