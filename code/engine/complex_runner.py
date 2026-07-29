"""
complex_runner.py — drive the orchestrator across runs and configurations
for the Phase 2 complex problems, plus bridge calibration (spec §6.4–6.5).

For each complex problem and each configuration, run `runs_per_config`
independent simulations. Agents for each run are drawn from the hash-locked
paired-agent population (spec §5.1 / §6.4: "all sampled from the paired-agent
population") via a deterministic per-run selection so runs are reproducible.

Bridge calibration (§6.5): the same orchestrator with `bridge=True` (parameter
block omitted), run under a single neutral configuration, `runs_per_config`
times per problem — the no-architecture baseline the parameterised runs are
reported against.

Records are write-once JSON (Appendix C.3) under
  experiments/phase2_complex/{problem}/{config}/run_{k}.json
  experiments/phase2_complex/bridge_calibration/{problem}/run_{k}.json
"""

from __future__ import annotations

import asyncio
from pathlib import Path

import numpy as np

from .llm_client import SupportsComplete
from .orchestrator import Orchestrator, run_result_to_record
from .population import Population
from .problems import COMPLEX_PROBLEMS
from .record_sink import JsonFileSink, RecordSink
from .seeding import derive_seed

REPO_ROOT = Path(__file__).resolve().parents[2]
OUT_ROOT = REPO_ROOT / "experiments" / "phase2_complex"
NEUTRAL_CONFIG = "bridge_neutral"   # sentinel; bridge omits parameter block anyway


def select_run_agents(population: Population, problem_short: str, config_code: str,
                      run_index: int, n_agents: int, root_seed: int) -> list[dict]:
    """Deterministically pick n_agents distinct profiles for one run."""
    local = derive_seed(root_seed, problem_short, config_code, f"run{run_index}")
    rng = np.random.default_rng(local)
    idx = rng.choice(len(population.agents), size=n_agents, replace=False)
    return [population.agents[i].as_record() for i in idx]


async def run_complex(*, client: SupportsComplete, population: Population,
                      config_codes: list[str], root_seed: int,
                      problems=("C1", "C2", "C3"), sink: RecordSink | None = None,
                      out_root: Path = OUT_ROOT, resume: bool = True,
                      max_concurrent_runs: int = 4) -> dict:
    """Parameterised complex runs across problems x configs x runs."""
    if sink is None:
        sink = JsonFileSink(out_root)
    run_sem = asyncio.Semaphore(max_concurrent_runs)
    planned = executed = skipped = 0
    lock = asyncio.Lock()

    async def one_run(problem, config_code, k):
        nonlocal executed, skipped
        key = f"{problem.short_id}/{config_code}/run_{k:03d}"
        if resume and sink.exists(key):
            async with lock:
                skipped += 1
            return
        run_id = f"{problem.short_id}_{config_code}_run{k:03d}"
        profiles = select_run_agents(population, problem.short_id, config_code, k,
                                     problem.n_agents, root_seed)
        run_seed = derive_seed(run_id)
        async with run_sem:
            orch = Orchestrator(problem, config_code, profiles, client=client,
                                run_id=run_id, seed=run_seed, bridge=False)
            result = await orch.run()
        sink.write(key, run_result_to_record(result))
        async with lock:
            executed += 1
            if executed % 10 == 0:
                print(f"  complex runs executed: {executed} (skipped {skipped})")

    tasks = []
    for short in problems:
        problem = COMPLEX_PROBLEMS[short]
        for config_code in config_codes:
            for k in range(1, problem.runs_per_config + 1):
                planned += 1
                tasks.append(one_run(problem, config_code, k))
    await asyncio.gather(*tasks)
    summary = {"mode": "parameterised", "planned": planned,
               "executed": executed, "skipped": skipped}
    print(f"complex runner: {summary}")
    return summary


async def run_bridge(*, client: SupportsComplete, population: Population,
                     root_seed: int, problems=("C1", "C2", "C3"),
                     sink: RecordSink | None = None, out_root: Path = OUT_ROOT,
                     resume: bool = True, max_concurrent_runs: int = 4) -> dict:
    """Bridge calibration: no-parameter baseline, single neutral config (§6.5)."""
    if sink is None:
        sink = JsonFileSink(out_root)
    run_sem = asyncio.Semaphore(max_concurrent_runs)
    planned = executed = skipped = 0
    lock = asyncio.Lock()

    async def one_run(problem, k):
        nonlocal executed, skipped
        key = f"bridge_calibration/{problem.short_id}/run_{k:03d}"
        if resume and sink.exists(key):
            async with lock:
                skipped += 1
            return
        run_id = f"{problem.short_id}_bridge_run{k:03d}"
        profiles = select_run_agents(population, problem.short_id, NEUTRAL_CONFIG, k,
                                     problem.n_agents, root_seed)
        run_seed = derive_seed(run_id)
        async with run_sem:
            orch = Orchestrator(problem, NEUTRAL_CONFIG, profiles, client=client,
                                run_id=run_id, seed=run_seed, bridge=True)
            result = await orch.run()
        sink.write(key, run_result_to_record(result))
        async with lock:
            executed += 1

    tasks = []
    for short in problems:
        problem = COMPLEX_PROBLEMS[short]
        for k in range(1, problem.runs_per_config + 1):
            planned += 1
            tasks.append(one_run(problem, k))
    await asyncio.gather(*tasks)
    summary = {"mode": "bridge", "planned": planned,
               "executed": executed, "skipped": skipped}
    print(f"bridge runner: {summary}")
    return summary
