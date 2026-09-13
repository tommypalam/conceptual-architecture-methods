from copy import deepcopy
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "code"))
from phase3_claude_review import IDS, MODEL, execute, make_plan, validate_response
from phase3_budget import Budget, BudgetStop


def response():
    result = {"benchmarks": [{"id": x, "status": "needs_revision", "blockers": ["draft"],
                              "smallest_next_step": "Complete stimuli", "defensible_claim": "No data yet"} for x in IDS],
              "overall_release": "blocked", "shared_issues": []}
    return {"model": MODEL, "stop_reason": "end_turn", "usage": {"input_tokens": 100, "output_tokens": 200},
            "content": [{"type": "text", "text": json.dumps(result)}]}


class ReviewTests(unittest.TestCase):
    def test_valid_replay_never_calls_provider(self):
        plan = make_plan()
        with tempfile.TemporaryDirectory() as root:
            record, n = execute(plan, root, lambda _: response())
            self.assertEqual(n, 1)
            with Budget(root) as budget:
                self.assertEqual(budget.audit()["charged_or_reserved_nano"], record["accounted_nano"])
            def forbidden(_):
                self.fail("Replay attempted another paid call")
            saved, n = execute(plan, root, forbidden)
            self.assertEqual(n, 0)
            self.assertEqual(saved, record)
            altered = deepcopy(plan)
            altered["request"]["temperature"] = 0
            with self.assertRaises(BudgetStop):
                execute(altered, root, forbidden)

    def test_failure_preserved_and_never_retried(self):
        with tempfile.TemporaryDirectory() as root:
            def failed(_):
                raise TimeoutError("sensitive text must not be saved")
            with self.assertRaises(BudgetStop):
                execute(make_plan(), root, failed)
            with self.assertRaises(BudgetStop):
                execute(make_plan(), root, lambda _: self.fail("Retried failure"))
            raw = next((Path(root) / "records").glob("*.json")).read_text()
            self.assertNotIn("sensitive text", raw)

    def test_reject_missing_benchmark_wrong_model_and_excess_usage(self):
        plan = make_plan()
        for field, value in (("model", "different"), ("stop_reason", "max_tokens")):
            raw = response()
            raw[field] = value
            with self.assertRaises(ValueError):
                validate_response(raw, plan)
        raw = response()
        raw["usage"]["input_tokens"] = plan["input_token_bound"] + 1
        with self.assertRaises(ValueError):
            validate_response(raw, plan)
        raw = response()
        body = json.loads(raw["content"][0]["text"])
        body["benchmarks"].pop()
        raw["content"][0]["text"] = json.dumps(body)
        with self.assertRaises(ValueError):
            validate_response(raw, plan)


if __name__ == "__main__":
    unittest.main()
