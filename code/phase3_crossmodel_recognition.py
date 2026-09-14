"""Cross-model recognition screen; frozen evidence is never edited.

The completed [recognition_r1] screen probed **one model**. It found that five
decanonised social-psychology paradigms were identified 50/50 in every cell,
with two cross-provider raters agreeing 500/500. That is a strong result about
one model and a weak one about the method, because a single model cannot
distinguish "structure-preserving domain substitution does not conceal a
paradigm" from "this particular model happens to recognise these five".

This designation probes the **same frozen stimuli** across three models spanning
two providers, so the claim can be stated about models rather than about a model.

  claude-sonnet-4-6            anthropic   (the original probe target)
  claude-haiku-4-5-20251001    anthropic   (same family, smaller)
  gpt-5.4-mini-2026-03-17      openai      (different family)

Stimuli, question and system prompt are imported unchanged from the frozen
recognition modules. No stimulus is regenerated, reworded or re-reviewed: reusing
the exact frozen text is what makes the comparison across models meaningful.

Coding reuses the established two-rater scheme with the frozen rubric. Raters are
the two non-probed models where possible; a model's own answers are still coded
by both raters, which is disclosed rather than avoided, since excluding
self-coding would change the rater pair per cell and confound the comparison.
"""
from __future__ import annotations

import argparse
import json
import random
from pathlib import Path

from phase3_budget import BudgetStop, POLICY, digest, read_checked, token_cost_nano
from phase3_recognition import JUDGE, PRICES, QUESTION, RATERS, RUBRIC, SYSTEM
from phase3_recognition_recovery import sha, verify
from phase3_recognition_run import LEDGER, Ledger, MODELS, ROOT, charge, network
from phase3_recognition_stimuli import alternatives, task_content
from phase3_design_pilot import request
from phase3_variant_round import save

FOLDER = ROOT / "experiments/phase3_benchmarks/crossmodel_recognition_r1"
PARENT = ROOT / "experiments/phase4_coding/moral_capstone_r3"
STUDY = "crossmodel_recognition_r1"

FAMILIES = ("milgram", "asch", "ultimatum", "bystander", "reactance")
FORMS = ("canonical", "alternative")
PROBE_MODELS = ("claude-sonnet-4-6", "claude-haiku-4-5-20251001",
                "gpt-5.4-mini-2026-03-17")
N_PER_CELL = 10
BATCH = 10                      # coding items per rater call, as in recognition_r1
# Worst-case reservation, not expected spend. The Milgram stimulus is ~8k chars
# and input_token_bound counts utf-8 bytes, over-counting tokens roughly 4x, so
# the bound is far above settlement. Prior runs settled near 17% of reservation.
CAP = 18_000_000_000            # 18.00 USD ceiling; ~$3 expected settlement
SEEDS = {"schedule": 2026091560, "analysis": 2026091561}
MAX_PROBE_BYTES = 1024


def probe_body(family, form):
    """Exact frozen stimulus text plus the frozen recognition question."""
    content = task_content(family, form)
    text = content if isinstance(content, str) else json.dumps(content, ensure_ascii=False,
                                                              sort_keys=True)
    return text + "\n\n" + QUESTION


def make_job(slot, kind, model, system_text, body, maximum):
    bound = len((system_text + body).encode("utf-8")) + 1024
    req = request(model, system_text, body, maximum, temperature=1)
    if MODELS[model] == "openai":
        req["response_format"] = {"type": "json_object"} if kind == "coding" else None
        if req["response_format"] is None:
            del req["response_format"]
    return {"slot": f"{STUDY}/{slot}", "kind": kind, "stage": kind, "request": req,
            "input_token_bound": bound,
            "reserved_nano": token_cost_nano(bound, maximum, *PRICES[model])}


def probe_jobs():
    """Five families x two forms x three models x N probes, shuffled once."""
    batch = []
    for family in FAMILIES:
        for form in FORMS:
            body = probe_body(family, form)
            for model in PROBE_MODELS:
                for i in range(N_PER_CELL):
                    job = make_job(f"probe/{family}/{form}/{model}/{i}", "probe",
                                   model, SYSTEM, body, 128)
                    job["cell"] = {"stage": "probe", "family": family, "form": form,
                                   "model": model, "index": i}
                    batch.append(job)
    random.Random(SEEDS["schedule"]).shuffle(batch)
    return batch


