# semantics_r1 — protocol

**Status: prepared offline. NOT released, NOT authorised, no API call made.**
Programme context: [../PROGRAMME.md](../PROGRAMME.md). Exploratory; not part of
the submitted thesis.

## Question

Does the Procedural Dependence effect follow what the PD scale is *said to mean*,
or the name and the number regardless of the explanation?

## Run statement (rule 4)

| | |
|---|---|
| Model | `gpt-5.4-mini-2026-03-17`, temperature 1, reasoning disabled |
| Configuration | NEUTRAL on all five axes (`-----`), as every Phase 4B/5 call |
| Agents | 40, independent Beta marginals, seed **2026091901** |
| Items | the seven screened gpt items of `phase4b_perm_pool`, byte-identical |
| Cells | 4 variants × 2 levels = 8; **2,240 calls**, one run |
| Seeds | population 2026091901, schedule 2026091902, analysis 2026091903 |
| Cost | $10.976 reserved worst case; about $1.66 expected at settlement |

## Design

PD is pinned to 0.10 and 0.90 under four renderings of the PD entry. The nine other
entries, the item text and the user turn are byte-identical across all eight cells.

| Variant | Line 6 reads | Endpoint explanation |
|---|---|---|
| CANON | `Procedural Dependence` | canonical — byte-identical to the parent's prompt |
| FLIP | `Procedural Dependence` | the two endpoint texts exchanged |
| INVERT | `Outcome Dominance` | exchanged |
| NONCE | `Factor K` | canonical |

Verified for all 40 agents before any call (`leakage_gate`): within a variant the two
levels differ on exactly one line and are equal in length; across variants only the
PD entry's three lines differ; FLIP is a pure rearrangement of CANON's characters
and applying it twice restores the block byte for byte; CANON equals the parent
collector's system prompt byte for byte; the canonical name appears nowhere in
INVERT or NONCE.

## Locked predictions

Effect = share classifying `good`, printed 0.90 minus printed 0.10, paired by
agent and item.

| Variant | MEANING | NAME | EXTREMITY |
|---|---|---|---|
| CANON | + | + | + |
| **FLIP** | **negative** | + | + |
| INVERT | negative | ~0 | + |
| NONCE | + | ~0 | + |

Content hash of the design and predictions:
`7d00c81efc2234b77ff02e2acafdbadc41fe55ca42a8877edc169eeef1a87a8a`.

## Analysis, fixed before collection

1. **Gate.** CANON must replicate: one-sided sign test, Holm over the four
   within-variant tests, positive in at least 4 of 7 items. If it fails, the
   designation reports a failed gate and interprets nothing else.
2. **Primary.** The within-unit differences `e_CANON − e_V` and each `e_V`, with
   95% unit-bootstrap intervals (10,000 draws, agent-item units complete in all
   eight cells, conditional on the tested items).
3. **Descriptive.** Reversal indices `e_FLIP/e_CANON`, `e_INVERT/e_CANON` and the
   transfer index `e_NONCE/e_CANON`. Ratios are unstable near a small denominator
   and do not lead.
4. **Decision rule on FLIP.** *Meaning carries it*: `e_FLIP < 0`, interval
   excluding zero, negative in ≥ 4 of 7 items. *Explanation ignored*: `e_FLIP > 0`,
   interval excluding zero. *Conflict*: anything else, reported as such.
5. No conclusion is drawn from one arm being significant while another is not.
   All seven items are primary; none is dropped after results. No cell is re-run.

Power (20 seeds, measured baselines, Holm family 4): full reversal 20/20; −0.20
20/20; −0.15 18/20; −0.10 8/20; false positives 0/20.

## Disclosed differences from the parent, `position_counterbalance_r1`

1. **Output cap 256, not 1,536.** The longest of the parent's 2,240 replies was 21
   tokens. A truncated reply would be preserved as a failure and never retried.
2. **No review call.** The items are byte-identical to material the parent's review
   accepted with zero blocking issues, and the review packet never included the
   profile block. Under the 16 September amendment such a review is advisory and
   re-running it is forbidden; the parent's verdict is read from the ledger and
   reported. *The edited PD entry is new material that no reviewer has seen* — a
   reviewer judges item wording, and the entry's validity rests instead on the
   byte-level construction checks above.
3. **Fresh population seed**, so CANON is a replication on new agents.

## What no outcome establishes

Understanding beyond tracking the stated meaning of a scale; a difference between
reading an explanation and following an instruction phrased as one; anything about
other fields, other models, or items outside these seven; moral quality or human
resemblance.
