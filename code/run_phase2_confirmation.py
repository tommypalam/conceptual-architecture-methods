"""Prepare, verify, run or analyze the separately frozen fresh-sample Phase 2 confirmation.

Examples (dependencies in the ignored workspace target):
  py -3.11 -B code/run_phase2_confirmation.py prepare
  py -3.11 -B code/run_phase2_confirmation.py mock
  py -3.11 -B code/run_phase2_confirmation.py run --yes
  py -3.11 -B code/run_phase2_confirmation.py analyze
"""
from __future__ import annotations

import argparse
import asyncio
import hashlib
import importlib.metadata
import json
import logging
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "output" / "phase2_runtime"))

import numpy as np
import pandas as pd
import utils
from engine.population import Population
from phase2_confirmation_design import PACKAGE, SEED, CONDITIONS, FILES, make_design, simple_messages, execute
from phase2_confirmation_transport import Ledger, StopRun, digest, write_once, read_record, now, MODEL, reservation
from analyze_phase2_confirmation import analyze

RAW = ROOT / "data" / "raw" / "phase2_confirmation_20260913"


def source_files():
    files = [ROOT / "code" / name for name in ("run_phase2_confirmation.py", "phase2_confirmation_design.py",
             "phase2_confirmation_transport.py", "analyze_phase2_confirmation.py", "phase2_group_fields_v2.py", "phase2_pilot_design.py", "phase2_pilot_transport.py", "phase2_confirmation_power.py", "utils.py")]
    files += sorted((ROOT / "code" / "engine").glob("*.py"))
    files += sorted((ROOT / "config").glob("*.json"))
    files += [ROOT / "prompts" / "system_prompt_template.md", PACKAGE / "PROTOCOL.md", ROOT / "experiments" / "phase2_exploratory_20260912" / "evidence_schedule.json"]
    files += [ROOT / "experiments" / "phase0b_calibration" / "questions" / name for name in FILES.values()]
    files += [ROOT / "experiments" / "phase2_exploratory_20260912" / "analysis" / "integrity_audit.json",
              ROOT / "experiments" / "phase2_exploratory_20260912" / "population.json",
              ROOT / "code" / "audit_phase2_confirmation.py"]
    return {str(p.relative_to(ROOT)).replace("\\", "/"): hashlib.sha256(p.read_bytes()).hexdigest() for p in files}


def runtime_versions():
    return {name: importlib.metadata.version(name) for name in ("numpy", "scipy", "pandas", "openai", "httpx", "tiktoken")}


def prepare():
    if (PACKAGE / "manifest.json").exists():
        return verify()
    population, groups = make_design()
    pop = population.to_dict()
    prior = Population.load(ROOT / "experiments" / "phase2_exploratory_20260912" / "population.json")
    vectors = lambda p: {tuple(a.parameters[k] for k in utils.PARAM_NAMES) for a in p.agents}
    assert not (vectors(population) & vectors(prior))
    import decimal
    prior_cost = json.loads((ROOT / "experiments" / "phase2_exploratory_20260912" / "analysis" / "integrity_audit.json").read_text(encoding="utf-8"))
    assert decimal.Decimal(str(prior_cost["conservative_accounted_usd"])) == decimal.Decimal("4.15084065")
    prior_audit = read_record(ROOT / "experiments" / "phase2_exploratory_20260912" / "manifest.json")
    if prior_audit["root_seed"] == SEED:
        raise StopRun("Confirmation must use an independent population seed")
    from phase2_confirmation_power import power
    schedule = {"root_seed": SEED, "groups": groups}
    population.write_locked(PACKAGE / "population.json")
    write_once(PACKAGE / "schedule.json", schedule)
    matrix = population.parameter_matrix()
    utils.log_dataframe_summary(pd.DataFrame(matrix, columns=utils.PARAM_NAMES), "Confirmation population; no filtering", logging.getLogger("pilot"))
    examples, reserves = [], []
    for problem in ("S1", "S2", "S3"):
        for config, arm in CONDITIONS:
            messages = simple_messages(population.agents[0], config, arm, problem)
            examples.append({"problem": problem, "config": config, "arm": arm, "messages": messages})
        for agent in population.agents:
            for config, arm in CONDITIONS:
                request = {"messages": simple_messages(agent, config, arm, problem), "max_completion_tokens": 600}
                reserves.append(reservation(request)[1])
    write_once(PACKAGE / "prompt_examples.json", examples)
    diagnostics = {"root_seed": SEED, "n_profiles": 400, "simple_calls": 4800, "group_max_calls": 7900,
                   "maximum_calls": 12700, "groups_per_problem_per_condition": 20,
                   "minimum_R_eigenvalue": float(np.linalg.eigvalsh(utils.R).min()),
                   "population_sha256": population.content_hash(), "schedule_sha256": digest(schedule),
                   "simple_all_max_reservations_usd": sum(reserves) / 1e9,
                   "confirmation_cap_usd": 30, "prior_phase2_accounted_usd": 4.15084065, "new_package_absolute_cap_usd": 100,
                   "full_group_reservation_is_not_claimed": True,
                   "means": dict(zip(utils.PARAM_NAMES, matrix.mean(axis=0).tolist())),
                   "minimum": float(matrix.min()), "maximum": float(matrix.max()),
                   "individual_power_delta10pp_discordance30pp": power(400, .2, .1, .05/6),
                   "group_power_scenarios": [{"difference": d, "discordance": q,
                                              "power_at_alpha_05_over_7": power(20, (q+d)/2, (q-d)/2, .05/7)}
                                             for d, q in [(.2, .4), (.4, .5), (.6, .6)]]}
    write_once(PACKAGE / "preflight.json", diagnostics)
    manifest = {"designation": "phase2_confirmation_20260913", "frozen_at": now(), "root_seed": SEED,
                "model": MODEL, "source_hashes": source_files(), "runtime": runtime_versions(),
                "population_hash": digest(pop), "schedule_hash": digest(schedule), "diagnostics": diagnostics,
                "authorization": "Researcher instruction: lets go ahead and complete phase 2 run it; 2026-09-13. Revised two-anchor study, fresh profiles, pilot-informed group repairs, local prospective freeze."}
    write_once(PACKAGE / "manifest.json", manifest)
    print(json.dumps({"manifest_sha256": digest(manifest), **diagnostics}), flush=True)
    return manifest


