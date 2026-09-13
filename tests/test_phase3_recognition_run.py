import copy
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "code"))
from phase3_budget import Budget, BudgetStop, digest, read_checked
from phase3_recognition_run import Ledger, execute, parse, JUDGE, RATERS
from phase3_recognition_analysis import analyze


class RecognitionRuntime(unittest.TestCase):
    def fixture(self, root):
        with Budget(root):
            pass
        jobs = [{"kind": "probe", "slot": f"recognition_r1/probe/test/{i}",
                 "request": {"model": JUDGE, "max_tokens": 128},
                 "input_token_bound": 200, "reserved_nano": 3000000} for i in range(2)]
        release = {"slots": {j["slot"]: {"model": JUDGE, "reserved_nano": j["reserved_nano"],
                    "kind": "probe", "input_token_bound": 200, "max_output": 128,
                    "request_sha256": digest(j["request"])} for j in jobs},
                   "recognition_cap_nano": 6000000, "provider_caps_nano": {"anthropic": 15000000000, "openai": 30000000000},
                   "historical_keys": [], "preserved_files": {"policy.json": hashlib.sha256((Path(root)/"policy.json").read_bytes()).hexdigest()}}
        return jobs, release

    def response(self, request):
        return {"model": request["model"], "stop_reason": "end_turn", "usage": {"input_tokens": 30, "output_tokens": 15},
                "content": [{"type": "text", "text": "This resembles the Asch conformity experiment."}]}

    def test_complete_and_zero_call_replay(self):
        with tempfile.TemporaryDirectory() as root:
            jobs, release = self.fixture(root)
            actual = execute(jobs, release, "probe", root=root, responder=self.response)
            expected = execute(jobs, release, "probe", root=root, replay=True, responder=lambda _: self.fail("Network on replay"))
            self.assertEqual(actual, expected)
            with Ledger(root, release) as ledger:
                self.assertEqual(len(ledger.state["reservations"]), 2)
                self.assertFalse(ledger.state["failed"])

    def test_unknown_failure_retains_bound_and_blocks_resume(self):
        with tempfile.TemporaryDirectory() as root:
            jobs, release = self.fixture(root)
            def fail(_):
                raise TimeoutError()
            with self.assertRaises(BudgetStop):
                execute(jobs, release, "probe", root=root, responder=fail)
            with self.assertRaises(BudgetStop):
                execute(jobs, release, "probe", root=root, responder=lambda _: self.fail("Retry"))
            with Ledger(root, release) as ledger:
                self.assertEqual(ledger.state["recognition_nano"], 3000000)
                self.assertEqual(len(ledger.state["failed"]), 1)

    def test_duplicate_missing_and_changed_requests_block(self):
        with tempfile.TemporaryDirectory() as root:
            jobs, release = self.fixture(root)
            with self.assertRaises(BudgetStop):
                execute([jobs[0], jobs[0]], release, "probe", root=root)
            with self.assertRaises(BudgetStop):
                execute(jobs, release, "probe", root=root, replay=True)
            execute(jobs, release, "probe", root=root, responder=self.response)
            changed = copy.deepcopy(jobs)
            changed[0]["request"]["temperature"] = 0
            with self.assertRaises(BudgetStop):
                execute(changed, release, "probe", root=root, replay=True)
            (Path(root)/"records"/(digest(jobs[0]["slot"])+".json")).unlink()
            with self.assertRaises(BudgetStop):
                Ledger(root, release)

    def test_complete_capacity_and_dispatch_output_guard(self):
        with tempfile.TemporaryDirectory() as root:
            jobs, release = self.fixture(root)
            bad = copy.deepcopy(release)
            bad["provider_caps_nano"]["anthropic"] = 1
            with self.assertRaises(BudgetStop):
                Ledger(root, bad)
            jobs[0]["request"]["max_tokens"] = 10000
            with self.assertRaises(BudgetStop):
                execute(jobs, release, "probe", root=root, responder=lambda _: self.fail("Out-of-bound dispatch"))
            self.assertFalse(list((Path(root)/"reservations").glob("*.json")))

    def test_pending_and_historical_corruption_block(self):
        from phase3_budget import write_once
        with tempfile.TemporaryDirectory() as root:
            jobs, release = self.fixture(root)
            with Ledger(root, release) as ledger:
                intent = {"slot": jobs[0]["slot"], "request": jobs[0]["request"], "stage": "recognition",
                          "reserved_nano": 3000000, "release_sha256": digest(release), "manifest_sha256": "interrupted"}
                write_once(Path(root)/"reservations"/(digest(jobs[0]["slot"])+".json"), intent)
            with self.assertRaises(BudgetStop):
                execute(jobs, release, "probe", root=root, responder=lambda _: self.fail("Pending repeated"))
            (Path(root)/"policy.json").write_text("{}")
            with self.assertRaises((BudgetStop, KeyError)):
                Ledger(root, release)

    def test_truncation_usage_and_coding_ids(self):
        job = {"kind": "probe", "request": {"model": JUDGE, "max_tokens": 128}, "input_token_bound": 200}
        raw = self.response(job["request"])
        for field, value in (("stop_reason", "max_tokens"), ("model", "unknown")):
            bad = copy.deepcopy(raw); bad[field] = value
            with self.assertRaises(ValueError):
                parse(bad, job)
        raw["usage"]["input_tokens"] = 201
        with self.assertRaises(ValueError):
            parse(raw, job)
        job = {"kind": "coding", "request": {"model": RATERS[0], "max_tokens": 1024},
               "input_token_bound": 200, "item_ids": ["0"*16]}
        raw = self.response(job["request"])
        raw["content"][0]["text"] = json.dumps({"ratings": [{"id": "1"*16, "families": [], "ambiguous": False, "refusal": False}]})
        with self.assertRaises(ValueError):
            parse(raw, job)

    def test_threshold_and_unresolved_denominator(self):
        jobs = [{"slot": f"{name}/{form}/{i}", "benchmark": name, "form": form}
                for name in ("milgram", "asch", "ultimatum", "bystander", "reactance")
                for form in ("canonical", "alternative") for i in range(50)]
        ratings = {}
        for j in jobs:
            key = digest(j["slot"])[:16]
            ratings[key] = {"id": key, "families": [j["benchmark"]] if int(j["slot"].split("/")[-1]) < 15 else [],
                            "ambiguous": False, "refusal": False}
        result = analyze(jobs, [ratings, ratings], [ratings, ratings])
        self.assertTrue(all(r["decision"] == "passes_recognition_screen" for r in result["rows"] if r["form"] == "alternative"))
        key = digest("milgram/alternative/15")[:16]
        changed = copy.deepcopy(ratings); changed[key]["families"] = ["milgram"]
        result = analyze(jobs, [ratings, ratings], [changed, changed])
        self.assertEqual(result["rows"][1]["decision"], "reject")
        result = analyze(jobs, [ratings, ratings], [ratings, changed])
        self.assertEqual(result["rows"][1]["decision"], "incomplete")
        self.assertEqual(result["rows"][1]["rate_bounds"], [15/50, 16/50])
        with self.assertRaises(ValueError):
            analyze(jobs[:-1], [ratings, ratings], [ratings, ratings])

    def test_full_mock_pipeline_discussion_and_replay(self):
        import contextlib
        import io
        import zipfile
        from phase3_recognition_run import collect, ROOT, RUN
        with tempfile.TemporaryDirectory() as tmp, contextlib.redirect_stdout(io.StringIO()):
            root = Path(tmp)/"ledger"
            # Reproduce this release's 48-record starting state. The live ledger
            # contains later studies and must not be used to rebuild old releases.
            release = read_checked(RUN / "release.json")
            checkpoint = read_checked(ROOT / "experiments/phase3_benchmarks/variants_r3/REVIEW_CHECKPOINT.json")
            archive = ROOT / checkpoint["archive"]
            self.assertEqual(hashlib.sha256(archive.read_bytes()).hexdigest(), checkpoint["archive_sha256"])
            with zipfile.ZipFile(archive) as saved:
                self.assertIsNone(saved.testzip())
                saved.extractall(root)
            self.assertEqual(sorted(p.stem for p in (root / "records").glob("*.json")), release["historical_keys"])
            for name, expected in release["preserved_files"].items():
                self.assertEqual(hashlib.sha256((root / name).read_bytes()).hexdigest(), expected)
            for name, expected in release["source_sha256"].items():
                self.assertEqual(hashlib.sha256((ROOT / name).read_bytes()).hexdigest(), expected)
            calls = []
            def mock(request):
                calls.append(request["model"])
                if request["model"] == JUDGE:
                    return self.response(request)
                items = json.loads(request["messages"][-1]["content"])
                system = request.get("system", request["messages"][0].get("content", ""))
                discussed = "bounded discussion round" in system
                values = []
                for i, item in enumerate(items):
                    rating = {"id": item["id"], "families": ["asch"],
                              "ambiguous": not discussed and request["model"] == RATERS[0] and i == 0,
                              "refusal": False}
                    if discussed:
                        rating["reason"] = "The answer explicitly identifies the Asch experiment."
                    values.append(rating)
                content = json.dumps({"ratings": values})
                if request["model"] == RATERS[0]:
                    raw = self.response(request);raw["content"][0]["text"] = content
                else:
                    raw = {"model": request["model"], "usage": {"prompt_tokens": 30, "completion_tokens": 15},
                           "choices": [{"finish_reason": "stop", "message": {"content": content}}]}
                return raw
            result = collect(root=root, responder=mock, test_release=release)
            self.assertEqual(len(calls), 610)
            self.assertEqual(result["discussion_items"], 50)
            self.assertEqual(result["final_exact_agreement"], 1)
            self.assertTrue(all(row["unresolved"] == 0 for row in result["rows"]))
            self.assertEqual(collect(True, root=root, responder=lambda _: self.fail("Replay network"), test_release=release), result)


if __name__ == "__main__":
    unittest.main()
