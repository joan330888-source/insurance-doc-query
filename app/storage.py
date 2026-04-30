from pathlib import Path

from fastapi import UploadFile


BASE_DIR = Path(__file__).resolve().parent.parent

SAMPLE_DOCS_DIR = BASE_DIR / "data" / "sample_docs"
UPLOAD_DIR = BASE_DIR / "data" / "uploads"

SAMPLE_DOCS_DIR.mkdir(parents=True, exist_ok=True)
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def list_available_files() -> list[str]:
    """列出 data/sample_docs 與 data/uploads 裡的 PDF。"""
    files = []

    for path in SAMPLE_DOCS_DIR.glob("*.pdf"):
        files.append(path.name)

    for path in UPLOAD_DIR.glob("*.pdf"):
        if path.name not in files:
            files.append(path.name)

    return sorted(files)


def list_uploaded_files() -> list[str]:
    """保留舊函式名稱，避免其他地方匯入失敗。"""
    return list_available_files()


async def save_uploaded_file(file: UploadFile) -> Path | None:
    """儲存使用者上傳的 PDF 到 data/uploads。"""
    if not file.filename:
        return None

    if not file.filename.lower().endswith(".pdf"):
        return None

    output_path = UPLOAD_DIR / file.filename
    content = await file.read()

    if not content:
        return None

    with output_path.open("wb") as f:
        f.write(content)

    return output_path