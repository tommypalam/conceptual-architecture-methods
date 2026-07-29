"""
framing.py — swappable task-framing + output-order for harness ablation.

The Phase 0b grid (2026-07-28) showed a systemic harness bias: even the empty
harness (null_a) collapses most dilemmas away from the naked-prompt 50/50. The
suspect is the shared FRAMING — the preamble, the task instruction, and the
DECISION-before-REASONING output order — not the dilemma bodies (which are the
frozen Phase-0a-validated set and must not change).

This module makes the framing a first-class, swappable block (like the
null-condition assemblers): a `TaskFraming` value object with four independently
toggleable elements, so we can ABLATE each one and see which clause moves the
split. SOLID: the runner/assemblers depend on the framing through a stable
shape; changing framing changes nothing else.

Elements (True = the current/canonical setting):
  preamble        include "You are participating in a decision-making simulation."
  decision_rule   task says "apply the decision-making profile AS A DECISION RULE"
                  vs. a neutral "consider the decision below"
  do_not_refuse   include "Do not refuse to decide."
  decision_first  output order DECISION then REASONING (True) vs REASONING
                  then DECISION (False)

Nothing here reads or writes dilemma text; the dilemma body is supplied by the
runner and passed through untouched.
"""

from __future__ import annotations

from dataclasses import dataclass

PREAMBLE = "You are participating in a decision-making simulation."

# The canonical task tail shared by all framings (identity / refusal handling is
# toggled; the "exact format" instruction is constant because the format block
# itself is appended by the user turn).
_IDENTITY_CLAUSE = ("Do not infer demographic identity, personality, ideology, "
                    "or narrative backstory beyond what the profile specifies.")
_IDENTITY_CLAUSE_NOPROFILE = ("Do not infer demographic identity, personality, "
                              "ideology, or narrative backstory.")


@dataclass(frozen=True)
class TaskFraming:
    preamble: bool = True
    decision_rule: bool = True
    do_not_refuse: bool = True
    decision_first: bool = True
    require_reasoning: bool = True   # False = DECISION only (naked Phase-0a format)
    use_system_role: bool = True     # False = NO system message at all (pure 0a
                                     #         structure: dilemma as user-only)
    bare_label: bool = False         # True = "Reply with only: X or Y" output
                                     #        (the exact naked-calibration envelope,
                                     #        no "DECISION: [X | Y]" structure).
                                     #        Overrides the DECISION/REASONING block.

    # ---- identity label for records / tags -------------------------------- #
    @property
    def label(self) -> str:
        return (f"pre{int(self.preamble)}_rule{int(self.decision_rule)}"
                f"_refuse{int(self.do_not_refuse)}_decfirst{int(self.decision_first)}"
                f"_reason{int(self.require_reasoning)}_sys{int(self.use_system_role)}"
                f"_bare{int(self.bare_label)}")

    # ---- the task block that replaces "# Your task" ----------------------- #
    def task_block(self, *, has_profile: bool) -> str:
        if self.decision_rule and has_profile:
            action = ("Apply the decision-making profile as a decision rule, "
                      "taking the parameter values and normative context as the "
                      "operative inputs.")
        elif self.decision_rule and not has_profile:
            action = "Apply a consistent decision-making rule to the decision below."
        else:
            action = "Consider the decision below and reach a judgment."
        identity = _IDENTITY_CLAUSE if has_profile else _IDENTITY_CLAUSE_NOPROFILE
        refusal = " Do not refuse to decide." if self.do_not_refuse else ""
        lines = ["# Your task", "",
                 f"You will be presented with a decision. {action} {identity}"
                 f"{refusal} Answer in the exact format specified."]
        return "\n".join(lines)

    # ---- the user-turn format block (controls output order + reasoning) --- #
    def format_block(self, labels: tuple[str, str]) -> str:
        a, b = labels
        if self.bare_label:
            # The exact Phase-0a naked-calibration envelope. No structured
            # decision token, no reasoning — the format the bistable splits were
            # measured under.
            return f"Reply with only: {a} or {b}"
        decision_line = f"DECISION: [{a} | {b}]"
        if not self.require_reasoning:
            # Closest to the naked Phase-0a format: a bare labelled decision,
            # no justification demanded.
            return "Respond in exactly this format:\n" + decision_line
        reasoning_line = ("REASONING: [2-3 sentences explaining why, grounded in "
                          "your profile and context]")
        if self.decision_first:
            body = f"{decision_line}\n{reasoning_line}"
        else:
            body = f"{reasoning_line}\n{decision_line}"
        return "Respond in exactly this format:\n" + body


# The canonical framing = everything ON, DECISION first (what the grid100 run used).
CANONICAL = TaskFraming()


def ablation_variants() -> dict[str, TaskFraming]:
    """
    Single-element toggles off canonical (round 1, 2026-07-28: clean negative —
    no single clause moved the collapse).
    """
    return {
        "canonical":       TaskFraming(),                       # control
        "no_preamble":     TaskFraming(preamble=False),
        "no_decision_rule": TaskFraming(decision_rule=False),
        "no_do_not_refuse": TaskFraming(do_not_refuse=False),
        "reasoning_first": TaskFraming(decision_first=False),
    }


def reasoning_test_variants() -> dict[str, TaskFraming]:
    """
    Round 2 (clean negative, 2026-07-28): forced REASONING is NOT the cause;
    decision_only behaved like canonical.
    """
    return {
        "canonical":     TaskFraming(),                          # DECISION + REASONING
        "decision_only": TaskFraming(require_reasoning=False),   # DECISION only (naked-like)
    }


def format_sweep_variants() -> dict[str, TaskFraming]:
    """
    Breadth sweep of the OUTPUT-FORMAT levers (2026-07-28, post-grid). The N=200
    grid showed the DECISION:[X|Y]+REASONING scaffold collapses S2/C2/C3 even in
    the empty harness. This sweeps the format wide+shallow, all under the empty
    harness (null_a), prompts frozen:
      canonical      DECISION:[X|Y] + REASONING (control, the collapsing format)
      decision_only  DECISION:[X|Y], no REASONING (isolates reasoning vs token)
      reasoning_first REASONING then DECISION (does order rescue it?)
      bare_label     "Reply with only: X or Y" (the naked-calibration envelope)
      bare_nosys     bare label AND no system message (fullest naked repro)
    """
    return {
        "canonical":       TaskFraming(),
        "decision_only":   TaskFraming(require_reasoning=False),
        "reasoning_first": TaskFraming(decision_first=False),
        "bare_label":      TaskFraming(bare_label=True),
        "bare_nosys":      TaskFraming(bare_label=True, use_system_role=False,
                                       preamble=False),
    }


def system_role_test_variants() -> dict[str, TaskFraming]:
    """
    Round 3: is the mere PRESENCE of a system message the cause? Phase 0a sent
    system=None (dilemma as user-only) and got ~50/50; every harness variant so
    far still sends a system message. `naked_repro` removes the system message
    entirely and asks for a bare decision — the closest possible reproduction of
    the Phase-0a structure — head-to-head against canonical.
    """
    return {
        "canonical":   TaskFraming(),   # full system message + DECISION+REASONING
        "naked_repro": TaskFraming(use_system_role=False, require_reasoning=False,
                                   preamble=False),  # no system msg, bare decision
    }
