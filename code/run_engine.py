"""
run_engine.py — operator entry point for the Phase 2 simulation engine.

Drives the simple-problem LPM runner (spec Part 5) and the complex-problem
orchestrator + bridge calibration (spec §6). Reads the configuration subset
from config/configurations.json and the phase-2 seed from config/seeds.json.

SAFETY: nothing calls a live model unless you pass --provider openai (or
anthropic/google) AND the corresponding API key is set. The default --provider
mock runs the entire engine offline with deterministic responses, for
structural verification and cost estimation.

Examples
--------
# Offline end-to-end smoke of everything, tiny N (no API, no cost):
python code/run_engine.py --provider mock --stage all --n-agents 6 \
    --configs 00100 11011 --runs-per-config 2

# Real simple-problem Phase 2 (only after config subset sign-off + Phase 1.5):
python code/run_engine.py --provider openai --stage simple

Records are write-once under experiments/phase2_simple/ and phase2_complex/.
"""

from __future__ import annotations

import argparse
import asyncio
import json
from pathlib import Path

import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

sys.path.insert(0, str(Path(__file__).resolve().parent))

from engine import simple_runner, complex_runner
from engine.llm_client import LLMClient, MockClient
from engine.population import Population

REPO_ROOT = Path(__file__).resolve().parent.parent
CONFIG_DIR = REPO_ROOT / "config"


def load_config_codes(explicit: list[str] | None) -> list[str]:
    if explicit:
        return explicit
    path = CONFIG_DIR / "configurations.json"
    if not path.exists():
        raise SystemExit("config/configurations.json missing — run build_config.py or pass --configs")
    data = json.loads(path.read_text(encoding="utf-8"))
    return [e["code"] for e in data["configurations"]]


def load_seed(name: str, default: int) -> int:
    path = CONFIG_DIR / "seeds.json"
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))["seeds"].get(name, default)


def make_client(provider: str, model: str, concurrency: int):
    if provider == "mock":
        return MockClient(model="mock-model", concurrency=concurrency)
    return LLMClient(model=model, concurrency=concurrency)


async def main_async(args) -> None:
    config_codes = load_config_codes(args.configs)
    phase2_seed = load_seed("phase2_simple", 20260605)
    complex_seed = load_seed("phase2_complex", 20260606)

    client = make_client(args.provider, args.model, args.concurrency)
    is_mock = args.provider == "mock"

    # Population: for a real run use the locked 200; for mock allow a small N.
    if is_mock:
        population = Population.draw(args.n_agents, seed=phase2_seed)
    else:
        population = simple_runner.load_or_draw_population(phase2_seed, n=args.n_agents)
        print(f"population hash: {population.content_hash()[:16]}  (N={population.n})")

    if args.stage in ("simple", "all"):
        print("\n== SIMPLE PROBLEMS (LPM) ==")
        await simple_runner.run_simple(
            client=client, config_codes=config_codes, root_seed=phase2_seed,
            population=population,
            out_root=(REPO_ROOT / "experiments" / ("_mock_phase2_simple" if is_mock else "phase2_simple")))

    if args.stage in ("complex", "all"):
        print("\n== COMPLEX PROBLEMS (orchestrator) ==")
        out = REPO_ROOT / "experiments" / ("_mock_phase2_complex" if is_mock else "phase2_complex")
        await complex_runner.run_complex(
            client=client, population=population, config_codes=config_codes,
            root_seed=complex_seed,
            problems=tuple(args.problems), out_root=out,
            max_concurrent_runs=args.max_runs)
        if args.bridge:
            print("\n== BRIDGE CALIBRATION ==")
            await complex_runner.run_bridge(
                client=client, population=population, root_seed=complex_seed,
                problems=tuple(args.problems), out_root=out,
                max_concurrent_runs=args.max_runs)


def parse_args():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--provider", choices=["mock", "openai", "anthropic", "google"],
                   default="mock", help="mock = offline, no API, no cost (default).")
    p.add_argument("--model", default="gpt-5.4-mini")
    p.add_argument("--stage", choices=["simple", "complex", "all"], default="all")
    p.add_argument("--problems", nargs="+", choices=["C1", "C2", "C3"],
                   default=["C1", "C2", "C3"])
    p.add_argument("--configs", nargs="+", default=None,
                   help="Config codes (default: all from configurations.json).")
    p.add_argument("--n-agents", type=int, default=200,
                   help="Population size (use small, e.g. 6, for mock smoke).")
    p.add_argument("--runs-per-config", type=int, default=None,
                   help="Override runs per config (mock only; real uses problem defaults).")
    p.add_argument("--concurrency", type=int, default=10)
    p.add_argument("--max-runs", type=int, default=4, help="Concurrent complex runs.")
    p.add_argument("--bridge", action="store_true", help="Also run bridge calibration.")
    args = p.parse_args()
    # runs-per-config override (mock convenience): patch the problem defaults.
    if args.runs_per_config is not None:
        from engine import problems as _pr
        for prob in _pr.COMPLEX_PROBLEMS.values():
            object.__setattr__(prob, "runs_per_config", args.runs_per_config)
    return args


def main():
    asyncio.run(main_async(parse_args()))


if __name__ == "__main__":
    main()
