# Which Parts of a Prompt Carry Behaviour?

## Fields, Glosses and Stated Meaning in Parameterised LLM Agents

**Tommaso Piero Palamenga** — Bocconi University

*Draft, 22 September 2026. Every figure in this paper is traceable to a frozen
per-call record in the accompanying repository; designations are named inline so
each claim can be checked against its own assessment.*

> **Relation to the thesis.** This paper and the author's undergraduate thesis
> draw on one body of evidence and are separate documents. The thesis
> (`docs/thesis/LF3262767.pdf`, submitted and frozen) presents the ten-parameter
> encoding framework on evidence to 18 September 2026. **This paper is not a
> longer version of it.** It makes a narrower claim — that behaviour tracks the
> stated meaning of a prompt field — on a wider evidence base, and it reports
> results collected afterwards that *constrain* the framework the thesis
> presents: an invented field outperforms the verified parameter (§6.3), and that
> parameter does not behave as its name suggests (§6.4). Neither document is
> edited to agree with the other; see `docs/PROJECT_SPLIT.md`.

> **Status.** Section 10's citations are **verified** against their sources
> (`docs/paper/citation_verification.md`); two that did not exist were removed
> rather than replaced. The principal limitation, stated here and not deferred,
> is that every result comes from a single family of seven workplace-resource
> vignettes with tied payoffs.

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

**This is a methods demonstration on a single task domain, not a generalisation
claim.** Every result comes from one family of workplace-resource vignettes with
payoff totals tied by construction. That narrowness is what buys the
identification; it also bounds what may be concluded, and we make no claim that
the map transfers to other task families.

Across 35,542 frozen API calls we find: profiles change a deterministic
good/bad classification on two models from different providers (+0.171 and
+0.228 against an explicit-instruction control that does not reproduce the
effect); **one coordinate of ten is verified and one remains a candidate** under
Holm correction and a direct difference-of-differences; and for the verified one
the effect is **bound to the coordinate's labelled, glossed field** — the same
numeral on the partner field gives −0.036, and the partner field pinned in its own
right at 80 agents gives +0.016, 90% equivalence bound 0.050.

**What that does and does not exclude, stated here rather than in §9.** Holding
the block, its length and its numeral multiset identical excludes block presence
and verbosity *by construction*, and excludes *free-floating* numeric extremity by
inference. Two further mechanisms were open in an earlier version of this paper
and are now closed. **Position** — the two swapped labels sit at different lines,
so primacy over a numbered list would mimic the result — is excluded by the 2×2
control of §5.2. **Field-weighted extremity** — a model weighting an extreme value
by the salience of the field holding it, with no semantic reading — is excluded by
§6: exchanging only what the two ends of a scale are *said to mean*, holding the
name, the line, the numeral and the block's entire character multiset fixed,
**reverses** the effect. Extremity predicts every arm positive; two are negative.

We therefore claim that behaviour tracks the field's **stated meaning**, and still
disclaim understanding: §6.3 shows that four fields invented for the purpose, none
of them in the encoding, move choices as *their* explanations predict — one of them
more strongly than the verified parameter. Explanation-following is general, and
nothing here requires these ten parameters in particular.

The result we consider most informative is a failure. A third coordinate cleared
a Holm-corrected bar at 25 agents (−0.131, Holm 0.00082), then measured −0.014
(Holm 0.708) at 40 agents on the same model. Its post-hoc correlation had been
**+0.271**. Three measurements, three answers — positive, negative, null. The
replication gate caught it; without a TRUE arm, its null swap control would have
been read as evidence that its label carried the effect. We withdraw it.

**Scope, stated up front rather than deferred to limitations.** All results come
from a single family of short workplace-resource vignettes — seven items on one
model, six on the other — with an identical tied-payoff structure, and **no human
comparison of any kind was collected**. We establish no moral improvement, no
human resemblance, and no evidence that any coordinate is *understood*. Every outcome label is computed deterministically
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

1. **A field-bound label effect** — the behaviour depends on *which labelled
   field* holds the value, not merely on the value's presence. The intended
   mechanism, and the only one this paper can demonstrate. Note that this is
   weaker than semantic understanding: a purely associative mapping from the
   string `Procedural Dependence` to a behavioural disposition would satisfy it.
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

**Two constraints shape everything that follows, and we state them here rather
than in §9 so they frame the results rather than qualifying them afterwards.**

First, **the task family is narrow, and we therefore position this paper as a
methods demonstration on one domain rather than as a generalisable finding about
the ten coordinates.** Every item is a short workplace-resource vignette in which
a claim under a stated arrangement is either kept or overridden, with payoff
totals tied by construction (§2.2). Seven such items were used on one model and
six on the other.

That narrowness is not incidental — it is what the identification rests on. Tied
totals are what make welfare-maximisation, minimax and best-case seeking
indifferent by construction, and constructing them required items built to a
three-level authoring criterion that took five review stops to derive. A broader
item set would weaken exactly the property that makes the contrast interpretable.

The cost is external validity. **Whether the method or the map transfers to other
task families is untested**, and it is the most important open question about this
work. The contribution we claim is the method and the identification strategy; the
coordinate map is a demonstration that the method yields non-trivial results on
one domain, not a general claim about the encoding.

Second, **there is no human comparison**. No human data was collected at any
point. Nothing here speaks to whether these agents resemble people, and readers
should not supply that inference — the outcome measure is a stipulated lookup
(§2.3), not a behavioural standard calibrated against humans.

### 1.3 Contributions

- **A one-binding swap control** that isolates a *field-bound* label effect from
  block structure and verbosity by construction, and from free-floating numeric
  extremity by inference, holding the numeral multiset identical and moving a
  single binding (§3.2).
- **A replication gate** making the swap control interpretable, and a
  demonstration of what happens without it (§5.4).
- **An empirical map** of a ten-coordinate encoding: two load-bearing, seven not,
  one withdrawn (§5).
- **Cross-provider replication** of both survivors, including a one-sided
  theory-derived prediction (§7).
- **A negative methodological finding**: AI design review returns contradictory
  verdicts on byte-identical material (§8.2).
