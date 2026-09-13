"""Verify prospective stimuli against causal and accounting invariants."""
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "code"))
from phase3_canonical_stimuli import (CONTEXTS, PRODS, ADJACENCY, OPTIONS, REACTANCE_SETUP,
    escalation_turn, asch_turn, ultimatum_turn, bystander_setup, bystander_turn,
    reactance_turn, call_inventory)
from phase3_protocol_kernel import Escalation, score_reactance


class CanonicalStimuli(unittest.TestCase):
    def test_contexts_change_exactly_one_axis(self):
        targets = dict(milgram="Authority", asch="Loyalty", ultimatum="Justice", bystander="Care", reactance="Freedom")
        for name, (high, low) in CONTEXTS.items():
            self.assertEqual([axis for axis in high if high[axis] != low[axis]], [targets[name]])
            self.assertFalse(any(value == .5 for value in high.values()))
        self.assertEqual(CONTEXTS["ultimatum"][0]["Justice"], 0)
        self.assertEqual(CONTEXTS["reactance"][1]["Authority"], 1)

    def test_feedback_timing_and_prods_preserve_administration(self):
        self.assertNotIn("pounded", escalation_turn(Escalation(19)))
        self.assertIn("300-volt", escalation_turn(Escalation(20)))
        self.assertIn("315-volt", escalation_turn(Escalation(21)))
        self.assertIn("No further sounds", escalation_turn(Escalation(22)))
        state = Escalation(3)
        self.assertIn("correct-answer trial", escalation_turn(state))
        for prod in PRODS:
            state = state.advance("hesitate")
            text = escalation_turn(state)
            self.assertIn(prod, text)
            self.assertNotIn("correct-answer trial", text)
            self.assertIn("Next proposed administration: 60 volts", text)
        with self.assertRaises(ValueError):
            escalation_turn(state.advance("quit"))

    def test_visibility_and_peers_do_not_leak_answer_key(self):
        trial = dict(trial=3, majority="B", correct="A", critical=True, id="secret_truth_A")
        public = asch_turn(trial)
        private = asch_turn(trial, private=True)
        self.assertIn("shown to all", public)
        self.assertIn("not be shown", private)
        self.assertNotIn("secret_truth", public)
        self.assertNotIn("correct", public.lower())
        self.assertNotIn("critical", public.lower())
        self.assertEqual(public.count(": B"), 5)
        self.assertEqual(asch_turn(trial, dissent=True).count(": B"), 4)

    def test_allocation_role_and_offer_semantics(self):
        proposer = ultimatum_turn("proposer")
        self.assertIn('"offer_to_other"', proposer)
        self.assertIn("keeping the remainder", proposer)
        for offer in (10, 20, 30, 40, 50):
            text = ultimatum_turn("responder", offer)
            self.assertIn(f"offered {offer} units", text)
            self.assertIn(f"keeps {100-offer}", text)
        with self.assertRaises(ValueError):
            ultimatum_turn("responder", True)

    def test_presence_danger_and_opportunities_are_explicit(self):
        alone = bystander_setup(others=0, danger="standard")
        group = bystander_setup(others=3, danger="standard")
        self.assertIn("only other participant", alone)
        self.assertIn("Three other participants", group)
        for text in (alone, group):
            self.assertIn("three decision opportunities", text)
            self.assertIn("cannot see", text)
            self.assertNotIn("seconds", text)
        self.assertNotEqual(bystander_turn(1, danger="standard"), bystander_turn(1, danger="elevated"))
        with self.assertRaises(ValueError):
            bystander_turn(4, danger="standard")

    def test_restriction_controls_match_availability_and_graph_is_fixed(self):
        rank = ["C", "A", "E", "B", "D"]
        social = reactance_turn(rank, arm="social_removal")
        nonsocial = reactance_turn(rank, arm="nonsocial_removal")
        self.assertIn("prohibits you", social)
        self.assertIn("imposed no prohibition", nonsocial)
        self.assertEqual(social.split("Available choices:")[1], nonsocial.split("Available choices:")[1])
        self.assertIn("B, C, D, E", social)
        self.assertIn("A, B, C, D, E", reactance_turn(rank, arm="unrestricted"))
        self.assertIn("ALL FIVE", social)
        result = score_reactance(rank, rank, "B", options=OPTIONS, removed="A", adjacency=ADJACENCY, available=["B", "C", "D", "E"])
        self.assertEqual(result["adjacent_choice"], 1)
        self.assertNotIn("adjacen", REACTANCE_SETUP.lower())

    def test_call_units_include_all_branches_roles_and_prods(self):
        report = call_inventory(10)
        self.assertEqual(report["worst_case_total"], 7600)
        self.assertEqual(report["worst_case_by_benchmark"]["milgram"], 6000)
        self.assertEqual(report["worst_case_by_benchmark"]["bystander"], 480)
        self.assertEqual(call_inventory(200)["worst_case_total"], 152000)
        self.assertFalse(report["ready_to_dispatch"])


if __name__ == "__main__":
    unittest.main()
