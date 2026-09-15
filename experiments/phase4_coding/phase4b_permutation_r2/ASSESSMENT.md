# phase4b_permutation_r2: the prespecified rule was not met

**Outcome: complete, and the declared decision rule FAILED.** 736 calls,
736/736 valid, zero failures, $0.488823. 16 September 2026. Review **accept**,
zero blocking issues.

Ledger after this designation: Claude $19.673975200/$32, OpenAI $5.497067400/$30.
Usage estimates, not wallet balances.

**The Phase 4B caveat is not retired.** It stands, and this designation is the
reason it stands rather than an argument for retiring it.

## The result

| Arm | Good-rate | n | vs U | Fisher p |
|---|---:|---:|---:|---:|
| **U** no block | 0.400 | 175 | — | — |
| **P** same numbers, deranged labels | 0.475 | 280 | +0.075 | 0.122 |
| **E** same numbers, correct labels | 0.564 | 280 | **+0.164** | **0.00074** |

**Paired E vs P**, same agent and item, identical user text, identical system
length, identical numeral multiset:

| | Value |
|---|---|
| effect | +0.089 |
| pairs | 280 |
| discordant | 57 E-good-only, 32 P-good-only |
| raw p | 0.0105 |
| **pooled Holm** | **0.084** |
| direction consistency | 5 of 7 positive (rule met) |

**The rule required BOTH pooled Holm p < 0.05 AND ≥ 4 of 7 items agreeing.**
Consistency passed; significance did not. **Under the criterion declared in
source before collection, this is a null.**

No item survives individual Holm correction. The largest are `tool_library`
+0.225 (Holm 0.157) and `weekend_rota` +0.175 (Holm 0.234).

## What the three arms show

The ordering is monotone and the two contrasts against the unprofiled baseline
separate cleanly:

- **A scrambled block alone does not significantly move the headline**
  (P − U = +0.075, p = 0.122).
- **The correctly-labelled block does** (E − U = +0.164, p = 0.00074).
- The difference between them, +0.089, is **not significant under correction**.

Read together, the effect appears to be **split between the two components** —
part carried by the presence of a structured numeric block, part by the
label-to-value mapping — with this design unable to resolve the second component
at the size it turned out to be.

## Why the null is weak, stated before collection

The protocol recorded this power table, measured over 12 seeds **before any
call**:

| True E−P gap | Power |
|---:|---:|
| 0.21 (permutation destroys the effect) | 12/12 |
| 0.15 | 10/12 |
| **0.10** | **7/12** |
| 0.05 | 3/12 |
| 0 | 1/12 false positive |

The protocol's own words: *"this design is well powered for a large effect and
underpowered for a small one. If permuting labels merely dents the effect rather
than destroying it, a null here would be weak evidence."*

**The observed gap is +0.089, which sits almost exactly at the 7/12 row.** The
design was built to detect destruction of the effect and it would have. It was
not built to resolve a gap this size, and it did not.

This is a limitation identified in advance and confirmed by the result, not an
excuse constructed afterwards.

## What this establishes

**The cue reading is not ruled out, and the Phase 4B caveat stands.** Every claim
resting on the numeric profile must continue to carry it: a shift under a numeric
block remains consistent with the block acting in part as an elaborate context
cue.

**A scrambled block is not equivalent to no block.** P sits 0.075 above U. That
is not significant on its own, but it is the right direction and it constrains
the interpretation: whatever the profile does, part of it plausibly survives
scrambling the labels.

**The correct-label block is the only arm that clears its contrast against
baseline.** E − U = +0.164 at p = 0.00074. P − U does not.

## What this does NOT establish

- **Not that the profile is merely a cue.** A null under an underpowered rule is
  not evidence for the null. The point estimate is positive and directionally
  consistent across 5 of 7 items.
- **Not that the labels are irrelevant.** +0.089 with raw p = 0.0105 is a
  positive point estimate that failed correction, which is a different thing
  from no effect.
- **Not a refutation of any Phase 4B result.** `phase4b_profiled_r1` and
  `phase4b_gpt_r2` are untouched. This bounds their *interpretation*; it does not
  contradict their data.
- **Not moral truth**; deterministic classification under stipulated standards.
- **No human validation**; human raters remain deferred.

## What a conclusive version needs

The effect to be resolved is roughly **0.09**, not the 0.21 the design was
powered for. Reaching 90% power at that size needs roughly **four times the
pairs** — on the order of 1,100 paired decisions rather than 280, which at this
per-call cost is about $2 and is entirely affordable.

That is a straightforward rerun at larger n, not a redesign. The items, arms,
derangement and analysis are all validated and unchanged. **It is the single
cheapest open question in the project**, and it is the one that decides whether
the central result is about parameters or about presentation.

Nothing here authorises it.

## One item excluded on review

`phase4b_permutation_r1` stopped at its hard gate flagging `sample_draw` alone,
while explicitly clearing the other seven as "structurally parallel and
balanced". That was the **second independent reviewer** to name it. r2 dropped it
and cleared review with zero blocking issues, which confirms the finding was
specific to that item rather than a general objection.

**The exclusion was not outcome-driven.** It followed a review finding, was made
before any profiled call here, and does not rescue anything: the
`phase4b_gpt_r2` effect is *larger* without `sample_draw` (+0.228 → +0.243).

## Provenance

The control was verified exact across all 40 agents before collection:
identical user turns, identical system-prompt length, identical multiset of
rendered numerals, E ≠ P for every agent, and a fixed 10-cycle derangement with
no fixed point, seeded and declared in source. One agent had a tied value pair,
recorded rather than excluded.

736 calls dispatched, 736 valid, zero entries in `failures.jsonl` for this
designation. Two failures remain inherited from earlier designations, preserved
and unretried.

Review returned **accept**, zero blocking issues, three non-blocking limits.
Screen gate passed on all seven items on fresh probes.
