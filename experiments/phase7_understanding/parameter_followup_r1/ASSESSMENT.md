# parameter_followup_r1 — assessment

**Complete. 2,240 calls, 2,240/2,240 valid, zero failures, $1.661963.**
`gpt-5.4-mini-2026-03-17`, 80 agents (seed 2026092022), seven items, four arms,
20 September 2026. Protocol: [PROTOCOL.md](PROTOCOL.md). Design hash
`dc92b7ad…2db94111`.

**Both coordinates: no effect detected.**

| Coordinate | Effect | 95% CI | Holm | Items | 90% equivalence bound | Prior |
|---|---:|---|---:|---|---:|---:|
| **AW** Affective Weighting | **+0.0161** | [−0.0268, +0.0572] | 0.494 | 4+/2− | **0.050** | −0.036 |
| **LL** Legitimacy Locus | −0.0357 | [−0.0804, +0.0089] | 0.261 | 1+/5− | 0.073 | −0.131 |

560 agent-item units complete in all four arms.

## AW: the assumption under the thesis's swap controls holds

Every swap control in the thesis puts the tested level on AW's entry as the
partner field. That rested on AW measuring −0.036 **as a by-product of
`label_semantics_r1`** — AW had never been pinned in its own right. It now has
been, at 80 agents, and it is flat: **+0.016, interval [−0.027, +0.057], and a 90%
equivalence bound of 0.050**.

This is the tightest bound any coordinate in this project has received. Seven of
the sweep's coordinates certify only |effect| < 0.20, and only RT and CS certify
< 0.10; **AW certifies < 0.05**, at twice the agents.

**What it does and does not license.** It supports the swap controls: the partner
field does not itself carry the outcome, so a numeral placed on AW's entry is not
silently doing work. It does **not** prove the controls are sound, because they
additionally assume AW's entry is a *fair partner* for the tested field's entry —
comparable salience, comparable readability. `probe_fields_r1` showed that entry
10 carries a *glossed* field perfectly well (Status-quo Preference reached +0.400
there), so the slot is capable of carrying an effect; AW's own gloss does not
produce one. That is the right shape for a partner field, and it is stronger
evidence than the thesis had. It is still an assumption about comparability, not a
measurement of it.

**And a null is a bound, not a zero.** At 18/20 power for |0.10|, this bounds AW's
effect below about 0.05 on these items and does not establish that it is zero.

## LL: a fourth measurement, and it does not rehabilitate anything

Legitimacy Locus has now been measured four times:

| Measurement | Value | Sample |
|---|---:|---|
| Post-hoc correlation, Phase 5 | +0.271 | unmanipulated arm |
| Pinned, `coordinate_sweep_r2` | −0.131 | 25 agents |
| Pinned, `label_semantics_r2` TRUE | −0.014 | 40 agents |
| **Pinned, here** | **−0.036** | **80 agents** |

Positive, negative, null, null. **The withdrawal stands.** This designation's
protocol fixed in advance that a third pinned measurement is reported as a
measurement and does not overturn the withdrawal by majority vote, and that holds
whichever way it came out.

What the sequence shows is a coordinate whose measured effect shrinks as the
sample grows: −0.131 at 25 agents, −0.014 at 40, −0.036 at 80, with the 80-agent
interval [−0.080, +0.009] comfortably containing both later estimates and
excluding the first. The sweep's −0.131 at Holm 0.0008 looks, in retrospect, like
the small-sample overestimate that the larger runs have been correcting. **LL is
not load-bearing and is not demonstrated inert** — the equivalence bound is 0.073,
so a real effect below that size is not excluded.

`on_call` runs +0.237 against LL's five negative items, the same item that runs
against the grain under PD. It is reported, not smoothed.

## Method note

The degeneracy defect was caught before collection, not after. Under the first
seed, agent 76 drew an AW value rendering as one of the two levels at the block's
two decimals, which would have made that agent's two arms byte-identical.
`verify_construction` tests at **rendered** precision and blocked it; the seed was
advanced by one on a property of the draw alone, before any call — the same repair
`label_semantics_r2` made for the same defect. **The check transferred to a new
designation and worked.**

## What this does not establish

Understanding, or that any coordinate is understood as a concept. That AW or LL is
inert — both are bounded, not zeroed. That a coordinate which moves the outcome is
a *label* effect: that needs a swap control, which this designation does not run.
Anything beyond `gpt-5.4-mini` and these seven items.

## Accounting

OpenAI $17.947571 → **$19.609534**/$40. Anthropic unchanged $22.268707/$32.
Package ≈ $41.878/$100. Usage estimates, not verified provider balances.
