# probe_fields_r1 — assessment

**Complete. 2,240 calls, 2,240/2,240 valid, zero failures, $1.680032.**
`gpt-5.4-mini-2026-03-17`, 40 agents (seed 2026092001), seven items, eight cells,
20 September 2026. Protocol and locked predictions: [PROTOCOL.md](PROTOCOL.md).

Exploratory, on branch `understanding-programme-20260919`. Not part of the
submitted thesis.

## Result

The prespecified rule returned **MEANING_GENERAL**.

| Probe field | Predicted | Effect | 95% CI | Holm | Items |
|---|---|---:|---|---:|---|
| Status-quo Preference | + | **+0.4000** | [+0.3357, +0.4643] | ~0 | **7+/0−** |
| Stated-Wish Deference | + | **+0.3071** | [+0.2536, +0.3607] | ~0 | **7+/0−** |
| **Numbers Count** | **negative** | **−0.2464** | [−0.3107, −0.1821] | ~0 | **0+/7−** |
| Worst-off Priority | + | −0.0643 | [−0.1286, 0.0000] | 0.066 | 2+/4− |

Effect = share classifying `good`, printed 0.90 minus printed 0.10, paired by agent
and item; 280 units complete in all eight cells. Reference: PD CANON +0.3393
(`semantics_r1`; different slot and population, so the comparison is descriptive).

## What it shows

**1. Fields are not generic cues.** Two fields in the same slot, same format, same
numerals, moved choices in OPPOSITE directions as their explanations said — Numbers
Count negative on all seven items, Status-quo and Stated-Wish positive on all
seven. With `semantics_r1`'s FLIP this is the second independent demonstration
that direction follows stated meaning, now across fields rather than within one.

**2. PD is NOT special on effect size, and this caps the framework's claim.** A
field invented in an afternoon, naming what the items are about, gives **+0.400** —
larger than the framework's verified parameter (+0.339) and consistent on every
item where PD is 6+/1−. What the thesis verified is therefore better described as
*a glossed field whose stated meaning bears on the items moves choices*, of which
PD is one instance. Nothing in the evidence so far requires the ten parameters in
particular. **This is the outcome the programme said would not embarrass the
method but would bound the architecture, and it is reported as that.**

**3. It sharpens the status-quo worry into a live hypothesis.** On these items
"process-dominant" and "keep the existing arrangement" select the same option, and
a field that says only "keep existing arrangements" reproduces PD's effect and
more. **PD may be functioning as a status-quo dial.** These data cannot tell;
Stage 3a's illegitimate-arrangement items are built to, because there the two
readings predict opposite signs. That stage is now the programme's critical path.

**4. One prediction FAILED, and it is mine.** Worst-off Priority was predicted
positive — the holder loses 5, the most of anyone — and came out −0.064 with the
interval touching zero, 2+/4−, not surviving Holm. Nothing is claimed about its
sign. The likeliest reason is that "who would lose most" is genuinely ambiguous on
these items: the holder loses 5 if overridden, but the other side are described as
already badly placed (a corridor bench; supplies spoiling outdoors) and lose 4 if
the arrangement is kept. The derivation read "lose most" off the stipulated
numbers; the model need not. This is the project's recurring lesson in a new
place — **a designer's judgement of what wording implies does not predict model
behaviour** — and it is why FLIP-type designs, which need no such judgement, carry
more weight than derivations like this one. Per-item, `rest_break` ran +0.275 and
`desk_booking` −0.275: the field does something, item by item, that the pooled
figure hides and this design cannot resolve.

**5. Numbers Count held even where its prediction was weak.** It was flagged in
advance as item-dependent, since only some items put a countable larger group on
the overriding side. It was negative on all seven; weakest on `on_call` (−0.025),
strongest on `tool_library` (−0.475) and `storage_unit` (−0.425) — neither of which
is a clean head-count item. So "helping more people" is being read more loosely
than a literal count. Reported, not explained.

## Per-item

| Item | SQ | SW | NC | WO |
|---|---:|---:|---:|---:|
| desk_booking | +0.575 | +0.350 | −0.175 | −0.275 |
| meeting_room | +0.750 | +0.250 | −0.175 | −0.100 |
| on_call | +0.375 | +0.525 | −0.025 | +0.050 |
| rest_break | +0.175 | +0.425 | −0.300 | +0.275 |
| storage_unit | +0.450 | +0.275 | −0.425 | −0.200 |
| tool_library | +0.375 | +0.275 | −0.475 | −0.200 |
| weekend_rota | +0.100 | +0.050 | −0.150 | 0.000 |

`on_call`, negative under PD in three designations, is positive under both SQ and
SW. Whatever makes it resist PD is specific to PD's wording, not to the item being
immovable.

## What this does NOT establish

- That any probe is or should be a parameter. None is proposed.
- Understanding, or a difference between reading an explanation and following an
  instruction phrased as one. A field reading "existing arrangements stand" is
  about as close to an instruction as a field can be; its success is exactly what
  the instruction-following account predicts.
- Magnitudes. This was a 40-agent screen. SQ > PD is descriptive: different slot,
  different agents, no direct within-unit contrast.
- Anything beyond this model and these seven items.

## Accounting

OpenAI $14.407543 → **$16.087575**/$40. Anthropic unchanged $22.247448/$32.
Package ≈ $38.335/$100. Usage estimates, not verified provider balances.
