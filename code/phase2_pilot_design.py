"""Frozen prospective pilot design and deterministic group state transitions.

Historical engine modules are reused read-only; their old behaviour is unchanged.
"""
from __future__ import annotations

import asyncio
import json
import re
from pathlib import Path

import numpy as np

from engine.population import Population
from engine.prompt_assembly import build_system_prompt
from engine.phase0b import split_blocks, _NEUTRAL_CONTEXT
from engine.questions import load_dilemma_body, PHASE0B_QUESTIONS
from engine.seeding import derive_seed
from engine.simple_runner import SIMPLE_PROBLEMS
from engine.problems import COMPLEX_PROBLEMS, EvidenceItem, assign_evidence
from phase2_pilot_transport import digest, write_once, read_record, StopRun

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "experiments" / "phase2_exploratory_20260912"
SEED = 2026091202
CONDITIONS = [("00100", "E"), ("00100", "U"), ("11011", "E"), ("11011", "U")]
GROUP_CONDITIONS = CONDITIONS + [("neutral", "B")]
FILES = {p.short_id: p.question_file for p in SIMPLE_PROBLEMS}
FILES.update({"C1": "C1_resource_council.md", "C2": "C2_restructuring_board.md",
              "C3": "C3_scientific_approach_dilemma.md"})
LABELS = {p.short_id: p.labels for p in SIMPLE_PROBLEMS}
LABELS.update({p.short_id: p.vote_labels for p in COMPLEX_PROBLEMS.values()})
NO_PROFILE_TASK = ("# Your task\n\nYou will be presented with a decision. Consider the situation "
                   "and normative context. Do not infer demographic identity, personality, "
                   "ideology, or narrative backstory. Do not refuse to decide. "
                   "Answer in the exact format specified.")


def shuffled(items, *seed_parts):
    rng = np.random.default_rng(derive_seed(SEED, *seed_parts))
    return [items[i] for i in rng.permutation(len(items))]


def system_prompt(agent, config, arm, *, role=None):
    if arm not in ("E", "U", "B") or (config == "neutral") != (arm == "B"):
        raise ValueError("Invalid arm/context")
    prompt = build_system_prompt(agent.parameters, config if arm != "B" else "00100")
    if arm != "E":
        blocks = split_blocks(prompt)
        prompt = "\n\n".join([blocks["preamble"],
                               _NEUTRAL_CONTEXT if arm == "B" else blocks["context"],
                               NO_PROFILE_TASK])
    if role:
        prompt += "\n\n# Your role\n" + role
    return prompt


def simple_messages(agent, config, arm, problem):
    a, b = LABELS[problem]
    body = load_dilemma_body(FILES[problem], PHASE0B_QUESTIONS)
    # Symmetric task wording avoids asking U to ground its answer in absent values.
    user = (f"{body}\n\nRespond in exactly this format:\nDECISION: [{a} | {b}]\n"
            "REASONING: [2-3 sentences explaining why]")
    return [{"role": "system", "content": system_prompt(agent, config, arm)},
            {"role": "user", "content": user}]


def evidence_items():
    data = json.loads((PACKAGE / "evidence_schedule.json").read_text(encoding="utf-8"))
    items = [EvidenceItem(**x) for x in data]
    assert [x.item_id for x in items] == [f"E{i:02}" for i in range(1, 25)]
    assert [x.round_delivered for x in items] == [(i % 5) + 1 for i in range(24)]
    assert [x.polarity for x in items] == ["continue", "pivot", "neutral"] * 8
    assert all(len(x.content) > 80 and "placeholder" not in x.content.lower() for x in items)
    return items


def make_design():
    population = Population.draw(50, seed=SEED)
    items = evidence_items()
    groups = []
    for problem, n in [("C1", 5), ("C2", 6), ("C3", 4)]:
        order = shuffled(list(range(1, 51)), "membership", problem)
        for group in range(1, 6):
            ids = order[(group - 1) * n:group * n]
            seed = derive_seed(SEED, "group", problem, group)
            ceo = ids[int(np.random.default_rng(derive_seed(seed, "ceo")).integers(n))] if problem == "C2" else None
            assignment = assign_evidence(items, 4, derive_seed(seed, "evidence")) if problem == "C3" else {}
            direct = {str(a): {} for a in ids}
            for rnd, recipients in assignment.items():
                for idx, subset in recipients.items():
                    direct[str(ids[idx])][str(rnd)] = [x.item_id for x in subset]
            if problem == "C3":
                assert all(sum(map(len, rounds.values())) < 24 for rounds in direct.values())
                for item in items:
                    count = sum(item.item_id in rounds.get(str(item.round_delivered), []) for rounds in direct.values())
                    assert 1 <= count <= 3
            groups.append({"problem": problem, "group": group, "agent_ids": ids, "seed": seed,
                           "ceo": ceo, "direct_evidence": direct,
                           "conditions": shuffled(GROUP_CONDITIONS, "conditions", problem, group),
                           "tie_seed": derive_seed(seed, "tie")})
    return population, shuffled(groups, "group_order")


