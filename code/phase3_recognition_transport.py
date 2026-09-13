"""Prospective short opaque IDs for remaining coding; no scientific rubric change."""
import argparse
import copy
import json
from pathlib import Path
import random

from phase3_budget import BudgetStop, canonical, digest, read_checked
from phase3_recognition_run import ROOT, RUN, LEDGER, PACKAGE, Ledger, RATERS, network
from phase3_recognition_recovery import (RECOVERY as PREVIOUS, REPLACEMENT, inherited,
    archived_evidence, sha, verify, execute)
from phase3_recognition_discussion import discussion_request
from phase3_recognition_analysis import analyze
from phase3_variant_round import save

TRANSPORT = RUN / "transport_r1"


def short_job(job):
    result = copy.deepcopy(job)
    original = result["item_ids"]
    if len(set(original)) != len(original) or not 1 <= len(original) <= 10:
        raise BudgetStop("Invalid original ID mapping")
    rows = json.loads(result["request"]["messages"][-1]["content"])
    if [x["id"] for x in rows] != original:
        raise BudgetStop("Request IDs differ from job IDs")
    local = [str(i+1) for i in range(len(rows))]
    for row, identity in zip(rows, local):
        row["id"] = identity
        if result["kind"] == "discussion":
            row["own_rating"]["id"] = identity
            row["other_rating"]["id"] = identity
    result["request"]["messages"][-1]["content"] = json.dumps(rows, ensure_ascii=False, separators=(",", ":"))
    result["original_item_ids"], result["item_ids"] = original, local
    result["original_slot"] = job["slot"]
    result["slot"] = "recognition_transport_r1/" + "/".join(job["slot"].split("/")[1:])
    return result


def original_rows(job, record):
    rows = record["parsed"]
    if [r["id"] for r in rows] != job["item_ids"]:
        raise BudgetStop("Unparseable local ID map")
    if len(job["original_item_ids"]) != len(rows) or len(set(job["original_item_ids"])) != len(rows):
        raise BudgetStop("Nonbijective original ID map")
    return [{**row, "id": identity} for row, identity in zip(rows, job["original_item_ids"])]


def prepare(persist=False):
    parent = read_checked(PREVIOUS / "release.json")
    verify(parent)
    prior = read_checked(PREVIOUS / "CHECKPOINT.json")
    archived_evidence(prior, LEDGER)
    with Ledger(LEDGER, parent) as ledger:
        if ledger.state["pending"] or ledger.state["failed"] != [digest(REPLACEMENT)] or len(ledger.state["reservations"]) != 578:
            raise BudgetStop("Unexpected prior recovery state")
    _, _, _, _, remaining = inherited()
    short = [short_job(j) for j in remaining]
    slots = {}
    for job, shortened in zip(remaining, short):
        slots[shortened["slot"]] = {**parent["slots"][job["slot"]], "request_sha256": digest(shortened["request"])}
    for slot, cap in parent["slots"].items():
        if cap["kind"] == "discussion":
            slots["recognition_transport_r1/" + "/".join(slot.split("/")[1:])] = copy.deepcopy(cap)
    maximum = sum(x["reserved_nano"] for x in slots.values())
    if prior["screening_accounted_nano"] + maximum > parent["original_screening_cap_nano"]:
        raise BudgetStop("Transport amendment exceeds screening ceiling")
    paths = [Path(__file__), TRANSPORT / "PROTOCOL.md", PREVIOUS / "release.json", PREVIOUS / "CHECKPOINT.json"]
    release = {"id": "recognition_transport_r1", "parent_release_sha256": digest(parent),
        "prior_screening_nano": prior["screening_accounted_nano"],
        "original_screening_cap_nano": parent["original_screening_cap_nano"],
        "recognition_cap_nano": maximum, "slots": slots,
        "provider_caps_nano": parent["provider_caps_nano"],
        "historical_keys": sorted(p.stem for p in (LEDGER / "records").glob("*.json")),
        "preserved_files": {p.relative_to(LEDGER).as_posix(): sha(p) for p in LEDGER.rglob("*.json")},
        "failure_log_prefix_bytes": (LEDGER / "failures.jsonl").stat().st_size,
        "failure_log_prefix_sha256": sha(LEDGER / "failures.jsonl"),
        "source_sha256": {**parent["source_sha256"], **{p.relative_to(ROOT).as_posix(): sha(p) for p in paths}}}
    with Ledger(LEDGER, release):
        pass
    if persist:
        save(TRANSPORT / "release.json", release)
    return release


