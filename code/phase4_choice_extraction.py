"""Provider-agnostic choice extraction for cross-model Phase 4 runs.

The Phase 4 collectors inherited a response contract that assumes bare JSON in
under 1024 bytes, which is how `gpt-5.4-mini` answers. `claude-haiku-4-5` answers
the same prompts correctly but reasons first and then emits the JSON, often in a
fenced block, so its replies were rejected on format.

Output format is not part of the estimand. The comparison is: same input, same
deterministic rule map, does the profile move the choice? A reply carrying
`{"choice": "X"}` after a paragraph of reasoning contains exactly the same datum
as a bare `{"choice": "X"}`. Reading it is measurement plumbing, not a design
change - unlike editing the prompt, which would confound the comparison and was
refused.

**Strictness is preserved, and in one respect increased.** This extractor:

  - reads ONLY from a JSON object of the exact form {"choice": "..."}; prose is
    never scanned for option names, even when the prose names them (a sampled
    haiku reply mentioned both options by name while choosing one);
  - requires exactly ONE such object. Two or more, agreeing or not, is ambiguous
    and returns None rather than picking the last or the majority;
  - requires the chosen value to be a declared action id for that task;
  - rejects objects carrying any key besides "choice", and rejects duplicate
    JSON keys.

It never repairs, truncates or infers. An unreadable reply stays unreadable.
"""
from __future__ import annotations

import json
import re

# A JSON object whose only key is "choice". Deliberately narrow: this must not
# match a larger object that merely contains a choice field among others.
_CHOICE_OBJECT = re.compile(r'\{\s*"choice"\s*:\s*"([^"\\]{1,64})"\s*\}')


def _unique_keys(pairs):
    if len({k for k, _ in pairs}) != len(pairs):
        raise ValueError("Duplicate JSON key")
    return dict(pairs)


def extract_choice(text, valid):
    """Return the chosen action id, or None if the reply is not unambiguous.

    `valid` is the set of lower-cased action ids declared for the task. The
    match is case-insensitive because models vary in how they echo the labels,
    but the value must be a declared id: nothing is inferred.
    """
    if not isinstance(text, str) or not text.strip():
        return None

    matches = _CHOICE_OBJECT.findall(text)
    if len(matches) != 1:
        # Zero: no answer object. More than one: ambiguous, even if they agree.
        return None

    # Re-parse the matched object properly rather than trusting the regex, so
    # duplicate keys and malformed escapes are still rejected.
    span = _CHOICE_OBJECT.search(text)
    try:
        value = json.loads(span.group(0), object_pairs_hook=_unique_keys)
    except (ValueError, TypeError):
        return None
    if not isinstance(value, dict) or set(value) != {"choice"}:
        return None

    picked = str(value["choice"]).strip().lower()
    return picked if picked in valid else None


def response_text(raw):
    """Concatenated text of a provider response, or None.

    Handles both request shapes without judging either. Does not check stop
    reasons or lengths: the caller's own guards own that.
    """
    if not isinstance(raw, dict):
        return None
    if raw.get("choices"):
        message = raw["choices"][0].get("message") or {}
        content = message.get("content")
        return content if isinstance(content, str) else None
    if raw.get("content"):
        blocks = raw["content"]
        if not isinstance(blocks, list):
            return None
        return "".join(b.get("text", "") for b in blocks if isinstance(b, dict))
    return None


def _selftest():
    valid = {"describe_vaguely", "break_seal"}
    cases = [
        ('{"choice":"BREAK_SEAL"}', "break_seal", "bare json, upper case"),
        ('Reasoning about break_seal and describe_vaguely at length.\n\n'
         '```json\n{"choice":"DESCRIBE_VAGUELY"}\n```', "describe_vaguely",
         "prose naming BOTH options, then one json object"),
        ('{"choice":"break_seal"} and also {"choice":"break_seal"}', None,
         "two objects, agreeing -> still ambiguous"),
        ('{"choice":"break_seal"} then {"choice":"describe_vaguely"}', None,
         "two objects, disagreeing"),
        ('I choose break_seal.', None, "prose only, no object"),
        ('{"choice":"not_an_action"}', None, "undeclared action id"),
        ('{"choice":"break_seal","why":"x"}', None, "extra key"),
        ('', None, "empty"),
        (None, None, "not a string"),
    ]
    failures = []
    for text, expected, label in cases:
        got = extract_choice(text, valid)
        status = "ok " if got == expected else "FAIL"
        if got != expected:
            failures.append(label)
        print(f"  [{status}] {label:48s} -> {got!r}")
    print()
    print("selftest:", "all pass" if not failures else f"FAILURES: {failures}")
    return not failures


if __name__ == "__main__":
    raise SystemExit(0 if _selftest() else 1)
