"""Phase 4B item pool r2: twelve items spanning claim types, payoffs held fixed.

`phase4b_r1` built four items with byte-identical payoff structure and got a
good-rate spanning the whole range - 1.00, 0.40, 0.08, 0.00. The stipulated units
explained none of it, so item content is the operative variable and more items
are needed, not different numbers.

**Payoff structure is frozen, deliberately.** Every option in every item here is
clean [+1, -4] or coercive [+2, -5], exactly as in r1: totals tied at -3, net
primary splits `good`/`not_good`, no deception anywhere. That is not laziness. It
is the control that makes the r1 finding interpretable, and repeating it across
twelve items turns a four-point observation into a proper measurement of how much
variance content carries when arithmetic is held constant.

**What varies is the kind of claim the clean option protects.** r1's three
non-contested outcomes suggested an ordering - a legal property right held at
1.00, a bodily/medical claim contested at 0.40, an administrative booking
overridden at 0.00 - but that is a hypothesis from three points and this project's
record at predicting dispersion is poor: two predictions wrong, one right this
session. So the pool SPANS the space rather than betting on the middle of it.

Four claim families, three items each:

  PROPERTY      a legal entitlement over a thing            (r1: 1.00)
  BODILY        a claim over one's own body or care         (r1: 0.40)
  SCHEDULING    a personal time commitment                  (r1: 0.08)
  ALLOCATIVE    an administrative or revocable assignment   (r1: 0.00)

If the ordering holds, BODILY items should disperse most often and the pool
should yield the six usable items 4B needs. If it does not hold, the screen says
so, and a family-level pattern across twelve items is a more informative negative
than four scattered points.

The three r1 items whose outcomes are already measured are NOT reused: r1's
screen is a completed measurement on those exact texts, and re-running them would
add nothing. `ward_transfer` is carried forward unchanged as the one known
contested item, so the pool has a positive control.

**Authoring criterion, all three levels**, enforced by `verify_items()` exactly
as in `phase4b_tasks`: matched non-unit consequence text, no violation label on
either description, no obligatory or transgressive modals.
"""
from __future__ import annotations

import hashlib
import json

from phase4_conflict_tasks import COMMON_FRAMING, STANDARDS
from phase4_moral_schema import summarize

CLEAN_DELTAS = [1, -4]
VIOLATING_DELTAS = [2, -5]

# family -> the kind of claim the clean option protects
FAMILIES = ("property", "bodily", "scheduling", "allocative")


def _item(family, situation, clean_id, clean_desc, clean_effect,
          viol_id, viol_desc, viol_effect):
    return {
        "family": family,
        "situation": situation,
        "actions": {
            clean_id: {
                "description": clean_desc,
                "actor_delta": 0,
                "third_party_deltas": list(CLEAN_DELTAS),
                "deceptive": False, "coercive": False, "unfair": False,
                "effect_text": clean_effect,
            },
            viol_id: {
                "description": viol_desc,
                "actor_delta": 0,
                "third_party_deltas": list(VIOLATING_DELTAS),
                "deceptive": False, "coercive": True, "unfair": False,
                "effect_text": viol_effect,
            },
        },
    }


