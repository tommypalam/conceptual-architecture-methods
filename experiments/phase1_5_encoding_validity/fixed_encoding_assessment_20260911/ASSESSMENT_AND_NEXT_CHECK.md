# What the saved evidence supports, and the next check

The target is a profile whose ethical dispositions inform the agent's decision
before it acts. A filter that replaces or justifies the decision afterwards would
not establish that target. The current experiment tests behavioural consequences
of explicit parameter descriptions and values; it does not identify a unique
internal mechanism or establish ethical understanding or AGI.

This is an offline assessment of existing results, not a revised validity rule.
The [30-row evidence map](EVIDENCE_MAP.md) joins the original full-harness sweeps,
representation gradients, paraphrase rotations and active-parameter audit.
[The machine-readable matrix](evidence_matrix.json) preserves source estimates
and hashes. Raw historical calls were not re-audited by this join.

## Strongest existing evidence

MoR/S3 has canonical ADOPT rates of **10%, 26%, 42%, 76%, 84%** at values
.1/.3/.5/.7/.9, with 50 responses per point. Its original directional criterion
is met. This is evidence of graded response across the sampled values, beyond
an endpoint flip; it does not establish behaviour at every intermediate value.
The verbal-only slope retains .562 of the canonical magnitude and meets the
original retention rule. Numeric-only retains .454, below the .50 requirement.
Paraphrase equivalence at .8 is not established. These results make MoR/S3 a
useful diagnostic target, not a validated ethical concept or complete agent.

MS/S2 also meets its original directional criterion, but numeric/verbal slope
retention is only .262/.290. PD/S1 meets the source criterion with rates
94/98/100/100/100%; its limited decision headroom and completely pinned verbal
variant make it weak evidence for flexible control. None of the three eligible
parameter/problem pairs meets both representation-retention checks.

Across all ten parameters, the active audit has 20 items per parameter and no
permutation p below .05. Small samples and imperfect recovery from rationales
leave interpretation unresolved; this is not proof that parameters have no
effect. The audit is shared across problem rows, not 600 independent items.
Only 8/30 original paraphrase cells establish equivalence, against 24 required.
Unestablished equivalence includes imprecision as well as demonstrated
discrepancies; it must not all be relabelled as proven wording effects.

## Grounding candidate: useful result, distinct implementation

The [completed endpoint screen](../evidence_sensitivity_20260911/analysis/SENSITIVITY_REPORT.md)
found grounding MoR/S3 ADOPT 3/30 at .1 and 23/30 at .9, a +.667 difference
with conservative 95% interval [.261,.897]. This establishes local endpoint
response under the added grounding instruction. It does not inherit the original
canonical five-value curve or its verbal/numeric results. The added text is an
experimental aid to interpreting the scenario, not evidence that an agent has
acquired an ethical representation. Grounding's advantage over repetition is
not established merely because their separate intervals differ in significance.

## Next work, in order

1. Review the existing MoR audit items and saved rationales against the exact
   endpoint definitions. Distinguish a wrong semantic interpretation from an
   unrecoverable value or an ambiguous rationale. Preserve blind audit labels
   and treat this unblinded error review as diagnostic, not a replacement score.
   This can start offline without buying more decisions.
2. If that review leaves grounding a coherent candidate, prepare a small test
   of its missing intermediate values, with repetition as a control. The
   original canonical curve already exists and needs no exploratory rerun.
   Specify exact conditions, uncertainty, batch limitations, stop conditions
   and the spending cap before dispatch; no such run is launched here.
3. A promising curve would still need evidence of semantic interpretation and
   robustness under the approved battery. Freeze any selected revision before
   independent confirmation. Do not promote a development screen to a battery
   pass or select a revision merely because decisions agree more often.

The architectural objective retains all five concepts and ten parameters. MoR
is a diagnostic starting point, not a decision to remove the others. Phase 1.5
remains open and Phase 2 remains on hold. No source prompts, theory, scoring
thresholds or agent/tool integration changed. This assessment spent no API
credit; approximately $7.85 remains of the latest $9 allowance, rather than a
verified provider account balance.
