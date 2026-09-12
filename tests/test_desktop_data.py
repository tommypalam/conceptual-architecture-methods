import hashlib
import importlib.util
from pathlib import Path

import pytest

spec = importlib.util.spec_from_file_location(
    "verify_desktop_data", Path(__file__).resolve().parents[1] / "code/maintenance/verify_desktop_data.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_existing_missing_and_changed_files(tmp_path):
    data = b'original response\r\n'
    target = tmp_path / "record.json"
    target.write_bytes(data)
    manifest = {"files": [{"path": "record.json", "bytes": len(data),
                            "sha256": hashlib.sha256(data).hexdigest()}]}
    assert module.verify(tmp_path, manifest)["all_verified"]
    target.write_bytes(b'x' * len(data))
    assert module.verify(tmp_path, manifest)["failures"][0]["error"] == "checksum mismatch"
    target.unlink()
    assert module.verify(tmp_path, manifest)["failures"][0]["error"] == "missing"


def test_refuses_paths_outside_checkout(tmp_path):
    with pytest.raises(ValueError):
        module.verify(tmp_path, {"files": [{"path": "../outside", "bytes": 0, "sha256": ""}]})


def test_refuses_duplicate_paths(tmp_path):
    row = {"path": "a", "bytes": 0, "sha256": ""}
    with pytest.raises(ValueError):
        module.verify(tmp_path, {"files": [row, row]})
