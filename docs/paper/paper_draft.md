# Does the Model Read the Field, or Just the Numeral?

## Isolating What Carries Behaviour in a Structured Prompt

**Tommaso Piero Palamenga** — Bocconi University

*Draft, 22 September 2026. Every figure is traceable to a frozen per-call record
in the accompanying repository; designations are named inline so each claim can
be checked against its own assessment. The long-form draft this was cut from,
containing the full coordinate map and the complete methodological record, is
retained as `paper_full_record.md`.*

> **Relation to the author's thesis.** This paper and the author's undergraduate
> thesis draw on one body of evidence and are separate documents. The thesis
> (submitted and frozen) presents a ten-parameter encoding framework on evidence
> to 18 September 2026. **This paper is not a longer version of it.** It makes a
> narrower claim on a wider evidence base, and reports results collected
> afterwards that *constrain* that framework. Neither document is edited to agree
> with the other; see `../PROJECT_SPLIT.md`.

---

## Abstract

Practitioners condition language-model agents on structured descriptions —
personas, trait vectors, configuration blocks — and infer from a behavioural
change that the model read the description as intended. That inference is rarely
tested, because a block that shifts behaviour could be acting through its labels,
through the mere presence of structured text, through verbosity, or through an
extreme numeral sitting anywhere in the prompt.

We separate these. Our method has three components: **pinning** one field to its
endpoints while holding every other byte of the prompt identical; a **swap
control** that moves the identical numeral onto a field measured inert, holding
the numeral multiset, block length and field order constant; and a **replication
gate** requiring an effect to reproduce before its swap control is interpretable.

Applied to a ten-field encoding over a family of workplace-resource decisions,
this yields a field-bound effect of +0.339 on a deterministic good/bad outcome,
with the same numeral on the partner field giving −0.036 and the direct
difference of differences +0.375 [+0.286, +0.464]. It replicates on a second
provider and survives a 2×2 separating the field from the line it occupies.

**We then ask what about the field carries it, and the answer is its stated
meaning.** Exchanging only the two endpoint texts — holding the name, the line,
the numeral and the block's entire character multiset fixed — **reverses** the
effect, from +0.339 to −0.114 [−0.179, −0.050]. No account resting on numeric
extremity or name-association survives that: extremity predicts every arm
positive, and an identical printed name cannot produce opposite signs.

**Three results bound what this licenses, and we report them as prominently as
the finding.** Four fields we invented for the purpose, none in the encoding,
move choices as *their* glosses predict — one more strongly than the verified
parameter (+0.400 against +0.339) — so the finding concerns glossed fields in
general and does not privilege this encoding. The verified parameter proves
*less* sensitive to whether a stated procedure was honoured than an explicit
status-quo field is, so it does not behave as its name suggests. And showing an
agent five of its own prior decisions induces the behaviour within 0.034 of what
stating the rule achieves, which favours a model reading whatever relevant text
is present over one that has acquired a disposition.

**Scope, stated here rather than deferred.** All results come from a single
family of seven workplace-resource vignettes with payoff totals tied by
construction; an attempt to build a second family was stopped at its dispersion
screen and is reported. No human comparison of any kind was collected. Every
outcome label is computed deterministically from a stipulated transition and
never read from model text. We establish no moral improvement, no human
resemblance and no semantic understanding. The contribution is an identification
method, a demonstration that it retracts its own findings, and a bounded
empirical claim about what in a structured prompt does the work.

---

## 1. The inference everyone makes

Give a language model a block of structured text — a persona, a trait vector, a
configuration — and its behaviour changes. The near-universal next step is to
attribute the change to the *content* of the block: the model read that this
agent is cautious, or process-oriented, and acted accordingly.

That step is an inference, and it has at least four rivals. The block adds text,
and more text changes behaviour. The block adds structure, and structured text is
read differently from prose. The block contains an extreme numeral, and extreme
numerals are salient wherever they sit. The block contains a label the model
associates with a disposition, independently of anything the block says that
label means.

These are not pedantic alternatives. Each predicts the same observation — a
behavioural shift when the block is present — and they license entirely different
conclusions about what a practitioner is building. Our question is narrow:

