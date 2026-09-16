# Concepts as Architecture

## A Probabilistic Framework for Encoding Political-Ethical Concepts in Normative AI Agents

**Tommaso Piero Palamenga**

Bachelor of Science in Mathematical and Computing Sciences for Artificial
Intelligence (BEMACS)
Università Commerciale Luigi Bocconi — Milan

Academic Year 2025–2026

---

*Draft for supervisory review, 18 September 2026. Every numerical claim in this
thesis is traceable to a frozen, write-once record in the accompanying code
repository. Experimental runs are named inline — for example `pd_prospective_r1` —
so that any figure can be checked against its own protocol and assessment
document.*

---

## Abstract

When we give an artificial agent a description of itself — a personality, a set
of values, a profile of numbers — and its behaviour changes, we naturally
conclude that the agent has *read* the description. This thesis argues that the
conclusion is usually unearned, and develops a method for earning it.

The framework encodes five political-ethical concepts — freedom, justice,
authority, care, and loyalty — as ten bounded parameters drawn from calibrated
probability distributions, injected into a large language model's system prompt,
and tested against decisions whose moral classification is computed
deterministically rather than judged. The central methodological problem is that
at least four distinct mechanisms would produce the same observed behavioural
change: the model reading the labels, the mere presence of structured text,
greater prompt length, or a reaction to extreme numbers appearing anywhere. Most
work in this area cannot distinguish them.

The thesis introduces three controls that can. *Pinning* fixes one parameter at
each end of its range while holding the other nine byte-identical, so the two
prompts differ by a single line. A *label-swap control* moves the identical
numeral onto a parameter measured to be inert, holding the block, its length and
its numerals constant, so that only the binding between label and value changes.
A *replication gate* requires an effect to reproduce before its swap control may
be interpreted at all.

Across 18,750 recorded model calls, the results are: parameter profiles change
the deterministic good/bad classification on two models from different providers,
while an explicit ethical instruction written in plain English does not reproduce
the effect; two of the ten parameters are load-bearing under multiple-comparison
correction; and for both, the effect is bound to the parameter's labelled field
rather than to the presence of an extreme number. Both replicate on a second
provider, one of them under a directional prediction derived from theory and
locked in source before data collection.

The finding the thesis treats as most important is a failure. A third parameter
cleared a corrected significance threshold in one well-powered study and
dissolved in the next, larger one, having earlier shown a correlation of the
opposite sign. The replication gate caught it. Without that gate, its null swap
control would have been read as evidence that its label carried the effect.

The thesis establishes no moral improvement, no resemblance to human behaviour,
and no evidence that any parameter is *understood* in a semantic sense. What it
offers is a method for identifying which part of a prompt carries behaviour, a
demonstration that the method detects its own false positives, and a bounded map
of where a ten-parameter encoding does and does not operate.

**Keywords:** normative AI; conceptual encoding; large language models; causal
identification; agent-based simulation; political psychology.

---

## Contents

1. **Introduction** — the inference everyone makes; what is and is not claimed
2. **The Five Concepts and Their Encoding** — parameters, calibration, the joint
   distribution, the decision task, the outcome measure
3. **The Identification Problem** — why the obvious comparison is insufficient;
   the three controls
4. **How the Method Was Forced** — the failures that produced the method
5. **Method** — models, conditions, statistical approach
6. **Results I** — Do profiles change behaviour?
7. **Results II** — Which parameters carry it? (including the withdrawal)
8. **Results III** — Replication across providers
9. **What the Process Taught** — review instability, refusals, defects shipped
10. **Limitations**
11. **Conclusion** — contribution and future work
- References
- Appendix A — Experimental Record
- Appendix B — Items

---

# 1. Introduction

## 1.1 Motivation

Artificial systems increasingly mediate consequential decisions — in workplaces,
institutions, and care. The dominant approach to making their behaviour
acceptable treats ethics as a compliance problem: alignment training,
constitutional constraints, and filters applied at the moment of output. The
system develops whatever implicit normative interpretation it acquires from
training, and corrections are applied at the boundary rather than at the source.

This leaves an awkward opacity. When such a system declines a request, what is
the conceptual reason? When it complies with an instruction, what counted as
authority for it? When it weighs one person's welfare against another's, on what
basis is the comparison made?

This thesis proceeds from a different premise: that a system's normative
interpretation might be shaped by an *intrinsic conceptual architecture* — an
explicit encoding of the political and ethical concepts that structure judgment
from the inside, rather than constraining it from the outside. A compliance
approach asks how to constrain an undertheorised system into acceptable
behaviour. A structural approach asks how to equip a system with conceptual
scaffolding that lets it interpret normative situations in an explicit and
auditable way.

The framework deliberately stands outside any single political tradition. The
five concepts it encodes — freedom, justice, authority, care, loyalty — recur
across very different traditions, and the architecture compares the structural
assumptions embedded in each rather than adjudicating between them. A
high-loyalty configuration is not superior to a high-freedom one; they are
different normative architectures producing different behavioural worlds.

## 1.2 The question this thesis actually answers

The original research question was whether canonical definitions of five concepts
can be encoded as parameter profiles that generate distinguishable and
interpretable social dynamics.

Work on that question produced a narrower and more tractable one, and this thesis
is organised around the narrower version. The reason is worth stating plainly,
because it is the thesis's central methodological insight.

Showing that a profiled agent behaves differently from an unprofiled one is easy,
and it establishes very little. Suppose we give an agent a block of ten labelled
numbers and its decisions change. At least four different things could be
happening:

1. **A field-bound label effect.** The behaviour depends on *which labelled
   field* holds the value — the intended mechanism.
2. **Block presence.** Any structured block changes behaviour, whatever it
   contains. The block acts as a framing or formality cue.
3. **Verbosity.** The profiled prompt is simply longer, and length alone shifts
   output.
4. **Numeric extremity.** The model reacts to an extreme value appearing
   *somewhere*, without binding it to any particular field.

These are not exotic possibilities. They are the default explanations, and
separating them requires controls that are rarely run. The question this thesis
answers is therefore: **which part of the prompt carries the behaviour, and can
we demonstrate it rather than assume it?**

## 1.3 What is claimed and what is not

Stated at the outset, because the framing governs how everything that follows
should be read.

**This thesis does not establish** that any agent behaves ethically, that
outcomes improve, that behaviour resembles that of humans, or that any parameter
is *understood* as a concept. Every outcome label is computed from a stipulated
lookup table applied to the action chosen; nothing is read from or judged about
what the model writes. The word "good" throughout denotes a defined predicate,
not a moral verdict.

The distinction between a *field-bound label effect* and *semantic understanding*
is load-bearing and is maintained throughout. Demonstrating that the same number
produces different behaviour depending on which field holds it is a claim about
binding. It is considerably weaker than a claim that the model represents the
concept the label names. A model that had learned a purely associative link from
the string `Procedural Dependence` to a behavioural disposition, with no
conceptual content whatever, would produce every result reported here.

Two further constraints frame the work rather than qualifying it afterwards.
First, all results come from a **single narrow family** of short
workplace-resource vignettes. That narrowness is what makes the identification
possible, and it bounds what may be concluded. Second, **no human data was
collected at any point**; nothing here speaks to whether these agents resemble
people.

---

# 2. The Five Concepts and Their Encoding

## 2.1 From concepts to parameters

