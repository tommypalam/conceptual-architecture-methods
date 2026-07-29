"""
phase0b_runner.py — Phase 0b harness-neutral runner (spec §2.1.4).

Pure orchestration. It depends only on injected abstractions:
  - a client satisfying `SupportsComplete`   (llm_client.LLMClient / MockClient)
  - a mapping of condition_id -> NullConditionAssembler  (phase0b.default_assemblers)
  - a `RecordSink`                            (record_sink.JsonFileSink / MemorySink)

Because none of those are constructed here, the runner has no knowledge of which
provider, which prompt internals, or which storage backend are in play. Swap any
block (mock client, in-memory sink, a fourth null condition) and this file does
not change — Dependency Inversion + Liskov substitution end to end.

Protocol (spec §2.1.4): 3 conditions × 6 problems × N calls; one independent
call per response; one record per call; DECISION + REASONING; per-call record
carries condition_id + problem_id + harness provenance (Appendix C).
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass

from . import parsing
from .llm_client import Message, SupportsComplete
from .phase0b import NullConditionAssembler
from .prompt_assembly import build_simple_user_turn, load_template
from .questions import load_dilemma_body
from .record_sink import RecordSink
from .seeding import derive_seed

TEMPERATURE = 1.0
MAX_TOKENS = 600
N_DEFAULT = 500


@dataclass(frozen=True)
class Problem:
    short_id: str
    question_file: str
    labels: tuple[str, str]


# All six problems, single-call direct form (Phase 0b tests the harness, not the
# multi-agent dynamics), v0.6 canonical labels.
PROBLEMS = (
    Problem("S1", "S1_promotion_decision.md", ("A", "B")),
    Problem("S2", "S2_quiet_error.md", ("FORMAL_REPORT", "LOCAL_CORRECTION")),
    Problem("S3", "S3_strategic_pivot.md", ("ADOPT", "WAIT")),
    Problem("C1", "C1_resource_council.md", ("PACKAGE_A", "PACKAGE_B")),
    Problem("C2", "C2_restructuring_board.md", ("APPROVE", "REJECT")),
    Problem("C3", "C3_scientific_approach_dilemma.md", ("CONTINUE", "PIVOT")),
)


def build_record(*, condition, problem, k, provenance, system_prompt, user_turn,
                 result, decision, status, reasoning) -> dict:
    """Appendix C per-call record; carries condition_id, problem_id, provenance."""
    rec = {
        "schema_version": "1.0",
        "phase": "phase0b_harness_neutral",
        "condition_id": condition,
        "problem_id": problem.short_id,
        "labels": list(problem.labels),   # stable rate anchor for the scorer
        "call_index": k,
        "model_name": result.model,
        "model_version": result.model_version,
        "provider": result.provider,
        "temperature": result.temperature,
        "max_tokens": result.max_tokens,
        "seed": result.seed,
        "timestamp_utc": result.timestamp_utc,
        "api_call_id": result.api_call_id,
        "attempts": result.attempts,
        "harness_provenance": provenance,
        "system_prompt": system_prompt,
        "user_prompt": user_turn,
        "raw_response": result.text,
        "parsed_decision": decision,
        "parsed_reasoning": reasoning,
        "parse_status": status,
    }
    if result.error:
        rec["error_message"] = result.error
        rec["parse_status"] = "failed_api"
    return rec


async def run_phase0b(*, client: SupportsComplete,
                      assemblers: dict[str, NullConditionAssembler],
                      sink: RecordSink, root_seed: int, n: int = N_DEFAULT,
                      problems=PROBLEMS, delivery=None, questions_dir=None,
                      bare_label: bool = False, max_tokens: int = MAX_TOKENS,
                      resume: bool = True) -> dict:
    """
    Execute the (conditions × problems × N) grid. Conditions are exactly the keys
    of `assemblers`. `delivery` (a Delivery; default SystemRoleDelivery) decides
    whether the assembled harness is sent as a system message or prepended to the
    user turn — so the same runner tests both without change. `questions_dir`
    selects which locked question set to source dilemma bodies from; it defaults
    to the immutable Phase-0a set. Pass questions.PHASE0B_QUESTIONS for the
    recalibrated set. `bare_label` uses the naked-calibration output envelope
    (no DECISION/REASONING structure), and `max_tokens` overrides the per-call
    cap (use a small value with bare_label). Returns a summary.
    """
    from .delivery import SystemRoleDelivery
    from .questions import PHASE0_QUESTIONS
    if delivery is None:
        delivery = SystemRoleDelivery()
    if questions_dir is None:
        questions_dir = PHASE0_QUESTIONS
    template = load_template()
    dilemmas = {p.short_id: load_dilemma_body(p.question_file, questions_dir)
                for p in problems}

    planned = executed = skipped = ok = 0
    lock = asyncio.Lock()

    async def one(condition, assembler, problem, k):
        nonlocal executed, skipped, ok
        key = f"{condition}/{problem.short_id}/call_{k:04d}"
        if resume and sink.exists(key):
            async with lock:
                skipped += 1
            return
        seed = derive_seed(root_seed, condition, problem.short_id, k)
        system_prompt, provenance = assembler.build(template, seed=seed)
        user_turn = build_simple_user_turn(dilemmas[problem.short_id],
                                            problem.labels, bare_label=bare_label)
        result = await client.complete(
            delivery.messages(system_prompt, user_turn),
            temperature=TEMPERATURE, max_tokens=max_tokens, seed=seed)
        decision, status = parsing.parse_decision(result.text, problem.labels)
        reasoning = parsing.parse_reasoning(result.text)
        rec = build_record(condition=condition, problem=problem, k=k,
                           provenance=provenance, system_prompt=system_prompt,
                           user_turn=user_turn, result=result, decision=decision,
                           status=status, reasoning=reasoning)
        rec["delivery"] = delivery.delivery_id
        sink.write(key, rec)
        if result.error:
            sink.write_failure({"condition": condition, "problem": problem.short_id,
                                "call_index": k, "error": result.error})
        async with lock:
            executed += 1
            if rec["parse_status"] == "ok":
                ok += 1
            if executed % 250 == 0:
                print(f"  executed {executed} (ok {ok}, skipped {skipped})")

    tasks = []
    for condition, assembler in assemblers.items():
        for problem in problems:
            for k in range(1, n + 1):
                planned += 1
                tasks.append(one(condition, assembler, problem, k))
    await asyncio.gather(*tasks)

    summary = {"planned": planned, "executed": executed, "skipped": skipped, "ok": ok}
    print(f"phase 0b runner: {summary}")
    return summary
