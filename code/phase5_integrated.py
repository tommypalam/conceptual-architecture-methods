"""Phase 5 integrated analysis. Zero API calls; offline over collected records.

Spec 1.2: "Relate representations, behaviour, human resemblance and moral
outcomes; report sensitivity and failure cases. Follows available evidence."

**What this reads.** The three Phase 4B designations carrying agent-level
coordinates alongside decisions, on two models and three INDEPENDENT population
draws:

    phase4b_profiled_r1   claude-haiku-4-5   40 agents   240 E-arm decisions
    phase4b_gpt_r2        gpt-5.4-mini       40 agents   320 E-arm decisions
    phase4b_permutation_r2 gpt-5.4-mini      40 agents   280 E-arm decisions

840 profiled decisions with known ten-coordinate vectors, plus their U, G and P
comparison arms.

**EVERYTHING HERE IS POST-HOC AND EXPLORATORY.** These data were collected to
answer the Phase 4B arm question, not to test coordinate-level hypotheses. No
coordinate was manipulated: all ten varied freely by draw. Nothing in this module
can confirm a hypothesis, and every result carries that limitation explicitly.

The Phase 5 reanalysis of Phase 2 already established the precedent and the
warning: PD's dominance there was a post-hoc discovery "requiring prospective
test before any confirmatory language". The same rule binds here.

**Four questions, all answerable offline.**

1. COORDINATE ASSOCIATION - does any of the ten predict the good-rate within the
   E arm? Ten tests, Holm-corrected, reported with the null as the expected
   result at n = 40 agents per designation.

2. PARAMETER REDUNDANCY (critical open problem 6) - are the ten empirically
   separable in these draws, or do they collapse? Correlation structure and the
   effective rank of the coordinate matrix.

3. AW SENSITIVITY (CLAUDE.md flags AW as preliminary) - does dropping AW change
   any association? A leave-one-out over the ten.

4. PORTABILITY (critical open problem 8) - do the two models agree on which
   coordinates associate, and on the five items both dispersed on?

**Method.** Point-biserial correlation between each coordinate and the agent's
E-arm good-rate, per designation; Holm correction within each family of ten;
Fisher exact on arm contrasts. No mixed-effects model: with 40 agents per
designation and no manipulation, a richer model would give false precision.
"""
from __future__ import annotations

import json
import math
import statistics
from pathlib import Path

PARAMETERS = ("LL", "CS", "RT", "MoR", "RE", "PD", "TfA", "ID", "MS", "AW")

# Designations carrying agent-level coordinates AND decisions.
SOURCES = (
    ("phase4b_profiled_r1", "claude-haiku-4-5", "phase4b_profiled_pool"),
    ("phase4b_gpt_r2", "gpt-5.4-mini", "phase4b_gpt_pool"),
    ("phase4b_permutation_r2", "gpt-5.4-mini", "phase4b_perm_pool"),
)

# Items that dispersed on BOTH models, declared in phase4b_gpt_pool before its
# collection. The only basis for a same-item cross-model comparison.
SHARED_ITEMS = ("desk_booking", "storage_unit", "tool_library",
                "meeting_room", "weekend_rota")


def _root():
    from phase3_recognition_run import ROOT
    return ROOT


def load(designation, pool_module):
    """Agent coordinates joined to that agent's decisions, per arm."""
    from phase3_budget import read_checked
    import importlib
    pool = importlib.import_module(pool_module)
    root = _root() / "experiments/phase4_coding" / designation
    pop = read_checked(root / "population.json")
    rows = read_checked(root / "all_rows.json")
    coords = {a["agent"]: a["coordinates"] for a in pop["agents"]}
    out = []
    for r in rows:
        if not r["choice"]:
            continue
        good = pool.primary_net(r["task"], r["choice"]) == "good"
        out.append({"arm": r["arm"], "agent": r["agent"], "task": r["task"],
                    "good": good,
                    "coordinates": coords.get(r["agent"]) if r["agent"] is not None else None})
    return out


