# Phase 0b — null_a task-text sweep (neutral envelope, N=100, 2026-07-29)

3 null_a TASK variants (orig / neutral / minimal) x fragile trio {S2, C2, C3} x
N=100, under the blessed neutral delivery (user_prefix + bare_label, max_tokens
30). Only the task text varies. Recalibrated dilemmas. Prompts FROZEN.

## Results (opt0 rate; bistable = minority >= 20%)

| task | C2 | C3 | S2 |
|------|----|----|----|
| orig ("apply a consistent decision-making rule") | 1.00 collapse | 0.97 collapse | 0.13 collapse |
| neutral ("consider and choose one option") | 1.00 collapse | 0.76 BISTABLE | 0.56 BISTABLE |
| minimal ("answer in the format") | 1.00 collapse | 1.00 collapse | 0.16 collapse |

## Findings

1. The "neutral" rewording (drop "consistent rule") RESCUES C3 and S2 — wording
   of the task matters for those two.
2. "minimal" is WORSE than "neutral" (C3 collapses at minimal, bistable at
   neutral): it is not "less framing = better"; the specific neutral phrasing
   does active good.
3. **C2 collapses to 100% APPROVE under ALL THREE task variants** — no task-text
   change touches it.

## The C2 crux (resolved by diffing messages)

C2 was 69% BISTABLE in the bare_nosys run (bare_nosys_all6_n100_2026-07-28). The
only structural difference from this sweep's collapsed C2:

- bare_nosys message = dilemma + "Reply with only: APPROVE or REJECT". NOTHING else.
- this sweep message = "You are participating in a decision-making simulation.
  # Your task. Consider the decision below and choose one option. Do not infer
  demographic identity ..." + dilemma + bare label.

=> For C2, the collapse is driven by the PRESENCE of the preamble + task
scaffolding itself, not its wording. C3/S2 tolerate neutral-worded scaffolding;
C2 tolerates none.

## Conclusion

The ONLY null_a configuration neutral across all six problems is the FULLY-NAKED
one: dilemma + bare label, with NO "decision-making simulation" preamble and NO
"# Your task" block. That is exactly bare_nosys, already measured bistable on all
six (bare_nosys_all6_n100_2026-07-28).

Any scaffolding ("# Your task", "decision-making simulation", "do not infer
identity") collapses at least C2.

## Design tension for the decision (unchanged, now fully evidenced)

The preamble + task block is structurally WHERE Phase 2 injects the parameter
profile. A fully-naked null_a is neutral but no longer mirrors the Phase-2
harness structure. Options on the table:
1. Adopt fully-naked as null_a AND rethink Phase-2 profile injection to match
   (profile delivered without the "# Your task / simulation" scaffolding).
2. Keep the scaffolding for Phase 2 but accept null_a can only be neutral naked;
   report the scaffolding as a measured harness effect and rely on the
   parameter-CONTRAST (null_b/null_c vs null_a) rather than absolute neutrality.
3. Investigate WHICH scaffolding token collapses C2 (preamble line vs "# Your
   task" header vs "do not infer identity" clause) — one more cheap sweep — to
   find the minimal scaffolding C2 tolerates.

## Prompts FROZEN. No dilemma text edited.
