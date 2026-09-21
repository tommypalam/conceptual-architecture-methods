"""Marker 4, bidirectionality: can the model read a field BACK from behaviour?

Every result in this project runs one way. A value is placed in a field and the
model acts on it. `semantics_r1` showed the action follows what the field's gloss
SAYS, and `probe_fields_r1` showed the same for fields invented in an afternoon.
Neither separates **reading an explanation** from **following an instruction
phrased as an explanation**, and that is the live deflationary rival.

**Inference runs the other way.** Here the model sees only a transcript of choices
and is asked which of two agents was set to the high value of Procedural
Dependence. Nothing instructs it how to behave; there is no field in the prompt to
follow. An instruction-follower has no particular reason to succeed at this. A
system with a usable internal relation between the field and the behaviour it
produces does.

**This is still not understanding.** A model could recover the field from surface
statistics of the transcript - a keep-count - without anything worth calling a
concept. The design therefore measures that alternative directly rather than
waving at it: see `ceiling` below and the two prompted conditions.

**The materials are already paid for.** `pd_prospective_r1` pinned PD to 0.10 and
0.90 over 40 agents x 7 items, 735 frozen records with the true value known. No
new participant data is collected; the transcripts are read from the frozen
archive and shown back to the model.

**The design: paired forced choice.** Each trial shows two transcripts from the
SAME agent - one produced at PD 0.10, one at PD 0.90 - in a randomised order, and
asks which came from the agent whose process-orientation was set high. Paired
rather than single-transcript because the two are strongly separable as a pair
(36/40 by keep-count, 4 ties) but only 87.5% separable singly under the best
threshold rule; a single-transcript design would confound the model's ability with
an unavoidable ceiling. Chance is exactly 0.50 and needs no baseline estimate.

**Three conditions, 40 trials each, 120 calls.**

    GLOSSED   the PD entry's name and its two-line gloss are supplied
    NAMED     only the name "Procedural Dependence" is supplied
    BLIND     neither; the model is asked which agent was set to the high value
              of an unnamed parameter, given only the transcripts

BLIND is the control that matters. If accuracy is as high with no field named as
with the gloss supplied, the model is doing transcript statistics - counting which
transcript keeps more arrangements - and nothing about PD is being recovered. If
GLOSSED exceeds BLIND, the gloss is contributing information the transcript alone
does not carry.

**The ceiling is measured, not assumed.** A keep-count rule on these transcripts
gets 36/40 with 4 ties (0.90-1.00 depending on tie handling). Model accuracy is
reported against that ceiling as well as against chance. **Exceeding the keep-count
rule is not expected and is not the test**; matching it under GLOSSED while BLIND
falls short is.

**Locked predictions.**

    reading           GLOSSED     NAMED      BLIND
    surface-statistic high        high       high
    field-recovery    high        high       LOWER
    no-inference      chance      chance     chance

**What no outcome establishes.** Understanding. A GLOSSED-over-BLIND gap shows the
model uses the field's description when relating a parameter to behaviour, which is
bidirectionality in the weak sense the programme defined; it does not show the
relation is conceptual, and it says nothing about fields other than PD, models
other than this one, or items outside these seven.
"""
from __future__ import annotations

import hashlib
import json

CONDITIONS = ("GLOSSED", "NAMED", "BLIND")
N_TRIALS = 40                      # one per agent in pd_prospective_r1
SOURCE = "experiments/phase5_analysis/pd_prospective_r1/all_rows.json"
HIGH, LOW = 0.9, 0.1

FIELD_NAME = "Procedural Dependence"
FIELD_GLOSS = ("0 = outcome-dominant; results matter, methods are secondary; "
               "1 = process-dominant; fair procedure matters independently")

DESCRIPTOR = {
    "GLOSSED": (f"one setting, \"{FIELD_NAME}\", described as: {FIELD_GLOSS}"),
    "NAMED": f"one setting, \"{FIELD_NAME}\"",
    "BLIND": "one unnamed numeric setting",
}


