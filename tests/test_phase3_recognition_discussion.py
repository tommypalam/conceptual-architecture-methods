from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "code"))
from phase3_recognition_discussion import discussion_request, discussion_bound, RATERS, RUBRIC, DISCUSSION


class DiscussionPreparation(unittest.TestCase):
    def item(self, i=0):
        key = f"{i:016x}"
        return {"id": key, "answer": "This resembles the Asch conformity experiment.",
                "own_rating": {"id": key, "families": ["asch"], "ambiguous": False, "refusal": False},
                "other_rating": {"id": key, "families": [], "ambiguous": True, "refusal": False}}

    def test_original_positions_preserved_and_bounded(self):
        import json
        for model in RATERS:
            items = [self.item(i) for i in range(10)]
            request = discussion_request(model, items)
            self.assertEqual(json.loads(request["messages"][-1]["content"]), items)
            bound, cost = discussion_bound(model)
            self.assertGreater(bound, len((RUBRIC + DISCUSSION + request["messages"][-1]["content"]).encode()))
            self.assertGreater(cost, 0)

    def test_rejects_duplicate_long_id_invalid_labels_and_truncation(self):
        for items in ([self.item(), self.item()], []):
            with self.assertRaises(ValueError):
                discussion_request(RATERS[0], items)
        for field, value in (("id", "x" * 100), ("answer", "a" * 1025)):
            item = self.item()
            item[field] = value
            with self.assertRaises(ValueError):
                discussion_request(RATERS[0], [item])
        item = self.item()
        item["other_rating"]["families"] = ["unknown"]
        with self.assertRaises(ValueError):
            discussion_request(RATERS[0], [item])

    def test_partial_batch_and_distinct_raters(self):
        for model in RATERS:
            request = discussion_request(model, [self.item()])
            self.assertEqual(request["model"], model)
        with self.assertRaises(ValueError):
            discussion_request("different-model", [self.item()])


if __name__ == "__main__":
    unittest.main()
