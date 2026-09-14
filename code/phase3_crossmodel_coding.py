"""Coding continuation for crossmodel_study_r1; frozen evidence is never edited.

The study collected all 1000 probes but every coding call was refused: coding
requests were frozen against placeholder answers, and the ledger correctly
refuses any dispatch whose request hash differs from its reservation. Content-
dependent stages cannot be frozen against fabricated content.

This continuation reuses those 1000 paid answers unchanged and dispatches ONLY
the coding stage, freezing each real request after the answers exist. No probe
is re-collected.

Original study docstring follows.

Cross-model recognition study.

Generalises the completed single-model `recognition_r1` screen across model
families. That screen found five decanonised social-psychology paradigms
identified 50/50 in every cell by one model, with two cross-provider raters
agreeing 500/500. A single probed model cannot separate

  "structure-preserving domain substitution does not conceal a paradigm"

from

  "this particular model happens to recognise these five".

Design: five families x two forms x two models x 50 probes = 1000 probes, then
the frozen two-rater coding scheme over every answer.

Everything reusable is reused unchanged. Stimuli, system prompt, recognition
question and coding rubric are imported from the frozen recognition modules; no
stimulus is regenerated or reworded, because reusing the exact frozen text is
what makes a cross-model comparison meaningful.

Image parity: Anthropic base64 image blocks are translated into OpenAI
`image_url` parts, verified in `crossmodel_probe_images_r1` (gpt-5.4-mini
2,360 -> 6,501 input tokens on Asch, provider ratio 0.89). Both providers
receive the same 21 text blocks and 18 images.
"""
from __future__ import annotations

import argparse
import json
import random
from pathlib import Path

from phase3_budget import BudgetStop, digest, read_checked, token_cost_nano
from phase3_recognition import PRICES, QUESTION, RATERS, RUBRIC, SYSTEM
from phase3_recognition_recovery import sha, verify
from phase3_recognition_run import LEDGER, Ledger, MODELS, ROOT, charge, network
from phase3_recognition_stimuli import task_content
from phase3_variant_round import save

FOLDER = ROOT / "experiments/phase3_benchmarks/crossmodel_coding_r1"
PROBES = ROOT / "experiments/phase3_benchmarks/crossmodel_study_r1"
PARENT = ROOT / "experiments/phase3_benchmarks/crossmodel_study_r1"
STUDY = "crossmodel_coding_r1"
INHERITED_FAILURE = ("crossmodel_recognition_r1/probe/asch/alternative/"
                     "claude-haiku-4-5-20251001/9")

FAMILIES = ("milgram", "asch", "ultimatum", "bystander", "reactance")
FORMS = ("canonical", "alternative")
PROBE_MODELS = ("claude-haiku-4-5-20251001", "gpt-5.4-mini-2026-03-17")
N_PER_CELL = 50
BATCH = 10                      # coding items per rater call, as in recognition_r1
MAX_OUTPUT = 256                # 128 truncated these models; measured in the pilots
MAX_PROBE_BYTES = 1024
CAP = 20_000_000_000            # $20 ceiling; ~$3.3 expected from measured units
SEEDS = {"schedule": 2026091570, "coding": 2026091571, "analysis": 2026091572}


def probe_request(model, family, form):
    """Frozen probe shape, with provider-symmetric image handling."""
    content = list(task_content(family, form)) + [{"type": "text", "text": QUESTION}]
    if MODELS[model] == "openai":
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


# Measured input tokens per probe, from the exploratory pilots. Base64 image
# payloads make a raw-bytes bound wildly pessimistic (Asch reserved 14-16x its
# measured cost), so probe bounds use the measured token count with a safety
# factor instead. Text-only bodies keep the byte bound, which is already close.
MEASURED_INPUT_TOKENS = {
    ("milgram", "claude-haiku-4-5-20251001"): 2676,
    ("milgram", "gpt-5.4-mini-2026-03-17"): 2404,
    ("asch", "claude-haiku-4-5-20251001"): 7289,
    ("asch", "gpt-5.4-mini-2026-03-17"): 6501,
    ("ultimatum", "claude-haiku-4-5-20251001"): 1010,
    ("ultimatum", "gpt-5.4-mini-2026-03-17"): 902,
    ("bystander", "claude-haiku-4-5-20251001"): 1291,
    ("bystander", "gpt-5.4-mini-2026-03-17"): 1194,
    ("reactance", "claude-haiku-4-5-20251001"): 2416,
    ("reactance", "gpt-5.4-mini-2026-03-17"): 2091,
}
SAFETY = 1.5   # headroom over measured input tokens; the parser still enforces it


