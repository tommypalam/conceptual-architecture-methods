"""
ablation_scorer.py — score framing-ablation records into a variant × problem table.

Reads ablation records (any RecordSink) and, per (framing_label, problem),
computes the split, the rate of the first label, the Wilson CI, whether it
brackets 50%, and the absolute distance |rate - 0.5| (how far from balanced).

The point is comparison against the `canonical` control: an element whose
ablation pulls a problem's rate toward 0.5 is a cause of the collapse.
"""

from __future__ import annotations

from collections import defaultdict
from typing import Iterable

from .scoring import wilson_ci


def score_ablation(records: Iterable[dict]) -> dict:
    cells: dict[str, dict[str, dict]] = defaultdict(lambda: defaultdict(
        lambda: {"counts": defaultdict(int), "n_ok": 0, "bad": 0, "order": None}))
    for rec in records:
        label, pid = rec.get("framing_label"), rec.get("problem_id")
        if label is None or pid is None:
            continue
        cell = cells[label][pid]
        # A bare-label response ("APPROVE" with no "DECISION:" prefix) parses as
        # `ambiguous` (a single recovered label), not `ok`. Both are valid
        # decisions here; only genuine non-decisions (fail/refusal/api) are bad.
        if rec.get("parse_status") in ("ok", "ambiguous") and rec.get("parsed_decision"):
            cell["counts"][rec["parsed_decision"]] += 1
            cell["n_ok"] += 1
            # Remember declared label order so the rate anchors to a stable
            # option even when a cell only ever emits one decision value.
            if rec.get("labels") and "order" not in cell:
                cell["order"] = list(rec["labels"])
        else:
            cell["bad"] += 1

    out: dict = {"phase": "phase0b_ablation", "variants": {}}
    for label in sorted(cells):
        out["variants"][label] = {}
        for pid, cell in sorted(cells[label].items()):
            n_ok = cell["n_ok"]
            entry = {"n_ok": n_ok, "bad": cell["bad"], "counts": dict(cell["counts"])}
            # Anchor the rate to a stable option: the first declared label if we
            # captured it, else the alphabetical fallback (back-compat).
            order = cell["order"] or sorted(cell["counts"])
            if order and n_ok:
                first = order[0]
                k = cell["counts"].get(first, 0)
                lo, hi = wilson_ci(k, n_ok)
                rate = k / n_ok
                entry.update({"rate_label": first, "rate": round(rate, 4),
                              "wilson_95": [round(lo, 4), round(hi, 4)],
                              "contains_50pct": lo <= 0.5 <= hi,
                              "dist_from_50": round(abs(rate - 0.5), 4)})
            out["variants"][label][pid] = entry
    return out


def format_table(summary: dict) -> str:
    """Variant × problem grid of dist-from-50 (lower = more balanced), with a
    per-variant mean distance so the best framing is obvious at a glance."""
    variants = summary.get("variants", {})
    if not variants:
        return "(no ablation records)"
    problems = sorted({p for v in variants.values() for p in v})
    lines = []
    header = "variant".ljust(18) + "".join(p.rjust(9) for p in problems) + "   mean"
    lines.append(header)
    lines.append("-" * len(header))
    for label in sorted(variants):
        row = label.ljust(18)
        dists = []
        for p in problems:
            c = variants[label].get(p, {})
            if "dist_from_50" in c:
                d = c["dist_from_50"]
                dists.append(d)
                mark = "*" if c.get("contains_50pct") else " "
                row += f"{d:.2f}{mark}".rjust(9)
            else:
                row += "-".rjust(9)
        mean = sum(dists) / len(dists) if dists else float("nan")
        row += f"   {mean:.3f}"
        lines.append(row)
    lines.append("-" * len(header))
    lines.append("cells: distance |rate-0.5| (0.00 = perfectly balanced); "
                 "* = Wilson 95% CI contains 50%.")
    lines.append("Lower is better. Compare each ablation row against 'canonical'.")
    return "\n".join(lines)
