"""Exploratory cross-model recognition pilot; small, cheap, measures real cost.

Purpose: find out what a cross-model recognition probe actually costs and
whether the frozen stimuli work unchanged on models other than the one probed
in `recognition_r1`. This is an exploratory probe batch under $1, not a study.

It exists because a first attempt at the full design mis-sized the request:
stimuli were JSON-dumped instead of passed as content blocks, and the Asch
family carries 18 image blocks, so a single probe consumed 81,266 input tokens.
This module uses the frozen `probe_request` shape and reports measured usage per
family and model so a real design can be sized from evidence.

No recognition claim is made here. Answers are saved and left uncoded: the
two-rater coding step belongs to a properly designated study.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from phase3_budget import BudgetStop, digest, read_checked, token_cost_nano
from phase3_recognition import PRICES, QUESTION, SYSTEM
from phase3_recognition_recovery import sha, verify
from phase3_recognition_run import LEDGER, Ledger, MODELS, ROOT, charge, network
from phase3_recognition_stimuli import task_content
from phase3_variant_round import save

FOLDER = ROOT / "experiments/phase3_benchmarks/crossmodel_pilot_images_r1"
# The stopped crossmodel_recognition_r1 attempt is the ledger head: it collected
# probes before failing on an over-sized Asch request, and its failed slot is
# preserved at full reservation under the no-retry rule.
PARENT = ROOT / "experiments/phase3_benchmarks/crossmodel_pilot_asch_r1"
INHERITED_FAILURE = ("crossmodel_recognition_r1/probe/asch/alternative/"
                     "claude-haiku-4-5-20251001/9")
STUDY = "crossmodel_pilot_images_r1"

# Asch is excluded from the pilot: its 18 image blocks dominate cost and it is
# the one family whose sizing is already known to be extreme. Text-only families
# first, so the cheap majority of the design can be priced accurately.
FAMILIES = ("asch",)   # verify the repaired OpenAI image path
FORMS = ("alternative",)
PROBE_MODELS = ("claude-haiku-4-5-20251001", "gpt-5.4-mini-2026-03-17")
N_PER_CELL = 1
CAP = 1_000_000_000             # $1.00 exploratory ceiling
MAX_OUTPUT = 256                # the frozen screen used 128 and hit max_tokens


def probe_request(model, family, form):
    """Frozen probe shape: stimulus content blocks plus the recognition question."""
    content = list(task_content(family, form)) + [{"type": "text", "text": QUESTION}]
    if MODELS[model] == "openai":
        # Translate Anthropic content blocks to OpenAI parts, CARRYING IMAGES.
        # The first pilot flattened to text and silently dropped Asch's 18
        # images, so the two providers saw different stimuli for that family.
        parts = []
        for block in content:
            if block.get("type") == "text":
                parts.append({"type": "text", "text": block["text"]})
            elif block.get("type") == "image":
                source = block["source"]
                if source.get("type") != "base64":
                    raise BudgetStop(f"Unsupported image source: {source.get('type')}")
                parts.append({"type": "image_url", "image_url": {
                    "url": f"data:{source['media_type']};base64,{source['data']}"}})
            else:
                raise BudgetStop(f"Unsupported content block: {block.get('type')}")
        return {"model": model, "temperature": 1.0,
                "max_completion_tokens": MAX_OUTPUT,
                "messages": [{"role": "system", "content": SYSTEM},
                             {"role": "user", "content": parts}]}
    return {"model": model, "system": SYSTEM, "temperature": 1.0,
            "thinking": {"type": "disabled"}, "max_tokens": MAX_OUTPUT,
            "messages": [{"role": "user", "content": content}]}


def jobs():
    batch = []
    for family in FAMILIES:
        for form in FORMS:
            for model in PROBE_MODELS:
                for i in range(N_PER_CELL):
                    req = probe_request(model, family, form)
                    payload = json.dumps(req, ensure_ascii=False)
                    bound = len(payload.encode("utf-8")) + 1024
                    batch.append({
                        "slot": f"{STUDY}/probe/{family}/{form}/{model}/{i}",
                        "kind": "probe", "stage": "probe", "request": req,
                        "input_token_bound": bound,
                        "reserved_nano": token_cost_nano(bound, MAX_OUTPUT, *PRICES[model]),
                        "cell": {"family": family, "form": form, "model": model,
                                 "index": i}})
    return batch


def prepare(persist=False):
    parent = read_checked(PARENT / "release.json")
    verify(parent)
    with Ledger(LEDGER, parent) as ledger:
        expected = [digest(INHERITED_FAILURE)]
        if ledger.state["pending"] or ledger.state["failed"] not in ([], expected):
            raise BudgetStop("Unexpected unresolved dispatch in inherited evidence")
    batch = jobs()
    bound = sum(j["reserved_nano"] for j in batch)
    if bound > CAP:
        raise BudgetStop(f"Cap exceeded: {len(batch)} calls, {bound / 1e9:.6f} USD")
    slots = {j["slot"]: {"kind": j["kind"], "stage": j["stage"],
                         "model": j["request"]["model"],
                         "input_token_bound": j["input_token_bound"],
                         "reserved_nano": j["reserved_nano"],
                         "max_output": j["request"].get("max_tokens",
                                                        j["request"].get("max_completion_tokens")),
                         "request_sha256": digest(j["request"])} for j in batch}
    paths = [Path(__file__), ROOT / "code/phase3_recognition.py",
             ROOT / "code/phase3_recognition_stimuli.py"]
    release = {"id": STUDY, "jobs_sha256": digest(batch), "slots": slots,
               "recognition_cap_nano": bound, "prior_screening_nano": 0,
               "original_screening_cap_nano": CAP,
               "provider_caps_nano": parent["provider_caps_nano"],
               "parent_checkpoint_sha256": digest(parent),
               "historical_keys": sorted(p.stem for p in (LEDGER / "records").glob("*.json")),
               "preserved_files": {p.relative_to(LEDGER).as_posix(): sha(p)
                                   for p in LEDGER.rglob("*.json")},
               "failure_log_prefix_bytes": (LEDGER / "failures.jsonl").stat().st_size,
               "failure_log_prefix_sha256": sha(LEDGER / "failures.jsonl"),
               "source_sha256": {**parent["source_sha256"],
                                 **{p.relative_to(ROOT).as_posix(): sha(p) for p in paths}}}
    with Ledger(LEDGER, release):
        pass
    if persist:
        save(FOLDER / "requests.json", batch)
        save(FOLDER / "release.json", release)
    return release, batch


def collect(root=LEDGER, folder=FOLDER, responder=network):
    root, folder = Path(root), Path(folder)
    release = read_checked(folder / "release.json")
    batch = read_checked(folder / "requests.json")
    verify(release, root)
    manifest = {"release_sha256": digest(release), "jobs_sha256": digest(batch)}
    save(folder / "execution_manifest.json", manifest)

    rows, failures = [], []
    with Ledger(root, release) as ledger:
        for job in batch:
            try:
                record, _ = ledger.dispatch(job, digest(manifest), responder, False)
            except BudgetStop as stop:
                # Exploratory: record the stop and continue measuring other cells.
                failures.append({**job["cell"], "slot": job["slot"], "error": str(stop)})
                break
            raw = record["raw"]
            usage = raw.get("usage", {})
            text = record["parsed"]
            if text is None and isinstance(raw, dict):
                if raw.get("choices"):
                    text = raw["choices"][0]["message"]["content"]
                elif raw.get("content"):
                    text = "".join(b.get("text", "") for b in raw["content"])
            rows.append({
                **job["cell"], "slot": job["slot"],
                "input_tokens": usage.get("input_tokens", usage.get("prompt_tokens")),
                "output_tokens": usage.get("output_tokens", usage.get("completion_tokens")),
                "stop": raw.get("stop_reason") or (raw.get("choices") or [{}])[0].get("finish_reason"),
                "accounted_nano": record["accounted_nano"],
                "answer": (text or "")[:600]})
            print(json.dumps({"done": len(rows), "of": len(batch),
                              "accounted_usd": ledger.state["recognition_nano"] / 1e9}),
                  flush=True)
        spent = ledger.state["recognition_nano"]

    result = {"study": STUDY, "probes": len(rows), "failures": failures,
              "accounted_nano": spent,
              "status": "exploratory cost and feasibility probe; no recognition claim"}
    save(folder / "probe_rows.json", rows)
    save(folder / "results.json", result)
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("prepare", "run"))
    parser.add_argument("--yes", action="store_true")
    args = parser.parse_args()
    if args.command == "prepare":
        release, batch = prepare(True)
        print(json.dumps({"maximum_usd": release["recognition_cap_nano"] / 1e9,
                          "probes": len(batch), "models": list(PROBE_MODELS),
                          "families": list(FAMILIES)}))
    else:
        if not args.yes:
            raise BudgetStop("Explicit execution flag required")
        print(json.dumps(collect())[:400])
