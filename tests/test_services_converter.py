import subprocess
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from app.services.converter import ConversionError, convert_pptx_to_pdf


def _mock_result(returncode: int = 0, stderr: str = "", stdout: str = "") -> MagicMock:
    result = MagicMock()
    result.returncode = returncode
    result.stderr = stderr
    result.stdout = stdout
    return result


def test_success(tmp_path: Path) -> None:
    input_path = tmp_path / "deck.pptx"
    input_path.touch()
    output_path = tmp_path / "deck.pdf"
    output_path.touch()

    with patch("subprocess.run", return_value=_mock_result(returncode=0)):
        result = convert_pptx_to_pdf("/usr/bin/soffice", input_path, tmp_path)

    assert result == output_path


def test_timeout_raises_conversion_error(tmp_path: Path) -> None:
    input_path = tmp_path / "deck.pptx"
    input_path.touch()

    with patch("subprocess.run", side_effect=subprocess.TimeoutExpired(cmd="soffice", timeout=120)):
        with pytest.raises(ConversionError, match="terlalu lama"):
            convert_pptx_to_pdf("/usr/bin/soffice", input_path, tmp_path)


def test_nonzero_returncode_raises_conversion_error(tmp_path: Path) -> None:
    input_path = tmp_path / "deck.pptx"
    input_path.touch()

    with patch("subprocess.run", return_value=_mock_result(returncode=1, stderr="error detail")):
        with pytest.raises(ConversionError, match="gagal"):
            convert_pptx_to_pdf("/usr/bin/soffice", input_path, tmp_path)


def test_nonzero_returncode_includes_stderr_in_message(tmp_path: Path) -> None:
    input_path = tmp_path / "deck.pptx"
    input_path.touch()

    with patch("subprocess.run", return_value=_mock_result(returncode=1, stderr="corrupt file")):
        with pytest.raises(ConversionError, match="corrupt file"):
            convert_pptx_to_pdf("/usr/bin/soffice", input_path, tmp_path)


def test_missing_output_raises_conversion_error(tmp_path: Path) -> None:
    input_path = tmp_path / "deck.pptx"
    input_path.touch()

    with patch("subprocess.run", return_value=_mock_result(returncode=0)):
        with pytest.raises(ConversionError, match="tidak terbentuk"):
            convert_pptx_to_pdf("/usr/bin/soffice", input_path, tmp_path)