> **Which part of a structured prompt carries the behaviour, and what about that
> part does the carrying?**

### 1.1 What this paper does

We answer for one encoding on one task family, and treat the narrowness as the
price of the answer rather than an embarrassment. The identification requires
holding every byte of the prompt constant except one, which requires a frozen
prompt, a deterministic outcome and a fixed item set. Nothing about that design
generalises for free, and §7 says so at length.

The method's most important property is that **it can fail**. §4.4 reports a
field that cleared a corrected significance bar, then dissolved on a larger
sample of the same model, and was withdrawn. We regard that as the paper's
strongest evidence that the rest of it can be believed.

### 1.2 Contributions

- **A separation method** — pinning, a numeral-identical swap control, and a
  replication gate — applicable to any prompt with addressable fields.
- **A reversal**: exchanging what a scale is *said to mean*, holding its name,
  line and numeral fixed, reverses the effect. This excludes field-weighted
  extremity, the mechanism an earlier version of this work could not rule out.
- **A bound on the same result**: fields we invented move choices as their
  glosses predict, one more strongly than the encoding's own parameter.
- **A retraction**, made by the method's own gate, of a field it had certified.
- **A negative methodological finding**: automated design review returns opposite
  verdicts on byte-identical material.

### 1.3 What we do not claim

No moral quality, no human resemblance, no semantic understanding, and no
generality beyond the tested family. §7 states each as a constraint on what may
be concluded rather than as a caveat.

---

## 2. Setup

### 2.1 The decision task

An agent faces a two-option choice in which both options set aside something a
reasonable person could hold binding: one party's claim, or an outcome for
others. There is deliberately no option that sets aside nothing.

**Payoff totals are tied by construction** — each option's stipulated effects sum
to −3 — so welfare-maximisation, minimax and best-case reasoning are all
indifferent between them. This is the design's load-bearing control: it removes
arithmetic as the operative variable, leaving the prompt field as the candidate.

Seven items survived screening on the calibration model. All are
workplace-resource vignettes; all state consequences in artificial units declared
equally valuable to every person.

### 2.2 The outcome

Each action is classified `good` or `not_good` by a deterministic rule reading
the action's declared properties — whether it deceives, coerces or treats
equivalent claims unequally — and never the model's text. The model chooses an
option identifier; the label is a lookup. **No moral judgement is made by any
model at any point**, ours or the subject's.

### 2.3 The encoding

Ten fields, each rendered as a name, a value in [0,1] and a two-line gloss naming
what each end of the scale means:

```
 6. Procedural Dependence: 0.90
    (0 = outcome-dominant; results matter, methods are secondary;
     1 = process-dominant; fair procedure matters independently)
```

The encoding's provenance is not this paper's subject. What matters is that it
provides *addressable fields with declared meanings* — the object the method
operates on.

### 2.4 Screening before profiling

Items are screened for baseline dispersion before any profiled study, and
screening is on dispersion only, never on outcomes. This rule exists because four
early designs returned nulls later traced to deterministic unprofiled baselines:
an item on which the model always answers the same way cannot show any effect,
and spending on one is a loss with no information.

---

## 3. Method

### 3.1 Pinning

One field is set to 0.10 and to 0.90 while the other nine keep the values drawn
for that agent. The two prompts differ on exactly one line — verified per agent,
byte for byte — and the user turn is identical. Each agent meets both levels, so
the contrast is within-agent and within-item.

### 3.2 The swap control

Pinning shows that *a* numeral moved the outcome, not that the *field* did. The
swap control puts the identical numeral on a partner field measured inert:

```
TRUE(L)   L on the tested field,   the drawn partner value on the partner
SWAP(L)   the drawn partner value on the tested field,   L on the partner
```

Both arms carry the same multiset of ten numbers across the same ten lines in the
same order. Block presence, length and numeral extremity are held **by
construction**; only which field holds the value differs.

The partner field is itself pinned in its own right (§4.5), which earlier
versions of this work assumed rather than tested.

### 3.3 The replication gate

A swap control is interpretable only if the effect it explains reproduces in the
same designation. A null swap beside an unreplicated TRUE arm reads as "the field
carries it" when it may mean "there was nothing to carry". §4.4 is the case where
this mattered.

