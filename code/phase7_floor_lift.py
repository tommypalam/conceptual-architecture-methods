"""Stage 3a, one-directional: does PD lift a twin off the floor, as a status-quo dial would?

`probe_fields_r1` raised the live worry: an invented "existing arrangements stand"
field (+0.400) matched Procedural Dependence (+0.339), so PD may be functioning as
a status-quo dial rather than as anything about process. `defeasibility_screen_r1`
and `_r2` tried to settle it with twins the model splits on and could not build
them: eleven wordings across two designations put three items on a floor of
0.00-0.04 unprofiled keep, and the rest failed an order check.

**The floor is not an obstacle here; it is the instrument.** This project has
recorded that a deterministic baseline makes detection one-directional, not
impossible. On a floored twin the two readings of PD still differ:

    DIAL     "PD high -> keep what exists". Raising PD should LIFT the keep-rate
             off the floor, as raising Status-quo Preference should.
    PROCESS  a process-dominant agent has no reason to protect an arrangement that
             went around its own procedure. The keep-rate STAYS on the floor.

**Status-quo Preference is the positive control.** It is the field whose entire
content is "existing arrangements stand", it moved these items +0.400 on the base
versions, and if IT cannot lift the twins then nothing can and the designation
reports an uninformative floor rather than a PD result.

**The design.** Two fields x two levels x two item versions, 40 agents:

    field  PD  (Procedural Dependence, entry 6, canonical gloss)
           SQ  (Status-quo Preference, entry 10, from phase7_probe_fields)
    level  0.10 / 0.90
    版本   BASE  the seven screened items
           TWIN  their r1 twins - reviewed and accepted, byte-identical options

Eight cells. The BASE arms are the replication gate and the reference: PD's effect
there is known (+0.339) and SQ's is known (+0.400), so a failure to reproduce them
invalidates the twin arms before they are read.

**The three floored twins carry the test** (`storage_unit`, `tool_library`,
`rest_break`; unprofiled keep 0.00, 0.00, 0.04). They are also the three where PD's
BASE effect is largest (+0.400, +0.675, +0.800), so the design asks the sharpest
available question: does the field that moves these items most on the base version
move them at all once the arrangement went around its procedure?

**Power**, simulated at a 0.02 floor, 40 agents x 3 items, one-sided, Holm over
four: +0.20 lift 200/200, +0.15 194/200, +0.10 148/200, **+0.05 44/200**, zero
false positives. A NULL therefore bounds the lift below about 0.10 and does NOT
establish zero.

**Locked readings.** Let L(field) be the paired lift on the three floored twins.

    PD_IS_NOT_A_DIAL   L(SQ) clears the gate and L(PD) does not, with the direct
                       difference L(SQ) - L(PD) excluding zero
    PD_IS_A_DIAL       both lift, and L(SQ) - L(PD) includes zero
    UNINFORMATIVE      L(SQ) does not clear the gate: the floor cannot be lifted
                       by any field tested, so PD's null says nothing

The primary quantity is the DIRECT difference L(SQ) - L(PD) with a unit-bootstrap
interval - not one arm clearing a threshold while the other does not, the inference
this project withdrew once already over ID.

**What no outcome establishes.** Understanding; that PD encodes procedural justice;
anything about models or items outside these. PD_IS_NOT_A_DIAL would establish that
PD and a pure status-quo field come apart on items where an arrangement bypassed
its procedure - a dissociation, which is stronger than anything in the thesis and
still not understanding.
"""
from __future__ import annotations

import hashlib
import json

import phase7_block_variants as BV
import phase7_probe_fields as PF
import phase7_defeasibility_items as D1
import phase4b_perm_pool as P

PD_SLOT = "PD"
SQ_SLOT = PF.SLOT              # AW's entry, renamed by the probe
SQ_PROBE = "SQ"
LOW, HIGH = 0.1, 0.9
FIELDS = ("PD", "SQ")
VERSIONS = ("BASE", "TWIN")
CELLS = tuple(f"{f}:{v}{s}" for f in FIELDS for v in VERSIONS for s in ("+", "-"))

# Unprofiled keep-share of each r1 twin (defeasibility_screen_r1). The three at or
# near zero are the floored set that carries the test.
TWIN_FLOOR = {"desk_booking": 0.84, "meeting_room": 0.52, "on_call": 0.52,
              "weekend_rota": 0.44, "rest_break": 0.00, "storage_unit": 0.00,
              "tool_library": 0.00}
FLOORED = tuple(t for t, v in sorted(TWIN_FLOOR.items()) if v <= 0.10)
# PD's effect on the BASE version of each item (semantics_r1 CANON).
BASE_PD_EFFECT = {"rest_break": 0.800, "tool_library": 0.675, "storage_unit": 0.400,
                  "desk_booking": 0.225, "weekend_rota": 0.175, "meeting_room": 0.150,
                  "on_call": -0.050}
GATE_REFERENCE = {"PD:BASE": +0.3393, "SQ:BASE": +0.4000}


def pin(coordinates, field, level):
    """The drawn profile with ONE field overwritten. The other nine keep their draw."""
    if set(coordinates) != set(BV.PARAMETERS):
        raise ValueError("Require exactly the ten parameter codes")
    out = dict(coordinates)
    out[PD_SLOT if field == "PD" else SQ_SLOT] = level
    return out


