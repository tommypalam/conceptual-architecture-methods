# Phase 0 â€” Baseline Calibration Experiment

## Purpose

Each experimental problem must produce an approximately 50/50 binary response distribution under RLHF baseline â€” before any parameter profile is injected. This folder stores the calibration runs against gpt-5.4-mini to verify that baseline.

If the base LLM has a default answer driven by alignment training, the encoded architecture's effect on the decision cannot be isolated. A problem that consistently produces 70% answer-A under baseline is not usable â€” it measures RLHF training signal, not the normative architecture.

**Calibration target:** 45/55 to 55/45 split. Problems outside 40/60 to 60/40 are rewritten or replaced before Phase 2.

---

## Experimental Problems Under Calibration

### Simple Problems (LPM route â€” binary decision, N=200)

| ID | Name | Concepts activated | Notes |
|----|------|--------------------|-------|
| S1 | The Promotion Decision | Justice-loyalty tension | TfA, RE, MS, PD |
| S2 | The Quiet Error | Authority-loyalty-care tension | ID, LL, TfA, RT, MS |
| S3 | The Strategic Pivot | Care-justice tension under strategic uncertainty | MoR, RE, MS, PD, RT |

### Complex Problems (Agents-of-Chaos route â€” multi-agent, N=4â€“6 per run, 20 runs)

| ID | Name | Concepts activated | Notes |
|----|------|--------------------|-------|
| C1 | The Resource Council | All five concepts | Group decision, 5 agents, â‚¬500k allocation |
| C2 | The Restructuring Board | Authority-justice tension (Milgram analogue) | 6 agents, CEO + committee |
| C3 | The Scientific-Approach Dilemma | Epistemic dimension | 4 founder-agents, 6 rounds |

---

## Folder Structure

```
phase0_baseline_calibration/
â”œâ”€â”€ README.md                    # This file
â”œâ”€â”€ questions/
â”‚   â”œâ”€â”€ S1_promotion_decision.md
â”‚   â”œâ”€â”€ S2_quiet_error.md
â”‚   â”œâ”€â”€ S3_strategic_pivot.md
â”‚   â”œâ”€â”€ C1_resource_council.md
â”‚   â”œâ”€â”€ C2_restructuring_board.md
â”‚   â””â”€â”€ C3_scientific_approach_dilemma.md
â””â”€â”€ results/
    â”œâ”€â”€ raw/
    â”‚   â””â”€â”€ evals/               # One file per call/run â€” anti-anchoring isolation
    â”‚       â”œâ”€â”€ README.md        # Schema, naming, write rules
    â”‚       â”œâ”€â”€ S1_promotion_decision/    # N=200 files: S1_001.json ... S1_200.json
    â”‚       â”œâ”€â”€ S2_quiet_error/           # N=200 files: S2_001.json ... S2_200.json
    â”‚       â”œâ”€â”€ S3_strategic_pivot/       # N=200 files: S3_001.json ... S3_200.json
    â”‚       â”œâ”€â”€ C1_resource_council/      # N=20 files: C1_run_01.json ... C1_run_20.json
    â”‚       â”œâ”€â”€ C2_restructuring_board/   # N=20 files
    â”‚       â””â”€â”€ C3_scientific_approach/   # N=20 files
    â””â”€â”€ processed/               # Aggregated response rates, calibration verdict per problem
```

**Why one file per call.** gpt-5.4-mini writes responses directly. If multiple answers shared a single file, the model could read prior responses and anchor on them â€” the resulting baseline would measure RLHF-plus-anchoring rather than RLHF alone. Per-call isolation is the only way to keep the 50/50 calibration target interpretable. The disk cost is trivial (~660 small JSON files total). See `results/raw/evals/README.md` for the full schema and write rules.

---

## Protocol

1. Present each problem to gpt-5.4-mini with **no system prompt** (bare user message only).
2. Run N=200 independent calls per simple problem; N=20 runs per complex problem.
3. **Each call writes its own file** in `results/raw/evals/{problem_id}/{problem_id}_{NNN}.json`. Files are write-once, never appended. See `results/raw/evals/README.md` for the schema.
4. Parse binary choice (A/B or equivalent) from each response file.
5. Compute response distribution and 95% CI across all files for a given problem.
6. Log aggregate result in `results/processed/calibration_summary.csv`.
7. Flag any problem outside 40/60â€“60/40 for rewrite.

**Model:** `gpt-5.4-mini` (OpenAI API)
**Temperature:** 1.0 (maximum diversity, no determinism)
**Seed:** None (each call independent)
**System prompt:** None for baseline. System prompt is added only in Phases 1â€“3.

---

## Calibration Summary

Run date: 2026-04-30 (rebalanced prompts, post-panel revision). Wilson 95% CIs.

| Problem | N | Choice A% | Choice B% | 95% CI on A | In band? | Action |
|---------|---|-----------|-----------|-------------|----------|--------|
| S1 | 200 | A: 53.0% | B: 47.0% | [46.1%, 59.8%] | PASS (45/55–55/45) | retain |
| S2 | 200 | REPORT: 51.0% | QUIET: 49.0% | [44.1%, 57.8%] | PASS (45/55–55/45) | retain |
| S3 (startup-pivot family, retired) | 200 | PIVOT: 61.0% | PERSIST: 39.0% | [54.1%, 67.5%] | FAIL → retired | see archive |
| S3 (Dept Reorganisation v7, ADOPT/WAIT) | 200 | ADOPT: 50.0% | WAIT: 50.0% | [43.1%, 56.9%] | PASS (45/55–55/45) | retain — locked |
| C1 | — | — | — | — | PENDING | — |
| C2 | — | — | — | — | PENDING | — |
| C3 | — | — | — | — | PENDING | — |

S1 and S2: locked. Both straddle 50% in their CI and sit inside the well-calibrated 45/55–55/45 band. Raw evals at `results/raw/evals/{S1,S2}_*/`.

S3: startup-pivot scenario family retired after ~20 documented retunes failed to produce a balanced split. Replaced with **The Department Reorganisation** (ADOPT/WAIT), calibrated to exactly 100/100 at N=200 on v7 (2026-05-01). Locked. Raw evals at `results/raw/evals/S3_strategic_pivot/` (S3_001–S3_200, all ADOPT/WAIT). Full retune history in `questions/archive/README.md`.

---

## Note on S3 (The Strategic Pivot)

The startup-pivot scenario family is retired; the current S3 lives in a different scenario family (Department Reorganisation, ADOPT/WAIT labels). The original calibration warning that gpt-5.4-mini baselines toward PIVOT is preserved for context — it is precisely the failure mode that motivated the scenario-level rewrite. A new failure mode in the new scenario family would warrant a fresh rewrite, not a return to startup-pivot framing.