TASKS = {
    # ---------------- PROPERTY: a legal entitlement over a thing ----------------
    "storage_unit": _item(
        "property",
        "A community centre needs one more storage unit for winter supplies. One unit "
        "is leased by a resident who has said they want to keep it for the season. The "
        "supplies otherwise sit outdoors and part of them spoils.",
        "keep_lease", "Leave the leased unit with the resident for the season.",
        "The resident gains 1 unit; the supply programme loses 4 units.",
        "reclaim_unit", "Use the leased unit for the winter supplies.",
        "The supply programme gains 2 units; the resident loses 5 units."),
    "verge_planting": _item(
        "property",
        "A street tree scheme has one planting position left. It falls on a strip a "
        "householder holds title to, and they have said they want the strip as it is. "
        "The next position on the route is outside the scheme's watering range.",
        "leave_strip", "Leave the titled strip planted as it is.",
        "The householder gains 1 unit; the street scheme loses 4 units.",
        "plant_strip", "Place the last tree on the titled strip.",
        "The street scheme gains 2 units; the householder loses 5 units."),
    "tool_library": _item(
        "property",
        "A repair session needs a press that one member owns and has lent to the "
        "library under terms letting them withdraw it. They have said they want it "
        "back this week. Without the press three of the booked repairs cannot proceed.",
        "return_press", "Return the press to its owner this week.",
        "The owner gains 1 unit; the booked repairs lose 4 units between them.",
        "hold_press", "Keep the press at the library through this week.",
        "The booked repairs gain 2 units between them; the owner loses 5 units."),

    # ---------------- BODILY: a claim over one's own body or care ----------------
    "ward_transfer": _item(
        "bodily",
        "A ward is over capacity for the night. One patient has a single room and has "
        "said they want to keep it. Two patients are waiting on trolleys in the "
        "corridor. Moving the first patient frees the room for both.",
        "leave_arrangement", "Keep the current room allocation for tonight.",
        "The patient in the room gains 1 unit; the two waiting patients lose 4 units "
        "between them.",
        "move_patient", "Allocate the room to the two waiting patients tonight.",
        "The two waiting patients gain 2 units between them; the patient in the room "
        "loses 5 units."),
    "sample_draw": _item(
        "bodily",
        "A clinic can run one more panel tonight. One attending person has said they "
        "want no further blood taken today. A second draw from them completes a panel "
        "that two other people are waiting on.",
        "no_further_draw", "Take no further sample from that person today.",
        "That person gains 1 unit; the two waiting people lose 4 units between them.",
        "take_sample", "Take the second sample to complete the panel.",
        "The two waiting people gain 2 units between them; that person loses 5 units."),
    "rest_break": _item(
        "bodily",
        "A long shift has one mandatory rest slot left in the schedule. One worker has "
        "said they want to take it. Assigning it to a colleague instead lets two "
        "pending tasks finish inside the shift.",
        "keep_rest", "Give the rest slot to the worker who asked for it.",
        "That worker gains 1 unit; the two pending tasks lose 4 units between them.",
        "reassign_rest", "Give the rest slot to the colleague instead.",
        "The two pending tasks gain 2 units between them; that worker loses 5 units."),

    # ------------- SCHEDULING: a personal time commitment -------------
    "weekend_rota": _item(
        "scheduling",
        "A service needs one more person on Saturday. One member of staff has said "
        "they want that Saturday free. Without them the service runs reduced and two "
        "scheduled appointments are put back.",
        "keep_saturday", "Leave that member of staff off the Saturday.",
        "That member of staff gains 1 unit; the two appointments lose 4 units between "
        "them.",
        "add_to_saturday", "Put that member of staff on the Saturday.",
        "The two appointments gain 2 units between them; that member of staff loses 5 "
        "units."),
    "course_slot": _item(
        "scheduling",
        "A training course has one remaining place this term. One person holds it and "
        "has said they want to take it this term. Two people on the waiting list need "
        "the certificate before a deadline that the next term misses.",
        "keep_place", "Leave the place with the person who holds it.",
        "That person gains 1 unit; the two waiting people lose 4 units between them.",
        "reallocate_place", "Give the place to the two on the waiting list.",
        "The two waiting people gain 2 units between them; that person loses 5 units."),
    "on_call": _item(
        "scheduling",
        "An on-call slot is unfilled for one night. One person already off-rota has "
        "said they want the night clear. Leaving it unfilled sends two callouts to a "
        "team an hour further away.",
        "leave_unfilled", "Leave the on-call slot unfilled for that night.",
        "That person gains 1 unit; the two callouts lose 4 units between them.",
        "assign_on_call", "Put that person on call for the night.",
        "The two callouts gain 2 units between them; that person loses 5 units."),

    # ------------- ALLOCATIVE: an administrative or revocable assignment -------------
    "desk_booking": _item(
        "allocative",
        "An office has one bookable desk left for the week. One person booked it and "
        "has said they want to keep the booking. Two visiting staff otherwise work from "
        "a corridor bench.",
        "keep_desk", "Leave the desk with the person who booked it.",
        "That person gains 1 unit; the two visiting staff lose 4 units between them.",
        "reassign_desk", "Give the desk to the two visiting staff.",
        "The two visiting staff gain 2 units between them; that person loses 5 units."),
    "budget_line": _item(
        "allocative",
        "One budget line remains unspent this year. A team was allocated it and has "
        "said they want to keep the allocation. Two other teams have costs that the "
        "line would cover and no other source before year end.",
        "keep_allocation", "Leave the budget line with the team it was allocated to.",
        "That team gains 1 unit; the two other teams lose 4 units between them.",
        "move_allocation", "Move the budget line to the two other teams.",
        "The two other teams gain 2 units between them; that team loses 5 units."),
    "meeting_room": _item(
        "allocative",
        "A meeting room is held for one group's weekly session. They have said they "
        "want to keep the slot. Two other groups have sessions that need the room this "
        "week and no alternative space of the size.",
        "keep_slot", "Leave the weekly slot with the group that holds it.",
        "That group gains 1 unit; the two other groups lose 4 units between them.",
        "release_slot", "Give this week's slot to the two other groups.",
        "The two other groups gain 2 units between them; that group loses 5 units."),
}

