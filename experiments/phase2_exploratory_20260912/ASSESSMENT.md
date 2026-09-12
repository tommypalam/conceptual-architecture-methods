# Exploratory Phase 2 assessment

**The pilot is complete and informative. It supports a fresh confirmation of
individual profile-package effects, but the group study needs specific repairs
before scaling. It does not establish ethical understanding or moral quality.**

Completed 2026-09-12 on `phase2-design-20260912`; collector frozen at `642c1297`.
Root seed **2026091202**; 50 fresh profiles; configurations **00100** and **11011**;
encoded E and context-only U; five matched groups per task and condition, plus
neutral B bridges. Original marginal distributions and R were unchanged.

## Execution and cost

All 600 individual responses and all 75 group runs were collected: **2,180 API
responses**, below the 2,575 maximum because C1 sometimes reached consensus early.
There were no transport failures, unknown dispatches, duplicate provider IDs,
model substitutions or output-token truncations. All 2,180 generations finished
with `stop`. Exact reconstruction of every request and group state passed with
**zero new API calls**; see [integrity audit](analysis/integrity_audit.json).

600/600 individual responses parsed. Group responses had 25 strict-format
failures (2 C1, 13 C2, 10 C3), leaving 1,555/1,580 valid group responses. Two C3
final outcomes are incomplete because one final vote was unparseable in each.
Those groups remain in the planned denominators and archives. No cleanup call
or retrospective repair replaced the frozen primary results.

Estimated token charge at published global rates: **$3.7734915**, not an invoice
verification. Conservative accounting, including the 10% allowance:
**$4.15084065 / $10**. This leaves **$95.84915935** within the researcher's $100
new-package ceiling; it is not a provider credit-balance statement or permission
to spend the remainder. All paid pilot collection has stopped.

The local raw archive contains 4,436 files (requests, responses, group states and
the fixed review pack). Every archived member was checked against its source
SHA256; see [archive verification](analysis/archive_manifest.json). A local copy
does not establish an off-device backup.

## Individual decisions

Each percentage is based on 50 profiles; intervals are Wilson 95%. E−U intervals
are the prospectively specified paired bootstrap, exploratory and unadjusted.
The response labels below do not designate ethically good or bad outcomes.

| Task and endpoint | Context | Encoded E | Context-only U | E−U, percentage points (95% bootstrap) |
|---|---|---|---|---|
| S1: promote A | 00100 | 100% [93,100] | 92% [81,97] | +8 [2,16] |
| S1: promote A | 11011 | 100% [93,100] | 98% [90,100] | +2 [0,6] |
| S2: formal report | 00100 | 22% [13,35] | 0% [0,7] | +22 [12,34] |
| S2: formal report | 11011 | 12% [6,24] | 0% [0,7] | +12 [4,22] |
| S3: adopt reorganisation | 00100 | 84% [71,92] | 100% [93,100] | −16 [−26,−6] |
| S3: adopt reorganisation | 11011 | 58% [44,71] | 100% [93,100] | −42 [−56,−28] |

S2 and S3 show useful profile-package contrasts. In S3, moving from 00100 to
11011 reduced encoded adoption by 26 points [−40,−12], while the context-only
sample chose ADOPT throughout. This is a promising context-sensitive pattern to
test on a new sample. It is not evidence that any single coordinate caused it.
Both environmental packages change several axes at once.

S1 is saturated: every encoded profile selects A. Retain that negative diagnostic
finding. Increasing N will not automatically make S1 a sensitive measure. Small
bootstrap intervals near a boundary, including degenerate [0,0] intervals in the
machine-readable tables, are not proof of zero population uncertainty.

The whole injection package changes text, instructions and profile information.
This pilot cannot distinguish semantic encoding from all other prompt effects.
It also cannot establish unseen-task transfer: these are previously used dilemmas.

## Group behaviour

Only five matched groups underpin each cell. All cell intervals, missing counts,
pre-tie tallies and process diagnostics appear in [the results](analysis/RESULTS.md)
and [machine-readable analysis](analysis/summary.json). Utterances are not treated
as independent subjects.

- **C1, resource council:** under 00100, E selected A in 4/5 groups (80%, CI
  38–96%), versus U 5/5 (100%, CI 57–100%). Under 11011, both arms selected B
  in 5/5; all five neutral bridges selected B too. Environmental sensitivity
  already exists without profiles. Encoding cannot receive all the credit.
  In 00100, only 2/5 E groups reached unanimous consensus, versus 5/5 U;
  average observed completion rounds were 4.6 and 1.4 respectively. Completion
  at round five is not necessarily consensus. This process contrast merits study.
- **C2, restructuring:** 24/25 groups approved. E in 11011 approved 4/5
  (80%, CI 38–96%); every other cell approved 5/5 (100%, CI 57–100%). Proposals
  and actual adoptions occurred, but final approval is nearly saturated and
  requires interpreting what agents thought was in the working plan.
