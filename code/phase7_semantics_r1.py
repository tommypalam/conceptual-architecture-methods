"""Collector for semantics_r1: does the PD effect follow what the scale is SAID TO MEAN?

Design, the four variants, the competing predictions and the decision rule live in
`phase7_semantics`. The in-place block edits live in `phase7_block_variants`. This
module dispatches.

**Eight cells on gpt-5.4-mini, seven items, 40 agents: 2,240 calls.** PD is pinned
to 0.10 and 0.90 under four renderings of the PD entry - CANON, FLIP, INVERT,
NONCE. The nine other entries, the items and the user turn are byte-identical.

**Built on `position_counterbalance_r1` by import, not by copy.** The item bodies,
the population draw, the review parser and the dispatch path are the parent's own
functions; only what differs is written here. The parent module is hash-pinned
and is not edited.

**Three disclosed differences from the parent.**

  1. OUTPUT_BUDGET is 256, not 1536. Across the parent's 2,240 gpt calls the
     longest reply was 21 tokens; 1536 reserved 73 times that and made the
     ledger reservation $25 against a settled cost of $1.66. At 256 it is $10.98. A reply
     truncated at 256 would be preserved as a failure and never retried.
  2. NO review call. The seven items are byte-identical to those the parent's
     review accepted with zero blocking issues, and the review packet carries
     items only - the profile block was never part of it. Under the 16 September
     amendment a review of already-accepted material is advisory, and re-running
     one to obtain a different verdict is forbidden. The parent's recorded
     verdict is READ from the ledger and reported; it is not re-dispatched.
  3. A fresh population seed, so CANON is a replication on new agents rather
     than a re-run of the parent's.

The empty-analysis defect stays fixed at source: `declared_tasks()`.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

from phase3_budget import BudgetStop, digest, read_checked, token_cost_nano
from phase3_design_pilot import request, PRICES
from phase3_protocol_kernel import context_prompt, AXES
from phase3_recognition_recovery import verify, sha
from phase3_recognition_run import ROOT, LEDGER, Ledger, network, charge, MODELS
from phase4_crossmodel_dispatch_v2 import dispatch as crossmodel_dispatch
from phase3_representation_diagnostic import profile_parts
from phase3_variant_round import save

import phase4b_perm_pool as P
import phase5_position_counterbalance_r1 as R1   # parent collector, pinned, imported
import phase7_block_variants as BV
import phase7_semantics as S

FOLDER = ROOT / "experiments/phase7_understanding/semantics_r1"
PARENT = ROOT / "experiments/phase5_analysis/position_counterbalance_r1"
STUDY = "semantics_r1"

MODEL = R1.GPT
INHERITED_REVIEW = "position_counterbalance_r1/review/0"   # read, never re-dispatched
INHERITED_FAILURES = (R1.INHERITED_FAILURE, R1.INHERITED_FAILURE_2)

ARMS = S.CELLS                       # CANON+, CANON-, FLIP+, ... NONCE-
N_AGENTS = 40
OUTPUT_BUDGET = 256
SEEDS = {"population": 2026091901, "schedule": 2026091902, "analysis": 2026091903}
NEUTRAL = dict.fromkeys(AXES, "NEUTRAL")
BOOTSTRAP_DRAWS = 10_000

# 2,240 calls at a 256-token output budget, all on gpt. OpenAI headroom at
# designation time is $40.00 - $12.742 = $27.26; the worst case is $10.976,
# because the input bound is counted in BYTES plus a margin, not in tokens.
CAP = 12_000_000_000
PROVIDER_CAPS = {"anthropic": 32_000_000_000, "openai": 40_000_000_000}


def population():
    """The parent's draw - independent Beta marginals - under this study's seed."""
    import numpy as np
    rng = np.random.default_rng(SEEDS["population"])
    agents = []
    for i in range(N_AGENTS):
        draw = {k: float(round(rng.beta(a, b), 3)) for k, (a, b) in R1.BETA.items()}
        agents.append({"agent": i, "coordinates": draw})
    return {"n_agents": N_AGENTS, "agents": agents, "seed": SEEDS["population"],
            "note": ("Independent Beta marginals. PD is overwritten in every cell; "
                     "the other nine coordinates are identical across cells per agent.")}


def _render(profile):
    return profile_parts(context_prompt(dict(profile), NEUTRAL))[1]


def system(coordinates, variant, level):
    """The parent's E-arm system prompt with the PD entry edited in place."""
    pinned = S.pin(coordinates, level)
    canonical = R1.system(pinned, "E")
    block = _render(pinned)
    if canonical.count(block) != 1:
        raise BudgetStop("Profile block not found exactly once in the system prompt")
    edited = BV.variant(block, S.FIELD, variant,
                        invert_name=S.INVERT_NAME, nonce_name=S.NONCE_NAME)
    return canonical.replace(block, edited)


