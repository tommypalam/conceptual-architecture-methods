"""Which of the ten coordinates are causally load-bearing?

`pd_prospective_r1` showed PD moves the deterministic good/bad headline by +0.346
when pinned to its endpoints. `label_semantics_r1` then showed the effect belongs
to the PD *label*: the same numerals on the inert AW label give -0.036.

Together those established a **validated method** - pin one coordinate to 0.1 and
0.9, hold the other nine identical, and measure the paired contrast. This module
applies it to the remaining eight.

**The eight.** PD and AW are excluded: both were tested at 40 agents in
`label_semantics_r1`, PD at +0.339 (Holm ~0) and AW at -0.036 (Holm 1.000).
Re-testing them would spend budget to re-derive known results.

    LL  Legitimacy Locus          CS  Constraint Sensitivity
    RT  Response Threshold        MoR Mode of Response
    RE  Relational Embedding      TfA Tolerance for Asymmetry
    ID  Internalisation Dependence MS Moral Scope

**The design, identical in form to the PD test.** For each coordinate C and each
agent, two arms:

    C-    the agent's drawn profile with C pinned to 0.1
    C+    the agent's drawn profile with C pinned to 0.9

The nine other coordinates are drawn once per agent and held IDENTICAL between
the two arms, so the system prompts differ by exactly one line. Paired within
agent and item.

**No directional prediction per coordinate.** The PD prediction was derivable
because every item presents a claim under a stated arrangement, which maps onto
PD's process/outcome definition. No comparable mapping exists for the other
eight: nothing in these items is specifically about legitimacy locus or moral
scope. Predicting directions without grounds would be decoration, so the test is
**two-sided** and the prespecified rule requires only a difference.

**A survivor here is not yet a label result.** This measures whether pinning a
coordinate on its own label moves the outcome. Proving the LABEL carries it -
rather than the numeral - needs the swap control `label_semantics_r1` ran for PD.
That is the correct follow-up for coordinates that survive, and is deliberately
not run for all eight in advance.

**Holm correction is over the whole sweep.** Eight pooled contrasts in one
family. A coordinate that clears that bar has cleared a genuinely multiple-
comparison-corrected test, which is the point of running them together rather
than one at a time.

**Items are NOT trimmed.** Three of the seven showed small effects under the PD
manipulation. Cutting them would save ~40% and would be outcome-driven selection,
biasing the sweep toward coordinates that behave like PD. All seven are retained,
and that decision is recorded in the 17 September ceiling amendment.
"""
from __future__ import annotations

import hashlib
import json

PARAMETERS = ("LL", "CS", "RT", "MoR", "RE", "PD", "TfA", "ID", "MS", "AW")

# Tested at 40 agents in label_semantics_r1; excluded to avoid re-deriving.
ALREADY_TESTED = {
    "PD": {"effect": +0.339, "holm": 0.0, "verdict": "load-bearing"},
    "AW": {"effect": -0.036, "holm": 1.0, "verdict": "inert"},
}

SWEPT = tuple(p for p in PARAMETERS if p not in ALREADY_TESTED)

LOW, HIGH = 0.1, 0.9


def pin(coordinates, coordinate, level):
    """The agent's drawn profile with one coordinate overwritten."""
    if set(coordinates) != set(PARAMETERS):
        raise ValueError("Require exactly the ten parameter codes")
    if coordinate not in PARAMETERS:
        raise ValueError(f"Unknown coordinate: {coordinate}")
    out = dict(coordinates)
    out[coordinate] = level
    return out


