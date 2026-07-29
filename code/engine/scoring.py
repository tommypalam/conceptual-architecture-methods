"""
scoring.py — bare-bones aggregation of engine output records.

Reads the write-once JSON records produced by simple_runner and complex_runner
and rolls them up to the per-configuration decision rates + Wilson 95% CIs that
Phase 5 consumes (spec §7.5.3 Wilson intervals; §9.2 descriptive rates). This is
deliberately minimal: point estimates, counts, parse-integrity, and Wilson CIs.
The mixed-effects model, bootstrap, and sensitivity regimes (spec §9.1, §9.2)
are later work; this just turns raw records into a tidy scored summary.

No dependencies beyond the standard library + math.
"""

from __future__ import annotations

import json
import math
from collections import defaultdict
from pathlib import Path


def wilson_ci(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    """Wilson score interval for a binomial proportion (spec §7.5.3)."""
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    denom = 1 + z * z / n
    centre = p + z * z / (2 * n)
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return ((centre - half) / denom, (centre + half) / denom)


def _iter_json(root: Path, pattern: str):
    for path in sorted(root.rglob(pattern)):
        try:
            yield path, json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue


# --------------------------------------------------------------------------- #
# Simple problems (spec §5): one record per (agent, config, problem)
# --------------------------------------------------------------------------- #

def score_simple(runs_root: Path) -> dict:
    """
    Aggregate simple-problem records to per-(problem, config) rates.
    Cell = {problem_id: {config_id: {label: count, ..., n_ok, parse_fail,
            refusal, rate_<first_label>, wilson_low, wilson_high}}}.
    """
    cells: dict[str, dict[str, dict]] = defaultdict(lambda: defaultdict(
        lambda: {"counts": defaultdict(int), "n_ok": 0, "parse_fail": 0,
                 "refusal": 0, "failed_api": 0, "n_records": 0}))
    for _, rec in _iter_json(runs_root, "agent_*.json"):
        pid, cid = rec.get("problem_id"), rec.get("configuration_id")
        if pid is None or cid is None:
            continue
        cell = cells[pid][cid]
        cell["n_records"] += 1
        status = rec.get("parse_status")
        if status == "ok":
            cell["counts"][rec["parsed_decision"]] += 1
            cell["n_ok"] += 1
        elif status == "refusal":
            cell["refusal"] += 1
        elif status == "failed_api":
            cell["failed_api"] += 1
        else:
            cell["parse_fail"] += 1

    out: dict = {"phase": "phase2_simple", "problems": {}}
    for pid, byconfig in sorted(cells.items()):
        out["problems"][pid] = {}
        for cid, cell in sorted(byconfig.items()):
            labels = sorted(cell["counts"])
            n_ok = cell["n_ok"]
            summary = {"n_records": cell["n_records"], "n_ok": n_ok,
                       "parse_fail": cell["parse_fail"], "refusal": cell["refusal"],
                       "failed_api": cell["failed_api"],
                       "counts": dict(cell["counts"])}
            if labels and n_ok:
                first = labels[0]
                k = cell["counts"][first]
                lo, hi = wilson_ci(k, n_ok)
                summary["rate_label"] = first
                summary["rate"] = round(k / n_ok, 4)
                summary["wilson_95"] = [round(lo, 4), round(hi, 4)]
            out["problems"][pid][cid] = summary
    return out


# --------------------------------------------------------------------------- #
# Complex problems (spec §6): one record per run
# --------------------------------------------------------------------------- #

def score_complex(runs_root: Path) -> dict:
    """
    Aggregate complex-problem run records to per-(problem, config) outcome rates.
    Uses the run's final_outcome. Bridge runs (bridge_calibration=True) are
    tallied separately as the no-architecture baseline (spec §6.5).
    """
    param = defaultdict(lambda: defaultdict(lambda: {"runs": 0, "outcomes": defaultdict(int),
                                                     "leakage_runs": 0, "lean_flips": 0}))
    bridge = defaultdict(lambda: {"runs": 0, "outcomes": defaultdict(int)})

    for _, rec in _iter_json(runs_root, "run_*.json"):
        pid = rec.get("problem_id")
        outcome = rec.get("final_outcome", {})
        key = _outcome_key(pid, outcome)
        if rec.get("bridge_calibration"):
            b = bridge[pid]
            b["runs"] += 1
            b["outcomes"][key] += 1
            continue
        cid = rec.get("configuration_id")
        cell = param[pid][cid]
        cell["runs"] += 1
        cell["outcomes"][key] += 1
        if any("leakage_violation" in e for e in rec.get("leakage_log", [])):
            cell["leakage_runs"] += 1
        cell["lean_flips"] += rec.get("consistency_audit", {}).get("total_lean_flips", 0)

    def finalise(d):
        out = {}
        for pid, byc in sorted(d.items()):
            out[pid] = {}
            for cid, cell in sorted(byc.items()):
                runs = cell["runs"]
                entry = {"runs": runs, "outcomes": dict(cell["outcomes"])}
                if "leakage_runs" in cell:
                    entry["leakage_runs"] = cell["leakage_runs"]
                    entry["mean_lean_flips"] = round(cell["lean_flips"] / runs, 3) if runs else 0
                # rate + Wilson CI on the modal outcome
                if runs and cell["outcomes"]:
                    top = max(cell["outcomes"], key=cell["outcomes"].get)
                    lo, hi = wilson_ci(cell["outcomes"][top], runs)
                    entry["modal_outcome"] = top
                    entry["modal_rate"] = round(cell["outcomes"][top] / runs, 4)
                    entry["wilson_95"] = [round(lo, 4), round(hi, 4)]
                out[pid][cid] = entry
        return out

    return {"phase": "phase2_complex",
            "parameterised": finalise(param),
            "bridge": {pid: {"runs": b["runs"], "outcomes": dict(b["outcomes"])}
                       for pid, b in sorted(bridge.items())}}


def _outcome_key(pid: str, outcome: dict) -> str:
    """Reduce a run's final_outcome to a single categorical label per problem."""
    if pid == "C1":
        return str(outcome.get("final_selection"))
    if pid == "C2":
        return "APPROVED" if outcome.get("approved") else "REJECTED"
    if pid == "C3":
        return str(outcome.get("final_vote"))
    return "unknown"
