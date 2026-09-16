# Which Parts of a Prompt Carry Behaviour?

## Label-Semantic Controls for Parameterised LLM Agents

**Tommaso Piero Palamenga** — Bocconi University

*Draft, 18 September 2026. Every figure in this paper is traceable to a frozen
per-call record in the accompanying repository; designations are named inline so
each claim can be checked against its own assessment.*

---

## Abstract

Practitioners routinely condition large-language-model agents on structured
descriptions — personas, trait vectors, configuration blocks — and infer from a
behavioural change that the model has read the description as intended. That
inference is rarely tested. A numeric block that shifts behaviour could be acting
through its labels, through the mere presence of structured text, through
verbosity, or through numeric extremity anywhere in the prompt; these are
routinely conflated.

We present a method that separates them, and apply it to a ten-parameter encoding
of five political-ethical concepts. The method has three components: **pinning**
one coordinate to its endpoints while holding the other nine byte-identical;
a **label-swap control** that moves the identical numeral onto a coordinate
measured inert, holding the numeral multiset, block length and field order
constant; and a **replication gate** requiring the effect to reproduce before its
swap control is interpretable.

Across 18,750 frozen API calls we find: profiles change a deterministic
good/bad classification on two models from different providers (+0.171 and
+0.228 against an explicit-instruction control that does not reproduce the
effect); two of ten coordinates are load-bearing under Holm correction; and for
both, the effect belongs to the coordinate's **label** rather than to numeric
extremity — the same numeral on an inert label gives −0.036 and +0.046, both
non-significant.

The result we consider most informative is a failure. A third coordinate cleared
a Holm-corrected bar at 25 agents (−0.131, Holm 0.00082), then measured −0.014
(Holm 0.708) at 40 agents on the same model. Its post-hoc correlation had been
**+0.271**. Three measurements, three answers — positive, negative, null. The
replication gate caught it; without a TRUE arm, its null swap control would have
been read as evidence that its label carried the effect. We withdraw it.

We establish no moral improvement, no human resemblance, and no evidence that any
coordinate is *understood*. Every outcome label is computed deterministically
from stipulated transitions and never read from agent text. The contribution is
an identification method, a demonstration that it catches its own false
positives, and a bounded empirical map of where a ten-parameter encoding does and
does not operate.

---

## 1. Introduction

### 1.1 The inference everyone makes

A common pattern in LLM agent work: write a structured description of an agent —
a persona, a trait vector, a configuration — put it in the system prompt, observe
that behaviour changes, and conclude that the model is operating on the
description's *semantics*. The agent "has" high agreeableness; the agent "is"
process-oriented.

The behavioural change is usually real. The inference from it is usually
untested. At least four mechanisms produce the same observation:

1. **Label semantics** — the model reads `Procedural Dependence: 0.90` and
   behaves accordingly. The intended mechanism.
2. **Block presence** — any structured block changes behaviour, regardless of
   content. A framing or formality cue.
3. **Verbosity** — the profiled prompt is longer, and length alone shifts
   outputs.
4. **Numeric extremity** — the model responds to an extreme value *somewhere*,
   without binding it to its field.

These are not exotic alternatives. They are the default explanations, and
distinguishing them requires controls that most work does not run.

### 1.2 What this paper does

We treat this as an identification problem rather than an implementation one. The
question is not "can we build a parameterised agent" — that is easy and
uninformative — but "can we demonstrate *which component of the prompt* is
carrying the behaviour, and rule out the alternatives."

Our answer is a three-part method (§3), applied to a concrete ten-parameter
encoding of five political-ethical concepts (§2). The method's key property is
that **it can fail**, and in one case it did (§5.4). We regard that failure as
the paper's most transferable result.

### 1.3 Contributions

- **A one-binding swap control** that isolates label semantics from block
  structure, verbosity and numeric extremity simultaneously, by holding the
  numeral multiset identical and moving a single binding (§3.2).
