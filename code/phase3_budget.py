"""Offline, write-once Phase 3 reservation ledger. Does not make API calls.

Use one shared ledger root for every tonight stage. Unresolved dispatches retain
their full reservation across restarts; they cannot be retried under the same ID.
"""
from __future__ import annotations

from decimal import Decimal, ROUND_CEILING
import hashlib
import json
import os
from pathlib import Path

NANO = 1_000_000_000
POLICY = {
    "id": "phase3_evening_20260913",
    "tonight_cap_nano": 30 * NANO,
    "package_cap_nano": 100 * NANO,
    "prior_package_nano": 22_906_073_025,
    "validation_cap_nano": 10 * NANO,
    "stage_caps_nano": {"generation": NANO, "structural_review": 2 * NANO,
                        "recognition": 7 * NANO},
}


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False).encode("utf-8")


def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def write_once(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as handle:
        handle.write(canonical({"sha256": digest(value), "payload": value}))
        handle.flush()
        os.fsync(handle.fileno())


def read_checked(path):
    envelope = json.loads(Path(path).read_bytes())
    if digest(envelope["payload"]) != envelope["sha256"]:
        raise ValueError("Ledger checksum mismatch")
    return envelope["payload"]


def token_cost_nano(input_tokens, output_tokens, input_usd_per_million,
                    output_usd_per_million):
    if any(type(x) is not int or x < 0 for x in (input_tokens, output_tokens)):
        raise ValueError("Token counts must be nonnegative integers")
    prices = [Decimal(str(x)) for x in (input_usd_per_million, output_usd_per_million)]
    if any(not x.is_finite() or x < 0 for x in prices):
        raise ValueError("Prices must be finite and nonnegative")
    amount = (input_tokens * prices[0] + output_tokens * prices[1]) * 1000 * Decimal("1.10")
    return int(amount.to_integral_value(rounding=ROUND_CEILING))


class BudgetStop(RuntimeError):
    pass


class Budget:
    def __init__(self, root):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)
        self.fd = None
        self.lock = self.root / "execution.lock"
        self.fd = os.open(self.lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        os.write(self.fd, canonical({"pid": os.getpid(), "policy": digest(POLICY)}))
        try:
            policy_path = self.root / "policy.json"
            if not policy_path.exists():
                if any(self.root.glob("reservations/*.json")) or any(self.root.glob("settlements/*.json")):
                    raise BudgetStop("Missing policy on existing ledger")
                write_once(policy_path, POLICY)
            if read_checked(policy_path) != POLICY:
                raise BudgetStop("Budget policy changed; existing spending cannot reset")
            self.audit()
        except BaseException:
            self.close()
            raise

    def close(self):
        if self.fd is not None:
            os.close(self.fd)
            self.fd = None
            self.lock.unlink()

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()

    def audit(self):
        reservations = {p.stem: read_checked(p) for p in self.root.glob("reservations/*.json")}
        settlements = {p.stem: read_checked(p) for p in self.root.glob("settlements/*.json")}
        if settlements.keys() - reservations.keys():
            raise BudgetStop("Orphan settlement")
        spent = {stage: 0 for stage in POLICY["stage_caps_nano"]}
        pending, failed = [], []
        for key, reservation in reservations.items():
            if digest(reservation["slot"]) != key or reservation["stage"] not in spent:
                raise BudgetStop("Reservation identity or stage invalid")
            bound = reservation["reserved_nano"]
            if type(bound) is not int or bound <= 0:
                raise BudgetStop("Invalid reservation amount")
            charge = bound
            if key in settlements:
                settlement = settlements[key]
                if settlement["reservation_sha256"] != digest(reservation):
                    raise BudgetStop("Settlement attached to a different reservation")
                charge = settlement["charged_nano"]
                if type(charge) is not int or charge < 0:
                    raise BudgetStop("Invalid settlement amount")
                if settlement["status"] not in ("complete", "failed", "unknown"):
                    raise BudgetStop("Invalid settlement status")
                if settlement["status"] != "complete":
                    failed.append(key)
                    charge = max(charge, bound)
                if charge > bound:
                    failed.append(key)
            else:
                pending.append(key)
            spent[reservation["stage"]] += charge
        total = sum(spent.values())
        if (total > POLICY["tonight_cap_nano"] or total > POLICY["validation_cap_nano"]
                or total + POLICY["prior_package_nano"] > POLICY["package_cap_nano"]
                or any(spent[k] > POLICY["stage_caps_nano"][k] for k in spent)):
            raise BudgetStop("Existing charges exceed a cap; no further dispatch")
        return {"charged_or_reserved_nano": total, "by_stage_nano": spent,
                "pending": pending, "failed": failed, "reservations": reservations}

    def reserve(self, slot, stage, request, upper_bound_nano, manifest_sha256):
        if self.fd is None:
            raise BudgetStop("Ledger is closed")
        state = self.audit()
        if state["pending"] or state["failed"]:
            raise BudgetStop("Unresolved/failed dispatch; inspect before further spending")
        if stage not in POLICY["stage_caps_nano"]:
            raise BudgetStop("Unreleased stage")
        if type(upper_bound_nano) is not int or upper_bound_nano <= 0:
            raise ValueError("Positive integer reservation required")
        key = digest(slot)
        if key in state["reservations"]:
            raise BudgetStop("Slot already dispatched; never retry in place")
        total = state["charged_or_reserved_nano"] + upper_bound_nano
        if (total > POLICY["tonight_cap_nano"] or total > POLICY["validation_cap_nano"]
                or total + POLICY["prior_package_nano"] > POLICY["package_cap_nano"]
                or state["by_stage_nano"][stage] + upper_bound_nano > POLICY["stage_caps_nano"][stage]):
            raise BudgetStop("Next request cannot fit its reserved cost")
        value = {"slot": slot, "stage": stage, "request": request,
                 "reserved_nano": upper_bound_nano, "manifest_sha256": manifest_sha256}
        write_once(self.root / "reservations" / f"{key}.json", value)
        return key

    def settle(self, key, charged_nano, response_sha256, *, status="complete"):
        if self.fd is None:
            raise BudgetStop("Ledger is closed")
        if type(charged_nano) is not int or charged_nano < 0:
            raise ValueError("Nonnegative integer charge required")
        if status not in ("complete", "failed", "unknown"):
            raise ValueError("Invalid settlement status")
        # Only keys loaded from the ledger may be used as filesystem components.
        state = self.audit()
        if key not in state["reservations"]:
            raise BudgetStop("Unknown reservation")
        reservation = state["reservations"][key]
        value = {"reservation_sha256": digest(reservation), "charged_nano": charged_nano,
                 "response_sha256": response_sha256, "status": status}
        write_once(self.root / "settlements" / f"{key}.json", value)
        return self.audit()
