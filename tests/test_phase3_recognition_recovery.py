import contextlib
import copy
import io
import json
from pathlib import Path
import zipfile
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "code"))
import phase3_recognition_recovery as recovery
from phase3_budget import BudgetStop, digest, read_checked, write_once
from phase3_recognition_run import Ledger, RATERS, parse


class Recovery(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        frozen = recovery.RECOVERY / "release.json"
        cls.release = read_checked(frozen) if frozen.exists() else recovery.prepare()

    def fixture(self, tmp):
        root, folder = Path(tmp)/"ledger", Path(tmp)/"run"
        old = read_checked(recovery.RUN / "CHECKPOINT.json")
        with zipfile.ZipFile(recovery.ROOT / old["archive"]) as archive:
            archive.extractall(root)
        return root, folder

    def mock(self, request):
        self.assertIn(request["model"], RATERS, "A probe must never be dispatched")
        items = json.loads(request["messages"][-1]["content"])
        discussion = "bounded discussion round" in request.get("system", request["messages"][0].get("content", ""))
        values = [{"id": i["id"], "families": ["asch"], "ambiguous": False, "refusal": False,
                   **({"reason": "Synthetic agreement for recovery testing."} if discussion else {})} for i in items]
        content = json.dumps({"ratings": values})
        if request["model"] == RATERS[0]:
            return {"model": request["model"], "stop_reason": "end_turn",
                    "usage": {"input_tokens": 30, "output_tokens": 15},
                    "content": [{"type": "text", "text": content}]}
        return {"model": request["model"], "usage": {"prompt_tokens": 30, "completion_tokens": 15},
                "choices": [{"finish_reason": "stop", "message": {"content": content}}]}

    def test_full_recovery_replay_and_preserved_failure(self):
        with tempfile.TemporaryDirectory() as tmp, contextlib.redirect_stdout(io.StringIO()):
            root, folder = self.fixture(tmp)
            calls = []
            def responder(request):
                calls.append(digest(request))
                return self.mock(request)
            result = recovery.collect(root=root, folder=folder, responder=responder, test_release=self.release)
            self.assertEqual(len(calls), 72 + result["discussion_calls"])
            self.assertGreater(result["discussion_calls"], 0)
            self.assertEqual(result["reused_probe_calls"], 500)
            self.assertEqual(result["reused_coding_calls"], 28)
            self.assertEqual(result["final_exact_agreement"], 1)
            self.assertFalse(result["population_released"])
            self.assertEqual(recovery.collect(True, root=root, folder=folder, test_release=self.release,
                responder=lambda _: self.fail("Network on replay")), result)
            for name, sha in self.release["preserved_files"].items():
                self.assertEqual(recovery.sha(root/name), sha)
            with Ledger(root, self.release) as ledger:
                self.assertFalse(ledger.state["failed"])
                self.assertFalse(ledger.state["pending"])
                self.assertEqual(len(ledger.state["reservations"]), 577+len(calls))
            original = read_checked(root/"records"/(digest(recovery.FAILED)+".json"))
            self.assertIsNotNone(original["error"])
            self.assertEqual(original["accounted_nano"], 31920900)
            self.assertEqual(read_checked(folder/"coding_manifest.json")["jobs"][0]["slot"], recovery.REPLACEMENT)

    def test_new_failure_stops_without_retry(self):
        with tempfile.TemporaryDirectory() as tmp:
            root, folder = self.fixture(tmp)
            def failure(_):
                raise TimeoutError()
            with self.assertRaises(BudgetStop):
                recovery.collect(root=root, folder=folder, responder=failure, test_release=self.release)
            with self.assertRaises(BudgetStop):
                recovery.collect(root=root, folder=folder, responder=lambda _: self.fail("Retry"), test_release=self.release)
            with Ledger(root, self.release) as ledger:
                self.assertEqual(ledger.state["recognition_nano"], 31920900)
                self.assertEqual(ledger.state["failed"], [digest(recovery.REPLACEMENT)])

    def test_pending_corruption_budget_and_duplicate_guards(self):
        with tempfile.TemporaryDirectory() as tmp:
            root, folder = self.fixture(tmp)
            jobs = recovery.inherited(root)[-1]
            with self.assertRaises(BudgetStop):
                recovery.execute([jobs[0], jobs[0]], self.release, "coding", root, folder, self.mock, False)
            with self.assertRaises(BudgetStop):
                recovery.collect(True, root=root, folder=folder, test_release=self.release,
                    responder=lambda _: self.fail("Missing replay dispatch"))
            bad = copy.deepcopy(self.release)
            bad["provider_caps_nano"]["anthropic"] = 1
            with self.assertRaises(BudgetStop):
                Ledger(root, bad)
            bad = copy.deepcopy(self.release)
            bad["original_screening_cap_nano"] = 1
            with self.assertRaises(BudgetStop):
                recovery.verify(bad, root)
            job = jobs[0]
            write_once(root/"reservations"/(digest(job["slot"])+".json"),
                {"slot": job["slot"], "request": job["request"], "stage": "recognition",
                 "reserved_nano": job["reserved_nano"], "release_sha256": digest(self.release), "manifest_sha256": "interrupted"})
            with self.assertRaises(BudgetStop):
                recovery.collect(root=root, folder=folder, test_release=self.release,
                    responder=lambda _: self.fail("Pending dispatch repeated"))
            (root/"records"/(digest(recovery.FAILED)+".json")).write_text("{}")
            with self.assertRaises((BudgetStop, KeyError)):
                Ledger(root, self.release)

    def test_identity_omission_reorder_truncation_guards(self):
        job = recovery.inherited()[-1][0]
        raw = self.mock(job["request"])
        self.assertEqual(len(parse(raw, job)), 10)
        ratings = json.loads(raw["content"][0]["text"])["ratings"]
        variants = [ratings[:-1], ratings + [ratings[0]], ratings[::-1], [ratings[0]] * 10]
        changed = copy.deepcopy(ratings); changed[0]["id"] = "0"*16
        variants.append(changed)
        for rows in variants:
            bad = copy.deepcopy(raw)
            bad["content"][0]["text"] = json.dumps({"ratings": rows})
            with self.assertRaises(ValueError):
                parse(bad, job)
        bad = copy.deepcopy(raw); bad["stop_reason"] = "max_tokens"
        with self.assertRaises(ValueError):
            parse(bad, job)
        bad = copy.deepcopy(raw); bad["content"][0]["text"] = '{"ratings": ['
        with self.assertRaises(ValueError):
            parse(bad, job)
        self.assertEqual(job["request"], next(j for j in read_checked(recovery.RUN/"coding_manifest.json")["jobs"] if j["slot"] == recovery.FAILED)["request"])


if __name__ == "__main__":
    unittest.main()
