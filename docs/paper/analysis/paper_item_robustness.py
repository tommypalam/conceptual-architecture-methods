"""Item- and agent-level robustness for the paper's headline contrasts.

Zero API calls. Reads frozen all_rows.json records only; writes one JSON summary.
For every contrast (paired high-minus-low keep-rate within agent and item):

  unit      percentile bootstrap over agent-item differences (as in the designations)
  item      two-stage bootstrap: resample items, then agent-item units within item
  crossed   pigeonhole bootstrap: resample agents AND items independently, keep
            every agent-item cell of the resampled pair (crossed random factors)
  items_t   one-sample t over the k per-item effects (items as the unit, df = k-1)
  items_sign exact two-sided sign test over per-item effects

Items are few (3-7), so item-level intervals are wide and their coverage is itself
uncertain; they are reported as sensitivity analyses, not as replacements for the
prespecified tests.
"""
from __future__ import annotations
import json, math, sys
from collections import defaultdict
from pathlib import Path
import numpy as np
from scipy import stats

ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
OUT = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("paper_item_robustness.json")
B = 10_000
SEED = 2026092301

KEEP = {"keep_desk", "keep_lease", "return_press", "leave_unfilled", "keep_slot",
        "keep_rest", "keep_saturday", "leave_arrangement"}


def rows(rel):
    return json.load(open(ROOT / rel))["payload"]


def cells(rs, arm_hi, arm_lo, key=lambda r: (r["agent"], r["task"]), tasks=None):
    """{(agent, task): (hi - lo)} for units complete in both arms. None choices dropped."""
    hi, lo = defaultdict(list), defaultdict(list)
    for r in rs:
        if r.get("choice") is None or (tasks and r["task"] not in tasks):
            continue
        k = key(r)
        v = 1.0 if r["choice"] in KEEP else 0.0
        if r["arm"] == arm_hi:
            hi[k].append(v)
        elif r["arm"] == arm_lo:
            lo[k].append(v)
    return {k: np.mean(hi[k]) - np.mean(lo[k]) for k in hi if k in lo}


def combine(*ds, weights=None):
    """Linear combination of unit-level contrasts over common units (e.g. TRUE - SWAP)."""
    weights = weights or [1] * len(ds)
    common = set.intersection(*(set(d) for d in ds))
    return {k: sum(w * d[k] for w, d in zip(weights, ds)) for k in common}


def summarise(d, rng):
    keys = sorted(d)
    agents = sorted({k[0] for k in keys})
    items = sorted({k[1] for k in keys})
    diff = np.array([d[k] for k in keys])
    est = float(diff.mean())
    # unit bootstrap
    idx = rng.integers(0, len(diff), size=(B, len(diff)))
    unit = np.percentile(diff[idx].mean(axis=1), [2.5, 97.5])
    # per-item
    by_item = {i: np.array([d[k] for k in keys if k[1] == i]) for i in items}
    item_eff = {i: float(v.mean()) for i, v in by_item.items()}
    # two-stage item bootstrap
    ib = np.empty(B)
    for b in range(B):
        pick = rng.choice(items, size=len(items), replace=True)
        vals = [by_item[i][rng.integers(0, len(by_item[i]), len(by_item[i]))] for i in pick]
        ib[b] = np.concatenate(vals).mean()
    item_ci = np.percentile(ib, [2.5, 97.5])
    # crossed (pigeonhole) bootstrap over agents x items
    a_ix = {a: n for n, a in enumerate(agents)}
    i_ix = {i: n for n, i in enumerate(items)}
    M = np.full((len(agents), len(items)), np.nan)
    for k in keys:
        M[a_ix[k[0]], i_ix[k[1]]] = d[k]
    cb = np.empty(B)
    for b in range(B):
        ra = rng.integers(0, len(agents), len(agents))
        ri = rng.integers(0, len(items), len(items))
        cb[b] = np.nanmean(M[np.ix_(ra, ri)])
    crossed = np.percentile(cb, [2.5, 97.5])
    ie = np.array(list(item_eff.values()))
    if len(ie) > 1 and ie.std(ddof=1) > 0:
        t = stats.ttest_1samp(ie, 0.0)
        t_p = float(t.pvalue)
        half = stats.t.ppf(0.975, len(ie) - 1) * ie.std(ddof=1) / math.sqrt(len(ie))
        t_ci = [float(ie.mean() - half), float(ie.mean() + half)]
    else:
        t_p, t_ci = None, None
    pos, neg = int((ie > 0).sum()), int((ie < 0).sum())
    sign_p = float(stats.binomtest(pos, pos + neg, 0.5).pvalue) if pos + neg else None
    return {
        "estimate": round(est, 4), "n_units": len(keys), "n_agents": len(agents),
        "n_items": len(items),
        "unit_ci": [round(float(x), 4) for x in unit],
        "item_ci": [round(float(x), 4) for x in item_ci],
        "crossed_ci": [round(float(x), 4) for x in crossed],
        "items_mean": round(float(ie.mean()), 4),
        "items_t_ci": [round(x, 4) for x in t_ci] if t_ci else None,
        "items_t_p": round(t_p, 6) if t_p is not None else None,
        "items_pos_neg": [pos, neg], "items_sign_p": round(sign_p, 4) if sign_p else None,
        "per_item": {i: round(v, 4) for i, v in item_eff.items()},
    }


