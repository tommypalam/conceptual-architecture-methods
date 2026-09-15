# label_semantics_r1: the label carries the effect, not the numerals

**Outcome: complete. 1,296 calls, 1,296/1,296 valid, zero failures.**
17 September 2026. Review **accept**, zero blocking issues. Cost $0.900097
against a $14.354 reservation.

Ledger after this designation: Claude $19.701708400/$32, OpenAI $6.868692600/$30.
Usage estimates, not wallet balances.

**The permutation confound is resolved.** Move the same number from the
Procedural Dependence line to the Affective Weighting line and the effect
disappears.

## Result

| Arm | PD field | AW field | Good-rate | n |
|---|---|---|---:|---:|
| **TRUE+** | **0.9** | drawn | **0.729** | 280 |
| **TRUE−** | **0.1** | drawn | **0.389** | 280 |
| **SWAP+** | drawn | **0.9** | 0.557 | 280 |
| **SWAP−** | drawn | **0.1** | 0.593 | 280 |
| U (no profile) | — | — | 0.429 | 175 |

| Contrast | Effect | Discordant | raw p | **pooled Holm** | Consistency |
|---|---:|---|---:|---:|---|
| **TRUE** (0.9 vs 0.1 on PD) | **+0.339** | 107 / 12 | < 10⁻⁸ | **≈ 0** | 6+ / 1− |
| **SWAP** (same numbers on AW) | **−0.036** | 27 / 37 | 0.260 | **1.000** | 2+ / 4− |

Per item, Holm-corrected over the doubled 16-member family:

| Item | TRUE | Holm | SWAP | Holm |
|---|---:|---:|---:|---:|
| `rest_break` | **+0.700** | **≈ 0** | −0.050 | 1.000 |
| `tool_library` | **+0.675** | **≈ 0** | −0.175 | 0.430 |
| `storage_unit` | **+0.650** | **0.000003** | −0.075 | 1.000 |
| `desk_booking` | **+0.250** | **0.0234** | +0.100 | 1.000 |
| `meeting_room` | +0.100 | 1.000 | −0.125 | 0.625 |
| `weekend_rota` | +0.100 | 1.000 | +0.000 | 1.000 |
| `on_call` | −0.100 | 1.000 | +0.075 | 1.000 |

**Four items survive Holm on TRUE. Zero on SWAP.**

## What the manipulation was

Both arms carry an identical ten-line block with the **identical multiset of
numerals**, identical length, identical field order. The only difference:

```
- 6. Procedural Dependence: 0.90
+ 6. Procedural Dependence: 0.61
- 10. Affective Weighting: 0.61
+ 10. Affective Weighting: 0.90
```

Verified across all 40 agents before collection: **80/80 arm pairs
numeral-identical**, user text byte-identical, rendered diff confined to exactly
four lines in the two named fields, zero degenerate agents.

## What this establishes

**The label-to-value binding carries the effect.** The same numerals in the same
block produce a 34-point swing when `0.9` sits on Procedural Dependence and
nothing at all when it sits on Affective Weighting. This is not a formatting cue,
a verbosity effect, or a response to numeric extremity: extremity was held
constant and moved.

**It resolves what `phase4b_permutation_r2` could not.** That designation
deranged all ten labels at once, measured E−P = +0.089 and failed its rule at
pooled Holm 0.084. The dilution explanation is now confirmed: a ten-binding
derangement spreads the contrast across coordinates that carry no signal. **One
binding on a coordinate that does carry signal gives +0.339 at Holm ≈ 0.**

**TRUE replicates `pd_prospective_r1` on an independent draw.** +0.339 here
against +0.346 there, different population seed, same seven items. The
replication check the protocol required as a gate on the whole designation
passed.

**AW is confirmed inert, prospectively.** Phase 5's integrated analysis measured
AW as the weakest coordinate post-hoc (r = −0.051, −0.167). Pinning it to 0.1 and
0.9 moves nothing (−0.036, p = 0.260). CLAUDE.md flags AW as preliminary; that
flag is now supported by a manipulation, not only a correlation.

## What this does NOT establish

- **Not moral truth, and not moral improvement.** Every label is a deterministic
  classification under stipulated standards, computed from stipulated
  transitions and never read from agent text.
- **Not that the model "understands" procedural dependence.** It shows the field
  a number sits in determines its effect. Whether that constitutes representing
  the concept is a further question this does not answer.
- **Not a claim about the other eight coordinates.** Only PD and AW were moved.
  The result shows one label is load-bearing and one is not; it says nothing
  about the remaining eight, which may be either.
- **Not that every label is load-bearing.** AW is a label and it is inert. The
  finding is that labels *can* be load-bearing, not that they all are.
- **Not cross-model.** `gpt-5.4-mini` only. PD was flat on haiku (r = +0.089), so
  no transfer is assumed.
- **Not generalisation.** Seven items, n = 40 agents, one harness, one snapshot.
- **The drawn PD value is discarded in every arm.** This designation tests the
  label binding at two fixed levels, not the drawn PD distribution. Disclosed in
  `LOCKED_PREDICTION` before collection.
- **`on_call` ran negative on TRUE** (−0.100), as it did in `pd_prospective_r1`.
  One item of seven consistently does not follow the pattern, and that is
  reported rather than smoothed.
- **No human validation**; raters remain deferred.

## Effect on the standing caveat

Every Phase 4B assessment carries: *"A shift under a numeric block is consistent
with the block acting as an elaborate context cue."*

**That caveat is now answered for PD.** A cue account must explain why the
identical block, with the identical ten numerals, produces +0.339 when `0.9` sits
on one line and −0.036 when it sits on another. It cannot.

The caveat is **not** retired in full: `phase4b_permutation_r2`'s ten-binding
test still failed its own rule, and this designation tests two labels of ten. The
honest statement is that **the cue reading is ruled out for the coordinate that
carries the effect**, which is the part that mattered.

## Provenance

Review returned **accept**, zero blocking issues, three non-blocking limits, all
recorded — the same seven-item packet that `phase4b_permutation_r3` blocked and
that `permutation_r2`, `pd_prospective_r1` and this designation accepted. Five
reviews on this packet now stand at four accepts and one revise.

Build-time checks before any call: `verify_construction()` confirming the TRUE
and SWAP multisets are identical, no label keeps a value it should not, the eight
untouched coordinates are unchanged, and no agent is degenerate;
`block_equivalence()` against the real renderer at both levels; and a per-agent
wire check across all 40 agents.

Power was measured before collection over the doubled 16-member Holm family:
16/16 at a gap of 0.20 and at the PD effect size, 14/16 at 0.15, 7/16 at 0.10,
**0/16 false positives at gap 0**. TRUE's +0.339 is well inside the powered
range. SWAP's −0.036 is below it, so a true SWAP effect smaller than ~0.12 would
not have been detected — the prespecified reading for that case was "smaller than
TRUE", which is what is reported.

1,296 calls dispatched, 1,296 valid, zero entries in `failures.jsonl` for this
designation. Three failures remain inherited from earlier designations, preserved
and unretried.
