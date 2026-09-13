"""Offline 48-call checkpoint: exact review replay and cumulative provenance."""
import hashlib
import json
from pathlib import Path
import zipfile

from phase3_budget import digest, read_checked
from phase3_variant_round import make_plan, save
from phase3_repaired_candidates import review_plan, repaired
from phase3_validation_continuation import execute, Continuation, LEDGER, FAILED_SLOT

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "experiments/phase3_benchmarks"


def verify():
    rec = read_checked(BASE / "variants_r2/reconciliation.json")
    plans = (make_plan("generation"), review_plan())
    summaries = []
    for plan, folder, kind in zip(plans, ("variants_r2", "variants_r3"), ("generation", "review")):
        if plan != read_checked(BASE / folder / (kind + "_manifest.json")):
            raise ValueError("Frozen plan/source mismatch")
        records, calls = execute(plan, rec, replay=True,
                                 responder=lambda _: (_ for _ in ()).throw(AssertionError("No network")))
        summary = read_checked(BASE / folder / (kind + "_result.json"))
        if calls or summary["manifest_sha256"] != digest(plan) or len(summary["results"]) != 5:
            raise ValueError("Unexpected replay count/identity")
        for job, entry, record in zip(plan["jobs"], summary["results"], records):
            if (entry["benchmark"] != job["slot"].split("/")[-1]
                    or entry["record_sha256"] != digest(record)
                    or entry["parsed" if kind == "generation" else "review"] != record["parsed"]):
                raise ValueError("Derived result mismatch")
        if sum(r["accounted_nano"] for r in records) != summary["accounted_nano"]:
            raise ValueError("Derived charge mismatch")
        summaries.append(summary)
    if repaired() != read_checked(BASE / "variants_r3/candidates.json"):
        raise ValueError("Repaired wording/provenance changed")
    with Continuation(LEDGER, rec) as budget:
        state = budget.audit()
        expected = {Path(p).stem for p in rec["preserved_files"] if p.startswith("records/")}
        expected |= {digest(job["slot"]) for plan in plans for job in plan["jobs"]}
        if (len(expected) != 48 or expected != set(state["reservations"])
                or state["pending"] or state["failed"] or state["historical_failed"] != [digest(FAILED_SLOT)]):
            raise ValueError("Incomplete or unexpected checkpoint")
        if state["charged_or_reserved_nano"] != 337570200 + sum(s["accounted_nano"] for s in summaries):
            raise ValueError("Cumulative charge mismatch")
    # Earlier archives remain exact historical snapshots, not overwritten with
    # the larger current ledger. Verify their bytes and member subsets in place.
    for relative in ("resolution_20260913/VERIFICATION.json", "variants_r2/GENERATION_CHECKPOINT.json"):
        previous = read_checked(BASE / relative)
        path = ROOT / previous["archive"]
        if hashlib.sha256(path.read_bytes()).hexdigest() != previous["archive_sha256"]:
            raise ValueError("Earlier archive changed")
        with zipfile.ZipFile(path) as zf:
            if zf.testzip() is not None:
                raise ValueError("Earlier archive corrupt")
            for name in zf.namelist():
                if zf.read(name) != (LEDGER / name).read_bytes():
                    raise ValueError("Historical archived record changed")
    original = json.loads((ROOT / "experiments/phase3_preparation_20260913/VERIFICATION.json").read_bytes())
    for relative, expected_hash in original["immutable_inputs_sha256"].items():
        if hashlib.sha256((ROOT / relative).read_bytes()).hexdigest() != expected_hash:
            raise ValueError("Historical scientific input changed")
    if (ROOT / "AGENTS.md").read_text(encoding="utf-8").split("\n", 1)[1] != (ROOT / "CLAUDE.md").read_text(encoding="utf-8").split("\n", 1)[1]:
        raise ValueError("Companion instructions differ")
    members = {p.relative_to(LEDGER).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in LEDGER.rglob("*.json")}
    archive = ROOT / "output/phase3_structural_review_20260913.zip"
    if not archive.exists():
        with zipfile.ZipFile(archive, "x", compression=zipfile.ZIP_DEFLATED) as zf:
            for name in sorted(members):
                zf.write(LEDGER / name, name)
    with zipfile.ZipFile(archive) as zf:
        if zf.testzip() is not None or set(zf.namelist()) != set(members):
            raise ValueError("Current archive incomplete/corrupt")
        for name, expected_hash in members.items():
            if hashlib.sha256(zf.read(name)).hexdigest() != expected_hash:
                raise ValueError("Current archive member mismatch")
    result = {"calls": 48, "generation_calls": 5, "independent_review_calls": 5,
              "new_calls_during_verification": 0, "accepted_pairs": [r["benchmark"] for r in summaries[1]["results"] if r["review"]["verdict"] == "accept"],
              "review_accounted_nano": summaries[1]["accounted_nano"],
              "phase3_accounted_nano": state["charged_or_reserved_nano"],
              "by_provider_nano": state["by_provider_nano"],
              "package_accounted_nano": 22906073025 + state["charged_or_reserved_nano"],
              "preserved_historical_failure_count": 1, "new_failures": 0, "pending": 0,
              "recognition_calls": 0, "population_calls": 0, "historical_evidence_unchanged": True,
              "archive": archive.relative_to(ROOT).as_posix(), "archive_members": len(members),
              "archive_sha256": hashlib.sha256(archive.read_bytes()).hexdigest(), "off_device_backup_verified": False}
    save(BASE / "variants_r3/REVIEW_CHECKPOINT.json", result)
    return result


if __name__ == "__main__":
    print(json.dumps(verify()))
