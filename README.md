# 保險文件智慧查詢系統

## 專案簡介

本專案模擬保險公司內部文件查詢情境，使用 Python 將保險 PDF 文件解析成 JSON，並將文件內容切分為可查詢段落。使用者可透過網頁輸入問題，系統會從保險文件中找出相關段落，並顯示來源檔案、頁碼與相關分數。

此專案作為國泰人壽實習申請作品，展示基礎軟體開發、文件解析、資料處理、查詢紀錄與系統化開發能力。

## 使用技術

- Python
- FastAPI
- Jinja2
- Bootstrap 5
- SQLite
- PyMuPDF

## 系統功能

### 1. 文件解析

將 PDF 文件逐頁解析，保留：

- 檔案名稱
- 頁碼
- 文字內容

### 2. 段落切分

將解析後的長篇文字切分成 chunks，方便後續查詢與 RAG 擴充。

### 3. 文件查詢

使用者可在網頁輸入問題，系統會從 chunks 中找出相關內容，並顯示：

- 來源檔案
- 頁碼
- 相關分數
- 內容片段

### 4. 查詢紀錄

系統會將每次查詢記錄於 SQLite，包含：

- 查詢時間
- 使用者問題
- 最相關來源檔案
- 頁碼
- 相關分數

## 專案資料夾結構

```text
insurance-doc-query/
│
├── app/
│   ├── main.py
│   ├── parser.py
│   ├── chunker.py
│   ├── search.py
│   ├── db.py
│   └── templates/
│       ├── index.html
│       └── history.html
│
├── data/
│   ├── sample_docs/
│   ├── parsed/
│   ├── chunks/
│   └── app.db
│
├── requirements.txt
└── README.md