### 3.4 Analysis, and one inference we do not make

Paired sign tests with Holm correction over each designation's contrast family,
an item-consistency requirement, and 95% unit-bootstrap intervals over agent-item
pairs. Power is simulated against measured per-item baselines before collection.

**We never infer a difference from one arm being significant while another is
not.** That inference was made once in this project, about a field whose TRUE arm
cleared correction and whose SWAP arm did not, and it had to be withdrawn. Every
comparison here is a direct within-unit difference of differences with its own
interval.

### 3.5 Prespecification and the ledger

Every designation is frozen before collection: its jobs, prompts, population and
locked predictions are hashed, and the hash is checked at dispatch. Failed calls
are preserved at full reservation and **never retried**; a designation halted by
a failure is closed rather than resumed. One transport failure occurred during
this work; its designation was closed and re-designated, with none of its records
reused.

---

## 4. Which field carries the behaviour?

### 4.1 Profiles change the outcome, and an instruction does not reproduce it

| Model | no profile | explicit instruction | numeric profile | paired E−G | Holm |
|---|---:|---:|---:|---:|---:|
| `claude-haiku-4-5` | 0.367 | 0.429 | 0.600 | **+0.171** | 0.000112 |
| `gpt-5.4-mini` | 0.395 | **0.378** | 0.606 | **+0.228** | ~0 |

The instruction arm states the target behaviour in plain English. On the
calibration model it lands *below* the unprofiled baseline. The numeric profile
moves the outcome; saying the same thing in prose does not.

### 4.2 The effect is bound to one field

`pd_prospective_r1` pinned Procedural Dependence with a direction derived from
the field's definition and locked in source before collection: **+0.346**, Holm
~0, six of seven items positive.

The swap control gives **−0.036** (n.s.) on the partner field, and the direct
within-unit difference of differences is **+0.375 [+0.286, +0.464]**, six items
positive to one negative.

A second field reached +0.111 to +0.143 pinned, but its direct difference is
**+0.064 [−0.014, +0.146]** — the interval includes zero. It is reported as a
**candidate**, not a verified field effect. This is the distinction the
significance-versus-non-significance inference obscured.

### 4.3 It is not the line the field occupies

The swapped fields sit at different lines, so a primacy effect over a numbered
list would mimic the result. A 2×2 crossing *which field holds the value* with
*which line it occupies*:

| Cell | Value on | At line | Effect | Holm | Items |
|---|---|---:|---:|---:|---|
| **A** | tested field | 6 | **+0.393** | ~0 | 7+/0− |
| **C** | tested field | 10 | **+0.271** | ~0 | 5+/1− |
| B | partner | 10 | +0.061 | 0.157 | 6+/1− |
| D | partner | 6 | +0.004 | 1.000 | 3+/2− |

Cell D is decisive: the value at the privileged line, on the partner field, gives
+0.004. Keep the field and move it four lines down (C) and the effect survives.
**Field factor +0.300; position factor +0.032** — small, not zero, so we do not
round it away.

### 4.4 A field the method retracted

The result we consider most informative is a withdrawal. A third field cleared a
Holm-corrected bar at 25 agents (−0.131, Holm 0.00082) with the most
directionally consistent result in its sweep. At 40 agents on the same model it
measured **−0.014** (Holm 0.708). Its post-hoc correlation had been **+0.271**.
Three measurements, three answers: positive, negative, null. A fourth at 80
agents gave −0.036 [−0.080, +0.009].

**It failed on the larger sample, not the smaller** — this is not a power
failure. Had its swap control run without a replication gate, its null swap would
have read as evidence that its field carried the effect. We withdraw it, and it
is not reinstated by majority vote across measurements.

### 4.5 The partner field, tested directly

Every swap control assumes the partner field does not itself carry the outcome.
That assumption rested on a by-product measurement. Pinned in its own right at 80
agents it is flat: **+0.016 [−0.027, +0.057], 90% equivalence bound 0.050** — the
tightest bound in this work.

