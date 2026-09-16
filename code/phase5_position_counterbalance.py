"""Is the effect bound to the LABEL, or to the POSITION the label occupies?

**The gap this closes, and it is a real one.** `label_semantics_r1` moved the
level from the Procedural Dependence line to the Affective Weighting line and the
effect vanished (TRUE +0.339, SWAP -0.036). That was read as showing the effect
belongs to the PD *label*.

It does not show that. In the rendered block PD is **line 6** and AW is **line
10**, so the swap moves the label AND the position together:

    TRUE+    6. Procedural Dependence: 0.90   ...  10. Affective Weighting: 0.50
    SWAP+    6. Procedural Dependence: 0.50   ...  10. Affective Weighting: 0.90

A model that weighted earlier lines more heavily - an ordinary primacy effect -
would produce the entire published result with **no label reading whatsoever**.
Position is a third unexcluded mechanism alongside field-weighted extremity, and
it was not named in the paper's list.

**The design: a 2x2 crossing binding with position.** The block is rendered in
two orders. NORMAL is the canonical order used by every prior designation. In
EXCHANGED, the PD and AW *lines swap places* - AW is printed at position 6 and PD
at position 10 - while every other line stays put. Crossing that with the
TRUE/SWAP binding gives four arms:

    arm   binding   order       level 0.90 sits on   at position
    A     TRUE      normal      PD                   6
    B     SWAP      normal      AW                   10
    C     TRUE      exchanged   PD                   10
    D     SWAP      exchanged   AW                   6

**The two contrasts that matter.** Each holds one factor constant:

    LABEL effect, position held fixed:
        A vs D    both carry 0.90 at position 6   -> differ only in WHICH LABEL
        C vs B    both carry 0.90 at position 10  -> differ only in WHICH LABEL

    POSITION effect, label held fixed:
        A vs C    both put 0.90 on PD             -> differ only in POSITION
        B vs D    both put 0.90 on AW             -> differ only in POSITION

**Predictions, locked before collection.** These are genuinely competing and the
result is not predetermined:

  - If the effect is the LABEL: A > D and C > B, while A is close to C. The
    published reading survives and strengthens.
  - If the effect is POSITION: A > C and D > B, while A is close to D. The
    published reading is WRONG and the paper's central claim must be restated as
    a position effect.
  - If both contribute, both contrasts are non-zero and the effect decomposes.

**Every arm carries the identical numeral multiset, block length and line count.**
Only which label holds 0.90, and at which line, varies. All ten lines are
present in every arm and the other eight parameters never move.

**A null result is informative and a failure is publishable.** If the label
contrast is null while the position contrast is significant, that is a refutation
of this project's own published finding, and it is reported as one rather than
reframed.
"""
from __future__ import annotations

import hashlib
import json

PARAMETERS = ("LL", "CS", "RT", "MoR", "RE", "PD", "TfA", "ID", "MS", "AW")

ACTIVE = "PD"
INERT = "AW"

LOW, HIGH = 0.1, 0.9

# Canonical order, as every prior designation rendered it. PD is 6th, AW 10th.
NORMAL_ORDER = PARAMETERS

# PD and AW exchange line positions; everything else stays put.
def exchanged_order():
    o = list(PARAMETERS)
    i, j = o.index(ACTIVE), o.index(INERT)
    o[i], o[j] = o[j], o[i]
    return tuple(o)


EXCHANGED_ORDER = exchanged_order()

ARMS = {
    "A": {"binding": "TRUE", "order": "normal",    "level_on": ACTIVE, "position": 6},
    "B": {"binding": "SWAP", "order": "normal",    "level_on": INERT,  "position": 10},
    "C": {"binding": "TRUE", "order": "exchanged", "level_on": ACTIVE, "position": 10},
    "D": {"binding": "SWAP", "order": "exchanged", "level_on": INERT,  "position": 6},
}

# Measured in label_semantics_r1, which this designation re-examines.
PUBLISHED = {"true": +0.339, "swap": -0.036,
             "reading": "the label carries the effect",
             "confound": "label and position moved together"}


