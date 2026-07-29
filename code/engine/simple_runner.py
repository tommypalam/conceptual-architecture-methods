"""
simple_runner.py — the LPM engine for Phase 2 simple problems (spec Part 5).

Large-population-model execution: a single hash-locked population of paired
agents is exposed within-subjects to every configuration on every simple
problem (S1–S3). Each (agent, config, problem) triple is one independent API
call in the full Phase 2 system-prompt format, producing DECISION + REASONING.

Per spec:
  §5.1  population drawn once, hash-locked
  §5.2  deterministic per-(agent, problem) configuration exposure order
  §5.3  system-prompt assembly, per-call seed from (agent, config, problem)
  §5.4  parsing, error handling (record-not-retry), rerun policy
  §5.4.4  200 agents x 3 problems x ~10 configs ≈ 6,000 calls

Records are write-once JSON under
  experiments/phase2_simple/runs_per_configuration/{config}/{problem}/agent_{id}.json
mirroring the Appendix C.1 per-call schema. This runner does not begin unless a
real client is provided; pass a MockClient for offline structural verification.
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from pathlib import Path

from . import prompt_assembly, parsing
from .llm_client import Message, SupportsComplete
from .population import Population, exposure_order
from .questions import load_dilemma_body
from .record_sink import JsonFileSink, RecordSink
from .seeding import derive_seed

REPO_ROOT = Path(__file__).resolve().parents[2]
OUT_ROOT = REPO_ROOT / "experiments" / "phase2_simple"
POP_FILE = OUT_ROOT / "paired_agent_population" / "agents.json"

TEMPERATURE = 1.0
MAX_TOKENS = 600


@dataclass(frozen=True)
class SimpleProblem:
    short_id: str
    question_file: str
    labels: tuple[str, str]


# v0.6 canonical labels (see thesis §6.2 / Appendix C).
SIMPLE_PROBLEMS = (
    SimpleProblem("S1", "S1_promotion_decision.md", ("A", "B")),
    SimpleProblem("S2", "S2_quiet_error.md", ("FORMAL_REPORT", "LOCAL_CORRECTION")),
    SimpleProblem("S3", "S3_strategic_pivot.md", ("ADOPT", "WAIT")),
)


def build_record(*, agent, config_code, problem, exposure_pos, system_prompt,
                 user_turn, result, decision, status, reasoning) -> dict:
    rec = {
        "schema_version": "1.0",
        "phase": "phase2_simple",
        "problem_id": problem.short_id,
        "configuration_id": config_code,
        "agent_id": agent.agent_id,
        "agent_parameters": agent.parameters,
        "exposure_order_position": exposure_pos,
        "model_name": result.model,
        "model_version": result.model_version,
        "provider": result.provider,
        "temperature": result.temperature,
        "max_tokens": result.max_tokens,
        "seed": result.seed,
        "timestamp": result.timestamp_utc,
        "api_call_id": result.api_call_id,
        "latency_s": result.latency_s,
        "attempts": result.attempts,
        "request_payload": {"messages": result.request_messages},
        "response_payload": result.raw_response,
        "raw_response": result.text,
        "parsed_decision": decision,
        "parsed_reasoning": reasoning,
        "parse_status": status,
    }
    if result.error:
        rec["error_message"] = result.error
        rec["parse_status"] = "failed_api"
    return rec


async def run_simple(*, client: SupportsComplete, config_codes: list[str],
                     root_seed: int, population: Population,
                     problems=SIMPLE_PROBLEMS, sink: RecordSink | None = None,
                     out_root: Path = OUT_ROOT, questions_dir=None,
                     resume: bool = True) -> dict:
    """
    Execute the simple-problem grid. Returns a summary dict. `resume=True`
    skips triples whose record already exists (safe restart after a mid-run
    failure — spec §5.4.3 rerun policy: continue, never edit).

    Storage is injected via `sink` (any RecordSink). If omitted, a JsonFileSink
    rooted at `out_root/runs_per_configuration` is used — so callers may pass a
    MemorySink for offline tests without this runner changing.

    `questions_dir` selects the locked question set (defaults to the immutable
    Phase-0a set; pass questions.PHASE0B_QUESTIONS for the recalibrated set).
    """
    from .questions import PHASE0_QUESTIONS
    if questions_dir is None:
        questions_dir = PHASE0_QUESTIONS
    if sink is None:
        sink = JsonFileSink(out_root / "runs_per_configuration")
    template = prompt_assembly.load_template()
    dilemmas = {p.short_id: load_dilemma_body(p.question_file, questions_dir)
                for p in problems}

    planned = 0
    executed = 0
    skipped = 0
    ok = 0
    lock = asyncio.Lock()

    async def one(agent, config_code, problem, exposure_pos):
        nonlocal executed, skipped, ok
        key = f"{config_code}/{problem.short_id}/agent_{agent.agent_id:04d}"
        if resume and sink.exists(key):
            async with lock:
                skipped += 1
            return
        system_prompt = prompt_assembly.build_system_prompt(
            agent.parameters, config_code, template=template)
        user_turn = prompt_assembly.build_simple_user_turn(
            dilemmas[problem.short_id], problem.labels)
        seed = derive_seed(root_seed, agent.agent_id, config_code, problem.short_id)
        result = await client.complete(
            [Message("system", system_prompt), Message("user", user_turn)],
            temperature=TEMPERATURE, max_tokens=MAX_TOKENS, seed=seed)
        decision, status = parsing.parse_decision(result.text, problem.labels)
        reasoning = parsing.parse_reasoning(result.text)
        rec = build_record(agent=agent, config_code=config_code, problem=problem,
                           exposure_pos=exposure_pos, system_prompt=system_prompt,
                           user_turn=user_turn, result=result, decision=decision,
                           status=status, reasoning=reasoning)
        sink.write(key, rec)
        if result.error:
            sink.write_failure({
                "agent_id": agent.agent_id, "config": config_code,
                "problem": problem.short_id, "error": result.error})
        async with lock:
            executed += 1
            if rec["parse_status"] == "ok":
                ok += 1
            if executed % 50 == 0:
                print(f"  executed {executed} (ok {ok}, skipped {skipped})")

    tasks = []
    for problem in problems:
        for agent in population.agents:
            order = exposure_order(config_codes, seed=root_seed,
                                   agent_id=agent.agent_id, problem_id=problem.short_id)
            for pos, config_code in enumerate(order):
                planned += 1
                tasks.append(one(agent, config_code, problem, pos))
    await asyncio.gather(*tasks)

    summary = {"planned": planned, "executed": executed, "skipped": skipped,
               "ok": ok, "population_hash": population.content_hash()}
    print(f"simple runner: {summary}")
    return summary


def load_or_draw_population(seed: int, n: int = 200) -> Population:
    """Load the hash-locked population if present, else draw and lock it."""
    if POP_FILE.exists():
        return Population.load(POP_FILE)
    pop = Population.draw(n, seed=seed)
    pop.write_locked(POP_FILE)
    return pop
