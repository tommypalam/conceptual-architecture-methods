"""Prospective ten-contrast analysis; consumes scored profile outcomes, no API.

Inputs are bounded participant outcomes (including Asch fractions), not raw
trials. Missingness blocks complete-data inference rather than silently filtering.
"""
import math
import numpy as np
from scipy.stats import permutation_test

from phase3_canonical_stimuli import BENCHMARKS

FAMILY = tuple(f"{name}/{variant}" for name in BENCHMARKS for variant in ("canonical", "decanonised"))


def paired_estimate(high, low, *, seed, resamples=9999):
    if not high or set(high) != set(low) or any(type(key) is not str for key in high):
        raise ValueError("Exact nonempty string profile IDs must match")
    if type(seed) is not int or type(resamples) is not int or resamples < 99:
        raise ValueError("Explicit integer seed and at least 99 resamples required")
    for value in list(high.values()) + list(low.values()):
        if value is not None and (type(value) not in (float, int) or not math.isfinite(value) or not 0 <= value <= 1):
            raise ValueError("Need bounded [0,1] profile outcomes or explicit missing")
    keys = sorted(high)
    n = len(keys)
    complete = [key for key in keys if high[key] is not None and low[key] is not None]
    lower = sum((high[key] if high[key] is not None else 0) -
                (low[key] if low[key] is not None else 1) for key in keys) / n
    upper = sum((high[key] if high[key] is not None else 1) -
                (low[key] if low[key] is not None else 0) for key in keys) / n
    result = {"assigned_pairs": n, "complete_pairs": len(complete),
              "missing_pairs": n - len(complete), "identification_interval": [lower, upper],
              "estimate": None, "complete_pair_supplement": None,
              "bootstrap_95_interval": None, "bootstrap_degenerate": None,
              "hoeffding_95_interval": None, "p_two_sided": None,
              "analysis_seed": seed, "resamples": resamples,
              "status": "incomplete_assigned_data"}
    if complete:
        result["complete_pair_supplement"] = sum(high[k] - low[k] for k in complete) / len(complete)
    if len(complete) != n:
        return result
    differences = np.asarray([high[key] - low[key] for key in keys], dtype=float)
    estimate = float(differences.mean())
    result.update(estimate=estimate, status="complete", bootstrap_degenerate=bool(np.ptp(differences) == 0))
    # Every independent paired outcome lies in [-1,1]. This conservative bound
    # remains nonzero-width under empirical saturation, unlike a naive bootstrap.
    radius = math.sqrt(2 * math.log(40) / n)
    result["hoeffding_95_interval"] = [max(-1, estimate-radius), min(1, estimate+radius)]
    rng = np.random.default_rng(seed)
    means = []
    for start in range(0, resamples, 256):
        size = min(256, resamples - start)
        means.extend(differences[rng.integers(0, n, size=(size, n))].mean(axis=1))
    result["bootstrap_95_interval"] = np.quantile(means, [.025, .975]).tolist()
    if n == 1:
        result["p_two_sided"] = 1.0  # both sign assignments tie in magnitude
        return result
    # One-sample paired 'samples' permutations independently flip each pair's sign.
    test = permutation_test((differences,), np.mean, permutation_type="samples",
                            vectorized=True, n_resamples=resamples, batch=256,
                            alternative="two-sided", random_state=np.random.default_rng(seed + 1))
    result["p_two_sided"] = float(test.pvalue)
    return result


def holm(pvalues):
    if set(pvalues) != set(FAMILY):
        raise ValueError("Freeze all ten primary contrasts, not a favourable subset")
    if any(value is not None and (type(value) not in (float, int) or not math.isfinite(value) or not 0 <= value <= 1)
           for value in pvalues.values()):
        raise ValueError("Invalid p-value")
    # Missing endpoints remain in the family as p=1 for multiplicity only. They
    # remain untested (None) in output and can never count as passed.
    ordered = sorted(FAMILY, key=lambda key: (1 if pvalues[key] is None else pvalues[key], key))
    adjusted, previous = {}, 0
    for rank, key in enumerate(ordered):
        value = 1 if pvalues[key] is None else pvalues[key]
        previous = min(1, max(previous, (len(FAMILY)-rank) * value))
        adjusted[key] = None if pvalues[key] is None else previous
    return {key: adjusted[key] for key in FAMILY}


def primary_family(cells, *, seed=2026091307, resamples=9999, exploratory=False):
    if set(cells) != set(FAMILY) or type(exploratory) is not bool:
        raise ValueError("Require the ten predeclared cells and explicit study status")
    profile_ids = set(cells[FAMILY[0]]["high"])
    if any(set(cell[arm]) != profile_ids for cell in cells.values() for arm in ("high", "low")):
        raise ValueError("All primary cells must retain the same assigned profile IDs")
    if not exploratory and len(profile_ids) != 200:
        raise ValueError("The specified confirmation requires 200 matched profiles")
    results = {key: paired_estimate(cells[key]["high"], cells[key]["low"],
                                    seed=seed + 100*index, resamples=resamples)
               for index, key in enumerate(FAMILY)}
    adjusted = holm({key: result["p_two_sided"] for key, result in results.items()})
    for key, result in results.items():
        result["holm_p"] = adjusted[key]
        result["positive_context_evidence"] = (not exploratory and adjusted[key] is not None
                                                and adjusted[key] < .05 and result["estimate"] > 0)
    return {"stage": "exploratory" if exploratory else "confirmatory",
            "primary_family_size": 10, "results": results,
            "phase3_pass": None, "human_rate_match": None,
            "note": "Context-effect inference only; no human-rate, minimum-effect or moral-validation decision."}
