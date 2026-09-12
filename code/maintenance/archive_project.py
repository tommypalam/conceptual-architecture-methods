"""Move an explicit archive plan within a workspace, preserving every file byte.

Preparation hashes all sources and refuses collisions, aliases and overlapping
moves. Apply requires that inventory and verifies the destination after each move.
This maintenance tool never dispatches model requests or deletes record files.
"""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import stat


def contained(root: Path, name: str) -> Path:
    relative = Path(name)
    if relative.is_absolute() or not relative.parts or ".." in relative.parts:
        raise ValueError(f"Require a relative workspace path: {name}")
    path = root / relative
    resolved = path.resolve()
    if not resolved.is_relative_to(root.resolve()) or resolved == root.resolve():
        raise ValueError(f"Path escapes workspace or names its root: {name}")
    if relative.parts[0] in {".git", ".agents", ".codex"}:
        raise ValueError(f"Protected administration path: {name}")
    for part in (path, *path.parents):
        if part == root:
            break
        if part.exists() and (part.is_symlink() or getattr(part.lstat(), "st_file_attributes", 0)
                              & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)):
            raise ValueError(f"Refuse a symlink or reparse point: {part}")
    return path


def sha256(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def files_under(path: Path) -> list[Path]:
    if path.is_file():
        return [path]
    return sorted(p for p in path.rglob("*") if p.is_file())


def prepare(root: Path, moves: list[dict]) -> dict:
    roots = []
    entries = []
    for move in moves:
        source = contained(root, move["source"])
        destination = contained(root, move["destination"])
        if not source.exists() or destination.exists():
            raise ValueError(f"Missing source or occupied destination: {move}")
        if not destination.relative_to(root).parts[0] == "archive":
            raise ValueError("Every destination must be inside archive/")
        if destination.is_relative_to(source):
            raise ValueError("Cannot move a directory into itself")
        for previous in roots:
            if source.is_relative_to(previous) or previous.is_relative_to(source):
                raise ValueError("Overlapping move sources")
        roots.append(source)
        source_files = files_under(source)
        if not source_files:
            raise ValueError(f"Empty move source: {source}")
        for path in source_files:
            contained(root, path.relative_to(root).as_posix())
            target = destination / path.relative_to(source) if source.is_dir() else destination
            entries.append({"source": path.relative_to(root).as_posix(),
                            "destination": target.relative_to(root).as_posix(),
                            "bytes": path.stat().st_size})
    destinations = [e["destination"].casefold() for e in entries]
    if len(set(destinations)) != len(destinations):
        raise ValueError("Duplicate destination files")
    print(f"Hashing {len(entries)} files before relocation", flush=True)
    with ThreadPoolExecutor(max_workers=8) as pool:
        for number, (entry, digest) in enumerate(zip(entries, pool.map(
                lambda item: sha256(root / item["source"]), entries)), 1):
            entry["sha256"] = digest
            if number % 5000 == 0:
                print(f"Hashed {number}/{len(entries)}", flush=True)
    return {"schema_version": 1, "moves": moves, "files": entries,
            "file_count": len(entries), "total_bytes": sum(e["bytes"] for e in entries)}


def verify(root: Path, inventory: dict, side: str) -> None:
    if side not in {"source", "destination"}:
        raise ValueError(side)
    def check(entry):
        path = contained(root, entry[side])
        if not path.is_file() or path.stat().st_size != entry["bytes"]:
            raise ValueError(f"Missing or resized file: {path}")
        if sha256(path) != entry["sha256"]:
            raise ValueError(f"Changed bytes: {path}")
    with ThreadPoolExecutor(max_workers=8) as pool:
        for _ in pool.map(check, inventory["files"]):
            pass


def apply(root: Path, inventory: dict) -> None:
    # Check every source and collision before the first mutation.
    for move in inventory["moves"]:
        source = contained(root, move["source"])
        destination = contained(root, move["destination"])
        if not source.exists() or destination.exists():
            raise ValueError(f"Source missing or destination occupied: {move}")
        expected = {e["source"] for e in inventory["files"] if
                    e["source"] == move["source"] or e["source"].startswith(move["source"] + "/")}
        actual = {p.relative_to(root).as_posix() for p in files_under(source)}
        if expected != actual:
            raise ValueError(f"Source file set changed: {move['source']}")
    verify(root, inventory, "source")
    for move in inventory["moves"]:
        source = contained(root, move["source"])
        destination = contained(root, move["destination"])
        destination.parent.mkdir(parents=True, exist_ok=True)
        # Path.rename on Windows refuses an occupied destination. Same-volume move.
        source.rename(destination)
        subset = {"files": [e for e in inventory["files"] if e["source"] == move["source"]
                            or e["source"].startswith(move["source"] + "/")]}
        verify(root, subset, "destination")
        print(f"Verified {move['source']} -> {move['destination']} ({len(subset['files'])} files)", flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--plan", type=Path)
    parser.add_argument("--inventory", type=Path, required=True)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    if args.apply and args.verify:
        parser.error("Choose --apply or --verify")
    if args.apply or args.verify:
        inventory = json.loads(args.inventory.read_text(encoding="utf-8"))
        if args.apply:
            apply(root, inventory)
        verify(root, inventory, "destination")
        print(f"Verified {inventory['file_count']} destination files, {inventory['total_bytes']} bytes.")
    else:
        if args.plan is None:
            parser.error("Preparation requires --plan")
        inventory = prepare(root, json.loads(args.plan.read_text(encoding="utf-8"))["moves"])
        with args.inventory.open("x", encoding="utf-8", newline="\n") as stream:
            json.dump(inventory, stream, indent=2)
            stream.write("\n")
        print(f"Prepared inventory: {args.inventory}")


if __name__ == "__main__":
    main()
