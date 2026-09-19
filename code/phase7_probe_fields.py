"""Stage 4b of the understanding programme: is PD special, or does ANY glossed field work?

`semantics_r1` showed the PD effect follows the stated meaning of the PD scale.
That leaves the framework-level question open: is this a property of the
framework's parameter, or of any on-topic field that carries an explanation?

**The design.** Four PROBE fields, none of them among the ten parameters, each
rendered in Affective Weighting's slot (entry 10) in the block's own two-line
format and pinned to 0.10 and 0.90. The nine other entries - PD included, at the
agent's drawn value - the items and the user turn are byte-identical across all
eight cells. AW's slot is used because `position_counterbalance_r1` measured an
extreme numeral there at +0.061 and +0.004: the slot itself is near-neutral.

These are probe fields on the experimental branch. They are NOT amendments to the
ten-parameter framework, and no result here adds a parameter.

**Predictions, locked before collection, derived from each field's own gloss and
a property of the ITEM SET** (every item: one party holds an arrangement, has said
they want to keep it, and loses 5 if it is overridden, against 4 lost on the other
side if it is kept; keeping classifies `good` on all seven):

    field                   high end says...                       predicted sign
    Status-quo Preference   existing arrangements stand            +
    Stated-Wish Deference   the holder's stated wish is decisive   +
    Worst-off Priority      whoever would lose most matters most   +  (the holder loses 5)
    Numbers Count           favour the option helping more people  NEGATIVE

Numbers Count is the specificity control: its meaning points the OTHER way. Its
prediction is weaker than the others by construction - only some items put a
countable larger group on the overriding side (two visiting staff; a supply
programme is not a head-count) - so per-item results are reported beside the pool.

**Readings.**
  GENERIC CUE     all four move the same way regardless of meaning
  MEANING-GENERAL the three + fields go positive AND Numbers Count goes negative:
                  explanation-following is general, not special to PD
  PD-SPECIAL      the probes do little (every interval inside +/-0.15) although
                  they name what the items are about more directly than PD does

MEANING-GENERAL would cap what the ten parameters can claim; it would not
embarrass the method. The programme's criterion for PD being special is then
defeasibility (Stage 3a), not effect size.

**Analysis.** Each within-field effect (printed 0.90 minus 0.10, paired by agent
and item) with a 95% unit-bootstrap interval; two-sided sign tests, Holm over the
four. No gate: no probe has a prior effect to replicate. Power at 40 agents,
Holm family 4, measured baselines: 18/20 at |0.15|, 20/20 at |0.20|, 8/20 at
|0.10| - a screen, not a settlement; survivors get a larger follow-up.
"""
from __future__ import annotations

import hashlib
import json

import phase7_block_variants as BV

PARAMETERS = BV.PARAMETERS
SLOT = "AW"
LOW, HIGH = 0.1, 0.9

PROBES = {
    "SQ": {"name": "Status-quo Preference",
           "low": "existing arrangements carry no special weight",
           "high": "existing arrangements stand unless there is strong reason to change them",
           "predicted": "+"},
    "SW": {"name": "Stated-Wish Deference",
           "low": "a stated wish is one input among many",
           "high": "a person's stated wish about their own arrangement is decisive",
           "predicted": "+"},
    "WO": {"name": "Worst-off Priority",
           "low": "total benefit matters however it is spread",
           "high": "whoever would lose most matters most",
           "predicted": "+"},
    "NC": {"name": "Numbers Count",
           "low": "claims are weighed regardless of how many hold them",
           "high": "the option helping more people is favoured",
           "predicted": "NEGATIVE"},
}
CELLS = tuple(f"{p}{s}" for p in PROBES for s in ("+", "-"))


def probe_block(block, probe):
    """Replace the AW entry's name and both endpoint texts, in place."""
    spec = PROBES[probe]
    _, i = BV.locate(block, SLOT)
    out = BV.rename(block, SLOT, spec["name"]).split("\n")
    out[i + 1] = BV._LOW_PREFIX + spec["low"] + BV._LOW_SUFFIX
    out[i + 2] = BV._HIGH_PREFIX + spec["high"] + BV._HIGH_SUFFIX
    return "\n".join(out)


