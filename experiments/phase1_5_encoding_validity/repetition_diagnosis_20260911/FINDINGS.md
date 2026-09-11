# Offline diagnosis: two different limitations

No API calls were made. The original experiment outcomes, prompts and gates
remain unchanged. This analysis combines an exact sampling calculation with
an explicitly unblinded review of existing explanations.

## 1. Observed monotonicity is sensitive to sampling

The [precision table](PRECISION_TABLE.md) calculates the probability that five
independent binomial counts are nondecreasing. Positive fitted logistic curves
from four completed datasets supply hypothetical true probabilities. Dynamic
programming sums the probability exactly, including ties; no simulation seed
or additional model responses are involved.

Under the **fresh repetition fitted curve**, the chance of nondecreasing
observed rates at N30 is **30.4%**. Thus sampling alone would break this part
of the rule about 69.6% of the time *if that fitted curve were the truth*.
For the earlier grounding fit, the corresponding ordering probability is
49.2%; for the original canonical MoR fit it is 86.4%.

These are conditional calculations, not probabilities that noise caused our
observed failures. They impose a smooth increasing logistic curve; neither
its correctness nor its estimated parameters are certain. They also omit
the other gate requirements, so ordering probability is an upper bound on
full positive-direction sweep success under valid collection. The historical
pass/fail outcomes stand. No threshold, smoothing rule or sample-size change
is adopted here.

This separates the original strong canonical curve from the weaker repeated
one: a small diagnostic can miss monotonic ordering despite a positive overall
slope. Buying more samples could improve ordering precision under the assumed
curve; it cannot guarantee a valid representation or justify sampling until
a pass appears. The hypothetical N50-N1000 rows are not run recommendations.

## 2. A near-constant decision is a separate issue

The repeated verbal variant selected WAIT 149/150 times. A flat hypothetical
ADOPT probability of 1/150 across all five values produces nondecreasing
counts at N30 with probability 46.9%, largely through tied low counts, despite
having no parameter effect. Under that illustrative flat model, at most one
ADOPT in 150 calls has probability 73.6%. These examples explain why ordering
or a sparse fitted slope alone cannot establish useful control. They are not
an estimate of a genuine verbal-response function.

For historical context, the original unrepeated verbal gradient had ADOPT
counts 4/1/20/10/22 out of 50 per value; numeric-only had 22/18/24/35/40.
Those are recorded in the [original gradient summary](../gradients_20260909_final/analysis/cells_6f4ee2cee96409c4.json).
They show that a floor is not an established universal property of these
representation templates. However, these were different batches: the contrast
with the recent repeated results does not isolate repetition causally.

## 3. What the saved explanations say

Review selection: the first two scheduled calls in **every** one of the 15
recent cells (30 items, independent of their decisions), plus the sole verbal
ADOPT as a separate, openly outcome-selected exception. The
[trace inventory](precision_and_traces.json) contains record keys and source/text
hashes; no responses, original coding labels or audit scores were altered.
This is qualitative diagnosis, not blind gold-standard coding or a prevalence
estimate from a random sample.

| Representation / MoR values | Observations in the two fixed-index items per value |
|---|---|
| Canonical .1/.3 | WAIT justified through process, mixed evidence and staff harm; some wording compresses conditional costs. |
| Canonical .5/.7 | WAIT tied to procedural/internalisation concerns and the neutral context. |
| Canonical .9 | Both sampled items ADOPT, citing peer gains and an implementation plan; the second still invokes procedural fairness. |
| Numeric .1 | One WAIT and one ADOPT; procedural considerations appear in arguments for both decisions. |
| Numeric .3/.5 | WAIT based on caution, asymmetrical costs and uncertain benefits. |
| Numeric .7/.9 | WAIT linked to neutral context, constraint sensitivity and procedural dependence despite high intended MoR. |
| Verbal .1/.3 | WAIT based on risk, staff disruption, fair procedure and endorsement. |
| Verbal .5/.7 | WAIT linked to process/constraint levels, uncertainty and asymmetric staff costs. |
| Verbal .9 | WAIT linked to procedure, genuine endorsement and absence of external pressure. |
| Verbal .7 call0029, exception | ADOPT based on peer gains and a proposed clear plan while still citing sensitivity to process and staff impact. |

The semantic distinction matters: MoR concerns **response form**, whereas
internal endorsement and fair procedure concern other profile dimensions.
These explanations suggest that procedural considerations and contextual
caution compete with response mode, and that the neutral-context wording may
be interpreted as a reason against action. They do not demonstrate those
mechanisms internally or prove that MoR was ignored. Joint-profile decisions
may legitimately reflect several dimensions. The lone verbal ADOPT also shows
that procedural language is not uniquely diagnostic of WAIT.

Some rationales omit the under-delivery condition when describing the
productivity cost, or propose mitigation that is not guaranteed by the dilemma.
These are specific interpretation questions for further review; a short
explanation may compress information without revealing the model's complete
decision process. Do not infer a new gold label or theoretical inversion.

## Decision and next useful comparison

Keep repetition unvalidated and do not commission a larger repeated battery
merely to get a smoother curve. Preserve the original canonical evidence of
parameter influence and the separate representation limitations.

A useful next paid diagnostic would compare **original versus repeated text
contemporaneously**, retaining canonical/numeric/verbal profiles and the
original MoR endpoints. That would distinguish an effect of repetition on
decision variation from a historical batch comparison. Predefine endpoint
contrasts and their uncertainty; two endpoints cannot close the full curve or
encoding-validity gate. Exact allocation, prompts and cap must be prepared
before any launch. No such run is prepared or dispatched by this diagnosis.

No claim of an unresolvable limit, ethical understanding, AGI or phase closure
follows. All five concepts and ten parameters remain. Any actual theoretical
departure still requires a demonstrated technical limitation and consultation.
