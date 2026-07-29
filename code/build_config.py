"""
build_config.py — Materialise the config/ JSON layer from the canonical
constants in utils.py + the thesis v0.6 configuration-selection rule (§4.3).

This is a ONE-SHOT scaffolding generator, not part of the forward pipeline.
It reads the human-owned constants (R, Beta marginals) from utils.py so the
JSON files never drift from code, and it computes a DRAFT 8-12 configuration
subset for human sign-off (CLAUDE.md: config subset requires approval).

Run:  python code/build_config.py
Writes config/parameters.json, correlation_matrix_R.json, population_means.json,
seeds.json, and configurations.json (marked DRAFT).

Nothing here calls an API. Idempotent: overwrites the generated JSONs in place.
"""

from __future__ import annotations

import itertools
import json
from pathlib import Path

import numpy as np

import utils

REPO_ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = REPO_ROOT / "config"

# Per-parameter metadata (endpoints + proxy), thesis v0.6 Table 1 / §3.1.
# LL convention is 0=external, 1=internal (v0.6 fix).
PARAM_META = {
    "LL":  ("Legitimacy Locus", "external warrant (institutional, role-based, socially recognised)",
            "internal endorsement (self-authored, autonomy-driven)", "GCOS (Deci & Ryan 1985)"),
    "CS":  ("Constraint Sensitivity", "low (influence registered as environmental feature)",
            "high (even soft pressure registers as restriction)", "HPRS (Hong & Faedda 1996)"),
    "RT":  ("Response Threshold", "high tolerance (only major violations activate response)",
            "hair-trigger (minor deviations activate response)", "UG rejection thresholds (Wallace et al. 2007)"),
    "MoR": ("Mode of Response", "internal/reflective (self adjusts)",
            "external/behavioural (world is acted on)", "STAXI / Thomas-Kilmann / Davis IRI"),
    "RE":  ("Relational Embedding", "atomised (abstract-person model)",
            "role-sensitive/socially embedded", "Singelis SCS (1994)"),
    "PD":  ("Procedural Dependence", "outcome-dominant (results matter, methods secondary)",
            "process-dominant (fair procedure matters independently)", "Colquitt (2001)"),
    "TfA": ("Tolerance for Asymmetry", "egalitarian (asymmetry inherently suspect)",
            "hierarchical (asymmetry accepted if justified)", "SDO7 (Pratto 1994; Ho 2015)"),
    "ID":  ("Internalisation Dependence", "surface compliance suffices",
            "genuine endorsement required", "SRQ (Ryan & Connell 1989)"),
    "MS":  ("Moral Scope", "local/role-bound/partial",
            "universalised/generalisable", "MES (Crimston et al. 2016)"),
    "AW":  ("Affective Weighting", "cognitive/deliberative",
            "affective/intuitive", "Davis IRI EC/PT ratio (1983) — PRELIMINARY"),
}

CONFIG_AXES = utils.CONFIG_AXES  # [Freedom, Justice, Authority, Care, Loyalty]


def build_parameters() -> dict:
    params = {}
    for name in utils.PARAM_NAMES:
        alpha, beta = utils.BETA_PARAMS[name]
        label, e0, e1, proxy = PARAM_META[name]
        params[name] = {
            "label": label,
            "beta_alpha": alpha,
            "beta_beta": beta,
            "beta_mean": round(alpha / (alpha + beta), 3),
            "endpoint_0": e0,
            "endpoint_1": e1,
            "proxy_instrument": proxy,
        }
    return {
        "schema_version": "1.0",
        "source": "thesis v0.6 Table 1 / §3.1; generated from code/utils.py",
        "axis_convention_note": "LL runs 0=external, 1=internal (thesis v0.6 §3.1).",
        "parameter_order": list(utils.PARAM_NAMES),
        "parameters": params,
    }


def build_correlation() -> dict:
    return {
        "schema_version": "1.0",
        "source": "thesis v0.6 Appendix D, Table D.1; generated from code/utils.py",
        "parameter_order": list(utils.PARAM_NAMES),
        "psd_verified": True,
        "min_eigenvalue": round(float(utils._MIN_EIG), 4),
        "matrix": utils.R.tolist(),
    }


def build_population_means() -> dict:
    return {
        "schema_version": "1.0",
        "source": "Beta means from code/utils.py (alpha / (alpha + beta))",
        "note": "Used by Phase 0b null condition B and Phase 1.5 sweeps/rotations.",
        "means": utils.POPULATION_MEANS,
    }


def build_seeds() -> dict:
    # Deterministic phase-name -> root seed map (spec §1.4). Values are fixed,
    # documented, and never regenerated from a clock.
    return {
        "schema_version": "1.0",
        "source": "spec v0.1 §1.4 — deterministic phase-name -> integer-seed map",
        "note": "Stochastic operations within a phase consume a derived sequence "
                "from the phase root seed. Do not change a seed once a phase has run.",
        "seeds": {
            "phase0b_harness_neutral": 20260601,
            "phase0c_locked_holdout": 20260602,
            "phase1_pilot": 20260603,
            "phase1_5_encoding_validity": 20260604,
            "phase2_simple": 20260605,
            "phase2_complex": 20260606,
            "phase3_benchmarks": 20260607,
        },
    }


