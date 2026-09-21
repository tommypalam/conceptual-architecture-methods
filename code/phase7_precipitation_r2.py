"""Collector for precipitation_r2: does a boundary form from instances?

**A RE-DESIGNATION, not a retry.** `precipitation_r1` halted on a transport
`TimeoutError` at call 294 of 840. That designation is closed: its failed slot is
preserved unresolved and never touched, and its 293 settled records are excluded
from every analysis. This is a fresh designation with its own release and its own
seed, which is what would have been built had r1 failed at call 1.

The distinction the project's rule protects is between REPAIRING a halted run -
forbidden, because it is indistinguishable after the fact from retrying until the
numbers look clean - and STARTING a new one, which is always permitted. Nothing
here reads r1's records, reuses its reservations, or resolves its failure.

Design, the three circularity controls, the locked predictions and the
dose-response secondary live in `phase7_precipitation`, unchanged and at the same
content hash. The experiment is identical; only the designation is new.

**840 calls on gpt-5.4-mini**: 3 arms x 40 agents x 7 twin items, each an
independent stateless call. No new participant data and no new items: exemplars
are frozen `pd_prospective_r1` decisions, the items are the reviewed twins, and
both inherited review verdicts are read from the ledger, never re-dispatched.
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
import phase7_precipitation as F
import phase7_defeasibility_items as D

FOLDER = ROOT / "experiments/phase7_understanding/precipitation_r2"
# The parent is the most recent designation that TOUCHED THE LEDGER, which is the
# halted precipitation_r1: its 294 reservations exist, so any earlier parent is
# stale by exactly that count. A halted designation is still a valid parent - its
# records are settled and preserved; what is forbidden is reusing or resolving
# them, not building after them.
# precipitation_r1, the halted designation itself. Its release DECLARED all 840
# slots although only 294 dispatched, and the guard accepts a reservation that
# matches a declared slot, so r1's historical_keys plus its own slots cover the
# ledger exactly (verified: 0 uncovered). inverse_inference_r1 does NOT cover it -
# r1's 294 would be unaccounted. A halted designation is the right parent
# precisely because it declared more than it spent.
PARENT = ROOT / "experiments/phase7_understanding/precipitation_r1"
# r1's preserved failure. Named so a NEW unresolved dispatch still stops the run,
# and never retried: that slot stays unresolved permanently.
INHERITED_FAILURE = "precipitation_r1/profiled/RULE/1/weekend_rota"
STUDY = "precipitation_r2"
TWIN_REVIEW = "defeasibility_screen_r1/review/0"

SEEDS = {"analysis": 2026092211}
BOOTSTRAP_DRAWS = 10_000
# 840 calls at a 256-token output budget: 3 arms x 40 agents x 7 twins.
# Worst case $3.162; expected settlement about $0.63 at the measured rate.
# The 1.0 here was inherited from the 120-call inverse_inference collector and
# refused this designation at prepare(). `check` reports the cost but does not
# enforce the cap, so the mismatch only surfaced at the freeze.
CAP = 4_000_000_000
PROVIDER_CAPS = C.PROVIDER_CAPS


def _ledger_clean(ledger):
    """r1's preserved failure is expected; anything else still stops the run.

    Widening the allowed set by exactly one NAMED slot is the whole of what a
    re-designation may do to the ledger guard. It does not retry that slot, does
    not resolve it, and does not loosen the check: a new unresolved dispatch
    raises exactly as before.
    """
    allowed = {digest(f) for f in C.INHERITED_FAILURES} | {digest(INHERITED_FAILURE)}
    if ledger.state["pending"] or not set(ledger.state["failed"]) <= allowed:
        raise BudgetStop("Unexpected unresolved dispatch in inherited evidence")


def _describe(task_id):
    """One clause identifying the situation, from the item's own first sentence."""
    return P.task(task_id)["situation"].split(".")[0]


def records():
    """Frozen PD+ transcripts. Actual decisions, not idealised."""
    rows = read_checked(ROOT / F.SOURCE)
    return F.transcripts(rows, P.TASK_IDS, P.clean_action)


def exemplars():
    """The five shown per agent, deterministic: the first five in sorted task order.

    JSON-NATIVE BY CONSTRUCTION: string keys and lists, not int keys and tuples.
    The ledger checksums an object before saving and recomputes it after loading,
    so a shape that does not survive a JSON round-trip fails its own checksum.
    That is what happened on the first run of this collector; the fix is the
    shape, never the check. `_shown()` restores the working form.
    """
    return {str(a): [list(e) for e in v[:F.N_EXEMPLARS]]
            for a, v in records().items()}


