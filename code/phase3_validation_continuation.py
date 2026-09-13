"""Linked validation continuation on the SAME ledger; never retries old slots."""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from phase3_budget import Budget, BudgetStop, canonical, digest, read_checked, token_cost_nano, write_once
from phase3_provider_budget import CAPS, check_caps, provider

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "data/raw/phase3_20260913_budget"
FAILED_SLOT = "resolution_consultation_r2"


class Continuation(Budget):
    def __init__(self, root, reconciliation):
        self.reconciliation = reconciliation
        super().__init__(root)

    def audit(self):
        state = super().audit()  # original stage/$10 limits remain stricter here
        rec = self.reconciliation
        for relative, expected in rec["preserved_files"].items():
            path = Path(relative)
            if path.is_absolute() or ".." in path.parts:
                raise BudgetStop("Invalid preserved path")
            if hashlib.sha256((self.root / path).read_bytes()).hexdigest() != expected:
                raise BudgetStop("Preserved historical ledger changed")
        accepted = rec["accepted_failure_key"]
        if (rec["accepted_failure_slot"] != FAILED_SLOT or accepted != digest(FAILED_SLOT)
                or accepted not in state["failed"]):
            raise BudgetStop("Expected preserved failure absent")
        record = read_checked(self.root / "records" / (accepted + ".json"))
        settlement = read_checked(self.root / "settlements" / (accepted + ".json"))
        if (record["raw"]["stop_reason"] != "max_tokens" or record["error"]["type"] != "ValueError"
                or record["accounted_nano"] != rec["retained_charge_nano"]
                or settlement["status"] != "failed"):
            raise BudgetStop("Failure disposition differs")
        by_provider = dict.fromkeys(CAPS, 0)
        records = {p.stem for p in (self.root / "records").glob("*.json")}
        settled = {p.stem for p in (self.root / "settlements").glob("*.json")}
        if records - set(state["reservations"]) or records != settled:
            raise BudgetStop("Orphan/missing response or settlement; reconcile before dispatch")
        for key, intent in state["reservations"].items():
            charge = intent["reserved_nano"]
            if key in settled:
                response = read_checked(self.root / "records" / (key + ".json"))
                paid = read_checked(self.root / "settlements" / (key + ".json"))
                if (paid["response_sha256"] != digest(response)
                        or response["manifest_sha256"] != intent["manifest_sha256"]
                        or response["accounted_nano"] != paid["charged_nano"]):
                    raise BudgetStop("Broken response/manifest/charge link")
                charge = paid["charged_nano"] if paid["status"] == "complete" else max(charge, paid["charged_nano"])
            by_provider[provider(intent["request"])] += charge
        check_caps(by_provider, state["by_stage_nano"])
        return {**state, "historical_failed": state["failed"],
                "failed": [key for key in state["failed"] if key != accepted],
                "by_provider_nano": by_provider}

    def reserve(self, slot, stage, request, upper_bound_nano, manifest_sha256):
        if not slot.startswith(("candidate_r2/", "equivalence_r3/")):
            raise BudgetStop("Only the new designated candidate/review slots are allowed")
        state = self.audit()
        check_caps(state["by_provider_nano"], state["by_stage_nano"],
                   [{"request": request, "stage": stage, "reserved_nano": upper_bound_nano}])
        return super().reserve(slot, stage, request, upper_bound_nano, manifest_sha256)

    def settle(self, key, charged_nano, response_sha256, *, status="complete"):
        # The immutable response is written before settlement. Check its identity
        # while temporarily permitting this single response-without-settlement.
        # super().settle calls audit before writing, so implement the small write
        # explicitly and then perform the full audit with all links present.
        if self.fd is None or type(charged_nano) is not int or charged_nano < 0:
            raise BudgetStop("Invalid settlement")
        if status not in ("complete", "failed", "unknown"):
            raise BudgetStop("Invalid status")
        intents = {p.stem: p for p in (self.root / "reservations").glob("*.json")}
        if key not in intents:
            raise BudgetStop("Unknown reservation")
        intent = read_checked(intents[key])
        response = read_checked(self.root / "records" / (key + ".json"))
        if digest(response) != response_sha256 or response["accounted_nano"] != charged_nano:
            raise BudgetStop("Settlement does not match response")
        write_once(self.root / "settlements" / (key + ".json"),
                   {"reservation_sha256": digest(intent), "charged_nano": charged_nano,
                    "response_sha256": response_sha256, "status": status})
        return self.audit()


def network(request):
    if provider(request) == "openai":
        url = "https://api.openai.com/v1/chat/completions"
        headers = {"Authorization": "Bearer " + os.environ["OPENAI_API_KEY"]}
    else:
        url = "https://api.anthropic.com/v1/messages"
        headers = {"x-api-key": os.environ["ANTHROPIC_API_KEY"], "anthropic-version": "2023-06-01"}
    headers["Content-Type"] = "application/json"
    with urlopen(Request(url, data=canonical(request), headers=headers, method="POST"), timeout=300) as handle:
        return json.loads(handle.read())


