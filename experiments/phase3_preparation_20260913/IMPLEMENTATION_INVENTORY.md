# Phase 3 implementation inventory

Existing reusable components, inspected read-only:

- code/engine/population.py: paired profiles, content hash and deterministic order.
- code/engine/prompt_assembly.py: canonical profile template; accepts binary contexts
  only. It cannot represent individual neutral benchmark axes as written.
- code/engine/llm_client.py: provider abstraction and MockClient; a production Phase 3
  transport needs its own audited reservation/retry contract before reuse.
- code/phase2_confirmation_transport.py: immutable confirmation ledger and accounting;
  frozen study code remains unchanged. Its rates were checked against current docs.
- code/utils.py: canonical R and Beta marginals; unchanged by the sensitivity module.

No Phase 3 benchmark runner or canonical/decanonised benchmark prompt files were
found under code/ or prompts/. Existing C1-C3 viewer endpoints cannot display new
benchmarks without a separately checked adapter.

Added preparation tools:

- code/phase3_preflight.py: all-five nominal schedule accounting, explicit-neutral
  validation, duplicate slot detection and cost scenarios. No network or API client.
- code/phase3_sensitivity.py: draft A/B/C/100 D matrices, Higham projection and
  Gaussian/t copula sampling with unchanged ten Beta marginals. Weak entries are
  provisionally absolute correlations below .25, excluding the diagonal. Projection
  can move strong entries; record raw/projected matrices and correction sizes before
  using any of these in a released study. Samples are offline fixtures, not frozen
  experimental populations.
- tests/test_phase3_preparation.py: scope/count and duplicate checks, explicit
  neutral semantics, PSD/unit-diagonal checks, deterministic D generation, canonical
  immutability and marginal-distribution checks (including the t-copula CDF).

Run from repository root, using the research Python environment:

    py -3.11 -B code/phase3_preflight.py --output experiments/phase3_preparation_20260913/preflight_report.json
    py -3.11 -B -m unittest discover -s tests -p test_phase3_preparation.py -v

If dependencies are only in output/phase2_runtime, put that directory on PYTHONPATH.
Passing preparation tests is not a benchmark-validity pass or paid-run release.
