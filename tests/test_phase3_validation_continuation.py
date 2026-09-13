import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "code"))
from phase3_budget import Budget, BudgetStop, digest, write_once
from phase3_validation_continuation import Continuation, FAILED_SLOT, execute


class LinkedContinuation(unittest.TestCase):
    def fixture(self, root):
        with Budget(root) as budget:
            key = budget.reserve(FAILED_SLOT, "structural_review", {"model": "claude-sonnet-4-6"}, 100, "old")
            record = {"raw": {"stop_reason": "max_tokens"}, "error": {"type": "ValueError"},
                      "accounted_nano": 100, "manifest_sha256": "old"}
            write_once(Path(root) / "records" / (key + ".json"), record)
            budget.settle(key, 100, digest(record), status="failed")
        return {"accepted_failure_slot": FAILED_SLOT, "accepted_failure_key": key,
                "retained_charge_nano": 100,
                "preserved_files": {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in Path(root).rglob("*.json")}}

    def plan(self, slot="candidate_r2/milgram"):
        return {"jobs": [{"slot": slot, "kind": "generation", "stage": "generation",
                         "required_fields": ["setup"], "request": {"model": "gpt-5.4-2026-03-05", "max_completion_tokens": 100},
                         "input_token_bound": 100, "reserved_nano": 1000000}]}

    def response(self, _):
        return {"model": "gpt-5.4-2026-03-05", "usage": {"prompt_tokens": 10, "completion_tokens": 10},
                "choices": [{"finish_reason": "stop", "message": {"content": json.dumps({"stimulus": {"setup": "A candidate"}, "correspondence": [], "unresolved_elements": []})}}]}

    def test_preserved_failure_and_zero_call_replay(self):
        with tempfile.TemporaryDirectory() as root:
            rec = self.fixture(root)
            results, calls = execute(self.plan(), rec, root=root, responder=self.response)
            self.assertEqual(calls, 1)
            again, calls = execute(self.plan(), rec, root=root, replay=True,
                                   responder=lambda _: self.fail("Network during replay"))
            self.assertEqual((again, calls), (results, 0))
            with Continuation(root, rec) as budget:
                state = budget.audit()
                self.assertEqual(state["failed"], [])
                self.assertEqual(state["historical_failed"], [digest(FAILED_SLOT)])
                self.assertEqual(state["by_provider_nano"]["anthropic"], 100)
                with self.assertRaises(BudgetStop):
                    budget.reserve(FAILED_SLOT, "structural_review", {}, 100, "retry")

    def test_new_failure_stops_and_retains_full_reservation(self):
        with tempfile.TemporaryDirectory() as root:
            rec = self.fixture(root)
            def truncated(request):
                response = self.response(request)
                response["choices"][0]["finish_reason"] = "length"
                return response
            with self.assertRaises(BudgetStop):
                execute(self.plan(), rec, root=root, responder=truncated)
            with self.assertRaises(BudgetStop):
                execute(self.plan("candidate_r2/asch"), rec, root=root, responder=self.response)
            with Continuation(root, rec) as budget:
                self.assertEqual(budget.audit()["by_provider_nano"]["openai"], 1000000)

    def test_changed_manifest_and_omitted_response_block(self):
        with tempfile.TemporaryDirectory() as root:
            rec = self.fixture(root)
            execute(self.plan(), rec, root=root, responder=self.response)
            changed = {**self.plan(), "different": True}
            with self.assertRaises(BudgetStop):
                execute(changed, rec, root=root, responder=lambda _: self.fail("Must not dispatch"))
            (Path(root) / "records" / (digest("candidate_r2/milgram") + ".json")).unlink()
            with self.assertRaises(BudgetStop):
                Continuation(root, rec)

    def test_historical_corruption_and_missing_replay_call_block(self):
        with tempfile.TemporaryDirectory() as root:
            rec = self.fixture(root)
            with self.assertRaises(BudgetStop):
                execute(self.plan(), rec, root=root, replay=True)
            path = Path(root) / "records" / (digest(FAILED_SLOT) + ".json")
            path.write_text("{}", encoding="utf-8")
            with self.assertRaises(BudgetStop):
                Continuation(root, rec)


if __name__ == "__main__":
    unittest.main()