def profile(coordinates, binding, level):
    """Values per parameter. `binding` selects which label holds `level`."""
    if set(coordinates) != set(PARAMETERS):
        raise ValueError("Require exactly the ten parameter codes")
    out = dict(coordinates)
    if binding == "TRUE":
        out[ACTIVE] = level
        out[INERT] = coordinates[INERT]
    elif binding == "SWAP":
        out[ACTIVE] = coordinates[INERT]
        out[INERT] = level
    else:
        raise ValueError(f"Unknown binding: {binding}")
    return out


def order_for(arm):
    return NORMAL_ORDER if ARMS[arm]["order"] == "normal" else EXCHANGED_ORDER


def arm_profile(coordinates, arm, level):
    """The (values, line order) pair fully specifying one arm's block."""
    if arm not in ARMS:
        raise ValueError(f"Unknown arm: {arm}")
    return profile(coordinates, ARMS[arm]["binding"], level), order_for(arm)


def verify_construction(agents):
    """The properties the 2x2 rests on, checked for every agent."""
    problems, degenerate = [], []
    if set(EXCHANGED_ORDER) != set(PARAMETERS):
        problems.append("exchanged order is not a permutation of the ten")
    if EXCHANGED_ORDER.index(INERT) != NORMAL_ORDER.index(ACTIVE):
        problems.append("exchange did not put INERT at ACTIVE's position")
    if EXCHANGED_ORDER.index(ACTIVE) != NORMAL_ORDER.index(INERT):
        problems.append("exchange did not put ACTIVE at INERT's position")
    moved = [p for p in PARAMETERS
             if NORMAL_ORDER.index(p) != EXCHANGED_ORDER.index(p)]
    if sorted(moved) != sorted([ACTIVE, INERT]):
        problems.append(f"exchange moved more than the two named lines: {moved}")

    for agent in agents:
        c = agent["coordinates"]
        for level in (LOW, HIGH):
            blocks = {}
            for arm in ARMS:
                vals, order = arm_profile(c, arm, level)
                # every arm must carry the same multiset of values
                if sorted(vals.values()) != sorted(profile(c, "TRUE", level).values()):
                    problems.append(f"agent {agent['agent']} arm {arm}: multiset differs")
                # the eight untouched parameters must be unchanged
                for p in PARAMETERS:
                    if p in (ACTIVE, INERT):
                        continue
                    if vals[p] != c[p]:
                        problems.append(f"agent {agent['agent']} arm {arm}: {p} changed")
                # the declared level must sit on the declared label
                if vals[ARMS[arm]["level_on"]] != level:
                    problems.append(f"agent {agent['agent']} arm {arm}: level misplaced")
                # and at the declared position (1-indexed)
                pos = order.index(ARMS[arm]["level_on"]) + 1
                if pos != ARMS[arm]["position"]:
                    problems.append(f"agent {agent['agent']} arm {arm}: "
                                    f"position {pos} != declared {ARMS[arm]['position']}")
                blocks[arm] = tuple((p, vals[p]) for p in order)
            # the four arms must be four DISTINCT blocks
            if len(set(blocks.values())) != 4:
                problems.append(f"agent {agent['agent']} L={level}: arms not distinct")

        # Rendered-precision degeneracy, the lesson from label_semantics_r2.
        rendered = f"{c[INERT]:.2f}"
        if rendered in (f"{LOW:.2f}", f"{HIGH:.2f}"):
            degenerate.append({"agent": agent["agent"], INERT: c[INERT],
                               "rendered": rendered,
                               "why": "collides with a level at rendered precision; "
                                      "TRUE and SWAP become identical for this agent"})
    if degenerate:
        problems.append(f"{len(degenerate)} agent(s) have a drawn {INERT} colliding "
                        f"with a level at rendered precision: {degenerate}. Redraw.")
    if problems:
        raise ValueError("Construction verification failed: " + "; ".join(problems))
    return {"verified": True, "agents": len(agents), "arms": list(ARMS),
            "normal_order": list(NORMAL_ORDER),
            "exchanged_order": list(EXCHANGED_ORDER),
            "lines_moved_by_exchange": sorted(moved),
            "degenerate_agents": degenerate,
            "note": ("All four arms carry the identical numeral multiset, block "
                     "length and line count. Only which label holds the level, "
                     "and at which line, varies. The eight other parameters never "
                     "move in value or in position.")}


