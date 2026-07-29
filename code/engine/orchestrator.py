"""
orchestrator.py — the Agents-of-Chaos-style multi-agent runner (spec §6.1–6.3).

One Orchestrator instance runs one complex-problem simulation: a fixed set of
agents deliberates across rounds under a single configuration. Structure follows
spec §6.1 exactly:

  - single-threaded, deterministic round ordering (so a mid-run failure can be
    recovered without altering the outcome);
  - call-level parallelism WITHIN a round (all agents' round-N calls dispatched
    concurrently), never across rounds;
  - per-round parameter reinjection (§6.3): every round re-issues each agent's
    full system prompt as the `system` message, because the model has no memory
    across calls — this is load-bearing, not stylistic;
  - a structured transcript summary (§6.2), not raw concatenation, delivered to
    each agent each round to prevent context bloat;
  - a vote ledger and termination check;
  - for C3, asymmetric evidence delivery + a leakage-audit log (§6.4.3);
  - round-to-round consistency audit hook (§6.3).

The orchestrator is problem-agnostic: it consumes a ComplexProblem (problems.py)
and an LLM client (llm_client.py). It works identically with MockClient, so the
full multi-agent machine runs offline for verification.

Bridge calibration (§6.5) is the same orchestrator run with agents whose system
prompt omits the parameter block — see `build_agent_system_prompt(bridge=True)`.
"""

from __future__ import annotations

import asyncio
import hashlib
from dataclasses import dataclass, field

import utils

from . import prompt_assembly, parsing
from .llm_client import Message
from .problems import ComplexProblem, assign_evidence, C3_EVIDENCE_SCHEDULE
from .seeding import derive_seed


@dataclass
class AgentState:
    index: int                       # 0-based seat index within the run
    agent_id: int                    # id in the paired-agent population
    parameters: dict[str, float]
    role: str = "member"             # "member" | "ceo"
    system_prompt: str = ""
    # per-agent private memory (spec §4.1.1): evidence held, delivered by round
    evidence_held: list[str] = field(default_factory=list)


@dataclass
class RoundResponse:
    agent_index: int
    agent_id: int
    role: str
    action_type: str | None
    reasoning: str | None
    vote: str | None
    vote_status: str
    raw: str | None
    api_call_id: str | None
    error: str | None
    evidence_cited: list[str] = field(default_factory=list)
    leakage_flags: list[str] = field(default_factory=list)


@dataclass
class RunResult:
    run_id: str
    problem_id: str
    configuration_id: str
    bridge: bool
    agents: list[dict]
    rounds: list[dict]
    vote_ledger: list[dict[str, int]]
    final_outcome: dict
    leakage_log: list[dict]
    consistency_audit: dict


