"""Does ID's effect exist outside the calibration model?

**Every ID measurement in this project is `gpt-5.4-mini`.** The post-hoc
correlation (+0.303), the pinned sweep (+0.143) and the swap control (+0.111)
are three measurements on one model. `label_semantics_r2` verified ID as a
*label* effect - the same numerals on the inert AW label gave +0.046, n.s. - but
verified it on the calibration model only.

That is the largest remaining hole in the coordinate claim. The architecture-level
result is already two-provider (`phase4b_profiled_r1` on haiku +0.171,
`phase4b_gpt_r2` on gpt +0.228). The *coordinate*-level result is not.

**The design, identical in form to the PD and sweep tests.** For each agent:

    ID-   the agent's drawn profile with ID pinned to 0.1
    ID+   the agent's drawn profile with ID pinned to 0.9

The nine other coordinates are drawn once per agent and held IDENTICAL between
the two arms, so the system prompts differ by exactly one line. Paired within
agent and item.

**The item set is haiku's, not gpt's.** `phase4b_profiled_r1` screened six items
that disperse on haiku; `haiku_screen_r4`'s six alternative items all returned
modal share 1.00 and are unusable. Those two sets are NOT the same as gpt's seven:
`ward_transfer` is haiku-only, and `on_call`/`rest_break` are gpt-only. Four items
overlap. This is therefore **ID tested on haiku's dispersing items**, not a
byte-identical repetition of the gpt designation, and it is reported that way.

**Endpoints only - no swap control, and that is a power decision, not a saving.**
Simulated against haiku's MEASURED per-item baselines, a four-arm swap design at
40 agents gives 14/20 at ID's gpt effect size, against 16/20 for the two-arm
design, because the Holm family is four times larger. A TRUE arm that fails
leaves the SWAP arms uninterpretable - exactly what happened to LL in
`label_semantics_r2`. Running an underpowered swap would manufacture that
outcome by design. So this designation asks the prior question only: does ID move
the outcome on haiku at all? A swap control on haiku is the correct follow-up
*if* this succeeds, and is deliberately not run in advance.

**Power is marginal and is stated before collection, not after.** Against the
measured haiku E-arm baselines, 40 agents over six items gives:

    true effect  +0.080   14/20
    true effect  +0.111   16/20   <- ID's measured gpt effect
    true effect  +0.143   18/20
    true effect  +0.200   19/20
    true effect   0.000    1/20   <- false positive rate

16/20 is 80%. **A null here is therefore a weak null**, and will be reported with
that number in the same sentence. Two of the six items sit near a bound in one
arm (`tool_library` 0.90 in E, `storage_unit` 0.04 in U), which compresses the
detectable range; adding agents does not fix that, which is why 60 agents was not
chosen instead.

**No directional prediction.** ID had no theory-derived direction on gpt either -
the sweep was two-sided and its observed sign is descriptive. Importing gpt's
sign to set expectations on haiku would be precisely the post-hoc move this
project keeps refusing, and would convert a fresh test into a confirmation. The
test is **two-sided** and the prespecified rule requires only a difference.

**A null is a real finding.** If ID does not move the outcome on haiku at 80%
power, the verified coordinate map is "two of ten, on one model", and that
scoping belongs in the paper rather than in a reviewer's report.
"""
from __future__ import annotations

import hashlib
import json

PARAMETERS = ("LL", "CS", "RT", "MoR", "RE", "PD", "TfA", "ID", "MS", "AW")

# The coordinate under test. Verified as a label effect on gpt, never measured
# on any other model.
ACTIVE = "ID"

LOW, HIGH = 0.1, 0.9

# Measured on gpt across three designations. Recorded so the cross-model
# comparison is against stated numbers rather than remembered ones.
GPT_MEASURED = {
    "post_hoc_correlation": +0.303,   # integrated_20260916, E arm, unmanipulated
    "coordinate_sweep_r2": +0.143,    # 25 agents, pinned, Holm 0.00056
    "label_semantics_r2_true": +0.111,  # 40 agents, pinned, Holm 0.00467
    "label_semantics_r2_swap": +0.046,  # 40 agents, same numerals on AW, n.s.
}

