"""Regression checks for scientific state, accounting and restart safety."""
import asyncio
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "code"))
from phase2_confirmation_design import (make_design, evidence_items, initial_state, advance, resolve,
                                held_items, system_prompt, group_messages, parse, fields, LABELS, run_group)
from phase2_confirmation_transport import (Ledger, StopRun, digest, read_record, cost_nano,
                                   write_once, mock_response, MODEL)
from analyze_phase2_pilot import contrast, wilson
from analyze_phase2_confirmation import paired, holm
from scipy.stats import multinomial


def response(vote, **fields_):
    return {"vote": vote, "status": "ok" if vote else "parse_failure",
            "fields": {"REASONING": "Test", **fields_}, "text": "Test",
            "evidence_text": "Test " + fields_.get("SHARE", "")}


class StateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.population, cls.groups = make_design()

    def group(self, problem):
        return next(g for g in self.groups if g["problem"] == problem)

    def test_population_and_membership(self):
        self.assertEqual(self.population.n, 400)
        for problem, n in [("C1", 5), ("C2", 6), ("C3", 4)]:
            groups = [g for g in self.groups if g["problem"] == problem]
            ids = [a for g in groups for a in g["agent_ids"]]
            self.assertEqual(len(ids), 20 * n)
            self.assertEqual(len(set(ids)), len(ids))
            self.assertTrue(all(len(g["conditions"]) == 5 for g in groups))

    def test_neutral_and_roles_in_every_arm(self):
        agent = self.population.agents[0]
        neutral = system_prompt(agent, "neutral", "B", role="CEO")
        self.assertIn("balanced on every", neutral)
        self.assertNotIn("Legitimacy Locus", neutral)
        self.assertNotIn("Authority: HIGH", neutral)
        self.assertIn("CEO", neutral)
        for arm in ("E", "U"):
            p = system_prompt(agent, "00100", arm, role="CEO")
            self.assertEqual("Legitimacy Locus" in p, arm == "E")
            self.assertIn("CEO", p)

    def test_missing_votes_cannot_create_consensus_or_tie(self):
        for problem in ("C1", "C2", "C3"):
            group = self.group(problem)
            state = initial_state(group)
            responses = {a: response(None) for a in group["agent_ids"]}
            responses[group["agent_ids"][0]] = response(LABELS[problem][0])
            self.assertFalse(advance(state, responses, 1))
            self.assertIsNone(resolve(state)["outcome"])
            self.assertFalse(resolve(state)["tie_break"])

    def test_valid_consensus_and_ceo_excluded(self):
        group = self.group("C1")
        state = initial_state(group)
        self.assertTrue(advance(state, {a: response("PACKAGE_A") for a in group["agent_ids"]}, 1))
        self.assertTrue(resolve(state)["consensus"])
        group = self.group("C2")
        state = initial_state(group)
        advance(state, {a: response("REJECT" if a == group["ceo"] else "APPROVE") for a in group["agent_ids"]}, 5)
        self.assertEqual(resolve(state)["final_tally"]["APPROVE"], 5)
        self.assertEqual(resolve(state)["final_tally"]["REJECT"], 0)

    def test_real_tie_only_and_deterministic(self):
        group = self.group("C3")
        state = initial_state(group)
        advance(state, {a: response("CONTINUE" if i < 2 else "PIVOT") for i, a in enumerate(group["agent_ids"])}, 6)
        self.assertTrue(resolve(state)["tie_break"])
        self.assertEqual(resolve(state), resolve(state))

    def test_evidence_persistence_and_barrier(self):
        group = self.group("C3")
        item = evidence_items()[0].item_id
        owners = [a for a in group["agent_ids"] if item in held_items(group, a, 1)]
        nonowner = next(a for a in group["agent_ids"] if a not in owners)
        self.assertIn(item, held_items(group, owners[0], 6))
        resp = {a: response("CONTINUE", SHARE=item if a in (owners[0], nonowner) else "NONE") for a in group["agent_ids"]}
        one, two = initial_state(group), initial_state(group)
        advance(one, resp, 1)
        advance(two, dict(reversed(list(resp.items()))), 1)
        self.assertEqual(one, two)
        self.assertIn(item, next(a for a in one["audit"] if a["agent"] == nonowner)["unavailable_citations"])
        self.assertIn(item, one["public_evidence"])
        agent = next(a for a in self.population.agents if a.agent_id == nonowner)
        prompt = group_messages(agent, "00100", "E", group, one, 2)[1]["content"]
        self.assertIn(evidence_items()[0].content, prompt)
        self.assertNotIn('"polarity"', prompt)

    def test_amendment_visible_then_adopted(self):
        group = self.group("C2")
        state = initial_state(group)
        author = next(a for a in group["agent_ids"] if a != group["ceo"])
        pid = f"R1A{author}"
        resp = {a: response("APPROVE") for a in group["agent_ids"]}
        resp[author] = response("APPROVE", ACTION="amend", AMENDMENT="Publish the process rationale.")
        resp[group["ceo"]] = response("APPROVE", ADOPT=pid)
        advance(state, resp, 1)
        self.assertIn(pid, state["proposals"])
        self.assertNotIn(pid, state["adopted"])
        advance(state, {a: response("APPROVE", ADOPT=pid if a == group["ceo"] else "NONE") for a in group["agent_ids"]}, 2)
        self.assertIn(pid, state["adopted"])

    def test_parser_fields_and_truncation(self):
        f, error = fields("REASONING: a reason\nVOTE: CONTINUE")
        self.assertEqual(f["REASONING"], "a reason")
        self.assertIsNone(error)
        self.assertEqual(fields("VOTE: CONTINUE\nVOTE: PIVOT")[1], "duplicate_field")
        raw = mock_response({}, {"stage": "complex", "labels": ["CONTINUE", "PIVOT"]})
        raw["choices"][0]["finish_reason"] = "length"
        self.assertIsNone(parse({"response": raw}, ("CONTINUE", "PIVOT"))["vote"])


