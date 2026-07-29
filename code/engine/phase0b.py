"""
phase0b.py — Phase 0b null-condition assemblers (spec §2.1).

SOLID decomposition:
  - `NullConditionAssembler` is a Protocol (interface). The runner depends only
    on this, never on a concrete condition — Dependency Inversion.
  - `EmptyHarness`, `NeutralMeans`, `ShamProfile` are three independently
    swappable implementations. Each is Liskov-substitutable: same `.build(...)`
    contract, same return shape `(system_prompt, provenance)`. Any one can be
    replaced or extended without touching the runner or the others.
  - Single Responsibility: this module only assembles prompts. It does not call
    models, write files, or score. Those are separate blocks.
  - Open/Closed: adding a fourth null condition = add a class + register it in
    `default_assemblers()`; no existing code changes.

Each condition is a surgical variant of the canonical template
(prompts/system_prompt_template.md):

  null_a  empty harness   — profile AND normative-context blocks removed; a
                            self-contained task that supplies no rule (§2.1.1).
  null_b  neutral means   — full template; params at population means; balanced
                            (neutral) normative context (§2.1.2).
  null_c  sham profile     — full template shape; params relabelled X1..X10 with
                            random values; config axes replaced by meaningless
                            tokens of the same syntactic shape (§2.1.3).

The assembler returns provenance (the sham draw / the means used) so the runner
can persist exactly what was shown on each call — required for auditing null_c
and null_b after the fact.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

import numpy as np

import utils

CONDITIONS = ("null_a", "null_b", "null_c")

POPULATION_MEANS = utils.POPULATION_MEANS


# --------------------------------------------------------------------------- #
# Template block splitting (shared helper, no state)
# --------------------------------------------------------------------------- #

def split_blocks(template: str) -> dict[str, str]:
    """Split the canonical template into {preamble, profile, context, task}."""
    profile_h = "# Your decision-making profile"
    context_h = "# Your normative context"
    task_h = "# Your task"
    pre, _, rest = template.partition(profile_h)
    profile_body, _, rest = rest.partition(context_h)
    context_body, _, task_body = rest.partition(task_h)
    return {
        "preamble": pre.rstrip(),
        "profile": (profile_h + profile_body).rstrip(),
        "context": (context_h + context_body).rstrip(),
        "task": (task_h + task_body).rstrip(),
    }


# --------------------------------------------------------------------------- #
# The interface every null condition satisfies (LSP / DIP seam)
# --------------------------------------------------------------------------- #

class NullConditionAssembler(Protocol):
    condition_id: str

    def build(self, template: str, *, seed: int) -> tuple[str, dict]:
        """Return (system_prompt, provenance) for one call. Deterministic in seed."""
        ...


# --------------------------------------------------------------------------- #
# null_a — empty harness (§2.1.1)
# --------------------------------------------------------------------------- #

_NULL_A_TASK = """# Your task

You will be presented with a decision. Apply a consistent decision-making
rule to the decision below. Do not infer demographic identity, personality,
ideology, or narrative backstory. Do not refuse to decide. Answer in the exact
format specified."""

# --- Task-text variants (2026-07-29) ------------------------------------- #
# The N=300 canonical grid showed the null_a TASK TEXT (not the delivery
# envelope) collapses the fragile dilemmas. Prime suspect: "Apply a CONSISTENT
# decision-making rule" — a determinism cue that resolves a coin-flip
# deterministically. These variants vary the task text ONLY, so a sweep under
# the neutral envelope (user_prefix + bare_label) can isolate the offending
# clause. `_NULL_A_TASK` above is the original (collapsing) text, kept for the
# comparison baseline.

# Drops "consistent … rule"; neutral consideration instead.
_NULL_A_TASK_NEUTRAL = """# Your task

You will be presented with a decision. Consider the decision below and choose
one option. Do not infer demographic identity, personality, ideology, or
narrative backstory. Answer in the exact format specified."""

# Minimal: no task framing beyond "answer in the format". Closest to naked.
_NULL_A_TASK_MINIMAL = """# Your task

