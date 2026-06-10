from typing import Optional, TypeGuard, Union

from fastapi import FastAPI, File, Request, UploadFile
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.background import BackgroundTask

from app.core.config import ALLOWED_EXTENSION, TEMPLATES_DIR
from app.services.converter import ConversionError, convert_pptx_to_pdf
from app.services.libreoffice import find_libreoffice
from app.utils.files import (
    cleanup_work_dir,
    create_work_dir,
    get_safe_upload_path,
    save_upload_file,
)


app = FastAPI(title="Nawala")
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


def render_index(request: Request, error: Optional[str] = None) -> HTMLResponse:
    return templates.TemplateResponse(request, "index.html", {"error": error})


def is_valid_pptx(filename: Optional[str]) -> TypeGuard[str]:
    return bool(filename and filename.lower().endswith(ALLOWED_EXTENSION))


@app.get("/", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
    return render_index(request)


@app.post("/convert", response_model=None)
async def convert(request: Request, file: UploadFile = File(...)) -> Union[HTMLResponse, FileResponse]:
    filename = file.filename
    if not is_valid_pptx(filename):
        await file.close()
        return render_index(request, "File harus berformat .pptx.")

    libreoffice_path = find_libreoffice()
    if not libreoffice_path:
        await file.close()
        return render_index(
            request,
            "LibreOffice tidak ditemukan. Install LibreOffice terlebih dahulu, lalu coba lagi.",
        )

    work_dir = create_work_dir()
    input_path = get_safe_upload_path(work_dir, filename)

    try:
        await save_upload_file(file, input_path)
        output_path = convert_pptx_to_pdf(libreoffice_path, input_path, work_dir)

        return FileResponse(
            path=output_path,
            media_type="application/pdf",
            filename=f"{input_path.stem}.pdf",
            background=BackgroundTask(cleanup_work_dir, work_dir),
        )
    except ConversionError as exc:
        cleanup_work_dir(work_dir)
        return render_index(request, str(exc))
    except Exception as exc:
        cleanup_work_dir(work_dir)
        return render_index(request, f"Terjadi error saat memproses file: {exc}")
    finally:
        await file.close()
