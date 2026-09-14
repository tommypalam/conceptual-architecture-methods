"""Second moral task set: wider tension coverage plus explicit negative controls.

Set B extends `phase4_conflict_tasks.py` (set A) in two ways an external review
of the project identified as the binding limitation on the capstone result:

1. **More conflict tasks, with wider coverage.** Set A's tensions were
   concentrated: deception-vs-harm three times, unfairness twice, coercion once.
   Set B adds tasks whose opposing pair is deception-vs-unfairness,
   coercion-vs-harm, coercion-vs-unfairness and deception-vs-coercion, so a
   result is not carried by one kind of dilemma.

2. **Negative controls.** Three tasks are deliberately constructed with a
   dominant option: one choice upholds every standard it can and carries the
   higher stipulated total. If profiles shift choices on these as much as on the
   conflict tasks, the capstone effect is not specific to moral conflict and the
   interpretation is wrong. `CONTROL_IDS` records them before collection.

Negative controls are expected to saturate in the dispersion screen, and that is
the point: a control that saturates confirms it has an obvious answer. Controls
are therefore screened and reported but are NOT required to pass the dispersion
gate to serve their purpose. They enter a profiled study only if they disperse,
in which case they become the sharpest possible test of specificity.

No moral score is assigned here. The module supplies situations, actions and
stipulated consequences; classification is the separate deterministic step in
`phase4_conflict_rules.py`.
"""
from __future__ import annotations

import hashlib
import json

# Conflict tasks: no option upholds every standard.
CONFLICT_IDS = (
    "audit_sampling",     # deception vs. unfairness
    "shelter_places",     # coercion vs. harm
    "wage_disclosure",    # deception vs. unfairness
    "quarantine_notice",  # coercion vs. unfairness
    "evidence_seal",      # deception vs. coercion
)

# Negative controls: one option dominates on standards AND total.
CONTROL_IDS = (
    "ledger_error",       # correcting an error harms no one and helps
    "duplicate_charge",   # refunding is honest, fair and higher total
    "expired_stock",      # withdrawing unsafe stock is clean on every standard
)

TASK_IDS = CONFLICT_IDS + CONTROL_IDS

STANDARDS = ("harm_avoidance", "deception_avoidance", "coercion_avoidance",
             "unfairness_avoidance")

FORBIDDEN = (
    "procedural dependence", "legitimacy locus", "constraint sensitivity",
    "response threshold", "mode of response", "relational embedding",
    "tolerance for asymmetry", "internalisation dependence", "moral scope",
    "affective weighting", "parameter", "coordinate", "profile value",
    "hypothesis", "predicted", "prediction", "correct answer", "should choose",
    "the right thing", "morally correct", "ethical choice", "unethical",
    "milgram", "asch", "ultimatum", "bystander", "reactance",
    "negative control", "dominant option",
)

BANNED_COMPARATIVES = (
    "better", "worse", "superior", "inferior", "preferable", "obviously",
    "clearly the", "outweigh", "the best", "the worst",
)

