# label_semantics_r2: ID verified, LL fails to replicate

**Outcome: complete. 2,241 calls, 2,240/2,240 valid, zero failures.**
17 September 2026. Review **accept**, zero blocking issues. Cost $1.656270
against a $25.223 reservation.

Ledger after this designation: Claude $19.728369100/$32, OpenAI $11.093290725/$40.
Usage estimates, not wallet balances.

**ID is confirmed as a label effect. LL is demoted — it failed its own
replication gate and the coordinate map must be corrected.**

## Result

| Contrast | Effect | Pairs | raw p | **Holm** | Items |
|---|---:|---:|---:|---:|---|
| **ID:TRUE** | **+0.111** | 280 | 0.00117 | **0.00467** | 5+/1− |
| ID:SWAP | +0.046 | 280 | 0.136 | 0.408 | 5+/2− |
| LL:TRUE | **−0.014** | 280 | 0.708 | **0.708** | 4+/3− |
| LL:SWAP | −0.046 | 280 | 0.148 | 0.408 | 1+/4− |

### ID — verified

**TRUE significant, SWAP not.** The same numerals on the inert AW label produce
nothing; on the ID label they produce +0.111. That is the pattern
`label_semantics_r1` established for PD, reproduced for a second coordinate.

ID across three independent measurements:

| Measurement | ID |
|---|---:|
| post-hoc correlation (`gpt_r2`, E arm) | r = +0.303 |
| `coordinate_sweep_r2`, 25 agents, pinned | +0.143 (Holm 0.00056) |
| **this designation, 40 agents, pinned** | **+0.111 (Holm 0.0047)** |

Consistent in sign and magnitude across all three, with a null swap control.

### LL — fails its replication gate

**TRUE is −0.014 at Holm 0.708** against the sweep's −0.131. The protocol's
prespecified rule applies: *"a coordinate whose TRUE arm fails to replicate under
correction has an uninterpretable SWAP contrast, and that is reported per
coordinate."* **Nothing is claimed for LL's swap.**

LL across the same three measurements:

| Measurement | LL |
|---|---:|
| post-hoc correlation (`gpt_r2`, E arm) | **r = +0.271** |
| `coordinate_sweep_r2`, 25 agents, pinned | **−0.131** (Holm 0.00082) |
| **this designation, 40 agents, pinned** | **−0.014** (Holm 0.708) |

**Three measurements, three different answers — positive, negative, null.**

**This is not a power failure.** The sweep used 25 agents; this used 40. LL
failed on the *larger* sample. Power here was 17/20 at a true effect of 0.131,
so an effect of that size would probably have been detected.

## The corrected coordinate map

| Coordinate | Pinned effect | Label control | Status |
|---|---:|---|---|
| **PD** Procedural Dependence | **+0.339** | **SWAP −0.036** | **verified label effect** |
| **ID** Internalisation Dependence | **+0.111 to +0.143** | **SWAP +0.046, n.s.** | **verified label effect** |
| ~~LL Legitimacy Locus~~ | −0.131 then −0.014 | uninterpretable | **not replicated — withdrawn** |
| the other seven | −0.10 to +0.05 | — | not load-bearing |

**Two of ten coordinates are verified label effects, not three.**

## What this establishes

**ID joins PD as a coordinate whose label carries its effect.** Two of ten, each
with a numeral-identical swap control showing the effect disappears when the same
value sits on an inert label.

**LL's apparent effect does not survive replication**, and the coordinate map
published this morning **overstated it**. `coordinate_sweep_r2`'s LL row was
Holm-significant at 25 agents and is not reproduced at 40. That designation's
finding for LL is superseded by this one.

**The sequence is itself the finding.** LL was positive post-hoc, negative under
one manipulation, null under a larger one. A coordinate can clear a
Holm-corrected bar in a single well-powered designation and still be noise. **The
replication gate built into this protocol is what caught it** — had the swap
control been run without a TRUE arm, LL's null swap would have been read as
"the label carries it".

## What this does NOT establish

- **Not that LL is inert.** It failed to replicate; that is different from being
  measured flat. Its status is **unresolved**, not negative.
- **Not moral truth or improvement.** Deterministic classification under
  stipulated standards, never read from agent text.
- **Not that ID is understood as a concept.** It shows the field a number sits in
  determines its effect, which is weaker than comprehension.
- **Not a claim about the other seven coordinates**, untouched here.
- **Not cross-model.** `gpt-5.4-mini` only.
- **Not generalisation.** Seven items, 40 agents.
- **The drawn ID and LL values are discarded in every arm**, so this tests the
  label binding at two fixed levels, not the drawn distribution.
- **No human validation**; raters remain deferred.

## A bug caught before collection

The first population draw (seed …711) gave agent 7 **AW = 0.102**, which renders
as `0.10` in the two-decimal block and **collides with the LOW level**. That
agent's TRUE and SWAP blocks were byte-identical at L = 0.1, so the swap did
nothing and would have diluted the paired contrast.

`verify_construction()` tested degeneracy on the raw draw (`AW in (0.1, 0.9)`)
and missed it. It now tests **rendered precision** and **blocks** rather than
merely recording. The population seed was changed to …712, chosen before any call
on a property of the draw alone — the first seed whose 40 agents have no
collision. Zero degenerate agents under the replacement, and all **160 TRUE/SWAP
pairs verified numeral-identical** on the wire.

## Provenance

Review returned **accept**, zero blocking issues, three non-blocking limits.

Build-time checks before any call: `verify_construction()` across all 40 agents
and both active coordinates; `block_equivalence()` against the real renderer at
both levels for each coordinate; and a per-pair wire check across all 160
TRUE/SWAP pairs confirming identical length, identical numeral multiset,
byte-identical user text, and a rendered diff of exactly four lines confined to
the two named fields.

Power was measured before collection over the four-contrast Holm family, 20
seeds: 18/20 at ID's swept effect, 17/20 at LL's, 20/20 at 0.20, **0/20 false
positives**. The protocol recorded in advance that ID and LL are ~2.4× smaller
than PD and that a SWAP null here is weaker evidence than PD's was.

2,241 calls dispatched, 2,240 valid, zero entries in `failures.jsonl` for this
designation. Three failures remain inherited from earlier designations, preserved
and unretried.
