import importlib.util
from pathlib import Path

import pytest

spec = importlib.util.spec_from_file_location(
    "archive_project", Path(__file__).resolve().parents[1] / "code/maintenance/archive_project.py")
archive = importlib.util.module_from_spec(spec)
spec.loader.exec_module(archive)


def fixture_plan(root):
    source = root / "old/records"
    source.mkdir(parents=True)
    (source / "response.json").write_bytes(b'{"raw":"unchanged"}\r\n')
    return [{"source": "old", "destination": "archive/phase0/runs"}]


def test_preserves_raw_bytes_and_moves_once(tmp_path):
    moves = fixture_plan(tmp_path)
    inventory = archive.prepare(tmp_path, moves)
    archive.apply(tmp_path, inventory)
    assert not (tmp_path / "old").exists()
    assert (tmp_path / "archive/phase0/runs/records/response.json").read_bytes() == b'{"raw":"unchanged"}\r\n'
    archive.verify(tmp_path, inventory, "destination")
    with pytest.raises(ValueError):
        archive.apply(tmp_path, inventory)


@pytest.mark.parametrize("path", ["../elsewhere", ".git/index", ".", "archive/../../elsewhere"])
def test_rejects_unsafe_paths(tmp_path, path):
    with pytest.raises(ValueError):
        archive.contained(tmp_path, path)


def test_changed_response_stops_before_mutation(tmp_path):
    inventory = archive.prepare(tmp_path, fixture_plan(tmp_path))
    (tmp_path / "old/records/response.json").write_bytes(b'changed')
    with pytest.raises(ValueError):
        archive.apply(tmp_path, inventory)
    assert (tmp_path / "old").exists()
    assert not (tmp_path / "archive").exists()


def test_added_file_stops_before_mutation(tmp_path):
    inventory = archive.prepare(tmp_path, fixture_plan(tmp_path))
    (tmp_path / "old/extra.txt").write_text("unexpected")
    with pytest.raises(ValueError):
        archive.apply(tmp_path, inventory)
    assert (tmp_path / "old").exists()


def test_collision_is_not_overwritten(tmp_path):
    inventory = archive.prepare(tmp_path, fixture_plan(tmp_path))
    destination = tmp_path / "archive/phase0/runs"
    destination.mkdir(parents=True)
    (destination / "keep.txt").write_text("keep")
    with pytest.raises(ValueError):
        archive.apply(tmp_path, inventory)
    assert (destination / "keep.txt").read_text() == "keep"
    assert (tmp_path / "old").exists()
