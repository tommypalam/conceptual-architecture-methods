---
title: "Which Part of a Prompt Carries Behaviour?"
subtitle: "Separating Names, Numbers, and Definitions in Structured Prompts"
author: "Tommaso Piero Palamenga^[Bocconi University. This preprint builds on research conducted for the author's undergraduate thesis, adding later experiments and robustness analyses while narrowing the claims about the original framework. Code, prespecified protocols, and analysis records: <https://github.com/tommypalam/conceptual-architecture-methods>.]"
date: "Preprint, September 2026"
abstract: |
  Structured profiles configure language-model agents through named traits, numerical values, and definitions. A behavioural change under such a prompt does not identify which field caused it or whether the model responds to the field's name, numerical value, or definition. We combine endpoint pinning, numeral-preserving swaps, position crossing, replication gates, and definition edits to distinguish these explanations without access to model internals. In a ten-field profile on seven allocation dilemmas, Procedural Dependence has a high-minus-low keep-rate effect 0.375 larger than its partner-field control. Exchanging its endpoint definitions while preserving its name, numeric values, and character inventory changes that effect from +0.339 to -0.114. The paired difference is +0.454, with a crossed agent-and-item bootstrap interval of [+0.179, +0.739], and has the same sign on all seven items. Replacing the name with a nonce label retains a positive effect; the name also contributes. Three of four invented fields move choices in their predicted directions, including opposite effects from two fields in the same slot. Follow-ups withdraw an earlier finding and expose limits to interpreting a field as the construct its name suggests. The strongest evidence concerns one model and one task family. It establishes sensitivity to the assignment of definitions to scale endpoints, not semantic understanding or a complete decomposition of the profile's effect. The contribution is a reproducible set of controls for auditing what structured prompts actually change.
---

## 1. Introduction

Structured prompts are often used as behavioural interfaces for language-model
agents: a persona, a configuration, or a list of named traits with numeric levels.
An interface may change decisions while failing to implement the distinctions
its designer intended. A field labelled for procedure, for example, could
increase respect for an existing arrangement without reliably distinguishing
whether that arrangement followed a procedure. Establishing that a prompt works
therefore leaves an identification problem: **which part changes behaviour,
and what does the change establish?**

Several explanations fit a difference between a profiled and an unprofiled
model. Adding a block changes its length and structure. Extreme numerals may
be salient. Field positions may matter. A familiar name may evoke a disposition
independently of its supplied definition. Prompt-sensitivity studies show why
such alternatives deserve controls [@lu2021fantastically; @sclar2023quantifying;
@razavi2025benchmarking]. A useful audit must vary the suspected cause while
preserving the competing features wherever the intervention permits.

We apply a sequence of such controls to a ten-field block and a family of
two-option allocation dilemmas. We first pin one field to low and high values,
then move the same numerals to a partner field, cross field identity with
position, and require the original effect to reproduce before interpreting its
control. Finally, we change the assignment of definitions to scale endpoints
while preserving the field's name and numeric values.

**The central result is a definition intervention.** For Procedural Dependence
(PD), exchanging the endpoint definitions changes the high-minus-low keep-rate
effect from +0.339 to −0.114. The direct difference, +0.454, is positive on all
seven items and remains positive under crossed agent-and-item resampling. The
reversal through zero is less secure across items than the difference itself.
Replacing the name with *Factor K* preserves a positive effect of +0.175, while
reducing it relative to the original. These results establish a contribution
from the definition's endpoint assignment and a contribution from the name;
neither a name-only account nor definition-insensitive numeric salience is
sufficient.

The rest of the evidence sets boundaries on that result. Three of four invented
fields move choices in the directions predicted from their definitions, including
opposite effects from two fields in the same slot. Other original fields also
have detectable pinned effects, so PD is not established as the profile's sole
cause. A previously significant field fails to replicate. Tests involving
procedural violations challenge the intended interpretation of PD but do not
establish an alternative construct. Examples and a prose principle also move
choices, leaving ordinary instruction and context following as viable explanations.

**Contributions.**

- **An experimental audit of addressable prompt fields:** endpoint pinning,
  numeral-preserving swaps, position crossing, replication gates, and definition
  edits, with explicit estimands and construction checks.
- **A controlled demonstration that endpoint definitions matter:** a
  prespecified direct contrast that changes no field name or numeric value and
  survives sensitivity analyses across the seven tested items.
- **A documented boundary between control and interpretation:** field names,
  initial significance, and a designer's predicted direction do not by
  themselves validate the intended behavioural construct.

The identification experiments use `gpt-5.4-mini`; a second provider is tested
for first-stage pinning only. The contribution is a bounded experimental case
study and reusable audit design. We do not infer understanding, moral quality,
human resemblance, or generality beyond the tested task family.

## 2. Related work

**Prompt sensitivity.** Surface form matters. The order of in-context examples
can move performance from near chance to near the state of the art
[@lu2021fantastically]. Formatting alone spans large accuracy ranges with meaning
held constant [@sclar2023quantifying], and even slight reformulations can make answer quality difficult to predict
[@razavi2025benchmarking]. Increasing scale or applying instruction tuning does not necessarily reduce
prompt sensitivity [@chatterjee2024posix]. These results motivate preserving
all prompt bytes outside the intended intervention. Definition edits still
change word order and endpoint association; they do not hold every aspect of
surface form constant.

**Do models use what prompts mean?** @webson2022prompt found that prompt-based
models could learn as fast from irrelevant or misleading templates as from
instructive ones, and @min2022rethinking that randomly replacing demonstration
labels barely hurts in-context performance. Large models can override semantic
priors to learn from semantically unrelated labels [@wei2023larger], and output
can bind to a demonstrated label inventory regardless of plausibility
[@liu2026incontext]. These results are deflationary about semantic reading, and
we take them seriously. Our setting differs: a current instruction-tuned model
makes a zero-shot choice, and the manipulated text is a definition, not a
template or a label. Here the assignment of a definition to the scale's endpoints changes the
measured effect (§6). What remains open is *why* it does. Our evidence is
consistent with the model treating a definition as an instruction (§6.4, §9).

**Persona and profile conditioning.** @luzdearaujo2025helpful compare 162
personas across seven models against an empty persona and 30 paraphrases of "a
helpful assistant", and find more variability under personas than under the
control. @zheng2024helpful find that personas in system prompts do not reliably
improve performance on objective tasks, and that the effects of particular
personas are hard to predict. These comparisons motivate a complementary question: once conditioning
changes behaviour, which component of a multi-field block contributes? We study
within-block interventions that preserve the surrounding profile and task. Our
contribution is their combined application to field identity, position, and
endpoint definitions, rather than a claim to introduce controlled prompt
comparisons in general.

**Causal localisation.** Mechanistic interpretability localises behaviour inside
the model through patching, mediation and tracing, unified as causal abstraction
[@geiger2023causal]. It has well-documented sensitivities to the choice of
intervention [@zhang2023towards] and to hidden interactions between mediators
[@vaidyanathan2026curse]. Label words have been found to act as anchors that
gather information in shallow layers [@wang2023label]. Our interventions operate on prompt fields rather than activations. They
identify effects of input changes, not internal mediators, and require no access
to weights. On an open model, the same prompt pairs could define contrasts for
a subsequent internal analysis; no circuit-level explanation is established here.