def fields(text):
    # Bound each field at the next recognized heading; reject duplicate headings.
    pattern = r"(?m)^(DECISION|ACTION|AMENDMENT|ADOPT|SHARE|REASONING|VOTE):\s*"
    matches = list(re.finditer(pattern, text or ""))
    names = [m[1] for m in matches]
    if len(names) != len(set(names)):
        return {}, "duplicate_field"
    return {m[1]: text[m.end():matches[i + 1].start() if i + 1 < len(matches) else len(text)].strip()
            for i, m in enumerate(matches)}, None


def parse(result, labels, *, simple=False):
    choices = ((result.get("response") or {}).get("choices") or [{}])
    choice = choices[0]
    message = choice.get("message") or {}
    text = message.get("content") or ""
    values, error = fields(text)
    status = "ok"
    if result.get("error"):
        status = "failed_api"
    elif result.get("integrity_error"):
        status = "integrity_error"
    elif message.get("refusal"):
        status = "refusal"
    elif choice.get("finish_reason") != "stop":
        status = "incomplete_generation"
    elif error:
        status = error
    elif values.get("DECISION" if simple else "VOTE") not in labels or not values.get("REASONING"):
        status = "parse_failure"
    elif not simple and labels[0] == "APPROVE" and (
            values.get("ACTION") not in ("argue", "amend", "vote") or
            not values.get("AMENDMENT") or not values.get("ADOPT")):
        status = "action_schema_failure"
    elif not simple and labels[0] == "CONTINUE" and (
            values.get("ACTION") not in ("share", "argue", "vote") or not values.get("SHARE")):
        status = "action_schema_failure"
    vote = values.get("DECISION" if simple else "VOTE") if status == "ok" else None
    return {"vote": vote, "status": status, "fields": values, "text": text}


def initial_state(group):
    return {"history": [], "public_evidence": [], "mentioned_ids": [], "proposals": {},
            "adopted": [], "audit": [], "tallies": [], "group": group}


def held_items(group, agent_id, rnd):
    return {item for round_s, items in group["direct_evidence"][str(agent_id)].items()
            if int(round_s) <= rnd for item in items}


