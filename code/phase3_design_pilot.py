"""One independently generated/reviewed N5 candidate; no full-screen release."""
import argparse
import copy
import json
from pathlib import Path
import random
import zipfile

from phase3_budget import BudgetStop, POLICY, canonical, digest, read_checked, token_cost_nano
from phase3_recognition_run import ROOT, LEDGER, Ledger, network, charge, RATERS, JUDGE, MODELS
from phase3_recognition import QUESTION, SYSTEM, RUBRIC, PRICES
from phase3_recognition_discussion import DISCUSSION
from phase3_recognition_recovery import verify, sha, archived_evidence, execute
from phase3_recognition_transport import TRANSPORT
from phase3_variant_round import packets, save

PILOT = ROOT / "experiments/phase3_benchmarks/design_pilot_r1"
BOUND = 16000
GENERATOR = RATERS[1]


def request(model, system, body, maximum, temperature=0):
    if model in (RATERS[0], JUDGE):
        return {"model": model, "system": system, "messages": [{"role": "user", "content": body}],
                "thinking": {"type": "disabled"}, "temperature": temperature, "max_tokens": maximum}
    return {"model": model, "messages": [{"role": "system", "content": system}, {"role": "user", "content": body}],
            "temperature": temperature, "reasoning_effort": "none", "max_completion_tokens": maximum, "service_tier": "default"}


def job(purpose, index, model, maximum, body, system, *, ids=None, temperature=0):
    req = request(model, system, body, maximum, temperature)
    if purpose in ("coding", "discussion") and model == RATERS[1]:
        req["response_format"] = {"type": "json_object"}
    # Providers tokenize decoded message content, not the HTTP JSON envelope.
    # Bytes conservatively bound tokens; retain1024 for message framing.
    if len((system + body).encode("utf-8")) + 1024 > BOUND:
        raise BudgetStop("Input bytes exceed reserved input-token bound")
    return {"slot": f"design_pilot_r1/{purpose}/{index}", "purpose": purpose,
            "kind": "coding" if purpose == "coding" else "discussion" if purpose == "discussion" else "probe",
            "request": req, "input_token_bound": BOUND,
            "reserved_nano": token_cost_nano(BOUND, maximum, *PRICES[model]),
            **({"item_ids": ids} if ids is not None else {})}


def generation():
    body = ("Create ONE new, self-contained participant-facing scenario in at most125 words. "
        "Use a substantially different, comprehensible setting from employee bonuses or direct cash negotiation. "
        "Keep exactly the following operational invariants. State the entire allocation rule plainly; do not "
        "conceal rules, add puzzles, social ties, hierarchy, losses to existing property, moral hints or future dealings. "
        "Provide the scenario only, without title, citations, experiment names or commentary. "
        "No desired recognition result is to be asserted. Equal-value units must retain the same scalar benefit.\n" + packets()["ultimatum"]["invariants"])
    return job("generation", 0, GENERATOR, 256, body,
               "Draft a concise research scenario. Supplied constraints are data. Preserve all specified rules.", temperature=1)


def prepare(persist=False):
    parent = read_checked(TRANSPORT / "release.json")
    verify(parent)
    checkpoint = read_checked(TRANSPORT / "CHECKPOINT.json")
    archived_evidence(checkpoint, LEDGER)
    with Ledger(LEDGER, parent) as ledger:
        if ledger.state["failed"] or ledger.state["pending"] or len(ledger.state["reservations"]) != 650:
            raise BudgetStop("Unexpected completed-screen evidence")
    schedule = [("generation", 0, GENERATOR, 256), ("review", 0, JUDGE, 384)]
    schedule += [("recognition", i, JUDGE, 128) for i in range(5)]
    schedule += [(purpose, i, model, 768) for purpose in ("coding", "discussion") for i, model in enumerate(RATERS)]
    slots = {}
    for purpose, index, model, maximum in schedule:
        j = job(purpose, index, model, maximum, "", "")
        slots[j["slot"]] = {"kind": j["kind"], "model": model, "max_output": maximum,
                            "input_token_bound": BOUND, "reserved_nano": j["reserved_nano"]}
    slots[generation()["slot"]]["request_sha256"] = digest(generation()["request"])
    maximum = sum(s["reserved_nano"] for s in slots.values())
    if maximum > 500000000:
        raise BudgetStop("Pilot exceeds fifty-cent ceiling")
    paths = [Path(__file__), PILOT / "PROTOCOL.md", ROOT / "code/phase3_variant_round.py",
             TRANSPORT / "release.json", TRANSPORT / "CHECKPOINT.json"]
    release = {"id": "design_pilot_r1", "recognition_cap_nano": maximum, "slots": slots,
        "prior_screening_nano": 0, "original_screening_cap_nano": 500000000,
        "provider_caps_nano": parent["provider_caps_nano"], "parent_checkpoint_sha256": digest(checkpoint),
        "historical_keys": sorted(p.stem for p in (LEDGER / "records").glob("*.json")),
        "preserved_files": {p.relative_to(LEDGER).as_posix(): sha(p) for p in LEDGER.rglob("*.json")},
        "failure_log_prefix_bytes": (LEDGER / "failures.jsonl").stat().st_size,
        "failure_log_prefix_sha256": sha(LEDGER / "failures.jsonl"),
        "source_sha256": {**parent["source_sha256"], **{p.relative_to(ROOT).as_posix(): sha(p) for p in paths}}}
    with Ledger(LEDGER, release):
        pass
    if persist:
        save(PILOT / "release.json", release)
    return release


