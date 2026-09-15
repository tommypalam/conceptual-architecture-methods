"""Prospective PD test: the design four prior attempts could not build.

**The question.** Procedural Dependence is the one coordinate this project keeps
finding. The Phase 2 within-arm reanalysis ranked it first of ten under
multivariate control, and recorded the binding caveat: that was a POST-HOC
discovery "requiring prospective test before any confirmatory language". The
Phase 5 integrated analysis then found PD top-ranked in both gpt designations
(r = +0.406 and +0.522, the latter surviving Holm) - also post-hoc, on partially
shared items, and absent on haiku.

**Four prior attempts reached the profiled stage zero times.** `pd_endpoint_r2`
and `pd_gradient_r1`-`r5` were stopped by dispersion screens; `pd_discriminant_r1`
and `r2` cleared review and were stopped by their own screens. The obstacle was
never wording or magnitude - it was that no item set both dispersed unprofiled
and could carry a PD contrast.

**What is new.** Phase 4B produced one. The seven-item gpt set cleared an
independent review with ZERO blocking issues in `phase4b_permutation_r2`, all
seven disperse on `gpt-5.4-mini` (mean headroom 0.331), and their baselines are
measured on three models by `phase4b_grand_r1`.

**The design.** Two arms, identical in every respect but one number:

    PD-    full ten-coordinate profile, PD pinned to 0.1  (outcome-dominant)
    PD+    full ten-coordinate profile, PD pinned to 0.9  (process-dominant)

The nine other coordinates are drawn once per agent and held IDENTICAL between
the arms. The system prompts differ by exactly one line. A difference between
them cannot be a profile-presence effect, a verbosity effect, or a demand
characteristic of being profiled: both arms are equally profiled.

This is the same isolation `pd_discriminant_r1` built and verified, now applied
to an item set that actually disperses.

**The prediction is DIRECTIONAL, and derived from theory, not from the
correlation.** CLAUDE.md defines PD as 0 = outcome-dominant (results matter,
methods secondary), 1 = process-dominant (fair procedure matters independently).

Every item in this set presents someone holding a claim under a stated
arrangement - a booking, a lease, a loan with withdrawal rights, an off-rota
night, a held slot, a mandatory rest break, a requested day off. The clean option
KEEPS the arrangement; the violating option overrides it for a better outcome.
On all seven, the clean option classifies `good` and the violating one
`not_good`.

So process-dominance predicts keeping the arrangement, and therefore a HIGHER
good-rate under PD+ than PD-. That direction follows from the definition of the
coordinate and would have been predicted without seeing any Phase 5 result.

**This can fail, and failure is the point.** If PD+ and PD- do not differ, the
prospective PD test fails on the first item set ever built that could run it, and
the Phase 2 and Phase 5 findings stay post-hoc indefinitely. That is reported as
a failure, not reframed.
"""
from __future__ import annotations

import hashlib
import json

import phase4b_perm_pool as POOL

PARAMETERS = ("LL", "CS", "RT", "MoR", "RE", "PD", "TfA", "ID", "MS", "AW")

PD_LOW, PD_HIGH = 0.1, 0.9

# The seven items, inherited verbatim. permutation_r2 accepted this exact
# composition with zero blocking issues.
TASK_IDS = POOL.TASK_IDS
SCREENED = POOL.SCREENED
FAMILY = POOL.FAMILY
MODEL = "gpt-5.4-mini-2026-03-17"

# On every item the clean option keeps a stated arrangement and classifies
# `good`; the violating option overrides it and classifies `not_good`. Verified
# in verify_design(), not assumed.
ARRANGEMENT = {
    "desk_booking": "a desk booking",
    "storage_unit": "a leased storage unit",
    "tool_library": "a loan held under withdrawal rights",
    "on_call": "an off-rota night",
    "meeting_room": "a held weekly room slot",
    "rest_break": "a mandatory rest slot",
    "weekend_rota": "a requested Saturday off",
}

