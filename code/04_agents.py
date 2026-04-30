"""
04_agents.py — Sample agent population from the joint Gaussian copula distribution.

Phase: 4 (Simulation)
Input:  data/processed/fitted_marginals.json, code/utils.py (R matrix)
Output: data/processed/agents_{config_code}_{seed}.parquet — one file per config per run

Done when:
  - N agents sampled per societal configuration (target: 500 per config, 20 runs)
  - Parameter summary statistics printed and plausible (means near Beta means in BETA_PARAMS)
  - No agent has jointly extreme values on negatively correlated parameters at rate > 2%
  - PSD re-verified after sampling (utils.verify_psd called)
  - Seed logged per run

Population sizing: 8 configs × 500 agents × 20 runs = 80,000 draws total (trivial compute).
See modus operandi §3.4.3.
"""

# TODO (Phase 4): implement using utils.sample_agents().
# Print agent count, parameter means, and parameter ranges after every sampling call.
# Non-negotiable per CLAUDE.md Rule 3 and Rule 6.

raise NotImplementedError("04_agents.py is not yet implemented.")
