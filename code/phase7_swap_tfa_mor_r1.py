"""Collector for swap_tfa_mor_r1: are the TfA and MoR effects bound to their fields?

Design, priors, power and the locked prediction live in
`phase7_parameter_followup`. This module dispatches. 2,240 calls on gpt-5.4-mini:
80 agents x 2 coordinates x 2 levels x 7 items.

Design, the TRUE/SWAP construction, the gate and the power caution live in
`phase7_swap_tfa_mor`. 2,240 calls: 80 agents x 2 coordinates x 2 arms x 2 levels
x 7 items. TRUE and SWAP are numeral-identical; only which entry holds the level
differs. MoR is underpowered here at its measured size (8/20) and that is binding
on how its result may be read.

Built on `phase7_semantics_r1` by import, carrying its disclosed choices: a
256-token output cap, no review call (the seven items are byte-identical to
accepted material; the verdict is read from the ledger), and a fresh population
seed. Two inherited review verdicts are read from the ledger, never re-dispatched.
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
import phase7_swap_tfa_mor as F

CODES = F.ACTIVE
STUDY = "swap_tfa_mor_r1"
FOLDER = ROOT / f"experiments/phase7_understanding/{STUDY}"
PARENT = ROOT / "experiments/phase7_understanding/parameter_followup_r2"

N_AGENTS = 80
ARMS = F.ARMS
# Seed chosen before any call as the first whose 80 agents have no
# rendered-precision collision on TfA, MoR or the partner AW. A drawn partner
# value printing as a level would collapse TRUE and SWAP into the same block.
SEEDS = {"population": 2026092107, "schedule": 2026092117, "analysis": 2026092118}
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
    builder = {"TRUE": F.true_profile, "SWAP": F.swap_profile}
    for agent in pop["agents"]:
        for code in CODES:
            for arm in ("TRUE", "SWAP"):
                for level in (F.HIGH, F.LOW):
                    profile = builder[arm](agent["coordinates"], code, level)
                    system_text = R1.system(profile, "E")
                    sign = "+" if level == F.HIGH else "-"
                    lvl = "hi" if level == F.HIGH else "lo"
                    for task_id in P.TASK_IDS:
                        job = C.make_job("x", R1.body(task_id, agent["agent"] % 2 == 0),
                                         system_text)
                        job["slot"] = (f"{STUDY}/profiled/{code}_{arm}_{lvl}/"
                                       f"{agent['agent']}/{task_id}")
                        job["valid_actions"] = sorted(a.lower() for a in P.action_ids(task_id))
                        job["cell"] = {"arm": f"{code}:{arm}{sign}", "coordinate": code,
                                       "swap_arm": arm, "level": level, "task": task_id,
                                       "agent": agent["agent"], "index": None}
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
    for code in CODES:
        for arm, fn in (("TRUE", F.true_profile), ("SWAP", F.swap_profile)):
            text = R1.system(fn(c, code, F.HIGH), "E")
            if "Ethical guidance" in text:
                raise BudgetStop(f"{code}/{arm}: arm carries guidance text")
            if "Procedural Dependence" not in text:
                raise BudgetStop(f"{code}/{arm}: arm lost the profile block")
        # The two arms must be numeral-identical at both levels, for every agent.
        for agent in agents:
            for level in (F.LOW, F.HIGH):
                eq = F.block_equivalence(C._render, agent["coordinates"], code, level)
                if not eq["matched"]:
                    raise BudgetStop(f"{code}: TRUE/SWAP not matched at L={level}: {eq}")
    return {"items_verified": symmetry, "construction_verified": construction,
            "locked_prediction": F.LOCKED_PREDICTION,
            "followup_sha256": F.content_hash(),
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

    def sign_test(key, subset):
        """Paired high-minus-low within one coordinate's TRUE or SWAP arm."""
        pairs = [(v[f"{key}-"], v[f"{key}+"]) for (a, t), v in table.items()
                 if t in subset and f"{key}-" in v and f"{key}+" in v]
        if not pairs:
            return None
        hi = sum(1 for lo, h in pairs if h and not lo)
        lo = sum(1 for lo, h in pairs if lo and not h)
        n = hi + lo
        p = min(1.0, 2 * sum(math.comb(n, i) for i in range(min(hi, lo) + 1)) / 2 ** n) if n else 1.0
        return {"pairs": len(pairs), "more_under_high": hi, "more_under_low": lo,
                "effect": round((hi - lo) / len(pairs), 4), "p_two_sided": round(p, 8)}

    keys = [f"{c}:{arm}" for c in CODES for arm in ("TRUE", "SWAP")]
    within = {k: sign_test(k, tasks) for k in keys}
    per_item = {k: {t: sign_test(k, [t]) for t in tasks} for k in keys}

    # Holm over all four contrasts as ONE family, as label_semantics_r2 did.
    holm, running = {}, 0.0
    live = sorted(((k, w["p_two_sided"]) for k, w in within.items() if w), key=lambda kv: kv[1])
    for i, (k, raw) in enumerate(live):
        running = min(1.0, max(running, raw * (len(live) - i)))
        holm[k] = round(running, 8)

    units = [v for v in table.values() if all(a in v for a in ARMS)]
    rng = np.random.default_rng(SEEDS["analysis"])
    idx = rng.integers(0, len(units), size=(BOOTSTRAP_DRAWS, len(units))) if units else None

    def arm_vector(key):
        return np.array([int(u[f"{key}+"]) - int(u[f"{key}-"]) for u in units], float)

    def interval(x):
        lo, hi = np.percentile(x[idx].mean(axis=1), [2.5, 97.5])
        return {"estimate": round(float(x.mean()), 4),
                "ci95": [round(float(lo), 4), round(float(hi), 4)],
                "excludes_zero": bool(lo > 0 or hi < 0)}

    def consistency(key):
        effs = [w["effect"] for w in per_item[key].values() if w]
        return {"items": len(effs), "positive": sum(e > 0 for e in effs),
                "negative": sum(e < 0 for e in effs),
                "meets_rule": max(sum(e > 0 for e in effs), sum(e < 0 for e in effs)) >= 4}

    arms = {k: interval(arm_vector(k)) for k in keys} if units else {}
    cons = {k: consistency(k) for k in keys}

    # PRIMARY: the within-unit difference TRUE - SWAP, per coordinate.
    difference, readings = {}, {}
    for c in CODES:
        prior_sign = -1.0 if F.PRIOR[c]["effect"] < 0 else 1.0
        gate = bool(within[f"{c}:TRUE"]
                    and np.sign(within[f"{c}:TRUE"]["effect"]) == prior_sign
                    and holm.get(f"{c}:TRUE", 1.0) < 0.05
                    and cons[f"{c}:TRUE"]["meets_rule"])
        if units:
            d = interval(arm_vector(f"{c}:TRUE") - arm_vector(f"{c}:SWAP"))
            # Sign-agnostic: the difference should run AWAY from zero in the
            # direction of the coordinate's own effect if the field carries it.
            d["favours_field_binding"] = bool(d["excludes_zero"]
                                              and np.sign(d["estimate"]) == prior_sign)
            difference[c] = d
        if not gate:
            readings[c] = {"decision": "gate_failed", "reading": (
                f"The {c} TRUE arm did not reproduce parameter_followup_r2 under the "
                "prespecified gate, so its SWAP contrast is uninterpretable and nothing "
                "is claimed. Note the recorded power caution before reading this as a "
                "non-replication.")}
        elif difference.get(c, {}).get("favours_field_binding"):
            readings[c] = {"decision": "field_bound", "reading": (
                f"{c}: the level moves the outcome on its own entry and significantly "
                "less on the numeral-identical partner entry. The effect is bound to the "
                "field. This does NOT establish that the field's stated MEANING carries "
                "it - that needs the gloss-reversal design of semantics_r1.")}
        else:
            readings[c] = {"decision": "not_separated", "reading": (
                f"{c}: TRUE and SWAP are not separated by this designation. The effect is "
                "not shown to be field-bound; it is equally consistent with a response to "
                "an extreme numeral wherever it sits. Reported as an inconclusive "
                "separation, not as evidence for either reading.")}

    return {"units_complete": len(units), "within_arm": within, "per_item": per_item,
            "holm": holm, "holm_family_size": len(live), "arm_effects": arms,
            "consistency": cons, "difference_TRUE_minus_SWAP": difference,
            "readings": readings, "coordinates": list(CODES),
            "power_caution": F.LOCKED_PREDICTION["power"]["caution"],
            "prior": F.PRIOR, "partner_evidence": F.PARTNER_EVIDENCE,
            "bootstrap": {"draws": BOOTSTRAP_DRAWS, "seed": SEEDS["analysis"],
                          "unit": "agent-item complete in all eight cells"},
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
    paths = [Path(__file__), ROOT / "code/phase7_swap_tfa_mor.py",
             ROOT / "code/phase7_parameter_followup_r2.py",
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
                          "arms": len(ARMS), "design_sha256": gate["followup_sha256"]}))
    elif args.command == "prepare":
        release, _, batch = prepare(True)
        print(json.dumps({"maximum_usd": release["recognition_cap_nano"] / 1e9,
                          "total_calls": len(batch), "seed": SEEDS["population"]}))
    else:
        if not args.yes:
            raise BudgetStop("Explicit execution flag required")
        print(json.dumps({k: v for k, v in collect().items() if k != "analysis"}))
