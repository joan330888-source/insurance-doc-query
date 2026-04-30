from fastapi import FastAPI, File, Request, UploadFile
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from app.db import get_query_history, init_db, save_query_history
from app.parser import parse_default_documents, save_chunks
from app.search import build_answer, get_corpus_stats, search_documents
from app.storage import list_available_files, save_uploaded_file


app = FastAPI(title="保險文件 RAG Assistant")

templates = Jinja2Templates(directory="app/templates")


@app.on_event("startup")
def startup_event():
    """
    啟動伺服器時，自動解析 data/sample_docs 和 data/uploads 裡的 PDF，
    並初始化 SQLite 查詢紀錄資料庫。
    """
    init_db()
    parse_default_documents(force=False)


@app.get("/")
def home(request: Request):
    parse_default_documents(force=False)
    stats = get_corpus_stats()

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "question": "",
            "answer": None,
            "files": list_available_files(),
            "stats": stats,
        },
    )


@app.get("/search")
def search(request: Request, question: str = ""):
    parse_default_documents(force=False)

    question = question.strip()
    results = search_documents(question) if question else []
    answer = build_answer(question, results) if question else None

    if question:
        save_query_history(question, results, answer)

    stats = get_corpus_stats()

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "question": question,
            "answer": answer,
            "files": list_available_files(),
            "stats": stats,
        },
    )


@app.get("/history")
def history(request: Request):
    records = get_query_history(limit=100)

    return templates.TemplateResponse(
        request=request,
        name="history.html",
        context={
            "records": records,
        },
    )


@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    pdf_path = await save_uploaded_file(file)

    if pdf_path is not None:
        save_chunks(pdf_path)

    return RedirectResponse(url="/", status_code=303)