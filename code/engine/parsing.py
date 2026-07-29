"""
parsing.py — extract structured fields from model output.

Implements spec §5.4.1 (DECISION label extraction anchored on the line
beginning, tolerant of terminal punctuation and quotes; REASONING capture) and
the parsing needs of the complex-problem orchestrator (votes, action types,
and item-citation extraction for the C3 leakage audit, spec §6.4.3).

parse_status values (spec §5.4):
  "ok"        clean DECISION line matched
  "ambiguous" a single label recovered leniently (not on the DECISION line)
  "refusal"   refusal language, no decision
  "fail"      no decision recoverable
"""

from __future__ import annotations

import re

REFUSAL_RE = re.compile(
    r"\b(cannot|can't|unable|won't|refuse|as an ai|i do not have enough|"
    r"i'm sorry|i am sorry)\b",
    re.IGNORECASE,
)


def parse_decision(raw: str | None, labels: tuple[str, str]) -> tuple[str | None, str]:
    """Return (canonical_label | None, parse_status)."""
    if raw is None:
        return None, "fail"
    escaped = "|".join(re.escape(x) for x in labels)

    # Strict: a DECISION: line, optionally bracketed/quoted, terminal punctuation ok.
    strict = re.search(
        rf"^\s*DECISION:\s*[\"'\[]?\s*({escaped})\s*[\"'\]]?\s*\.?\s*$",
        raw, flags=re.IGNORECASE | re.MULTILINE)
    if strict:
        picked = strict.group(1).upper()
        for lab in labels:
            if lab.upper() == picked:
                return lab, "ok"

    # Lenient: exactly one label token appears anywhere.
    present = {lab for lab in labels if re.search(rf"\b{re.escape(lab)}\b", raw, re.IGNORECASE)}
    if len(present) == 1:
        return present.pop(), "ambiguous"

    if REFUSAL_RE.search(raw):
        return None, "refusal"
    return None, "fail"


def parse_reasoning(raw: str | None) -> str | None:
    if raw is None:
        return None
    m = re.search(r"REASONING:\s*[\[\"']?\s*(.*?)\s*[\]\"']?\s*$",
                  raw, flags=re.IGNORECASE | re.DOTALL)
    if m:
        return m.group(1).strip()
    return None


def parse_vote(raw: str | None, labels: tuple[str, str]) -> tuple[str | None, str]:
    """
    Votes in the complex problems use the same DECISION/VOTE line convention.
    Accept either 'VOTE:' or 'DECISION:' as the anchor.
    """
    if raw is None:
        return None, "fail"
    escaped = "|".join(re.escape(x) for x in labels)
    m = re.search(
        rf"^\s*(?:VOTE|DECISION):\s*[\"'\[]?\s*({escaped})\s*[\"'\]]?\s*\.?\s*$",
        raw, flags=re.IGNORECASE | re.MULTILINE)
    if m:
        picked = m.group(1).upper()
        for lab in labels:
            if lab.upper() == picked:
                return lab, "ok"
    return parse_decision(raw, labels)


# Action types agents can take in multi-round deliberation (C1/C2/C3).
ACTION_TYPES = ("propose", "amend", "vote", "share", "argue")


def parse_action_type(raw: str | None) -> str | None:
    """
    Best-effort extraction of a declared action from an ACTION: line, used to
    tag deliberation moves (e.g. amendment-move patterns in C2, spec §6.4.2).
    Falls back to None; the orchestrator does not require it to be present.
    """
    if raw is None:
        return None
    m = re.search(r"^\s*ACTION:\s*([A-Za-z_]+)", raw, flags=re.IGNORECASE | re.MULTILINE)
    if not m:
        return None
    token = m.group(1).lower()
    return token if token in ACTION_TYPES else None


def extract_evidence_citations(raw: str | None, item_ids: list[str]) -> list[str]:
    """
    For the C3 leakage audit (spec §6.4.3): find which pre-specified evidence
    item ids (E01..E24) the agent's text references. The orchestrator compares
    this against what the agent actually received directly or via the transcript.
    """
    if raw is None:
        return []
    found = []
    for item_id in item_ids:
        if re.search(rf"\b{re.escape(item_id)}\b", raw):
            found.append(item_id)
    return found
