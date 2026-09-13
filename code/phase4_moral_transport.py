"""Prospective Phase 4 transport: inherited immutable ledger audit, 16 KiB text.

Provider model/usage/finish validation and dispatch are copied from the frozen
phase3_recognition_run.py. Only the text kind/limit changes; no old parser is
patched, no raw response is rewritten, and no retry behavior changes.
"""
from datetime import datetime, timezone
import os
from urllib.error import HTTPError
from phase3_recognition_run import Ledger as HistoricalLedger, MODELS, charge
from phase3_budget import BudgetStop, canonical, digest, read_checked, write_once

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
    if job['kind'] != 'moral_text':
        raise ValueError('Unexpected extended-text job kind')
    if (not isinstance(text, str) or not text.strip() or len(text.encode('utf-8')) > 16384
            or any(ord(ch) < 32 and ch not in '\n\r\t' for ch in text)):
        raise ValueError('Empty, oversized or invalid moral text')
    return text


class Ledger(HistoricalLedger):
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
