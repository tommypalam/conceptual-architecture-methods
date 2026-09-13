from pathlib import Path
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "code"))
from phase3_repaired_candidates import repaired, PARENT
from phase3_budget import read_checked, digest


class RepairedCandidates(unittest.TestCase):
    def test_provenance_and_unchanged_fields_are_preserved(self):
        parent = read_checked(PARENT / "generation_result.json")
        result = repaired()
        self.assertEqual(result["parent_generation_result_sha256"], digest(parent))
        self.assertEqual(len(result["candidates"]), 5)
        for old, new in zip(parent["results"], result["candidates"]):
            self.assertEqual(new["parent_record_sha256"], old["record_sha256"])
            for field, value in old["parsed"]["stimulus"].items():
                if field not in new["changed_fields"]:
                    self.assertEqual(new["stimulus"][field], value)
                else:
                    self.assertEqual(new["changed_fields"][field]["before"], value)
        self.assertFalse(result["ready_for_population"])

    def test_controls_do_not_collapse_and_proposer_is_free(self):
        rows = {row["benchmark"]: row["stimulus"] for row in repaired()["candidates"]}
        self.assertIn("present beside", rows["milgram"]["mod_base"])
        self.assertIn("not beside", rows["milgram"]["mod_remote"])
        self.assertNotIn("{offer}", rows["ultimatum"]["proposer"])
        self.assertIn("{offer}", rows["ultimatum"]["responder"])
        self.assertIn("no other observer", rows["bystander"]["setup_alone"])
        self.assertIn("three other observers", rows["bystander"]["setup_group"])

    def test_wrong_domain_placeholder_in_preserved_field_is_rejected(self):
        parent = read_checked(PARENT / "generation_result.json")
        parent["results"][0]["parsed"]["stimulus"]["feedback_early"] = "Bad {removed}"
        with patch("phase3_repaired_candidates.read_checked", return_value=parent):
            with self.assertRaisesRegex(ValueError, "placeholder"):
                repaired()


if __name__ == "__main__":
    unittest.main()