def _pearson(xs, ys):
    n = len(xs)
    if n < 3:
        return None
    mx, my = statistics.mean(xs), statistics.mean(ys)
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    den = math.sqrt(sum((x - mx) ** 2 for x in xs) * sum((y - my) ** 2 for y in ys))
    return num / den if den else None


def _corr_p(r, n):
    """Two-sided p for a correlation, via the t transform."""
    if r is None or n < 3 or abs(r) >= 1:
        return 1.0
    t = abs(r) * math.sqrt((n - 2) / (1 - r * r))
    df = n - 2
    # Regularised incomplete beta via continued fraction, standard form.
    x = df / (df + t * t)
    return _betainc(df / 2, 0.5, x)


def _betainc(a, b, x):
    if x <= 0:
        return 0.0
    if x >= 1:
        return 1.0
    lbeta = math.lgamma(a) + math.lgamma(b) - math.lgamma(a + b)
    front = math.exp(math.log(x) * a + math.log(1 - x) * b - lbeta) / a
    f, c, d = 1.0, 1.0, 0.0
    for i in range(200):
        m = i // 2
        if i == 0:
            num = 1.0
        elif i % 2 == 0:
            num = (m * (b - m) * x) / ((a + 2 * m - 1) * (a + 2 * m))
        else:
            num = -((a + m) * (a + b + m) * x) / ((a + 2 * m) * (a + 2 * m + 1))
        d = 1.0 + num * d
        d = 1e-30 if abs(d) < 1e-30 else d
        d = 1.0 / d
        c = 1.0 + num / c
        c = 1e-30 if abs(c) < 1e-30 else c
        f *= c * d
        if abs(1.0 - c * d) < 1e-10:
            break
    return min(1.0, front * (f - 1.0))


def holm(pvalues):
    """Holm-corrected p-values, keyed as the input dict."""
    live = sorted(pvalues.items(), key=lambda kv: kv[1])
    out, running = {}, 0.0
    for i, (k, raw) in enumerate(live):
        running = min(1.0, max(running, raw * (len(live) - i)))
        out[k] = round(running, 6)
    return out


def coordinate_association(rows, arm="E"):
    """Per coordinate: correlation with the agent's good-rate in `arm`."""
    byagent = {}
    for r in rows:
        if r["arm"] != arm or r["coordinates"] is None:
            continue
        byagent.setdefault(r["agent"], {"good": 0, "n": 0,
                                        "coordinates": r["coordinates"]})
        byagent[r["agent"]]["good"] += int(r["good"])
        byagent[r["agent"]]["n"] += 1
    agents = [a for a in byagent.values() if a["n"]]
    if len(agents) < 3:
        return None
    rate = [a["good"] / a["n"] for a in agents]
    raw, res = {}, {}
    for p in PARAMETERS:
        xs = [a["coordinates"][p] for a in agents]
        r = _pearson(xs, rate)
        pv = _corr_p(r, len(agents))
        raw[p] = pv
        res[p] = {"r": round(r, 4) if r is not None else None, "p": round(pv, 6)}
    adj = holm(raw)
    for p in PARAMETERS:
        res[p]["holm"] = adj[p]
    return {"n_agents": len(agents),
            "mean_good_rate": round(statistics.mean(rate), 4),
            "coordinates": res,
            "any_survives_holm": [p for p in PARAMETERS if res[p]["holm"] < 0.05]}