def verify_sweep(agents):
    """Each coordinate's two arms must differ in that coordinate and nothing else."""
    problems = []
    if set(SWEPT) | set(ALREADY_TESTED) != set(PARAMETERS):
        problems.append("swept and already-tested sets do not partition the ten")
    if len(SWEPT) != 8:
        problems.append(f"expected eight swept coordinates, got {len(SWEPT)}")
    for agent in agents:
        c = agent["coordinates"]
        for coordinate in SWEPT:
            lo, hi = pin(c, coordinate, LOW), pin(c, coordinate, HIGH)
            if lo[coordinate] != LOW or hi[coordinate] != HIGH:
                problems.append(f"agent {agent['agent']} {coordinate}: level misplaced")
            for p in PARAMETERS:
                if p == coordinate:
                    continue
                if lo[p] != c[p] or hi[p] != c[p]:
                    problems.append(f"agent {agent['agent']} {coordinate}: {p} changed")
            if lo == hi:
                problems.append(f"agent {agent['agent']} {coordinate}: arms identical")
    if problems:
        raise ValueError("Sweep verification failed: " + "; ".join(problems))
    return {"verified": True, "swept": list(SWEPT), "agents": len(agents),
            "levels": [LOW, HIGH],
            "excluded": {k: v for k, v in ALREADY_TESTED.items()},
            "note": ("Each coordinate's two arms differ in that coordinate alone; "
                     "the nine others are drawn once per agent and held identical.")}


LOCKED_PREDICTION = {
    "question": ("Which of the remaining eight coordinates move the deterministic "
                 "good/bad headline when pinned to their endpoints?"),
    "swept": list(SWEPT),
    "excluded": ALREADY_TESTED,
    "levels": [LOW, HIGH],
    "primary": ("per coordinate, the paired C+ vs C- contrast on the share of "
                "decisions classifying `good`, Holm-corrected over all eight "
                "pooled contrasts as one family"),
    "directional": ("NONE. The PD direction was derivable because every item "
                    "presents a claim under a stated arrangement, mapping onto "
                    "PD's process/outcome definition. No comparable mapping exists "
                    "for these eight, so the test is two-sided and the rule "
                    "requires only a difference."),
    "decision_rule": ("a coordinate is declared load-bearing if its pooled Holm "
                      "p < 0.05 AND its effect points the same direction in at "
                      "least 4 of 7 items"),
    "what_a_survivor_means": ("that pinning the coordinate on its own label moves "
                              "the outcome. It does NOT yet show the LABEL carries "
                              "it rather than the numeral; that needs the swap "
                              "control label_semantics_r1 ran for PD, which is the "
                              "correct follow-up for survivors."),
    "expected_outcome": ("Phase 5's post-hoc correlations found no coordinate "
                         "besides PD surviving Holm in any designation, and no "
                         "stable ordering across designations. A null across all "
                         "eight is a plausible and informative result."),
    "null_result_is_informative": True,
    "failure_condition": ("If no coordinate survives, the finding is that PD is "
                          "the only load-bearing coordinate of the ten under this "
                          "method, on this item set and model. Reported as such, "
                          "not reframed."),
    "items_not_trimmed": ("Three of the seven items showed small effects under the "
                          "PD manipulation. They are RETAINED. Cutting them would "
                          "save ~40% and would bias the sweep toward coordinates "
                          "behaving like PD."),
}


def content_hash():
    payload = json.dumps({"swept": list(SWEPT), "levels": [LOW, HIGH],
                          "excluded": ALREADY_TESTED,
                          "prediction": LOCKED_PREDICTION},
                         sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def main():
    print("content hash:", content_hash())
    print(f"swept: {len(SWEPT)} coordinates -> {', '.join(SWEPT)}")
    print(f"excluded (already tested at 40 agents in label_semantics_r1):")
    for k, v in ALREADY_TESTED.items():
        print(f"   {k}: effect {v['effect']:+.3f}  Holm {v['holm']}  -> {v['verdict']}")
    print(f"\nlevels: {LOW} / {HIGH}, two arms per coordinate")
    example = {p: 0.5 for p in PARAMETERS}
    v = verify_sweep([{"agent": 0, "coordinates": example}])
    print("verified:", v["verified"])


if __name__ == "__main__":
    main()