**Moral-choice evaluation.** We borrow a task framing from work on in-context
ethical policies [@rao2023ethical], but we measure only which option is chosen.
@sachdeva2025normative report low agreement between models on everyday moral
dilemmas despite moderate-to-high self-consistency. That is one reason not to
expect effect sizes to transfer across providers (§5.6).

## 3. Setup

### 3.1 Models and calls

The identification work (§5.1–5.5, §6) uses `gpt-5.4-mini-2026-03-17`
(temperature 1, reasoning disabled). Cross-provider tests use
`claude-haiku-4-5-20251001` (temperature 1). Each call is one system prompt and
one user turn, with no conversational state. The model returns a JSON object
naming an option. Output caps were 1,536 tokens in earlier designations and 256
in later ones, since the longest reply observed in 2,240 calls was 21 tokens. A
reply that fails to parse is preserved as a failure and never retried.

### 3.2 Items

Each item is a short allocation dilemma in which one party holds an arrangement
(a desk booking, a leased storage unit, a weekly meeting slot) and has said they
want to keep it, while others would benefit from overriding it. One option
**keeps** the arrangement and one **overrides** it. A shared framing states that
all effects are certain, that units are artificial and equally valuable to
everyone, and that no one is applying pressure. An example:

> *An office has one bookable desk left for the week. One person booked it and
> has said they want to keep the booking. Two visiting staff otherwise work from
> a corridor bench.*
>
> `KEEP_DESK`: Leave the desk with the person who booked it. That person gains 1
> unit; the two visiting staff lose 4 units between them.
>
> `REASSIGN_DESK`: Give the desk to the two visiting staff. The two visiting
> staff gain 2 units between them; that person loses 5 units.

**Payoff totals are tied by construction.** Both options sum to −3 on every
item, so maximising the stated aggregate payoff does not select between them.
This does not make their distributions equivalent: worst-off, inequality, and
group-size considerations can still favour one option. The tie removes an
aggregate-payoff advantage, not all numerical reasons for choosing. Items were
written to an authoring criterion of matched consequence text, no asymmetric
violation labels, and no asymmetric obligation words, checked in code. These
checks constrain wording; they do not establish neutrality under every reading.
Appendix B reports the stimuli and item membership.

The main identification studies use seven items on `gpt-5.4-mini`; the initial
profile-versus-guidance comparison uses eight. The second provider uses six,
five shared with the seven-item set. Item pools were screened for variation in
unprofiled choices before the corresponding profiled tests. This selects a
restricted task population. A deterministic baseline still permits movement in
one direction, as the later floor-lift test demonstrates (§6.3). Within a
designation, no item was removed after inspecting its profiled result.

### 3.3 Outcome

The outcome is **keep-rate**: the share of decisions choosing to keep the
arrangement. It is read from the option identifier alone, and no model text is
interpreted. (The project's frozen classification table labels the keep option
`good` and the override option `not_good`. Since that label is a fixed function
of the choice, we report the choice directly and attach no moral reading to it.)

### 3.4 The structured block and the agents

The system prompt carries a ten-field block. Each field is rendered as a name, a
value in [0, 1] to two decimals, and a two-line definition of the scale's ends:

```
 6. Procedural Dependence: 0.90
    (0 = outcome-dominant; results matter, methods are secondary;
     1 = process-dominant; fair procedure matters independently)
```

The ten fields come from an encoding of political-ethical concepts developed in
the author's thesis. Their provenance is not this paper's subject. What matters
is that they are **addressable fields with stated meanings**, which is what the
controls operate on. An **agent** is one draw of the ten values from independent
Beta distributions. The same agent appears in every arm of a designation, so all
contrasts are paired within agent and item. Here an agent is a matched prompt profile, not an independently trained model
or a persistent entity. A designation is a separately specified experimental
run. Designations use 40 agents unless stated (25 in the initial sweep, 80 in
follow-ups). Appendix A reproduces a full system prompt. The estimates average
over these background profiles; they do not establish invariance to other
profile distributions or to interactions among fields.

## 4. Method

### 4.1 Pinning

To test field *F*, set *F* to 0.10 in one arm and 0.90 in the other, keeping the
other nine values as drawn for that agent. The two system prompts differ on
exactly one line, verified byte for byte for every agent before any call, and
the user turn is identical. The **effect** of *F* is the paired difference in
keep-rate, 0.90 minus 0.10.


Writing $Y_{ai}(v,l)$ for the binary keep response for profile $a$, item $i$,
rendering $v$, and level $l$, we estimate

$$
\widehat e_v = \frac{1}{AI}\sum_{a=1}^{A}\sum_{i=1}^{I}
\left[Y_{ai}(v,0.90)-Y_{ai}(v,0.10)\right].
$$

The swap estimand is $\widehat e_{\mathrm{TRUE}}-\widehat e_{\mathrm{SWAP}}$;
the definition estimand is $\widehat e_{\mathrm{CANON}}-\widehat e_{\mathrm{FLIP}}$.
Both are computed from within-profile, within-item differences, preserving the
pairing across all relevant arms. Where both option orders are observed, their
differences are averaged within that cell for the crossed robustness analysis.

### 4.2 The swap control

Pinning estimates the effect of a numeric change within a particular field.
It does not separate the field identity from the presence of an extreme value. The
swap control uses a partner field *P* and a level *L*:

```
TRUE(L)   L on F,                  P's drawn value on P
SWAP(L)   P's drawn value on F,    L on P
```

At each level, TRUE and SWAP contain the same multiset of ten numerals and
preserve the field order, definitions, and character count. Two numerals change
their assignment to fields; their order in the rendered block is not preserved. Block presence, length and the presence of an
extreme numeral are held fixed **by construction**. Only which field holds the
value differs. The quantity of interest is the within-unit difference of
differences, TRUE effect minus SWAP effect, with its own interval. We never infer
a difference from one arm being significant and the other not
[@gelman2006difference].

Two refinements matter. Values are compared **at rendered precision**: a drawn
partner value of 0.102 prints as `0.10` and would make TRUE and SWAP identical for
that agent, so degeneracy is checked on the rendered prompt. The direct contrast estimates differential sensitivity between the two
fields. Interpreting the partner as a negative control additionally requires
evidence that its effect is small in this setting (§5.4).

### 4.3 The replication gate

To interpret a swap as explaining an earlier effect, we require the TRUE arm
to reproduce that effect in the same designation. A null SWAP alone cannot
validate an effect that failed to replicate. The direct TRUE-minus-SWAP
contrast remains an estimable quantity; the gate limits the explanatory claim
we attach to it. §5.5 shows why this distinction matters.

### 4.4 Line crossing and definition edits

Because the tested and partner fields sit on different lines, a primacy effect
over a numbered list could mimic a field effect. A 2×2 design crosses *which field
holds the value* with *which line it occupies*, by re-rendering the block with the
two entries exchanged (§5.3). To ask what about the field matters, we edit the
field's own entry while holding the other nine entries and the user turn fixed
(§6.1).

