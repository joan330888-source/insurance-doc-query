import os
from openai import OpenAI


def generate_ai_answer(question: str, results: list[dict], fallback: str = "") -> str:
    """
    使用大型語言模型根據檢索到的保險條款產生回答。
    如果沒有設定 OPENAI_API_KEY，或 API 呼叫失敗，就回傳原本的規則式回答。
    """

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        return fallback

    if not results:
        return fallback

    client = OpenAI(api_key=api_key)

    references = []

    for index, result in enumerate(results[:3], start=1):
        file_name = result.get("file_name", "未知檔案")
        page = result.get("page", "未知頁碼")
        content = result.get("content", "")

        references.append(
            f"""
[來源 {index}]
檔案：{file_name}
頁碼：{page}
內容：
{content}
"""
        )

    reference_text = "\n".join(references)

    prompt = f"""
你是一位保險文件查詢助理。

請你只能根據下方提供的保險條款內容回答問題。
如果條款內容不足以回答，請明確說「目前提供的文件內容不足以判斷」。
不要自行編造保險條款、金額、理賠條件或除外責任。

使用者問題：
{question}

保險條款內容：
{reference_text}

請用繁體中文回答，語氣清楚、白話、適合一般保戶理解。
回答請控制在 3 到 6 句內。
"""

    try:
        response = client.responses.create(
            model="gpt-5.5",
            input=prompt,
        )

        return response.output_text.strip()

    except Exception:
        return fallback