def coding_jobs(answers):
    """Two independent raters classify every probe answer, in fixed batches.

    `answers` maps slot -> answer text. Items are shuffled into batches so a
    rater never sees one cell contiguously, exactly as in recognition_r1.
    """
    slots = sorted(answers)
    order = list(slots)
    random.Random(SEEDS["schedule"] + 1).shuffle(order)
    batch = []
    for rater_index, rater in enumerate(RATERS):
        for start in range(0, len(order), BATCH):
            chunk = order[start:start + BATCH]
            items = [{"id": str(n + 1), "answer": answers[s][:MAX_PROBE_BYTES]}
                     for n, s in enumerate(chunk)]
            job = make_job(f"coding/{rater_index}/{start // BATCH}", "coding", rater,
                           RUBRIC, json.dumps({"answers": items}, ensure_ascii=False),
                           1024)
            job["item_ids"] = [str(n + 1) for n in range(len(chunk))]
            job["cell"] = {"stage": "coding", "rater": rater,
                           "rater_index": rater_index, "slots": chunk}
            batch.append(job)
    return batch


def analyze(probe_rows, coded):
    """Recognition rate per family x form x model, plus cross-model comparison.

    A probe counts as recognised only when **both raters independently name the
    intended family**, with neither flagging the answer ambiguous or a refusal.
    That is the frozen recognition_r1 rule. Disagreements are reported, never
    resolved by majority or by one rater.
    """
    cells, disagreements, unresolved = {}, 0, 0
    for family in FAMILIES:
        for form in FORMS:
            for model in PROBE_MODELS:
                slots = [r["slot"] for r in probe_rows
                         if r["family"] == family and r["form"] == form
                         and r["model"] == model]
                both = either = missing = 0
                for slot in slots:
                    labels = coded.get(slot)
                    if not labels or len(labels) < 2:
                        missing += 1
                        continue
                    votes = []
                    flagged = False
                    for fams, ambiguous, refusal in labels:
                        if ambiguous or refusal:
                            flagged = True
                        votes.append(family in fams)
                    if flagged:
                        unresolved += 1
                    if votes[0] != votes[1]:
                        disagreements += 1
                    if all(votes) and not flagged:
                        both += 1
                    if any(votes):
                        either += 1
                cells[f"{family}/{form}/{model}"] = {
                    "assigned": len(slots), "missing": missing,
                    "recognised_both_raters": both,
                    "recognised_either_rater": either,
                    "rate": round(both / len(slots), 4) if slots else None}

    by_model = {}
    for model in PROBE_MODELS:
        for form in FORMS:
            rates = [cells[f"{f}/{form}/{model}"]["rate"] for f in FAMILIES
                     if cells[f"{f}/{form}/{model}"]["rate"] is not None]
            by_model[f"{model}/{form}"] = {
                "mean_rate": round(sum(rates) / len(rates), 4) if rates else None,
                "families": len(rates)}
    for model in PROBE_MODELS:
        can = by_model[f"{model}/canonical"]["mean_rate"]
        alt = by_model[f"{model}/alternative"]["mean_rate"]
        by_model[f"{model}/canonical_minus_alternative"] = (
            None if can is None or alt is None else round(can - alt, 4))

    return {"study": STUDY, "cells": cells, "by_model_and_form": by_model,
            "rater_disagreements": disagreements,
            "answers_flagged_ambiguous_or_refusal": unresolved,
            "recognition_rule": ("both raters name the intended family, neither "
                                 "flags ambiguity or refusal; as in recognition_r1"),
            "stimuli": "frozen recognition_r1 text, reused unchanged",
            "phase3_pass": None, "moral_scores_assigned": False,
            "analysis_status": ("descriptive cross-model comparison; recognition does "
                                "not identify memorisation, and no model is claimed "
                                "better than another")}