- **A replication gate** making the swap control interpretable, and a
  demonstration of what happens without it (§5.4).
- **An empirical map** of a ten-coordinate encoding: two load-bearing, seven not,
  one withdrawn (§5).
- **Cross-provider replication** of both survivors, including a one-sided
  theory-derived prediction (§6).
- **A negative methodological finding**: AI design review returns contradictory
  verdicts on byte-identical material (§7.2).

### 1.4 What we do not claim

Stated here rather than buried in limitations, because the framing matters for
how the results should be read.

We do **not** establish that any agent behaves ethically, that outcomes improve,
that behaviour resembles humans, or that any coordinate is *understood* as a
concept. Every outcome label in this paper is a deterministic function of a
stipulated transition table, computed from the chosen action and never inferred
from agent text. "Good" is a defined predicate, not a moral judgment. We measure
whether a labelled number changes which action is chosen; we do not measure
whether the model represents the concept the label names.

---

## 2. Setup

### 2.1 The encoding

Agents are drawn as ten bounded parameters, each in [0,1], encoding five
political-ethical concepts (freedom, justice, authority, care, loyalty) operationalised
from psychological instruments:

| Code | Parameter | 0-endpoint | 1-endpoint |
|---|---|---|---|
| LL | Legitimacy Locus | external/institutional warrant | internal endorsement |
| CS | Constraint Sensitivity | low | high |
| RT | Response Threshold | tolerant | hair-trigger |
| MoR | Mode of Response | reflective | confrontational |
| RE | Relational Embedding | atomised | socially embedded |
| **PD** | **Procedural Dependence** | **outcome-dominant** | **process-dominant** |
| TfA | Tolerance for Asymmetry | egalitarian | hierarchical |
| **ID** | **Internalisation Dependence** | **surface compliance** | **genuine endorsement** |
| MS | Moral Scope | local/role-bound | universalised |
| AW | Affective Weighting | deliberative | intuitive |

Each is rendered as one line of a ten-line block in the system prompt, to two
decimal places. The two coordinates in bold are the ones that survive (§5).

The parameters are sampled from Beta marginals. A Gaussian copula couples them in
the general framework; the designations in this paper draw **independent Beta
marginals**, because each tests a single coordinate's effect with the other nine
held byte-identical between arms, so the dependence structure would introduce
correlated variation in held-constant fields without serving the question.

### 2.2 The decision task

Agents choose between two options in short workplace-resource vignettes. Each
item presents a claim under a stated arrangement: one option **keeps** the
arrangement, the other **overrides** it.

The critical design property is that **the payoff totals are tied**. On every
item both options net −3 stipulated units (one option: +1 gain, −4 loss; the
other: +2 gain, −5 loss). Welfare-maximisation, minimax and best-case seeking are
therefore **indifferent by construction**. This was established empirically:
`pd_discriminant_r2` tied the totals and the unprofiled choices did not move,
refuting an earlier designation's own welfare-based reading of the same items.

### 2.3 The outcome measure

Each action maps to a deterministic classification through a stipulated table:
a configuration-relative 8-vector (four negative categories, four positive) and a
fixed-standard 4-vector (harm, deception, coercion, unfairness avoidance). The
headline is a net score collapsing to `good` / `not_good`.

**This is computed from the chosen action identifier alone.** No model output is
interpreted, rated or scored. The measure is a lookup, which is what makes the
dependent variable immune to the interpretive drift that would otherwise attend
a "moral" outcome.

### 2.4 Screening before profiling

A task whose unprofiled answer is deterministic cannot show any arm difference.
Four nulls across three earlier phases traced to exactly this: in four of six
Phase 2 cells the unprofiled model chose identically across 400/400 calls.

Every item set used here is therefore **screened for baseline dispersion before
any profiled call**, on the model that will be used. Screening is on dispersion
only, never on outcomes; outcome-driven item selection is prohibited and was
explicitly refused once when it would have cut 40% of a budget (§7.3).

