"""
run_nulla_tasksweep.py — isolate which null_a TASK-TEXT clause collapses the
fragile dilemmas, envelope held neutral.

The N=300 canonical grid collapsed null_a; diffing prompts localized the cause to
the null_a task-instruction text (prime suspect "apply a CONSISTENT decision rule")
rather than the delivery envelope. This runs the three EmptyHarness task variants
(orig / neutral / minimal) as three conditions, under the blessed neutral delivery
(user_prefix + bare_label), on the fragile trio, so the task text is the only thing
that varies.

Archived under archive/phase0b/runs/. SAFETY: default provider mock.

Example:
  python code/run_nulla_tasksweep.py --provider openai --n 100 --problems S2 C2 C3 \
      --sample-tag nulla_tasksweep_n100
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

from engine import phase0b_runner, phase0b_scorer
from engine.phase0b import EmptyHarness, LadderHarness, _NULL_A_LADDER, _NULL_A_SCAFFOLDS
from engine.delivery import UserPrefixDelivery, SystemRoleDelivery
from engine.llm_client import LLMClient, MockClient
from engine.questions import PHASE0B_QUESTIONS
from engine.record_sink import JsonFileSink

REPO_ROOT = Path(__file__).resolve().parent.parent
ARCHIVE = REPO_ROOT / "archive" / "phase0b" / "runs"
COST_PER_CALL_USD = 0.001
VARIANTS = ("orig", "neutral", "minimal")
LADDER = tuple(_NULL_A_LADDER.keys())   # L0_naked .. L3_identity
SCAFFOLDS = tuple(_NULL_A_SCAFFOLDS.keys())   # w0_orig .. w3_plain


def load_seed() -> int:
    path = REPO_ROOT / "config" / "seeds.json"
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))["seeds"].get(
            "phase0b_harness_neutral", 20260601)
    return 20260601


def make_client(provider, model, concurrency):
    return (MockClient(concurrency=concurrency) if provider == "mock"
            else LLMClient(model=model, concurrency=concurrency))


async def run(args):
    client = make_client(args.provider, args.model, args.concurrency)
    if args.mode == "ladder":
        assemblers = {lv: LadderHarness(condition_id=lv, level=lv) for lv in LADDER}
        delivery, bare = UserPrefixDelivery(), True
    elif args.mode == "scaffold":
        # Full-scaffold WORDING variants under the SPEC-FAITHFUL config:
        # system-message delivery + DECISION/REASONING (bare_label False).
        assemblers = {w: EmptyHarness(condition_id=w, scaffold=w) for w in SCAFFOLDS}
        delivery, bare = SystemRoleDelivery(), args.bare_label
    else:  # task
        assemblers = {v: EmptyHarness(condition_id=v, task_variant=v) for v in VARIANTS}
        delivery, bare = UserPrefixDelivery(), True
    problems = tuple(p for p in phase0b_runner.PROBLEMS
                     if p.short_id in args.problems)
    tag = args.sample_tag or f"nulla_{args.mode}"

    if args.mode == "struct2x2":
        # 2x2: delivery {system_role, user_prefix} x output {DECISION+REASONING,
        # bare_label}. Wording held at w0 (spec original). Each corner is one
        # run_phase0b call into its own subfolder; scored together.
        corners = {
            "sys_decision":  (SystemRoleDelivery(), False, 600),
            "sys_bare":      (SystemRoleDelivery(), True, 30),
            "user_decision": (UserPrefixDelivery(), False, 600),
            "user_bare":     (UserPrefixDelivery(), True, 30),
        }
        for name, (deliv, br, mt) in corners.items():
            asm = {name: EmptyHarness(condition_id=name, scaffold="w0_orig")}
            await phase0b_runner.run_phase0b(
                client=client, assemblers=asm, sink=JsonFileSink(ARCHIVE / tag),
                delivery=deliv, questions_dir=PHASE0B_QUESTIONS,
                bare_label=br, max_tokens=mt,
                root_seed=load_seed(), n=args.n, problems=problems)
        print_table(phase0b_scorer.score_phase0b(JsonFileSink(ARCHIVE / tag).read_all()))
        return

    sink = JsonFileSink(ARCHIVE / tag)
    await phase0b_runner.run_phase0b(
        client=client, assemblers=assemblers, sink=sink,
        delivery=delivery, questions_dir=PHASE0B_QUESTIONS,
        bare_label=bare, max_tokens=args.max_tokens,
        root_seed=load_seed(), n=args.n, problems=problems)
    summary = phase0b_scorer.score_phase0b(sink.read_all())
    print_table(summary)


def print_table(summary: dict) -> None:
    print("\n" + "=" * 66)
    print("NULL_A TASK-TEXT SWEEP  (neutral envelope; task text is the only var)")
    print("bistable target: minority >= 20% (Wilson CI clear of extremes)")
    print("=" * 66)
    hdr = f"{'task':9} {'prob':5} {'n_ok':>5}  {'split':<24} {'CI':<16} bistable?"
    print(hdr); print("-" * len(hdr))
    for cond, byprob in summary.get("cells", {}).items():
        for pid, c in byprob.items():
            n_ok = c.get("n_ok", 0)
            counts = c.get("counts", {})
            split = ", ".join(f"{k} {v}" for k, v in sorted(counts.items())) or "-"
            if "rate" in c:
                lo, hi = c["wilson_95"]
                ci = f"[{lo:.2f}, {hi:.2f}]"
                minority = min(c["rate"], 1 - c["rate"])
                bis = "YES" if minority >= 0.20 else "no"
            else:
                ci, bis = "-", "?"
            print(f"{cond:9} {pid:5} {n_ok:>5}  {split:<24} {ci:<16} {bis}")
    print("-" * len(hdr))


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--provider", choices=["mock", "openai", "anthropic", "google"],
                   default="mock")
    p.add_argument("--model", default="gpt-5.4-mini")
    p.add_argument("--n", type=int, default=100)
    p.add_argument("--concurrency", type=int, default=5)
    p.add_argument("--problems", nargs="+",
                   choices=[pr.short_id for pr in phase0b_runner.PROBLEMS],
                   default=["S2", "C2", "C3"])
    p.add_argument("--max-tokens", type=int, default=600)
    p.add_argument("--mode",
                   choices=["task", "ladder", "scaffold", "struct2x2"],
                   default="scaffold",
                   help="scaffold = wording variants w0..w3 (spec-faithful config); "
                        "struct2x2 = delivery x output-format 2x2 (wording=w0), "
                        "isolates which STRUCTURAL lever collapses; "
                        "task = orig/neutral/minimal; ladder = L0..L3.")
    p.add_argument("--bare-label", action="store_true",
                   help="(scaffold mode) use bare-label output instead of "
                        "DECISION/REASONING — a further deviation, try only if the "
                        "spec-faithful wording fix does not reach 50%%.")
    p.add_argument("--sample-tag", default=None)
    p.add_argument("--yes", action="store_true")
    args = p.parse_args()

    n_conds = {"ladder": len(LADDER), "scaffold": len(SCAFFOLDS),
               "struct2x2": 4}.get(args.mode, len(VARIANTS))
    n_calls = args.n * n_conds * len(args.problems)
    print(f"Planned: {n_calls} calls ({n_conds} {args.mode} conditions x "
          f"{len(args.problems)} problems x N={args.n}) | est ~${n_calls*COST_PER_CALL_USD:,.2f}")
    if args.provider != "mock" and not args.yes:
        if input("Proceed? [y/N] ").strip().lower() not in ("y", "yes"):
            print("Aborted."); return
    asyncio.run(run(args))


if __name__ == "__main__":
    main()
