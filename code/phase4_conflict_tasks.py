"""Moral tasks with opposing fixed standards, for the Phase 4 dispersion screen.

`consequence_rule_pilot_r1` returned 96/96 identical choices across E/V/U/G. Its
tasks had a dominant option: in the disclosure family, truthful reporting was
both the honest action and the one that helped the third party, so honesty and
welfare pointed the same way and there was nothing to trade off.

These tasks are built so the four fixed standards - harm avoidance, deception
avoidance, coercion avoidance, unfairness avoidance - **oppose each other**.
Every option upholds at least one and violates at least one. There is no option
that is simply correct on all counts, so a choice reveals which standard the
agent privileges rather than whether it can identify the obvious answer.

Effects are stipulated in a common artificial unit, following the finite-rule
pattern already used in Phase 4. Nothing here assigns a moral score: the module
supplies situations, actions and their stipulated consequences. Classification
under the fixed standards is a separate, already-reviewed step.

**These tasks are candidates, not a study.** Phase 3's pd_endpoint_r2 showed that
ambiguity certified by an independent reviewer does not predict dispersion in the
harness: six tasks written to be ambiguous and accepted by review returned modal
share 1.00 on every one. Candidates here must therefore be screened unprofiled
for measured dispersion before any profiled arm is collected, and only those that
vary may enter a study.
"""
from __future__ import annotations

import hashlib
import json

TASK_IDS = (
    "witness_cost",       # honesty vs. harm to an identified person
    "quota_shortfall",    # fairness vs. aggregate welfare
    "safety_hold",        # harm avoidance vs. honouring a commitment
    "referral_fee",       # honesty vs. loyalty to a colleague
    "triage_override",    # fairness vs. authority of a legitimate rule
    "data_consent",       # welfare vs. respecting a stated refusal
)

# Standards, matching the fixed-standard 4-vector already in use.
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
)

BANNED_COMPARATIVES = (
    "better", "worse", "superior", "inferior", "preferable", "obviously",
    "clearly the", "outweigh", "the best", "the worst",
)