class LedgerTests(unittest.IsolatedAsyncioTestCase):
    async def test_group_replay_after_json_roundtrip(self):
        with tempfile.TemporaryDirectory() as d:
            pop, groups = make_design()
            group = next(g for g in groups if g["problem"] == "C3")
            ledger = Ledger(d, "frozen", mock=True)
            await run_group(ledger, pop, group, "00100", "E")
            before = ledger.n_new
            await run_group(ledger, pop, json.loads(json.dumps(group)), "00100", "E")
            self.assertEqual(ledger.n_new, before)
            ledger.close()


class ConfirmationTests(unittest.TestCase):
    def test_no_simple_prompt_change(self):
        from phase2_pilot_design import simple_messages as old
        from phase2_confirmation_design import simple_messages as new, CONDITIONS
        pop, _ = make_design()
        for p in ("S1", "S2", "S3"):
            for c, arm in CONDITIONS:
                self.assertEqual(old(pop.agents[0], c, arm, p), new(pop.agents[0], c, arm, p))

    def test_bad_vote_does_not_drop_authenticated_evidence(self):
        pop, groups = make_design()
        group = next(g for g in groups if g["problem"] == "C3")
        owner = next(a for a in group["agent_ids"] if held_items(group, a, 1))
        item = sorted(held_items(group, owner, 1))[0]
        raw = mock_response({}, {"stage": "complex", "labels": LABELS["C3"]})
        raw["choices"][0]["message"]["content"] = f"SHARE: {item}\nREASONING: Consider {item}.\nVOTE: UNCERTAIN"
        parsed = parse({"response": raw}, LABELS["C3"])
        self.assertIsNone(parsed["vote"])
        state = initial_state(group)
        advance(state, {owner: parsed}, 1)
        self.assertIn(item, state["public_evidence"])
        self.assertEqual(state["tallies"][0]["missing"], 1)

    def test_refusal_cannot_disclose_or_adopt(self):
        raw = mock_response({}, {"stage": "complex", "labels": LABELS["C3"]})
        raw["choices"][0]["message"].update(content="SHARE: E01\nREASONING: E01\nVOTE: CONTINUE", refusal="refused")
        parsed = parse({"response": raw}, LABELS["C3"])
        self.assertEqual(parsed["fields"], {})
        self.assertIsNone(parsed["evidence_text"])

    def test_reference_only_is_not_new_proposal_and_prose_is_not_adoption(self):
        pop, groups = make_design()
        group = next(g for g in groups if g["problem"] == "C2")
        state = initial_state(group)
        author = group["ceo"]
        state["proposals"]["R1A9"] = "A real safeguard."
        advance(state, {author: response(None, ACTION="amend", AMENDMENT="R1A9", ADOPT="I might adopt R1A9")}, 2)
        self.assertEqual(len(state["proposals"]), 1)
        self.assertEqual(state["adopted"], [])
        advance(state, {author: response(None, ADOPT="R1A9")}, 3)
        self.assertEqual(state["adopted"], ["R1A9"])
        agent = next(a for a in pop.agents if a.agent_id == author)
        prompt = group_messages(agent, "00100", "U", group, state, 4)[1]["content"]
        self.assertIn('"adopted_amendments": {"R1A9": "A real safeguard."}', prompt)

    def test_exact_effect_missing_and_holm(self):
        a = paired([1]*20, [0]*20, 20)
        self.assertEqual(a["difference"], 1.)
        self.assertLess(a["primary_p"], .00001)
        b = paired([1, None], [0, 1], 2)
        self.assertEqual(b["primary_p"], 1.)
        self.assertEqual(b["missing_assignment_bounds"], [0., 1.])
        rows = [{"primary_p": p} for p in [.01, .04, .001]]
        holm(rows)
        self.assertEqual([r["holm_p"] for r in rows], [.02, .04, .003])

    def test_non_degenerate_ceilings_and_interval_symmetry(self):
        zero = paired([1]*400, [1]*400, 400)
        self.assertLess(zero["ci95"][0], 0.)
        self.assertGreater(zero["ci95"][1], 0.)
        self.assertLess(zero["family_ci95"][0], zero["ci95"][0])
        a, b = paired([1, 1, 0], [0, 1, 0], 3), paired([0, 1, 0], [1, 1, 0], 3)
        self.assertAlmostEqual(a["ci95"][0], -b["ci95"][1])

    def test_finite_sample_interval_coverage_by_enumeration(self):
        n = 8
        intervals = {}
        for n10 in range(n+1):
            for n01 in range(n-n10+1):
                x = [1]*n10 + [0]*n01 + [0]*(n-n10-n01)
                y = [0]*n10 + [1]*n01 + [0]*(n-n10-n01)
                intervals[n10, n01] = paired(x, y, n)["ci95"]
        for p10, p01 in [(0., 0.), (.01, .01), (.2, .1), (.5, .5), (.9, .05), (1., 0.)]:
            covered = 0.
            for (n10, n01), (lo, hi) in intervals.items():
                if lo <= p10-p01 <= hi:
                    covered += multinomial.pmf([n10, n01, n-n10-n01], n, [p10, p01, 1-p10-p01])
            self.assertGreaterEqual(covered, .95-1e-12)

