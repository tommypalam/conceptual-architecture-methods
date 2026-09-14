# closeout_r1 — Phase 4A closeout on repaired materials

**Screen only. No profiled arm, no participant profiles, no moral score.**

901 calls, worst case $11.386 against a $12.00 ceiling. Hard review gate.

## Why this exists

`breadth_focus_r1` stopped at its gate on a correct blocking issue: a violating
option whose **description** carried the violation, where the paired option's
description carried no corresponding clause.

`phase4_repaired_tasks` removes three such clauses. The information survives in
`effect_text`, and every flag, delta, action id and classification rule is
unchanged — `verify_repair()` enforces that the repair is a deletion from three
description strings and nothing else.

| Task | Option | Removed clause | Already in `effect_text` |
|---|---|---|---|
| `safety_hold` | `ship_as_promised` | ", without reporting the defect rate you measured" | "The measured rate is not reported." |
| `witness_cost` | `state_partially` | " while stating nothing false" | "The review record is incomplete." |
| `referral_fee` | `recommend_colleague` | " without mentioning the alternative" | "The recommendation omits the alternative." |

The third was found by an asymmetry audit in `phase4_repaired_tasks`, not by
reading; the `breadth_focus_r1` assessment had recorded two after a manual pass.

Five other options are **deliberately not repaired**: naming a refusal or a
substitution *is* the act being chosen (`include_records`, `reassign_room`,
`break_seal`, `substitute_files`), and `evidence_seal` marks both its options
symmetrically. The operative test is whether deleting the clause leaves a
complete, performable act behind.

## Three arms

| Arm | Tasks | Models | Calls |
|---|---|---|---:|
| **re-baseline** | 6 with a discriminating primary | all three | 450 |
| **breadth** | 5 coercion/unfairness, never screened | all three | 375 |
| **focus** | `safety_hold` at x2, x5, x12 (repaired) | sonnet | 75 |

**Re-baseline.** Prior measurements were taken on unrepaired text and **do not
transfer**. `haiku_screen_r4`'s modal shares and `magnitude_sweep_r1`'s x1 cells
describe different stimuli. Comparing this arm against those records also shows
how much of the earlier saturation the wording was carrying — informative either
way.

**Breadth.** `magnitude_sweep_r1` tested deception vs. utility only. If haiku is
flat here too, its rigidity is general across fixed standards; if it disperses,
that finding is deception-specific. These five have
`primary_discriminates() == False`: they close 4A, they cannot carry 4B.

**Focus.** The unrepaired `sonnet/safety_hold` curve (0.72 at x1, 0.12 at x20,
Holm 0.0005) is **not assumed**. The repaired x1 comes from the re-baseline arm
in this same designation. The aim is a cell near 0.5 — both options live — which
is what a profiled cross-model contrast needs and what `capstone_model2_r4`
lacked.

Locating a crossover is selection on **baseline dispersion**, which the Phase 3
protocol requires, not on outcomes. Every cell is reported whatever its shape.

## Gates

**Hard review gate** — repaired descriptions are new materials, so the
16 September advisory amendment does not apply. The reviewer prompt now
explicitly asks whether an option's *description* labels it with a norm violation
its paired option does not carry, so the defect that stopped `breadth_focus_r1`
is something the gate is now looking for.

Before any call: `verify_repair()`, the appended-label audit (must be clean), the
leakage audit, and a check that repair and scaling **compose** without either
undoing the other in the focus arm.

## What this cannot establish

- Nothing about whether profiles move decisions. No profiled call is made.
- No moral label, score or claim; no classification is computed.
- The breadth tasks cannot support an arm contrast even in principle.
- Results on repaired text are not comparable cell-for-cell with prior
  designations on the unrepaired text.
- n = 25 per cell, unprofiled, one snapshot.

## Verification before collection

- `verify_repair()`: situations, effect texts, deltas, all standard flags and all
  classifications identical to the frozen pool; three descriptions differ by a
  clean deletion; every repaired description still ends as a sentence.
- Appended-label audit: clean across the whole pool.
- Leakage audit: zero hits.
- Repaired text confirmed on the wire, with `effect_text` retained.
- Review packet carries text and kind only, under neutral keys; task identity,
  arm, standard type and magnitude withheld.
- Full 901-call schedule simulated end-to-end against a fake responder:
  901/901 parsed, zero errors, zero network calls; 36 cells populated and the
  crossover series spans x1 → x12.