This is load-bearing rather than hygienic: `haiku_screen_r4` measured six
candidate items on `claude-haiku-4-5` and **all six returned modal share 1.00** —
fully deterministic, unable to show any effect. Those items were never run.

---

## 3. Method

### 3.1 Pinning

For coordinate C and agent a, two arms:

```
C-    a's drawn profile with C set to 0.10
C+    a's drawn profile with C set to 0.90
```

The other nine coordinates are drawn once per agent and held **identical**
between arms. The system prompts differ by exactly one line; the user text is
byte-identical. Contrasts are paired within agent and item.

Because both arms are equally profiled, a difference between them cannot be a
profile-presence effect, a verbosity effect, or a demand characteristic of being
profiled at all.

Verified at build time across every agent-item pair before any call: exactly two
diff lines, on the named coordinate, at the two levels, with byte-identical user
text.

### 3.2 The label-swap control

Pinning shows that *a coordinate* moves the outcome. It does not show that the
**label** carries it rather than numeric extremity. For that, take an inert
partner coordinate I and a level L:

```
TRUE(L)    L on C's label,          I's drawn value on I's label
SWAP(L)    I's drawn value on C,    L on I's label
```

Both arms carry the **identical multiset of numerals** across those two fields:
same block length, same line count, same ten numbers, same field order. Only
*which label holds L* differs.

This is the paper's central control. It holds constant, simultaneously:

- block presence (both arms carry the full block),
- verbosity (identical length),
- numeric extremity (the extreme value is present in both, just elsewhere),

and varies only the label-to-value binding. A TRUE effect with a null SWAP
localises the behaviour to label semantics.

**Choice of inert partner.** AW (Affective Weighting) is the only coordinate
measured inert by two independent methods: post-hoc correlation (r = −0.051 and
−0.167, both Holm 1.000) and prospective manipulation (−0.036, Holm 1.000).

**A precision trap.** The block renders two decimals. An agent whose drawn AW is
0.102 renders as `0.10` and collides with the LOW level, making TRUE and SWAP
byte-identical for that agent and diluting the paired contrast. Our first
degeneracy check tested the raw draw and missed it; it now tests **rendered**
precision and blocks rather than warns. Caught before collection; the population
seed was changed on a property of the draw alone, before any call.

### 3.3 The replication gate

A swap control is only interpretable if the effect it explains is present. We
therefore require, in the same designation and the same Holm family, that the
**TRUE arm reproduce the previously measured effect**. A coordinate whose TRUE
arm fails to replicate has an **uninterpretable** SWAP contrast, and nothing is
claimed for it.

This is not a formality. §5.4 reports a coordinate whose TRUE arm failed and
whose SWAP was null — a pattern that, without the gate, reads exactly like "the
label carries the effect."

### 3.4 Prespecification and the ledger

Every designation fixes in source, before any call: the question, the arms, the
primary test, the decision rule, the directional prediction (or its explicit
absence), the interpretation of each outcome, and a failure condition. These are
hashed into a frozen release alongside the full request schedule.

Calls run against a **write-once ledger** with exclusive locking, reservation
identity checks and source-hash pinning. Failures are preserved and **never
retried in place**: a lost call stays lost. Three such failures persist across
the record and are named in every designation that inherits them.

**Power is simulated against measured per-item baselines before collection**, not
against a uniform assumed effect. That distinction has teeth: one designation's
power check applied a uniform effect and reported 8/8; against the model's real
per-item baselines the true figure was ≤5/10, and the designation was abandoned
rather than run underpowered.

---

## 4. Do profiles change the outcome at all?

Before asking which coordinate matters, the prior question: does the profile
change the deterministic classification, and does an explicit instruction do the
same work?

Three arms: **U** (no profile), **G** (no profile, plus an explicit ethical
instruction in plain English), **E** (the numeric profile).

