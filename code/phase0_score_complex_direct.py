"""
Score Phase 0 C1/C2/C3 simple direct-call calibration outputs.

Mirrors code/phase0_score_simple.py for C1/C2/C3 direct prompts.
"""

from __future__ import annotations

import argparse
import json
import math
from collections import Counter
from pathlib import Path
from typing import Any

from phase0_run_complex_direct import PROBLEMS, QUESTIONS_DIR, load_bare_prompt


REPO_ROOT = Path(__file__).resolve().parents[1]
EVALS_DIR = REPO_ROOT / "experiments" / "phase0_baseline_calibration" / "results" / "raw" / "evals"


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def wilson_interval(successes: int, n: int, z: float = 1.959963984540054) -> tuple[float, float]:
    if n == 0:
        return (math.nan, math.nan)
    phat = successes / n
    denom = 1 + z * z / n
    center = (phat + z * z / (2 * n)) / denom
    margin = z * math.sqrt((phat * (1 - phat) + z * z / (4 * n)) / n) / denom
    return (center - margin, center + margin)


def verdict(max_share: float) -> str:
    if math.isnan(max_share):
        return "NO DATA"
    if max_share <= 0.55:
        return "WELL-CALIBRATED"
    if max_share <= 0.60:
        return "ACCEPTABLE FLAG"
    return "REWRITE / RETUNE"


def pct(value: float) -> str:
    if math.isnan(value):
        return "n/a"
    return f"{100 * value:.1f}%"


def score_problem(problem: Any, expected_n: int | None, last_n: int | None) -> None:
    expected_prompt = load_bare_prompt(QUESTIONS_DIR / problem.question_file)
    folder = EVALS_DIR / problem.folder_id
    files = sorted(folder.glob(f"{problem.short_id}_*.json"))
    all_file_count = len(files)
    if last_n is not None:
        files = files[-last_n:]

    rows: list[dict[str, Any]] = []
    bad_json: list[str] = []
    for path in files:
        try:
            payload = load_json(path)
        except Exception as exc:  # noqa: BLE001
            bad_json.append(f"{path.name}: {type(exc).__name__}: {exc}")
            continue
        payload["_path"] = path
        rows.append(payload)

    parse_counts = Counter(row.get("parse_status") for row in rows)
    choice_counts = Counter(row.get("parsed_choice") for row in rows if row.get("parsed_choice"))
    model_counts = Counter(row.get("model") for row in rows)
    prompt_matches = sum(1 for row in rows if row.get("user_prompt") == expected_prompt)
    api_ids = [row.get("api_call_id") for row in rows if row.get("api_call_id")]
    timestamps = [row.get("timestamp_utc") for row in rows if row.get("timestamp_utc")]
    raw_responses = [row.get("raw_response") for row in rows if row.get("raw_response") is not None]

    ok_rows = [row for row in rows if row.get("parse_status") == "ok" and row.get("parsed_choice")]
    n_ok = len(ok_rows)
    ok_choice_counts = Counter(row.get("parsed_choice") for row in ok_rows)
    dominant_count = max(ok_choice_counts.values(), default=0)
    dominant_share = dominant_count / n_ok if n_ok else math.nan
    ci_low, ci_high = wilson_interval(dominant_count, n_ok)

    print(f"\n--- {problem.folder_id} ---")
    if last_n is not None:
        print(f"selection: last {last_n} files by filename/call index out of {all_file_count}")
    print(f"files read: {len(rows)}" + (f" / expected {expected_n}" if expected_n else ""))
    if expected_n and len(rows) != expected_n:
        print(f"WARNING: expected {expected_n} files but found {len(rows)}")
    if bad_json:
        print(f"bad json files: {len(bad_json)}")
        for item in bad_json[:10]:
            print(f"  {item}")

    print(f"models: {dict(model_counts)}")
    print(f"prompt matches current file: {prompt_matches}/{len(rows)}")
    if prompt_matches != len(rows):
        print("WARNING: some raw files were generated from a different prompt version")

    print(f"parse_status: {dict(parse_counts)}")
    print(f"all parsed choices: {dict(choice_counts)}")
    print(f"ok-only choices: {dict(ok_choice_counts)}")
    print(f"unique api_call_id: {len(set(api_ids))}/{len(api_ids)}")
    print(f"unique timestamp_utc: {len(set(timestamps))}/{len(timestamps)}")
    print(f"unique raw_response: {len(set(raw_responses))}/{len(raw_responses)}")

    if n_ok:
        for choice in problem.choices:
            count = ok_choice_counts.get(choice, 0)
            share = count / n_ok
            low, high = wilson_interval(count, n_ok)
            print(f"{choice}: {count}/{n_ok} = {pct(share)} (95% Wilson CI {pct(low)}-{pct(high)})")
        dominant_choice = ok_choice_counts.most_common(1)[0][0]
        print(
            "dominant choice: "
            f"{dominant_choice} at {pct(dominant_share)} "
            f"(95% Wilson CI {pct(ci_low)}-{pct(ci_high)})"
        )
    print(f"calibration verdict: {verdict(dominant_share)}")

    failures = [
        row
        for row in rows
        if row.get("parse_status") not in {"ok", None} or row.get("error_message")
    ]
    if failures:
        print("failure/ambiguity examples:")
        for row in failures[:5]:
            print(
                f"  {row['_path'].name}: status={row.get('parse_status')!r}, "
                f"choice={row.get('parsed_choice')!r}, error={row.get('error_message')!r}"
            )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--expected-n", type=int, default=None)
    parser.add_argument("--last-n", type=int, default=None)
    parser.add_argument(
        "--problems",
        nargs="+",
        choices=[problem.short_id for problem in PROBLEMS],
        default=[problem.short_id for problem in PROBLEMS],
    )
    args = parser.parse_args()
    if args.last_n is not None and args.last_n < 1:
        raise ValueError("--last-n must be at least 1")
    return args


def main() -> None:
    args = parse_args()
    print("Phase 0 C1/C2/C3 direct calibration scorer")
    print(f"raw evals: {EVALS_DIR}")
    selected = set(args.problems)
    for problem in PROBLEMS:
        if problem.short_id not in selected:
            continue
        score_problem(problem, args.expected_n, args.last_n)


if __name__ == "__main__":
    main()
