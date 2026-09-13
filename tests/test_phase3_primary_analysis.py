from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "code"))
from phase3_primary_analysis import FAMILY, holm, paired_estimate, primary_family


class PrimaryAnalysis(unittest.TestCase):
    def test_exact_paired_permutation_and_saturation_warning(self):
        result = paired_estimate(dict.fromkeys("abcd", 1), dict.fromkeys("abcd", 0), seed=1, resamples=199)
        self.assertEqual(result["estimate"], 1)
        self.assertAlmostEqual(result["p_two_sided"], .125)
        self.assertTrue(result["bootstrap_degenerate"])
        self.assertLess(result["hoeffding_95_interval"][0], 1)

    def test_missing_outcomes_block_primary_not_denominator(self):
        result = paired_estimate({"a": 1, "b": None}, {"a": 0, "b": 1}, seed=1)
        self.assertEqual(result["identification_interval"], [0, .5])
        self.assertEqual(result["assigned_pairs"], 2)
        self.assertIsNone(result["p_two_sided"])
        self.assertIsNone(result["estimate"])
        self.assertEqual(result["complete_pair_supplement"], 1)

    def test_fractional_outcomes_and_dictionary_order_do_not_break_pairs(self):
        high = {"a": .5, "b": 1, "c": 0, "d": .25}
        low = {"d": .75, "c": .25, "b": .5, "a": 0}
        one = paired_estimate(high, low, seed=3, resamples=199)
        two = paired_estimate(dict(reversed(list(high.items()))), low, seed=3, resamples=199)
        self.assertEqual(one, two)
        self.assertAlmostEqual(one["estimate"], .0625)
        with self.assertRaises(ValueError):
            paired_estimate({"a": 1}, {"b": 0}, seed=1)

    def test_multiplicity_keeps_missing_cells_in_family(self):
        values = {key: None for key in FAMILY}
        values[FAMILY[0]] = .004
        self.assertEqual(holm(values)[FAMILY[0]], .04)
        self.assertIsNone(holm(values)[FAMILY[1]])
        with self.assertRaises(ValueError):
            holm({FAMILY[0]: .004})

    def test_exploration_never_passes_phase(self):
        cells = {key: {"high": dict.fromkeys("abcd", 1), "low": dict.fromkeys("abcd", 0)} for key in FAMILY}
        result = primary_family(cells, resamples=99, exploratory=True)
        self.assertIsNone(result["phase3_pass"])
        self.assertTrue(all(not row["positive_context_evidence"] for row in result["results"].values()))
        with self.assertRaises(ValueError):
            primary_family(cells, resamples=99)


if __name__ == "__main__":
    unittest.main()
