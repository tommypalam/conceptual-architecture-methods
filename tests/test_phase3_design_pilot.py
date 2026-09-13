import contextlib
import copy
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/"code"))
import phase3_design_pilot as pilot
from phase3_budget import BudgetStop, read_checked
from phase3_recognition_discussion import FAMILIES
from phase3_recognition_run import Ledger


class DesignPilot(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path = pilot.PILOT/"release.json"
        cls.release = read_checked(path) if path.exists() else pilot.prepare()

    def fixture(self, tmp):
        root, folder = Path(tmp)/"ledger", Path(tmp)/"run"
        old = read_checked(pilot.TRANSPORT/"CHECKPOINT.json")
        with zipfile.ZipFile(pilot.ROOT/old["archive"]) as z: z.extractall(root)
        return root, folder

    def response(self, request, text):
        if request["model"] == pilot.RATERS[1]:
            return {"model": request["model"], "usage": {"prompt_tokens": 100, "completion_tokens": 100},
                    "choices": [{"finish_reason": "stop", "message": {"content": text}}]}
        return {"model": request["model"], "usage": {"input_tokens": 100, "output_tokens": 100},
                "stop_reason": "end_turn", "content": [{"type": "text", "text": text}]}

    def mock(self, request):
        system = request.get("system", request["messages"][0]["content"])
        if "Draft a concise" in system:
            text = "Synthetic candidate preserving the allocation rule."
        elif "Independent structural" in system:
            text = json.dumps({"verdict": "accept", "blocking_issues": [], "limits": ["Synthetic review."]})
        elif system == pilot.SYSTEM:
            text = "This is the ultimatum game."
        else:
            items = json.loads(request["messages"][-1]["content"])
            discussion = "bounded discussion round" in system
            text = json.dumps({"ratings": [{"id": x["id"], "families": ["ultimatum"],
                    "ambiguous": not discussion and request["model"] == pilot.RATERS[0], "refusal": False,
                    **({"reason": "The answer explicitly names the game."} if discussion else {})} for x in items]})
        return self.response(request, text)

    def test_full_mock_discussion_and_zero_call_replay(self):
        with tempfile.TemporaryDirectory() as tmp, contextlib.redirect_stdout(io.StringIO()):
            root, folder = self.fixture(tmp); calls = []
            def responder(req): calls.append(req); return self.mock(req)
            result = pilot.collect(root=root, folder=folder, responder=responder, test_release=self.release)
            self.assertEqual(len(calls), 11)
            self.assertEqual(result["recognised"], 5)
            self.assertEqual(result["decision"], "discard_exploratory_candidate")
            self.assertEqual(result["formal_n50_gate"], "not_tested")
            self.assertFalse(result["population_released"])
            self.assertEqual(pilot.collect(True, root=root, folder=folder, test_release=self.release,
                responder=lambda _: self.fail("Replay network")), result)
            for name, expected in self.release["preserved_files"].items(): self.assertEqual(pilot.sha(root/name), expected)

    def test_structural_stop_and_new_api_failure(self):
        with tempfile.TemporaryDirectory() as tmp, contextlib.redirect_stdout(io.StringIO()):
            root, folder = self.fixture(tmp)
            def reject(req):
                system = req.get("system", req["messages"][0]["content"])
                if "Independent structural" in system:
                    return self.response(req, json.dumps({"verdict": "reject", "blocking_issues": ["Wrong payoff."], "limits": []}))
                return self.mock(req)
            result = pilot.collect(root=root, folder=folder, responder=reject, test_release=self.release)
            self.assertEqual(result["calls"], 2)
            self.assertEqual(result["decision"], "structural_stop")
        with tempfile.TemporaryDirectory() as tmp:
            root, folder = self.fixture(tmp)
            def fail(_): raise TimeoutError()
            with self.assertRaises(BudgetStop): pilot.collect(root=root, folder=folder, responder=fail, test_release=self.release)
            with self.assertRaises(BudgetStop): pilot.collect(root=root, folder=folder, responder=lambda _: self.fail("Retry"), test_release=self.release)

    def test_review_schema_missingness_and_worst_case_budget(self):
        with self.assertRaises(ValueError): pilot.review_value('{"verdict":"accept","blocking_issues":["bad"],"limits":[]}')
        self.assertLessEqual(self.release["recognition_cap_nano"], 500000000)
        with self.assertRaises(BudgetStop):
            pilot.job("recognition", 0, pilot.JUDGE, 128, "x"*pilot.BOUND, pilot.SYSTEM)
        ratings = {str(i+1): {"id": str(i+1), "families": ["ultimatum"] if i == 0 else [], "ambiguous": False, "refusal": False} for i in range(5)}
        self.assertEqual(pilot.analyze([ratings, ratings], [ratings, ratings])["decision"], "consider_separate_full_screen")
        missing = copy.deepcopy(ratings); missing["2"]["ambiguous"] = True
        self.assertEqual(pilot.analyze([ratings, ratings], [ratings, missing])["decision"], "inconclusive")
        with self.assertRaises(BudgetStop): pilot.analyze([{}, ratings], [ratings, ratings])
        items = []
        for i in range(5):
            identity = str(i+1)
            rating = {"id": identity, "families": list(FAMILIES), "ambiguous": False, "refusal": False}
            items.append({"id": identity, "answer": "\\"*1024, "own_rating": rating, "other_rating": rating})
        for model in pilot.RATERS:
            pilot.job("discussion", 0, model, 768, json.dumps(items, ensure_ascii=False, separators=(",", ":")),
                      pilot.RUBRIC+"\n\n"+pilot.DISCUSSION, ids=[i["id"] for i in items])


if __name__ == "__main__": unittest.main()