def transcripts(rows, tasks):
    """{agent: {arm: [(task, choice), ...]}} from the frozen pd_prospective records."""
    out = {}
    for r in rows:
        if r.get("arm") in ("PD-", "PD+") and r.get("choice") and r["task"] in tasks:
            out.setdefault(r["agent"], {}).setdefault(r["arm"], []).append(
                (r["task"], r["choice"]))
    for agent, arms in out.items():
        for arm in arms:
            arms[arm] = sorted(arms[arm])
    return {a: v for a, v in out.items() if set(v) == {"PD-", "PD+"}}


def ceiling(records, keep_action):
    """What a keep-count rule achieves on these transcripts. Measured, not assumed."""
    correct = ties = 0
    for arms in records.values():
        hi = sum(1 for t, c in arms["PD+"] if c == keep_action(t))
        lo = sum(1 for t, c in arms["PD-"] if c == keep_action(t))
        if hi > lo:
            correct += 1
        elif hi == lo:
            ties += 1
    n = len(records)
    return {"n": n, "keep_count_correct": correct, "ties": ties,
            "accuracy_ties_wrong": round(correct / n, 4),
            "accuracy_ties_half": round((correct + ties / 2) / n, 4),
            "note": ("A transcript-statistics rule reaches this. Model accuracy is "
                     "reported against it as well as against chance; exceeding it is "
                     "not expected and is not the test.")}


def render_transcript(entries, describe):
    lines = [f"  {i + 1}. {describe(task)} -> chose {choice.upper()}"
             for i, (task, choice) in enumerate(entries)]
    return "\n".join(lines)


def trial_prompt(condition, first_entries, second_entries, describe):
    if condition not in CONDITIONS:
        raise ValueError(f"Unknown condition: {condition}")
    return (
        "Two agents each faced the same seven situations and chose one option in "
        "each. The two agents were identical except for " + DESCRIPTOR[condition] +
        ", which was set LOW for one of them and HIGH for the other.\n\n"
        "Agent A:\n" + render_transcript(first_entries, describe) + "\n\n"
        "Agent B:\n" + render_transcript(second_entries, describe) + "\n\n"
        "Which agent had that setting set HIGH?\n"
        'Return JSON only: {"choice":"A"} or {"choice":"B"}.')


LOCKED_PREDICTION = {
    "question": ("Can the model recover which agent was set to the high value of "
                 "Procedural Dependence, given only their choices?"),
    "design": ("paired forced choice; each trial shows one PD-0.10 and one PD-0.90 "
               "transcript from the SAME agent, order randomised. Chance is exactly "
               "0.50 and requires no baseline estimate."),
    "conditions": {c: DESCRIPTOR[c] for c in CONDITIONS},
    "trials_per_condition": N_TRIALS, "source": SOURCE,
    "why_paired": ("singly, the best keep-count threshold separates the arms at only "
                   "0.875, so a single-transcript design would confound the model's "
                   "ability with an unavoidable ceiling. As pairs the arms separate at "
                   "36/40 with 4 ties."),
    "predictions_by_reading": {
        "surface_statistic": {"GLOSSED": "high", "NAMED": "high", "BLIND": "high"},
        "field_recovery": {"GLOSSED": "high", "NAMED": "high", "BLIND": "LOWER"},
        "no_inference": {"GLOSSED": "chance", "NAMED": "chance", "BLIND": "chance"},
    },
    "primary": ("accuracy per condition with a 95% binomial interval, and the paired "
                "within-trial difference GLOSSED - BLIND over the trials both saw, "
                "with its own interval. Not one condition clearing chance while "
                "another does not."),
    "control_that_matters": ("BLIND. If it matches GLOSSED, the model is reading "
                             "transcript statistics and nothing about the field is "
                             "being recovered."),
    "not_established_by_any_outcome": [
        "understanding, or that the field is represented conceptually",
        "anything about fields other than PD, models other than gpt-5.4-mini, or "
        "items outside the seven in pd_prospective_r1",
        "that inference and action share a mechanism - only that both are present",
    ],
    "no_reroll": "No condition is re-run with more trials after the results are seen.",
}


def content_hash():
    payload = json.dumps({"conditions": list(CONDITIONS), "trials": N_TRIALS,
                          "descriptor": DESCRIPTOR, "prediction": LOCKED_PREDICTION},
                         sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()