- **A reversal**: exchanging what a scale is *said to mean*, holding its name,
  line and numeral fixed, reverses the effect — excluding field-weighted
  extremity, the last mechanism an earlier draft could not rule out (§6.1).
- **A bound on the encoding**: fields we invented move choices as their glosses
  predict, one of them more strongly than the verified parameter (§6.3).

### 1.4 What we do not claim

Stated here rather than buried in limitations, because the framing matters for
how the results should be read.

**The central distinction in this paper is between a label-specific behavioural
effect and semantic understanding.** We demonstrate the former and explicitly
disclaim the latter. A *label-specific behavioural effect* means: the same numeral
produces a different behavioural change depending on which labelled field holds
it. That is a claim about binding, and it is what our controls test. *Semantic
understanding* would mean the model represents the construct the label names —
that `Procedural Dependence` functions because the model has something answering
to the concept of procedural dependence. **Nothing here tests that.** A model that
had learned a purely associative mapping from that string to a behavioural
disposition, with no conceptual content whatever, would produce every result we
report.

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
localises the behaviour **to the field binding** — it shows the effect depends on
which label holds the value. It does not show *why* the field matters, and in
particular does not distinguish a semantic reading of the label from a learned
association with that string.

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

Move the identical number from one line to another and the effect vanishes.

Two of the four candidate mechanisms are excluded **by construction** rather than
by inference: both arms carry the full block, so block presence cannot differ,
and both are byte-identical in length, so verbosity cannot differ. These are
design invariants, verified on the wire, not statistical conclusions.

The third is weakened but **not excluded**. Numeric extremity is *present* in both
arms — 0.9 appears either way — so a model responding to extremity per se would
respond equally to both. What remains possible is that extremity matters *more in
some fields than others*: a model might weight an extreme value by the salience of
the field it occupies, which would produce this pattern without any semantic
reading of the label. Our design cannot separate field-weighted extremity from a
label effect, and we do not claim it does.

**A fourth mechanism, and the control that excludes it.** In the rendered block
Procedural Dependence is line 6 and Affective Weighting is line 10, so the swap
above moves the label *and its position together*. A model weighting earlier lines
more heavily — an ordinary primacy effect over a numbered list — would produce the
entire result with no label reading at all. We did not name this in earlier drafts
and it was a genuine gap in the claim.

`position_counterbalance_r1` decomposes it with a 2×2 crossing the binding with
the line order. The block is re-rendered with the two entries exchanged, so the
level can sit on Procedural Dependence at line 10 and on Affective Weighting at
line 6; all four arms keep an identical numeral multiset, block length and line
count. 2,241 calls, 2,240/2,240 valid.

| Arm | Level on | At line | Effect | Holm | Items |
|---|---|---:|---:|---:|---|
| **A** | **Procedural Dependence** | **6** | **+0.393** | **≈ 0** | **7+/0−** |
| **C** | **Procedural Dependence** | **10** | **+0.271** | **≈ 0** | 5+/1− |
| B | Affective Weighting | 10 | +0.061 | 0.157 | 6+/1− |
| D | Affective Weighting | 6 | +0.004 | 1.000 | 3+/2− |

**The label factor is +0.300.** The decisive cell is D: it places the level at
line 6 — the privileged position under any primacy account — on the inert label,
and yields **+0.004**. A generic serial-position account predicts slot 6 lifts
whatever sits in it; D is the direct test and it fails.

**There is no position main effect, but there is an interaction.** Averaging
position across labels gives +0.032, and that average is the wrong summary:
position does opposite things on the two labels (+0.121 on PD, −0.057 on AW).
Decomposed, with 95% intervals from a paired bootstrap over all 280 agent-item
units:

| Term | Estimate | 95% CI |
|---|---:|---|
| Position main effect | +0.032 | [−0.025, +0.088] — includes zero |
| **Interaction** | **+0.089** | **[+0.030, +0.150]** |
| Position on the PD label (A − C) | **+0.121** | **[+0.046, +0.200]** |

Position modulates the *magnitude of an already-present label effect* rather than
acting on the value independently — which cell D rules out directly. The
decomposition was not prespecified and rests on one designation; we report it to
be replicated, not as an established magnitude.

What the design therefore establishes is that the effect is **bound to the label
string**. It does not establish that the binding is semantic — see §1.4 and §9.2.

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

## 6. Does behaviour track what the field *says*?

Sections 4 and 5 establish that the effect is bound to one labelled, glossed
field, and not to block presence, verbosity, free-floating extremity or line
position. They cannot say *what about the field* carries it. Three readings
survive, and they differ once the entry itself is edited:

- **MEANING** — the model reads what the scale is said to mean and acts on it.
- **NAME** — a learned association between the string "Procedural Dependence", a
  magnitude and a disposition; the gloss is decoration.
- **FIELD-WEIGHTED EXTREMITY** — an extreme numeral in a salient slot, no
  semantic reading anywhere.

### 6.1 Reversing the gloss reverses the effect

`semantics_r1` pins PD to 0.10 and 0.90 under four renderings of its own entry,
with the nine other entries, the items and the user turn byte-identical
throughout. 2,240 calls, 40 fresh agents, seven items.

| Variant | Entry reads | Gloss | Effect | 95% CI | Items |
|---|---|---|---:|---|---|
| CANON | Procedural Dependence | canonical | +0.3393 | [+0.2714, +0.4036] | 6+/1− |
| **FLIP** | **Procedural Dependence** | **ends exchanged** | **−0.1143** | **[−0.1786, −0.0500]** | 1+/5− |
| INVERT | Outcome Dominance | ends exchanged | −0.6143 | [−0.6714, −0.5536] | **0+/7−** |
| NONCE | Factor K | canonical | +0.1750 | [+0.1143, +0.2357] | 6+/1− |

The CANON arm is a replication gate and it holds: +0.3393 against +0.339 and
+0.346 in earlier designations, on a fresh population. Predictions were locked in
source before collection under a published content hash; they differ in **sign**,
which is what makes the design decisive rather than suggestive.

**FLIP is the decisive cell.** The name, the line, the printed numeral and the
block's entire character multiset are identical to CANON — the edit is a pure
exchange of two strings, verified as an involution — and the effect reverses.
Field-weighted extremity predicts every arm positive; two are negative. A pure
name-association account cannot produce +0.339 and −0.114 from an identical
printed name. Both are excluded.