| Model | U | G | E | paired E−G | Holm |
|---|---:|---:|---:|---:|---:|
| `claude-haiku-4-5` | 0.367 | 0.429 | 0.600 | **+0.171** | **0.000112** |
| `gpt-5.4-mini` | 0.395 | **0.378** | 0.606 | **+0.228** | **≈ 0** |

The G arm states the target behaviour in plain English — weigh everyone's
interests, avoid harm, deception, coercion, unfairness. On the calibration model
it lands **below** the unprofiled baseline (−0.017, p = 0.712). The numeric
profile moves the headline; the instruction does not reproduce it.

E and G are byte-identical in participant text and differ only in the system
prompt, paired within agent and item. Prespecified same-item subgroup across both
models: **+0.255, p < 10⁻⁷**.

**The permutation control, and why it was insufficient.** An early control
deranged all ten labels — same ten numbers, scrambled across fields. It gave
E 0.564, P 0.475, U 0.400: a scrambled block does not clear baseline
(p = 0.122), a correctly-labelled one does (p = 0.00074), but the difference
between them is **+0.089 at pooled Holm 0.084** and **fails its prespecified
rule**.

We report this as a failure rather than a trend. It is also the direct motivation
for §3.2: deranging ten labels at once dilutes the effect across nine
non-load-bearing coordinates, so the control lacks power *by construction*. The
one-binding swap concentrates the manipulation where the effect is.

---

## 5. Which coordinates carry the behaviour?

### 5.1 The prospective test

PD was ranked first of ten in a post-hoc reanalysis, which explicitly flagged it
as requiring prospective test before any confirmatory language. Four prior
attempts reached the profiled stage **zero** times, each stopped by its own
dispersion screen.

`pd_prospective_r1` is that test. The direction was derived from the coordinate's
definition and locked in source before collection: PD is 0 = outcome-dominant,
1 = process-dominant; every item presents a claim under a stated arrangement; the
option that keeps the arrangement classifies `good`; therefore **PD+ produces more
`good` decisions than PD−**.

| Arm | Good-rate | n | vs U | p |
|---|---:|---:|---:|---:|
| PD− (0.1) | 0.382 | 280 | −0.041 | 0.431 |
| U | 0.423 | 175 | — | — |
| **PD+ (0.9)** | **0.729** | 280 | **+0.306** | **< 10⁻⁸** |

**Paired +0.346, pooled Holm ≈ 0, 6 of 7 items positive.** The entire
manipulation is one line of the prompt. `on_call` ran negative (−0.150) and is
reported rather than smoothed.

### 5.2 The label carries it

`label_semantics_r1` applies the swap control to PD, with AW inert:

| Arm | 0.9 sits on | Good-rate |
|---|---|---:|
| **TRUE+** | **Procedural Dependence** | **0.729** |
| TRUE− (0.1 there) | Procedural Dependence | 0.389 |
| SWAP+ | Affective Weighting | 0.557 |
| SWAP− (0.1 there) | Affective Weighting | 0.593 |

**TRUE +0.339 (Holm ≈ 0). SWAP −0.036 (Holm 1.000).** Four items survive Holm on
TRUE; **zero** on SWAP.

Move the identical number from one line to another and the effect vanishes. This
rules out block presence, verbosity and numeric extremity — extremity was held
constant and *moved*.

### 5.3 The sweep

`coordinate_sweep_r2` pins each remaining coordinate to its endpoints, 25 agents
× 7 items, Holm over all eight pooled contrasts as one family:

| Coordinate | Effect | Holm | Items | Load-bearing |
|---|---:|---:|---|---|
| **ID** | **+0.143** | **0.00056** | 6+/1− | **yes** |
| ~~LL~~ | −0.131 | 0.00082 | 0+/6− | *see §5.4* |
| TfA | −0.103 | 0.111 | 2+/5− | no |
| MoR | −0.097 | 0.069 | 1+/6− | no |
| MS | −0.069 | 0.292 | 2+/5− | no |
| RE | +0.046 | 0.906 | 4+/2− | no |
| RT | −0.023 | 1.000 | 3+/3− | no |
| CS | −0.017 | 1.000 | 3+/3− | no |

