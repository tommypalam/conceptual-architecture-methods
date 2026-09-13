"""Verify the 38-call consultation checkpoint without repeating paid calls."""
import hashlib
import json
from pathlib import Path
import zipfile

from phase3_budget import Budget, digest, read_checked, write_once
from phase3_resolution_consult import plan

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data/raw/phase3_20260913_budget"
PACKAGE = ROOT / "experiments/phase3_benchmarks/resolution_20260913"


def verify():
    prior = read_checked(ROOT / "experiments/phase3_benchmarks/CHECKPOINT_VERIFICATION.json")
    for name, expected in prior["member_sha256"].items():
        if hashlib.sha256((RAW / name).read_bytes()).hexdigest() != expected:
            raise ValueError("Previous paid evidence changed")
    with zipfile.ZipFile(ROOT / prior["archive"]) as zf:
        if zf.testzip() or set(zf.namelist()) != set(prior["member_sha256"]):
            raise ValueError("Previous archive damaged")
        for name, expected in prior["member_sha256"].items():
            if hashlib.sha256(zf.read(name)).hexdigest() != expected:
                raise ValueError("Previous archive member changed")
    if hashlib.sha256((ROOT / prior["archive"]).read_bytes()).hexdigest() != prior["archive_sha256"]:
        raise ValueError("Previous archive bytes changed")
    p = plan()
    if p != read_checked(PACKAGE / "consult_manifest.json"):
        raise ValueError("Frozen consultation changed")
    consultation_key = digest(p["slot"])
    record = read_checked(RAW / "records" / (consultation_key + ".json"))
    if (record["raw"]["model"] != p["request"]["model"]
            or record["raw"]["stop_reason"] != "max_tokens"
            or record["raw"]["usage"]["output_tokens"] != 7000
            or record["error"]["type"] != "ValueError"
            or record["parsed"] is not None
            or record["accounted_nano"] != p["reserved_nano"]):
        raise ValueError("Unexpected incomplete consultation record")
    for relative in ("validation_20260913/canonical_audit_manifest.json", "perception_20260913/manifest.json"):
        manifest = read_checked(ROOT / "experiments/phase3_benchmarks" / relative)
        for name, expected in manifest["source_sha256"].items():
            if hashlib.sha256((ROOT / name).read_bytes()).hexdigest() != expected:
                raise ValueError("Frozen prerequisite source changed")
    original = json.loads((ROOT / "experiments/phase3_preparation_20260913/VERIFICATION.json").read_bytes())
    for name, expected in original["immutable_inputs_sha256"].items():
        if hashlib.sha256((ROOT / name).read_bytes()).hexdigest() != expected:
            raise ValueError("Historical input changed")
    with Budget(RAW) as budget:
        state = budget.audit()
        sets = {kind: {p.stem for p in (RAW / kind).glob("*.json")}
                for kind in ("reservations", "records", "settlements")}
        if (state["pending"] or state["failed"] != [consultation_key] or len(sets["records"]) != 38
                or not sets["records"] == sets["reservations"] == sets["settlements"]):
            raise ValueError("Incomplete consultation checkpoint")
        expected_keys = {Path(name).stem for name in prior["member_sha256"] if name.startswith("records/")}
        if sets["records"] != expected_keys | {digest(p["slot"])}:
            raise ValueError("Unscheduled call in ledger")
        total = 0
        for key in sets["records"]:
            intent = read_checked(RAW / "reservations" / (key + ".json"))
            response = read_checked(RAW / "records" / (key + ".json"))
            settlement = read_checked(RAW / "settlements" / (key + ".json"))
            if (settlement["response_sha256"] != digest(response)
                    or settlement["reservation_sha256"] != digest(intent)
                    or response["manifest_sha256"] != intent["manifest_sha256"]
                    or response["accounted_nano"] != settlement["charged_nano"]
                    or settlement["status"] != ("failed" if key == consultation_key else "complete")
                    or (response["error"] is not None) != (key == consultation_key)):
                raise ValueError("Broken response/cost link")
            total += settlement["charged_nano"]
        if total != state["charged_or_reserved_nano"] or total != 89_443_200 + record["accounted_nano"]:
            raise ValueError("Cost discrepancy")
    if (ROOT / "AGENTS.md").read_text(encoding="utf-8").split("\n", 1)[1] != (ROOT / "CLAUDE.md").read_text(encoding="utf-8").split("\n", 1)[1]:
        raise ValueError("Companion instructions differ")
    members = {p.relative_to(RAW).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in RAW.rglob("*.json")}
    archive = ROOT / "output/phase3_resolution_20260913.zip"
    if not archive.exists():
        with zipfile.ZipFile(archive, "x", compression=zipfile.ZIP_DEFLATED) as zf:
            for name in sorted(members):
                zf.write(RAW / name, name)
    with zipfile.ZipFile(archive) as zf:
        if zf.testzip() or set(zf.namelist()) != set(members):
            raise ValueError("New archive completeness failure")
        for name, expected in members.items():
            if hashlib.sha256(zf.read(name)).hexdigest() != expected:
                raise ValueError("New archive member changed")
    result = {"calls": 38, "new_calls_during_verification": 0, "accounted_nano": total,
              "consultation_nano": record["accounted_nano"], "tonight_remaining_nano": 30_000_000_000 - total,
              "package_accounted_nano": 22_906_073_025 + total,
              "prior_evidence_unchanged": True, "frozen_sources_unchanged": True,
              "pending": 0, "failed": 1, "failure": "truncated_consultation_preserved_no_retry",
              "further_paid_dispatch_blocked": True,
              "archive": archive.relative_to(ROOT).as_posix(),
              "archive_sha256": hashlib.sha256(archive.read_bytes()).hexdigest(),
              "archive_members": len(members), "off_device_backup_verified": False}
    target = PACKAGE / "VERIFICATION.json"
    if target.exists():
        if read_checked(target) != result:
            raise ValueError("Existing verification differs")
    else:
        write_once(target, result)
    return result


if __name__ == "__main__":
    print(json.dumps(verify()))
