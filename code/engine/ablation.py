"""
ablation.py — harness-framing ablation runner (diagnostic for the 2026-07-28
systemic Phase 0b bias).

Goal: find WHICH framing element collapses the naked-prompt 50/50, by toggling
one element at a time (framing.ablation_variants) and measuring the split. The
dilemma bodies are held fixed (frozen Phase-0a set); only the framing changes.

To isolate framing from parameter/config content, ablations run under the
EMPTY-HARNESS profile (null_a): no parameter block, no normative-context block.
Whatever still moves the split is therefore attributable to the framing alone.
The full system prompt for a variant is:

    preamble? (from framing)          # toggled
    [no profile block]                # null_a: empty harness
    [no normative-context block]      # null_a: empty harness
    task block                        # from framing (decision_rule / refusal)
  + user turn: dilemma body + format block  # format order from framing

Records reuse the standard per-call schema with an added `framing_label`, and
are written through the injected RecordSink into a per-variant subfolder so each
ablation is independently scorable and archivable.
"""

from __future__ import annotations

import asyncio

from . import parsing
from .framing import TaskFraming, ablation_variants
from .llm_client import Message, SupportsComplete
from .prompt_assembly import load_template
from .phase0b import split_blocks
from .questions import load_dilemma_body
from .phase0b_runner import PROBLEMS, TEMPERATURE, MAX_TOKENS
from .record_sink import RecordSink
from .seeding import derive_seed


def build_system_prompt(framing: TaskFraming, template: str) -> str:
    """Empty-harness (null_a) profile + framing-controlled preamble & task."""
    b = split_blocks(template)
    parts = []
    if framing.preamble:
        parts.append(b["preamble"])
    parts.append(framing.task_block(has_profile=False))
    return "\n\n".join(parts).strip()


def build_user_turn(framing: TaskFraming, dilemma_body: str,
                    labels: tuple[str, str]) -> str:
    return f"{dilemma_body}\n\n{framing.format_block(labels)}"


def build_record(*, variant_label, problem, k, framing, system_prompt, user_turn,
                 result, decision, status, reasoning) -> dict:
    rec = {
        "schema_version": "1.0",
        "phase": "phase0b_ablation",
        "framing_label": variant_label,
        "framing": {"preamble": framing.preamble, "decision_rule": framing.decision_rule,
                    "do_not_refuse": framing.do_not_refuse,
                    "decision_first": framing.decision_first},
        "condition_id": "null_a",   # ablations run under empty harness
        "problem_id": problem.short_id,
        "labels": list(problem.labels),   # stable rate anchor for the scorer
        "call_index": k,
        "model_name": result.model, "model_version": result.model_version,
        "provider": result.provider, "temperature": result.temperature,
        "max_tokens": result.max_tokens, "seed": result.seed,
        "timestamp_utc": result.timestamp_utc, "api_call_id": result.api_call_id,
        "attempts": result.attempts,
        "system_prompt": system_prompt, "user_prompt": user_turn,
        "raw_response": result.text, "parsed_decision": decision,
        "parsed_reasoning": reasoning, "parse_status": status,
    }
    if result.error:
        rec["error_message"] = result.error
        rec["parse_status"] = "failed_api"
    return rec


async def run_ablation(*, client: SupportsComplete, sink: RecordSink,
                       root_seed: int, n: int, variants=None, problems=PROBLEMS,
                       questions_dir=None, resume: bool = True) -> dict:
    """
    Run each framing variant × each problem × N, under the empty harness.
    Records keyed `{variant_label}/{problem}/call_{k:04d}` so each variant is a
    self-contained scorable cell-set. `questions_dir` selects the locked question
    set (defaults to the immutable Phase-0a set; pass PHASE0B_QUESTIONS for the
    recalibrated set).
    """
    from .questions import PHASE0_QUESTIONS
    if questions_dir is None:
        questions_dir = PHASE0_QUESTIONS
    variants = variants or ablation_variants()
    template = load_template()
    dilemmas = {p.short_id: load_dilemma_body(p.question_file, questions_dir)
                for p in problems}

    planned = executed = skipped = ok = 0
    lock = asyncio.Lock()

    async def one(label, framing, problem, k):
        nonlocal executed, skipped, ok
        key = f"{label}/{problem.short_id}/call_{k:04d}"
        if resume and sink.exists(key):
            async with lock:
                skipped += 1
            return
        user_turn = build_user_turn(framing, dilemmas[problem.short_id], problem.labels)
        seed = derive_seed(root_seed, label, problem.short_id, k)
        if framing.use_system_role:
            system_prompt = build_system_prompt(framing, template)
            messages = [Message("system", system_prompt), Message("user", user_turn)]
        else:
            # Pure Phase-0a structure: no system message; dilemma as user-only.
            system_prompt = None
            messages = [Message("user", user_turn)]
        result = await client.complete(
            messages, temperature=TEMPERATURE, max_tokens=MAX_TOKENS, seed=seed)
        decision, status = parsing.parse_decision(result.text, problem.labels)
        reasoning = parsing.parse_reasoning(result.text)
        rec = build_record(variant_label=label, problem=problem, k=k, framing=framing,
                           system_prompt=system_prompt, user_turn=user_turn,
                           result=result, decision=decision, status=status,
                           reasoning=reasoning)
        sink.write(key, rec)
        if result.error:
            sink.write_failure({"variant": label, "problem": problem.short_id,
                                "call_index": k, "error": result.error})
        async with lock:
            executed += 1
            if rec["parse_status"] == "ok":
                ok += 1

    tasks = []
    for label, framing in variants.items():
        for problem in problems:
            for k in range(1, n + 1):
                planned += 1
                tasks.append(one(label, framing, problem, k))
    await asyncio.gather(*tasks)

    summary = {"planned": planned, "executed": executed, "skipped": skipped, "ok": ok}
    print(f"ablation runner: {summary}")
    return summary