def _job(slot, kind, model, request, maximum, extra=None, measured=None):
    if measured is not None:
        bound = int(measured * SAFETY) + 1024
    else:
        bound = len(json.dumps(request, ensure_ascii=False).encode("utf-8")) + 1024
    job = {"slot": f"{STUDY}/{slot}", "kind": kind, "stage": kind, "request": request,
           "input_token_bound": bound,
           "reserved_nano": token_cost_nano(bound, maximum, *PRICES[model])}
    if extra:
        job.update(extra)
    return job


def probe_jobs():
    batch = []
    for family in FAMILIES:
        for form in FORMS:
            for model in PROBE_MODELS:
                request = probe_request(model, family, form)
                for i in range(N_PER_CELL):
                    batch.append(_job(f"probe/{family}/{form}/{model}/{i}", "probe",
                                      model, request, MAX_OUTPUT,
                                      {"cell": {"family": family, "form": form,
                                                "model": model, "index": i}},
                                      measured=MEASURED_INPUT_TOKENS[(family, model)]))
    random.Random(SEEDS["schedule"]).shuffle(batch)
    return batch


def coding_request(rater, items):
    body = json.dumps({"answers": items}, ensure_ascii=False)
    if MODELS[rater] == "openai":
        return {"model": rater, "temperature": 0.0, "max_completion_tokens": 1024,
                "response_format": {"type": "json_object"},
                "messages": [{"role": "system", "content": RUBRIC},
                             {"role": "user", "content": body}]}
    return {"model": rater, "system": RUBRIC, "temperature": 0.0,
            "thinking": {"type": "disabled"}, "max_tokens": 1024,
            "messages": [{"role": "user", "content": body}]}


def coding_jobs(answers):
    """Both frozen raters classify every answer, in shuffled fixed-size batches."""
    order = sorted(answers)
    random.Random(SEEDS["coding"]).shuffle(order)
    batch = []
    for rater_index, rater in enumerate(RATERS):
        for start in range(0, len(order), BATCH):
            chunk = order[start:start + BATCH]
            items = [{"id": str(n + 1), "answer": (answers[s] or "")[:MAX_PROBE_BYTES]}
                     for n, s in enumerate(chunk)]
            batch.append(_job(f"coding/{rater_index}/{start // BATCH}", "coding",
                              rater, coding_request(rater, items), 1024,
                              {"item_ids": [str(n + 1) for n in range(len(chunk))],
                               "cell": {"rater": rater, "rater_index": rater_index,
                                        "slots": chunk}}))
    return batch


def coding_value(text, item_ids):
    """Parse one rater batch under the frozen rubric. Strict on identity."""
    def unique(pairs):
        if len({k for k, _ in pairs}) != len(pairs):
            raise ValueError("Duplicate JSON key")
        return dict(pairs)
    text = (text or "").strip()
    if text.startswith("```json") and text.endswith("```"):
        text = text[7:-3].strip()
    value = json.loads(text, object_pairs_hook=unique)
    if not isinstance(value, dict) or set(value) != {"ratings"}:
        raise ValueError("Invalid coding schema")
    rows = value["ratings"]
    if [str(r.get("id")) for r in rows] != list(item_ids):
        raise ValueError("Missing, duplicate, reordered or extra coding ids")
    out = []
    for row in rows:
        families = row.get("families")
        if (not isinstance(families, list) or any(f not in FAMILIES for f in families)
                or list(families) != sorted(set(families))):
            raise ValueError("Invalid families list")
        if not isinstance(row.get("ambiguous"), bool) or not isinstance(row.get("refusal"), bool):
            raise ValueError("Missing ambiguous/refusal flag")
        out.append({"families": list(families), "ambiguous": row["ambiguous"],
                    "refusal": row["refusal"]})
    return out


