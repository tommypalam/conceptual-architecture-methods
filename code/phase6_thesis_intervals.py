"""Paired bootstrap intervals and equivalence bounds for the thesis contrasts.

Zero API calls. Reads each designation's frozen, checksum-verified
`all_rows.json`, reconstructs the paired (agent, item) units for every headline
contrast the thesis reports, and computes:

  * the paired effect (mean of within-unit differences in the `good`
    classification), which reproduces the prespecified point estimate;
  * a percentile bootstrap 95% and 90% interval over agent-item units
    (10,000 resamples, fixed seed);
  * a two-stage cluster bootstrap that resamples items first and then units
    within item, as a robustness check on item heterogeneity;
  * for the sweep's non-significant coordinates, the smallest symmetric margin
    that contains the 90% interval, which is the bound an equivalence (TOST)
    test at alpha = 0.05 would certify.

None of this was prespecified. The sign tests remain the primary analysis; this
module supplies the interval estimates the project's own reporting rule asks for
and the bounded reading of the sweep's nulls. Nothing here can alter a record.
"""
from __future__ import annotations

import json

import numpy as np

from phase3_budget import read_checked
from phase3_recognition_run import ROOT

import phase4b_gpt_pool as GPTPOOL
import phase4b_perm_pool as PERM
import phase4b_profiled_pool as PROF

R = ROOT / "experiments"
SEED = 20260919
REPS = 10000
POOLS = {"perm": PERM, "profiled": PROF, "gpt": GPTPOOL}


def units(path, hi, lo, pool):
    """Within-unit differences hi - lo in the good classification, keyed by item."""
    data = read_checked(R / path)
    d = {}
    for r in data:
        arm = r.get("arm")
        if arm not in (hi, lo) or not r.get("choice"):
            continue
        key = (str(r["agent"]), r["task"])
        d.setdefault(key, {})[arm] = 1.0 if pool.primary_net(r["task"], r["choice"]) == "good" else 0.0
    out = [(k[1], v[hi] - v[lo]) for k, v in d.items() if hi in v and lo in v]
    return out


def boot(diffs, reps=REPS, seed=SEED):
    rng = np.random.default_rng(seed)
    x = np.asarray(diffs)
    n = len(x)
    idx = rng.integers(0, n, size=(reps, n))
    return x[idx].mean(axis=1)


def cluster_boot(items, diffs, reps=REPS, seed=SEED):
    rng = np.random.default_rng(seed + 1)
    by = {}
    for it, dd in zip(items, diffs):
        by.setdefault(it, []).append(dd)
    names = sorted(by)
    arrs = [np.asarray(by[n]) for n in names]
    out = np.empty(reps)
    for b in range(reps):
        pick = rng.integers(0, len(names), size=len(names))
        vals = []
        for j in pick:
            a = arrs[j]
            vals.append(a[rng.integers(0, len(a), size=len(a))])
        out[b] = np.concatenate(vals).mean()
    return out


def pct(m, lo, hi):
    return [float(np.percentile(m, lo)), float(np.percentile(m, hi))]


CONTRASTS = [
    ("E vs G (gpt)", "phase4_coding/phase4b_gpt_r2/all_rows.json", "E", "G", "gpt", "6"),
    ("E vs G (haiku)", "phase4_coding/phase4b_profiled_r1/all_rows.json", "E", "G", "profiled", "6"),
    ("PD prospective (gpt)", "phase5_analysis/pd_prospective_r1/all_rows.json", "PD+", "PD-", "perm", "7.1"),
    ("PD swap TRUE", "phase5_analysis/label_semantics_r1/all_rows.json", "TRUE+", "TRUE-", "perm", "7.2"),
    ("PD swap SWAP", "phase5_analysis/label_semantics_r1/all_rows.json", "SWAP+", "SWAP-", "perm", "7.2"),
    ("Counterbalance A (PD, line 6)", "phase5_analysis/position_counterbalance_r1/all_rows.json", "A+", "A-", "perm", "7.3"),
    ("Counterbalance C (PD, line 10)", "phase5_analysis/position_counterbalance_r1/all_rows.json", "C+", "C-", "perm", "7.3"),
    ("Counterbalance B (AW, line 10)", "phase5_analysis/position_counterbalance_r1/all_rows.json", "B+", "B-", "perm", "7.3"),
    ("Counterbalance D (AW, line 6)", "phase5_analysis/position_counterbalance_r1/all_rows.json", "D+", "D-", "perm", "7.3"),
    ("ID swap TRUE", "phase5_analysis/label_semantics_r2/all_rows.json", "ID:TRUE+", "ID:TRUE-", "perm", "7.6"),
    ("ID swap SWAP", "phase5_analysis/label_semantics_r2/all_rows.json", "ID:SWAP+", "ID:SWAP-", "perm", "7.6"),
    ("LL TRUE", "phase5_analysis/label_semantics_r2/all_rows.json", "LL:TRUE+", "LL:TRUE-", "perm", "7.6"),
    ("LL SWAP", "phase5_analysis/label_semantics_r2/all_rows.json", "LL:SWAP+", "LL:SWAP-", "perm", "7.6"),
    ("PD cross-provider (haiku)", "phase5_analysis/pd_crossmodel_r1/all_rows.json", "PD+", "PD-", "profiled", "8"),
    ("ID cross-provider (haiku)", "phase5_analysis/id_crossmodel_r1/all_rows.json", "ID+", "ID-", "profiled", "8"),
] + [
    (f"sweep {c}", "phase5_analysis/coordinate_sweep_r2/all_rows.json", f"{c}+", f"{c}-", "perm", "7.5")
    for c in ("ID", "LL", "TfA", "MoR", "MS", "RE", "RT", "CS")
]


def run(verbose=True):
    results = []
    for name, path, hi, lo, pool, sec in CONTRASTS:
        u = units(path, hi, lo, POOLS[pool])
        items = [a for a, _ in u]
        diffs = [b for _, b in u]
        m = boot(diffs)
        cm = cluster_boot(items, diffs)
        ci90 = pct(m, 5, 95)
        rec = {"name": name, "section": sec, "path": path, "hi": hi, "lo": lo,
               "pairs": len(u), "items": len(set(items)),
               "effect": float(np.mean(diffs)),
               "ci95": pct(m, 2.5, 97.5), "ci90": ci90,
               "cluster_ci95": pct(cm, 2.5, 97.5),
               "equivalence_margin_90": float(max(abs(ci90[0]), abs(ci90[1])))}
        results.append(rec)
        if verbose:
            print(f"{name:32s} n={rec['pairs']:4d} effect {rec['effect']:+.3f} "
                  f"95% [{rec['ci95'][0]:+.3f}, {rec['ci95'][1]:+.3f}] "
                  f"item-cluster [{rec['cluster_ci95'][0]:+.3f}, {rec['cluster_ci95'][1]:+.3f}] "
                  f"90% margin {rec['equivalence_margin_90']:.3f}")
    return results


def main():
    res = run()
    out = ROOT / "experiments/phase5_analysis/thesis_intervals.json"
    out.write_text(json.dumps({"seed": SEED, "reps": REPS, "results": res}, indent=2), encoding="utf-8")
    print(f"\nwritten: {out}")


if __name__ == "__main__":
    main()