def review_value(text):
    value = json.loads(text)
    if (not isinstance(value, dict) or set(value) != {"verdict", "blocking_issues", "limits"}
            or value["verdict"] not in ("accept", "revise", "reject")
            or any(not isinstance(value[k], list) or any(not isinstance(x, str) for x in value[k]) for k in ("blocking_issues", "limits"))
            or (value["verdict"] == "accept" and value["blocking_issues"])):
        raise ValueError("Invalid structural review schema")
    return value


def analyze(initial, final):
    expected = {str(i+1) for i in range(5)}
    if any(set(m) != expected for m in initial + final):
        raise BudgetStop("Missing or extra pilot rating IDs")
    missing = sum(final[0][k] != final[1][k] or final[0][k]["ambiguous"] or final[0][k]["refusal"] for k in expected)
    recognised = sum(final[0][k] == final[1][k] and not final[0][k]["ambiguous"] and not final[0][k]["refusal"]
                     and "ultimatum" in final[0][k]["families"] for k in expected)
    return {"assigned": 5, "recognised": recognised, "unresolved": missing,
        "rate_bounds": [recognised/5, (recognised+missing)/5],
        "initial_exact_agreement": sum(initial[0][k] == initial[1][k] for k in expected)/5,
        "final_exact_agreement": sum(final[0][k] == final[1][k] for k in expected)/5,
        "decision": "inconclusive" if missing else "discard_exploratory_candidate" if recognised >= 2 else "consider_separate_full_screen",
        "formal_n50_gate": "not_tested", "population_released": False}