Seven coordinates are **not** load-bearing — a Holm-corrected null at adequate
power (24/24 simulated at d ≥ 0.20, 0/24 false positives), not an absence of
evidence.

### 5.4 The finding we consider most important: a coordinate that died

LL (Legitimacy Locus) cleared the sweep's bar with the most directionally
consistent result in it — negative in 6 of 6 items with any effect, zero
positive, Holm 0.00082.

`label_semantics_r2` then ran swap controls for both survivors, each with a TRUE
arm as a replication gate, 40 agents, Holm over all four contrasts:

| Contrast | Effect | Holm | Items | Reading |
|---|---:|---:|---|---|
| **ID:TRUE** | **+0.111** | **0.00467** | 5+/1− | replicates |
| ID:SWAP | +0.046 | 0.408 | 5+/2− | **null — label carries it** |
| LL:TRUE | **−0.014** | **0.708** | 4+/3− | **fails to replicate** |
| LL:SWAP | −0.046 | 0.408 | 1+/4− | **uninterpretable** |

LL across three measurements:

| Measurement | LL |
|---|---:|
| post-hoc correlation, unmanipulated | **+0.271** |
| pinned, 25 agents | **−0.131** (Holm 0.00082) |
| pinned, 40 agents | **−0.014** (Holm 0.708) |

**Positive, negative, null.** This is not a power failure: it failed on the
*larger* sample, with power 17/20 at an effect of the size previously measured.

**We withdraw LL.** Its status is **unresolved, not inert** — failing to
replicate is not the same as being measured flat, and we do not claim it is
inactive.

**Why this matters beyond one coordinate.** LL's SWAP was null. Had the swap
control been run *alone* — as it was for PD, and as would be natural — that null
would have read as "the label carries the effect," promoting a coordinate that
does not replicate. **The replication gate is the only reason LL was caught
rather than confirmed.** We therefore state as a design rule: *every swap control
must carry a TRUE arm that reproduces the effect it purports to explain.*

A coordinate can clear a Holm-corrected bar in a single well-powered designation
and still be noise.

---

## 6. Cross-provider replication

Every measurement to §5 was `gpt-5.4-mini`. Both survivors were re-tested on
`claude-haiku-4-5`, 40 agents, on that model's six dispersing items.

| Coordinate | gpt | haiku | p (haiku) | Items | Test |
|---|---:|---:|---:|---|---|
| **PD** | +0.346 | **+0.133** | **0.00031** | 4+/1− | **one-sided, theory-derived** |
| **ID** | +0.111 | **+0.075** | **0.0328** | 4+/2− | two-sided |

PD's is the stronger test: the direction was locked **one-sided** from the
coordinate definition, and the derivation's premise — that on every item the
arrangement-keeping option classifies `good` — is a property of the *item set*,
not the coordinate. It was therefore re-verified against the new items at build
time and **gated the release**. Only the direction transferred; never the
magnitude.

**Both effects shrink**: PD to ~38% of its gpt value, ID to ~68%. What replicates
is the **direction and the decision rule, not the magnitude**, and we make no
magnitude-stability claim.

**A correlation pointing at nothing.** PD's post-hoc correlation on haiku was
**+0.089** — near flat, and the basis on which this project had described PD as
"flat on haiku." Pinned, it gives **+0.133 at p = 0.0003**. Together with LL
(correlation +0.271, manipulation null), post-hoc correlations on unmanipulated
coordinates mislead in **both** directions. Only manipulation settles a
coordinate.

**Item sets differ by model, and that is forced.** Four of six haiku items
overlap gpt's seven. This is not a byte-identical repetition, and we report it as
such.

