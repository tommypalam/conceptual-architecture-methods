# semantics_r1 — assessment

**Complete. 2,240 calls, 2,240/2,240 valid, zero failures, $1.665947.**
`gpt-5.4-mini-2026-03-17`, 40 agents, seven items, eight cells, 20 September 2026.
Protocol and locked predictions: [PROTOCOL.md](PROTOCOL.md). Programme context:
[../PROGRAMME.md](../PROGRAMME.md).

Exploratory, on branch `understanding-programme-20260919`. **Not part of the
submitted thesis**, which is frozen at `docs/thesis/LF3262767.pdf`.

## Result

The gate passed and the decision rule returned `meaning_carries_it`.

| Variant | PD entry | Effect | 95% CI | Holm | Items |
|---|---|---:|---|---:|---|
| CANON | canonical | **+0.3393** | [+0.2714, +0.4036] | ~0 | 6+/1− |
| **FLIP** | **explanations exchanged** | **−0.1143** | **[−0.1786, −0.0500]** | 0.00063 | 1+/5− |
| **INVERT** | renamed *and* exchanged | **−0.6143** | [−0.6714, −0.5536] | ~0 | **0+/7−** |
| NONCE | renamed "Factor K" | +0.1750 | [+0.1143, +0.2357] | 1.6e−07 | 6+/1− |

Effect = share classifying `good`, printed 0.90 minus printed 0.10, paired by
agent and item. 280 agent-item units complete in all eight cells.

Within-unit differences from CANON, the primary quantity:

| Contrast | Estimate | 95% CI |
|---|---:|---|
| CANON − FLIP | **+0.4536** | [+0.3607, +0.5464] |
| CANON − INVERT | +0.9536 | [+0.8536, +1.0500] |
| CANON − NONCE | +0.1643 | [+0.0821, +0.2429] |

## What the locked predictions said, and what happened

| Variant | MEANING | NAME | EXTREMITY | Observed |
|---|---|---|---|---|
| CANON | + | + | + | **+0.339** |
| FLIP | **negative** | + | + | **−0.114** |
| INVERT | **negative** | ~0 | + | **−0.614** |
| NONCE | + | ~0 | + | **+0.175** |

**MEANING predicted the sign of all four cells. NAME and EXTREMITY each got two
wrong.** The predictions were recorded in source before collection under content
hash `7d00c81e…a87a8a` and are reproduced in the frozen release.

## The three findings, in order of what they cost the alternatives

**1. The gate replicated on a fresh population.** CANON gives +0.3393 against
`label_semantics_r1`'s +0.339, `pd_prospective_r1`'s +0.346 and
`position_counterbalance_r1` cell A's +0.393, on 40 agents drawn under a new seed.
The instrument is the same instrument, so the other three cells are interpretable.

**2. Field-weighted extremity is EXCLUDED.** It was the last surviving mechanism
in the thesis and the one no prior design could touch. It predicts a positive
effect in every cell, because an extreme numeral occupies a salient slot whatever
the surrounding words say. Two cells are negative, one of them at −0.614 with
every item agreeing. **The thesis's open mechanism list is now closed for PD on
this model and these items.**

**3. Name-association is excluded as a SUFFICIENT account, and measured as a
contributing one.** CANON and FLIP print the identical string `Procedural
Dependence: 0.90` on line 6; the blocks have the identical length and the identical
multiset of characters — FLIP is a pure rearrangement. A pure name account cannot
produce +0.339 and −0.114 from that pair. But the name is not doing nothing:

  - FLIP (−0.114) sets name against explanation, and they partly cancel.
  - INVERT (−0.614) makes the name agree with the exchanged explanation, and the
    reversal roughly **quintuples**.
  - NONCE (+0.175) removes the name and keeps the explanation: about **52%** of
    CANON survives.

So the explanation dominates when the two conflict, and the two compose roughly
additively when they agree. **This is the decomposition future-work item two asked
for** — the thesis could only say "the labelled AND glossed field", never name
against gloss.

## Per-item

| Item | CANON | FLIP | INVERT | NONCE |
|---|---:|---:|---:|---:|
| desk_booking | +0.225 | +0.150 | −0.375 | +0.200 |
| meeting_room | +0.150 | 0.000 | −0.425 | +0.150 |
| on_call | **−0.050** | −0.200 | −0.475 | −0.125 |
| rest_break | +0.800 | −0.225 | −0.775 | +0.425 |
| storage_unit | +0.400 | −0.200 | −0.900 | +0.150 |
| tool_library | +0.675 | −0.175 | −0.750 | +0.375 |
| weekend_rota | +0.175 | −0.150 | −0.600 | +0.050 |

`on_call` is negative under CANON, as it was in `pd_prospective_r1` (−0.150). The
same item misbehaves the same way across designations and is reported, not
smoothed. INVERT is negative on all seven, `on_call` included.

## What this does NOT establish

- **Not understanding.** This is one of six markers in the programme
  (transformation-invariance and reversal). Five are untested.
- **It does not separate reading an explanation from following an instruction
  phrased as an explanation.** Both predict every number above. That separation is
  Stage 3a's defeasibility test and nothing here anticipates its outcome.
- **Not general.** One field (PD), one model, the seven screened workplace-resource
  vignettes with tied payoffs. Whether any on-topic field with an explanation
  behaves this way is Stage 4b, unrun.
- **Not moral quality, improvement or human resemblance.** Outcomes remain a
  deterministic lookup on the chosen action.
- INVERT's magnitude rests on the soft premise that "Outcome Dominance" with
  exchanged ends means what the original meant — a human judgement, and this
  project has found such judgements do not predict model behaviour. **FLIP carries
  the argument** precisely because it needs no such premise.

## Method notes worth carrying forward

**The output cap change worked and should be the default.** 256 tokens rather than
1,536: reservation $10.976 against a settled $1.666, where the parent's
byte-comparable run reserved $25.223. Realised mean was $0.000745 per call. No
reply was truncated. The longest reply across the parent's 2,240 calls had been 21
tokens, so 256 remains 12× headroom.

**No review call was dispatched.** The items are byte-identical to material the
parent's review accepted with zero blocking issues; that verdict was read from the
ledger and is recorded in the release. **The edited PD entry is new material no
reviewer has seen** — its validity rests on the byte-level construction checks
(FLIP an involution and a pure rearrangement, CANON byte-identical to the parent's
prompt, changes confined to three lines), not on anyone's judgement of wording.

**`declared_tasks()` again.** The empty-analysis defect did not recur; the
collector produced its own analysis without offline rescoring.

## Accounting

OpenAI $12.741596 → **$14.407543**/$40. Anthropic unchanged at $22.247448/$32.
Package ≈ $36.655/$100. Usage estimates, not verified provider balances.