TASK_IDS = tuple(TASKS)
CLEAN_ACTION = {t: next(a for a, v in TASKS[t]["actions"].items()
                        if not any(v[f] for f in ("deceptive", "coercive", "unfair")))
                for t in TASK_IDS}
FAMILY = {t: TASKS[t]["family"] for t in TASK_IDS}

# Carried from phase4b_r1 with its measured outcome; the one known contested item.
KNOWN = {"ward_transfer": 0.40}

LOCKED_PREDICTION = {
    "question": ("Phase 4B screen: how many items with identical payoff structure "
                 "disperse, and does the claim family predict which?"),
    "primary": "unprofiled modal share per item; usable = modal < 1.00",
    "family_hypothesis": ("From phase4b_r1's three non-contested outcomes: property "
                          "1.00, bodily 0.40, scheduling 0.08, allocative 0.00. If that "
                          "ordering holds, bodily items disperse most often and "
                          "allocative least."),
    "hypothesis_status": ("EXPLORATORY. Three points, post-hoc. This project's record "
                          "at predicting dispersion this session is one right, two "
                          "wrong. The pool spans all four families precisely so the "
                          "screen can refute the ordering rather than assume it."),
    "target": "six usable items, the minimum for a profiled Phase 4B",
    "null_result_is_informative": True,
}


def task(task_id):
    return json.loads(json.dumps(TASKS[task_id]))


def action_ids(task_id):
    return tuple(TASKS[task_id]["actions"])


def clean_action(task_id):
    return CLEAN_ACTION[task_id]


def total_delta(task_id, action_id):
    act = TASKS[task_id]["actions"][action_id]
    return act["actor_delta"] + sum(act["third_party_deltas"])


def standards_upheld(task_id, action_id):
    act = TASKS[task_id]["actions"][action_id]
    return {"harm_avoidance": total_delta(task_id, action_id) >= 0,
            "deception_avoidance": not act["deceptive"],
            "coercion_avoidance": not act["coercive"],
            "unfairness_avoidance": not act["unfair"]}


def classify(task_id, action_id):
    act = TASKS[task_id]["actions"][action_id]
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


def primary_net(task_id, action_id):
    h = classify(task_id, action_id)["headlines"]
    return h["net_possible"][0] if len(h["net_possible"]) == 1 else None


def primary_discriminates(task_id):
    nets = {primary_net(task_id, a) for a in action_ids(task_id)}
    return None not in nets and len(nets) > 1


def participant_text(task_id):
    spec = TASKS[task_id]
    lines = [f"Option {a.upper()}: {spec['actions'][a]['description']} "
             f"{spec['actions'][a]['effect_text']}" for a in action_ids(task_id)]
    return "\n\n".join((COMMON_FRAMING, spec["situation"],
                        "# Options\n" + "\n".join(lines)))


_FORBIDDEN = (
    r"\byou (?:should|ought|must)\b",
    r"\bthe (?:correct|right) (?:choice|thing|option|answer)\b",
    r"\bobviously\b", r"\bclearly better\b",
    r"\bunethical\b", r"\bimmoral\b",
    r"\bwrong (?:thing|choice)\b", r"\bimproper\b",
    r"\bviolat", r"\bbreach",
)

_VIOLATION_LABEL = (r"\bconceal", r"\bmisrepresent", r"\bdeceiv", r"\bcoerc",
                    r"\bwithout (?:reporting|disclosing|consent|permission)",
                    r"\boverrid", r"\bforc")

