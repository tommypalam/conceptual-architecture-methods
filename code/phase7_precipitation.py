"""Marker: does a boundary PRECIPITATE from instances, or only follow a stated rule?

Reactive Grounding (vertex 4) holds a concept in two registers: an extensional
cloud of remembered instances, and an intensional region - a boundary - fitted to
them. Its Conjecture 1 is that the boundary STIFFENS as the cloud evaporates: the
concept survives the loss of every exemplar that built it. That is the claimed
difference between a concept and a rule you are currently being told.

Phase 7 so far measured lens-stacking inside a fixed dimensionality: a gloss is
supplied, behaviour narrows, reversing the gloss reverses the narrowing
(`semantics_r1`). Real, and not the same thing. A supplied gloss is a rule the
model is reading. This designation asks whether a boundary forms from INSTANCES
and generalises once the instances are withdrawn.

**Three circularity traps, and what is done about each.**

1. **Instruction persistence.** If "withdrawal" means the material is earlier in a
   conversation, persistence is trivial - the text is still in context. The
   harness sends ONE user turn per call and holds no state, so every cell here is
   an independent call and withdrawn material is genuinely absent. Verified in
   `phase3_design_pilot.request`.

2. **Measuring the outcome that defines the treatment.** Asking whether a profile's
   effect persists, measured by the rate the profile was chosen to move, is the
   triviality trap Cognitive Economics names in Claim 1: it balances by
   construction. **The read-out is therefore a dimension the exemplars are silent
   on.** The exemplars are decisions on the seven base items, where keeping the
   arrangement and respecting the procedure are the SAME choice. The test items
   are the queue-jumped twins, where they come apart. Nothing in the exemplars
   mentions procedure; whether the model extracts `keep` or `procedure` from them
   is not stated by the instances.

3. **Idealised exemplars.** Constructing clean all-keep transcripts would be
   writing the rule this design claims to test for. **Exemplars are actual frozen
   decisions** from `pd_prospective_r1`, taken as they came, noise included. No
   agent there chose keep on all seven; the maximum is six. That is the material.

**Three arms, each an independent call on the same held-out twins.**

    INSTANCES   five of the agent's own prior decisions, shown as a transcript.
                No rule, no field, no gloss. Extensional register only.
    RULE        the PD gloss stated as an instruction. No exemplars.
                Intensional register, supplied rather than fitted.
    NEITHER     no exemplars and no rule. The unprofiled baseline for these items.

**Locked predictions.** Let k(arm) be the share choosing the base item's KEEP
option on the twins.

    reading                    INSTANCES      RULE         vs NEITHER
    boundary precipitates      k differs      k differs    both shifted
    rule-following only        k ~ NEITHER    k differs    only RULE shifts
    context effect only        k differs      k differs    equal shifts
    no effect                  k ~ NEITHER    k ~ NEITHER  nothing shifts

**The primary quantity is INSTANCES - NEITHER**, with RULE as the comparison and
NEITHER as the anchor. A direct within-item contrast, not one arm clearing a
threshold while another does not.

**What this CANNOT establish, stated before collection.** There is no memory decay
across independent calls, so there is no gamma: this tests whether a boundary
forms from instances and generalises, which is the first half of Conjecture 1. It
does NOT test survival under decay, which is the second half and the part that
distinguishes a concept from a summary. A null is also not a verdict on the model
alone - Reactive Grounding's own honest flag concedes the max-entropy
identification is its most suspect move, and this harness cannot separate "the
model holds no boundary" from "the vertex-4 bet is wrong here".
"""
from __future__ import annotations

import hashlib
import json

ARMS = ("INSTANCES", "RULE", "NEITHER")
N_EXEMPLARS = 5
SOURCE = "experiments/phase5_analysis/pd_prospective_r1/all_rows.json"

FIELD_NAME = "Procedural Dependence"
RULE_TEXT = ("You place weight on fair procedure for its own sake: where an "
             "arrangement was arrived at through a stated process, that matters "
             "independently of the outcome it produces.")

PREAMBLE = {
    "INSTANCES": ("Below are five decisions previously made by the person whose role "
                  "you now hold, in situations of this kind."),
    "RULE": None,
    "NEITHER": None,
}


def transcripts(rows, tasks, keep_action):
    """{agent: [(task, choice, kept)]} from the frozen PD+ records. Actual decisions."""
    out = {}
    for r in rows:
        if r.get("arm") == "PD+" and r.get("choice") and r["task"] in tasks:
            out.setdefault(r["agent"], []).append(
                (r["task"], r["choice"], r["choice"] == keep_action(r["task"])))
    return {a: sorted(v) for a, v in out.items() if len(v) == len(tasks)}


def exemplar_block(entries, describe):
    lines = [f"  {i + 1}. {describe(task)} -> chose {choice.upper()}"
             for i, (task, choice, _) in enumerate(entries)]
    return "\n".join(lines)


def compose(arm, body, entries=None, describe=None):
    """The user turn for one cell. The item body is byte-identical across arms."""
    if arm not in ARMS:
        raise ValueError(f"Unknown arm: {arm}")
    if arm == "NEITHER":
        return body
    if arm == "RULE":
        return RULE_TEXT + "\n\n" + body
    if entries is None or describe is None:
        raise ValueError("INSTANCES requires exemplars")
    return PREAMBLE["INSTANCES"] + "\n" + exemplar_block(entries, describe) + "\n\n" + body