This supports the controls without proving them: they additionally assume the
partner's *slot* is a fair comparison, and §5.2 bears on that, since an invented
field placed in the same slot reached +0.400. The slot can carry an effect; the
partner's own gloss does not produce one.

### 4.6 Cross-provider

Both surviving fields were pinned on a second provider over its own screened
items: **+0.133** (p = 0.00031) and **+0.075** (p = 0.0328). Both effects shrink —
to ~38% and ~68% of their calibration-model size. **What replicates is direction
and decision rule, not magnitude**, and no swap control was run there, so these
license "the field moves the outcome on this model too" and nothing further.

---

## 5. What about the field carries it?

§4 localises the effect to one labelled, glossed field. It cannot say what about
that field does the work. Three readings survive and they differ once the field's
own text is edited: the model reads the **stated meaning**; the model responds to
the **name** and the gloss is decoration; or an extreme numeral in a salient slot
does it all — **field-weighted extremity**, which no design in §4 excludes.

### 5.1 Reversing the gloss reverses the effect

`semantics_r1` pinned the field under four renderings of its own entry, nine
other entries and the user turn byte-identical, 40 fresh agents:

| Variant | Entry reads | Gloss | Effect | 95% CI | Items |
|---|---|---|---:|---|---|
| CANON | Procedural Dependence | canonical | +0.3393 | [+0.2714, +0.4036] | 6+/1− |
| **FLIP** | **Procedural Dependence** | **ends exchanged** | **−0.1143** | **[−0.1786, −0.0500]** | 1+/5− |
| INVERT | Outcome Dominance | ends exchanged | −0.6143 | [−0.6714, −0.5536] | **0+/7−** |
| NONCE | Factor K | canonical | +0.1750 | [+0.1143, +0.2357] | 6+/1− |

CANON is a replication gate and it holds at +0.3393 against +0.339 and +0.346 in
earlier designations, on a new population. Predictions were locked in source
under a published hash and **differ in sign**, which makes the design decisive
rather than suggestive.

**FLIP is the decisive cell.** The name, line, printed numeral and the block's
entire character multiset are identical to CANON — the edit is a pure exchange of
two strings, verified as an involution — and the effect reverses.
Field-weighted extremity predicts every arm positive; two are negative. A
name-association account cannot produce +0.339 and −0.114 from an identical
printed name. **Both are excluded.**

FLIP also requires no human judgement that two wordings are equivalent. INVERT
does, and that premise is soft — this work has repeatedly found reviewer
judgements about materials failing to predict model behaviour — which is why
FLIP, not the larger INVERT effect, carries the argument.

**Name and gloss separate.** They conflict in FLIP and partly cancel (−0.114);
they agree in INVERT and compose (−0.614, the largest effect measured here); and
with the name removed entirely, **about 52% of the effect survives** (+0.175).
The gloss dominates when the two disagree.

### 5.2 The same is true of fields we invented, which bounds the claim

If explanations are followed, the question becomes whether the encoding's fields
are special. We wrote four fields **not** in the encoding, placed each in the
partner slot and pinned them identically. Signs were derived from each gloss and
locked in advance; one was written to point the *opposite* way.

| Probe field | Predicted | Effect | 95% CI | Items |
|---|---|---:|---|---|
| Status-quo Preference | + | **+0.4000** | [+0.3357, +0.4643] | 7+/0− |
| Stated-Wish Deference | + | +0.3071 | [+0.2536, +0.3607] | 7+/0− |
| **Numbers Count** | **negative** | **−0.2464** | [−0.3107, −0.1821] | 0+/7− |
| Worst-off Priority | + | −0.0643 | [−0.1286, 0.0000] | 2+/4− |

Two fields in the same slot, same format, same numerals, moved choices in
**opposite directions**, each as its own gloss predicted. This is a second,
independent demonstration of §5.1 — across fields rather than within one — and it
rules out any account on which a glossed field acts as a generic cue.

**It also bounds what the encoding can claim.** Status-quo Preference, written in
an afternoon and naming what these items are plainly about, reaches **+0.400
against the encoding parameter's +0.339**, consistent on all seven items where
the parameter is 6+/1−. **Nothing in our evidence requires these ten fields in
particular.** The honest description of §4 is: *a glossed field whose stated
meaning bears on the items moves choices, and the encoding's parameter is one
such field.*

