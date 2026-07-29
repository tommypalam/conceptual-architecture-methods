"""
recalibrate.py — Step D naked-prompt recalibration of drifted dilemmas.

Phase 0b (2026-07-28) established that model drift, not the harness, pushed 4 of
6 dilemmas off their May 2026 ~50/50 baseline on the current model
(gpt-5.4-mini-2026-03-17). Harness levers were exhausted (Steps A–C). Per the
approved remediation plan, the last resort is to recalibrate the drifted
dilemmas — the exact process Phase 0a used: iterate the wording until the NAKED
prompt (no system message, bare decision) splits ~50/50 on the current model.

This rig is the calibration loop:
  - take a CANDIDATE dilemma text + its two labels
  - run it naked at N (no system message; user turn = dilemma + bare reply line)
  - report split, Wilson 95% CI, and PASS/FAIL against 45-55 (spec §6.1 target)
  - every candidate is archived (records + a variant summary), like the 0a archive

It does NOT edit any locked file. Candidate texts are supplied by the caller
(a human-authored rewording). The frozen Phase-0a question files remain
untouched; an accepted candidate becomes a NEW file only at the explicit lock
step, with human sign-off (CLAUDE.md: rewriting a Phase-0 problem needs approval).
"""

from __future__ import annotations

import asyncio

from . import parsing
from .llm_client import Message, SupportsComplete
from .record_sink import RecordSink
from .scoring import wilson_ci
from .seeding import derive_seed

TEMPERATURE = 1.0
MAX_TOKENS = 20        # bare decision only; no reasoning needed for calibration


def naked_user_turn(dilemma_body: str, labels: tuple[str, str]) -> str:
    """Phase-0a naked format: dilemma + 'Reply with only: X or Y'. No system msg."""
    a, b = labels
    return f"{dilemma_body}\n\nReply with only: {a} or {b}"


async def calibrate_candidate(*, client: SupportsComplete, sink: RecordSink,
                              candidate_id: str, dilemma_body: str,
                              labels: tuple[str, str], n: int, root_seed: int,
                              resume: bool = True) -> dict:
    """
    Run one candidate dilemma naked at N. Returns split + Wilson CI + verdict.
    Records keyed `{candidate_id}/call_{k:04d}`.
    """
    user_turn = naked_user_turn(dilemma_body, labels)
    counts = {labels[0]: 0, labels[1]: 0}
    n_ok = bad = 0
    lock = asyncio.Lock()

    async def one(k):
        nonlocal n_ok, bad
        key = f"{candidate_id}/call_{k:04d}"
        if resume and sink.exists(key):
            # Re-tally from the existing record so resume stays accurate.
            return
        seed = derive_seed(root_seed, candidate_id, k)
        result = await client.complete([Message("user", user_turn)],
                                       temperature=TEMPERATURE, max_tokens=MAX_TOKENS,
                                       seed=seed)
        decision, status = parsing.parse_decision(result.text, labels)
        rec = {"schema_version": "1.0", "phase": "phase0b_recalibrate",
               "candidate_id": candidate_id, "call_index": k,
               "labels": list(labels), "model_name": result.model,
               "model_version": result.model_version, "provider": result.provider,
               "temperature": TEMPERATURE, "seed": seed,
               "timestamp_utc": result.timestamp_utc, "api_call_id": result.api_call_id,
               "user_prompt": user_turn, "raw_response": result.text,
               "parsed_decision": decision, "parse_status": status}
        if result.error:
            rec["error_message"] = result.error
            rec["parse_status"] = "failed_api"
        sink.write(key, rec)

    await asyncio.gather(*(one(k) for k in range(1, n + 1)))

    # Tally from all records on disk (covers resumed + new). The NAKED format
    # asks for a bare label ("Reply with only: X or Y"), so a clean response has
    # no "DECISION:" prefix and parses as `ambiguous` (a single recovered label)
    # rather than `ok`. Both count as a valid decision here; only genuine
    # non-decisions (fail / refusal / failed_api) are excluded.
    valid = {"ok", "ambiguous"}
    for rec in sink.read_all():
        if rec.get("candidate_id") != candidate_id:
            continue
        if rec.get("parse_status") in valid and rec.get("parsed_decision") in counts:
            counts[rec["parsed_decision"]] += 1
            n_ok += 1
        else:
            bad += 1

    first = labels[0]
    k = counts[first]
    lo, hi = wilson_ci(k, n_ok) if n_ok else (0.0, 0.0)
    rate = k / n_ok if n_ok else 0.0
    # Spec §6.1 calibration target: 45-55 ideal; 40-60 acceptable band.
    in_45_55 = 0.45 <= rate <= 0.55
    in_40_60 = 0.40 <= rate <= 0.60
    verdict = ("PASS (45-55)" if in_45_55 else
               "ACCEPTABLE (40-60)" if in_40_60 else "FAIL (rewrite)")
    return {"candidate_id": candidate_id, "n_ok": n_ok, "bad": bad,
            "counts": dict(counts), "rate_label": first, "rate": round(rate, 4),
            "wilson_95": [round(lo, 4), round(hi, 4)], "verdict": verdict}