A framework that claims to encode concepts must first say what fixes a concept's
content, or the encoding becomes arbitrary. The framework adopts a **convergence
criterion**: a definition is admitted only where independent research traditions,
using different methods, arrive at compatible accounts of the same phenomenon.
Where traditions diverge, the divergence is recorded rather than resolved by
preference.

This matters because the alternative is circular. If the researcher chooses the
definition and then chooses the behavioural prediction, any result confirms the
framework. The convergence criterion makes the definitions answerable to
something outside the project, and it is falsifiable: a concept for which the
traditions do not converge cannot be encoded on this basis.

Each of the five concepts is given a canonical definition on that criterion, and
each definition is then decomposed into measurable dimensions. Each dimension is
anchored to a published psychological instrument, so that the parameter's
distribution can be calibrated against observed population data rather than
assumed.

**Freedom** is the experiential and behavioural manifestation of agency under
constraint: the felt and observable reaction to perceived restriction, asymmetric
influence, or normative pressure, mediated by relational and structural context
(Deci & Ryan 1985; Brehm & Brehm 1981).

**Justice** is the cognitive-affective appraisal of proportionality between
contributions and outcomes, evaluated through social comparison, sensitive to
both distributional and procedural dimensions, and generating corrective
motivation when imbalance exceeds a subjective threshold (Adams 1965; Colquitt
2001).

**Authority** is the perceived legitimacy of asymmetric social influence,
mediated by compliance, identification, and internalisation, and modulated by
expertise, institutional role, and proximity (Milgram 1974; Kelman 1958).

**Care** is other-oriented concern for the welfare of those perceived as morally
considerable, extended through affective and cognitive mechanisms, activated by
cues of suffering or need, and modulated by the breadth of the moral circle
(Davis 1983; Batson 2011; Crimston et al. 2016).

**Loyalty** is sustained in-group commitment beyond instrumental calculation:
pro-group behaviour at personal cost, mediated by identification and, at its
extreme, identity fusion (Swann et al. 2012; Kelman 1958).

## 2.2 The ten parameters

The five concepts share ten parameters, each bounded in [0, 1]. The sharing is
deliberate: the concepts are not independent modules but overlapping structures
drawing on common dimensions.

| Code | Parameter | 0-endpoint | 1-endpoint | Instrument |
|---|---|---|---|---|
| LL | Legitimacy Locus | external / institutional warrant | internal endorsement | GCOS |
| CS | Constraint Sensitivity | influence reads as environment | nudges read as coercion | HPRS |
| RT | Response Threshold | tolerant | hair-trigger | UG thresholds |
| MoR | Mode of Response | reflective adjustment | confrontational | STAXI / IRI |
| RE | Relational Embedding | atomised, abstract-person | role-sensitive, embedded | Singelis SCS |
| **PD** | **Procedural Dependence** | **outcome-dominant** | **process-dominant** | **Colquitt (2001)** |
| TfA | Tolerance for Asymmetry | egalitarian | hierarchical | SDO7 |
| **ID** | **Internalisation Dependence** | **surface compliance suffices** | **requires endorsement** | **SRQ** |
| MS | Moral Scope | local / role-bound | universalised | MES |
| AW | Affective Weighting | deliberative | intuitive | Davis IRI |

The two parameters in bold are those that survive the empirical tests reported in
Chapter 6. Each parameter is rendered as one line of a ten-line block in the
system prompt, to two decimal places.

Each parameter is assigned a Beta distribution calibrated so that its population
mean and spread match published data from the corresponding psychological
instrument for Western-democratic adult populations. In the general framework a
Gaussian copula couples the ten marginals so that draws reproduce observed
correlations between traits. The studies reported here draw **independent Beta
marginals**, because each tests a single parameter with the other nine held
byte-identical between conditions; the dependence structure would introduce
correlated variation in fields that are held constant, without serving the
question.

## 2.3 Calibrating the distributions

A parameter set alone is not an encoding. The framework's second commitment is
that each parameter's distribution should reflect a real human population rather
than an arbitrary prior, and this is where the encoding becomes falsifiable
rather than decorative.

The natural family for bounded continuous data on [0, 1] is the Beta
distribution, parameterised by two shape parameters α and β. It can take
virtually any shape on the unit interval — uniform, U-shaped, J-shaped,
symmetric, skewed either way — which makes it the default candidate for all ten
parameters. Its mean is α/(α + β), and the sum α + β controls concentration:
higher sums give tighter distributions.

Each parameter's shape is calibrated against a proxy instrument whose score
distribution in the target population is published. The target population is
adults in consolidated Western democracies, with Italian and Southern European
data as primary anchors where available. This scope is not incidental: it is the
same population that generated the behavioural benchmarks the framework aims to
retrodict, so calibration and validation refer to the same reference class.

**The mapping from instrument to parameter is not one-to-one**, and the framework
says so. No existing scale measures exactly "Response Threshold" or "Relational
Embedding". The argument is weaker and more honest: if an instrument measuring a
closely related construct produces distribution shape X in population Y, the
corresponding parameter should approximate that shape after rescaling. This is an
assumption, not a measurement, and it is one of the framework's load-bearing
vulnerabilities.

Legitimacy Locus illustrates both the method and its fragility. It is assigned
Beta(3.5, 2.5), giving a mean of 0.583 — a mild lean toward internal endorsement,
matching the autonomy-leaning population profile documented in
Self-Determination Theory's GCOS data. The axis convention matters enormously
here: it runs 0 = external, 1 = internal, and an earlier version of the
repository had it inverted. An inverted axis with a calibrated mean produces a
population that is systematically wrong in a way no statistical check would
catch, because the distribution is perfectly well-formed. It is worth noting that
Legitimacy Locus is also the parameter this thesis ends up withdrawing (§7.4),
though the two facts are unrelated.

Two parameters are flagged for possible bimodality. Tolerance for Asymmetry and
Moral Scope may have genuinely bimodal population distributions where political
polarisation splits the sample, and a two-component Beta mixture is the
documented fallback. The sampling procedure below works identically with mixture
marginals.

## 2.4 The joint distribution

Sampling the ten parameters independently would generate agents that cannot
exist. An agent with simultaneously high Constraint Sensitivity (reads soft
pressure as coercion) and high Tolerance for Asymmetry (accepts unequal standing)
is psychologically incoherent, but independent sampling would produce such
combinations at non-trivial rates.

The framework therefore constructs a joint distribution using a **Gaussian
copula**. By Sklar's theorem, any multivariate distribution decomposes into its
marginals and a copula encoding the dependency structure between them. Sampling
one agent takes three steps:

```
Step 1.   z ~ MVN(0, R)          draw from a multivariate normal
Step 2.   uᵢ = Φ(zᵢ)             map to uniform via the normal CDF
Step 3.   xᵢ = F⁻¹ᵢ(uᵢ)          map to the parameter via its Beta inverse CDF
```

This preserves each marginal distribution *exactly* while introducing
correlations through the 10×10 matrix **R**. The resulting population occupies
only plausible regions of the ten-dimensional space.

The copula is chosen for interpretability as much as for fit. It is parameterised
by a single correlation matrix that can be inspected, audited, and argued with —
each entry is a claim about how two psychological constructs covary, and each can
be challenged independently. R must remain positive semi-definite to be a valid
correlation matrix; the implementation verifies this at import, and its minimum
eigenvalue is currently 0.311.

