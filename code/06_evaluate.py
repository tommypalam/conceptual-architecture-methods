"""
06_evaluate.py — Validation: Milgram retrodiction test and SPE benchmark.

Phase: 5 (Evaluation)
Input:  data/processed/results_{config_code}_{run_id}.parquet (all configs)
Output: output/tables/table_02_config_results.tex
        output/figures/fig_04_milgram_retrodiction.html
        output/logs/evaluation.log

Done when:
  - Config 001 (Despotism) obedience rate computed across all runs with 95% CI
  - Milgram retrodiction: 0.61–0.66 = PASS; outside range = FAIL (log the number, do not fudge)
  - Config 110 (Direct Democracy) used as structural inverse comparison
  - SPE analogy: 111→001 transition dynamics documented
  - Three-regime sensitivity analysis (regimes A, B, C from utils.py) run and compared
  - All results logged with config code, N, runs, seed, CI

PRIMARY VALIDATION METRIC: obedience_rate for config 001.
Do not mark Phase 5 complete without a logged retrodiction result, pass or fail.
"""

# TODO (Phase 5): implement evaluation and retrodiction test.
# If retrodiction fails, DO NOT adjust R silently — log the failure, convene panel,
# diagnose before any recalibration.

raise NotImplementedError("06_evaluate.py is not yet implemented.")