One locked prediction failed, and it was ours. Worst-off Priority was derived
positive from the stipulated payoffs and came out −0.064, failing correction and
splitting across presentation orders. We claim nothing for it.

### 5.3 The parameter does not behave as its name suggests

On every item, "process-dominant" and "keep the existing arrangement" select the
same option, so the effect is consistent with a status-quo disposition — a worry
§5.2 sharpens, since an explicit status-quo field outperforms the parameter. We
built items to separate them: each vignette gained a twin whose only difference
was a clause stating that the holder came by the arrangement outside its stated
procedure.

Two screening designations (417 calls) failed to produce enough usable twins:
eleven wordings drove three items to an unprofiled floor of 0.00–0.04, and others
proved presentation-order determined. **We report both stops rather than the
wordings that survived.**

A one-directional test remained possible on the floored twins, where the two
readings diverge: a status-quo disposition should lift the keep-rate off the
floor; a procedure-sensitive one should not. With an explicit status-quo field as
positive control and both base arms reproducing as a gate:

| Lift on the floored twins | Estimate | 95% CI |
|---|---:|---|
| the encoding's parameter | +0.3833 | [+0.2917, +0.4750] |
| Status-quo Preference | +0.1333 | [+0.0583, +0.2083] |
| **Difference** | **−0.2500** | **[−0.3583, −0.1417]** |

**The two dissociate** — the cleanest such result here, and a direct answer to the
worry. But the dissociation runs *against* the reading the parameter's name
invites. Comparing each field's high arm across versions, a high-parameter agent
is **less** deterred by the holder's procedural lapse than a high-status-quo
agent (−0.30 against −0.50 on one item; −0.15 against +0.05 on another).

Whatever the parameter does to this model, it is not *care that the procedure was
followed*. **We attach no procedural-justice interpretation to it**, and this
result is evidence against one. Two items carry the comparison.

### 5.4 Examples do almost exactly what a rule does

If a field becomes something the model *holds* rather than reads, the disposition
should be inducible by examples rather than statement. We showed an agent five of
its own previously recorded decisions — no rule, no field name, no gloss — and
measured behaviour on the provenance twins of §5.3, items the examples never
covered and on which they are silent.

Three controls were fixed in advance: the harness holds no conversational state,
so withdrawn material is genuinely absent rather than earlier in context; the
read-out is a dimension the examples do not state; and the examples are actual
frozen decisions rather than idealised transcripts, since constructing clean
examples would be writing the rule the design tests for.

| Arm | Keep-rate | vs bare item |
|---|---:|---:|
| bare item | 0.305 | — |
| **five of the agent's own prior decisions** | **0.734** | **+0.429** [+0.384, +0.473] |
| **the principle stated** | **0.768** | **+0.463** [+0.418, +0.507] |

Examples move behaviour substantially on items they never covered. **An explicit
principle moves it slightly more, and the gap is +0.034 [+0.004, +0.064].**

The measure that would distinguish a fitted disposition from ordinary context did
not survive scrutiny. If a disposition were being fitted, the shift should track
how many of the five examples leaned one way. We prespecified that the
stated-principle arm *cannot* produce such a slope — its text is identical for
every agent — and that a slope there would void the measure. In a first run the
slope appeared there, because example composition was confounded with agent
index, which set presentation order. A second run crossing order with the
covariate moved the slope to the arm that can carry it (+0.080 [+0.018, +0.137])
and left the other flat (−0.011).

**It still does not support the claim.** Example composition, inherited from the
frozen transcripts, is badly unbalanced, and restricted to the two populated
levels the slope is **−0.011 [−0.066, +0.046]**. A graded response is what a
fitted disposition predicts; a step separating seven sparse agents from everyone
else is equally what a small-sample artefact predicts.

We therefore report: examples induce the behaviour almost as well as stating the
rule; nothing establishes that anything was fitted rather than read; and the
near-equality favours the reading on which the model acts on whatever relevant
text is in front of it.

---

## 6. What the process taught

### 6.1 Automated design review is not a stable instrument

