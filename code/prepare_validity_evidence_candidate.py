"""Prepare an offline S3 evidence candidate; never construct or send API requests."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path

from engine.questions import PHASE0B_QUESTIONS, REPO_ROOT, load_dilemma_body
from research_support.evidence import EvidenceCard, digest, render_evidence_card


DESTINATION = REPO_ROOT / "experiments/phase1_5_encoding_validity/evidence_candidate_20260911"
SOURCE = PHASE0B_QUESTIONS / "S3_strategic_pivot.md"


def prepare(destination: Path = DESTINATION) -> dict:
    source_bytes = SOURCE.read_bytes()
    body = load_dilemma_body(SOURCE.name, base_dir=PHASE0B_QUESTIONS)
    card = EvidenceCard(
        scenario_id="S3",
        source_path=SOURCE.relative_to(REPO_ROOT).as_posix(),
        source_file_sha256=sha256(source_bytes).hexdigest(),
        body_sha256=digest(body),
        paragraphs=tuple(body.split("\n\n")),
    )
    # Reassembly must cover the WHOLE loader body, in order, without commentary
    # from the surrounding source file's metadata or calibration notes.
    assert "\n\n".join(card.paragraphs) == body
    artifacts = {
        "S3.evidence.json": card.to_json().encode("utf-8"),
        "S3_OVERLAY_DRAFT.txt": (render_evidence_card(card) + "\n").encode("utf-8"),
    }
    manifest = {
        "status": "DRAFT_NOT_APPROVED_FOR_INJECTION",
        "scenario_id": "S3",
        "source_path": card.source_path,
        "source_file_sha256": card.source_file_sha256,
        "loader_body_sha256": card.body_sha256,
        "n_paragraphs": len(card.paragraphs),
        "whole_body_reconstruction": True,
        "artifact_sha256": {name: sha256(raw).hexdigest() for name, raw in artifacts.items()},
        "preparation_source_sha256": {
            name: sha256((REPO_ROOT / name).read_bytes()).hexdigest()
            for name in (
                "code/prepare_validity_evidence_candidate.py",
                "code/research_support/evidence.py",
                "code/engine/questions.py",
            )
        },
        "paid_calls": 0,
        "runner_integration": False,
    }
    artifacts["manifest.json"] = (json.dumps(manifest, indent=2) + "\n").encode("utf-8")
    destination.mkdir(parents=True, exist_ok=True)
    # Check all conflicts before writing anything. Existing artifacts are never
    # overwritten; a revised candidate belongs in a separate designation.
    for name, raw in artifacts.items():
        path = destination / name
        if path.exists() and path.read_bytes() != raw:
            raise ValueError(f"Existing artifact differs: {path}")
    for name, raw in artifacts.items():
        path = destination / name
        if not path.exists():
            with path.open("xb") as handle:
                handle.write(raw)
    assert SOURCE.read_bytes() == source_bytes
    return manifest


if __name__ == "__main__":
    print(json.dumps(prepare(), indent=2))