### 4.5 Analysis and prespecification

Before collection, each designation fixes its question, arms, primary test,
decision rule and any directional prediction, and records them in source under a
content hash that is checked at dispatch. Primary tests are paired exact sign
tests with Holm correction [@holm1979simple] over the designation's family, plus a requirement of directional consistency across items. The later designations (§6) also use decision rules based on unit-bootstrap
intervals; their specific gates and directional predictions are preserved in
the corresponding protocols. Intervals are 95%
percentile bootstraps over agent-item units (10,000 resamples). Power simulations used measured per-item baselines and assumed effect sizes;
they do not guarantee detection or account for all sources of item heterogeneity.
Holm corrections apply within a designation, not across the whole adaptive
research programme. Bootstrap intervals are pointwise, not simultaneous. Failed calls are preserved and
never retried, and a designation halted by a failure is closed and re-designated
rather than resumed.

**Item-level robustness.** Unit-level intervals treat the items as fixed. With
seven items, generalisation to other items of the same kind is a separate
question. For the principal field and conditioning contrasts we also report, after the fact and
without further calls, (a) a **crossed bootstrap** that resamples agents and items
independently, and (b) a one-sample *t*-test over the per-item effects, with
items as the unit. With so few items these analyses have uncertain coverage.
The unit bootstrap does not preserve dependence across items sharing a profile;
the crossed bootstrap addresses both grouping dimensions. Neither resampling
scheme makes these selected items representative of a broader population. The
item-level tests are sensitivity checks, not replacements for the prespecified
tests, and disagreements are reported. For the §5.1
contrasts we also report crossed random-effects logistic models with an
item-specific treatment slope [@barr2013random], fitted in the thesis. Appendix C
has the full table.

## 5. Which field carries the behaviour?

### 5.1 The profile changes choices relative to generic guidance

Three arms: no block (U), a one-paragraph ethical instruction in place of the
block (G), and the full numeric block (E).

| Model | U | G | E | E − G | Holm | Item CI |
|:------------------------|----:|----:|----:|------:|------:|:-----------------|
| gpt-5.4-mini, 8 items | 0.395 | 0.378 | 0.606 | **+0.228** | $<0.001$ | [+0.091, +0.372] |
| claude-haiku-4-5, 6 items | 0.367 | 0.429 | 0.600 | **+0.171** | 0.000112 | [−0.025, +0.362] |

: Keep-rates by arm. *Item CI* is a two-stage bootstrap over items, then units, for E − G (from the thesis analyses).

The instruction reads: *"Weigh the interests of everyone affected. Avoid causing
harm, avoid deceiving anyone, avoid coercing anyone, and treat people with
equivalent claims equally. Where these cannot all be satisfied, decide which
matters most in this situation and act on it."* No change relative to U is detected on
`gpt-5.4-mini` (−0.017 against U, p = 0.712), while the block moves it by about
0.2 on both models. On `haiku` the item-level interval includes zero, although a
mixed model with item slopes gives p = 0.041.

This comparison motivates the rest of the paper, and it should not be read as
"numbers beat prose". The instruction does not say anything about keeping or
overriding arrangements, so it is not matched in meaning to the block. §6.4 shows
that a one-sentence on-topic prose principle also produces a large change,
on a different item version. That is not a matched effect-size comparison. The question is what in the block does the work.

### 5.2 PD responds differently from its partner field

An offline reanalysis of earlier data ranked Procedural Dependence (PD) first of
the ten fields. That ranking was post hoc, so PD was tested prospectively, with
the direction derived from the field's definition and locked before collection.
Pinned, PD moves keep-rate by **+0.346** [+0.275, +0.414] (Holm < 0.001; 6 of 7
items positive).

The swap control used Affective Weighting (AW) as the partner. With the numeral on
PD the effect is +0.339. With the identical numeral on AW it is **−0.036**
(Holm 1.000). The within-unit difference is **+0.375 [+0.286, +0.464]**, and it
survives resampling items (crossed CI [+0.082, +0.661]; item-level *t* p = 0.046).
No effect is detected when the same numeral is varied on the partner. The
direct difference supports field-specific sensitivity, not an exact zero for
the partner or a decomposition of the full profile-versus-baseline effect.

A second field, Internalisation Dependence (ID), moved keep-rate when pinned
(+0.111 to +0.143), but its difference against its swap control is +0.064
[−0.014, +0.146]. We report ID as a **candidate**, not a verified field effect.
An earlier reading, "ID's TRUE arm is significant and its SWAP arm is not, so the
field carries it", was the significance-versus-non-significance inference, and we
withdrew it.

### 5.3 The field effect persists at both tested positions

In the block, PD is line 6 and AW is line 10, so the swap moved the value's field
and its line together. The 2×2 separates them (40 agents, all four arms with
identical numeral multisets and lengths):

| Cell | Value on | At line | Effect | Holm | Items +/− |
|---|---|---:|---:|---:|---|
| A | PD | 6 | **+0.393** | $<0.001$ | 7 / 0 |
| C | PD | 10 | **+0.271** | $<0.001$ | 5 / 1 |
| B | AW | 10 | +0.061 | 0.157 | 6 / 1 |
| D | AW | 6 | +0.004 | 1.000 | 3 / 2 |

The field factor, (A + C − B − D)/2, is **+0.300** [+0.232, +0.370] (crossed CI
[+0.111, +0.495]). The position factor is +0.032 [−0.025, +0.088]. Cell D is the
direct test of a primacy account. It puts the value at line 6 on the partner
field and gives +0.004. Position is not irrelevant, though. It **modulates** the
field's effect (A − C = +0.121 [+0.043, +0.200]; interaction +0.089 [+0.030,
+0.150]), a decomposition that was not prespecified.

### 5.4 The partner field, tested directly

Pinned independently at 80 agents, AW has a small estimated effect: **+0.016** [−0.027, +0.057], with a 90%
symmetric bound of 0.050. This is the smallest symmetric interval containing
the pointwise 90% unit-bootstrap interval, calculated after collection and
conditional on the tested items; it is not a prespecified equivalence margin. That supports the
controls but does not prove the partner's *slot* is a fair comparison. §6.2 bears
on this: an invented field placed in the same slot reached +0.400. The slot can
carry an effect. The small average AW effect supports its role as a partner
on these items, without establishing that AW is inactive in every context.

### 5.5 A field the method withdrew

Legitimacy Locus (LL) had a post-hoc correlation with keep-rate of **+0.271** on
unmanipulated profiles. In the initial sweep (25 agents, Holm over eight fields)
it cleared correction with the most directionally consistent result of any field:
**−0.131** (Holm 0.00082; six negative items and one tie). In a designation with a
replication gate (40 agents), its TRUE arm gave **−0.014** (Holm 0.708), and at
80 agents it gave −0.036 [−0.080, +0.009]. The three measurements gave three
answers: positive, negative and null.

