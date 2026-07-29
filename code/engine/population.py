"""
population.py — paired-agent population draw and deterministic exposure ordering.

Implements spec §5.1 (single hash-locked population of N_paired = 200 profiles,
drawn once from the Gaussian copula and held fixed across all configurations and
all problems) and §5.2 (per-agent, per-problem randomised configuration exposure
order, deterministic from a seed so runs are reproducible and recoverable).

The population is the paired-agent backbone: the same agent_id maps to a fixed
parameter draw, exposed within-subjects to every configuration (thesis §7.5.5).
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, asdict
from pathlib import Path

import numpy as np

import utils

N_PAIRED_DEFAULT = 200


@dataclass(frozen=True)
class Agent:
    agent_id: int
    parameters: dict[str, float]

    def as_record(self) -> dict:
        return {"agent_id": self.agent_id, "parameters": self.parameters}


class Population:
    """A hash-locked set of agent profiles. Immutable once written to disk."""

    def __init__(self, agents: list[Agent], seed: int, n: int):
        self.agents = agents
        self.seed = seed
        self.n = n

    # ---- construction ---------------------------------------------------- #

    @classmethod
    def draw(cls, n: int = N_PAIRED_DEFAULT, *, seed: int) -> "Population":
        """
        Draw n agents from the Gaussian copula (utils.sample_agents), rounding
        parameter values to 4 dp for stable hashing and record equality.
        """
        x = utils.sample_agents(n, seed=seed)
        agents = [
            Agent(agent_id=i + 1,
                  parameters={name: round(float(x[i, j]), 4)
                              for j, name in enumerate(utils.PARAM_NAMES)})
            for i in range(n)
        ]
        return cls(agents, seed=seed, n=n)

    # ---- integrity ------------------------------------------------------- #

    def content_hash(self) -> str:
        """Stable SHA-256 over the ordered agent records — the population lock."""
        blob = json.dumps([a.as_record() for a in self.agents],
                          sort_keys=True, separators=(",", ":")).encode()
        return hashlib.sha256(blob).hexdigest()

    def parameter_matrix(self) -> np.ndarray:
        return np.array([[a.parameters[name] for name in utils.PARAM_NAMES]
                         for a in self.agents])

    # ---- persistence ----------------------------------------------------- #

    def to_dict(self) -> dict:
        return {
            "schema_version": "1.0",
            "n_agents": self.n,
            "seed": self.seed,
            "parameter_order": list(utils.PARAM_NAMES),
            "content_hash": self.content_hash(),
            "agents": [a.as_record() for a in self.agents],
        }

    def write_locked(self, path: Path) -> str:
        """
        Write the population once. If the file exists, verify its hash matches
        (idempotent re-draw with the same seed) and refuse to overwrite a
        different population (spec §5.1: mid-phase re-draws not permitted;
        a genuine re-draw must be a new file, e.g. population_v2.json).
        """
        payload = self.to_dict()
        if path.exists():
            existing = json.loads(path.read_text(encoding="utf-8"))
            if existing.get("content_hash") != payload["content_hash"]:
                raise FileExistsError(
                    f"{path} holds a DIFFERENT locked population "
                    f"({existing.get('content_hash','?')[:12]} vs "
                    f"{payload['content_hash'][:12]}). A re-draw must be a new file.")
            return payload["content_hash"]
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_suffix(path.suffix + ".tmp")
        with tmp.open("x", encoding="utf-8") as fh:
            json.dump(payload, fh, indent=2, ensure_ascii=False)
            fh.write("\n")
        tmp.rename(path)
        return payload["content_hash"]

    @classmethod
    def load(cls, path: Path) -> "Population":
        data = json.loads(path.read_text(encoding="utf-8"))
        agents = [Agent(agent_id=a["agent_id"], parameters=a["parameters"])
                  for a in data["agents"]]
        pop = cls(agents, seed=data["seed"], n=data["n_agents"])
        if pop.content_hash() != data.get("content_hash"):
            raise ValueError(f"{path}: content hash mismatch — file was modified.")
        return pop


# --------------------------------------------------------------------------- #
# Deterministic exposure ordering (spec §5.2)
# --------------------------------------------------------------------------- #

def exposure_order(config_codes: list[str], *, seed: int, agent_id: int,
                   problem_id: str) -> list[str]:
    """
    Deterministic per-(agent, problem) permutation of the configuration list.
    Two agents see configurations in different orders; the same (seed, agent,
    problem) always yields the same order — so a mid-run failure can be resumed
    without altering exposure sequence, and order effects cannot confound
    configuration effects (spec §5.2).
    """
    key = f"{seed}:{agent_id}:{problem_id}".encode()
    local_seed = int(hashlib.sha256(key).hexdigest(), 16) % (2 ** 32)
    rng = np.random.default_rng(local_seed)
    idx = rng.permutation(len(config_codes))
    return [config_codes[i] for i in idx]
