# C1 — Raw Evals

One file per multi-agent run. Naming: `C1_run_{run_index:02d}.json` (e.g. `C1_run_01.json` ... `C1_run_20.json`).

Each file contains the full transcript: 5 agents × up to 5 deliberation rounds, plus the final `final_allocation` over R&D / bonuses / CSR / reserve, `consensus_reached`, and `rounds_to_consensus`.

Schema and write rules: see `../README.md`. Prompt template: `../../../questions/C1_resource_council.md`.
