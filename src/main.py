import mimetypes
import tempfile
import zipfile
from urllib.parse import quote
from pathlib import Path

from fastapi import FastAPI, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from PIL import UnidentifiedImageError
from docx.opc.exceptions import PackageNotFoundError
from pypdf.errors import PdfReadError

from src.converter.documents import docx_to_pdf, docx_to_txt, pdf_to_docx, pdf_to_txt, txt_to_docx, txt_to_pdf
from src.converter.image import convert_image

_DOCUMENT_CONVERTERS = {
    ("txt", "pdf"): txt_to_pdf,
    ("pdf", "txt"): pdf_to_txt,
    ("docx", "txt"): docx_to_txt,
    ("txt", "docx"): txt_to_docx,
    ("docx", "pdf"): docx_to_pdf,
    ("pdf", "docx"): pdf_to_docx,
}

app = FastAPI(title="TransCon")
app.mount("/static", StaticFiles(directory="src/static"), name="static")
templates = Jinja2Templates(directory="src/templates")

_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"}
_MAX_FILE_SIZE = 20 * 1024 * 1024  # 20 МБ


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(request, "index.html")


@app.post("/convert")
async def convert(file: UploadFile = File(...), target_format: str = Form(...)):
    suffix = Path(file.filename).suffix.lower()
    target_format = target_format.lower()

    content = await file.read()
    if len(content) > _MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="Файл слишком большой (максимум 20 МБ)")

    with tempfile.TemporaryDirectory() as tmp_dir:
        input_path = Path(tmp_dir) / file.filename
        input_path.write_bytes(content)

        try:
            if suffix in _IMAGE_EXTENSIONS:
                output_path = convert_image(input_path, target_format)
            elif (converter := _DOCUMENT_CONVERTERS.get((suffix.lstrip("."), target_format))) is not None:
                output_path = converter(input_path)
            else:
                raise HTTPException(status_code=400, detail="Неподдерживаемая пара форматов")
        except (
            ValueError,
            UnidentifiedImageError,
            PdfReadError,
            PackageNotFoundError,
            zipfile.BadZipFile,
            OSError,
        ) as error:
            raise HTTPException(
                status_code=400,
                detail="Не удалось обработать файл — возможно, он повреждён или не соответствует ожидаемому формату",
            )

        result_content = output_path.read_bytes()
        media_type, _ = mimetypes.guess_type(output_path.name)

    return Response(
        content=result_content,
        media_type=media_type or "application/octet-stream",
        headers={
            "Content-Disposition": f"attachment; filename*=UTF-8''{quote(output_path.name)}"
        },
    )