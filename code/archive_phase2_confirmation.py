"""Create and verify a local raw-data archive after collection and replay audit."""
import hashlib
import json
from pathlib import Path
import zipfile

from run_phase2_confirmation import ROOT, RAW, PACKAGE, verify
from phase2_confirmation_transport import digest, now


def archive():
    manifest = verify()
    if (RAW / "execution.lock").exists():
        raise RuntimeError("Archive only after collection/audit releases its lock")
    audit = json.loads((PACKAGE / "analysis" / "integrity_audit.json").read_text(encoding="utf-8"))
    if not (audit["exact_request_replay_passed"] and audit["group_state_replay_passed"] and audit["new_dispatches"] == 0):
        raise RuntimeError("Successful no-network audit required")
    if audit["manifest_hash"] != digest(manifest):
        raise RuntimeError("Audit belongs to another manifest")
    target = ROOT / "output" / "phase2_confirmation_20260913_raw.zip"
    files = sorted(p for p in RAW.rglob("*") if p.is_file())
    inventory = []
    if target.exists():
        raise FileExistsError("Preserve existing archive; verify separately rather than overwrite")
    with zipfile.ZipFile(target, "x", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        for p in files:
            content = p.read_bytes()
            relative = p.relative_to(RAW).as_posix()
            z.writestr(relative, content)
            inventory.append({"path": relative, "bytes": len(content), "sha256": hashlib.sha256(content).hexdigest()})
    with zipfile.ZipFile(target) as z:
        assert z.namelist() == [x["path"] for x in inventory]
        for entry in inventory:
            content = z.read(entry["path"])
            assert len(content) == entry["bytes"]
            assert hashlib.sha256(content).hexdigest() == entry["sha256"]
            assert hashlib.sha256((RAW / entry["path"]).read_bytes()).hexdigest() == entry["sha256"]
    inventory_path = ROOT / "output" / "phase2_confirmation_20260913_raw_inventory.json"
    with inventory_path.open("x", encoding="utf-8", newline="\n") as f:
        json.dump(inventory, f, indent=2)
        f.write("\n")
    report = {"verified_at": now(), "manifest_hash": digest(manifest), "archive": str(target.relative_to(ROOT)),
              "sha256": hashlib.sha256(target.read_bytes()).hexdigest(), "archive_bytes": target.stat().st_size,
              "file_count": len(files), "uncompressed_bytes": sum(x["bytes"] for x in inventory),
              "inventory": str(inventory_path.relative_to(ROOT)),
              "inventory_sha256": hashlib.sha256(inventory_path.read_bytes()).hexdigest(),
              "every_member_crc_and_source_sha256_verified": True, "off_device_backup_verified": False}
    path = PACKAGE / "analysis" / "raw_archive.json"
    with path.open("x", encoding="utf-8", newline="\n") as f:
        json.dump(report, f, indent=2)
        f.write("\n")
    print(json.dumps(report), flush=True)


if __name__ == "__main__":
    archive()
