"""Three analyses a reviewer asked for, run on the frozen records. Zero API calls.

1. **TRUE minus SWAP, tested directly.** A significant TRUE contrast beside a
   non-significant SWAP contrast does not establish that the two differ
   (Gelman and Stern, 2006). For each swap design the within-unit difference
   of differences, (TRUE+ - TRUE-) - (SWAP+ - SWAP-), is computed per agent-item
   unit and given a paired bootstrap interval, an item-cluster interval and an
   exact sign test. The same is done for the label and position contrasts of the
   counterbalance.

2. **The two E - G contrasts refitted** under the crossed random-intercept model,
   which the thesis had described as applied to every headline contrast while
   the table left them blank.

3. **A random-slope refit** of every primary contrast, with a random slope of
   condition by item (`phase6_mixed_slopes`), which is the model that actually
   addresses treatment-effect heterogeneity across items.

None of this was prespecified. Output: experiments/phase5_analysis/review_tests.json.
"""
from __future__ import annotations

import json

import numpy as np
from scipy import stats

from phase3_budget import read_checked
from phase3_recognition_run import ROOT

import phase4b_gpt_pool as GPTPOOL
import phase4b_perm_pool as PERM
import phase4b_profiled_pool as PROF
import phase5_mixed_effects as ME
import phase6_mixed_slopes as MS
from phase5_refit_primary import CONTRASTS as PRIMARY

R = ROOT / "experiments"
SEED = 20260920
REPS = 10000
POOLS = {"perm": PERM, "profiled": PROF, "gpt": GPTPOOL}


def good_by_unit(path, pool, arms):
    data = read_checked(R / path)
    d = {}
    for r in data:
        arm = r.get("arm")
        if arm not in arms or not r.get("choice"):
            continue
        d.setdefault((str(r["agent"]), r["task"]), {})[arm] = 1.0 if pool.primary_net(r["task"], r["choice"]) == "good" else 0.0
    return {k: v for k, v in d.items() if all(a in v for a in arms)}


def boot(vals, seed):
    rng = np.random.default_rng(seed)
    x = np.asarray(vals)
    idx = rng.integers(0, len(x), size=(REPS, len(x)))
    m = x[idx].mean(axis=1)
    return [float(np.percentile(m, 2.5)), float(np.percentile(m, 97.5))]


def cluster_boot(items, vals, seed):
    rng = np.random.default_rng(seed + 1)
    by = {}
    for it, v in zip(items, vals):
        by.setdefault(it, []).append(v)
    arrs = [np.asarray(by[n]) for n in sorted(by)]
    out = np.empty(REPS)
    for b in range(REPS):
        pick = rng.integers(0, len(arrs), size=len(arrs))
        out[b] = np.concatenate([arrs[j][rng.integers(0, len(arrs[j]), size=len(arrs[j]))] for j in pick]).mean()
    return [float(np.percentile(out, 2.5)), float(np.percentile(out, 97.5))]


def diff_of_diffs(name, path, pool, hi1, lo1, hi2, lo2):
    u = good_by_unit(path, POOLS[pool], (hi1, lo1, hi2, lo2))
    items = [k[1] for k in u]
    d1 = np.array([v[hi1] - v[lo1] for v in u.values()])
    d2 = np.array([v[hi2] - v[lo2] for v in u.values()])
    dd = d1 - d2
    nz = dd[dd != 0]
    pos = int((nz > 0).sum())
    p_sign = float(stats.binomtest(pos, len(nz), 0.5).pvalue) if len(nz) else 1.0
    by_item = {}
    for it, v in zip(items, dd):
        by_item.setdefault(it, []).append(v)
    item_means = {k: float(np.mean(v)) for k, v in by_item.items()}
    return {"name": name, "path": path, "first": f"{hi1} - {lo1}", "second": f"{hi2} - {lo2}",
            "units": len(dd), "first_effect": float(d1.mean()), "second_effect": float(d2.mean()),
            "difference": float(dd.mean()), "ci95": boot(dd, SEED), "cluster_ci95": cluster_boot(items, dd, SEED),
            "sign_test": {"nonzero": int(len(nz)), "positive": pos, "p": p_sign},
            "items_positive": sum(1 for v in item_means.values() if v > 0),
            "items_negative": sum(1 for v in item_means.values() if v < 0),
            "item_means": item_means}


DIFFS = [
    ("PD: TRUE minus SWAP", "phase5_analysis/label_semantics_r1/all_rows.json", "perm", "TRUE+", "TRUE-", "SWAP+", "SWAP-"),
    ("ID: TRUE minus SWAP", "phase5_analysis/label_semantics_r2/all_rows.json", "perm", "ID:TRUE+", "ID:TRUE-", "ID:SWAP+", "ID:SWAP-"),
    ("LL: TRUE minus SWAP", "phase5_analysis/label_semantics_r2/all_rows.json", "perm", "LL:TRUE+", "LL:TRUE-", "LL:SWAP+", "LL:SWAP-"),
    ("label at line 6: A minus D", "phase5_analysis/position_counterbalance_r1/all_rows.json", "perm", "A+", "A-", "D+", "D-"),
    ("label at line 10: C minus B", "phase5_analysis/position_counterbalance_r1/all_rows.json", "perm", "C+", "C-", "B+", "B-"),
    ("position on PD: A minus C", "phase5_analysis/position_counterbalance_r1/all_rows.json", "perm", "A+", "A-", "C+", "C-"),
    ("position on AW: D minus B", "phase5_analysis/position_counterbalance_r1/all_rows.json", "perm", "D+", "D-", "B+", "B-"),
]


