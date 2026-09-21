"""Collector for inverse_inference_r1: reading a field back from behaviour.

Design, conditions, the measured ceiling and the locked predictions live in
`phase7_inverse_inference`. This module dispatches.

**120 calls on gpt-5.4-mini**: 3 conditions x 40 paired trials. Each trial shows
two transcripts from the SAME agent of `pd_prospective_r1` - one produced at PD
0.10, one at 0.90 - and asks which agent had the setting HIGH.

**No new participant data.** The transcripts are read from the frozen
`pd_prospective_r1` archive. That designation's review is inherited and recorded,
never re-dispatched; the items themselves are the same seven, byte-identical.

**A/B order is randomised per trial from a fixed seed** and the correct answer is
recorded per trial before collection, so accuracy is scored against a key that
exists in the release, not derived afterwards.

The output cap is 256 as in every Phase 7 designation. No profile block is
rendered: the model is a judge here, not an agent, so `R1.system(None, "U")`
supplies the unprofiled system prompt and the whole task is in the user turn.
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
import phase7_inverse_inference as F

FOLDER = ROOT / "experiments/phase7_understanding/inverse_inference_r1"
PARENT = ROOT / "experiments/phase7_understanding/parameter_followup_r2"
STUDY = "inverse_inference_r1"

SEEDS = {"order": 2026092131, "analysis": 2026092132}
BOOTSTRAP_DRAWS = 10_000
CAP = 1_000_000_000
PROVIDER_CAPS = C.PROVIDER_CAPS


def _describe(task_id):
    """One clause identifying the situation, from the item's own first sentence."""
    return P.task(task_id)["situation"].split(".")[0]


def records():
    rows = read_checked(ROOT / F.SOURCE)
    return F.transcripts(rows, P.TASK_IDS)


def trials():
    """One trial per agent, A/B order fixed by seed, with the answer key."""
    import numpy as np
    rec = records()
    rng = np.random.default_rng(SEEDS["order"])
    out = []
    for agent in sorted(rec):
        high_is_a = bool(rng.integers(0, 2))
        first = rec[agent]["PD+" if high_is_a else "PD-"]
        second = rec[agent]["PD-" if high_is_a else "PD+"]
        out.append({"agent": agent, "high_is_a": high_is_a,
                    "answer": "A" if high_is_a else "B",
                    "first": first, "second": second})
    if len(out) != F.N_TRIALS:
        raise BudgetStop(f"Expected {F.N_TRIALS} trials, built {len(out)}")
    return out


def judge_jobs(built):
    batch, system_text = [], R1.system(None, "U")
    for condition in F.CONDITIONS:
        for t in built:
            text = F.trial_prompt(condition, t["first"], t["second"], _describe)
            job = C.make_job("x", text, system_text)
            job["slot"] = f"{STUDY}/judge/{condition}/{t['agent']}"
            job["stage"] = "judge"
            job["valid_actions"] = ["a", "b"]
            job["cell"] = {"condition": condition, "agent": t["agent"],
                           "answer": t["answer"], "high_is_a": t["high_is_a"]}
            batch.append(job)
    return batch


def leakage_gate():
    symmetry = P.verify_items()
    rec = records()
    if len(rec) != F.N_TRIALS:
        raise BudgetStop(f"Expected {F.N_TRIALS} complete agents, found {len(rec)}")
    built = trials()
    if sum(t["high_is_a"] for t in built) in (0, F.N_TRIALS):
        raise BudgetStop("A/B order is degenerate")
    system_text = R1.system(None, "U")
    if "Procedural Dependence" in system_text:
        raise BudgetStop("Judge system prompt carries a profile block")
    for condition in F.CONDITIONS:
        text = F.trial_prompt(condition, built[0]["first"], built[0]["second"], _describe)
        named = "Procedural Dependence" in text
        glossed = "process-dominant" in text
        if condition == "BLIND" and (named or glossed):
            raise BudgetStop("BLIND condition names or glosses the field")
        if condition == "NAMED" and (not named or glossed):
            raise BudgetStop("NAMED condition is not name-only")
        if condition == "GLOSSED" and not (named and glossed):
            raise BudgetStop("GLOSSED condition lacks the name or the gloss")
        if "0.10" in text or "0.90" in text or "PD" in text:
            raise BudgetStop(f"{condition}: the prompt leaks the pinned value")
    return {"items_verified": symmetry, "complete_agents": len(rec),
            "ceiling": F.ceiling(rec, P.clean_action),
            "locked_prediction": F.LOCKED_PREDICTION,
            "inverse_sha256": F.content_hash(),
            "task_content_sha256": P.content_hash(), "output_budget": C.OUTPUT_BUDGET,
            "inherited_review": {"slot": C.INHERITED_REVIEW, **C.inherited_review()}}