def make_job(slot, text, system_text):
    bound = len((system_text + text).encode("utf-8")) + 1024
    req = request(MODEL, system_text, text, OUTPUT_BUDGET, temperature=1)
    req["response_format"] = {"type": "json_object"}
    return {"slot": f"{STUDY}/{slot}", "kind": "probe", "stage": "profiled", "request": req,
            "input_token_bound": bound,
            "reserved_nano": token_cost_nano(bound, OUTPUT_BUDGET, *PRICES[MODEL])}


def profiled_jobs(pop):
    batch = []
    for agent in pop["agents"]:
        for variant in S.VARIANTS:
            for level in (S.HIGH, S.LOW):
                system_text = system(agent["coordinates"], variant, level)
                sign = "+" if level == S.HIGH else "-"
                tag = f"{variant}_{'hi' if level == S.HIGH else 'lo'}"
                for task_id in P.TASK_IDS:
                    job = make_job(f"profiled/{tag}/{agent['agent']}/{task_id}",
                                   R1.body(task_id, agent["agent"] % 2 == 0), system_text)
                    job["valid_actions"] = sorted(a.lower() for a in P.action_ids(task_id))
                    job["cell"] = {"arm": f"{variant}{sign}", "variant": variant,
                                   "level": level, "task": task_id,
                                   "agent": agent["agent"], "index": None}
                    batch.append(job)
    return batch


def inherited_review():
    """The parent's recorded review verdict, read from the ledger. No API call."""
    record = read_checked(LEDGER / "records" / (digest(INHERITED_REVIEW) + ".json"))
    if record.get("error"):
        raise BudgetStop("Inherited review did not complete")
    return R1.read_review(record["parsed"])


def leakage_gate():
    symmetry = P.verify_items()
    leaks = {t: P.audit_leakage(t) for t in P.TASK_IDS if P.audit_leakage(t)}
    if leaks:
        raise BudgetStop("Task text leaks: " + str(leaks))
    agents = population()["agents"]
    construction = S.verify_construction(_render, agents)
    c = agents[0]["coordinates"]
    # CANON must be the parent's prompt byte for byte: the replication gate is
    # only a replication if the instrument is the same instrument.
    for level in (S.LOW, S.HIGH):
        if system(c, "CANON", level) != R1.system(S.pin(c, level), "E"):
            raise BudgetStop("CANON system prompt differs from the parent's")
    for variant in S.VARIANTS:
        text = system(c, variant, S.HIGH)
        if "Ethical guidance" in text:
            raise BudgetStop(f"{variant}: arm carries guidance text")
        names = {"CANON": "Procedural Dependence", "FLIP": "Procedural Dependence",
                 "INVERT": S.INVERT_NAME, "NONCE": S.NONCE_NAME}
        if text.count(f" 6. {names[variant]}: 0.90") != 1:
            raise BudgetStop(f"{variant}: PD entry not rendered as designed")
        if variant in ("INVERT", "NONCE") and "Procedural Dependence" in text:
            raise BudgetStop(f"{variant}: the canonical name survives elsewhere in the prompt")
    return {"items_verified": symmetry, "construction_verified": construction,
            "locked_prediction": S.LOCKED_PREDICTION, "semantics_sha256": S.content_hash(),
            "task_content_sha256": P.content_hash(), "output_budget": OUTPUT_BUDGET,
            "inherited_review": {"slot": INHERITED_REVIEW, **inherited_review()}}


def declared_tasks():
    return list(P.TASK_IDS)


def _good(r):
    return P.primary_net(r["task"], r["choice"]) == "good"


