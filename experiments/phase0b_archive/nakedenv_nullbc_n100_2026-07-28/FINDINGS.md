# Phase 0b — null_b / null_c under the naked-envelope delivery (N=100, 2026-07-28)

Delivery: user_prefix (NO system message) + bare-label output + max_tokens 20.
This is the SAME delivery that made null_a (empty harness) bistable on all six
problems. Here it is applied to null_b (population means at neutral config) and
null_c (sham profile). Recalibrated dilemmas. Prompts FROZEN.

## Three conditions, same delivery (opt0 rate)

| prob | null_a (empty) | null_b (neutral means) | null_c (sham) |
|------|----------------|------------------------|---------------|
| S1 | 0.60 | 1.00 | 0.98 |
| S2 | 0.32 | 0.03 | 0.09 |
| S3 | 0.60 | 0.13 | 0.67 |
| C1 | 0.49 | 0.61 | 0.52 |
| C2 | 0.69 | 0.02 | 0.92 |
| C3 | 0.73 | 0.82 | 0.50 |

(null_a values from bare_nosys_all6_n100_2026-07-28.)

## Result: the profile bias PERSISTS under the naked envelope

The delivery fix (naked envelope) solved the empty-harness (null_a) collapse but
did NOT neutralise the profiles. The signature is unchanged from the old
canonical N=200 grid:
- C2 / null_b: 2% APPROVE (98% REJECT) — the same full flip seen under the
  DECISION-format system message. Delivery format was NOT the cause of C2's flip.
- S1 / null_b: 100% A. S3 / null_b: 13% ADOPT. S1 / null_c: 98% A.

So null_b ("population means at neutral configuration") is NOT behaviourally
neutral: the specific mid-range parameter values (LL 0.58, PD 0.56, TfA 0.36,
ID 0.60, ...) themselves steer the decision. Likewise null_c (sham profile)
imposes its own direction.

## Interpretation — this is signal, not a bug

A "null" condition per spec §2.1.2 is expected to sit near 50/50. It does not,
because "neutral MEANS" is not the same as "no signal": injecting a full
8-parameter profile at mid values gives the model concrete inputs it acts on.

This is the SAME mechanism Phase 2 relies on (parameters -> distinguishable
decisions). null_b's strong parameter-sensitivity is, in that light, evidence
the encoding is potent. The tension is purely definitional: §2.1.2 treats a
mean-valued profile as a null, but on this model a mean-valued profile is an
active input.

## Data note
7-14 unparsed/api/refusal per null_c cell (max_tokens 20 is tight for some
responses). Rates are over parsed decisions. A slightly higher cap (e.g. 30)
may reduce loss without reintroducing the reasoning collapse.

## Open question for the 0b design (decision needed)

The null-condition pass criterion (§2.1.4: Wilson CI contains 50% in all cells)
is not achievable while a mean-valued profile is itself an active input. Options:
1. Redefine null_b: use NO profile (i.e. null_b == null_a empty) as the true
   null, and treat "population means" as a separate (non-null) reference cell.
2. Keep null_b but change the pass criterion: a neutral profile need not yield
   50/50; it need only sit BETWEEN the high/low parameterisations (a monotonicity
   / ordering test) rather than at 50/50.
3. Accept null_a as the sole neutrality guarantee (empty harness is neutral =
   the harness adds no bias); characterise null_b/null_c as parameter-sensitivity
   evidence, not neutrality tests.

## Prompts FROZEN. No dilemma text edited.