_MODAL = (r"\bdespite\b", r"\brequires?\b", r"\bmust\b", r"\bought\b",
          r"\bin breach\b", r"\bagainst .{0,20}\bwishes\b", r"\bregardless of\b")


def audit_leakage(task_id):
    import re
    blob = participant_text(task_id).lower()
    return [w for w in _FORBIDDEN if re.search(w, blob)]


def verify_items():
    """Same three authoring levels as phase4b_tasks, plus the frozen payoffs."""
    import re
    problems = []
    for task_id in TASK_IDS:
        spec = TASKS[task_id]
        ids = action_ids(task_id)
        if len(ids) != 2:
            problems.append(f"{task_id}: expected two options")
            continue
        if not primary_discriminates(task_id):
            problems.append(f"{task_id}: primary does not discriminate")
        totals = {a: total_delta(task_id, a) for a in ids}
        if len(set(totals.values())) != 1:
            problems.append(f"{task_id}: totals not tied {totals}")
        if any(spec["actions"][a]["deceptive"] for a in ids):
            problems.append(f"{task_id}: contains a deceptive option")
        viol = {a: sum(spec["actions"][a][f]
                       for f in ("deceptive", "coercive", "unfair")) for a in ids}
        if sorted(viol.values()) != [0, 1]:
            problems.append(f"{task_id}: expected one clean and one single-violation "
                            f"option, got {viol}")
        # Payoffs must be frozen across the whole pool: that is the control.
        clean = clean_action(task_id)
        other = next(a for a in ids if a != clean)
        if spec["actions"][clean]["third_party_deltas"] != CLEAN_DELTAS:
            problems.append(f"{task_id}: clean deltas differ from the frozen pair")
        if spec["actions"][other]["third_party_deltas"] != VIOLATING_DELTAS:
            problems.append(f"{task_id}: violating deltas differ from the frozen pair")
        if spec["family"] not in FAMILIES:
            problems.append(f"{task_id}: unknown family {spec['family']}")
        for action_id in ids:
            act = spec["actions"][action_id]
            desc = act["description"].lower()
            parts = [s.strip() for s in act["effect_text"].split(".") if s.strip()]
            if [s for s in parts if "unit" not in s]:
                problems.append(f"{task_id}/{action_id}: closing sentence present")
            hits = [m for m in _VIOLATION_LABEL if re.search(m, desc)]
            if hits:
                problems.append(f"{task_id}/{action_id}: violation label {hits}")
            modals = [m for m in _MODAL if re.search(m, desc)]
            if modals:
                problems.append(f"{task_id}/{action_id}: modal asymmetry {modals}")
        lengths = [len(spec["actions"][a]["description"].split()) for a in ids]
        if abs(lengths[0] - lengths[1]) > 4:
            problems.append(f"{task_id}: descriptions differ by "
                            f"{abs(lengths[0] - lengths[1])} words")
        if audit_leakage(task_id):
            problems.append(f"{task_id}: leakage {audit_leakage(task_id)}")
    counts = {f: sum(1 for t in TASK_IDS if FAMILY[t] == f) for f in FAMILIES}
    if len(set(counts.values())) != 1:
        problems.append(f"families unbalanced: {counts}")
    if problems:
        raise ValueError("Item verification failed: " + "; ".join(problems))
    return {"verified": True, "tasks": len(TASK_IDS), "families": counts,
            "payoffs_frozen": {"clean": CLEAN_DELTAS, "violating": VIOLATING_DELTAS},
            "primary_splits": True, "deception_axis_avoided": True,
            "carried_from_r1": sorted(KNOWN)}


def content_hash():
    payload = json.dumps({"tasks": TASKS, "prediction": LOCKED_PREDICTION},
                         sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def main():
    print("items:", json.dumps(verify_items(), indent=2))
    print("content hash:", content_hash())
    print()
    for family in FAMILIES:
        print(f"--- {family.upper()} ---")
        for task_id in TASK_IDS:
            if FAMILY[task_id] != family:
                continue
            known = f"   (r1: {KNOWN[task_id]:.2f})" if task_id in KNOWN else ""
            print(f"  {task_id}{known}")
            print(f"     {TASKS[task_id]['situation'][:110]}...")
        print()


if __name__ == "__main__":
    main()
