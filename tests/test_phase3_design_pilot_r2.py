import contextlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/"code"))
import phase3_design_pilot_r2 as pilot
import test_phase3_design_pilot as previous_tests
from phase3_budget import BudgetStop, read_checked
from phase3_recognition_run import Ledger


class ClarifiedPilot(unittest.TestCase):
    mock = previous_tests.DesignPilot.mock
    response = previous_tests.DesignPilot.response

    @classmethod
    def setUpClass(cls):
        path = pilot.PILOT/"release.json"
        cls.release = read_checked(path) if path.exists() else pilot.prepare()

    def fixture(self, tmp):
        root, folder = Path(tmp)/"ledger", Path(tmp)/"run"
        old = read_checked(pilot.PARENT/"STOP_CHECKPOINT.json")
        with zipfile.ZipFile(pilot.ROOT/old["archive"]) as z: z.extractall(root)
        return root, folder

    def test_full_fenced_review_mock_discussion_and_replay(self):
        with tempfile.TemporaryDirectory() as tmp, contextlib.redirect_stdout(io.StringIO()):
            root, folder = self.fixture(tmp); calls = []
            def respond(req):
                calls.append(req)
                raw = self.mock(req)
                if "Independent structural" in req.get("system", ""):
                    raw["content"][0]["text"] = "```json\n"+raw["content"][0]["text"]+"\n```"
                return raw
            result = pilot.collect(root=root, folder=folder, responder=respond, test_release=self.release)
            self.assertEqual(len(calls), 10)
            self.assertEqual(result["recognised"], 5)
            self.assertEqual(result["discussion_calls"], 2)
            self.assertEqual(result["formal_n50_gate"], "not_tested")
            self.assertFalse(result["population_released"])
            self.assertEqual(pilot.collect(True, root=root, folder=folder, responder=lambda _: self.fail("Replay network"), test_release=self.release), result)
            for name, expected in self.release["preserved_files"].items(): self.assertEqual(pilot.sha(root/name), expected)

    def test_six_roles_and_strict_json_envelopes(self):
        tasks = pilot.candidate()["tasks"]
        self.assertEqual(len(tasks), 6)
        self.assertEqual([t["role"] for t in tasks], ["proposer"]+["responder"]*5)
        self.assertEqual([t["offer"] for t in tasks[1:]], [10,20,30,40,50])
        self.assertIn("any integer offer", tasks[0]["prompt"])
        value = {"verdict": "accept", "blocking_issues": [], "limits": []}
        for text in (json.dumps(value), "```json\n"+json.dumps(value)+"\n```"):
            self.assertEqual(pilot.review_value(text), value)
        for text in ('before\n```json\n{}\n```', '```json\n{}\n```\nafter', '```json\n{\n```', '{"verdict":"accept"}'):
            with self.assertRaises(ValueError): pilot.review_value(text)
        self.assertLessEqual(self.release["recognition_cap_nano"]+self.release["prior_screening_nano"], self.release["original_screening_cap_nano"])

    def test_revise_stops_before_probes(self):
        with tempfile.TemporaryDirectory() as tmp, contextlib.redirect_stdout(io.StringIO()):
            root, folder = self.fixture(tmp)
            def revise(req): return self.response(req, '```json\n{"verdict":"revise","blocking_issues":["Synthetic defect"],"limits":[]}\n```')
            result = pilot.collect(root=root, folder=folder, responder=revise, test_release=self.release)
            self.assertEqual(result["calls"], 1)
            self.assertEqual(result["recognition_calls"], 0)
            self.assertEqual(result["decision"], "structural_stop")

    def test_failure_retained_and_no_retry(self):
        with tempfile.TemporaryDirectory() as tmp:
            root, folder = self.fixture(tmp)
            def fail(_): raise TimeoutError()
            with self.assertRaises(BudgetStop): pilot.collect(root=root, folder=folder, responder=fail, test_release=self.release)
            with self.assertRaises(BudgetStop): pilot.collect(root=root, folder=folder, responder=lambda _: self.fail("Retry"), test_release=self.release)
            with Ledger(root, self.release) as ledger: self.assertEqual(len(ledger.state["failed"]), 1)


if __name__ == "__main__": unittest.main()
