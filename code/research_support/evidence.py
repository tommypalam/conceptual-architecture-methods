"""Immutable evidence snapshots and a provider-independent, read-only facade.

No API client, active-runner registration, ethical scoring, or profile sampling.
Providers are validated snapshots: construction can fail, but once constructed
both obey the same lookup contract irrespective of subsequent file changes.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
from pathlib import Path
from types import MappingProxyType
from typing import Iterable, Mapping, Protocol


def digest(text: str) -> str:
    return sha256(text.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class EvidenceCard:
    scenario_id: str
    source_path: str
    source_file_sha256: str
    body_sha256: str
    paragraphs: tuple[str, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.scenario_id, str) or not self.scenario_id:
            raise ValueError("A nonempty scenario ID is required")
        if not isinstance(self.source_path, str) or not self.source_path:
            raise ValueError("A source reference is required")
        for value in (self.source_file_sha256, self.body_sha256):
            if not isinstance(value, str) or len(value) != 64 or any(
                c not in "0123456789abcdef" for c in value
            ):
                raise ValueError("Invalid SHA-256")
        if not isinstance(self.paragraphs, tuple) or not self.paragraphs or any(
            not isinstance(p, str) or not p or p != p.strip() or "\n\n" in p
            for p in self.paragraphs
        ):
            raise ValueError("Paragraphs must be a nonempty immutable tuple")
        if digest("\n\n".join(self.paragraphs)) != self.body_sha256:
            raise ValueError("Evidence does not reconstruct the pinned dilemma body")

    def to_json(self) -> str:
        return json.dumps(asdict(self), ensure_ascii=False, indent=2) + "\n"

    @classmethod
    def from_json(cls, text: str) -> EvidenceCard:
        data = json.loads(text)
        if not isinstance(data, dict) or set(data) != set(cls.__dataclass_fields__):
            raise ValueError("Unexpected evidence schema")
        if not isinstance(data["paragraphs"], list):
            raise ValueError("Expected an array of paragraphs")
        data["paragraphs"] = tuple(data["paragraphs"])
        return cls(**data)


class UnknownScenarioError(KeyError):
    """The requested scenario is not in this provider's fixed catalogue."""


class EvidenceProvider(Protocol):
    """Lookup by string ID, returning the same immutable card on every call.

    Unknown IDs raise UnknownScenarioError(id), including path-like IDs.
    Lookup performs no I/O and changes neither provider nor source state.
    Implementations may reject invalid catalogues during construction.
    """

    def get(self, scenario_id: str) -> EvidenceCard: ...


class MemoryEvidenceProvider:
    def __init__(self, cards: Iterable[EvidenceCard]) -> None:
        catalogue: dict[str, EvidenceCard] = {}
        for card in cards:
            if card.scenario_id in catalogue:
                raise ValueError(f"Duplicate scenario: {card.scenario_id}")
            catalogue[card.scenario_id] = card
        self._cards = MappingProxyType(catalogue)

    def get(self, scenario_id: str) -> EvidenceCard:
        try:
            return self._cards[scenario_id]
        except KeyError:
            raise UnknownScenarioError(scenario_id) from None


class JsonEvidenceProvider:
    """Load trusted, hash-pinned local artifacts once, before serving lookups.

    Paths and expected raw-file hashes are supplied by the application, never
    by a model/tool caller. Source references in cards are metadata, not paths
    this provider opens. Pinning is integrity protection, not semantic approval.
    """

    def __init__(self, artifacts: Mapping[str, tuple[Path, str]]) -> None:
        cards = []
        for scenario_id, (path, expected_sha256) in artifacts.items():
            raw = path.read_bytes()
            if sha256(raw).hexdigest() != expected_sha256:
                raise ValueError(f"Artifact hash mismatch: {scenario_id}")
            card = EvidenceCard.from_json(raw.decode("utf-8"))
            if card.scenario_id != scenario_id:
                raise ValueError("Catalogue ID does not match evidence")
            cards.append(card)
        self._snapshot = MemoryEvidenceProvider(cards)

    def get(self, scenario_id: str) -> EvidenceCard:
        return self._snapshot.get(scenario_id)


# Draft model-facing addition, NOT approved or connected to an experiment.
GROUNDING_NOTE = (
    "The entries below repeat the dilemma in its original order. Keep reports, "
    "warnings, and conditional consequences in their stated scope. Details not "
    "stated are unspecified, not established as present or absent. If you propose "
    "additional actions or procedures, distinguish those proposals from facts "
    "already given in the dilemma."
)


def render_evidence_card(card: EvidenceCard) -> str:
    entries = "\n\n".join(
        f"[E{i}] {paragraph}" for i, paragraph in enumerate(card.paragraphs, 1)
    )
    return f"Dilemma evidence reference\n\n{GROUNDING_NOTE}\n\n{entries}"


@dataclass(frozen=True)
class EvidenceTool:
    """Optional local facade, dependent only on the narrow provider protocol.

    This is not an SDK tool registration or construct-injection algorithm.
    Output equals the direct renderer; an LLM tool call may still behave
    differently from a text overlay and would need separate validation.
    """

    provider: EvidenceProvider

    def read(self, scenario_id: str) -> str:
        return render_evidence_card(self.provider.get(scenario_id))
