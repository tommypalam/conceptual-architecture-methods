"""
problems.py — declarative protocol definitions for the complex problems
(spec §6.4) plus the C3 evidence schedule (§6.4.3) and bridge calibration (§6.5).

Each ComplexProblem is a data object the generic orchestrator consumes: how many
agents, how many rounds, which rounds carry a binding vote, the vote labels and
tally rule, termination condition, whether a CEO role and asymmetric evidence
apply, and the per-round action prompt. Keeping the protocol declarative means
the orchestrator (orchestrator.py) has no per-problem branching.

Dilemma bodies are sourced from the locked Phase 0 question files where a direct
single-call baseline exists; the multi-round framing is layered on top (spec
§6.4: Phase 0 was single-call, Phases 2–3 restore the multi-agent structure).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from .questions import load_dilemma_body as _load_body
from .seeding import derive_seed


# --------------------------------------------------------------------------- #
# C3 evidence schedule (spec §6.4.3): 24 items E01..E24, polarity + round.
# Content is placeholder-but-structured: each item is a labelled paragraph slot
# with a fixed polarity and delivery round. Real content is authored at the C3
# design-freeze; the schema, ids, polarities, and round map are what the engine
# and the leakage audit depend on, and those are fixed here.
# --------------------------------------------------------------------------- #

@dataclass(frozen=True)
class EvidenceItem:
    item_id: str
    round_delivered: int          # 1..5 (no new evidence in round 6)
    polarity: str                 # "continue" | "pivot" | "neutral"
    content: str


def _default_c3_schedule() -> list[EvidenceItem]:
    # 24 items across rounds 1–5, balanced polarity. Content strings are
    # explicit placeholders (design-freeze replaces them); ids/rounds/polarity
    # are load-bearing and final.
    polarity_cycle = ["continue", "pivot", "neutral"]
    items = []
    for i in range(1, 25):
        rnd = ((i - 1) % 5) + 1
        pol = polarity_cycle[(i - 1) % 3]
        items.append(EvidenceItem(
            item_id=f"E{i:02d}", round_delivered=rnd, polarity=pol,
            content=f"[E{i:02d} · round {rnd} · {pol}] Placeholder evidence paragraph "
                    f"bearing on the CONTINUE-vs-PIVOT decision; replace at C3 design-freeze."))
    return items


C3_EVIDENCE_SCHEDULE = _default_c3_schedule()


def assign_evidence(items: list[EvidenceItem], n_agents: int, run_seed: int
                    ) -> dict[int, dict[int, list[EvidenceItem]]]:
    """
    Per-round assignment of items to agents (spec §6.4.3): each item goes to
    1–3 of the agents, randomised within configuration with a deterministic
    seed. Returns {round: {agent_index: [items]}}. Recorded in the leakage log.
    """
    import numpy as np
    assignment: dict[int, dict[int, list[EvidenceItem]]] = {}
    for item in items:
        local = derive_seed(run_seed, item.item_id)
        rng = np.random.default_rng(local)
        k = int(rng.integers(1, min(3, n_agents) + 1))
        recipients = sorted(rng.choice(n_agents, size=k, replace=False).tolist())
        rnd = assignment.setdefault(item.round_delivered, {})
        for a in recipients:
            rnd.setdefault(a, []).append(item)
    return assignment


# --------------------------------------------------------------------------- #
# Complex problem definitions
# --------------------------------------------------------------------------- #

@dataclass(frozen=True)
class ComplexProblem:
    short_id: str
    n_agents: int
    max_rounds: int
    vote_labels: tuple[str, str]
    dilemma_body: str
    # rounds (1-indexed) that carry a binding vote counted into the ledger
    vote_rounds: tuple[int, ...]
    # termination: given the per-round vote tallies so far, return True to stop
    terminate: Callable[[list[dict[str, int]]], bool]
    # final outcome resolver: given the ledger, return an outcome dict
    resolve: Callable[["ComplexProblem", list[dict[str, int]], "object"], dict]
    has_ceo: bool = False
    has_evidence: bool = False
    calls_per_run_estimate: int = 0
    runs_per_config: int = 20
    action_prompt: str = ""
    notes: str = ""


def _majority(tally: dict[str, int], labels: tuple[str, str]) -> str | None:
    a, b = labels
    if tally.get(a, 0) > tally.get(b, 0):
        return a
    if tally.get(b, 0) > tally.get(a, 0):
        return b
    return None


# ---- C1 The Resource Council (spec §6.4.1) -------------------------------- #

def _c1_terminate(tallies: list[dict[str, int]]) -> bool:
    # Consensus: all agents vote the same direction in the latest round.
    if not tallies:
        return False
    t = tallies[-1]
    return (t.get("PACKAGE_A", 0) == 0) != (t.get("PACKAGE_B", 0) == 0)  # one side is zero


def _c1_resolve(problem, tallies, run):
    final = tallies[-1] if tallies else {}
    winner = _majority(final, problem.vote_labels)
    return {"final_selection": winner,
            "rounds_to_completion": len(tallies),
            "consensus": winner is not None and (final.get(problem.vote_labels[0], 0) == 0
                                                 or final.get(problem.vote_labels[1], 0) == 0)}


C1 = ComplexProblem(
    short_id="C1", n_agents=5, max_rounds=5,
    vote_labels=("PACKAGE_A", "PACKAGE_B"),
    dilemma_body=_load_body("C1_resource_council.md"),
    vote_rounds=(1, 2, 3, 4, 5),
    terminate=_c1_terminate, resolve=_c1_resolve,
    calls_per_run_estimate=25, runs_per_config=20,
    action_prompt=("Deliberate on the two packages, then cast your binding vote "
                   "for this round.\nRespond in exactly this format:\n"
                   "REASONING: [1-3 sentences grounded in your profile and context]\n"
                   "VOTE: [PACKAGE_A | PACKAGE_B]"),
    notes="5-agent council; consensus (unanimous) ends early, else round-5 vote binds.",
)


# ---- C2 The Restructuring Board (spec §6.4.2) ----------------------------- #

def _c2_terminate(tallies: list[dict[str, int]]) -> bool:
    return False  # always runs to round 5 (binding vote only at round 5)


def _c2_resolve(problem, tallies, run):
    final = tallies[-1] if tallies else {}
    approve = final.get("APPROVE", 0)
    # Plan passes if 3 of 5 non-CEO agents approve (spec §6.4.2 vote logic).
    passed = approve >= 3
    return {"approved": passed, "approve_votes": approve,
            "rounds_to_completion": len(tallies)}


C2 = ComplexProblem(
    short_id="C2", n_agents=6, max_rounds=5,
    vote_labels=("APPROVE", "REJECT"),
    dilemma_body=_load_body("C2_restructuring_board.md"),
    vote_rounds=(5,),
    terminate=_c2_terminate, resolve=_c2_resolve,
    has_ceo=True, calls_per_run_estimate=30, runs_per_config=20,
    action_prompt=("Rounds 1-4 are deliberation: you may argue for or against the plan "
                   "and propose amendments (ACTION: amend) which the CEO may adopt. "
                   "Round 5 is the binding vote.\nRespond in exactly this format:\n"
                   "ACTION: [argue | amend | vote]\n"
                   "REASONING: [1-3 sentences grounded in your profile and context]\n"
                   "VOTE: [APPROVE | REJECT]   (only counted at round 5; put your current lean otherwise)"),
    notes="6 agents incl. randomised CEO; 5 non-CEO vote at round 5; passes if >=3 approve.",
)


# ---- C3 The Scientific-Approach Dilemma (spec §6.4.3) --------------------- #

def _c3_terminate(tallies: list[dict[str, int]]) -> bool:
    return False  # runs all 6 rounds; binding vote at round 6


def _c3_resolve(problem, tallies, run):
    final = tallies[-1] if tallies else {}
    winner = _majority(final, problem.vote_labels)
    tie_break = None
    if winner is None:
        # 2-2 tie: uniform random draw seeded from run_id (spec §6.4.3).
        import numpy as np
        local = derive_seed(run.run_id)
        winner = problem.vote_labels[int(np.random.default_rng(local).integers(0, 2))]
        tie_break = "random"
    return {"final_vote": winner, "tie_break": tie_break,
            "rounds_to_completion": len(tallies)}


C3 = ComplexProblem(
    short_id="C3", n_agents=4, max_rounds=6,
    vote_labels=("CONTINUE", "PIVOT"),
    dilemma_body=_load_body("C3_scientific_approach_dilemma.md"),
    vote_rounds=(6,),
    terminate=_c3_terminate, resolve=_c3_resolve,
    has_evidence=True, calls_per_run_estimate=24, runs_per_config=20,
    action_prompt=("New evidence for this round (if any) is shown above. You may share "
                   "evidence you hold with the group (ACTION: share) and argue. The binding "
                   "vote is at round 6.\nRespond in exactly this format:\n"
                   "ACTION: [share | argue | vote]\n"
                   "REASONING: [1-3 sentences; you may cite evidence ids you legitimately hold]\n"
                   "VOTE: [CONTINUE | PIVOT]   (only counted at round 6; put your current lean otherwise)"),
    notes="4 founders; asymmetric evidence (24 items); leakage audit; round-6 vote; 2-2 tie random.",
)


COMPLEX_PROBLEMS = {"C1": C1, "C2": C2, "C3": C3}
