---
title: "The Model Reads the Definition"
subtitle: "Field-Level Controls Show Which Part of a Structured Prompt Carries Behaviour"
author: "Tommaso Piero Palamenga^[Bocconi University. This paper and the author's undergraduate thesis draw on one body of evidence but are separate documents: the thesis (submitted, frozen) presents a ten-parameter encoding framework on evidence to 18 September 2026; this paper makes a narrower claim on a wider evidence base, including later results that constrain that framework. Code, prespecifications and every per-call record: <https://github.com/tommypalam/conceptual-architecture-methods>.]"
date: "Preprint, September 2026"
abstract: |
  When a structured block in a prompt (a persona, a trait vector, a configuration) changes a language model's behaviour, the usual inference is that the model read what the block says. That inference is rarely tested, because the natural comparisons confound what a field *means* with the fact that text is present, how long it is, where it sits and what number it carries. We introduce field-level controls that separate these: **pinning** one field to its endpoints with every other byte fixed; a **swap control** that moves the identical numeral onto a partner field, so both prompts contain the same numbers on the same lines; a **replication gate** that requires the effect to reproduce before its control is read; and **definition edits** that change what a field says while holding its name, line and numeral fixed. Applied to a ten-field block over seven two-option allocation dilemmas with tied payoffs (35,879 recorded calls, mainly on `gpt-5.4-mini`), the controls localise the behaviour to one field (+0.375 on keep-rate against its swap control) rather than to its line or its numeral. Exchanging only which end of that field's scale is defined as which moves the effect by −0.454 on all seven items and makes it negative on five; fields we invented move choices in the directions their definitions state, including one written to point the opposite way (three of four locked predictions held). The field's *name*, by contrast, is a poor guide to what it does: the field called Procedural Dependence behaves as a status-quo pressure rather than as sensitivity to procedure. The same controls withdrew a field that had cleared a corrected significance test. We report item-level robustness for every contrast, and we claim no understanding, no moral quality and no generality beyond one task family.
---

## 1. Introduction

Practitioners routinely condition language-model agents on structured text: a
persona, a list of traits with numeric levels, a configuration block. When
behaviour changes, the next step is almost always to say the model *read* the
block. It saw that this agent is cautious, or process-oriented, and acted on it.
Persona prompting and much of agent design rest on that step.

The step is an inference, and several rival mechanisms predict the same
observation. The block adds text, and more text changes outputs. It adds
structure, which models may treat differently from prose. It contains extreme
numerals, which may be salient wherever they sit, or salient only on some lines.
It contains names the model may associate with dispositions regardless of what
the block says they mean. The prompt-sensitivity literature shows that changes of
exactly this kind, with meaning held constant, can move model behaviour
substantially [@lu2021fantastically; @sclar2023quantifying; @razavi2025benchmarking].
A practitioner who has built a persona and seen it work therefore cannot say,
from that observation alone, which of these is happening, and the alternatives
license very different conclusions about what was built.

This paper asks a narrow question: **which part of a structured prompt carries
the behaviour, and what about that part does the carrying?** We answer it with
controls that change one thing at a time, holding every other byte of the prompt
fixed, and we apply them to one structured block on one family of decisions.

**What we find.** (i) The effect localises to one field of ten. Moving the
identical numeral to a different field removes it, and moving the field to a
different line keeps it. (ii) What carries it is the field's **definition**, the
two-line gloss saying what each end of the scale means. Exchanging the two ends of
the gloss, with the name, line, numeral and the block's full character multiset
unchanged, moves the effect by −0.454 on every item and makes it negative on five of seven.
Removing the name while keeping the definition preserves about half of the effect.
(iii) The result is not specific to the block we started from. Of four fields we
wrote for the purpose, three move choices in the directions their definitions
state, and two of these, in the same slot, move choices in opposite directions. (iv) A field's
name is a poor guide to what it does. The field named *Procedural Dependence*
behaves as a pressure to keep existing arrangements, and it is **less** sensitive
to whether a procedure was followed than an explicit status-quo field is. (v) The
method can retract its own findings. A second field cleared a Holm-corrected test
at 25 agents and did not replicate at 40 or 80. Its swap control, read without a
replication gate, would have certified it.

**Contributions.**

- **A set of field-level controls** (pinning, a numeral-identical swap control, a
  line-by-field crossing, a replication gate, and definition edits) that apply to
  any prompt with addressable fields and require no access to model internals.
- **Evidence that the definition carries the effect**, excluding numeric salience
  and name association as sufficient explanations, with item-level robustness
  analyses for every contrast.
- **Evidence that field names mislead.** An invented field can outperform the
  block's own field, and that field does not do what its name suggests.
- **Two methodological findings** for anyone running prompt experiments:
  presentation order must be *crossed* with anything that could correlate with it,
  not merely randomised, and automated design review returns different verdicts
  on byte-identical material.