def _shown(built):
    """Working form: int agent ids, tuple entries, whatever the round-trip did."""
    return {int(a): [tuple(e) for e in v] for a, v in built.items()}


def twin_review():
    record = read_checked(LEDGER / "records" / (digest(TWIN_REVIEW) + ".json"))
    if record.get("error"):
        raise BudgetStop("Inherited twin review did not complete")
    return R1.read_review(record["parsed"])


def profiled_jobs(built):
    """Three arms x agents x twins. The system prompt is unprofiled in every arm."""
    shown = _shown(built)
    batch, system_text = [], R1.system(None, "U")
    for arm in F.ARMS:
        for agent in sorted(shown):
            for task_id in D.TASK_IDS:
                body = D.body(task_id, True, agent % 2 == 0)
                text = F.compose(arm, body, shown[agent], _describe)
                job = C.make_job("x", text, system_text)
                job["slot"] = f"{STUDY}/profiled/{arm}/{agent}/{task_id}"
                job["valid_actions"] = sorted(a.lower() for a in P.action_ids(task_id))
                job["cell"] = {"arm": arm, "agent": agent, "task": task_id,
                               "keep_action": P.clean_action(task_id),
                               "exemplar_keeps": sum(1 for _, _, k in shown[agent] if k)}
                batch.append(job)
    return batch


def leakage_gate():
    symmetry = P.verify_items()
    twins = D.verify_twins(R1.body)
    shown = _shown(exemplars())
    if len(shown) != 40:
        raise BudgetStop(f"Expected 40 transcripts, found {len(shown)}")
    bodies = [D.body(t, True, True) for t in D.TASK_IDS]
    construction = F.verify_construction(bodies, shown, _describe)
    system_text = R1.system(None, "U")
    if "Procedural Dependence" in system_text:
        raise BudgetStop("System prompt carries a profile block")
    # The manipulation is the user-turn prefix ONLY; no arm may render a profile.
    for arm in F.ARMS:
        text = F.compose(arm, bodies[0], shown[sorted(shown)[0]], _describe)
        if "0.90" in text or "0.10" in text:
            raise BudgetStop(f"{arm}: prompt leaks a pinned value")
        if arm != "RULE" and "procedure" in text.lower():
            raise BudgetStop(f"{arm}: prompt mentions procedure outside the RULE arm")
    keeps = sorted({sum(1 for _, _, k in v if k) for v in shown.values()})
    if len(keeps) < 2:
        raise BudgetStop("Exemplar keep-counts do not vary; the secondary is void")
    return {"items_verified": symmetry, "twins_verified": twins,
            "construction_verified": construction,
            "exemplar_keep_counts": keeps,
            "locked_prediction": F.LOCKED_PREDICTION,
            "precipitation_sha256": F.content_hash(),
            "task_content_sha256": P.content_hash(),
            "twin_content_sha256": D.content_hash(),
            "output_budget": C.OUTPUT_BUDGET,
            "inherited_reviews": {"base_items": {"slot": C.INHERITED_REVIEW,
                                                 **C.inherited_review()},
                                  "twins": {"slot": TWIN_REVIEW, **twin_review()}}}


