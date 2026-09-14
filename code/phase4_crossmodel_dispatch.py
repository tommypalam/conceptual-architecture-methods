"""Ledger dispatch with a provider-agnostic response contract.

The shared `phase3_recognition_run.dispatch` validates every reply through
`parse`, which offers two contracts: raw text under 1024 bytes (`kind ==
"probe"`), or a strict ratings schema. Both encode one model's answering style.
`claude-haiku-4-5` answers the Phase 4 tasks correctly but reasons first, so its
replies are rejected on format and the no-retry rule halts the run.

Output format is not part of the estimand. The comparison is: same input, same
deterministic rule map, does the profile move the choice? This module keeps every
ledger guarantee and changes only how a reply is read.

**Preserved exactly, by reusing the shared implementations:**
  - `Ledger` for the exclusive lock, reservation audit and provider totals
  - `write_once` for reservations, records and settlements
  - `charge` for cost accounting, including full reservation on failure
  - the complete-reservation identity check before any dispatch
  - failure preservation in `failures.jsonl` with no retry
  - replay: a resumed slot must reproduce the same extracted value

**Changed:** the parse step is chosen per job by `parse_for`, from two contracts
that a job declares explicitly and exclusively:

  - `valid_actions` -> `extract_choice`, which reads only a single unambiguous
    `{"choice": "..."}` object and never scans prose. Strictly narrower than the
    inherited parser, and verified to reproduce all 960 `moral_capstone_r3`
    decisions byte-identically before use.
  - `raw_text` -> the complete reply verbatim, for calls that do not return a
    task choice. A design review returns a verdict; the inherited `probe`
    contract caps such a reply at 1024 bytes, a bound sized for a 35-word
    recognition answer, which rejected two complete review replies on length
    alone. The reservation bounds these replies instead, via the same usage
    guard every other call passes.

Both paths share `_complete_text`: same usage guard, same stop-reason check, same
truncation rule. Only what happens to the validated text differs. A job that
declares both contracts or neither is a construction error and raises.

This module does not edit any frozen source. `phase3_recognition.py` and
`phase3_recognition_run.py` are imported, never modified.
"""
from __future__ import annotations

import os
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError

from phase3_budget import BudgetStop, canonical, digest, read_checked
from phase3_recognition_run import MODELS, charge, write_once
from phase4_choice_extraction import extract_choice, response_text


def _usage_within_reservation(raw, job):
    """The inherited usage guard, kept verbatim in effect.

    A reply that exceeds the frozen input bound or output budget is a failure
    regardless of content: the reservation must bound what was actually spent.
    """
    request = job["request"]
    is_openai = MODELS[request["model"]] == "openai"
    keys = ("prompt_tokens", "completion_tokens") if is_openai else ("input_tokens", "output_tokens")
    usage = raw.get("usage", {}) if isinstance(raw, dict) else {}
    if raw.get("model") != request["model"]:
        raise ValueError("Model mismatch")
    if any(type(usage.get(k)) is not int or usage[k] < 0 for k in keys):
        raise ValueError("Usage missing or negative")
    maximum = (request["max_completion_tokens"] if is_openai else request["max_tokens"])
    if usage[keys[0]] > job["input_token_bound"] or usage[keys[1]] > maximum:
        raise ValueError("Usage exceeds frozen reservation")
    return usage[keys[1]], maximum


def _complete_text(raw, job):
    """Shared guards, then the reply text. Raises on anything not complete.

    Truncation is a failure for both call kinds: a reply cut off at the output
    limit may have been about to say something else, so its content is not
    trusted even if a well-formed object happens to appear before the cut.
    """
    produced, maximum = _usage_within_reservation(raw, job)
    stop = (raw.get("choices", [{}])[0].get("finish_reason")
            if raw.get("choices") else raw.get("stop_reason"))
    if stop not in ("stop", "end_turn"):
        raise ValueError(f"Incomplete output: {stop}")
    if produced >= maximum:
        raise ValueError("Output reached the token limit")
    text = response_text(raw)
    if text is None:
        raise ValueError("No readable response text")
    return text


def parse_choice(raw, job):
    """Extract the decision, or raise. `job` must carry `valid_actions`."""
    text = _complete_text(raw, job)
    picked = extract_choice(text, set(job["valid_actions"]))
    if picked is None:
        raise ValueError("No single unambiguous choice object")
    return picked


