# C3 — Raw Evals

One file per multi-agent run. Naming: `C3_run_{run_index:02d}.json` (e.g. `C3_run_01.json` ... `C3_run_20.json`).

Each file contains the full transcript: 4 founder-agents across 6 deliberation rounds with asymmetric private evidence, plus `final_vote` ∈ {`continue`, `pivot`}, `information_sharing_rate`, and per-agent updating trace.

**Critical:** The orchestrator must enforce private-evidence boundaries — Agent N's private evidence must never appear verbatim in Agent M's user prompt unless Agent N voluntarily shared it in a prior round. Audit transcripts for leaks before treating runs as valid.

Schema and write rules: see `../README.md`. Prompt template and per-agent evidence distribution: `../../../questions/C3_scientific_approach_dilemma.md`.