def analyse(rows):
    """Arm contrasts against NEITHER, plus the exemplar dose-response."""
    import numpy as np
    table = {}
    for r in rows:
        if r.get("choice"):
            table.setdefault((r["agent"], r["task"]), {})[r["arm"]] = (
                r["choice"] == r["keep_action"])
    units = [v for v in table.values() if all(a in v for a in F.ARMS)]
    rng = np.random.default_rng(SEEDS["analysis"])
    idx = rng.integers(0, len(units), size=(BOOTSTRAP_DRAWS, len(units))) if units else None

    def vec(arm):
        return np.array([int(u[arm]) for u in units], float)

    def interval(x):
        lo, hi = np.percentile(x[idx].mean(axis=1), [2.5, 97.5])
        return {"estimate": round(float(x.mean()), 4),
                "ci95": [round(float(lo), 4), round(float(hi), 4)],
                "excludes_zero": bool(lo > 0 or hi < 0)}

    keep_rate = {a: interval(vec(a)) for a in F.ARMS} if units else {}
    contrasts = {f"{a}-NEITHER": interval(vec(a) - vec("NEITHER"))
                 for a in ("INSTANCES", "RULE")} if units else {}
    if units:
        contrasts["INSTANCES-RULE"] = interval(vec("INSTANCES") - vec("RULE"))

    # Secondary: does the shift track how keep-leaning the shown exemplars were?
    by_agent = {}
    for r in rows:
        if r.get("choice"):
            by_agent.setdefault((r["agent"], r["exemplar_keeps"]), {}).setdefault(
                r["arm"], []).append(r["choice"] == r["keep_action"])
    dose = {}
    for arm in ("INSTANCES", "RULE"):
        pts = []
        for (agent, keeps), arms in by_agent.items():
            if arm in arms and "NEITHER" in arms:
                pts.append((keeps, sum(arms[arm]) / len(arms[arm])
                            - sum(arms["NEITHER"]) / len(arms["NEITHER"])))
        if len(pts) > 2:
            xs = np.array([x for x, _ in pts], float)
            ys = np.array([y for _, y in pts], float)
            slope = float(np.polyfit(xs, ys, 1)[0]) if xs.std() > 0 else None
            bs = []
            for _ in range(2000):
                s = rng.integers(0, len(xs), len(xs))
                if xs[s].std() > 0:
                    bs.append(np.polyfit(xs[s], ys[s], 1)[0])
            lo, hi = (float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))) if bs else (None, None)
            dose[arm] = {"n_agents": len(pts), "slope": None if slope is None else round(slope, 4),
                         "ci95": [None if lo is None else round(lo, 4),
                                  None if hi is None else round(hi, 4)],
                         "excludes_zero": bool(lo is not None and (lo > 0 or hi < 0))}

    inst = contrasts.get("INSTANCES-NEITHER")
    rule = contrasts.get("RULE-NEITHER")
    both = inst and rule
    if not both:
        decision, reading = "incomplete", "Insufficient complete units to interpret."
    elif not inst["excludes_zero"] and not rule["excludes_zero"]:
        decision, reading = "no_effect", (
            "Neither exemplars nor a stated rule shifts behaviour on the twins relative "
            "to the bare item. Nothing precipitated and nothing was followed; the "
            "designation is uninformative about boundaries rather than negative.")
    elif rule["excludes_zero"] and not inst["excludes_zero"]:
        decision, reading = "rule_following_only", (
            "A stated rule shifts behaviour; the agent's own prior decisions do not. No "
            "boundary formed from instances - what looks like a held concept is a rule "
            "being read while present. This is the deflationary reading, and it is the "
            "one this design was built to be able to return.")
    elif inst["excludes_zero"] and not rule["excludes_zero"]:
        decision, reading = "instances_only", (
            "Exemplars shift behaviour and a stated rule does not, which neither locked "
            "reading predicted. Reported as found; no mechanism is claimed.")
    elif contrasts["INSTANCES-RULE"]["excludes_zero"]:
        decision, reading = "boundary_precipitates_differently", (
            "Both shift, and they differ. Something forms from instances that the stated "
            "rule does not reproduce. This is the strongest outcome available here and "
            "still does NOT establish a concept: no decay was tested, so only the first "
            "half of Conjecture 1 is addressed.")
    else:
        decision, reading = "context_effect", (
            "Both exemplars and a stated rule shift behaviour by indistinguishable "
            "amounts. Consistent with a generic effect of additional context, and does "
            "not separate a fitted boundary from a supplied rule.")

    return {"units_complete": len(units), "keep_rate": keep_rate, "contrasts": contrasts,
            "dose_response": dose, "decision": decision, "reading": reading,
            "dose_note": F.LOCKED_PREDICTION["secondary_dose_response"],
            "bootstrap": {"draws": BOOTSTRAP_DRAWS, "seed": SEEDS["analysis"],
                          "unit": "agent-item complete in all three arms"},
            "locked_prediction": F.LOCKED_PREDICTION}