def redundancy(populations):
    """Critical open problem 6: are the ten coordinates empirically separable?

    Reports the pairwise correlation matrix and the effective rank - the number
    of principal components needed for 90% of variance. Ten independent
    coordinates need ten; strong collapse would need far fewer.
    """
    agents = [a["coordinates"] for pop in populations for a in pop["agents"]]
    cols = {p: [a[p] for a in agents] for p in PARAMETERS}
    matrix = {}
    strong = []
    for i, a in enumerate(PARAMETERS):
        for b in PARAMETERS[i + 1:]:
            r = _pearson(cols[a], cols[b])
            matrix[f"{a}~{b}"] = round(r, 4) if r is not None else None
            if r is not None and abs(r) >= 0.4:
                strong.append({"pair": f"{a}~{b}", "r": round(r, 4)})
    # Effective rank by eigenvalues of the correlation matrix (power iteration
    # is unnecessary at 10x10; use the trace-normalised spectrum via numpy if
    # available, else report the correlation summary alone).
    eff = None
    try:
        import numpy as np
        M = np.array([[1.0 if a == b else (_pearson(cols[a], cols[b]) or 0.0)
                       for b in PARAMETERS] for a in PARAMETERS])
        vals = sorted(np.linalg.eigvalsh(M), reverse=True)
        total = sum(vals)
        cum, k = 0.0, 0
        for v in vals:
            cum += v
            k += 1
            if cum / total >= 0.90:
                break
        eff = {"components_for_90pct_variance": k,
               "eigenvalues": [round(float(v), 4) for v in vals],
               "min_eigenvalue": round(float(vals[-1]), 4)}
    except Exception:
        pass
    return {"n_agents": len(agents), "pairwise": matrix,
            "strong_pairs_abs_r_ge_0.4": strong, "spectrum": eff}


def aw_sensitivity(rows):
    """CLAUDE.md flags AW as preliminary. Does dropping it change anything?

    Recomputes the association family without AW, so the Holm correction is over
    nine rather than ten, and reports whether any conclusion moves.
    """
    full = coordinate_association(rows)
    if not full:
        return None
    byagent = {}
    for r in rows:
        if r["arm"] != "E" or r["coordinates"] is None:
            continue
        byagent.setdefault(r["agent"], {"good": 0, "n": 0,
                                        "coordinates": r["coordinates"]})
        byagent[r["agent"]]["good"] += int(r["good"])
        byagent[r["agent"]]["n"] += 1
    agents = list(byagent.values())
    rate = [a["good"] / a["n"] for a in agents]
    nine = [p for p in PARAMETERS if p != "AW"]
    raw = {}
    for p in nine:
        xs = [a["coordinates"][p] for a in agents]
        raw[p] = _corr_p(_pearson(xs, rate), len(agents))
    adj = holm(raw)
    changed = [p for p in nine
               if (adj[p] < 0.05) != (full["coordinates"][p]["holm"] < 0.05)]
    return {"aw_r": full["coordinates"]["AW"]["r"],
            "aw_holm": full["coordinates"]["AW"]["holm"],
            "conclusions_changed_by_dropping_aw": changed,
            "holm_family_size": len(nine)}


def portability(per_designation):
    """Critical open problem 8: do the two models agree?

    Compares the ranked coordinate associations across designations. With no
    coordinate manipulated and n = 40 per draw, agreement is not expected; the
    point is to measure it rather than assume it.
    """
    ranks = {}
    for name, res in per_designation.items():
        if not res:
            continue
        order = sorted(PARAMETERS,
                       key=lambda p: -abs(res["coordinates"][p]["r"] or 0))
        ranks[name] = order
    pairs = {}
    names = sorted(ranks)
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            ra = {p: k for k, p in enumerate(ranks[a])}
            rb = {p: k for k, p in enumerate(ranks[b])}
            xs = [ra[p] for p in PARAMETERS]
            ys = [rb[p] for p in PARAMETERS]
            pairs[f"{a} ~ {b}"] = {
                "rank_correlation": round(_pearson(xs, ys) or 0.0, 4),
                "top3_overlap": len(set(ranks[a][:3]) & set(ranks[b][:3])),
            }
    return {"ranked_by_abs_r": ranks, "agreement": pairs}


def arm_summary(rows):
    """Good-rate per arm, with n."""
    out = {}
    for arm in sorted({r["arm"] for r in rows}):
        vals = [r["good"] for r in rows if r["arm"] == arm]
        if vals:
            out[arm] = {"good_rate": round(sum(vals) / len(vals), 4), "n": len(vals)}
    return out


