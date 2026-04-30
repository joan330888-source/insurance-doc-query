import sqlite3
from datetime import datetime, timezone, timedelta
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "app.db"

TAIPEI_TZ = timezone(timedelta(hours=8))


def get_connection():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS query_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            question TEXT NOT NULL,
            answer_summary TEXT,
            top_file TEXT,
            top_page INTEGER,
            top_score INTEGER,
            top_relevance TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_query_history(question: str, results: list[dict], answer: dict | None = None):
    init_db()

    question = (question or "").strip()
    if not question:
        return

    created_at = datetime.now(TAIPEI_TZ).strftime("%Y-%m-%d %H:%M:%S")

    answer_summary = ""
    if answer:
        answer_summary = answer.get("summary", "")

    top_file = ""
    top_page = None
    top_score = None
    top_relevance = ""

    if results:
        top_result = results[0]
        top_file = top_result.get("file_name", "")
        top_page = top_result.get("page", None)
        top_score = top_result.get("score", None)
        top_relevance = top_result.get("relevance", "")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO query_history (
            created_at,
            question,
            answer_summary,
            top_file,
            top_page,
            top_score,
            top_relevance
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        created_at,
        question,
        answer_summary,
        top_file,
        top_page,
        top_score,
        top_relevance
    ))

    conn.commit()
    conn.close()


def get_query_history(limit: int = 100) -> list[dict]:
    init_db()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            created_at,
            question,
            answer_summary,
            top_file,
            top_page,
            top_score,
            top_relevance
        FROM query_history
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]