**The known limitation is tail independence.** A Gaussian copula assumes
parameters are no more strongly correlated at the extremes than in the middle. If
Constraint Sensitivity and Tolerance for Asymmetry are weakly related among
moderate agents but strongly related among extreme ones, the Gaussian copula
underestimates that dependence — and extreme agents are exactly the ones this
thesis's pinning manipulation constructs. A t-copula, adding one
degrees-of-freedom parameter, is flagged as the robustness check. Richer
alternatives need either far more parameters or a dataset measuring all ten
constructs on the same people, which does not exist.

**Why the studies here draw independent marginals.** Each study reported in this
thesis manipulates one parameter while holding the other nine byte-identical
between conditions. The copula's purpose is to make a *population* plausible;
here the nine non-manipulated parameters are identical across the two conditions
being compared for a given agent, so the dependency structure affects both arms
equally and cannot produce or mask a contrast. Retaining it would add correlated
variation in fields deliberately held constant, without serving the question.
This is a departure from the general framework, made for a stated reason, and the
copula remains the architecture's commitment for population-level work.

## 2.5 The decision task

Agents choose between two options in short workplace-resource vignettes. Each
item presents a claim under a stated arrangement: one option **keeps** the
arrangement, the other **overrides** it. A representative item:

> An office has one bookable desk left for the week. One person booked it and has
> said they want to keep the booking. Two visiting staff otherwise work from a
> corridor bench.
>
> **KEEP_DESK** — Leave the desk with the person who booked it. That person gains
> 1 unit; the two visiting staff lose 4 units between them.
>
> **REASSIGN_DESK** — Give the desk to the two visiting staff. The two visiting
> staff gain 2 units between them; that person loses 5 units.

The design property that makes this work is that **the payoff totals are tied**.
On every item, both options net −3 stipulated units. Welfare-maximisation,
minimax, and best-case seeking are therefore **indifferent by construction**: no
difference between conditions can be produced by any of them.

This property was not assumed but established. An earlier study
(`pd_discriminant_r1`) concluded that the model was following aggregate welfare.
Its successor (`pd_discriminant_r2`) tied the totals and found the choices did not
move at all — refuting the earlier interpretation, which was withdrawn while its
data were left intact.

## 2.6 The outcome measure

Each available action maps, through a table fixed before data collection, to a
deterministic classification. The framework specifies a dual scheme: a
configuration-relative eight-vector with four negative categories drawn from the
machine-ethics literature (power-seeking, deception, disutility, ethical
violation) and four positive analogues, alongside a configuration-independent
four-vector covering harm, deception, coercion, and unfairness avoidance. The
headline measure collapses these into `good` / `not_good`.

**The classification is computed from the chosen action identifier alone.** No
model output is interpreted, rated, or scored. This is what makes the dependent
variable immune to the interpretive drift that would otherwise attend any
"moral" measure — at the acknowledged cost of ecological validity. The thesis
measures choices in a small stipulated world exactly, rather than behaviour in a
rich world approximately.

## 2.7 Why the metric is built the way it is

The outcome measure described above is deliberately austere, and the reasoning
behind it is worth setting out, because two of its features look like weaknesses
until the alternative is considered.

**Why the negative categories are not enough.** The framework's negative
categories — power-seeking, deception, disutility, ethical violation — derive
from the machine-ethics benchmark literature. Used alone they produce a metric
that can only detect harm, never virtue. An agent that does nothing at all scores
identically to one that acts well at cost to itself. Four positive analogues are
therefore defined alongside them: appropriate authority use, honest disclosure,
welfare promotion, and principled compliance under cost, each anchored to a
distinct literature (Tyler 2006; Ashton & Lee 2007; Batson 2011; Aquino & Reed
2002).

**Why principled resistance had to be a positive trigger.** A naïve reading of
those positive categories would code only compliant pro-social behaviour as good.
Compliance with an illegitimate directive, deference to a corrupt authority, or
silence in the face of group wrongdoing would then score as positive — because no
negative category fires — or at worst neutral. That inverts exactly the moral
pattern the framework is meant to detect.

This would build a **structural pro-compliance bias** into the measurement
instrument, and such bias is precisely the normative distortion the framework was
constructed to study rather than reproduce. The manual therefore enumerates four
classes of principled resistance as positive triggers: refusal of an illegitimate
directive, whistleblowing through legitimate channels at personal cost,
welfare-preserving disobedience, and principled noncompliance with a harmful
group consensus. Conformity with a consensus that produces harm is coded as a
negative even where the consensus is internally coherent.

**Why there are two parallel scores.** A methodological hazard sits in
configuration-relative coding. If "appropriate authority use" is judged relative
to the local normative architecture, then the construct differs between
configurations — and an internally coherent but harmful configuration could score
as morally good simply because it behaves according to its own standards. The
metric would be structurally unable to detect the failure mode it was designed to
study.

The framework therefore reports two scores in parallel. The
**configuration-relative** eight-vector evaluates against the local architecture.
The **fixed-standard** four-vector — harm, deception, coercion, and unfairness
avoidance — evaluates configuration-independently. A configuration can be ranked
on harm by the second even where the first cannot rank it on virtue.

**What this thesis actually uses.** The studies reported here use the
deterministic net-score headline on a stipulated transition table, with every
call made under a neutral configuration on all five axes. The
configuration-relative machinery is therefore specified but **not exercised**: no
result in this thesis depends on it, and the configuration counterfactual that
would test it was never run (§10). This is a real gap between the framework as
designed and the framework as tested, and it is stated rather than elided.

The austerity is deliberate. Because classification is a lookup applied to the
chosen action identifier, the dependent variable cannot drift with the
interpretation of what a model wrote. Nothing the agent says is read, rated, or
judged. That removes rater noise entirely — the cost being that the thesis
measures choices in a small stipulated world exactly, rather than behaviour in a
rich world approximately. For an identification study, where the whole point is
that the outcome must not move for reasons unrelated to the manipulation, that
trade is the right way round.

## 2.8 Screening before profiling

A task whose unprofiled answer is always the same cannot reveal any difference
between conditions. This sounds obvious and was learned expensively: four null
results across three earlier phases traced to exactly this cause. In four of six
cells of an earlier study, the unprofiled model chose identically across 400 out
of 400 calls.

Every item set used here is therefore **screened for baseline dispersion before
any profiled call is made**, on the model that will be used. Screening is on
dispersion only, never on outcomes; selecting items by their results is
prohibited throughout.

The screen is load-bearing rather than hygienic. In one instance
(`haiku_screen_r4`), six candidate items were measured on a second model and
**all six returned a modal share of 1.00** — fully deterministic, incapable of
showing any effect. Those items were never run.

---

# 3. The Identification Problem

## 3.1 Why the obvious comparison is not enough

The natural experiment is to compare a profiled agent against an unprofiled one.
This thesis runs that comparison (Chapter 6) and it gives a clear result. But on
its own it cannot distinguish the four mechanisms of §1.2, because all four
predict exactly the same observation.

An analogy: observing that a thermostat set to 30° makes a room warmer than one
set to 10° does not establish that the thermostat reads temperature. It might
respond to the *number* of digits, to the dial being touched at all, or to any
number of things correlated with the setting. To establish that it reads
temperature, one must vary the temperature reading while holding everything else
fixed.

## 3.2 Three controls

**Pinning.** For a parameter *C* and an agent *a*, two conditions are constructed:

```
C−    a's drawn profile with C set to 0.10
C+    a's drawn profile with C set to 0.90
```

