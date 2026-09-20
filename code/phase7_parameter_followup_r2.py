"""Collector for parameter_followup_r2: TfA and MoR pinned at 80 agents.

Design, priors, power and the locked prediction live in
`phase7_parameter_followup`. This module dispatches. 2,240 calls on gpt-5.4-mini:
80 agents x 2 coordinates x 2 levels x 7 items.

These are the sweep's two near-misses: TfA -0.1029 (Holm 0.1112) and MoR -0.0971
(Holm 0.0690) at 25 agents. Both have uncorrected intervals excluding zero and
neither survived correction - the thesis records them as "below the certified
threshold", not flat. At 25 agents an effect of 0.10 is barely detectable; at 80
it is 18/20. This settles them or bounds them, and is the last unfinished
business inside the ten.

Built on `phase7_semantics_r1` by import, carrying its disclosed choices: a
256-token output cap, no review call (the seven items are byte-identical to
accepted material; the verdict is read from the ledger), and a fresh population
seed. The designation is set by DESIGNATION and the collector refuses to run two
coordinate sets from one module.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

from phase3_budget import BudgetStop, digest, read_checked
from phase3_recognition_recovery import verify, sha
from phase3_recognition_run import ROOT, LEDGER, Ledger, network, charge, MODELS
from phase4_crossmodel_dispatch_v2 import dispatch as crossmodel_dispatch
from phase3_variant_round import save

import phase4b_perm_pool as P
import phase5_position_counterbalance_r1 as R1
import phase7_semantics_r1 as C
import phase7_parameter_followup as F

DESIGNATION = "r2"
CODES = F.DESIGNATIONS[DESIGNATION]
STUDY = f"parameter_followup_{DESIGNATION}"
FOLDER = ROOT / f"experiments/phase7_understanding/{STUDY}"
PARENT = ROOT / "experiments/phase7_understanding/parameter_followup_r1"

N_AGENTS = F.N_AGENTS
ARMS = tuple(f"{c}{s}" for c in CODES for s in ("+", "-"))
# Seed 2026092025 chosen before any call as the first whose 80 agents have no
# rendered-precision collision on TfA or MoR - the same degeneracy check that
# blocked r1's first seed. See phase7_parameter_followup.verify_construction.
SEEDS = {"population": 2026092025, "schedule": 2026092035, "analysis": 2026092036}
BOOTSTRAP_DRAWS = 10_000
CAP = 12_000_000_000
PROVIDER_CAPS = C.PROVIDER_CAPS


def population():
    import numpy as np
    rng = np.random.default_rng(SEEDS["population"])
    agents = []
    for i in range(N_AGENTS):
        draw = {k: float(round(rng.beta(a, b), 3)) for k, (a, b) in R1.BETA.items()}
        agents.append({"agent": i, "coordinates": draw})
    return {"n_agents": N_AGENTS, "agents": agents, "seed": SEEDS["population"],
            "note": ("Independent Beta marginals. One coordinate is overwritten per arm; "
                     "the other nine are identical between levels per agent.")}


def profiled_jobs(pop):
    batch = []
    for agent in pop["agents"]:
        for code in CODES:
            for level in (F.HIGH, F.LOW):
                system_text = R1.system(F.pin(agent["coordinates"], code, level), "E")
                sign = "+" if level == F.HIGH else "-"
                lvl = "hi" if level == F.HIGH else "lo"
                for task_id in P.TASK_IDS:
                    job = C.make_job("x", R1.body(task_id, agent["agent"] % 2 == 0),
                                     system_text)
                    job["slot"] = f"{STUDY}/profiled/{code}_{lvl}/{agent['agent']}/{task_id}"
                    job["valid_actions"] = sorted(a.lower() for a in P.action_ids(task_id))
                    job["cell"] = {"arm": f"{code}{sign}", "coordinate": code,
                                   "level": level, "task": task_id,
                                   "agent": agent["agent"], "index": None}
                    batch.append(job)
    return batch


def leakage_gate():
    symmetry = P.verify_items()
    leaks = {t: P.audit_leakage(t) for t in P.TASK_IDS if P.audit_leakage(t)}
    if leaks:
        raise BudgetStop("Task text leaks: " + str(leaks))
    if len(CODES) != 2:
        raise BudgetStop("This designation pins exactly two coordinates")
    agents = population()["agents"]
    construction = F.verify_construction(C._render, agents, CODES)
    c = agents[0]["coordinates"]
    for code in CODES:
        text = R1.system(F.pin(c, code, F.HIGH), "E")
        if "Ethical guidance" in text:
            raise BudgetStop(f"{code}: arm carries guidance text")
        if "Procedural Dependence" not in text:
            raise BudgetStop(f"{code}: arm lost the profile block")
    return {"items_verified": symmetry, "construction_verified": construction,
            "locked_prediction": F.locked_prediction(DESIGNATION),
            "followup_sha256": F.content_hash(DESIGNATION),
            "task_content_sha256": P.content_hash(), "output_budget": C.OUTPUT_BUDGET,
            "inherited_review": {"slot": C.INHERITED_REVIEW, **C.inherited_review()}}


def analyse(rows):
    import numpy as np
    tasks = list(P.TASK_IDS)
    table = {}
    for r in rows:
        if r.get("choice") and r["task"] in tasks:
            table.setdefault((r["agent"], r["task"]), {})[r["arm"]] = (
                P.primary_net(r["task"], r["choice"]) == "good")

    def sign_test(code, subset):
        pairs = [(v[f"{code}-"], v[f"{code}+"]) for (a, t), v in table.items()
                 if t in subset and f"{code}-" in v and f"{code}+" in v]
        if not pairs:
            return None
        hi = sum(1 for lo, h in pairs if h and not lo)
        lo = sum(1 for lo, h in pairs if lo and not h)
        n = hi + lo
        p = min(1.0, 2 * sum(math.comb(n, i) for i in range(min(hi, lo) + 1)) / 2 ** n) if n else 1.0
        return {"pairs": len(pairs), "more_under_high": hi, "more_under_low": lo,
                "effect": round((hi - lo) / len(pairs), 4), "p_two_sided": round(p, 8)}

    within = {c: sign_test(c, tasks) for c in CODES}
    per_item = {c: {t: sign_test(c, [t]) for t in tasks} for c in CODES}
    holm, running = {}, 0.0
    live = sorted(((c, w["p_two_sided"]) for c, w in within.items() if w), key=lambda kv: kv[1])
    for i, (c, raw) in enumerate(live):
        running = min(1.0, max(running, raw * (len(live) - i)))
        holm[c] = round(running, 8)

    units = [v for v in table.values() if all(a in v for a in ARMS)]
    rng = np.random.default_rng(SEEDS["analysis"])
    idx = rng.integers(0, len(units), size=(BOOTSTRAP_DRAWS, len(units))) if units else None
    effects = {}
    for c in CODES:
        d = np.array([int(u[f"{c}+"]) - int(u[f"{c}-"]) for u in units], float)
        lo, hi = np.percentile(d[idx].mean(axis=1), [2.5, 97.5])
        effs = [w["effect"] for w in per_item[c].values() if w]
        # Equivalence bound: smallest symmetric margin containing the 90% interval.
        q5, q95 = np.percentile(d[idx].mean(axis=1), [5, 95])
        effects[c] = {"estimate": round(float(d.mean()), 4),
                      "ci95": [round(float(lo), 4), round(float(hi), 4)],
                      "excludes_zero": bool(lo > 0 or hi < 0),
                      "equivalence_bound_90": round(float(max(abs(q5), abs(q95))), 4),
                      "items_positive": sum(e > 0 for e in effs),
                      "items_negative": sum(e < 0 for e in effs),
                      "meets_consistency": max(sum(e > 0 for e in effs),
                                               sum(e < 0 for e in effs)) >= 4,
                      "prior": F.PRIOR[c]}

    readings = {}
    for c in CODES:
        e = effects[c]
        moves = holm.get(c, 1.0) < 0.05 and e["meets_consistency"]
        readings[c] = ("moves_the_outcome" if moves else "no_effect_detected")
    return {"units_complete": len(units), "within_coordinate": within, "per_item": per_item,
            "holm": holm, "holm_family_size": len(live), "effects": effects,
            "readings": readings, "coordinates": list(CODES),
            "power_note": F.POWER["consequence"],
            "bootstrap": {"draws": BOOTSTRAP_DRAWS, "seed": SEEDS["analysis"],
                          "unit": "agent-item, conditional on the tested items"},
            "locked_prediction": F.locked_prediction(DESIGNATION)}


def prepare(persist=False):
    leak = leakage_gate()
    parent = read_checked(PARENT / "release.json")
    verify(parent)
    with Ledger(LEDGER, parent) as ledger:
        C._ledger_clean(ledger)
        providers = dict(ledger.state["providers"])
    pop = population()
    batch = profiled_jobs(pop)
    slots = {j["slot"]: {"kind": j["kind"], "stage": j["stage"], "model": j["request"]["model"],
                         "input_token_bound": j["input_token_bound"],
                         "reserved_nano": j["reserved_nano"],
                         "max_output": j["request"].get("max_tokens",
                                                        j["request"].get("max_completion_tokens")),
                         "request_sha256": digest(j["request"])} for j in batch}
    bound = sum(j["reserved_nano"] for j in batch)
    for j in batch:
        providers[MODELS[j["request"]["model"]]] += j["reserved_nano"]
    if len(slots) != N_AGENTS * len(ARMS) * len(P.TASK_IDS) or bound > CAP:
        raise BudgetStop(f"Size or cap exceeded: {len(slots)} calls, {bound / 1e9:.6f} USD")
    for provider, total in providers.items():
        if total > PROVIDER_CAPS[provider]:
            raise BudgetStop(f"{provider} ceiling would be exceeded: {total / 1e9:.4f}")
    paths = [Path(__file__), ROOT / "code/phase7_parameter_followup.py",
             ROOT / "code/phase7_parameter_followup_r1.py",
             ROOT / "code/phase7_semantics_r1.py", FOLDER / "PROTOCOL.md"]
    release = {"id": STUDY, "population_sha256": digest(pop), "jobs_sha256": digest(batch),
               "slots": slots, "recognition_cap_nano": bound, "prior_screening_nano": 0,
               "original_screening_cap_nano": CAP,
               "provider_caps_nano": {**parent["provider_caps_nano"], **PROVIDER_CAPS},
               "parent_checkpoint_sha256": digest(parent), "leakage_gate": leak,
               "historical_keys": sorted(p.stem for p in (LEDGER / "records").glob("*.json")),
               "preserved_files": {p.relative_to(LEDGER).as_posix(): sha(p)
                                   for p in LEDGER.rglob("*.json")},
               "failure_log_prefix_bytes": (LEDGER / "failures.jsonl").stat().st_size,
               "failure_log_prefix_sha256": sha(LEDGER / "failures.jsonl"),
               "source_sha256": {**parent["source_sha256"],
                                 **{p.relative_to(ROOT).as_posix(): sha(p) for p in paths}}}
    with Ledger(LEDGER, release):
        pass
    if persist:
        save(FOLDER / "population.json", pop)
        save(FOLDER / "requests.json", batch)
        save(FOLDER / "release.json", release)
    return release, pop, batch


def collect(replay=False, root=LEDGER, folder=FOLDER, responder=network, test_data=None):
    root, folder = Path(root), Path(folder)
    if root == LEDGER and test_data is not None:
        raise BudgetStop("Test data on real ledger")
    leakage_gate()
    release, pop, batch = test_data or tuple(
        read_checked(folder / f) for f in ("release.json", "population.json", "requests.json"))
    verify(release, root)
    if digest(pop) != release["population_sha256"] or digest(batch) != release["jobs_sha256"]:
        raise BudgetStop("Changed population or requests")
    if batch != profiled_jobs(pop):
        raise BudgetStop("Reconstructed schedule differs")
    if release["leakage_gate"]["task_content_sha256"] != P.content_hash():
        raise BudgetStop("Task content changed after release")
    manifest = {"release_sha256": digest(release), "jobs_sha256": digest(batch)}
    save(folder / "execution_manifest.json", manifest)
    with Ledger(root, release) as ledger:
        C._ledger_clean(ledger)
        seen, rows = set(), []
        for job in batch:
            record, _ = crossmodel_dispatch(ledger, job, digest(manifest), responder, replay)
            if charge(record["raw"], job, False) != record["accounted_nano"]:
                raise BudgetStop("Cost replay mismatch")
            seen.add(digest(job["slot"]))
            rows.append({**job["cell"], "choice": record["parsed"]})
            if len(rows) % 200 == 0:
                print(json.dumps({"progress": len(rows), "of": len(batch)}), flush=True)
        save(folder / "all_rows.json", rows)
        result = {"study": STUDY, "decision": "complete", "analysis": analyse(rows),
                  "profiled_calls": len(rows), "moral_scores_assigned": False,
                  "review": release["leakage_gate"]["inherited_review"],
                  "note": ("Deterministic choice counts under stipulated standards. No "
                           "moral label is assigned and no moral quality is measured.")}
        if set(ledger.state["reservations"]) - set(release["historical_keys"]) != seen:
            raise BudgetStop("Unmanifested dispatch")
        result.update(calls=len(seen), accounted_nano=ledger.state["recognition_nano"],
                      provider_totals_nano=ledger.state["providers"],
                      release_sha256=digest(release))
        save(folder / "results.json", result)
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("check", "prepare", "run"))
    parser.add_argument("--yes", action="store_true")
    args = parser.parse_args()
    if args.command == "check":
        gate = leakage_gate()
        batch = profiled_jobs(population())
        print(json.dumps({"gates": "passed", "calls": len(batch),
                          "maximum_usd": sum(j["reserved_nano"] for j in batch) / 1e9,
                          "coordinates": list(CODES), "agents": N_AGENTS,
                          "design_sha256": gate["followup_sha256"]}))
    elif args.command == "prepare":
        release, _, batch = prepare(True)
        print(json.dumps({"maximum_usd": release["recognition_cap_nano"] / 1e9,
                          "total_calls": len(batch), "seed": SEEDS["population"]}))
    else:
        if not args.yes:
            raise BudgetStop("Explicit execution flag required")
        print(json.dumps({k: v for k, v in collect().items() if k != "analysis"}))