# The architecture-level result that IS already cross-model, for contrast.
ARCHITECTURE_CROSSMODEL = {
    "haiku": +0.171,   # phase4b_profiled_r1, paired E-G, Holm 0.000112
    "gpt": +0.228,     # phase4b_gpt_r2, paired E-G, Holm ~0
}


def pin(coordinates, level):
    """The agent's drawn profile with ID overwritten. Nothing else moves."""
    if set(coordinates) != set(PARAMETERS):
        raise ValueError("Require exactly the ten parameter codes")
    out = dict(coordinates)
    out[ACTIVE] = level
    return out


def verify_construction(agents):
    """The two arms must differ in ID and nothing else, for every agent."""
    problems, degenerate = [], []
    for agent in agents:
        c = agent["coordinates"]
        lo, hi = pin(c, LOW), pin(c, HIGH)
        if lo[ACTIVE] != LOW or hi[ACTIVE] != HIGH:
            problems.append(f"agent {agent['agent']}: level misplaced")
        for p in PARAMETERS:
            if p == ACTIVE:
                continue
            if lo[p] != c[p] or hi[p] != c[p]:
                problems.append(f"agent {agent['agent']}: {p} changed")
        if lo == hi:
            problems.append(f"agent {agent['agent']}: arms identical")
        # Degeneracy at RENDERED precision, the lesson from label_semantics_r2
        # where a drawn AW of 0.102 rendered as "0.10" and collided with a level.
        # Here the drawn ID value is DISCARDED in both arms, so a collision
        # cannot make the arms identical - but it is checked and recorded anyway,
        # because a drawn ID equal to a level means that agent contributes a
        # pairing the profile would have produced on its own.
        rendered = f"{c[ACTIVE]:.2f}"
        if rendered in (f"{LOW:.2f}", f"{HIGH:.2f}"):
            degenerate.append({"agent": agent["agent"], ACTIVE: c[ACTIVE],
                               "rendered": rendered,
                               "why": ("drawn value coincides with a pinned level; "
                                       "harmless here because the drawn value is "
                                       "overwritten in BOTH arms, but recorded")})
    if problems:
        raise ValueError("Construction verification failed: " + "; ".join(problems))
    return {"verified": True, "agents": len(agents), "active": ACTIVE,
            "levels": [LOW, HIGH], "coincident_draws": degenerate,
            "note": ("Each agent's two arms differ in the ID line alone; the nine "
                     "other coordinates are drawn once per agent and held "
                     "identical. The drawn ID value is overwritten in both arms.")}


def block_equivalence(render, coordinates):
    """Confirm the rendered blocks differ only in the one ID line."""
    import difflib
    a = render(pin(coordinates, LOW))
    b = render(pin(coordinates, HIGH))
    diff = [x for x in difflib.unified_diff(a.splitlines(), b.splitlines(),
                                            lineterm="", n=0)
            if x.startswith(("+", "-")) and not x.startswith(("+++", "---"))]
    same_lines = len(a.splitlines()) == len(b.splitlines())
    return {"blocks_differ": a != b, "diff_lines": len(diff),
            "same_line_count": same_lines,
            "matched": a != b and len(diff) == 2 and same_lines}


# Measured against haiku's per-item E-arm baselines from phase4b_profiled_r1,
# 20 seeds, Holm family of 1. Recorded here BEFORE collection.
MEASURED_POWER = {
    "baselines_source": ("phase4b_profiled_r1 E arm, per item, on "
                         "claude-haiku-4-5-20251001"),
    "agents": 40, "items": 6, "seeds": 20, "holm_family": 1,
    "0.080": "14/20", "0.111": "16/20", "0.143": "18/20", "0.200": "19/20",
    "0.000_false_positive": "1/20",
    "swap_design_rejected": ("a four-arm swap at 40 agents gives 14/20 at +0.111 "
                             "because the Holm family is 4x larger; an "
                             "underpowered TRUE arm would render the SWAP arms "
                             "uninterpretable by design, as happened to LL"),
    "honest_reading": ("16/20 is 80%. A null from this designation is a WEAK null "
                       "and will be reported with this number in the same "
                       "sentence. Two of six items sit near a bound in one arm, "
                       "which compresses the detectable range; more agents does "
                       "not fix that."),
}