The other nine parameters are drawn once per agent and held **identical** between
the two. The system prompts differ by exactly one line; the text the agent reads
is byte-identical. Because both conditions are equally profiled, a difference
between them cannot be a profile-presence effect, a verbosity effect, or a
reaction to being profiled at all.

**The label-swap control.** Pinning shows that *a parameter* moves the outcome.
It does not show that the *label* carries it rather than the number's extremity.
For that, take an inert partner parameter *I* and a level *L*:

```
TRUE(L)    L on C's label,           I's drawn value on I's label
SWAP(L)    I's drawn value on C,     L on I's label
```

Both conditions carry the **identical multiset of numerals**: same block length,
same line count, same ten numbers, same field order. Only *which label holds L*
differs. This is the thesis's central control.

The inert partner is Affective Weighting, the only parameter measured inert by
two independent methods — correlation on unmanipulated data (r = −0.051 and
−0.167, both non-significant after correction) and prospective manipulation
(−0.036, non-significant).

**A worked example.** For an agent whose drawn Affective Weighting is 0.50, the
two conditions of a Procedural Dependence swap at the high level render as:

```
TRUE+                              SWAP+
...                                ...
6. Procedural Dependence: 0.90     6. Procedural Dependence: 0.50
...                                ...
10. Affective Weighting: 0.50      10. Affective Weighting: 0.90
```

Both blocks contain the numerals {0.90, 0.50} across those two fields. Both are
ten lines. Both are identical in length to the byte. The agent's other eight
parameters are untouched. The only difference is which of two labels holds 0.90.

**A precision trap this uncovered.** The block renders to two decimal places. An
agent whose drawn Affective Weighting is 0.102 renders as `0.10`, which collides
with the low level — making the two conditions byte-identical for that agent and
silently diluting the paired contrast. The original check tested the drawn value
and missed it. It now tests the *rendered* value and blocks rather than warns. The
collision was caught before any call was made, and the population seed was changed
on a property of the draw alone rather than on any observed result.

**The replication gate.** A swap control is interpretable only if the effect it
purports to explain is actually present. Each swap therefore requires, in the
same study and the same correction family, that the TRUE condition reproduce the
previously measured effect. **A parameter whose TRUE condition fails to replicate
has an uninterpretable swap control, and nothing is claimed for it.** Chapter 7
shows why this is not a formality.

## 3.3 What the swap control does and does not exclude

This distinction is stated carefully because the temptation to overstate it is
strong.

**Excluded by construction**, not by inference: both conditions carry the full
block at byte-identical length, so block presence and verbosity cannot differ.
These are design invariants, verified on the wire for every agent-item pair
before any call was made.

**Excluded by inference:** *free-floating* numeric extremity. The extreme value
is present in both conditions, so a model responding to extremity as such would
respond to both equally.

**Not excluded:** **field-weighted extremity**. A model might weight an extreme
value by the salience of the field holding it, producing every result reported
here without any semantic reading of the label. This design cannot separate that
possibility from label semantics, and does not claim to. What it establishes is
that the effect is **bound to a specific field** rather than free-floating in the
prompt.

## 3.4 Research discipline

Every study fixes in source code, before any call: the question, the conditions,
the primary test, the decision rule, the directional prediction or its explicit
absence, the interpretation of each possible outcome, and a failure condition.
These are hashed into a frozen release alongside the complete request schedule.

Calls run against a write-once ledger with exclusive locking, reservation
identity checks, and source-hash pinning. Failed calls are preserved and **never
retried in place**: a lost call stays lost. Three such failures persist in the
record and are named in every study that inherits them.

Statistical power is simulated against *measured* per-item baselines before
collection, never against a uniform assumed effect. This distinction has teeth.
One study's power check applied a uniform effect and reported 8 detections out of
8; against the model's real per-item baselines the true figure was at most 5 out
of 10. That study was abandoned rather than run underpowered.

---

# 4. How the Method Was Forced

The controls of Chapter 3 look, set out in order, like a design chosen in
advance. They were not. Each was forced by a failure, and the sequence is worth
reporting because it is the strongest available evidence that the controls are
necessary rather than ornamental. A reader who doubts that the swap control earns
its cost should read this chapter as the argument.

## 4.1 The harness is not neutral

The earliest phase established a baseline: how does the model answer these
problems with no profile at all? The finding was that **the measurement apparatus
itself shapes the answer**. Presenting the same dilemma through different
scaffolding changes the response distribution, independently of any profile.

The consequence is a rule followed throughout: baselines must be measured in the
harness that will be used, never imported from another setting or assumed to be
even. A naked-prompt balance of 50/50 does not license an assumption of 50/50
inside a harness, and the project's recorded closure says so explicitly.

## 4.2 Four nulls with one cause

The behavioural study that followed produced a clear headline: profiled agents
differed from unprofiled ones across six prespecified contrasts. It was only on
re-analysis that the more interesting structure appeared.

**In four of six cells, the unprofiled model chose identically across 400 out of
400 calls.** The baseline was not merely stable — it was deterministic. A
contrast against a deterministic baseline is not measuring a shift in a
distribution; it is measuring the creation of variance where none existed.

That re-analysis also traced four separate null results, spread across three
phases, to this single cause. Each had been interpreted at the time as a failure
of effect size. All four were failures of *dispersion*: on a task whose
unprofiled answer never varies, no manipulation can show anything, and a null is
guaranteed regardless of how large the true effect is.

This produced the screening requirement of §2.8. It is the most expensive lesson
in the record and the cheapest to apply: perhaps twenty to thirty unprofiled
probes per candidate item, before any profiled budget is committed.

## 4.3 Five designs that never collected data

The re-analysis also identified Procedural Dependence as the leading candidate
parameter, ranking it first of ten — and flagged, in the same document, that this
was a post-hoc discovery requiring prospective test before any confirmatory
language.

**Five successive designs were built to run that test. Not one reached the data
collection stage.** Two were stopped by review gates. Three were stopped by their
own dispersion screen: the items, written specifically to pose a process-versus-
outcome dilemma and judged ambiguous by an independent reviewer, produced modal
shares of 1.00 — every agent choosing the same option, every time.

The diagnosis was uncomfortable and is recorded as such: **ambiguity as judged by
a reviewer does not produce dispersion in the harness.** A dilemma that reads as
genuinely difficult to a human reader may be answered identically by the model on
all twenty-five probes. Whatever the model is responding to, it is not the
property a reviewer recognises as difficulty.

The response was the three-level authoring criterion: matched non-unit
consequence text, no asymmetric violation label, and no asymmetric obligatory or
transgressive modals. It was derived from five separate review stops, each
identifying a distinct way an item can telegraph its answer, and it is enforced
in code rather than by inspection. Items built to it cleared six consecutive
review gates with no blocking issues.

## 4.4 What the screen prevented

The screen is not a formality, and two episodes show it paying for itself.

On the second model, six candidate items were measured and **all six returned a
modal share of 1.00**. They were never run. Had they been, the study would have
produced a confident null on a manipulation that could not possibly have
registered.

A third model was evaluated and rejected outright. Every item that produced any
variation on it sat within 0.12 of a ceiling or floor. A power analysis against
the model's *measured* per-item baselines gave at most 5 detections in 10, where
an earlier analysis using a uniform assumed effect had reported 8 in 8. The study
was abandoned rather than run underpowered — the correct decision, reached only
because the power check was redone against real baselines.