def select_configuration_subset(k: int = 10) -> list[str]:
    """
    Thesis v0.6 §4.3 selection rule, applied deterministically:
      1. Anchor inclusion: 00100 (Milgram-analogue) and 11011 (its inverse).
      2. Per-axis coverage: >= 3 configs at each level (0 and 1) of each of the
         five axes.
      3. Max-entropy Hamming spread: greedily add the configuration that
         maximises the minimum Hamming distance to the already-selected set
         (farthest-point sampling), breaking ties by larger mean distance then
         lexicographic order for determinism.
    Returns k configuration codes.
    """
    anchors = [utils.MILGRAM_ANALOGUE, utils.MILGRAM_INVERSE]  # "00100", "11011"
    selected = list(anchors)
    pool = [c for c in utils.ALL_CONFIGS if c not in selected]

    def hamming(a: str, b: str) -> int:
        return sum(x != y for x, y in zip(a, b))

    def coverage_ok(subset: list[str]) -> bool:
        arr = np.array([[int(ch) for ch in c] for c in subset])
        for axis in range(5):
            col = arr[:, axis]
            if (col == 0).sum() < 3 or (col == 1).sum() < 3:
                return False
        return True

    # Greedy farthest-point selection until we reach k.
    while len(selected) < k:
        best = None
        best_key = None
        for cand in pool:
            dists = [hamming(cand, s) for s in selected]
            key = (min(dists), sum(dists) / len(dists), [-ord(ch) for ch in cand])
            if best_key is None or key > best_key:
                best_key, best = key, cand
        selected.append(best)
        pool.remove(best)

    # If per-axis coverage not yet satisfied, swap in configs that fix the gap.
    # (With k=10 farthest-point over the full cube this is normally already met;
    # the check makes the guarantee explicit and auditable.)
    if not coverage_ok(selected):
        for cand in list(pool):
            trial = selected + [cand]
            if coverage_ok(trial):
                selected = trial
                pool.remove(cand)
                break

    return selected


def build_configurations() -> dict:
    subset = select_configuration_subset(k=10)
    arr = np.array([[int(ch) for ch in c] for c in subset])
    coverage = {
        axis: {"level_0": int((arr[:, i] == 0).sum()),
               "level_1": int((arr[:, i] == 1).sum())}
        for i, axis in enumerate(CONFIG_AXES)
    }
    entries = []
    for code in subset:
        axes = utils.config_to_axes(code)
        role = None
        if code == utils.MILGRAM_ANALOGUE:
            role = "anchor: Milgram-analogue (authority-high)"
        elif code == utils.MILGRAM_INVERSE:
            role = "anchor: full inverse of Milgram-analogue"
        entries.append({
            "code": code,
            "axes": axes,
            "role": role,
        })
    return {
        "schema_version": "1.0",
        "status": "DRAFT — REQUIRES HUMAN SIGN-OFF (CLAUDE.md: config subset is human-approval)",
        "source": "thesis v0.6 §4.3 selection rule, computed by code/build_config.py",
        "selection_rule": [
            "1. Anchor inclusion: 00100 and 11011.",
            "2. Per-axis coverage: >= 3 configs at each level of each axis.",
            "3. Max-entropy Hamming spread (farthest-point) on remaining slots.",
        ],
        "axis_order": CONFIG_AXES,
        "n_configs": len(subset),
        "per_axis_coverage": coverage,
        "coverage_satisfied": all(
            v["level_0"] >= 3 and v["level_1"] >= 3 for v in coverage.values()
        ),
        "configurations": entries,
        "config_description_note": "Each configuration needs a two-sentence practical "
        "description for the system prompt (thesis §4.3 / §6.4.1). Those are drafted "
        "at sign-off, not auto-generated here.",
    }


def write_json(name: str, payload: dict) -> None:
    path = CONFIG_DIR / name
    with path.open("w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    print(f"wrote {path.relative_to(REPO_ROOT)}")


def main() -> None:
    CONFIG_DIR.mkdir(exist_ok=True)
    write_json("parameters.json", build_parameters())
    write_json("correlation_matrix_R.json", build_correlation())
    write_json("population_means.json", build_population_means())
    write_json("seeds.json", build_seeds())
    cfg = build_configurations()
    write_json("configurations.json", cfg)
    print("\nDRAFT configuration subset (needs sign-off):")
    for e in cfg["configurations"]:
        tag = f"  <- {e['role']}" if e["role"] else ""
        print(f"  {e['code']}  {e['axes']}{tag}")
    print(f"\nper-axis coverage satisfied: {cfg['coverage_satisfied']}")
    print(f"coverage detail: {json.dumps(cfg['per_axis_coverage'])}")


if __name__ == "__main__":
    main()