FLIP also requires no human judgement that two wordings are equivalent. INVERT
does, and that premise is soft — this project has repeatedly found that reviewer
judgements about materials fail to predict model behaviour — which is why FLIP,
not the larger INVERT effect, carries the argument.

### 6.2 Name and gloss, separated

An earlier reviewer observed that every design here moves a label *together with*
its two-line gloss, so "label effect" had always meant the pair. The four arms
separate them:

- They **conflict** in FLIP (name says one thing, gloss the other) and partly
  cancel: −0.114.
- They **agree** in INVERT and compose: −0.614, the largest effect in the project.
- With the name removed entirely (NONCE), **about 52% of the effect survives**:
  +0.175 against CANON's +0.339.

The gloss dominates when the two disagree; the name contributes when they agree.

### 6.3 The same is true of fields we invented, which bounds the claim

If explanations are followed, the question becomes whether the encoding's
parameters are special or whether any on-topic glossed field would do. We wrote
four fields that are **not** in the encoding, placed each in the partner slot, and
pinned them identically. Signs were derived from each gloss and locked in advance;
one was written to point the *opposite* way.

| Probe field | Predicted | Effect | 95% CI | Items |
|---|---|---:|---|---|
| Status-quo Preference | + | **+0.4000** | [+0.3357, +0.4643] | 7+/0− |
| Stated-Wish Deference | + | +0.3071 | [+0.2536, +0.3607] | 7+/0− |
| **Numbers Count** | **negative** | **−0.2464** | [−0.3107, −0.1821] | 0+/7− |
| Worst-off Priority | + | −0.0643 | [−0.1286, 0.0000] | 2+/4− |

Two fields in the same slot, in the same format, carrying the same numerals, moved
choices in **opposite directions**, each as its own gloss predicted. This is a
second, independent demonstration of §6.1 — across fields rather than within one —
and it rules out any account on which a glossed field acts as a generic cue.

**It also bounds what the encoding can claim.** Status-quo Preference, written in
an afternoon and naming what these items are plainly about, reaches **+0.400
against the verified parameter's +0.339**, and is consistent on all seven items
where PD is 6+/1−. Nothing in our evidence requires *these ten parameters* in
particular. The honest description of what §5 verified is: **a glossed field whose
stated meaning bears on the items moves choices, and PD is one such field.**

One locked prediction failed, and it was ours. Worst-off Priority was derived
positive from the stipulated payoffs — the holder loses 5, more than anyone — and
came out −0.064, failing Holm and splitting across presentation orders. We claim
nothing for it. The failure is instructive in the same direction as the INVERT
caveat above: a designer's reading of what wording implies is not a reliable
predictor of what the model does.

### 6.4 What the parameter is *not* doing

On every item in this family, "process-dominant" and "keep the existing
arrangement" select the same option, so PD's effect is consistent with a
status-quo dial — a worry §6.3 sharpens, since an explicit status-quo field
outperforms it. We built items to separate the two: each vignette gained a matched
twin whose only difference was one clause stating that the holder came by the
arrangement outside its stated procedure.

Two screening designations (417 calls) failed to produce enough usable twins:
eleven wordings, from blatant to trivial, drove three items to an unprofiled floor
of 0.00–0.04, and others proved presentation-order determined. We report both
stops rather than the wordings that survived.

A one-directional test was possible on the floored twins, where the two readings
still diverge: a status-quo dial should lift the keep-rate off the floor, a
procedure-sensitive field should not. With Status-quo Preference as a positive
control, and both base arms reproducing as a gate:

| Lift on the floored twins | Estimate | 95% CI |
|---|---:|---|
| PD | +0.3833 | [+0.2917, +0.4750] |
| Status-quo Preference | +0.1333 | [+0.0583, +0.2083] |
| **Difference (SQ − PD)** | **−0.2500** | **[−0.3583, −0.1417]** |

**PD and a pure status-quo field dissociate** — the cleanest such result we have,
and a direct answer to the worry. But the dissociation runs *against* the reading
the parameter's name invites. Comparing each field's high arm across versions —
how much the holder's procedural lapse deters an agent already at that field's
maximum — a high-PD agent is **less** deterred than a high-status-quo agent
(tool_library: −0.30 against −0.50; rest_break: −0.15 against +0.05).

Whatever "Procedural Dependence: 0.90" does to this model, it is not *care that
the procedure was followed*. It behaves as a stronger and less discriminating
pressure to preserve the standing arrangement. **We claim no procedural-justice
interpretation of the parameter**, and this result is evidence against one. Two
items carry the comparison, one further twin being degenerate in all four cells
and retained rather than dropped.

### 6.5 The partner field, tested directly

Every swap control in §5 places the tested numeral on the entry of Affective
Weighting, treated as a field that does not itself carry the outcome. That rested
on a single by-product measurement. Pinned in its own right at 80 agents, AW is
flat: **+0.016, 95% CI [−0.027, +0.057], 90% equivalence bound 0.050** — the
tightest bound in the project, where seven coordinates certify only 0.20.

This supports the swap controls without proving them: they additionally assume
AW's entry is a *fair partner* slot, not merely that AW is quiet. §6.3 is
reassuring on exactly that point, since the same slot carried an invented field to
+0.400. The slot can carry an effect; AW's own gloss does not produce one.

The same designation gave Legitimacy Locus a fourth measurement: +0.271 post-hoc,
−0.131 at 25 agents, −0.014 at 40, **−0.036 at 80**, with the 80-agent interval
excluding the original. The withdrawal of §5.4 stands, and the protocol fixed in
advance that a further measurement would not overturn it by majority.

---

### 6.6 Can the field be read back from behaviour?

Everything above runs one way: a description is supplied and the model acts on it.
None of it separates *reading an explanation* from *following an instruction
phrased as an explanation*, which is the deflationary rival to every result in
this section. Inference runs the other way. We showed the model two transcripts
from the same agent — one produced at 0.10, one at 0.90 — and asked which agent
had the setting high, under three framings: the field named and glossed, named
only, and neither.

