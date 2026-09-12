"""Read-only post-collection audit and fixed review pack; cannot dispatch API calls.

This auditor is separate from the frozen collector. It does not alter the analysis
or responses and verifies state reconstruction against every exact saved request.
"""
from __future__ import annotations

import asyncio
from collections import Counter
import hashlib
import json
from pathlib import Path

from run_phase2_confirmation import ROOT, PACKAGE, RAW, verify
from engine.population import Population
from phase2_confirmation_design import execute, parse, LABELS
from phase2_confirmation_transport import Ledger, StopRun, read_record, digest, now


class ReadOnlyLedger(Ledger):
    async def complete(self, slot, messages, seed, meta):
        key = digest(slot)
        if key not in self.results:
            raise StopRun("Read-only audit: missing call; network execution is prohibited")
        self.visited.add(key)
        # Cached branch only: the membership check above prevents transport entry.
        return await super().complete(slot, messages, seed, meta)


async def audit():
    manifest = verify()
    ledger = ReadOnlyLedger(RAW, digest(manifest), mock=False)
    ledger.visited = set()
    try:
        population = Population.load(PACKAGE / "population.json")
        groups = read_record(PACKAGE / "schedule.json")["groups"]
        expected_groups = {digest([g["problem"], g["group"], config, arm])
                           for g in groups for config, arm in g["conditions"]}
        if {p.stem for p in (RAW / "groups").glob("*.json")} != expected_groups:
            raise StopRun("Read-only audit requires all expected group artifacts and no extras")
        await execute(ledger, population, groups)
        if ledger.visited != ledger.results.keys():
            raise StopRun("Unexplained extra response slots")
        records = list(ledger.results.values())
        assert ledger.n_new == 0 and ledger.client is None
    finally:
        ledger.close()
    statuses, finishes = Counter(), Counter()
    ids = []
    actual_price_nano = 0
    review_simple, review_groups = [], []
    for r in sorted(records, key=lambda r: str(r["slot"])):
        meta = r["meta"]
        parsed = parse(r, LABELS[meta["problem"]], simple=meta["stage"] == "simple")
        statuses[parsed["status"]] += 1
        raw = r.get("response") or {}
        ids.append(raw.get("id"))
        finishes[(raw.get("choices") or [{}])[0].get("finish_reason")] += 1
        usage = raw.get("usage") or {}
        cached = (usage.get("prompt_tokens_details") or {}).get("cached_tokens", 0)
        if r["usage_known"]:
            actual_price_nano += (usage["prompt_tokens"] - cached) * 750 + cached * 75 + usage["completion_tokens"] * 4500
        entry = {"slot": r["slot"], "meta": meta, "text": parsed["text"], "status": parsed["status"],
                 "response_hash": digest(r)}
        if meta["stage"] == "simple" and meta["agent"] in range(1, 362, 40):
            review_simple.append(entry)
        elif meta["stage"] == "complex" and meta["group"] == 1:
            review_groups.append(entry)
    if len(ids) != len(set(ids)) or None in ids:
        raise StopRun("Missing or duplicate API IDs")
    review_root = RAW / "review"
    review_root.mkdir(exist_ok=True)
    pack = {"selection": "Simple IDs 1,41,...361, all cells; group 1, all cells and rounds", "simple": review_simple, "groups": review_groups}
    pack_path = review_root / "fixed_review_pack.json"
    if pack_path.exists():
        if json.loads(pack_path.read_text(encoding="utf-8")) != pack:
            raise StopRun("Existing review pack differs")
    else:
        pack_path.write_text(json.dumps(pack, indent=2) + "\n", encoding="utf-8", newline="\n")
    report = {"audited_at": now(), "manifest_hash": digest(manifest), "exact_request_replay_passed": True,
              "group_state_replay_passed": True, "new_dispatches": 0, "unique_api_ids": len(ids),
              "statuses": dict(statuses), "finish_reasons": dict(finishes),
              "estimated_provider_token_cost_usd_at_global_rates": actual_price_nano / 1e9,
              "provider_invoice_verified": False, "conservative_accounted_usd": ledger.charged / 1e9,
              "fixed_review_simple_n": len(review_simple), "fixed_review_group_responses_n": len(review_groups),
              "fixed_review_pack_sha256": hashlib.sha256(pack_path.read_bytes()).hexdigest(),
              "manual_review_status": "pack prepared; interpretation must be recorded separately"}
    path = PACKAGE / "analysis" / "integrity_audit.json"
    path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(report), flush=True)


if __name__ == "__main__":
    asyncio.run(audit())