LOCKED_PREDICTION = {
    "question": ("Does pinning ID to its endpoints move the deterministic "
                 "good/bad headline on a model other than the calibration model?"),
    "active": ACTIVE, "levels": [LOW, HIGH], "arms": ["ID-", "ID+"],
    "model": "claude-haiku-4-5-20251001",
    "items": ("haiku's six dispersing items from phase4b_profiled_r1, NOT gpt's "
              "seven. Four overlap; ward_transfer is haiku-only; on_call and "
              "rest_break are gpt-only. This is ID tested on haiku's items, not a "
              "byte-identical repetition of the gpt designation."),
    "primary": ("the paired ID+ vs ID- contrast on the share of decisions "
                "classifying `good`, pooled across items, paired within agent "
                "and item"),
    "directional": ("NONE. Two-sided. ID had no theory-derived direction on gpt "
                    "either; its observed sign there is descriptive. Importing "
                    "that sign to set expectations here would convert a fresh "
                    "test into a confirmation."),
    "decision_rule": ("ID is declared to move the outcome on haiku if the pooled "
                      "p < 0.05 AND the effect points the same direction in at "
                      "least 4 of 6 items"),
    "gpt_reference": GPT_MEASURED,
    "power": MEASURED_POWER,
    "interpretation": {
        "replicates_same_sign": ("ID's effect is not specific to the calibration "
                                 "model. The verified coordinate map survives a "
                                 "second provider. This licenses `ID moves the "
                                 "outcome on haiku too`, NOT `ID is verified "
                                 "cross-model` - verification on gpt required a "
                                 "null swap control, which is not run here."),
        "null": ("ID's effect is specific to the calibration model at 80% power. "
                 "The verified map is `two of ten, on one model` and the paper "
                 "scopes its coordinate claims to gpt."),
        "opposite_sign": ("reported as measured, not reframed, exactly as LL's "
                          "sign reversal was"),
    },
    "null_result_is_informative": True,
    "no_reroll": ("If this returns null it is NOT re-run with more agents. That "
                  "is the re-roll this project forbids. The null stands with its "
                  "power stated."),
    "failure_condition": ("If ID- and ID+ do not differ under the prespecified "
                          "rule, ID does not move the outcome on haiku on this "
                          "item set, and that is the finding."),
}


def content_hash():
    payload = json.dumps({"active": ACTIVE, "levels": [LOW, HIGH],
                          "gpt_measured": GPT_MEASURED,
                          "power": MEASURED_POWER,
                          "prediction": LOCKED_PREDICTION},
                         sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def main():
    example = {"LL": 0.41, "CS": 0.83, "RT": 0.19, "MoR": 0.57, "RE": 0.28,
               "PD": 0.22, "TfA": 0.66, "ID": 0.74, "MS": 0.35, "AW": 0.50}
    print("content hash:", content_hash())
    print(f"active={ACTIVE}  levels={LOW}/{HIGH}  model=claude-haiku-4-5\n")
    print("ID measured on gpt across three designations:")
    for k, v in GPT_MEASURED.items():
        print(f"   {k:28s} {v:+.3f}")
    print("\narchitecture-level result, already cross-model:")
    for k, v in ARCHITECTURE_CROSSMODEL.items():
        print(f"   {k:28s} {v:+.3f}")
    lo, hi = pin(example, LOW), pin(example, HIGH)
    print(f"\ndrawn ID={example[ACTIVE]} is DISCARDED in both arms:")
    print(f"   ID-  ID={lo[ACTIVE]:.2f}   ID+  ID={hi[ACTIVE]:.2f}")
    print(f"   nine others identical: "
          f"{all(lo[p] == hi[p] for p in PARAMETERS if p != ACTIVE)}")
    v = verify_construction([{"agent": 0, "coordinates": example}])
    print("\nverified:", v["verified"])
    print(f"\npower at ID's gpt effect (+0.111): {MEASURED_POWER['0.111']}")
    print(f"false positive rate: {MEASURED_POWER['0.000_false_positive']}")


if __name__ == "__main__":
    main()
