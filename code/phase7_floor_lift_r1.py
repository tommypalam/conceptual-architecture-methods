"""Collector for floor_lift_r1: does PD lift a floored twin, as a status-quo field does?

Design, locked readings, power and the gate live in `phase7_floor_lift`. This
module dispatches. 2,240 calls on gpt-5.4-mini: 40 agents x 8 cells x 7 items.

Built on `phase7_semantics_r1` by import, carrying its three disclosed choices:
a 256-token output cap, no review call (the base items and the r1 twins have both
been reviewed and accepted; verdicts are read from the ledger, never re-dispatched),
and a fresh population seed.

**Two inherited review verdicts are recorded**, because this designation uses two
item sets: `position_counterbalance_r1/review/0` (base items, accept) and
`defeasibility_screen_r1/review/0` (the r1 twins, accept). Neither is re-run.
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
import phase7_floor_lift as F

FOLDER = ROOT / "experiments/phase7_understanding/floor_lift_r1"
PARENT = ROOT / "experiments/phase7_understanding/defeasibility_screen_r2"
STUDY = "floor_lift_r1"

N_AGENTS = 40
SEEDS = {"population": 2026092011, "schedule": 2026092012, "analysis": 2026092013}
BOOTSTRAP_DRAWS = 10_000
CAP = 12_000_000_000
PROVIDER_CAPS = C.PROVIDER_CAPS
TWIN_REVIEW = "defeasibility_screen_r1/review/0"


def population():
    import numpy as np
    rng = np.random.default_rng(SEEDS["population"])
    agents = []
    for i in range(N_AGENTS):
        draw = {k: float(round(rng.beta(a, b), 3)) for k, (a, b) in R1.BETA.items()}
        agents.append({"agent": i, "coordinates": draw})
    return {"n_agents": N_AGENTS, "agents": agents, "seed": SEEDS["population"],
            "note": ("Independent Beta marginals. One field is overwritten per cell; the "
                     "other nine coordinates are identical across cells per agent.")}


def system(coordinates, field, level):
    pinned = F.pin(coordinates, field, level)
    canonical = R1.system(pinned, "E")
    block = C._render(pinned)
    if canonical.count(block) != 1:
        raise BudgetStop("Profile block not found exactly once in the system prompt")
    return canonical.replace(block, F.block_for(C._render, coordinates, field, level))


def profiled_jobs(pop):
    batch = []
    for agent in pop["agents"]:
        for field in F.FIELDS:
            for level in (F.HIGH, F.LOW):
                system_text = system(agent["coordinates"], field, level)
                sign = "+" if level == F.HIGH else "-"
                lvl = "hi" if level == F.HIGH else "lo"
                for version in F.VERSIONS:
                    for task_id in P.TASK_IDS:
                        job = C.make_job("x", F.body(task_id, version, agent["agent"] % 2 == 0),
                                         system_text)
                        job["slot"] = (f"{STUDY}/profiled/{field}_{version}_{lvl}/"
                                       f"{agent['agent']}/{task_id}")
                        job["valid_actions"] = sorted(a.lower() for a in P.action_ids(task_id))
                        job["cell"] = {"arm": f"{field}:{version}{sign}", "field": field,
                                       "version": version, "level": level, "task": task_id,
                                       "agent": agent["agent"], "index": None}
                        batch.append(job)
    return batch


def twin_review():
    record = read_checked(LEDGER / "records" / (digest(TWIN_REVIEW) + ".json"))
    if record.get("error"):
        raise BudgetStop("Inherited twin review did not complete")
    return R1.read_review(record["parsed"])


def leakage_gate():
    symmetry = P.verify_items()
    leaks = {t: P.audit_leakage(t) for t in P.TASK_IDS if P.audit_leakage(t)}
    if leaks:
        raise BudgetStop("Task text leaks: " + str(leaks))
    agents = population()["agents"]
    construction = F.verify_construction(C._render, agents)
    c = agents[0]["coordinates"]
    # The PD arm must be byte-identical to the instrument semantics_r1 validated.
    for level in (F.LOW, F.HIGH):
        if system(c, "PD", level) != R1.system(F.pin(c, "PD", level), "E"):
            raise BudgetStop("PD arm differs from the canonical system prompt")
    for field in F.FIELDS:
        text = system(c, field, F.HIGH)
        if "Ethical guidance" in text:
            raise BudgetStop(f"{field}: arm carries guidance text")
    return {"items_verified": symmetry, "construction_verified": construction,
            "locked_prediction": F.LOCKED_PREDICTION, "floor_lift_sha256": F.content_hash(),
            "task_content_sha256": P.content_hash(),
            "twin_content_sha256": __import__("phase7_defeasibility_items").content_hash(),
            "output_budget": C.OUTPUT_BUDGET,
            "inherited_reviews": {"base_items": {"slot": C.INHERITED_REVIEW,
                                                 **C.inherited_review()},
                                  "twins": {"slot": TWIN_REVIEW, **twin_review()}}}


def _keep(r):
    return r["choice"] == P.clean_action(r["task"])


def analyse(rows):
    """Base arms gate; the floored twins carry the test; SQ - PD is primary."""
    import numpy as np
    tasks = list(P.TASK_IDS)
    table = {}
    for r in rows:
        if r.get("choice") and r["task"] in tasks:
            table.setdefault((r["agent"], r["task"]), {})[r["arm"]] = _keep(r)

    def sign_test(arm_lo, arm_hi, subset):
        pairs = [(v[arm_lo], v[arm_hi]) for (a, t), v in table.items()
                 if t in subset and arm_lo in v and arm_hi in v]
        if not pairs:
            return None
        hi = sum(1 for lo, h in pairs if h and not lo)
        lo = sum(1 for lo, h in pairs if lo and not h)
        n = hi + lo
        tail = sum(math.comb(n, i) for i in range(min(hi, lo) + 1)) / 2 ** n if n else 1.0
        return {"pairs": len(pairs), "more_under_high": hi, "more_under_low": lo,
                "effect": round((hi - lo) / len(pairs), 4),
                "p_one_sided_positive": round(
                    (sum(math.comb(n, i) for i in range(lo + 1)) / 2 ** n) if n else 1.0, 8),
                "p_two_sided": round(min(1.0, 2 * tail), 8)}

    cells = {f"{f}:{v}": sign_test(f"{f}:{v}-", f"{f}:{v}+", tasks)
             for f in F.FIELDS for v in F.VERSIONS}
    floored = {f"{f}:TWIN": sign_test(f"{f}:TWIN-", f"{f}:TWIN+", list(F.FLOORED))
               for f in F.FIELDS}
    per_item = {f"{f}:{v}": {t: sign_test(f"{f}:{v}-", f"{f}:{v}+", [t]) for t in tasks}
                for f in F.FIELDS for v in F.VERSIONS}

    base_p = {k: v["p_one_sided_positive"] for k, v in cells.items() if v}
    holm, running = {}, 0.0
    for i, (k, p) in enumerate(sorted(base_p.items(), key=lambda kv: kv[1])):
        running = min(1.0, max(running, p * (len(base_p) - i)))
        holm[k] = round(running, 8)

    def consistent(key, subset=tasks):
        effs = [per_item[key][t]["effect"] for t in subset if per_item[key][t]]
        return sum(e > 0 for e in effs)

    gate = all(holm.get(f"{f}:BASE", 1.0) < 0.05 and consistent(f"{f}:BASE") >= 4
               for f in F.FIELDS)

    units = [v for v in ((k, v) for k, v in table.items() if k[1] in F.FLOORED)
             for v in [v[1]] if all(a in v for a in F.CELLS)]
    lift, diff = {}, None
    if units:
        rng = np.random.default_rng(SEEDS["analysis"])
        idx = rng.integers(0, len(units), size=(BOOTSTRAP_DRAWS, len(units)))
        d = {f: np.array([int(u[f"{f}:TWIN+"]) - int(u[f"{f}:TWIN-"]) for u in units], float)
             for f in F.FIELDS}

        def interval(x):
            lo, hi = np.percentile(x[idx].mean(axis=1), [2.5, 97.5])
            return {"estimate": round(float(x.mean()), 4),
                    "ci95": [round(float(lo), 4), round(float(hi), 4)],
                    "excludes_zero": bool(lo > 0 or hi < 0)}
        lift = {f: interval(d[f]) for f in F.FIELDS}
        diff = interval(d["SQ"] - d["PD"])

    if not gate:
        decision, reading = "gate_failed", (
            "A base arm did not reproduce its known effect, so the twin arms are not "
            "interpreted. Nothing is claimed.")
    elif not lift or not lift["SQ"]["excludes_zero"] or lift["SQ"]["estimate"] <= 0:
        decision, reading = "uninformative_floor", (
            "Status-quo Preference did not lift the floored twins either. No field tested "
            "can move them, so PD's behaviour there says nothing about whether PD is a "
            "status-quo dial. The question remains open.")
    elif lift["PD"]["excludes_zero"] and lift["PD"]["estimate"] > 0 and not diff["excludes_zero"]:
        decision, reading = "pd_is_a_dial", (
            "Both fields lift the floored twins and their difference includes zero. On "
            "items where the arrangement went around its own procedure, Procedural "
            "Dependence behaves like a pure status-quo field. This SUPPORTS the "
            "status-quo-dial reading and bounds what the thesis's PD result means.")
    elif diff["excludes_zero"] and diff["estimate"] > 0:
        decision, reading = "pd_is_not_a_dial", (
            "Status-quo Preference lifts the floored twins and Procedural Dependence "
            "lifts them significantly less. The two fields DISSOCIATE on items where the "
            "arrangement bypassed its procedure, which a pure status-quo reading of PD "
            "cannot produce. This is not understanding and does not show PD encodes "
            "procedural justice; it shows PD is not simply a status-quo dial.")
    else:
        decision, reading = "mixed", (
            "Neither locked reading holds cleanly. Reported field by field through "
            "L(SQ) - L(PD) and its interval, not rounded to either.")

    return {"cells": cells, "floored_twin_arms": floored, "per_item": per_item,
            "holm_base": holm, "gate_passed": gate, "gate_reference": F.GATE_REFERENCE,
            "lift_on_floored_twins": lift, "difference_SQ_minus_PD": diff,
            "units_complete": len(units), "floored_twins": list(F.FLOORED),
            "decision": decision, "reading": reading,
            "power_note": F.LOCKED_PREDICTION["power"]["consequence"],
            "bootstrap": {"draws": BOOTSTRAP_DRAWS, "seed": SEEDS["analysis"],
                          "unit": "agent-item over the floored twins"},
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
    if len(slots) != N_AGENTS * len(F.CELLS) * len(P.TASK_IDS) or bound > CAP:
        raise BudgetStop(f"Size or cap exceeded: {len(slots)} calls, {bound / 1e9:.6f} USD")
    for provider, total in providers.items():
        if total > PROVIDER_CAPS[provider]:
            raise BudgetStop(f"{provider} ceiling would be exceeded: {total / 1e9:.4f}")
    paths = [Path(__file__), ROOT / "code/phase7_floor_lift.py",
             ROOT / "code/phase7_defeasibility_items.py", ROOT / "code/phase7_probe_fields.py",
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
                  "reviews": release["leakage_gate"]["inherited_reviews"],
                  "note": ("Deterministic choice counts. The outcome is the share choosing "
                           "the base item's KEEP option; no moral label is assigned to any "
                           "twin option.")}
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
                          "design_sha256": gate["floor_lift_sha256"],
                          "floored_twins": list(F.FLOORED),
                          "reviews": {k: v["verdict"] for k, v
                                      in gate["inherited_reviews"].items()}}))
    elif args.command == "prepare":
        release, _, batch = prepare(True)
        print(json.dumps({"maximum_usd": release["recognition_cap_nano"] / 1e9,
                          "total_calls": len(batch), "seed": SEEDS["population"]}))
    else:
        if not args.yes:
            raise BudgetStop("Explicit execution flag required")
        print(json.dumps({k: v for k, v in collect().items() if k != "analysis"}))