def analyse(rows):
    """Within-variant effects, then DIRECT contrasts between variants.

    Primary: e_CANON - e_V as a within-unit difference of differences with a
    unit-bootstrap interval. The ratio indices are descriptive. Nothing is read
    from one arm clearing a threshold while another does not.
    """
    import numpy as np
    tasks = declared_tasks()
    table = {}
    for r in rows:
        if r.get("choice") and r["task"] in tasks:
            table.setdefault((r["agent"], r["task"]), {})[r["arm"]] = _good(r)

    def sign_test(variant, subset, one_sided_positive=False):
        pairs = [(v[f"{variant}-"], v[f"{variant}+"]) for (a, t), v in table.items()
                 if t in subset and f"{variant}-" in v and f"{variant}+" in v]
        if not pairs:
            return None
        hi = sum(1 for lo, h in pairs if h and not lo)
        lo = sum(1 for lo, h in pairs if lo and not h)
        n = hi + lo
        tail = lambda k: sum(math.comb(n, i) for i in range(k + 1)) / (2 ** n) if n else 1.0
        two = min(1.0, 2 * tail(min(hi, lo))) if n else 1.0
        out = {"pairs": len(pairs), "more_under_high": hi, "more_under_low": lo,
               "effect": round((hi - lo) / len(pairs), 4), "p_two_sided": round(two, 8)}
        if one_sided_positive:
            out["p_one_sided_positive"] = round(tail(lo) if n else 1.0, 8)
        return out

    within = {v: sign_test(v, tasks, one_sided_positive=(v == "CANON")) for v in S.VARIANTS}
    per_item = {v: {t: sign_test(v, [t]) for t in tasks} for v in S.VARIANTS}

    # Holm over the four within-variant tests. CANON's is the one-sided gate test.
    raw = {v: (w["p_one_sided_positive"] if v == "CANON" else w["p_two_sided"])
           for v, w in within.items() if w}
    holm, running = {}, 0.0
    for i, (v, p) in enumerate(sorted(raw.items(), key=lambda kv: kv[1])):
        running = min(1.0, max(running, p * (len(raw) - i)))
        holm[v] = round(running, 8)

    def consistency(v):
        effs = [w["effect"] for w in per_item[v].values() if w]
        return {"items": len(effs), "positive": sum(e > 0 for e in effs),
                "negative": sum(e < 0 for e in effs)}
    cons = {v: consistency(v) for v in S.VARIANTS}

    # Unit bootstrap over agent-item units present in ALL eight cells.
    units = [v for v in table.values() if all(a in v for a in ARMS)]
    d = {v: np.array([int(u[f"{v}+"]) - int(u[f"{v}-"]) for u in units], float)
         for v in S.VARIANTS}
    rng = np.random.default_rng(SEEDS["analysis"])
    idx = rng.integers(0, len(units), size=(BOOTSTRAP_DRAWS, len(units))) if units else None

    def interval(x):
        if idx is None:
            return None
        means = x[idx].mean(axis=1)
        lo, hi = np.percentile(means, [2.5, 97.5])
        return {"estimate": round(float(x.mean()), 4),
                "ci95": [round(float(lo), 4), round(float(hi), 4)],
                "excludes_zero": bool(lo > 0 or hi < 0)}

    effects = {v: interval(d[v]) for v in S.VARIANTS}
    differences = {f"CANON-{v}": interval(d["CANON"] - d[v])
                   for v in S.VARIANTS if v != "CANON"}

    def ratio(v):
        if idx is None:
            return None
        num, den = d[v][idx].mean(axis=1), d["CANON"][idx].mean(axis=1)
        ok = np.abs(den) > 1e-9
        lo, hi = np.percentile(num[ok] / den[ok], [2.5, 97.5])
        return {"estimate": round(float(d[v].mean() / d["CANON"].mean()), 4)
                if abs(d["CANON"].mean()) > 1e-9 else None,
                "ci95": [round(float(lo), 4), round(float(hi), 4)],
                "note": "descriptive; the within-unit difference is primary"}

    gate = bool(within["CANON"] and holm.get("CANON", 1.0) < 0.05
                and cons["CANON"]["positive"] >= 4)
    if not gate:
        decision = "gate_failed"
        reading = ("e_CANON did not replicate under the prespecified gate. Nothing else "
                   "in this designation is interpreted.")
        indices = None
    else:
        indices = {"reversal_FLIP": ratio("FLIP"), "reversal_INVERT": ratio("INVERT"),
                   "transfer_NONCE": ratio("NONCE")}
        f = effects["FLIP"]
        if f["estimate"] < 0 and f["excludes_zero"] and cons["FLIP"]["negative"] >= 4:
            decision = "meaning_carries_it"
            reading = ("With name, line, number and character multiset held fixed, exchanging "
                       "what the two ends of the scale are said to mean REVERSES the effect. "
                       "Behaviour tracks the stated meaning of the scale. This is not a "
                       "demonstration of understanding, and does not separate reading an "
                       "explanation from following an instruction phrased as one.")
        elif f["estimate"] > 0 and f["excludes_zero"]:
            decision = "explanation_ignored"
            reading = ("The effect keeps its sign when the explanation is reversed: the name "
                       "and number carry it and the explanation does not dominate. How much "
                       "the explanation contributes is given by CANON-FLIP.")
        else:
            decision = "conflict"
            reading = ("Setting the name against the explanation neither reverses nor preserves "
                       "the effect cleanly. The explanation matters but does not dominate the "
                       "name; reported through CANON-FLIP and the reversal index, not rounded "
                       "to either reading.")

    return {"units_complete": len(units), "within_variant": within, "per_item": per_item,
            "holm": holm, "holm_family_size": len(raw), "consistency": cons,
            "effects_bootstrap": effects, "differences_from_canon": differences,
            "indices": indices, "gate_passed": gate, "decision": decision, "reading": reading,
            "bootstrap": {"draws": BOOTSTRAP_DRAWS, "seed": SEEDS["analysis"],
                          "unit": "agent-item, conditional on the tested items"},
            "task_list_source": "declared_tasks()",
            "locked_prediction": S.LOCKED_PREDICTION}


