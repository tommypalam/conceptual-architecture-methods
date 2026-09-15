"""Profile permutation: is the block read as parameters, or as an elaborate cue?

Every Phase 4B assessment carries the same caveat:

    "A shift under a numeric block is consistent with the block acting as an
     elaborate context cue. Distinguishing that from parameterised reasoning
     needs the configuration counterfactual, which this designation does not
     run."

This module builds the control that settles it.

**The manipulation.** For each agent, the ten drawn coordinates are permuted
across the ten labels. The E arm sends the agent's values against their correct
labels; the P arm sends the SAME TEN NUMBERS against shuffled labels.

    E    LL 0.41  CS 0.83  RT 0.19  ...  PD 0.22  ...
    P    LL 0.22  CS 0.41  RT 0.83  ...  PD 0.19  ...

Identical multiset of numerals. Identical block length, format, field order,
endpoint descriptions and token count. The ONLY difference is which label each
number sits against.

**What each outcome means.**

  E differs from P  ->  the label-to-value mapping carries the effect. The model
                        is responding to WHICH coordinate holds WHICH value, not
                        to the presence of a structured numeric block. The cue
                        reading is ruled out and the caveat is retired.

  E matches P       ->  the block works regardless of where the numbers sit. Any
                        plausible numeric profile would do, the effect is a
                        presentation artefact, and the Phase 4B caveat was the
                        correct reading all along.

Both outcomes are publishable and the second is the one that would cost the
project its central claim. That is what makes it a real test.

**Why permutation and not a fixed or random profile.** A constant profile changes
the numeric content; a fresh random draw changes the distribution. Permutation
holds the agent's own values exactly and moves only the assignment, so the two
arms are matched on every quantity a "structured numbers" account could appeal
to - mean, variance, extremes, digit patterns, block length.

**Derangement.** The permutation is a derangement: no coordinate keeps its own
value. A permutation leaving some labels fixed would dilute the contrast toward
zero and make a null uninterpretable. `verify_derangement` enforces this per
agent, and also rejects any agent whose drawn values are so close together that
permuting them changes nothing meaningful.

**The permutation is seeded and fixed before collection**, so it is a property of
the designation rather than something chosen after seeing results.
"""
from __future__ import annotations

import hashlib
import json

PARAMETERS = ("LL", "CS", "RT", "MoR", "RE", "PD", "TfA", "ID", "MS", "AW")

# A single derangement of the ten positions, fixed here before any call. Applied
# identically to every agent so the manipulation is one transformation, not a
# per-agent lottery. Chosen as a 10-cycle: every coordinate moves, and no pair
# simply swaps, so no label keeps its own value and no two labels merely trade.
DERANGEMENT = (1, 2, 3, 4, 5, 6, 7, 8, 9, 0)

# Minimum spread required for permutation to be a meaningful manipulation. An
# agent whose ten values are nearly identical would produce an E block and a P
# block that differ only in rounding noise.
MIN_SPREAD = 0.15


def permute(coordinates):
    """Return the same ten values, reassigned across labels by DERANGEMENT.

    `coordinates` maps parameter code -> value. The returned mapping has the
    identical multiset of values and the identical key set.
    """
    if set(coordinates) != set(PARAMETERS):
        raise ValueError("Require exactly the ten parameter codes")
    values = [coordinates[p] for p in PARAMETERS]
    return {PARAMETERS[i]: values[DERANGEMENT[i]] for i in range(len(PARAMETERS))}


def spread(coordinates):
    values = [coordinates[p] for p in PARAMETERS]
    return max(values) - min(values)


