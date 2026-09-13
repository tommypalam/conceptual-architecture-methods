"""Offline provenance/accounting check and local archive of the initial Phase 3 checks."""
from __future__ import annotations

from decimal import Decimal
import hashlib
import json
from pathlib import Path
import zipfile

from phase3_budget import Budget, digest, read_checked, write_once

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data/raw/phase3_20260913_budget"
PACKAGE = ROOT / "experiments/phase3_benchmarks"


def main():
    with Budget(RAW) as budget:
        state = budget.audit()
        if state["pending"] or state["failed"]:
            raise ValueError("Unresolved records")
        indexes = {name: {p.stem: p for p in (RAW / name).glob("*.json")}
                   for name in ("reservations", "records", "settlements")}
        if not (indexes["reservations"].keys() == indexes["records"].keys() == indexes["settlements"].keys()):
            raise ValueError("Missing or orphan provenance record")
        if len(indexes["records"]) != 37:
            raise ValueError("Checkpoint expects exactly one review and 36 perception responses")
        accounted = 0
        for key, path in indexes["records"].items():
            record = read_checked(path)
            intent = read_checked(indexes["reservations"][key])
            settlement = read_checked(indexes["settlements"][key])
            if (settlement["response_sha256"] != digest(record)
                    or settlement["reservation_sha256"] != digest(intent)
                    or record["manifest_sha256"] != intent["manifest_sha256"]
                    or settlement["status"] != "complete" or record["error"]):
                raise ValueError("Broken provenance link or unsuccessful call")
            if record["accounted_nano"] != settlement["charged_nano"]:
                raise ValueError("Charge disagreement")
            accounted += settlement["charged_nano"]
        if accounted != state["charged_or_reserved_nano"] or accounted != 89_443_200:
            raise ValueError("Checkpoint cost disagreement")
    # Verify all scientific inputs retained from the earlier preparation checkpoint.
    original = json.loads((ROOT / "experiments/phase3_preparation_20260913/VERIFICATION.json").read_bytes())
    for name, expected in original["immutable_inputs_sha256"].items():
        if hashlib.sha256((ROOT / name).read_bytes()).hexdigest() != expected:
            raise ValueError("Historical scientific input changed")
    for relative in ("validation_20260913/canonical_audit_manifest.json", "perception_20260913/manifest.json"):
        manifest = read_checked(PACKAGE / relative)
        for name, expected in manifest["source_sha256"].items():
            if hashlib.sha256((ROOT / name).read_bytes()).hexdigest() != expected:
                raise ValueError("Frozen source changed")
    if (ROOT / "AGENTS.md").read_text(encoding="utf-8").split("\n", 1)[1] != (ROOT / "CLAUDE.md").read_text(encoding="utf-8").split("\n", 1)[1]:
        raise ValueError("AGENTS/CLAUDE rules differ")
    members = {p.relative_to(RAW).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
               for p in RAW.rglob("*.json")}
    archive = ROOT / "output/phase3_checkpoint_20260913.zip"
    archive.parent.mkdir(exist_ok=True)
    if not archive.exists():
        with zipfile.ZipFile(archive, "x", compression=zipfile.ZIP_DEFLATED) as zf:
            for name in sorted(members):
                zf.write(RAW / name, name)
    with zipfile.ZipFile(archive) as zf:
        if zf.testzip() is not None or set(zf.namelist()) != set(members):
            raise ValueError("Archive completeness/CRC failure")
        for name, sha in members.items():
            if hashlib.sha256(zf.read(name)).hexdigest() != sha:
                raise ValueError("Archive member checksum failure")
    result = {"date": "2026-09-13", "calls": 37, "pending": 0, "failed": 0,
              "new_calls_this_verification": 0, "accounted_usd": str(Decimal(accounted) / 10**9),
              "tonight_remaining_usd": str(Decimal(30) - Decimal(accounted) / 10**9),
              "historical_inputs_unchanged": True, "frozen_sources_unchanged": True,
              "companion_rules_match": True, "archive": archive.relative_to(ROOT).as_posix(),
              "archive_members": len(members), "archive_sha256": hashlib.sha256(archive.read_bytes()).hexdigest(),
              "member_sha256": members, "off_device_backup_verified": False,
              "note": "Prerequisite checks only; main Phase 3 and recognition collection remain unstarted."}
    path = PACKAGE / "CHECKPOINT_VERIFICATION.json"
    if path.exists():
        if read_checked(path) != result:
            raise ValueError("Existing checkpoint verification differs")
    else:
        write_once(path, result)
    print(json.dumps({k: v for k, v in result.items() if k != "member_sha256"}))


if __name__ == "__main__":
    main()