def analyse(rows):
    import numpy as np
    by = {c: [r for r in rows if r["condition"] == c and r.get("choice")]
          for c in F.CONDITIONS}
    rng = np.random.default_rng(SEEDS["analysis"])

    def binomial_ci(k, n):
        if not n:
            return None
        draws = rng.binomial(n, k / n, BOOTSTRAP_DRAWS) / n if 0 < k < n else None
        lo, hi = (float(np.percentile(draws, 2.5)), float(np.percentile(draws, 97.5))) \
            if draws is not None else ((k / n), (k / n))
        return [round(lo, 4), round(hi, 4)]

    def one_sided_p(k, n):
        if not n:
            return 1.0
        return round(sum(math.comb(n, i) for i in range(k, n + 1)) / 2 ** n, 8)

    acc = {}
    for c in F.CONDITIONS:
        n = len(by[c])
        k = sum(1 for r in by[c] if str(r["choice"]).strip().upper()[:1] == r["answer"])
        acc[c] = {"n": n, "correct": k, "accuracy": round(k / n, 4) if n else None,
                  "ci95": binomial_ci(k, n), "p_one_sided_vs_chance": one_sided_p(k, n),
                  "above_chance": bool(n and one_sided_p(k, n) < 0.05 / len(F.CONDITIONS))}

    # Paired within-trial difference over agents seen by both conditions.
    def paired(c1, c2):
        m1 = {r["agent"]: str(r["choice"]).strip().upper()[:1] == r["answer"] for r in by[c1]}
        m2 = {r["agent"]: str(r["choice"]).strip().upper()[:1] == r["answer"] for r in by[c2]}
        shared = sorted(set(m1) & set(m2))
        if not shared:
            return None
        d = np.array([int(m1[a]) - int(m2[a]) for a in shared], float)
        idx = rng.integers(0, len(d), size=(BOOTSTRAP_DRAWS, len(d)))
        lo, hi = np.percentile(d[idx].mean(axis=1), [2.5, 97.5])
        only1 = sum(1 for a in shared if m1[a] and not m2[a])
        only2 = sum(1 for a in shared if m2[a] and not m1[a])
        n = only1 + only2
        p = min(1.0, 2 * sum(math.comb(n, i) for i in range(min(only1, only2) + 1)) / 2 ** n) \
            if n else 1.0
        return {"trials": len(shared), "estimate": round(float(d.mean()), 4),
                "ci95": [round(float(lo), 4), round(float(hi), 4)],
                "excludes_zero": bool(lo > 0 or hi < 0),
                "discordant": n, "p_two_sided": round(p, 8)}

    diffs = {"GLOSSED-BLIND": paired("GLOSSED", "BLIND"),
             "NAMED-BLIND": paired("NAMED", "BLIND"),
             "GLOSSED-NAMED": paired("GLOSSED", "NAMED")}

    ceil = F.ceiling(records(), P.clean_action)
    gb = diffs["GLOSSED-BLIND"]
    any_above = any(acc[c]["above_chance"] for c in F.CONDITIONS)
    if not any_above:
        decision, reading = "no_inference", (
            "No condition exceeds chance. The model does not recover the setting from "
            "behaviour under any framing. Bidirectionality is not demonstrated.")
    elif gb and gb["excludes_zero"] and gb["estimate"] > 0:
        decision, reading = "field_recovery", (
            "Accuracy is higher when the field's description is supplied than when the "
            "model is told only that some unnamed setting differed. The description "
            "carries information the transcripts alone do not. This is bidirectionality "
            "in the weak sense the programme defined - it does NOT show the relation is "
            "conceptual, and a transcript-statistics rule reaches "
            f"{ceil['accuracy_ties_wrong']} on the same pairs.")
    else:
        decision, reading = "surface_statistic", (
            "The model is above chance, but naming or glossing the field does not help: "
            "BLIND does as well as GLOSSED. The task is solvable from transcript "
            "statistics - which transcript keeps more arrangements - and nothing "
            "specific to the field is being recovered. Bidirectionality is NOT "
            "demonstrated by this result.")

    return {"accuracy": acc, "paired_differences": diffs, "ceiling": ceil,
            "decision": decision, "reading": reading,
            "chance": 0.5, "alpha_note": "per-condition alpha Bonferroni-adjusted over 3",
            "bootstrap": {"draws": BOOTSTRAP_DRAWS, "seed": SEEDS["analysis"]},
            "locked_prediction": F.LOCKED_PREDICTION}


