# Phase 0b Investigation — Diagnosis Summary

**Date:** 2026-07-28
**Model today:** `gpt-5.4-mini-2026-03-17` (snapshot the `gpt-5.4-mini` alias currently resolves to)
**Phase 0a model:** `gpt-5.4-mini` (bare alias recorded; no dated snapshot captured, Apr 30–May 2 2026)

## Question

Phase 0b (grid100, same date) showed the full harness collapses the six dilemmas
away from their Phase-0a-validated ~50/50 splits (16/18 cells failed). Owner
constraint: fix WITHOUT rewriting the dilemma prompts. So: what causes the
collapse — and is any of it model drift rather than the harness?

## Method: elimination by ablation (all under empty harness / null_a)

Each round held the frozen dilemmas fixed and changed one harness variable.
Runs archived beside this file.

| Round | Test | Result |
|-------|------|--------|
| grid100 | full 18-cell grid, N=100 | 16/18 collapse; 4/6 problems lean same way even under sham params |
| ablation_singleclause | toggle preamble / decision-rule / do-not-refuse / output-order individually, N=30 | **clean negative** — every variant ~0.40 mean; no single clause is the cause |
| ablation_reasoning | DECISION+REASONING vs DECISION-only, N=30 | **clean negative** — decision_only (0.367) ≈ canonical (0.361); forced reasoning is not the cause |
| ablation_systemrole | canonical vs naked_repro (NO system message, pure 0a structure), N=30 | **partial** — mean 0.350 → 0.244; recovered C2, S3, improved S1; C1/C3/S2 still collapse |

## The decisive comparison (naked_repro reproduces 0a's exact structure)

Because `naked_repro` sends no system message and the dilemma as a user-only
turn — byte-identical structure to Phase 0a — any problem whose split differs
from 0a can only be the model changing.

| Problem | 0a (May 2026) | naked_repro (today) | drift? |
|---------|---------------|---------------------|--------|
| S1 | A 53% | B 60% | mild flip |
| S2 | FORMAL_REPORT 51% | LOCAL_CORRECTION 100% | **hard drift** |
| S3 | ADOPT 50% | ADOPT 53% | stable |
| C1 | PACKAGE_A 51.5% | PACKAGE_B 100% | **hard drift** |
| C2 | APPROVE 50% | REJECT 53% | stable |
| C3 | CONTINUE 51% | PIVOT 80% | **major drift** |

## Conclusion (two causes, drift dominant)

1. **System-role presence** is a real but secondary contributor: removing the
   system message recovered 3/6 problems and improved S1.
2. **Model drift is the dominant cause.** Under a faithful Phase-0a reproduction,
   4 of 6 dilemmas no longer sit at 50/50 (S2 and C1 fully inverted to 100%).
   The identical prompt that gave 51% FORMAL_REPORT in May gives 100%
   LOCAL_CORRECTION today. The harness is absent in this test, so this is the
   model, not the framework.

## Ruled out (with data)

- ❌ parameter block content (null_c gibberish behaved like real params)
- ❌ any single framing clause (preamble / decision-rule / refusal / output order)
- ❌ the forced REASONING output

## Spec mapping & implications

- Spec §11.5 anticipated exactly this: Phase 0a is *calibration*, not validation;
  the model can move. §2.2.2 gives the contingency — modest shift → report vs the
  re-measured baseline; substantial shift → retire & rebalance that prompt.
- S3 and C2 still calibrate on the current model → keep.
- S1 drifted mildly (near the 40/60 edge). S2, C1, C3 drifted hard → need
  rebalancing on the current model, OR the framework adopts a no-system-message
  delivery (which itself recovered several problems) — a design decision.
- **Phase 0a's method, infrastructure, and dilemma-engineering all stand.** Only
  the specific calibration NUMBERS are stale, because the model underneath moved.

## Required next action regardless of path

Pin the model snapshot. Today's calls resolve to `gpt-5.4-mini-2026-03-17`;
Phase 0a captured only the alias. Any recalibration must pin to a dated snapshot
id and record `model_version` per call (the engine already records it) so the
baseline cannot silently drift again mid-project. This is a supervisor-level
decision point per spec §2.3 / §11.

## Cost of the whole investigation

grid100 (1,800) + 3 ablation rounds (900 + 360 + 360) = 3,420 calls ≈ $3.42.
This established, before any Phase 2 spend (~$3,500+), that the current model is
mis-calibrated against the May baseline — the exact contamination Phase 0b exists
to catch.
