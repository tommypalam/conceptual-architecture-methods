import base64
import itertools
import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "code"))
import phase3_recognition_stimuli as s
import phase3_recognition as r


class RecognitionAssembly(unittest.TestCase):
    def test_all_1200_escalation_states_reconstruct_exactly(self):
        for form in ("canonical", "alternative"):
            recipe = s.escalation_recipe(form)
            for d, p, m in itertools.product(range(30), range(5), range(4)):
                self.assertEqual(s.expand_recipe(recipe, d, p, m),
                                 s.escalation_text(form, s.Escalation(d, p), s.MODS[m]))

    def test_all_perception_turns_and_images_match(self):
        for form in ("canonical", "alternative"):
            blocks = s.task_content("asch", form)
            images = [b for b in blocks if b["type"] == "image"]
            rows = s.image_schedule(form)
            self.assertEqual(len(images), 18)
            self.assertEqual([base64.b64decode(b["source"]["data"]) for b in images], [x["png"] for x in rows])
            packed = json.loads(blocks[-1]["text"].split("\n", 1)[1])
            actual = s.unpack_lines(packed)
            expected = []
            for size, dissent, private in ((5, False, False), (5, True, False), (5, False, True),
                                          (1, False, False), (2, False, False), (3, False, False)):
                for row in rows:
                    expected.append(s.c.asch_turn(row, group_size=size, dissent=dissent, private=private)
                                    if form == "canonical" else s.alternative_asch(row, size, dissent, private))
            self.assertEqual(actual, expected)

    def test_recognition_projection_excludes_keys_and_metadata(self):
        forbidden = ("milgram", "asch", "ultimatum", "bystander", "reactance", "critical", "correct\":",
                     "image_sha256", "reference\":", "configuration", "profile", "LL_VALUE", "high-rate", "low-rate")
        for name in s.c.BENCHMARKS:
            for form in ("canonical", "alternative"):
                request = r.probe_request(name, form)
                text = "\n".join(b["text"] for b in request["messages"][0]["content"] if b["type"] == "text").lower()
                for word in forbidden:
                    self.assertNotIn(word.lower(), text, (name, form, word))
                self.assertEqual(request["messages"][0]["content"][-1]["text"], r.QUESTION)
                self.assertNotIn("{removed}", text)
                self.assertNotIn("{offer}", text)

    def test_all_reactance_initial_rankings_same_branch_contract(self):
        for form in ("canonical", "alternative"):
            recipe = json.loads(s.task_content("reactance", form)[0]["text"])
            fn = s.c.reactance_turn if form == "canonical" else s.alternative_reactance
            for ranking in itertools.permutations("ABCDE"):
                for index, arm in enumerate(s.ARMS):
                    self.assertEqual(recipe["cases"][ranking[1]][index], fn(ranking, arm=arm))
                    text = fn(ranking, arm=arm)
                    available = text.split("Available choices: ")[1].split(".")[0]
                    self.assertEqual(ranking[1] in available, arm == "unrestricted")

    def test_roles_events_and_terminal_contract(self):
        for form in ("canonical", "alternative"):
            allocation = json.loads(s.task_content("ultimatum", form)[0]["text"])["tasks"]
            self.assertEqual(len(allocation), 6)
            self.assertIn('"offer_to_other"', allocation[0])
            for offer, text in zip((10, 20, 30, 40, 50), allocation[1:]):
                self.assertIn(str(offer), text)
                self.assertIn(str(100-offer), text)
                self.assertNotIn('"offer_to_other"', text)
            cases = json.loads(s.task_content("bystander", form)[0]["text"])["cases"]
            self.assertEqual(len(cases), 4)
            self.assertTrue(all(len(case["turns"]) == 3 for case in cases))
        state = s.Escalation()
        for _ in range(5):
            state = state.advance("hesitate")
        self.assertEqual(state.terminal, "quit")
        with self.assertRaises(ValueError):
            s.alternative_escalation(state)

    def test_coding_is_blind_and_bounds_cover_escaping(self):
        for model in r.RATERS:
            items = [{"id": f"{i:016x}", "answer": 'Perhaps Asch: a wrong majority influences perception. "Yes".'} for i in range(10)]
            request = r.rater_request(model, items)
            bound, charge = r.coding_bound(model)
            self.assertGreater(bound, len(r.canonical(request)))
            self.assertGreater(charge, 0)
            user = request["messages"][-1]["content"]
            self.assertEqual(json.loads(user), items)
            self.assertNotIn("benchmark", user)
            self.assertNotIn("canonical", user)
        self.assertFalse(r.valid_probe_text(""))
        self.assertFalse(r.valid_probe_text("a" * 1025))
        self.assertFalse(r.valid_probe_text("bad\x00"))
        self.assertTrue(r.valid_probe_text("I cannot assess this."))  # Rater, not parser, determines refusal.


if __name__ == "__main__":
    unittest.main()
