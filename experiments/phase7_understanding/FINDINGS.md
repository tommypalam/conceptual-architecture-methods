# Phase 7 — what the understanding programme established

**Nine designations, 12,031 calls, 12,030 valid, one preserved failure, $8.796.**
20 September 2026, branch `understanding-programme-20260919`. All on
`gpt-5.4-mini-2026-03-17` except two review calls on `claude-sonnet-4-6`.

**Not part of the submitted thesis** (`docs/thesis/LF3262767.pdf`, frozen on
`thesis-final-20260919`). These results belong to the paper, and two of them
require the paper to be changed.

| Designation | Calls | Outcome |
|---|---:|---|
| [semantics_r1](semantics_r1/ASSESSMENT.md) | 2,240 | meaning carries the effect; extremity excluded |
| [probe_fields_r1](probe_fields_r1/ASSESSMENT.md) | 2,240 | fields follow their stated meanings; PD not special on size |
| [defeasibility_screen_r1](defeasibility_screen_r1/ASSESSMENT.md) | 176 | screen stop, 2 usable twins of 7 |
| [defeasibility_screen_r2](defeasibility_screen_r2/ASSESSMENT.md) | 241 | screen stop, 0 of 10 candidates usable |
| [floor_lift_r1](floor_lift_r1/ASSESSMENT.md) | 2,240 | PD and a status-quo field dissociate, against the framework's story |
| [parameter_followup_r1](parameter_followup_r1/ASSESSMENT.md) | 2,240 | AW flat at a 0.050 bound; LL null a fourth time |
| [parameter_followup_r2](parameter_followup_r2/ASSESSMENT.md) | 2,240 | TfA and MoR both move the outcome at 80 agents |
| [inverse_inference_r1](inverse_inference_r1/ASSESSMENT.md) | 120 | **instrument failed**: a positional bias, not a measure of inference |
| [precipitation_r1](precipitation_r1/ASSESSMENT.md) | 294 | **halted** by a network timeout at call 294 of 840; no result, not re-run |

Plus [ORDER_DEPENDENCE.md](ORDER_DEPENDENCE.md), an offline re-analysis with no
API calls.

---

## 1. The thesis's last open mechanism is closed

The thesis could not exclude **field-weighted extremity**: a model weighting an
extreme numeral by the salience of the field holding it would produce every result
in the paper, with no semantic reading of the label. The abstract says so.

`semantics_r1` excludes it. PD was pinned to 0.10 and 0.90 under four renderings
of its own entry, everything else byte-identical:

| Variant | PD entry | Effect | 95% CI | Items |
|---|---|---:|---|---|
| CANON | canonical | +0.3393 | [+0.2714, +0.4036] | 6+/1− |
| **FLIP** | **endpoint texts exchanged** | **−0.1143** | [−0.1786, −0.0500] | 1+/5− |
| INVERT | renamed *and* exchanged | −0.6143 | [−0.6714, −0.5536] | **0+/7−** |
| NONCE | renamed "Factor K" | +0.1750 | [+0.1143, +0.2357] | 6+/1− |

**FLIP is decisive.** Name, line, number and the block's entire character multiset
are identical to CANON — it is a pure rearrangement of two strings — and the
effect reverses. Extremity predicts every cell positive; two are negative.
Name-association cannot produce opposite signs from an identical printed name.

**The decomposition the thesis asked for.** Reviewer point 3 on 19 September was
that the designs isolate the labelled *and glossed* field, never the label string,
and that separating them was future work. It is now done: the explanation
dominates when the two conflict (FLIP), they compose when they agree (INVERT, the
largest effect in the project), and **about 52% of the effect survives with the
name removed** (NONCE).

**Paper consequence.** The abstract's "does not exclude … field-weighted
extremity" is superseded, and "field-bound label effect" can become a claim about
the field's *stated meaning*. This is the single biggest gain of the phase.

## 2. But the framework's parameters are not special

`probe_fields_r1` put four invented fields — none among the ten — in the partner
slot, pinned 0.10/0.90:

| Probe field | Predicted | Effect | 95% CI | Items |
|---|---|---:|---|---|
| Status-quo Preference | + | **+0.4000** | [+0.3357, +0.4643] | 7+/0− |
| Stated-Wish Deference | + | +0.3071 | [+0.2536, +0.3607] | 7+/0− |
| **Numbers Count** | **negative** | **−0.2464** | [−0.3107, −0.1821] | 0+/7− |
| Worst-off Priority | + | −0.0643 | [−0.1286, 0.0000] | 2+/4− |

