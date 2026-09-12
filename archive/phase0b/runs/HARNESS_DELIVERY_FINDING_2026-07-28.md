# Phase 0b Harness-Delivery Investigation (2026-07-28, after recalibration)

## Scope

Phase 0a is LOCKED. The recalibrated dilemmas are bistable NAKED (all six with
minority >=20% at N>=300, bare "Reply with only: X or Y" format). The remaining
problem is entirely in Phase 0b's scope: the HARNESS collapses several of these
bistable dilemmas back to a deterministic extreme.

## What was tested

Smoke grid (N=50, all 18 cells, recalibrated set) showed:
- S3, C1 SURVIVE the harness: null_a (empty harness) split ~= naked split.
- S2, C2, C3 COLLAPSE under the harness (near 0/100), including C3 which was
  never drifted or recalibrated -> the collapse is a harness x dilemma
  interaction, not a calibration failure.

## Reconciling two "naked" rigs (the key measurement)

Two separate code paths both claim to send a "naked" prompt but gave DIFFERENT
splits for the same dilemma. Diffing the exact recorded prompts:

| Rig | Format instruction | max_tokens | system msg | C2 result |
|-----|--------------------|-----------|-----------|-----------|
| recalibrate | `Reply with only: APPROVE or REJECT` (bare label) | 20 | none | 64% APPROVE |
| ablation naked_repro | `Respond in exactly this format:\nDECISION: [APPROVE \| REJECT]` | 600 | none | 100% APPROVE |
| smoke null_a | `DECISION: [.. \| ..]` + REASONING | 600 | yes | 100% APPROVE |

## Corrected conclusion (an earlier note was WRONG)

An earlier working note claimed "the system message is the single cause;
naked_repro restores bistability." **That was wrong** and is retracted. The
N=100 confirm on the recalibrated set (archived confirm_naked_vs_canonical_
recalib_2026-07-28) shows:

| Problem | recalibrate bare (naked truth) | naked_repro (DECISION fmt, no sys) | null_a (DECISION+reason+sys) |
|---------|-------------------------------|------------------------------------|------------------------------|
| C2 | 64% APPROVE | 100% APPROVE | 100% APPROVE |
| C3 | ~55% CONTINUE | 21% CONTINUE (flips to PIVOT) | 99% CONTINUE |
| S2 | 34% REPORT | 17% REPORT | 0% REPORT |

There is NO single universal collapsing lever:
- C2 collapses at the `DECISION: [X | Y]` format step (naked_repro already 100%,
  before any system message or reasoning). The structured decision-token format
  is the driver for C2.
- C3 is an interaction: `DECISION` format alone pushes it toward PIVOT (21%
  CONTINUE), but adding the system message + REASONING slams it back to
  CONTINUE (99%). Opposite forces, dilemma-specific.
- S2 shifts under both format and harness, never reaching its 34% naked truth.

## Interpretation

The decision surface for these dilemmas is steep and idiosyncratic at the
HARNESS level, exactly as it was at the naked wording level. Each dilemma
responds to a different harness element, and some respond in opposite
directions. Searching for one harness configuration that holds all six bistable
is likely a random walk, the same trap encountered (and abandoned) during
prompt tweaking.

## Prompts remain FROZEN throughout this investigation. No dilemma text edited.

## Archived runs
- smoke_recalibrated_n50_2026-07-28/ (18-cell smoke, moved out of the real tree)
- confirm_naked_vs_canonical_recalib_2026-07-28/ (C2/C3/S2, canonical vs naked_repro, N=100)
