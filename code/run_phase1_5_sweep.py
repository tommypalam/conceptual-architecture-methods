"""
run_phase1_5_sweep.py — Phase 1.5 §4.1 single-parameter sweep (PILOT SCALE).

Reduced-scale diagnostic BEFORE committing to the full 7,500-call sweep: sweep a
small set of parameters that have pre-specified directional hypotheses (§6.1.1),
on the PRIMARY-tier problems (S1, S3), at reduced N, to confirm gradients appear
at all.

Each parameter is swept across {0.1, 0.3, 0.5, 0.7, 0.9} with the other nine held
at population means and a neutral normative context (SweepProfile), delivered as
the full Phase-2 harness (system message + DECISION/REASONING). Per (param,
problem) it fits a logistic regression of P(opt0) on the swept value and reports
slope, monotonicity, and Cohen's h between the extreme sweep values (§4.1.2/3).

Directional hypotheses under test (§6.1.1):
  - RE on S1: higher RE -> A (opt0).            predicted slope > 0
  - RE on S3: higher RE -> WAIT (opt1=ADOPT is opt0) -> predicted slope < 0 for ADOPT
  - RT on S3: higher RT -> ADOPT (opt0).        predicted slope > 0
(One parameter, RE, with OPPOSITE predicted signs on S1 vs S3 is the cleanest
evidence the model reads the parameter rather than carrying a fixed bias.)

SAFETY: default provider mock. Real runs print cost + confirm.

Example:
  python code/run_phase1_5_sweep.py --provider openai --params RE RT \
      --problems S1 S3 --n 25 --yes
"""

from __future__ import annotations

import argparse
import asyncio
import json
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

sys.path.insert(0, str(Path(__file__).resolve().parent))

from engine import phase0b_runner
from engine.phase0b import SweepProfile
from engine.delivery import SystemRoleDelivery
from engine.llm_client import LLMClient, MockClient
from engine.questions import PHASE0B_QUESTIONS
from engine.record_sink import JsonFileSink

REPO_ROOT = Path(__file__).resolve().parent.parent
OUT_ROOT = REPO_ROOT / "experiments" / "phase1_5_encoding_validity" / "sweeps_pilot"
SWEEP_VALUES = (0.1, 0.3, 0.5, 0.7, 0.9)
COST_PER_CALL_USD = 0.001


def load_seed() -> int:
    path = REPO_ROOT / "config" / "seeds.json"
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))["seeds"].get(
            "phase1_5_sweep", 20260729)
    return 20260729


def make_client(provider, model, concurrency):
    return (MockClient(concurrency=concurrency) if provider == "mock"
            else LLMClient(model=model, concurrency=concurrency))


def logistic_slope(xs, ys):
    """Tiny Newton-Raphson logistic fit P(y=1)=sigmoid(b0+b1*x). Returns b1."""
    b0 = b1 = 0.0
    for _ in range(50):
        g0 = g1 = h00 = h01 = h11 = 0.0
        for x, y in zip(xs, ys):
            p = 1.0 / (1.0 + math.exp(-(b0 + b1 * x)))
            g0 += (y - p); g1 += (y - p) * x
            w = p * (1 - p)
            h00 += w; h01 += w * x; h11 += w * x * x
        det = h00 * h11 - h01 * h01
        if abs(det) < 1e-12:
            break
        b0 += (h11 * g0 - h01 * g1) / det
        b1 += (-h01 * g0 + h00 * g1) / det
    return b1


def cohens_h(p1, p2):
    def phi(p):
        p = min(max(p, 1e-9), 1 - 1e-9)
        return 2 * math.asin(math.sqrt(p))
    return abs(phi(p1) - phi(p2))


async def run(args):
    client = make_client(args.provider, args.model, args.concurrency)
    problems = tuple(p for p in phase0b_runner.PROBLEMS if p.short_id in args.problems)
    seed = load_seed()
    for param in args.params:
        # Each sweep value is a "condition"; the phase0b runner iterates
        # conditions x problems x N. Full Phase-2 harness (system role + DECISION).
        assemblers = {f"{param}_{v:.1f}": SweepProfile(sweep_param=param, sweep_value=v,
                                                       condition_id=f"{param}_{v:.1f}")
                      for v in SWEEP_VALUES}
        sink = JsonFileSink(OUT_ROOT / param)
        await phase0b_runner.run_phase0b(
            client=client, assemblers=assemblers, sink=sink,
            delivery=SystemRoleDelivery(), questions_dir=PHASE0B_QUESTIONS,
            bare_label=False, max_tokens=600,
            root_seed=seed, n=args.n, problems=problems)
    analyze(args)


