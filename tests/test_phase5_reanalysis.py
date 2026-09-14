"""Offline checks for the Phase 5 within-arm reanalysis.

No API calls. Verifies the statistical helpers against hand-computable cases and
confirms the published artefact is internally consistent with its own inputs.
These checks establish software behaviour, not scientific or moral validity.
"""
from __future__ import annotations

import csv
import importlib.util
import json
import math
import random
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
MODULE_PATH = ROOT / "code" / "phase5_reanalysis.py"
RESULTS = ROOT / "experiments" / "phase5_analysis" / "reanalysis_20260914" / "dispersion_results.json"
RESPONSES = ROOT / "experiments" / "phase2_confirmation_20260913" / "analysis" / "responses.csv"


def _load_module():
    spec = importlib.util.spec_from_file_location("phase5_reanalysis", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


mod = _load_module()


class TestPointBiserial:
    def test_no_variance_returns_none(self):
        assert mod.point_biserial([0.1, 0.2, 0.3], [0, 0, 0]) is None
        assert mod.point_biserial([0.1, 0.2, 0.3], [1, 1, 1]) is None

    def test_constant_predictor_returns_none(self):
        assert mod.point_biserial([0.5, 0.5, 0.5, 0.5], [0, 1, 0, 1]) is None

    def test_perfect_separation_is_strongly_positive(self):
        values = [0.1, 0.2, 0.8, 0.9]
        r = mod.point_biserial(values, [0, 0, 1, 1])
        assert r is not None and r > 0.9

    def test_sign_flips_with_outcome(self):
        values = [0.1, 0.2, 0.8, 0.9]
        high = mod.point_biserial(values, [0, 0, 1, 1])
        low = mod.point_biserial(values, [1, 1, 0, 0])
        assert high == pytest.approx(-low)

    def test_matches_pearson_on_binary_outcome(self):
        """Point-biserial is Pearson r when one variable is 0/1."""
        rng = random.Random(7)
        values = [rng.random() for _ in range(50)]
        binary = [1 if v > 0.5 else 0 for v in values]

        n = len(values)
        mx = sum(values) / n
        my = sum(binary) / n
        cov = sum((a - mx) * (b - my) for a, b in zip(values, binary))
        sx = math.sqrt(sum((a - mx) ** 2 for a in values))
        sy = math.sqrt(sum((b - my) ** 2 for b in binary))
        pearson = cov / (sx * sy)

        assert mod.point_biserial(values, binary) == pytest.approx(pearson, abs=1e-9)


class TestPermutationP:
    def test_bounded_and_never_zero(self):
        """A permutation p is (hits+1)/(N+1), so it can never be exactly 0."""
        rng = random.Random(11)
        values = [i / 40 for i in range(40)]
        binary = [1 if i >= 20 else 0 for i in range(40)]
        observed = mod.point_biserial(values, binary)
        p = mod.permutation_p(values, binary, observed, rng)
        assert 0 < p <= 1
        assert p >= 1 / (mod.N_PERM + 1)

    def test_strong_effect_gives_small_p(self):
        rng = random.Random(13)
        values = [i / 60 for i in range(60)]
        binary = [1 if i >= 30 else 0 for i in range(60)]
        observed = mod.point_biserial(values, binary)
        assert mod.permutation_p(values, binary, observed, rng) < 0.01

    def test_does_not_mutate_caller_outcome(self):
        rng = random.Random(17)
        values = [i / 20 for i in range(20)]
        binary = [1 if i >= 10 else 0 for i in range(20)]
        original = list(binary)
        mod.permutation_p(values, binary, mod.point_biserial(values, binary), rng)
        assert binary == original


class TestMinorityOption:
    def test_prefers_option_the_baseline_never_chose(self):
        counts = {"ADOPT": 400}
        assert mod.minority_option(counts, ["ADOPT", "WAIT"]) == "WAIT"

    def test_falls_back_to_least_chosen(self):
        counts = {"A": 369, "B": 31}
        assert mod.minority_option(counts, ["A", "B"]) == "B"


class TestLogistic:
    def test_recovers_sign_of_a_known_effect(self):
        rng = random.Random(19)
        design, outcome = [], []
        for _ in range(200):
            x = rng.gauss(0, 1)
            design.append([x, rng.gauss(0, 1)])
            outcome.append(1 if rng.random() < 1 / (1 + math.exp(-2.0 * x)) else 0)
        weights = mod.logistic(design, outcome)
        assert weights[0] > 0
        assert abs(weights[0]) > abs(weights[1])


class TestPublishedArtefact:
    """The committed artefact must stay consistent with its own recorded inputs."""

    @pytest.fixture(scope="class")
    def results(self):
        if not RESULTS.exists():
            pytest.skip("artefact not generated; run code/phase5_reanalysis.py")
        return json.loads(RESULTS.read_text())

    def test_provenance_recorded(self, results):
        assert results["seed"] == mod.SEED
        assert results["n_permutations"] == mod.N_PERM
        assert results["source_population_content_hash"]

    def test_population_hash_matches_source(self, results):
        pop = ROOT / "experiments" / "phase2_confirmation_20260913" / "population.json"
        if not pop.exists():
            pytest.skip("frozen population not present")
        assert results["source_population_content_hash"] == json.loads(pop.read_text())["content_hash"]

    def test_degeneracy_matches_raw_responses(self, results):
        """Recomputed U-arm modal shares must equal the published ones."""
        if not RESPONSES.exists():
            pytest.skip("frozen responses not present")
        with RESPONSES.open() as fh:
            rows = [
                r for r in csv.DictReader(fh)
                if r["stage"] == "simple" and r["status"] == "ok" and r["arm"] == "U"
            ]
        for key, cell in results["u_arm_degeneracy"].items():
            task, config = key.split("_")
            votes = [r["vote"] for r in rows if r["problem"] == task and r["config"] == config]
            assert len(votes) == cell["n"]
            modal = max(votes.count(v) for v in set(votes)) / len(votes)
            assert modal == pytest.approx(cell["modal_share"], abs=5e-5)
            assert cell["unanimous"] is (modal == 1.0)

    def test_four_of_six_baselines_are_deterministic(self, results):
        """The documented saturation claim, asserted so a data change would surface."""
        unanimous = [k for k, v in results["u_arm_degeneracy"].items() if v["unanimous"]]
        assert sorted(unanimous) == ["S2_00100", "S2_11011", "S3_00100", "S3_11011"]

    def test_pd_leads_every_non_degenerate_cell(self, results):
        """PD ranked first of ten wherever the outcome had variance to explain."""
        ranked = [
            (k, c["multivariate"]["pd_rank"])
            for k, c in results["dissent_cells"].items()
            if c.get("multivariate") and c["n_dissent"] >= 20
        ]
        assert len(ranked) == 4
        for name, rank in ranked:
            assert rank == 1, f"{name} PD rank {rank}"

    def test_quintile_rates_are_probabilities(self, results):
        for cell in results["dissent_cells"].values():
            block = cell.get("pd")
            if block:
                assert len(block["quintile_dissent_rates"]) == 5
                assert all(0.0 <= q <= 1.0 for q in block["quintile_dissent_rates"])

    def test_dissent_counts_within_cell_size(self, results):
        for cell in results["dissent_cells"].values():
            assert 0 <= cell["n_dissent"] <= cell["n"]

    def test_hypothesis_verdicts_are_known_values(self, results):
        allowed = {"supported", "null", "wrong_sign", "degenerate"}
        scored = results["prospective_hypotheses"]["scored"]
        assert len(scored) == len(mod.HYPOTHESES)
        assert all(h["verdict"] in allowed for h in scored)

    def test_no_hypothesis_has_the_wrong_sign(self, results):
        """Documented as 5 supported, 4 null, 0 wrong sign."""
        tally = results["prospective_hypotheses"]["tally"]
        assert tally.get("wrong_sign", 0) == 0
        assert sum(tally.values()) == len(mod.HYPOTHESES)

    def test_supported_hypotheses_have_positive_r(self, results):
        for h in results["prospective_hypotheses"]["scored"]:
            if h["verdict"] == "supported":
                assert h["r"] > 0 and h["perm_p"] < 0.05