def prepare(persist=False):
    leak = leakage_gate()
    parent = read_checked(PARENT / "release.json")
    verify(parent)
    with Ledger(LEDGER, parent) as ledger:
        _ledger_clean(ledger)
        providers = dict(ledger.state["providers"])
    built = exemplars()
    batch = profiled_jobs(built)
    slots = {j["slot"]: {"kind": j["kind"], "stage": j["stage"], "model": j["request"]["model"],
                         "input_token_bound": j["input_token_bound"],
                         "reserved_nano": j["reserved_nano"],
                         "max_output": j["request"].get("max_tokens",
                                                        j["request"].get("max_completion_tokens")),
                         "request_sha256": digest(j["request"])} for j in batch}
    bound = sum(j["reserved_nano"] for j in batch)
    for j in batch:
        providers[MODELS[j["request"]["model"]]] += j["reserved_nano"]
    if len(slots) != len(F.ARMS) * 40 * len(D.TASK_IDS) or bound > CAP:
        raise BudgetStop(f"Size or cap exceeded: {len(slots)} calls, {bound / 1e9:.6f} USD")
    for provider, total in providers.items():
        if total > PROVIDER_CAPS[provider]:
            raise BudgetStop(f"{provider} ceiling would be exceeded: {total / 1e9:.4f}")
    paths = [Path(__file__), ROOT / "code/phase7_precipitation.py",
             ROOT / "code/phase7_defeasibility_items.py",
             ROOT / "code/phase7_semantics_r1.py", FOLDER / "PROTOCOL.md"]
    release = {"id": STUDY, "population_sha256": digest(built), "jobs_sha256": digest(batch),
               "slots": slots, "recognition_cap_nano": bound, "prior_screening_nano": 0,
               "original_screening_cap_nano": CAP,
               "provider_caps_nano": {**parent["provider_caps_nano"], **PROVIDER_CAPS},
               "parent_checkpoint_sha256": digest(parent), "leakage_gate": leak,
               "exemplar_keeps": {a: sum(1 for e in v if e[2]) for a, v in built.items()},
               "redesignation_of": {"study": "precipitation_r1",
                                    "halted_at": 294, "of": 840,
                                    "preserved_failure": INHERITED_FAILURE,
                                    "records_reused": 0},
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
        save(FOLDER / "exemplars.json", built)
        save(FOLDER / "requests.json", batch)
        save(FOLDER / "release.json", release)
    return release, built, batch


def collect(replay=False, root=LEDGER, folder=FOLDER, responder=network, test_data=None):
    root, folder = Path(root), Path(folder)
    if root == LEDGER and test_data is not None:
        raise BudgetStop("Test data on real ledger")
    leakage_gate()
    release, built, batch = test_data or tuple(
        read_checked(folder / f) for f in ("release.json", "exemplars.json", "requests.json"))
    verify(release, root)
    if digest(built) != release["population_sha256"] or digest(batch) != release["jobs_sha256"]:
        raise BudgetStop("Changed trials or requests")
    if batch != profiled_jobs(built):
        raise BudgetStop("Reconstructed schedule differs")
    manifest = {"release_sha256": digest(release), "jobs_sha256": digest(batch)}
    save(folder / "execution_manifest.json", manifest)
    with Ledger(root, release) as ledger:
        _ledger_clean(ledger)
        seen, rows = set(), []
        for job in batch:
            record, _ = crossmodel_dispatch(ledger, job, digest(manifest), responder, replay)
            if charge(record["raw"], job, False) != record["accounted_nano"]:
                raise BudgetStop("Cost replay mismatch")
            seen.add(digest(job["slot"]))
            rows.append({**job["cell"], "choice": record["parsed"]})
        save(folder / "all_rows.json", rows)
        result = {"study": STUDY, "decision": "complete", "analysis": analyse(rows),
                  "profiled_calls": len(rows), "moral_scores_assigned": False,
                  "reviews": release["leakage_gate"]["inherited_reviews"],
                  "note": ("No profile block is rendered in any arm; the manipulation is "
                           "the user-turn prefix. Exemplars are frozen pd_prospective_r1 "
                           "decisions and the items are the reviewed twins.")}
        print(json.dumps({"contrasts": result["analysis"]["contrasts"]}), flush=True)
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
        batch = profiled_jobs(exemplars())
        print(json.dumps({"gates": "passed", "calls": len(batch),
                          "maximum_usd": sum(j["reserved_nano"] for j in batch) / 1e9,
                          "exemplar_keep_counts": gate["exemplar_keep_counts"],
                          "design_sha256": gate["precipitation_sha256"]}))
    elif args.command == "prepare":
        release, _, batch = prepare(True)
        print(json.dumps({"maximum_usd": release["recognition_cap_nano"] / 1e9,
                          "total_calls": len(batch)}))
    else:
        if not args.yes:
            raise BudgetStop("Explicit execution flag required")
        print(json.dumps({k: v for k, v in collect().items() if k != "analysis"}))
