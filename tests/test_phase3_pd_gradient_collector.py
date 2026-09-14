"""Offline checks for the pd_gradient_r1 collector.

No API calls. Verifies the stage gates, the parser, the unprofiled screen arm,
and that the analysis recovers a planted effect and reports none when there is
none. Establishes software behaviour, not scientific validity.
"""
from __future__ import annotations

import importlib.util
import random
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
CODE = ROOT / "code"
if str(CODE) not in sys.path:
    sys.path.insert(0, str(CODE))


def _load(name):
    spec = importlib.util.spec_from_file_location(name, CODE / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


G = _load("phase3_pd_gradient")
# Use the SAME module object the collector imported, so mutating a task in a
# test actually reaches the gate under test rather than a second copy.
T = G.T


def usable_screen():
    return {t: {"n_valid": G.SCREEN_N, "modal_share": 0.6, "usable": True,
                "reason": "usable", "near_ceiling": False} for t in T.TASK_IDS}


def synthetic_rows(gradient_on_p, seed=7):
    rng = random.Random(seed)
    preds = T.predictions()
    rows = []
    for task_id in T.TASK_IDS:
        label = preds[task_id]["process_label"]
        other = "BETA" if label == "ALPHA" else "ALPHA"
        for i in range(G.N_PER_TASK):
            pd_value = rng.betavariate(2.5, 2.0)
            if preds[task_id]["task_class"] == "P" and gradient_on_p:
                prob = 0.1 + 0.8 * pd_value
            else:
                prob = 0.5
            rows.append({"stage": "participant", "task": task_id, "agent_id": i + 1,
                         "pd": pd_value, "task_class": preds[task_id]["task_class"],
                         "process_label": label,
                         "choice": label if rng.random() < prob else other})
    return rows


class TestSystemPrompt:
    def test_screen_arm_has_no_profile_block(self):
        assert "# Your decision-making profile" not in G.system(None)

    def test_profiled_arm_has_profile_block(self):
        profile = {code: 0.42 for code in G.PARAMETERS}
        assert "# Your decision-making profile" in G.system(profile)

    def test_placeholder_values_never_reach_the_screen_prompt(self):
        """The unprofiled arm is built from a placeholder that must be stripped."""
        head = G.system(None).split("# Your task")[0]
        assert "50" not in head

    def test_profile_values_are_rendered(self):
        profile = {code: 0.42 for code in G.PARAMETERS}
        assert "42" in G.system(profile)


class TestJobConstruction:
    def test_screen_job_count(self):
        assert len(G.screen_jobs()) == G.SCREEN_N * len(T.TASK_IDS)

    def test_screen_jobs_cover_every_task_equally(self):
        counts = {}
        for job in G.screen_jobs():
            counts[job["cell"]["task"]] = counts.get(job["cell"]["task"], 0) + 1
        assert set(counts) == set(T.TASK_IDS)
        assert set(counts.values()) == {G.SCREEN_N}

    def test_every_job_reserves_cost_and_hashes(self):
        for job in G.screen_jobs()[:5]:
            assert job["reserved_nano"] > 0
            assert job["input_token_bound"] > 0
            assert job["slot"].startswith(G.STUDY)

    def test_label_order_is_balanced_within_a_task(self):
        """Presentation order must not align with the counterbalanced label."""
        firsts = [j["cell"]["index"] % 2 == 0 for j in G.screen_jobs()
                  if j["cell"]["task"] == "permit_sequence"]
        assert 0 < sum(firsts) < len(firsts)

    def test_body_lists_both_options(self):
        text = G.body("permit_sequence", True)
        assert "Option ALPHA:" in text and "Option BETA:" in text

    def test_body_order_flips(self):
        first = G.body("permit_sequence", True)
        second = G.body("permit_sequence", False)
        assert first.index("Option ALPHA:") < first.index("Option BETA:")
        assert second.index("Option BETA:") < second.index("Option ALPHA:")


class TestLeakageGate:
    def test_passes_on_the_authored_tasks(self):
        result = G.leakage_gate()
        assert result["forbidden_terms_found"] == 0
        assert result["counterbalanced"] is True
        assert result["task_content_sha256"] == T.content_hash()

    def test_blocks_a_leaking_task(self):
        original = T._TASKS["permit_sequence"]["situation"]
        try:
            T._TASKS["permit_sequence"]["situation"] = original + " Consider procedural dependence."
            with pytest.raises(Exception):
                G.leakage_gate()
        finally:
            T._TASKS["permit_sequence"]["situation"] = original
        G.leakage_gate()

    def test_blocks_a_broken_counterbalance(self):
        original = dict(T.PROCESS_LABEL)
        try:
            for task_id in T.TASK_IDS:
                T.PROCESS_LABEL[task_id] = "BETA"
            with pytest.raises(Exception):
                G.leakage_gate()
        finally:
            T.PROCESS_LABEL.update(original)
        G.leakage_gate()


class TestChoiceParser:
    @pytest.mark.parametrize("raw,expected", [
        ('{"choice":"ALPHA"}', "ALPHA"),
        ('{"choice":"BETA"}', "BETA"),
        ('{"choice":"X"}', None),
        ('{"choice":"alpha"}', None),
        ('{"choice":"ALPHA","extra":1}', None),
        ('{"pick":"ALPHA"}', None),
        ("not json", None),
        ("", None),
        ('{"choice":"ALPHA","choice":"BETA"}', None),
        ("[]", None),
    ])
    def test_parser(self, raw, expected):
        assert G.choice(raw) == expected


class TestScreenGate:
    def test_deterministic_task_is_rejected(self):
        rows = [{"task": "permit_sequence", "choice": "BETA"} for _ in range(25)]
        outcome = G.screen_outcome(rows)["permit_sequence"]
        assert outcome["modal_share"] == 1.0
        assert outcome["usable"] is False

    def test_dispersed_task_is_usable(self):
        rows = [{"task": "tender_award", "choice": "ALPHA" if i < 10 else "BETA"}
                for i in range(25)]
        outcome = G.screen_outcome(rows)["tender_award"]
        assert outcome["usable"] is True
        assert outcome["near_ceiling"] is False

    def test_near_ceiling_is_usable_but_flagged(self):
        rows = [{"task": "records_release", "choice": "BETA" if i < 23 else "ALPHA"}
                for i in range(25)]
        outcome = G.screen_outcome(rows)["records_release"]
        assert outcome["usable"] is True
        assert outcome["near_ceiling"] is True

    def test_no_valid_responses_is_not_usable(self):
        rows = [{"task": "grant_arithmetic", "choice": None} for _ in range(25)]
        assert G.screen_outcome(rows)["grant_arithmetic"]["usable"] is False

    def test_threshold_is_exactly_one(self):
        """The gate rejects only fully deterministic baselines."""
        assert G.SCREEN_REJECT_AT == 1.0


class TestAnalysis:
    def test_recovers_a_planted_effect(self):
        result = G.analyze(synthetic_rows(True), usable_screen(), G.N_PER_TASK)
        assert result["mean_r_class_P"] > 0.2
        assert abs(result["mean_r_class_N"]) < 0.15
        assert result["primary_contrast_P_minus_N"] > 0.2

    def test_reports_no_effect_when_there_is_none(self):
        result = G.analyze(synthetic_rows(False), usable_screen(), G.N_PER_TASK)
        assert abs(result["primary_contrast_P_minus_N"]) < 0.2

    def test_every_task_is_reported(self):
        result = G.analyze(synthetic_rows(True), usable_screen(), G.N_PER_TASK)
        assert set(result["tasks"]) == set(T.TASK_IDS)

    def test_class_and_prediction_carried_through(self):
        result = G.analyze(synthetic_rows(True), usable_screen(), G.N_PER_TASK)
        for task_id in T.CLASS_P:
            assert result["tasks"][task_id]["gradient_predicted"] is True
        for task_id in T.CLASS_N:
            assert result["tasks"][task_id]["gradient_predicted"] is False

    def test_missing_decisions_are_rejected(self):
        rows = synthetic_rows(True)[:-1]
        with pytest.raises(Exception):
            G.analyze(rows, usable_screen(), G.N_PER_TASK)

    def test_rejected_tasks_are_excluded_from_estimates(self):
        screen = usable_screen()
        screen["permit_sequence"]["usable"] = False
        result = G.analyze(synthetic_rows(True), screen, G.N_PER_TASK)
        assert "permit_sequence" not in result["tasks"]

    def test_makes_no_pass_or_moral_claim(self):
        result = G.analyze(synthetic_rows(True), usable_screen(), G.N_PER_TASK)
        assert result["phase3_pass"] is None
        assert result["moral_scores_assigned"] is False
        assert "not a success gate" in result["analysis_status"]

    def test_permutation_p_is_never_zero(self):
        result = G.analyze(synthetic_rows(True), usable_screen(), G.N_PER_TASK)
        for entry in result["tasks"].values():
            assert entry["perm_p"] > 0


class TestConfiguration:
    def test_sample_size_matches_the_protocol(self):
        assert G.N_PER_TASK == 120
        assert G.SCREEN_N == 25

    def test_cap_is_below_remaining_allowance(self):
        assert G.CAP == 1_000_000_000

    def test_seeds_are_distinct_and_recorded(self):
        assert len(set(G.SEEDS.values())) == 3

    def test_participant_model_is_the_cheaper_provider(self):
        assert G.PARTICIPANT == G.RATERS[1]
