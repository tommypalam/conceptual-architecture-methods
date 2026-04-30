# C2 — Raw Evals

One file per multi-agent run. Naming: `C2_run_{run_index:02d}.json` (e.g. `C2_run_01.json` ... `C2_run_20.json`).

Each file contains the full transcript: 1 deterministic CEO script + 5 committee-member agents across iterative rounds, plus per-round `approval_per_round` (list) and `final_decision` ∈ {`approve`, `amend`, `reject`}.

C2 is the Milgram analogue. The Phase 2+ retrodiction target is 61–66% approval in the `00100` configuration — but Phase 0 is unconditioned baseline only.

Schema and write rules: see `../README.md`. Prompt template: `../../../questions/C2_restructuring_board.md`.