def verify_construction(bodies, records, describe):
    """Every property the design rests on."""
    problems = []
    if not records:
        problems.append("no complete exemplar transcripts")
    for agent, entries in list(records.items())[:200]:
        use = entries[:N_EXEMPLARS]
        if len(use) != N_EXEMPLARS:
            problems.append(f"agent {agent}: fewer than {N_EXEMPLARS} exemplars")
            continue
        for body in bodies:
            cells = {a: compose(a, body, use, describe) for a in ARMS}
            # The item itself must be byte-identical across arms: only the prefix differs.
            for a in ARMS:
                if not cells[a].endswith(body):
                    problems.append(f"agent {agent} {a}: item body altered")
            if len(set(cells.values())) != len(ARMS):
                problems.append(f"agent {agent}: arms are not distinct")
            # The exemplar arm must state no rule, and the rule arm no exemplars.
            if FIELD_NAME in cells["INSTANCES"] or "procedure" in cells["INSTANCES"].lower():
                problems.append(f"agent {agent}: INSTANCES arm names the field or procedure")
            if "chose" in cells["RULE"].split(body)[0]:
                problems.append(f"agent {agent}: RULE arm carries exemplars")
            if cells["NEITHER"] != body:
                problems.append(f"agent {agent}: NEITHER arm is not the bare item")
    if problems:
        raise ValueError("Construction verification failed: " + "; ".join(problems[:6]))
    return {"verified": True, "agents": len(records), "arms": list(ARMS),
            "exemplars_per_agent": N_EXEMPLARS,
            "note": ("The item body is byte-identical across the three arms; only the "
                     "prefix differs. The INSTANCES arm names no field and no procedure; "
                     "the RULE arm carries no exemplars; NEITHER is the bare item.")}


LOCKED_PREDICTION = {
    "question": ("Does a boundary form from the agent's own prior decisions and "
                 "generalise to items the decisions are silent about, or does "
                 "behaviour only follow a rule while the rule is present?"),
    "arms": {a: (PREAMBLE.get(a) or RULE_TEXT if a == "RULE" else PREAMBLE.get(a))
             for a in ARMS},
    "exemplars": {"source": SOURCE, "n": N_EXEMPLARS,
                  "selection": ("the agent's own PD+ decisions on the base items, taken "
                                "as recorded. NOT idealised: no agent chose keep on all "
                                "seven, and the transcripts carry that noise.")},
    "test_items": ("the queue-jumped twins of defeasibility_screen_r1, on which keeping "
                   "the arrangement and respecting the procedure come APART. The "
                   "exemplars never contain a twin and never mention procedure."),
    "why_not_held_out_items": ("four of the five unused pool items saturated on gpt and "
                               "one was excluded on review, so no clean held-out item set "
                               "exists. Generalisation is tested across the keep/procedure "
                               "DIRECTION instead, which the exemplars do not state."),
    "primary": ("INSTANCES - NEITHER on the twins, a within-item contrast with a 95% "
                "bootstrap interval, with RULE - NEITHER alongside it. Not one arm "
                "clearing a threshold while another does not."),
    "secondary_dose_response": ("The five exemplars shown vary across agents in how many "
                                "are keeps (range 1-4 of 5, mean 3.15). If a boundary is "
                                "FITTED to the instances, agents with keep-leaning "
                                "exemplars should shift more; the slope of shift on "
                                "exemplar keep-count is that test. **The RULE arm cannot "
                                "produce this**: its text is identical for every agent, so "
                                "a slope there would indicate the exemplar count is "
                                "proxying something else and the secondary is void."),
    "predictions_by_reading": {
        "boundary_precipitates": {"INSTANCES": "shifts", "RULE": "shifts"},
        "rule_following_only": {"INSTANCES": "~NEITHER", "RULE": "shifts"},
        "context_effect_only": {"INSTANCES": "shifts", "RULE": "shifts, equally"},
        "no_effect": {"INSTANCES": "~NEITHER", "RULE": "~NEITHER"},
    },
    "circularity_controls": {
        "instruction_persistence": ("every cell is an independent stateless call; "
                                    "withdrawn material is absent, not earlier in context"),
        "outcome_defines_treatment": ("read out on a dimension the exemplars are silent "
                                      "on, not on the rate the exemplars exhibit"),
        "idealised_exemplars": "actual frozen decisions, noise included, not constructed",
    },
    "not_established_by_any_outcome": [
        "understanding, or that the model holds a concept",
        "survival under decay - there is no gamma across independent calls, so this is "
        "the first half of Conjecture 1 only",
        "a verdict on the model alone: Reactive Grounding concedes its max-entropy "
        "identification is its most suspect move, and this cannot separate 'no boundary "
        "in the model' from 'the vertex-4 bet is wrong here'",
        "anything about fields other than PD, models other than gpt-5.4-mini, or items "
        "outside these",
    ],
    "no_reroll": "No arm is re-run with more agents after the results are seen.",
}


def content_hash():
    payload = json.dumps({"arms": list(ARMS), "n_exemplars": N_EXEMPLARS,
                          "rule": RULE_TEXT, "preamble": PREAMBLE,
                          "prediction": LOCKED_PREDICTION},
                         sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()