**Two independent confirmations of §1**: two fields in the same slot, same format,
same numerals, moved choices in *opposite* directions as their explanations said.
Numbers Count was predicted negative in advance and was negative on all seven
items.

**And a bound on the architecture.** Status-quo Preference — a field written in an
afternoon, naming what the items are about — reaches **+0.400 against PD's
+0.339**, and is consistent on 7 items where PD is 6+/1−. **Nothing in the
evidence requires the ten parameters in particular.** What was verified is better
described as: *a glossed field whose stated meaning bears on the items moves
choices*, of which PD is one instance.

**One prediction failed and it was ours.** Worst-off Priority was derived positive
from the stipulated numbers (the holder loses 5, the most of anyone) and came out
−0.064, not surviving Holm, and splitting across presentation orders. A designer's
reading of what wording implies did not predict model behaviour — which is why
FLIP-type designs, needing no such judgement, carry more weight than derivations.

## 3. PD does not behave like "procedure matters"

§2 raised a sharp worry: on every item, "process-dominant" and "keep the existing
arrangement" are the same choice, so PD may be a **status-quo dial**. Two screens
tried to build items where those come apart and both stopped — eleven wordings put
three items on a floor of 0.00–0.04 unprofiled keep. `floor_lift_r1` used the floor
as the instrument instead:

| Quantity (three floored twins) | Estimate | 95% CI |
|---|---:|---|
| L(PD) | +0.3833 | [+0.2917, +0.4750] |
| L(SQ) | +0.1333 | [+0.0583, +0.2083] |
| **L(SQ) − L(PD)** | **−0.2500** | **[−0.3583, −0.1417]** |

Gate passed: PD:BASE +0.350, SQ:BASE +0.357.

**PD is not interchangeable with a status-quo field** — the cleanest dissociation
the project has, and a real answer to §2's worry. **But it runs against the
framework's story.** Comparing each field's high arm across item versions, i.e.
how much the holder's procedural lapse deters an agent already at that field's
maximum:

| Item | PD high: BASE to TWIN | SQ high: BASE to TWIN |
|---|---|---|
| tool_library | 0.975 to 0.675 (**−0.30**) | 0.950 to 0.450 (**−0.50**) |
| rest_break | 0.925 to 0.775 (−0.15) | 0.725 to 0.775 (+0.05) |

**A high-PD agent is LESS deterred by the procedural lapse than a high-SQ agent.**
Whatever "Procedural Dependence: 0.90" does, it is not "care that the procedure
was followed". It behaves as a stronger, less discriminating keep-the-arrangement
pressure. **No procedural-justice claim is licensed and §7 must not be
strengthened on this.**

Caveats: two informative items (`storage_unit` is 0.000 in all four twin cells and
is retained, not dropped); part of PD's larger lift is a lower low arm rather than
a higher ceiling; the two fields sit in different slots.

## 4. The partner field under every swap control is now directly tested

`parameter_followup_r1`, 80 agents:

| Coordinate | Effect | 95% CI | 90% equivalence bound | Prior |
|---|---:|---|---:|---:|
| **AW** Affective Weighting | +0.0161 | [−0.0268, +0.0572] | **0.050** | −0.036 |
| LL Legitimacy Locus | −0.0357 | [−0.0804, +0.0089] | 0.073 | −0.131 |

**AW had never been pinned in its own right**, although every swap control in the
thesis uses its entry as the partner field; the −0.036 was a by-product of
`label_semantics_r1`. It is now flat at the **tightest bound in the project** —
the sweep certifies 0.20 for seven coordinates and 0.10 for two.

It **supports** the swap controls without proving them: they additionally assume
AW's entry is a *fair partner* slot. `probe_fields_r1` helps here — entry 10
carried Status-quo Preference to +0.400, so the slot can carry an effect; AW's own
gloss does not produce one. That is the right shape for a partner field.

**LL, fourth measurement:** +0.271 post-hoc, −0.131 at 25 agents, −0.014 at 40,
−0.036 at 80. The effect shrinks as the sample grows and the 80-agent interval
excludes the sweep's −0.131. The withdrawal stands, as the protocol fixed in
advance. LL is bounded at 0.073 — not load-bearing, and not demonstrated inert.

## 4b. The two near-misses were real; underpowering hid them

`parameter_followup_r2`, 80 agents, both two-sided:

| Coordinate | Effect | 95% CI | Holm | Items | Prior (25 agents) |
|---|---:|---|---:|---|---:|
| **TfA** Tolerance for Asymmetry | **−0.1107** | [−0.1536, −0.0661] | 2.5e−6 | 2+/4− | −0.1029 |
| **MoR** Mode of Response | **−0.0732** | [−0.1161, −0.0304] | 0.00106 | **0+/6−** | −0.0971 |

