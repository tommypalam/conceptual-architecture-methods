"""
run_phase0c.py — Phase 0c locked holdout (spec §2.2), naked delivery.

Phase 0c is the multi-iteration false-pass check (spec §11.5): freeze the
accepted prompts, run a FRESH, larger, no-edit sample, and confirm the ~50/50
calibration HOLDS rather than being iteration luck. It validates the DILEMMAS,
not the harness.

Given the Phase 0b finding (the agent-framing harness is non-neutral on this
model — PHASE0B_RESULT_2026-07-29.md), the only condition that validates the
dilemma calibration is the VALIDATED-NEUTRAL naked delivery (dilemma + bare
"Reply with only: X or Y", no system message). Spec §2.2.1 names null_b, but that
condition provably collapses S2/C2/C3 and would merely re-measure the harness
effect, not the dilemmas. This deviation is documented; the naked holdout is the
coherent 0c given the state of the world.

Protocol:
  - Prompt freeze: SHA-256 hash-lock the six recalibrated question files into
    experiments/phase0c_locked_holdout/frozen_prompts/manifest.json (spec §2.2.1).
  - Sample size: N = 1000 per problem (spec §2.2.1). Six problems = 6,000 calls.
  - No-edit rule: the manifest hashes are re-verified before scoring; any change
    to a frozen file aborts (spec §2.2.1 lock invalidation).
  - Pass tiers (spec §2.2.2): contains 50% = validated; CI within 45-55 =
    modest shift (document); CI outside 40-60 = substantial (retire).

SAFETY: default provider mock. Real runs print cost + confirm.

Examples
--------
python code/run_phase0c.py --freeze          # hash-lock only, no calls
python code/run_phase0c.py --provider openai --n 1000
python code/run_phase0c.py --score-only
"""

from __future__ import annotations

import argparse
import asyncio
import hashlib
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
from engine.phase0b_runner import PROBLEMS
from engine.questions import PHASE0B_QUESTIONS, load_dilemma_body
from engine.record_sink import JsonFileSink
from engine.scoring import wilson_ci

REPO_ROOT = Path(__file__).resolve().parent.parent
HOLDOUT_DIR = REPO_ROOT / "experiments" / "phase0c_locked_holdout"
FROZEN_DIR = HOLDOUT_DIR / "frozen_prompts"
MANIFEST = FROZEN_DIR / "manifest.json"
RESULTS_DIR = HOLDOUT_DIR / "results"
COST_PER_CALL_USD = 0.001

LABELS = {p.short_id: p.labels for p in PROBLEMS}
QFILE = {p.short_id: p.question_file for p in PROBLEMS}
PIDS = [p.short_id for p in PROBLEMS]


def load_seed() -> int:
    path = REPO_ROOT / "config" / "seeds.json"
    if path.exists():
        # A distinct 0c seed so the holdout sample is INDEPENDENT of 0b draws.
        return json.loads(path.read_text(encoding="utf-8"))["seeds"].get(
            "phase0c_locked_holdout", 20260729)
    return 20260729


def file_hash(pid: str) -> str:
    raw = (PHASE0B_QUESTIONS / QFILE[pid]).read_bytes()
    return hashlib.sha256(raw).hexdigest()


def freeze(timestamp: str) -> dict:
    """Hash-lock the six recalibrated question files (spec §2.2.1)."""
    FROZEN_DIR.mkdir(parents=True, exist_ok=True)
    manifest = {"phase": "phase0c_locked_holdout", "frozen_at": timestamp,
                "source_dir": str(PHASE0B_QUESTIONS.relative_to(REPO_ROOT)),
                "delivery": "naked (no system message; 'Reply with only: X or Y')",
                "hashes": {pid: file_hash(pid) for pid in PIDS}}
    MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest


def verify_lock() -> None:
    """Abort if any frozen file changed since freeze (spec §2.2.1)."""
    if not MANIFEST.exists():
        raise SystemExit("No manifest. Run --freeze first (with a timestamp).")
    locked = json.loads(MANIFEST.read_text(encoding="utf-8"))["hashes"]
    drift = [pid for pid in PIDS if file_hash(pid) != locked.get(pid)]
    if drift:
        raise SystemExit(f"LOCK INVALIDATED — frozen prompt(s) changed: {drift}. "
                         "Per spec §2.2.1, Phase 0c must restart with a new freeze.")