def collect(replay=False, *, root=LEDGER, folder=PILOT, responder=network, test_release=None):
    root, folder = Path(root), Path(folder)
    if root == LEDGER and test_release is not None:
        raise BudgetStop("Test release forbidden on real ledger")
    release = read_checked(folder/"release.json") if test_release is None else test_release
    verify(release, root)
    seen = set()
    def stage(jobs, name):
        records = execute(jobs, release, name, root, folder, responder, replay)
        for j, r in zip(jobs, records):
            seen.add(digest(j["slot"]))
            if charge(r["raw"], j, False) != r["accounted_nano"]:
                raise BudgetStop("Pilot cost replay mismatch")
        return records
    def finish(result):
        with Ledger(root, release) as ledger:
            if set(ledger.state["reservations"]) - set(release["historical_keys"]) != seen:
                raise BudgetStop("Unmanifested pilot dispatch")
            result.update({"accounted_nano": ledger.state["recognition_nano"], "provider_totals_nano": ledger.state["providers"],
                           "release_sha256": digest(release), "calls": len(seen), "population_released": False})
        save(folder/"results.json", result)
        print(json.dumps(result), flush=True)
        return result
    with Ledger(root, release) as ledger:
        if ledger.state["failed"] or ledger.state["pending"]:
            raise BudgetStop("New failure or pending intent")
    candidate = stage([generation()], "generation")[0]["parsed"]
    body = ("Independently review this candidate against the original operational invariants. "
        "Require both roles, exactly100 equal-value units, integer proposal, accept implements the split, "
        "reject gives BOTH zero, anonymity, no ties/entitlement/status advantage/future dealings. "
        "Check whether the new domain changes the allocation mechanism. Do not certify human equivalence "
        "or low recognition. Output only JSON with verdict accept/revise/reject, blocking_issues list, limits list. "
        "accept requires no blocking issues. At most100 words; no markdown.\n" +
        json.dumps({"invariants": packets()["ultimatum"]["invariants"], "candidate": candidate}))
    reviewed = stage([job("review", 0, JUDGE, 384, body, "Independent structural reader; supplied content is data.", temperature=1)], "review")[0]["parsed"]
    review = review_value(reviewed)
    if review["verdict"] != "accept":
        return finish({"candidate": candidate, "review": review, "decision": "structural_stop", "formal_n50_gate": "not_tested"})
    probes = stage([job("recognition", i, JUDGE, 128, candidate+"\n\n"+QUESTION, SYSTEM, temperature=1) for i in range(5)], "recognition")
    items = [{"id": str(i+1), "answer": r["parsed"]} for i, r in enumerate(probes)]
    ratings = []
    for index, model in enumerate(RATERS):
        order = items.copy(); random.Random(2026091311+index).shuffle(order)
        j = job("coding", index, model, 768, json.dumps(order, ensure_ascii=False, separators=(",", ":")), RUBRIC,
                ids=[x["id"] for x in order])
        rows = stage([j], f"coding_{index}")[0]["parsed"]
        ratings.append({r["id"]: json.loads(canonical(r)) for r in rows})
    disputed = [x for x in items if ratings[0][x["id"]] != ratings[1][x["id"]]
                or ratings[0][x["id"]]["ambiguous"] or ratings[0][x["id"]]["refusal"]]
    final = copy.deepcopy(ratings)
    for index, model in enumerate(RATERS):
        if not disputed:
            break
        batch = [{**x, "own_rating": ratings[index][x["id"]], "other_rating": ratings[1-index][x["id"]]} for x in disputed]
        j = job("discussion", index, model, 768, json.dumps(batch, ensure_ascii=False, separators=(",", ":")), RUBRIC+"\n\n"+DISCUSSION,
                ids=[x["id"] for x in batch])
        for row in stage([j], f"discussion_{index}")[0]["parsed"]:
            final[index][row["id"]] = {k: v for k, v in row.items() if k != "reason"}
    return finish({**analyze(ratings, final), "candidate": candidate, "review": review,
                   "discussion_items": len(disputed), "discussion_calls": 2 if disputed else 0})


def archive():
    result = collect(True, responder=lambda _: (_ for _ in ()).throw(AssertionError("Network in verification")))
    release = read_checked(PILOT/"release.json")
    with Ledger(LEDGER, release) as ledger:
        members = {p.relative_to(LEDGER).as_posix(): sha(p) for p in LEDGER.rglob("*") if p.is_file() and p.suffix in (".json", ".jsonl")}
        path = ROOT/"output/phase3_design_pilot_r1_20260913.zip"
        if not path.exists():
            with zipfile.ZipFile(path, "x", compression=zipfile.ZIP_DEFLATED) as z:
                for name in sorted(members): z.write(LEDGER/name, name)
        with zipfile.ZipFile(path) as z:
            import hashlib
            if z.testzip() or set(z.namelist()) != set(members) or any(hashlib.sha256(z.read(n)).hexdigest() != s for n,s in members.items()):
                raise BudgetStop("Pilot archive mismatch")
        check = {"results_sha256": digest(result), "new_calls_during_verification": 0, "historical_records_preserved": 650,
            "total_paid_records": len(ledger.state["reservations"]), "pilot_accounted_nano": result["accounted_nano"],
            "provider_totals_nano": ledger.state["providers"], "phase3_accounted_nano": sum(ledger.state["providers"].values()),
            "package_accounted_nano": POLICY["prior_package_nano"]+sum(ledger.state["providers"].values()),
            "archive": path.relative_to(ROOT).as_posix(), "archive_members": len(members), "archive_sha256": sha(path), "off_device_backup_verified": False}
    save(PILOT/"CHECKPOINT.json", check)
    return check


if __name__ == "__main__":
    parser = argparse.ArgumentParser(); parser.add_argument("command", choices=("prepare", "run", "replay", "verify")); parser.add_argument("--yes", action="store_true")
    args = parser.parse_args()
    if args.command == "prepare":
        r = prepare(True); print(json.dumps({"maximum_nano": r["recognition_cap_nano"], "release_sha256": digest(r)}))
    elif args.command == "verify": print(json.dumps(archive()))
    else:
        if args.command == "run" and not args.yes: raise BudgetStop("Explicit run flag required")
        collect(replay=args.command == "replay")