Both reproduce their 25-agent estimates and now clear Holm. **Nothing about the
effects changed; only the power did** — 9/20 at 25–40 agents against 18/20 at 80.

**The mirror image of the LL story.** LL cleared a corrected bar at 25 agents and
dissolved at 40 and 80; TfA and MoR failed one at 25 and survive at 80. One false
positive, two false negatives, the same cause and the same remedy: choose n from
simulated power, not from budget.

Both are order-robust (gaps 0.000 and 0.004). **MoR is uniform** (6 of 7 items
negative, range −0.125 to 0.000). **TfA is not** — per-item from +0.175
(`desk_booking`) to −0.312 (`on_call`), so its pooled figure is a partial
cancellation and is reported as such.

**What it changes:** four of ten coordinates move the outcome on these items (PD,
ID, TfA, MoR), against LL null and AW flat. **What it does not change:** none of
this makes them *label* effects — no swap control was run, so TfA and MoR sit
where PD sat before `label_semantics_r1`. And §2 still applies: an invented field
beat all of them, so four movers are instances of the general finding, not
evidence that these were the right ten.

## 5. Two method findings that outlast these results

**Presentation-order dependence is a property of the item pool.**
`meeting_room` (gap 0.75) and `desk_booking` (0.73) are largely determined by
which option is printed first — unrecorded before now. **No headline result is
affected**: every contrast is paired within agent with order fixed inside the pair,
and each keeps its sign and size within both orders. But *unpaired screens* are
destroyed by it: an order-determined item averages to ~0.50 and passes a band rule
meant to catch the opposite condition, which is exactly how
`defeasibility_screen_r1` returned a false pass. **Standing rule: screens report
keep-share by order and reject a gap above 0.20.**

**An unprofiled floor is not a floor under profile.** The twins sat at 0.00–0.04
unprofiled and reached 0.775 under PD-high. A screen's baseline does not bound the
profiled range, so both screen stops were more conservative than necessary.

## 6. What Phase 7 does NOT establish

- **Bidirectionality is UNTESTED, not refuted.** `inverse_inference_r1` was built
  to ask whether the model can read a field back from behaviour. The model
  answered "B" in 94 of 120 trials — 0/19 correct in one condition when the answer
  was A — so its accuracies measure a positional bias, not inference. The
  hypothesis is untouched and a corrected two-order design remains available.
- **Precipitation is UNTESTED.** `precipitation_r1` asked whether a boundary forms
  from an agent's own prior decisions and generalises where those decisions are
  silent - the first half of Reactive Grounding's Conjecture 1, and the first test
  in this phase of something *forming* rather than being followed. It halted on a
  network timeout at call 294 of 840 and, under the no-retry rule, is not resumed.
  The 293 collected decisions are excluded: they cover one arm and part of a
  second, and every primary quantity needs all three on the same unit.
- **Understanding.** Two of six programme markers were reached
  (transformation/reversal, and selectivity in the weak sense that fields move as
  their meanings say). Defeasibility, bidirectionality, composition and the
  selectivity matrix are untested or blocked.
- **A difference between reading an explanation and following an instruction
  phrased as one.** A field reading "existing arrangements stand" is close to an
  instruction, and its success is what the instruction-following account predicts.
  Stage 3a was built to separate these and is blocked.
- **That PD encodes procedural justice.** §3 is evidence against.
- **Generality.** One model, one item family, seven items, tied payoffs.
- **Moral quality, improvement or human resemblance.** Outcomes remain a
  deterministic lookup; no human data exists.

## 7. What the paper must change

1. **Abstract**: the field-weighted-extremity disclaimer is superseded (§1); add
   that an invented field matches the verified parameter (§2).
2. **§5/§7**: "field-bound label effect" becomes a claim about the field's stated
   meaning, with the name/gloss decomposition (52% survives name removal).
3. **New section**: probe fields, and the bound they place on the architecture.
4. **§7**: PD does not behave as its name suggests (§3). This *weakens* a claim
   the paper might otherwise have made.
5. **§8 Limitations**: order dependence in two items; the screen rules that follow.
6. **Appendix A**: totals become 32,902 calls across 53 studies.

## Accounting

OpenAI $12.741596 to **$21.497550**/$40. Anthropic $22.247448 to
**$22.268707**/$32. Package about $43.766/$100. Usage estimates, not verified
provider balances.
