from pathlib import Path

import pytest

from app.utils.files import cleanup_work_dir, create_work_dir, get_safe_upload_path


def test_get_safe_upload_path_normal(tmp_path: Path) -> None:
    result = get_safe_upload_path(tmp_path, "presentation.pptx")
    assert result == tmp_path / "presentation.pptx"


def test_get_safe_upload_path_strips_directory_traversal(tmp_path: Path) -> None:
    result = get_safe_upload_path(tmp_path, "../../etc/passwd")
    assert result == tmp_path / "passwd"
    assert ".." not in result.parts


def test_get_safe_upload_path_strips_nested_path(tmp_path: Path) -> None:
    result = get_safe_upload_path(tmp_path, "subdir/file.pptx")
    assert result == tmp_path / "file.pptx"


def test_create_work_dir_creates_directory(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("app.utils.files.TEMP_DIR", tmp_path)
    work_dir = create_work_dir()
    assert work_dir.exists()
    assert work_dir.is_dir()


def test_create_work_dir_returns_unique_paths(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("app.utils.files.TEMP_DIR", tmp_path)
    assert create_work_dir() != create_work_dir()


def test_cleanup_work_dir_removes_directory_and_contents(tmp_path: Path) -> None:
    work_dir = tmp_path / "work"
    work_dir.mkdir()
    (work_dir / "file.pptx").write_bytes(b"data")
    cleanup_work_dir(work_dir)
    assert not work_dir.exists()


def test_cleanup_work_dir_nonexistent_does_not_raise(tmp_path: Path) -> None:
    cleanup_work_dir(tmp_path / "nonexistent")