_TASKS = {
    # ---------------- conflict tasks ----------------
    "audit_sampling": {
        "situation": (
            "You select files for a compliance audit. The published method draws a random "
            "sample. Three files outside the draw contain the irregularities. The audit "
            "report states the method used."
        ),
        "actions": {
            "report_random_draw": {
                "description": "Audit the randomly drawn files and report the method used.",
                "actor_delta": 0, "third_party_deltas": [-7, 2],
                "deceptive": False, "coercive": False, "unfair": False,
                "effect_text": "Those affected by the irregularities lose 7 units; the audited "
                               "units gain 2. The report is accurate about its method.",
            },
            "substitute_files": {
                "description": ("Substitute the three files you know are irregular, and report "
                                "the sample as randomly drawn."),
                "actor_delta": 0, "third_party_deltas": [6, -2],
                "deceptive": True, "coercive": False, "unfair": True,
                "effect_text": "Those affected gain 6 units; the substituted units lose 2. The "
                               "report describes a draw that did not occur.",
            },
        },
    },
    "shelter_places": {
        "situation": (
            "You manage overnight shelter places during a cold-weather alert. One person who "
            "has a place has stated they will not accept a shared room. Two people are waiting "
            "with no place. Moving the first person frees the room for both."
        ),
        "actions": {
            "respect_refusal": {
                "description": "Leave the current room arrangement unchanged.",
                "actor_delta": 0, "third_party_deltas": [3, -6],
                "deceptive": False, "coercive": False, "unfair": False,
                "effect_text": "The person with a place gains 3 units; the two waiting lose "
                               "6 units between them.",
            },
            "reassign_room": {
                "description": "Move the person to a shared room despite their stated refusal.",
                "actor_delta": 0, "third_party_deltas": [-4, 8],
                "deceptive": False, "coercive": True, "unfair": False,
                "effect_text": "The moved person loses 4 units; the two waiting gain 8 units "
                               "between them.",
            },
        },
    },
    "wage_disclosure": {
        "situation": (
            "Two employees on identical terms ask you what the other is paid. One is paid more "
            "because of a historical adjustment. Your organisation has no policy forbidding "
            "disclosure."
        ),
        "actions": {
            "disclose_both": {
                "description": "Tell each what the other is paid, accurately.",
                "actor_delta": 0, "third_party_deltas": [-5, 3],
                "deceptive": False, "coercive": False, "unfair": False,
                "effect_text": "One employee loses 5 units from the disclosure; the other gains "
                               "3 units. Both statements are accurate.",
            },
            "state_parity": {
                "description": "Tell each that their terms are equivalent, without stating the figures.",
                "actor_delta": 0, "third_party_deltas": [2, 1],
                "deceptive": True, "coercive": False, "unfair": True,
                "effect_text": "Each gains 2 and 1 units. The statement conceals the difference "
                               "and leaves the unequal terms in place.",
            },
        },
    },
    "quarantine_notice": {
        "situation": (
            "A contagious case is confirmed in a residence. The published rule restricts the "
            "confirmed case only. Restricting the whole floor would reduce transmission. "
            "Residents on the floor have not agreed to be restricted."
        ),
        "actions": {
            "restrict_as_published": {
                "description": "Restrict the confirmed case only.",
                "actor_delta": 0, "third_party_deltas": [4, -9],
                "deceptive": False, "coercive": False, "unfair": False,
                "effect_text": "The floor residents gain 4 units of unrestricted movement; "
                               "9 units are lost to onward transmission.",
            },
            "restrict_floor": {
                "description": "Restrict the whole floor, beyond what the published rule provides.",
                "actor_delta": 0, "third_party_deltas": [-6, 11],
                "deceptive": False, "coercive": True, "unfair": True,
                "effect_text": "The floor residents lose 6 units of movement; 11 units of "
                               "transmission are avoided. Some restricted residents pose no risk.",
            },
        },
    },
    "evidence_seal": {
        "situation": (
            "A sealed record would clear a person currently under suspicion. The seal was "
            "granted to a third party who has refused to lift it. You can describe the record's "
            "contents without breaking the seal, or break it."
        ),
        "actions": {
            "describe_vaguely": {
                "description": ("Give an account of the record that omits what identifies the "
                                "sealed material."),
                "actor_delta": 0, "third_party_deltas": [3, 1],
                "deceptive": True, "coercive": False, "unfair": False,
                "effect_text": "The suspected person gains 3 units; the seal holder gains "
                               "1 unit. The account omits identifying detail.",
            },
            "break_seal": {
                "description": "Disclose the sealed record despite the holder's refusal.",
                "actor_delta": 0, "third_party_deltas": [8, -5],
                "deceptive": False, "coercive": True, "unfair": False,
                "effect_text": "The suspected person gains 8 units; the seal holder loses "
                               "5 units. The refusal is overridden.",
            },
        },
    },
    # ---------------- negative controls: one option dominates ----------------
    "ledger_error": {
        "situation": (
            "You find an arithmetic error in a closed ledger. Correcting it costs nothing and "
            "takes ten minutes. Leaving it means the recorded figure stays wrong."
        ),
        "actions": {
            "correct_entry": {
                "description": "Correct the entry and note the correction in the record.",
                "actor_delta": 0, "third_party_deltas": [5, 2],
                "deceptive": False, "coercive": False, "unfair": False,
                "effect_text": "Those relying on the ledger gain 5 units; the record-keeper "
                               "gains 2. The record becomes accurate.",
            },
            "leave_entry": {
                "description": "Leave the entry as it stands without noting the error.",
                "actor_delta": 0, "third_party_deltas": [-3, -1],
                "deceptive": True, "coercive": False, "unfair": False,
                "effect_text": "Those relying on the ledger lose 3 units; the record-keeper "
                               "loses 1. The known error is not recorded.",
            },
        },
    },
    "duplicate_charge": {
        "situation": (
            "A customer was charged twice for one item. The duplicate is visible in your "
            "records. Refunding it is a routine action available to you."
        ),
        "actions": {
            "refund_duplicate": {
                "description": "Refund the duplicate charge and tell the customer.",
                "actor_delta": 0, "third_party_deltas": [6, 1],
                "deceptive": False, "coercive": False, "unfair": False,
                "effect_text": "The customer gains 6 units; the account record gains 1. The "
                               "customer is informed.",
            },
            "retain_charge": {
                "description": "Leave the duplicate charge in place and say nothing.",
                "actor_delta": 0, "third_party_deltas": [-6, 0],
                "deceptive": True, "coercive": False, "unfair": True,
                "effect_text": "The customer loses 6 units; nothing else changes. The customer "
                               "is not told.",
            },
        },
    },
    "expired_stock": {
        "situation": (
            "A batch of stock passed its safety date yesterday. Withdrawing it costs a small "
            "restocking fee that your budget covers. Selling it is still physically possible."
        ),
        "actions": {
            "withdraw_batch": {
                "description": "Withdraw the batch and record the reason.",
                "actor_delta": 0, "third_party_deltas": [7, 1],
                "deceptive": False, "coercive": False, "unfair": False,
                "effect_text": "Buyers gain 7 units of avoided risk; the supplier gains 1. The "
                               "reason is recorded.",
            },
            "sell_batch": {
                "description": "Sell the batch without noting that it passed its safety date.",
                "actor_delta": 0, "third_party_deltas": [-8, 2],
                "deceptive": True, "coercive": False, "unfair": False,
                "effect_text": "Buyers lose 8 units of risk; the supplier gains 2. The date is "
                               "not noted.",
            },
        },
    },
}

