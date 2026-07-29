# Phase 0b Remediation Plan — Within-Scope, Prompt-Edits Last Resort

**Date:** 2026-07-28
**Owner directive:** stay strictly inside Phase 0b; treat dilemma-prompt edits as a
LAST RESORT; supervisor is consulted only after Phases 0 and 1 are complete;
proceed rigorously. Model is `gpt-5.4-mini` (older → drift assumed small/stable).

**Established diagnosis (see DIAGNOSIS_2026-07-28.md):** the 0b collapse has two
causes — (1) the system-role message (secondary; removing it recovered C2, S3,
improved S1) and (2) model drift (dominant; S2, C1, C3 hard-drifted from the May
baseline even under a faithful naked reproduction). Ruled out with data:
parameter content, every single framing clause, and the forced REASONING output.

---

## Guiding principles

1. **Exhaust harness levers before any dilemma edit.** Dilemmas are the frozen
   Phase-0a-validated set. Editing one is the last resort and, when done, is a
   controlled rebalance (spec §2.2.2), archived like the Phase-0a variants.
2. **One variable at a time, at decision-grade N.** N=30 is a direction probe;
   N≥100 is needed before any keep/rebalance decision (±~10pp CI).
3. **Pin the model.** Every remediation run records `model_version` (already
   done). If the API exposes a dated snapshot id, pin it so the baseline cannot
   drift again mid-remediation. Today's alias resolves to
   `gpt-5.4-mini-2026-03-17`.
4. **Archive, never pollute.** All runs go to `experiments/phase0b_archive/`
   under dated tags. A canonical `phase0b_harness_neutral/` directory is written
   ONLY by the final accepted configuration.

---

## Definitions the plan depends on

- **"Balanced"** = Wilson 95% CI on the reported option contains 50% (spec §2.1.4).
- **"Recovered"** = a problem that was collapsed under the current harness becomes
  balanced under a candidate harness change.
- **"Hard-drifted"** = balanced under NO harness is still impossible because the
  current model itself no longer splits 50/50 on the frozen dilemma (S2, C1, C3
  candidates from the N=30 naked_repro read).

---

## The key scoping subtlety (why this is more than "delete the system prompt")

The spec 0b pass criterion requires all three NULL CONDITIONS to balance. But
null_a/null_b/null_c are defined AS system-prompt variants. If the remediation is
"no system message," the null-condition apparatus must be **re-expressed in the
user turn** (the profile/neutral/sham blocks moved into the user message, or the
null semantics reproduced without a system role). So "fix the harness" =
"re-house the null apparatus + re-run the grid," all harness work, zero dilemma
edits.

---

## Ordered plan

### Step A — Widen the naked_repro signal (decision-grade drift map)
- **What:** re-run `naked_repro` vs `canonical`, all 6 problems, **N=100**.
- **Why:** the N=30 read (3/6 recovered) has wide CIs. We need a solid per-problem
  classification: {recovered-by-no-system} vs {hard-drifted}.
- **Cost:** ~$1.20 (2 × 6 × 100).
- **Decision output:** a definitive list of which problems the no-system lever
  can rescue and which are genuinely drift-broken.

### Step B — Build the no-system Phase-2 harness (if Step A shows ≥ meaningful recovery)
- **What:** a harness variant that injects the real parameter profile + config
  via the USER turn, with NO system message; re-express null_a/b/c accordingly.
- **Why:** Step A tests the empty harness; Phase 2 needs the *parameterised*
  harness. This is the real deliverable if no-system is the fix.
- **Cost:** build only (no API). SOLID: a new delivery block, swappable; the
  runner/assemblers unchanged in contract.

### Step C — Re-run the full 18-cell grid on the no-system harness, N=100
- **What:** the spec §2.1 grid under the new delivery.
- **Cost:** ~$1.80.
- **Decision output:**
  - If ≥ most cells balance → the no-system harness is the fix; proceed to a
    confirmation run at higher N and lock it. **No dilemma edits.**
  - Cells still failing = the hard-drifted set → Step D.

### Step D — LAST RESORT: controlled rebalance of hard-drifted dilemmas
- **Trigger:** only the specific problems that fail Step C AND were classified
  hard-drifted in Step A.
- **What:** minimal wording nudges to re-center the split on the CURRENT model,
  preserving the parameter-activation cluster and conceptual tension (the exact
  discipline Phase 0a used — e.g. the S3 Strategic-Pivot → Department-Reorg
  rebalance). Each candidate archived with its N=200 split, like the 0a variants.
- **Constraint:** change wording, never the concept mapping or the primary
  parameters a problem is designed to activate (§6.1.1). Document every variant.
- **Cost:** iterative, ~$0.20–0.60 per variant × however many iterations a
  problem needs (0a needed up to ~20 for the hardest).

### Step E — Lock and record
- **What:** once all cells balance (via harness, and dilemma rebalance only where
  forced), run the canonical 0b at N=500 (spec §2.1.4) into
  `phase0b_harness_neutral/`, then 0c locked-holdout at N=1000 (spec §2.2).
- **Output:** the validated harness-neutral baseline Phase 2 is allowed to build
  on. This is the real "Phase 0b PASS."

---

## Stopping / escalation rules

- If Step C balances everything → done, skip D. Best case, zero dilemma edits.
- If a problem needs > ~15 rebalance iterations in Step D without reaching 45–55 →
  flag it for the descope path (spec Appendix A: MVT keeps the problems that
  calibrate, defers the rest) rather than forcing it.
- Supervisor is engaged only after Phases 0 and 1 are complete (owner directive),
  so within this plan we do NOT pause for supervisor input; we document
  thoroughly for that later conversation.

## What this plan explicitly will NOT do

- Will not edit any dilemma before Steps A–C prove the harness lever insufficient
  for that specific problem.
- Will not write to any canonical results directory until Step E.
- Will not change the parameter set, R matrix, Beta marginals, or configuration
  definitions (out of 0b scope; human-approval items).

## Cost envelope

Steps A + C ≈ $3.00. Step D depends on how many problems drift-broke and how many
iterations each needs (bounded, cheap per iteration). Whole remediation likely
well under $10 — versus a contaminated Phase 2 at $3,500+.