**The designation failed as an instrument and is reported for that reason.** The
model answered "B" in 94 of 120 trials, and in the named-only condition was
correct 0 times out of 19 when the answer was A. Accuracy therefore tracks a
positional bias, not inference, and the below-chance result in the unframed
condition (0.275) is that bias meeting an answer key that happened to run 19/21.
Nothing about bidirectionality is established in either direction.

We record the cause because it recurs. Randomising presentation order per trial
makes a position-following responder *visible* but does not *neutralise* it;
neutralising it requires each item shown in both orders, so that a content-free
responder scores chance by construction. That design was available and we did not
use it.

### 6.7 Do examples do what a rule does?

If the model holds a field as something more than text it is currently reading,
the natural test is whether the disposition can be *induced by examples* rather
than stated. We showed an agent five of its own previously recorded decisions —
no rule, no field name, no gloss — and measured behaviour on the provenance twins
of §6.4, items the examples never covered and on which they are silent, since
in the base items keeping the arrangement and respecting the procedure coincide.
Three arms: examples only, the principle stated outright, and the bare item.

Three controls were fixed in advance. The harness holds no conversational state,
so every cell is an independent call and withdrawn material is genuinely absent
rather than earlier in context. The read-out is a dimension the examples do not
state, so the outcome is not the quantity that defines the treatment. And the
examples are actual frozen decisions rather than idealised transcripts — no agent
in the source chose to keep on all seven items — since constructing clean examples
would be writing the rule the design is testing for.

| Arm | Keep-rate | vs bare item |
|---|---:|---:|
| bare item | 0.305 | — |
| **five of the agent's own prior decisions** | **0.734** | **+0.429** [+0.384, +0.473] |
| **the principle stated** | **0.768** | **+0.463** [+0.418, +0.507] |

Examples move behaviour substantially on items they never covered, in a direction
they never state. **An explicit principle moves it slightly more, and the gap is
+0.034 [+0.004, +0.064].** Examples very nearly reproduce what stating the rule
achieves.

**The test that would distinguish a fitted disposition from ordinary context did
not survive scrutiny.** If a boundary were being fitted to the examples, the shift
should track how many of the five examples leaned toward keeping. We prespecified
that the stated-principle arm *cannot* produce such a slope — its text is
identical for every agent — and that a slope there would void the measure. In the
first run the slope appeared in the stated-principle arm, because example
composition was confounded with agent index, which set presentation order. A
second run crossing order with the covariate moved the slope to the arm that can
carry it (+0.080 [+0.018, +0.137]) and left the other flat (−0.011), which is the
cleanest available confirmation that the first diagnosis was correct.

**It still does not support the claim.** Example composition, inherited from the
frozen transcripts, is badly unbalanced — 3, 4, 17 and 16 agents across the four
levels — and restricted to the 33 agents in the two populated levels the slope is
**−0.011 [−0.066, +0.046]**. Between the cells holding most of the data there is
no dose-response at all. A graded response is what a fitted disposition predicts;
a step separating seven sparse agents from everyone else is equally what a
small-sample artefact predicts, and this design cannot tell them apart.

We therefore report §6.7 as follows. Examples induce the behaviour almost as well
as stating the rule; nothing establishes that anything was *fitted* rather than
read; and the near-equality of the two arms, if anything, favours the reading on
which the model acts on whatever relevant text is in front of it — a rule, a
gloss, or a transcript of examples — without that text having become anything
else.

---

## 7. Cross-provider replication

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

**Item sets differ by model, and that is forced.** Five of six haiku items
overlap gpt's seven. This is not a byte-identical repetition, and we report it as
such.

**Neither coordinate is *verified* cross-model.** No swap control ran on haiku:
a four-arm design quadruples the Holm family, and an underpowered TRUE arm would
render the SWAP arms uninterpretable *by construction* — manufacturing the LL
outcome by design. These results license "the coordinate moves the outcome on
haiku too," and nothing stronger.

---

## 8. What the process taught

### 8.1 The final map

| Coordinate | Pinned (gpt) | Swap control | Cross-provider | Status |
|---|---:|---|---:|---|
| **PD** | +0.339 to +0.393 | −0.036 n.s.; direct diff **+0.375** [+0.286, +0.464] | +0.133 | **verified: bound to the field's stated meaning** (§6.1) |
| **ID** | +0.111 to +0.143 | direct diff +0.064 [−0.014, +0.146] | +0.075 | **candidate**: binding not established |
| **TfA** | −0.111 [−0.154, −0.066] | not run | not tested | moves the outcome; mechanism unidentified; item-dependent (2+/4−) |
| **MoR** | −0.073 [−0.116, −0.030] | not run | not tested | moves the outcome; mechanism unidentified; uniform (0+/6−) |
| ~~LL~~ | −0.131 → −0.014 → −0.036 | uninterpretable | not tested | **withdrawn, unresolved** (bound 0.073 at 80 agents) |
| AW | +0.016 [−0.027, +0.057] | — (it *is* the partner field) | not tested | flat; 90% bound **0.050** |
| RT, CS, MS, RE | −0.07 to +0.05 | — | — | not load-bearing at this n |

**Four of ten coordinates move the outcome on these items; for one the effect is
verified as bound to the field's stated meaning, and one is a candidate.** TfA and
MoR were measured only after this paper's first draft, at 80 agents rather than
25; they sit where PD sat before its swap control, and **no mechanism claim is
made for them**.

Two cautions belong with this table rather than after it. Counting movers is not
counting *concepts*: §6.3 finds a field invented in an afternoon moving these
items more than any coordinate here, so a mover is an instance of
explanation-following, not a vindication of the encoding. And the two bounds —
AW at 0.050 and LL at 0.073 — are the only entries in the project tight enough to
support "small if present" rather than merely "not detected".

### 8.2 AI design review is not a stable instrument

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

### 8.3 Refusals that shaped the record

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

### 8.4 Four defects we shipped

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