class Orchestrator:
    def __init__(self, problem: ComplexProblem, configuration_id: str,
                 agent_profiles: list[dict], *, client, run_id: str, seed: int,
                 bridge: bool = False, temperature: float = 1.0, max_tokens: int = 600):
        self.problem = problem
        self.config = configuration_id
        self.client = client
        self.run_id = run_id
        self.seed = seed
        self.bridge = bridge
        self.temperature = temperature
        self.max_tokens = max_tokens

        # Template must exist before agents are instantiated (system prompts
        # are built at construction time and reinjected every round).
        self._template = prompt_assembly.load_template()
        self.transcript: list[dict] = []          # structured per-round records
        self.vote_ledger: list[dict[str, int]] = []
        self.leakage_log: list[dict] = []
        self.shared_evidence_ids: set[str] = set()  # ids surfaced into transcript
        self.agents = self._instantiate_agents(agent_profiles)

        # C3 evidence assignment (deterministic per run).
        self.evidence_by_round: dict[int, dict[int, list]] = {}
        if problem.has_evidence:
            self.evidence_by_round = assign_evidence(
                C3_EVIDENCE_SCHEDULE, problem.n_agents, run_seed=seed)

    # ---- setup ----------------------------------------------------------- #

    def _instantiate_agents(self, profiles: list[dict]) -> list[AgentState]:
        agents = []
        for i, p in enumerate(profiles[: self.problem.n_agents]):
            agents.append(AgentState(index=i, agent_id=p["agent_id"],
                                     parameters=p["parameters"]))
        # CEO role assignment, randomised across runs (spec §6.4.2).
        if self.problem.has_ceo:
            local = int(hashlib.sha256(f"ceo:{self.run_id}".encode()).hexdigest(), 16)
            ceo_idx = local % len(agents)
            agents[ceo_idx].role = "ceo"
        for a in agents:
            a.system_prompt = self.build_agent_system_prompt(a)
        return agents

    def build_agent_system_prompt(self, agent: AgentState) -> str:
        """
        Full parameter-conditioned system prompt (reused every round via
        reinjection). In bridge mode the parameter block is omitted so the run
        measures orchestration-only behaviour (spec §6.5).
        """
        # Bridge runs use a single neutral structural configuration for the
        # normative-context block; the config code may be a non-binary sentinel
        # ("bridge_neutral"), so fall back to the all-low baseline for rendering.
        render_config = self.config if self.config in utils.ALL_CONFIGS else "00000"
        if self.bridge:
            base = prompt_assembly.build_system_prompt(
                agent.parameters, render_config, template=self._template)
            # Strip the parameter block; keep framing + normative context + task.
            head, _, rest = base.partition("# Your decision-making profile")
            _, _, after = rest.partition("# Your normative context")
            return (head.strip() + "\n\n# Your normative context" + after).strip()
        prompt = prompt_assembly.build_system_prompt(
            agent.parameters, render_config, template=self._template)
        role_note = ""
        if agent.role == "ceo":
            role_note = ("\n\n# Your role\nYou are the CEO. You proposed the plan and may "
                         "adopt amendments into the working version during deliberation.")
        return prompt + role_note

    # ---- per-round machinery (spec §6.2) --------------------------------- #

    def _transcript_summary(self, up_to_round: int) -> str:
        """Structured (not raw) summary of prior rounds (spec §6.2)."""
        if not self.transcript:
            return "No prior rounds."
        lines = []
        for rec in self.transcript:
            lines.append(f"Round {rec['round']}:")
            for r in rec["responses"]:
                bits = []
                if r.get("action_type"):
                    bits.append(f"action={r['action_type']}")
                if r.get("vote"):
                    bits.append(f"lean/vote={r['vote']}")
                summary = r.get("reasoning") or ""
                if len(summary) > 240:
                    summary = summary[:240] + "…"
                who = f"Agent {r['agent_id']}" + (" (CEO)" if r["role"] == "ceo" else "")
                lines.append(f"  {who}: {' '.join(bits)} — {summary}")
        if self.shared_evidence_ids:
            lines.append(f"Evidence shared into the record: "
                         f"{', '.join(sorted(self.shared_evidence_ids))}")
        return "\n".join(lines)

    def _round_new_info(self, agent: AgentState, round_num: int) -> str:
        """Evidence privately delivered to this agent this round (C3)."""
        if not self.problem.has_evidence:
            return ""
        items = self.evidence_by_round.get(round_num, {}).get(agent.index, [])
        if not items:
            return ""
        for it in items:
            if it.item_id not in agent.evidence_held:
                agent.evidence_held.append(it.item_id)
            self.leakage_log.append({"round": round_num, "agent_id": agent.agent_id,
                                     "item_delivered": it.item_id})
        rendered = "\n".join(f"- {it.item_id} ({it.polarity}): {it.content}" for it in items)
        return f"New evidence delivered privately to you this round:\n{rendered}"

    def _assemble_user_turn(self, agent: AgentState, round_num: int) -> str:
        parts = [f"# The decision\n{self.problem.dilemma_body}",
                 f"# Deliberation so far (round {round_num} of {self.problem.max_rounds})\n"
                 f"{self._transcript_summary(round_num)}"]
        new_info = self._round_new_info(agent, round_num)
        if new_info:
            parts.append(f"# New information\n{new_info}")
        binding = round_num in self.problem.vote_rounds
        vote_note = ("This round carries the BINDING vote."
                     if binding else "This is a deliberation round; your vote is a non-binding lean.")
        parts.append(f"# Your turn (round {round_num})\n{vote_note}\n\n{self.problem.action_prompt}")
        return "\n\n".join(parts)

    def _derived_seed(self, agent: AgentState, round_num: int) -> int:
        return derive_seed(self.seed, self.run_id, agent.agent_id, f"r{round_num}")

    async def _dispatch_round(self, round_num: int) -> list[RoundResponse]:
        """All agents' round-N calls in parallel; system prompt reinjected each."""
        async def call_agent(agent: AgentState) -> RoundResponse:
            user_turn = self._assemble_user_turn(agent, round_num)
            result = await self.client.complete(
                [Message("system", agent.system_prompt), Message("user", user_turn)],
                temperature=self.temperature, max_tokens=self.max_tokens,
                seed=self._derived_seed(agent, round_num))
            vote, vstatus = parsing.parse_vote(result.text, self.problem.vote_labels)
            reasoning = parsing.parse_reasoning(result.text)
            action = parsing.parse_action_type(result.text)
            cited = parsing.extract_evidence_citations(
                result.text, [it.item_id for it in C3_EVIDENCE_SCHEDULE]) \
                if self.problem.has_evidence else []
            # leakage: cited an item the agent neither holds nor saw shared.
            leak = [c for c in cited
                    if c not in agent.evidence_held and c not in self.shared_evidence_ids]
            # any legitimately shared item mentioned becomes visible going forward
            if action == "share":
                for c in cited:
                    if c in agent.evidence_held:
                        self.shared_evidence_ids.add(c)
            return RoundResponse(
                agent_index=agent.index, agent_id=agent.agent_id, role=agent.role,
                action_type=action, reasoning=reasoning, vote=vote, vote_status=vstatus,
                raw=result.text, api_call_id=result.api_call_id, error=result.error,
                evidence_cited=cited, leakage_flags=leak)
        return list(await asyncio.gather(*(call_agent(a) for a in self.agents)))

    def _tally(self, responses: list[RoundResponse]) -> dict[str, int]:
        """Count votes for this round. C2: only non-CEO agents count (§6.4.2)."""
        a, b = self.problem.vote_labels
        tally = {a: 0, b: 0}
        for r in responses:
            if self.problem.has_ceo and r.role == "ceo":
                continue
            if r.vote in tally:
                tally[r.vote] += 1
        return tally

    # ---- consistency audit (spec §6.3) ----------------------------------- #

    def _consistency_audit(self) -> dict:
        """
        Are an agent's stated leans stable across rounds when parameters have
        not changed? Reports per-agent number of lean-flips as architectural
        noise vs. substantive deliberation (spec §6.3). Reported, not enforced.
        """
        per_agent_votes: dict[int, list[str]] = {}
        for rec in self.transcript:
            for r in rec["responses"]:
                if r.get("vote"):
                    per_agent_votes.setdefault(r["agent_id"], []).append(r["vote"])
        flips = {aid: sum(1 for x, y in zip(v, v[1:]) if x != y)
                 for aid, v in per_agent_votes.items()}
        total_flips = sum(flips.values())
        return {"per_agent_lean_flips": flips, "total_lean_flips": total_flips}

    # ---- main loop (spec §6.1 run()) ------------------------------------- #

    async def run(self) -> RunResult:
        for round_num in range(1, self.problem.max_rounds + 1):
            responses = await self._dispatch_round(round_num)
            resp_records = [{
                "agent_index": r.agent_index, "agent_id": r.agent_id, "role": r.role,
                "action_type": r.action_type, "reasoning": r.reasoning,
                "vote": r.vote, "vote_status": r.vote_status,
                "evidence_cited": r.evidence_cited, "leakage_flags": r.leakage_flags,
                "api_call_id": r.api_call_id, "error": r.error, "raw_response": r.raw,
            } for r in responses]
            self.transcript.append({"round": round_num, "responses": resp_records})
            for r in responses:
                for item_id in r.leakage_flags:
                    self.leakage_log.append({"round": round_num, "agent_id": r.agent_id,
                                             "leakage_violation": item_id})
            if round_num in self.problem.vote_rounds:
                self.vote_ledger.append(self._tally(responses))
            if self.problem.terminate(self.vote_ledger):
                break

        outcome = self.problem.resolve(self.problem, self.vote_ledger, self)
        return RunResult(
            run_id=self.run_id, problem_id=self.problem.short_id,
            configuration_id=self.config, bridge=self.bridge,
            agents=[{"agent_id": a.agent_id, "index": a.index, "role": a.role,
                     "parameters": (None if self.bridge else a.parameters)}
                    for a in self.agents],
            rounds=self.transcript, vote_ledger=self.vote_ledger,
            final_outcome=outcome, leakage_log=self.leakage_log,
            consistency_audit=self._consistency_audit())


def run_result_to_record(rr: RunResult) -> dict:
    """Appendix C.3 multi-agent run record shape."""
    return {
        "schema_version": "1.0",
        "phase": "phase2_complex" if not rr.bridge else "phase2_complex_bridge",
        "problem_id": rr.problem_id,
        "run_id": rr.run_id,
        "configuration_id": rr.configuration_id,
        "bridge_calibration": rr.bridge,
        "agents": rr.agents,
        "rounds": rr.rounds,
        "vote_ledger": rr.vote_ledger,
        "final_outcome": rr.final_outcome,
        "leakage_log": rr.leakage_log,
        "consistency_audit": rr.consistency_audit,
    }