def verify():
    manifest = read_record(PACKAGE / "manifest.json")
    if manifest["source_hashes"] != source_files():
        changed = sorted(k for k in set(manifest["source_hashes"]) | set(source_files())
                         if manifest["source_hashes"].get(k) != source_files().get(k))
        raise StopRun("Frozen source/assets changed: " + ", ".join(changed))
    if manifest["runtime"] != runtime_versions():
        raise StopRun("Runtime versions differ from frozen manifest")
    pop = Population.load(PACKAGE / "population.json")
    schedule = read_record(PACKAGE / "schedule.json")
    if digest(pop.to_dict()) != manifest["population_hash"] or digest(schedule) != manifest["schedule_hash"]:
        raise StopRun("Population/schedule changed")
    return manifest


async def run(manifest, *, mock=False):
    raw = ROOT / "output" / ("phase2_mock_" + now().replace(":", "").replace("+", "_")) if mock else RAW
    pop = Population.load(PACKAGE / "population.json")
    groups = read_record(PACKAGE / "schedule.json")["groups"]
    print(json.dumps({"phase": "phase2_confirmation", "mock": mock, "configuration_codes": ["00100", "11011", "neutral_bridge"],
                      "N_profiles": 400, "N_group_runs": 300, "max_calls": 12700, "root_seed": SEED,
                      "manifest_sha256": digest(manifest), "confirmation_cap_usd": 30, "prior_phase2_accounted_usd": 4.15084065, "raw_root": str(raw)}), flush=True)
    ledger = Ledger(raw, digest(manifest), mock=mock)
    stopped = None
    if mock:
        ledger.cap = 100_000_000_000  # Synthetic fixed usage; live ceiling stays $30.
    try:
        await execute(ledger, pop, groups)
        if mock:
            before = ledger.n_new
            await execute(ledger, pop, groups)
            assert ledger.n_new == before
            print(json.dumps({"mock_replay_new_calls": 0}), flush=True)
    except StopRun as exc:
        stopped = str(exc)
        print(json.dumps({"stopped": stopped}), flush=True)
    finally:
        if ledger.client:
            await ledger.client.close()
        ledger.close()
    out = raw / "analysis" if mock else PACKAGE / "analysis"
    summary = analyze(raw, out)
    if stopped or not summary["complete_allocation"]:
        raise StopRun(stopped or "Incomplete allocation")
    return summary


def main():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout, format="%(message)s")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["prepare", "verify", "mock", "run", "analyze", "audit"])
    parser.add_argument("--yes", action="store_true", help="Use the researcher-authorised paid pilot mode")
    args = parser.parse_args()
    logging.getLogger("httpx").setLevel(logging.WARNING)
    if args.command == "audit":
        from audit_phase2_confirmation import audit
        asyncio.run(audit())
    elif args.command == "prepare":
        prepare()
    elif args.command == "analyze":
        verify()
        analyze(RAW, PACKAGE / "analysis")
    else:
        manifest = verify()
        if args.command == "verify":
            print(json.dumps({"verified": digest(manifest)}))
        else:
            if args.command == "run" and (not args.yes or not os.environ.get("OPENAI_API_KEY")):
                parser.error("Live execution needs --yes and an existing OPENAI_API_KEY; never paste the key into logs")
            asyncio.run(run(manifest, mock=args.command == "mock"))


if __name__ == "__main__":
    main()