LOCKED_PREDICTION = {
    "coordinate": "PD (Procedural Dependence)",
    "low_level": PD_LOW,
    "high_level": PD_HIGH,
    "directional": ("PD+ (0.9, process-dominant) produces a HIGHER share of "
                    "decisions classifying `good` than PD- (0.1, outcome-dominant)."),
    "derivation": ("From the coordinate definition in CLAUDE.md, not from any "
                   "measured correlation. PD 1 = 'process-dominant; fair procedure "
                   "matters independently'. Every item presents a stated "
                   "arrangement; the option that keeps it classifies `good` on all "
                   "seven. Process-dominance therefore predicts a higher good-rate. "
                   "This direction would have been predicted without seeing the "
                   "Phase 2 or Phase 5 results."),
    "why_it_isolates": ("The nine non-PD coordinates are drawn once per agent and "
                        "held identical between arms; the system prompts differ by "
                        "exactly one line. Both arms are equally profiled, so the "
                        "contrast cannot be a profile-presence or verbosity effect."),
    "prior_status": ("PD's dominance is POST-HOC in both the Phase 2 reanalysis and "
                     "the Phase 5 integrated analysis. Four prior prospective "
                     "attempts reached the profiled stage zero times. This "
                     "designation is the first prospective test."),
    "null_result_is_informative": True,
    "failure_condition": ("If PD+ and PD- do not differ under the prespecified rule, "
                          "the prospective PD test FAILS on the first item set ever "
                          "built that could run it, and the Phase 2 and Phase 5 "
                          "findings remain post-hoc. Reported as a failure, not "
                          "reframed."),
}


def task(task_id):
    return POOL.task(task_id)


def action_ids(task_id):
    return POOL.action_ids(task_id)


def clean_action(task_id):
    return POOL.clean_action(task_id)


def primary_net(task_id, action_id):
    return POOL.primary_net(task_id, action_id)


def participant_text(task_id):
    return POOL.participant_text(task_id)


def audit_leakage(task_id):
    return POOL.audit_leakage(task_id)


def pd_profile(coordinates, level):
    """The agent's drawn coordinates with PD overwritten. Nothing else moves."""
    if set(coordinates) != set(PARAMETERS):
        raise ValueError("Require exactly the ten parameter codes")
    out = dict(coordinates)
    out["PD"] = level
    return out


def verify_design(agents=None):
    """Everything the prediction depends on, checked before any call."""
    parent = POOL.verify_items()
    problems = []

    # The directional prediction requires clean -> good on EVERY item. If any
    # item broke that, PD+ and PD- would predict opposite signs on different
    # items and the pooled contrast would be meaningless.
    for task_id in TASK_IDS:
        clean = clean_action(task_id)
        other = next(a for a in action_ids(task_id) if a != clean)
        if primary_net(task_id, clean) != "good":
            problems.append(f"{task_id}: clean option does not classify good")
        if primary_net(task_id, other) != "not_good":
            problems.append(f"{task_id}: violating option does not classify not_good")
        if task_id not in ARRANGEMENT:
            problems.append(f"{task_id}: no stated arrangement recorded")
        if audit_leakage(task_id):
            problems.append(f"{task_id}: leakage {audit_leakage(task_id)}")
        if SCREENED[task_id]["modal"] >= 1.0:
            problems.append(f"{task_id}: saturated, cannot show an arm difference")

    # The two arms must differ in PD and nothing else.
    if agents:
        for agent in agents:
            lo = pd_profile(agent["coordinates"], PD_LOW)
            hi = pd_profile(agent["coordinates"], PD_HIGH)
            if {k: v for k, v in lo.items() if k != "PD"} != \
               {k: v for k, v in hi.items() if k != "PD"}:
                problems.append(f"agent {agent['agent']}: arms differ outside PD")
            if lo["PD"] == hi["PD"]:
                problems.append(f"agent {agent['agent']}: PD levels identical")

    if problems:
        raise ValueError("PD design verification failed: " + "; ".join(problems))
    return {"verified": True, "parent": parent, "tasks": len(TASK_IDS),
            "model": MODEL, "pd_levels": [PD_LOW, PD_HIGH],
            "clean_is_good_on_all_items": True,
            "mean_headroom": round(sum(min(SCREENED[t]["good"], 1 - SCREENED[t]["good"])
                                       for t in TASK_IDS) / len(TASK_IDS), 3),
            "agents_checked": len(agents) if agents else 0,
            "locked_prediction": LOCKED_PREDICTION}


def content_hash():
    payload = json.dumps({"tasks": list(TASK_IDS), "pd": [PD_LOW, PD_HIGH],
                          "arrangement": ARRANGEMENT,
                          "prediction": LOCKED_PREDICTION,
                          "parent": POOL.content_hash()},
                         sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def main():
    v = verify_design()
    print("verified:", v["verified"], "| model:", v["model"])
    print("items:", v["tasks"], "| mean headroom:", v["mean_headroom"])
    print("content hash:", content_hash())
    print()
    print(f"{'item':16s} {'clean option':22s} {'keeps':34s} {'clean':>7s} {'other':>9s}")
    for t in TASK_IDS:
        c = clean_action(t)
        o = next(a for a in action_ids(t) if a != c)
        print(f"  {t:14s} {c:22s} {ARRANGEMENT[t]:34s} "
              f"{primary_net(t, c):>7s} {primary_net(t, o):>9s}")
    print()
    print("PREDICTION:", LOCKED_PREDICTION["directional"])


if __name__ == "__main__":
    main()
