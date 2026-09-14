"""Negative-control pool for the capstone specificity check.

The three control tasks from set B, declared as controls in `CONTROL_IDS` before
any collection and verified to have exactly one dominant option that upholds all
four fixed standards and carries the higher stipulated total.

They saturated at modal share 1.00 unprofiled, as designed. This module exposes
them for a PROFILED run, which is the specificity check
`moral_capstone_r3` records as outstanding:

  If profiles shift choices on these as much as on the conflict tasks, the
  capstone's interpretation - that profiles change WHICH standard is sacrificed
  when standards conflict - is wrong, and the effect is a general answer shift.

Prediction, fixed before collection: **no arm difference on any control task.**
There is no standard-conflict to resolve, so the process/outcome axis has
nothing to act on.

This module defines no new task text and changes no stipulated effect.
"""
from __future__ import annotations

import hashlib
import json

import phase4_conflict_tasks_b as B

TASK_IDS = B.CONTROL_IDS
SOURCE = {t: "B" for t in TASK_IDS}
STANDARDS = B.STANDARDS
COMMON_FRAMING = B.COMMON_FRAMING

# Measured unprofiled dispersion, from moral_conflict_screen_b2. All saturated.
DISPERSION = {"ledger_error": 1.00, "duplicate_charge": 1.00, "expired_stock": 1.00}


def task(task_id):
    if task_id not in TASK_IDS:
        raise ValueError(f"Task not in the control pool: {task_id}")
    return B.task(task_id)


def action_ids(task_id):
    return B.action_ids(task_id)


def participant_text(task_id):
    return B.participant_text(task_id)


def total_delta(task_id, action_id):
    return B.total_delta(task_id, action_id)


def standards_upheld(task_id, action_id):
    return B.standards_upheld(task_id, action_id)


def audit_leakage(task_id):
    return B.audit_leakage(task_id)


def audit_comparatives(task_id):
    return B.audit_comparatives(task_id)


def classify(task_id, action_id):
    """Same deterministic rules as the conflict pool, routed to set B."""
    from phase4_moral_schema import summarize
    if action_id not in action_ids(task_id):
        raise ValueError(f"Action outside the registry: {task_id}/{action_id}")
    act = task(task_id)["actions"][action_id]
    ups = standards_upheld(task_id, action_id)
    tot = total_delta(task_id, action_id)
    third, actor = act["third_party_deltas"], act["actor_delta"]
    dec, coe, unf = act["deceptive"], act["coercive"], act["unfair"]
    viol = dec or coe or unf
    rel = [0, int(dec), int(tot < 0), int(viol), int(not viol), int(not dec),
           int(any(x > 0 for x in third) and (actor < 0 or tot > 0)),
           int(not dec and not coe and tot < 0)]
    fix = [int(ups["harm_avoidance"]), int(ups["deception_avoidance"]),
           int(ups["coercion_avoidance"]), int(ups["unfairness_avoidance"])]
    return {"rule_version": "conflict-rules-r1", "task": task_id, "action": action_id,
            "effects": {"actor_delta": actor, "third_party_deltas": list(third),
                        "total_delta": tot},
            "configuration_relative": rel, "fixed_standard": fix,
            "headlines": summarize(rel, fix),
            "measurement": ("deterministic operational classification under stipulated "
                            "standards; no AI or human rater label, and not moral truth")}


def primary_outcome(task_id, action_id):
    h = classify(task_id, action_id)["headlines"]
    return {"primary_net": h["net_possible"][0] if len(h["net_possible"]) == 1 else None,
            "secondary_strict_relative": h["relative_headline"],
            "secondary_weighted": (h["weighted_possible"][0]
                                   if len(h["weighted_possible"]) == 1 else None),
            "fixed_standard_headline": h["fixed_headline"]}


def verify_pool():
    """Every pooled task must be a genuine control: one dominant clean option.

    The mirror of the conflict pool's check. A control that does not dominate
    cannot serve as a negative control, and the primary must still discriminate
    or an arm difference could not be detected even if one existed.
    """
    problems = []
    for task_id in TASK_IDS:
        ids = action_ids(task_id)
        clean = [a for a in ids if all(standards_upheld(task_id, a).values())]
        if len(clean) != 1:
            problems.append(f"{task_id}: expected one standard-clean option, got {clean}")
        elif total_delta(task_id, clean[0]) != max(total_delta(task_id, a) for a in ids):
            problems.append(f"{task_id}: the clean option does not carry the higher total")
        nets = {primary_outcome(task_id, a)["primary_net"] for a in ids}
        if None in nets:
            problems.append(f"{task_id}: net primary not identified")
        if len(nets) < 2:
            problems.append(f"{task_id}: net primary constant; no arm difference detectable")
    if problems:
        raise ValueError("Control pool verification failed: " + "; ".join(problems))
    return {"verified": True, "tasks": len(TASK_IDS), "kind": "negative_controls"}


def content_hash():
    payload = json.dumps({"tasks": list(TASK_IDS), "dispersion": DISPERSION,
                          "set_b": B.content_hash()},
                         sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def main():
    print(f"control pool: {verify_pool()}")
    print(f"content hash: {content_hash()}")
    print()
    for t in TASK_IDS:
        for a in action_ids(t):
            ups = standards_upheld(t, a)
            viol = [s.split("_")[0] for s, v in ups.items() if not v]
            print(f"  {t:18s} {a:18s} total={total_delta(t, a):+3d} "
                  f"net={primary_outcome(t, a)['primary_net']:8s} "
                  f"violates={','.join(viol) or 'none'}")


if __name__ == "__main__":
    main()