def prepare(persist=False):
    parent = read_checked(PARENT / "release.json")
    verify(parent)
    with Ledger(LEDGER, parent) as ledger:
        if ledger.state["pending"]:
            raise BudgetStop("Unresolved dispatch in inherited evidence")
        providers = dict(ledger.state["providers"])
    # Provider ceiling amendment, 15 September 2026: the researcher stated the
    # $15 Anthropic figure was a conservative planning estimate and raised it for
    # this designation. Recorded in the protocol; the package cap is unchanged
    # and still enforced below.
    caps = dict(parent["provider_caps_nano"])
    caps["anthropic"] = 25_000_000_000

    probes = probe_jobs()
    n_coding = 2 * ((len(probes) + BATCH - 1) // BATCH)
    # Coding bodies are sized from a worst-case answer, so the reservation holds
    # before any answer exists.
    placeholder = {s["slot"]: "x" * MAX_PROBE_BYTES for s in probes}
    batch = probes + coding_jobs(placeholder)
    if len(batch) != len(probes) + n_coding:
        raise BudgetStop("Unexpected coding batch size")

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

    paths = [Path(__file__), ROOT / "code/phase3_recognition.py",
             ROOT / "code/phase3_recognition_stimuli.py", FOLDER / "PROTOCOL.md"]
    release = {"id": STUDY, "jobs_sha256": digest(batch), "slots": slots,
               "recognition_cap_nano": bound, "prior_screening_nano": 0,
               "original_screening_cap_nano": CAP,
               "provider_caps_nano": caps,
               "parent_checkpoint_sha256": digest(parent),
               "probe_models": list(PROBE_MODELS), "n_per_cell": N_PER_CELL,
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


def coding_value(text, item_ids):
    """Parse one rater batch under the FROZEN recognition rubric.

    The rubric returns, per item, a sorted unique `families` subset plus
    `ambiguous` and `refusal` flags - not a boolean. Strict, as in
    recognition_r1: wrong, duplicate, missing or reordered ids fail the whole
    batch rather than being partially salvaged.

    Returns a list of (families, ambiguous, refusal) per item, in input order.
    """
    def unique(pairs):
        if len({k for k, _ in pairs}) != len(pairs):
            raise ValueError("Duplicate JSON key")
        return dict(pairs)
    text = text.strip()
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
        fams = row.get("families")
        if (not isinstance(fams, list)
                or any(f not in FAMILIES for f in fams)
                or list(fams) != sorted(set(fams))):
            raise ValueError("Invalid families list")
        if not isinstance(row.get("ambiguous"), bool) or not isinstance(row.get("refusal"), bool):
            raise ValueError("Missing ambiguous/refusal flag")
        out.append((tuple(fams), row["ambiguous"], row["refusal"]))
    return out


def collect(replay=False, root=LEDGER, folder=FOLDER, responder=network):
    root, folder = Path(root), Path(folder)
    release = read_checked(folder / "release.json")
    batch = read_checked(folder / "requests.json")
    verify(release, root)
    if digest(batch) != release["jobs_sha256"]:
        raise BudgetStop("Changed requests")
    manifest = {"release_sha256": digest(release), "jobs_sha256": digest(batch)}
    save(folder / "execution_manifest.json", manifest)

    probes = [j for j in batch if j["kind"] == "probe"]
    with Ledger(root, release) as ledger:
        if ledger.state["pending"]:
            raise BudgetStop("Unresolved dispatch")
        seen = set()

        def dispatch(job):
            record, _ = ledger.dispatch(job, digest(manifest), responder, replay)
            if charge(record["raw"], job, False) != record["accounted_nano"]:
                raise BudgetStop("Cost replay mismatch")
            seen.add(digest(job["slot"]))
            return record["parsed"]

        answers, probe_rows = {}, []
        for i, job in enumerate(probes, 1):
            answers[job["slot"]] = dispatch(job)
            probe_rows.append({**job["cell"], "slot": job["slot"]})
            if i % 50 == 0:
                print(json.dumps({"probes": i, "of": len(probes),
                                  "accounted_usd": ledger.state["recognition_nano"] / 1e9}),
                      flush=True)
        save(folder / "probe_rows.json", probe_rows)

        # Coding requests were reserved against a worst-case placeholder; rebuild
        # them with the real answers and dispatch under the same frozen slots.
        real = coding_jobs(answers)
        frozen = {j["slot"]: j for j in batch if j["kind"] == "coding"}
        coded = {}
        for i, job in enumerate(real, 1):
            if job["slot"] not in frozen:
                raise BudgetStop(f"Unmanifested coding slot {job['slot']}")
            reserved = frozen[job["slot"]]
            if job["request"]["model"] != reserved["request"]["model"]:
                raise BudgetStop("Coding model changed after freeze")
            if job["reserved_nano"] > reserved["reserved_nano"]:
                raise BudgetStop("Coding body exceeds its reservation")
            job["reserved_nano"] = reserved["reserved_nano"]
            labels = coding_value(dispatch(job), job["item_ids"])
            for slot, label in zip(job["cell"]["slots"], labels):
                coded.setdefault(slot, []).append(label)
            if i % 20 == 0:
                print(json.dumps({"coding": i, "of": len(real),
                                  "accounted_usd": ledger.state["recognition_nano"] / 1e9}),
                      flush=True)

        result = analyze(probe_rows, coded)
        save(folder / "coded.json", coded)
        if set(ledger.state["reservations"]) - set(release["historical_keys"]) != seen:
            raise BudgetStop("Unmanifested dispatch")
        result.update(calls=len(seen), accounted_nano=ledger.state["recognition_nano"],
                      provider_totals_nano=ledger.state["providers"],
                      release_sha256=digest(release))
        save(folder / "results.json", result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("prepare", "run"))
    parser.add_argument("--yes", action="store_true")
    args = parser.parse_args()
    if args.command == "prepare":
        release, batch = prepare(True)
        probes = sum(1 for j in batch if j["kind"] == "probe")
        print(json.dumps({"maximum_usd": release["recognition_cap_nano"] / 1e9,
                          "probes": probes, "coding_calls": len(batch) - probes,
                          "models": list(PROBE_MODELS),
                          "cells": len(FAMILIES) * len(FORMS) * len(PROBE_MODELS)}))
    else:
        if not args.yes:
            raise BudgetStop("Explicit execution flag required")
        print(json.dumps(collect()))


if __name__ == "__main__":
    main()
