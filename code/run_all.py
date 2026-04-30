"""
run_all.py — Master entry point. Runs the full PARIA pipeline from raw data to outputs.

Usage:
    python code/run_all.py --seed 42

Sequence:
    01_intake.py        → load and validate raw calibration data
    02_distributions.py → fit Beta marginals, verify copula PSD
    03_encode.py        → encode concept priors via PyMC
    04_agents.py        → sample agent populations
    05_simulate.py      → run Mesa ABM across all 8 configurations
    06_evaluate.py      → Milgram retrodiction + SPE benchmark
    07_output.py        → generate tables and figures

Replication packaging requirement (research-os-template.md §15):
  A newcomer must be able to run this single script and reproduce all outputs.
  No hardcoded local paths. All paths relative to project root.
"""

# TODO (Phase 6): implement master pipeline runner.
# Do not implement until all constituent scripts are individually verified.

raise NotImplementedError(
    "run_all.py is not yet implemented. "
    "Run individual scripts (01_intake.py through 07_output.py) during development."
)