def analyze(args):
    print("\n" + "=" * 72)
    print("PHASE 1.5 SWEEP (pilot scale) — logistic gradient per (param, problem)")
    print("full Phase-2 harness | neutral config | recalibrated set")
    print("=" * 72)
    print(f"{'param':6}{'prob':5}{'sweep proportions (opt0 rate @ .1/.3/.5/.7/.9)':48}")
    print(f"{'':11}{'slope':8}{'CohenH(ext)':13}{'monotonic':11}{'signal?'}")
    print("-" * 72)
    for param in args.params:
        sink = JsonFileSink(OUT_ROOT / param)
        recs = list(sink.read_all())
        for pid in args.problems:
            props = {}
            for v in SWEEP_VALUES:
                cell = [r for r in recs if r.get("problem_id") == pid
                        and r.get("condition_id") == f"{param}_{v:.1f}"
                        and r.get("parse_status") == "ok" and r.get("parsed_decision")]
                if not cell:
                    props[v] = None; continue
                labels = cell[0].get("labels")
                k = sum(1 for r in cell if r["parsed_decision"] == labels[0])
                props[v] = k / len(cell)
            vals = [(v, props[v]) for v in SWEEP_VALUES if props[v] is not None]
            if len(vals) < 2:
                print(f"{param:6}{pid:5} insufficient data"); continue
            xs = [v for v, _ in vals]; ps = [p for _, p in vals]
            # reconstruct per-call ys for the slope fit
            ys_x = []
            for v in SWEEP_VALUES:
                cell = [r for r in recs if r.get("problem_id") == pid
                        and r.get("condition_id") == f"{param}_{v:.1f}"
                        and r.get("parse_status") == "ok" and r.get("parsed_decision")]
                for r in cell:
                    ys_x.append((v, 1 if r["parsed_decision"] == r["labels"][0] else 0))
            slope = logistic_slope([x for x, _ in ys_x], [y for _, y in ys_x])
            h = cohens_h(ps[0], ps[-1])
            diffs = [ps[i + 1] - ps[i] for i in range(len(ps) - 1)]
            monotonic = all(d >= -1e-9 for d in diffs) or all(d <= 1e-9 for d in diffs)
            signal = "YES" if (h >= 0.20 and monotonic) else ("weak" if h >= 0.20 else "no")
            propstr = " ".join(f"{p:.2f}" for p in ps)
            print(f"{param:6}{pid:5}{propstr:48}")
            print(f"{'':11}{slope:<8.2f}{h:<13.2f}{str(monotonic):11}{signal}")
    print("-" * 72)
    print("signal = Cohen's h>=0.20 between extremes AND monotonic (pilot proxy for §4.1.3)")


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--provider", choices=["mock", "openai", "anthropic", "google"],
                   default="mock")
    p.add_argument("--model", default="gpt-5.4-mini")
    p.add_argument("--params", nargs="+", default=["RE", "RT"])
    p.add_argument("--problems", nargs="+", default=["S1", "S3"])
    p.add_argument("--n", type=int, default=25, help="Calls per sweep value.")
    p.add_argument("--concurrency", type=int, default=5)
    p.add_argument("--score-only", action="store_true")
    p.add_argument("--yes", action="store_true")
    args = p.parse_args()

    if args.score_only:
        analyze(args); return

    n_calls = len(args.params) * len(SWEEP_VALUES) * len(args.problems) * args.n
    print(f"Planned: {n_calls} calls ({len(args.params)} params x {len(SWEEP_VALUES)} "
          f"values x {len(args.problems)} problems x N={args.n}) | "
          f"est ~${n_calls*COST_PER_CALL_USD:,.2f} | provider {args.provider}")
    if args.provider != "mock" and not args.yes:
        if input("Proceed? [y/N] ").strip().lower() not in ("y", "yes"):
            print("Aborted."); return
    asyncio.run(run(args))


if __name__ == "__main__":
    main()
