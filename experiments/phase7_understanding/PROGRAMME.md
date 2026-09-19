# Phase 7 — the understanding programme

**Status: exploratory, on branch `understanding-programme-20260919`. Nothing here
is part of the submitted thesis**, which is frozen on `thesis-final-20260919` as
`docs/thesis/LF3262767.pdf`. Results from this programme belong to the paper.

Drafted 19 September 2026. No API call has been made under this programme. Each
designation below still needs its own frozen release and the researcher's
authorisation before any paid call.

## The question, stated at the strength it can be answered

The thesis established that the Procedural Dependence effect is bound to the PD
*entry* — its name together with its endpoint explanation — and not to block
presence, prompt length, free-floating extremity or line position. It explicitly
could not say whether the model *understands* the field.

**No input-side experiment can prove understanding**, and this programme does not
claim to. What it can do is build a *convergent case*, in the way psychometrics
treats a construct: nobody proves a person "has" conscientiousness; one shows the
construct behaves like one across independent tests. Six markers, each with a
falsifiable test, none sufficient alone:

| # | Marker | The test | Stage |
|---|---|---|---|
| 1 | **Transformation** | the effect survives changes of form that keep meaning, and *reverses* under changes of meaning that keep form | 1, 2 |
| 2 | **Gradedness and composition** | a graded, reversible dose-response; two fields combining lawfully | 2 |
| 3 | **Defeasibility** | a process-dominant agent *overrides* an arrangement that was itself obtained by breaching process | 3 |
| 4 | **Bidirectionality** | the model can act from the field, predict a third party from it, and infer it from choices | 3 |
| 5 | **Selectivity** | each parameter moves the item family its definition addresses, and not the others | 5 |
| 6 | **Specificity** | the framework's fields do something arbitrary on-topic fields do not | 4 |

**The deflationary rival, kept in the room throughout:** *this is instruction
following, with the explanation as the instruction.* A good instruction-follower
passes several markers. If a field passes all six, that is functional
understanding in any sense an experiment can reach; the residual gap is
philosophical and no data closes it. The paper will say so and claim the
empirical part only.

## Decisions taken with the researcher (19 September)

- **Models.** Stay on `gpt-5.4-mini` (calibration) and `claude-haiku-4-5` for
  now. A newer model is deferred until Stage 1 shows the effect is worth
  replicating. Verified reachable from the project's keys: `claude-sonnet-5`
  ($2/$10 per MTok), `claude-opus-5` ($5/$25), and on OpenAI `gpt-5.5`,
  `gpt-5.6-*`, `gpt-6-astra` (prices not verified — do not budget from memory).
- **Parameters.** Investigate both ways: unfinished business inside the ten
  (Stage 4a) and new probe fields outside them (Stage 4b).
- **Branches.** `thesis-final-20260919` stays the rigorous thesis line. This
  branch is for experiments.

## What a newer model will require, recorded so it is not rediscovered

1. **The harness cannot talk to the newest Claude models as it stands.** They
   reject `temperature` with a 400, and `phase3_design_pilot.request()` sends it
   on every call. That module is hash-pinned, so support goes in a new unpinned
   module that builds the request and registers provider and price.
2. **Every result to date was collected with reasoning disabled** (`thinking:
   disabled` / `reasoning_effort: none`). On newer models reasoning is on by
   default. Whether the model may deliberate is a real design factor for an
   understanding programme; it also costs output tokens and breaks comparability.
   Reasoning OFF stays primary; reasoning ON, if run, is a separate factor.
3. **More capable models have been MORE deterministic on these items.**
   `claude-sonnet-4-6` had every dispersing item within 0.12 of a bound;
   `haiku_screen_r4` returned six modal shares of 1.00. Any new model starts with
   the dispersion screen, which may end the idea on that model for about $1.

## Budget mechanics that constrain the order of work

Ledger at the start: Claude $22.25/$32, OpenAI $12.74/$40 — **$27.26 of OpenAI
headroom**. No ceiling change is requested.

The ledger reserves every call at its *worst case* and the reservation must fit
under the ceiling, although prior runs settle near 7% of it. Measured over the
2,240 most recent `gpt-5.4-mini` calls: **input 801 tokens (max 805); output mean
15.2, maximum 21.** The harness reserves 1,536 output tokens per call — 73 times
the largest reply ever observed — which is why a $1.66 designation needs about
$25 of headroom and why three of them in sequence would not fit.