def parse(raw, job):
    request = job["request"]
    is_openai = provider(request) == "openai"
    usage = raw.get("usage", {})
    keys = ("prompt_tokens", "completion_tokens") if is_openai else ("input_tokens", "output_tokens")
    maximum = request["max_completion_tokens"] if is_openai else request["max_tokens"]
    if raw.get("model") != request["model"] or any(type(usage.get(k)) is not int or usage[k] < 0 for k in keys):
        raise ValueError("Wrong model or missing usage")
    if usage[keys[0]] > job["input_token_bound"] or usage[keys[1]] > maximum:
        raise ValueError("Usage exceeds reservation assumptions")
    if is_openai:
        choices = raw.get("choices", [])
        if len(choices) != 1 or choices[0].get("finish_reason") != "stop":
            raise ValueError("Incomplete output")
        text = choices[0]["message"]["content"]
    else:
        if (raw.get("stop_reason") != "end_turn" or any(part.get("type") != "text" for part in raw.get("content", []))
                or usage.get("cache_creation_input_tokens", 0) or usage.get("cache_read_input_tokens", 0)):
            raise ValueError("Incomplete output or unsupported content/cache charge")
        text = "".join(part["text"] for part in raw["content"])
    text = text.strip()
    if text.startswith("```json\n") and text.endswith("```"):
        text = text[8:-3].strip()
    value = json.loads(text)
    if job["kind"] == "generation":
        if (set(value) != {"stimulus", "correspondence", "unresolved_elements"}
                or not isinstance(value["stimulus"], dict) or not value["stimulus"]
                or any(not isinstance(k, str) or not isinstance(v, str) or not v.strip() for k, v in value["stimulus"].items())):
            raise ValueError("Invalid candidate schema")
        arrays = ("correspondence", "unresolved_elements")
        if set(value["stimulus"]) != set(job["required_fields"]):
            raise ValueError("Candidate omitted or added a required wording field")
    else:
        if (set(value) != {"verdict", "blocking_mismatches", "nonblocking_limits", "required_changes"}
                or value["verdict"] not in ("accept", "revise", "reject")):
            raise ValueError("Invalid review schema")
        arrays = ("blocking_mismatches", "nonblocking_limits", "required_changes")
        if value["verdict"] == "accept" and (value["blocking_mismatches"] or value["required_changes"]):
            raise ValueError("Inconsistent acceptance")
    if any(not isinstance(value[k], list) or not all(isinstance(x, str) for x in value[k]) for k in arrays):
        raise ValueError("Invalid text array")
    return value


def execute(plan, reconciliation, *, root=LEDGER, responder=network, replay=False):
    jobs = plan["jobs"]
    if len({job["slot"] for job in jobs}) != len(jobs):
        raise BudgetStop("Duplicate job slots")
    results, new_calls = [], 0
    with Continuation(root, reconciliation) as budget:
        state = budget.audit()
        if state["pending"] or state["failed"]:
            raise BudgetStop("A new unresolved failure blocks continuation")
        missing = [job for job in jobs if digest(job["slot"]) not in state["reservations"]]
        check_caps(state["by_provider_nano"], state["by_stage_nano"], missing)
        for job in jobs:
            key = digest(job["slot"])
            record_path = Path(root) / "records" / (key + ".json")
            if key in state["reservations"]:
                intent = state["reservations"][key]
                if intent["request"] != job["request"] or intent["manifest_sha256"] != digest(plan):
                    raise BudgetStop("Replay manifest/request mismatch")
                record = read_checked(record_path)
                if parse(record["raw"], job) != record["parsed"]:
                    raise BudgetStop("Replay parse mismatch")
            else:
                if replay:
                    raise BudgetStop("Missing call during offline replay")
                budget.reserve(job["slot"], job["stage"], job["request"], job["reserved_nano"], digest(plan))
                raw, parsed, error = None, None, None
                try:
                    raw = responder(job["request"])
                    parsed = parse(raw, job)
                except Exception as exc:
                    error = {"type": type(exc).__name__, "status": exc.code if isinstance(exc, HTTPError) else None}
                usage = (raw or {}).get("usage", {})
                is_openai = provider(job["request"]) == "openai"
                keys = ("prompt_tokens", "completion_tokens") if is_openai else ("input_tokens", "output_tokens")
                known = all(type(usage.get(k)) is int and usage[k] >= 0 for k in keys)
                charge = token_cost_nano(usage[keys[0]], usage[keys[1]], "2.50" if is_openai else "3", "15") if known else job["reserved_nano"]
                if error:
                    charge = max(charge, job["reserved_nano"])
                record = {"raw": raw, "parsed": parsed, "error": error, "accounted_nano": charge,
                          "manifest_sha256": digest(plan), "timestamp": datetime.now(timezone.utc).isoformat()}
                write_once(record_path, record)
                budget.settle(key, charge, digest(record), status="failed" if error else "complete")
                new_calls += 1
                if error:
                    raise BudgetStop("New failure preserved; no automatic retry")
            results.append(record)
            print(json.dumps({"slot": job["slot"], "complete": True}), flush=True)
    return results, new_calls
