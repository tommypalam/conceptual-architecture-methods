"""Review gate and order-aware dispersion screen for the re-authored Stage 3a twins.

Candidates and the authoring rule live in `phase7_defeasibility_items_r2`. This is
a NEW designation on NEW wording; `defeasibility_screen_r1` stands as recorded.

  1. ONE independent review (claude-sonnet-4-6) of all ten candidates. New
     material: an accepted review is a HARD gate, and it is not re-run.
  2. 24 unprofiled decisions per candidate, 12 in each presentation order:
     240 calls on gpt-5.4-mini, no profile block.

**Usability rule, fixed before collection - the r1 rule plus the order check r1
lacked.** A candidate is usable if its pooled keep-share lies in [0.10, 0.90] AND
the keep-share gap between the two presentation orders is at most 0.20.

**Selection rule, fixed before collection.** Per item: if exactly one candidate is
usable it is taken; if both are, the one whose pooled keep-share is nearer 0.50,
ties to A; if neither, the item has no twin. `desk_booking` and `weekend_rota`
carry their r1 twins and r1 screen results (0.84 gap 0.01; 0.44 gap 0.04) and are
not re-screened. The profiled stage needs at least 4 twins in total, so at least
2 of the 5 re-authored items must yield one. Selection is on unprofiled baseline
dispersion only; no profiled outcome exists to select on.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from phase3_budget import BudgetStop, digest, read_checked
from phase3_design_pilot import JUDGE
from phase3_recognition_recovery import verify, sha
from phase3_recognition_run import ROOT, LEDGER, Ledger, network, charge, MODELS
from phase4_crossmodel_dispatch_v2 import dispatch as crossmodel_dispatch
from phase3_variant_round import save

import phase4b_perm_pool as P
import phase5_position_counterbalance_r1 as R1
import phase7_semantics_r1 as C
import phase7_defeasibility_items_r2 as D

FOLDER = ROOT / "experiments/phase7_understanding/defeasibility_screen_r2"
PARENT = ROOT / "experiments/phase7_understanding/defeasibility_screen_r1"
STUDY = "defeasibility_screen_r2"

SCREEN_N = 24          # 12 per presentation order
MAX_ORDER_GAP = 0.20
R1_CARRIED = {"desk_booking": {"keep_share": 0.84, "order_gap": 0.01},
              "weekend_rota": {"keep_share": 0.44, "order_gap": 0.04}}
KEEP_BAND = (0.10, 0.90)
MIN_TWINS = 4
CAP = 2_000_000_000
PROVIDER_CAPS = C.PROVIDER_CAPS

REVIEW_PROMPT = (
    "Review these decision items independently. Stipulated consequences are an "
    "intended and necessary part of every item; their presence is not a defect. "
    "Every item offers two options and each sets aside something a reasonable person "
    "could hold binding; there is deliberately no option that sets aside nothing. "
    "Each situation also states, as plain fact, a procedure and how the current "
    "holder came by the arrangement. That statement is an intended part of the item "
    "and its presence is not a defect. Judge whether each item is answerable and "
    "non-leading. Flag an item only if it states which option the decision-maker "
    "ought to choose beyond the stipulated facts, if the situation or either option "
    "uses evaluative or accusatory wording about any person rather than stating what "
    "happened, if the two options are unequally characterised in weight or wording, "
    "if it names a psychological construct or reveals a study hypothesis, or if its "
    "stipulated facts are internally contradictory or too unclear to act on. Do not "
    "accept merely because the design could show an effect. Return only JSON with an "
    "overall verdict accept/revise/reject, a blocking_issues list and a limits list. "
    "Under 150 words.")


def candidates():
    return [(t, k) for t in D.REAUTHORED for k in ("A", "B")]


def review_packet():
    return {"items": {f"item_{i:02d}": {"item": D.body(t, D.CANDIDATES[t][k], True)}
                      for i, (t, k) in enumerate(candidates())},
            "design_note": ("Every item offers two options and each option sets aside a "
                            "different stipulated expectation. How the holder came by "
                            "the arrangement is stated as fact in every item; that is "
                            "intended. Some items appear twice with different wording of "
                            "that fact; judge each on its own.")}


def review_job():
    job = R1.make_job(JUDGE, "review/0", "review",
                      json.dumps(review_packet(), ensure_ascii=False, sort_keys=True),
                      1024, REVIEW_PROMPT)
    job["slot"] = f"{STUDY}/review/0"
    job["raw_text"] = True
    return job


def screen_jobs():
    batch, system_text = [], R1.system(None, "U")
    for t, k in candidates():
        for i in range(SCREEN_N):
            job = C.make_job("x", D.body(t, D.CANDIDATES[t][k], i % 2 == 0), system_text)
            job["slot"] = f"{STUDY}/screen/{t}/{k}/{i}"
            job["stage"] = "screen"
            job["valid_actions"] = sorted(a.lower() for a in P.action_ids(t))
            job["cell"] = {"arm": "U", "task": t, "candidate": k, "index": i,
                           "keep_first": i % 2 == 0}
            batch.append(job)
    return batch


def gate():
    verified = D.verify_candidates()
    if "Procedural Dependence" in R1.system(None, "U"):
        raise BudgetStop("Unprofiled system prompt carries a profile block")
    return {"candidates_verified": verified, "twin_content_sha256": D.content_hash(),
            "base_content_sha256": P.content_hash(), "screen_n": SCREEN_N,
            "keep_band": list(KEEP_BAND), "max_order_gap": MAX_ORDER_GAP,
            "min_twins": MIN_TWINS, "carried_from_r1": R1_CARRIED}


def _share(votes, keep):
    return round(sum(1 for v in votes if v == keep) / len(votes), 4) if votes else None


def screen_outcome(rows):
    out = {}
    for t, k in candidates():
        keep = D.KEEP_ACTION[t]
        mine = [r for r in rows if r["task"] == t and r["candidate"] == k and r["choice"]]
        pooled = _share([r["choice"] for r in mine], keep)
        first = _share([r["choice"] for r in mine if r["keep_first"]], keep)
        second = _share([r["choice"] for r in mine if not r["keep_first"]], keep)
        gap = None if first is None or second is None else round(abs(first - second), 4)
        usable = (pooled is not None and gap is not None
                  and KEEP_BAND[0] <= pooled <= KEEP_BAND[1] and gap <= MAX_ORDER_GAP)
        out[f"{t}/{k}"] = {"n_valid": len(mine), "keep_share": pooled,
                           "keep_shown_first": first, "override_shown_first": second,
                           "order_gap": gap, "usable": usable}
    return out


def select(screen):
    chosen = {}
    for t in D.REAUTHORED:
        ok = [k for k in ("A", "B") if screen[f"{t}/{k}"]["usable"]]
        if ok:
            chosen[t] = min(ok, key=lambda k: (abs(screen[f"{t}/{k}"]["keep_share"] - 0.5), k))
    return chosen


def prepare(persist=False):
    g = gate()
    parent = read_checked(PARENT / "release.json")
    verify(parent)
    with Ledger(LEDGER, parent) as ledger:
        C._ledger_clean(ledger)
        providers = dict(ledger.state["providers"])
    batch = [review_job()] + screen_jobs()
    slots = {j["slot"]: {"kind": j["kind"], "stage": j["stage"], "model": j["request"]["model"],
                         "input_token_bound": j["input_token_bound"],
                         "reserved_nano": j["reserved_nano"],
                         "max_output": j["request"].get("max_tokens",
                                                        j["request"].get("max_completion_tokens")),
                         "request_sha256": digest(j["request"])} for j in batch}
    bound = sum(j["reserved_nano"] for j in batch)
    for j in batch:
        providers[MODELS[j["request"]["model"]]] += j["reserved_nano"]
    if len(slots) != 1 + SCREEN_N * len(candidates()) or bound > CAP:
        raise BudgetStop(f"Size or cap exceeded: {len(slots)} calls, {bound / 1e9:.6f} USD")
    for provider, total in providers.items():
        if total > PROVIDER_CAPS[provider]:
            raise BudgetStop(f"{provider} ceiling would be exceeded: {total / 1e9:.4f}")
    paths = [Path(__file__), ROOT / "code/phase7_defeasibility_items_r2.py",
             ROOT / "code/phase7_defeasibility_items.py",
             ROOT / "code/phase7_defeasibility_screen_r1.py",
             FOLDER / "PROTOCOL.md"]
    release = {"id": STUDY, "population_sha256": digest({}), "jobs_sha256": digest(batch),
               "slots": slots, "recognition_cap_nano": bound, "prior_screening_nano": 0,
               "original_screening_cap_nano": CAP,
               "provider_caps_nano": {**parent["provider_caps_nano"], **PROVIDER_CAPS},
               "parent_checkpoint_sha256": digest(parent), "leakage_gate": g,
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
        save(FOLDER / "requests.json", batch)
        save(FOLDER / "release.json", release)
    return release, batch


def collect(replay=False, root=LEDGER, folder=FOLDER, responder=network, test_data=None):
    root, folder = Path(root), Path(folder)
    if root == LEDGER and test_data is not None:
        raise BudgetStop("Test data on real ledger")
    gate()
    release, batch = test_data or tuple(
        read_checked(folder / f) for f in ("release.json", "requests.json"))
    verify(release, root)
    if digest(batch) != release["jobs_sha256"] or batch != [review_job()] + screen_jobs():
        raise BudgetStop("Changed or non-reconstructible requests")
    if release["leakage_gate"]["twin_content_sha256"] != D.content_hash():
        raise BudgetStop("Twin content changed after release")
    manifest = {"release_sha256": digest(release), "jobs_sha256": digest(batch)}
    save(folder / "execution_manifest.json", manifest)
    with Ledger(root, release) as ledger:
        C._ledger_clean(ledger)
        seen = set()

        def dispatch(job):
            record, _ = crossmodel_dispatch(ledger, job, digest(manifest), responder, replay)
            if charge(record["raw"], job, False) != record["accounted_nano"]:
                raise BudgetStop("Cost replay mismatch")
            seen.add(digest(job["slot"]))
            return record["parsed"]

        review_text = dispatch(batch[0])
        review = R1.read_review(review_text)
        save(folder / "review.json", {"verdict": review, "raw": review_text})
        print(json.dumps({"review": review}), flush=True)
        if review["verdict"] != "accept":
            result = {"study": STUDY, "decision": "review_stop", "screen_calls": 0,
                      "note": ("New materials: an accepted review is a hard gate. The "
                               "screen did not run and the review is not re-run.")}
        else:
            rows = [{**j["cell"], "choice": dispatch(j)} for j in batch[1:]]
            save(folder / "screen_rows.json", rows)
            screen = screen_outcome(rows)
            chosen = select(screen)
            twins = sorted(set(chosen) | set(R1_CARRIED))
            result = {"study": STUDY,
                      "decision": "screen_pass" if len(twins) >= MIN_TWINS else "screen_stop",
                      "screen": screen, "selected_candidates": chosen,
                      "carried_from_r1": R1_CARRIED, "twin_set": twins,
                      "screen_calls": len(rows), "moral_scores_assigned": False}
            print(json.dumps({"screen": screen, "selected": chosen, "twins": twins}),
                  flush=True)
        if set(ledger.state["reservations"]) - set(release["historical_keys"]) != seen:
            raise BudgetStop("Unmanifested dispatch")
        result.update(review=review, calls=len(seen),
                      accounted_nano=ledger.state["recognition_nano"],
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
        gate()
        batch = [review_job()] + screen_jobs()
        print(json.dumps({"gates": "passed", "calls": len(batch),
                          "maximum_usd": sum(j["reserved_nano"] for j in batch) / 1e9,
                          "twin_sha256": D.content_hash()}))
    elif args.command == "prepare":
        release, batch = prepare(True)
        print(json.dumps({"maximum_usd": release["recognition_cap_nano"] / 1e9,
                          "total_calls": len(batch)}))
    else:
        if not args.yes:
            raise BudgetStop("Explicit execution flag required")
        print(json.dumps(collect()))
