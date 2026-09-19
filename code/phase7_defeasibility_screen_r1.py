"""Review gate and unprofiled dispersion screen for the Stage 3a twin items.

Items and rationale live in `phase7_defeasibility_items`. This designation spends
the minimum needed to learn whether the twins can carry a profiled study at all:

  1. ONE independent review (claude-sonnet-4-6). The twins are NEW material, so
     under the 16 September amendment an accepted review is a HARD gate. A
     `revise` or `reject` stops the designation. It is not re-run.
  2. 25 unprofiled decisions on each of the seven twins, gpt-5.4-mini, no profile
     block: 175 calls. Presentation order alternates.

**Usability rule, fixed before collection.** A twin is usable if its unprofiled
keep-share lies in [0.10, 0.90] - both options live. That is stricter than the
parent pool's "modal share below 1.00", because a profiled study needs room to
move in BOTH directions: the two readings of PD predict opposite signs. The
profiled stage needs at least 4 usable twins. Screening is on baseline dispersion
only; no profiled outcome exists yet to select on.

No profile is rendered, no parameter is manipulated and no moral label is
assigned. The base items are not re-screened: they have been screened four times
on this model with consistent results.
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
import phase7_defeasibility_items as D

FOLDER = ROOT / "experiments/phase7_understanding/defeasibility_screen_r1"
PARENT = ROOT / "experiments/phase7_understanding/probe_fields_r1"
STUDY = "defeasibility_screen_r1"

SCREEN_N = 25
KEEP_BAND = (0.10, 0.90)
MIN_USABLE = 4
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


def review_packet():
    return {"items": {f"item_{i:02d}": {"item": D.body(t, True, True)}
                      for i, t in enumerate(D.TASK_IDS)},
            "design_note": ("Every item offers two options and each option sets aside a "
                            "different stipulated expectation. How the holder came by "
                            "the arrangement is stated as fact in every item; that is "
                            "intended.")}


def review_job():
    job = R1.make_job(JUDGE, "review/0", "review",
                      json.dumps(review_packet(), ensure_ascii=False, sort_keys=True),
                      1024, REVIEW_PROMPT)
    job["slot"] = f"{STUDY}/review/0"
    job["raw_text"] = True
    return job


def screen_jobs():
    batch, system_text = [], R1.system(None, "U")
    for t in D.TASK_IDS:
        for i in range(SCREEN_N):
            job = C.make_job("x", D.body(t, True, i % 2 == 0), system_text)
            job["slot"] = f"{STUDY}/screen/{t}/{i}"
            job["stage"] = "screen"
            job["valid_actions"] = sorted(a.lower() for a in P.action_ids(t))
            job["cell"] = {"arm": "U", "task": t, "twin": True, "index": i}
            batch.append(job)
    return batch


def gate():
    twins = D.verify_twins(R1.body)
    if "Procedural Dependence" in R1.system(None, "U"):
        raise BudgetStop("Unprofiled system prompt carries a profile block")
    if set(review_packet()) != {"items", "design_note"}:
        raise BudgetStop("Review packet carries unexpected keys")
    return {"twins_verified": twins, "twin_content_sha256": D.content_hash(),
            "base_content_sha256": P.content_hash(), "screen_n": SCREEN_N,
            "keep_band": list(KEEP_BAND), "min_usable": MIN_USABLE}


def screen_outcome(rows):
    out = {}
    for t in D.TASK_IDS:
        votes = [r["choice"] for r in rows if r["task"] == t and r["choice"]]
        keep = sum(1 for v in votes if v == D.KEEP_ACTION[t]) / len(votes) if votes else None
        base = P.SCREENED.get(t, {})
        base_keep = base.get("good")
        out[t] = {"n_valid": len(votes), "keep_share": None if keep is None else round(keep, 4),
                  "base_keep_share_prior_screen": base_keep,
                  "usable": keep is not None and KEEP_BAND[0] <= keep <= KEEP_BAND[1]}
    return out


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
    if len(slots) != 1 + SCREEN_N * len(D.TASK_IDS) or bound > CAP:
        raise BudgetStop(f"Size or cap exceeded: {len(slots)} calls, {bound / 1e9:.6f} USD")
    for provider, total in providers.items():
        if total > PROVIDER_CAPS[provider]:
            raise BudgetStop(f"{provider} ceiling would be exceeded: {total / 1e9:.4f}")
    paths = [Path(__file__), ROOT / "code/phase7_defeasibility_items.py",
             ROOT / "code/phase7_probe_fields_r1.py", ROOT / "code/phase7_probe_fields.py",
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
            usable = [t for t, v in screen.items() if v["usable"]]
            result = {"study": STUDY,
                      "decision": "screen_pass" if len(usable) >= MIN_USABLE else "screen_stop",
                      "screen": screen, "usable_twins": usable, "screen_calls": len(rows),
                      "moral_scores_assigned": False}
            print(json.dumps({"screen": screen, "usable": usable}), flush=True)
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