**A dispersion screen that passed items making no choice.** Screens are *unpaired*
— they count votes across independent calls with presentation order alternating.
An item that simply follows whichever option is printed first then averages to a
keep-share near 0.50 and passes a band rule designed to catch the opposite
condition. One of our screens returned a pass on two such items; a follow-up check
found both were order-determined, 25/25 in each direction. The same check found
that **two items in the main pool share this property** (keep-share gaps 0.75 and
0.73), unrecorded until now. No result in this paper is affected — every contrast
is paired within agent with order held fixed inside the pair, and each retains its
sign and magnitude within both orders — but the screen rule was wrong, and screens
now report keep-share by order. An earlier designation had checked order on
different items, found it irrelevant, and the check lapsed; it does not transfer
between item sets.

**The same defect a third time, in a covariate.** In §6.7 the agent index set
presentation order and, through the frozen transcripts it indexed, also the
composition of the examples shown: 14 of the 16 most keep-leaning agents fell in
one order. The prespecified dose-response then read order rather than examples,
and declared itself void by the criterion we had written for it — the slope
appeared in the arm whose text is identical for every agent. Crossing order with
the covariate fixed it. Three occurrences in one phase, each in a new disguise:
items, then a judge prompt, then a covariate. **Presentation order must be crossed
with anything that could correlate with it, not merely randomised.**

---

## 9. Limitations

Stated as constraints on what may be concluded, not as caveats.

**No moral claim of any kind.** Every outcome is a deterministic lookup from a
stipulated table. We measure which action is chosen, never whether it is good.
Nothing here says an agent behaves ethically or that outcomes improve.

**No human resemblance.** No human data was collected. This was the fourth of
four specified deliverables for the analysis phase and it is **unmet**, deferred
under a no-budget constraint. It is not retrospectively passed.

**No evidence of understanding, and the attempts to find some are reported.**
§6 shows behaviour follows what a field's gloss *says*, which is more than the
swap control alone established. It does not distinguish *reading an explanation*
from *following an instruction phrased as an explanation*. A field reading
"existing arrangements stand unless there is strong reason to change them" is
close to an instruction, and its success is what an instruction-following account
predicts.

Four designs were built to separate them and none succeeded. Defeasibility items,
on which a procedure-sensitive and a status-quo-preserving agent must diverge,
could not be built at all (below). Inference from behaviour failed as an
instrument (§6.6). And induction from examples (§6.7) produced behaviour within
0.034 of what stating the rule produces, with the measure that would show a fitted
disposition resting on seven agents. **The accumulated evidence is consistent with
a model that acts on whatever relevant text is in front of it — a rule, a gloss,
or a transcript of examples — and we report that as the reading our own attempts
failed to displace.**

**The parameters are not privileged.** §6.3 finds an invented field outperforming
the verified parameter on the same items. The evidence supports *glossed fields
whose stated meaning bears on the items move choices*; it does not single out this
ten-parameter encoding, and we do not claim it does.

**The verified parameter does not behave as its name suggests.** §6.4 finds a
high-PD agent *less* deterred by a holder's procedural lapse than a high
status-quo agent. We therefore attach no procedural-justice reading to the
parameter, and a reader should not import one from its name.

**Two designations failed to build their items, and are reported as failures.**
Seventeen wordings across two screens could not produce enough twins on which the
model splits; three items saturated to unanimous override, others proved
presentation-order determined. The defeasibility question stays open.

**Two items are presentation-order dependent.** `meeting_room` and `desk_booking`
are largely determined by which option is printed first (keep-share gaps 0.75 and
0.73). **No headline result is affected** — every contrast is paired within agent
with order held fixed inside the pair, and each retains its sign and magnitude
within both orders — but unpaired dispersion screens are invalidated by it, and
one of ours was. Screens must now report keep-share by order.

**Narrow coverage — the principal limitation.** Seven items on one model, six on
the other; 25–40 agents per designation; one harness; one snapshot in time. All
items are workplace-resource vignettes with an identical tied-payoff structure.
Whether the method or the map generalises to other item families is **untested**.

**Item sets are not identical across models**, being constrained by which items
disperse on each.

**Four of ten coordinates, on these items.** The remaining nulls are corrected
nulls on this item set at this n, not a claim of general inertness — and the
history here is cautionary in both directions. TfA and MoR sat just outside
correction at 25 agents and clear it comfortably at 80, while LL cleared it at 25
and dissolved at 40 and 80. Sample sizes chosen from budget rather than from
simulated power produced one false positive and two false negatives in the same
sweep.

**Not verified cross-model.** §7.

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

## 10. Related work

> **Citation status: verified.** Every reference below was checked against its
> source for existence, authorship, year, venue, and that the paper makes the
> claim attributed to it. Two supplied citations did not exist and were
> **removed rather than replaced**; four verified entries needed correction.
> The record is `docs/paper/citation_verification.md`. Two claims in this section
> are ours rather than the literature's — that field-level identification under
> byte-held surface form is scarce for closed models, and that the replication
> gate is not represented elsewhere — and both keep their hedges, since absence
> of evidence in a search is not evidence of absence.

The move this paper depends on is now visible across several literatures:
**treating a prompt not as a monolithic instruction but as a causal object with
separable components.** Our contribution sits at a specific gap in that movement.

### 10.1 Prompt conditioning and its sensitivity

Conditioning behaviour on prompt content is the foundational capability (Radford
et al. 2019; Brown et al. 2020), organised as a research programme by Liu et al.
(2021), with template and label-word choice made methodologically explicit by Gao
et al. (2021). Instruction tuning further changes how models follow zero-shot
prompts (Wei et al. 2021), and minimal zero-shot prompt changes can produce large
effects (Kojima et al. 2022).

That behaviour is also strikingly unstable under changes that preserve meaning.
Example ordering alone can move performance between near-random and
near-state-of-the-art (Lu et al. 2021); formatting alone can span dozens of
accuracy points with meaning held constant (Sclar et al. 2023); and broader
benchmarks find the same for wording, structure and punctuation (Razavi et al.
2025). Scale and instruction tuning do not reliably remove the brittleness
(Chatterjee et al. 2024). Mechanistic work on shared lexical task heads offers
one account of why superficially different prompts engage task representations of
differing strength (Yang et al. 2026).