def pin(coordinates, level):
    if set(coordinates) != set(PARAMETERS):
        raise ValueError("Require exactly the ten parameter codes")
    out = dict(coordinates)
    out[SLOT] = level
    return out


def render_cell(render_block, coordinates, probe, level):
    return probe_block(render_block(pin(coordinates, level)), probe)


def verify_construction(render_block, agents):
    problems = []
    for agent in agents:
        c = agent["coordinates"]
        canon = {L: render_block(pin(c, L)) for L in (LOW, HIGH)}
        _, i = BV.locate(canon[HIGH], SLOT)
        target = {i, i + 1, i + 2}
        seen = set()
        for probe, spec in PROBES.items():
            lo, hi = (render_cell(render_block, c, probe, L) for L in (LOW, HIGH))
            a, b = lo.split("\n"), hi.split("\n")
            if len(a) != len(b) or [k for k, (x, y) in enumerate(zip(a, b)) if x != y] != [i]:
                problems.append(f"agent {agent['agent']} {probe}: levels do not differ on the entry line alone")
            if len(lo) != len(hi):
                problems.append(f"agent {agent['agent']} {probe}: levels differ in length")
            for L, built in ((LOW, lo), (HIGH, hi)):
                base, new = canon[L].split("\n"), built.split("\n")
                changed = {k for k, (x, y) in enumerate(zip(base, new)) if x != y}
                if len(base) != len(new) or changed != target:
                    problems.append(f"agent {agent['agent']} {probe}: edit not confined to the slot's three lines")
                if "Affective Weighting" in built or built.count(spec["name"]) != 1:
                    problems.append(f"agent {agent['agent']} {probe}: slot name not replaced exactly once")
                seen.add(built)
        if len(seen) != 8:
            problems.append(f"agent {agent['agent']}: eight cells are not eight distinct blocks")
    if problems:
        raise ValueError("Construction verification failed: " + "; ".join(problems[:6]))
    return {"verified": True, "agents": len(agents), "cells": list(CELLS),
            "note": ("Every cell differs from the agent's canonical block on the three "
                     "lines of entry 10 only; within a probe the two levels differ in "
                     "one numeral. PD and the eight other entries keep the drawn values.")}


LOCKED_PREDICTION = {
    "question": ("Do on-topic probe fields outside the ten parameters move choices as "
                 "their own explanations predict - including one whose meaning points "
                 "the other way?"),
    "slot": SLOT, "levels": [LOW, HIGH], "probes": PROBES,
    "effect_definition": ("paired difference in the share classifying `good`, printed "
                          "0.90 minus printed 0.10"),
    "readings": {
        "GENERIC_CUE": "all four effects share a sign, intervals excluding zero",
        "MEANING_GENERAL": ("NC negative with its interval excluding zero AND at least two "
                            "of SQ, SW, WO positive with intervals excluding zero"),
        "PD_SPECIAL": "every probe interval lies inside (-0.15, +0.15)",
        "MIXED": "anything else, reported field by field and not rounded to a reading",
    },
    "weaker_prediction": ("NC's negative sign is item-dependent: only some items put a "
                          "countable larger group on the overriding side. Per-item "
                          "effects are reported beside the pool."),
    "reference_effect": {"PD_CANON_semantics_r1": +0.3393},
    "not_established_by_any_outcome": [
        "that any probe is or should be a framework parameter",
        "understanding; a difference between reading and instruction-following",
        "anything beyond gpt-5.4-mini and the seven screened items",
    ],
    "no_reroll": "No cell is re-run with more agents after the results are seen.",
}


def content_hash():
    payload = json.dumps({"slot": SLOT, "levels": [LOW, HIGH], "prediction": LOCKED_PREDICTION},
                         sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()
