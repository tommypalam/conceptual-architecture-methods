"""
llm_client.py — provider-agnostic async LLM call layer.

Implements spec §1.1 (LLM access, explicit temperature/max_tokens/seed),
§5.4.2 (retry-with-backoff, failures recorded not retried-in-place), and the
Appendix C per-call record shape.

Design goals:
  - One interface (`LLMClient.complete`) over OpenAI (primary), Anthropic, and
    Google, selected by model-name prefix. Adding a provider is one branch.
  - Every call returns a `CallResult` carrying the full request/response, the
    provider call id, the model-version string, timestamp, seed, and latency —
    the raw material for the immutable per-call JSON record.
  - Bounded concurrency via an internal semaphore.
  - A `MockClient` with the same interface so the whole engine can be exercised
    end-to-end with zero API calls (deterministic, seedable).

Nothing here writes files; persistence is the caller's job (see records.py-style
helpers in the runners). This keeps the transport layer pure and testable.
"""

from __future__ import annotations

import asyncio
import os
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Protocol


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


@dataclass
class Message:
    role: str          # "system" | "user" | "assistant"
    content: str


@dataclass
class CallResult:
    """Everything needed to build an immutable per-call record (Appendix C)."""
    text: str | None
    model: str
    model_version: str | None
    provider: str
    api_call_id: str | None
    timestamp_utc: str
    temperature: float
    max_tokens: int
    seed: int | None
    latency_s: float
    attempts: int
    error: str | None = None
    request_messages: list[dict[str, str]] = field(default_factory=list)
    raw_response: dict[str, Any] | None = None

    @property
    def ok(self) -> bool:
        return self.error is None and self.text is not None


class SupportsComplete(Protocol):
    async def complete(self, messages: list[Message], *, temperature: float,
                       max_tokens: int, seed: int | None) -> CallResult: ...


# --------------------------------------------------------------------------- #
# Provider routing
# --------------------------------------------------------------------------- #

def provider_for(model: str) -> str:
    m = model.lower()
    if m.startswith(("gpt", "o1", "o3", "o4")):
        return "openai"
    if m.startswith("claude"):
        return "anthropic"
    if m.startswith("gemini"):
        return "google"
    # Default to OpenAI-compatible; explicit so failures are legible.
    return "openai"


# --------------------------------------------------------------------------- #
# Real client
# --------------------------------------------------------------------------- #