**Scope.** All results come from one family of seven short allocation dilemmas.
The identification work uses one model (`gpt-5.4-mini`), with a second provider
for the first-stage results. Every outcome is a deterministic function of the
option chosen. We make no claim about moral quality, human resemblance or
understanding (§9).

## 2. Related work

**Prompt sensitivity.** Surface form matters. The order of in-context examples
can move performance from near chance to near the state of the art
[@lu2021fantastically]. Formatting alone spans large accuracy ranges with meaning
held constant [@sclar2023quantifying], and the same holds for wording, structure
and punctuation [@razavi2025benchmarking]. Neither scale nor instruction tuning
removes the brittleness [@chatterjee2024posix]. This literature is why our
controls hold surface form fixed to the byte rather than approximately: any
looser comparison sits within the range these studies show to matter on its own.

**Do models use what prompts mean?** @webson2022prompt found that prompt-based
models could learn as fast from irrelevant or misleading templates as from
instructive ones, and @min2022rethinking that randomly replacing demonstration
labels barely hurts in-context performance. Large models can override semantic
priors to learn from semantically unrelated labels [@wei2023larger], and output
can bind to a demonstrated label inventory regardless of plausibility
[@liu2026incontext]. These results are deflationary about semantic reading, and
we take them seriously. Our setting differs: a current instruction-tuned model
makes a zero-shot choice, and the manipulated text is a definition, not a
template or a label. Here the definition's content does determine the direction
of the effect (§6). What remains open is *why* it does. Our evidence is
consistent with the model treating a definition as an instruction (§6.4, §9).

**Persona and profile conditioning.** @luzdearaujo2025helpful compare 162
personas across seven models against an empty persona and 30 paraphrases of "a
helpful assistant", and find more variability under personas than under the
control. @zheng2024helpful find that personas in system prompts do not reliably
improve performance on objective tasks, and that the effects of particular
personas are hard to predict. Both compare conditioned with unconditioned
prompts. As far as our search found, work that isolates *which field* within a
conditioning block carries an effect, with every other byte held fixed, is
scarce. That is the gap this paper addresses. A search that found nothing is not
proof that nothing exists.

**Causal localisation.** Mechanistic interpretability localises behaviour inside
the model through patching, mediation and tracing, unified as causal abstraction
[@geiger2023causal]. It has well-documented sensitivities to the choice of
intervention [@zhang2023towards] and to hidden interactions between mediators
[@vaidyanathan2026curse]. Label words have been found to act as anchors that
gather information in shallow layers [@wang2023label]. Our controls are the
input-side analogue: the same interventionist logic, applied to prompt fields
rather than activations. We gain applicability to closed models and lose
resolution. We localise to a field, not a circuit.

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

**Payoff totals are tied by construction.** Both options sum to −3 on every item,
so welfare maximisation, minimax and best-case reasoning are indifferent between
them. An earlier designation that tied the totals left unprofiled choices
unchanged, which rules out arithmetic as the operative variable. Items were
written to a three-part authoring criterion (matched consequence text, no
asymmetric violation labels, no asymmetric obligation words), enforced in code.
All item texts are in Appendix B.

Seven items were used on `gpt-5.4-mini` and six on `claude-haiku-4-5`, five of
them shared. The item sets differ because items were **screened for baseline
dispersion** on each model before any profiled call. An item on which the
unprofiled model always gives the same answer cannot show an effect. Screening
was on dispersion only, never on outcomes, and no item was dropped after a
profiled result was seen.

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
contrasts are paired within agent and item. Designations use 40 agents unless
stated (25 in the initial sweep, 80 in follow-ups). Appendix A reproduces a full
system prompt.

## 4. Method

### 4.1 Pinning

To test field *F*, set *F* to 0.10 in one arm and 0.90 in the other, keeping the
other nine values as drawn for that agent. The two system prompts differ on
exactly one line, verified byte for byte for every agent before any call, and
the user turn is identical. The **effect** of *F* is the paired difference in
keep-rate, 0.90 minus 0.10.

### 4.2 The swap control

Pinning shows that *a* number moved the outcome, not that the *field* did. The
swap control uses a partner field *P* and a level *L*:

```
TRUE(L)   L on F,                  P's drawn value on P
SWAP(L)   P's drawn value on F,    L on P
```

Both arms contain the same multiset of ten numerals on the same ten lines in the
same order, at the same length. Block presence, length and the presence of an
extreme numeral are held fixed **by construction**. Only which field holds the
value differs. The quantity of interest is the within-unit difference of
differences, TRUE effect minus SWAP effect, with its own interval. We never infer
a difference from one arm being significant and the other not
[@gelman2006difference].

Two refinements matter. Values are compared **at rendered precision**: a drawn
partner value of 0.102 prints as `0.10` and would make TRUE and SWAP identical for
that agent, so degeneracy is checked on the rendered prompt. And the partner
field must itself be shown not to carry the outcome, which we test directly
(§5.4).

### 4.3 The replication gate