class TransportTests(unittest.IsolatedAsyncioTestCase):
    async def test_replay_no_duplicate_and_changed_request_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            meta = {"stage": "simple", "labels": ["A", "B"]}
            messages = [{"role": "user", "content": "Long test " * 200}]
            ledger = Ledger(d, "frozen", mock=True)
            first = await ledger.complete(["slot"], messages, 1, meta)
            charged = ledger.charged
            ledger.close()
            ledger = Ledger(d, "frozen", mock=True)
            again = await ledger.complete(["slot"], messages, 1, meta)
            self.assertEqual(first, again)
            self.assertEqual(ledger.n_new, 0)
            self.assertEqual(ledger.charged, charged)
            with self.assertRaises(StopRun):
                await ledger.complete(["slot"], messages, 2, meta)
            ledger.close()

    async def test_budget_reserves_before_dispatch(self):
        with tempfile.TemporaryDirectory() as d:
            ledger = Ledger(d, "frozen", mock=True)
            ledger.cap = 1
            with self.assertRaises(StopRun):
                await ledger.complete(["slot"], [{"role": "user", "content": "test"}], 1, {"labels": ["A", "B"], "stage": "simple"})
            self.assertFalse(list((Path(d) / "dispatches").glob("*.json")))
            ledger.close()

    async def test_pending_corruption_and_lock_block_restart(self):
        with tempfile.TemporaryDirectory() as d:
            ledger = Ledger(d, "frozen", mock=True)
            with self.assertRaises(FileExistsError):
                Ledger(d, "frozen", mock=True)
            ledger.close()
            write_once(Path(d) / "dispatches" / "pending.json", {"manifest_hash": "frozen", "mock": True})
            with self.assertRaises(StopRun):
                Ledger(d, "frozen", mock=True)
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "r.json"
            write_once(path, {"a": 1})
            data = json.loads(path.read_text())
            data["payload"]["a"] = 2
            path.write_text(json.dumps(data))
            with self.assertRaises(ValueError):
                read_record(path)

    async def test_error_keeps_reserve_and_halts(self):
        def broken(*args):
            raise TimeoutError("not saved")
        with tempfile.TemporaryDirectory() as d:
            ledger = Ledger(d, "frozen", mock=True, responder=broken)
            result = await ledger.complete(["one"], [{"role": "user", "content": "test"}], 1, {"stage": "simple", "labels": ["A", "B"]})
            self.assertFalse(result["usage_known"])
            self.assertGreater(result["charged_nano"], 0)
            self.assertTrue(ledger.halted)
            with self.assertRaises(StopRun):
                await ledger.complete(["two"], [], 2, {})
            ledger.close()
            ledger = Ledger(d, "frozen", mock=True)
            self.assertTrue(ledger.halted)
            ledger.close()
