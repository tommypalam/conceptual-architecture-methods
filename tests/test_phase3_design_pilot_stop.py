import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/"code"))
from verify_phase3_design_pilot_stop import review_text


class StoppedReview(unittest.TestCase):
    def test_complete_fence_preserves_fields(self):
        value = {"verdict": "revise", "blocking_issues": ["Unclear role schedule."], "limits": []}
        self.assertEqual(review_text("```json\n"+json.dumps(value)+"\n```"), value)

    def test_no_surrounding_prose_or_incomplete_json(self):
        for text in ('before\n```json\n{}\n```', '```json\n{}\n```\nafter', '```json\n{\n```', '{"verdict":"revise"}'):
            with self.assertRaises(ValueError): review_text(text)

    def test_original_semantic_schema_remains_strict(self):
        value = {"verdict": "accept", "blocking_issues": ["Still wrong."], "limits": []}
        with self.assertRaises(ValueError): review_text("```json\n"+json.dumps(value)+"\n```")


if __name__ == "__main__": unittest.main()