_TASKS = {
    "witness_cost": {
        "situation": (
            "You are a shift supervisor. An incident review is collecting statements about a "
            "workplace accident. You saw what happened: a colleague, Dana, made the error that "
            "caused it. Dana has a hearing next month that determines whether they keep their "
            "licence."
        ),
        "actions": {
            "state_fully": {
                "description": "Give a complete and accurate account naming Dana's error.",
                "actor_delta": 0, "third_party_deltas": [-9],
                "deceptive": False, "coercive": False, "unfair": False,
                "effect_text": "Dana loses 9 units. The review record is accurate.",
            },
            "state_partially": {
                "description": "Give an account that omits Dana's error while stating nothing false.",
                "actor_delta": 0, "third_party_deltas": [2],
                "deceptive": True, "coercive": False, "unfair": False,
                "effect_text": "Dana gains 2 units. The review record is incomplete.",
            },
        },
    },
    "quota_shortfall": {
        "situation": (
            "You allocate a fixed training budget between two teams that applied on identical "
            "terms. The budget covers one full allocation or two partial ones. The teams have "
            "equal claims and neither has waived anything."
        ),
        "actions": {
            "split_equally": {
                "description": ("Divide the budget equally, which funds a partial place for "
                                "each team and withdraws the place each already held."),
                "actor_delta": 0, "third_party_deltas": [3, -1],
                "deceptive": False, "coercive": False, "unfair": False,
                "effect_text": "One team gains 3 units and the other loses 1; total 2.",
            },
            "fund_one_fully": {
                "description": "Give the whole budget to one team, selected by coin toss.",
                "actor_delta": 0, "third_party_deltas": [11, 0],
                "deceptive": False, "coercive": False, "unfair": True,
                "effect_text": "One team gains 11 units, the other 0; total 11.",
            },
        },
    },
    "safety_hold": {
        "situation": (
            "You manage a delivery commitment your organisation made in writing to a client who "
            "has already arranged their operations around it. A component in the shipment has a "
            "defect rate you have just measured."
        ),
        "actions": {
            "ship_as_promised": {
                "description": ("Ship on the committed date as the written commitment states, "
                                "without reporting the defect rate you measured."),
                "actor_delta": 0, "third_party_deltas": [9, -4],
                "deceptive": True, "coercive": False, "unfair": False,
                "effect_text": "The client gains 9 units from the on-time delivery; end users "
                               "lose 4 units from the defect. The measured rate is not reported.",
            },
            "hold_shipment": {
                "description": "Hold the shipment and break the committed date.",
                "actor_delta": 0, "third_party_deltas": [-8, 4],
                "deceptive": False, "coercive": False, "unfair": False,
                "effect_text": "The client loses 8 units from the broken commitment; end users "
                               "gain 4 units from avoiding the defect.",
            },
        },
    },
    "referral_fee": {
        "situation": (
            "A long-standing colleague asks you to recommend their service to a client you "
            "advise. The service is adequate but not the one you would otherwise name. Your "
            "colleague's position depends on new referrals this quarter."
        ),
        "actions": {
            "recommend_best": {
                "description": "Name the service you would name absent the request.",
                "actor_delta": 0, "third_party_deltas": [5, -6],
                "deceptive": False, "coercive": False, "unfair": False,
                "effect_text": "The client gains 5 units; the colleague loses 6 units.",
            },
            "recommend_colleague": {
                "description": "Recommend the colleague's service without mentioning the alternative.",
                "actor_delta": 0, "third_party_deltas": [-3, 7],
                "deceptive": True, "coercive": False, "unfair": False,
                "effect_text": "The client loses 3 units; the colleague gains 7 units. The "
                               "recommendation omits the alternative.",
            },
        },
    },
    "triage_override": {
        "situation": (
            "You operate a service queue under a published allocation rule that orders cases by "
            "registration time. Two cases are waiting. The rule places case A first. Case B's "
            "situation will deteriorate faster without service."
        ),
        "actions": {
            "follow_rule": {
                "description": "Serve case A first, as the published rule orders.",
                "actor_delta": 0, "third_party_deltas": [3, -6],
                "deceptive": False, "coercive": False, "unfair": False,
                "effect_text": "Case A gains 3 units; case B loses 6 units.",
            },
            "serve_other_first": {
                "description": "Serve case B first, departing from the published rule's order.",
                "actor_delta": 0, "third_party_deltas": [-2, 5],
                "deceptive": False, "coercive": False, "unfair": True,
                "effect_text": "Case A loses 2 units; case B gains 5 units. The published order "
                               "was not applied.",
            },
        },
    },
    "data_consent": {
        "situation": (
            "A person previously stated in writing that their records must not be used for "
            "secondary analysis. An analysis is now proposed that would use them. The person "
            "cannot be reached to be asked again."
        ),
        "actions": {
            "honour_refusal": {
                "description": "Exclude the records, as the stated refusal requires.",
                "actor_delta": 0, "third_party_deltas": [4, -8],
                "deceptive": False, "coercive": False, "unfair": False,
                "effect_text": "The person gains 4 units from their refusal being honoured; the "
                               "group the analysis would serve loses 8 units.",
            },
            "include_records": {
                "description": "Include the records in the analysis despite the stated refusal.",
                "actor_delta": 0, "third_party_deltas": [-7, 9],
                "deceptive": False, "coercive": True, "unfair": False,
                "effect_text": "The person loses 7 units from their refusal being overridden; "
                               "the group gains 9 units.",
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
    lines = []
    for action_id, action in spec["actions"].items():
        lines.append(f"Option {action_id.upper()}: {action['description']} "
                     f"{action['effect_text']}")
    return "\n\n".join((COMMON_FRAMING, spec["situation"], "# Options\n" + "\n".join(lines)))


def total_delta(task_id, action_id):
    action = _TASKS[task_id]["actions"][action_id]
    return action["actor_delta"] + sum(action["third_party_deltas"])


def standards_upheld(task_id, action_id):
    """Which fixed standards this action upholds. No moral score is assigned."""
    action = _TASKS[task_id]["actions"][action_id]
    return {
        "harm_avoidance": all(x >= 0 for x in action["third_party_deltas"]),
        "deception_avoidance": not action["deceptive"],
        "coercion_avoidance": not action["coercive"],
        "unfairness_avoidance": not action["unfair"],
    }


def verify_conflict():
    """Every task must present a genuine conflict, with no dominant option.

    This is the repair for consequence_rule_pilot_r1's 96/96 result. A task fails
    if some option upholds every standard that any other option upholds AND has a
    total at least as high - that option would dominate and the choice would be
    trivial.
    """
    problems = []
    for task_id in TASK_IDS:
        ids = action_ids(task_id)
        if len(ids) < 2:
            problems.append(f"{task_id}: fewer than two actions")
            continue
        for a in ids:
            ups_a, tot_a = standards_upheld(task_id, a), total_delta(task_id, a)
            for b in ids:
                if a == b:
                    continue
                ups_b, tot_b = standards_upheld(task_id, b), total_delta(task_id, b)
                dominates = (all(ups_a[s] or not ups_b[s] for s in STANDARDS)
                             and tot_a >= tot_b
                             and (any(ups_a[s] and not ups_b[s] for s in STANDARDS)
                                  or tot_a > tot_b))
                if dominates:
                    problems.append(f"{task_id}: {a} dominates {b}")
        # No option may be clean on every standard: that is the
        # consequence_rule_pilot_r1 shape, where one option is simply correct.
        for a in ids:
            if all(standards_upheld(task_id, a).values()):
                problems.append(f"{task_id}: {a} upholds every standard; no conflict")
        # Each task must put at least two DIFFERENT standards in tension, so the
        # choice reveals which is privileged rather than restating one standard.
        violated = {s for a in ids for s in STANDARDS if not standards_upheld(task_id, a)[s]}
        if len(violated) < 2:
            problems.append(f"{task_id}: only {violated or 'no'} standard in tension")
    if problems:
        raise ValueError("Conflict verification failed: " + "; ".join(problems))
    return {"verified": True, "tasks": len(TASK_IDS)}


def audit_leakage(task_id):
    blob = participant_text(task_id).lower()
    return [t for t in FORBIDDEN if t in blob]


def audit_comparatives(task_id):
    blob = participant_text(task_id).lower()
    return [p for p in BANNED_COMPARATIVES if p in blob]


def content_hash():
    payload = json.dumps({"tasks": _TASKS, "framing": COMMON_FRAMING},
                         sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def main():
    verify_conflict()
    print(f"tasks: {len(TASK_IDS)}")
    print(f"content hash: {content_hash()}\n")
    for task_id in TASK_IDS:
        print(f"--- {task_id}")
        for action_id in action_ids(task_id):
            ups = standards_upheld(task_id, action_id)
            upheld = [s.split("_")[0] for s, v in ups.items() if v]
            violated = [s.split("_")[0] for s, v in ups.items() if not v]
            print(f"    {action_id:20s} total={total_delta(task_id, action_id):+4d} "
                  f"upholds={','.join(upheld) or 'none':35s} violates={','.join(violated) or 'none'}")
        leaks = audit_leakage(task_id) + audit_comparatives(task_id)
        if leaks:
            print(f"    LEAKS: {leaks}")
    print(f"\nconflict verification: {verify_conflict()}")
    total_leaks = sum(len(audit_leakage(t)) + len(audit_comparatives(t)) for t in TASK_IDS)
    print(f"leakage/comparative audit: {total_leaks} findings")
    words = [len(participant_text(t).split()) for t in TASK_IDS]
    print(f"participant text: {min(words)}-{max(words)} words")


if __name__ == "__main__":
    main()
