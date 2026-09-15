# label_semantics_r2 — do the ID and LL labels carry their effects?

**2,241 calls, worst case $25.223 against a $28.00 ceiling. Hard review gate.**

## The gap this closes

`coordinate_sweep_r2` found three of ten coordinates load-bearing:

| Coordinate | Effect | Holm | Label control |
|---|---:|---:|---|
| PD | +0.339 | ≈ 0 | **done** — `label_semantics_r1` |
| **ID** | **+0.143** | 0.00056 | **none** |
| **LL** | **−0.131** | 0.00082 | **none** |

`label_semantics_r1` proved the PD effect belongs to the PD **label**: the same
numerals on the inert AW label gave −0.036. **ID and LL have had no such
control.** Every assessment records them as load-bearing *coordinates*, not
demonstrated *label* effects. This designation runs the control.

## Design

For each active coordinate A ∈ {ID, LL}, each agent, and each level L ∈ {0.1, 0.9}:

| Arm | A's field | AW's field |
|---|---|---|
| **TRUE(L)** | **L** | drawn AW |
| **SWAP(L)** | drawn AW | **L** |

Both arms carry the multiset {L, drawn-AW} across those two fields, so the blocks
are **numeral-identical** — same length, same ten numbers, same field order. Only
which of the two labels holds L differs.

**AW is the inert partner**, as it was for PD. It is the only coordinate measured
inert by two independent methods: post-hoc correlation (r = −0.051, −0.167, both
Holm 1.000) and prospective manipulation (−0.036, Holm 1.000). CS and RT are also
flat in the sweep but have one measurement each.

40 agents × 2 coordinates × 4 arms × 7 items = **2,240 profiled decisions**.

**Verified across all 160 TRUE/SWAP pairs before collection:** numeral-identical,
byte-identical user text, rendered diff confined to four lines in the two named
fields.

## A bug caught before collection, and recorded

The first population draw (seed …711) gave agent 7 **AW = 0.102**, which renders
as `0.10` and **collides with the LOW level**. That agent's TRUE and SWAP blocks
were byte-identical at L = 0.1, so the swap did nothing and would have diluted
the paired contrast.

`verify_construction()` originally tested degeneracy on the raw draw
(`AW in (0.1, 0.9)`) and missed it, because the block renders to two decimals.
The check now tests **rendered precision** and **blocks** rather than merely
recording. The population seed was changed to …712, chosen before any call on a
property of the draw alone — the first seed whose 40 agents have no such
collision. Zero degenerate agents under the replacement.

## Locked prediction

**TRUE should reproduce the sweep** — ID around +0.143, LL around −0.131. A
coordinate whose TRUE arm fails to replicate under correction has an
**uninterpretable** SWAP contrast, reported per coordinate. TRUE gates each
coordinate separately.

**SWAP is the test and is not predicted directionally:**

| Outcome | Reading |
|---|---|
| SWAP ≈ 0 while TRUE significant | the **label-to-value binding** carries that coordinate's effect, as for PD |
| SWAP comparable to TRUE (≥ 75%) | the model responds to **numeric extremity**, and that coordinate's result is a presentation effect |
| SWAP significant but smaller | partial; reported as measured, neither reading claimed |

## Power, measured before collection

Holm over the four pooled contrasts as one family, 40 agents, 20 seeds:

| True gap | Power |
|---:|---:|
| 0.131 (LL's swept effect) | 17/20 |
| 0.143 (ID's swept effect) | 18/20 |
| 0.20 | 20/20 |
| 0.34 (PD, for scale) | 20/20 |
| 0 (null) | **0/20** |

**A caution stated in advance.** PD's effect was +0.339 and its swap control was
comfortably powered. ID and LL are roughly 2.4× smaller, so their TRUE arms sit
nearer the edge of what 40 agents resolve, and **a SWAP null here is weaker
evidence than PD's was**.

## Failure is a result

If a coordinate's SWAP is indistinguishable from its TRUE, that coordinate's
effect is a **presentation effect** and is reported as such, not reframed.

## What this cannot establish

- **Not moral truth or improvement.** Deterministic classification under
  stipulated standards, never read from agent text.
- **Not a claim about the other seven coordinates.**
- **Not cross-model.** `gpt-5.4-mini` only.
- **Not generalisation.** Seven items, 40 agents.
- **The drawn ID/LL value is discarded in every arm** — this tests the label
  binding at two fixed levels, not the drawn distribution.
- **No human validation**; raters remain deferred.
