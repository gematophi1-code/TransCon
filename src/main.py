import mimetypes
import tempfile
from pathlib import Path
from urllib.parse import quote

from fastapi import FastAPI, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from src.converter.documents import pdf_to_txt, txt_to_pdf
from src.converter.image import convert_image

app = FastAPI(title="TransCon")
app.mount("/static", StaticFiles(directory="src/static"), name="static")
templates = Jinja2Templates(directory="src/templates")

_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"}


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/convert")
async def convert(file: UploadFile = File(...), target_format: str = Form(...)):
    suffix = Path(file.filename).suffix.lower()
    target_format = target_format.lower()

    with tempfile.TemporaryDirectory() as tmp_dir:
        input_path = Path(tmp_dir) / file.filename
        input_path.write_bytes(await file.read())

        try:
            if suffix in _IMAGE_EXTENSIONS:
                output_path = convert_image(input_path, target_format)
            elif suffix == ".txt" and target_format == "pdf":
                output_path = txt_to_pdf(input_path)
            elif suffix == ".pdf" and target_format == "txt":
                output_path = pdf_to_txt(input_path)
            else:
                raise HTTPException(status_code=400, detail="Неподдерживаемая пара форматов")
        except ValueError as error:
            raise HTTPException(status_code=400, detail=str(error))

        # Важно: читаем байты результата, пока временная папка ещё жива
        content = output_path.read_bytes()
        media_type, _ = mimetypes.guess_type(output_path.name)

    return Response(
        content=content,
        media_type=media_type or "application/octet-stream",
        headers={
            "Content-Disposition": f"attachment; filename*=UTF-8''{quote(output_path.name)}"
        },
    )