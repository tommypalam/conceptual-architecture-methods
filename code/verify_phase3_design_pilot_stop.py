"""Audit the stopped pilot and unwrap only complete JSON fences, without API calls."""
import hashlib
import json
import zipfile

import phase3_design_pilot as pilot
from phase3_budget import POLICY, BudgetStop, digest, read_checked
from phase3_recognition_run import Ledger, parse, charge
from phase3_variant_round import save


def review_text(text):
    stripped = text.strip()
    if not stripped.startswith("```json\n") or not stripped.endswith("```"):
        raise ValueError("Expected complete JSON fence, no surrounding prose")
    return pilot.review_value(stripped[8:-3].strip())


def verify():
    release = read_checked(pilot.PILOT / "release.json")
    pilot.verify(release)
    records, keys = {}, set()
    with Ledger(pilot.LEDGER, release) as ledger:
        if ledger.state["pending"] or ledger.state["failed"]:
            raise BudgetStop("Unresolved transport dispatch")
        for purpose in ("generation", "review"):
            manifest = read_checked(pilot.PILOT / (purpose + "_manifest.json"))
            if manifest["release_sha256"] != digest(release) or len(manifest["jobs"]) != 1:
                raise BudgetStop("Unlinked or unexpected pilot stage")
            job = manifest["jobs"][0]
            if job["slot"] != f"design_pilot_r1/{purpose}/0" or job["purpose"] != purpose:
                raise BudgetStop("Unexpected pilot purpose/slot")
            if purpose == "generation" and job != pilot.generation():
                raise BudgetStop("Generation request replay mismatch")
            key = digest(job["slot"]); keys.add(key)
            record = read_checked(pilot.LEDGER / "records" / (key + ".json"))
            intent = ledger.state["reservations"][key]
            if intent["manifest_sha256"] != digest(manifest) or intent["request"] != job["request"]:
                raise BudgetStop("Request/manifest mismatch")
            if record["error"] or parse(record["raw"], job) != record["parsed"] or charge(record["raw"], job, False) != record["accounted_nano"]:
                raise BudgetStop("Raw parser/cost replay mismatch")
            records[purpose] = record
        if set(ledger.state["reservations"]) - set(release["historical_keys"]) != keys:
            raise BudgetStop("Unexpected additional pilot dispatch")
        review = review_text(records["review"]["parsed"])
        if review["verdict"] not in ("revise", "reject"):
            raise BudgetStop("This stopped-run audit cannot release recognition")
        old = read_checked(pilot.TRANSPORT / "CHECKPOINT.json")
        pilot.archived_evidence(old, pilot.LEDGER)
        members = {p.relative_to(pilot.LEDGER).as_posix(): pilot.sha(p) for p in pilot.LEDGER.rglob("*")
                   if p.is_file() and p.suffix in (".json", ".jsonl")}
        path = pilot.ROOT / "output/phase3_design_pilot_r1_stopped_20260913.zip"
        if not path.exists():
            with zipfile.ZipFile(path, "x", compression=zipfile.ZIP_DEFLATED) as archive:
                for name in sorted(members): archive.write(pilot.LEDGER / name, name)
        with zipfile.ZipFile(path) as archive:
            if archive.testzip() or set(archive.namelist()) != set(members):
                raise BudgetStop("Incomplete/corrupt stopped-run archive")
            for name, expected in members.items():
                if hashlib.sha256(archive.read(name)).hexdigest() != expected:
                    raise BudgetStop("Archive member mismatch")
        result = {"decision": "structural_stop", "runner_status": "stopped_on_fenced_review_JSON",
            "semantic_disposition": "Complete JSON fence removed only in derived audit; original strict schema validates revise/reject.",
            "candidate": records["generation"]["parsed"], "review": review,
            "record_sha256": {k: digest(v) for k,v in records.items()},
            "new_calls_during_verification": 0, "pilot_calls": 2, "recognition_calls": 0,
            "coding_calls": 0, "formal_n50_gate": "not_tested", "population_released": False,
            "pilot_accounted_nano": ledger.state["recognition_nano"],
            "phase3_accounted_nano": sum(ledger.state["providers"].values()),
            "provider_totals_nano": ledger.state["providers"],
            "package_accounted_nano": POLICY["prior_package_nano"]+sum(ledger.state["providers"].values()),
            "historical_records_preserved": 650, "total_paid_records": len(ledger.state["reservations"]),
            "frozen_sources_unchanged": True, "archive": path.relative_to(pilot.ROOT).as_posix(),
            "archive_members": len(members), "archive_sha256": pilot.sha(path), "off_device_backup_verified": False}
    save(pilot.PILOT / "STOP_CHECKPOINT.json", result)
    return result


if __name__ == "__main__":
    print(json.dumps(verify()))
