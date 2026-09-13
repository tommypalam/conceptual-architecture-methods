from collections import Counter
from io import BytesIO
import json
import hashlib
from pathlib import Path
import sys
import tempfile
import unittest

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "code"))
from phase3_perception_check import MODEL, parse, render, request_for, reservation, stimuli, summary, run
from phase3_budget import digest


class PerceptionTests(unittest.TestCase):
    def test_write_once_collection_and_offline_replay(self):
        with tempfile.TemporaryDirectory() as root:
            jobs, answers = [], {}
            for row in stimuli()[:2]:
                png = render(row)
                path = Path(root) / (row["id"] + ".png")
                path.write_bytes(png)
                req = request_for(row, png)
                bound, cost = reservation(req)
                jobs.append({"slot": row["id"], "stimulus": row, "image": str(path),
                             "image_sha256": hashlib.sha256(png).hexdigest(), "request_sha256": digest(req),
                             "input_token_bound": bound, "reserved_nano": cost})
                answers[digest(req)] = row["correct"]
            def mock(req):
                return {"model": MODEL, "usage": {"prompt_tokens": 100, "completion_tokens": 8},
                        "choices": [{"finish_reason": "stop", "message": {"content": json.dumps({"choice": answers[digest(req)]})}}]}
            rows, count = run({"jobs": jobs}, Path(root) / "ledger", mock)
            self.assertEqual(count, 2)
            self.assertTrue(all(r["correct"] for r in rows))
            saved, count = run({"jobs": jobs}, Path(root) / "ledger", lambda _: self.fail("Unexpected call"), replay=True)
            self.assertEqual(count, 0)
            self.assertEqual(saved, rows)

    def test_balance_and_rendered_ground_truth(self):
        rows = stimuli()
        self.assertEqual(rows, stimuli())
        self.assertEqual(len({r["id"] for r in rows}), 36)
        self.assertEqual(Counter((r["kind"], r["correct"]) for r in rows),
                         Counter({(kind, choice): 6 for kind in ("line", "colour") for choice in "ABC"}))
        for row in rows:
            self.assertEqual(row["choices"].count(row["reference"]), 1)
            image = Image.open(BytesIO(render(row)))
            correct_x = (192, 320, 448)["ABC".index(row["correct"])]
            if row["kind"] == "line":
                for x, length in zip((64, 192, 320, 448), [row["reference"]] + row["choices"]):
                    self.assertEqual(sum(image.getpixel((x, y)) == (0, 0, 0) for y in range(65, 330)), length)
            else:
                self.assertEqual(image.getpixel((64, 180)), tuple(row["reference"]))
                self.assertEqual(image.getpixel((correct_x, 180)), tuple(row["reference"]))

    def test_request_keeps_truth_outside_text_and_budget_fits(self):
        total = 0
        for row in stimuli():
            request = request_for(row, render(row))
            text = request["messages"][1]["content"][0]["text"]
            self.assertNotIn(row["id"], text)
            self.assertNotIn("correct", text)
            self.assertEqual(request["messages"][1]["content"][1]["type"], "image_url")
            total += reservation(request)[1]
        self.assertLess(total, 200_000_000)

    def test_wrong_choice_is_retained_and_incomplete_set_cannot_pass(self):
        row = stimuli()[0]
        bound, _ = reservation(request_for(row, render(row)))
        raw = {"model": MODEL, "usage": {"prompt_tokens": 100, "completion_tokens": 8},
               "choices": [{"finish_reason": "stop", "message": {"content": '{"choice":"A"}'}}]}
        self.assertEqual(parse(raw, {"input_token_bound": bound}), "A")
        rows = [{"kind": "line", "correct": True} for _ in range(18)]
        self.assertTrue(summary(rows)["line"]["stimulus_gate_passed"])
        rows[0]["correct"] = False
        self.assertFalse(summary(rows)["line"]["stimulus_gate_passed"])
        self.assertFalse(summary(rows[1:])["line"]["stimulus_gate_passed"])
        raw["choices"][0]["message"]["content"] = json.dumps({"choice": "D"})
        with self.assertRaises(ValueError):
            parse(raw, {"input_token_bound": bound})


if __name__ == "__main__":
    unittest.main()
