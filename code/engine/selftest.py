"""
selftest.py — offline structural verification of the engine (no API calls).

Exercises every spec-critical property with the MockClient and asserts on
structure, not model quality:

  - population hash-lock + reload integrity (§5.1)
  - deterministic exposure ordering, same seed -> same order (§5.2)
  - simple runner writes one record per (agent, config, problem) (§5.3–5.4)
  - orchestrator: per-round reinjection present in every call (§6.3)
  - vote ledger + termination (§6.1)
  - C2 CEO vote excluded from the 5-of-non-CEO tally (§6.4.2)
  - C3 evidence delivery + leakage flag when an agent cites unheld evidence (§6.4.3)
  - bridge run omits the parameter block (§6.5)

Run:  python code/engine/selftest.py
"""

from __future__ import annotations

import asyncio
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # code/ on path

from engine import simple_runner, prompt_assembly
from engine.llm_client import MockClient, Message
from engine.population import Population, exposure_order
from engine.orchestrator import Orchestrator
from engine.problems import COMPLEX_PROBLEMS, C3_EVIDENCE_SCHEDULE

PASS, FAIL = "PASS", "FAIL"
results = []


def check(name, cond):
    results.append((name, bool(cond)))
    print(f"  [{PASS if cond else FAIL}] {name}")


def test_population():
    pop = Population.draw(20, seed=123)
    h1 = pop.content_hash()
    pop2 = Population.draw(20, seed=123)
    check("population draw is deterministic (same seed -> same hash)", h1 == pop2.content_hash())
    check("population draw differs by seed", h1 != Population.draw(20, seed=124).content_hash())
    with tempfile.TemporaryDirectory() as d:
        path = Path(d) / "agents.json"
        pop.write_locked(path)
        reloaded = Population.load(path)
        check("population reload preserves hash (lock integrity)",
              reloaded.content_hash() == h1)
        # second write with same content is idempotent
        pop.write_locked(path)
        check("re-lock with identical population is idempotent", True)


def test_exposure():
    configs = ["00100", "11011", "00000", "11111", "01010"]
    o1 = exposure_order(configs, seed=42, agent_id=7, problem_id="S1")
    o2 = exposure_order(configs, seed=42, agent_id=7, problem_id="S1")
    o3 = exposure_order(configs, seed=42, agent_id=8, problem_id="S1")
    check("exposure order deterministic per (seed,agent,problem)", o1 == o2)
    check("exposure order is a permutation", sorted(o1) == sorted(configs))
    check("exposure order varies across agents", o1 != o3)


def test_prompt_assembly():
    params = {n: 0.5 for n in prompt_assembly.utils.PARAM_NAMES}
    sysp = prompt_assembly.build_system_prompt(params, "00100")
    check("no [X_VALUE] placeholders remain", "_VALUE]" not in sysp)
    check("no [AXIS] placeholders remain",
          not any(f"[{a.upper()}]" in sysp for a in prompt_assembly.AXIS_ORDER))
    check("authority rendered HIGH for 00100", "Authority: HIGH" in sysp)
    check("freedom rendered LOW for 00100", "Freedom:   LOW" in sysp or "Freedom: LOW" in sysp)


def test_simple_runner():
    async def go():
        client = MockClient(concurrency=8)
        pop = Population.draw(4, seed=5)
        with tempfile.TemporaryDirectory() as d:
            out = Path(d)
            summary = await simple_runner.run_simple(
                client=client, config_codes=["00100", "11011"], root_seed=5,
                population=pop, out_root=out)
            # 4 agents x 3 problems x 2 configs = 24
            check("simple runner planned == 4*3*2 = 24", summary["planned"] == 24)
            check("simple runner executed all", summary["executed"] == 24)
            files = list(out.rglob("agent_*.json"))
            check("simple runner wrote one file per call", len(files) == 24)
            # re-run resumes (skips existing)
            s2 = await simple_runner.run_simple(
                client=client, config_codes=["00100", "11011"], root_seed=5,
                population=pop, out_root=out)
            check("simple runner resume skips existing", s2["skipped"] == 24 and s2["executed"] == 0)
    asyncio.run(go())


