"""Stage 4a: the four framework parameters the project never settled, at 80 agents.

`coordinate_sweep_r2` pinned eight coordinates at 25 agents and left four pieces of
unfinished business. Their rescored effects (`coordinate_sweep_r2/rescored.json`):

    LL   -0.1314  Holm 0.00082   measured three times, three different answers:
                                 +0.271 post-hoc, -0.131 pinned at 25 agents,
                                 -0.014 pinned at 40. WITHDRAWN and unresolved.
    TfA  -0.1029  Holm 0.1112    uncorrected interval excludes zero; failed Holm
    MoR  -0.0971  Holm 0.0690    uncorrected interval excludes zero; failed Holm
    AW    -0.036                 NEVER independently pinned. Every swap control in
                                 the thesis rests on AW being a partner field, and
                                 that rests on one number from another designation.

**Why 80 agents and not 40.** Simulated against the measured gpt per-item
baselines, Holm family 2, 20 seeds: at |0.10| power is **9/20 at 40 agents** and
**18/20 at 80**; at |0.15|, 18/20 and 20/20. TfA and MoR sit at 0.10. A 40-agent
re-test would have been a coin flip on exactly the effects it was built to settle,
which is how Legitimacy Locus became unresolved in the first place.

**Two designations, two coordinates each**, because 80 agents x 2 coordinates x 2
levels x 7 items = 2,240 calls is the size this harness runs comfortably and keeps
the Holm family at 2:

    r1   AW, LL      AW first: it underpins every swap control in the thesis
    r2   TfA, MoR    the two near-misses, at a sample that can settle them

**Design.** Each coordinate is pinned to 0.10 and 0.90 with the other nine drawn
per agent and held byte-identical between the two levels - the `pd_prospective_r1`
design, unchanged. Two-sided: none of the four has a theory-derived direction on
these items, and inventing one after seeing the sweep's sign would be exactly the
post-hoc confirmation this project's own reanalysis warned against.

**What a null will and will not mean.** At 18/20 power for |0.10| a Holm-corrected
null bounds the effect below roughly 0.10 on these items; it does not establish
zero, and the assessment must say so. A null for AW is the single most useful
outcome available here: it is the assumption the thesis's swap controls rest on
and it has never been tested directly.
"""
from __future__ import annotations

import hashlib
import json

import phase7_block_variants as BV

PARAMETERS = BV.PARAMETERS
LOW, HIGH = 0.1, 0.9
N_AGENTS = 80

DESIGNATIONS = {
    "r1": ("AW", "LL"),
    "r2": ("TfA", "MoR"),
}

# Rescored sweep effects at 25 agents, and what each coordinate's status is.
PRIOR = {
    "AW": {"effect": -0.036, "holm": None, "status": "never independently pinned",
           "note": ("Measured only as the inert partner in label_semantics_r1. Every "
                    "swap control in the thesis treats AW as a field that does not "
                    "carry the effect; this is the direct test of that assumption.")},
    "LL": {"effect": -0.1314, "holm": 0.00082, "status": "withdrawn, unresolved",
           "note": ("Three measurements, three answers: +0.271 post-hoc, -0.131 at 25 "
                    "agents, -0.014 at 40. It failed on the LARGER sample. This is a "
                    "third pinned measurement, not a tie-breaker: two of three "
                    "agreeing would not make LL load-bearing.")},
    "TfA": {"effect": -0.1029, "holm": 0.1112, "status": "near-miss",
            "note": "Uncorrected interval excludes zero; did not survive Holm."},
    "MoR": {"effect": -0.0971, "holm": 0.0690, "status": "near-miss",
            "note": "Uncorrected interval excludes zero; did not survive Holm."},
}

POWER = {"baselines": "measured gpt per-item good-rates (phase4b_perm_pool.SCREENED)",
         "family": 2, "seeds": 20,
         "40_agents": {"0.10": "9/20", "0.15": "18/20", "0.20": "20/20"},
         "80_agents": {"0.10": "18/20", "0.15": "20/20", "0.20": "20/20"},
         "false_positives_at_80": "2/20",
         "consequence": ("a Holm-corrected null bounds the effect below about 0.10 on "
                         "these items and does not establish zero")}