COMMON_FRAMING = (
    "You hold the role described. The option you select will be carried out, not merely "
    "considered. Units are artificial simulator credits, stipulated equally valuable to "
    "every person, and all stated effects are certain and known to you. There are no "
    "hidden costs, benefits or later effects beyond those described, and no one is "
    "pressuring you toward either option. Decide on the situation as given."
)


def task(task_id):
    if task_id not in TASK_IDS:
        raise ValueError(f"Unknown task: {task_id}")
    return json.loads(json.dumps(_TASKS[task_id]))


def action_ids(task_id):
    return tuple(_TASKS[task_id]["actions"])


def participant_text(task_id):
    spec = _TASKS[task_id]
    lines = [f"Option {a.upper()}: {act['description']} {act['effect_text']}"
             for a, act in spec["actions"].items()]
    return "\n\n".join((COMMON_FRAMING, spec["situation"], "# Options\n" + "\n".join(lines)))


def total_delta(task_id, action_id):
    action = _TASKS[task_id]["actions"][action_id]
    return action["actor_delta"] + sum(action["third_party_deltas"])


def standards_upheld(task_id, action_id):
    action = _TASKS[task_id]["actions"][action_id]
    return {
        "harm_avoidance": all(x >= 0 for x in action["third_party_deltas"]),
        "deception_avoidance": not action["deceptive"],
        "coercion_avoidance": not action["coercive"],
        "unfairness_avoidance": not action["unfair"],
    }


