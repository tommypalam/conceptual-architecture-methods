# parameter_followup_r2 — assessment

**Complete. 2,240 calls, 2,240/2,240 valid, zero failures, $1.668358.**
`gpt-5.4-mini-2026-03-17`, 80 agents (seed 2026092025), seven items, four arms,
21 September 2026. Protocol: [PROTOCOL.md](PROTOCOL.md). Design hash
`3897b681…91f03212`.

**Both coordinates move the outcome.** This is the opposite of the expected
result: the protocol recorded that, given the priors, "the most likely outcome is
two tighter bounds rather than two effects."

| Coordinate | Effect | 95% CI | Holm | Items | 90% bound | Prior (25 agents) |
|---|---:|---|---:|---|---:|---:|
| **TfA** Tolerance for Asymmetry | **−0.1107** | [−0.1536, −0.0661] | **2.5e−06** | 2+/4− | 0.146 | −0.1029 |
| **MoR** Mode of Response | **−0.0732** | [−0.1161, −0.0304] | **0.00106** | **0+/6−** | 0.109 | −0.0971 |

560 agent-item units complete in all four arms. Both two-sided, no direction
adopted from the sweep.

## The near-misses were real, and underpowering hid them

Both reproduce their 25-agent point estimates closely — TfA −0.103 → −0.111, MoR
−0.097 → −0.073 — and both now clear Holm comfortably. **Nothing about the effects
changed; only the power did.** At 25 agents an effect of 0.10 on these baselines
is detected roughly 9 times in 20; at 80 agents, 18.

This is the mirror image of the Legitimacy Locus story and worth stating beside
it. LL cleared a corrected bar at 25 agents and **dissolved** at 40 and 80. TfA and
MoR **failed** a corrected bar at 25 agents and survive at 80. Small samples
produced a false positive in one case and two false negatives in the other; the
same remedy — measuring at a size chosen from simulated power rather than from
budget — fixed both. The thesis's description of these two as "below the certified
threshold, not flat" was the correct hedge and is now resolved in the direction
the hedge left open.

**Order-robust.** Under the standing rule from
[ORDER_DEPENDENCE.md](../ORDER_DEPENDENCE.md): TfA gives −0.1107 under both
presentation orders (gap 0.000) and MoR −0.0714 / −0.0750 (gap 0.004). Neither is
an artefact of which option is printed first.

## Item consistency: MoR is clean, TfA is not

**MoR is negative on 6 of 7 items** (the seventh is exactly 0.000), with a narrow
per-item range of −0.125 to 0.000. It is a small, uniform effect.

**TfA is 2+/4−** and meets the 4-of-7 rule only on the negative side, with a per-item
range from **+0.175 to −0.312**. Four items run clearly negative
(`on_call` −0.312, `rest_break` −0.275, `storage_unit` −0.212, `tool_library`
−0.175) while `desk_booking` runs **+0.175** against them. The pooled figure is a
partial cancellation, not a uniform shift. **TfA's effect is item-dependent in a
way MoR's is not**, and reporting only the pooled −0.111 would obscure that.

## What this does and does not mean

**The coordinate map changes.** Of the ten, the count of coordinates that move the
outcome on these items rises from two to four: PD, ID, TfA, MoR. Against that, LL
is null at 80 agents and AW is flat at a 0.050 bound
([r1](../parameter_followup_r1/ASSESSMENT.md)).

**It does not make any of them a label effect.** Moving the outcome is not the same
as the effect being bound to the field; that requires a swap control, and **no
swap control was run here**. TfA and MoR are at the stage PD was at after
`coordinate_sweep_r2` and before `label_semantics_r1` — pinned effects with the
mechanism unidentified.

**And it does not privilege the encoding.**
[probe_fields_r1](../probe_fields_r1/ASSESSMENT.md) found an invented field
reaching +0.400 on the same items, above every coordinate measured here. That four
of ten framework parameters move choices is consistent with the general finding
that **a glossed field whose stated meaning bears on the items moves choices** —
these four are instances, not evidence that the ten were the right ten.

**No direction was predicted**, so the signs carry no theoretical weight. Both are
negative; the framework supplies no derivation of that on these items, and none is
offered after the fact.

## What no outcome establishes

Understanding, or that any coordinate is understood as a concept. That either
effect is bound to its label or its gloss. Anything beyond `gpt-5.4-mini`, these
seven workplace-resource items with tied payoffs, and this harness. No moral
claim: outcomes remain a deterministic lookup on the chosen action.

## Accounting

OpenAI $19.609534 → **$21.277892**/$40. Anthropic unchanged $22.268707/$32.
Package ≈ $43.547/$100. Usage estimates, not verified provider balances.