**Neither coordinate is *verified* cross-model.** No swap control ran on haiku:
a four-arm design quadruples the Holm family, and an underpowered TRUE arm would
render the SWAP arms uninterpretable *by construction* — manufacturing the LL
outcome by design. These results license "the coordinate moves the outcome on
haiku too," and nothing stronger.

---

## 7. What the process taught

### 7.1 The final map

| Coordinate | Pinned (gpt) | Swap control | Cross-provider | Status |
|---|---:|---|---:|---|
| **PD** | +0.339 to +0.346 | −0.036 n.s. | +0.133 | **verified label effect** |
| **ID** | +0.111 to +0.143 | +0.046 n.s. | +0.075 | **verified label effect** |
| ~~LL~~ | −0.131 → −0.014 | uninterpretable | not tested | **withdrawn, unresolved** |
| seven others | −0.10 to +0.05 | — | — | not load-bearing |

**Two of ten coordinates carry the behaviour, and for both the label carries the
effect.**

### 7.2 AI design review is not a stable instrument

Each designation introducing new materials passed an independent AI review gate.
The gate caught genuine errors: a reviewer-prompt mismatch, an answer-key leak in
a review packet, normative cues in option wording. Those catches were correct and
valuable, and drove a three-level authoring criterion (matched non-unit
consequence text; no asymmetric violation label; no asymmetric obligatory or
transgressive modals).

But the **verdict** is not a stable property of the material. One item pool was
reviewed on byte-identical content and returned **accept** (which then collected
956 decisions), **accept**, **accept**, **reject**. A second pool: four accepts
with zero blocking issues, then **revise** with two blocking issues on material
that had already grounded 631 collected decisions.

We adopted the rule that for already-accepted materials a review is **advisory** —
findings recorded and assessed, a reject does not stop collection — while new
materials remain hard-gated. Re-running a review to obtain a different verdict is
prohibited, and every verdict obtained is recorded, including those we proceeded
past.

Anyone using an LLM as a design gate should expect verdict instability and decide
in advance what a reject licenses.

### 7.3 Refusals that shaped the record

- **Outcome-driven item selection, refused.** Three of seven items showed
  |effect| ≤ 0.10 and never survive correction. Cutting them would have saved
  ~40% of a budget and would have biased a coordinate sweep toward coordinates
  behaving like PD. All seven were retained.
- **A designation abandoned on power.** A third model's items all sat within 0.12
  of a bound; a corrected power analysis gave ≤5/10 where an incorrect uniform
  one had given 8/8. It was not run.
- **An interpretation withdrawn.** `pd_discriminant_r1` concluded the model was
  welfare-following. `r2` tied the totals and the choices did not move, refuting
  it. r1 is marked superseded with its data intact.
- **A lost call never retried.** A network timeout at call 689 of 2,801 left a
  slot unresolved. It is preserved unresolved, named in every inheriting
  designation, and the 689 paid calls were not reused.

### 7.4 Two defects we shipped

Reported because the paper's claim is about method discipline.

**An empty analysis, twice.** Two designations dropped the dispersion screen (its
items already screened) but derived the analysis task list *from* that screen,
yielding an empty list and `None` for every contrast. All decisions were intact
and were rescored offline against the designation's own **declared** item set,
with the hash-pinned collectors left frozen. The second occurrence was inherited
from the first: we had fixed the symptom and not the collector. The third
designation built on it carries the fix at source and produced its own analysis.

**A power check against an assumed baseline.** Described in §3.4. Caught before
spending.

---

## 8. Limitations

Stated as constraints on what may be concluded, not as caveats.

**No moral claim of any kind.** Every outcome is a deterministic lookup from a
stipulated table. We measure which action is chosen, never whether it is good.
Nothing here says an agent behaves ethically or that outcomes improve.

**No human resemblance.** No human data was collected. This was the fourth of
four specified deliverables for the analysis phase and it is **unmet**, deferred
under a no-budget constraint. It is not retrospectively passed.