def _ledger_clean(ledger):
    allowed = {digest(f) for f in INHERITED_FAILURES}
    if ledger.state["pending"] or not set(ledger.state["failed"]) <= allowed:
        raise BudgetStop("Unexpected unresolved dispatch in inherited evidence")


def prepare(persist=False):
    leak = leakage_gate()
    parent = read_checked(PARENT / "release.json")
    checkpoint = PARENT / "CHECKPOINT.json"
    check = read_checked(checkpoint) if checkpoint.exists() else parent
    verify(parent)
    with Ledger(LEDGER, parent) as ledger:
        _ledger_clean(ledger)
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

    expected = N_AGENTS * len(ARMS) * len(P.TASK_IDS)
    if len(slots) != expected or bound > CAP:
        raise BudgetStop(f"Size or cap exceeded: {len(slots)} calls, {bound / 1e9:.6f} USD")
    for provider, total in providers.items():
        if total > PROVIDER_CAPS[provider]:
            raise BudgetStop(f"{provider} ceiling would be exceeded: "
                             f"{total / 1e9:.4f} > {PROVIDER_CAPS[provider] / 1e9:.2f}")

    paths = [Path(__file__), ROOT / "code/phase7_semantics.py",
             ROOT / "code/phase7_block_variants.py",
             ROOT / "code/phase5_position_counterbalance_r1.py",
             ROOT / "code/phase5_position_render.py", ROOT / "code/phase4b_perm_pool.py",
             ROOT / "code/phase4_crossmodel_dispatch_v2.py",
             ROOT / "code/phase4_choice_extraction_v2.py",
             FOLDER / "PROTOCOL.md", ROOT / "code/phase3_protocol_kernel.py",
             ROOT / "prompts/system_prompt_template.md"]
    release = {"id": STUDY, "population_sha256": digest(pop), "jobs_sha256": digest(batch),
               "slots": slots, "recognition_cap_nano": bound, "prior_screening_nano": 0,
               "original_screening_cap_nano": CAP,
               "provider_caps_nano": {**parent["provider_caps_nano"], **PROVIDER_CAPS},
               "parent_checkpoint_sha256": digest(check), "leakage_gate": leak,
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
        _ledger_clean(ledger)
        seen, rows = set(), []
        for job in batch:
            record, _ = crossmodel_dispatch(ledger, job, digest(manifest), responder, replay)
            if charge(record["raw"], job, False) != record["accounted_nano"]:
                raise BudgetStop("Cost replay mismatch")
            seen.add(digest(job["slot"]))
            rows.append({**job["cell"], "choice": record["parsed"]})
            if len(rows) % 100 == 0:
                print(json.dumps({"progress": len(rows), "of": len(batch),
                                  "usd": round(ledger.state["recognition_nano"] / 1e9, 6)}),
                      flush=True)
        save(folder / "all_rows.json", rows)
        result = {"study": STUDY, "decision": "complete", "analysis": analyse(rows),
                  "profiled_calls": len(rows), "moral_scores_assigned": False,
                  "review": release["leakage_gate"]["inherited_review"],
                  "note": ("Deterministic choice counts under stipulated standards. No moral "
                           "label is assigned and no moral quality is measured.")}
        print(json.dumps({"analysis": result["analysis"]}), flush=True)
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
        # Offline only: gates, schedule size and worst-case cost. Writes nothing.
        gate = leakage_gate()
        batch = profiled_jobs(population())
        print(json.dumps({"gates": "passed", "calls": len(batch),
                          "maximum_usd": sum(j["reserved_nano"] for j in batch) / 1e9,
                          "inherited_review_verdict": gate["inherited_review"]["verdict"],
                          "seed": SEEDS["population"]}))
    elif args.command == "prepare":
        release, _, batch = prepare(True)
        print(json.dumps({"maximum_usd": release["recognition_cap_nano"] / 1e9,
                          "total_calls": len(batch), "seed": SEEDS["population"]}))
    else:
        if not args.yes:
            raise BudgetStop("Explicit execution flag required")
        print(json.dumps(collect()))
