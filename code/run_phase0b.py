"""
run_phase0b.py — composition root for Phase 0b (harness-neutral baseline, spec §2.1).

The ONE place concrete blocks are wired together (a small DI container). Every
other module depends on interfaces; this file chooses the client, the
assemblers, and the sink.

Blocks:
  client      SupportsComplete   — MockClient (offline) | LLMClient (real)
  assemblers  {id: NullConditionAssembler}
  sink        RecordSink         — JsonFileSink | MemorySink

Running economically
--------------------
  --n N            calls per condition per problem (any size — start small)
  --sample-tag T   isolate this batch in its own folder, so exploratory runs at
                   different N (or after a prompt tweak) never reuse or clobber
                   each other. Untagged runs share the canonical directory and
                   RESUME: a later larger --n only pays for the additional calls.
  --conditions / --problems   run just one cell while iterating.
  --dry-run        assemble + print prompts; no API, nothing written, no cost.
  --yes            skip the cost confirmation (for scripted/non-interactive use).

SAFETY: default --provider mock is fully offline. A real run prints a cost
estimate and asks for confirmation before making any paid call.

Examples
--------
python code/run_phase0b.py --dry-run --conditions null_b --problems S1
python code/run_phase0b.py --provider openai --n 5 --conditions null_b --problems S1 --sample-tag probe
python code/run_phase0b.py --provider openai --n 50 --sample-tag pilot50
python code/run_phase0b.py --provider openai --n 500        # canonical, resumable
python code/run_phase0b.py --score-only --sample-tag pilot50
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from pathlib import Path

# Windows consoles default to cp1252 and crash on non-ASCII prints (—, ×, →).
# Force UTF-8 so any Unicode in output/records prints safely everywhere.
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

sys.path.insert(0, str(Path(__file__).resolve().parent))

from engine import phase0b, phase0b_runner, phase0b_scorer
from engine.llm_client import LLMClient, MockClient
from engine.prompt_assembly import build_simple_user_turn, load_template
from engine.questions import load_dilemma_body
from engine.record_sink import JsonFileSink

REPO_ROOT = Path(__file__).resolve().parent.parent
CONFIG_DIR = REPO_ROOT / "config"
REAL_DIR = REPO_ROOT / "experiments" / "phase0b_harness_neutral"
MOCK_DIR = REPO_ROOT / "experiments" / "_mock_phase0b"

# Rough per-call cost for the confirmation preview (Appendix B budgeting figure:
# ~1,500 input + 200 output tokens ≈ $0.001). Estimate only.
COST_PER_CALL_USD = 0.001


def load_seed(default: int = 20260601) -> int:
    path = CONFIG_DIR / "seeds.json"
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))["seeds"].get(
        "phase0b_harness_neutral", default)


def make_client(provider: str, model: str, concurrency: int):
    if provider == "mock":
        return MockClient(model="mock-model", concurrency=concurrency)
    return LLMClient(model=model, concurrency=concurrency)


def resolve_root(args) -> Path:
    """Where records live. --sample-tag isolates a batch; else canonical/mock."""
    base = MOCK_DIR if (args.provider == "mock" and not args.score_only) else REAL_DIR
    if args.runs_root is not None:
        return args.runs_root
    if args.sample_tag:
        return base.parent / f"{base.name}__{args.sample_tag}"
    return base


def selected_conditions(args):
    return args.conditions or list(phase0b.CONDITIONS)


def selected_problems(args):
    return args.problems or [pr.short_id for pr in phase0b_runner.PROBLEMS]


def selected_questions_dir(args):
    """Which locked question set to source dilemma bodies from."""
    from engine.questions import PHASE0_QUESTIONS, PHASE0B_QUESTIONS
    return PHASE0B_QUESTIONS if args.questions_set == "phase0b" else PHASE0_QUESTIONS


def do_dry_run(args):
    template = load_template()
    assemblers = phase0b.default_assemblers(sham_keep_glosses=not args.sham_bare)
    probs = [p for p in phase0b_runner.PROBLEMS if p.short_id in selected_problems(args)]
    seed = load_seed()
    from engine.delivery import DELIVERIES
    delivery = DELIVERIES[args.delivery]()
    for cond in selected_conditions(args):
        asm = assemblers[cond]
        for prob in probs:
            body = load_dilemma_body(prob.question_file, selected_questions_dir(args))
            user = build_simple_user_turn(body, prob.labels, bare_label=args.bare_label)
            sysp, prov = asm.build(template, seed=seed)
            print("=" * 74)
            print(f"CONDITION {cond}  PROBLEM {prob.short_id}  ({prov['detail']})")
            print(f"delivery: {delivery.delivery_id}")
            print("=" * 74)
            # Preview the ACTUAL messages the delivery will send (system_role vs
            # user_prefix change the shape), so the dry-run doesn't mislead.
            for msg in delivery.messages(sysp, user):
                print(f"[{msg.role.upper()}]\n{msg.content}\n")
    print("DRY RUN - no API calls, nothing written.")


def confirm_cost(args, sink, n_conditions, n_problems) -> bool:
    """Print a cost estimate for the calls NOT already recorded; ask to proceed."""
    total = args.n * n_conditions * n_problems
    already = sum(1 for _ in sink.read_all()) if hasattr(sink, "read_all") else 0
    to_run = max(0, total - already)                 # true delta, resume-aware
    est = to_run * COST_PER_CALL_USD
    print(f"\nPlanned: {total} calls  ({n_conditions} conditions x {n_problems} "
          f"problems x N={args.n})")
    if already:
        print(f"Already recorded here: {already} -> new calls to make: {to_run}")
    print(f"Provider: {args.provider} | model: {args.model}")
    print(f"Estimated cost of new calls: ~${est:,.2f} "
          f"(@ ${COST_PER_CALL_USD}/call, rough)")
    if args.provider == "mock":
        return True
    if args.yes:
        print("--yes given: proceeding without prompt.")
        return True
    reply = input("Proceed with the paid run? [y/N] ").strip().lower()
    return reply in ("y", "yes")


async def do_run(args, sink):
    from engine.delivery import DELIVERIES
    client = make_client(args.provider, args.model, args.concurrency)
    assemblers = phase0b.default_assemblers(sham_keep_glosses=not args.sham_bare)
    assemblers = {c: assemblers[c] for c in selected_conditions(args)}
    problems = tuple(p for p in phase0b_runner.PROBLEMS
                     if p.short_id in selected_problems(args))
    delivery = DELIVERIES[args.delivery]()
    await phase0b_runner.run_phase0b(
        client=client, assemblers=assemblers, sink=sink, delivery=delivery,
        questions_dir=selected_questions_dir(args),
        bare_label=args.bare_label, max_tokens=args.max_tokens,
        root_seed=load_seed(), n=args.n, problems=problems)


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--provider", choices=["mock", "openai", "anthropic", "google"],
                   default="mock", help="mock = offline (default).")
    p.add_argument("--model", default="gpt-5.4-mini")
    p.add_argument("--n", type=int, default=500, help="Calls per condition per problem.")
    p.add_argument("--concurrency", type=int, default=5,
                   help="Kept low (5) by default: the 200k TPM cap throttles "
                        "higher concurrency into 429s.")
    p.add_argument("--conditions", nargs="+", choices=phase0b.CONDITIONS, default=None)
    p.add_argument("--problems", nargs="+",
                   choices=[pr.short_id for pr in phase0b_runner.PROBLEMS], default=None)
    p.add_argument("--sample-tag", default=None,
                   help="Isolate this batch in its own folder (for iterating).")
    # --- Defaults track the SPEC (§2.1.4): system message + DECISION/REASONING - #
    # The spec's null_a is the full Phase-2 system prompt (preamble + task, empty
    # content slots) delivered as a system message, with DECISION + REASONING
    # output. That is the faithful baseline. The 2026-07-28 investigation found
    # the DECISION/REASONING format and system-message delivery can also collapse
    # some dilemmas; those are opt-in deviations (--bare-label, --delivery
    # user_prefix) tried only if a wording fix alone does not reach 18/18.
    p.add_argument("--delivery", choices=["system_role", "user_prefix"],
                   default="system_role",
                   help="Where the harness goes. DEFAULT system_role (spec-faithful "
                        "system message). user_prefix = no system message (deviation).")
    p.add_argument("--bare-label", dest="bare_label", action="store_true",
                   help="Deviation: bare-label output ('Reply with only: X or Y') "
                        "instead of the spec's DECISION/REASONING schema.")
    p.set_defaults(bare_label=False)
    p.add_argument("--max-tokens", type=int, default=600,
                   help="Per-call max tokens. DEFAULT 600 (fits DECISION+REASONING); "
                        "use ~30 with --bare-label.")
    p.add_argument("--questions-set", choices=["phase0a", "phase0b"],
                   default="phase0b",
                   help="Which locked question set to use: phase0b = the "
                        "recalibrated 2026-07-28 set (default, current model); "
                        "phase0a = the frozen original May-2026 set.")
    p.add_argument("--sham-bare", action="store_true",
                   help="null_c uses bare sham names (no endpoint glosses).")
    p.add_argument("--dry-run", action="store_true",
                   help="Assemble + print prompts; no API, nothing written.")
    p.add_argument("--yes", action="store_true", help="Skip the cost confirmation.")
    p.add_argument("--score-only", action="store_true")
    p.add_argument("--runs-root", type=Path, default=None)
    p.add_argument("--out", type=Path, help="Write scored JSON summary here.")
    args = p.parse_args()

    if args.dry_run:
        do_dry_run(args)
        return

    root = resolve_root(args)
    sink = JsonFileSink(root)
    print(f"records dir: {root}")

    if not args.score_only:
        if not confirm_cost(args, sink, len(selected_conditions(args)),
                            len(selected_problems(args))):
            print("Aborted - no calls made.")
            return
        asyncio.run(do_run(args, sink))

    summary = phase0b_scorer.score_phase0b(sink.read_all())
    if args.out:
        args.out.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n",
                            encoding="utf-8")
        print(f"wrote {args.out}")
    print_summary(summary)


def print_summary(summary: dict) -> None:
    """Readable per-cell table: split, Wilson CI, and whether it brackets 50%."""
    print("\n" + "=" * 62)
    print("PHASE 0b RESULTS  (Wilson 95% CI must contain 50% to be balanced)")
    print("=" * 62)
    header = f"{'cond':<7} {'prob':<5} {'n_ok':>5}  {'split':<22} {'CI(95%)':<18} verdict"
    print(header)
    print("-" * len(header))
    for cond, byprob in summary.get("cells", {}).items():
        for pid, c in byprob.items():
            n_ok = c.get("n_ok", 0)
            counts = c.get("counts", {})
            split = ", ".join(f"{k} {v}" for k, v in sorted(counts.items())) or "-"
            if "rate" in c:
                lo, hi = c["wilson_95"]
                ci = f"[{lo:.2f}, {hi:.2f}]"
                verdict = c["verdict"]
                if verdict != "PASS":
                    verdict += f"  (lean {c.get('lean','?')})"
            else:
                ci, verdict = "-", c.get("verdict", "INCOMPLETE")
            bad = sum([c.get("parse_fail", 0), c.get("failed_api", 0), c.get("refusal", 0)])
            note = f"  [{bad} unparsed/api/refusal]" if bad else ""
            print(f"{cond:<7} {pid:<5} {n_ok:>5}  {split:<22} {ci:<18} {verdict}{note}")
    print("-" * len(header))
    print(f"OVERALL: {summary['overall']}")


if __name__ == "__main__":
    main()