def group_messages(agent, config, arm, group, state, rnd):
    problem = group["problem"]
    definition = COMPLEX_PROBLEMS[problem]
    is_ceo = group["ceo"] == agent.agent_id
    role = (f"You are agent {agent.agent_id} in a group of {definition.n_agents}. "
            "Responses within a round are simultaneous; you see only earlier rounds.")
    if problem == "C2":
        role += (" You are the CEO who proposed the original plan. You may adopt earlier amendments in rounds 2-4. Your vote is not counted."
                 if is_ceo else f" Agent {group['ceo']} is the CEO. You are one of five voting board members.")
    else:
        role += " You are a voting council member." if problem == "C1" else " You are one of four voting founders."
    sections = [load_dilemma_body(FILES[problem], PHASE0B_QUESTIONS),
                f"\nGroup protocol: round {rnd} of {definition.max_rounds}.",
                "Earlier-round structured transcript (reasoning excerpts may be truncated):\n" +
                ("\n".join(state["history"]) or "No previous rounds.")]
    if problem == "C2":
        sections += ["The dilemma above is the original proposal. For this group task, APPROVE or REJECT concerns "
                     "that proposal plus the adopted amendments below. Claims made during discussion are "
                     "proposals or opinions, not newly verified financial or operational facts.",
                     "Amendment proposals (ID: text):\n" + json.dumps(state["proposals"], ensure_ascii=False),
                     "Currently adopted amendment IDs: " + (", ".join(state["adopted"]) or "NONE"),
                     "Rounds 1-4: deliberate; you may propose one amendment. The CEO may adopt any previously "
                     "listed proposal in rounds 2-4. Round 5: the five non-CEO members cast binding votes; "
                     "at least three APPROVE votes pass the working plan. No new amendments or adoptions bind in round 5.",
                     "Respond in exactly this format:\nACTION: [argue | amend | vote]\n"
                     "AMENDMENT: [one proposed amendment, or NONE]\nADOPT: [previously listed amendment IDs, or NONE; CEO only]\n"
                     "REASONING: [1-3 sentences explaining why]\nVOTE: [APPROVE | REJECT; current lean before round 5]"]
    elif problem == "C3":
        own = held_items(group, agent.agent_id, rnd)
        public = set(state["public_evidence"])
        item_map = {x.item_id: x.content for x in evidence_items()}
        sections += ["Private evidence you have received (retained across rounds):\n" +
                     "\n".join(f"{eid}: {item_map[eid]}" for eid in sorted(own)),
                     "Authenticated evidence shared publicly in earlier rounds:\n" +
                     ("\n".join(f"{eid}: {item_map[eid]}" for eid in sorted(public)) or "NONE"),
                     "You may disclose evidence you hold. SHARE lists IDs to share; citing a held item in your "
                     "public reasoning also discloses it. Public evidence becomes visible next round. "
                     "Other agents' claims are not verified facts unless present in the evidence supplied here. "
                     "Rounds 1-5 are deliberation; round 6 is binding. A 2-2 tie uses a uniform random tie-break.",
                     "Respond in exactly this format:\nACTION: [share | argue | vote]\nSHARE: [evidence IDs, or NONE]\n"
                     "REASONING: [1-3 sentences; cite evidence IDs when discussing an item]\n"
                     "VOTE: [CONTINUE | PIVOT; current lean before round 6]"]
    else:
        sections += ["Each round has a binding vote. Unanimous agreement by all five members ends the council. "
                     "Otherwise the fifth round's majority determines the choice.",
                     "Respond in exactly this format:\nREASONING: [1-3 sentences explaining why]\n"
                     "VOTE: [PACKAGE_A | PACKAGE_B]"]
    return [{"role": "system", "content": system_prompt(agent, config, arm, role=role)},
            {"role": "user", "content": "\n\n".join(sections)}]


def advance(state, responses, rnd):
    """Apply a round barrier. Input order is irrelevant; no await/shared mutation."""
    group = state["group"]
    problem = group["problem"]
    prior_public = set(state["public_evidence"])
    prior_mentions = set(state["mentioned_ids"])
    prior_proposals = set(state["proposals"])
    new_public, new_mentions = set(), set()
    a, b = LABELS[problem]
    tally = {a: 0, b: 0, "missing": 0}
    for agent_id, response in sorted(responses.items()):
        f = response["fields"]
        reason = f.get("REASONING", "")
        excerpt = reason[:360] + (" [truncated]" if len(reason) > 360 else "")
        state["history"].append(f"Round {rnd}, agent {agent_id}: action={f.get('ACTION', 'vote')}; "
                                f"vote={response['vote']}; status={response['status']}; reasoning={excerpt}")
        if agent_id != group["ceo"]:
            tally[response["vote"] if response["vote"] in (a, b) else "missing"] += 1
        if problem == "C2" and response["status"] == "ok":
            proposed = f.get("AMENDMENT", "NONE").strip()
            if rnd < 5 and f.get("ACTION") == "amend" and proposed not in ("", "NONE"):
                state["proposals"][f"R{rnd}A{agent_id}"] = proposed
            adopted = set(re.findall(r"\bR\d+A\d+\b", f.get("ADOPT", "")))
            allowed = prior_proposals if agent_id == group["ceo"] and 2 <= rnd <= 4 else set()
            for pid in sorted(adopted & allowed):
                if pid not in state["adopted"]:
                    state["adopted"].append(pid)
            if adopted - allowed:
                state["audit"].append({"round": rnd, "agent": agent_id, "invalid_adoptions": sorted(adopted - allowed)})
        if problem == "C3" and response["status"] == "ok":
            cited = set(re.findall(r"\bE\d{2}\b", reason + " " + f.get("SHARE", "")))
            own = held_items(group, agent_id, rnd)
            legal = own | prior_public
            authenticated = cited & legal
            new_public |= authenticated
            new_mentions |= cited
            state["history"].append(f"Round {rnd}, agent {agent_id}: cited/shared IDs={','.join(sorted(cited)) or 'NONE'}; "
                                    f"authenticated disclosures={','.join(sorted(authenticated)) or 'NONE'}")
            state["audit"].append({"round": rnd, "agent": agent_id,
                                   "direct_held": sorted(own), "public_before": sorted(prior_public),
                                   "authenticated_disclosures": sorted(authenticated),
                                   "transcript_only_citations": sorted(cited & prior_mentions - legal),
                                   "unavailable_citations": sorted(cited - legal - prior_mentions)})
    state["public_evidence"] = sorted(prior_public | new_public)
    state["mentioned_ids"] = sorted(prior_mentions | new_mentions)
    state["tallies"].append(tally)
    return problem == "C1" and tally["missing"] == 0 and max(tally[a], tally[b]) == 5


