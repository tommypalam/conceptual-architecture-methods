"""One linked coding replacement; original recognition evidence stays immutable."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import random
import zipfile

from phase3_budget import BudgetStop, POLICY, canonical, digest, read_checked
from phase3_recognition_run import (ROOT, RUN, LEDGER, PACKAGE, Ledger, MODELS,
    RATERS, parse, charge, network, item_id, verify_release)
from phase3_recognition import rater_request
from phase3_recognition_discussion import discussion_request
from phase3_recognition_analysis import analyze
from phase3_variant_round import save

RECOVERY = RUN / "recovery_r1"
FAILED = "recognition_r1/coding/0/28"
REPLACEMENT = "recognition_recovery_r1/coding/0/28"


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def archived_evidence(checkpoint, root):
    path = ROOT / checkpoint["archive"]
    if sha(path) != checkpoint["archive_sha256"]:
        raise BudgetStop("Stopped-run archive hash changed")
    with zipfile.ZipFile(path) as archive:
        if archive.testzip() or len(archive.namelist()) != checkpoint["archive_members"]:
            raise BudgetStop("Stopped-run archive incomplete/corrupt")
        for name in archive.namelist():
            if archive.read(name) != (Path(root) / name).read_bytes():
                raise BudgetStop("Stopped-run archived evidence changed")


def inherited(root=LEDGER):
    """Check saved evidence and independently reconstruct all initial requests."""
    parent = read_checked(RUN / "release.json")
    probes = read_checked(RUN / "probe_manifest.json")
    coding = read_checked(RUN / "coding_manifest.json")
    records, items = {}, []
    for stage in (probes, coding):
        if stage["release_sha256"] != digest(parent):
            raise BudgetStop("Unlinked original manifest")
        stage_hash = digest(stage)
        # Only the original 29 coding records belong to the stopped snapshot.
        # Later slots may now exist under the continuation manifest on replay.
        prior_jobs = stage["jobs"] if stage is probes else stage["jobs"][:29]
        for job in prior_jobs:
            path = Path(root) / "records" / (digest(job["slot"]) + ".json")
            if not path.exists():
                if job["kind"] == "probe":
                    raise BudgetStop("Missing original probe")
                continue
            record = read_checked(path)
            intent = read_checked(Path(root) / "reservations" / path.name)
            if intent["request"] != job["request"] or intent["manifest_sha256"] != stage_hash:
                raise BudgetStop("Inherited request/manifest mismatch")
            if record["error"]:
                if job["slot"] != FAILED or digest(record) != "953d184b61b0f17ef2bd74324fb4a758d6b2132a8ada92187a42f45cf275a60f":
                    raise BudgetStop("Unexpected inherited failure")
                continue
            if parse(record["raw"], job) != record["parsed"] or charge(record["raw"], job, False) != record["accounted_nano"]:
                raise BudgetStop("Inherited parser/cost mismatch")
            records[job["slot"]] = record
            if job["kind"] == "probe":
                items.append({"id": item_id(job["slot"]), "answer": record["parsed"]})
    if len(items) != 500 or len({x["id"] for x in items}) != 500 or len(records) != 528:
        raise BudgetStop("Unexpected original reuse set")
    initial = read_checked(PACKAGE / "cost_plan.json")
    if probes["jobs"] != [{**j, "kind": "probe"} for j in initial["jobs"]]:
        raise BudgetStop("Changed probe coverage/order")
    expected = []
    for index, model in enumerate(RATERS):
        order = items.copy()
        random.Random(2026091307 + index).shuffle(order)
        row = initial["coding"][index]
        for start in range(0, 500, 10):
            batch = order[start:start+10]
            expected.append({"kind": "coding", "rater": index,
                "slot": f"recognition_r1/coding/{index}/{start//10:02}",
                "request": rater_request(model, batch), "item_ids": [x["id"] for x in batch],
                "input_token_bound": row["input_token_bound"], "reserved_nano": row["reserved_nano_per_call"]})
    if expected != coding["jobs"]:
        raise BudgetStop("Changed or incomplete initial coding schedule")
    remaining = [{**j, "slot": REPLACEMENT if j["slot"] == FAILED else j["slot"]}
                 for j in expected if j["slot"] not in records]
    if len(remaining) != 72 or remaining[0]["slot"] != REPLACEMENT:
        raise BudgetStop("Unexpected replacement/remaining workload")
    return probes["jobs"], items, expected, records, remaining


def prepare(persist=False):
    parent = verify_release()
    checkpoint = read_checked(RUN / "CHECKPOINT.json")
    archived_evidence(checkpoint, LEDGER)
    with Ledger(LEDGER, parent) as ledger:
        if ledger.state["pending"] or ledger.state["failed"] != [digest(FAILED)]:
            raise BudgetStop("Unexpected stopped-run disposition")
        if len(ledger.state["reservations"]) != 577:
            raise BudgetStop("Unexpected stopped-run count")
    _, _, _, _, remaining = inherited()
    slots = {slot: copy.deepcopy(cap) for slot, cap in parent["slots"].items()
             if cap["kind"] == "discussion"}
    for job in remaining:
        old_slot = FAILED if job["slot"] == REPLACEMENT else job["slot"]
        slots[job["slot"]] = {**parent["slots"][old_slot], "request_sha256": digest(job["request"])}
    maximum = sum(s["reserved_nano"] for s in slots.values())
    if checkpoint["recognition_accounted_nano"] + maximum > parent["recognition_cap_nano"]:
        raise BudgetStop("Continuation exceeds existing screening ceiling")
    paths = [Path(__file__), RECOVERY / "PROTOCOL.md", RUN / "release.json", RUN / "CHECKPOINT.json",
             RUN / "probe_manifest.json", RUN / "coding_manifest.json"]
    release = {"id": "recognition_recovery_r1", "parent_release_sha256": digest(parent),
        "failed_slot": FAILED, "replacement_slot": REPLACEMENT,
        "prior_screening_nano": checkpoint["recognition_accounted_nano"],
        "original_screening_cap_nano": parent["recognition_cap_nano"],
        "recognition_cap_nano": maximum, "slots": slots,
        "provider_caps_nano": parent["provider_caps_nano"],
        "historical_keys": sorted(p.stem for p in (LEDGER / "records").glob("*.json")),
        "preserved_files": {p.relative_to(LEDGER).as_posix(): sha(p) for p in LEDGER.rglob("*.json")},
        "failure_log_prefix_bytes": (LEDGER / "failures.jsonl").stat().st_size,
        "failure_log_prefix_sha256": sha(LEDGER / "failures.jsonl"),
        "source_sha256": {**parent["source_sha256"], **{p.relative_to(ROOT).as_posix(): sha(p) for p in paths}}}
    with Ledger(LEDGER, release) as ledger:
        if ledger.state["pending"] or ledger.state["failed"]:
            raise BudgetStop("Unresolved continuation entry")
    if persist:
        save(RECOVERY / "release.json", release)
    return release


def verify(release, root=LEDGER):
    if release["prior_screening_nano"] + release["recognition_cap_nano"] > release["original_screening_cap_nano"]:
        raise BudgetStop("Cumulative screen budget changed")
    for relative, expected in release["source_sha256"].items():
        if sha(ROOT / relative) != expected:
            raise BudgetStop("Frozen continuation source changed")
    prefix = (Path(root) / "failures.jsonl").read_bytes()[:release["failure_log_prefix_bytes"]]
    if hashlib.sha256(prefix).hexdigest() != release["failure_log_prefix_sha256"]:
        raise BudgetStop("Historical failure log changed")


def execute(jobs, release, kind, root, folder, responder, replay):
    if len({j["slot"] for j in jobs}) != len(jobs):
        raise BudgetStop("Duplicate continuation slots")
    stage = {"release_sha256": digest(release), "jobs": jobs}
    save(folder / (kind + "_manifest.json"), stage)
    stage_hash = digest(stage)
    records = []
    with Ledger(root, release) as ledger:
        for index, job in enumerate(jobs):
            record, called = ledger.dispatch(job, stage_hash, responder, replay)
            records.append(record)
            if called and ((index + 1) % 10 == 0 or index + 1 == len(jobs)):
                print(json.dumps({"stage": kind, "complete": index+1, "total": len(jobs),
                    "screening_usd": (release["prior_screening_nano"] + ledger.state["recognition_nano"]) / 1e9}), flush=True)
    return records


def collect(replay=False, *, root=LEDGER, folder=RECOVERY, responder=network, test_release=None):
    root, folder = Path(root), Path(folder)
    if root == LEDGER and test_release is not None:
        raise BudgetStop("Test release on real ledger forbidden")
    release = read_checked(folder / "release.json") if test_release is None else test_release
    verify(release, root)
    with Ledger(root, release) as ledger:
        if ledger.state["failed"] or ledger.state["pending"]:
            raise BudgetStop("New failure/pending intent blocks recovery")
    jobs, items, original_coding, saved, remaining = inherited(root)
    results = execute(remaining, release, "coding", root, folder, responder, replay)
    saved.update({FAILED if j["slot"] == REPLACEMENT else j["slot"]: r for j, r in zip(remaining, results)})
    ratings = [{}, {}]
    for job in original_coding:
        for row in saved[job["slot"]]["parsed"]:
            if row["id"] in ratings[job["rater"]]:
                raise BudgetStop("Duplicate recovered coding")
            ratings[job["rater"]][row["id"]] = json.loads(canonical(row))
    unresolved = [x for x in items if ratings[0][x["id"]] != ratings[1][x["id"]]
                  or ratings[0][x["id"]]["ambiguous"] or ratings[0][x["id"]]["refusal"]]
    full = read_checked(PACKAGE / "discussion_cost_plan.json")
    discussions = []
    for index, model in enumerate(RATERS):
        order = sorted(unresolved, key=lambda x: x["id"])
        random.Random(2026091309 + index).shuffle(order)
        row = full["discussion"][index]
        for start in range(0, len(order), 10):
            batch = [{**x, "own_rating": ratings[index][x["id"]], "other_rating": ratings[1-index][x["id"]]} for x in order[start:start+10]]
            discussions.append({"kind": "discussion", "rater": index,
                "slot": f"recognition_r1/discussion/{index}/{start//10:02}",
                "request": discussion_request(model, batch), "item_ids": [x["id"] for x in batch],
                "input_token_bound": row["input_token_bound"], "reserved_nano": row["maximum_nano"] // 50})
    discussed = execute(discussions, release, "discussion", root, folder, responder, replay)
    final = [dict(r) for r in ratings]
    for job, record in zip(discussions, discussed):
        for row in record["parsed"]:
            final[job["rater"]][row["id"]] = {k: v for k, v in row.items() if k != "reason"}
    analysis = analyze(jobs, ratings, final)
    with Ledger(root, release) as ledger:
        analysis.update({"accounted_nano": release["prior_screening_nano"] + ledger.state["recognition_nano"],
            "continuation_accounted_nano": ledger.state["recognition_nano"],
            "provider_totals_nano": ledger.state["providers"], "discussion_items": len(unresolved),
            "discussion_calls": len(discussions), "release_sha256": digest(release),
            "reused_probe_calls": 500, "reused_coding_calls": 28, "failed_slot_preserved": FAILED})
    save(folder / "results.json", analysis)
    print(json.dumps(analysis), flush=True)
    return analysis


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
