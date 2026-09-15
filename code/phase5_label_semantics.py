"""Does the PD LABEL carry the meaning, or would any field do?

**The confound this resolves.** `phase4b_permutation_r2` asked whether the
profile is read as parameters or acts as an elaborate formatting cue. It
deranged all ten labels at once and got E-P = +0.089, pooled Holm 0.084 - the
prespecified rule failed, and the caveat stands.

A ten-binding derangement is a blunt instrument. It moves every coordinate
simultaneously, so the contrast is diluted across whatever fraction of the ten
actually carry signal. If one coordinate does most of the work and the
derangement happens to move it somewhere unimportant, a weak gap is exactly what
you would see.

`pd_prospective_r1` then showed where the signal is: PD, manipulated on its own
label, moved the good-rate by **+0.346** (pooled Holm ~0, 6 of 7 items). That
result makes a far sharper control possible.

**The design.** One binding, on a known-active coordinate, against a known-inert
one. Phase 5's integrated analysis measured AW as the weakest coordinate in both
gpt designations (r = -0.051 and -0.167, both Holm 1.000), found it inert, and
confirmed that dropping it changes no conclusion. CLAUDE.md independently flags
AW as preliminary. It is the natural inert partner.

For each agent and each level L in {0.1, 0.9}:

    arm       PD field    AW field    other eight
    TRUE(L)      L          d_aw        drawn
    SWAP(L)     d_aw          L         drawn

Both arms carry the multiset {L, d_aw} across those two fields, so **the two
blocks are numeral-identical**: same length, same line count, same ten numbers,
same field order. The only difference is which of the two labels holds L.

The agent's drawn PD value is discarded in every arm. That is deliberate - it is
what keeps TRUE and SWAP numeral-identical, and it is disclosed rather than
hidden.

**The two contrasts.**

    TRUE(0.9) vs TRUE(0.1)   PD manipulated on the PD label
    SWAP(0.9) vs SWAP(0.1)   the same two numbers manipulated on the AW label

**Predictions, locked before collection.**

  - TRUE should reproduce `pd_prospective_r1`: a large positive effect. If it
    does not, that designation failed to replicate and everything else here is
    uninterpretable - so this arm is also a replication check.
  - SWAP is the test. If the label carries the meaning, SWAP is near zero. If
    any extreme value anywhere in the block does the work, SWAP matches TRUE.

**Why this beats the derangement.** The expected effect is the PD effect
(+0.346), not a diluted average, so the same sample size is far better powered.
And the manipulation is interpretable: one binding, named coordinates, a
directional prediction on each.

**This can fail and the failure is informative.** If SWAP is as large as TRUE,
the model is responding to numeric extremity rather than to the field it sits in,
and the parameter reading is substantially weakened. That is reported as such.
"""
from __future__ import annotations

import hashlib
import json

PARAMETERS = ("LL", "CS", "RT", "MoR", "RE", "PD", "TfA", "ID", "MS", "AW")

ACTIVE = "PD"    # manipulated in pd_prospective_r1 at +0.346, pooled Holm ~0
INERT = "AW"     # Phase 5: r = -0.051 and -0.167, both Holm 1.000, non-load-bearing

LOW, HIGH = 0.1, 0.9


def true_profile(coordinates, level):
    """`level` on the ACTIVE label; the drawn INERT value stays on INERT."""
    _check(coordinates)
    out = dict(coordinates)
    out[ACTIVE] = level
    out[INERT] = coordinates[INERT]
    return out


def swap_profile(coordinates, level):
    """The SAME two numbers, exchanged: `level` on INERT, drawn INERT on ACTIVE.

    Numeral-identical to `true_profile(coordinates, level)` by construction.
    """
    _check(coordinates)
    out = dict(coordinates)
    out[ACTIVE] = coordinates[INERT]
    out[INERT] = level
    return out


def _check(coordinates):
    if set(coordinates) != set(PARAMETERS):
        raise ValueError("Require exactly the ten parameter codes")


def verify_construction(agents):
    """The property the whole design rests on, checked before any call."""
    problems, degenerate = [], []
    for agent in agents:
        c = agent["coordinates"]
        for level in (LOW, HIGH):
            t, s = true_profile(c, level), swap_profile(c, level)
            if sorted(t.values()) != sorted(s.values()):
                problems.append(f"agent {agent['agent']} L={level}: multiset differs")
            if t == s:
                problems.append(f"agent {agent['agent']} L={level}: arms identical")
            # everything outside the two fields must be untouched
            for p in PARAMETERS:
                if p in (ACTIVE, INERT):
                    continue
                if t[p] != c[p] or s[p] != c[p]:
                    problems.append(f"agent {agent['agent']}: {p} changed")
            if t[ACTIVE] != level or s[INERT] != level:
                problems.append(f"agent {agent['agent']} L={level}: level misplaced")
            if t[INERT] != c[INERT] or s[ACTIVE] != c[INERT]:
                problems.append(f"agent {agent['agent']} L={level}: filler misplaced")
        # If the drawn INERT value happens to equal a level, TRUE and SWAP
        # collapse to the same block for that level. Recorded, not excluded.
        if c[INERT] in (LOW, HIGH):
            degenerate.append({"agent": agent["agent"], "aw": c[INERT]})
    if problems:
        raise ValueError("Construction verification failed: " + "; ".join(problems))
    return {"verified": True, "agents": len(agents),
            "active": ACTIVE, "inert": INERT, "levels": [LOW, HIGH],
            "numeral_identical": True,
            "degenerate_agents": degenerate,
            "note": ("TRUE and SWAP carry the identical multiset of numerals, "
                     "block length, format and field order; only which of the two "
                     "labels holds the level differs. The agent's drawn ACTIVE "
                     "value is discarded in every arm to preserve that property, "
                     "which is disclosed rather than hidden.")}