def tier(rate: float, lo: float, hi: float) -> str:
    """Spec §2.2.2 pass tiers."""
    if lo <= 0.5 <= hi:
        return "VALIDATED (CI contains 50%)"
    if 0.45 <= rate <= 0.55:
        return "MODEST SHIFT (document baseline)"
    if 0.40 <= rate <= 0.60:
        return "MODEST-OUTER (45-55 excl; within 40-60)"
    return "SUBSTANTIAL (retire; outside 40-60)"


def make_client(provider, model, concurrency):
    return (MockClient(concurrency=concurrency) if provider == "mock"
            else LLMClient(model=model, concurrency=concurrency))


async def run(args):
    verify_lock()
    client = make_client(args.provider, args.model, args.concurrency)
    sink = JsonFileSink(RESULTS_DIR)
    results = []
    for pid in PIDS:
        body = load_dilemma_body(QFILE[pid], PHASE0B_QUESTIONS)
        r = await recalibrate.calibrate_candidate(
            client=client, sink=sink, candidate_id=pid, dilemma_body=body,
            labels=LABELS[pid], n=args.n, root_seed=load_seed())
        results.append((pid, r))
    score(results)


def score_only():
    verify_lock()
    sink = JsonFileSink(RESULTS_DIR)
    recs = list(sink.read_all())
    from collections import defaultdict, Counter
    by = defaultdict(Counter)
    for rec in recs:
        pid = rec.get("candidate_id")
        if rec.get("parse_status") in ("ok", "ambiguous") and rec.get("parsed_decision"):
            by[pid][rec["parsed_decision"]] += 1
    results = []
    for pid in PIDS:
        c = by[pid]; l0 = LABELS[pid][0]; k = c.get(l0, 0); n = sum(c.values())
        lo, hi = wilson_ci(k, n) if n else (0.0, 0.0)
        rate = k / n if n else 0.0
        results.append((pid, {"counts": dict(c), "n_ok": n, "rate": rate,
                              "wilson_95": [lo, hi], "rate_label": l0}))
    score(results)


def score(results):
    print("\n" + "=" * 70)
    print("PHASE 0c — LOCKED HOLDOUT (naked delivery, frozen recalibrated set)")
    print("spec §2.2.2 tiers")
    print("=" * 70)
    print(f"{'prob':5}{'split':30}{'rate':7}{'CI':16}{'tier'}")
    print("-" * 70)
    for pid, r in results:
        rate = r["rate"]; lo, hi = r["wilson_95"]
        split = ", ".join(f"{k} {v}" for k, v in sorted(r["counts"].items())) or "-"
        t = tier(rate, lo, hi)
        print(f"{pid:5}{split:30}{rate:<7.2f}[{lo:.2f},{hi:.2f}]   {t}")
    print("-" * 70)


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--provider", choices=["mock", "openai", "anthropic", "google"],
                   default="mock")
    p.add_argument("--model", default="gpt-5.4-mini")
    p.add_argument("--n", type=int, default=1000)
    p.add_argument("--concurrency", type=int, default=5)
    p.add_argument("--freeze", action="store_true",
                   help="Hash-lock the recalibrated question files and exit.")
    p.add_argument("--freeze-timestamp", default=None,
                   help="Timestamp string to record in the manifest (required with "
                        "--freeze; e.g. 2026-07-29T00:00:00Z).")
    p.add_argument("--score-only", action="store_true")
    p.add_argument("--yes", action="store_true")
    args = p.parse_args()

    if args.freeze:
        if not args.freeze_timestamp:
            p.error("--freeze requires --freeze-timestamp")
        m = freeze(args.freeze_timestamp)
        print(f"Locked {len(m['hashes'])} prompts -> {MANIFEST}")
        for pid, h in m["hashes"].items():
            print(f"  {pid}: {h[:16]}...")
        return

    if args.score_only:
        score_only(); return

    n_calls = args.n * len(PIDS)
    print(f"Planned: {n_calls} calls (6 problems x N={args.n}) | "
          f"est ~${n_calls*COST_PER_CALL_USD:,.2f} | provider {args.provider}")
    if args.provider != "mock" and not args.yes:
        if input("Proceed? [y/N] ").strip().lower() not in ("y", "yes"):
            print("Aborted."); return
    asyncio.run(run(args))


if __name__ == "__main__":
    main()
