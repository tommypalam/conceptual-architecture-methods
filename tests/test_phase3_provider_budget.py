import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "code"))
from phase3_budget import BudgetStop, POLICY
from phase3_provider_budget import CAPS, check_caps, provider


class ProviderBudget(unittest.TestCase):
    def stages(self, amount=0):
        return {"generation": 0, "structural_review": amount, "recognition": 0}

    def test_existing_spend_carries_forward_and_providers_are_distinct(self):
        current = {"anthropic": 327472200, "openai": 10098000}
        checked, _ = check_caps(current, self.stages(sum(current.values())))
        self.assertEqual(CAPS["anthropic"] - checked["anthropic"], 14672527800)
        self.assertEqual(CAPS["openai"] - checked["openai"], 29989902000)
        self.assertEqual(provider({"model": "claude-sonnet-4-6"}), "anthropic")
        with self.assertRaises(BudgetStop):
            provider({"model": "unregistered-model"})

    def test_provider_caps_cannot_borrow_from_other_balance(self):
        for name, cap in CAPS.items():
            current = dict.fromkeys(CAPS, 0)
            current[name] = cap + 1
            with self.assertRaisesRegex(BudgetStop, "Provider hard cap"):
                check_caps(current, self.stages(cap + 1))

    def test_stage_budget_still_limits_whole_batch(self):
        proposals = [{"request": {"model": "gpt-5.4-2026-03-05"}, "stage": "generation", "reserved_nano": 600000000}] * 2
        with self.assertRaisesRegex(BudgetStop, "Stage allocation"):
            check_caps(dict.fromkeys(CAPS, 0), self.stages(), proposals)
        with self.assertRaisesRegex(BudgetStop, "totals disagree"):
            check_caps({"anthropic": 1, "openai": 0}, self.stages())


if __name__ == "__main__":
    unittest.main()
