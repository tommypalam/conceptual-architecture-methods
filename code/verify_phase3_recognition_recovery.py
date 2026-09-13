"""Zero-network audit and new linked archive for recognition recovery."""
import hashlib
import json
import zipfile

from phase3_budget import POLICY, BudgetStop, digest, read_checked
from phase3_recognition_run import Ledger, parse, charge
from phase3_recognition_recovery import ROOT, RUN, RECOVERY, LEDGER, verify, collect, inherited, sha
from phase3_variant_round import save


def checkpoint(folder=RECOVERY, predecessor=RUN, collector=collect,
               archive_name="phase3_recognition_recovery_r1_20260913.zip"):
    release = read_checked(folder / "release.json")
    verify(release)
    inherited()
    complete = (folder / "results.json").exists()
    if complete:
        collector(True, responder=lambda _: (_ for _ in ()).throw(AssertionError("Network in verification")))
    expected = {}
    counts = {kind: {"complete": 0, "failed": 0, "undispatched": 0} for kind in ("coding", "discussion")}
    for kind in counts:
        path = folder / (kind + "_manifest.json")
        if not path.exists():
            continue
        stage = read_checked(path)
        if stage["release_sha256"] != digest(release):
            raise BudgetStop("Unlinked recovery stage")
        stage_hash = digest(stage)
        for job in stage["jobs"]:
            key = digest(job["slot"])
            if key in expected:
                raise BudgetStop("Duplicate recovery slot")
            expected[key] = (job, stage_hash)
    with Ledger(LEDGER, release) as ledger:
        state = ledger.state
        if state["pending"]:
            raise BudgetStop("Pending intent requires reconciliation")
        if set(state["reservations"]) - set(release["historical_keys"]) - set(expected):
            raise BudgetStop("Unmanifested recovery dispatch")
        failures = []
        for key, (job, stage_hash) in expected.items():
            if key not in state["reservations"]:
                counts[job["kind"]]["undispatched"] += 1
                continue
            intent = state["reservations"][key]
            if intent["request"] != job["request"] or intent["manifest_sha256"] != stage_hash:
                raise BudgetStop("Recovery request mismatch")
            record = read_checked(LEDGER / "records" / (key + ".json"))
            if record["error"]:
                counts[job["kind"]]["failed"] += 1
                failures.append({"slot": job["slot"], "error": record["error"], "record_sha256": digest(record)})
            else:
                if parse(record["raw"], job) != record["parsed"]:
                    raise BudgetStop("Recovery parser replay mismatch")
                counts[job["kind"]]["complete"] += 1
            if charge(record["raw"], job, record["error"] is not None) != record["accounted_nano"]:
                raise BudgetStop("Recovery cost replay mismatch")
        if complete and (state["failed"] or any(v["failed"] or v["undispatched"] for v in counts.values())):
            raise BudgetStop("Incomplete recovery claimed complete")
        old = read_checked(predecessor / "CHECKPOINT.json")
        old_archive = ROOT / old["archive"]
        if sha(old_archive) != old["archive_sha256"]:
            raise BudgetStop("Previous archive changed")
        with zipfile.ZipFile(old_archive) as archive:
            if archive.testzip():
                raise BudgetStop("Previous archive corrupt")
            for name in archive.namelist():
                before, after = archive.read(name), (LEDGER / name).read_bytes()
                changed = not after.startswith(before) if name == "failures.jsonl" else before != after
                if changed:
                    raise BudgetStop("Previous evidence changed")
        members = {p.relative_to(LEDGER).as_posix(): sha(p) for p in LEDGER.rglob("*")
                   if p.is_file() and p.suffix in (".json", ".jsonl")}
        path = ROOT / "output" / archive_name
        if not path.exists():
            with zipfile.ZipFile(path, "x", compression=zipfile.ZIP_DEFLATED) as archive:
                for name in sorted(members):
                    archive.write(LEDGER / name, name)
        with zipfile.ZipFile(path) as archive:
            if archive.testzip() or set(archive.namelist()) != set(members):
                raise BudgetStop("New archive incomplete/corrupt")
            for name, expected_sha in members.items():
                if hashlib.sha256(archive.read(name)).hexdigest() != expected_sha:
                    raise BudgetStop("New archive member changed")
        result = {"collection_complete": complete, "counts": counts, "failures": failures,
            "reused_probe_calls": 500, "reused_coding_calls": 28,
            "preserved_historical_records": len(release["historical_keys"]), "total_paid_records": len(state["reservations"]),
            "continuation_accounted_nano": state["recognition_nano"],
            "screening_accounted_nano": release["prior_screening_nano"] + state["recognition_nano"],
            "phase3_accounted_nano": sum(state["providers"].values()), "provider_totals_nano": state["providers"],
            "package_accounted_nano": POLICY["prior_package_nano"] + sum(state["providers"].values()),
            "new_calls_during_verification": 0, "historical_evidence_unchanged": True,
            "archive": path.relative_to(ROOT).as_posix(), "archive_members": len(members),
            "archive_sha256": sha(path), "off_device_backup_verified": False,
            "parent_checkpoint_sha256": digest(old), "release_sha256": digest(release)}
    save(folder / "CHECKPOINT.json", result)
    return result


if __name__ == "__main__":
    print(json.dumps(checkpoint()))