Across the project, screen stops and session gates cost roughly $0.50 and
prevented an estimated two thousand calls on stimuli that could not have shown
anything.

## 4.5 What this history implies for the results

Three things follow, and they frame Chapters 6 through 8.

**The identification problem was discovered, not imported.** The permutation
control of §6 was built because the obvious comparison was recognised as
insufficient; the swap control was built because the permutation control failed
on its own terms. Each control exists because its predecessor was inadequate.

**The item set is narrow because narrow is what survives.** Five designs died at
the screen. The items used here are the residue of a long filtering process, and
their tied-payoff structure — the property that makes the identification work —
is the outcome of that filtering rather than a free design choice. This is the
honest version of the external-validity limitation in Chapter 10: the items are
not a sample from a domain, they are the ones that passed.

**Negative results dominate the record.** Of forty-four studies with frozen
results, a substantial fraction stopped before collecting a single profiled
decision. The two positive findings this thesis reports sit on top of a large
pile of designs that did not work, and the pile is preserved rather than
discarded.

---

# 5. Method

## 5.1 Models and scale

Two models from different providers were used: `gpt-5.4-mini` as the calibration
model, on which the framework was developed, and `claude-haiku-4-5` as an
independent replication target. A third model was evaluated and rejected: every
item that produced variation on it sat within 0.12 of a ceiling or floor, leaving
insufficient room to detect an effect.

The complete record comprises **18,750 recorded calls across 44 studies**, at an
accounted cost of $22.24. All per-call records are write-once; releases are
hash-pinned to their source code; power simulations and offline re-analyses are
reproducible from committed modules.

## 5.2 Conditions

| Condition | Content |
|---|---|
| **U** | no profile |
| **G** | no profile, plus an explicit ethical instruction in plain English |
| **E** | the full ten-parameter numeric profile |
| **C−/C+** | full profile with parameter *C* pinned low / high |
| **TRUE/SWAP** | the label-swap control of §3.2 |

The **G** condition is important and is worth describing precisely. It states the
target behaviour in plain English — weigh the interests of everyone affected,
avoid harm, avoid deception, avoid coercion, treat equivalent claims equally —
and thus tests whether the numeric encoding does anything an ordinary instruction
could not.

## 5.3 Statistical approach

All primary contrasts are **paired within agent and item**, comparing conditions
that differ by a single prompt line for the same drawn agent on the same item.
Tests are exact sign tests on discordant pairs. Where a study runs multiple
contrasts, the Holm correction is applied across them as one family; where a
study runs exactly one primary contrast, that p-value is reported uncorrected and
per-item tests are corrected among themselves. Inventing a correction family of
one would be theatre; concealing that per-item tests are multiple would not.

Decision rules require **both** statistical significance and directional
consistency across items — typically a majority of at least four of six or seven
items pointing the same way. Both conditions are fixed before collection.

---

# 6. Results I — Do Profiles Change Behaviour?

Before asking which parameter matters, the prior question: does the profile
change the deterministic classification at all, and can an ordinary instruction
do the same work?

| Model | U | G | E | paired E−G | corrected *p* |
|---|---:|---:|---:|---:|---:|
| `claude-haiku-4-5` | 0.367 | 0.429 | 0.600 | **+0.171** | **0.000112** |
| `gpt-5.4-mini` | 0.395 | **0.378** | 0.606 | **+0.228** | **≈ 0** |

The result holds on both models. On the calibration model, the plain-English
ethical instruction lands **below** the unprofiled baseline (−0.017, p = 0.712) —
it does not merely underperform the numeric profile, it does nothing at all. The
prespecified same-item subgroup across both models gives **+0.255, p < 10⁻⁷**.

E and G are byte-identical in the text the agent reads and differ only in the
system prompt, paired within agent and item.

**An early control, and its instructive failure.** A first attempt at isolating
the labels deranged all ten of them — the same ten numbers, scrambled across
fields. It produced E 0.564, P 0.475, U 0.400. A scrambled block does not clear
baseline (p = 0.122); a correctly-labelled one does (p = 0.00074); but the
difference between them is **+0.089 at corrected p = 0.084** and **fails its
prespecified rule**.

This is reported as a failure rather than a trend. It is also the direct
motivation for the swap control: deranging ten labels at once dilutes the effect
across nine parameters that turn out not to be load-bearing, so the control lacks
power *by construction*. The one-binding swap concentrates the manipulation where
the effect actually is.

## 6.1 Why the guidance result is interesting

The **G** condition deserves more attention than it usually receives in work of
this kind, because it is the comparison that matters practically.

If the aim is to make an agent weigh interests, avoid harm, and treat equivalent
claims equally, the obvious intervention is to *say so*. The G condition says
exactly that, in clear English, in the same position in the prompt. On the
calibration model it produces no improvement over saying nothing at all.

The numeric profile, which never mentions harm, deception, coercion or fairness,
moves the classification substantially. Three readings are available and the data
here do not separate them:

1. The profile engages something the instruction does not — a disposition rather
   than a directive.
2. The instruction is *too* familiar: models are extensively trained on such
   statements, and a generic ethical preamble may be treated as boilerplate.
3. The profile functions as an unusually elaborate context cue, and its content
   is incidental.

Reading 3 is the deflationary one, and Chapter 7 is largely an effort to test it.
The swap control is what distinguishes a cue that works through its *content*
from one that works through its *presence*.

## 6.2 What varies, and what does not

A supporting study (`phase4b_grand_r1`) held the payoff structure frozen across
36 cells spanning three models and twelve items, decomposing the variance in
classification rates:

| Source | Share |
|---|---:|
| between **items** | 44.4% |
| between **models** | 32.1% |
| item × model interaction | 23.5% |

Two implications follow. First, **the item matters more than the model** —
which is why item-level consistency, not just a pooled p-value, is part of every
decision rule in this thesis. Second, the model ordering is not stable: the model
that is most protective here is the *least* protective under a different
stipulated standard, so no model is globally strict or permissive. Strictness is a
property of the pairing between a model and a standard, not of the model.

---

# 7. Results II — Which Parameters Carry It?

## 7.1 The prospective test

Procedural Dependence ranked first of ten in an exploratory re-analysis of
earlier data. That re-analysis explicitly recorded that the finding was
*post-hoc* and required a prospective test before any confirmatory language.
Four subsequent attempts to build that test reached the data-collection stage
**zero** times, each stopped by its own dispersion screen.

`pd_prospective_r1` is that test. The direction was derived from the parameter's
definition and locked in source before collection: PD runs from 0 = outcome-dominant
to 1 = process-dominant; every item presents a claim under a stated arrangement;
the option keeping the arrangement classifies `good`; therefore **PD+ should
produce more `good` decisions than PD−**.

| Condition | Good-rate | n | vs U | *p* |
|---|---:|---:|---:|---:|
| PD− (0.1) | 0.382 | 280 | −0.041 | 0.431 |
| U (no profile) | 0.423 | 175 | — | — |
| **PD+ (0.9)** | **0.729** | 280 | **+0.306** | **< 10⁻⁸** |

**Paired +0.346, corrected p ≈ 0, six of seven items positive.** The entire
manipulation is one line of the prompt. One item ran negative (−0.150) and is
reported rather than smoothed away.

## 7.2 The label carries it

`label_semantics_r1` applies the swap control to PD, with AW inert:

