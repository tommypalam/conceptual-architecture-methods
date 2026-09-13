import contextlib
import copy
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "code"))
import phase3_recognition_transport as transport
from phase3_budget import BudgetStop, read_checked
from phase3_recognition_run import parse, Ledger
from test_phase3_recognition_recovery import Recovery


class Transport(unittest.TestCase):
    mock = Recovery.mock

    @classmethod
    def setUpClass(cls):
        path = transport.TRANSPORT / "release.json"
        cls.release = read_checked(path) if path.exists() else transport.prepare()

    def fixture(self, tmp):
        root, folder = Path(tmp)/"ledger", Path(tmp)/"run"
        old = read_checked(transport.PREVIOUS/"CHECKPOINT.json")
        with zipfile.ZipFile(transport.ROOT/old["archive"]) as archive:
            archive.extractall(root)
        return root, folder

    def test_full_completion_replay_and_preservation(self):
        with tempfile.TemporaryDirectory() as tmp, contextlib.redirect_stdout(io.StringIO()):
            root, folder = self.fixture(tmp)
            calls = []
            def responder(request):
                calls.append(request)
                return self.mock(request)
            result = transport.collect(root=root, folder=folder, responder=responder, test_release=self.release)
            self.assertEqual(len(calls), 72+result["discussion_calls"])
            self.assertGreater(result["discussion_calls"], 0)
            self.assertEqual(result["final_exact_agreement"], 1)
            self.assertEqual(transport.collect(True, root=root, folder=folder, test_release=self.release,
                responder=lambda _: self.fail("Replay network")), result)
            for name, sha in self.release["preserved_files"].items():
                self.assertEqual(transport.sha(root/name), sha)
            with Ledger(root, self.release) as ledger:
                self.assertFalse(ledger.state["failed"])
                self.assertEqual(len(ledger.state["reservations"]), 578+len(calls))

    def test_mapping_changes_only_ids_and_rejects_bad_ids(self):
        original = transport.inherited()[-1][0]
        job = transport.short_job(original)
        before = json.loads(original["request"]["messages"][-1]["content"])
        after = json.loads(job["request"]["messages"][-1]["content"])
        self.assertEqual([r["answer"] for r in before], [r["answer"] for r in after])
        self.assertEqual(job["item_ids"], [str(i) for i in range(1,11)])
        restored = copy.deepcopy(job["request"])
        restored["messages"][-1]["content"] = original["request"]["messages"][-1]["content"]
        self.assertEqual(restored, original["request"])
        raw = self.mock(job["request"])
        parsed = parse(raw, job)
        recovered = transport.original_rows(job, {"parsed": parsed})
        self.assertEqual([r["id"] for r in recovered], original["item_ids"])
        for rows in (parsed[:-1], parsed+[parsed[0]], parsed[::-1]):
            bad = copy.deepcopy(raw); bad["content"][0]["text"] = json.dumps({"ratings": rows})
            with self.assertRaises(ValueError): parse(bad, job)
        bad = copy.deepcopy(job); bad["original_item_ids"][0] = bad["original_item_ids"][1]
        with self.assertRaises(BudgetStop): transport.original_rows(bad, {"parsed": parsed})

    def test_failure_preserves_new_intent_and_stops(self):
        with tempfile.TemporaryDirectory() as tmp:
            root, folder = self.fixture(tmp)
            def fail(_): raise TimeoutError()
            with self.assertRaises(BudgetStop):
                transport.collect(root=root, folder=folder, responder=fail, test_release=self.release)
            with self.assertRaises(BudgetStop):
                transport.collect(root=root, folder=folder, responder=lambda _: self.fail("Retry"), test_release=self.release)
            with Ledger(root, self.release) as ledger:
                self.assertEqual(ledger.state["recognition_nano"], 31920900)
                self.assertEqual(len(ledger.state["failed"]), 1)


if __name__ == "__main__": unittest.main()
