# app.py
from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import FileResponse, JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from services.rag_pipeline import RAGPipeline
import uvicorn
import shutil
from openpyxl import Workbook
from pathlib import Path
import json
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(title="Invoice Processing with OCR + NLP + RAG")

static_dir = BASE_DIR / "static"
templates_dir = BASE_DIR / "templates"

app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
templates = Jinja2Templates(directory=str(templates_dir))

rag = RAGPipeline()

DATA_DIR = BASE_DIR / "data"
EXPORTS_DIR = BASE_DIR / "exports"
HISTORY_FILE = BASE_DIR / "history.json"

DATA_DIR.mkdir(exist_ok=True)
EXPORTS_DIR.mkdir(exist_ok=True)

# ensure history file exists
if not HISTORY_FILE.exists():
    HISTORY_FILE.write_text("[]", encoding="utf-8")


def read_history():
    try:
        return json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
    except Exception:
        return []


def append_history(entry: dict):
    h = read_history()
    h.insert(0, entry)  # newest first
    HISTORY_FILE.write_text(json.dumps(h, indent=2), encoding="utf-8")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/upload-invoice")
async def upload_invoice(file: UploadFile = File(...)):
    filename = Path(file.filename).name
    file_path = DATA_DIR / filename

    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # Process invoice with RAG pipeline
    result = rag.add_invoice(str(file_path))
    fields = result.get("fields", {})

    # Create Excel export
    excel_filename = f"{file_path.stem}.xlsx"
    excel_path = EXPORTS_DIR / excel_filename

    wb = Workbook()
    ws = wb.active
    ws.title = "Invoice Data"
    ws.append(["Field", "Value"])
    for key, value in fields.items():
        ws.append([key, value])
    wb.save(excel_path)

    # Append to history
    entry = {
        "filename": filename,
        "uploaded_at": datetime.utcnow().isoformat() + "Z",
        "fields": fields,
        "excel_file": f"/download-excel/{excel_filename}"
    }
    append_history(entry)

    return {
        "filename": filename,
        "message": "Invoice uploaded & processed successfully!",
        "fields": fields,
        "excel_file": f"/download-excel/{excel_filename}"
    }


@app.get("/download-excel/{filename}")
async def download_excel(filename: str):
    file_path = EXPORTS_DIR / filename
    if file_path.exists():
        return FileResponse(
            path=str(file_path),
            filename=filename,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    return JSONResponse({"error": "File not found"}, status_code=404)


@app.get("/history")
async def get_history():
    """Return upload history (newest first)."""
    return {"history": read_history()}


@app.post("/query")
async def query_invoice(query: str):
    answer = rag.generate(query)
    return {"query": query, "answer": answer}


if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
