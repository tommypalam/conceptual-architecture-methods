"""Prospective independent-field parser; offline candidate, not the pilot parser.

No moral label is supplied or substituted. A unique terminal VOTE label can be
read inline; malformed votes do not erase a valid reasoning/evidence field.
This module is deliberately not imported by the frozen exploratory collector.
"""
from __future__ import annotations

import re

HEADINGS = ("ACTION", "AMENDMENT", "ADOPT", "SHARE", "REASONING", "VOTE")


def parse_group_fields(text, labels, *, finish_reason="stop", refusal=False):
    if finish_reason != "stop" or refusal:
        return {"vote": None, "vote_status": "incomplete_or_refused", "fields": {},
                "field_errors": {}, "evidence_text": None, "evidence_status": "unavailable"}
    headings = list(re.finditer(r"(?m)^(" + "|".join(HEADINGS) + r"):[ \t]*", text or ""))
    fields, errors = {}, {}
    for i, match in enumerate(headings):
        name = match[1]
        value = text[match.end():headings[i + 1].start() if i + 1 < len(headings) else len(text)].strip()
        if name in fields or name in errors:
            fields.pop(name, None)
            errors[name] = "duplicate_field"
        else:
            fields[name] = value
    # Only a single unquoted canonical terminal marker is accepted. Do not infer
    # a preference from explanatory prose, repair spelling, or choose among votes.
    markers = list(re.finditer(r"\bVOTE:", text or ""))
    vote_match = re.search(r"(?:^|[\s])VOTE:[ \t]*(" + "|".join(map(re.escape, labels)) + r")[ \t]*$", text or "")
    vote = vote_match[1] if vote_match and len(markers) == 1 else None
    if "REASONING" in fields and vote_match and len(markers) == 1:
        fields["REASONING"] = re.sub(r"[\s]+VOTE:[ \t]*(?:" + "|".join(map(re.escape, labels)) + r")[ \t]*$", "", fields["REASONING"]).strip()
    reason = fields.get("REASONING")
    share = fields.get("SHARE")
    evidence = " ".join(x for x in (reason, share) if x)
    return {"vote": vote, "vote_status": "ok" if vote else "missing_or_ambiguous",
            "fields": fields, "field_errors": errors,
            "evidence_text": evidence or None,
            "evidence_status": "available" if evidence else "unavailable"}


def authenticate_disclosures(parsed, directly_held, public_before):
    """Evidence visibility depends on provenance, independently of vote validity."""
    cited = set(re.findall(r"\bE\d{2}\b", parsed.get("evidence_text") or ""))
    allowed = set(directly_held) | set(public_before)
    return {"authenticated": sorted(cited & allowed), "unavailable": sorted(cited - allowed)}