The later estimates do not reproduce the original effect. Simulated power of
17/20 at its initially measured size does not rule out a missed effect, and that
initial size may itself be overestimated. We withdraw the initial claim rather
than classify the underlying effect as exactly zero. The 80-agent pointwise
90% unit-bootstrap interval fits inside ±0.073, a post-hoc bound conditional on
these items. The positive correlation and negative intervention estimate also
answer different questions: association in randomly drawn profiles did not
predict the pinned effect's sign.

**LL's SWAP arm was null, but the replication gate failed.** Reading the null
control alone as validation would have concealed that failure. The lesson is to
reproduce the target effect alongside its control and estimate their difference.

Tolerance for Asymmetry and Mode of Response show a different pattern: neither
survived the eight-field Holm correction at 25 agents, but both survived their
two-field follow-up correction at 80 (−0.111 and −0.073; Appendix C). Both sample
size and correction family changed. MoR remains negative under item resampling;
TfA does not. These are additional pinned effects with no swap controls, not
proof that PD is the only active field. The sequence demonstrates changing
evidential strength, not known counts of false positives and false negatives.

### 5.6 A second provider

PD and ID were pinned on `claude-haiku-4-5` over its own six screened items. PD's
direction was again locked one-sided from its definition, after re-verifying that
the derivation's premise held on the new items. PD gave **+0.133** (p = 0.00031;
4/1 items) and ID **+0.075** (p = 0.033). Both effects shrink, to about 38% and 68%
of their `gpt` values. These are descriptive ratios across partly different
item sets, not estimates of a pure provider effect. At item level PD's interval is borderline (crossed CI
[−0.013, +0.283]; item bootstrap [+0.008, +0.267]; *t* p = 0.076), and ID's
includes zero. No swap control was run on `haiku`. These results show that pinning
PD moves the outcome on a second provider in the predicted direction, and nothing
more.

## 6. What about the field carries it?

§5 establishes PD's differential sensitivity relative to AW and its persistence
at both tested positions. Block presence, character count, a free-floating
numeral, and a position-only account cannot by themselves explain those
contrasts. Three restricted explanations motivate the next intervention:

- **Definition sensitivity:** behaviour changes when the meanings assigned to
  the scale endpoints change.
- **Name-only association:** the field name and value drive behaviour, with no
  contribution from the endpoint definition.
- **Definition-insensitive salience:** an extreme number acts through a salient
  field or slot regardless of the endpoint text.

These are testable alternatives, not an exhaustive taxonomy of model mechanisms.

### 6.1 Exchanging the definition's ends

`semantics_r1` pinned PD under four renderings of its entry, with the nine other
entries and the user turn byte-identical, on 40 new agents. Predictions were
locked under a published hash and differ in sign across explanations.

| Variant | Line 6 reads | Definition | Effect | 95% CI (units) | Items +/− |
|:-------|:----------------------|:---------------|-------:|:-----------------|:------|
| CANON | Procedural Dependence | as original | +0.339 | [+0.271, +0.404] | 6 / 1 |
| FLIP | Procedural Dependence | ends exchanged | −0.114 | [−0.179, −0.050] | 1 / 5 |
| INVERT | Outcome Dominance | ends exchanged | −0.614 | [−0.671, −0.554] | 0 / 7 |
| NONCE | Factor K | as original | +0.175 | [+0.114, +0.236] | 6 / 1 |

**FLIP is the decisive intervention.** It exchanges the two endpoint strings,
preserving the name, numeric values, field position, character count, and
character multiset. Applying the edit twice restores the original block byte
for byte. It changes which phrase is associated with 0 and 1, including the
phrases' order; it does not preserve the token sequence. A name-only or
definition-insensitive salience account predicts no systematic change.

The frozen protocol prespecified both each variant's high-minus-low effect and
the direct contrasts **CANON − variant**. Its decision rule additionally required
FLIP to be negative with an interval excluding zero and at least four negative
items. CANON − FLIP is **+0.454 [+0.361, +0.546]**, with all seven item-level
differences positive. The post-hoc crossed interval is [+0.179, +0.739] and the
item-level *t* p = 0.019. Thus, sensitivity to the endpoint assignment survives
both reported approaches to item uncertainty.

FLIP itself is −0.114 and negative on five items, positive on one, and tied on
one. It meets the original unit-level decision rule. Its crossed interval,
[−0.239, +0.025], includes zero (*t* p = 0.071), so the data support a change in
the effect more securely than a reversal generalising across items. The
definition is causally relevant in these prompts; its general dominance over
conflicting names is not established.

**The name contributes too.** NONCE preserves a positive effect of +0.175
(crossed CI [+0.025, +0.325]). CANON − NONCE is +0.164 (crossed CI [+0.011,
+0.321]), supporting a contribution from the original name in this comparison.
INVERT combines the exchanged definition with *Outcome Dominance* and gives
−0.614, negative on every item. This shows how strongly the joint wording can
matter, but the four variants are not a complete factorial crossing of names
and definitions. They do not identify a universal additive decomposition or
show that every name is dispensable.

![**Effects of the principal manipulations.** Blue bars are 95% intervals from the unit-bootstrap analysis; thin black bars resample agents and items independently. All contrasts use `gpt-5.4-mini`, with 40 agents × 7 items unless stated. Differences in field assignment (§5) and endpoint definitions (§6.1) change the estimated effect. Three invented fields follow their predicted directions; Worst-off Priority does not (§6.2). Intervals are pointwise.](figures/fig1_forest.pdf){width=100%}

### 6.2 Three of four invented fields follow predicted directions

If definitions are what the model acts on, then the block's own fields should not
be special. We wrote four fields that are **not** in the block, each with a name
and a two-line definition, placed each in the partner slot (line 10), and pinned
them in the same way. Signs were derived from each definition and locked in
advance. The high ends read:

- *Status-quo Preference*: "existing arrangements stand unless there is strong
  reason to change them";
- *Stated-Wish Deference*: "a person's stated wish about their own arrangement is
  decisive";
- *Worst-off Priority*: "whoever would lose most matters most";
- *Numbers Count*: "the option helping more people is favoured", written to point
  toward overriding.

| Invented field | Sign | Effect | 95% CI (units) | Crossed CI | Items +/− |
|:----------------------|:----|-------:|:-----------------|:-----------------|:------|
| Status-quo Preference | + | **+0.400** | [+0.336, +0.464] | [+0.229, +0.579] | 7 / 0 |
| Stated-Wish Deference | + | +0.307 | [+0.254, +0.361] | [+0.179, +0.436] | 7 / 0 |
| Numbers Count | − | **−0.246** | [−0.311, −0.182] | [−0.386, −0.114] | 0 / 7 |
| Worst-off Priority | + | −0.064 | [−0.129, 0.000] | [−0.218, +0.096] | 2 / 4 |

Two fields in the same slot, in the same format, carrying the same numerals, move
choices in **opposite directions** on every item, each as its own definition
states (Figure 2b). This is inconsistent with an identical directional response to every field
in that slot. It complements §6.1, but changes names and definitions together,
so it cannot independently attribute the difference to definitions alone.

