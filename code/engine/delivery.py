"""
delivery.py — how an assembled harness reaches the model (a swappable seam).

Step A (2026-07-28) showed the mere presence of a system message contributes to
the Phase 0b collapse. To test a no-system-message harness WITHOUT rewriting the
null-condition assemblers, we separate two concerns that were previously fused:

  - WHAT the harness says      -> the null-condition assemblers (phase0b.py)
  - WHERE it is delivered      -> this module (system role vs user-turn prefix)

A `Delivery` turns (harness_text, user_turn) into the actual message list. Both
implementations satisfy the same shape (Liskov), so the runner is injected with
one and never branches on delivery mode itself.

  SystemRoleDelivery  harness as a system message, dilemma as user  (canonical)
  UserPrefixDelivery  NO system message; harness text prepended to the user turn
                      (reproduces the Phase-0a structure: user-only), separated
                      by a rule so the model still sees the profile/task.
"""

from __future__ import annotations

from typing import Protocol

from .llm_client import Message


class Delivery(Protocol):
    delivery_id: str

    def messages(self, harness_text: str, user_turn: str) -> list[Message]:
        ...


class SystemRoleDelivery:
    delivery_id = "system_role"

    def messages(self, harness_text: str, user_turn: str) -> list[Message]:
        return [Message("system", harness_text), Message("user", user_turn)]


class UserPrefixDelivery:
    """
    No system message. The harness (profile/task block) is prepended to the user
    turn, separated from the dilemma by a divider so the two remain legible. The
    empty-harness (null_a) case degrades naturally: if harness_text is only the
    preamble+task, that is all that precedes the dilemma.
    """
    delivery_id = "user_prefix"

    def messages(self, harness_text: str, user_turn: str) -> list[Message]:
        # Empty harness text => truly naked: the user turn alone, no leading
        # separator (used by the null_a scaffolding-ladder L0 level).
        if not harness_text:
            return [Message("user", user_turn)]
        combined = f"{harness_text}\n\n---\n\n{user_turn}"
        return [Message("user", combined)]


DELIVERIES = {
    "system_role": SystemRoleDelivery,
    "user_prefix": UserPrefixDelivery,
}