**From Stage 1 onward the output cap is 256 tokens** (12× the observed maximum).
Measured by the collector's offline check, `semantics_r1` then reserves **$10.98**
instead of about $25 - the input side is bounded in bytes, not tokens, so it does
not fall further. Reservations are released at settlement, so designations run
**one at a time** each fit the $27.26 headroom; two cannot be open at once.
It is a disclosed protocol difference from earlier designations. It cannot change
behaviour unless a reply is truncated, and a truncated reply would be preserved
as a failure and never retried, exactly as the rules require.

## Stage 1 — COMPLETE, 20 September: meaning carries it

**Ran as specified. 2,240 calls, 2,240/2,240 valid, zero failures, $1.665947.**
Full numbers in [semantics_r1/ASSESSMENT.md](semantics_r1/ASSESSMENT.md).

| Variant | Effect | 95% CI | Items |
|---|---:|---|---|
| CANON | +0.3393 | [+0.2714, +0.4036] | 6+/1- |
| **FLIP** | **-0.1143** | [-0.1786, -0.0500] | 1+/5- |
| INVERT | -0.6143 | [-0.6714, -0.5536] | 0+/7- |
| NONCE | +0.1750 | [+0.1143, +0.2357] | 6+/1- |

**MEANING predicted the sign of all four cells; NAME and EXTREMITY each got two
wrong.** The gate replicated at +0.3393 on a fresh population.

**Field-weighted extremity is excluded** - the last open mechanism in the thesis,
which predicted every cell positive. **Name-association is excluded as a
sufficient account and measured as a contributing one**: the explanation
dominates when the two conflict (FLIP), they compose when they agree (INVERT),
and about 52% of the effect survives with the name removed (NONCE). That is
marker 1 of six. It does NOT separate reading an explanation from following an
instruction phrased as one - Stage 3a.

**Carry forward:** the 256-token output cap settled $1.666 against a $10.976
reservation and truncated nothing. Use it for every designation below.

## Stage 4b - COMPLETE, 20 September: meaning is followed generally; PD is not special on size

`probe_fields_r1`, 2,240/2,240 valid, zero failures, $1.680032. Full numbers in
[probe_fields_r1/ASSESSMENT.md](probe_fields_r1/ASSESSMENT.md).

| Probe | Predicted | Effect | 95% CI | Items |
|---|---|---:|---|---|
| Status-quo Preference | + | +0.4000 | [+0.3357, +0.4643] | 7+/0- |
| Stated-Wish Deference | + | +0.3071 | [+0.2536, +0.3607] | 7+/0- |
| Numbers Count | negative | -0.2464 | [-0.3107, -0.1821] | 0+/7- |
| Worst-off Priority | + | -0.0643 | [-0.1286, 0.0000] | 2+/4- (prediction failed) |

Fields are not generic cues: same slot, opposite directions, as their explanations
say. But an invented field beats the framework's verified parameter (+0.400 vs
+0.339), so **nothing so far requires the ten parameters in particular**, and
**PD may be a status-quo dial**. **Stage 3a is now the critical path**: it is the
only stage where "process-dominant" and "keep the arrangement" come apart.

### Stage 1 as designed

**Built and verified offline**: `code/phase7_block_variants.py`,
`code/phase7_semantics.py`. 2,240 calls, about $1.66 settled ($10.98 reserved), `gpt-5.4-mini`, 40 agents,
the seven screened items. PD pinned to 0.10 / 0.90 under four renderings of the PD
entry; everything else byte-identical.

| Variant | Name | Explanation | Isolates |
|---|---|---|---|
| CANON | Procedural Dependence | canonical | the replication gate |
| **FLIP** | Procedural Dependence | **ends swapped** | explanation against name + number |
| INVERT | Outcome Dominance | ends swapped | a consistent re-encoding |
| NONCE | Factor K | canonical | the explanation with no name |

**Locked predictions — they differ in SIGN.** Effect = printed 0.90 minus 0.10.

| Variant | MEANING | NAME association | field-weighted EXTREMITY |
|---|---|---|---|
| CANON | + | + | + |
| **FLIP** | **negative** | + | + |
| INVERT | negative | ~0 | + |
| NONCE | + | ~0 | + |

