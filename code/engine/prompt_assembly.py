"""
prompt_assembly.py — build the parameter-conditioned system prompt and the
per-problem user turns.

Implements spec §5.3 (parameter substitution to two decimals; configuration
substitution LOW/HIGH + two-sentence description; user turn from the problem
dilemma). The same system prompt is reused verbatim for per-round reinjection
in the orchestrator (spec §6.3).

The canonical template is prompts/system_prompt_template.md (thesis §6.4.1).
Configuration descriptions come from config/configurations.json when present;
a deterministic fallback description is generated from the axis levels so the
engine runs before the descriptions are hand-authored at config sign-off.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import utils

REPO_ROOT = Path(__file__).resolve().parents[2]
TEMPLATE_FILE = REPO_ROOT / "prompts" / "system_prompt_template.md"
CONFIG_FILE = REPO_ROOT / "config" / "configurations.json"

AXIS_ORDER = utils.CONFIG_AXES  # [Freedom, Justice, Authority, Care, Loyalty]

# Placeholder key per parameter (MoR is the only non-uppercase-clean code).
_PLACEHOLDER = {name: ("MOR" if name == "MoR" else name.upper()) for name in utils.PARAM_NAMES}


def load_template() -> str:
    text = TEMPLATE_FILE.read_text(encoding="utf-8")
    m = re.search(r"```\s*\n(You are participating.*?)\n```", text, flags=re.DOTALL)
    if not m:
        raise ValueError(f"Canonical system-prompt block not found in {TEMPLATE_FILE}")
    return m.group(1).strip()


def _load_config_descriptions() -> dict[str, str]:
    if not CONFIG_FILE.exists():
        return {}
    data = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
    out = {}
    for entry in data.get("configurations", []):
        desc = entry.get("description")
        if desc:
            out[entry["code"]] = desc
    return out


_CONFIG_DESCRIPTIONS = _load_config_descriptions()


def config_axes(code: str) -> dict[str, int]:
    return utils.config_to_axes(code)


def _fallback_description(code: str) -> str:
    axes = config_axes(code)
    highs = [a.lower() for a, v in axes.items() if v == 1]
    lows = [a.lower() for a, v in axes.items() if v == 0]
    def phrase(names):
        return ", ".join(names) if names else "none"
    return (
        f"Structurally, this environment is high on {phrase(highs)} and low on "
        f"{phrase(lows)}. High axes are enforced, permitted, and rewarded by the "
        f"institution; low axes are unstructured, unprotected, or penalised."
    )


def config_description(code: str) -> str:
    return _CONFIG_DESCRIPTIONS.get(code) or _fallback_description(code)


def build_system_prompt(agent_parameters: dict[str, float], config_code: str,
                        *, template: str | None = None) -> str:
    """
    Populate the canonical template with an agent's parameter values (two dp)
    and a configuration's axis levels + description. Used for both simple
    problems and every round of the complex problems (reinjection).
    """
    tpl = template if template is not None else load_template()
    for name in utils.PARAM_NAMES:
        tpl = tpl.replace(f"[{_PLACEHOLDER[name]}_VALUE]", f"{agent_parameters[name]:.2f}")
    axes = config_axes(config_code)
    for axis in AXIS_ORDER:
        level = "HIGH" if axes[axis] == 1 else "LOW"
        tpl = tpl.replace(f"[{axis.upper()}]", level)
    tpl = tpl.replace("[CONFIG_DESCRIPTION]", config_description(config_code))
    return tpl


def build_simple_user_turn(dilemma_body: str, labels: tuple[str, str],
                           *, bare_label: bool = False) -> str:
    """Spec §6.4.2 user-turn template for a single binary decision.

    `bare_label=True` uses the naked-calibration envelope ("Reply with only:
    X or Y", no DECISION/REASONING structure) — the delivery shown (grid +
    ablations, 2026-07-28) to keep the recalibrated dilemmas bistable, whereas
    the DECISION+REASONING format collapses the format-fragile ones. Default
    False preserves the original §6.4.2 format for existing callers.
    """
    a, b = labels
    if bare_label:
        return f"{dilemma_body}\n\nReply with only: {a} or {b}"
    return (
        f"{dilemma_body}\n\n"
        "Respond in exactly this format:\n"
        f"DECISION: [{a} | {b}]\n"
        "REASONING: [2-3 sentences explaining why, grounded in your profile and context]"
    )