You will be presented with a decision. Answer in the exact format specified."""

_NULL_A_TASKS = {
    "orig": _NULL_A_TASK,          # collapsing baseline
    "neutral": _NULL_A_TASK_NEUTRAL,
    "minimal": _NULL_A_TASK_MINIMAL,
}

# --- Full scaffold WORDING variants (2026-07-29) ------------------------- #
# Reasoning traces show why the original scaffold collapses C2: "decision-making
# simulation" + "apply a decision rule" primes an ANALYTICAL OPTIMISER, which
# resolves a morally-balanced dilemma toward the financially/strategically
# dominant option (killing the coin-flip). These variants keep the FULL null_a
# structure (a framing line + a task instruction + the format instruction) but
# vary the framing STANCE to avoid priming optimisation. Each is a complete
# system prompt for the empty harness (preamble + task, no content blocks).
# Spec §2.1.5 "revise the template" done deliberately.
_NULL_A_SCAFFOLDS = {
    # w0: the spec original (analytical-optimiser priming) — baseline.
    "w0_orig": (
        "You are participating in a decision-making simulation.\n\n"
        "# Your task\n\n"
        "You will be presented with a decision. Apply a consistent "
        "decision-making rule to the decision below. Do not infer demographic "
        "identity, personality, ideology, or narrative backstory. Do not refuse "
        "to decide. Answer in the exact format specified."),
    # w1: drop "simulation" + "consistent rule"; neutral respondent stance.
    "w1_respondent": (
        "You are responding to a decision scenario.\n\n"
        "# Your task\n\n"
        "You will be presented with a decision. Choose the option you find most "
        "appropriate. There is no single correct answer. Do not infer "
        "demographic identity, personality, ideology, or narrative backstory. "
        "Answer in the exact format specified."),
    # w2: explicitly frame as a genuinely balanced judgement call.
    "w2_balanced": (
        "You are considering a difficult decision on which reasonable people "
        "disagree.\n\n"
        "# Your task\n\n"
        "Weigh the considerations on both sides and choose one option. Neither "
        "option is presumed correct. Do not infer demographic identity, "
        "personality, ideology, or narrative backstory. Answer in the exact "
        "format specified."),
    # w3: minimal framing line, no simulation/optimiser cue at all.
    "w3_plain": (
        "# Your task\n\n"
        "You will be presented with a decision. Choose one option. Do not infer "
        "demographic identity, personality, ideology, or narrative backstory. "
        "Answer in the exact format specified."),
}

# --- Scaffolding ladder (2026-07-29) ------------------------------------- #
# C2 collapses under ANY preamble/task scaffolding. This additive ladder finds
# the exact token where C2 breaks. Each level adds ONE piece to the fully-naked
# base. The assembler emits the `system` chunk; the runner prepends it via
# UserPrefixDelivery (or nothing at "naked"). Sentinel "" => emit no system chunk
# at all (fully-naked: dilemma + bare label only).
_LADDER_PREAMBLE = "You are participating in a decision-making simulation."
_LADDER_TASK = ("# Your task\n\nYou will be presented with a decision. Consider "
                "the decision below and choose one option. Answer in the exact "
                "format specified.")
_LADDER_IDENTITY = ("Do not infer demographic identity, personality, ideology, "
                    "or narrative backstory.")

_NULL_A_LADDER = {
    "L0_naked": "",                                                  # nothing
    "L1_preamble": _LADDER_PREAMBLE,
    "L2_task": f"{_LADDER_PREAMBLE}\n\n{_LADDER_TASK}",
    "L3_identity": (f"{_LADDER_PREAMBLE}\n\n# Your task\n\nYou will be presented "
                    f"with a decision. Consider the decision below and choose one "
                    f"option. {_LADDER_IDENTITY} Answer in the exact format "
                    f"specified."),
}


@dataclass
class EmptyHarness:
    """Preamble + a self-contained task. Profile and context blocks removed.

    The canonical task references "the decision-making profile … parameter
    values and normative context" and "beyond what the profile specifies" — all
    incoherent when there is no profile. This condition therefore substitutes a
    task that supplies no rule at all (scaffolding present, content absent).

    `task_variant` selects the task text (see _NULL_A_TASKS). Default "orig"
    preserves the original behaviour for existing callers (Liskov-safe).
    """
    condition_id: str = "null_a"
    task_variant: str = "orig"
    scaffold: str | None = None   # if set, use a full _NULL_A_SCAFFOLDS wording
                                  # verbatim (preamble + task); overrides task_variant

    def build(self, template: str, *, seed: int) -> tuple[str, dict]:
        if self.scaffold is not None:
            system = _NULL_A_SCAFFOLDS[self.scaffold].strip()
            return system, {"condition": self.condition_id,
                            "detail": f"empty harness — scaffold={self.scaffold}"}
        b = split_blocks(template)
        task = _NULL_A_TASKS[self.task_variant]
        system = f"{b['preamble']}\n\n{task}".strip()
        return system, {"condition": "null_a",
                        "detail": f"empty harness — task_variant={self.task_variant}"}


@dataclass
class LadderHarness:
    """null_a scaffolding-ladder assembler (diagnostic, 2026-07-29).

    Emits one level of the additive scaffolding ladder (_NULL_A_LADDER). L0_naked
    emits an empty string so UserPrefixDelivery sends the dilemma alone. Does not
    read the template preamble — the ladder text is self-contained so each level
    adds exactly one known piece.
    """
    condition_id: str = "L0_naked"
    level: str = "L0_naked"

    def build(self, template: str, *, seed: int) -> tuple[str, dict]:
        system = _NULL_A_LADDER[self.level]
        return system, {"condition": self.condition_id,
                        "detail": f"scaffolding ladder level={self.level}"}


# --------------------------------------------------------------------------- #
# null_b — population means at neutral configuration (§2.1.2)
# --------------------------------------------------------------------------- #

_NEUTRAL_CONTEXT = """# Your normative context

