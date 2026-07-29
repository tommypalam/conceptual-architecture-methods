"""
phase0b_scorer.py — Phase 0b pass/fail evaluation (spec §2.1.4 pass criterion).

Single Responsibility: this block only scores. It consumes an iterable of record
dicts (from any RecordSink, or any source) and never reads the filesystem
itself — Dependency Inversion, so the same scorer works over JsonFileSink,
MemorySink, or a hand-built list in a test.

Pass criterion (§2.1.4): for each (condition, problem) cell, the Wilson 95% CI
on the proportion of one binary option must contain 50%. Phase 0b passes iff all
eighteen cells pass. Reports each failing cell's lean for the §2.1.5 triage.

The only contract with the runner is the record shape: fields
`condition_id`, `problem_id`, `parse_status`, `parsed_decision`.
"""

from __future__ import annotations

from collections import defaultdict
from typing import Iterable

from .scoring import wilson_ci

CONDITIONS = ("null_a", "null_b", "null_c")


def score_phase0b(records: Iterable[dict]) -> dict:
    """Aggregate records into the 18-cell pass/fail table."""
    cells: dict[str, dict[str, dict]] = defaultdict(lambda: defaultdict(
        lambda: {"counts": defaultdict(int), "n_ok": 0, "parse_fail": 0,
                 "refusal": 0, "failed_api": 0, "n_records": 0, "order": None}))

    for rec in records:
        cond, pid = rec.get("condition_id"), rec.get("problem_id")
        if cond is None or pid is None:
            continue
        cell = cells[cond][pid]
        cell["n_records"] += 1
        status = rec.get("parse_status")
        # A bare-label response ("APPROVE" with no "DECISION:" prefix) parses as
        # `ambiguous` (single recovered label), not `ok`. Both are valid
        # decisions; only refusals / api failures / true parse failures are bad.
        if status in ("ok", "ambiguous") and rec.get("parsed_decision"):
            cell["counts"][rec["parsed_decision"]] += 1
            cell["n_ok"] += 1
            if rec.get("labels") and cell["order"] is None:
                cell["order"] = list(rec["labels"])
        elif status == "refusal":
            cell["refusal"] += 1
        elif status == "failed_api":
            cell["failed_api"] += 1
        else:
            cell["parse_fail"] += 1

    out: dict = {"phase": "phase0b_harness_neutral", "cells": {}, "n_cells": 0,
                 "n_pass": 0, "failures": []}
    n_cells = n_pass = 0
    for cond in sorted(cells):
        out["cells"][cond] = {}
        for pid, cell in sorted(cells[cond].items()):
            n_cells += 1
            # Anchor the rate to a stable option: the first declared label if
            # captured, else alphabetical fallback (back-compat with old records
            # that lack a `labels` field).
            order = cell["order"] or sorted(cell["counts"])
            n_ok = cell["n_ok"]
            entry = {"n_records": cell["n_records"], "n_ok": n_ok,
                     "parse_fail": cell["parse_fail"], "refusal": cell["refusal"],
                     "failed_api": cell["failed_api"], "counts": dict(cell["counts"])}
            if order and n_ok:
                first = order[0]
                k = cell["counts"].get(first, 0)
                lo, hi = wilson_ci(k, n_ok)
                rate = k / n_ok
                contains_50 = lo <= 0.5 <= hi
                other = order[1] if len(order) > 1 else "other"
                entry.update({
                    "rate_label": first, "rate": round(rate, 4),
                    "wilson_95": [round(lo, 4), round(hi, 4)],
                    "contains_50pct": contains_50,
                    "lean": ("balanced" if contains_50
                             else (f"toward {first}" if rate > 0.5 else f"toward {other}")),
                    "verdict": "PASS" if contains_50 else "FAIL"})
                if contains_50:
                    n_pass += 1
                else:
                    out["failures"].append({"condition": cond, "problem": pid,
                                            "rate": round(rate, 4),
                                            "wilson_95": [round(lo, 4), round(hi, 4)],
                                            "lean": entry["lean"]})
            else:
                entry["verdict"] = "INCOMPLETE"
                out["failures"].append({"condition": cond, "problem": pid,
                                        "reason": "no parseable decisions"})
            out["cells"][cond][pid] = entry

    out["n_cells"] = n_cells
    out["n_pass"] = n_pass
    out["full_grid"] = (n_cells == 18)
    # Judge only the cells actually present. The full 18/18 Phase 0b gate is a
    # separate, explicit statement so a deliberate partial probe is never
    # mislabelled a failure.
    all_present_pass = (n_cells > 0 and n_pass == n_cells)
    if n_cells == 0:
        out["overall"] = "NO DATA (no records found)"
    elif n_cells < 18:
        verdict = "all balanced" if all_present_pass else f"{n_pass}/{n_cells} balanced"
        out["overall"] = (f"PARTIAL RUN - {n_pass}/{n_cells} cells present pass "
                          f"({verdict}); full Phase 0b needs all 18 cells")
    else:
        out["overall"] = ("PASS (18/18 cells balanced)" if all_present_pass
                          else f"FAIL ({n_pass}/18 cells balanced)")
    return out
