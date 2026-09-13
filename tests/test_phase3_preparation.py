"""Meaningful offline guardrails for draft Phase 3 accounting and sampling."""
import sys
import unittest
from pathlib import Path
import numpy as np
from scipy.stats import beta, kstest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "code"))
from phase3_preflight import cells, inventory, context_descriptor, report, MODULATORS
from phase3_sensitivity import matrix_regimes, sample_profiles, nearest_correlation
from utils import R, PARAM_NAMES, BETA_PARAMS


class Phase3Preparation(unittest.TestCase):
    def test_complete_scope_and_budget_ambiguity(self):
        self.assertEqual(inventory(cells(100))["nominal_calls"], 110400)
        self.assertEqual(inventory(cells(10))["nominal_calls"], 20400)
        self.assertEqual(inventory(cells(1))["nominal_calls"], 11400)
        self.assertEqual(sum(map(len, MODULATORS.values())), 9)
        counts = inventory(cells())["counts"]
        self.assertEqual(counts["primary"], 4000)
        self.assertEqual(counts["recognition"], 500)
        self.assertEqual(counts["modulator"], 900)
        self.assertFalse(report()["ready_to_collect"])

    def test_reject_duplicate_slots_and_invalid_sample(self):
        rows = cells(1)
        with self.assertRaises(ValueError):
            inventory(rows + [rows[0]])
        for n in (0, -1, 1.5, True):
            with self.assertRaises(ValueError):
                cells(n)

    def test_neutral_is_not_low(self):
        context = dict(Freedom="NEUTRAL", Justice=0, Authority=1, Care=0, Loyalty=0)
        self.assertEqual(context_descriptor(context), "NEUTRAL/0/1/0/0")
        for value in (None, .5, True, "0"):
            with self.assertRaises(ValueError):
                context_descriptor({**context, "Freedom": value})

    def test_sensitivity_does_not_modify_canonical_matrix(self):
        original = R.copy()
        regimes = matrix_regimes(2026091303)
        np.testing.assert_array_equal(R, original)
        self.assertEqual(len(regimes), 103)
        self.assertEqual(len({m.tobytes() for k,m in regimes.items() if k.startswith("D")}), 100)
        for matrix in regimes.values():
            np.testing.assert_allclose(matrix, matrix.T, atol=1e-10)
            np.testing.assert_allclose(np.diag(matrix), 1, atol=1e-10)
            self.assertGreaterEqual(np.linalg.eigvalsh(matrix)[0], -1e-9)
        again = matrix_regimes(2026091303)
        np.testing.assert_array_equal(again["D007"], regimes["D007"])

    def test_projection_and_marginals(self):
        broken = np.array([[1,.9,.9],[.9,1,-.9],[.9,-.9,1]])
        corrected = nearest_correlation(broken)
        self.assertGreaterEqual(np.linalg.eigvalsh(corrected)[0], -1e-9)
        np.testing.assert_allclose(np.diag(corrected), 1)
        # A wrong normal CDF for t samples distorts marginals; this catches that.
        for df in (None, 4, 8, 16):
            sample = sample_profiles(R, 6000, 2026091303, df=df)
            self.assertTrue(np.isfinite(sample).all())
            for j,name in enumerate(PARAM_NAMES):
                self.assertLess(kstest(sample[:,j], beta(*BETA_PARAMS[name]).cdf).statistic, .04)
        with self.assertRaises(ValueError):
            sample_profiles(-R, 10, 1)


if __name__ == "__main__":
    unittest.main()
