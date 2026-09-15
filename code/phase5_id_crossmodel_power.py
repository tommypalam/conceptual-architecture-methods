"""Power for id_crossmodel_r1, simulated against haiku's MEASURED baselines.

Zero API calls. Run this to reproduce the figures in the protocol.

**Why this module exists separately.** The power numbers in
`phase5_id_crossmodel.MEASURED_POWER` are load-bearing: they are what makes a
null from that designation interpretable, and what ruled out the four-arm swap
design. A number that only ever existed in a scratch session is not reproducible
evidence, so the simulation lives in source and can be re-run.

**The error this avoids.** `phase4b_sonnet_r1`'s power check applied a UNIFORM
effect to a single assumed baseline and reported 8/8. Against sonnet's real
per-item baselines the true figure was <=5/10, because items sitting near a bound
cannot move. That designation was abandoned on the corrected analysis rather than
run underpowered. This simulation draws from the measured per-item good-rates of
`phase4b_profiled_r1`'s E arm on haiku, so bounded items are bounded here too.

**What it shows.** At ID's measured gpt effect of +0.111, the two-arm endpoint
design reaches 16/20 and the four-arm swap design only 14/20, because the swap's
Holm family is four times larger. Hence endpoints.
"""
from __future__ import annotations

import math
import pathlib
import random

from phase3_budget import read_checked
from phase3_recognition_run import ROOT

import phase4b_profiled_pool as P

SOURCE = ROOT / "experiments/phase4_coding/phase4b_profiled_r1/all_rows.json"

# ID's measured effect on gpt, the size that matters most here.
ID_GPT_EFFECT = 0.111

SEEDS = 20
AGENTS = 40
SEED0 = 7000


def baselines(arm="E"):
    """Measured per-item good-rates on haiku. Not assumed, read from the record."""
    rows = read_checked(SOURCE)
    out = {}
    for t in P.TASK_IDS:
        vals = [P.primary_net(r["task"], r["choice"]) == "good"
                for r in rows
                if r.get("arm") == arm and r.get("task") == t and r.get("choice")]
        if vals:
            out[t] = sum(vals) / len(vals)
    return out


def sign_p(hi, lo):
    n = hi + lo
    if n == 0:
        return 1.0
    k = min(hi, lo)
    return min(1.0, 2 * sum(math.comb(n, i) for i in range(k + 1)) / (2 ** n))


def simulate(base, effect, agents=AGENTS, seeds=SEEDS, family=1, alpha=0.05):
    """Paired sign test over the six items, `family` = Holm family size."""
    hits = 0
    for s in range(seeds):
        rng = random.Random(SEED0 + s)
        hi_only = lo_only = 0
        for p in base.values():
            plo = max(0.02, min(0.98, p - effect / 2))
            phi = max(0.02, min(0.98, p + effect / 2))
            for _ in range(agents):
                a = rng.random() < plo
                b = rng.random() < phi
                if b and not a:
                    hi_only += 1
                elif a and not b:
                    lo_only += 1
        if min(1.0, sign_p(hi_only, lo_only) * family) < alpha:
            hits += 1
    return hits


def main():
    base = baselines()
    print("haiku E-arm baselines, measured in phase4b_profiled_r1:")
    for t, v in sorted(base.items()):
        head = min(v, 1 - v)
        mark = "   <-- near a bound" if head < 0.12 else ""
        print(f"   {t:16s} {v:.3f}  headroom {head:.3f}{mark}")

    grid = (0.0, 0.080, ID_GPT_EFFECT, 0.143, 0.200)
    print(f"\ntwo-arm endpoint design (Holm family 1), {AGENTS} agents, "
          f"{SEEDS} seeds:")
    for e in grid:
        h = simulate(base, e, family=1)
        tag = ("   <-- ID's gpt effect" if e == ID_GPT_EFFECT else
               "   <-- FALSE POSITIVE RATE" if e == 0 else "")
        print(f"   true effect {e:+.3f}: {h}/{SEEDS}{tag}")

    print(f"\nfour-arm swap design (Holm family 4), {AGENTS} agents — REJECTED:")
    for e in grid:
        h = simulate(base, e, family=4)
        tag = "   <-- ID's gpt effect" if e == ID_GPT_EFFECT else ""
        print(f"   true effect {e:+.3f}: {h}/{SEEDS}{tag}")

    endpoint = simulate(base, ID_GPT_EFFECT, family=1)
    swap = simulate(base, ID_GPT_EFFECT, family=4)
    print(f"\nAt ID's gpt effect: endpoints {endpoint}/{SEEDS}, "
          f"swap {swap}/{SEEDS}.")
    print("The swap design is weaker because its Holm family is 4x larger, and a")
    print("failed TRUE arm makes its SWAP arms uninterpretable - the LL outcome.")
    print(f"\n{endpoint}/{SEEDS} is {100*endpoint//SEEDS}%. A null from this")
    print("designation is a WEAK null and is reported with that number.")


if __name__ == "__main__":
    main()