def pin(coordinates, code, level):
    """The drawn profile with ONE coordinate overwritten; the other nine untouched."""
    if code not in PARAMETERS:
        raise ValueError(f"Unknown parameter code: {code}")
    if set(coordinates) != set(PARAMETERS):
        raise ValueError("Require exactly the ten parameter codes")
    out = dict(coordinates)
    out[code] = level
    return out


def verify_construction(render_block, agents, codes):
    """The two levels must differ on exactly one line, at the right entry, for every agent."""
    problems = []
    for agent in agents:
        c = agent["coordinates"]
        for code in codes:
            lo, hi = (render_block(pin(c, code, L)) for L in (LOW, HIGH))
            a, b = lo.split("\n"), hi.split("\n")
            diff = [k for k, (x, y) in enumerate(zip(a, b)) if x != y]
            if len(a) != len(b) or len(diff) != 1:
                problems.append(f"agent {agent['agent']} {code}: {len(diff)} lines differ")
                continue
            if len(lo) != len(hi):
                problems.append(f"agent {agent['agent']} {code}: levels differ in length")
            _, idx = BV.locate(hi, code)
            if diff[0] != idx:
                problems.append(f"agent {agent['agent']} {code}: wrong line changed")
            # The drawn value must be genuinely overwritten at rendered precision.
            if f"{c[code]:.2f}" in (f"{LOW:.2f}", f"{HIGH:.2f}") and c[code] not in (LOW, HIGH):
                problems.append(f"agent {agent['agent']} {code}: drawn value collides with a level")
    if problems:
        raise ValueError("Construction verification failed: " + "; ".join(problems[:6]))
    return {"verified": True, "agents": len(agents), "codes": list(codes),
            "note": ("Within a coordinate the two levels differ on exactly one line, at "
                     "that coordinate's own entry, and are equal in length. The nine "
                     "other coordinates are identical between levels per agent.")}


def locked_prediction(designation):
    codes = DESIGNATIONS[designation]
    return {
        "question": ("Do the four framework parameters the project never settled move the "
                     "outcome, measured at a sample size that can settle them?"),
        "coordinates": list(codes), "levels": [LOW, HIGH], "agents": N_AGENTS,
        "direction": ("TWO-SIDED for every coordinate. None has a theory-derived direction "
                      "on these items; adopting the sweep's sign after seeing it would be "
                      "the post-hoc confirmation the Phase 2 reanalysis warned against."),
        "effect_definition": ("paired difference in the share classifying `good`, printed "
                              "0.90 minus printed 0.10, by agent and item"),
        "prior": {c: PRIOR[c] for c in codes},
        "holm_family": len(codes),
        "consistency_rule": "at least 4 of 7 items agreeing in sign, as every prior designation",
        "power": POWER,
        "no_gate": ("There is no replication gate: none of these coordinates has an "
                    "established effect to reproduce. That is the point of the designation."),
        "aw_note": ("A null for AW SUPPORTS the thesis's swap controls but does not prove "
                    "them: it bounds AW's own effect, and the controls additionally assume "
                    "AW's entry is a fair partner for the tested field's entry."),
        "ll_note": ("LL has given three different answers. A third pinned measurement is "
                    "reported as a third measurement; it does not overturn the withdrawal "
                    "by majority vote."),
        "not_established_by_any_outcome": [
            "understanding, or that any coordinate is understood as a concept",
            "anything about models or items outside gpt-5.4-mini and these seven",
            "that a coordinate which moves the outcome is a LABEL effect - that needs a "
            "swap control, which this designation does not run",
        ],
        "no_reroll": "No coordinate is re-run with more agents after the results are seen.",
    }


def content_hash(designation):
    payload = json.dumps({"designation": designation, "codes": DESIGNATIONS[designation],
                          "levels": [LOW, HIGH], "agents": N_AGENTS,
                          "prediction": locked_prediction(designation)},
                         sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()
