# Research Operating System Template

> **Purpose:** A reusable, operationalized workflow for AI-assisted empirical research projects.
> Drop this into every new project folder. Fill in the blanks. Delete nothing until you understand why it's there.
>
> **Core philosophy:** The AI generates faster than you can verify. Your bottleneck is attention, not production. Every piece of structure here exists to make verification possible.

---

## Table of Contents

1. [Project Brief](#1-project-brief)
2. [L1 Diagnosis: Novelty Assessment](#2-l1-diagnosis-novelty-assessment)
3. [README Skeleton](#3-readme-skeleton)
4. [CLAUDE.md — Project Constitution](#4-claudemd--project-constitution)
5. [Variable Map (variables.json)](#5-variable-map-variablesjson)
6. [Folder Structure](#6-folder-structure)
7. [Done Criteria](#7-done-criteria)
8. [Execution Workflow](#8-execution-workflow)
9. [Verification Checklist](#9-verification-checklist)
10. [Econometric Guardrails](#10-econometric-guardrails)
11. [Session Management](#11-session-management)
12. [Git Protocol](#12-git-protocol)
13. [Tool Delegation Matrix](#13-tool-delegation-matrix)
14. [Parallelisation Protocol](#14-parallelisation-protocol)
15. [Replication Packaging](#15-replication-packaging)
16. [Quick-Reference Master Loop](#16-quick-reference-master-loop)

---

## 1. Project Brief

*Write this yourself. Not the AI. One page maximum.*

| Field | Your Entry |
|---|---|
| **Research question** | `[State the question in one sentence]` |
| **Unit of observation** | `[e.g., firm-year, individual-month, country-quarter]` |
| **Key datasets** | `[List names, sources, approximate size]` |
| **Core empirical strategy** | `[e.g., panel FE, DiD, IV, RDD, matching]` |
| **Main output artifacts** | `[e.g., 3 tables, 2 figures, cleaned panel]` |
| **What would make this project fail?** | `[Be honest. Weak instrument? Missing data? Ambiguous treatment?]` |

---

## 2. L1 Diagnosis: Novelty Assessment

Before touching any tool, classify every component of the project.

| Component | AI Has Seen This Before? | Implication |
|---|---|---|
| Data format (CSV, Stata, SQL) | Yes / No | If no → manual inspection first |
| Cleaning operations (dedup, reshape, impute) | Yes / No | If standard → delegate; if domain-specific → piecewise |
| Merge logic | Yes / No | If complex keys or fuzzy matching → step-by-step only |
| Econometric method | Yes / No | If standard OLS/FE → delegate with guardrails; if niche → theory-first |
| Variable construction | Yes / No | If domain-specific → require codebook before any code |
| Output format (LaTeX tables, figures) | Yes / No | If standard → delegate; if custom → template first |

**Rule:** If any critical component scores "No," that component gets piecewise execution with manual verification at every step. No exceptions, no matter how eager you are.

---

## 3. README Skeleton

*This is for the confused human who just fell into the repository. No poetry. Just answers.*

```markdown
# [Project Title]

## What This Project Does
[One-paragraph description of the research question and approach.]

## Data
- **Raw data:** `data/raw/` — NEVER modified by any script.
- **Processed data:** `data/processed/` — generated reproducibly by pipeline scripts.
- **Data sources:** [List origins, access dates, any restrictions.]

## How to Run the Full Pipeline
```bash
# [Single command or entry-point script that reproduces everything]
```

## Folder Structure
```
├── data/
│   ├── raw/           # Untouched source files
│   └── processed/     # Script-generated outputs
├── code/
│   ├── 01_intake.py
│   ├── 02_clean.py
│   ├── 03_merge.py
│   ├── 04_construct.py
│   ├── 05_estimate.py
│   └── 06_output.py
├── output/
│   ├── tables/
│   ├── figures/
│   └── logs/
├── notebooks/         # Exploratory only — not authoritative
├── docs/
│   ├── CLAUDE.md
│   ├── variables.json
│   └── pre_analysis_plan.md
├── tests/
└── README.md
```

## Outputs
When the pipeline succeeds, you should find:
- [List expected tables, figures, logs with filenames]

## Requirements
- [Python version, R version, packages, etc.]

## Contact
- [Name, email, role]
```

---

## 4. CLAUDE.md — Project Constitution

*This is not a prompt zoo. It is the operating charter the AI reads every session. Keep it under 40 lines. Every line should constrain behavior.*

```markdown
# CLAUDE.md — Project Constitution

## Purpose
[One sentence. What this project does and why.]

## Unit of Analysis
[e.g., firm-year panel, 2005–2020]

## Canonical Datasets
| Name | Description | Format | Rows (approx.) |
|---|---|---|---|
| `[dataset_1]` | [what it contains] | [CSV/Stata/etc.] | [n] |
| `[dataset_2]` | [what it contains] | [CSV/Stata/etc.] | [n] |

## Merge Keys
- `[dataset_1]` ↔ `[dataset_2]`: merge on `[key_variable(s)]`
- Expected match rate: ~[X]%

## Naming Conventions
- Variables: `snake_case`
- Files: `[NN]_[verb]_[noun].[ext]` (e.g., `02_clean_firms.py`)
- Outputs: `[table/fig]_[number]_[description].[ext]`

## Non-Negotiable Rules
1. Never modify files in `data/raw/`.
2. Never rename columns without explicit approval.
3. After every transformation, print: row count, column names, missing value summary.
4. For regressions: state fixed effects, clustering, and sample restrictions BEFORE estimation.
5. If uncertain about any specification choice, STOP and ASK.
6. Never silently drop observations. Log every filter with before/after counts.
7. Every merge must report: matched count, unmatched from left, unmatched from right.

## Econometric Defaults
- Standard errors: `[clustered at X / robust / bootstrap]`
- Fixed effects: `[entity + time / entity only / etc.]`
- Sample restrictions: `[describe any default exclusions]`
- Winsorization: `[rule, if any, e.g., 1st/99th percentile]`

## Things Requiring Human Approval
- Adding or removing control variables
- Changing the sample definition
- Altering the identification strategy
- Any transformation not in the pre-analysis plan
```

---

## 5. Variable Map (variables.json)

*Brutally boring. That is a compliment.*

```json
{
  "variables": [
    {
      "name": "firm_id",
      "label": "Unique firm identifier",
      "source_dataset": "compustat_annual",
      "type": "identifier",
      "role": "id",
      "data_type": "string",
      "unit": null,
      "allowed_values": "Non-null, unique within year",
      "missing_meaning": "Should never be missing — drop if so",
      "transformation": "None (raw key)",
      "notes": "Use GVKEY, not ticker"
    },
    {
      "name": "revenue",
      "label": "Total annual revenue",
      "source_dataset": "compustat_annual",
      "type": "continuous",
      "role": "outcome",
      "data_type": "float",
      "unit": "millions USD",
      "allowed_values": ">= 0 (negative values = data error)",
      "missing_meaning": "Not reported — may indicate delisting or private status",
      "transformation": "Log-transform for regressions (ln_revenue)",
      "notes": "Winsorize at 1st/99th before log"
    }
  ]
}
```

**Required fields for every variable:**

| Field | Description |
|---|---|
| `name` | Exact column name in code |
| `label` | Human-readable description |
| `source_dataset` | Which raw file it comes from |
| `type` | `identifier` / `continuous` / `categorical` / `binary` / `date` |
| `role` | `id` / `outcome` / `treatment` / `control` / `instrument` / `weight` / `derived` |
| `data_type` | `string` / `int` / `float` / `date` / `boolean` |
| `unit` | Measurement unit or `null` |
| `allowed_values` | Valid range or set of values |
| `missing_meaning` | Is missingness informative, random, or an error? |
| `transformation` | What gets done to it (log, winsorize, standardize, etc.) |
| `notes` | Anything that will save someone 30 minutes of confusion |

---

## 6. Folder Structure

```
project-root/
│
├── data/
│   ├── raw/               # IMMUTABLE. Never touched by scripts.
│   └── processed/         # Reproducibly generated. Can be deleted and rebuilt.
│
├── code/
│   ├── 01_intake.py       # Load and validate raw data
│   ├── 02_clean.py        # Clean, standardize, handle missing values
│   ├── 03_merge.py        # Join datasets, verify merge quality
│   ├── 04_construct.py    # Build analysis variables
│   ├── 05_estimate.py     # Run models
│   ├── 06_output.py       # Generate tables and figures
│   ├── utils.py           # Shared helper functions
│   └── run_all.py         # Master entry point — runs full pipeline
│
├── output/
│   ├── tables/            # Regression tables, summary stats
│   ├── figures/           # Plots, diagrams
│   └── logs/              # Diagnostic logs from pipeline runs
│
├── notebooks/             # EXPLORATORY ONLY. Not the source of truth.
│
├── docs/
│   ├── CLAUDE.md          # Project constitution (AI reads this every session)
│   ├── variables.json     # Variable codebook
│   ├── pre_analysis_plan.md  # Hypotheses, specifications, planned tests
│   └── handoff/           # Session handoff documents
│
├── tests/                 # Verification scripts and test cases
│
├── .gitignore
└── README.md
```

**Rules:**
- `data/raw/` is sacred. Nothing writes to it.
- `notebooks/` is a scratchpad. If something matters, it goes into `code/`.
- `output/` is ephemeral. The pipeline should regenerate it from scratch.
- `docs/handoff/` stores session-ending handoff notes (see Section 11).

---

## 7. Done Criteria

### 7a. Project-Level Done

Write these before execution begins. Every criterion must be checkable, not vibes-based.

- [ ] Raw data files remain byte-identical to originals
- [ ] Every processed dataset is reproducible from `run_all.py`
- [ ] All variable definitions match `variables.json`
- [ ] All merges report matched/unmatched counts in logs
- [ ] Baseline regressions use the specification from the pre-analysis plan
- [ ] Every table and figure regenerates from a single pipeline run
- [ ] All major transformations have row-count checks in logs
- [ ] A fresh AI session can audit the project and understand what was done
- [ ] README accurately describes the current state of the project

### 7b. Phase-Level Done

| Phase | Done When... |
|---|---|
| **Data intake** | Raw files loaded; row counts, column types, and key distributions printed and match expectations |
| **Cleaning** | Missing values handled per codebook rules; no unexpected nulls in IDs; value ranges validated |
| **Merge** | All joins report matched/unmatched counts; unique IDs verified post-merge; no unintended duplication |
| **Variable construction** | New variables match codebook definitions; spot-check 10+ rows manually; summary stats are plausible |
| **Estimation** | Specification matches pre-analysis plan; standard errors are correct; sample size matches expectations |
| **Robustness** | All planned robustness checks executed; results logged; deviations from baseline flagged |
| **Output packaging** | Tables and figures generated; labels are readable; pipeline runs end-to-end without manual intervention |

---

## 8. Execution Workflow

The loop is always the same. No exceptions, no shortcuts.

```
┌─────────────────────────────────────────────────────┐
│                                                     │
│   ORIENT → PLAN → EXECUTE → VERIFY → DOCUMENT      │
│      ↑                                    │         │
│      └────────────────────────────────────┘         │
│                    (repeat)                          │
│                                                     │
│   After each cycle: COMMIT                          │
│   When switching tasks or auditing: NEW CHAT         │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### Step-by-step

**ORIENT** — Before any code:
1. Read README, CLAUDE.md, and variable map.
2. Inspect data: unit of observation, time structure, IDs, merge keys, known oddities.
3. Identify the specific final output this session needs to produce.

**PLAN** — Before any execution:
1. Ask the AI for a step-by-step plan. Say explicitly: *"Do not write code yet."*
2. Require the plan to name: files to be created, edge cases, variables needing attention, verification steps after each phase.
3. Reject any plan without a verification section. That is not a plan; it is a wish list.

**EXECUTE** — One small step at a time:
1. Approve exactly one step.
2. Keep changes small and reviewable.
3. Interrupt immediately if the AI starts freelancing, renaming things, or solving a different problem.
4. No long autonomous loops. That is how you get polished nonsense.

**VERIFY** — Immediately after each step:
1. Run the verification checklist (Section 9).
2. Compare outputs against domain expectations, not just syntax.
3. If something looks wrong, do not let the AI "fix" it in the same breath. Diagnose first.

**DOCUMENT** — Before moving on:
1. Update CLAUDE.md if you discovered anything new (edge cases, rules, gotchas).
2. Note what was done, what remains, and what future sessions must not forget.
3. Keep notes short and operational.

**COMMIT** — After each clean milestone:
1. Stage and commit with a descriptive message.
2. Never commit mid-chaos.

---

## 9. Verification Checklist

### After Loading Data
- [ ] Print column names, types, shape
- [ ] Print missing values per column
- [ ] Print summary statistics for key variables
- [ ] Verify row count matches expected source size
- [ ] Check ID uniqueness (or uniqueness within expected group)

### After Filtering / Subsetting
- [ ] Print row count before and after
- [ ] Log the filter condition applied
- [ ] Verify no unintended loss of critical observations

### After Merging / Joining
- [ ] Print matched count, unmatched from left, unmatched from right
- [ ] Check for unintended row duplication (compare row count to expected)
- [ ] Verify unique ID counts post-merge
- [ ] Inspect a sample of unmatched rows — are they expected?

### After Aggregation
- [ ] Verify the new unit of observation explicitly
- [ ] Print row count and compare to expected number of groups
- [ ] Check that aggregation function is correct (mean vs. sum vs. first)

### After Variable Construction
- [ ] Print summary stats for new variables
- [ ] Hand-check 5–10 rows against raw data
- [ ] Verify value ranges match `variables.json` expectations
- [ ] Check for introduced NaN/Inf values

### After Model Estimation
- [ ] Confirm sample size matches expectations
- [ ] Verify fixed effects and clustering match the pre-analysis plan
- [ ] Check coefficient signs and magnitudes against theory
- [ ] Inspect residuals if relevant
- [ ] Confirm no leakage in predictive setups (train/test split integrity)

### Diagnostic Visualizations (generate as needed)
- [ ] Histograms of key variables
- [ ] Missingness heatmap
- [ ] Counts by group / time period
- [ ] Scatter plots for key relationships
- [ ] Residual plots post-estimation

---

## 10. Econometric Guardrails

These are the failure patterns that produce plausible, tidy, and wrong results.

| Guardrail | Rule |
|---|---|
| **Standard errors** | State the clustering/robustness choice BEFORE running the model. The AI will default to something — make sure it defaults to the right thing. |
| **Train/test leakage** | Lock down split logic before any model touches data. Verify no information from the test set leaks into training. |
| **Silent column renaming** | Forbid it. Require printing column names after every transformation. |
| **Aggregation level** | Verify the unit of observation after every reshape, collapse, or merge. The AI may silently change it. |
| **Fixed effects** | Confirm that entity and time FE match the research design, not just "what looks sophisticated." |
| **Model specification** | Check that the estimated model answers the original research question — not some nearby easier question the AI drifted toward. |
| **Sample composition** | Verify who is in the sample and who got dropped. Silent observation loss changes your estimand. |
| **Treatment definition** | If this is causal work, verify the treatment variable is coded exactly as intended. Off-by-one errors in treatment timing are common and devastating. |

---

## 11. Session Management

### Starting a Session
1. Instruct the AI to read README, CLAUDE.md, and the variable map.
2. State the specific task for this session.
3. If continuing prior work, provide the most recent handoff document.

### Ending a Session
Before closing any chat, generate a handoff document:

```markdown
# Session Handoff — [Date]

## What Was Accomplished
- [List completed steps]

## What Remains
- [List next steps]

## Key Decisions Made
- [Any specification, coding, or design choices]

## Bugs / Issues Encountered
- [What went wrong and how it was resolved, or not]

## Current File State
- [Which files were created or modified]
- [Current state of the pipeline]

## Warnings for Next Session
- [Anything the next session must know or avoid]
```

Save to `docs/handoff/handoff_YYYY-MM-DD_[topic].md`.

### When to Start a New Chat
- Switching to a different task or phase
- Verifying work done in a previous session (fresh context = independent check)
- Context is getting long and bloated
- You want an unbiased assessment, not anchored agreement

### When to Continue the Same Chat
- Directly continuing the previous step
- Prior context is genuinely useful for the next step
- You are in the middle of a multi-step debugging cycle

---

## 12. Git Protocol

| Principle | Practice |
|---|---|
| **Commit after clean milestones** | Not after chaos. Each commit should represent a verifiable state. |
| **Descriptive messages** | `"Add firm-level cleaning with winsorization (02_clean.py)"` — not `"updates"` |
| **Branch for risky changes** | If the change might break the pipeline, branch first. |
| **Use history for debugging** | `git log`, `git diff`, and `git bisect` are diagnostic tools, not decorations. |
| **Never commit raw data** | Add `data/raw/` to `.gitignore` if raw files are large or sensitive. Document provenance in README instead. |
| **Tag major milestones** | `v0.1-cleaning-complete`, `v0.2-baseline-estimated`, etc. |

---

## 13. Tool Delegation Matrix

### Claude Code (Terminal / Repo Work)

Use Claude Code when the task requires touching real files, running real commands, or interacting with the actual project environment.

| Task | Example |
|---|---|
| Repository inspection | "Read the folder structure and summarize what exists." |
| Data auditing | "Load the raw CSV, print shape, types, missing values." |
| Code writing | "Write the cleaning script following the plan." |
| Script execution | "Run `02_clean.py` and show me the output." |
| Debugging | "Here's the traceback. Diagnose and patch." |
| File manipulation | "Rename outputs to match the naming convention." |
| Table/figure generation | "Generate Table 1 with the baseline specification." |
| Pipeline testing | "Run the full pipeline from `run_all.py` and report." |
| CLAUDE.md / variable map updates | "Add this new merge key rule to CLAUDE.md." |

**Starter prompt for Claude Code:**
> Read README, CLAUDE.md, and the variable map. Orient to the project: summarize the data structure, unit of analysis, and likely risk points. Do not write code yet. Produce a stepwise plan with explicit verification after each step. During execution, never modify raw data, never rename columns without approval, and after each transformation print row counts, column names, duplicate checks, and relevant diagnostics. If uncertainty appears, stop and ask.

---

### Classical Claude / ChatGPT (Chat-First / Thinking Work)

Use chat models when the task is primarily language, judgment, conceptual reasoning, or review — nothing needs to be executed.

| Task | Example |
|---|---|
| Research design stress-testing | "Identify hidden assumptions in this identification strategy." |
| Methods section drafting | "Rewrite this methods section for clarity." |
| Literature positioning | "Summarize how these three papers differ on X." |
| Argument pressure-testing | "What would a skeptical reviewer say about this?" |
| Pre-analysis plan drafting | "Help me formalize the hypotheses and planned specifications." |
| Prompt generation | "Write me a good starter prompt for the cleaning phase." |
| Acceptance criteria generation | "Draft project-level done criteria for this design." |
| Econometric explanation | "Explain when clustering at firm vs. industry level matters." |
| Independent output review | "Here is the regression table. Do the signs and magnitudes make sense?" |
| Constitution drafting | "Help me write a concise CLAUDE.md for this project." |

**Starter prompt for classical chat models:**
> Help me stress-test this research design before implementation. Here is the question, theory, unit of analysis, variable map, and proposed pipeline. Identify hidden assumptions, likely econometric failure points, vague definitions, and missing acceptance criteria. Do not flatter the plan. Be adversarial and concrete.

---

### Delegation Flow

```
UPSTREAM (Thinking)          DOWNSTREAM (Implementation)         REVIEW (Verification)
─────────────────            ───────────────────────────         ─────────────────────
Classical Claude /           Claude Code                         Fresh classical chat
ChatGPT                                                         or new Claude session

• Sharpen the question       • Inspect the repo                  • Audit outputs
• Refine hypotheses          • Write and run code                • Check specification
• Draft project brief        • Debug tracebacks                  • Review pipeline logic
• Stress-test assumptions    • Execute pipeline steps            • Independent replication
• Generate done criteria     • Generate tables/figures           • Adversarial review
• Draft constitution         • Update files in repo              • Verify reproducibility
```

---

## 14. Parallelisation Protocol

### When to Parallelise
- Tasks are genuinely independent (no shared mutable state)
- Acceptance criteria are explicit for each task
- Your review capacity can handle the extra output

### When NOT to Parallelise
- Upstream theory/specification is still ambiguous
- Variable definitions are unstable
- Merge keys are disputed
- You cannot review each output independently

If you cannot verify them separately, parallelisation is fake productivity.

---

### The Seven Rules

**Rule 1 — Split by independent task, not by shared confusion.**
Good splits: literature extraction ∥ data dictionary ∥ code audit ∥ robustness plan.
Bad splits: five AIs editing the same ambiguous pipeline.

**Rule 2 — Every AI gets the same constitution, different assignment.**
All agents receive: project brief, CLAUDE.md, variable map, done criteria, prohibitions.
Each gets a distinct role: cleaning planner, merge auditor, specification reviewer, test writer, adversarial reviewer.

**Rule 3 — Use independent verification chats.**
Same chat = continuation. New chat = audit.
A fresh chat gives you an independent check, not anchored agreement.

**Rule 4 — Use multi-agent A/B testing when correctness is uncertain.**
Spawn 3–5 agents. Same task, independently. Compare outputs.
Majority agreement = higher confidence (not truth). Disagreement = where to inspect.

**Rule 5 — One synthesizer, not five cooks.**
One AI (or you) compares outputs against acceptance criteria.
Require agents to report discrepancies, not essays. Disagreement is more informative than consensus.

**Rule 6 — Maintain handoff documents.**
Before ending any session: what was done, what remains, decisions, bugs, file state.
A fresh start with a strong handoff beats compressed confusion.

**Rule 7 — Never parallelise upstream ambiguity.**
If the theory is unclear, the variables are unstable, or the merge keys are disputed: stop.
Buy the wheat before you bake the pizza.

---

### Parallel Role Assignments (Template)

| Agent | Role | Constitution | Assignment |
|---|---|---|---|
| Agent A | Cleaning planner | Shared CLAUDE.md + variable map | Draft cleaning plan with verification steps |
| Agent B | Merge auditor | Shared CLAUDE.md + variable map | Audit merge logic, report match rates |
| Agent C | Specification reviewer | Shared CLAUDE.md + pre-analysis plan | Check econometric specification against theory |
| Agent D | Test writer | Shared CLAUDE.md + done criteria | Write verification tests for each phase |
| Agent E | Adversarial reviewer | Shared CLAUDE.md + full pipeline | Find weaknesses, inconsistencies, silent failures |
| Synthesizer | You (or a fresh chat) | All outputs from A–E | Compare outputs, flag discrepancies, decide |

---

## 15. Replication Packaging

Before declaring the project complete:

- [ ] `run_all.py` (or equivalent) rebuilds the full analysis from raw data to final outputs
- [ ] README documents: data provenance, required files, variable definitions, how to run
- [ ] A newcomer can determine what the project does within 10 minutes
- [ ] A newcomer can determine when each part is "done"
- [ ] All dependencies are documented (packages, versions, system requirements)
- [ ] Raw data access is documented (where to get it, any restrictions)
- [ ] No hardcoded local paths in scripts
- [ ] Output files match what the README promises

If a newcomer cannot tell what counts as complete, your protocol is still too tacit.

---

## 16. Quick-Reference Master Loop

The shortest reusable version of everything above. Tape this to your wall.

```
1.  Orient the project (read everything, inspect data)
2.  Write project-level and step-level done criteria
3.  Build the repo structure
4.  Create README, CLAUDE.md, and variable map
5.  Feed the AI: database, theory, variables
6.  Ask for a plan with verification — no code yet
7.  Execute ONE small step only
8.  Verify: row counts, plots, sample checks
9.  Document what you learned
10. Commit
11. New chat for independent verification when needed
12. Parallelise only independent tasks with shared criteria + synthesis
13. Repeat until pipeline reproduces cleanly
14. Package for replication
```

**If you remember nothing else:** Orient. Plan. Execute small. Verify immediately. Document. Commit. Fresh chat when in doubt.

---

*Template version: 1.0 | Adapt per project. Do not cargo-cult.*