Every designation introducing new material passed an independent review gate, and
the gate caught genuine errors: a reviewer-prompt mismatch, an answer-key leak in
a review packet, normative cues in option wording, and — in this work's final
designation — an implicit incumbency an authoring check could not express.

**Its verdicts are not a stable property of the material.** One item set was
reviewed four times on byte-identical text: accepted, accepted, accepted, then
rejected, with the rejection blocking two items an earlier review had explicitly
cleared. Across seven reviews of that set: three accepts, four revises.

We therefore treat review as **advisory for materials already accepted** and as a
hard gate only for new material — a rule adopted mid-project and recorded with
the evidence that prompted it.

### 6.2 Presentation order, three times

Two items in the pool are largely determined by which option is printed first
(gaps 0.75 and 0.73), unrecorded until this work. **No result here is affected**:
every contrast is paired within agent with order held fixed inside the pair, and
each retains its sign within both orders. But *unpaired* screens are destroyed by
it — an order-determined item averages to ~0.50 and passes a band rule designed
to catch the opposite condition, which is how one of our screens returned a false
pass on two items making no choice at all.

The defect then recurred twice in new disguises: in a judge prompt, where a model
answered "B" in 94 of 120 trials and 0/19 when the answer was A, voiding that
designation entirely; and in a covariate, where example composition proxied order
and voided a prespecified measure. **Presentation order must be crossed with
anything that could correlate with it, not merely randomised.**

### 6.3 Refusals that shaped the record

Failed calls are preserved at full reservation and never retried; a halted
designation is closed rather than resumed. A provenance guard refused a release
because a docstring in a hash-pinned module had been edited; **the pinned bytes
were restored rather than the check loosened**, and that module still carries a
retired project name in one comment as a result.

---

## 7. Limitations

Stated as constraints on what may be concluded.

**No moral claim of any kind.** Every outcome is a deterministic lookup from a
stipulated table. We measure which action is chosen, never whether it is good.

**No human comparison.** None was collected, anywhere in this work.

**No evidence of understanding, and the attempts are reported.** §5.1 shows
behaviour follows what a gloss *says*. It does not distinguish *reading an
explanation* from *following an instruction phrased as one* — and a field reading
"existing arrangements stand unless there is strong reason to change them" is
close to an instruction. Four designs were built to separate them and none
succeeded: defeasibility items could not be built (§5.3), inference from
behaviour failed as an instrument (§6.2), and induction from examples produced
behaviour within 0.034 of stating the rule (§5.4). **The accumulated evidence is
consistent with a model that acts on whatever relevant text is present, and we
report that as the reading our own attempts failed to displace.**

**The fields are not privileged.** §5.2 finds an invented field outperforming the
encoding's parameter on the same items.

**One task family — the principal limitation.** Seven items on one model, six on
another; all workplace-resource vignettes with an incumbent holder and an
identical tied-payoff structure. **A second family was attempted and stopped**:
14 civic-allocation candidates passed an accepted review, 11 of 14 dispersed, but
only 3 were order-robust against 6 required. The failure differs from the
saturation that blocked earlier attempts and is specific — order-robustness must
be designed in rather than discovered — but the limitation stands.

**Single model for identification.** Every §5 result is on one model; the
cross-provider work of §4.6 covers §4 only.

**Two fields are pinned without swap controls.** Two further fields move the
outcome at 80 agents (−0.111 and −0.073) with no swap control run. They sit where
the verified field sat before its own control: real effects, mechanism
unidentified.

**The configuration counterfactual was never run.** Every call used a neutral
configuration on all five axes.

---

## 8. Related work

> **Citation status: verified.** Every reference was checked against its source
> for existence, authorship, year, venue, and that the paper makes the claim
> attributed to it. Two supplied citations did not exist and were **removed
> rather than replaced**; four verified entries needed correction. The record is
> `citation_verification.md`. Two claims in this section are ours rather than the
> literature's — that field-level identification under byte-held surface form is
> scarce for closed models, and that the replication gate is not represented
> elsewhere — and both keep their hedges, since absence of evidence in a search
> is not evidence of absence.

