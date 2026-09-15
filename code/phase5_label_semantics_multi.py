"""Swap controls for ID and LL: does the label carry their effect too?

`coordinate_sweep_r2` found three of ten coordinates load-bearing: PD (+0.339),
ID (+0.143) and LL (-0.131). `label_semantics_r1` then proved the PD effect
belongs to the PD **label** - the same numerals on the inert AW label gave -0.036.

**ID and LL have had no such control.** They are load-bearing *coordinates*, not
demonstrated *label* effects. Every assessment says so explicitly. This module
runs the control that closes the gap.

**The construction, generalised from `phase5_label_semantics`.** For an active
coordinate A, an inert partner I, and a level L in {0.1, 0.9}:

    TRUE(L)   L on A's label,        the drawn I value on I's label
    SWAP(L)   the drawn I value on A, L on I's label

Both arms carry the multiset {L, drawn-I} across those two fields, so the blocks
are **numeral-identical**: same length, same line count, same ten numbers, same
field order. Only which of the two labels holds L differs.

**AW is the inert partner for both**, as it was for PD. It is the only coordinate
measured inert by two independent methods: post-hoc correlation (r = -0.051 and
-0.167, both Holm 1.000) and prospective manipulation (-0.036, Holm 1.000). CS
and RT are also flat in the sweep but have only one measurement each.

**Predictions, locked before collection.**

  - TRUE reproduces the sweep: ID around +0.143, LL around -0.131. If it does
    not, the sweep failed to replicate and the SWAP contrast for that coordinate
    is uninterpretable - so TRUE gates each coordinate separately.
  - SWAP is the test, and is NOT predicted directionally. Near zero means the
    label carries the effect; comparable to TRUE means the model responds to
    numeric extremity wherever it sits.

**A power caution recorded in advance.** PD's effect was +0.339 and its swap
control was well powered. ID (+0.143) and LL (-0.131) are roughly 2.4x smaller,
so the TRUE arms here sit near the edge of what 40 agents can resolve, and a
SWAP null is correspondingly weaker evidence than PD's was. Measured power is in
the protocol; this is stated now rather than after seeing the result.

**Both coordinates run in one designation** so the Holm family covers all four
contrasts together rather than treating each coordinate as its own lucky draw.
"""
from __future__ import annotations

import hashlib
import json

PARAMETERS = ("LL", "CS", "RT", "MoR", "RE", "PD", "TfA", "ID", "MS", "AW")

# Load-bearing in coordinate_sweep_r2, no label control yet.
ACTIVE = ("ID", "LL")

# Inert by two independent measurements. Same partner PD's control used.
INERT = "AW"

LOW, HIGH = 0.1, 0.9

# Measured in coordinate_sweep_r2 at 25 agents; the TRUE arms should reproduce
# these. Recorded so the replication check is against a stated number.
SWEPT_EFFECT = {"ID": +0.143, "LL": -0.131}

# The completed PD control, for reference in the assessment.
PD_REFERENCE = {"true": +0.339, "swap": -0.036,
                "reading": "the label carries the effect"}


def _check(coordinates):
    if set(coordinates) != set(PARAMETERS):
        raise ValueError("Require exactly the ten parameter codes")


def true_profile(coordinates, active, level):
    """`level` on the active label; the drawn inert value stays on the inert one."""
    _check(coordinates)
    if active not in ACTIVE:
        raise ValueError(f"Not an active coordinate here: {active}")
    out = dict(coordinates)
    out[active] = level
    out[INERT] = coordinates[INERT]
    return out


def swap_profile(coordinates, active, level):
    """The same two numbers exchanged: drawn inert on active, `level` on inert.

    Numeral-identical to `true_profile(coordinates, active, level)`.
    """
    _check(coordinates)
    if active not in ACTIVE:
        raise ValueError(f"Not an active coordinate here: {active}")
    out = dict(coordinates)
    out[active] = coordinates[INERT]
    out[INERT] = level
    return out


def verify_construction(agents):
    """The property the design rests on, checked for every agent and coordinate."""
    problems, degenerate = [], []
    if INERT in ACTIVE:
        problems.append("the inert partner is also an active coordinate")
    for agent in agents:
        c = agent["coordinates"]
        for active in ACTIVE:
            for level in (LOW, HIGH):
                t = true_profile(c, active, level)
                s = swap_profile(c, active, level)
                if sorted(t.values()) != sorted(s.values()):
                    problems.append(f"agent {agent['agent']} {active} L={level}: "
                                    "multiset differs")
                if t == s:
                    problems.append(f"agent {agent['agent']} {active} L={level}: "
                                    "arms identical")
                for p in PARAMETERS:
                    if p in (active, INERT):
                        continue
                    if t[p] != c[p] or s[p] != c[p]:
                        problems.append(f"agent {agent['agent']} {active}: {p} changed")
                if t[active] != level or s[INERT] != level:
                    problems.append(f"agent {agent['agent']} {active} L={level}: "
                                    "level misplaced")
                if t[INERT] != c[INERT] or s[active] != c[INERT]:
                    problems.append(f"agent {agent['agent']} {active} L={level}: "
                                    "filler misplaced")
        # Degeneracy must be tested at RENDERED precision, not on the raw draw.
        # The block prints two decimals, so a drawn AW of 0.102 renders as "0.10"
        # and collides with LOW - making TRUE and SWAP byte-identical for that
        # agent at that level, so the swap does nothing. Caught on agent 7 of the
        # first draw, where AW = 0.102.
        rendered = f"{c[INERT]:.2f}"
        if rendered in (f"{LOW:.2f}", f"{HIGH:.2f}"):
            degenerate.append({"agent": agent["agent"], INERT: c[INERT],
                               "rendered": rendered,
                               "why": "collides with a level at rendered precision"})
    if degenerate:
        problems.append(
            f"{len(degenerate)} agent(s) have a drawn {INERT} that collides with a "
            f"level at rendered precision: {degenerate}. Their TRUE and SWAP arms "
            f"are byte-identical at that level, so the swap does nothing and the "
            f"paired contrast is diluted. Redraw the population.")
    if problems:
        raise ValueError("Construction verification failed: " + "; ".join(problems))
    return {"verified": True, "agents": len(agents),
            "active": list(ACTIVE), "inert": INERT, "levels": [LOW, HIGH],
            "numeral_identical": True, "degenerate_agents": degenerate,
            "note": ("For each active coordinate, TRUE and SWAP carry the identical "
                     "multiset of numerals, block length, format and field order; "
                     "only which of the two labels holds the level differs. The "
                     "agent's drawn ACTIVE value is discarded in every arm to "
                     "preserve that property, as in label_semantics_r1.")}


