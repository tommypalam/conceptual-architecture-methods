"""Offline rescore of id_crossmodel_r1. Zero API calls.

`id_crossmodel_r1` collected all 480 profiled decisions successfully - 481 calls,
zero failures - and then produced an empty analysis.

**The bug, and it is a repeat.** This designation drops the U screen arm
(`SCREEN_N = 0`), because its six items were screened on haiku in
`phase4b_profiled_r1`. But `collect()` derives its task list from the screen:

    usable = [t for t, v in screen.items() if v["usable"]]

With no screen probes, `screen` is empty, `usable` is empty, and `analyse()`
filters every contrast to an empty task list. Both arms report n=0 and the pooled
contrast is None.

**This is the same defect as `coordinate_sweep_r2`**, which I had already
diagnosed and written up in `phase5_sweep_rescore.py`. The collector for this
designation was adapted from that one and inherited the defect unfixed: I
corrected the *symptom* there with a rescore module and did not carry the lesson
into the next collector built on it. The remedy is identical and the repetition
is recorded rather than quietly patched.

**Nothing is wrong with the data.** All 480 decisions are in `all_rows.json`,
240 per arm, 80 per item across six items, 40 agents, zero invalid.

**Why this module rather than a fix in place.** `phase5_id_crossmodel_r1.py` is
hash-pinned by its own release. Editing it would break `verify()` for any
designation inheriting from it, exactly as an earlier in-place correction did for
`phase4_capstone_specificity_r2`. The collector stays frozen.

**The task list used here is the designation's own declared item set** -
`phase4b_profiled_pool.TASK_IDS`, the six items the protocol names and the review
accepted - not a list chosen after seeing results. That is the list `usable`
would have held had the screen run.
"""
from __future__ import annotations

import json
import math

import phase4b_profiled_pool as P
import phase5_id_crossmodel as IDX


def load():
    from phase3_budget import read_checked
    from phase3_recognition_run import ROOT
    root = ROOT / "experiments/phase5_analysis/id_crossmodel_r1"
    return read_checked(root / "all_rows.json")


def paired(rows, tasks):
    """The designation's own paired contrast, reproduced exactly."""
    hi_arm, lo_arm = "ID+", "ID-"
    by = {}
    for r in rows:
        if r["arm"] in (hi_arm, lo_arm) and r["task"] in tasks and r["choice"]:
            by.setdefault((r["agent"], r["task"]), {})[r["arm"]] = (
                P.primary_net(r["task"], r["choice"]) == "good")
    pairs = [(v[lo_arm], v[hi_arm]) for v in by.values() if len(v) == 2]
    if not pairs:
        return None
    hi_only = sum(1 for lo, hi in pairs if hi and not lo)
    lo_only = sum(1 for lo, hi in pairs if lo and not hi)
    n = hi_only + lo_only
    if n == 0:
        p = 1.0
    else:
        k = min(hi_only, lo_only)
        p = min(1.0, 2 * sum(math.comb(n, i) for i in range(k + 1)) / (2 ** n))
    return {"pairs": len(pairs), "good_more_under_high": hi_only,
            "good_more_under_low": lo_only, "discordant": n,
            "effect": round((hi_only - lo_only) / len(pairs), 4),
            "p": round(p, 8)}


