"""Write-once, single-attempt transport for the prospective Phase 2 confirmation."""
from __future__ import annotations

import asyncio
import hashlib
import json
import os
from pathlib import Path
from datetime import datetime, timezone

MODEL = "gpt-5.4-mini-2026-03-17"
CAP_NANO = 30_000_000_000
PRIOR_PHASE2_NANO = 4_150_840_650
TOTAL_CAP_NANO = 100_000_000_000
assert PRIOR_PHASE2_NANO + CAP_NANO <= TOTAL_CAP_NANO
MAX_TOKENS = 600


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def now():
    return datetime.now(timezone.utc).isoformat()


def write_once(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    envelope = {"sha256": digest(value), "payload": value}
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("x", encoding="utf-8", newline="\n") as fh:
        json.dump(envelope, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
        fh.flush()
        os.fsync(fh.fileno())
    # Windows rename refuses an existing destination; explicitly guard elsewhere.
    if path.exists():
        raise FileExistsError(path)
    tmp.rename(path)


def read_record(path):
    envelope = json.loads(Path(path).read_text(encoding="utf-8"))
    value = envelope["payload"]
    if digest(value) != envelope["sha256"]:
        raise ValueError(f"Record checksum mismatch: {path}")
    return value


def cost_nano(input_tokens, output_tokens):
    # Full uncached input price, 10% allowance, round up to nanodollar.
    return ((int(input_tokens) * 750 + int(output_tokens) * 4500) * 11 + 9) // 10


def reservation(request):
    # UTF-8 bytes bound byte-BPE text tokens. Add ample protocol framing margin.
    bound = sum(len(m["content"].encode("utf-8")) for m in request["messages"]) + 512
    return bound, cost_nano(bound, request["max_completion_tokens"])


class StopRun(RuntimeError):
    pass


class Ledger:
    def __init__(self, root, manifest_hash, *, mock=False, responder=None):
        self.root = Path(root)
        self.manifest_hash = manifest_hash
        self.mock = mock
        self.responder = responder
        self.client = None
        self.sem = asyncio.Semaphore(6)
        self.cap = CAP_NANO
        self.charged = 0
        self.results = {}
        self.halted = False
        self.n_new = 0
        self.root.mkdir(parents=True, exist_ok=True)
        self.lock = self.root / "execution.lock"
        self.lock_fd = os.open(self.lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        os.write(self.lock_fd, canonical({"pid": os.getpid(), "manifest": manifest_hash, "time": now()}))
        try:
            self._audit()
        except BaseException:
            self.close()
            raise

    def _audit(self):
        intents = {p.stem: p for p in (self.root / "dispatches").glob("*.json")}
        records = {p.stem: p for p in (self.root / "records").glob("*.json")}
        if records.keys() - intents.keys():
            raise StopRun("Orphan response: inspect provenance before continuation")
        if list(self.root.rglob("*.tmp")):
            raise StopRun("Unfinished atomic write: inspect before continuation")
        for key, path in intents.items():
            intent = read_record(path)
            if intent["manifest_hash"] != self.manifest_hash or intent["mock"] != self.mock:
                raise StopRun("Mixed manifest or mock/live ledger")
            if key not in records:
                raise StopRun(f"Unresolved dispatch {key}; no automatic retry")
            result = read_record(records[key])
            if result["intent_hash"] != digest(intent):
                raise StopRun("Response/intent mismatch")
            self.charged += result["charged_nano"]
            self.results[key] = result
            if result["error"] or result.get("integrity_error"):
                self.halted = True
        if self.charged > self.cap:
            raise StopRun("Existing ledger exceeds cap")

    def close(self):
        if self.client is not None:
            # Async client closed explicitly by caller before this method.
            self.client = None
        if getattr(self, "lock_fd", None) is not None:
            os.close(self.lock_fd)
            self.lock_fd = None
            self.lock.unlink()

    async def complete(self, slot, messages, seed, meta):
        request = {"model": MODEL, "messages": messages, "temperature": 1.0,
                   "max_completion_tokens": MAX_TOKENS, "reasoning_effort": "none",
                   "seed": seed, "service_tier": "default"}
        key = digest(slot)
        identity = {"slot": slot, "request": request, "meta": meta}
        if key in self.results:
            result = self.results[key]
            if result["identity_hash"] != digest(identity):
                raise StopRun("Replay request differs from frozen recorded request")
            return result
        async with self.sem:
            if self.halted:
                raise StopRun("Transport/integrity failure stopped further dispatch")
            input_bound, reserved = reservation(request)
            if self.charged + reserved > self.cap:
                self.halted = True
                raise StopRun("Confirmation $30 cap: next request reservation would not fit")
            intent = {**identity, "identity_hash": digest(identity),
                      "manifest_hash": self.manifest_hash, "mock": self.mock,
                      "input_token_bound": input_bound, "reserved_nano": reserved,
                      "timestamp": now()}
            write_once(self.root / "dispatches" / f"{key}.json", intent)
            self.charged += reserved  # no await between check and reservation
            raw, error = None, None
            try:
                if self.mock:
                    raw = self.responder(request, meta) if self.responder else mock_response(request, meta)
                    await asyncio.sleep(0)
                else:
                    if self.client is None:
                        from openai import AsyncOpenAI
                        # Pin endpoint: never follow inherited custom endpoint configuration.
                        self.client = AsyncOpenAI(base_url="https://api.openai.com/v1",
                                                  max_retries=0, timeout=90.0)
                    response = await self.client.chat.completions.create(**request)
                    raw = response.model_dump()
            except Exception as exc:
                # Exception text can contain credentials; save only safe typed metadata.
                error = {"type": type(exc).__name__,
                         "status_code": getattr(exc, "status_code", None)}
            usage = (raw or {}).get("usage") or {}
            valid_usage = all(isinstance(usage.get(x), int) and usage[x] >= 0
                              for x in ("prompt_tokens", "completion_tokens"))
            charged = cost_nano(usage["prompt_tokens"], usage["completion_tokens"]) if valid_usage else reserved
            integrity_error = None
            if raw and raw.get("model") != MODEL:
                integrity_error = "unexpected_model_snapshot"
            if valid_usage and (usage["prompt_tokens"] > input_bound or usage["completion_tokens"] > MAX_TOKENS):
                integrity_error = "usage_exceeds_reservation_bound"
            result = {"slot": slot, "meta": meta, "identity_hash": digest(identity),
                      "intent_hash": digest(intent), "timestamp": now(), "response": raw,
                      "error": error, "integrity_error": integrity_error,
                      "charged_nano": charged, "usage_known": valid_usage, "mock": self.mock}
            write_once(self.root / "records" / f"{key}.json", result)
            self.charged += charged - reserved
            self.results[key] = result
            self.n_new += 1
            if error or integrity_error:
                self.halted = True
            if len(self.results) % 50 == 0:
                print(json.dumps({"responses": len(self.results), "accounted_usd": self.charged / 1e9,
                                  "mock": self.mock}), flush=True)
            return result


def mock_response(request, meta):
    labels = meta["labels"]
    label = labels[int(digest(request), 16) % 2]
    text = f"DECISION: {label}\nREASONING: Offline plumbing response."
    if meta["stage"] == "complex":
        text = (f"ACTION: argue\nAMENDMENT: NONE\nADOPT: NONE\nSHARE: NONE\n"
                f"REASONING: Offline plumbing response.\nVOTE: {label}")
    return {"id": "mock-" + digest(request), "model": MODEL,
            "choices": [{"finish_reason": "stop", "message": {"content": text, "refusal": None}}],
            "usage": {"prompt_tokens": 1200, "completion_tokens": 100}, "mock": True}
