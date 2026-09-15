"""Does PD's prospective endpoint effect exist outside the calibration model?

`pd_prospective_r1` pinned PD to its endpoints on gpt and measured **+0.346**,
the largest effect in the project, with the direction **locked from theory before
collection**. `label_semantics_r1` then showed the effect belongs to the PD
*label*: the same numerals on the inert AW label gave -0.036.

**Both of those ran on `gpt-5.4-mini` only.**

`id_crossmodel_r1` has since replicated ID on haiku (+0.075, p=0.033), which
leaves an odd asymmetry: **ID now has broader model evidence than PD does**, even
though PD's effect is three times larger and is the one with a theory-derived
direction. This designation closes that gap.

**The design is identical in form to `id_crossmodel_r1`.** For each agent:

    PD-   the agent's drawn profile with PD pinned to 0.1   (outcome-dominant)
    PD+   the agent's drawn profile with PD pinned to 0.9   (process-dominant)

The nine other coordinates are drawn once per agent and held IDENTICAL between
the arms, so the system prompts differ by exactly one line. Paired within agent
and item.

**The prediction is DIRECTIONAL, and that is the difference from the ID run.**
ID had no theory mapping onto these items, so `id_crossmodel_r1` was two-sided.
PD does: the coordinate is defined 0 = outcome-dominant, 1 = process-dominant,
every item presents a claim under a stated arrangement, and the option that keeps
the arrangement classifies `good`. **Verified on all six haiku items at build
time** by `verify_direction()` - the derivation is re-checked against this item
set rather than assumed from gpt's.

So: **PD+ produces a HIGHER share of `good` than PD-.** Derived from the
coordinate definition, not from gpt's measured +0.346. Importing that magnitude
as an expectation would be the post-hoc move this project keeps refusing; only
the *direction*, which follows from the definition, carries over.

**Power, measured against haiku's own per-item baselines before any call.** PD's
effect size on haiku is UNKNOWN and should not be assumed to be gpt's: the Phase
4B post-hoc correlation for PD on haiku was +0.089, near flat. So power is
reported across the plausible range rather than at one flattering point:

    +0.089  15/20      +0.150  19/20      +0.250  20/20
    +0.120  16/20      +0.200  19/20      +0.346  20/20   <- gpt's effect
    0.000   1/20 false positive

**15/20 at the pessimistic end.** A null would be weaker evidence than a positive
and is reported with that number attached.

**What a positive licenses.** That PD moves the outcome on haiku too - NOT that
PD is verified cross-model. Verification on gpt required the swap control from
`label_semantics_r1`, which is not run here, for the same power reason it was not
run for ID: a four-arm design quadruples the Holm family.
"""
from __future__ import annotations

import hashlib
import json

PARAMETERS = ("LL", "CS", "RT", "MoR", "RE", "PD", "TfA", "ID", "MS", "AW")

ACTIVE = "PD"

LOW, HIGH = 0.1, 0.9

# Measured on gpt. Recorded so the cross-model comparison is against stated
# numbers, and so the DIRECTION carried over is visibly the derived one rather
# than these.
GPT_MEASURED = {
    "pd_prospective_r1": +0.346,        # 40 agents, pinned, pooled Holm ~0
    "label_semantics_r1_true": +0.339,  # 40 agents, pinned, Holm ~0
    "label_semantics_r1_swap": -0.036,  # same numerals on AW, Holm 1.000
}

# The haiku post-hoc correlation, which is NOT a manipulation and is near flat.
# Recorded because it is the reason not to plan around gpt's +0.346.
HAIKU_POSTHOC_CORRELATION = +0.089

# The completed ID cross-model run, the sibling of this designation.
ID_CROSSMODEL = {"haiku_effect": +0.075, "p": 0.0328, "items": "4+/2-"}


def pin(coordinates, level):
    """The agent's drawn profile with PD overwritten. Nothing else moves."""
    if set(coordinates) != set(PARAMETERS):
        raise ValueError("Require exactly the ten parameter codes")
    out = dict(coordinates)
    out[ACTIVE] = level
    return out


def verify_direction(pool):
    """The directional prediction's premise, re-checked on THIS item set.

    The derivation is: PD 1 = process-dominant; every item presents a claim under
    a stated arrangement; the option that KEEPS the arrangement classifies
    `good`. That last step is a property of the item set, not of the coordinate,
    so it must hold on haiku's six items or the direction does not follow.

    `pd_prospective_r1` verified it for gpt's seven. This re-verifies for haiku's
    six rather than assuming it transfers.
    """
    problems, table = [], {}
    for task_id in pool.TASK_IDS:
        clean = pool.clean_action(task_id)
        verdict = pool.primary_net(task_id, clean)
        table[task_id] = {"clean_action": clean, "classifies": verdict}
        if verdict != "good":
            problems.append(f"{task_id}: clean action classifies {verdict!r}, "
                            "so keeping the arrangement is not the `good` option "
                            "and the directional derivation does not hold")
    if problems:
        raise ValueError("Directional premise failed: " + "; ".join(problems))
    return {"verified": True, "items": len(table), "per_item": table,
            "premise": ("on every item the option that keeps the stated "
                        "arrangement classifies `good`, so a process-dominant "
                        "agent is predicted to produce more `good` decisions")}


def verify_construction(agents):
    """The two arms must differ in PD and nothing else, for every agent."""
    problems, coincident = [], []
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
        rendered = f"{c[ACTIVE]:.2f}"
        if rendered in (f"{LOW:.2f}", f"{HIGH:.2f}"):
            coincident.append({"agent": agent["agent"], ACTIVE: c[ACTIVE],
                               "rendered": rendered,
                               "why": ("drawn value coincides with a pinned level; "
                                       "harmless because the drawn value is "
                                       "overwritten in BOTH arms")})
    if problems:
        raise ValueError("Construction verification failed: " + "; ".join(problems))
    return {"verified": True, "agents": len(agents), "active": ACTIVE,
            "levels": [LOW, HIGH], "coincident_draws": coincident,
            "note": ("Each agent's two arms differ in the PD line alone; the nine "
                     "other coordinates are drawn once per agent and held "
                     "identical. The drawn PD value is overwritten in both arms.")}