def block_equivalence(render, coordinates, level):
    """Confirm the rendered blocks differ only in the two swapped lines."""
    import re
    a = render(true_profile(coordinates, level))
    b = render(swap_profile(coordinates, level))
    numerals = lambda t: sorted(re.findall(r"\d+\.\d+", t))
    import difflib
    diff = [x for x in difflib.unified_diff(a.splitlines(), b.splitlines(),
                                            lineterm="", n=0)
            if x.startswith(("+", "-")) and not x.startswith(("+++", "---"))]
    named = all(ACTIVE in x or INERT in x or "Procedural" in x or "Affective" in x
                for x in diff) if diff else False
    return {"same_length": len(a) == len(b),
            "same_numerals": numerals(a) == numerals(b),
            "blocks_differ": a != b,
            "diff_lines": len(diff),
            "diff_confined_to_two_fields": named,
            "matched": (len(a) == len(b) and numerals(a) == numerals(b)
                        and a != b and named)}


LOCKED_PREDICTION = {
    "question": ("Does the PD label carry the meaning, or would an extreme value "
                 "in any field do the same work?"),
    "active": ACTIVE, "inert": INERT, "levels": [LOW, HIGH],
    "arms": ["TRUE+ (0.9 on PD)", "TRUE- (0.1 on PD)",
             "SWAP+ (0.9 on AW)", "SWAP- (0.1 on AW)"],
    "primary": ("the SWAP contrast: SWAP+ vs SWAP-, paired within agent and item, "
                "on the share of decisions classifying `good`"),
    "replication_check": ("TRUE+ vs TRUE- should reproduce pd_prospective_r1's "
                          "+0.346. If it does not, that designation failed to "
                          "replicate and the SWAP contrast is uninterpretable."),
    "directional": ("TRUE+ > TRUE-, as in pd_prospective_r1. SWAP is NOT predicted "
                    "directionally: if the label carries the meaning it is near "
                    "zero, and if numeric extremity carries it, it matches TRUE."),
    "interpretation": {
        "swap_near_zero": ("the label-to-value binding carries the effect. The "
                           "permutation caveat is resolved in favour of the "
                           "parameter reading."),
        "swap_matches_true": ("the model responds to numeric extremity rather than "
                              "to the field it sits in. The parameter reading is "
                              "substantially weakened and this is reported as such."),
        "swap_intermediate": ("partial. Reported as measured, with the point "
                              "estimate and interval, and neither reading claimed."),
    },
    "why_this_beats_the_derangement": (
        "phase4b_permutation_r2 moved all ten bindings at once, diluting the "
        "contrast across coordinates that may carry no signal; it measured +0.089 "
        "and failed its rule at pooled Holm 0.084. This moves ONE binding on a "
        "coordinate measured at +0.346, so the expected effect is large and the "
        "same sample size is far better powered."),
    "disclosed": ("The agent's drawn PD value is discarded in every arm. That is "
                  "what makes TRUE and SWAP numeral-identical, and it means this "
                  "designation does not test the drawn PD distribution - it tests "
                  "the label binding at two fixed levels."),
    "null_result_is_informative": True,
    "failure_condition": ("If SWAP is statistically indistinguishable from TRUE, "
                          "the parameter reading is weakened and reported as such, "
                          "not reframed."),
}


def content_hash():
    payload = json.dumps({"active": ACTIVE, "inert": INERT,
                          "levels": [LOW, HIGH],
                          "prediction": LOCKED_PREDICTION},
                         sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def main():
    example = {"LL": 0.41, "CS": 0.83, "RT": 0.19, "MoR": 0.57, "RE": 0.28,
               "PD": 0.22, "TfA": 0.66, "ID": 0.74, "MS": 0.35, "AW": 0.50}
    print("content hash:", content_hash())
    print(f"active={ACTIVE}  inert={INERT}  levels={LOW}/{HIGH}")
    print(f"\nexample agent: drawn {ACTIVE}={example[ACTIVE]}, {INERT}={example[INERT]}")
    print(f"\n{'arm':8s} {ACTIVE:>6s} {INERT:>6s}   numeral multiset over the two fields")
    for level in (HIGH, LOW):
        t, s = true_profile(example, level), swap_profile(example, level)
        tag = "+" if level == HIGH else "-"
        print(f"  TRUE{tag}  {t[ACTIVE]:>6.2f} {t[INERT]:>6.2f}   "
              f"{sorted([t[ACTIVE], t[INERT]])}")
        print(f"  SWAP{tag}  {s[ACTIVE]:>6.2f} {s[INERT]:>6.2f}   "
              f"{sorted([s[ACTIVE], s[INERT]])}")
    print()
    v = verify_construction([{"agent": 0, "coordinates": example}])
    print("construction verified:", v["verified"], "| numeral-identical:",
          v["numeral_identical"])


if __name__ == "__main__":
    main()
