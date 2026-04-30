"""
05_simulate.py — Mesa ABM: agent interaction loop across societal configurations.

Phase: 4 (Simulation)
Input:  data/processed/agents_{config_code}_{seed}.parquet
        data/processed/concept_priors.nc (from 03_encode.py)
Output: data/processed/results_{config_code}_{run_id}.parquet — per-step metrics
        output/logs/sim_{config_code}_{run_id}.log

Done when:
  - Interaction loop runs for all 8 configurations
  - Per-step metrics collected (obedience rate or relevant metric, config code, seed, N, run index)
  - At least 20 runs per configuration completed
  - Results written with full provenance (config, N, runs, seed, timestamp)

CRITICAL: parameter-to-behaviour mapping rules (how a PLB score of 0.8 affects
agent decisions) must be panel-reviewed before this script is written.
See CLAUDE.md trigger conditions for five-agent panel.
See modus operandi §4.2 for the proposed mapping logic.

Performance metric (welfare_score) is NOT yet defined — see Open Problem L1 in meta.md.
Do not implement a proxy metric without explicit human sign-off.
"""

# TODO (Phase 4): implement Mesa model.
# State config code, N agents, N runs, and seed BEFORE execution (CLAUDE.md Rule 4).

raise NotImplementedError("05_simulate.py is not yet implemented.")
