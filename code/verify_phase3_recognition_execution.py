"""Verify completed or stopped recognition collection without repeating API calls."""
import hashlib
import json
from pathlib import Path
import zipfile

from phase3_budget import digest, read_checked, POLICY
from phase3_recognition_run import RUN, ROOT, LEDGER, Ledger, verify_release, parse, charge, collect
from phase3_variant_round import save


def verify():
    release = verify_release()
    complete = (RUN / "results.json").exists()
    if complete:
        # This reconstructs all response-dependent coding/discussion requests and
        # analysis; replay raises before any responder could be called for a gap.
        collect(replay=True, responder=lambda _: (_ for _ in ()).throw(AssertionError("Network in verification")))
    manifests = {}
    for kind in ("probe", "coding", "discussion"):
        path = RUN / (kind + "_manifest.json")
        if path.exists():
            stage = read_checked(path)
            if stage["release_sha256"] != digest(release):
                raise ValueError("Unlinked stage manifest")
            for job in stage["jobs"]:
                key = digest(job["slot"])
                if key in manifests:
                    raise ValueError("Duplicate stage slot")
                manifests[key] = (job, digest(stage))
    with Ledger(LEDGER, release) as ledger:
        state = ledger.state
        counts = {k: {"complete": 0, "failed": 0, "undispatched": 0} for k in ("probe", "coding", "discussion")}
        failures = []
        for key, (job, stage_hash) in manifests.items():
            if key not in state["reservations"]:
                counts[job["kind"]]["undispatched"] += 1
                continue
            intent = state["reservations"][key]
            if intent["manifest_sha256"] != stage_hash or intent["request"] != job["request"]:
                raise ValueError("Request/manifest mismatch")
            record = read_checked(LEDGER / "records" / (key + ".json"))
            if record["error"]:
                counts[job["kind"]]["failed"] += 1
                failures.append({"slot": job["slot"], "error": record["error"], "record_sha256": digest(record)})
            else:
                if parse(record["raw"], job) != record["parsed"]:
                    raise ValueError("Parser replay mismatch")
                counts[job["kind"]]["complete"] += 1
            if charge(record["raw"], job, record["error"] is not None) != record["accounted_nano"]:
                raise ValueError("Cost replay mismatch")
        if set(state["reservations"]) - set(release["historical_keys"]) - set(manifests):
            raise ValueError("Unmanifested dispatch")
        if state["pending"]:
            raise ValueError("Pending dispatch needs separate reconciliation before archive")
        if complete and (state["failed"] or any(v["undispatched"] or v["failed"] for v in counts.values())):
            raise ValueError("Incomplete data claimed complete")
        # Verify every member of the previous archive against current bytes.
        previous = read_checked(RUN.parent.parent / "variants_r3/REVIEW_CHECKPOINT.json")
        old_path = ROOT / previous["archive"]
        if hashlib.sha256(old_path.read_bytes()).hexdigest() != previous["archive_sha256"]:
            raise ValueError("Historical archive changed")
        with zipfile.ZipFile(old_path) as archive:
            if archive.testzip() is not None:
                raise ValueError("Historical archive corrupt")
            for name in archive.namelist():
                if archive.read(name) != (LEDGER / name).read_bytes():
                    raise ValueError("Historical member changed")
        original = json.loads((ROOT / "experiments/phase3_preparation_20260913/VERIFICATION.json").read_bytes())
        for relative, sha in original["immutable_inputs_sha256"].items():
            if hashlib.sha256((ROOT / relative).read_bytes()).hexdigest() != sha:
                raise ValueError("Historical scientific source changed")
        members = {p.relative_to(LEDGER).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                   for p in LEDGER.rglob("*") if p.is_file() and p.suffix in (".json", ".jsonl")}
        path = ROOT / "output/phase3_recognition_r1_20260913.zip"
        if not path.exists():
            with zipfile.ZipFile(path, "x", compression=zipfile.ZIP_DEFLATED) as archive:
                for name in sorted(members):
                    archive.write(LEDGER / name, name)
        with zipfile.ZipFile(path) as archive:
            if archive.testzip() is not None or set(archive.namelist()) != set(members):
                raise ValueError("Current archive corrupt/incomplete")
            for name, sha in members.items():
                if hashlib.sha256(archive.read(name)).hexdigest() != sha:
                    raise ValueError("Current archive member mismatch")
        result = {"collection_complete": complete, "counts": counts, "failures": failures,
                  "total_paid_records": len(state["reservations"]), "historical_records_preserved": 48,
                  "recognition_accounted_nano": state["recognition_nano"],
                  "phase3_accounted_nano": sum(state["providers"].values()), "provider_totals_nano": state["providers"],
                  "package_accounted_nano": POLICY["prior_package_nano"] + sum(state["providers"].values()),
                  "new_calls_during_verification": 0, "historical_evidence_unchanged": True,
                  "archive": path.relative_to(ROOT).as_posix(), "archive_members": len(members),
                  "archive_sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "off_device_backup_verified": False}
    save(RUN / "CHECKPOINT.json", result)
    return result


if __name__ == "__main__":
    print(json.dumps(verify()))
