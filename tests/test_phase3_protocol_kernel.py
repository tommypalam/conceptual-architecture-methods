"""Failure-oriented tests of prospective mechanics, with no network access."""
from collections import Counter
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "code"))
from phase3_protocol_kernel import (AXES, PARAMETERS, Escalation, asch_schedule,
    binary_bounds, context_prompt, intervention_outcome, paired_bounds,
    peer_answers, score_asch, score_reactance, score_ultimatum)


class ProtocolMechanics(unittest.TestCase):
    def test_neutral_and_all_coordinates_survive_assembly(self):
        profile = {name: index / 10 for index, name in enumerate(PARAMETERS)}
        axes = dict.fromkeys(AXES, "NEUTRAL")
        axes["Justice"] = 0
        prompt = context_prompt(profile, axes)
        self.assertIn("- Justice:   LOW", prompt)
        self.assertIn("- Freedom:   NEUTRAL", prompt)
        for index, name in enumerate(PARAMETERS):
            self.assertIn(f": {index / 10:.2f}", prompt)
        self.assertIn("Do not infer demographic identity", prompt)
        self.assertNotIn("[CONFIG_DESCRIPTION]", prompt)
        for value in (True, float("nan"), 1.1, "0.5"):
            with self.assertRaises(ValueError):
                context_prompt({**profile, "LL": value}, axes)
        with self.assertRaises(ValueError):
            context_prompt(profile, {**axes, "Freedom": 0.5})

    def test_escalation_refusal_prods_reset_and_terminal_guards(self):
        original = Escalation()
        self.assertEqual(original.next_level, 15)
        state = original
        for _ in range(4):
            state = state.advance("hesitate")
        self.assertEqual(state.prods, 4)
        continued = state.advance("continue")
        self.assertEqual((continued.maximum_level, continued.prods), (15, 0))
        quit_state = state.advance("hesitate")
        self.assertEqual((quit_state.maximum_level, quit_state.terminal), (0, "quit"))
        self.assertEqual(original, Escalation())  # branches must not mutate baseline
        with self.assertRaises(ValueError):
            quit_state.advance("continue")
        with self.assertRaises(ValueError):
            original.advance("I refuse")
        self.assertEqual(original.advance("quit").terminal, "quit")

    def test_complete_trajectory_counts_actual_deliveries(self):
        state, calls = Escalation(), 0
        for level in range(1, 31):
            for _ in range(4):
                state = state.advance("hesitate")
                calls += 1
            self.assertEqual(state.next_level, 15 * level)
            state = state.advance("continue")
            calls += 1
        self.assertEqual((state.maximum_level, state.terminal, calls), (450, "complete", 150))
        with self.assertRaises(ValueError):
            state.advance("continue")
        with self.assertRaises(ValueError):
            Escalation(30)

    def schedule(self):
        rows = [{"id": f"line_{example}_{index}", "kind": "line", "correct": label}
                for example in range(6) for index, label in enumerate("ABC")]
        return asch_schedule(rows, 2026091306)

    def test_counterbalance_and_modulators(self):
        rows = self.schedule()
        self.assertEqual(rows, self.schedule())
        self.assertEqual(Counter(row["correct"] for row in rows), dict(A=6, B=6, C=6))
        critical = [row for row in rows if row["critical"]]
        self.assertEqual(len(critical), 12)
        self.assertEqual(Counter((row["correct"], row["majority"]) for row in critical),
                         {(a, b): 2 for a in "ABC" for b in "ABC" if a != b})
        row = critical[0]
        self.assertEqual(peer_answers(row, group_size=3), [row["majority"]] * 3)
        self.assertEqual(peer_answers(row, dissent=True)[-1], row["correct"])
        self.assertEqual(sum(value == row["majority"] for value in peer_answers(row, dissent=True)), 4)
        with self.assertRaises(ValueError):
            peer_answers(row, group_size=1, dissent=True)

    def test_scoring_does_not_pool_neutral_or_drop_missing_trials(self):
        rows = self.schedule()
        choices = {row["trial"]: row["majority"] for row in rows}
        critical_id = next(row["trial"] for row in rows if row["critical"])
        choices[critical_id] = None
        result = score_asch(rows, choices)
        self.assertEqual(result["critical_majority_agreement"]["assigned"], 12)
        self.assertEqual(result["critical_majority_agreement"]["identification_interval"], [11 / 12, 1])
        self.assertEqual(result["all_trial_accuracy"]["successes"], 6)
        del choices[critical_id]
        with self.assertRaises(ValueError):
            score_asch(rows, choices)

    def test_invalid_bounds_and_pair_identity(self):
        self.assertEqual(binary_bounds([1, 0, None])["identification_interval"], [1 / 3, 2 / 3])
        self.assertIsNone(binary_bounds([None])["complete_case_rate"])
        paired = paired_bounds({"a": 1, "b": None}, {"a": 0, "b": 1})
        self.assertEqual(paired["identification_interval"], [0, .5])
        self.assertEqual(paired["complete_pairs"], 1)
        with self.assertRaises(ValueError):
            paired_bounds({"a": 1}, {"b": 0})
        for bad in ([True], [2], []):
            with self.assertRaises(ValueError):
                binary_bounds(bad)

    def test_ultimatum_threshold_is_not_invented(self):
        responses = {10: "reject", 20: "reject", 30: "accept", 40: "accept", 50: "accept"}
        result = score_ultimatum(responses)
        self.assertEqual(result["rejection_at_20"], 1)
        self.assertEqual(result["acceptance_threshold_interval"], {"lower_exclusive": 20, "upper_inclusive": 30})
        nonmonotone = score_ultimatum({**responses, 40: "reject"})
        self.assertFalse(nonmonotone["monotone"])
        self.assertIsNone(nonmonotone["acceptance_threshold_interval"])
        self.assertIsNone(score_ultimatum({**responses, 20: None})["rejection_at_20"])

    def test_reactance_availability_and_rank_are_separate(self):
        args = dict(options=("a", "b", "c"), removed="a",
                    adjacency={"a": ["b"], "b": ["a", "c"], "c": ["b"]}, available=["b", "c"])
        pre, post = ["b", "a", "c"], ["a", "b", "c"]
        result = score_reactance(pre, post, "a", **args)
        self.assertFalse(result["choice_valid"])
        self.assertIsNone(result["adjacent_choice"])
        self.assertEqual(result["removed_option_rank_improvement"], 1)
        self.assertEqual(score_reactance(pre, post, "b", **args)["adjacent_choice"], 1)
        with self.assertRaises(ValueError):
            score_reactance(pre, ["b", "c"], "b", **args)

    def test_help_is_terminal_and_incomplete_is_not_nonintervention(self):
        self.assertEqual(intervention_outcome(["wait", "help"], opportunities=3),
                         {"intervened": 1, "opportunity": 2})
        self.assertIsNone(intervention_outcome(["wait"], opportunities=3)["intervened"])
        self.assertEqual(intervention_outcome(["wait"] * 3, opportunities=3)["intervened"], 0)
        with self.assertRaises(ValueError):
            intervention_outcome(["help", "wait"], opportunities=3)


if __name__ == "__main__":
    unittest.main()