MEASURED_POWER = {
    "baselines_source": ("phase4b_profiled_r1 E arm, per item, on "
                         "claude-haiku-4-5-20251001"),
    "agents": 40, "items": 6, "seeds": 20, "holm_family": 1,
    "0.089": "15/20", "0.120": "16/20", "0.150": "19/20",
    "0.200": "19/20", "0.250": "20/20", "0.346": "20/20",
    "0.000_false_positive": "1/20",
    "why_not_60_agents": ("60 agents buys 20/20 at +0.120 against 16/20, and "
                          "nothing elsewhere in the plausible range, for 50% more "
                          "cost. 40 keeps symmetry with id_crossmodel_r1."),
    "honest_reading": ("PD's effect size on haiku is UNKNOWN and is NOT assumed "
                       "to be gpt's +0.346: the haiku post-hoc correlation was "
                       "+0.089, near flat. Power is therefore reported across the "
                       "whole plausible range. At the pessimistic end it is "
                       "15/20, so a null is weaker evidence than a positive and "
                       "is reported with that number."),
}


LOCKED_PREDICTION = {
    "question": ("Does pinning PD to its endpoints move the deterministic "
                 "good/bad headline on a model other than the calibration model?"),
    "active": ACTIVE, "levels": [LOW, HIGH], "arms": ["PD-", "PD+"],
    "model": "claude-haiku-4-5-20251001",
    "items": ("haiku's six dispersing items from phase4b_profiled_r1. Four of "
              "six overlap with gpt's seven; ward_transfer is haiku-only, "
              "on_call and rest_break are gpt-only."),
    "primary": ("the paired PD+ vs PD- contrast on the share of decisions "
                "classifying `good`, pooled across items, paired within agent "
                "and item"),
    "directional": ("PD+ (0.9, process-dominant) produces a HIGHER share of "
                    "decisions classifying `good` than PD- (0.1, "
                    "outcome-dominant). ONE-SIDED."),
    "derivation": ("From the coordinate definition in CLAUDE.md - 0 = "
                   "outcome-dominant, 1 = process-dominant - combined with a "
                   "property of the item set verified at build time by "
                   "verify_direction(): on every item the option that keeps the "
                   "stated arrangement classifies `good`. NOT from gpt's measured "
                   "+0.346, which is a magnitude and does not transfer."),
    "decision_rule": ("PD is declared to move the outcome on haiku if the pooled "
                      "one-sided p < 0.05 in the PREDICTED direction AND the "
                      "effect points that way in at least 4 of 6 items"),
    "wrong_direction_is_a_failure": ("A significant effect in the OPPOSITE "
                                     "direction fails this test. It is reported "
                                     "as a directional failure, not rescued by "
                                     "switching to a two-sided reading after the "
                                     "fact."),
    "gpt_reference": GPT_MEASURED,
    "haiku_posthoc_correlation": HAIKU_POSTHOC_CORRELATION,
    "power": MEASURED_POWER,
    "interpretation": {
        "replicates": ("PD's effect is not specific to the calibration model, and "
                       "its theory-derived direction holds on a second provider. "
                       "Licenses `PD moves the outcome on haiku too`, NOT `PD is "
                       "verified cross-model` - verification on gpt required the "
                       "label_semantics_r1 swap control, not run here."),
        "null": ("PD's endpoint effect is specific to the calibration model at "
                 "the power stated. Given the haiku post-hoc correlation of "
                 "+0.089 this is a live possibility and is NOT treated as a "
                 "surprise or re-run."),
        "opposite": ("a directional failure, reported as such"),
    },
    "null_result_is_informative": True,
    "no_reroll": ("If this returns null it is NOT re-run with more agents."),
    "failure_condition": ("If PD- and PD+ do not differ in the predicted "
                          "direction under the prespecified rule, PD's endpoint "
                          "effect does not transfer to haiku on this item set, "
                          "and that is the finding."),
}


def content_hash():
    payload = json.dumps({"active": ACTIVE, "levels": [LOW, HIGH],
                          "gpt_measured": GPT_MEASURED,
                          "power": MEASURED_POWER,
                          "prediction": LOCKED_PREDICTION},
                         sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def main():
    import phase4b_profiled_pool as PP
    print("content hash:", content_hash())
    print(f"active={ACTIVE}  levels={LOW}/{HIGH}  model=claude-haiku-4-5\n")
    print("PD measured on gpt:")
    for k, v in GPT_MEASURED.items():
        print(f"   {k:28s} {v:+.3f}")
    print(f"   {'haiku post-hoc correlation':28s} {HAIKU_POSTHOC_CORRELATION:+.3f}"
          "   <- NOT a manipulation, near flat")
    d = verify_direction(PP)
    print(f"\ndirectional premise on haiku's {d['items']} items: {d['verified']}")
    for t, v in d["per_item"].items():
        print(f"   {t:16s} clean={v['clean_action']:20s} -> {v['classifies']}")
    print(f"\nPREDICTION (one-sided): {LOCKED_PREDICTION['directional']}")
    print(f"\npower at gpt's effect (+0.346): {MEASURED_POWER['0.346']}")
    print(f"power at haiku's post-hoc size (+0.089): {MEASURED_POWER['0.089']}")
    print(f"false positive rate: {MEASURED_POWER['0.000_false_positive']}")


if __name__ == "__main__":
    main()
