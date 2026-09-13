import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "code"))
from phase3_budget import Budget, BudgetStop, NANO, token_cost_nano


class BudgetTests(unittest.TestCase):
    def test_aggregate_and_stage_caps_survive_restart(self):
        with tempfile.TemporaryDirectory() as root:
            with Budget(root) as budget:
                key = budget.reserve("one", "generation", {"text": "a"}, NANO, "manifest")
                budget.settle(key, NANO, "response")
            with Budget(root) as budget:
                self.assertEqual(budget.audit()["charged_or_reserved_nano"], NANO)
                with self.assertRaises(BudgetStop):
                    budget.reserve("two", "generation", {}, 1, "manifest")
                key = budget.reserve("review", "structural_review", {}, 2 * NANO, "manifest")
                budget.settle(key, 2 * NANO, "response")
                key = budget.reserve("recognition", "recognition", {}, 7 * NANO, "manifest")
                budget.settle(key, 7 * NANO, "response")
                with self.assertRaises(BudgetStop):
                    budget.reserve("extra", "recognition", {}, 1, "manifest")
                with self.assertRaises(BudgetStop):
                    budget.reserve("main", "main", {}, 1, "manifest")

    def test_interruption_retains_reservation_and_blocks_duplicates(self):
        with tempfile.TemporaryDirectory() as root:
            with Budget(root) as budget:
                key = budget.reserve("one", "generation", {}, 100, "manifest")
            with Budget(root) as budget:
                self.assertEqual(budget.audit()["charged_or_reserved_nano"], 100)
                with self.assertRaises(BudgetStop):
                    budget.reserve("two", "generation", {}, 100, "manifest")
                budget.settle(key, 50, "response")
                with self.assertRaises(BudgetStop):
                    budget.reserve("one", "generation", {}, 100, "different")
                with self.assertRaises(FileExistsError):
                    budget.settle(key, 0, "overwrite")

    def test_unknown_charge_keeps_full_bound(self):
        with tempfile.TemporaryDirectory() as root:
            with Budget(root) as budget:
                key = budget.reserve("one", "generation", {}, 100, "manifest")
                budget.settle(key, 0, "failed-response", status="unknown")
            with Budget(root) as budget:
                self.assertEqual(budget.audit()["charged_or_reserved_nano"], 100)
                with self.assertRaises(BudgetStop):
                    budget.reserve("two", "generation", {}, 1, "manifest")

    def test_corruption_and_competing_writer_fail_closed(self):
        with tempfile.TemporaryDirectory() as root:
            with Budget(root) as budget:
                with self.assertRaises(FileExistsError):
                    Budget(root)
                budget.reserve("one", "generation", {}, 100, "manifest")
            path = next((Path(root) / "reservations").glob("*.json"))
            value = json.loads(path.read_bytes())
            value["payload"]["reserved_nano"] = 0
            path.write_text(json.dumps(value), encoding="utf-8")
            with self.assertRaises(ValueError):
                Budget(root)
            self.assertFalse((Path(root) / "execution.lock").exists())

    def test_cost_and_input_validation(self):
        self.assertEqual(token_cost_nano(1000, 1000, "2.50", "15"), 19_250_000)
        for value in (True, -1, 1.5):
            with self.assertRaises(ValueError):
                token_cost_nano(value, 1, 1, 1)
        with self.assertRaises(ValueError):
            token_cost_nano(1, 1, "NaN", 1)


if __name__ == "__main__":
    unittest.main()