- **C3, scientific strategy:** every valid group outcome was CONTINUE. Three
  cells have 5/5 valid outcomes (CI 57–100%); U in 11011 and neutral B each have
  4/4 valid outcomes (CI 51–100%) plus one incomplete group. The final choice
  does not discriminate encoding in this pilot. Authenticated public evidence
  totals ranged from 14 to 23 of 24 items. Item-count balance did not produce
  behavioural balance, and no correct scientific answer was defined.

## What the review found

The outcome-independent review comprised 120 individual explanations (IDs
1,6,...46 in every cell) and group 1 in all 15 group cells. Inspection was by
the assistant, unblinded: C1/C3 structured histories, C2 all proposals/adoptions,
all CEO turns and final votes, with selected full raw responses checked against
their exact requests. The archived review pack contains 315 group responses.
This is qualitative diagnostic inspection, **not human gold coding**, and does
not estimate the population frequency of semantic errors.

Individual explanations generally track their chosen options; S1 repeatedly
prioritises reliability and senior-role readiness. S2 gives competing accounts
of procedural legitimacy and proportionality. S3 often balances staff disruption
against institutional momentum. The prose is compatible with functional use of
the profile; self-description alone does not verify the mechanism or all ten axes.

Three issues matter before confirmation:

1. **Formatting changes downstream state.** Most invalid votes are clear labels
   placed at the end of a reasoning line. The frozen parser requires a separate
   line. In addition, the orchestrator only authenticates C3 disclosures from a
   response whose vote parses. Four malformed replies contained directly held
   citations that had not previously been public; in two rounds, two such items
   remained unauthenticated after the barrier. The reasoning excerpt could still
   enter the transcript. This couples vote-format validity to evidence propagation
   and audit coverage. Separate field validity before future collection. Merely
   reparsing final votes cannot reconstruct how the conversation would have changed.
2. **Models can invent adoption.** In C2 group 1, context 00100, U, the CEO's
   round-4 request explicitly said `Currently adopted amendment IDs: NONE`, yet
   its reply referred to “The adopted safeguard”. Several final voter statements
   likewise described an amended plan. The recorded state was correct; the model
   contradicted it. This is a factual state-adherence failure worth retaining,
   not a reason to silently replace the generated vote or invent realised welfare.
3. **Scientific claims can become overstated.** In C3 group 1, 00100, E, agent 14
   at round 5 described “four independent positive trials”. Independence was not
   supplied by the locked facts or evidence schedule. Other replies acknowledge
   uncertainty. This example warrants a separately defined factuality audit; it
   does not justify claiming a measured rate of dishonesty or confirmation bias.

Exact slots, hashes and short excerpts are in
[post-hoc diagnostics](analysis/posthoc_diagnostics.json). The automated C3 audit
flagged zero unavailable-ID citations among the 590 valid-format replies it
processed. That is not a clean semantic-leakage pass: ten malformed replies were
outside that audit, and invented facts or uncited paraphrases evade ID matching.

An [independent-field parser candidate](../../code/phase2_group_fields_v2.py)
has now passed five offline regression checks and was checked against all 1,580
saved group responses. It preserves every previously valid vote and reads 24 of
the 25 malformed votes; the remaining reply contains a zero-width joiner inside
`VOTE`. It also allows legitimate evidence extraction when the vote is invalid.
See [candidate check](analysis/parser_candidate_check.json). This is prospective
engineering work, not a replacement pilot analysis or proof that earlier group
trajectories would have stayed the same. It is not wired into the frozen collector.

## Decision and next study

Do not launch the earlier $27 design unchanged. A larger version would repeat
the group parser/evidence coupling and would still not make moral or human-validity
claims conclusive. The pilot has done its job: it identified usable contrasts,
saturation, actual costs and concrete failure modes cheaply.

Prepare a separate confirmatory record with fresh profiles and seeds, all planned
contrasts (including S1), a prespecified multiplicity correction and missing-data
policy. Make group state adherence an explicit observable diagnostic. Repair
format/evidence handling prospectively and test it against saved failure cases;
do not rewrite this pilot's collector, prompts, records or outcomes. Review
practical context descriptions, evidence informativeness and the moral manual
before claims requiring them. A final confirmation of package effects remains
different from evidence of ethical understanding, human resemblance or better
moral consequences.

See [the concrete confirmation options](CONFIRMATION_NEXT.md) for sample-size and
cost implications. No confirmatory paid call has been dispatched.

Five synthetic review perspectives (not external expert approval): Linden accepts
behavioural evidence but rejects inferring ethical understanding from it; Osei
emphasises ceiling effects and absent human comparison; Tanaka supports fresh
paired confirmation with multiplicity control and rejects treating five groups
as adequate power; Renna treats state hallucination as an empirical limitation
of the agent system; Okafor requires independently valid vote/evidence fields.
The disagreement is whether to scale immediately or repair first. Resolution:
preserve the useful individual evidence and all negative group findings, then
repair and freeze a scoped confirmatory design before further paid collection.