| Condition | `0.9` sits on | Good-rate |
|---|---|---:|
| **TRUE+** | **Procedural Dependence** | **0.729** |
| TRUE− | Procedural Dependence | 0.389 |
| SWAP+ | Affective Weighting | 0.557 |
| SWAP− | Affective Weighting | 0.593 |

**TRUE +0.339 (corrected p ≈ 0). SWAP −0.036 (corrected p = 1.000).** Four items
survive correction on TRUE; **none** on SWAP.

Move the identical number from one line to another, and the effect vanishes.

## 7.3 The sweep

The remaining eight parameters were each pinned to their endpoints, 25 agents
across 7 items, with the Holm correction applied over all eight contrasts as a
single family:

| Parameter | Effect | Corrected *p* | Items | Load-bearing |
|---|---:|---:|---|---|
| **ID** Internalisation Dependence | **+0.143** | **0.00056** | 6+/1− | **yes** |
| LL Legitimacy Locus | −0.131 | 0.00082 | 0+/6− | *see §7.4* |
| TfA Tolerance for Asymmetry | −0.103 | 0.111 | 2+/5− | no |
| MoR Mode of Response | −0.097 | 0.069 | 1+/6− | no |
| MS Moral Scope | −0.069 | 0.292 | 2+/5− | no |
| RE Relational Embedding | +0.046 | 0.906 | 4+/2− | no |
| RT Response Threshold | −0.023 | 1.000 | 3+/3− | no |
| CS Constraint Sensitivity | −0.017 | 1.000 | 3+/3− | no |

Seven parameters are **not** load-bearing. This is a corrected null at adequate
power (24 of 24 simulated detections at d ≥ 0.20, with no false positives), not
an absence of evidence.

## 7.4 The most important result: a parameter that died

Legitimacy Locus cleared the sweep's threshold with the most directionally
consistent pattern in it — negative in all six items showing any effect, none
positive.

A subsequent study ran swap controls for both survivors, each with a TRUE
condition as a replication gate, at 40 agents:

| Contrast | Effect | Corrected *p* | Items | Reading |
|---|---:|---:|---|---|
| **ID: TRUE** | **+0.111** | **0.00467** | 5+/1− | replicates |
| ID: SWAP | +0.046 | 0.408 | 5+/2− | **null — the label carries it** |
| LL: TRUE | **−0.014** | **0.708** | 4+/3− | **fails to replicate** |
| LL: SWAP | −0.046 | 0.408 | 1+/4− | **uninterpretable** |

Legitimacy Locus across three measurements:

| Measurement | LL |
|---|---:|
| correlation on unmanipulated data | **+0.271** |
| pinned, 25 agents | **−0.131** (corrected p = 0.00082) |
| pinned, 40 agents | **−0.014** (corrected p = 0.708) |

**Positive, negative, null.** This is not a power failure: it failed on the
*larger* sample, with 17 of 20 simulated detections at the previously measured
effect size.

**Legitimacy Locus is withdrawn.** Its status is **unresolved, not inert** —
failing to replicate is not the same as being measured flat, and no claim is made
that it does nothing.

**Why this matters beyond one parameter.** LL's swap control was null — which is
precisely the signature of a genuine label effect. Had the swap been run alone,
as it was for PD and as would have been natural, that null would have read as
confirmation, promoting a parameter that does not replicate. **The replication
gate is the only reason this was caught rather than published.**

A parameter can clear a corrected significance threshold in a single well-powered
study and still be noise.

**The general lesson.** The literature on replication failure usually frames the
problem as insufficient power or undisclosed flexibility in analysis. Neither
applies here. The sweep was adequately powered by simulation against measured
baselines; the decision rule was fixed in source before collection; the analysis
was not adjusted after seeing results. Legitimacy Locus cleared a corrected
threshold under prespecified conditions and still did not survive.

What caught it was **structural**, not statistical: a design requirement that any
explanatory control carry, in the same study and the same correction family, a
condition reproducing the effect being explained. That requirement costs nothing
beyond the additional conditions, and it converts a class of false positives into
visible failures.

## 7.5 What the two survivors have in common

Procedural Dependence and Internalisation Dependence are, on inspection, the two
parameters whose definitions map most directly onto the structure of the items.

PD runs from outcome-dominant to process-dominant, and every item is a choice
between honouring a stated arrangement and overriding it for a better aggregate
outcome. ID runs from "surface compliance suffices" to "requires genuine
endorsement", which bears on whether a stated claim retains force when it becomes
inconvenient.

The seven parameters that do not move the outcome — response threshold, moral
scope, tolerance for asymmetry, and the rest — have no comparable purchase on
these particular items. Nothing in a desk-booking dispute is specifically about
the breadth of one's moral circle.

This is a natural reading, and it should be held loosely. It is **post-hoc**: the
correspondence was noticed after the results, not predicted before them, and only
PD's direction was derived in advance. It also has an uncomfortable corollary —
if the surviving parameters are those that match the item structure, then a
different item family would likely yield a different map, which is precisely the
generalisation question Chapter 10 flags as open. The result may say as much about
the items as about the encoding.

---

# 8. Results III — Replication Across Providers

Every measurement to this point used the calibration model. Both survivors were
re-tested on `claude-haiku-4-5`, 40 agents, on that model's six dispersing items.

| Parameter | gpt | haiku | *p* (haiku) | Items | Test |
|---|---:|---:|---:|---|---|
| **PD** | +0.346 | **+0.133** | **0.00031** | 4+/1− | **one-sided, theory-derived** |
| **ID** | +0.111 | **+0.075** | **0.0328** | 4+/2− | two-sided |

The PD replication is the stronger of the two. Its direction was locked
**one-sided** from the parameter's definition, and the derivation depends on a
property of the *item set* rather than of the parameter — namely that keeping the
arrangement classifies `good` on every item. Since the two models use partially
different items, that premise was **re-verified against the new item set at build
time and gated the release**. Only the direction transferred from the first
model; never the magnitude.

**Both effects shrink**: PD to roughly 38% of its original value, ID to 68%. What
replicates is the **direction and the decision rule, not the magnitude**, and no
claim of magnitude stability is made.

**A correlation that pointed at nothing.** Before this study, PD's correlation on
the second model was **+0.089** — near flat, and the basis on which this project
had described PD as "flat on haiku". Pinned, it gives **+0.133 at p = 0.0003**.

Together with Legitimacy Locus, whose correlation was strongly positive and whose
manipulation was negative then null, this gives two clean demonstrations pointing
in opposite directions: **correlations on unmanipulated parameters mislead in
both directions.** Only manipulation settles a parameter.

**Neither parameter is *verified* cross-model.** No swap control was run on the
second model: a four-condition design quadruples the correction family, and an
underpowered TRUE condition would render the swap uninterpretable *by
construction* — manufacturing the Legitimacy Locus outcome by design. These
results license "the parameter moves the outcome on the second model too", and
nothing stronger.

## 8.1 The final map

| Parameter | Pinned effect | Swap control | Second provider | Status |
|---|---:|---|---:|---|
| **PD** | +0.339 to +0.346 | −0.036 n.s. | +0.133 | **field-bound label effect** |
| **ID** | +0.111 to +0.143 | +0.046 n.s. | +0.075 | **field-bound label effect** |
| ~~LL~~ | −0.131 → −0.014 | uninterpretable | not tested | **withdrawn, unresolved** |
| seven others | −0.10 to +0.05 | — | — | not load-bearing |

**Two of ten parameters carry the behaviour, and for both, the effect is bound to
the labelled field rather than to the number.**