**FLIP is the decisive cell**, as condition D was for position. Name, line, number
and even the multiset of characters in the block are held fixed — FLIP is a pure
rearrangement, 1,714 bytes either way — and only what the two ends of the scale
are *said to mean* changes. It needs no judgement that two wordings are
equivalent. INVERT does, and that premise is soft: this project has already found
that reviewer judgements about materials do not predict model behaviour.

**Primary quantities are direct contrasts with 95% unit-bootstrap intervals** —
each within-variant effect, each within-unit difference from CANON, the reversal
indices `e_FLIP / e_CANON` and `e_INVERT / e_CANON` (−1 = full reversal, +1 =
explanation ignored) and the transfer index `e_NONCE / e_CANON`. **No conclusion
is drawn from one arm being significant while another is not**; that inference
was made once in this project, about ID, and had to be withdrawn.

**Gate:** `e_CANON` must replicate (prior: +0.339 to +0.393). If it does not, the
designation reports a failed gate and interprets nothing else.

**Power**, simulated against the *measured* per-item baselines of `phase4b_gpt_r2`,
20 seeds, Holm family of 4: **20/20** for a full reversal (−0.34), 20/20 at −0.20,
**18/20 at −0.15, 8/20 at −0.10**, 0/20 false positives. A weak partial reversal
is therefore poorly detected as a *sign test* — one more reason the reversal index
with its interval, not a p-value, is the headline.

**A third outcome is live and is not a failure:** FLIP sets the name against the
explanation, so the conflict may cancel. That reads as "the explanation matters
but does not dominate the name" and is reported through the index, not rounded to
either reading.

## Stage 2 — robustness of the meaning claim

Run only if Stage 1's gate passes. About $1.70.

- **Paraphrased explanation** sharing no content words with the original, to rule
  out association with particular tokens in the gloss.
- **Name only**, explanation removed: what does the phrase alone carry?
- **Five-level dose-response** (0.10 … 0.90), canonical and flipped. A graded
  gradient that reverses with the explanation is what reading a scale looks like;
  a step is what a categorical cue looks like.
- **PD × ID factorial**, if budget allows: do two fields combine, or does one
  swamp the other?

## Stage 3 — two tests the present items cannot make

**3a. Defeasibility: the illegitimate-arrangement reversal.** On every current
item "process-dominant" and "keep the status quo" are the *same choice*, so PD may
be nothing more than a status-quo dial. New items will present an arrangement that
was itself obtained by breaching process — a booking made by jumping the queue.
An agent that understands process-dominance should then **override more**; a
"PD high → keep" association keeps more. Opposite signs, derived from the
framework's own definition. **New items: hard review gate, the three-level
authoring criterion, and the dispersion screen** — the path on which five earlier
designs died. This is the single most informative test in the programme about
what PD actually *is*.

**3b. Bidirectionality.** *Predict*: ask what a third-party agent with PD 0.90
would choose, item by item, and compare with how the model behaves *as* that agent
— including on `on_call`, the item that ran negative. *Infer*: show the frozen
choice transcripts from `pd_prospective_r1` and ask for the agent's PD. Reuses
frozen records; about $0.50.

## Stage 4 — the parameters

**4a. Unfinished business inside the ten. 80 agents, not 40.** The sweep ran 25
agents and left two near-misses whose uncorrected intervals exclude zero — TfA
(−0.103) and MoR (−0.097). A 40-agent re-test would have had **8/20 power** at
that size: it would have manufactured another Legitimacy Locus, a small effect
measured too noisily to settle. Measured power at |0.10|, Holm family of 2:
40 agents 12/20, 60 → 15/20, **80 → 18/20**, 100 → 20/20. Hence two designations
of 2,240 calls each, about $1.66 apiece:

| Designation | Pins | Why |
|---|---|---|
| `parameter_followup_r1` | **AW**, LL | AW was never independently pinned, yet every swap control rests on it; LL needs a third measurement or stays withdrawn |
| `parameter_followup_r2` | TfA, MoR | the two near-misses, at a sample size that can settle them |

Two-sided, no directional prediction — none of the four has a theory mapping onto
these items. **AW runs first**: Stage 4b edits AW's slot.