def resolve(state):
    group = state["group"]
    problem = group["problem"]
    a, b = LABELS[problem]
    tally = state["tallies"][-1]
    result = {"outcome": None, "status": "incomplete" if tally["missing"] else "ok",
              "final_tally": tally, "rounds": len(state["tallies"]), "tie_break": False,
              "consensus": False, "proposals": len(state["proposals"]),
              "adoptions": len(state["adopted"]), "public_evidence": len(state["public_evidence"])}
    if tally["missing"]:
        return result
    if tally[a] == tally[b]:
        if problem != "C3" or tally[a] != 2:
            raise ValueError("Impossible complete tally")
        result["outcome"] = (a, b)[int(np.random.default_rng(group["tie_seed"]).integers(2))]
        result["tie_break"] = True
    else:
        result["outcome"] = a if tally[a] > tally[b] else b
    result["consensus"] = problem == "C1" and max(tally[a], tally[b]) == 5
    return result


async def run_group(ledger, population, group, config, arm):
    agents = {x.agent_id: x for x in population.agents}
    state = initial_state(group)
    problem = group["problem"]
    for rnd in range(1, COMPLEX_PROBLEMS[problem].max_rounds + 1):
        jobs = []
        ids = sorted(group["agent_ids"])
        for agent_id in ids:
            slot = ["complex", problem, group["group"], config, arm, rnd, agent_id]
            meta = {"stage": "complex", "problem": problem, "group": group["group"],
                    "config": config, "arm": arm, "round": rnd, "agent": agent_id,
                    "labels": list(LABELS[problem]), "state_hash_before": digest(state)}
            jobs.append(ledger.complete(slot, group_messages(agents[agent_id], config, arm, group, state, rnd),
                                        derive_seed(SEED, *slot), meta))
        results = await asyncio.gather(*jobs, return_exceptions=True)
        failures = [r for r in results if isinstance(r, BaseException)]
        if failures:
            raise failures[0]
        parsed = {agent_id: parse(result, LABELS[problem]) for agent_id, result in zip(ids, results)}
        done = advance(state, parsed, rnd)
        if ledger.halted:
            raise StopRun("Stopped after preserving current round responses")
        if done:
            break
    outcome = {"problem": problem, "group": group["group"], "config": config, "arm": arm,
               "result": resolve(state), "state": state}
    key = digest([problem, group["group"], config, arm])
    path = ledger.root / "groups" / f"{key}.json"
    if path.exists():
        if digest(read_record(path)) != digest(outcome):
            raise StopRun("Replayed group state differs")
    else:
        write_once(path, outcome)
    print(json.dumps({"group_complete": [problem, group["group"], config, arm],
                      "responses": len(ledger.results), "accounted_usd": ledger.charged / 1e9}), flush=True)
    return outcome


async def execute(ledger, population, groups):
    blocks = shuffled([(p, a.agent_id) for p in ("S1", "S2", "S3") for a in population.agents], "simple_blocks")
    agents = {a.agent_id: a for a in population.agents}
    # Round-robin batches of whole profiles; each arm gets an isolated conversation.
    for problem, agent_id in blocks:
        jobs = []
        for config, arm in shuffled(CONDITIONS, "simple_conditions", problem, agent_id):
            slot = ["simple", problem, agent_id, config, arm]
            meta = {"stage": "simple", "problem": problem, "agent": agent_id,
                    "config": config, "arm": arm, "labels": list(LABELS[problem])}
            jobs.append(ledger.complete(slot, simple_messages(agents[agent_id], config, arm, problem),
                                        derive_seed(SEED, *slot), meta))
        results = await asyncio.gather(*jobs, return_exceptions=True)
        failures = [r for r in results if isinstance(r, BaseException)]
        if failures:
            raise failures[0]
        if ledger.halted:
            raise StopRun("Stopped after preserving current simple block")
    for group in groups:
        for config, arm in group["conditions"]:
            await run_group(ledger, population, group, config, arm)