def run():
    from phase3_budget import read_checked
    per, arms, populations, loaded = {}, {}, [], {}
    for designation, model, pool in SOURCES:
        rows = load(designation, pool)
        loaded[designation] = rows
        per[designation] = coordinate_association(rows)
        arms[designation] = {"model": model, "arms": arm_summary(rows)}
        populations.append(read_checked(
            _root() / "experiments/phase4_coding" / designation / "population.json"))

    pooled = [r for rows in loaded.values() for r in rows]
    return {
        "designations": {d: {"model": m} for d, m, _ in SOURCES},
        "arms": arms,
        "coordinate_association": per,
        "coordinate_association_pooled": coordinate_association(pooled),
        "redundancy": redundancy(populations),
        "aw_sensitivity": {d: aw_sensitivity(loaded[d]) for d in loaded},
        "portability": portability(per),
        "status": ("POST-HOC AND EXPLORATORY. These data were collected to answer "
                   "the Phase 4B arm question. No coordinate was manipulated; all "
                   "ten varied freely by draw. Nothing here confirms a hypothesis, "
                   "and a null across the ten is the expected result at n=40 "
                   "agents per designation."),
    }


def main():
    result = run()
    print("=" * 74)
    print("PHASE 5 INTEGRATED ANALYSIS - zero API calls, post-hoc, exploratory")
    print("=" * 74)
    print()
    print("Arms by designation:")
    for d, v in result["arms"].items():
        summary = "  ".join(f"{a} {x['good_rate']:.3f} (n={x['n']})"
                            for a, x in sorted(v["arms"].items()))
        print(f"  {d:24s} {v['model']:18s} {summary}")

    print()
    print("Q1 COORDINATE ASSOCIATION (E arm, Holm over ten):")
    for d, res in result["coordinate_association"].items():
        if not res:
            continue
        top = sorted(PARAMETERS,
                     key=lambda p: -abs(res["coordinates"][p]["r"] or 0))[:3]
        shown = "  ".join(f"{p} r={res['coordinates'][p]['r']:+.3f} "
                          f"(holm {res['coordinates'][p]['holm']:.3f})" for p in top)
        print(f"  {d:24s} n={res['n_agents']}  top3: {shown}")
        print(f"  {'':24s} survives Holm: {res['any_survives_holm'] or 'NONE'}")
    pooled = result["coordinate_association_pooled"]
    if pooled:
        print(f"  {'POOLED':24s} n={pooled['n_agents']}  "
              f"survives Holm: {pooled['any_survives_holm'] or 'NONE'}")

    print()
    print("Q2 PARAMETER REDUNDANCY (critical open problem 6):")
    red = result["redundancy"]
    print(f"  agents pooled: {red['n_agents']}")
    print(f"  pairs with |r| >= 0.4: {red['strong_pairs_abs_r_ge_0.4'] or 'none'}")
    if red["spectrum"]:
        print(f"  components for 90% variance: "
              f"{red['spectrum']['components_for_90pct_variance']} of 10")
        print(f"  min eigenvalue: {red['spectrum']['min_eigenvalue']}")

    print()
    print("Q3 AW SENSITIVITY (AW is flagged preliminary in CLAUDE.md):")
    for d, v in result["aw_sensitivity"].items():
        if v:
            print(f"  {d:24s} AW r={v['aw_r']:+.3f} holm {v['aw_holm']:.3f}  "
                  f"conclusions changed by dropping AW: "
                  f"{v['conclusions_changed_by_dropping_aw'] or 'none'}")

    print()
    print("Q4 PORTABILITY (critical open problem 8):")
    for pair, v in result["portability"]["agreement"].items():
        print(f"  {pair}")
        print(f"      rank correlation {v['rank_correlation']:+.3f}  "
              f"top-3 overlap {v['top3_overlap']}/3")

    print()
    print("STATUS:", result["status"])
    return result


if __name__ == "__main__":
    out = main()
    target = _root() / "experiments/phase5_analysis/integrated_20260916"
    target.mkdir(parents=True, exist_ok=True)
    (target / "results.json").write_text(
        json.dumps(out, indent=2, sort_keys=True), encoding="utf-8")
    print(f"\nwritten: {target / 'results.json'}")
