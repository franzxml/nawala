import subprocess
from pathlib import Path

from app.core.config import CONVERSION_TIMEOUT_SECONDS


class ConversionError(Exception):
    """Error yang aman ditampilkan ke pengguna."""


def convert_pptx_to_pdf(
    libreoffice_path: str,
    input_path: Path,
    output_dir: Path,
) -> Path:
    output_path = output_dir / input_path.with_suffix(".pdf").name
    command = [
        libreoffice_path,
        "--headless",
        "--convert-to",
        "pdf",
        "--outdir",
        str(output_dir),
        str(input_path),
    ]

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=CONVERSION_TIMEOUT_SECONDS,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise ConversionError(
            "Proses konversi terlalu lama dan dihentikan. Coba gunakan file PPTX yang lebih kecil."
        ) from exc

    if result.returncode != 0:
        detail = (result.stderr or result.stdout or "").strip()
        message = "Proses konversi gagal."
        if detail:
            message = f"{message} Detail: {detail}"
        raise ConversionError(message)

    if not output_path.exists():
        raise ConversionError(
            "File PDF hasil konversi tidak terbentuk. Pastikan file PPTX valid dan tidak rusak."
        )

    return output_path

