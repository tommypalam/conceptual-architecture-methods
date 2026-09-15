"""Offline rescore of coordinate_sweep_r2. Zero API calls.

`coordinate_sweep_r2` collected all 2,800 profiled decisions successfully - 2,801
calls, zero failures - and then produced an empty analysis.

**The bug.** This designation drops the U screen arm (`SCREEN_N = 0`), because
its seven items had already been screened four times on gpt with consistent
results. But `collect()` derives its task list from the screen:

    usable = [t for t, v in screen.items() if v["usable"]]

With no screen probes, `screen` is empty, `usable` is empty, and `analyse()`
filters every contrast to an empty task list. Every contrast came back `None`
and the Holm family had size 0.

**Nothing is wrong with the data.** All 2,800 decisions are present in
`all_rows.json`, 175 per arm across 16 arms, 400 per item across seven items.
The failure is in how the analysis was handed its task list, not in collection.

**Why this module exists rather than a fix in place.** `phase5_coordinate_sweep_r2.py`
is hash-pinned by its own release. Editing it would break `verify()` on every
future designation that inherits from it, exactly as an earlier in-place
correction did for `phase4_capstone_specificity_r2`. The correction lives here,
the collector stays frozen, and the release remains valid.

**The task list used here is the designation's own declared item set** -
`phase4b_perm_pool.TASK_IDS`, the seven items the protocol names and the review
accepted - not a list chosen after seeing results. That is the list `usable`
would have held had the screen run.
"""
from __future__ import annotations

import json
import math

import phase4b_perm_pool as P
import phase5_coordinate_sweep as SW


def load():
    from phase3_budget import read_checked
    from phase3_recognition_run import ROOT
    root = ROOT / "experiments/phase5_analysis/coordinate_sweep_r2"
    return read_checked(root / "all_rows.json")


def paired(rows, tasks, coordinate):
    """The designation's own paired contrast, reproduced exactly."""
    hi_arm, lo_arm = f"{coordinate}+", f"{coordinate}-"
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
    return {"coordinate": coordinate, "pairs": len(pairs),
            "good_more_under_high": hi_only, "good_more_under_low": lo_only,
            "discordant": n, "effect": round((hi_only - lo_only) / len(pairs), 4),
            "p": round(p, 8)}


def rescore():
    rows = load()
    tasks = list(P.TASK_IDS)   # the declared item set, not an outcome-chosen one

    contrasts = {c: paired(rows, tasks, c) for c in SW.SWEPT}
    per_item = {c: {t: paired(rows, [t], c) for t in tasks} for c in SW.SWEPT}

    pooled = {c: v["p"] for c, v in contrasts.items() if v}
    live = sorted(pooled.items(), key=lambda kv: kv[1])
    holm, running = {}, 0.0
    for i, (c, raw) in enumerate(live):
        running = min(1.0, max(running, raw * (len(live) - i)))
        holm[c] = round(running, 8)

    def consistency(c):
        effs = [v["effect"] for v in per_item[c].values() if v]
        pos = sum(1 for e in effs if e > 0)
        neg = sum(1 for e in effs if e < 0)
        return {"items": len(effs), "positive": pos, "negative": neg,
                "meets_requirement": max(pos, neg) >= 4}

    cons = {c: consistency(c) for c in SW.SWEPT}
    survivors = [c for c in SW.SWEPT
                 if holm.get(c, 1.0) < 0.05 and cons[c]["meets_requirement"]]

    rates = {}
    for arm in sorted({r["arm"] for r in rows}):
        vals = [P.primary_net(r["task"], r["choice"]) == "good"
                for r in rows if r["arm"] == arm and r["choice"]]
        if vals:
            rates[arm] = {"good_rate": round(sum(vals) / len(vals), 4), "n": len(vals)}

    return {"rows": len(rows), "tasks": tasks,
            "arm_rates": rates, "contrasts": contrasts, "per_item": per_item,
            "holm": holm, "holm_family_size": len(live),
            "consistency": cons, "survivors": survivors,
            "ranked_by_abs_effect": sorted(
                SW.SWEPT, key=lambda c: -abs(contrasts[c]["effect"]) if contrasts[c] else 0),
            "reference": SW.ALREADY_TESTED,
            "decision_rule": ("pooled Holm p < 0.05 over all eight contrasts as one "
                              "family, AND the effect in the same direction in at "
                              "least 4 of 7 items"),
            "correction_note": ("coordinate_sweep_r2 dropped the screen arm, so its "
                                "collect() derived an empty usable-task list and "
                                "every contrast returned None. The data are intact; "
                                "this rescore supplies the designation's own declared "
                                "item set. No API call was made and no frozen source "
                                "was edited.")}


def main():
    out = rescore()
    print(f"decisions rescored: {out['rows']}  over {len(out['tasks'])} items\n")
    print(f"{'coord':6s} {'effect':>8s} {'pairs':>6s} {'raw p':>11s} {'HOLM':>11s} "
          f"{'items':>8s}  survives")
    for c in out["ranked_by_abs_effect"]:
        v = out["contrasts"][c]
        if not v:
            continue
        h = out["holm"].get(c, 1.0)
        k = out["consistency"][c]
        mark = "YES" if c in out["survivors"] else ""
        print(f"  {c:4s} {v['effect']:>+8.3f} {v['pairs']:>6d} {v['p']:>11.6f} "
              f"{h:>11.6f} {str(k['positive'])+'+/'+str(k['negative'])+'-':>8s}  {mark}")
    print(f"\nSURVIVORS: {out['survivors'] or 'NONE'}")
    print("\nreference (label_semantics_r1, 40 agents):")
    for k, v in out["reference"].items():
        print(f"   {k}: {v['effect']:+.3f}  Holm {v['holm']}  -> {v['verdict']}")
    return out


if __name__ == "__main__":
    out = main()
    from phase3_recognition_run import ROOT
    target = ROOT / "experiments/phase5_analysis/coordinate_sweep_r2"
    (target / "rescored.json").write_text(
        json.dumps(out, indent=2, sort_keys=True), encoding="utf-8")
    print(f"\nwritten: {target / 'rescored.json'}")
