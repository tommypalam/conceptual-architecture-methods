"""Offline checks for the prospective PD gradient test (pd_gradient_r2).

No API calls. Locks the design invariants that make the study interpretable:
class assignment, counterbalancing, absence of hypothesis leakage, and the
power/calibration figures quoted in the protocol.

These checks establish design and software properties, not scientific validity.
"""
from __future__ import annotations

import importlib.util
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
PROTOCOL = ROOT / "experiments" / "phase3_benchmarks" / "pd_gradient_r2" / "PROTOCOL.md"


def _load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "code" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


tasks = _load("phase3_pd_gradient_tasks_r2")
power = _load("phase3_pd_gradient_power")

DEPARTURE_MARKERS = (
    "without the survey sign-off", "without applying the deadline",
    "without the two-person board", "departing from",
    "without the independent recheck",
)


class TestTaskStructure:
    def test_six_tasks_three_per_class(self):
        assert len(tasks.TASK_IDS) == 6
        assert len(tasks.CLASS_P) == 3
        assert len(tasks.CLASS_N) == 3
        assert not set(tasks.CLASS_P) & set(tasks.CLASS_N)

    def test_every_task_has_exactly_two_options(self):
        for task_id in tasks.TASK_IDS:
            options = tasks.labelled_options(task_id)
            assert set(options) == {"ALPHA", "BETA"}
            assert all(text.strip() for text in options.values())

    def test_options_are_distinct(self):
        for task_id in tasks.TASK_IDS:
            options = tasks.labelled_options(task_id)
            assert options["ALPHA"] != options["BETA"]

    def test_unknown_task_rejected(self):
        with pytest.raises(ValueError):
            tasks.task("not_a_task")

    def test_task_returns_a_copy(self):
        first = tasks.task("permit_sequence")
        first["situation"] = "mutated"
        assert tasks.task("permit_sequence")["situation"] != "mutated"


class TestClassAssignment:
    def test_class_p_predicts_the_process_option(self):
        preds = tasks.predictions()
        for task_id in tasks.CLASS_P:
            entry = preds[task_id]
            assert entry["gradient_predicted"] is True
            assert entry["pd_predicts"] == entry["process_label"]
            assert entry["outcome_label"] != entry["process_label"]

    def test_class_n_predicts_no_gradient(self):
        preds = tasks.predictions()
        for task_id in tasks.CLASS_N:
            entry = preds[task_id]
            assert entry["gradient_predicted"] is False
            assert entry["pd_predicts"] is None

    def test_process_label_maps_to_process_respecting_text(self):
        """The labelled process option must never be the rule-departing one."""
        preds = tasks.predictions()
        for task_id in tasks.TASK_IDS:
            options = tasks.labelled_options(task_id)
            process_text = options[preds[task_id]["process_label"]].lower()
            for marker in DEPARTURE_MARKERS:
                assert marker not in process_text, f"{task_id}: process option departs"

    def test_non_process_option_is_the_departing_one(self):
        preds = tasks.predictions()
        for task_id in tasks.TASK_IDS:
            options = tasks.labelled_options(task_id)
            other_label = "BETA" if preds[task_id]["process_label"] == "ALPHA" else "ALPHA"
            other = options[other_label].lower()
            assert any(m in other for m in DEPARTURE_MARKERS), f"{task_id}: no departure"


class TestCounterbalancing:
    def test_process_label_is_balanced_overall(self):
        """A fixed label must not encode the prediction."""
        labels = [tasks.PROCESS_LABEL[t] for t in tasks.TASK_IDS]
        assert labels.count("ALPHA") == 3
        assert labels.count("BETA") == 3

    def test_neither_class_is_label_constant(self):
        """Class and label must not be confounded either."""
        for class_ids in (tasks.CLASS_P, tasks.CLASS_N):
            labels = {tasks.PROCESS_LABEL[t] for t in class_ids}
            assert len(labels) == 2, "class is label-constant"

    def test_every_task_has_a_declared_label(self):
        assert set(tasks.PROCESS_LABEL) == set(tasks.TASK_IDS)


class TestNoLeakage:
    def test_no_forbidden_terms_in_participant_text(self):
        for task_id in tasks.TASK_IDS:
            assert tasks.audit_leakage(task_id) == [], task_id

    def test_parameter_names_absent(self):
        """No coordinate name may appear in anything a participant sees."""
        names = ("procedural dependence", "moral scope", "legitimacy locus",
                 "affective weighting", "tolerance for asymmetry")
        for task_id in tasks.TASK_IDS:
            blob = (tasks.participant_text(task_id) + " "
                    + " ".join(tasks.labelled_options(task_id).values())).lower()
            for name in names:
                assert name not in blob

    def test_labels_carry_no_valence(self):
        """Labels must be neutral tokens, not words implying a better option."""
        for task_id in tasks.TASK_IDS:
            assert set(tasks.labelled_options(task_id)) == {"ALPHA", "BETA"}

    def test_class_not_stated_in_participant_text(self):
        for task_id in tasks.TASK_IDS:
            text = tasks.participant_text(task_id).lower()
            assert "class" not in text
            assert "divergent" not in text

    def test_audit_detects_a_planted_term(self):
        """The leakage audit must actually fire, not vacuously pass."""
        original = tasks._TASKS["permit_sequence"]["situation"]
        try:
            tasks._TASKS["permit_sequence"]["situation"] = original + " This tests procedural dependence."
            assert tasks.audit_leakage("permit_sequence") != []
        finally:
            tasks._TASKS["permit_sequence"]["situation"] = original
        assert tasks.audit_leakage("permit_sequence") == []


