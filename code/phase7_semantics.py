"""Stage 1 of the understanding programme: does behaviour track a field's MEANING?

`label_semantics_r1` and `position_counterbalance_r1` established that the PD
effect is bound to the PD entry - its name together with its two-line endpoint
explanation - and not to block presence, length, free-floating extremity or line
position. They could not say WHAT about the entry carries it. Three readings
survive, and they make different predictions once the entry is edited:

  MEANING      the model reads what the scale is said to mean and acts on it
  NAME         a learned association between the string "Procedural Dependence",
               a magnitude, and a disposition; the explanation is decoration
  EXTREMITY    an extreme number in a salient slot (field-weighted extremity)

**The design.** PD is pinned to 0.10 and 0.90 exactly as in `pd_prospective_r1`,
under four renderings of the PD entry (`phase7_block_variants`). The nine other
entries, the items and the user turn are byte-identical throughout.

    variant   name                    explanation     what it isolates
    CANON     Procedural Dependence   canonical       the replication gate
    FLIP      Procedural Dependence   ends SWAPPED    explanation vs name+number
    INVERT    Outcome Dominance       ends swapped    a consistent re-encoding
    NONCE     Factor K                canonical       explanation with no name

"Effect" below always means the paired difference in the share of decisions
classifying `good`, PRINTED NUMBER 0.90 minus printed number 0.10.

**Predictions, locked before collection.** They differ in SIGN, which is what
makes the design decisive rather than suggestive:

    variant   MEANING       NAME            EXTREMITY
    CANON     +             +               +
    FLIP      NEGATIVE      +               +
    INVERT    NEGATIVE      ~0              +
    NONCE     +             ~0              +

FLIP is the decisive cell, as condition D was for position. Name, line, number
and even the multiset of characters in the block are held fixed; only what the
two ends of the scale are said to mean changes. Under MEANING a printed 0.90 now
says "outcome-dominant", so the effect must REVERSE. FLIP also needs no human
judgement of equivalence - it is a literal exchange of two strings - whereas
INVERT rests on the softer premise that "Outcome Dominance" with swapped ends
means the same as the original, and this project has already found that reviewer
judgements about materials do not predict model behaviour.

FLIP sets the name against the explanation, so a third outcome is live: the
conflict may simply cancel (effect near zero). That is reported as what it is -
the explanation matters but does not dominate - via the reversal index below.

**Primary quantities. Direct contrasts, never significance-vs-non-significance.**
A significant arm beside a non-significant one is not a test of their difference;
that inference was made once in this project, about ID, and had to be withdrawn.

  e_V                    the within-variant effect, for each of the four variants
  e_CANON - e_V          the within-unit difference of differences, by unit
                         bootstrap over the agent-item pairs present in all cells
  reversal index         e_FLIP / e_CANON and e_INVERT / e_CANON
                         -1 = full reversal (MEANING)   +1 = explanation ignored
  transfer index         e_NONCE / e_CANON
                         +1 = the explanation alone carries it   0 = the name did

**The gate.** Every other quantity is interpretable only if e_CANON replicates
(one-sided, Holm-corrected, at least 4 of 7 items positive). If it does not, the
designation reports a failed gate and claims nothing - the LL lesson.

**What no outcome can show.** A full reversal would establish that behaviour
tracks the stated meaning of the scale under a form-preserving change of meaning.
It would NOT establish understanding in any sense beyond that, and it would not
separate "reads the explanation" from "follows an instruction phrased as an
explanation". The programme's other stages exist because this one cannot.
"""
from __future__ import annotations

import hashlib
import json

import phase7_block_variants as BV

PARAMETERS = BV.PARAMETERS

FIELD = "PD"
LOW, HIGH = 0.1, 0.9
VARIANTS = BV.VARIANTS                      # CANON, FLIP, INVERT, NONCE
INVERT_NAME = "Outcome Dominance"
NONCE_NAME = "Factor K"

CELLS = tuple(f"{v}{s}" for v in VARIANTS for s in ("+", "-"))

# Measured on this model, this item set, 40 agents. The gate is against these.
PRIOR_CANON = {"pd_prospective_r1": +0.346, "label_semantics_r1_true": +0.339,
               "position_counterbalance_r1_cell_A": +0.393}


def pin(coordinates, level):
    """The agent's drawn profile with PD overwritten; nothing else moves."""
    if set(coordinates) != set(PARAMETERS):
        raise ValueError("Require exactly the ten parameter codes")
    out = dict(coordinates)
    out[FIELD] = level
    return out


def render_cell(render_block, coordinates, variant, level):
    """The profile block for one cell: pin PD, render, then edit the PD entry."""
    block = render_block(pin(coordinates, level))
    return BV.variant(block, FIELD, variant, invert_name=INVERT_NAME, nonce_name=NONCE_NAME)