**This literature is the direct motivation for our controls, and it is why the
obvious comparison is insufficient.** If format alone moves behaviour by that
much, observing that a structured profile moves behaviour tells us little about
the profile's content. It is also why our swap control holds block length, field
order and the complete numeral multiset constant rather than merely similar:
anything less sits within the range this literature shows to be consequential on
its own.

### 10.2 Label binding and what in-context labels actually do

The most directly relevant cluster concerns whether models use input-label
semantics as users assume. Min et al. (2022) report that randomising
demonstration labels barely degrades performance, arguing that label space, input
distribution and format are the operative drivers; Kim et al. (2022) find the
effect of correct mappings varies by configuration, with verbosity and model size
shaping robustness. Fei et al. (2023) identify domain-label bias as a systematic
failure mode, and a calibration line (Zhao et al. 2021; Jiang et al. 2023; Zhou
et al. 2023) shows these biases are measurable and correctable distortions rather
than noise.

**Two results bear directly on our interpretation, and they cut against the
strongest reading of our own finding.** Wei et al. (2023) show large models can
override semantic priors to perform in-context learning with semantically
unrelated labels, and Liu (2026) argues models can bind output to a demonstrated
token inventory regardless of semantic plausibility, with mechanistic evidence
for a label-slot effect.

If models can bind behaviour to arbitrary label strings, then a field-bound label
effect is **precisely what one would expect from a purely associative mechanism**
with no semantic reading. We take this as support for the restraint in §1.4
rather than as a problem: it is independent reason to claim field binding and
disclaim understanding. Our result is consistent with the model having learned an
association between the string `Procedural Dependence` and a behavioural
disposition, and that possibility is not one we can exclude.

### 10.3 Causal localisation, and why ours is the input-side analogue

Mechanistic interpretability localises behaviour to internal components, unified
theoretically under causal abstraction (Geiger et al. 2023). That work also
documents its own fragility: activation patching admits many hyperparameter
variants producing disparate results (Zhang & Nanda 2023), and patching estimates
may absorb hidden interaction effects rather than isolating single components
(Vaidyanathan et al. 2026).

Substantive accounts of in-context learning include induction heads (Olsson et
al. 2022), implicit gradient descent (von Oswald et al. 2022),
and implicit Bayesian inference, which explicitly notes mismatch between prompt
and pretraining distributions including formatting and delimiters (Xie et al.
2021). Function-vector work (Todd et al. 2023; Yin & Steinhardt 2025) and the
label-word anchoring result of Wang et al. (2023) are closest in spirit to ours —
the latter finds label words gather information in shallow layers and support
prediction in deep ones, a mechanistic counterpart to the field binding we
measure behaviourally. Recent work continues toward finer-grained causal
decomposition (Nam et al. 2025; Wang et al. 2026).

**Our method is the input-side analogue of this work:** the same interventionist
logic, applied to prompt fields rather than activations. The trade is explicit.
We gain applicability to closed models, where internals are unavailable, and we
lose resolution — we localise to a *field*, not to a circuit or a head. We also
avoid the patching-variant fragility above, since our intervention has no
hyperparameters: a field either holds a value or it does not.

### 10.4 Persona conditioning, and the gap this paper occupies

The persona literature establishes that structured role and trait prompts change
behaviour. De Araujo & Roth (2024) is the strongest comparison point, assigning
162 personas across seven models against both empty-persona and control-persona
baselines, and finding personas produce greater variability than controls. Han et
al. (2025) show trait prompting yields personality-aligned behaviour recognisable
to users, and Tang et al. (2026) extend this to facet-level steering while noting
that prompt-only persona signals dilute under long context and prompt noise.
Agent surveys frame prompt engineering as a central parameter-free optimisation
method (Du et al. 2025).

**This is where the gap is clearest.** These studies compare conditioned against
unconditioned arms. What is scarce is work isolating *which prompt field* carries
the effect under surface form held constant to the byte — and scarcer still for
closed models, where the mechanistic toolkit is unavailable. That intersection,
field-level causal identification through a closed-model prompt interface, is the
niche this paper occupies.

### 10.5 Moral and behavioural evaluation

Our outcome space is political-ethical, which brings in a further cluster. Rao et
al. (2023) formalise prompts as a composition of task, ethical policy and user
input, defining ethical consistency relative to the supplied policy — structurally
close to our E/G contrast, where an explicit policy statement fails to reproduce
what a parameter block achieves. Benkler et al. (2023) probe value pluralism
through demographic prompting at scale, and Sachdeva and van Nuenen (2025) compare
models against human judgements on everyday moral dilemmas, finding low
inter-model agreement despite moderate-to-high self-consistency, with model
judgements diverging substantially from the human evaluations.

**That last result bears on our §6 cross-model shrinkage.** If models disagree
substantially with one another on moral judgements, then a parameter effect that
replicates in direction across two providers while shrinking in magnitude is
roughly what should be expected, and we should resist reading the shrinkage as
evidence of a weak effect rather than of model heterogeneity.

### 10.6 Positioning

Against this literature our contribution is narrow and specific:

- **Relative to prompt-sensitivity work**, we hold surface form constant to the
  byte rather than approximately, using a numeral-identical swap in which the
  token multiset is fixed and a single binding moves.
- **Relative to label-bias work**, we manipulate the binding prospectively on a
  deterministic outcome measure rather than diagnosing bias post-hoc on accuracy.
- **Relative to mechanistic work**, we operate input-side on closed models,
  trading resolution for applicability.
- **Relative to persona work**, we identify which field carries the effect rather
  than establishing that a profile has one.
- **The replication gate** is the component we believe least represented
  elsewhere: requiring an explanatory control to carry a condition reproducing
  the effect it explains. The literature search did not surface a counterexample,
  though absence of evidence in a search is not evidence of absence.

## 10.7 Anticipated objections

Stated so the answers are fixed in the paper rather than improvised in a rebuttal.
Where the honest answer is a concession, it is recorded as one.

