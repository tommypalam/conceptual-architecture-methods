# Phase 4B closure — 16 September 2026

Phase 4B, **the central moral experiment**, is closed with an affirmative result
on its stated question and one named question left open.

The question was fixed in CLAUDE.md before any of this ran: **do parameter
profiles change the deterministic good/bad classification, not merely the
choice?**

**The answer is yes, on two models from different providers, and an explicit
ethical instruction does not reproduce it.**

---

## The result

### `claude-haiku-4-5` — [phase4b_profiled_r1](phase4b_profiled_r1/ASSESSMENT.md)

| Arm | Good-rate | n | vs U | p |
|---|---:|---:|---:|---:|
| U no profile | 0.367 | 150 | — | — |
| G ethical guidance | 0.429 | 240 | +0.062 | 0.244 |
| **E numeric profile** | **0.600** | 240 | **+0.233** | **0.000008** |

Paired E vs G: **+0.171**, 240 pairs, **pooled Holm 0.000112**, 4 of 6 items
positive.

### `gpt-5.4-mini` — the calibration model — [phase4b_gpt_r2](phase4b_gpt_r2/ASSESSMENT.md)

| Arm | Good-rate | n | vs U | p |
|---|---:|---:|---:|---:|
| G ethical guidance | 0.378 | 320 | −0.017 | 0.712 |
| U no profile | 0.395 | 200 | — | — |
| **E numeric profile** | **0.606** | 320 | **+0.211** | **0.0000038** |

Paired E vs G: **+0.228**, 320 pairs, **pooled Holm ≈ 0**, **7 of 8 items
positive**.

**Prespecified same-item subgroup** — the five items dispersing on both models,
declared before collection: **+0.255, p < 10⁻⁷**.

### What makes this the result rather than a rate

The **G arm is the control that carries the claim**. It states the target
behaviour in plain English — weigh everyone's interests, avoid harm, deception,
coercion and unequal treatment — inherited verbatim from
`phase4_capstone_model2.GUIDANCE` and asserted identical at gate time.

On haiku it moves the headline by +0.062 (p = 0.244). **On the calibration model
it lands *below* the unprofiled baseline**, −0.017 (p = 0.712).

Ten numbers carrying no ethical vocabulary move it by +0.21 on both.

---

## The open question, named

**Is the model reading the parameters, or does any structured numeric block do
similar work?**

[phase4b_permutation_r2](phase4b_permutation_r2/ASSESSMENT.md) built the control:
the same ten numbers per agent, permuted across the ten labels by a fixed
derangement. Verified identical user text, system-prompt length and numeral
multiset; only the label-to-value assignment differs.

| Arm | Good-rate | vs U | p |
|---|---:|---:|---:|
| U no block | 0.400 | — | — |
| P scrambled labels | 0.475 | +0.075 | 0.122 |
| E correct labels | 0.564 | **+0.164** | **0.00074** |

Paired E−P **+0.089**, raw p = 0.0105, **pooled Holm 0.084** — the prespecified
rule required Holm < 0.05 **and** ≥ 4 of 7 items agreeing. Consistency passed;
significance did not. **Under the declared criterion this is a null.**

**Reading:** the effect appears **split** between block-presence and
label-mapping. A scrambled block does not clear baseline; a correctly-labelled
one does; the difference between them is not resolved at n = 280.

The protocol recorded the power limitation **before collection** — 7/12 at a gap
of 0.10 — and the observed gap was 0.089.

[phase4b_permutation_r3](phase4b_permutation_r3/ASSESSMENT.md) re-powered it at
120 agents (16/16) and was **stopped by a review that contradicted r2's review of
the byte-identical packet**. Proceeding would have meant invoking the advisory
amendment selectively, so it did not proceed.

**This caveat is published standing.** It is a real limit on interpretation, not
on the data.

---

## Supporting evidence

**[phase4b_grand_r1](phase4b_grand_r1/ASSESSMENT.md)** — 12 items × 3 models,
901 calls, payoff structure frozen identical in all 36 cells. Good-rate variance:
**items 44.4%, models 32.1%, interaction 23.5%**. Neither dominates. `on_call`
spans the full range across models on identical text and numbers.

**Stipulated units are not the operative variable**, established three ways:
[pd_discriminant_r2](pd_discriminant_r2/ASSESSMENT.md) tied totals, worst losses
and best gains and the screen returned identical results — refuting
`pd_discriminant_r1`'s own welfare reading, which is marked superseded;
[phase4b_r1](phase4b_r1/ASSESSMENT.md) held payoffs byte-identical across four
items and got a 0.00–1.00 spread; `grand_r1` repeated it across twelve items and
three models.

**[phase4b_sonnet_r1](phase4b_sonnet_r1/ASSESSMENT.md)** — a third model where
the question **cannot be asked with these items**. Every sonnet item that
disperses sits within 0.12 of a bound; mean headroom 0.080 against haiku's 0.293.
A power analysis run before further spending showed ≤ 5/10 even at a generous
effect size, and more agents did not help. **Abandoned deliberately** rather than
run underpowered.

---

## Method carried out of Phase 4B

**A three-level authoring criterion**, derived from five review stops and
enforced in code by `verify_items()`. Paired options must match in:

1. presence and weight of non-unit consequence text;
2. violation labelling;
3. obligatory and transgressive modals.

Each level came from a designation stopped at its gate —
[breadth_focus_r1](breadth_focus_r1/ASSESSMENT.md) (description),
[closeout_r1](closeout_r1/ASSESSMENT.md) (consequence text, where a repair of
mine **relocated** the cue instead of removing it),
[breadth_r2](breadth_r2/ASSESSMENT.md) (modals, in items an earlier audit of mine
had cleared).

