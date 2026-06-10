from pathlib import Path
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app
from app.services.converter import ConversionError

client = TestClient(app)

FAKE_PPTX = ("presentation.pptx", b"PK fake pptx content", "application/vnd.openxmlformats-officedocument.presentationml.presentation")
FAKE_DOCX = ("document.docx", b"PK fake docx content", "application/octet-stream")


def test_index_returns_200() -> None:
    response = client.get("/")
    assert response.status_code == 200


def test_index_contains_form() -> None:
    response = client.get("/")
    assert 'action="/convert"' in response.text


def test_convert_rejects_non_pptx() -> None:
    response = client.post("/convert", files={"file": FAKE_DOCX})
    assert response.status_code == 200
    assert "pptx" in response.text.lower()


def test_convert_shows_error_when_libreoffice_missing() -> None:
    with patch("app.main.find_libreoffice", return_value=None):
        response = client.post("/convert", files={"file": FAKE_PPTX})
    assert response.status_code == 200
    assert "LibreOffice" in response.text


def test_convert_shows_conversion_error_message() -> None:
    with patch("app.main.find_libreoffice", return_value="/usr/bin/soffice"), \
         patch("app.main.convert_pptx_to_pdf", side_effect=ConversionError("Proses konversi gagal.")):
        response = client.post("/convert", files={"file": FAKE_PPTX})
    assert response.status_code == 200
    assert "gagal" in response.text.lower()


def test_convert_shows_generic_error_on_unexpected_exception() -> None:
    with patch("app.main.find_libreoffice", return_value="/usr/bin/soffice"), \
         patch("app.main.convert_pptx_to_pdf", side_effect=RuntimeError("unexpected")):
        response = client.post("/convert", files={"file": FAKE_PPTX})
    assert response.status_code == 200
    assert "error" in response.text.lower()


def test_convert_returns_pdf_on_success(tmp_path: Path) -> None:
    pdf_path = tmp_path / "presentation.pdf"
    pdf_path.write_bytes(b"%PDF-1.4 fake pdf")

    with patch("app.main.find_libreoffice", return_value="/usr/bin/soffice"), \
         patch("app.main.create_work_dir", return_value=tmp_path), \
         patch("app.main.save_upload_file"), \
         patch("app.main.convert_pptx_to_pdf", return_value=pdf_path), \
         patch("app.main.cleanup_work_dir"):
        response = client.post("/convert", files={"file": FAKE_PPTX})

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"


def test_convert_pdf_filename_matches_input(tmp_path: Path) -> None:
    pdf_path = tmp_path / "presentation.pdf"
    pdf_path.write_bytes(b"%PDF-1.4 fake pdf")

    with patch("app.main.find_libreoffice", return_value="/usr/bin/soffice"), \
         patch("app.main.create_work_dir", return_value=tmp_path), \
         patch("app.main.save_upload_file"), \
         patch("app.main.convert_pptx_to_pdf", return_value=pdf_path), \
         patch("app.main.cleanup_work_dir"):
        response = client.post("/convert", files={"file": FAKE_PPTX})

    content_disposition = response.headers.get("content-disposition", "")
    assert "presentation.pdf" in content_disposition