def main():
    rng = np.random.default_rng(SEED)
    C = {}
    sem = rows("phase7_understanding/semantics_r1/all_rows.json")
    for v in ("CANON", "FLIP", "INVERT", "NONCE"):
        C[f"semantics_r1:{v}"] = cells(sem, f"{v}+", f"{v}-")
    C["semantics_r1:CANON-FLIP"] = combine(C["semantics_r1:CANON"], C["semantics_r1:FLIP"], weights=[1, -1])
    C["semantics_r1:CANON-NONCE"] = combine(C["semantics_r1:CANON"], C["semantics_r1:NONCE"], weights=[1, -1])

    pf = rows("phase7_understanding/probe_fields_r1/all_rows.json")
    for p in ("SQ", "SW", "NC", "WO"):
        C[f"probe_fields_r1:{p}"] = cells(pf, f"{p}+", f"{p}-")
    C["probe_fields_r1:SQ-NC"] = combine(C["probe_fields_r1:SQ"], C["probe_fields_r1:NC"], weights=[1, -1])

    pp = rows("phase5_analysis/pd_prospective_r1/all_rows.json")
    C["pd_prospective_r1:PD"] = cells(pp, "PD+", "PD-")

    ls = rows("phase5_analysis/label_semantics_r1/all_rows.json")
    C["label_semantics_r1:TRUE"] = cells(ls, "TRUE+", "TRUE-")
    C["label_semantics_r1:SWAP"] = cells(ls, "SWAP+", "SWAP-")
    C["label_semantics_r1:TRUE-SWAP"] = combine(C["label_semantics_r1:TRUE"], C["label_semantics_r1:SWAP"], weights=[1, -1])

    ls2 = rows("phase5_analysis/label_semantics_r2/all_rows.json")
    C["label_semantics_r2:ID_TRUE-SWAP"] = combine(cells(ls2, "ID:TRUE+", "ID:TRUE-"), cells(ls2, "ID:SWAP+", "ID:SWAP-"), weights=[1, -1])

    pc = rows("phase5_analysis/position_counterbalance_r1/all_rows.json")
    for c in "ABCD":
        C[f"position_counterbalance_r1:{c}"] = cells(pc, f"{c}+", f"{c}-")
    A, Bc, Cc, D = (C[f"position_counterbalance_r1:{c}"] for c in "ABCD")
    C["position_counterbalance_r1:field_factor"] = combine(A, Cc, Bc, D, weights=[.5, .5, -.5, -.5])
    C["position_counterbalance_r1:position_factor"] = combine(A, D, Cc, Bc, weights=[.5, .5, -.5, -.5])

    fl = rows("phase7_understanding/floor_lift_r1/all_rows.json")
    floored = {"rest_break", "storage_unit", "tool_library"}
    Lpd = cells(fl, "PD:TWIN+", "PD:TWIN-", tasks=floored)
    Lsq = cells(fl, "SQ:TWIN+", "SQ:TWIN-", tasks=floored)
    C["floor_lift_r1:L_PD"], C["floor_lift_r1:L_SQ"] = Lpd, Lsq
    C["floor_lift_r1:L_SQ-L_PD"] = combine(Lsq, Lpd, weights=[1, -1])
    C["floor_lift_r1:PD_BASE"] = cells(fl, "PD:BASE+", "PD:BASE-")
    C["floor_lift_r1:SQ_BASE"] = cells(fl, "SQ:BASE+", "SQ:BASE-")

    pr = rows("phase7_understanding/precipitation_r3/all_rows.json")
    key = lambda r: (r["agent"], r["task"])
    C["precipitation_r3:INSTANCES-NEITHER"] = cells(pr, "INSTANCES", "NEITHER", key=key)
    C["precipitation_r3:RULE-NEITHER"] = cells(pr, "RULE", "NEITHER", key=key)
    C["precipitation_r3:RULE-INSTANCES"] = cells(pr, "RULE", "INSTANCES", key=key)

    f1 = rows("phase7_understanding/parameter_followup_r1/all_rows.json")
    f2 = rows("phase7_understanding/parameter_followup_r2/all_rows.json")
    for c, src in (("AW", f1), ("LL", f1), ("TfA", f2), ("MoR", f2)):
        C[f"parameter_followup:{c}"] = cells(src, f"{c}+", f"{c}-")

    C["pd_crossmodel_r1:PD_haiku"] = cells(rows("phase5_analysis/pd_crossmodel_r1/all_rows.json"), "PD+", "PD-")
    C["id_crossmodel_r1:ID_haiku"] = cells(rows("phase5_analysis/id_crossmodel_r1/all_rows.json"), "ID+", "ID-")

    out = {"note": __doc__.strip().splitlines()[0], "B": B, "seed": SEED,
           "api_calls": 0, "contrasts": {k: summarise(v, rng) for k, v in C.items()}}
    OUT.write_text(json.dumps(out, indent=1))
    for k, s in out["contrasts"].items():
        print(f"{k:42s} {s['estimate']:+.4f} unit{s['unit_ci']} item{s['item_ci']} crossed{s['crossed_ci']} "
              f"t_p={s['items_t_p']} {s['items_pos_neg']} sign_p={s['items_sign_p']} n={s['n_units']}")


if __name__ == "__main__":
    main()