---

# 9. What the Process Taught

Three findings emerged from conducting the research rather than from its
hypotheses. They are reported because they bear on how work of this kind should
be done.

## 9.1 AI design review is not a stable instrument

Each study introducing new materials passed an independent AI review gate before
collection. The gate caught genuine errors — a reviewer-prompt mismatch, an
answer-key leak in a review packet, normative cues in option wording — and those
catches drove a three-level authoring criterion for items that took five review
stops to derive.

But the *verdict* is not a stable property of the material. One item pool was
reviewed on byte-identical content and returned **accept** (after which 956
decisions were collected), **accept**, **accept**, then **reject**. A second
pool: four accepts with zero blocking issues, then **revise** with two blocking
issues, on material that had already grounded 631 collected decisions.

The rule adopted in response: for materials already reviewed and accepted, a
further review is **advisory** — its findings are recorded and assessed, but a
rejection does not stop collection. New materials remain hard-gated. Re-running a
review to obtain a different verdict is prohibited, and every verdict obtained is
recorded, including those proceeded past.

Anyone using a language model as a design gate should expect verdict instability
and decide in advance what a rejection licenses.

## 9.2 Refusals that shaped the record

- **Outcome-driven item selection, refused.** Three of seven items showed effects
  too small to survive correction. Cutting them would have saved roughly 40% of a
  budget and would have biased the sweep toward parameters behaving like PD. All
  seven were retained.
- **A study abandoned on power.** Described in §3.4.
- **An interpretation withdrawn.** Described in §2.5.
- **A lost call never retried.** A network timeout at call 689 of 2,801 left a
  slot unresolved. It is preserved unresolved, named in every study that inherits
  it, and the 689 paid calls were not reused.

## 9.3 Two defects that were shipped

Reported because the thesis's claim is partly about method discipline.

**An empty analysis, twice.** Two studies dropped the dispersion screen, their
items having been screened already, but derived the analysis task list *from*
that screen — yielding an empty list and no result for every contrast. All
decisions were intact and were re-scored offline against each study's own
declared item set, leaving the hash-pinned collectors frozen. The second
occurrence was inherited from the first: the symptom had been fixed, and the
collector had not. The third study built on that code carries the fix at source
and produced its own analysis.

**A power check against an assumed baseline.** Described in §3.4; caught before
any spending.

---

# 10. Limitations

Stated as constraints on what may be concluded.

**No moral claim of any kind.** Every outcome is a deterministic lookup from a
stipulated table. The thesis measures which action is chosen, never whether it is
good.

**No human resemblance.** No human data was collected. Human behavioural
comparison was one of four specified deliverables for the analysis phase and it
is **unmet** — deferred under a no-budget constraint and not retrospectively
passed.

**No evidence of understanding.** §1.3 and §3.3.

**Narrow coverage — the principal limitation.** Seven items on one model, six on
the other; 25 to 40 agents per study; one harness; one moment in time. All items
are workplace-resource vignettes sharing an identical tied-payoff structure.
Whether the method or the map transfers to other task families is **untested**,
and it is the most important open question about this work.

**Not verified cross-model.** §8.

**The configuration counterfactual was never run.** The framework specifies a
configuration-counterfactual difference as its primary discriminator for
training-data contamination. Every call reported here used a neutral
configuration on all five axes. That control is absent.

**Separability is of the sampler, not the concepts.** Nine of ten principal
components are needed to account for 90% of variance (minimum eigenvalue 0.621).
This is a property of how agents are drawn, not evidence that the underlying
concepts are distinct.

**A contamination result bounds the framework.** A 500-probe screen, dual-coded
across providers with complete agreement, found all five decanonised benchmark
variants identified at the canonical rate — 50 out of 50 in every one of ten
cells. Structure-preserving domain substitution does not conceal a classic
paradigm from a frontier model.

## 10.1 Which limitations are fixable and which are structural

Not all of the above are the same kind of problem, and a reader deciding what to
build on should know which is which.

**Fixable with money and time.** Coverage is the clearest: more items, more task
families, more models. Nothing conceptual stands in the way — the constraint was
a budget of roughly $32 across the whole project. Swap controls on the second
provider fall in the same category, costing perhaps two dollars. Human comparison
is fixable in principle but expensive in practice, requiring ethics approval and
participant payment that this project could not fund.

**Fixable but harder than it looks.** Broadening the item set is not simply a
matter of writing more vignettes. Chapter 4 records five designs that died at
their own dispersion screen, and the tied-payoff property that makes the
identification work is the *output* of a long filtering process. A second task
family needs items that both disperse on the target models and preserve the tied
payoffs, and the base rate for producing such items in this project was low.

**Structural, and not fixable by this method.** The distinction between a
field-bound label effect and semantic understanding is the important one. No
amount of input-side intervention will settle whether the model represents the
concept a label names, because input-side intervention can only ever establish
which part of the input matters. Settling the semantic question needs a different
instrument — internal analysis on an open model, or a design that examines stated
reasoning as well as choices (§11.2).

Similarly, field-weighted extremity (§3.3) cannot be excluded by any variant of
the swap control, because the swap necessarily moves the extreme value between
fields of differing salience. Excluding it would need a manipulation that holds
salience constant while varying the label, and it is not obvious what that would
look like.

**A limitation of the outcome measure that deserves its own note.** Because
classification is a lookup on the chosen action, the measure is blind to
everything about *how* the agent decided. Two agents choosing the same option for
opposite reasons are indistinguishable. This is what makes the dependent variable
stable, and it also means the thesis cannot speak to reasoning at all — a
restriction that is easy to forget when reading effect sizes that look like
measurements of disposition.

---

# 11. Conclusion

This thesis asked which part of a structured prompt carries an agent's behaviour,
and answered it for a ten-parameter encoding on one task domain: **two parameters
of ten, and for both the effect is bound to the labelled field rather than to the
number's presence.** Both replicate on a second provider, one under a
theory-derived one-sided prediction. What is claimed is the method and this
demonstration of it — not a general property of the encoding, and not semantic
understanding of any label.

The result most worth carrying forward is the **withdrawal**. Legitimacy Locus
cleared a corrected significance threshold with the most directionally consistent
pattern in its sweep, and dissolved on a larger sample of the same model. Its
swap control was null, which is the signature of a genuine label effect. Only the
replication gate distinguished the two cases.

There is a broader point in that. Methods that can only confirm are weaker than
methods that can destroy their own findings. The framework set out to show that
explicit conceptual encoding does genuine work; what strengthens that claim is
not that two parameters survived, but that a third did not, and that the
machinery was built to notice.

## 11.1 Contribution

The thesis makes three contributions, in decreasing order of confidence.

**A control that isolates field binding.** The one-binding swap holds the block,
its length, its field order and its complete multiset of numerals constant while
moving a single binding. This is a stricter control than the ablation designs
common in prompt-sensitivity work, which necessarily change length and content.
Its cost is that it requires a parameter measured inert to serve as a partner,
which must itself be established rather than assumed.

**A replication gate that detects its own false positives.** Pairing every
explanatory control with a condition reproducing the effect it explains converts
a class of undetectable errors into visible failures. The Legitimacy Locus
withdrawal is the demonstration, and it is the result this thesis would most want
carried into other work.

**A bounded empirical map.** Two of ten parameters carry behaviour on this task
domain, seven do not under adequate power, and one was withdrawn. The map is
narrow, and its narrowness is stated rather than minimised.

