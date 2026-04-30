"""
Run Phase 0 simple baseline calibration calls.

This script sends the bare S1/S2/S3 prompts to gpt-5.4-mini with no system
prompt and writes one immutable JSON artifact per API call.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from openai import AsyncOpenAI


MODEL = "gpt-5.4-mini"
TEMPERATURE = 1.0
DEFAULT_CALLS_PER_PROBLEM = 200
DEFAULT_CONCURRENCY = 10

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE0_DIR = REPO_ROOT / "experiments" / "phase0_baseline_calibration"
QUESTIONS_DIR = PHASE0_DIR / "questions"
EVALS_DIR = PHASE0_DIR / "results" / "raw" / "evals"


@dataclass(frozen=True)
class Problem:
    short_id: str
    folder_id: str
    question_file: str
    choices: tuple[str, str]


PROBLEMS = (
    Problem(
        short_id="S1",
        folder_id="S1_promotion_decision",
        question_file="S1_promotion_decision.md",
        choices=("A", "B"),
    ),
    Problem(
        short_id="S2",
        folder_id="S2_quiet_error",
        question_file="S2_quiet_error.md",
        choices=("REPORT", "QUIET"),
    ),
    Problem(
        short_id="S3",
        folder_id="S3_strategic_pivot",
        question_file="S3_strategic_pivot.md",
        choices=("ADOPT", "WAIT"),
    ),
)


REFUSAL_RE = re.compile(
    r"\b("
    r"cannot|can't|unable|won't|refuse|sorry|as an ai|i do not have enough"
    r")\b",
    re.IGNORECASE,
)


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_bare_prompt(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    match = re.search(r"```(?:[a-zA-Z0-9_-]+)?\s*\n(.*?)\n```", text, flags=re.DOTALL)
    if not match:
        raise ValueError(f"No triple-backtick prompt block found in {path}")
    return match.group(1).strip()


def highest_existing_index(problem_dir: Path, short_id: str) -> int:
    pattern = re.compile(rf"^{re.escape(short_id)}_(\d+)\.json$")
    highest = 0
    if not problem_dir.exists():
        return highest

    for path in problem_dir.iterdir():
        match = pattern.match(path.name)
        if match:
            highest = max(highest, int(match.group(1)))
    return highest


def validate_existing_outputs(
    problem_dir: Path,
    short_id: str,
    expected_model: str,
    expected_prompt: str,
) -> None:
    pattern = re.compile(rf"^{re.escape(short_id)}_\d+\.json$")
    mismatches: list[str] = []
    if not problem_dir.exists():
        return

    for path in sorted(problem_dir.iterdir()):
        if not pattern.match(path.name):
            continue
        with path.open(encoding="utf-8") as handle:
            payload = json.load(handle)
        recorded_model = payload.get("model")
        if recorded_model != expected_model:
            mismatches.append(f"{path}: model={recorded_model!r}")
        if payload.get("user_prompt") != expected_prompt:
            mismatches.append(f"{path}: user_prompt does not match current prompt file")

    if mismatches:
        raise ValueError(
            f"Existing {short_id} eval files are incompatible with the current run. "
            "Archive or remove them before starting a new calibration run.\n"
            + "\n".join(mismatches)
        )


def parse_choice(raw_response: str | None, choices: tuple[str, str]) -> tuple[str | None, str]:
    if raw_response is None:
        return None, "error"

    normalized_choices = tuple(choice.upper() for choice in choices)
    escaped = "|".join(re.escape(choice) for choice in normalized_choices)

    strict_re = re.compile(rf"^\s*(?:{escaped})\s*$", re.IGNORECASE)
    strict_match = strict_re.match(raw_response)
    if strict_match:
        return strict_match.group(0).strip().upper(), "ok"

    if all(len(choice) == 1 for choice in normalized_choices):
        lenient_patterns = (
            rf"\b(?:answer|reply|choice|choose|promote|candidate|option)\s*(?:is|:|-)?\s*({escaped})\b",
            rf"\b({escaped})\s*(?:is my choice|would be promoted|should be promoted)\b",
            rf"(?:^|\n)\s*({escaped})\s*[\.\)]?\s*(?:$|\n)",
        )
        found: list[str] = []
        for pattern in lenient_patterns:
            found.extend(
                match.group(1).upper()
                for match in re.finditer(pattern, raw_response, flags=re.IGNORECASE)
            )
        unique_found = {choice for choice in found if choice in normalized_choices}
        if len(unique_found) == 1:
            return unique_found.pop(), "ambiguous"
        if REFUSAL_RE.search(raw_response):
            return None, "refusal"
        return None, "error"

    token_re = re.compile(rf"\b({escaped})\b", re.IGNORECASE)
    found = [match.group(1).upper() for match in token_re.finditer(raw_response)]
    unique_found = {choice for choice in found if choice in normalized_choices}
    if len(unique_found) == 1:
        return unique_found.pop(), "ambiguous"

    if REFUSAL_RE.search(raw_response):
        return None, "refusal"

    return None, "error"


def atomic_write_json(path: Path, payload: dict[str, Any]) -> None:
    if path.exists():
        raise FileExistsError(f"Target already exists: {path}")

    tmp_path = path.with_name(f"{path.name}.tmp")
    with tmp_path.open("x", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=False)
        handle.write("\n")
        handle.flush()
        os.fsync(handle.fileno())

    if path.exists():
        tmp_path.unlink(missing_ok=True)
        raise FileExistsError(f"Target already exists: {path}")

    os.rename(tmp_path, path)


async def call_model(client: AsyncOpenAI, prompt: str) -> tuple[str | None, str | None, str | None]:
    try:
        response = await client.chat.completions.create(
            model=MODEL,
            temperature=TEMPERATURE,
            messages=[{"role": "user", "content": prompt}],
        )
        raw_response = response.choices[0].message.content
        return raw_response, response.id, None
    except Exception as exc:  # noqa: BLE001 - API error is recorded as data.
        return None, None, f"{type(exc).__name__}: {exc}"


async def run_one_call(
    *,
    client: AsyncOpenAI,
    semaphore: asyncio.Semaphore,
    problem: Problem,
    prompt: str,
    call_index: int,
    output_path: Path,
) -> dict[str, Any]:
    async with semaphore:
        raw_response, api_call_id, api_error = await call_model(client, prompt)
        timestamp = utc_now_iso()

    parsed_choice, parse_status = parse_choice(raw_response, problem.choices)
    error_message = api_error
    if api_error is None and parse_status == "error":
        error_message = "Could not parse expected choice from response."

    payload: dict[str, Any] = {
        "problem_id": problem.short_id,
        "call_index": call_index,
        "model": MODEL,
        "temperature": TEMPERATURE,
        "system_prompt": None,
        "user_prompt": prompt,
        "raw_response": raw_response,
        "parsed_choice": parsed_choice,
        "parse_status": parse_status,
        "timestamp_utc": timestamp,
        "api_call_id": api_call_id,
    }
    if error_message is not None:
        payload["error_message"] = error_message

    atomic_write_json(output_path, payload)
    return payload


async def run_problem(
    *,
    client: AsyncOpenAI,
    semaphore: asyncio.Semaphore,
    problem: Problem,
    calls_per_problem: int,
) -> None:
    prompt = load_bare_prompt(QUESTIONS_DIR / problem.question_file)
    problem_dir = EVALS_DIR / problem.folder_id
    problem_dir.mkdir(parents=True, exist_ok=True)

    validate_existing_outputs(problem_dir, problem.short_id, MODEL, prompt)
    first_index = highest_existing_index(problem_dir, problem.short_id) + 1
    planned_paths = [
        problem_dir / f"{problem.short_id}_{call_index:03d}.json"
        for call_index in range(first_index, first_index + calls_per_problem)
    ]
    existing_targets = [str(path) for path in planned_paths if path.exists()]
    if existing_targets:
        raise FileExistsError(
            "Refusing to overwrite existing target files:\n" + "\n".join(existing_targets)
        )

    completed = 0
    lock = asyncio.Lock()

    async def wrapped(call_index: int, output_path: Path) -> None:
        nonlocal completed
        await run_one_call(
            client=client,
            semaphore=semaphore,
            problem=problem,
            prompt=prompt,
            call_index=call_index,
            output_path=output_path,
        )
        async with lock:
            completed += 1
            if completed % 10 == 0 or completed == calls_per_problem:
                print(f"{problem.short_id}: {completed}/{calls_per_problem} calls complete")

    tasks = [
        asyncio.create_task(wrapped(call_index, output_path))
        for call_index, output_path in zip(
            range(first_index, first_index + calls_per_problem), planned_paths, strict=True
        )
    ]
    await asyncio.gather(*tasks)


async def main_async(args: argparse.Namespace) -> None:
    if not os.environ.get("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY is not set in the environment.")

    client = AsyncOpenAI()
    semaphore = asyncio.Semaphore(args.concurrency)
    selected_problem_ids = set(args.problems)

    for problem in PROBLEMS:
        if problem.short_id not in selected_problem_ids:
            continue
        await run_problem(
            client=client,
            semaphore=semaphore,
            problem=problem,
            calls_per_problem=args.calls_per_problem,
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--calls-per-problem",
        type=int,
        default=DEFAULT_CALLS_PER_PROBLEM,
        help="Number of independent calls to make per simple problem.",
    )
    parser.add_argument(
        "--concurrency",
        type=int,
        default=DEFAULT_CONCURRENCY,
        help="Maximum number of concurrent OpenAI API calls.",
    )
    parser.add_argument(
        "--problems",
        nargs="+",
        choices=[problem.short_id for problem in PROBLEMS],
        default=[problem.short_id for problem in PROBLEMS],
        help="Problem IDs to run. Example: --problems S1 S2",
    )
    args = parser.parse_args()

    if args.calls_per_problem < 1:
        raise ValueError("--calls-per-problem must be at least 1")
    if args.concurrency < 1 or args.concurrency > DEFAULT_CONCURRENCY:
        raise ValueError(f"--concurrency must be between 1 and {DEFAULT_CONCURRENCY}")
    return args


def main() -> None:
    asyncio.run(main_async(parse_args()))


if __name__ == "__main__":
    main()
