import json
import re
from pathlib import Path

import fitz


BASE_DIR = Path(__file__).resolve().parent.parent

SAMPLE_DOCS_DIR = BASE_DIR / "data" / "sample_docs"
UPLOAD_DIR = BASE_DIR / "data" / "uploads"
CHUNKS_DIR = BASE_DIR / "data" / "chunks"

SAMPLE_DOCS_DIR.mkdir(parents=True, exist_ok=True)
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
CHUNKS_DIR.mkdir(parents=True, exist_ok=True)


def clean_text(text: str) -> str:
    """清除多餘空白。"""
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def split_text(text: str, chunk_size: int = 750, overlap: int = 150) -> list[str]:
    """將長文字切成 chunks。"""
    text = clean_text(text)

    if not text:
        return []

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


def parse_pdf_to_chunks(pdf_path: Path) -> list[dict]:
    """將 PDF 逐頁解析並切成 chunks。"""
    doc = fitz.open(pdf_path)
    all_chunks = []

    for page_index, page in enumerate(doc, start=1):
        text = clean_text(page.get_text())
        page_chunks = split_text(text)

        for chunk_index, chunk_text in enumerate(page_chunks, start=1):
            all_chunks.append({
                "file_name": pdf_path.name,
                "page": page_index,
                "chunk_index": chunk_index,
                "content": chunk_text,
            })

    doc.close()
    return all_chunks


def save_chunks(pdf_path: Path) -> Path:
    """解析 PDF，並將 chunks 存成 JSON。"""
    chunks = parse_pdf_to_chunks(pdf_path)

    output_name = pdf_path.stem + "_chunks.json"
    output_path = CHUNKS_DIR / output_name

    with output_path.open("w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)

    return output_path


def parse_default_documents(force: bool = False) -> int:
    """
    自動解析 data/sample_docs 與 data/uploads 裡的 PDF。

    force=False：如果 chunks 已存在，就不重複解析。
    force=True：強制重新解析。
    """
    pdf_dirs = [SAMPLE_DOCS_DIR, UPLOAD_DIR]
    parsed_count = 0

    for pdf_dir in pdf_dirs:
        for pdf_path in pdf_dir.glob("*.pdf"):
            output_path = CHUNKS_DIR / f"{pdf_path.stem}_chunks.json"

            if output_path.exists() and not force:
                continue

            save_chunks(pdf_path)
            parsed_count += 1

    return parsed_count