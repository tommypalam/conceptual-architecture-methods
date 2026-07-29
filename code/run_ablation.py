"""
run_ablation.py — composition root for the harness-framing ablation.

Isolates WHICH framing element causes the systemic Phase 0b bias (grid100,
2026-07-28) by toggling one element at a time and measuring how close each
problem's split gets to 50/50. Dilemma bodies are held fixed; only the framing
changes. Runs under the empty harness (null_a) so the signal is pure framing.

SAFETY: default --provider mock is offline. A real run prints a cost estimate
and asks for confirmation.

Sizing: 5 variants x 6 problems x N. At N=30 that is 900 calls (~$0.90).
Records live in experiments/phase0b_ablation__{tag}/ (never a canonical dir).

Examples
--------
python code/run_ablation.py --dry-run --variant no_decision_rule --problem S1
python code/run_ablation.py --provider openai --n 30 --sample-tag ablate1
python code/run_ablation.py --score-only --sample-tag ablate1
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

from engine import ablation, ablation_scorer
from engine.framing import (ablation_variants, reasoning_test_variants,
                            system_role_test_variants, format_sweep_variants)
from engine.llm_client import LLMClient, MockClient

VARIANT_SETS = {
    "ablation": ablation_variants,               # 5 single-clause toggles
    "reasoning-test": reasoning_test_variants,   # canonical vs decision_only
    "system-test": system_role_test_variants,    # canonical vs naked_repro (no system msg)
    "format-sweep": format_sweep_variants,       # breadth of output-format levers
}
from engine.phase0b_runner import PROBLEMS
from engine.prompt_assembly import load_template
from engine.record_sink import JsonFileSink

REPO_ROOT = Path(__file__).resolve().parent.parent
CONFIG_DIR = REPO_ROOT / "config"
COST_PER_CALL_USD = 0.001


def load_seed(default: int = 20260601) -> int:
    path = CONFIG_DIR / "seeds.json"
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))["seeds"].get(
        "phase0b_harness_neutral", default)


def resolve_root(tag: str | None) -> Path:
    base = REPO_ROOT / "experiments" / "phase0b_ablation"
    return base.parent / f"{base.name}__{tag}" if tag else base


def do_dry_run(variants_all, variant_names, problem_ids):
    template = load_template()
    variants = variants_all
    probs = [p for p in PROBLEMS if p.short_id in problem_ids]
    for label in variant_names:
        fr = variants[label]
        for prob in probs:
            body = ablation.load_dilemma_body(prob.question_file)
            user = ablation.build_user_turn(fr, body, prob.labels)
            sysp = ablation.build_system_prompt(fr, template) if fr.use_system_role \
                else "(none - no system message sent)"
            print("=" * 74)
            print(f"VARIANT {label}  ({fr.label})  PROBLEM {prob.short_id}")
            print("=" * 74)
            print("[SYSTEM]\n" + sysp + "\n\n[USER]\n" + user + "\n")
    print("DRY RUN - no API calls, nothing written.")


def confirm_cost(args, sink, n_variants, n_problems) -> bool:
    total = args.n * n_variants * n_problems
    already = sum(1 for _ in sink.read_all()) if hasattr(sink, "read_all") else 0
    to_run = max(0, total - already)
    print(f"\nPlanned: {total} calls  ({n_variants} variants x {n_problems} "
          f"problems x N={args.n})")
    if already:
        print(f"Already recorded here: {already} -> new calls to make: {to_run}")
    print(f"Provider: {args.provider} | model: {args.model}")
    print(f"Estimated cost of new calls: ~${to_run * COST_PER_CALL_USD:,.2f}")
    if args.provider == "mock" or args.yes:
        return True
    return input("Proceed with the paid run? [y/N] ").strip().lower() in ("y", "yes")


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--provider", choices=["mock", "openai", "anthropic", "google"],
                   default="mock")
    p.add_argument("--model", default="gpt-5.4-mini")
    p.add_argument("--n", type=int, default=30, help="Calls per variant per problem.")
    p.add_argument("--concurrency", type=int, default=10)
    p.add_argument("--variant-set", choices=list(VARIANT_SETS), default="ablation",
                   help="Which framing set to test (default: ablation).")
    p.add_argument("--variant", nargs="+", dest="variants", default=None,
                   help="Subset of variant names within the chosen set.")
    p.add_argument("--problem", nargs="+", dest="problems",
                   choices=[pr.short_id for pr in PROBLEMS], default=None)
    p.add_argument("--questions-set", choices=["phase0a", "phase0b"],
                   default="phase0b",
                   help="Which locked question set: phase0b = recalibrated "
                        "2026-07-28 set (default); phase0a = frozen originals.")
    p.add_argument("--sample-tag", default=None)
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--yes", action="store_true")
    p.add_argument("--score-only", action="store_true")
    p.add_argument("--out", type=Path)
    args = p.parse_args()

    variants_all = VARIANT_SETS[args.variant_set]()
    variant_names = args.variants or list(variants_all.keys())
    problem_ids = args.problems or [pr.short_id for pr in PROBLEMS]

    if args.dry_run:
        do_dry_run(variants_all, variant_names, problem_ids)
        return

    root = resolve_root(args.sample_tag if args.provider != "mock" or args.score_only
                        else (args.sample_tag or "mock"))
    if args.provider == "mock" and not args.sample_tag:
        root = REPO_ROOT / "experiments" / "_mock_phase0b_ablation"
    sink = JsonFileSink(root)
    print(f"records dir: {root}")

    if not args.score_only:
        if not confirm_cost(args, sink, len(variant_names), len(problem_ids)):
            print("Aborted - no calls made.")
            return
        variants = {k: variants_all[k] for k in variant_names}
        problems = tuple(pr for pr in PROBLEMS if pr.short_id in problem_ids)
        client = (MockClient(concurrency=args.concurrency) if args.provider == "mock"
                  else LLMClient(model=args.model, concurrency=args.concurrency))
        from engine.questions import PHASE0_QUESTIONS, PHASE0B_QUESTIONS
        qdir = PHASE0B_QUESTIONS if args.questions_set == "phase0b" else PHASE0_QUESTIONS
        asyncio.run(ablation.run_ablation(
            client=client, sink=sink, root_seed=load_seed(), n=args.n,
            variants=variants, problems=problems, questions_dir=qdir))

    summary = ablation_scorer.score_ablation(sink.read_all())
    if args.out:
        args.out.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n",
                            encoding="utf-8")
        print(f"wrote {args.out}")
    print("\n" + "=" * 62)
    print("HARNESS-FRAMING ABLATION  (empty harness / null_a)")
    print("=" * 62)
    print(ablation_scorer.format_table(summary))


if __name__ == "__main__":
    main()
