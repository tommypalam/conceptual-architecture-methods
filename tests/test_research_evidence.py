from dataclasses import FrozenInstanceError, replace
from hashlib import sha256
import json
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "code"))

from engine.questions import PHASE0B_QUESTIONS, load_dilemma_body
from prepare_validity_evidence_candidate import SOURCE, prepare
from research_support.evidence import (
    EvidenceCard, EvidenceTool, JsonEvidenceProvider, MemoryEvidenceProvider,
    UnknownScenarioError, render_evidence_card,
)


@pytest.fixture
def prepared(tmp_path):
    original = SOURCE.read_bytes()
    manifest = prepare(tmp_path)
    assert prepare(tmp_path) == manifest
    assert SOURCE.read_bytes() == original
    raw = (tmp_path / "S3.evidence.json").read_bytes()
    return tmp_path, manifest, EvidenceCard.from_json(raw.decode("utf-8"))


@pytest.mark.parametrize("adapter", ["memory", "json"])
def test_provider_substitution_contract(prepared, adapter):
    path, manifest, card = prepared
    catalogue = [card]
    pins = {"S3": (path / "S3.evidence.json", manifest["artifact_sha256"]["S3.evidence.json"])}
    provider = (MemoryEvidenceProvider(catalogue) if adapter == "memory"
                else JsonEvidenceProvider(pins))
    tool = EvidenceTool(provider)
    expected = render_evidence_card(card)
    # Snapshot semantics are identical: caller mutations and later file changes
    # cannot change a running lookup. Tool IDs never become filesystem paths.
    catalogue.clear()
    pins.clear()
    (path / "S3.evidence.json").write_bytes(b"changed after construction")
    assert provider.get("S3") == card
    assert provider.get("S3") is provider.get("S3")
    assert tool.read("S3") == expected
    for unknown in ("S1", "", "../../secrets", str(SOURCE)):
        with pytest.raises(UnknownScenarioError) as error:
            tool.read(unknown)
        assert error.value.args == (unknown,)
    with pytest.raises(FrozenInstanceError):
        provider.get("S3").paragraphs = ("replacement",)
    assert tool.read("S3") == expected


def test_full_source_coverage_no_calibration_leakage(prepared):
    path, manifest, card = prepared
    body = load_dilemma_body(SOURCE.name, base_dir=PHASE0B_QUESTIONS)
    assert "\n\n".join(card.paragraphs) == body
    assert card.source_file_sha256 == sha256(SOURCE.read_bytes()).hexdigest()
    overlay = (path / "S3_OVERLAY_DRAFT.txt").read_text(encoding="utf-8")
    assert overlay == render_evidence_card(card) + "\n"
    assert "ADOPT = outcome-dominant" not in overlay
    assert "Calibration notes" not in overlay
    assert manifest["paid_calls"] == 0 and manifest["runner_integration"] is False
    with pytest.raises(ValueError, match="reconstruct"):
        replace(card, paragraphs=card.paragraphs[:-1])
    with pytest.raises(ValueError, match="reconstruct"):
        replace(card, paragraphs=tuple(reversed(card.paragraphs)))
    with pytest.raises(ValueError, match="immutable"):
        replace(card, paragraphs=list(card.paragraphs))


def test_tampered_artifact_and_wrong_catalogue_fail_before_serving(prepared):
    path, manifest, card = prepared
    artifact = path / "S3.evidence.json"
    pin = manifest["artifact_sha256"][artifact.name]
    with pytest.raises(ValueError, match="Catalogue ID"):
        JsonEvidenceProvider({"S1": (artifact, pin)})
    with pytest.raises(ValueError, match="Duplicate"):
        MemoryEvidenceProvider([card, card])
    altered = json.loads(card.to_json())
    altered["paragraphs"][0] += " Added claim."
    artifact.write_text(json.dumps(altered), encoding="utf-8")
    with pytest.raises(ValueError, match="hash mismatch"):
        JsonEvidenceProvider({"S3": (artifact, pin)})
    with pytest.raises(ValueError, match="reconstruct"):
        EvidenceCard.from_json(artifact.read_text(encoding="utf-8"))
    before = artifact.read_bytes()
    with pytest.raises(ValueError, match="Existing artifact differs"):
        prepare(path)
    assert artifact.read_bytes() == before
