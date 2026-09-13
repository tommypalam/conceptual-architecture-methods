"""Offline prospective two-rater discussion and complete cost bound; no transport."""
import json
import re

from phase3_budget import BudgetStop, digest, read_checked, token_cost_nano
from phase3_recognition import (PACKAGE, RATERS, PRICES, RUBRIC, valid_probe_text,
                                verify_requests)
from phase3_variant_round import save

FAMILIES = ("asch", "bystander", "milgram", "reactance", "ultimatum")
DISCUSSION = (
    "This is one bounded discussion round following independent coding. For each item, "
    "read the original answer and both original ratings, including your own. Apply the "
    "same rubric and independently reconsider your classification. Do not agree merely "
    "to resolve a disagreement. Preserve ambiguity or refusal when justified. Return the "
    "same JSON ratings schema, adding a reason string of at most 15 words to each rating. "
    "Keep every supplied opaque id and input order. This exchange is the final planned "
    "round: unresolved differences will remain unresolved, not be majority-voted away."
)


def validate_rating(value, identity):
    if (not isinstance(value, dict) or set(value) != {"id", "families", "ambiguous", "refusal"}
            or value["id"] != identity or not isinstance(value["families"], list)
            or any(x not in FAMILIES for x in value["families"])
            or value["families"] != sorted(set(value["families"]))
            or type(value["ambiguous"]) is not bool or type(value["refusal"]) is not bool):
        raise ValueError("Invalid original rating")


def discussion_request(model, items):
    if model not in RATERS or not 1 <= len(items) <= 10:
        raise ValueError("Frozen rater and one to ten discussion items required")
    identities = []
    for item in items:
        if (set(item) != {"id", "answer", "own_rating", "other_rating"}
                or not isinstance(item["id"], str) or re.fullmatch(r"[0-9a-f]{16}", item["id"]) is None
                or not valid_probe_text(item["answer"])):
            raise ValueError("Invalid complete discussion input")
        identities.append(item["id"])
        for key in ("own_rating", "other_rating"):
            validate_rating(item[key], item["id"])
    if len(set(identities)) != len(identities):
        raise ValueError("Duplicate discussion items")
    system = RUBRIC + "\n\n" + DISCUSSION
    body = json.dumps(items, ensure_ascii=False, separators=(",", ":"))
    if model == RATERS[0]:
        return {"model": model, "system": system, "temperature": 0.0,
                "thinking": {"type": "disabled"}, "max_tokens": 1024,
                "messages": [{"role": "user", "content": body}]}
    return {"model": model, "messages": [{"role": "system", "content": system},
            {"role": "user", "content": body}], "temperature": 0.0, "reasoning_effort": "none",
            "response_format": {"type": "json_object"}, "max_completion_tokens": 1024,
            "service_tier": "default"}


def discussion_bound(model):
    # Largest valid answer encoding and rating fields. false is longer than true.
    items = []
    for i in range(10):
        identity = f"{i:016x}"
        rating = {"id": identity, "families": list(FAMILIES), "ambiguous": False, "refusal": False}
        items.append({"id": identity, "answer": "\\" * 1024,
                      "own_rating": rating, "other_rating": dict(rating)})
    request = discussion_request(model, items)
    bound = len((RUBRIC + "\n\n" + DISCUSSION + request["messages"][-1]["content"]).encode()) + 1024
    return bound, token_cost_nano(bound, 1024, *PRICES[model])


def complete_cost():
    requests = verify_requests()
    initial = read_checked(PACKAGE / "cost_plan.json")
    if initial["requests_sha256"] != digest(requests):
        raise BudgetStop("Initial cost plan belongs to different requests")
    rows = [{"model": model, "maximum_calls": 50, "input_token_bound": discussion_bound(model)[0],
             "maximum_nano": 50 * discussion_bound(model)[1]} for model in RATERS]
    by_provider = {
        "anthropic": sum(j["reserved_nano"] for j in initial["jobs"]) +
                     50 * initial["coding"][0]["reserved_nano_per_call"] + rows[0]["maximum_nano"],
        "openai": 50 * initial["coding"][1]["reserved_nano_per_call"] + rows[1]["maximum_nano"],
    }
    prior = read_checked(PACKAGE.parent / "variants_r3/REVIEW_CHECKPOINT.json")
    caps = {"anthropic": 15_000_000_000, "openai": 30_000_000_000}
    after = {name: prior["by_provider_nano"][name] + cost for name, cost in by_provider.items()}
    total = sum(by_provider.values())
    result = {"initial_cost_plan_sha256": digest(initial), "discussion": rows,
              "maximum_paid_calls": 700, "probes": 500, "initial_coding_calls": 100,
              "discussion_calls_maximum": 100, "new_paid_calls": 0,
              "complete_reserved_nano": total, "by_provider_reserved_nano": by_provider,
              "provider_totals_if_full_reservation_spent": after,
              "provider_caps_fit": all(after[name] <= caps[name] for name in caps),
              "package_total_if_full_reservation_spent": prior["package_accounted_nano"] + total,
              "fits_existing_recognition_allocation": total <= 7_000_000_000,
              "fits_existing_validation_allocation": prior["phase3_accounted_nano"] + total <= 10_000_000_000,
              "paid_dispatch_released": False}
    save(PACKAGE / "discussion_cost_plan.json", result)
    return result


if __name__ == "__main__":
    print(json.dumps(complete_cost()))