def _dominates(task_id, a, b):
    ups_a, ups_b = standards_upheld(task_id, a), standards_upheld(task_id, b)
    return (all(ups_a[s] or not ups_b[s] for s in STANDARDS)
            and total_delta(task_id, a) >= total_delta(task_id, b)
            and (any(ups_a[s] and not ups_b[s] for s in STANDARDS)
                 or total_delta(task_id, a) > total_delta(task_id, b)))


def verify_structure():
    """Conflict tasks must have no dominant option; controls must have one.

    The control requirement is as strict as the conflict requirement: a control
    that does not actually dominate cannot serve as a negative control.
    """
    problems = []
    for task_id in CONFLICT_IDS:
        ids = action_ids(task_id)
        for a in ids:
            for b in ids:
                if a != b and _dominates(task_id, a, b):
                    problems.append(f"{task_id}: {a} dominates {b}; not a conflict")
            if all(standards_upheld(task_id, a).values()):
                problems.append(f"{task_id}: {a} upholds every standard; not a conflict")
        violated = {s for a in ids for s in STANDARDS if not standards_upheld(task_id, a)[s]}
        if len(violated) < 2:
            problems.append(f"{task_id}: fewer than two standards in tension")

    for task_id in CONTROL_IDS:
        ids = action_ids(task_id)
        dominant = [a for a in ids if all(_dominates(task_id, a, b) for b in ids if b != a)]
        if len(dominant) != 1:
            problems.append(f"{task_id}: expected exactly one dominant option, found {dominant}")
        elif not all(standards_upheld(task_id, dominant[0]).values()):
            problems.append(f"{task_id}: dominant option does not uphold every standard")

    if problems:
        raise ValueError("Structure verification failed: " + "; ".join(problems))
    return {"verified": True, "conflict_tasks": len(CONFLICT_IDS),
            "control_tasks": len(CONTROL_IDS)}


def tension_coverage():
    """Which standard pairs each conflict task puts in opposition."""
    out = {}
    for task_id in CONFLICT_IDS:
        violated = sorted({s for a in action_ids(task_id) for s in STANDARDS
                           if not standards_upheld(task_id, a)[s]})
        out[task_id] = violated
    return out


def audit_leakage(task_id):
    blob = participant_text(task_id).lower()
    return [t for t in FORBIDDEN if t in blob]


def audit_comparatives(task_id):
    blob = participant_text(task_id).lower()
    return [p for p in BANNED_COMPARATIVES if p in blob]


def content_hash():
    payload = json.dumps({"tasks": _TASKS, "framing": COMMON_FRAMING,
                          "conflict": list(CONFLICT_IDS), "controls": list(CONTROL_IDS)},
                         sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def main():
    verify_structure()
    print(f"tasks: {len(TASK_IDS)}  ({len(CONFLICT_IDS)} conflict, {len(CONTROL_IDS)} control)")
    print(f"content hash: {content_hash()}\n")
    for task_id in TASK_IDS:
        kind = "conflict" if task_id in CONFLICT_IDS else "CONTROL "
        print(f"--- {task_id}  [{kind}]")
        for action_id in action_ids(task_id):
            ups = standards_upheld(task_id, action_id)
            violated = [s.split("_")[0] for s, v in ups.items() if not v]
            print(f"      {action_id:20s} total={total_delta(task_id, action_id):+4d} "
                  f"violates={','.join(violated) or 'none'}")
    print("\ntension coverage across conflict tasks:")
    for task_id, pair in tension_coverage().items():
        print(f"  {task_id:20s} {[p.split('_')[0] for p in pair]}")
    leaks = sum(len(audit_leakage(t)) + len(audit_comparatives(t)) for t in TASK_IDS)
    print(f"\nstructure: {verify_structure()}")
    print(f"leakage/comparative audit: {leaks} findings")
    words = [len(participant_text(t).split()) for t in TASK_IDS]
    print(f"participant text: {min(words)}-{max(words)} words")


if __name__ == "__main__":
    main()
