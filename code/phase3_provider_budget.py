"""Read-only provider accounting and prospective cap checks; no dispatch code.

The user replaces the combined nightly $30 cap with $15 Anthropic/$30 OpenAI.
Historical policy/records remain immutable. No failure is cleared by this change.
"""
from pathlib import Path
import json

from phase3_budget import Budget, BudgetStop, POLICY, digest, read_checked

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "data/raw/phase3_20260913_budget"
CAPS = {"anthropic": 15_000_000_000, "openai": 30_000_000_000}
MODELS = {"claude-sonnet-4-6": "anthropic", "gpt-5.4-mini-2026-03-17": "openai",
          "gpt-5.4-2026-03-05": "openai"}


def provider(request):
    try:
        return MODELS[request["model"]]
    except (KeyError, TypeError):
        raise BudgetStop("Unknown model/provider; explicit allocation required") from None


def check_caps(by_provider, by_stage, proposed=()):
    if set(by_provider) != set(CAPS) or set(by_stage) != set(POLICY["stage_caps_nano"]):
        raise BudgetStop("Incomplete accounting categories")
    providers, stages = dict(by_provider), dict(by_stage)
    for value in list(providers.values()) + list(stages.values()):
        if type(value) is not int or value < 0:
            raise BudgetStop("Invalid accounting amount")
    if sum(providers.values()) != sum(stages.values()):
        raise BudgetStop("Provider and stage totals disagree")
    for item in proposed:
        name = provider(item["request"])
        bound, stage = item["reserved_nano"], item["stage"]
        if type(bound) is not int or bound <= 0 or stage not in stages:
            raise BudgetStop("Invalid reservation or unreleased stage")
        providers[name] += bound
        stages[stage] += bound
    if any(providers[name] > cap for name, cap in CAPS.items()):
        raise BudgetStop("Provider hard cap would be exceeded; no cross-provider borrowing")
    if sum(providers.values()) + POLICY["prior_package_nano"] > POLICY["package_cap_nano"]:
        raise BudgetStop("Package hard cap would be exceeded")
    if (sum(stages.values()) > POLICY["validation_cap_nano"]
            or any(stages[name] > cap for name, cap in POLICY["stage_caps_nano"].items())):
        raise BudgetStop("Stage allocation would be exceeded; provider ceilings do not release stages")
    return providers, stages


def report(root=LEDGER):
    # This audits historical records under their original frozen policy and
    # acquires its shared writer lock. It does not create a new spending ledger.
    with Budget(root) as budget:
        state = budget.audit()
        by_provider = dict.fromkeys(CAPS, 0)
        for key, intent in state["reservations"].items():
            charge = intent["reserved_nano"]
            path = Path(root) / "settlements" / (key + ".json")
            if path.exists():
                settlement = read_checked(path)
                raw = read_checked(Path(root) / "records" / (key + ".json"))
                if (settlement["response_sha256"] != digest(raw)
                        or raw["manifest_sha256"] != intent["manifest_sha256"]
                        or raw["accounted_nano"] != settlement["charged_nano"]):
                    raise BudgetStop("Response provenance/cost mismatch")
                charge = settlement["charged_nano"] if settlement["status"] == "complete" else max(charge, settlement["charged_nano"])
            by_provider[provider(intent["request"])] += charge
        providers, stages = check_caps(by_provider, state["by_stage_nano"])
        return {"policy_revision": "provider_caps_20260913", "caps_nano": CAPS,
                "accounted_nano": providers,
                "remaining_nano": {name: cap - providers[name] for name, cap in CAPS.items()},
                "combined_provider_ceiling_nano": sum(CAPS.values()),
                "package_cap_nano": POLICY["package_cap_nano"],
                "package_accounted_nano": POLICY["prior_package_nano"] + sum(providers.values()),
                "by_stage_nano": stages, "pending": state["pending"], "failed": state["failed"],
                "ready_to_dispatch": False, "new_api_calls": 0,
                "note": "Read-only amendment accounting. Carry forward existing spend; no failure reconciliation or new stage release."}


if __name__ == "__main__":
    print(json.dumps(report()))
