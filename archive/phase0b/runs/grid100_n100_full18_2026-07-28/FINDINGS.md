# Phase 0b Diagnostic — Full 18-Cell Grid (N=100)

**Date:** 2026-07-28
**Run tag:** grid100
**Model:** gpt-5.4-mini (version string `gpt-5.4-mini-2026-03-17` as returned by the API)
**Protocol:** spec §2.1 — 3 null conditions × 6 problems × N=100 = 1,800 calls, temperature 1.0, DECISION+REASONING, one immutable JSON per call.
**Status:** ARCHIVED diagnostic. NOT a canonical result. Raw per-call JSON + `SCORED_summary.json` are in this folder.

> This run is a diagnostic probe, deliberately kept out of any canonical
> `phase0b_harness_neutral/` results directory. It documents a systemic harness
> bias discovered before committing to Phase 2. Nothing here modifies the locked
> Phase 0a archive or the validated dilemma prompts.

---

## Result: 2 / 18 cells balanced

Pass = Wilson 95% CI on the reported option contains 50%.

| cond | prob | n_ok | split | CI(95%) | verdict |
|------|------|------|-------|---------|---------|
| null_a | C1 | 100 | PACKAGE_A 11, PACKAGE_B 89 | [0.06, 0.19] | FAIL (lean PACKAGE_B) |
| null_a | C2 | 100 | APPROVE 100 | [0.96, 1.00] | FAIL (lean APPROVE) |
| null_a | C3 | 100 | CONTINUE 100 | [0.96, 1.00] | FAIL (lean CONTINUE) |
| null_a | S1 | 100 | A 59, B 41 | [0.49, 0.68] | **PASS** |
| null_a | S2 | 100 | LOCAL_CORRECTION 100 | [0.96, 1.00] | FAIL (lean LOCAL_CORRECTION) |
| null_a | S3 | 100 | ADOPT 23, WAIT 77 | [0.16, 0.32] | FAIL (lean WAIT) |
| null_b | C1 | 100 | PACKAGE_A 41, PACKAGE_B 59 | [0.32, 0.51] | **PASS** |
| null_b | C2 | 100 | REJECT 100 | [0.96, 1.00] | FAIL (lean REJECT) |
| null_b | C3 | 100 | CONTINUE 100 | [0.96, 1.00] | FAIL (lean CONTINUE) |
| null_b | S1 | 100 | A 100 | [0.96, 1.00] | FAIL (lean A) |
| null_b | S2 | 100 | LOCAL_CORRECTION 100 | [0.96, 1.00] | FAIL (lean LOCAL_CORRECTION) |
| null_b | S3 | 100 | ADOPT 4, WAIT 96 | [0.02, 0.10] | FAIL (lean WAIT) |
| null_c | C1 | 100 | PACKAGE_A 31, PACKAGE_B 69 | [0.23, 0.41] | FAIL (lean PACKAGE_B) |
| null_c | C2 | 100 | APPROVE 91, REJECT 9 | [0.84, 0.95] | FAIL (lean APPROVE) |
| null_c | C3 | 100 | CONTINUE 82, PIVOT 18 | [0.73, 0.88] | FAIL (lean CONTINUE) |
| null_c | S1 | 100 | A 90, B 10 | [0.83, 0.94] | FAIL (lean A) |
| null_c | S2 | 100 | FORMAL_REPORT 1, LOCAL_CORRECTION 99 | [0.00, 0.05] | FAIL (lean LOCAL_CORRECTION) |
| null_c | S3 | 100 | ADOPT 71, WAIT 29 | [0.61, 0.79] | FAIL (lean ADOPT) |

---

## Per-problem consistency across the three null conditions

The key diagnostic: does a problem lean the **same direction** under null_a (empty
harness), null_b (neutral means), AND null_c (sham/gibberish profile)?

| problem | null_a | null_b | null_c | verdict |
|---------|--------|--------|--------|---------|
| S1 | A | A | A | **SAME all three** |
| S2 | LOCAL_CORRECTION | LOCAL_CORRECTION | LOCAL_CORRECTION | **SAME all three** |
| S3 | WAIT | WAIT | ADOPT | mixed |
| C1 | PACKAGE_B | PACKAGE_B | PACKAGE_B | **SAME all three** |
| C2 | APPROVE | REJECT | APPROVE | mixed |
| C3 | CONTINUE | CONTINUE | CONTINUE | **SAME all three** |

---

## Diagnosis

**Systemic harness bias, not a per-problem or parameter-driven effect.**

1. **The lean is independent of parameter content.** For S1, S2, C1, C3 the model
   leans the *same way* even under null_c, where the parameter block is random
   gibberish (`Parameter X1: 0.23 (0 = tovcra; 1 = siltov)`) and the config is
   meaningless tokens. If nonsense parameters produce the same decision as real
   ones, the parameters are not causing the decision — the harness-wrapped
   dilemma is.

2. **The naked-prompt balance does not survive the harness.** Phase 0a validated
   all six dilemmas at ~50/50 under a *naked* prompt (no system prompt). Wrapping
   the identical dilemma text in the Phase 2 system-prompt harness collapses most
   of them to near-deterministic answers (S2 → LOCAL_CORRECTION 99–100/100 under
   all three conditions; C3 → CONTINUE 82–100; S1 → A 59→100).

3. **Reasoning evidence (null_b/S1, 50/50 sub-run):** every one of 50 reasonings
   cited the same meta-rule — "the criteria are balanced, and when balanced I
   weight reliability/stability → Candidate A." (`reliab` in 50/50, `balanced`
   49/50, `tie` 25/50.) The harness appears to convert a genuine dilemma into a
   rule-execution task, and a rule-executor resolves ambiguity deterministically.

4. **null_a still fails on 4/6 problems** despite having NO parameter block and
   NO normative-context block. This points at the **task framing** ("apply the
   decision-making profile as a decision rule … do not refuse to decide") as a
   prime suspect, more than the parameter or config blocks.

## Spec mapping

Per spec §2.3: *"Two or more null-condition failures across multiple problems
indicates a systemic problem with the prompt template rather than a
problem-specific issue. The contingency is a wholesale prompt-template revision
… revisited in dialogue with the supervisor before any further work."*

16/18 cells fail across 5 of 6 problems → this is the systemic-template case, not
a per-problem rebalance.

## Constraint on the fix (owner's decision, 2026-07-28)

**Do NOT rewrite the dilemma prompts.** The six dilemmas are the Phase-0a-validated,
frozen problem set. The fix must come from the **harness** (system-prompt
template / null-condition framing), tuned by trial-and-error, leaving the
dilemma bodies untouched. See the harness A/B trials (separate tag).

## Cost

1,800 calls at the ~$0.001/call budgeting figure ≈ $1.80. This diagnostic caught
a systemic contamination that would have invalidated a full Phase 2 run
(~$3,500+) — exactly the saving Phase 0b is designed to produce.