A swap control is interpretable only if, in the same designation, the TRUE arm
reproduces the effect it is meant to explain. A null SWAP beside a TRUE arm that
did not replicate says nothing: there may have been nothing to carry. §5.5 is the
case where this mattered.

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
tests with Holm correction [@holm1979simple] over the designation's family, plus a requirement of directional consistency across items. The later
designations (§6) instead prespecified decision rules on unit-bootstrap
intervals. Intervals are 95%
percentile bootstraps over agent-item units (10,000 resamples). Power was
simulated against measured per-item baselines. Failed calls are preserved and
never retried, and a designation halted by a failure is closed and re-designated
rather than resumed.

**Item-level robustness.** Unit-level intervals treat the items as fixed. With
seven items, generalisation to other items of the same kind is a separate
question. For every contrast we therefore also report, after the fact and
without further calls, (a) a **crossed bootstrap** that resamples agents and items
independently, and (b) a one-sample *t*-test over the per-item effects, with
items as the unit. With so few items these analyses have uncertain coverage.
They are sensitivity checks, not replacements for the prespecified tests, and
where a result depends on the choice between them we say so. For the §5.1
contrasts we also report crossed random-effects logistic models with an
item-specific treatment slope [@barr2013random], fitted in the thesis. Appendix C
has the full table.

## 5. Which field carries the behaviour?

### 5.1 A profile moves keep-rate; a generic ethical instruction does not

Three arms: no block (U), a one-paragraph ethical instruction in place of the
block (G), and the full numeric block (E).

| Model | U | G | E | E − G | Holm | Item CI |
|:------------------------|----:|----:|----:|------:|------:|:-----------------|
| gpt-5.4-mini, 8 items | 0.395 | 0.378 | 0.606 | **+0.228** | < 0.001 | [+0.091, +0.372] |
| claude-haiku-4-5, 6 items | 0.367 | 0.429 | 0.600 | **+0.171** | 0.000112 | [−0.025, +0.362] |

: Keep-rates by arm. *Item CI* is a two-stage bootstrap over items, then units, for E − G (from the thesis analyses).

The instruction reads: *"Weigh the interests of everyone affected. Avoid causing
harm, avoid deceiving anyone, avoid coercing anyone, and treat people with
equivalent claims equally. Where these cannot all be satisfied, decide which
matters most in this situation and act on it."* It does not move keep-rate on
`gpt-5.4-mini` (−0.017 against U, p = 0.712), while the block moves it by about
0.2 on both models. On `haiku` the item-level interval includes zero, although a
mixed model with item slopes gives p = 0.041.

This comparison motivates the rest of the paper, and it should not be read as
"numbers beat prose". The instruction does not say anything about keeping or
overriding arrangements, so it is not matched in meaning to the block. §6.4 shows
that a one-sentence prose principle that *is* on topic moves keep-rate as much as
anything in the block does. The question is what in the block does the work.

### 5.2 The effect is bound to one field

An offline reanalysis of earlier data ranked Procedural Dependence (PD) first of
the ten fields. That ranking was post hoc, so PD was tested prospectively, with
the direction derived from the field's definition and locked before collection.
Pinned, PD moves keep-rate by **+0.346** [+0.275, +0.414] (Holm < 0.001; 6 of 7
items positive).

The swap control used Affective Weighting (AW) as the partner. With the numeral on
PD the effect is +0.339. With the identical numeral on AW it is **−0.036**
(Holm 1.000). The within-unit difference is **+0.375 [+0.286, +0.464]**, and it
survives resampling items (crossed CI [+0.082, +0.661]; item-level *t* p = 0.046).
The same numeral, moved from this field to another, has no effect.

A second field, Internalisation Dependence (ID), moved keep-rate when pinned
(+0.111 to +0.143), but its difference against its swap control is +0.064
[−0.014, +0.146]. We report ID as a **candidate**, not a verified field effect.
An earlier reading, "ID's TRUE arm is significant and its SWAP arm is not, so the
field carries it", was the significance-versus-non-significance inference, and we
withdrew it.

### 5.3 It is the field, not the line

In the block, PD is line 6 and AW is line 10, so the swap moved the value's field
and its line together. The 2×2 separates them (40 agents, all four arms with
identical numeral multisets and lengths):

| Cell | Value on | At line | Effect | Holm | Items +/− |
|---|---|---:|---:|---:|---|
| A | PD | 6 | **+0.393** | < 0.001 | 7 / 0 |
| C | PD | 10 | **+0.271** | < 0.001 | 5 / 1 |
| B | AW | 10 | +0.061 | 0.157 | 6 / 1 |
| D | AW | 6 | +0.004 | 1.000 | 3 / 2 |

The field factor, (A + C − B − D)/2, is **+0.300** [+0.232, +0.370] (crossed CI
[+0.111, +0.495]). The position factor is +0.032 [−0.025, +0.088]. Cell D is the
direct test of a primacy account. It puts the value at line 6 on the partner
field and gives +0.004. Position is not irrelevant, though. It **modulates** the
field's effect (A − C = +0.121 [+0.043, +0.200]; interaction +0.089 [+0.030,
+0.150]), a decomposition that was not prespecified.