class TestParticipantText:
    def test_common_framing_present_in_every_task(self):
        for task_id in tasks.TASK_IDS:
            assert tasks.COMMON_FRAMING in tasks.participant_text(task_id)

    def test_lengths_are_comparable(self):
        """Large length differences would be a confound across tasks."""
        lengths = [len(tasks.participant_text(t).split()) for t in tasks.TASK_IDS]
        assert max(lengths) - min(lengths) <= 40

    def test_no_analysis_fields_reach_participants(self):
        for task_id in tasks.TASK_IDS:
            text = tasks.participant_text(task_id)
            for field in ("process_text", "outcome_text", "task_class", "pd_predicts"):
                assert field not in text


class TestFreezing:
    def test_content_hash_is_stable(self):
        assert tasks.content_hash() == tasks.content_hash()

    def test_content_hash_tracks_task_edits(self):
        original = tasks._TASKS["tender_award"]["situation"]
        before = tasks.content_hash()
        try:
            tasks._TASKS["tender_award"]["situation"] = original + " Extra."
            assert tasks.content_hash() != before
        finally:
            tasks._TASKS["tender_award"]["situation"] = original
        assert tasks.content_hash() == before

    def test_content_hash_tracks_label_edits(self):
        before = tasks.content_hash()
        original = tasks.PROCESS_LABEL["permit_sequence"]
        try:
            tasks.PROCESS_LABEL["permit_sequence"] = "ALPHA" if original == "BETA" else "BETA"
            assert tasks.content_hash() != before
        finally:
            tasks.PROCESS_LABEL["permit_sequence"] = original
        assert tasks.content_hash() == before


class TestPowerHelpers:
    def test_point_biserial_matches_the_reanalysis_helper(self):
        values = [0.1, 0.3, 0.7, 0.9]
        binary = [0, 0, 1, 1]
        assert power.point_biserial(values, binary) > 0.9

    def test_point_biserial_none_without_outcome_variance(self):
        assert power.point_biserial([0.1, 0.5, 0.9], [1, 1, 1]) is None

    def test_simulated_quintiles_respect_their_rates(self):
        """A zero-rate task yields no choices; a unit-rate task yields all."""
        import random
        rng = random.Random(3)
        _, none_chosen = power.simulate_task(100, [0.0] * 5, rng)
        _, all_chosen = power.simulate_task(100, [1.0] * 5, rng)
        assert sum(none_chosen) == 0
        assert sum(all_chosen) == 100

    def test_planning_effect_is_the_weakest_observed_cell(self):
        """Power must be planned conservatively, not against the largest effect."""
        gaps = {k: v[4] - v[0] for k, v in power.OBSERVED.items()}
        weakest = min(gaps, key=gaps.get)
        assert weakest == "S3_00100"
        assert gaps[weakest] == pytest.approx(0.350, abs=1e-9)

    def test_pd_is_separable_in_the_correlation_matrix(self):
        _, max_abs = power.pd_separability()
        assert max_abs == pytest.approx(0.200, abs=1e-9)
        assert max_abs < 0.5, "PD too correlated to separate by control"

    def test_pd_beta_matches_the_thesis_marginal(self):
        assert power.PD_BETA == (2.5, 2.0)


class TestProtocolConsistency:
    """The protocol document must agree with the code it describes."""

    @pytest.fixture(scope="class")
    def protocol(self):
        if not PROTOCOL.exists():
            pytest.skip("protocol not present")
        return PROTOCOL.read_text(encoding="utf-8")

    def test_states_draft_and_unauthorised(self, protocol):
        head = protocol[:400].lower()
        assert "draft" in head
        assert "not authorised" in head or "not frozen" in head

    def test_quotes_the_selected_sample_size(self, protocol):
        assert "120" in protocol

    def test_quotes_the_separability_figure(self, protocol):
        assert "0.200" in protocol or "0.20" in protocol

    def test_records_failure_conditions(self, protocol):
        # Normalise wrapping: the document hard-wraps, so match on collapsed text.
        flat = " ".join(protocol.lower().split())
        assert "failure condition" in flat
        assert "sign of the result is not a success gate" in flat

    def test_screen_rejects_deterministic_tasks(self, protocol):
        assert "1.00" in protocol
        assert re.search(r"dispersion pre-screen", protocol, re.I)

    def test_states_scope_limits(self, protocol):
        flat = " ".join(protocol.lower().split())
        for claim in ("no ethical understanding", "no human resemblance", "no moral quality"):
            assert claim in flat
