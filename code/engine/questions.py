"""
questions.py — read dilemma text from the locked Phase 0 question files.

Single Responsibility: this is the one place that knows how a locked question
file is laid out (a fenced code block, with a trailing "Reply with only:" line
the harness replaces). Every runner sources dilemma bodies through here, so the
file-format knowledge is not duplicated across simple / complex / phase0b.

The Phase 0 questions directory is immutable provenance; this module only reads.
"""

from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

# The Phase-0a calibration set — immutable provenance, NEVER edited.
PHASE0_QUESTIONS = REPO_ROOT / "experiments" / "phase0_baseline_calibration" / "questions"

# The Phase-0b recalibrated set — new canonical files created 2026-07-28 after
# model drift pushed 4 of 6 Phase-0a dilemmas off their bistable baseline on the
# current model. The 0a set above is left frozen; this is a SEPARATE directory.
PHASE0B_QUESTIONS = REPO_ROOT / "experiments" / "phase0b_calibration" / "questions"


def _extract_body(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    m = re.search(r"```(?:[a-zA-Z0-9_-]+)?\s*\n(.*?)\n```", text, flags=re.DOTALL)
    if not m:
        raise ValueError(f"No fenced prompt block in {path}")
    body = m.group(1).strip()
    return re.sub(r"\n\s*Reply with only:.*$", "", body,
                  flags=re.IGNORECASE | re.DOTALL).strip()


def load_dilemma_body(question_file: str, base_dir: Path = PHASE0_QUESTIONS) -> str:
    """
    Extract the dilemma text from a locked question file, dropping the
    naked-prompt 'Reply with only: …' line (the harness supplies its own
    DECISION+REASONING format instruction).

    `base_dir` defaults to the immutable Phase-0a set so every existing caller
    keeps its exact behaviour (Liskov-safe). Pass `PHASE0B_QUESTIONS` to source
    the recalibrated set.
    """
    return _extract_body(base_dir / question_file)