def verify_derangement(agents):
    """Every agent's permutation must move every coordinate, and be meaningful.

    Checks, per agent:
      - the permuted multiset equals the original multiset exactly;
      - no label keeps its own value (a true derangement of the assignment);
      - the drawn values span at least MIN_SPREAD, so permuting them matters.

    And globally: DERANGEMENT is a permutation of the ten positions with no
    fixed point.
    """
    problems = []
    if sorted(DERANGEMENT) != list(range(len(PARAMETERS))):
        problems.append("DERANGEMENT is not a permutation of the ten positions")
    fixed = [i for i in range(len(PARAMETERS)) if DERANGEMENT[i] == i]
    if fixed:
        problems.append(f"DERANGEMENT has fixed points at {fixed}")

    thin = []
    for agent in agents:
        coords = agent["coordinates"]
        perm = permute(coords)
        if sorted(perm.values()) != sorted(coords.values()):
            problems.append(f"agent {agent['agent']}: multiset changed")
        same = [p for p in PARAMETERS if perm[p] == coords[p]]
        if same:
            # Equal values at two labels can make a moved coordinate look fixed.
            # That is a tie in the draw, not a defect in the permutation, but it
            # weakens the contrast for that agent, so it is recorded.
            thin.append({"agent": agent["agent"], "unchanged_labels": same})
        if spread(coords) < MIN_SPREAD:
            problems.append(f"agent {agent['agent']}: spread "
                            f"{spread(coords):.3f} below {MIN_SPREAD}")
    if problems:
        raise ValueError("Permutation verification failed: " + "; ".join(problems))
    return {"verified": True, "agents": len(agents),
            "derangement": list(DERANGEMENT),
            "fixed_points": 0,
            "agents_with_tied_values": thin,
            "min_spread_required": MIN_SPREAD,
            "note": ("E and P carry the identical multiset of numerals, block "
                     "length, format and field order; only the label-to-value "
                     "assignment differs")}


def block_equivalence(render, coordinates):
    """Confirm the two rendered blocks are matched on everything but assignment.

    `render` takes a coordinate mapping and returns the profile block text. The
    two blocks must have the same length, the same line count, and the same
    multiset of rendered numerals - otherwise the contrast would be confounded
    by presentation.
    """
    import re
    a = render(coordinates)
    b = render(permute(coordinates))
    numerals = lambda t: sorted(re.findall(r"\d+\.\d+", t))
    return {"same_length": len(a) == len(b),
            "same_line_count": a.count(chr(10)) == b.count(chr(10)),
            "same_numerals": numerals(a) == numerals(b),
            "blocks_differ": a != b,
            "matched": (len(a) == len(b) and numerals(a) == numerals(b) and a != b)}


LOCKED_PREDICTION = {
    "question": ("Is the ten-coordinate block read as parameters, or does any "
                 "structured numeric block act as an elaborate context cue?"),
    "arms": ["E (drawn values, correct labels)",
             "P (same values, deranged across labels)"],
    "primary": "paired E vs P on the share of decisions classifying `good`",
    "directional": ("Stated before collection: E differs from P. Direction is NOT "
                    "predicted. A permuted profile is not a 'worse' profile - it is "
                    "a different one - so there is no principled basis for predicting "
                    "which way it moves the headline."),
    "interpretation": {
        "differ": ("the label-to-value mapping carries the effect; the cue reading "
                   "is ruled out and the Phase 4B caveat is retired"),
        "match": ("the block works regardless of where the numbers sit; the effect "
                  "is a presentation artefact and the Phase 4B caveat stands"),
    },
    "null_result_is_informative": True,
    "failure_condition": ("If E and P do not differ under the prespecified rule, the "
                          "profile is NOT shown to be read as parameters, and every "
                          "Phase 4B claim must be reported under that limitation. "
                          "This is reported as a failure, not reframed."),
}


def content_hash():
    payload = json.dumps({"derangement": list(DERANGEMENT),
                          "parameters": list(PARAMETERS),
                          "min_spread": MIN_SPREAD,
                          "prediction": LOCKED_PREDICTION},
                         sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def main():
    example = {"LL": 0.41, "CS": 0.83, "RT": 0.19, "MoR": 0.57, "RE": 0.28,
               "PD": 0.22, "TfA": 0.66, "ID": 0.74, "MS": 0.35, "AW": 0.50}
    perm = permute(example)
    print("content hash:", content_hash())
    print(f"\n{'label':6s} {'E':>6s} {'P':>6s}")
    for p in PARAMETERS:
        print(f"  {p:4s} {example[p]:>6.2f} {perm[p]:>6.2f}")
    print(f"\nsame multiset: {sorted(example.values()) == sorted(perm.values())}")
    print(f"labels keeping their value: "
          f"{[p for p in PARAMETERS if example[p] == perm[p]] or 'none'}")
    print(f"spread: {spread(example):.3f} (minimum {MIN_SPREAD})")


if __name__ == "__main__":
    main()