def rows_for(path, hi, lo, pool):
    data = read_checked(R / path)
    return [{"agent": r["agent"], "item": r["task"], "x": 1 if r["arm"] == hi else 0,
             "y": pool.primary_net(r["task"], r["choice"]) == "good"}
            for r in data if r.get("arm") in (hi, lo) and r.get("choice")]


EG = [("E vs G (gpt)", "phase4_coding/phase4b_gpt_r2/all_rows.json", "E", "G", "gpt"),
      ("E vs G (haiku)", "phase4_coding/phase4b_profiled_r1/all_rows.json", "E", "G", "profiled")]


def fit_robust(rows):
    """Fit from several starts; keep the converged fit with the best likelihood
    among those whose Wald standard error is finite and non-degenerate."""
    import math
    starts = [None,
              [0.0, 0.5, math.log(0.5), math.log(1.0), math.log(0.3)],
              [0.0, 1.0, math.log(0.7), math.log(1.2), math.log(0.8)],
              [-0.3, 0.3, math.log(0.4), math.log(0.6), math.log(0.15)]]
    fits = []
    for st in starts:
        f = MS.fit(rows, start=st)
        f["degenerate"] = not (np.isfinite(f["se"]) and f["se"] > 1e-4)
        fits.append(f)
    ok = [f for f in fits if not f["degenerate"]]
    best = min(ok or fits, key=lambda f: f["neg_loglik"])
    best["starts_tried"] = len(fits)
    best["starts_nondegenerate"] = len(ok)
    return best


def main():
    out = {"seed": SEED, "reps": REPS}
    print("== 1. difference of differences ==")
    out["diff_of_diffs"] = []
    for spec in DIFFS:
        r = diff_of_diffs(*spec)
        out["diff_of_diffs"].append(r)
        print(f"{r['name']:32s} {r['first_effect']:+.3f} vs {r['second_effect']:+.3f}  diff {r['difference']:+.3f} "
              f"95% [{r['ci95'][0]:+.3f}, {r['ci95'][1]:+.3f}] items [{r['cluster_ci95'][0]:+.3f}, {r['cluster_ci95'][1]:+.3f}] "
              f"sign p={r['sign_test']['p']:.4f} items {r['items_positive']}+/{r['items_negative']}-")

    print("\n== 2. E - G under the random-intercept model ==")
    out["eg_intercepts"] = []
    for name, path, hi, lo, pool in EG:
        f = ME.fit(rows_for(path, hi, lo, POOLS[pool]))
        rec = {"name": name, "beta": f["beta"], "se": f["se"], "p": f["p"], "sd_agent": f["sd_agent"], "sd_item": f["sd_item"]}
        out["eg_intercepts"].append(rec)
        print(f"{name:20s} beta {f['beta']:+.3f} p={f['p']:.6f} sd_item={f['sd_item']:.2f}")

    print("\n== 3. random slopes: validation ==")
    out["slopes_validation"] = MS.validate()
    print("\n== 3. random slopes: every primary contrast plus E - G ==")
    out["slopes"] = []
    specs = [(c["name"], c["path"], c["hi"], c["lo"], c["pool"], c["sign_p"]) for c in PRIMARY] + \
            [("sweep ID (gpt, 25 agents)", "phase5_analysis/coordinate_sweep_r2/all_rows.json", "ID+", "ID-", "perm", 7.025e-05),
             ("sweep LL (gpt, 25 agents)", "phase5_analysis/coordinate_sweep_r2/all_rows.json", "LL+", "LL-", "perm", 0.000117)] + \
            [(n, p, h, l, pool, None) for n, p, h, l, pool in EG]
    for name, path, hi, lo, pool, sign_p in specs:
        f = fit_robust(rows_for(path, hi, lo, POOLS[pool]))
        rec = {"name": name, "beta": f["beta"], "se": f["se"], "p": f["p"], "sd_agent": f["sd_agent"],
               "sd_item": f["sd_item"], "sd_slope": f["sd_slope"], "converged": f["converged"], "sign_p": sign_p,
               "degenerate": f["degenerate"], "starts_nondegenerate": f["starts_nondegenerate"]}
        out["slopes"].append(rec)
        flag = "" if sign_p is None or ((f["p"] < 0.05) == (sign_p < 0.05)) else "   <-- DISAGREES with sign test"
        print(f"{name:44s} beta {f['beta']:+.3f} se {f['se']:.3f} p={f['p']:.5f} sd_slope={f['sd_slope']:.2f} "
              f"[{f['starts_nondegenerate']}/{f['starts_tried']} starts ok]{flag}")

    path = R / "phase5_analysis/review_tests.json"
    path.write_text(json.dumps(out, indent=2, default=str), encoding="utf-8", newline="\n")
    print(f"\nwritten: {path}")


if __name__ == "__main__":
    main()