def block_equivalence(render, coordinates, active, level):
    """Confirm the rendered blocks differ only in the two swapped lines."""
    import re
    import difflib
    a = render(true_profile(coordinates, active, level))
    b = render(swap_profile(coordinates, active, level))
    numerals = lambda t: sorted(re.findall(r"\d+\.\d+", t))
    diff = [x for x in difflib.unified_diff(a.splitlines(), b.splitlines(),
                                            lineterm="", n=0)
            if x.startswith(("+", "-")) and not x.startswith(("+++", "---"))]
    return {"same_length": len(a) == len(b),
            "same_numerals": numerals(a) == numerals(b),
            "blocks_differ": a != b,
            "diff_lines": len(diff),
            "matched": (len(a) == len(b) and numerals(a) == numerals(b)
                        and a != b and len(diff) == 4)}


LOCKED_PREDICTION = {
    "question": ("Do the ID and LL labels carry their effects, as the PD label "
                 "does, or would an extreme value in any field do the same work?"),
    "active": list(ACTIVE), "inert": INERT, "levels": [LOW, HIGH],
    "arms_per_coordinate": ["TRUE+", "TRUE-", "SWAP+", "SWAP-"],
    "primary": ("the SWAP contrast per coordinate, paired within agent and item, "
                "Holm-corrected over all four contrasts as one family"),
    "replication_check": ("TRUE should reproduce coordinate_sweep_r2: ID around "
                          "+0.143, LL around -0.131. A coordinate whose TRUE arm "
                          "fails to replicate has an uninterpretable SWAP contrast, "
                          "and that is reported per coordinate."),
    "directional": ("TRUE follows the sweep's measured signs. SWAP is NOT predicted "
                    "directionally."),
    "interpretation": {
        "swap_near_zero": ("the label-to-value binding carries that coordinate's "
                           "effect, as it does for PD"),
        "swap_matches_true": ("the model responds to numeric extremity rather than "
                              "to the field, and that coordinate's result is a "
                              "presentation effect"),
    },
    "power_caution": ("PD's effect was +0.339 and its swap control was well "
                      "powered. ID (+0.143) and LL (-0.131) are roughly 2.4x "
                      "smaller, so the TRUE arms sit near the edge of what 40 "
                      "agents resolve and a SWAP null is weaker evidence here than "
                      "it was for PD. Recorded before collection."),
    "disclosed": ("The agent's drawn ACTIVE value is discarded in every arm, which "
                  "is what keeps TRUE and SWAP numeral-identical. This tests the "
                  "label binding at two fixed levels, not the drawn distribution."),
    "null_result_is_informative": True,
    "failure_condition": ("If a coordinate's SWAP is indistinguishable from its "
                          "TRUE, that coordinate's effect is a presentation effect "
                          "and is reported as such, not reframed."),
}


def content_hash():
    payload = json.dumps({"active": list(ACTIVE), "inert": INERT,
                          "levels": [LOW, HIGH], "swept": SWEPT_EFFECT,
                          "prediction": LOCKED_PREDICTION},
                         sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def main():
    example = {"LL": 0.41, "CS": 0.83, "RT": 0.19, "MoR": 0.57, "RE": 0.28,
               "PD": 0.22, "TfA": 0.66, "ID": 0.74, "MS": 0.35, "AW": 0.50}
    print("content hash:", content_hash())
    print(f"active={ACTIVE}  inert={INERT}  levels={LOW}/{HIGH}")
    print(f"\ndrawn {INERT}={example[INERT]}\n")
    for active in ACTIVE:
        print(f"{active} (swept effect {SWEPT_EFFECT[active]:+.3f}):")
        for level in (HIGH, LOW):
            t = true_profile(example, active, level)
            s = swap_profile(example, active, level)
            tag = "+" if level == HIGH else "-"
            print(f"   TRUE{tag}  {active}={t[active]:.2f} {INERT}={t[INERT]:.2f}   "
                  f"SWAP{tag}  {active}={s[active]:.2f} {INERT}={s[INERT]:.2f}   "
                  f"same multiset: {sorted([t[active], t[INERT]]) == sorted([s[active], s[INERT]])}")
        print()
    v = verify_construction([{"agent": 0, "coordinates": example}])
    print("verified:", v["verified"], "| numeral-identical:", v["numeral_identical"])
    print(f"\nPD reference: TRUE {PD_REFERENCE['true']:+.3f}, "
          f"SWAP {PD_REFERENCE['swap']:+.3f} -> {PD_REFERENCE['reading']}")


if __name__ == "__main__":
    main()