**No evidence of understanding.** A model responding to a value in a labelled
field in a predicted direction is weaker than representing the concept the label
names. Our swap control localises the effect to the label-to-value binding; it
says nothing about whether the binding is semantic.

**Narrow coverage — the principal limitation.** Seven items on one model, six on
the other; 25–40 agents per designation; one harness; one snapshot in time. All
items are workplace-resource vignettes with an identical tied-payoff structure.
Whether the method or the map generalises to other item families is **untested**.

**Item sets are not identical across models**, being constrained by which items
disperse on each.

**Two of ten coordinates, on these items.** The seven nulls are corrected nulls
on this item set at this n, not a claim of general inertness. TfA and MoR sit
just outside correction.

**Not verified cross-model.** §6.

**The configuration counterfactual was never run.** The framework names a
configuration-counterfactual difference as the primary discriminator for
training-data contamination. Every call in this paper used a neutral
configuration on all five axes. That control is absent.

**Separability is of the sampler, not the concepts.** Nine of ten principal
components are needed for 90% of variance (min eigenvalue 0.621) — a property of
the draw, not evidence that the concepts are distinct.

**A known contamination result bounds the framework.** A 500-probe screen,
dual-coded across providers with 500/500 agreement, found all five decanonised
benchmark variants identified at the canonical rate — 50/50 in every one of ten
cells. Structure-preserving domain substitution does not conceal a classic
paradigm from a frontier model.

---

## 9. Related work

*To be completed.* Positioning against: persona and trait-conditioning work in
LLM agents; prompt-sensitivity and format-effect literature; causal-mediation and
activation-patching approaches to localisation (which operate on internals where
we operate on inputs); behavioural-benchmark retrodiction; and the
machine-ethics-benchmark line from which the negative outcome categories derive.

The closest methodological neighbour is input-side ablation in prompt
sensitivity. Our contribution is the **numeral-identical swap**, which holds the
token multiset fixed while varying a single binding — a stricter control than
ablation, which necessarily changes length and content.

---

## 10. Conclusion

We asked which part of a structured prompt carries behaviour, and answered it for
a ten-parameter encoding: **two coordinates of ten, and for both the label rather
than the numeral.** Both replicate on a second provider; one with a theory-derived
one-sided prediction.

The result we would most want carried forward is the **withdrawal**. A coordinate
cleared a corrected significance bar with the most directionally consistent
result in its sweep, and dissolved on a larger sample of the same model. Its swap
control was null — the signature of a real label effect — and only the
replication gate distinguished the two cases.

Methods that can only confirm are weaker than methods that can kill their own
findings. We report one of ours dying.

---

## Appendix A — Scale of the record

18,750 API calls across 44 designations with frozen results, $22.24 accounted
spend. All per-call records are write-once with preserved failures; releases are
hash-pinned to their source; power simulations and offline rescorings are
reproducible from committed modules.

| Designation | Calls | Role |
|---|---:|---|
| `coordinate_sweep_r2` | 2,801 | eight-coordinate sweep |
| `label_semantics_r2` | 2,241 | ID/LL swap controls, LL withdrawal |
| `label_semantics_r1` | 1,296 | PD swap control |
| `phase4b_grand_r1` | 901 | three-model variance decomposition |
| `phase4b_gpt_r2` | 840 | E/G/U on calibration model |
| `pd_prospective_r1` | 736 | prospective PD test |
| `phase4b_permutation_r2` | 736 | ten-label derangement control |
| `phase4b_profiled_r1` | 631 | E/G/U on second model |
| `id_crossmodel_r1` | 481 | ID cross-provider |
| `pd_crossmodel_r1` | 481 | PD cross-provider |

## Appendix B — Prespecification

For each designation: the locked prediction object, its content hash, the
decision rule, the measured power table, and the build-time verification output.

## Appendix C — Items

Full participant text for all items, the stipulated transition tables, and the
three-level authoring criterion with the review stops that produced it.
