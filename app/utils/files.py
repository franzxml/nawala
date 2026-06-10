import shutil
import uuid
from pathlib import Path

from fastapi import UploadFile

from app.core.config import TEMP_DIR


def create_work_dir() -> Path:
    work_dir = TEMP_DIR / str(uuid.uuid4())
    work_dir.mkdir(parents=True, exist_ok=True)
    return work_dir


def cleanup_work_dir(work_dir: Path) -> None:
    shutil.rmtree(work_dir, ignore_errors=True)


def get_safe_upload_path(work_dir: Path, filename: str) -> Path:
    return work_dir / Path(filename).name


async def save_upload_file(upload_file: UploadFile, destination: Path) -> None:
    content = await upload_file.read()
    destination.write_bytes(content)