| Objection | Response |
|---|---|
| *"Why not test semantic understanding directly?"* | We do not, and we disclaim it. The paper demonstrates a **field-bound label effect** (§1.4). A purely associative mapping from the label string to a behavioural disposition, with no conceptual content, would produce every result here. Testing semantics needs a different instrument than input-side intervention. |
| *"How do you know it isn't verbosity or block structure?"* | Excluded **by construction**, not by inference: both arms carry the full block at byte-identical length with an identical numeral multiset, verified on the wire for every agent-item pair (§3.2). |
| *"Then it's just numeric extremity."* | **Partly conceded.** *Free-floating* extremity is excluded — the extreme value is present in both arms. **Field-weighted** extremity is not, and we say so in the abstract. Our design cannot separate it from a semantic reading. |
| *"LL cleared Holm correction. Why trust the gate?"* | That is the argument *for* the gate. LL cleared a corrected bar at 25 agents (−0.131, Holm 0.00082) and collapsed to −0.014 (Holm 0.708) at 40 — on the **larger** sample, with 17/20 power at the original effect. Its swap control was null, the signature of a real effect. Only the replication gate separated the two cases (§5.4). |
| *"Why only two models?"* | Budget. We claim **direction and decision-rule replication**, never magnitude stability — both effects shrink on the second provider (PD to ~38%, ID to ~68%), and §6 states this. |
| *"One vignette family is too narrow."* | **Conceded, and reframed rather than defended.** The paper is positioned as a methods demonstration on one domain (§1.2). Tied payoffs are what make the identification work; a broader set would weaken that property. Transfer is the most important open question. |
| *"The outcome measure is a lookup table, not morality."* | Correct, and deliberate. It removes rater noise and interpretive drift at the cost of ecological validity (§2.3, §9). We measure choices in a toy world exactly rather than behaviour in a rich world approximately. |
| *"A review returned* revise *on your own materials."* | Reported in §7.2 as a finding rather than hidden. Four prior reviews accepted the same byte-identical items with zero blocking issues. Both findings of the dissenting review are assessed in the designation's assessment; one describes the tied-payoff design correctly and reads it as a defect, and the other identifies an item that works *against* our result. |

## 11. Conclusion

We asked which part of a structured prompt carries behaviour, and answered it for
a ten-parameter encoding on one task domain. **One coordinate is verified and one
remains a candidate**; for the verified one the effect is bound to the labelled,
glossed field rather than to the numeral's presence, its position, or the block's
existence. Both replicate on a second provider; one under a theory-derived
one-sided prediction.

§6 sharpens that from a localisation to a claim about content. Exchanging only
what the two ends of a scale are *said to mean* — holding the name, the line, the
numeral and the block's character multiset fixed — **reverses** the effect, which
no account resting on extremity or name-association can produce. Behaviour tracks
the field's stated meaning.

The same sections bound what that is worth. Four fields we invented move choices
as their own glosses predict, one of them **more strongly than the verified
parameter**; so the finding is about glossed fields in general, not about this
encoding in particular. And the verified parameter turns out *less* sensitive to
whether a procedure was honoured than an explicit status-quo field is — it moves
behaviour reliably, but not in the way its name invites. We claim the method, this
demonstration of it, and these bounds; not a general property of the encoding, and
not understanding.

The result we would most want carried forward is the **withdrawal**. A coordinate
cleared a corrected significance bar with the most directionally consistent
result in its sweep, and dissolved on a larger sample of the same model. Its swap
control was null — the signature of a real field-bound effect — and only the
replication gate distinguished the two cases. It has since been measured a fourth
time, at 80 agents, and is null again.

§6.6 and §6.7 are the same discipline applied to the question we most wanted to
answer. Having shown that behaviour follows a field's stated meaning, the obvious
next claim is that the field has become something the model *holds* rather than
something it is reading. We built four designs to test that and report that none
of them established it: two could not produce usable materials, one failed as an
instrument through a defect of our own, and the fourth found that examples induce
the behaviour within 0.034 of what stating the rule achieves — a near-equality
that favours the deflationary reading rather than ours.

Methods that can only confirm are weaker than methods that can kill their own
findings. We report one finding dying, four designations that failed to establish
what they were built for, two locked predictions of our own that came out wrong,
a prespecified measure that voided itself, and a transport failure that closed a
designation we chose to re-designate rather than resume.


---

## Appendix A — Scale of the record

35,542 API calls across 55 designations with frozen results, $44.91 accounted
spend. One call is a preserved transport failure, never retried; the designation
it halted was closed and re-designated rather than resumed. All per-call records are write-once with preserved failures; releases are
hash-pinned to their source; power simulations and offline rescorings are
reproducible from committed modules.

| Designation | Calls | Role |
|---|---:|---|
| `coordinate_sweep_r2` | 2,801 | eight-coordinate sweep |
| `semantics_r1` | 2,240 | gloss reversal; extremity excluded |
| `probe_fields_r1` | 2,240 | four invented fields; architecture bound |
| `floor_lift_r1` | 2,240 | PD against a status-quo field on twins |
| `parameter_followup_r1` | 2,240 | AW and LL pinned at 80 agents |
| `parameter_followup_r2` | 2,240 | TfA and MoR pinned at 80 agents |
| `precipitation_r3` | 1,680 | examples vs a stated rule, order crossed |
| `precipitation_r2` | 840 | examples vs a stated rule, order confounded |
| `inverse_inference_r1` | 120 | inference from behaviour; failed as an instrument |
| `label_semantics_r2` | 2,241 | ID/LL swap controls, LL withdrawal |
| `label_semantics_r1` | 1,296 | PD swap control |
| `phase4b_grand_r1` | 901 | three-model variance decomposition |
| `phase4b_gpt_r2` | 840 | E/G/U on calibration model |
| `pd_prospective_r1` | 736 | prospective PD test |
| `phase4b_permutation_r2` | 736 | ten-label derangement control |
| `phase4b_profiled_r1` | 631 | E/G/U on second model |
| `id_crossmodel_r1` | 481 | ID cross-provider |
| `pd_crossmodel_r1` | 481 | PD cross-provider |

## Appendix B — Prespecification (repository supplement)

Not reproduced in full here. For each designation the repository carries, frozen
before collection: the `LOCKED_PREDICTION` object with its content hash, the
decision rule, the measured power table, and the build-time verification output.
These are in `code/phase5_*.py` and the per-designation `PROTOCOL.md`, with the
request schedule and source hashes pinned in each `release.json`.