LOCKED_PREDICTION = {
    "question": ("Is the label_semantics_r1 effect bound to the PD LABEL, or to "
                 "the POSITION that label occupies in the rendered block?"),
    "why_it_matters": ("In the canonical block PD is line 6 and AW is line 10, so "
                       "label_semantics_r1's swap moved label and position "
                       "TOGETHER. A primacy effect over block lines would produce "
                       "its entire result with no label reading."),
    "arms": ARMS,
    "primary": ("two paired contrasts: the LABEL contrast with position held "
                "fixed (A vs D, and C vs B), and the POSITION contrast with label "
                "held fixed (A vs C, and B vs D), Holm-corrected over all four as "
                "one family"),
    "competing_predictions": {
        "label_carries_it": ("A > D and C > B, with A close to C. The published "
                             "reading survives and is strengthened: position is "
                             "excluded."),
        "position_carries_it": ("A > C and D > B, with A close to D. The published "
                                "reading is WRONG and the paper's central claim "
                                "must be restated as a position effect."),
        "both_contribute": ("both contrasts non-zero; the effect decomposes and "
                            "is reported as decomposed."),
    },
    "published_result_under_test": PUBLISHED,
    "directional": ("The LABEL contrast is predicted POSITIVE if the published "
                    "reading is right, since PD+ produced more `good` decisions. "
                    "The POSITION contrast is NOT predicted directionally."),
    "decision_rule": ("the label binding is declared load-bearing if the pooled "
                      "LABEL contrast clears Holm p < 0.05 with the effect in the "
                      "same direction in at least 4 of 7 items; the position "
                      "factor is declared load-bearing on the same rule applied "
                      "to the POSITION contrast. Both can fire."),
    "failure_condition": ("If the LABEL contrast is null while the POSITION "
                          "contrast is significant, this REFUTES this project's "
                          "own published label-semantics finding. It is reported "
                          "as a refutation, not reframed, and label_semantics_r1 "
                          "is marked superseded with its data intact."),
    "null_result_is_informative": True,
    "no_reroll": "A null is not re-run with more agents.",
    "disclosed": ("The drawn PD value is discarded in every arm, which is what "
                  "keeps the numeral multiset identical. This tests the binding "
                  "at two fixed levels, not the drawn distribution."),
}


def content_hash():
    payload = json.dumps({"arms": ARMS, "normal": list(NORMAL_ORDER),
                          "exchanged": list(EXCHANGED_ORDER),
                          "published": PUBLISHED,
                          "prediction": LOCKED_PREDICTION},
                         sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def main():
    ex = {"LL": 0.41, "CS": 0.83, "RT": 0.19, "MoR": 0.57, "RE": 0.28,
          "PD": 0.22, "TfA": 0.66, "ID": 0.74, "MS": 0.35, "AW": 0.50}
    print("content hash:", content_hash())
    print(f"\nnormal order   : {NORMAL_ORDER}")
    print(f"exchanged order: {EXCHANGED_ORDER}")
    print(f"\nthe 2x2 at L={HIGH} (drawn {INERT}={ex[INERT]}):\n")
    for arm, spec in ARMS.items():
        vals, order = arm_profile(ex, arm, HIGH)
        pos = order.index(spec["level_on"]) + 1
        print(f"  arm {arm}  {spec['binding']:4s} / {spec['order']:9s}  "
              f"{HIGH} on {spec['level_on']:3s} at line {pos:2d}")
    print("\nrendered lines 6 and 10 per arm:")
    for arm in ARMS:
        vals, order = arm_profile(ex, arm, HIGH)
        l6, l10 = order[5], order[9]
        print(f"  arm {arm}:  6. {l6}: {vals[l6]:.2f}   |  10. {l10}: {vals[l10]:.2f}")
    v = verify_construction([{"agent": 0, "coordinates": ex}])
    print("\nverified:", v["verified"], "| lines moved:", v["lines_moved_by_exchange"])
    print(f"\nunder test: label_semantics_r1 TRUE {PUBLISHED['true']:+.3f}, "
          f"SWAP {PUBLISHED['swap']:+.3f}")
    print(f"confound:   {PUBLISHED['confound']}")


if __name__ == "__main__":
    main()
