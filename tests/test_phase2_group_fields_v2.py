import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "code"))
from phase2_group_fields_v2 import parse_group_fields, authenticate_disclosures


class IndependentFieldTests(unittest.TestCase):
    def test_inline_vote_does_not_pollute_reason(self):
        r = parse_group_fields("ACTION: argue\nSHARE: E03\nREASONING: Consider E03. VOTE: CONTINUE", ("CONTINUE", "PIVOT"))
        self.assertEqual(r["vote"], "CONTINUE")
        self.assertEqual(r["fields"]["REASONING"], "Consider E03.")

    def test_bad_vote_retains_legitimate_evidence(self):
        r = parse_group_fields("ACTION: share\nSHARE: E03, E99\nREASONING: Consider E03.\nVOTE: UNSURE", ("CONTINUE", "PIVOT"))
        self.assertIsNone(r["vote"])
        self.assertEqual(authenticate_disclosures(r, {"E03"}, set()), {"authenticated": ["E03"], "unavailable": ["E99"]})

    def test_ambiguous_vote_never_chosen(self):
        r = parse_group_fields("REASONING: Consider E01.\nVOTE: PIVOT\nVOTE: CONTINUE", ("CONTINUE", "PIVOT"))
        self.assertIsNone(r["vote"])
        self.assertEqual(authenticate_disclosures(r, {"E01"}, set())["authenticated"], ["E01"])

    def test_truncated_generation_has_no_actions(self):
        r = parse_group_fields("SHARE: E03\nREASONING: Partial\nVOTE: CONTINUE", ("CONTINUE", "PIVOT"), finish_reason="length")
        self.assertIsNone(r["vote"])
        self.assertIsNone(r["evidence_text"])

    def test_duplicate_reason_does_not_discard_separate_share(self):
        r = parse_group_fields("SHARE: E02\nREASONING: One\nREASONING: Two\nVOTE: CONTINUE", ("CONTINUE", "PIVOT"))
        self.assertEqual(r["field_errors"]["REASONING"], "duplicate_field")
        self.assertEqual(r["evidence_text"], "E02")


if __name__ == "__main__":
    unittest.main()
