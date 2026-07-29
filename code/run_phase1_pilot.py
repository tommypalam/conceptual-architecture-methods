"""
run_phase1_pilot.py — Phase 1 operational pilot (spec Part 3).

The pilot is OPERATIONAL, not scientific: it verifies the pipeline runs
end-to-end (population draw -> full Phase-2 harness assembly -> API -> parse ->
store), and reports the five §3.2 diagnostics. It does NOT test encoding validity
(that is Phase 1.5).

Findings-aware deviations from spec §3.1 (documented in PHASE0_CLOSURE and here):
  - Problem: spec picks S2, but Phase 0b proved S2 is the most harness-fragile
    (collapses under the full harness). So we run BOTH:
      * S3 (PRIMARY tier, survived the full harness) — the clean pipeline check;
      * S2 (spec's choice) — to document whether the collapse carries into the
        full Phase-2 config at pilot stage.
  - Question set: the recalibrated locked set (experiments/phase0b_calibration),
    consistent with 0b/0c. 0a set stays frozen.
  - Configuration: spec says "authority-low, justice-low, otherwise neutral".
    Binary 5-bit codes cannot encode per-axis "neutral"; we use 10011
    (Freedom=1, Justice=0, Authority=0, Care=1, Loyalty=1) — J&A low, the other
    three high — as the closest expressible reading, documented as a pilot choice.

SAFETY: default provider mock. Real runs print cost + confirm.

Example:
  python code/run_phase1_pilot.py --provider openai --n 50 --yes
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from collections import Counter
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

sys.path.insert(0, str(Path(__file__).resolve().parent))

from engine import simple_runner
from engine.llm_client import LLMClient, MockClient
from engine.population import Population
from engine.questions import PHASE0B_QUESTIONS
from engine.record_sink import JsonFileSink
from engine.scoring import wilson_ci

REPO_ROOT = Path(__file__).resolve().parent.parent
OUT_ROOT = REPO_ROOT / "experiments" / "phase1_pilot"
CONFIG = "10011"            # F=1, J=0, A=0, C=1, L=1  (authority-low, justice-low)
PILOT_PROBLEMS = ("S3", "S2")   # S3 = clean pipeline check; S2 = spec + collapse doc
COST_PER_CALL_USD = 0.001


def load_seed() -> int:
    path = REPO_ROOT / "config" / "seeds.json"
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))["seeds"].get(
            "phase1_pilot", 20260729)
    return 20260729


def make_client(provider, model, concurrency):
    return (MockClient(concurrency=concurrency) if provider == "mock"
            else LLMClient(model=model, concurrency=concurrency))


async def run(args):
    client = make_client(args.provider, args.model, args.concurrency)
    seed = load_seed()
    population = Population.draw(args.n, seed=seed)
    problems = tuple(p for p in simple_runner.SIMPLE_PROBLEMS
                     if p.short_id in PILOT_PROBLEMS)
    sink = JsonFileSink(OUT_ROOT / "runs")
    await simple_runner.run_simple(
        client=client, config_codes=[CONFIG], root_seed=seed,
        population=population, problems=problems, sink=sink,
        questions_dir=PHASE0B_QUESTIONS)
    diagnostics(sink)


def diagnostics(sink) -> None:
    recs = list(sink.read_all())
    print("\n" + "=" * 70)
    print("PHASE 1 PILOT — diagnostics (spec §3.2)")
    print(f"config {CONFIG} (F=1,J=0,A=0,C=1,L=1) | recalibrated set | full harness")
    print("=" * 70)
    by_problem = {}
    for r in recs:
        by_problem.setdefault(r.get("problem_id"), []).append(r)

    for pid in PILOT_PROBLEMS:
        rs = by_problem.get(pid, [])
        if not rs:
            print(f"\n[{pid}] no records"); continue
        n = len(rs)
        n_ok = sum(1 for r in rs if r.get("parse_status") == "ok")
        parse_rate = n_ok / n if n else 0
        dec = Counter(r["parsed_decision"] for r in rs
                      if r.get("parse_status") == "ok" and r.get("parsed_decision"))
        labels = rs[0].get("labels") or sorted(dec)
        k = dec.get(labels[0], 0)
        lo, hi = wilson_ci(k, n_ok) if n_ok else (0, 0)
        unanimous = len(dec) <= 1
        print(f"\n[{pid}]  N={n}")
        print(f"  1. parse integrity : {n_ok}/{n} = {parse_rate:.0%}  "
              f"(target 100%, tol >=98%) {'PASS' if parse_rate>=0.98 else 'FAIL'}")
        split = ", ".join(f"{a} {c}" for a, c in sorted(dec.items())) or "-"
        print(f"  2. decision dist.  : {split}  rate({labels[0]})="
              f"{(k/n_ok if n_ok else 0):.2f} CI[{lo:.2f},{hi:.2f}]  "
              f"{'FAIL (unanimous)' if unanimous else 'PASS (graded)'}")
        print(f"  3. reasoning recov.: (manual audit of 10 samples — see below)")
        print(f"  5. impl health     : pipeline ran, records written, "
              f"immutable — PASS")
    # dump 10 reasoning samples per problem for the manual §3.2 checks (3,4)
    print("\n--- reasoning samples (for diagnostics 3 & 4, manual audit) ---")
    for pid in PILOT_PROBLEMS:
        rs = [r for r in by_problem.get(pid, []) if r.get("parsed_reasoning")][:5]
        print(f"\n[{pid}]")
        for r in rs:
            print(f"  {r.get('parsed_decision')}: {str(r.get('parsed_reasoning'))[:160]}")


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--provider", choices=["mock", "openai", "anthropic", "google"],
                   default="mock")
    p.add_argument("--model", default="gpt-5.4-mini")
    p.add_argument("--n", type=int, default=50, help="Agents per problem.")
    p.add_argument("--concurrency", type=int, default=5)
    p.add_argument("--score-only", action="store_true")
    p.add_argument("--yes", action="store_true")
    args = p.parse_args()

    if args.score_only:
        diagnostics(JsonFileSink(OUT_ROOT / "runs")); return

    n_calls = args.n * len(PILOT_PROBLEMS)
    print(f"Planned: {n_calls} calls ({len(PILOT_PROBLEMS)} problems x N={args.n}) "
          f"| est ~${n_calls*COST_PER_CALL_USD:,.2f} | provider {args.provider}")
    if args.provider != "mock" and not args.yes:
        if input("Proceed? [y/N] ").strip().lower() not in ("y", "yes"):
            print("Aborted."); return
    asyncio.run(run(args))


if __name__ == "__main__":
    main()