One of our four locked predictions failed. We derived Worst-off Priority as
positive, because the holder loses the most under overriding. It came out near
zero and split across presentation orders. A designer's reading of what a
definition implies did not predict the model, which illustrates why predicted meanings need behavioural tests. FLIP
provides a particularly controlled test of endpoint assignment, although
interpreting the direction still depends on the task.

**The original fields are not uniquely effective.** Status-quo Preference gives
a descriptively larger effect than PD (+0.400 against +0.339), but those
estimates use different slots and populations and are not a controlled test of
superiority. The invented fields remain embedded in the other nine entries;
their success does not show that the surrounding block can be removed. It does
show that behavioural control is not restricted to the original vocabulary.

![**Per-item effects.** (a) Exchanging the ends of PD's definition (CANON → FLIP) lowers the effect on all seven items. (b) Two invented fields in the same slot move every item in opposite directions, as their definitions state.](figures/fig2_items.pdf){width=100%}

### 6.3 A field's effect does not validate its intended construct

The base items were written so that preserving an arrangement was taken to
align with a process-dominant reading. They do not independently distinguish
that reading from a preference for the status quo. We therefore wrote twins
adding a clause that the holder bypassed an applicable procedure. Under the
locked interpretation, PD should not protect that arrangement, whereas an
explicit Status-quo Preference field might. These are operational predictions,
not a uniquely determined theory of procedural justice.

Two screens (417 calls, 17 wordings) did not yield enough dispersing twins.
Three twins had unprofiled keep-rates of 0.00–0.04. A subsequent designation
retained these three for a one-directional test and required both fields to
reproduce their base-item effects (PD +0.350; Status-quo Preference +0.357).

| High-minus-low effect on three floored twins | Estimate | 95% CI (units) |
|---|---:|---|
| PD | +0.383 | [+0.292, +0.475] |
| Status-quo Preference (SQ) | +0.133 | [+0.058, +0.208] |
| SQ − PD | −0.250 | [−0.358, −0.142] |

The locked decision rule returned **mixed**, not confirmation of either account.
PD increased keeping on two twins despite the procedural lapse; the third was
zero in all four twin cells. However, a larger high-minus-low effect is not
necessarily a higher high arm. On `rest_break`, both fields reach 0.775 when
high, but PD starts at 0.100 and SQ at 0.425. On `tool_library`, their high arms
are 0.675 and 0.450. Sensitivity to the added clause is also mixed: high-PD
keep-rate falls by 0.15 on `rest_break`, while high-SQ rises by 0.05; on
`tool_library`, PD falls by 0.30 and SQ by 0.50. PD is not uniformly less
sensitive to the clause.

Only two items inform the difference, its crossed interval reaches zero
([−0.500, 0.000]), and the fields occupy different slots. These results challenge
the intended interpretation of PD without establishing it as a pure status-quo
construct. They also demonstrate that an unprofiled floor need not remain a
floor after conditioning.

### 6.4 Examples and a prose principle also change choices

To test whether explicit field text was necessary for a related shift, we
presented five earlier decisions associated with each profile, drawn from the
frozen prospective PD records, without its field names or definitions. Calls
were stateless: these were examples inserted into a new prompt, not memories
retained by a continuing agent. The examples concerned base items; evaluation
used the twins with procedural lapses. Each item was shown in both option orders.

| User-turn condition | Keep-rate | Difference from bare item |
|---|---:|---|
| Bare item | 0.305 | — |
| Five earlier decisions | 0.734 | +0.429 [+0.384, +0.473] |
| One-sentence principle | 0.768 | +0.463 [+0.418, +0.507] |

The principle reads: *"You place weight on fair procedure for its own sake:
where an arrangement was arrived at through a stated process, that matters
independently of the outcome it produces."* Both conditions increase keeping
relative to the bare twin. Principle minus examples is +0.034 [+0.004, +0.064]
over the original units; the crossed interval includes zero ([−0.032, +0.098]).
That is not an equivalence test. Because these are twins and a different
experiment, the magnitudes cannot establish that prose matches or outperforms
the original block (§5.1).

A secondary analysis asked whether keeping increased with the fraction of
examples that kept. An initial run confounded example composition with option
order. After crossing order, the slope was +0.080 [+0.018, +0.137] in the
examples arm and −0.011 in the principle arm. The four composition levels had
3, 4, 17, and 16 profiles. Restricting the analysis to the two well-populated
levels gave −0.011 [−0.066, +0.046]. This does not establish a stable graded
relationship. Even a positive slope would be compatible with ordinary
in-context conditioning; it would not by itself demonstrate a persistent
disposition. These experiments establish additional ways to change choices,
while leaving the underlying computational account unresolved.

## 7. How far do the results generalise across items?

With seven items, the prespecified unit-level tests support statements about
*these* items. The item-level analyses (§4.5; Appendix C) sort the claims into
three groups.

**Intervals exclude zero under crossed resampling:** pinning PD (+0.346), the field-versus-partner
difference (+0.375), the field factor of the 2×2 (+0.300), the definition exchange
(CANON − FLIP, +0.454, 7/7 items), INVERT, NONCE, the three invented fields that
moved as predicted (including the opposite-signed Numbers Count, 0/7), Mode of
Response, and the examples and principle arms against the bare item.

**Evidence weakens under item-level analysis:** FLIP's own sign, PD on the second
provider (borderline), ID's swap TRUE arm and ID pinned on the second provider,
Tolerance for Asymmetry (whose
items disagree in sign), the gap between examples and a stated principle, and the
floor-lift dissociation of §6.3.

**No effect detected under either approach:** the swap arm, the partner field, the partner at
the field's line, ID's swap difference, Worst-off Priority, and LL at 40 and 80
agents.

The central direct contrast belongs to the first group: exchanging endpoint
definitions changes the estimated field effect. These checks assess sensitivity
within the observed set, not transfer to unseen tasks. Some item-level results
are near the conventional threshold, and none is corrected across this entire
summary of contrasts.

## 8. Implications for auditing structured prompts

The results distinguish three questions that are easy to conflate: whether a
profile changes choices, whether a particular field contributes, and whether
that contribution implements the intended construct. Pinning and direct swap
contrasts address the second question. Definition edits further identify an
input feature that matters. The twins show why even this chain does not settle
the third question. For a practical audit, the outcome and predicted direction
should therefore be specified independently of the field's name.

**A four-step prompt audit.**

1. **Pin and replicate.** Specify the outcome and predicted direction, then
   compare low and high values with the surrounding profile and item held fixed.
   Include target-effect arms in subsequent control runs: a null control cannot
   explain an effect that fails to reproduce.
2. **Swap numeric assignments.** Move the target values to a partner field while
   preserving the numeral multiset, definitions, field order, and character
   count. Estimate the direct difference between target and partner effects,
   with uncertainty. A significant target and nonsignificant partner are not
   themselves evidence of a difference; treating the partner as a negative
   control also requires evidence that its effect is small.
3. **Cross identity with position.** Test both field assignments at both list
   positions. This tests a position-only explanation while allowing position to
   modulate the field effect.
4. **Edit definitions and names.** Exchange the definitions assigned to the
   scale endpoints while keeping the name, values, and character inventory
   fixed, and separately replace the name with a nonce label. Use direct
   contrasts to assess sensitivity to these edits. Character preservation does
   not guarantee identical token counts, and these tests do not fully separate
   all contributions of names, definitions, and their interactions.

The checklist identifies controlled input effects. Validating an intended
construct additionally requires scenarios that distinguish it from plausible
alternatives, as the procedural-violation twins illustrate (§6.3).

**Balance and report presentation order.** Two items show keep-rate differences
of 0.75 and 0.73 between option orders. Holding order fixed within each pair
protects the paired contrast from an order imbalance between its arms, but does
not remove treatment-by-order interactions. PD and three invented fields retain
their signs in both order strata; Worst-off Priority does not. A pooled baseline
near 0.50 can also conceal almost deterministic responses within each order.
Crossing both orders within profile and item provided exact balance in the
later example experiment. Randomisation remains valid, but can leave consequential
imbalance in small samples. Screens should inspect each order separately.

**Interpret controls with their target effect.** LL's failure to reproduce
prevents a null partner control from validating the earlier claim. Conversely,
the later TfA and MoR results show why non-detection in a small sweep is not a
permanent classification. An audit should preserve both findings and failures,
and distinguish small estimated effects from established zeros.

**Automated review complements empirical checks.** Model review identified
wording and packet errors, but repeated reviews of identical material gave
different verdicts. One four-item pool received three accepts and one rejection;
the seven-item pool received three accepts and four revision requests across
its recorded reviews. These are observations from this workflow, not an
estimate of reviewer reliability. Accepted historical material was not repeatedly
resubmitted to obtain a preferred verdict. Construction checks and measured
behaviour remained necessary even for accepted items.

## 9. Limitations

**Task and model coverage.** The main evidence comes from seven selected
allocation dilemmas on one model snapshot. The initial comparison has eight
items, and the second provider has six. Cross-provider pinning does not replicate
the swap, position, or definition controls. A second family of 14 items passed
review and 11 dispersed, but only three met both dispersion and order-robustness
criteria against six required, so collection stopped at screening. This failed
attempt does not provide out-of-family validation.

**Meaning and mechanism.** Exchanging definitions demonstrates sensitivity to
their endpoint assignment. It also changes phrase order and can be processed as
an instruction. We do not distinguish semantic understanding from instruction
following, learned lexical associations, or other sequence-sensitive mechanisms.
No internal representation is measured. The nonce and invented-field tests
use too few wordings to establish robustness to paraphrase or arbitrary labels.
The example experiment does not test durable learning across independent calls.

**Selection and uncertainty.** The programme was adaptive: earlier findings
motivated later, separately specified studies. Freezing each run's design does
not turn the whole sequence into a single preregistered confirmatory experiment.
Corrections are local to each designation, intervals are pointwise, and item-level
sensitivity analyses were added after collection. Seven closely related items
and one response per ordinary arm-profile-item cell limit what can be learned
about item and sampling variability.

**Partial attribution.** PD has the most complete chain of controls, not an
established monopoly on the profile effect. ID remains a candidate for
field-specific binding; TfA and MoR have follow-up pinned effects without swap
tests. The remaining four original fields were not detected in the 25-agent
sweep. The experiments neither remove PD to decompose the overall profile
effect nor exhaust interactions among fields. Invented fields were tested within
the existing block, not alone.

**Outcome scope.** Equal aggregate payoffs do not neutralise distributional or
worst-off considerations. Unequal-total tasks remain untested. Keep-rate is a
choice frequency, not moral quality, welfare improvement, or human resemblance;
no human comparison was collected.

## 10. Conclusion

A structured prompt can change behaviour without validating its designer's
interpretation of the fields. On the tested model and allocation items, PD's
numeric effect differs from its partner's and persists at both tested
positions. Exchanging only the endpoint definitions lowers that effect on all
seven items, with a direct difference of +0.454 and a crossed interval excluding
zero. Replacing the name preserves part of the effect, while also showing that
the name contributes. The evidence identifies sensitivity to the endpoint
assignment; it does not establish understanding or isolate an internal mechanism.

The practical contribution is a sequence of controls that turns an observed
prompt effect into a more specific, testable claim. The same sequence preserves
negative results, exposes a failed replication, and limits the interpretation
of apparently successful controls. It can be used to audit a behavioural
interface before relying on it, or to define controlled input contrasts for
subsequent work on open models.

## References

::: {#refs}
:::

## Appendix A. Full system prompt

The CANON-high system prompt for agent 0 in the definition experiment
(`semantics_r1`). The low prompt changes only `Procedural Dependence: 0.90`
to `0.10`. Long lines are wrapped for print; the frozen requests preserve the
exact whitespace. The G arm in §5.1 replaces the profile with the quoted guidance.

```
You are participating in a decision-making simulation.

# Your decision-making profile

You process decisions according to the following characteristics, each
on a continuous [0, 1] scale. The low and high ends of each are
described. Your value on each characteristic is given.

 1. Legitimacy Locus: 0.79
    (0 = validity comes from institutional warrant and shared norms;
     1 = validity comes from personal judgment and self-authored endorsement)

 2. Constraint Sensitivity: 0.69
    (0 = influence registers as environmental feature;
     1 = even soft pressure registers as meaningful restriction)

 3. Response Threshold: 0.23
    (0 = high tolerance; only major violations activate response;
     1 = hair-trigger; minor deviations activate response)

 4. Mode of Response: 0.40
    (0 = internal, reflective, self-adjusting;
     1 = external, behavioural, confrontational)

 5. Relational Embedding: 0.40
    (0 = atomised, agent-centred, abstract-person model;
     1 = role-sensitive, relational, socially embedded)

 6. Procedural Dependence: 0.90
    (0 = outcome-dominant; results matter, methods are secondary;
     1 = process-dominant; fair procedure matters independently)

 7. Tolerance for Asymmetry: 0.68
    (0 = asymmetry is inherently suspect, default is symmetry;
     1 = asymmetry is accepted if intelligible, hierarchy is fine)

 8. Internalization Dependence: 0.90
    (0 = surface compliance is sufficient;
     1 = genuine endorsement and value-congruence required)

 9. Moral Scope: 0.80
    (0 = local, role-bound, partial, context-limited;
     1 = universalised, generalisable, broadly applied)

 10. Affective Weighting: 0.84
    (0 = cognitive, deliberative, reasoned processing;
     1 = affective, intuitive, felt processing)

# Your normative context

You operate in a society with the following structural properties:
- Freedom:   NEUTRAL
- Justice:   NEUTRAL
- Authority: NEUTRAL
- Care:      NEUTRAL
- Loyalty:   NEUTRAL

For axes marked HIGH, the institution enforces, permits, and rewards that
    property; for axes marked LOW, that property is unstructured, unprotected, or
    penalised. NEUTRAL means no institutional high or low stance is specified on
    that axis; it does not remove your individual characteristics or the facts of
    the task.

# Your task
Use the supplied information to make the requested decision. Do not infer a
    demographic identity or additional facts. Return only the requested JSON
    object.
```

In FLIP the three lines of entry 6 read `(0 = process-dominant; fair procedure
matters independently; 1 = outcome-dominant; results matter, methods are
secondary)` with the name and value unchanged. INVERT additionally renames the
entry *Outcome Dominance*, and NONCE renames it *Factor K* with the original
definition. Invented fields (§6.2) replace entry 10 with the field's name, value
and definition in the same format.


The complete low and high definitions of the invented fields are:

| Field | Low endpoint (0) | High endpoint (1) |
|:---|:---|:---|
| Status-quo Preference | existing arrangements carry no special weight | existing arrangements stand unless there is strong reason to change them |
| Stated-Wish Deference | a stated wish is one input among many | a person's stated wish about their own arrangement is decisive |
| Worst-off Priority | total benefit matters however it is spread | whoever would lose most matters most |
| Numbers Count | claims are weighed regardless of how many hold them | the option helping more people is favoured |

## Appendix B. Task materials

### B.1 Base items

The seven main GPT identification items are `desk_booking`, `storage_unit`,
`tool_library`, `on_call`, `meeting_room`, `rest_break`, and `weekend_rota`.
The initial GPT comparison also includes `sample_draw`. Haiku uses the same
set except `on_call` and `rest_break`, with `ward_transfer` added (six items).
The following text is taken from the frozen request files. Option order below
is one recorded order; experiments also use the opposite order. Formatting is
adapted for print, without changing the scenario or option wording.

**Shared framing:**

You hold the role described. The option you select will be carried out, not merely considered. Units are artificial simulator credits, stipulated equally valuable to every person, and all stated effects are certain and known to you. There are no hidden costs, benefits or later effects beyond those described, and no one is pressuring you toward either option. Decide on the situation as given.

Every item ends with `Return JSON only: {"choice":"<OPTION NAME>"}.`

**desk booking**

An office has one bookable desk left for the week. One person booked it and has said they want to keep the booking. Two visiting staff otherwise work from a corridor bench.


Option KEEP_DESK: Leave the desk with the person who booked it. That person gains 1 unit; the two visiting staff lose 4 units between them.

Option REASSIGN_DESK: Give the desk to the two visiting staff. The two visiting staff gain 2 units between them; that person loses 5 units.

**storage unit**

A community centre needs one more storage unit for winter supplies. One unit is leased by a resident who has said they want to keep it for the season. The supplies otherwise sit outdoors and part of them spoils.


Option KEEP_LEASE: Leave the leased unit with the resident for the season. The resident gains 1 unit; the supply programme loses 4 units.

Option RECLAIM_UNIT: Use the leased unit for the winter supplies. The supply programme gains 2 units; the resident loses 5 units.

**tool library**

A repair session needs a press that one member owns and has lent to the library under terms letting them withdraw it. They have said they want it back this week. Without the press three of the booked repairs cannot proceed.


Option RETURN_PRESS: Return the press to its owner this week. The owner gains 1 unit; the booked repairs lose 4 units between them.

Option HOLD_PRESS: Keep the press at the library through this week. The booked repairs gain 2 units between them; the owner loses 5 units.

**on call**

An on-call slot is unfilled for one night. One person already off-rota has said they want the night clear. Leaving it unfilled sends two callouts to a team an hour further away.


Option LEAVE_UNFILLED: Leave the on-call slot unfilled for that night. That person gains 1 unit; the two callouts lose 4 units between them.

Option ASSIGN_ON_CALL: Put that person on call for the night. The two callouts gain 2 units between them; that person loses 5 units.

**meeting room**

A meeting room is held for one group's weekly session. They have said they want to keep the slot. Two other groups have sessions that need the room this week and no alternative space of the size.


Option KEEP_SLOT: Leave the weekly slot with the group that holds it. That group gains 1 unit; the two other groups lose 4 units between them.

Option RELEASE_SLOT: Give this week's slot to the two other groups. The two other groups gain 2 units between them; that group loses 5 units.

**rest break**

A long shift has one mandatory rest slot left in the schedule. One worker has said they want to take it. Assigning it to a colleague instead lets two pending tasks finish inside the shift.


Option KEEP_REST: Give the rest slot to the worker who asked for it. That worker gains 1 unit; the two pending tasks lose 4 units between them.

Option REASSIGN_REST: Give the rest slot to the colleague instead. The two pending tasks gain 2 units between them; that worker loses 5 units.

**weekend rota**

A service needs one more person on Saturday. One member of staff has said they want that Saturday free. Without them the service runs reduced and two scheduled appointments are put back.


Option KEEP_SATURDAY: Leave that member of staff off the Saturday. That member of staff gains 1 unit; the two appointments lose 4 units between them.

Option ADD_TO_SATURDAY: Put that member of staff on the Saturday. The two appointments gain 2 units between them; that member of staff loses 5 units.

**ward transfer**

A ward is over capacity for the night. One patient has a single room and has said they want to keep it. Two patients are waiting on trolleys in the corridor. Moving the first patient frees the room for both.


Option LEAVE_ARRANGEMENT: Keep the current room allocation for tonight. The patient in the room gains 1 unit; the two waiting patients lose 4 units between them.

Option MOVE_PATIENT: Allocate the room to the two waiting patients tonight. The two waiting patients gain 2 units between them; the patient in the room loses 5 units.

**sample draw**

A clinic can run one more panel tonight. One attending person has said they want no further blood taken today. A second draw from them completes a panel that two other people are waiting on.


Option NO_FURTHER_DRAW: Take no further sample from that person today. That person gains 1 unit; the two waiting people lose 4 units between them.

Option TAKE_SAMPLE: Take the second sample to complete the panel. The two waiting people gain 2 units between them; that person loses 5 units.

### B.2 Procedural-lapse twins

For the twin conditions, the scenario paragraph is replaced by the following
text. The shared framing, two option texts, and JSON instruction remain the
same. All seven twins are retained in the example experiment; the floor-lift
contrast uses `rest_break`, `storage_unit`, and `tool_library`.

**desk booking**

An office has one bookable desk left for the week. Desks are booked on a sheet that opens each Monday. One person entered their name on the Friday before the sheet opened, holds the booking, and has said they want to keep it. Two visiting staff otherwise work from a corridor bench.

**storage unit**

A community centre needs one more storage unit for winter supplies. Units are leased in order from a waiting list. One unit is leased by a resident who was given it ahead of the list by an acquaintance in the office, and who has said they want to keep it for the season. The supplies otherwise sit outdoors and part of them spoils.

**tool library**

A repair session needs a press that one member owns and has lent to the library under terms fixing the loan until the end of the month. Two weeks before that date they have said they want it back this week. Without the press three of the booked repairs cannot proceed.

**on call**

An on-call slot is unfilled for one night. Changes to the rota go through a swap form. One person is off-rota this week through a swap arranged privately and never entered on the form, and has said they want the night clear. Leaving it unfilled sends two callouts to a team an hour further away.

**meeting room**

A meeting room is held for one group's weekly session. Weekly slots are allocated by a room committee each term. This group entered its slot in the room diary itself, before the committee met, and has said it wants to keep the slot. Two other groups have sessions that need the room this week and no alternative space of the size.

**rest break**

A long shift has one mandatory rest slot left in the schedule. Rest slots are taken in an order drawn at the start of the shift. One worker who has already taken their slot has said they want to take this one. Assigning it to a colleague instead lets two pending tasks finish inside the shift.

**weekend rota**

A service needs one more person on Saturday. Saturdays off are granted through a request form with a two-week deadline. One member of staff, who did not file the form, has said they want that Saturday free. Without them the service runs reduced and two scheduled appointments are put back.

## Appendix C. Item-level robustness

Every contrast is estimated on `gpt-5.4-mini` with 40 agents unless marked. *Unit*
is a recomputed interval over agent-item units. For the example experiment,
the two order-specific differences are first averaged within agent and item;
the original report instead resampled agent-item-order units. *Crossed* resamples agents and
items independently. *t p* is from a one-sample *t*-test over per-item effects.
Items gives the per-item signs. The contrasts marked † are direct between-condition differences. The
CANON comparisons were prespecified in the semantics protocol; their crossed
and item-level analyses, like the other robustness analyses here, are post-hoc. All
are computed from the frozen records by `paper_item_robustness.py`, with zero API
calls and seed 2026092301. Unit intervals are recomputed here with one common
seed. They differ from the designation reports quoted in the main text by at most
0.01, due to resampling and, for the example experiment, averaging over option
orders. Point estimates are identical. Item counts omit exact-zero ties.

| Contrast | Estimate | Unit 95% CI | Crossed 95% CI | *t* p | Items +/− |
|:----------------------------------|----------:|:--------------------|:--------------------|--------:|:--------|
| PD pinned (prospective) | +0.346 | [+0.279, +0.414] | [+0.121, +0.568] | 0.024 | 6 / 1 |
| PD swap: TRUE | +0.339 | [+0.275, +0.404] | [+0.103, +0.582] | 0.035 | 6 / 1 |
| PD swap: SWAP | −0.036 | [−0.093, +0.018] | [−0.139, +0.075] | 0.385 | 2 / 4 |
| PD swap: TRUE − SWAP | +0.375 | [+0.286, +0.464] | [+0.082, +0.661] | 0.046 | 6 / 1 |
| ID swap: TRUE − SWAP | +0.064 | [−0.014, +0.146] | [−0.093, +0.221] | 0.353 | 3 / 2 |
| 2×2 field factor | +0.300 | [+0.232, +0.370] | [+0.111, +0.495] | 0.022 | 7 / 0 |
| 2×2 position factor | +0.032 | [−0.025, +0.087] | [−0.061, +0.123] | 0.281 | 5 / 1 |
| AW pinned (80 agents) | +0.016 | [−0.025, +0.057] | [−0.052, +0.087] | 0.492 | 4 / 2 |
| LL pinned (80 agents) | −0.036 | [−0.080, +0.007] | [−0.139, +0.080] | 0.513 | 1 / 5 |
| TfA pinned (80 agents) | −0.111 | [−0.154, −0.066] | [−0.245, +0.030] | 0.155 | 2 / 4 |
| MoR pinned (80 agents) | −0.073 | [−0.114, −0.030] | [−0.134, −0.007] | 0.003 | 0 / 6 |
| PD pinned, `haiku` (6 items) | +0.133 | [+0.062, +0.204] | [−0.013, +0.283] | 0.076 | 4 / 1 |
| ID pinned, `haiku` (6 items) | +0.075 | [+0.013, +0.142] | [−0.062, +0.204] | 0.218 | 4 / 2 |
| CANON | +0.339 | [+0.271, +0.407] | [+0.121, +0.568] | 0.026 | 6 / 1 |
| FLIP | −0.114 | [−0.179, −0.054] | [−0.239, +0.025] | 0.071 | 1 / 5 |
| INVERT | −0.614 | [−0.675, −0.557] | [−0.771, −0.457] | $<0.001$ | 0 / 7 |
| NONCE | +0.175 | [+0.114, +0.236] | [+0.025, +0.325] | 0.048 | 6 / 1 |
| CANON − FLIP † | +0.454 | [+0.361, +0.546] | [+0.179, +0.739] | 0.019 | 7 / 0 |
| CANON − NONCE † | +0.164 | [+0.082, +0.246] | [+0.011, +0.321] | 0.024 | 6 / 0 |
| Status-quo Preference | +0.400 | [+0.336, +0.464] | [+0.229, +0.579] | 0.003 | 7 / 0 |
| Stated-Wish Deference | +0.307 | [+0.254, +0.361] | [+0.179, +0.436] | 0.002 | 7 / 0 |
| Numbers Count | −0.246 | [−0.311, −0.182] | [−0.386, −0.114] | 0.007 | 0 / 7 |
| Worst-off Priority | −0.064 | [−0.129, 0.000] | [−0.218, +0.096] | 0.403 | 2 / 4 |
| Status-quo Preference − Numbers Count † | +0.646 | [+0.561, +0.736] | [+0.425, +0.857] | $<0.001$ | 7 / 0 |
| Floor lift: SQ − PD (3 items) | −0.250 | [−0.358, −0.133] | [−0.500, 0.000] | 0.191 | 0 / 2 |
| Examples vs bare item | +0.429 | [+0.382, +0.475] | [+0.223, +0.641] | 0.009 | 7 / 0 |
| Principle vs bare item | +0.463 | [+0.418, +0.507] | [+0.241, +0.693] | 0.009 | 7 / 0 |
| Principle − examples | +0.034 | [+0.004, +0.064] | [−0.032, +0.098] | 0.208 | 6 / 1 |

For the first-stage contrasts, the thesis also fitted logistic models with
crossed random intercepts for agent and item and an item-specific treatment slope.
Under those models E − G stays significant on both providers (*p* = 0.0001 and
0.041), PD pinned stays significant (*p* = 0.0006), and ID's swap TRUE arm does not
(*p* = 0.061), which is one reason ID is reported only as a candidate.

## Appendix D. Scale and reproducibility

The wider project reports 35,879 API calls across 56 designations and about
$45.05 in estimated usage, including development, screens, reviews, and
interrupted runs. These are not the central experiment's sample (2,240 calls)
or verified provider balances. Before collection, each designation's requests,
population, predictions, and decision rule are hash-frozen and checked at dispatch;
per-call records are write-once. Transport failures at call 689/2,801 in
`coordinate_sweep_r1` and 294/840 in `precipitation_r1` closed those designations;
replacements reused no records. Committed modules reproduce the power simulations
and offline analyses, including Appendix C. The
principal designations are `phase4b_gpt_r2` and `phase4b_profiled_r1` (§5.1),
`pd_prospective_r1` and `label_semantics_r1` (§5.2), `label_semantics_r2` (ID and
LL), `position_counterbalance_r1` (§5.3), `coordinate_sweep_r2` (sweep),
`parameter_followup_r1`/`r2` (80-agent pins), `pd_crossmodel_r1` and
`id_crossmodel_r1` (§5.6), `semantics_r1` (§6.1), `probe_fields_r1` (§6.2),
`floor_lift_r1` (§6.3) and `precipitation_r3` (§6.4).