## Appendix C — Items

The complete participant text for every item used in this paper, reproduced verbatim from the frozen pools. The shared framing paragraph is identical across all items and is printed once.

**Shared framing, prepended to every item:**

> You hold the role described. The option you select will be carried out, not merely considered. Units are artificial simulator credits, stipulated equally valuable to every person, and all stated effects are certain and known to you. There are no hidden costs, benefits or later effects beyond those described, and no one is pressuring you toward either option. Decide on the situation as given.

Of the 7 items used on `gpt-5.4-mini` and the 6 on `claude-haiku-4-5`, **5 overlap**. Items are marked with the models on which they were used.

### `desk_booking` — *gpt, haiku*

An office has one bookable desk left for the week. One person booked it and has said they want to keep the booking. Two visiting staff otherwise work from a corridor bench.

| Option | Text | Total | Classifies |
|---|---|---:|---|
| `KEEP_DESK` **(keeps arrangement)** | Leave the desk with the person who booked it. That person gains 1 unit; the two visiting staff lose 4 units between them. | -3 | `good` |
| `REASSIGN_DESK` | Give the desk to the two visiting staff. The two visiting staff gain 2 units between them; that person loses 5 units. | -3 | `not_good` |

### `storage_unit` — *gpt, haiku*

A community centre needs one more storage unit for winter supplies. One unit is leased by a resident who has said they want to keep it for the season. The supplies otherwise sit outdoors and part of them spoils.

| Option | Text | Total | Classifies |
|---|---|---:|---|
| `KEEP_LEASE` **(keeps arrangement)** | Leave the leased unit with the resident for the season. The resident gains 1 unit; the supply programme loses 4 units. | -3 | `good` |
| `RECLAIM_UNIT` | Use the leased unit for the winter supplies. The supply programme gains 2 units; the resident loses 5 units. | -3 | `not_good` |

### `tool_library` — *gpt, haiku*

A repair session needs a press that one member owns and has lent to the library under terms letting them withdraw it. They have said they want it back this week. Without the press three of the booked repairs cannot proceed.

| Option | Text | Total | Classifies |
|---|---|---:|---|
| `RETURN_PRESS` **(keeps arrangement)** | Return the press to its owner this week. The owner gains 1 unit; the booked repairs lose 4 units between them. | -3 | `good` |
| `HOLD_PRESS` | Keep the press at the library through this week. The booked repairs gain 2 units between them; the owner loses 5 units. | -3 | `not_good` |

### `on_call` — *gpt*

An on-call slot is unfilled for one night. One person already off-rota has said they want the night clear. Leaving it unfilled sends two callouts to a team an hour further away.

| Option | Text | Total | Classifies |
|---|---|---:|---|
| `LEAVE_UNFILLED` **(keeps arrangement)** | Leave the on-call slot unfilled for that night. That person gains 1 unit; the two callouts lose 4 units between them. | -3 | `good` |
| `ASSIGN_ON_CALL` | Put that person on call for the night. The two callouts gain 2 units between them; that person loses 5 units. | -3 | `not_good` |

### `meeting_room` — *gpt, haiku*

A meeting room is held for one group's weekly session. They have said they want to keep the slot. Two other groups have sessions that need the room this week and no alternative space of the size.

| Option | Text | Total | Classifies |
|---|---|---:|---|
| `KEEP_SLOT` **(keeps arrangement)** | Leave the weekly slot with the group that holds it. That group gains 1 unit; the two other groups lose 4 units between them. | -3 | `good` |
| `RELEASE_SLOT` | Give this week's slot to the two other groups. The two other groups gain 2 units between them; that group loses 5 units. | -3 | `not_good` |

### `rest_break` — *gpt*

A long shift has one mandatory rest slot left in the schedule. One worker has said they want to take it. Assigning it to a colleague instead lets two pending tasks finish inside the shift.

| Option | Text | Total | Classifies |
|---|---|---:|---|
| `KEEP_REST` **(keeps arrangement)** | Give the rest slot to the worker who asked for it. That worker gains 1 unit; the two pending tasks lose 4 units between them. | -3 | `good` |
| `REASSIGN_REST` | Give the rest slot to the colleague instead. The two pending tasks gain 2 units between them; that worker loses 5 units. | -3 | `not_good` |

### `weekend_rota` — *gpt, haiku*

A service needs one more person on Saturday. One member of staff has said they want that Saturday free. Without them the service runs reduced and two scheduled appointments are put back.

| Option | Text | Total | Classifies |
|---|---|---:|---|
| `KEEP_SATURDAY` **(keeps arrangement)** | Leave that member of staff off the Saturday. That member of staff gains 1 unit; the two appointments lose 4 units between them. | -3 | `good` |
| `ADD_TO_SATURDAY` | Put that member of staff on the Saturday. The two appointments gain 2 units between them; that member of staff loses 5 units. | -3 | `not_good` |

### `ward_transfer` — *haiku*

A ward is over capacity for the night. One patient has a single room and has said they want to keep it. Two patients are waiting on trolleys in the corridor. Moving the first patient frees the room for both.

| Option | Text | Total | Classifies |
|---|---|---:|---|
| `LEAVE_ARRANGEMENT` **(keeps arrangement)** | Keep the current room allocation for tonight. The patient in the room gains 1 unit; the two waiting patients lose 4 units between them. | -3 | `good` |
| `MOVE_PATIENT` | Allocate the room to the two waiting patients tonight. The two waiting patients gain 2 units between them; the patient in the room loses 5 units. | -3 | `not_good` |

**Note on the frozen modules.** Three collector modules record the overlap as
"four of six". That is an error of ours, corrected here and in the designation
assessments: the true overlap is **five of six**. The modules are hash-pinned by
their releases and are deliberately not edited, since altering them would
invalidate verification for every designation that inherits from them. The
discrepancy is recorded rather than silently reconciled.

**Authoring criterion.** Items were built to a three-level criterion derived from
five independent review stops: matched non-unit consequence text; no asymmetric
violation label; no asymmetric obligatory or transgressive modals. It is enforced
in code by `verify_items()` and items built to it cleared six consecutive review
gates with zero blocking issues.
