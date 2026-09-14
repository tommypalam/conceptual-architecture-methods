"""Offline within-arm reanalysis of the completed Phase 2 confirmation records.

Zero API calls. Reads only frozen artefacts:
  experiments/phase2_confirmation_20260913/analysis/responses.csv
  experiments/phase2_confirmation_20260913/population.json

Answers three questions the original Phase 2 analysis did not ask:
  1. How degenerate is the no-profile (U) baseline per cell?
  2. Does Procedural Dependence show a monotone dose-response on dissent?
  3. Is that effect specific to PD once all ten coordinates are controlled?

It also scores the thesis v0.6 section 6.1.1 directional hypotheses, which were
locked before Phase 2 collection but never evaluated against these responses.

Writes experiments/phase5_analysis/reanalysis_20260914/dispersion_results.json.
No frozen record, source or result is modified.
"""
from __future__ import annotations

import collections
import csv
import json
import math
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONF = ROOT / "experiments" / "phase2_confirmation_20260913"
OUT = ROOT / "experiments" / "phase5_analysis" / "reanalysis_20260914"
SEED = 20260914
N_PERM = 10_000

# Prospective directional hypotheses, thesis v0.6 section 6.1.1, simple problems only.
# Locked before Phase 2 execution; transcribed as (task, parameter, predicted label).
HYPOTHESES = [
    ("S1", "RE", "A"), ("S1", "TfA", "A"), ("S1", "PD", "A"),
    ("S2", "ID", "FORMAL_REPORT"), ("S2", "TfA", "LOCAL_CORRECTION"), ("S2", "MS", "FORMAL_REPORT"),
    ("S3", "RT", "ADOPT"), ("S3", "MoR", "ADOPT"), ("S3", "RE", "WAIT"),
]

TASKS = ["S1", "S2", "S3"]
CONFIGS = ["00100", "11011"]


def load():
    pop = json.loads((CONF / "population.json").read_text())
    profiles = {a["agent_id"]: a["parameters"] for a in pop["agents"]}
    with (CONF / "analysis" / "responses.csv").open() as fh:
        rows = [r for r in csv.DictReader(fh) if r["stage"] == "simple" and r["status"] == "ok"]
    return pop["parameter_order"], pop["content_hash"], profiles, rows


def point_biserial(values, binary):
    """Point-biserial correlation; None when the outcome has no variance."""
    n = len(values)
    m = sum(binary)
    if m == 0 or m == n:
        return None
    mu = sum(values) / n
    sd = math.sqrt(sum((v - mu) ** 2 for v in values) / n)
    if sd == 0:
        return None
    m1 = sum(v for v, b in zip(values, binary) if b) / m
    m0 = sum(v for v, b in zip(values, binary) if not b) / (n - m)
    return (m1 - m0) / sd * math.sqrt(m * (n - m) / (n * n))


def permutation_p(values, binary, observed, rng):
    """Two-sided permutation p on the label assignment, holding parameters fixed."""
    shuffled = list(binary)
    hits = 0
    for _ in range(N_PERM):
        rng.shuffle(shuffled)
        r = point_biserial(values, shuffled)
        if r is not None and abs(r) >= abs(observed):
            hits += 1
    return (hits + 1) / (N_PERM + 1)


def logistic(design, outcome, iters=3000, lr=0.25):
    """Unregularised batch-gradient logistic fit on standardised columns."""
    n, k = len(design), len(design[0])
    weights = [0.0] * k
    bias = 0.0
    for _ in range(iters):
        grad_w = [0.0] * k
        grad_b = 0.0
        for xi, yi in zip(design, outcome):
            z = bias + sum(weights[j] * xi[j] for j in range(k))
            resid = 1 / (1 + math.exp(-max(-30, min(30, z)))) - yi
            for j in range(k):
                grad_w[j] += resid * xi[j]
            grad_b += resid
        for j in range(k):
            weights[j] -= lr * grad_w[j] / n
        bias -= lr * grad_b / n
    return weights


def minority_option(u_counts, observed_votes):
    """The option the no-profile baseline (nearly) never chooses."""
    unseen = [o for o in set(observed_votes) | set(u_counts) if o not in u_counts]
    return unseen[0] if unseen else min(u_counts, key=lambda o: u_counts[o])