**Screen before profiling, per model, prospectively.** Applied throughout. Gate
and screen stops across the session cost roughly **$0.55** and prevented on the
order of **2,000 calls** on cued or saturated stimuli.

**A declared parser contract change.** `phase4_choice_extraction_v2` adds one
rule — where several well-formed choice objects appear, the last is the answer —
**verified before adoption** to reproduce all 960 stored `capstone_model2_r4`
decisions byte-identically, so it is provably empty on already-collected data.

**A measured output-budget constraint.** 768 tokens, calibrated on haiku,
truncates ~0.4% of sonnet replies. Any future sonnet designation needs ≥ 1536.

---

## A methods finding that was not planned

**AI design review returned opposite verdicts on byte-identical material, twice.**

`phase4b_permutation_r2` and `r3` reviewed the identical seven-item packet with
the identical prompt. r2: **accept**, zero blocking issues, `rest_break`
explicitly "a limit rather than a blocker". r3: **revise**, blocking on
`rest_break` and `on_call`.

Across the whole item set: seven reviews, **three accepts and four revises**, on
overlapping and in places identical material.

The 16 September amendment was written from evidence across *different*
designations. This is the tighter demonstration — same packet, same prompt,
opposite outcomes — and it belongs in the methods section rather than a footnote.

---

## What Phase 4B does NOT establish

- **No moral truth and no moral improvement.** Every label is a deterministic
  classification under stipulated standards, computed from stipulated transitions
  and never read from agent text. A higher `good` rate is a different
  distribution over rule-assigned labels, not a better agent.
- **Not that the profile is understood.** The permutation control did not clear
  this. The effect appears split between block-presence and label-mapping.
- **No coordinate-level claim.** Nine coordinates varied freely and none was
  manipulated in the profiled runs. Correlation tables in the assessments are
  exploratory and uncorrected.
- **Not a general cross-model law.** Two models where it holds, one where the
  question cannot be asked with these items.
- **Not generalisation across situations.** Six to eight items is six to eight
  situations. More calls on a handful of dilemmas is not evidence about new ones.
- **No human validation.** Human raters remain deferred by the 13 September
  instruction. AI agreement is not human validation.
- **A design-level caveat, conceded.** Two reviewers observed that stipulated
  units cannot fully neutralise the real-world normative weight of an item. That
  is partly correct and applies to **every moral dilemma in this project**,
  including `moral_capstone_r3`.

---

## Relation to `moral_capstone_r3`

`moral_capstone_r3` found profile effects on 956 decisions, on the original
conflict pool that five later reviews showed to cue the intended answer. Phase 4B
reaches the same conclusion on material built to avoid all three cueing surfaces,
screened in advance, with a G arm that fails where E succeeds, on two models.

The two are **independent and convergent**. r3 is **corroborated, not
superseded**.

---

## Designation record

| Designation | Outcome | Calls |
|---|---|---:|
| [phase4b_r1](phase4b_r1/ASSESSMENT.md) | screen stop; 0.00–1.00 spread under identical payoffs | 101 |
| [phase4b_screen_r2](phase4b_screen_r2/ASSESSMENT.md) | halted on a parse failure; family hypothesis refuted | 57 |
| [phase4b_grand_r1](phase4b_grand_r1/ASSESSMENT.md) | complete; variance decomposition | 901 |
| [phase4b_profiled_r1](phase4b_profiled_r1/ASSESSMENT.md) | **complete; haiku result** | 631 |
| [phase4b_sonnet_r1](phase4b_sonnet_r1/ASSESSMENT.md) | halted; abandoned on power analysis | 240 |
| [phase4b_gpt_r1](phase4b_gpt_r1/ASSESSMENT.md) | review stop | 1 |
| [phase4b_gpt_r2](phase4b_gpt_r2/ASSESSMENT.md) | **complete; calibration-model result** | 840 |
| [phase4b_permutation_r1](phase4b_permutation_r1/ASSESSMENT.md) | review stop; one item excluded | 1 |
| [phase4b_permutation_r2](phase4b_permutation_r2/ASSESSMENT.md) | complete; **rule not met** | 736 |
| [phase4b_permutation_r3](phase4b_permutation_r3/ASSESSMENT.md) | review stop; contradictory verdict | 1 |

Three preserved failures across the phase, none retried:
`phase4b_screen_r2/screen/tool_library/5`,
`phase4b_sonnet_r1/profiled/E/17/ward_transfer`, and one inherited from
`capstone_model2`.

**Accounting at closure: Claude $19.684017100/$32, OpenAI $5.497067400/$30.**
Usage estimates, not verified provider balances. The $100 package cap is
unchanged.

---

## What is NOT closed

- **The permutation question.** r2's null stands as the answer of record. A
  conclusive version needs ~840 pairs, which is affordable, and a review protocol
  that does not flip on identical materials.
- **The thesis §5.3 configuration counterfactual**, varying the five societal
  axes. Never run in Phase 4; every call used NEUTRAL on all five.
- **The prospective PD test** — built twice, cleared review twice, stopped by its
  own screen twice. **Untested, not failed.**
- **The breadth question** — untested across two attempts.
- **Human validation** — deferred by instruction.

No phase is reopened and no completed result is altered by this closure. Phase
4B's original ambition — a full moral evaluation with human-validated scoring —
is **not** claimed complete. This closes the central good/bad question for the
stated scope, in the manner of the accepted Phase 1.5 and Phase 3 closures.
