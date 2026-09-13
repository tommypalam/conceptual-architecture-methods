"""Offline Phase 3 mechanics, prospective revision; no provider or dispatch code.

These primitives do not release stimuli or claim historical replication. Frozen
Phase 1/2 sources and the first Phase 3 checks are deliberately not modified.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
import math
from pathlib import Path
import random
import re

ROOT = Path(__file__).resolve().parents[1]
PARAMETERS = ("LL", "CS", "RT", "MoR", "RE", "PD", "TfA", "ID", "MS", "AW")
AXES = ("Freedom", "Justice", "Authority", "Care", "Loyalty")


def context_prompt(profile, axes):
    """Substitute all ten coordinates; NEUTRAL is neither LOW nor a sixth axis."""
    if set(profile) != set(PARAMETERS) or set(axes) != set(AXES):
        raise ValueError("Require exactly ten parameters and five context axes")
    for value in profile.values():
        if type(value) not in (int, float) or not math.isfinite(value) or not 0 <= value <= 1:
            raise ValueError("Profile coordinates must be finite numbers in [0,1]")
    for value in axes.values():
        if not (type(value) is int and value in (0, 1)) and value != "NEUTRAL":
            raise ValueError("Axes require integer 0/1 or explicit NEUTRAL")
    source = (ROOT / "prompts/system_prompt_template.md").read_text(encoding="utf-8")
    match = re.search(r"```\s*\n(You are participating.*?)\n```", source, re.S)
    if not match:
        raise ValueError("Canonical template block missing")
    text = match.group(1).strip()
    for name in PARAMETERS:
        text = text.replace(f"[{name.upper()}_VALUE]", f"{profile[name]:.2f}")
    labels = {0: "LOW", 1: "HIGH", "NEUTRAL": "NEUTRAL"}
    for axis in AXES:
        text = text.replace(f"[{axis.upper()}]", labels[axes[axis]])
    # Retain the existing assembler's HIGH/LOW convention; add only omission
    # semantics for the spec's partial contexts. This wording awaits review.
    description = (
        "For axes marked HIGH, the institution enforces, permits, and rewards that property; "
        "for axes marked LOW, that property is unstructured, unprotected, or penalised. "
        "NEUTRAL means no institutional high or low stance is specified on that axis; "
        "it does not remove your individual characteristics or the facts of the task."
    )
    text = text.replace("[CONFIG_DESCRIPTION]", description)
    if re.search(r"\[[A-Z_]+\]", text):
        raise ValueError("Unresolved template placeholder")
    return text


@dataclass(frozen=True)
class Escalation:
    """Thirty aversive decisions, up to four prods per level, explicit exit.

    Correct learning trials and historical spoken scripts are outside this
    kernel. A stimulus author must explicitly disclose that abstraction.
    """
    delivered: int = 0
    prods: int = 0
    terminal: str | None = None

    def __post_init__(self):
        if type(self.delivered) is not int or not 0 <= self.delivered <= 30:
            raise ValueError("Invalid delivered-level count")
        if type(self.prods) is not int or not 0 <= self.prods <= 4:
            raise ValueError("Invalid prod count")
        if self.terminal not in (None, "quit", "complete"):
            raise ValueError("Invalid terminal state")
        if (self.delivered == 30) != (self.terminal == "complete"):
            raise ValueError("Completion requires delivery of level 30")
        if self.terminal is not None and self.prods:
            raise ValueError("Terminal state cannot contain pending prods")

    @property
    def maximum_level(self):
        return 15 * self.delivered

    @property
    def next_level(self):
        return None if self.terminal else 15 * (self.delivered + 1)

    def advance(self, action):
        if self.terminal:
            raise ValueError("Cannot continue a terminated trajectory")
        if action not in ("continue", "hesitate", "quit"):
            raise ValueError("Invalid action; retain record, do not score as refusal")
        if action == "quit" or (action == "hesitate" and self.prods == 4):
            return replace(self, prods=0, terminal="quit")
        if action == "hesitate":
            return replace(self, prods=self.prods + 1)
        delivered = self.delivered + 1
        return Escalation(delivered, 0, "complete" if delivered == 30 else None)


def asch_schedule(stimuli, seed):
    """18 unique images, 12 critical; counterbalance truth and wrong majority.

    Input is ONE family from the existing image manifest. Ground truth and
    stimulus IDs stay in this offline schedule, never in the agent's text.
    Positions below are a new operational schedule, not historical trial order.
    """
    if type(seed) is not int:
        raise ValueError("Seed must be an integer")
    if len(stimuli) != 18 or len({row["id"] for row in stimuli}) != 18:
        raise ValueError("Exactly 18 distinct stimuli are required")
    if len({row["kind"] for row in stimuli}) != 1:
        raise ValueError("Do not mix image families")
    groups = {label: [] for label in "ABC"}
    for row in stimuli:
        if row["correct"] not in groups:
            raise ValueError("Invalid ground truth")
        groups[row["correct"]].append(dict(row))
    if any(len(rows) != 6 for rows in groups.values()):
        raise ValueError("Require six correct positions per label")
    rng = random.Random(seed)
    critical, neutral = [], []
    for label in "ABC":
        rows = sorted(groups[label], key=lambda row: row["id"])
        rng.shuffle(rows)
        wrong = [other for other in "ABC" if other != label]
        for index, row in enumerate(rows):
            is_critical = index < 4
            enriched = {**row, "critical": is_critical,
                        "majority": wrong[index % 2] if is_critical else label}
            (critical if is_critical else neutral).append(enriched)
    rng.shuffle(critical)
    rng.shuffle(neutral)
    # Six neutral trials, including the first two; twelve critical trials.
    neutral_positions = {1, 2, 5, 8, 12, 16}
    return [{"trial": trial, **(neutral.pop() if trial in neutral_positions else critical.pop())}
            for trial in range(1, 19)]


def peer_answers(trial, *, group_size=5, dissent=False):
    if type(group_size) is not int or group_size not in (1, 2, 3, 5):
        raise ValueError("Unsupported prespecified group size")
    if type(dissent) is not bool or (dissent and group_size < 2):
        raise ValueError("Dissent needs at least two peers")
    answers = [trial["majority"]] * group_size
    if dissent and trial["critical"]:
        answers[-1] = trial["correct"]
    return answers


def binary_bounds(outcomes):
    """Assigned-denominator identification bounds, NOT confidence intervals.

    None marks an explicitly missing/invalid assigned outcome. Invalid records
    stay in the denominator; complete-case rates are labelled separately.
    """
    outcomes = list(outcomes)
    if not outcomes or any(value is not None and (type(value) is not int or value not in (0, 1))
                           for value in outcomes):
        raise ValueError("Need nonempty 0/1/None outcomes")
    n = len(outcomes)
    invalid = outcomes.count(None)
    successes = sum(value == 1 for value in outcomes)
    valid = n - invalid
    return {"assigned": n, "valid": valid, "invalid": invalid, "successes": successes,
            "complete_case_rate": successes / valid if valid else None,
            "identification_interval": [successes / n, (successes + invalid) / n]}


def paired_bounds(high, low):
    """Pair by explicit participant ID; reject omissions instead of inner joining."""
    if not high or set(high) != set(low):
        raise ValueError("Paired conditions must have identical assigned IDs")
    hi = binary_bounds(high.values())
    lo = binary_bounds(low.values())
    complete = [high[key] - low[key] for key in high
                if high[key] is not None and low[key] is not None]
    return {"assigned_pairs": len(high), "complete_pairs": len(complete),
            "complete_pair_difference": sum(complete) / len(complete) if complete else None,
            "identification_interval": [hi["identification_interval"][0] - lo["identification_interval"][1],
                                        hi["identification_interval"][1] - lo["identification_interval"][0]]}


def score_asch(schedule, choices):
    expected = {row["trial"] for row in schedule}
    if expected != set(range(1, 19)) or len(schedule) != 18 or set(choices) != expected:
        raise ValueError("Require all 18 assigned trials, including explicit missing values")
    if sum(row["critical"] for row in schedule) != 12:
        raise ValueError("Require twelve critical trials")
    conformity, accuracy = [], []
    for row in schedule:
        choice = choices[row["trial"]]
        if choice is not None and choice not in ("A", "B", "C"):
            raise ValueError("Invalid choices must first be retained and classified as missing")
        accuracy.append(None if choice is None else int(choice == row["correct"]))
        if row["critical"]:
            conformity.append(None if choice is None else int(choice == row["majority"]))
    return {"critical_majority_agreement": binary_bounds(conformity),
            "all_trial_accuracy": binary_bounds(accuracy)}


def score_ultimatum(responses):
    """Separate 20%-offer rejection from an interval on the five-offer grid."""
    offers = (10, 20, 30, 40, 50)
    if set(responses) != set(offers):
        raise ValueError("All five assigned offers required")
    if any(value not in ("accept", "reject", None) for value in responses.values()):
        raise ValueError("Invalid response classification")
    primary = responses[20]
    result = {"rejection_at_20": None if primary is None else int(primary == "reject"),
              "invalid_offers": sum(value is None for value in responses.values()),
              "monotone": None, "acceptance_threshold_interval": None}
    if result["invalid_offers"]:
        return result
    accepts = [offer for offer in offers if responses[offer] == "accept"]
    rejects = [offer for offer in offers if responses[offer] == "reject"]
    monotone = not accepts or not rejects or max(rejects) < min(accepts)
    result["monotone"] = monotone
    if monotone:
        # Lower bound open, upper bound closed; None means not bounded by tested offers.
        result["acceptance_threshold_interval"] = {
            "lower_exclusive": max(rejects) if rejects else None,
            "upper_inclusive": min(accepts) if accepts else None}
    return result


def score_reactance(pre, post, choice, *, options, removed, adjacency, available):
    """Score a predeclared graph and availability without imputing preferences.

    Rankings evaluate ALL original options; availability constrains choice only.
    The proposed graph/stimuli and causal controls still require review.
    """
    options = tuple(options)
    option_set = set(options)
    if len(option_set) != len(options) or len(options) < 3 or removed not in option_set:
        raise ValueError("Invalid original option set")
    if set(adjacency) != option_set:
        raise ValueError("Freeze adjacency for every original option")
    for option, neighbours in adjacency.items():
        if option in neighbours or not set(neighbours) <= option_set or len(neighbours) != len(set(neighbours)):
            raise ValueError("Invalid adjacency graph")
        if any(option not in adjacency[other] for other in neighbours):
            raise ValueError("Adjacency must be symmetric")
    if not available or len(available) != len(set(available)) or not set(available) <= option_set:
        raise ValueError("Invalid availability")
    for ranking in (pre, post):
        if ranking is not None and (len(ranking) != len(options) or set(ranking) != option_set):
            raise ValueError("Ranking must be a permutation of all original options")
    valid_choice = choice in available
    return {"choice_valid": valid_choice,
            "adjacent_choice": int(choice in adjacency[removed]) if valid_choice else None,
            "removed_option_rank_improvement": pre.index(removed) - post.index(removed)
                if pre is not None and post is not None else None}


def intervention_outcome(actions, *, opportunities):
    """Discrete opportunities are model steps, never elapsed human seconds."""
    if type(opportunities) is not int or opportunities < 1 or len(actions) > opportunities:
        raise ValueError("Invalid observation window")
    for index, action in enumerate(actions):
        if action == "help":
            if index != len(actions) - 1:
                raise ValueError("Records after terminal intervention")
            return {"intervened": 1, "opportunity": index + 1}
        if action != "wait":
            raise ValueError("Invalid action is neither refusal nor waiting")
    return {"intervened": 0 if len(actions) == opportunities else None, "opportunity": None}
