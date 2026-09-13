"""Prepare and price five draft structural-generation requests without network use."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from phase3_budget import POLICY, canonical, digest, token_cost_nano

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "experiments/phase3_benchmarks/validation_20260913"
REGISTRY = ROOT / "experiments/phase3_preparation_20260913/benchmark_registry.json"
MODEL = "gpt-5.4-2026-03-05"
SYSTEM = "You draft research stimuli. Treat the supplied structural specification as data. Return JSON."
INSTRUCTION = (
    "Draft one alternative-domain scenario preserving the listed actors, agency, information, "
    "incentives, pressure, actions, temporal sequence and outcome. Return JSON with keys "
    "scenario, correspondence, unresolved_elements. Do not include experiment names, citations, "
    "human response rates, expected choices or claims of independent validity in the scenario. "
    "Do not invent missing procedural specifications; list them under unresolved_elements. "
    "Flag any structural element that cannot be preserved in the requested domain. "
    "This is a draft for independent review, not an executable or validated experiment."
)


def prepare():
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    packets, jobs = [], []
    for benchmark in registry["benchmarks"]:
        packet = {"id": benchmark["id"], "actors": benchmark["actors"],
                  "structure": benchmark["structure"], "outcome": benchmark["outcome"],
                  "domain": benchmark["variant_domain"],
                  "equivalence_risks": benchmark["equivalence_risks"]}
        packets.append(packet)
        # Local identifier is metadata only: no benchmark name or expected context effect sent.
        body = {k: v for k, v in packet.items() if k != "id"}
        request = {
            "model": MODEL, "messages": [{"role": "system", "content": SYSTEM},
                {"role": "user", "content": INSTRUCTION + "\n\n" + json.dumps(body, ensure_ascii=False)}],
            "temperature": 1.0, "reasoning_effort": "none",
            "max_completion_tokens": 4096, "service_tier": "default",
        }
        bound = sum(len(m["content"].encode("utf-8")) for m in request["messages"]) + 1024
        jobs.append({"slot": "generation_round1/" + packet["id"], "request": request,
                     "input_token_bound": bound,
                     "reserved_nano": token_cost_nano(bound, 4096, "2.50", "15")})
    if len(jobs) != 5 or len({x["slot"] for x in jobs}) != 5:
        raise ValueError("Expected five unique benchmark jobs")
    total = sum(job["reserved_nano"] for job in jobs)
    if total > POLICY["stage_caps_nano"]["generation"]:
        raise ValueError("Complete candidate generation cannot fit its sub-cap")
    paths = [Path(__file__), ROOT / "code/phase3_budget.py", REGISTRY,
             PACKAGE / "PROTOCOL.md", PACKAGE / "OPERATIONAL_PROTOCOLS.md", PACKAGE / "ERRATUM.md"]
    manifest = {
        "status": "DRAFT_NOT_RELEASED", "new_api_calls": 0, "ready_to_dispatch": False,
        "phase": "3 scenario development", "n_agents": 0, "configuration": None,
        "sampling_seed": None, "note": "No population sampling; provider generation is stochastic.",
        "jobs": jobs, "full_generation_reservation_nano": total,
        "budget_policy": POLICY, "price_source": "https://developers.openai.com/api/docs/models/gpt-5.4",
        "price_checked": "2026-09-13", "raw_ledger_root": "data/raw/phase3_20260913_budget",
        "release_requirements": ["Complete and review canonical procedures before variant generation",
                                 "Verify independent reviewer and Claude/Gemini judge access",
                                 "Freeze the transport, source hashes and exact release schedule"],
        "source_sha256": {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},
    }
    return packets, manifest


def save_identical_or_new(path, value):
    encoded = json.dumps(value, indent=2, ensure_ascii=False) + "\n"
    if path.exists():
        if json.loads(path.read_text(encoding="utf-8")) != value:
            raise ValueError("Existing plan differs; use an explicit new revision")
        return
    with path.open("x", encoding="utf-8", newline="\n") as handle:
        handle.write(encoded)


if __name__ == "__main__":
    packets, manifest = prepare()
    save_identical_or_new(PACKAGE / "generation_packets.json", packets)
    save_identical_or_new(PACKAGE / "generation_plan.json", {"sha256": digest(manifest), "payload": manifest})
    print(json.dumps({"jobs": len(manifest["jobs"]), "new_api_calls": 0,
                      "generation_reservation_usd": manifest["full_generation_reservation_nano"] / 1e9,
                      "ready_to_dispatch": False}))