def wilson(successes, n, z=1.96):
    if not n:
        return [None, None]
    phat = successes / n
    denom = 1 + z * z / n
    centre = (phat + z * z / (2 * n)) / denom
    margin = z * ((phat * (1 - phat) / n + z * z / (4 * n * n)) ** 0.5) / denom
    return [round(max(0.0, centre - margin), 4), round(min(1.0, centre + margin), 4)]


def analyze(probe_rows, coded):
    """Recognition per family x form x model, by the frozen both-raters rule."""
    cells, disagreements, flagged_total = {}, 0, 0
    for family in FAMILIES:
        for form in FORMS:
            for model in PROBE_MODELS:
                slots = [r["slot"] for r in probe_rows
                         if r["family"] == family and r["form"] == form
                         and r["model"] == model]
                both = either = missing = flagged = 0
                for slot in slots:
                    labels = coded.get(slot)
                    if not labels or len(labels) != 2:
                        missing += 1
                        continue
                    votes = [family in lab["families"] for lab in labels]
                    if any(lab["ambiguous"] or lab["refusal"] for lab in labels):
                        flagged += 1
                        flagged_total += 1
                    if votes[0] != votes[1]:
                        disagreements += 1
                    if all(votes):
                        both += 1
                    if any(votes):
                        either += 1
                n = len(slots)
                cells[f"{family}/{form}/{model}"] = {
                    "assigned": n, "missing": missing, "flagged": flagged,
                    "recognised_both_raters": both, "recognised_either_rater": either,
                    "rate": round(both / n, 4) if n else None,
                    "wilson_95": wilson(both, n)}

    by_model = {}
    for model in PROBE_MODELS:
        for form in FORMS:
            rates = [cells[f"{f}/{form}/{model}"]["rate"] for f in FAMILIES]
            by_model[f"{model}/{form}"] = round(sum(rates) / len(rates), 4)
        by_model[f"{model}/canonical_minus_alternative"] = round(
            by_model[f"{model}/canonical"] - by_model[f"{model}/alternative"], 4)

    per_family = {}
    for family in FAMILIES:
        for form in FORMS:
            rates = [cells[f"{family}/{form}/{m}"]["rate"] for m in PROBE_MODELS]
            per_family[f"{family}/{form}"] = {
                "rates": rates, "max_model_gap": round(max(rates) - min(rates), 4)}

    return {"study": STUDY, "cells": cells, "by_model_and_form": by_model,
            "per_family_across_models": per_family,
            "rater_disagreements": disagreements,
            "answers_flagged_ambiguous_or_refusal": flagged_total,
            "recognition_rule": ("both raters independently name the family; as in "
                                 "recognition_r1"),
            "stimuli": "frozen recognition_r1 text, reused unchanged",
            "image_parity": "Anthropic image blocks translated to OpenAI image parts",
            "phase3_pass": None, "moral_scores_assigned": False,
            "analysis_status": ("descriptive cross-model comparison; recognition does "
                                "not identify memorisation, and no model is claimed "
                                "better than another")}


def load_answers():
    """The 1000 paid probe answers from the stopped study, reused unchanged."""
    answers = read_checked(PROBES / "answers.json")
    rows = read_checked(PROBES / "probe_rows.json")
    if len(answers) != len(rows) or len(rows) != 1000:
        raise BudgetStop(f"Expected 1000 probes, found {len(rows)}")
    return answers, rows