def test_reinjection_and_votes():
    async def go():
        # Responder that records how many system messages it sees, and votes C1.
        seen = {"system_msgs": 0, "calls": 0}

        def responder(messages, seed):
            seen["calls"] += 1
            seen["system_msgs"] += sum(1 for m in messages if m.role == "system")
            return "ACTION: vote\nREASONING: mock.\nVOTE: PACKAGE_A"

        client = MockClient(responder=responder, concurrency=8)
        pop = Population.draw(5, seed=9)
        profiles = [a.as_record() for a in pop.agents]
        orch = Orchestrator(COMPLEX_PROBLEMS["C1"], "00100", profiles,
                            client=client, run_id="C1_test", seed=9)
        rr = await orch.run()
        check("every call carries exactly one reinjected system prompt (§6.3)",
              seen["system_msgs"] == seen["calls"] and seen["calls"] > 0)
        check("C1 reaches consensus and terminates early on unanimous vote",
              rr.final_outcome["consensus"] is True and rr.final_outcome["rounds_to_completion"] == 1)
        check("C1 winner is PACKAGE_A", rr.final_outcome["final_selection"] == "PACKAGE_A")
    asyncio.run(go())


def test_c2_ceo_exclusion():
    async def go():
        # All 6 agents vote APPROVE; only 5 non-CEO should count.
        client = MockClient(
            responder=lambda m, s: "ACTION: vote\nREASONING: mock.\nVOTE: APPROVE",
            concurrency=8)
        pop = Population.draw(6, seed=11)
        profiles = [a.as_record() for a in pop.agents]
        orch = Orchestrator(COMPLEX_PROBLEMS["C2"], "00100", profiles,
                            client=client, run_id="C2_test", seed=11)
        rr = await orch.run()
        final_tally = rr.vote_ledger[-1]
        check("C2 round-5 tally counts exactly 5 non-CEO votes (CEO excluded §6.4.2)",
              final_tally.get("APPROVE", 0) == 5)
        check("C2 runs to round 5 (single binding vote round)",
              rr.final_outcome["rounds_to_completion"] == 1)  # ledger has one entry (round 5)
        check("C2 approved (5 >= 3)", rr.final_outcome["approved"] is True)
        ceo_count = sum(1 for a in rr.agents if a["role"] == "ceo")
        check("C2 has exactly one CEO", ceo_count == 1)
    asyncio.run(go())


def test_c3_leakage():
    async def go():
        # An agent cites E24 (which no one is guaranteed to hold) every round.
        client = MockClient(
            responder=lambda m, s: "ACTION: argue\nREASONING: I recall E24 clearly.\nVOTE: CONTINUE",
            concurrency=8)
        pop = Population.draw(4, seed=13)
        profiles = [a.as_record() for a in pop.agents]
        orch = Orchestrator(COMPLEX_PROBLEMS["C3"], "00100", profiles,
                            client=client, run_id="C3_test", seed=13)
        rr = await orch.run()
        check("C3 runs 6 rounds", len(rr.rounds) == 6)
        check("C3 evidence schedule has 24 items", len(C3_EVIDENCE_SCHEDULE) == 24)
        # E24 is delivered in round 4 (24 -> (24-1)%5+1 = 4). Before round 4, any
        # agent citing E24 without holding it should be flagged as leakage.
        early_flags = [e for e in rr.leakage_log
                       if e.get("leakage_violation") == "E24" and e["round"] < 4]
        check("C3 flags pre-delivery citation of E24 as leakage (§6.4.3)", len(early_flags) > 0)
        check("C3 produced a final vote", rr.final_outcome["final_vote"] in ("CONTINUE", "PIVOT"))
    asyncio.run(go())


def test_bridge():
    async def go():
        client = MockClient(concurrency=8)
        pop = Population.draw(5, seed=17)
        profiles = [a.as_record() for a in pop.agents]
        orch = Orchestrator(COMPLEX_PROBLEMS["C1"], "bridge_neutral", profiles,
                            client=client, run_id="C1_bridge", seed=17, bridge=True)
        # Inspect the first agent's system prompt.
        sp = orch.agents[0].system_prompt
        check("bridge system prompt omits the parameter block (§6.5)",
              "# Your decision-making profile" not in sp)
        check("bridge system prompt keeps normative context",
              "# Your normative context" in sp)
        rr = await orch.run()
        check("bridge run records parameters as None", rr.agents[0]["parameters"] is None)
    asyncio.run(go())


def main():
    print("Engine self-test (MockClient, no API calls)\n")
    for fn in (test_population, test_exposure, test_prompt_assembly, test_simple_runner,
               test_reinjection_and_votes, test_c2_ceo_exclusion, test_c3_leakage, test_bridge):
        print(f"{fn.__name__}:")
        fn()
    n_pass = sum(1 for _, ok in results if ok)
    n = len(results)
    print(f"\n=== {n_pass}/{n} checks passed ===")
    if n_pass != n:
        print("FAILURES:", [name for name, ok in results if not ok])
        sys.exit(1)


if __name__ == "__main__":
    main()