def main():
    order, pop_hash, profiles, rows = load()
    rng = random.Random(SEED)
    encoded = [r for r in rows if r["arm"] == "E"]
    unprofiled = [r for r in rows if r["arm"] == "U"]

    def param(row, code):
        return profiles[int(float(row["agent"]))][code]

    u_counts = {
        (t, c): collections.Counter(
            r["vote"] for r in unprofiled if r["problem"] == t and r["config"] == c
        )
        for t in TASKS for c in CONFIGS
    }

    results = {
        "seed": SEED,
        "n_permutations": N_PERM,
        "source_responses": str((CONF / "analysis" / "responses.csv").relative_to(ROOT)),
        "source_population_content_hash": pop_hash,
    }

    # 1. Baseline degeneracy: how much room does the U arm leave for an effect?
    degeneracy = {}
    for t in TASKS:
        for c in CONFIGS:
            counts = u_counts[(t, c)]
            total = sum(counts.values())
            modal = max(counts.values()) / total
            degeneracy[f"{t}_{c}"] = {
                "n": total,
                "modal_share": round(modal, 4),
                "unanimous": modal == 1.0,
                "distribution": dict(counts),
            }
    results["u_arm_degeneracy"] = degeneracy

    # 2 & 3. Per-cell dissent: PD dose-response, all-parameter correlations, multivariate ranking.
    cells = {}
    for t in TASKS:
        for c in CONFIGS:
            subset = [r for r in encoded if r["problem"] == t and r["config"] == c]
            target = minority_option(u_counts[(t, c)], [r["vote"] for r in subset])
            dissent = [1 if r["vote"] == target else 0 for r in subset]

            correlations = {}
            for code in order:
                r = point_biserial([param(x, code) for x in subset], dissent)
                correlations[code] = None if r is None else round(r, 4)

            entry = {
                "minority_option": target,
                "n": len(subset),
                "n_dissent": sum(dissent),
                "correlations": correlations,
            }

            pd_values = [param(x, "PD") for x in subset]
            pd_r = point_biserial(pd_values, dissent)
            if pd_r is not None:
                ordered = sorted(zip(pd_values, dissent))
                width = len(ordered) // 5
                entry["pd"] = {
                    "r": round(pd_r, 4),
                    "perm_p": permutation_p(pd_values, dissent, pd_r, rng),
                    "quintile_dissent_rates": [
                        round(sum(b for _, b in ordered[i * width:(i + 1) * width]) / width, 4)
                        for i in range(5)
                    ],
                }

                raw = [[param(x, code) for code in order] for x in subset]
                mu = [sum(col[j] for col in raw) / len(raw) for j in range(len(order))]
                sd = [
                    math.sqrt(sum((col[j] - mu[j]) ** 2 for col in raw) / len(raw)) or 1.0
                    for j in range(len(order))
                ]
                design = [[(col[j] - mu[j]) / sd[j] for j in range(len(order))] for col in raw]
                weights = logistic(design, dissent)
                ranking = sorted(range(len(order)), key=lambda j: -abs(weights[j]))
                entry["multivariate"] = {
                    "standardised_coefficients": {c2: round(w, 4) for c2, w in zip(order, weights)},
                    "pd_rank": ranking.index(order.index("PD")) + 1,
                    "rank_order": [order[j] for j in ranking],
                }
            cells[f"{t}_{c}"] = entry
    results["dissent_cells"] = cells

    # 4. Score the section 6.1.1 hypotheses that were locked before collection.
    scored = []
    for task, code, label in HYPOTHESES:
        subset = [r for r in encoded if r["problem"] == task]
        values = [param(x, code) for x in subset]
        hit = [1 if r["vote"] == label else 0 for r in subset]
        r = point_biserial(values, hit)
        if r is None:
            scored.append({
                "task": task, "parameter": code, "predicted": label, "verdict": "degenerate",
            })
            continue
        pval = permutation_p(values, hit, r, rng)
        if pval < 0.05:
            verdict = "supported" if r > 0 else "wrong_sign"
        else:
            verdict = "null"
        scored.append({
            "task": task, "parameter": code, "predicted": label,
            "r": round(r, 4), "perm_p": pval, "verdict": verdict,
        })
    tally = collections.Counter(h["verdict"] for h in scored)
    results["prospective_hypotheses"] = {
        "source": "thesis v0.6 section 6.1.1, simple problems",
        "note": "Directional signs were locked before Phase 2 collection; this is their first evaluation.",
        "scored": scored,
        "tally": dict(tally),
    }

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "dispersion_results.json").write_text(json.dumps(results, indent=2) + "\n")

    print(f"rows analysed: {len(rows)} (E={len(encoded)}, U={len(unprofiled)})")
    print(f"columns: {list(rows[0].keys())}")
    print("status=='ok' filter applied at load; no further rows dropped")
    print(f"cells: {len(cells)}; hypotheses scored: {len(scored)} -> {dict(tally)}")
    for name, cell in cells.items():
        block = cell.get("pd")
        if block:
            print(f"  {name}: PD r={block['r']:+.4f} p={block['perm_p']:.5f} "
                  f"rank={cell['multivariate']['pd_rank']}/10 "
                  f"quintiles={block['quintile_dissent_rates']}")
    print(f"written: {(OUT / 'dispersion_results.json').relative_to(ROOT)}")


if __name__ == "__main__":
    main()