The move this paper depends on is visible across several literatures: **treating
a prompt not as a monolithic instruction but as a causal object with separable
components.** Our contribution sits at a specific gap in that movement.

**Prompt sensitivity** establishes that surface form matters enormously —
example order can move performance from near-random to near-state-of-the-art (Lu
et al. 2021); formatting alone spans large accuracy ranges with meaning held
constant (Sclar et al. 2023); the same holds for wording, structure and
punctuation (Razavi et al. 2025); and neither scale nor instruction tuning
removes the brittleness (Chatterjee et al. 2024). This literature motivates
holding surface form constant to the byte, which is what our method does; it does
not attempt field-level attribution.

**Label binding** supplies the deflationary pressure we take seriously. Min et
al. (2022) show that randomly replacing demonstration labels barely hurts
performance; Wei et al. (2023) that large models override semantic priors on
unrelated labels; Liu (2026) that output binds to the demonstrated token
inventory. We use these *against* our own result: they are why §1.3 disclaims
semantic understanding and why §5.4's near-equality of examples and rule is
reported as favouring the deflationary reading.

**Causal localisation** in mechanistic interpretability shares our logic on the
other side of the model — patching, mediation and tracing unified as causal
abstraction (Geiger et al. 2023), with known sensitivity to variant choice (Zhang
& Nanda 2023) and to hidden interaction effects (Vaidyanathan et al. 2026). Ours
is the input-side analogue: the same ambition to localise, without access to
activations.

**Persona conditioning** is where the gap is clearest. De Araujo and Roth (2024)
run 162 personas across 7 models with both an empty-persona baseline and 30
paraphrases of "a helpful assistant" as control, finding personas show greater
variability than the control. That is a conditioned-against-unconditioned
comparison. What is scarce is work isolating *which field* within a conditioning
block carries the effect while holding every other byte fixed.

**Moral evaluation** provides our task framing (Rao et al. 2023) and a
cross-model caution: Sachdeva and van Nuenen (2025) find low inter-model
agreement on everyday moral dilemmas despite moderate-to-high self-consistency,
with model judgements diverging substantially from human evaluations. That bears
directly on §4.6's cross-model shrinkage — a smaller effect on a second model is
what one should expect if models disagree on the underlying judgements.

---

## 9. Conclusion

We asked which part of a structured prompt carries behaviour and what about that
part does the carrying.

**The answer to the first is one labelled, glossed field** — not block presence,
not verbosity, not the line it occupies, and not a free-floating numeral. **The
answer to the second is the field's stated meaning**: exchanging what the two ends
of a scale are said to mean, holding the name, line, numeral and character
multiset fixed, reverses the effect. No account resting on extremity or
name-association produces that.

**Three results bound it.** Fields we invented move choices as their glosses
predict, one more strongly than the encoding's parameter, so the finding concerns
glossed fields rather than this encoding. That parameter proves less sensitive to
procedure than an explicit status-quo field, so it does not behave as its name
suggests. And examples induce the behaviour within 0.034 of what stating the rule
achieves, which favours reading over holding.

The result we would most want carried forward is a **withdrawal**. A field
cleared a corrected significance bar with the most directionally consistent
result in its sweep and dissolved on a larger sample of the same model. Its swap
control was null — the signature of a real field-bound effect — and only the
replication gate distinguished the two cases.

Methods that can only confirm are weaker than methods that can kill their own
findings. We report one finding dying, five designations that failed to establish
what they were built for, two locked predictions of our own that came out wrong,
a prespecified measure that voided itself, and a transport failure that closed a
designation we re-designated rather than resumed.

---

## Appendix A — Scale of the record

35,879 API calls across 56 designations with frozen results, $45.05 accounted
spend. All per-call records are write-once with preserved failures; releases are
hash-pinned to their source; power simulations and offline rescorings are
reproducible from committed modules. One call is a preserved transport failure,
never retried. Per-designation table: `paper_full_record.md` Appendix A.

## Appendix B — Prespecification

Locked predictions, content hashes and decision rules for every designation are
in the repository under `experiments/`, each frozen before its collection.

## Appendix C — Items

Seven base items, their provenance twins, and the four probe fields:
`paper_full_record.md` Appendix C.