**4b. Probe fields outside the ten — also the specificity control.** Candidate
fields that name what these items are actually about, rendered in AW's slot with
the same two-line explanation format, pinned 0.10 / 0.90:

| Probe field | 0 = | 1 = | Predicted sign |
|---|---|---|---|
| Status-quo Preference | existing arrangements carry no special weight | existing arrangements stand unless there is strong reason to change them | + |
| Stated-Wish Deference | a stated wish is one input among many | a person's stated wish about their own arrangement is decisive | + |
| Worst-off Priority | total benefit matters however it is spread | whoever would lose most matters most | + |
| **Numbers Count** | claims are weighed regardless of how many hold them | the option helping more people is favoured | **negative** |

`Numbers Count` is there on purpose: its meaning predicts the *opposite*
direction, because overriding helps two people rather than one. **If all four move
choices the same way regardless of what they say, fields are acting as generic
cues.** If they move as their meanings predict, explanation-following is general —
and then the question for the framework becomes sharp: *is PD special, or does any
on-topic field with an explanation do the same work?* An answer of "any field
does" would not embarrass the method; it would cap what the ten parameters can
claim, and it is better discovered here than by a reviewer.

**These are probe fields on this branch, not amendments to the ten.** Adding a
parameter to the framework requires the researcher's approval. Their wording above
is a proposal and is **not built** until approved.

## Stage 5 — the selectivity matrix (scope)

New item families written from individual parameters' definitions (Moral Scope,
Tolerance for Asymmetry, Internalisation Dependence), directions locked in
advance, **the diagonal predicted**: each parameter moves its own family and not
the others. A double dissociation would validate concept-specific encoding and
answer the single-task-family limitation at once. Slowest and riskiest stage —
start with one or two families, after Stage 3a has shown whether new items can be
made to disperse at all.

## Five-perspective review (required: new parameter-to-behaviour mappings)

Structured review roles, not external expert review.

**Decision under review:** adopt this programme, and in particular the probe
fields of Stage 4b, whose predicted signs are mapping rules written for the first
time.

- **Linden (philosophy).** The probe fields are instructions wearing a parameter's
  clothes. Say in advance what distinguishes a *parameter* from an *instruction*,
  or Stage 4b cannot bear on the framework at all. Accepts FLIP as the cleanest
  test on the table; rejects any use of the word "understanding" in a result.
- **Osei (psychology).** On these items keep, status quo and stated wish coincide,
  so three probes load on one behaviour and cannot be told apart. Only new items
  dissociate them. Stage 3a is therefore the real test, not a side project.
- **Tanaka (statistics).** Approves direct contrasts with intervals and the
  80-agent sizing. Objects to ratio indices near a small denominator: report
  `e_CANON − e_V` as primary, the indices as description. Wants the Holm family
  fixed per designation before collection, which it is.
- **Renna (downstream).** If the probes work as well as PD, the architecture's
  claim shrinks to "explanations are followed". Decide now what would count as PD
  being special: a larger effect, a graded response, or defeasibility. Proposes
  defeasibility, since it is the only one an instruction does not trivially give.
- **Okafor (implementation).** Order by dependency: Stage 1 → 4a (AW first) → 4b →
  3a. Lower the output cap before anything runs. Freeze one designation at a time.

**Genuine disagreements, which are the load-bearing risks.** (i) Whether Stage 4b
can say anything about the framework without a prior criterion for "special"
(Linden, Renna) — *resolved*: defeasibility is adopted as that criterion, and
Stage 4b is read as a specificity control rather than a contest of effect sizes.
(ii) Whether the reversal index is a legitimate headline (Tanaka) — *resolved*:
the within-unit difference is primary, the index descriptive; `phase7_semantics`
records both and the protocol will say which leads. (iii) Whether Stage 3a should
precede Stage 4 (Osei) — *open*: it is the more informative but by far the more
likely to die at the dispersion screen, so the cheap stages run first while its
items are authored in parallel.

## What this programme cannot establish, whatever happens

- **Understanding**, in any sense beyond the six markers above.
- **Moral quality, moral improvement or human resemblance.** Outcomes remain a
  deterministic lookup on the chosen action; no human data exists.
- **Generality** beyond the screened item families and the models actually run.
- A difference between *reading an explanation* and *following an instruction
  phrased as an explanation*, unless defeasibility separates them.