### 5.4 The partner field, tested directly

Every swap control assumes the partner field does not carry the outcome. Pinned
in its own right at 80 agents, AW is flat: **+0.016** [−0.027, +0.057], with a 90%
equivalence bound of 0.050, the tightest bound in this work. That supports the
controls but does not prove the partner's *slot* is a fair comparison. §6.2 bears
on this: an invented field placed in the same slot reached +0.400. The slot can
carry an effect, and AW's own definition does not produce one.

### 5.5 A field the method withdrew

Legitimacy Locus (LL) had a post-hoc correlation with keep-rate of **+0.271** on
unmanipulated profiles. In the initial sweep (25 agents, Holm over eight fields)
it cleared correction with the most directionally consistent result of any field:
**−0.131** (Holm 0.00082; 0 of 6 items positive). In a designation with a
replication gate (40 agents), its TRUE arm gave **−0.014** (Holm 0.708), and at
80 agents it gave −0.036 [−0.080, +0.009]. The three measurements gave three
answers: positive, negative and null.

The larger samples failed and the smaller one passed, so this is not a power
failure. Power at the size first measured was 17/20. **LL's SWAP arm was null.**
Had the swap control been run without the TRUE arm as a gate, that null would
have read as "the field carries the effect". We withdraw LL. That is not a claim
that LL is inert: the 80-agent interval bounds its effect at 0.073.

The same sweep shows the reverse error. Tolerance for Asymmetry and Mode of
Response missed correction at 25 agents and cleared it at 80 (−0.111 and −0.073;
Appendix C). Sample sizes chosen from budget rather than simulated power gave one
false positive and two false negatives in one sweep. Neither of the two late
movers has had a swap control, so they are effects with unidentified mechanism.

### 5.6 A second provider

PD and ID were pinned on `claude-haiku-4-5` over its own six screened items. PD's
direction was again locked one-sided from its definition, after re-verifying that
the derivation's premise held on the new items. PD gave **+0.133** (p = 0.00031;
4/1 items) and ID **+0.075** (p = 0.033). Both effects shrink, to about 38% and 68%
of their `gpt` values. At item level PD's interval is borderline (crossed CI
[−0.013, +0.283]; item bootstrap [+0.008, +0.267]; *t* p = 0.076), and ID's
includes zero. No swap control was run on `haiku`. These results show that pinning
PD moves the outcome on a second provider in the predicted direction, and nothing
more.

## 6. What about the field carries it?

§5 localises the effect to one field and excludes block presence, length, a
free-floating numeral and line position. Three explanations survive, and they
make different predictions once the field's own entry is edited:

- **definition**: the model reads what the ends of the scale are said to mean;
- **name**: the model associates the field's name with a disposition, and the
  definition is decoration;
- **field-weighted salience**: an extreme numeral in a salient field moves
  behaviour with no reading of the text at all.

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

**FLIP is the decisive arm.** Its edit exchanges two strings, so the name, the
line, the printed numeral and the block's entire character multiset are identical
to CANON. The edit was verified as an involution: applied twice, it restores the
block byte for byte. Salience and name-association accounts both predict FLIP
equal to CANON. The definition account predicts a reversal. The prespecified
estimand compares FLIP with zero, but the contrast that tests all three accounts
at once is **CANON − FLIP**: exchanging the definition's ends changes the effect
by **−0.454** (CANON − FLIP = +0.454 [+0.361, +0.546]), with **all seven items**
moving in that direction (crossed CI [+0.179, +0.739]; item-level *t* p = 0.019).
That result does not depend on how items are treated.

Whether the FLIP effect is itself negative, a full reversal rather than a
cancellation, is less secure. Over agent-item units it is (−0.114, 1 of 7 items
positive). Over items its interval touches zero (crossed CI [−0.239, +0.025];
*t* p = 0.071). We therefore claim that the definition **determines the effect's
direction when name and definition conflict**, and we do not claim the reversal
is item-general.

**Name and definition separate.** With the name replaced by *Factor K* and the
definition kept (NONCE), about half the effect survives (+0.175; crossed CI
[+0.025, +0.325]). When the renamed field and exchanged definition agree
(INVERT), the effect is −0.614, negative on every item and the largest effect in
this work. The name contributes, but when name and definition disagree, the
definition wins. INVERT also rests on a human judgement that *Outcome Dominance*
with exchanged ends means the same as the original. FLIP needs no such judgement,
which is why FLIP carries the argument.

