"""Offline 43-call candidate checkpoint: replay, source identity and archive."""
import hashlib
import json
from pathlib import Path
import zipfile

from phase3_budget import digest, read_checked
from phase3_variant_round import make_plan, save, PACKAGE
from phase3_validation_continuation import execute, Continuation, LEDGER, FAILED_SLOT
from phase3_repaired_candidates import repaired, review_plan

ROOT = Path(__file__).resolve().parents[1]


def verify():
    plan = make_plan("generation")
    if plan != read_checked(PACKAGE / "generation_manifest.json"):
        raise ValueError("Generation source/request freeze changed")
    rec = read_checked(PACKAGE / "reconciliation.json")
    records, calls = execute(plan, rec, replay=True,
                             responder=lambda _: (_ for _ in ()).throw(AssertionError("Offline only")))
    if calls:
        raise ValueError("Unexpected new dispatch")
    derived = read_checked(PACKAGE / "generation_result.json")
    if derived["accounted_nano"] != sum(r["accounted_nano"] for r in records):
        raise ValueError("Candidate cost summary differs")
    for saved, raw in zip(derived["results"], records):
        if saved["record_sha256"] != digest(raw) or saved["parsed"] != raw["parsed"]:
            raise ValueError("Candidate summary/record mismatch")
    r3 = ROOT / "experiments/phase3_benchmarks/variants_r3"
    if repaired() != read_checked(r3 / "candidates.json") or review_plan() != read_checked(r3 / "review_manifest.json"):
        raise ValueError("Repaired candidate/review freeze differs")
    with Continuation(LEDGER, rec) as budget:
        state = budget.audit()
        original_keys = {Path(p).stem for p in rec["preserved_files"] if p.startswith("records/")}
        expected = original_keys | {digest(job["slot"]) for job in plan["jobs"]}
        if (len(expected) != 43 or set(state["reservations"]) != expected
                or state["pending"] or state["failed"] or state["historical_failed"] != [digest(FAILED_SLOT)]):
            raise ValueError("Unexpected/missing candidate checkpoint records")
        if state["charged_or_reserved_nano"] != 337570200 + derived["accounted_nano"]:
            raise ValueError("Cumulative cost mismatch")
    original = json.loads((ROOT / "experiments/phase3_preparation_20260913/VERIFICATION.json").read_bytes())
    for relative, expected in original["immutable_inputs_sha256"].items():
        if hashlib.sha256((ROOT / relative).read_bytes()).hexdigest() != expected:
            raise ValueError("Historical scientific input changed")
    if (ROOT / "AGENTS.md").read_text(encoding="utf-8").split("\n", 1)[1] != (ROOT / "CLAUDE.md").read_text(encoding="utf-8").split("\n", 1)[1]:
        raise ValueError("Companion instructions differ")
    members = {p.relative_to(LEDGER).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in LEDGER.rglob("*.json")}
    archive = ROOT / "output/phase3_candidates_20260913.zip"
    if not archive.exists():
        with zipfile.ZipFile(archive, "x", compression=zipfile.ZIP_DEFLATED) as zf:
            for name in sorted(members):
                zf.write(LEDGER / name, name)
    with zipfile.ZipFile(archive) as zf:
        if zf.testzip() is not None or set(zf.namelist()) != set(members):
            raise ValueError("Archive incomplete/corrupt")
        for name, expected in members.items():
            if hashlib.sha256(zf.read(name)).hexdigest() != expected:
                raise ValueError("Archive member changed")
    result = {"calls": 43, "generation_calls": 5, "new_calls_during_verification": 0,
              "generation_accounted_nano": derived["accounted_nano"],
              "phase3_accounted_nano": state["charged_or_reserved_nano"],
              "by_provider_nano": state["by_provider_nano"],
              "preserved_historical_failure_count": 1, "pending": 0, "new_failures": 0,
              "historical_evidence_unchanged": True, "repaired_candidate_provenance_verified": True,
              "independent_review_calls": 0, "archive": archive.relative_to(ROOT).as_posix(),
              "archive_members": len(members), "archive_sha256": hashlib.sha256(archive.read_bytes()).hexdigest(),
              "off_device_backup_verified": False}
    save(PACKAGE / "GENERATION_CHECKPOINT.json", result)
    return result


if __name__ == "__main__":
    print(json.dumps(verify()))
