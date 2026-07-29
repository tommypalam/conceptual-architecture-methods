"""
record_sink.py — where run records go (DIP seam).

The runner depends on the `RecordSink` Protocol, never on the filesystem. This
means:
  - production uses `JsonFileSink` (immutable write-once JSON per call, the
    spec §1.3 discipline);
  - tests use `MemorySink` (no disk) — Liskov-substitutable, so the exact same
    runner code is exercised offline;
  - a future DB/S3 sink drops in without touching the runner (Open/Closed).

A sink answers two questions the runner needs: "does a record for this key
already exist?" (resume/idempotency) and "persist this record". Failures are a
separate stream so raw records stay clean (spec §1.3: failures.jsonl, never
retried in place).
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Protocol


class RecordSink(Protocol):
    def exists(self, key: str) -> bool: ...
    def write(self, key: str, record: dict[str, Any]) -> None: ...
    def write_failure(self, payload: dict[str, Any]) -> None: ...
    def read_all(self): ...   # -> Iterable[dict]  (records only, order unspecified)


class JsonFileSink:
    """
    Write-once JSON files under a root. `key` is a relative path like
    "null_a/S2/call_0007" → root/null_a/S2/call_0007.json. Refuses to overwrite
    an existing record (raw records are immutable).
    """

    def __init__(self, root: Path):
        self.root = Path(root)
        self.failures_path = self.root / "failures.jsonl"

    def _path(self, key: str) -> Path:
        return self.root / f"{key}.json"

    def exists(self, key: str) -> bool:
        return self._path(key).exists()

    def write(self, key: str, record: dict[str, Any]) -> None:
        path = self._path(key)
        if path.exists():
            raise FileExistsError(f"Record already exists (write-once): {path}")
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_name(f"{path.name}.tmp")
        with tmp.open("x", encoding="utf-8") as fh:
            json.dump(record, fh, indent=2, ensure_ascii=False)
            fh.write("\n")
            fh.flush()
            os.fsync(fh.fileno())
        os.rename(tmp, path)

    def write_failure(self, payload: dict[str, Any]) -> None:
        self.failures_path.parent.mkdir(parents=True, exist_ok=True)
        with self.failures_path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(payload, ensure_ascii=False) + "\n")

    def read_all(self):
        for path in sorted(self.root.rglob("*.json")):
            if path.name.endswith(".tmp"):
                continue
            try:
                yield json.loads(path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                continue


class MemorySink:
    """In-memory sink for tests. Same contract, no filesystem."""

    def __init__(self):
        self.records: dict[str, dict] = {}
        self.failures: list[dict] = []

    def exists(self, key: str) -> bool:
        return key in self.records

    def write(self, key: str, record: dict[str, Any]) -> None:
        if key in self.records:
            raise FileExistsError(f"Record already exists (write-once): {key}")
        self.records[key] = record

    def write_failure(self, payload: dict[str, Any]) -> None:
        self.failures.append(payload)

    def read_all(self):
        return iter(self.records.values())
