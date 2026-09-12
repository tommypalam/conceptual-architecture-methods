"""Read-only checksum verification of the desktop data-transfer manifest."""

import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path


def verify(root, manifest):
    root = root.resolve()
    rows = manifest["files"]
    names = [row["path"] for row in rows]
    if len(names) != len(set(names)):
        raise ValueError("Duplicate manifest paths")

    def check(row):
        relative = Path(row["path"])
        path = (root / relative).resolve()
        if relative.is_absolute() or ".." in relative.parts or not path.is_relative_to(root):
            raise ValueError("Manifest path escapes the project")
        if not path.is_file():
            return {"path": row["path"], "error": "missing"}
        if path.stat().st_size != row["bytes"]:
            return {"path": row["path"], "error": "size mismatch"}
        with path.open("rb") as stream:
            digest = hashlib.file_digest(stream, "sha256").hexdigest()
        if digest != row["sha256"]:
            return {"path": row["path"], "error": "checksum mismatch"}
        return None

    failures = []
    with ThreadPoolExecutor(max_workers=8) as pool:
        for n, result in enumerate(pool.map(check, rows), 1):
            if result:
                failures.append(result)
            if n % 20000 == 0:
                print(f"Checked {n}/{len(rows)}", flush=True)
    return {"files_checked": len(rows), "failures": failures, "all_verified": not failures}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    result = verify(args.root, json.loads(args.manifest.read_text(encoding="utf-8")))
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["all_verified"] else 1)


if __name__ == "__main__":
    main()
