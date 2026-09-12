"""Offline checks of a proposed Phase 2 configuration design; never dispatches calls.

The repair is a proposal, not a replacement for config/configurations.json.
It exhausts single non-anchor substitutions and requires full additive rank.
Within that constraint it maximises entropy of pairwise Hamming distances,
then mean distance, then uses lexicographic order. No behavioural data is read.
"""
from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
from itertools import combinations, product
import json
import math
from pathlib import Path

AXES = ("Freedom", "Justice", "Authority", "Care", "Loyalty")
ANCHORS = {"00100", "11011"}


def matrix_rank(rows: list[list[int]]) -> int:
    matrix = [[Fraction(x) for x in row] for row in rows]
    rank = 0
    for col in range(len(matrix[0])):
        pivot = next((r for r in range(rank, len(matrix)) if matrix[r][col]), None)
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        divisor = matrix[rank][col]
        matrix[rank] = [x / divisor for x in matrix[rank]]
        for r in range(rank + 1, len(matrix)):
            factor = matrix[r][col]
            matrix[r] = [a - factor * b for a, b in zip(matrix[r], matrix[rank])]
        rank += 1
        if rank == len(matrix):
            break
    return rank


def inspect_design(codes: list[str]) -> dict:
    if not codes or any(len(c) != 5 or set(c) - {"0", "1"} for c in codes):
        raise ValueError("Expected nonempty list of five-bit configuration codes")
    if len(set(codes)) != len(codes):
        raise ValueError("Duplicate configuration codes")
    rows = [[int(bit) for bit in code] for code in codes]
    coverage = {axis: {str(level): sum(row[i] == level for row in rows)
                      for level in (0, 1)} for i, axis in enumerate(AXES)}
    distances = Counter(sum(a != b for a, b in zip(x, y))
                        for x, y in combinations(codes, 2))
    pairs = sum(distances.values())
    entropy = -sum((n / pairs) * math.log(n / pairs) for n in distances.values()) if pairs else 0
    aliases = []
    for i, j in combinations(range(5), 2):
        if all(row[i] == row[j] for row in rows):
            aliases.append(f"{AXES[i]} = {AXES[j]}")
        elif all(row[i] == 1 - row[j] for row in rows):
            aliases.append(f"{AXES[i]} = 1 - {AXES[j]}")
    rank = matrix_rank([[1] + row for row in rows])
    return {
        "codes": codes, "row_count": len(rows), "columns": ["intercept", *AXES],
        "missing_values": 0, "coverage": coverage,
        "anchors_present": ANCHORS <= set(codes),
        "coverage_pass": all(n >= 3 for levels in coverage.values() for n in levels.values()),
        "size_pass": 8 <= len(codes) <= 12,
        "additive_rank": rank, "required_rank": 6, "full_additive_rank": rank == 6,
        "exact_axis_aliases": aliases,
        "hamming_histogram": dict(sorted(distances.items())),
        "hamming_entropy_nats": entropy,
        "mean_hamming_distance": sum(d * n for d, n in distances.items()) / pairs if pairs else 0,
    }


def propose_single_replacement(codes: list[str]) -> dict | None:
    original = inspect_design(codes)
    if original["full_additive_rank"] and original["coverage_pass"] and original["anchors_present"]:
        return None
    pool = sorted("".join(bits) for bits in product("01", repeat=5) if "".join(bits) not in codes)
    candidates = []
    for removed in sorted(set(codes) - ANCHORS):
        for added in pool:
            proposal = inspect_design([added if c == removed else c for c in codes])
            if all(proposal[k] for k in ("full_additive_rank", "coverage_pass", "anchors_present", "size_pass")):
                candidates.append({"removed": removed, "added": added, "design": proposal})
    if not candidates:
        raise ValueError("No valid single replacement; a larger reviewed design change is needed")
    candidates.sort(key=lambda p: (-p["design"]["hamming_entropy_nats"],
                                   -p["design"]["mean_hamming_distance"],
                                   p["removed"], p["added"]))
    return {**candidates[0], "admissible_single_replacements": len(candidates),
            "status": "PROPOSAL_ONLY_REQUIRES_REVIEW",
            "global_entropy_optimality_claimed": False}


def call_budget(n: int = 200, configs: int = 10, problems: int = 3) -> dict:
    if min(n, configs, problems) < 1:
        raise ValueError("Positive design dimensions required")
    per_arm = n * configs * problems
    group_calls = 10 * (2 * 2 + 1) * (25 + 30 + 24)
    return {"profiles": n, "configurations": configs, "problems": problems,
            "encoded_calls": per_arm, "unencoded_calls": per_arm,
            "core_calls": 2 * per_arm,
            "group_calls_maximum": group_calls,
            "group_design": "10 groups per task; 2 anchors x E/U plus neutral bridge; C1/C2/C3 retained",
            "default_total_calls_maximum": 2 * per_arm + group_calls,
            "optional_anchor_postfilter_calls": n * len(ANCHORS) * problems,
            "core_plus_anchor_postfilter_calls": 2 * per_arm + n * len(ANCHORS) * problems,
            "default_plus_postfilter_calls_maximum": 2 * per_arm + group_calls + n * len(ANCHORS) * problems,
            "scope": "Excludes transfer, benchmarks, coding, human data and retries; these need separate allocations",
            "user_hard_cap_usd": 100, "proposed_operational_ceiling_usd": 90,
            "dollar_estimate": None, "note": "Budget received; exact payload and transcript reservations pending"}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=Path("config/configurations.json"))
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    codes = [x["code"] for x in json.loads(args.config.read_text(encoding="utf-8"))["configurations"]]
    report = {"kind": "offline_design_arithmetic_not_empirical_results",
              "current": inspect_design(codes), "proposal": propose_single_replacement(codes),
              "provisional_call_budget": call_budget()}
    text = json.dumps(report, indent=2) + "\n"
    if args.output:
        with args.output.open("x", encoding="utf-8", newline="\n") as handle:
            handle.write(text)
    print(text, end="")


if __name__ == "__main__":
    main()