def collect(replay=False, *, root=LEDGER, folder=TRANSPORT, responder=network, test_release=None):
    root, folder = Path(root), Path(folder)
    if root == LEDGER and test_release is not None:
        raise BudgetStop("Test release forbidden on real ledger")
    release = read_checked(folder / "release.json") if test_release is None else test_release
    verify(release, root)
    with Ledger(root, release) as ledger:
        if ledger.state["failed"] or ledger.state["pending"]:
            raise BudgetStop("New failure/pending intent blocks transport continuation")
    jobs, items, original_coding, saved, remaining = inherited(root)
    coding = [short_job(j) for j in remaining]
    results = execute(coding, release, "coding", root, folder, responder, replay)
    for job, record in zip(coding, results):
        original = "recognition_r1/" + "/".join(job["slot"].split("/")[1:])
        saved[original] = {"parsed": original_rows(job, record)}
    ratings = [{}, {}]
    for job in original_coding:
        for row in saved[job["slot"]]["parsed"]:
            if row["id"] in ratings[job["rater"]]:
                raise BudgetStop("Duplicate reconstructed rating")
            ratings[job["rater"]][row["id"]] = json.loads(canonical(row))
    unresolved = [x for x in items if ratings[0][x["id"]] != ratings[1][x["id"]]
                  or ratings[0][x["id"]]["ambiguous"] or ratings[0][x["id"]]["refusal"]]
    full = read_checked(PACKAGE / "discussion_cost_plan.json")
    discussions = []
    for index, model in enumerate(RATERS):
        order = sorted(unresolved, key=lambda x: x["id"])
        random.Random(2026091309 + index).shuffle(order)
        bound = full["discussion"][index]
        for start in range(0, len(order), 10):
            batch = [{**x, "own_rating": ratings[index][x["id"]], "other_rating": ratings[1-index][x["id"]]} for x in order[start:start+10]]
            discussions.append(short_job({"kind": "discussion", "rater": index,
                "slot": f"recognition_r1/discussion/{index}/{start//10:02}",
                "request": discussion_request(model, batch), "item_ids": [x["id"] for x in batch],
                "input_token_bound": bound["input_token_bound"], "reserved_nano": bound["maximum_nano"] // 50}))
    discussed = execute(discussions, release, "discussion", root, folder, responder, replay)
    final = [dict(r) for r in ratings]
    for job, record in zip(discussions, discussed):
        for row in original_rows(job, record):
            final[job["rater"]][row["id"]] = {k: v for k, v in row.items() if k != "reason"}
    result = analyze(jobs, ratings, final)
    with Ledger(root, release) as ledger:
        result.update({"accounted_nano": release["prior_screening_nano"] + ledger.state["recognition_nano"],
            "continuation_accounted_nano": ledger.state["recognition_nano"], "provider_totals_nano": ledger.state["providers"],
            "discussion_items": len(unresolved), "discussion_calls": len(discussions),
            "release_sha256": digest(release), "reused_probe_calls": 500, "reused_coding_calls": 28,
            "format_amendment": "Short opaque within-batch IDs mapped bijectively to original IDs; original two failures preserved."})
    save(folder / "results.json", result)
    print(json.dumps(result), flush=True)
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("prepare", "run", "replay"))
    parser.add_argument("--yes", action="store_true")
    args = parser.parse_args()
    if args.command == "prepare":
        release = prepare(True)
        print(json.dumps({"release_sha256": digest(release), "maximum_new_nano": release["recognition_cap_nano"],
            "maximum_total_screening_nano": release["prior_screening_nano"] + release["recognition_cap_nano"]}))
    else:
        if args.command == "run" and not args.yes:
            raise BudgetStop("Explicit run flag required")
        collect(replay=args.command == "replay")
