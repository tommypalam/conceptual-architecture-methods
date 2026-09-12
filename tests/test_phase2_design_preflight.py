"""Regression checks for design aliasing and outcome-free proposed repair."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "code"))
from phase2_design_preflight import inspect_design, propose_single_replacement, call_budget

CURRENT = ["00100", "11011", "00001", "11110", "00010", "11101", "00111", "11000", "00000", "11111"]


class DesignChecks(unittest.TestCase):
    def test_balanced_coverage_does_not_imply_identifiability(self):
        result = inspect_design(CURRENT)
        self.assertTrue(result["coverage_pass"])
        self.assertEqual(result["additive_rank"], 5)
        self.assertIn("Freedom = Justice", result["exact_axis_aliases"])

    def test_proposal_preserves_anchors_and_repairs_rank_without_mutation(self):
        before = list(CURRENT)
        result = propose_single_replacement(CURRENT)
        self.assertEqual(CURRENT, before)
        self.assertEqual(len(set(CURRENT) - set(result["design"]["codes"])), 1)
        self.assertTrue(result["design"]["full_additive_rank"])
        self.assertTrue(result["design"]["anchors_present"])
        self.assertTrue(result["design"]["coverage_pass"])
        self.assertEqual(result, propose_single_replacement(CURRENT))

    def test_healthy_design_requires_no_repair(self):
        proposal = propose_single_replacement(CURRENT)
        self.assertIsNone(propose_single_replacement(proposal["design"]["codes"]))

    def test_invalid_and_duplicate_codes_rejected(self):
        for codes in ([], ["0010"], ["nnnnn"], ["00000", "00000"]):
            with self.assertRaises(ValueError):
                inspect_design(codes)

    def test_complement_alias_detected(self):
        result = inspect_design(["01000", "10111"])
        self.assertIn("Freedom = 1 - Justice", result["exact_axis_aliases"])

    def test_budget_counts_shared_unencoded_base_once(self):
        result = call_budget()
        self.assertEqual(result["core_calls"], 12000)
        self.assertEqual(result["core_plus_anchor_postfilter_calls"], 13200)
        self.assertEqual(result["group_calls_maximum"], 3950)
        self.assertEqual(result["default_total_calls_maximum"], 15950)
        self.assertEqual(result["default_plus_postfilter_calls_maximum"], 17150)
        self.assertLess(result["proposed_operational_ceiling_usd"], result["user_hard_cap_usd"])
        self.assertIsNone(result["dollar_estimate"])


if __name__ == "__main__":
    unittest.main()
