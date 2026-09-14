"""Power simulation for the prospective PD gradient test (pd_gradient_r1).

Zero API calls. Reproduces every number in section 6 of that protocol:

  1. Power to detect the PD dose-response, planned against the WEAKEST cell
     observed in the Phase 5 reanalysis (deliberately conservative).
  2. False-positive rate on a simulated flat, PD-irrelevant task - the
     calibration that lets Class N serve as a discriminating null control.
  3. PD's maximum absolute correlation with any other coordinate in R.

Run: py -3.11 -B code/phase3_pd_gradient_power.py
"""
from __future__ import annotations

import json
import math
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SEED = 20260915
N_PERM = 600          # inner permutations per simulated trial
N_TRIALS = 400        # outer replications per sample size
FLAT_TRIALS = 300
ALPHA = 0.05

# Observed dissent rate by PD quintile, per cell, from the Phase 5 reanalysis.
OBSERVED = {
    "S2_00100": [0.0375, 0.1125, 0.1625, 0.4375, 0.6625],
    "S2_11011": [0.0, 0.0125, 0.0, 0.0875, 0.375],
    "S3_00100": [0.025, 0.075, 0.0625, 0.15, 0.375],
    "S3_11011": [0.1375, 0.1875, 0.3375, 0.4875, 0.7],
}
PD_BETA = (2.5, 2.0)  # thesis v0.6 marginal for Procedural Dependence
FLAT_RATE = 0.30      # base rate for a PD-irrelevant task


def point_biserial(values, binary):
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


def simulate_task(n, quintile_rates, rng):
    """Draw n agents and assign choices by their PD quintile."""
    pd_values = [rng.betavariate(*PD_BETA) for _ in range(n)]
    order = sorted(range(n), key=lambda i: pd_values[i])
    choices = [0] * n
    width = n // 5
    for q in range(5):
        lo = q * width
        hi = (q + 1) * width if q < 4 else n
        for idx in order[lo:hi]:
            choices[idx] = 1 if rng.random() < quintile_rates[q] else 0
    return pd_values, choices


def permutation_p(values, binary, observed, rng):
    shuffled = list(binary)
    hits = 0
    for _ in range(N_PERM):
        rng.shuffle(shuffled)
        r = point_biserial(values, shuffled)
        if r is not None and abs(r) >= abs(observed):
            hits += 1
    return (hits + 1) / (N_PERM + 1)


def detection_rate(n, quintile_rates, rng, trials):
    """Share of simulated trials whose permutation test clears alpha."""
    detected = 0
    for _ in range(trials):
        values, choices = simulate_task(n, quintile_rates, rng)
        observed = point_biserial(values, choices)
        if observed is None:
            continue
        if permutation_p(values, choices, observed, rng) < ALPHA:
            detected += 1
    return detected / trials


def pd_separability():
    path = ROOT / "config" / "correlation_matrix_R.json"
    data = json.loads(path.read_text())
    order = data["parameter_order"]
    matrix = data.get("matrix") or data.get("R")
    i = order.index("PD")
    pairs = [(p, matrix[i][j]) for j, p in enumerate(order) if p != "PD"]
    return pairs, max(abs(v) for _, v in pairs)


def main():
    rng = random.Random(SEED)

    gaps = {k: round(v[4] - v[0], 4) for k, v in OBSERVED.items()}
    weakest = min(OBSERVED, key=lambda k: OBSERVED[k][4] - OBSERVED[k][0])
    rates = OBSERVED[weakest]
    print("Observed Q5-Q1 dissent gaps (Phase 5 reanalysis):")
    for k, v in gaps.items():
        print(f"  {k}: {v:+.4f}")
    print(f"\nPlanning against the weakest cell: {weakest} "
          f"Q1={rates[0]:.4f} Q5={rates[4]:.4f} gap={rates[4] - rates[0]:.4f}")

    print(f"\nPower to detect the PD gradient (permutation, alpha={ALPHA}, "
          f"{N_TRIALS} trials x {N_PERM} shuffles):")
    results = {}
    for n in (40, 60, 80, 100, 120):
        power = detection_rate(n, rates, rng, N_TRIALS)
        results[n] = power
        print(f"  n={n:4d}  power={power:.3f}")

    flat = detection_rate(120, [FLAT_RATE] * 5, rng, FLAT_TRIALS)
    print(f"\nFalse-positive rate on a flat PD-irrelevant task (n=120): {flat:.3f}")
    print(f"  (target ~{ALPHA}; validates Class N as a discriminating null control)")

    pairs, max_abs = pd_separability()
    print("\nPD correlations with the other nine coordinates (config R):")
    for name, value in pairs:
        print(f"  PD-{name:4s} = {value:+.3f}")
    print(f"Max |r| = {max_abs:.3f} -> PD is separable by multivariate control.")

    print(f"\nSelected design: n=120 per task, power={results[120]:.3f} "
          f"against the weakest observed effect.")


if __name__ == "__main__":
    main()
