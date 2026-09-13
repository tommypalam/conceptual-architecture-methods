"""Offline Phase 3 specification accounting. This module cannot dispatch calls.

Counts are nominal one-call-per-agent slots, not a frozen experimental schedule:
trajectory/trial units and role/control conditions still require review.
"""
from __future__ import annotations

import argparse
from collections import Counter
from decimal import Decimal
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "experiments/phase3_preparation_20260913"
BENCHMARKS = ("milgram", "asch", "ultimatum", "bystander", "reactance")
MODULATORS = {
    "milgram": ("peer_rebellion", "experimenter_absent", "diffused_responsibility"),
    "asch": ("unanimity_break", "private_response", "group_size_1", "group_size_2",
             "group_size_3", "group_size_5"),
}
AXES = ("Freedom", "Justice", "Authority", "Care", "Loyalty")


def context_descriptor(axes):
    """Validate a benchmark context without coercing NEUTRAL to a binary bit."""
    if set(axes) != set(AXES):
        raise ValueError("Exactly the five named context axes are required")
    for value in axes.values():
        if not (type(value) is int and value in (0, 1)) and value != "NEUTRAL":
            raise ValueError("Context values must be integer 0/1 or explicit NEUTRAL")
    return "/".join(str(axes[a]) for a in AXES)


def cells(d_agents_per_matrix=100):
    if type(d_agents_per_matrix) is not int or d_agents_per_matrix < 1:
        raise ValueError("D requires a positive integer sample per matrix")
    result = []

    def add(stage, benchmark, variant, context, regime, n, condition="base"):
        result.append(dict(stage=stage, benchmark=benchmark, variant=variant,
                           context=context, regime=regime, condition=condition, n=n))

    for benchmark in BENCHMARKS:
        for variant in ("canonical", "decanonised"):
            add("recognition", benchmark, variant, "none", "none", 50)
            for context in ("high_rate", "low_rate"):
                add("primary", benchmark, variant, context, "A", 200)
        for condition in MODULATORS.get(benchmark, ()):
            add("modulator", benchmark, "decanonised", "high_rate", "A", 100, condition)
        for context in ("high_rate", "low_rate"):
            # A overlaps the primary's first 100 matched profiles; do not bill it twice.
            for regime in ("B", "C", "t4", "t8", "t16"):
                add("sensitivity", benchmark, "decanonised", context, regime, 100)
            for matrix in range(100):
                add("sensitivity", benchmark, "decanonised", context,
                    f"D{matrix:03}", d_agents_per_matrix)
    return result


def slot_ids(rows):
    for row in rows:
        base = "/".join(str(row[k]) for k in
                        ("stage", "benchmark", "variant", "context", "regime", "condition"))
        for participant in range(1, row["n"] + 1):
            yield f"{base}/{participant:04}"


def inventory(rows):
    ids = list(slot_ids(rows))
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate nominal slots")
    counts = Counter()
    for row in rows:
        counts[row["stage"]] += row["n"]
    return {"nominal_calls": len(ids), "counts": dict(counts),
            "nominal_slot_sha256": hashlib.sha256("\n".join(ids).encode()).hexdigest()}


def budget_scenario(benchmark_calls, input_tokens=1500, output_tokens=150):
    """Illustration at verified standard global rates, never a spend reservation."""
    if min(benchmark_calls, input_tokens, output_tokens) < 0:
        raise ValueError("Negative budget quantity")
    total = (Decimal(input_tokens) * Decimal("0.75") +
             Decimal(output_tokens) * Decimal("4.50")) / Decimal(1_000_000)
    return str((Decimal(benchmark_calls) * total * Decimal("1.10")).quantize(Decimal("0.000001")))


def report():
    registry = json.loads((PACKAGE / "benchmark_registry.json").read_text(encoding="utf-8"))
    if tuple(b["id"] for b in registry["benchmarks"]) != BENCHMARKS:
        raise ValueError("Benchmark omission or unexpected benchmark order")
    for benchmark in registry["benchmarks"]:
        context_descriptor(benchmark["high"])
        context_descriptor(benchmark["low"])
    scenarios = {}
    for n in (1, 10, 100):
        summary = inventory(cells(n))
        benchmark_calls = summary["nominal_calls"] - summary["counts"]["recognition"]
        scenarios[str(n)] = {
            **summary, "d_profiles_per_matrix": n,
            "illustrative_benchmark_usd_1500_in_150_out_plus_10pct": budget_scenario(benchmark_calls),
            "illustrative_benchmark_usd_1500_in_600_out_plus_10pct": budget_scenario(benchmark_calls, output_tokens=600),
        }
    return {
        "status": "OFFLINE_SPEC_AUDIT_NOT_A_COLLECTION_FREEZE", "ready_to_collect": False,
        "new_api_calls": 0, "benchmarks": list(BENCHMARKS), "modulator_cells": 9,
        "scenarios": scenarios,
        "budget": {"hard_cap_usd": "100", "prior_phase2_conservative_usd": "22.906073025",
                   "remaining_accounting_room_usd": str(Decimal("100") - Decimal("22.906073025")),
                   "provider_balance_verified": False,
                   "price_source": "https://developers.openai.com/api/docs/models/gpt-5.4-mini",
                   "price_checked": "2026-09-13",
                   "exclusions": ["separate judge model", "variant generation/revisions", "rater calls",
                                  "additional trials/roles/control conditions", "longer context growth"],
                   "warning": "Token assumptions are illustrations, not measured prompts or hard upper bounds."},
        "release_issues": [
            "Benchmark procedure, stimuli, units and reference targets are not frozen",
            "Canonical scenarios are not approved; no independently generated/reviewed variants exist",
            "Neutral-axis context text and high/low direction require specification",
            "Recognition model, two raters and threshold adjudication workflow not completed",
            "D sample-per-matrix interpretation conflicts with rough call budget",
            "Primary roles/control conditions and sensitivity replication may add calls",
            "Distinct-model pricing and all-call reservation budget not frozen",
            "A paid collector and its immutable recording/analysis contract are not released",
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="Write offline audit JSON to this path")
    args = parser.parse_args()
    data = report()
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(data, indent=2))


if __name__ == "__main__":
    main()