def prepare(persist=False):
    parent = read_checked(PARENT / "release.json")
    verify(parent)
    with Ledger(LEDGER, parent) as ledger:
        expected = [digest(INHERITED_FAILURE)]
        if ledger.state["pending"] or ledger.state["failed"] not in ([], expected):
            raise BudgetStop("Unexpected unresolved dispatch in inherited evidence")
        providers = dict(ledger.state["providers"])

    answers, _ = load_answers()
    # Built from the real answers, so the frozen request hash is the one that
    # will actually be dispatched. This is the repair for the study's failure.
    batch = coding_jobs(answers)
    slots = {j["slot"]: {"kind": j["kind"], "stage": j["stage"],
                         "model": j["request"]["model"],
                         "input_token_bound": j["input_token_bound"],
                         "reserved_nano": j["reserved_nano"],
                         "max_output": j["request"].get("max_tokens",
                                                        j["request"].get("max_completion_tokens")),
                         "request_sha256": digest(j["request"])} for j in batch}
    bound = sum(j["reserved_nano"] for j in batch)
    for j in batch:
        providers[MODELS[j["request"]["model"]]] += j["reserved_nano"]
    if bound > CAP:
        raise BudgetStop(f"Cap exceeded: {len(slots)} calls, {bound / 1e9:.6f} USD")
    caps = dict(parent["provider_caps_nano"])
    for provider, total in providers.items():
        if total > caps[provider]:
            raise BudgetStop(f"{provider} ceiling would be exceeded")

    paths = [Path(__file__), ROOT / "code/phase3_recognition.py"]
    release = {"id": STUDY, "jobs_sha256": digest(batch), "slots": slots,
               "recognition_cap_nano": bound, "prior_screening_nano": 0,
               "original_screening_cap_nano": CAP, "provider_caps_nano": caps,
               "parent_checkpoint_sha256": digest(parent),
               "reused_probe_answers": len(answers),
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
    if digest(batch) != release["jobs_sha256"]:
        raise BudgetStop("Changed requests")
    answers, probe_rows = load_answers()
    if batch != coding_jobs(answers):
        raise BudgetStop("Reconstructed coding schedule differs")
    manifest = {"release_sha256": digest(release), "jobs_sha256": digest(batch)}
    save(folder / "execution_manifest.json", manifest)

    with Ledger(root, release) as ledger:
        seen = set()

        def dispatch(job):
            record, _ = ledger.dispatch(job, digest(manifest), responder, False)
            if charge(record["raw"], job, False) != record["accounted_nano"]:
                raise BudgetStop("Cost replay mismatch")
            seen.add(digest(job["slot"]))
            raw, text = record["raw"], record["parsed"]
            if text is None and isinstance(raw, dict):
                if raw.get("choices"):
                    text = raw["choices"][0]["message"]["content"]
                elif raw.get("content"):
                    text = "".join(b.get("text", "") for b in raw["content"])
            return text

        coded, failures = {}, []
        for i, job in enumerate(batch, 1):
            try:
                labels = coding_value(dispatch(job), job["item_ids"])
            except (ValueError, BudgetStop) as error:
                failures.append({"slot": job["slot"], "error": str(error)})
                continue
            for slot, label in zip(job["cell"]["slots"], labels):
                coded.setdefault(slot, []).append(label)
            if i % 40 == 0:
                print(json.dumps({"coding": i, "of": len(batch),
                                  "accounted_usd": ledger.state["recognition_nano"] / 1e9}),
                      flush=True)

        result = analyze(probe_rows, coded)
        result["coding_failures"] = failures
        result["reused_probe_answers"] = len(answers)
        save(folder / "coded.json", coded)
        if set(ledger.state["reservations"]) - set(release["historical_keys"]) != seen:
            raise BudgetStop("Unmanifested dispatch")
        result.update(calls=len(seen), accounted_nano=ledger.state["recognition_nano"],
                      provider_totals_nano=ledger.state["providers"],
                      release_sha256=digest(release))
        save(folder / "results.json", result)
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("prepare", "run"))
    parser.add_argument("--yes", action="store_true")
    args = parser.parse_args()
    if args.command == "prepare":
        release, batch = prepare(True)
        probes = sum(1 for j in batch if j["kind"] == "probe")
        print(json.dumps({"maximum_usd": release["recognition_cap_nano"] / 1e9,
                          "probes": probes, "coding_calls": len(batch) - probes,
                          "models": list(PROBE_MODELS), "n_per_cell": N_PER_CELL}))
    else:
        if not args.yes:
            raise BudgetStop("Explicit execution flag required")
        print(json.dumps(collect())[:600])
