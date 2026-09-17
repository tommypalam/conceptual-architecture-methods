"""Refit every primary contrast as a mixed-effects logistic model. Zero API calls.

The sign tests remain the prespecified primary analysis. This module is the
robustness check the thesis's own statistical section called for and did not run:
crossed random intercepts for agent and item, fitted by Laplace approximation in
`phase5_mixed_effects`.

Reads the frozen `all_rows.json` of each designation, reconstructs the paired
conditions, and fits. Nothing here can alter a collected record.
"""
from __future__ import annotations

import json
import pathlib

from phase3_budget import read_checked
from phase3_recognition_run import ROOT

import phase5_mixed_effects as ME

R = ROOT / "experiments"


def _rows(path, hi, lo, pool, task_filter=None):
    """Observations for a two-condition contrast, in the model's input format."""
    data = read_checked(R / path)
    out = []
    for r in data:
        arm = r.get("arm")
        if arm not in (hi, lo):
            continue
        if not r.get("choice"):
            continue
        if task_filter and r["task"] not in task_filter:
            continue
        out.append({"agent": r["agent"], "item": r["task"],
                    "x": 1 if arm == hi else 0,
                    "y": pool.primary_net(r["task"], r["choice"]) == "good"})
    return out


CONTRASTS = []


def _register(name, path, hi, lo, pool_name, sign_effect, sign_p, note=""):
    CONTRASTS.append({"name": name, "path": path, "hi": hi, "lo": lo,
                      "pool": pool_name, "sign_effect": sign_effect,
                      "sign_p": sign_p, "note": note})


# The contrasts the thesis reports as primary, with their sign-test results.
_register("PD prospective (gpt)",
          "phase5_analysis/pd_prospective_r1/all_rows.json", "PD+", "PD-",
          "perm", +0.346, 0.0, "Chapter 7.1")
_register("PD swap TRUE (gpt)",
          "phase5_analysis/label_semantics_r1/all_rows.json", "TRUE+", "TRUE-",
          "perm", +0.339, 0.0, "Chapter 7.2")
_register("PD swap SWAP (gpt)",
          "phase5_analysis/label_semantics_r1/all_rows.json", "SWAP+", "SWAP-",
          "perm", -0.036, 0.260, "Chapter 7.2 - the inert control")
_register("PD counterbalance A (label PD, line 6)",
          "phase5_analysis/position_counterbalance_r1/all_rows.json", "A+", "A-",
          "perm", +0.393, 0.0, "Chapter 7.3")
_register("PD counterbalance C (label PD, line 10)",
          "phase5_analysis/position_counterbalance_r1/all_rows.json", "C+", "C-",
          "perm", +0.271, 0.0, "Chapter 7.3")
_register("PD counterbalance B (label AW, line 10)",
          "phase5_analysis/position_counterbalance_r1/all_rows.json", "B+", "B-",
          "perm", +0.061, 0.078, "Chapter 7.3 / 7.4")
_register("PD counterbalance D (label AW, line 6)",
          "phase5_analysis/position_counterbalance_r1/all_rows.json", "D+", "D-",
          "perm", +0.004, 1.000, "Chapter 7.3 - the decisive cell")
_register("ID swap TRUE (gpt)",
          "phase5_analysis/label_semantics_r2/all_rows.json", "ID:TRUE+", "ID:TRUE-",
          "perm", +0.111, 0.00117, "Chapter 7.6")
_register("ID swap SWAP (gpt)",
          "phase5_analysis/label_semantics_r2/all_rows.json", "ID:SWAP+", "ID:SWAP-",
          "perm", +0.046, 0.136, "Chapter 7.6")
_register("LL swap TRUE (gpt) - the withdrawal",
          "phase5_analysis/label_semantics_r2/all_rows.json", "LL:TRUE+", "LL:TRUE-",
          "perm", -0.014, 0.708, "Chapter 7.6 - failed to replicate")
_register("PD cross-provider (haiku)",
          "phase5_analysis/pd_crossmodel_r1/all_rows.json", "PD+", "PD-",
          "profiled", +0.133, 0.00031, "Chapter 8")
_register("ID cross-provider (haiku)",
          "phase5_analysis/id_crossmodel_r1/all_rows.json", "ID+", "ID-",
          "profiled", +0.075, 0.0328, "Chapter 8")


def run(verbose=True):
    import phase4b_perm_pool as PERM
    import phase4b_profiled_pool as PROF
    pools = {"perm": PERM, "profiled": PROF}

    results = []
    for c in CONTRASTS:
        pool = pools[c["pool"]]
        rows = _rows(c["path"], c["hi"], c["lo"], pool)
        if not rows:
            results.append({**c, "error": "no rows"})
            continue
        f = ME.fit(rows)
        agrees = (f["p"] < 0.05) == (c["sign_p"] < 0.05)
        same_sign = (f["beta"] > 0) == (c["sign_effect"] > 0)
        results.append({**c, "n": f["n_obs"], "beta": f["beta"], "se": f["se"],
                        "p_mixed": f["p"], "or": f["odds_ratio"],
                        "sd_agent": f["sd_agent"], "sd_item": f["sd_item"],
                        "ci95": f["ci95"], "converged": f["converged"],
                        "agrees_on_significance": bool(agrees),
                        "same_sign": bool(same_sign)})
        if verbose:
            r = results[-1]
            flag = "" if r["agrees_on_significance"] else "   <-- DISAGREES"
            print(f"{c['name']:44s} sign {c['sign_effect']:+.3f} p={c['sign_p']:.5f} | "
                  f"mixed b={r['beta']:+.3f} p={r['p_mixed']:.5f} "
                  f"sd_item={r['sd_item']:.2f}{flag}")
    return results


def main():
    print("Validating the estimator before any real fit...\n")
    ME.validate()
    print("\nRefitting every primary contrast:\n")
    res = run()
    dis = [r for r in res if "beta" in r and not r["agrees_on_significance"]]
    print(f"\ncontrasts refitted: {len([r for r in res if 'beta' in r])}")
    print(f"disagreements with the sign test at alpha=0.05: {len(dis)}")
    for d in dis:
        print(f"   {d['name']}: sign p={d['sign_p']:.5f}, mixed p={d['p_mixed']:.5f}")
    out = ROOT / "experiments/phase5_analysis/mixed_effects_refit.json"
    out.write_text(json.dumps(res, indent=2, default=str), encoding="utf-8")
    print(f"\nwritten: {out}")
    return res


if __name__ == "__main__":
    main()