class LLMClient:
    """
    Async client with bounded concurrency and retry-with-backoff.

    Retries transient API errors up to `max_retries` with exponential backoff
    (spec §5.4.2). A call that exhausts retries returns a CallResult with
    `error` set — the caller records it as data and does NOT retry in place.
    """

    def __init__(self, model: str, *, concurrency: int = 10, max_retries: int = 3,
                 base_backoff_s: float = 1.0, timeout_s: float = 60.0):
        self.model = model
        self.provider = provider_for(model)
        self.max_retries = max_retries
        self.base_backoff_s = base_backoff_s
        self.timeout_s = timeout_s   # per-attempt wall-clock cap; a hung call
                                     # fails cleanly instead of blocking gather()
        self._sem = asyncio.Semaphore(concurrency)
        self._client = None  # lazily constructed per provider
        # OpenAI param-compat flags; adapt on first 400 so a probe fixes them once.
        self._openai_uses_legacy_tokens = False   # -> max_tokens if new name rejected
        self._openai_supports_seed = True          # -> drop seed if rejected

    def _ensure_client(self):
        if self._client is not None:
            return
        if self.provider == "openai":
            from openai import AsyncOpenAI
            self._client = AsyncOpenAI()
        elif self.provider == "anthropic":
            from anthropic import AsyncAnthropic
            self._client = AsyncAnthropic()
        elif self.provider == "google":
            import google.generativeai as genai
            genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
            self._client = genai
        else:
            raise ValueError(f"Unknown provider for model {self.model!r}")

    async def _raw_call(self, messages: list[Message], temperature: float,
                        max_tokens: int, seed: int | None):
        """One attempt; returns (text, call_id, model_version, raw_dict)."""
        self._ensure_client()
        if self.provider == "openai":
            # Current OpenAI models require `max_completion_tokens`; older ones
            # only accept `max_tokens`. Use the modern name, remembering a
            # per-model fallback if the API rejects it (set on first 400).
            token_param = "max_tokens" if self._openai_uses_legacy_tokens \
                else "max_completion_tokens"
            kwargs: dict[str, Any] = dict(
                model=self.model, temperature=temperature,
                messages=[{"role": m.role, "content": m.content} for m in messages],
            )
            kwargs[token_param] = max_tokens
            if seed is not None and self._openai_supports_seed:
                kwargs["seed"] = seed
            try:
                resp = await self._client.chat.completions.create(**kwargs)
            except Exception as exc:  # noqa: BLE001
                msg = str(exc)
                retried = False
                # Flip token-param convention once, then retry this attempt.
                if "max_completion_tokens" in msg and "max_tokens" in msg \
                        and not self._openai_uses_legacy_tokens:
                    self._openai_uses_legacy_tokens = True
                    kwargs.pop("max_completion_tokens", None)
                    kwargs["max_tokens"] = max_tokens
                    retried = True
                # Drop seed if this model doesn't support it.
                if "seed" in msg and "seed" in kwargs:
                    self._openai_supports_seed = False
                    kwargs.pop("seed", None)
                    retried = True
                if not retried:
                    raise
                resp = await self._client.chat.completions.create(**kwargs)
            text = resp.choices[0].message.content
            version = getattr(resp, "model", None)
            return text, resp.id, version, resp.model_dump() if hasattr(resp, "model_dump") else None

        if self.provider == "anthropic":
            system = "\n\n".join(m.content for m in messages if m.role == "system") or None
            turns = [{"role": m.role, "content": m.content}
                     for m in messages if m.role in ("user", "assistant")]
            resp = await self._client.messages.create(
                model=self.model, max_tokens=max_tokens, temperature=temperature,
                system=system, messages=turns,
            )
            text = "".join(block.text for block in resp.content if getattr(block, "type", "") == "text")
            return text, resp.id, resp.model, resp.model_dump() if hasattr(resp, "model_dump") else None

        if self.provider == "google":
            system = "\n\n".join(m.content for m in messages if m.role == "system") or None
            user = "\n\n".join(m.content for m in messages if m.role == "user")
            model = self._client.GenerativeModel(self.model, system_instruction=system)
            resp = await model.generate_content_async(
                user, generation_config={"temperature": temperature,
                                         "max_output_tokens": max_tokens},
            )
            return resp.text, None, self.model, None

        raise ValueError(f"Unknown provider {self.provider}")

    async def complete(self, messages: list[Message], *, temperature: float,
                       max_tokens: int, seed: int | None = None) -> CallResult:
        req = [{"role": m.role, "content": m.content} for m in messages]
        start = time.monotonic()
        last_err: str | None = None
        async with self._sem:
            for attempt in range(1, self.max_retries + 1):
                try:
                    text, call_id, version, raw = await asyncio.wait_for(
                        self._raw_call(messages, temperature, max_tokens, seed),
                        timeout=self.timeout_s)
                    return CallResult(
                        text=text, model=self.model, model_version=version,
                        provider=self.provider, api_call_id=call_id,
                        timestamp_utc=utc_now_iso(), temperature=temperature,
                        max_tokens=max_tokens, seed=seed,
                        latency_s=round(time.monotonic() - start, 3),
                        attempts=attempt, error=None, request_messages=req,
                        raw_response=raw,
                    )
                except Exception as exc:  # noqa: BLE001 — recorded as data
                    last_err = f"{type(exc).__name__}: {exc}"
                    if attempt < self.max_retries:
                        await asyncio.sleep(self.base_backoff_s * (2 ** (attempt - 1)))
        return CallResult(
            text=None, model=self.model, model_version=None, provider=self.provider,
            api_call_id=None, timestamp_utc=utc_now_iso(), temperature=temperature,
            max_tokens=max_tokens, seed=seed,
            latency_s=round(time.monotonic() - start, 3),
            attempts=self.max_retries, error=last_err, request_messages=req,
        )


# --------------------------------------------------------------------------- #
# Mock client — same interface, zero API, deterministic
# --------------------------------------------------------------------------- #

class MockClient:
    """
    Drop-in replacement for LLMClient that returns deterministic canned
    responses. Lets the entire engine (simple runner + orchestrator) run
    end-to-end offline for structural verification.

    `responder(messages, seed) -> str` is a caller-supplied function that
    produces the assistant text. A default responder emits a well-formed
    DECISION/REASONING line by hashing the prompt, so parsing and aggregation
    can be exercised without any network.
    """

    def __init__(self, model: str = "mock-model", responder=None, concurrency: int = 10):
        self.model = model
        self.provider = "mock"
        self._responder = responder or self._default_responder
        self._sem = asyncio.Semaphore(concurrency)
        self.n_calls = 0

    @staticmethod
    def _default_responder(messages: list[Message], seed: int | None) -> str:
        # Deterministic pseudo-decision: pick from any "DECISION: [A | B]" hint
        # in the user turn, else echo a generic decision. Purely for plumbing.
        import re as _re
        user = next((m.content for m in reversed(messages) if m.role == "user"), "")
        opts = _re.search(r"DECISION:\s*\[([^\]]+)\]", user)
        if opts:
            choices = [c.strip() for c in opts.group(1).split("|")]
        else:
            choices = ["OPTION_A", "OPTION_B"]
        h = abs(hash((user, seed))) % len(choices)
        return f"DECISION: {choices[h]}\nREASONING: Deterministic mock response for plumbing verification."

    async def complete(self, messages: list[Message], *, temperature: float,
                       max_tokens: int, seed: int | None = None) -> CallResult:
        async with self._sem:
            self.n_calls += 1
            text = self._responder(messages, seed)
            return CallResult(
                text=text, model=self.model, model_version=f"{self.model}-mock",
                provider="mock", api_call_id=f"mock-{self.n_calls:06d}",
                timestamp_utc=utc_now_iso(), temperature=temperature,
                max_tokens=max_tokens, seed=seed, latency_s=0.0, attempts=1,
                error=None, request_messages=[{"role": m.role, "content": m.content} for m in messages],
                raw_response={"mock": True},
            )
