"""Exact planning power for a paired binary test; reads no pilot outcomes."""
import json
from pathlib import Path

import numpy as np
from scipy.stats import binom


def power(n, p10, p01, alpha):
    q = p10 + p01
    if not (0 <= p10 <= 1 and 0 <= p01 <= 1 and 0 < q <= 1):
        raise ValueError("Invalid discordance probabilities")
    result = 0.0
    for d in range(1, n + 1):
        k = np.arange(d + 1)
        pvalues = np.minimum(1.0, 2 * binom.cdf(np.minimum(k, d - k), d, .5))
        reject = pvalues <= alpha
        result += binom.pmf(d, n, q) * binom.pmf(k[reject], d, p10 / q).sum()
    return float(result)


if __name__ == "__main__":
    rows = []
    for n in [200, 400]:
        for difference, disagreement in [(.1, .1), (.1, .3), (.15, .3), (.2, .4)]:
            rows.append({"N": n, "risk_difference": difference, "pair_disagreement": disagreement,
                         "power": power(n, (disagreement + difference) / 2, (disagreement - difference) / 2, .05 / 6)})
    result = {"method": "Exact conditioning on binomial discordance count; two-sided exact paired binomial test",
              "alpha": .05 / 6, "family_size": 6, "pilot_outcomes_read": False,
              "note": "Bonferroni threshold supplies a conservative planning threshold for Holm; scenarios are assumptions, not estimated guarantees.",
              "scenarios": rows}
    path = Path(__file__).resolve().parents[1] / "experiments/phase2_exploratory_20260912/analysis/confirmation_power_scenarios.json"
    path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(result))