You operate in a society whose structural environment is balanced on every
dimension — neither high-freedom nor low-freedom, neither high-justice nor
low-justice, neither high-authority nor low-authority, neither high-care nor
low-care, and neither high-loyalty nor low-loyalty. No structural axis pushes
in either direction; the environment is neutral throughout."""


@dataclass
class NeutralMeans:
    """Full template; params at population means; balanced normative context."""
    condition_id: str = "null_b"

    def build(self, template: str, *, seed: int) -> tuple[str, dict]:
        b = split_blocks(template)
        profile = b["profile"]
        for name in utils.PARAM_NAMES:
            ph = "MOR" if name == "MoR" else name.upper()
            profile = profile.replace(f"[{ph}_VALUE]", f"{POPULATION_MEANS[name]:.2f}")
        system = "\n\n".join([b["preamble"], profile, _NEUTRAL_CONTEXT, b["task"]]).strip()
        return system, {"condition": "null_b",
                        "detail": "population means at neutral configuration",
                        "parameter_values": dict(POPULATION_MEANS)}


@dataclass
class SweepProfile:
    """
    Phase 1.5 §4.1 single-parameter sweep harness: nine parameters held at
    population means, ONE parameter (`sweep_param`) set to `sweep_value`,
    balanced (neutral) normative context. Same block structure as NeutralMeans
    (full Phase-2 harness), so the only thing that varies across a sweep is the
    one parameter's numeric value.
    """
    sweep_param: str = "RE"
    sweep_value: float = 0.5
    condition_id: str = "sweep"

    def build(self, template: str, *, seed: int) -> tuple[str, dict]:
        if self.sweep_param not in utils.PARAM_NAMES:
            raise ValueError(f"unknown parameter {self.sweep_param!r}")
        values = dict(POPULATION_MEANS)
        values[self.sweep_param] = self.sweep_value
        b = split_blocks(template)
        profile = b["profile"]
        for name in utils.PARAM_NAMES:
            ph = "MOR" if name == "MoR" else name.upper()
            profile = profile.replace(f"[{ph}_VALUE]", f"{values[name]:.2f}")
        system = "\n\n".join([b["preamble"], profile, _NEUTRAL_CONTEXT, b["task"]]).strip()
        return system, {"condition": self.condition_id,
                        "detail": f"sweep {self.sweep_param}={self.sweep_value:.2f}",
                        "sweep_param": self.sweep_param,
                        "sweep_value": self.sweep_value,
                        "parameter_values": values}


# --------------------------------------------------------------------------- #
# null_c — sham profile (§2.1.3)
# --------------------------------------------------------------------------- #

_SYLLABLES = ["vor", "tal", "mek", "sil", "dun", "cra", "pel", "nor", "bix",
              "quor", "fen", "lah", "tov", "wem", "zar", "kip"]


@dataclass
class ShamProfile:
    """
    Full template shape, semantic content scrambled. `keep_glosses` controls the
    one place the two prior runners disagreed (Open/Closed — the choice is a
    parameter, not a fork):
      keep_glosses=True  → each sham parameter keeps a two-endpoint gloss, so the
                           block matches the real template's syntactic shape most
                           closely (spec §2.1.3 "same syntactic shape").
      keep_glosses=False → bare `Parameter Xk: value` lines, no gloss.
    Deterministic given seed.
    """
    condition_id: str = "null_c"
    keep_glosses: bool = True

    def _token(self, rng: np.random.Generator, n_syllables: int = 2) -> str:
        return "".join(rng.choice(_SYLLABLES) for _ in range(n_syllables)).capitalize()

    def build(self, template: str, *, seed: int) -> tuple[str, dict]:
        rng = np.random.default_rng(seed)
        b = split_blocks(template)

        lines = ["# Your decision-making profile", "",
                 "You process decisions according to the following characteristics, each",
                 "on a continuous [0, 1] scale. The low and high ends of each are",
                 "described. Your value on each characteristic is given.", ""]
        values, glosses = [], []
        for i in range(1, 11):
            val = round(float(rng.uniform(0, 1)), 2)
            values.append(val)
            lines.append(f" {i}. Parameter X{i}: {val:.2f}")
            if self.keep_glosses:
                low, high = self._token(rng), self._token(rng)
                glosses.append((low, high))
                lines.append(f"    (0 = {low.lower()}; 1 = {high.lower()})")
            lines.append("")
        profile = "\n".join(lines).rstrip()

        axis_tokens = [self._token(rng).upper() for _ in range(5)]
        ctx = ["# Your normative context", "",
               "You operate in a society with the following structural properties:"]
        for j, tok in enumerate(axis_tokens, start=1):
            ctx.append(f"- Attribute Q{j}: {tok}")
        ctx.append("")
        ctx.append(f"{self._token(rng)} {self._token(rng)}; {self._token(rng)} {self._token(rng)}.")
        context = "\n".join(ctx)

        system = "\n\n".join([b["preamble"], profile, context, b["task"]]).strip()
        prov = {"condition": "null_c", "detail": "sham profile — random names/values/tokens",
                "sham_values": values, "sham_axis_tokens": axis_tokens,
                "keep_glosses": self.keep_glosses}
        if self.keep_glosses:
            prov["sham_glosses"] = glosses
        return system, prov


# --------------------------------------------------------------------------- #
# Registry (the runner is injected with this; can be overridden wholesale)
# --------------------------------------------------------------------------- #

def default_assemblers(*, sham_keep_glosses: bool = True
                       ) -> dict[str, NullConditionAssembler]:
    return {
        "null_a": EmptyHarness(),
        "null_b": NeutralMeans(),
        "null_c": ShamProfile(keep_glosses=sham_keep_glosses),
    }
