"""Collector for probe_fields_r1: do probe fields outside the ten move choices as they say?

Design, wording, predictions and readings live in `phase7_probe_fields`. This
module dispatches.

**Eight cells on gpt-5.4-mini, seven items, 40 agents: 2,240 calls.** Four probe
fields in Affective Weighting's slot, each at 0.10 and 0.90. Everything outside
entry 10's three lines is byte-identical to the agent's canonical prompt.

**Built on `semantics_r1` by import.** Job construction, the ledger guard and the
inherited-review read are that collector's own functions. It carries the same
three disclosed choices: 256-token output cap (settled $1.666 on a $10.976
reservation there, nothing truncated), no review call (the items are byte-identical
to accepted material; the parent verdict is read from the ledger), and a fresh
population seed. **The probe entries are new material no reviewer has seen**; a
reviewer judges item wording, and the entries rest on byte-level construction
checks and on the researcher's approval of their wording.
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
import phase7_semantics_r1 as C          # sibling collector, pinned by its release
import phase7_probe_fields as F

FOLDER = ROOT / "experiments/phase7_understanding/probe_fields_r1"
PARENT = ROOT / "experiments/phase7_understanding/semantics_r1"
STUDY = "probe_fields_r1"

ARMS = F.CELLS
N_AGENTS = 40
SEEDS = {"population": 2026092001, "schedule": 2026092002, "analysis": 2026092003}
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
            "note": ("Independent Beta marginals. The AW slot is overwritten by the probe "
                     "in every cell; the other nine coordinates, PD included, keep the "
                     "drawn values and are identical across cells per agent.")}


def system(coordinates, probe, level):
    pinned = F.pin(coordinates, level)
    canonical = R1.system(pinned, "E")
    block = C._render(pinned)
    if canonical.count(block) != 1:
        raise BudgetStop("Profile block not found exactly once in the system prompt")
    return canonical.replace(block, F.probe_block(block, probe))


def profiled_jobs(pop):
    batch = []
    for agent in pop["agents"]:
        for probe in F.PROBES:
            for level in (F.HIGH, F.LOW):
                system_text = system(agent["coordinates"], probe, level)
                sign = "+" if level == F.HIGH else "-"
                tag = f"{probe}_{'hi' if level == F.HIGH else 'lo'}"
                for task_id in P.TASK_IDS:
                    job = C.make_job(f"profiled/{tag}/{agent['agent']}/{task_id}",
                                     R1.body(task_id, agent["agent"] % 2 == 0), system_text)
                    job["slot"] = f"{STUDY}/profiled/{tag}/{agent['agent']}/{task_id}"
                    job["valid_actions"] = sorted(a.lower() for a in P.action_ids(task_id))
                    job["cell"] = {"arm": f"{probe}{sign}", "probe": probe, "level": level,
                                   "task": task_id, "agent": agent["agent"], "index": None}
                    batch.append(job)
    return batch


def leakage_gate():
    symmetry = P.verify_items()
    leaks = {t: P.audit_leakage(t) for t in P.TASK_IDS if P.audit_leakage(t)}
    if leaks:
        raise BudgetStop("Task text leaks: " + str(leaks))
    agents = population()["agents"]
    construction = F.verify_construction(C._render, agents)
    c = agents[0]["coordinates"]
    for probe, spec in F.PROBES.items():
        text = system(c, probe, F.HIGH)
        if "Ethical guidance" in text or "Affective Weighting" in text:
            raise BudgetStop(f"{probe}: guidance text or the slot's old name present")
        if text.count(f"10. {spec['name']}: 0.90") != 1 or "Procedural Dependence" not in text:
            raise BudgetStop(f"{probe}: probe entry not rendered as designed")
    return {"items_verified": symmetry, "construction_verified": construction,
            "locked_prediction": F.LOCKED_PREDICTION, "probe_fields_sha256": F.content_hash(),
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

    def sign_test(probe, subset):
        pairs = [(v[f"{probe}-"], v[f"{probe}+"]) for (a, t), v in table.items()
                 if t in subset and f"{probe}-" in v and f"{probe}+" in v]
        if not pairs:
            return None
        hi = sum(1 for lo, h in pairs if h and not lo)
        lo = sum(1 for lo, h in pairs if lo and not h)
        n = hi + lo
        p = min(1.0, 2 * sum(math.comb(n, i) for i in range(min(hi, lo) + 1)) / (2 ** n)) if n else 1.0
        return {"pairs": len(pairs), "more_under_high": hi, "more_under_low": lo,
                "effect": round((hi - lo) / len(pairs), 4), "p_two_sided": round(p, 8)}

    within = {p: sign_test(p, tasks) for p in F.PROBES}
    per_item = {p: {t: sign_test(p, [t]) for t in tasks} for p in F.PROBES}
    holm, running = {}, 0.0
    live = sorted(((p, w["p_two_sided"]) for p, w in within.items() if w), key=lambda kv: kv[1])
    for i, (p, raw) in enumerate(live):
        running = min(1.0, max(running, raw * (len(live) - i)))
        holm[p] = round(running, 8)

    units = [v for v in table.values() if all(a in v for a in ARMS)]
    rng = np.random.default_rng(SEEDS["analysis"])
    idx = rng.integers(0, len(units), size=(BOOTSTRAP_DRAWS, len(units)))
    effects = {}
    for p in F.PROBES:
        d = np.array([int(u[f"{p}+"]) - int(u[f"{p}-"]) for u in units], float)
        lo, hi = np.percentile(d[idx].mean(axis=1), [2.5, 97.5])
        effs = [w["effect"] for w in per_item[p].values() if w]
        effects[p] = {"name": F.PROBES[p]["name"], "predicted": F.PROBES[p]["predicted"],
                      "estimate": round(float(d.mean()), 4),
                      "ci95": [round(float(lo), 4), round(float(hi), 4)],
                      "excludes_zero": bool(lo > 0 or hi < 0),
                      "inside_pm_0.15": bool(lo > -0.15 and hi < 0.15),
                      "items_positive": sum(e > 0 for e in effs),
                      "items_negative": sum(e < 0 for e in effs)}

    pos = lambda p: effects[p]["estimate"] > 0 and effects[p]["excludes_zero"]
    neg = lambda p: effects[p]["estimate"] < 0 and effects[p]["excludes_zero"]
    if all(pos(p) for p in F.PROBES) or all(neg(p) for p in F.PROBES):
        reading = "GENERIC_CUE"
    elif neg("NC") and sum(pos(p) for p in ("SQ", "SW", "WO")) >= 2:
        reading = "MEANING_GENERAL"
    elif all(effects[p]["inside_pm_0.15"] for p in F.PROBES):
        reading = "PD_SPECIAL"
    else:
        reading = "MIXED"
    return {"units_complete": len(units), "effects": effects, "within_field": within,
            "per_item": per_item, "holm": holm, "holm_family_size": len(live),
            "reading": reading, "reading_definitions": F.LOCKED_PREDICTION["readings"],
            "bootstrap": {"draws": BOOTSTRAP_DRAWS, "seed": SEEDS["analysis"],
                          "unit": "agent-item, conditional on the tested items"},
            "locked_prediction": F.LOCKED_PREDICTION}


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
    paths = [Path(__file__), ROOT / "code/phase7_probe_fields.py",
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
            if len(rows) % 100 == 0:
                print(json.dumps({"progress": len(rows), "of": len(batch)}), flush=True)
        save(folder / "all_rows.json", rows)
        result = {"study": STUDY, "decision": "complete", "analysis": analyse(rows),
                  "profiled_calls": len(rows), "moral_scores_assigned": False,
                  "review": release["leakage_gate"]["inherited_review"],
                  "note": ("Deterministic choice counts under stipulated standards. No moral "
                           "label is assigned and no moral quality is measured.")}
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
                          "design_sha256": gate["probe_fields_sha256"],
                          "seed": SEEDS["population"]}))
    elif args.command == "prepare":
        release, _, batch = prepare(True)
        print(json.dumps({"maximum_usd": release["recognition_cap_nano"] / 1e9,
                          "total_calls": len(batch), "seed": SEEDS["population"]}))
    else:
        if not args.yes:
            raise BudgetStop("Explicit execution flag required")
        print(json.dumps({k: v for k, v in collect().items() if k != "analysis"}))