def prepare(persist=False):
    leak = leakage_gate()
    parent = read_checked(PARENT / "release.json")
    verify(parent)
    with Ledger(LEDGER, parent) as ledger:
        C._ledger_clean(ledger)
        providers = dict(ledger.state["providers"])
    built = trials()
    batch = judge_jobs(built)
    slots = {j["slot"]: {"kind": j["kind"], "stage": j["stage"], "model": j["request"]["model"],
                         "input_token_bound": j["input_token_bound"],
                         "reserved_nano": j["reserved_nano"],
                         "max_output": j["request"].get("max_tokens",
                                                        j["request"].get("max_completion_tokens")),
                         "request_sha256": digest(j["request"])} for j in batch}
    bound = sum(j["reserved_nano"] for j in batch)
    for j in batch:
        providers[MODELS[j["request"]["model"]]] += j["reserved_nano"]
    if len(slots) != len(F.CONDITIONS) * F.N_TRIALS or bound > CAP:
        raise BudgetStop(f"Size or cap exceeded: {len(slots)} calls, {bound / 1e9:.6f} USD")
    for provider, total in providers.items():
        if total > PROVIDER_CAPS[provider]:
            raise BudgetStop(f"{provider} ceiling would be exceeded: {total / 1e9:.4f}")
    paths = [Path(__file__), ROOT / "code/phase7_inverse_inference.py",
             ROOT / "code/phase7_semantics_r1.py", FOLDER / "PROTOCOL.md"]
    release = {"id": STUDY, "population_sha256": digest(built), "jobs_sha256": digest(batch),
               "slots": slots, "recognition_cap_nano": bound, "prior_screening_nano": 0,
               "original_screening_cap_nano": CAP,
               "provider_caps_nano": {**parent["provider_caps_nano"], **PROVIDER_CAPS},
               "parent_checkpoint_sha256": digest(parent), "leakage_gate": leak,
               "answer_key": {str(t["agent"]): t["answer"] for t in built},
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
        save(FOLDER / "trials.json", built)
        save(FOLDER / "requests.json", batch)
        save(FOLDER / "release.json", release)
    return release, built, batch


def collect(replay=False, root=LEDGER, folder=FOLDER, responder=network, test_data=None):
    root, folder = Path(root), Path(folder)
    if root == LEDGER and test_data is not None:
        raise BudgetStop("Test data on real ledger")
    leakage_gate()
    release, built, batch = test_data or tuple(
        read_checked(folder / f) for f in ("release.json", "trials.json", "requests.json"))
    verify(release, root)
    if digest(built) != release["population_sha256"] or digest(batch) != release["jobs_sha256"]:
        raise BudgetStop("Changed trials or requests")
    if batch != judge_jobs(built):
        raise BudgetStop("Reconstructed schedule differs")
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
        save(folder / "all_rows.json", rows)
        result = {"study": STUDY, "decision": "complete", "analysis": analyse(rows),
                  "judge_calls": len(rows), "moral_scores_assigned": False,
                  "review": release["leakage_gate"]["inherited_review"],
                  "note": ("The model is a judge here, not an agent. No profile block is "
                           "rendered and no new participant decisions were collected; the "
                           "transcripts come from the frozen pd_prospective_r1 archive.")}
        print(json.dumps({"analysis": result["analysis"]["accuracy"]}), flush=True)
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
        batch = judge_jobs(trials())
        print(json.dumps({"gates": "passed", "calls": len(batch),
                          "maximum_usd": sum(j["reserved_nano"] for j in batch) / 1e9,
                          "ceiling": gate["ceiling"]["accuracy_ties_wrong"],
                          "design_sha256": gate["inverse_sha256"]}))
    elif args.command == "prepare":
        release, _, batch = prepare(True)
        print(json.dumps({"maximum_usd": release["recognition_cap_nano"] / 1e9,
                          "total_calls": len(batch)}))
    else:
        if not args.yes:
            raise BudgetStop("Explicit execution flag required")
        print(json.dumps({k: v for k, v in collect().items() if k != "analysis"}))