def block_for(render_block, coordinates, field, level):
    """PD keeps the canonical block; SQ renames entry 10 and swaps in its gloss."""
    block = render_block(pin(coordinates, field, level))
    return block if field == "PD" else PF.probe_block(block, SQ_PROBE)


def body(task_id, version, first):
    situation = (P.task(task_id)["situation"] if version == "BASE"
                 else D1.TWIN_SITUATION[task_id])
    return D1.body(task_id, version == "TWIN", first) if version == "TWIN" else \
        D1.body(task_id, False, first)


def verify_construction(render_block, agents):
    """Every property the design rests on, against the real renderer."""
    problems = []
    for agent in agents:
        c = agent["coordinates"]
        for field in FIELDS:
            lo, hi = (block_for(render_block, c, field, L) for L in (LOW, HIGH))
            a, b = lo.split("\n"), hi.split("\n")
            diff = [k for k, (x, y) in enumerate(zip(a, b)) if x != y]
            if len(a) != len(b) or len(diff) != 1:
                problems.append(f"agent {agent['agent']} {field}: {len(diff)} lines differ, expected 1")
            if len(lo) != len(hi):
                problems.append(f"agent {agent['agent']} {field}: levels differ in length")
            entry = "Procedural Dependence" if field == "PD" else PF.PROBES[SQ_PROBE]["name"]
            if hi.count(f"{entry}: 0.90") != 1:
                problems.append(f"agent {agent['agent']} {field}: entry not rendered as designed")
        # The two fields must move DIFFERENT entries, and each must leave the other alone.
        pd_hi = block_for(render_block, c, "PD", HIGH)
        sq_hi = block_for(render_block, c, "SQ", HIGH)
        if "Procedural Dependence" not in sq_hi:
            problems.append(f"agent {agent['agent']}: SQ arm lost the PD entry")
        if "Affective Weighting" in sq_hi or "Status-quo Preference" in pd_hi:
            problems.append(f"agent {agent['agent']}: field slots crossed")
    # Item versions differ only in the situation paragraph.
    for t in P.TASK_IDS:
        for first in (True, False):
            b, w = body(t, "BASE", first), body(t, "TWIN", first)
            if b.split("# Options")[1] != w.split("# Options")[1]:
                problems.append(f"{t}: BASE and TWIN differ beyond the situation")
            if b == w:
                problems.append(f"{t}: TWIN text equals BASE text")
    if problems:
        raise ValueError("Construction verification failed: " + "; ".join(problems[:6]))
    return {"verified": True, "agents": len(agents), "cells": list(CELLS),
            "floored_twins": list(FLOORED),
            "note": ("Within a field the two levels differ on one line and are equal in "
                     "length; PD moves entry 6 and SQ entry 10, neither touching the "
                     "other; BASE and TWIN differ only in the situation paragraph.")}


LOCKED_PREDICTION = {
    "question": ("On twins where an arrangement went around its own procedure and the "
                 "unprofiled keep-rate is on the floor, does Procedural Dependence lift "
                 "it - as a pure status-quo field does - or leave it there?"),
    "fields": {"PD": "Procedural Dependence, entry 6, canonical gloss",
               "SQ": "Status-quo Preference, entry 10 (phase7_probe_fields)"},
    "levels": [LOW, HIGH], "versions": list(VERSIONS),
    "floored_twins": list(FLOORED), "twin_unprofiled_keep": TWIN_FLOOR,
    "base_pd_effect_semantics_r1": BASE_PD_EFFECT,
    "effect_definition": ("paired difference in the share choosing the base item's KEEP "
                          "option, printed 0.90 minus printed 0.10, by agent and item"),
    "gate": ("BOTH base arms must reproduce their known effects (one-sided, Holm over the "
             "four base contrasts, 4+ of 7 items positive): PD ~ +0.34, SQ ~ +0.40. If "
             "either fails, the twin arms are not interpreted."),
    "primary": ("L(SQ) - L(PD) on the floored twins, a within-unit difference with a 95% "
                "unit-bootstrap interval. NOT one arm clearing a threshold while the "
                "other does not - the inference withdrawn over ID."),
    "readings": {
        "PD_IS_NOT_A_DIAL": ("L(SQ) lifts the floor and L(PD) does not, with "
                             "L(SQ) - L(PD) excluding zero"),
        "PD_IS_A_DIAL": "both lift and L(SQ) - L(PD) includes zero",
        "UNINFORMATIVE": ("L(SQ) does not lift the floor: no field tested can, so PD's "
                          "null says nothing"),
    },
    "power": {"simulated_at_floor_0.02": {"+0.20": "200/200", "+0.15": "194/200",
                                          "+0.10": "148/200", "+0.05": "44/200"},
              "false_positive": "0/200",
              "consequence": ("a null bounds the lift below about 0.10 and does NOT "
                              "establish zero")},
    "not_established_by_any_outcome": [
        "understanding, or that PD encodes procedural justice",
        "anything about models or items outside these seven and gpt-5.4-mini",
        "that the twins are morally different from the base items - no twin option is "
        "classified, and the floor is consistent with simple salience of the clause",
    ],
    "no_reroll": "No cell is re-run with more agents after the results are seen.",
}


def content_hash():
    payload = json.dumps({"fields": FIELDS, "levels": [LOW, HIGH], "versions": VERSIONS,
                          "floored": FLOORED, "prediction": LOCKED_PREDICTION},
                         sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()