def parse_text(raw, job):
    """Return a complete reply verbatim, for calls that are not task choices.

    A design review returns a verdict, not an action id. The inherited `probe`
    contract would take this path but imposes a 1024-byte cap sized for a 35-word
    recognition answer; a reviewer that reasons before answering exceeds it while
    being perfectly complete. The reservation, not the byte count, is what bounds
    a reply here, and `_complete_text` already enforces it via the usage guard.

    No parsing, repair or inference: the caller owns interpretation.
    """
    return _complete_text(raw, job)


def parse_for(raw, job):
    """Pick the reader matched to what this job asks the model to return.

    A job declares exactly one contract. `raw_text` and `valid_actions` are
    mutually exclusive: a job carrying both, or neither, is a construction error
    and stops the run rather than guessing.
    """
    wants_text, wants_choice = bool(job.get("raw_text")), bool(job.get("valid_actions"))
    if wants_text == wants_choice:
        raise ValueError("Job must declare exactly one of raw_text or valid_actions")
    return parse_text(raw, job) if wants_text else parse_choice(raw, job)


def dispatch(ledger, job, manifest_sha, responder, replay=False):
    """Dispatch one job under the shared ledger, parsing with `parse_choice`.

    Mirrors `Ledger.dispatch` step for step; only the parser differs.
    """
    key = digest(job["slot"])
    if ledger.state["pending"] or ledger.state["failed"]:
        raise BudgetStop("Unresolved dispatch blocks continuation")
    path = ledger.root / "records" / (key + ".json")

    if key in ledger.state["reservations"]:
        previous = ledger.state["reservations"][key]
        if previous["request"] != job["request"] or previous["manifest_sha256"] != manifest_sha:
            raise BudgetStop("Changed request/manifest on resume")
        result = read_checked(path)
        if result["error"] is None and result["parsed"] != parse_for(result["raw"], job):
            raise BudgetStop("Replay parse mismatch")
        return result, False
    if replay:
        raise BudgetStop("Missing slot in offline replay")

    cap = ledger.release["slots"].get(job["slot"])
    if (cap is None or job["reserved_nano"] != cap["reserved_nano"]
            or job["request"]["model"] != cap["model"]
            or job["input_token_bound"] != cap["input_token_bound"]
            or job["kind"] != cap["kind"]
            or job["request"].get("max_tokens",
                                  job["request"].get("max_completion_tokens")) != cap["max_output"]
            or (cap.get("request_sha256") and digest(job["request"]) != cap["request_sha256"])):
        raise BudgetStop("Slot outside complete reservation")

    intent = {"slot": job["slot"], "stage": "recognition", "request": job["request"],
              "reserved_nano": job["reserved_nano"], "manifest_sha256": manifest_sha,
              "release_sha256": digest(ledger.release)}
    write_once(ledger.root / "reservations" / (key + ".json"), intent)
    ledger.state["reservations"][key] = intent

    raw, parsed, error = None, None, None
    try:
        raw = responder(job["request"])
        parsed = parse_for(raw, job)
    except Exception as exc:
        error = {"type": type(exc).__name__,
                 "status": exc.code if isinstance(exc, HTTPError) else None}
    amount = charge(raw, job, error is not None)
    result = {"raw": raw, "parsed": parsed, "error": error, "accounted_nano": amount,
              "manifest_sha256": manifest_sha,
              "timestamp": datetime.now(timezone.utc).isoformat()}
    write_once(path, result)
    write_once(ledger.root / "settlements" / (key + ".json"),
               {"reservation_sha256": digest(intent), "charged_nano": amount,
                "response_sha256": digest(result),
                "status": "failed" if error else "complete"})
    ledger.state["recognition_nano"] += amount
    ledger.state["providers"][MODELS[job["request"]["model"]]] += amount

    if error or amount > job["reserved_nano"]:
        with (ledger.root / "failures.jsonl").open("ab") as handle:
            handle.write(canonical({"slot": job["slot"], "record_sha256": digest(result),
                                    "error": error, "accounted_nano": amount}) + b"\n")
            handle.flush()
            os.fsync(handle.fileno())
        ledger.state["failed"].append(key)
        raise BudgetStop("Failure preserved at full reservation; no retry")
    return result, True