def verify_construction(render_block, agents):
    """Every property the design rests on, for every agent, against the renderer."""
    problems = []
    for agent in agents:
        c = agent["coordinates"]
        for level in (LOW, HIGH):
            BV.verify_variants(render_block, pin(c, level), FIELD,
                               invert_name=INVERT_NAME, nonce_name=NONCE_NAME)
        for v in VARIANTS:
            lo, hi = render_cell(render_block, c, v, LOW), render_cell(render_block, c, v, HIGH)
            if lo == hi:
                problems.append(f"agent {agent['agent']} {v}: the two levels render identically")
            a, b = lo.split("\n"), hi.split("\n")
            diff = [k for k, (x, y) in enumerate(zip(a, b)) if x != y]
            if len(a) != len(b) or len(diff) != 1:
                problems.append(f"agent {agent['agent']} {v}: levels differ on {len(diff)} lines, expected 1")
            if len(lo) != len(hi):
                problems.append(f"agent {agent['agent']} {v}: levels differ in length")
        blocks = {(v, L): render_cell(render_block, c, v, L) for v in VARIANTS for L in (LOW, HIGH)}
        if len(set(blocks.values())) != 8:
            problems.append(f"agent {agent['agent']}: the eight cells are not eight distinct blocks")
    if problems:
        raise ValueError("Construction verification failed: " + "; ".join(problems))
    return {"verified": True, "agents": len(agents), "cells": list(CELLS),
            "note": ("Within every variant the two levels differ on exactly one "
                     "line and are equal in length; across variants only the PD "
                     "entry's three lines ever differ from the canonical block. "
                     "The drawn PD value is overwritten in every cell.")}


LOCKED_PREDICTION = {
    "question": ("Does the PD effect follow what the PD scale is SAID TO MEAN, or "
                 "the name and the number regardless of the explanation?"),
    "field": FIELD, "levels": [LOW, HIGH], "variants": list(VARIANTS),
    "invert_name": INVERT_NAME, "nonce_name": NONCE_NAME,
    "effect_definition": ("paired difference in the share classifying `good`, "
                          "printed number 0.90 minus printed number 0.10"),
    "gate": ("e_CANON must replicate: one-sided sign test, Holm-corrected over the "
             "four within-variant tests, positive in at least 4 of 7 items. If it "
             "fails, nothing else in the designation is interpreted."),
    "predictions_by_reading": {
        "MEANING":   {"CANON": "+", "FLIP": "NEGATIVE", "INVERT": "NEGATIVE", "NONCE": "+"},
        "NAME":      {"CANON": "+", "FLIP": "+",        "INVERT": "~0",       "NONCE": "~0"},
        "EXTREMITY": {"CANON": "+", "FLIP": "+",        "INVERT": "+",        "NONCE": "+"},
    },
    "primary": ("direct contrasts with 95% unit-bootstrap intervals: each e_V, each "
                "within-unit difference e_CANON - e_V, the reversal indices "
                "e_FLIP/e_CANON and e_INVERT/e_CANON, and the transfer index "
                "e_NONCE/e_CANON. No conclusion is drawn from one arm being "
                "significant while another is not."),
    "decision_rule": {
        "meaning_carries_it": ("e_FLIP < 0 with its 95% interval excluding zero AND "
                               "negative in at least 4 of 7 items"),
        "explanation_ignored": ("e_FLIP > 0 with its 95% interval excluding zero"),
        "conflict": ("anything else: the explanation matters but does not dominate "
                     "the name; reported through the reversal index, not rounded "
                     "to either reading"),
    },
    "why_flip_is_decisive": ("name, line, number and the multiset of characters in "
                             "the block are all held fixed; only the meaning "
                             "assignment of the scale changes. It requires no "
                             "judgement that two wordings are equivalent."),
    "soft_premise_of_invert": ("INVERT assumes `Outcome Dominance` with swapped ends "
                               "means what the original meant. That is a human "
                               "judgement, and this project has found such "
                               "judgements do not predict model behaviour."),
    "not_established_by_any_outcome": [
        "understanding in any sense beyond tracking the stated meaning of a scale",
        "a difference between reading an explanation and following an instruction "
        "phrased as one",
        "anything about fields other than PD, models other than gpt-5.4-mini, or "
        "items outside the seven screened vignettes",
    ],
    "prior_canon_effects": PRIOR_CANON,
    "null_result_is_informative": True,
    "no_reroll": "No cell is re-run with more agents after the results are seen.",
}


def content_hash():
    payload = json.dumps({"field": FIELD, "levels": [LOW, HIGH], "variants": list(VARIANTS),
                          "invert": INVERT_NAME, "nonce": NONCE_NAME,
                          "prediction": LOCKED_PREDICTION},
                         sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def main():
    import sys
    sys.path.insert(0, ".")
    from phase3_protocol_kernel import context_prompt, AXES
    from phase3_representation_diagnostic import profile_parts
    neutral = dict.fromkeys(AXES, "NEUTRAL")
    render = lambda c: profile_parts(context_prompt(c, neutral))[1]
    ex = {"LL": 0.41, "CS": 0.83, "RT": 0.19, "MoR": 0.57, "RE": 0.28,
          "PD": 0.22, "TfA": 0.66, "ID": 0.74, "MS": 0.35, "AW": 0.50}
    print("content hash:", content_hash())
    v = verify_construction(render, [{"agent": 0, "coordinates": ex}])
    print("construction verified:", v["verified"], "| cells:", len(v["cells"]))
    print("\nwhat the agent sees on the PD entry, per cell:")
    for var in VARIANTS:
        for level in (HIGH, LOW):
            b = render_cell(render, ex, var, level).split("\n")
            i = next(k for k, l in enumerate(b) if l.startswith(" 6. "))
            says = b[i + 2][len("     1 = "):].split(";")[0] if level == HIGH else b[i + 1][len("    (0 = "):].split(";")[0]
            print(f"   {var:7s}{'+' if level == HIGH else '-'}  {b[i].strip():34s} -> the printed value sits nearest: {says}")
    print("\nlocked predictions (sign of the effect, printed 0.90 minus 0.10):")
    for reading, row in LOCKED_PREDICTION["predictions_by_reading"].items():
        print(f"   {reading:10s} " + "  ".join(f"{k}={v}" for k, v in row.items()))


if __name__ == "__main__":
    main()