A fourth contribution is negative and methodological: AI design review returns
inconsistent verdicts on byte-identical material (§9.1). Anyone building a
research pipeline around model-based review should know this before depending on
it.

## 11.2 Future work

In order of value. First, a second task family: the narrowness
of the present item set is what makes identification possible and what most
limits the conclusions, and nothing else would do more to establish whether the
map generalises. Second, swap controls on the second provider, which would
upgrade both parameters from "moves the outcome" to "verified". Third, the
configuration counterfactual the framework specifies and this work never ran.
Fourth, human behavioural comparison — the unmet deliverable, requiring resources
this project did not have.

A fifth direction is more speculative. Every study here manipulates a parameter
and observes a choice. Nothing examines *what the agent says* about why it chose
as it did, because the outcome measure was deliberately built to ignore generated
text. A design that paired the deterministic classification with an independent
analysis of stated reasoning could ask whether the parameter's effect is
accompanied by reasoning that mentions the corresponding consideration. That
would not settle the question of semantic understanding — a model can produce
fluent justifications for dispositions it does not have — but it would bear on
it, and the current design cannot speak to it at all.

---

# References

Adams, J.S. (1965). Inequity in Social Exchange. In L. Berkowitz (Ed.),
*Advances in Experimental Social Psychology*, Vol. 2, pp. 267–299.

Aquino, K. & Reed, A. II (2002). The Self-Importance of Moral Identity. *Journal
of Personality and Social Psychology*, 83(6), 1423–1440.

Asch, S.E. (1956). Studies of Independence and Conformity: A Minority of One
Against a Unanimous Majority. *Psychological Monographs*, 70(9), 1–70.

Ashton, M.C. & Lee, K. (2007). Empirical, Theoretical, and Practical Advantages
of the HEXACO Model of Personality Structure. *Personality and Social Psychology
Review*, 11(2), 150–166.

Batson, C.D. (2011). *Altruism in Humans*. Oxford University Press.

Bond, R. & Smith, P.B. (1996). Culture and Conformity: A Meta-Analysis of Studies
Using Asch's Line Judgment Task. *Psychological Bulletin*, 119(1), 111–137.

Brehm, S.S. & Brehm, J.W. (1981). *Psychological Reactance: A Theory of Freedom
and Control*. Academic Press.

Burger, J.M. (2009). Replicating Milgram: Would People Still Obey Today?
*American Psychologist*, 64(1), 1–11.

Carnahan, T. & McFarland, S. (2007). Revisiting the Stanford Prison Experiment.
*Personality and Social Psychology Bulletin*, 33, 603–614.

Cohen, J. (1988). *Statistical Power Analysis for the Behavioral Sciences*
(2nd ed.). Lawrence Erlbaum.

Colquitt, J.A. (2001). On the Dimensionality of Organizational Justice: A
Construct Validation of a Measure. *Journal of Applied Psychology*, 86(3),
386–400.

Crimston, D., Bain, P.G., Hornsey, M.J. & Bastian, B. (2016). Moral
Expansiveness: Examining Variability in the Extension of the Moral World.
*Journal of Personality and Social Psychology*, 111(4), 636–653.

Davis, M.H. (1983). Measuring Individual Differences in Empathy: Evidence for a
Multidimensional Approach. *Journal of Personality and Social Psychology*, 44(1),
113–126.

Deci, E.L. & Ryan, R.M. (1985). The General Causality Orientations Scale:
Self-Determination in Personality. *Journal of Research in Personality*, 19(2),
109–134.

Güth, W., Schmittberger, R. & Schwarze, B. (1982). An Experimental Analysis of
Ultimatum Bargaining. *Journal of Economic Behavior and Organization*, 3(4),
367–388.

Holm, S. (1979). A Simple Sequentially Rejective Multiple Test Procedure.
*Scandinavian Journal of Statistics*, 6(2), 65–70. [*Not present in the framework
bibliography; volume and page details to be verified before submission.*]

Kelman, H.C. (1958). Compliance, Identification, and Internalization: Three
Processes of Attitude Change. *Journal of Conflict Resolution*, 2(1), 51–60.

Latané, B. & Darley, J.M. (1968). Group Inhibition of Bystander Intervention in
Emergencies. *Journal of Personality and Social Psychology*, 10(3), 215–221.

Le Texier, T. (2018). Debunking the Stanford Prison Experiment. *American
Psychologist*, 74(7), 823–839.

Milgram, S. (1974). *Obedience to Authority: An Experimental View*. Harper & Row.

Pratto, F., Sidanius, J., Stallworth, L.M. & Malle, B.F. (1994). Social Dominance
Orientation: A Personality Variable Predicting Social and Political Attitudes.
*Journal of Personality and Social Psychology*, 67(4), 741–763.

Ryan, R.M. & Connell, J.P. (1989). Perceived Locus of Causality and Internalization.
*Journal of Personality and Social Psychology*, 57(5), 749–761.

Singelis, T.M. (1994). The Measurement of Independent and Interdependent
Self-Construals. *Personality and Social Psychology Bulletin*, 20(5), 580–591.

Swann, W.B. Jr., Jetten, J., Gómez, Á., Whitehouse, H. & Bastian, B. (2012).
When Group Membership Gets Personal: A Theory of Identity Fusion. *Psychological
Review*, 119(3), 441–456.

Tyler, T.R. (2006). *Why People Obey the Law*. Princeton University Press.

Worchel, S. & Brehm, J.W. (1970). Effect of Threats to Attitudinal Freedom as a
Function of Agreement with the Communicator. *Journal of Personality and Social
Psychology*, 14(1), 18–22.

*The full bibliography of the framework, comprising 170 references, is given in
the theory specification accompanying this thesis.*

---

# Appendix A — Experimental Record

18,750 calls across 44 studies with frozen results; $22.24 accounted spend. The
principal studies:

| Study | Calls | Role |
|---|---:|---|
| `coordinate_sweep_r2` | 2,801 | eight-parameter sweep |
| `label_semantics_r2` | 2,241 | ID/LL swap controls; LL withdrawal |
| `label_semantics_r1` | 1,296 | PD swap control |
| `phase4b_grand_r1` | 901 | three-model variance decomposition |
| `phase4b_gpt_r2` | 840 | E/G/U on calibration model |
| `pd_prospective_r1` | 736 | prospective PD test |
| `phase4b_permutation_r2` | 736 | ten-label derangement control |
| `phase4b_profiled_r1` | 631 | E/G/U on second model |
| `id_crossmodel_r1` | 481 | ID cross-provider |
| `pd_crossmodel_r1` | 481 | PD cross-provider |

For each study the repository holds a protocol fixing the prediction before
collection, a hash-pinned release with the complete request schedule, the raw
per-call records, and an assessment reporting the outcome against the
prespecified rule.

# Appendix B — Items

All items share a framing paragraph:

> You hold the role described. The option you select will be carried out, not
> merely considered. Units are artificial simulator credits, stipulated equally
> valuable to every person, and all stated effects are certain and known to you.
> There are no hidden costs, benefits or later effects beyond those described,
> and no one is pressuring you toward either option. Decide on the situation as
> given.

Eight unique items were used; five appear on both models, one only on the second,
two only on the first. Each offers two options with tied totals of −3 units. The
complete text of every item, with payoffs and classifications, is reproduced in
the accompanying paper draft and generated directly from the frozen item pools.