def rescore():
    rows = load()
    tasks = list(P.TASK_IDS)   # the declared item set, not an outcome-chosen one

    def rate(arm):
        vals = [P.primary_net(r["task"], r["choice"]) == "good"
                for r in rows if r["arm"] == arm and r["choice"]]
        return {"good_rate": round(sum(vals) / len(vals), 4), "n": len(vals)}

    cells = {arm: rate(arm) for arm in ("ID-", "ID+")}
    pooled = paired(rows, tasks)
    per_item = {t: paired(rows, [t]) for t in tasks}

    item_p = {t: v["p"] for t, v in per_item.items() if v}
    live = sorted(item_p.items(), key=lambda kv: kv[1])
    holm, running = {}, 0.0
    for i, (t, raw) in enumerate(live):
        running = min(1.0, max(running, raw * (len(live) - i)))
        holm[t] = round(running, 8)

    effs = [v["effect"] for v in per_item.values() if v]
    pos = sum(1 for e in effs if e > 0)
    neg = sum(1 for e in effs if e < 0)
    consistency = {"items": len(effs), "positive": pos, "negative": neg,
                   "majority": max(pos, neg), "meets_requirement": max(pos, neg) >= 4}

    moved = bool(pooled and pooled["p"] < 0.05 and consistency["meets_requirement"])
    gpt = IDX.GPT_MEASURED["label_semantics_r2_true"]

    if not pooled:
        reading = "no pairs; nothing measured"
    elif moved:
        same = (pooled["effect"] > 0) == (gpt > 0)
        reading = (
            "ID moves the outcome on haiku, SAME sign as gpt. ID's effect is not "
            "specific to the calibration model. This licenses `ID moves the "
            "outcome on haiku too`, NOT `ID is verified cross-model`: "
            "verification on gpt required a null swap control, which this "
            "designation does not run."
            if same else
            "ID moves the outcome on haiku with the OPPOSITE sign to gpt. "
            "Reported as measured, not reframed, exactly as LL's sign reversal "
            "was. A cross-model sign reversal on a manipulated coordinate is a "
            "stronger version of the LL finding and must not be smoothed.")
    else:
        reading = (
            "ID did NOT move the outcome on haiku under the prespecified rule. "
            "Power was 16/20 at ID's measured gpt effect of +0.111, so this is a "
            "WEAK null at 80% - not evidence that ID is inert on haiku. The "
            "verified coordinate map is `two of ten, on one model`, and the "
            "paper scopes its coordinate claims to gpt. This designation is NOT "
            "re-run with more agents.")

    return {"rows": len(rows), "tasks": tasks, "cells": cells,
            "pooled": pooled, "per_item": per_item, "holm_per_item": holm,
            "holm_family_size": len(live), "consistency": consistency,
            "moved_outcome": moved, "reading": reading,
            "gpt_reference": IDX.GPT_MEASURED,
            "architecture_crossmodel": IDX.ARCHITECTURE_CROSSMODEL,
            "power": IDX.MEASURED_POWER,
            "primary_test": ("pooled paired ID+ vs ID- p < 0.05 AND the effect "
                             "pointing the same direction in at least 4 of 6 "
                             "items; both required, prespecified, two-sided"),
            "item_overlap_with_gpt": {
                "haiku_items": list(P.TASK_IDS),
                "note": ("Four of six overlap with gpt's seven. ward_transfer is "
                         "haiku-only; on_call and rest_break are gpt-only.")},
            "correction_note": ("id_crossmodel_r1 dropped the screen arm, so its "
                                "collect() derived an empty usable-task list and "
                                "every contrast returned None - the same defect as "
                                "coordinate_sweep_r2, inherited unfixed by a "
                                "collector adapted from it. The data are intact; "
                                "this rescore supplies the designation's own "
                                "declared item set. No API call was made and no "
                                "frozen source was edited.")}


def main():
    out = rescore()
    print(f"decisions rescored: {out['rows']} over {len(out['tasks'])} items\n")
    for arm, v in out["cells"].items():
        print(f"  {arm:4s} good_rate={v['good_rate']:.4f}  n={v['n']}")
    p = out["pooled"]
    print(f"\nPOOLED  effect={p['effect']:+.4f}  pairs={p['pairs']}  "
          f"discordant={p['discordant']}  p={p['p']:.8f}")
    print(f"consistency: {out['consistency']['positive']}+/"
          f"{out['consistency']['negative']}-  "
          f"meets={out['consistency']['meets_requirement']}")
    print(f"\n{'item':16s} {'effect':>8s} {'p':>10s} {'HOLM':>10s}")
    for t, v in out["per_item"].items():
        print(f"{t:16s} {v['effect']:>+8.3f} {v['p']:>10.5f} "
              f"{out['holm_per_item'][t]:>10.5f}")
    print(f"\nMOVED OUTCOME: {out['moved_outcome']}")
    print(f"\ngpt reference: TRUE {out['gpt_reference']['label_semantics_r2_true']:+.3f}, "
          f"SWAP {out['gpt_reference']['label_semantics_r2_swap']:+.3f}")
    print(f"\nREADING:\n{out['reading']}")
    return out


if __name__ == "__main__":
    out = main()
    from phase3_recognition_run import ROOT
    target = ROOT / "experiments/phase5_analysis/id_crossmodel_r1"
    (target / "rescored.json").write_text(
        json.dumps(out, indent=2, sort_keys=True), encoding="utf-8")
    print(f"\nwritten: {target / 'rescored.json'}")
