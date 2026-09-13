"""Linked, write-once recognition collection on the existing Phase 3 ledger."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import random
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from phase3_budget import BudgetStop, POLICY, canonical, digest, read_checked, write_once
from phase3_recognition import PACKAGE, ROOT, RATERS, JUDGE, PRICES, rater_request, valid_probe_text, verify_requests
from phase3_recognition_discussion import discussion_request, validate_rating
from phase3_variant_round import save

LEDGER = ROOT / "data/raw/phase3_20260913_budget"
RUN = PACKAGE / "execution"
MODELS = {JUDGE: "anthropic", RATERS[0]: "anthropic", RATERS[1]: "openai", "gpt-5.4-2026-03-05": "openai"}


def parse(raw, job):
    req = job["request"]
    is_openai = MODELS[req["model"]] == "openai"
    keys = ("prompt_tokens", "completion_tokens") if is_openai else ("input_tokens", "output_tokens")
    usage = raw.get("usage", {})
    if raw.get("model") != req["model"] or any(type(usage.get(k)) is not int or usage[k] < 0 for k in keys):
        raise ValueError("Model or usage mismatch")
    maximum = req["max_completion_tokens"] if is_openai else req["max_tokens"]
    if usage[keys[0]] > job["input_token_bound"] or usage[keys[1]] > maximum:
        raise ValueError("Usage exceeds frozen reservation")
    if is_openai:
        choices = raw.get("choices", [])
        if len(choices) != 1 or choices[0].get("finish_reason") != "stop":
            raise ValueError("Incomplete output")
        text = choices[0]["message"]["content"]
    else:
        if (raw.get("stop_reason") != "end_turn" or not raw.get("content")
                or any(b.get("type") != "text" for b in raw["content"])
                or usage.get("cache_creation_input_tokens", 0) or usage.get("cache_read_input_tokens", 0)):
            raise ValueError("Incomplete output or unsupported cache/content")
        text = "".join(b["text"] for b in raw["content"])
    if job["kind"] == "probe":
        if not valid_probe_text(text):
            raise ValueError("Empty, oversized or invalid probe text")
        return text  # exact answer; do not strip, summarize or overwrite it
    text = text.strip()
    if text.startswith("```json\n") and text.endswith("```"):
        text = text[8:-3].strip()
    value = json.loads(text)
    if not isinstance(value, dict) or set(value) != {"ratings"} or not isinstance(value["ratings"], list):
        raise ValueError("Invalid coding schema")
    if [r.get("id") for r in value["ratings"]] != job["item_ids"]:
        raise ValueError("Missing, duplicate, reordered or extra coding IDs")
    for rating in value["ratings"]:
        core = dict(rating)
        if job["kind"] == "discussion":
            reason = core.pop("reason", None)
            if not isinstance(reason, str) or not reason.strip():
                raise ValueError("Discussion reason absent")
        validate_rating(core, rating["id"])
    return value["ratings"]


def charge(raw, job, failed):
    from phase3_budget import token_cost_nano
    usage = (raw or {}).get("usage", {})
    keys = ("prompt_tokens", "completion_tokens") if MODELS[job["request"]["model"]] == "openai" else ("input_tokens", "output_tokens")
    known = all(type(usage.get(k)) is int and usage[k] >= 0 for k in keys)
    amount = token_cost_nano(usage[keys[0]], usage[keys[1]], *PRICES[job["request"]["model"]]) if known else job["reserved_nano"]
    return max(amount, job["reserved_nano"]) if failed else amount


def network(request):
    if MODELS[request["model"]] == "openai":
        endpoint = "https://api.openai.com/v1/chat/completions"
        headers = {"Authorization": "Bearer " + os.environ["OPENAI_API_KEY"]}
    else:
        endpoint = "https://api.anthropic.com/v1/messages"
        headers = {"x-api-key": os.environ["ANTHROPIC_API_KEY"], "anthropic-version": "2023-06-01"}
    headers["Content-Type"] = "application/json"
    with urlopen(Request(endpoint, data=canonical(request), headers=headers, method="POST"), timeout=60) as response:
        return json.loads(response.read())


class Ledger:
    """Same lock, policy and directories; new allocation is an explicit supplement.

    The complete worst-case schedule fits at entry. Each dispatch records intent
    before network. Audit once under the exclusive lock, update local totals on
    settlement, and audit the complete disk state again on exit.
    """
    def __init__(self, root, release):
        self.root, self.release = Path(root), release
        self.lock = self.root / "execution.lock"
        self.fd = os.open(self.lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        os.write(self.fd, canonical({"pid": os.getpid(), "release": digest(release)}))
        try:
            self.state = self.audit()
        except BaseException:
            self.close()
            raise

    def close(self):
        if self.fd is not None:
            os.close(self.fd)
            self.fd = None
            self.lock.unlink()

    def __enter__(self):
        return self

    def __exit__(self, kind, value, trace):
        try:
            if kind is None:
                self.audit()
        finally:
            self.close()

    def audit(self):
        if sum(x["reserved_nano"] for x in self.release["slots"].values()) > self.release["recognition_cap_nano"]:
            raise BudgetStop("Complete schedule exceeds its allocation")
        if read_checked(self.root / "policy.json") != POLICY:
            raise BudgetStop("Original policy changed")
        for relative, sha in self.release["preserved_files"].items():
            path = Path(relative)
            if path.is_absolute() or ".." in path.parts or hashlib.sha256((self.root / path).read_bytes()).hexdigest() != sha:
                raise BudgetStop("Historical ledger changed")
        reservations = {p.stem: read_checked(p) for p in (self.root / "reservations").glob("*.json")}
        records = {p.stem: p for p in (self.root / "records").glob("*.json")}
        settlements = {p.stem: read_checked(p) for p in (self.root / "settlements").glob("*.json")}
        if records.keys() - reservations.keys() or records.keys() != settlements.keys():
            raise BudgetStop("Orphan/missing record or settlement")
        providers = {"anthropic": 0, "openai": 0}
        pending, failures, spent = [], [], 0
        for key, intent in reservations.items():
            if key != digest(intent["slot"]) or intent["request"]["model"] not in MODELS:
                raise BudgetStop("Invalid reservation identity/model")
            amount = intent["reserved_nano"]
            if type(amount) is not int or amount <= 0:
                raise BudgetStop("Invalid amount")
            historical = key in self.release["historical_keys"]
            if not historical:
                cap = self.release["slots"].get(intent["slot"])
                if (cap is None or intent["stage"] != "recognition" or intent.get("release_sha256") != digest(self.release)
                        or amount != cap["reserved_nano"] or intent["request"]["model"] != cap["model"]):
                    raise BudgetStop("Unreleased slot, model, allocation or source")
            if key in settlements:
                paid, record = settlements[key], read_checked(records[key])
                if (paid["reservation_sha256"] != digest(intent) or paid["response_sha256"] != digest(record)
                        or record["manifest_sha256"] != intent["manifest_sha256"]
                        or record["accounted_nano"] != paid["charged_nano"]
                        or type(paid["charged_nano"]) is not int or paid["charged_nano"] < 0
                        or paid["status"] not in ("complete", "failed")):
                    raise BudgetStop("Broken request/response/cost links")
                amount = paid["charged_nano"] if paid["status"] == "complete" else max(amount, paid["charged_nano"])
                if not historical and (paid["status"] != "complete" or record["error"] or amount > intent["reserved_nano"]):
                    failures.append(key)
            else:
                pending.append(key)
            providers[MODELS[intent["request"]["model"]]] += amount
            if not historical:
                spent += amount
        if (spent > self.release["recognition_cap_nano"]
                or any(providers[p] > self.release["provider_caps_nano"][p] for p in providers)
                or sum(providers.values()) + POLICY["prior_package_nano"] > POLICY["package_cap_nano"]):
            raise BudgetStop("Allocation/provider/package cap exceeded")
        projected = dict(providers)
        for slot, cap in self.release["slots"].items():
            if digest(slot) not in reservations:
                projected[MODELS[cap["model"]]] += cap["reserved_nano"]
        if (any(projected[p] > self.release["provider_caps_nano"][p] for p in projected)
                or sum(projected.values()) + POLICY["prior_package_nano"] > POLICY["package_cap_nano"]):
            raise BudgetStop("Full remaining schedule exceeds provider/package caps")
        return {"reservations": reservations, "providers": providers, "recognition_nano": spent,
                "pending": pending, "failed": failures}

    def dispatch(self, job, manifest_sha, responder, replay):
        key = digest(job["slot"])
        if self.state["pending"] or self.state["failed"]:
            raise BudgetStop("Unresolved dispatch blocks continuation")
        path = self.root / "records" / (key + ".json")
        if key in self.state["reservations"]:
            old = self.state["reservations"][key]
            if old["request"] != job["request"] or old["manifest_sha256"] != manifest_sha:
                raise BudgetStop("Changed request/manifest on resume")
            result = read_checked(path)
            if result["parsed"] != parse(result["raw"], job):
                raise BudgetStop("Replay parse mismatch")
            return result, False
        if replay:
            raise BudgetStop("Missing slot in offline replay")
        cap = self.release["slots"].get(job["slot"])
        if (cap is None or job["reserved_nano"] != cap["reserved_nano"]
                or job["request"]["model"] != cap["model"]
                or job["input_token_bound"] != cap["input_token_bound"]
                or job["kind"] != cap["kind"]
                or job["request"].get("max_tokens", job["request"].get("max_completion_tokens")) != cap["max_output"]
                or (cap.get("request_sha256") and digest(job["request"]) != cap["request_sha256"])):
            raise BudgetStop("Slot outside complete reservation")
        intent = {"slot": job["slot"], "stage": "recognition", "request": job["request"],
                  "reserved_nano": job["reserved_nano"], "manifest_sha256": manifest_sha,
                  "release_sha256": digest(self.release)}
        write_once(self.root / "reservations" / (key + ".json"), intent)
        self.state["reservations"][key] = intent
        raw, parsed, error = None, None, None
        try:
            raw = responder(job["request"])
            parsed = parse(raw, job)
        except Exception as exc:
            error = {"type": type(exc).__name__, "status": exc.code if isinstance(exc, HTTPError) else None}
        amount = charge(raw, job, error is not None)
        result = {"raw": raw, "parsed": parsed, "error": error, "accounted_nano": amount,
                  "manifest_sha256": manifest_sha, "timestamp": datetime.now(timezone.utc).isoformat()}
        write_once(path, result)
        write_once(self.root / "settlements" / (key + ".json"), {"reservation_sha256": digest(intent),
                   "charged_nano": amount, "response_sha256": digest(result), "status": "failed" if error else "complete"})
        self.state["recognition_nano"] += amount
        self.state["providers"][MODELS[job["request"]["model"]]] += amount
        if error or amount > job["reserved_nano"]:
            with (self.root / "failures.jsonl").open("ab") as handle:
                handle.write(canonical({"slot": job["slot"], "record_sha256": digest(result),
                                        "error": error, "accounted_nano": amount}) + b"\n")
                handle.flush()
                os.fsync(handle.fileno())
            self.state["failed"].append(key)
            raise BudgetStop("Failure preserved at full reservation; no retry")
        return result, True


def prepare(persist=True):
    from verify_phase3_structural_review import verify
    verify_requests()
    prior = verify()
    full = read_checked(PACKAGE / "discussion_cost_plan.json")
    initial = read_checked(PACKAGE / "cost_plan.json")
    slots = {j["slot"]: {"model": JUDGE, "reserved_nano": j["reserved_nano"], "kind": "probe",
                        "input_token_bound": j["input_token_bound"], "max_output": 128,
                        "request_sha256": digest(j["request"])} for j in initial["jobs"]}
    for kind, rows in (("coding", initial["coding"]), ("discussion", full["discussion"])):
        for index, row in enumerate(rows):
            bound = row["reserved_nano_per_call"] if kind == "coding" else row["maximum_nano"] // 50
            for batch in range(50):
                slots[f"recognition_r1/{kind}/{index}/{batch:02}"] = {"model": row["model"], "reserved_nano": bound,
                        "kind": kind, "max_output": 1024, "input_token_bound": row["input_token_bound"]}
    if sum(x["reserved_nano"] for x in slots.values()) != 14067432500 or len(slots) != 700:
        raise BudgetStop("Whole reviewed schedule changed")
    paths = [Path(__file__), ROOT / "code/phase3_recognition.py", ROOT / "code/phase3_recognition_discussion.py",
             ROOT / "code/phase3_recognition_analysis.py", RUN / "RELEASE.md", PACKAGE / "requests.json",
             PACKAGE / "cost_plan.json", PACKAGE / "discussion_cost_plan.json"]
    release = {"id": "recognition_execution_r1", "recognition_cap_nano": full["complete_reserved_nano"],
               "provider_caps_nano": {"anthropic": 15000000000, "openai": 30000000000},
               "slots": slots, "prior_accounted_nano": prior["phase3_accounted_nano"],
               "historical_keys": sorted(p.stem for p in (LEDGER / "records").glob("*.json")),
               "preserved_files": {p.relative_to(LEDGER).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in LEDGER.rglob("*.json")},
               "source_sha256": {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}}
    if len(release["historical_keys"]) != 48 or len(release["preserved_files"]) != 145:
        raise BudgetStop("Unexpected pre-collection evidence")
    if persist:
        save(RUN / "release.json", release)
    return release


def verify_release():
    verify_requests()
    release = read_checked(RUN / "release.json")
    for path, sha in release["source_sha256"].items():
        if hashlib.sha256((ROOT / path).read_bytes()).hexdigest() != sha:
            raise BudgetStop("Frozen runtime changed")
    with Ledger(LEDGER, release) as ledger:
        # Account for the complete still-reserved workload, not only the next call.
        projected = dict(ledger.state["providers"])
        for slot, cap in release["slots"].items():
            if digest(slot) not in ledger.state["reservations"]:
                projected[MODELS[cap["model"]]] += cap["reserved_nano"]
        if (any(projected[p] > release["provider_caps_nano"][p] for p in projected)
                or sum(projected.values()) + POLICY["prior_package_nano"] > POLICY["package_cap_nano"]):
            raise BudgetStop("Whole remaining workload cannot fit")
    return release


def execute(jobs, release, kind, *, root=LEDGER, responder=network, replay=False):
    if len({j["slot"] for j in jobs}) != len(jobs):
        raise BudgetStop("Duplicate manifest slots")
    stage = {"release_sha256": digest(release), "jobs": jobs}
    # Dynamic coding requests bind exact saved probe outputs, never unseen guesses.
    if root == LEDGER:
        save(RUN / (kind + "_manifest.json"), stage)
    stage_hash = digest(stage)
    results, calls = [], 0
    with Ledger(root, release) as ledger:
        for i, job in enumerate(jobs):
            result, called = ledger.dispatch(job, stage_hash, responder, replay)
            results.append(result)
            calls += int(called)
            if (i+1) % 10 == 0 or i+1 == len(jobs):
                print(json.dumps({"stage": kind, "complete": i+1, "total": len(jobs), "new_calls": calls,
                                  "screening_usd": ledger.state["recognition_nano"] / 1e9}), flush=True)
    return results


def item_id(slot):
    return digest(slot)[:16]


def collect(replay=False, *, root=LEDGER, responder=network, test_release=None):
    if root == LEDGER and test_release is not None:
        raise BudgetStop("Test release forbidden on the real ledger")
    release = verify_release() if test_release is None else test_release
    initial = read_checked(PACKAGE / "cost_plan.json")
    full = read_checked(PACKAGE / "discussion_cost_plan.json")
    jobs = [{**j, "kind": "probe"} for j in initial["jobs"]]
    probes = execute(jobs, release, "probe", root=root, responder=responder, replay=replay)
    items = [{"id": item_id(j["slot"]), "answer": r["parsed"]} for j, r in zip(jobs, probes)]
    if len(items) != 500 or len({i["id"] for i in items}) != 500:
        raise BudgetStop("Incomplete or duplicate probe set")
    coding_jobs = []
    for index, model in enumerate(RATERS):
        order = items.copy()
        random.Random(2026091307 + index).shuffle(order)
        row = initial["coding"][index]
        for start in range(0, 500, 10):
            batch = order[start:start+10]
            coding_jobs.append({"kind": "coding", "rater": index, "slot": f"recognition_r1/coding/{index}/{start//10:02}",
                                "request": rater_request(model, batch), "item_ids": [x["id"] for x in batch],
                                "input_token_bound": row["input_token_bound"], "reserved_nano": row["reserved_nano_per_call"]})
    codings = execute(coding_jobs, release, "coding", root=root, responder=responder, replay=replay)
    ratings = [{}, {}]
    for job, record in zip(coding_jobs, codings):
        for row in record["parsed"]:
            if row["id"] in ratings[job["rater"]]:
                raise BudgetStop("Duplicate coding")
            # Disk envelopes canonicalize key order. Normalize before composing
            # dependent prompts so first execution and disk replay are identical.
            ratings[job["rater"]][row["id"]] = json.loads(canonical(row))
    unresolved = [x for x in items if ratings[0][x["id"]] != ratings[1][x["id"]]
                  or ratings[0][x["id"]]["ambiguous"] or ratings[0][x["id"]]["refusal"]]
    discussions = []
    for index, model in enumerate(RATERS):
        order = sorted(unresolved, key=lambda x: x["id"])
        random.Random(2026091309 + index).shuffle(order)
        row = full["discussion"][index]
        for start in range(0, len(order), 10):
            batch = [{**x, "own_rating": ratings[index][x["id"]], "other_rating": ratings[1-index][x["id"]]} for x in order[start:start+10]]
            discussions.append({"kind": "discussion", "rater": index, "slot": f"recognition_r1/discussion/{index}/{start//10:02}",
                                "request": discussion_request(model, batch), "item_ids": [x["id"] for x in batch],
                                "input_token_bound": row["input_token_bound"], "reserved_nano": row["maximum_nano"] // 50})
    discussed = execute(discussions, release, "discussion", root=root, responder=responder, replay=replay)
    final_ratings = [dict(r) for r in ratings]
    for job, record in zip(discussions, discussed):
        for row in record["parsed"]:
            final_ratings[job["rater"]][row["id"]] = {k: v for k, v in row.items() if k != "reason"}
    from phase3_recognition_analysis import analyze
    analysis = analyze(jobs, ratings, final_ratings)
    with Ledger(root, release) as ledger:
        analysis.update({"accounted_nano": ledger.state["recognition_nano"], "provider_totals_nano": ledger.state["providers"],
                         "discussion_items": len(unresolved), "discussion_calls": len(discussions), "release_sha256": digest(release)})
    if root == LEDGER:
        save(RUN / "results.json", analysis)
    print(json.dumps(analysis), flush=True)
    return analysis


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("prepare", "run", "replay"))
    parser.add_argument("--yes", action="store_true")
    args = parser.parse_args()
    if args.command == "prepare":
        print(json.dumps({"release_sha256": digest(prepare()), "paid_calls": 0}))
    else:
        if args.command == "run" and not args.yes:
            raise BudgetStop("Explicit run flag required")
        collect(replay=args.command == "replay")