![**Effects of the principal manipulations.** Thick bars are 95% intervals over agent-item units (the prespecified analysis); thin bars resample agents and items independently. All contrasts use `gpt-5.4-mini`, with 40 agents × 7 items unless stated. Moving the numeral off the field, or putting it at the field's line on the partner, removes the effect (§5). Editing the field's definition sets the effect's direction (§6.1). Invented fields follow their own definitions (§6.2).](figures/fig1_forest.pdf){width=88%}

### 6.2 Fields we invented behave the same way

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

| Invented field | Predicted | Effect | 95% CI (units) | Crossed CI | Items +/− |
|:----------------------|:----|-------:|:-----------------|:-----------------|:------|
| Status-quo Preference | + | **+0.400** | [+0.336, +0.464] | [+0.229, +0.579] | 7 / 0 |
| Stated-Wish Deference | + | +0.307 | [+0.254, +0.361] | [+0.179, +0.436] | 7 / 0 |
| Numbers Count | − | **−0.246** | [−0.311, −0.182] | [−0.386, −0.114] | 0 / 7 |
| Worst-off Priority | + | −0.064 | [−0.129, 0.000] | [−0.218, +0.096] | 2 / 4 |

Two fields in the same slot, in the same format, carrying the same numerals, move
choices in **opposite directions** on every item, each as its own definition
states (Figure 2b). That rules out any account on which a defined field acts as a
generic cue, and it is independent of §6.1: the evidence comes from different
fields rather than an edit to one.

One of our four locked predictions failed. We derived Worst-off Priority as
positive, because the holder loses the most under overriding. It came out near
zero and split across presentation orders. A designer's reading of what a
definition implies did not predict the model, which is another reason to prefer
edits like FLIP that need no such reading.

**This bounds what the original block can claim.** Status-quo Preference, written
for this study and naming plainly what the items are about, moves keep-rate at
least as much as PD (+0.400 against +0.339) and is positive on all seven items.
Nothing in our evidence requires the block's ten fields in particular. §5 is best
described as follows: *a defined field whose stated meaning bears on the items
moves choices, and PD is one such field.*

![**Per-item effects.** (a) Exchanging the ends of PD's definition (CANON → FLIP) lowers the effect on all seven items. (b) Two invented fields in the same slot move every item in opposite directions, as their definitions state.](figures/fig2_items.pdf){width=100%}

### 6.3 The name is a poor guide to what the field does

On every item, "process-dominant" and "keep the existing arrangement" pick the
same option, so PD's effect is also consistent with a plain status-quo pressure.
§6.2 sharpens that worry. To separate the two readings, we wrote a **twin** of each
item that adds one clause saying the holder obtained the arrangement *outside*
its stated procedure (for example, booking a desk before the booking sheet
opened). A procedure-sensitive field should not protect such an arrangement. A
status-quo pressure should.

Two screening designations (417 calls, 17 wordings) failed to produce enough
twins on which the unprofiled model splits: three twins sat on a floor of
0.00–0.04 keep-rate, and others were determined by presentation order. We report
both stops. A one-directional test remained possible on the floored twins, where
the readings diverge: a status-quo pressure should lift keep-rate off the floor
and a procedure-sensitive field should not. Status-quo Preference served as a
positive control, and both fields first had to reproduce their base-item effects
(PD +0.350, Status-quo Preference +0.357).

| Lift on the three floored twins | Estimate | 95% CI (units) |
|---|---:|---|
| PD | +0.383 | [+0.292, +0.475] |
| Status-quo Preference | +0.133 | [+0.058, +0.208] |
| Difference | **−0.250** | [−0.358, −0.142] |

PD lifts the floored twins about three times as much as the explicit status-quo
field. Compared on the base item and its twin, a high-PD agent is **less**
deterred by the holder's procedural lapse than a high-status-quo agent (keep-rate
drops of 0.30 against 0.50 on one item; 0.15 against a rise of 0.05 on another).
Whatever *Procedural Dependence: 0.90* does to this model, it is not "care that
the procedure was followed". It behaves as a stronger and less discriminating
pressure to keep what exists.

This result rests on **two informative items**: the third twin is at 0.000 in all
four cells. Item-level analyses cannot support it (crossed CI [−0.500, 0.000]).
We report it as the direction of the evidence, not as an established effect. It
is enough to say that the field's name should not be trusted as a description of
its effect, and we attach no procedural-justice reading to PD.

### 6.4 Examples do almost what a stated rule does

A further question is whether the model *holds* something beyond the text it is
currently reading. If it did, a disposition might be inducible from examples
without being stated. We showed each agent five of its own earlier decisions,
taken from the frozen records of the prospective PD test (§5.2), with no field,
name or definition. We measured keep-rate on the
twins of §6.3, where keeping and following procedure come apart. The examples
came from the base versions, where the two coincide, so they say nothing about
how the holder came by the arrangement.
Three controls were fixed in advance. The harness holds no conversational state.
The read-out is a dimension the examples do not state. The examples are the
agent's actual frozen decisions rather than idealised ones. Each item was shown
in both option orders.

| Arm (user turn carries) | Keep-rate | vs bare item |
|---|---:|---|
| the bare item | 0.305 | — |
| five of the agent's own earlier decisions | 0.734 | +0.429 [+0.384, +0.473] |
| a one-sentence principle (below) | 0.768 | +0.463 [+0.418, +0.507] |

The principle reads: *"You place weight on fair procedure for its own sake: where
an arrangement was arrived at through a stated process, that matters
independently of the outcome it produces."* Examples move behaviour substantially
on a dimension they never state. The stated principle moves it slightly more. The gap is +0.034 [+0.004, +0.064] over units,
and it is not distinguishable from zero over items (crossed CI [−0.032, +0.098]).
Note also that a prose principle about *fair procedure* raises keeping on items
where the arrangement bypassed procedure, just as the PD field does (§6.3). It
also answers §5.1: on-topic prose moves keep-rate as strongly as the block.

A dose-response test would distinguish a fitted disposition from ordinary
context: the shift should track how many of the five examples kept. It did not
survive scrutiny. In a first run the slope appeared in the principle arm, whose
text is the same for every agent and cannot carry one, because example
composition was confounded with presentation order. A second run crossed order
with the covariate. The slope then moved to the examples arm (+0.080 [+0.018,
+0.137]) and vanished from the principle arm (−0.011). Example composition,
inherited from the frozen records, is unbalanced, however (3, 4, 17 and 16
agents across the four levels). Restricted to the two populated levels, the slope
is −0.011 [−0.066, +0.046]. A step carried by seven agents is not the graded
response a fitted disposition predicts.

We therefore report that examples induce the behaviour almost as well as a stated
rule, and that nothing establishes that anything was *fitted* rather than read.
The near-equality favours the plainer reading: the model acts on whatever
relevant text is in front of it.

## 7. How far do the results generalise across items?

With seven items, the prespecified unit-level tests support statements about
*these* items. The item-level analyses (§4.5; Appendix C) sort the claims into
three groups.

**Robust to resampling items:** pinning PD (+0.346), the field-versus-partner
difference (+0.375), the field factor of the 2×2 (+0.300), the definition exchange
(CANON − FLIP, −0.454, 7/7 items), INVERT, NONCE, the three invented fields that
moved as predicted (including the opposite-signed Numbers Count, 0/7), Mode of
Response, and the examples and principle arms against the bare item.

**Significant over units but not over items:** FLIP's own sign, PD on the second
provider (borderline), ID's swap TRUE arm and ID pinned on the second provider,
Tolerance for Asymmetry (whose
items disagree in sign), the gap between examples and a stated principle, and the
floor-lift dissociation of §6.3.

**Not significant under either:** the swap arm, the partner field, the partner at
the field's line, ID's swap difference, Worst-off Priority, and LL at 40 and 80
agents.

The central claim of this paper, that editing a field's definition sets the
direction of its effect while its name and numeral do not, rests on the first
group.

## 8. What the process taught

### 8.1 Presentation order must be crossed, not randomised

Two items are largely determined by which option is printed first: keep-rate
differs by 0.75 and 0.73 between orders. The paired contrasts are protected by
design, since each pair holds order fixed. Split by order, PD and three of the
four invented fields keep their sign in both orders. Worst-off Priority splits,
which is one more reason we claim nothing for it. *Unpaired* screens, however, were misled. An order-determined
item averages to about 0.50 and passes a dispersion rule meant to catch the
opposite problem, and one of our screens passed two items on which the model was
making no choice at all. The same defect recurred twice in new forms. In a judge
prompt, a model answered "B" in 94 of 120 trials, which voided that designation.
In a covariate, example composition proxied order and voided a prespecified
measure (§6.4). Randomising order makes a position-following responder *visible*.
Only crossing order with every variable that could correlate with it
*neutralises* it.

### 8.2 Automated design review is not a stable instrument

New materials had to pass an independent review by a separate model before
collection. The review caught real errors: a mismatch between reviewer prompt and
materials, an answer-key leak in a review packet, normative cues in option
wording. Its verdicts, however, were not a stable property of the material. One
four-item pool, reviewed four times on byte-identical text, was accepted three
times and then rejected. A later review of the seven-item pool asked for revision
and blocked two items that an earlier review had explicitly cleared. Across seven
reviews of that material there were three accepts and four requests to revise. We adopted, and recorded, the rule that review is a hard
gate for new material and advisory for material already accepted, and that
re-running a review to obtain a different verdict is forbidden.

### 8.3 An unprofiled floor is not a floor under profile

The twins of §6.3 sat at 0.00–0.04 keep-rate without a block and reached 0.775
with PD high. A screen's unprofiled baseline does not bound the profiled range,
so screens that reject floored items are more conservative than they need to be.

## 9. Limitations

**No moral claim.** The outcome is which option is chosen, recorded by a fixed
lookup. Nothing here says an agent behaves well or that outcomes improve.

**No human comparison.** No human data were collected.

**No evidence of understanding.** §6 shows that behaviour follows what a
definition *says*. It does not separate *reading an explanation* from *following
an instruction phrased as one*, and a definition such as "existing arrangements
stand unless there is strong reason to change them" is close to an instruction.
Our attempts to separate them did not succeed. Twins on which the readings diverge
could mostly not be built (§6.3). A test of whether the model could infer a
field's value from behaviour failed as an instrument, through the position bias
of §8.1. Examples and a stated rule produced nearly the same behaviour (§6.4).
The evidence is consistent with a model that acts on whatever relevant text is
present.

**One task family.** Seven items on one model and six on another, all short
allocation dilemmas with an incumbent holder and identical tied payoffs. This is
the principal limitation. A second family of 14 items (property, bodily,
allocative and scheduling dilemmas) passed review, and 11 of them dispersed, but
only 3 both dispersed and were robust to presentation order, against the 6
required, so that designation stopped at screening. Order-robustness
has to be designed into items, not discovered afterwards.

**One model for identification.** Every §6 result, and the swap and line controls
of §5, are on `gpt-5.4-mini`. The second-provider tests cover pinning only, and
effect sizes did not transfer.

**Tied payoffs by design.** Tied totals remove arithmetic as a reason for choice,
which is what makes the field the candidate cause. Whether definitions matter as
much when payoffs differ is untested.

**Partial map of the block.** Two further fields move keep-rate at 80 agents with
no swap control run, so their mechanism is unidentified. Four others are null in
a 25-agent sweep, which bounds them only weakly.

## 10. Conclusion

We asked which part of a structured prompt carries behaviour, and what about that
part does the carrying. On the evidence here, one field carries it. The effect
is not due to block presence, length, the line or a free-floating numeral. What
carries it is the field's **definition**. Exchange which end of the scale means
what, holding the name, line, numeral and every character fixed, and the effect
moves by −0.454 on every item. Fields we wrote ourselves mostly follow their own
definitions, in whichever direction those definitions point. Three of four locked
predictions held, and the one that failed was ours.

Two consequences follow for anyone who conditions agents on structured
descriptions. The first is that definitions deserve more care than names. A
field's name is a poor description of what it does: here the field named for
procedure acts as a pressure to keep what exists, and an invented field does its
job better. The second is that the claim "the model read the profile" is
testable. The controls in this paper need no access to model internals and cost
little. They include a replication gate, which in this work withdrew a field that a corrected test had certified and that its own swap control would have
confirmed.

## References

::: {#refs}
:::

## Appendix A. Full system prompt

The PD-high system prompt for one agent in the prospective PD test. The PD-low
prompt differs only in `Procedural Dependence: 0.90` → `0.10`. The G arm (§5.1)
replaces the profile section with the instruction quoted there.

```
You are participating in a decision-making simulation.

# Your decision-making profile

You process decisions according to the following characteristics, each
on a continuous [0, 1] scale. The low and high ends of each are
described. Your value on each characteristic is given.

 1. Legitimacy Locus: 0.79
    (0 = validity comes from institutional warrant and shared norms;
     1 = validity comes from personal judgment and self-authored endorsement)
 2. Constraint Sensitivity: 0.81
    (0 = influence registers as environmental feature;
     1 = even soft pressure registers as meaningful restriction)
 3. Response Threshold: 0.60
    (0 = high tolerance; only major violations activate response;
     1 = hair-trigger; minor deviations activate response)
 4. Mode of Response: 0.36
    (0 = internal, reflective, self-adjusting;
     1 = external, behavioural, confrontational)
 5. Relational Embedding: 0.45
    (0 = atomised, agent-centred, abstract-person model;
     1 = role-sensitive, relational, socially embedded)
 6. Procedural Dependence: 0.90
    (0 = outcome-dominant; results matter, methods are secondary;
     1 = process-dominant; fair procedure matters independently)
 7. Tolerance for Asymmetry: 0.42
    (0 = asymmetry is inherently suspect, default is symmetry;
     1 = asymmetry is accepted if intelligible, hierarchy is fine)
 8. Internalization Dependence: 0.77
    (0 = surface compliance is sufficient;
     1 = genuine endorsement and value-congruence required)
 9. Moral Scope: 0.73
    (0 = local, role-bound, partial, context-limited;
     1 = universalised, generalisable, broadly applied)
 10. Affective Weighting: 0.35
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
property; for axes marked LOW, that property is unstructured, unprotected,
or penalised. NEUTRAL means no institutional high or low stance is specified
on that axis; it does not remove your individual characteristics or the
facts of the task.

# Your task
Use the supplied information to make the requested decision. Do not infer
a demographic identity or additional facts. Return only the requested JSON
object.
```

In FLIP the three lines of entry 6 read `(0 = process-dominant; fair procedure
matters independently; 1 = outcome-dominant; results matter, methods are
secondary)` with the name and value unchanged. INVERT additionally renames the
entry *Outcome Dominance*, and NONCE renames it *Factor K* with the original
definition. Invented fields (§6.2) replace entry 10 with the field's name, value
and definition in the same format.

## Appendix B. Items

Every item is preceded by the same framing: *"You hold the role described. The
option you select will be carried out, not merely considered. Units are
artificial simulator credits, stipulated equally valuable to every person, and
all stated effects are certain and known to you. There are no hidden costs,
benefits or later effects beyond those described, and no one is pressuring you
toward either option. Decide on the situation as given."* In every item the keep
option gives the holder +1 and the others −4 between them, and the override
option gives the others +2 and the holder −5. The table gives each situation and
its twin clause (§6.3). Items marked g were used on `gpt-5.4-mini`, h on
`claude-haiku-4-5`.

| Item | Situation (base item) | Twin: how the holder came by it |
|:----------------|:---------------------------------------------|:-------------------------------|
| desk_booking (g, h) | One bookable desk left for the week; one person booked it and wants to keep it; two visiting staff otherwise work from a corridor bench. | entered their name the Friday before the booking sheet opened |
| storage_unit (g, h) | A community centre needs a storage unit for winter supplies; one unit is leased by a resident who wants to keep it; supplies otherwise spoil outdoors. | was given the unit ahead of the waiting list by an acquaintance in the office |
| tool_library (g, h) | A repair session needs a press a member lent under terms letting them withdraw it; they want it back this week; three repairs otherwise cannot proceed. | lent under terms fixing the loan until month end, and asks for it back two weeks early |
| on_call (g) | An on-call slot is unfilled for one night; one off-rota person wants the night clear; leaving it unfilled sends two callouts to a team an hour away. | is off-rota through a swap arranged privately and never entered on the form |
| meeting_room (g, h) | A room is held for one group's weekly session; they want to keep it; two other groups need the room this week. | entered its slot in the diary itself, before the room committee met |
| rest_break (g) | One mandatory rest slot left in a long shift; one worker wants it; assigning it elsewhere lets two tasks finish. | has already taken their own slot |
| weekend_rota (g, h) | A service needs one more person on Saturday; one staff member wants the day free; otherwise two appointments are put back. | did not file the request form by its deadline |
| ward_transfer (h) | A ward is over capacity; one patient has a single room and wants to keep it; two patients wait on trolleys. | — |

The profile-versus-instruction comparison on `gpt-5.4-mini` (§5.1) also used an
eighth item, `sample_draw`. Verbatim option texts are in the repository.

## Appendix C. Item-level robustness

Every contrast is estimated on `gpt-5.4-mini` with 40 agents unless marked. *Unit*
is the prespecified interval over agent-item units. *Crossed* resamples agents and
items independently. *t p* is from a one-sample *t*-test over per-item effects.
Items gives the per-item signs. The contrasts marked † are new in this paper. All
are computed from the frozen records by `paper_item_robustness.py`, with zero API
calls and seed 2026092301. Unit intervals are recomputed here with one common
seed. They differ from the designation reports quoted in the main text by at most
0.01, through resampling alone. Point estimates are identical.

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
| INVERT | −0.614 | [−0.675, −0.557] | [−0.771, −0.457] | < 0.001 | 0 / 7 |
| NONCE | +0.175 | [+0.114, +0.236] | [+0.025, +0.325] | 0.048 | 6 / 1 |
| CANON − FLIP † | +0.454 | [+0.361, +0.546] | [+0.179, +0.739] | 0.019 | 7 / 0 |
| CANON − NONCE † | +0.164 | [+0.082, +0.246] | [+0.011, +0.321] | 0.024 | 6 / 0 |
| Status-quo Preference | +0.400 | [+0.336, +0.464] | [+0.229, +0.579] | 0.003 | 7 / 0 |
| Stated-Wish Deference | +0.307 | [+0.254, +0.361] | [+0.179, +0.436] | 0.002 | 7 / 0 |
| Numbers Count | −0.246 | [−0.311, −0.182] | [−0.386, −0.114] | 0.007 | 0 / 7 |
| Worst-off Priority | −0.064 | [−0.129, 0.000] | [−0.218, +0.096] | 0.403 | 2 / 4 |
| Status-quo Preference − Numbers Count † | +0.646 | [+0.561, +0.736] | [+0.425, +0.857] | < 0.001 | 7 / 0 |
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

The record spans 35,879 API calls across 56 designations, with $45.05 of
accounted spend. Every designation is frozen before collection: its request
schedule, population, locked predictions and decision rule are hashed, and the
hash is checked at dispatch. Per-call records are write-once. Two calls are
preserved transport failures, at call 689 of 2,801 in `coordinate_sweep_r1` and
at call 294 of 840 in `precipitation_r1`. Each closed its designation, which was
re-designated without reusing any records. Power simulations and offline
analyses, including Appendix C, are reproducible from committed modules. The
principal designations are `phase4b_gpt_r2` and `phase4b_profiled_r1` (§5.1),
`pd_prospective_r1` and `label_semantics_r1` (§5.2), `label_semantics_r2` (ID and
LL), `position_counterbalance_r1` (§5.3), `coordinate_sweep_r2` (sweep),
`parameter_followup_r1`/`r2` (80-agent pins), `pd_crossmodel_r1` and
`id_crossmodel_r1` (§5.6), `semantics_r1` (§6.1), `probe_fields_r1` (§6.2),
`floor_lift_r1` (§6.3) and `precipitation_r3` (§6.4).
