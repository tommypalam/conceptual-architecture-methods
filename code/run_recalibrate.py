"""
run_recalibrate.py — Step D naked-prompt recalibration CLI.

Two modes:
  --baseline   run all six ORIGINAL dilemmas naked on the current model, to
               establish today's true naked split per problem (the reference
               every rewrite is measured against). No edits, just measurement.
  --candidate  run one candidate dilemma (text from a file) naked at N, to see
               if a rewording lands in 45-55 on the current model.

Naked = Phase-0a protocol: no system message, dilemma + "Reply with only: X or Y",
bare decision. Records archived under experiments/phase0b_archive/recalibrate__{tag}/.

SAFETY: default --provider mock. Real runs print cost + confirm.

Examples
--------
python code/run_recalibrate.py --provider openai --baseline --n 100 --sample-tag baseline_current
python code/run_recalibrate.py --provider openai --candidate S2 --text prompts/candidates/S2_v1.md --n 100 --sample-tag S2_v1
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

sys.path.insert(0, str(Path(__file__).resolve().parent))

from engine import recalibrate
from engine.llm_client import LLMClient, MockClient
from engine.questions import load_dilemma_body
from engine.phase0b_runner import PROBLEMS
from engine.record_sink import JsonFileSink

REPO_ROOT = Path(__file__).resolve().parent.parent
ARCHIVE = REPO_ROOT / "experiments" / "phase0b_archive"
COST_PER_CALL_USD = 0.001

LABELS = {p.short_id: p.labels for p in PROBLEMS}
QFILE = {p.short_id: p.question_file for p in PROBLEMS}


def load_seed() -> int:
    path = REPO_ROOT / "config" / "seeds.json"
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))["seeds"].get(
            "phase0b_harness_neutral", 20260601)
    return 20260601


def make_client(provider, model, concurrency):
    return (MockClient(concurrency=concurrency) if provider == "mock"
            else LLMClient(model=model, concurrency=concurrency))


def confirm(args, n_calls) -> bool:
    print(f"\nPlanned: {n_calls} calls | provider: {args.provider} | "
          f"est ~${n_calls * COST_PER_CALL_USD:,.2f}")
    if args.provider == "mock" or args.yes:
        return True
    return input("Proceed? [y/N] ").strip().lower() in ("y", "yes")


async def run_baseline(args):
    client = make_client(args.provider, args.model, args.concurrency)
    tag = args.sample_tag or "baseline_current"
    sink = JsonFileSink(ARCHIVE / f"recalibrate__{tag}")
    results = []
    for pid in [p.short_id for p in PROBLEMS]:
        body = load_dilemma_body(QFILE[pid])
        r = await recalibrate.calibrate_candidate(
            client=client, sink=sink, candidate_id=pid, dilemma_body=body,
            labels=LABELS[pid], n=args.n, root_seed=load_seed())
        results.append((pid, r))
    print("\n" + "=" * 60)
    print("NAKED BASELINE (original dilemmas, current model)")
    print("=" * 60)
    print(f"{'prob':5} {'split':30} {'CI':18} verdict")
    print("-" * 60)
    for pid, r in results:
        split = ", ".join(f"{k} {v}" for k, v in sorted(r["counts"].items()))
        ci = f"[{r['wilson_95'][0]:.2f},{r['wilson_95'][1]:.2f}]"
        print(f"{pid:5} {split:30} {ci:18} {r['verdict']}")


async def run_candidate(args):
    client = make_client(args.provider, args.model, args.concurrency)
    body = Path(args.text).read_text(encoding="utf-8").strip()
    labels = LABELS[args.candidate]
    tag = args.sample_tag or f"{args.candidate}_cand"
    sink = JsonFileSink(ARCHIVE / f"recalibrate__{tag}")
    r = await recalibrate.calibrate_candidate(
        client=client, sink=sink, candidate_id=tag, dilemma_body=body,
        labels=labels, n=args.n, root_seed=load_seed())
    print("\n" + "=" * 60)
    print(f"CANDIDATE {args.candidate}  (labels {labels})")
    print("=" * 60)
    split = ", ".join(f"{k} {v}" for k, v in sorted(r["counts"].items()))
    print(f"split: {split}")
    print(f"rate({r['rate_label']}): {r['rate']}  CI {r['wilson_95']}")
    print(f"verdict: {r['verdict']}")


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--provider", choices=["mock", "openai", "anthropic", "google"],
                   default="mock")
    p.add_argument("--model", default="gpt-5.4-mini")
    p.add_argument("--n", type=int, default=100)
    p.add_argument("--concurrency", type=int, default=10)
    p.add_argument("--baseline", action="store_true", help="Run all 6 original dilemmas.")
    p.add_argument("--candidate", choices=[p.short_id for p in PROBLEMS],
                   help="Recalibrate one problem from a candidate text file.")
    p.add_argument("--text", type=Path, help="Candidate dilemma text file (with --candidate).")
    p.add_argument("--sample-tag", default=None)
    p.add_argument("--yes", action="store_true")
    args = p.parse_args()

    if args.baseline:
        n_calls = args.n * len(PROBLEMS)
        if not confirm(args, n_calls):
            print("Aborted."); return
        asyncio.run(run_baseline(args))
    elif args.candidate:
        if not args.text:
            p.error("--candidate requires --text")
        if not confirm(args, args.n):
            print("Aborted."); return
        asyncio.run(run_candidate(args))
    else:
        p.error("pass --baseline or --candidate")


if __name__ == "__main__":
    main()
