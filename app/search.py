import json
import re
from pathlib import Path

from app.llm import generate_ai_answer


BASE_DIR = Path(__file__).resolve().parent.parent
CHUNKS_DIR = BASE_DIR / "data" / "chunks"


DOCUMENT_RULES = [
    {
        "label": "國泰人壽旅行平安保險",
        "file_keywords": [
            "cathay_life_new_travel",
            "cathay_life_travel_full",
            "cathay_life_travel",
            "new_travel",
            "travel_full",
            "旅行",
            "旅平",
        ],
        "query_keywords": [
            "國泰人壽新旅行平安保險",
            "國泰人壽旅行平安保險",
            "旅行平安保險",
            "旅平險",
            "旅行保險",
            "旅遊保險",
            "意外傷害事故",
            "大眾運輸交通工具",
            "傷害醫療保險金",
            "海外突發疾病",
            "旅行",
            "旅遊",
        ],
    },
    {
        "label": "國泰人壽微型個人定期壽險",
        "file_keywords": [
            "cathay_life_micro_term_life",
            "micro_term_life",
            "微型個人定期壽險",
            "微型",
            "定期壽險",
        ],
        "query_keywords": [
            "國泰人壽微型個人定期壽險",
            "微型個人定期壽險",
            "微型壽險",
            "定期壽險",
            "承保年齡",
            "投保年齡",
            "保額限制",
            "保險期間",
            "身故保險金",
            "完全失能保險金",
        ],
    },
]


INTENT_RULES = [
    {
        "label": "名詞定義",
        "query_keywords": [
            "是什麼",
            "什麼是",
            "定義",
            "怎麼定義",
            "何謂",
            "意外傷害事故",
            "大眾運輸交通工具",
        ],
        "evidence_keywords": [
            "名詞定義",
            "意外傷害事故",
            "大眾運輸交通工具",
            "係指",
            "是指",
            "指",
            "非由疾病引起",
            "外來突發事故",
        ],
    },
    {
        "label": "承保範圍",
        "query_keywords": [
            "承保範圍",
            "保障範圍",
            "保什麼",
            "保障什麼",
            "有哪些保障",
        ],
        "evidence_keywords": [
            "承保範圍",
            "保險範圍",
            "主要給付項目",
            "身故",
            "失能",
            "體傷",
            "死亡",
            "財物損失",
            "賠償責任",
        ],
    },
    {
        "label": "理賠申請",
        "query_keywords": [
            "理賠",
            "申請",
            "需要文件",
            "檢具",
            "準備哪些",
            "怎麼申請",
        ],
        "evidence_keywords": [
            "理賠申請",
            "申請書",
            "診斷書",
            "證明文件",
            "收據",
            "檢具",
            "通知",
        ],
    },
    {
        "label": "除外責任",
        "query_keywords": [
            "除外",
            "不賠",
            "不保",
            "除外責任",
            "除外原因",
        ],
        "evidence_keywords": [
            "除外責任",
            "除外原因",
            "不負",
            "不保",
            "不賠",
        ],
    },
    {
        "label": "保險期間",
        "query_keywords": [
            "保險期間",
            "期間",
            "多久",
            "起訖",
            "什麼時候開始",
        ],
        "evidence_keywords": [
            "保險期間",
            "始日",
            "終日",
            "有效期間",
            "延長",
            "一年期",
            "1年期",
        ],
    },
    {
        "label": "承保年齡",
        "query_keywords": [
            "承保年齡",
            "投保年齡",
            "幾歲",
            "年齡",
        ],
        "evidence_keywords": [
            "承保年齡",
            "投保年齡",
            "0歲",
            "64歲",
            "年齡",
        ],
    },
    {
        "label": "保額限制",
        "query_keywords": [
            "保額限制",
            "保險金額",
            "金額",
            "賠多少",
            "上限",
            "限額",
            "保額",
        ],
        "evidence_keywords": [
            "保額限制",
            "保險金額",
            "限額",
            "給付",
            "10萬",
            "50萬",
            "新臺幣",
        ],
    },
]


IMPORTANT_TERMS = [
    "國泰人壽新旅行平安保險",
    "國泰人壽旅行平安保險",
    "國泰人壽微型個人定期壽險",
    "微型個人定期壽險",
    "意外傷害事故",
    "大眾運輸交通工具",
    "傷害醫療保險金",
    "海外突發疾病",
    "承保年齡",
    "投保年齡",
    "保額限制",
    "保險期間",
    "保險金額",
    "承保範圍",
    "保險範圍",
    "名詞定義",
    "主要給付項目",
    "理賠申請",
    "除外責任",
    "除外原因",
    "第三人責任保險",
    "第三人",
    "體傷",
    "死亡",
    "財物損失",
    "自負額",
    "保險事故",
    "給付條件",
    "保險金申請書",
    "申請書",
    "診斷書",
    "住院證明",
    "賠償責任",
    "損害賠償",
    "有效期間",
    "受賠償請求",
    "身故保險金",
    "完全失能保險金",
]


DEFINITION_TERMS = [
    "意外傷害事故",
    "大眾運輸交通工具",
]


STOPWORDS = [
    "什麼",
    "如何",
    "可以",
    "請問",
    "是否",
    "哪些",
    "怎麼",
    "為什麼",
    "的",
    "是",
    "嗎",
    "呢",
    "了",
    "有",
    "和",
    "或",
    "以及",
    "這個",
    "一個",
    "我要",
    "想問",
    "一下",
    "國泰",
    "人壽",
]


def normalize(text: str) -> str:
    return re.sub(r"\s+", "", text or "")


def clean_display_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text or "")
    return text.strip()


def load_chunks() -> list[dict]:
    chunks = []

    if not CHUNKS_DIR.exists():
        return chunks

    for path in CHUNKS_DIR.glob("*_chunks.json"):
        with path.open("r", encoding="utf-8") as f:
            chunks.extend(json.load(f))

    return chunks


def get_corpus_stats() -> dict:
    chunks = load_chunks()
    files = sorted(
        {
            chunk.get("file_name", "")
            for chunk in chunks
            if chunk.get("file_name")
        }
    )

    return {
        "file_count": len(files),
        "chunk_count": len(chunks),
        "files": files,
    }


def detect_document_type(question: str) -> dict | None:
    for rule in DOCUMENT_RULES:
        if any(keyword in question for keyword in rule["query_keywords"]):
            return rule

    return None


def detect_intent(question: str) -> dict:
    for rule in INTENT_RULES:
        if any(keyword in question for keyword in rule["query_keywords"]):
            return rule

    return {
        "label": "一般查詢",
        "query_keywords": [],
        "evidence_keywords": IMPORTANT_TERMS,
    }


def detect_definition_target(question: str) -> str | None:
    for term in DEFINITION_TERMS:
        if term in question:
            return term

    return None


def is_target_file(chunk: dict, rule: dict | None) -> bool:
    if rule is None:
        return True

    file_name = chunk.get("file_name", "")
    return any(keyword in file_name for keyword in rule["file_keywords"])


def remove_redundant_terms(terms: list[str]) -> list[str]:
    cleaned = []

    for term in terms:
        redundant = False

        for other in terms:
            if term != other and term in other and len(other) > len(term):
                redundant = True
                break

        if not redundant:
            cleaned.append(term)

    return cleaned


def extract_query_terms(question: str) -> list[str]:
    question_norm = normalize(question)
    terms = set()

    for term in IMPORTANT_TERMS:
        if term in question:
            terms.add(term)

    max_len = min(8, len(question_norm))

    for length in range(max_len, 1, -1):
        for i in range(len(question_norm) - length + 1):
            term = question_norm[i:i + length]

            if term in STOPWORDS:
                continue

            if any(stopword in term and len(term) <= 3 for stopword in STOPWORDS):
                continue

            terms.add(term)

    return remove_redundant_terms(sorted(terms, key=len, reverse=True))


def get_matched_terms(content: str, terms: list[str]) -> list[str]:
    content_norm = normalize(content)
    matched = []

    for term in terms:
        if term in content_norm and term not in matched:
            matched.append(term)

    return remove_redundant_terms(matched)[:6]


def has_definition_pattern(content: str, target: str | None) -> bool:
    if not target:
        return False

    content_norm = normalize(content)

    if target not in content_norm:
        return False

    definition_markers = [
        "係指",
        "是指",
        "指",
        "定義",
        "非由疾病引起",
        "外來突發事故",
    ]

    return any(marker in content_norm for marker in definition_markers)


def score_chunk(
    question: str,
    chunk: dict,
    terms: list[str],
    doc_rule: dict | None,
    intent_rule: dict,
) -> int:
    content = normalize(chunk.get("content", ""))
    page = int(chunk.get("page", 999))
    score = 0

    if doc_rule:
        if is_target_file(chunk, doc_rule):
            score += 500
        else:
            return 0

    target_definition = detect_definition_target(question)

    if target_definition and target_definition in content:
        score += 700

        if has_definition_pattern(chunk.get("content", ""), target_definition):
            score += 1000

        if page <= 3:
            score += 250

    for term in terms:
        if term in content:
            score += len(term) * 12

            if term in IMPORTANT_TERMS:
                score += 80

    for keyword in intent_rule["evidence_keywords"]:
        if keyword in content:
            score += 80

    if "是什麼" in question and "名詞定義" in content:
        score += 300

    if "定義" in question and "名詞定義" in content:
        score += 300

    if "意外傷害事故" in question and "傷害醫療保險金" in content:
        score -= 300

    if "大眾運輸交通工具" in question and "大眾運輸交通工具" in content:
        score += 600

    if "理賠" in question and ("理賠" in content or "申請" in content):
        score += 240

    if "除外" in question and ("除外責任" in content or "除外原因" in content):
        score += 240

    if "承保年齡" in question and "承保年齡" in content:
        score += 600

    if "保額限制" in question and ("保額限制" in content or "保額" in content):
        score += 600

    if "保險期間" in question and "保險期間" in content:
        score += 400

    return score


def split_sentences(text: str) -> list[str]:
    text = clean_display_text(text)
    raw_sentences = re.split(r"[。；;]", text)
    sentences = []

    for sentence in raw_sentences:
        sentence = sentence.strip(" ，,、：: \n\t")

        if 10 <= len(sentence) <= 280:
            sentences.append(sentence)

    return sentences


def score_sentence(
    sentence: str,
    question: str,
    terms: list[str],
    intent_rule: dict,
) -> int:
    sentence_norm = normalize(sentence)
    score = 0
    target_definition = detect_definition_target(question)

    if target_definition and target_definition in sentence_norm:
        score += 900

        if any(
            marker in sentence_norm
            for marker in ["係指", "是指", "指", "非由疾病引起", "外來突發事故"]
        ):
            score += 1300

    for term in terms:
        if term in sentence_norm:
            score += len(term) * 12

    for keyword in intent_rule["evidence_keywords"]:
        if keyword in sentence_norm:
            score += 70

    if "理賠" in question and ("理賠" in sentence_norm or "申請" in sentence_norm):
        score += 220

    if "除外" in question and ("除外責任" in sentence_norm or "除外原因" in sentence_norm):
        score += 220

    if "承保年齡" in question and "承保年齡" in sentence_norm:
        score += 500

    if "保額限制" in question and ("保額限制" in sentence_norm or "保額" in sentence_norm):
        score += 500

    if "保險期間" in question and "保險期間" in sentence_norm:
        score += 350

    return score


def extract_evidence_sentences(
    question: str,
    results: list[dict],
    terms: list[str],
    intent_rule: dict,
) -> list[dict]:
    candidates = []

    for result in results:
        sentences = split_sentences(result.get("content", ""))

        for sentence in sentences:
            score = score_sentence(sentence, question, terms, intent_rule)

            if score > 0:
                candidates.append({
                    "sentence": sentence,
                    "score": score,
                    "file_name": result.get("file_name", ""),
                    "page": result.get("page", ""),
                })

    candidates.sort(key=lambda item: item["score"], reverse=True)

    evidence = []
    seen = set()

    for item in candidates:
        key = normalize(item["sentence"])

        if key in seen:
            continue

        seen.add(key)
        evidence.append(item)

        if len(evidence) >= 3:
            break

    return evidence


def make_snippet(content: str, matched_terms: list[str], width: int = 300) -> str:
    clean = clean_display_text(content)

    best_pos = None

    for term in matched_terms:
        pos = clean.find(term)
        if pos != -1:
            best_pos = pos
            break

    if best_pos is None:
        return clean[:width] + ("..." if len(clean) > width else "")

    start = max(best_pos - 70, 0)
    end = min(start + width, len(clean))

    snippet = clean[start:end]

    if start > 0:
        snippet = "..." + snippet

    if end < len(clean):
        snippet += "..."

    return snippet


def relevance_label(score: int) -> str:
    if score >= 900:
        return "高度相關"
    if score >= 450:
        return "中度相關"
    return "低度相關"


def confidence_label(results: list[dict]) -> str:
    if not results:
        return "低"

    top_score = results[0]["score"]

    if top_score >= 1200:
        return "高"
    if top_score >= 650:
        return "中"
    return "低"


def search_documents(question: str, top_k: int = 3) -> list[dict]:
    chunks = load_chunks()
    terms = extract_query_terms(question)
    doc_rule = detect_document_type(question)
    intent_rule = detect_intent(question)

    results = []

    for chunk in chunks:
        if doc_rule and not is_target_file(chunk, doc_rule):
            continue

        score = score_chunk(question, chunk, terms, doc_rule, intent_rule)

        if score <= 0:
            continue

        matched_terms = get_matched_terms(
            chunk.get("content", ""),
            terms + intent_rule["evidence_keywords"],
        )

        results.append({
            **chunk,
            "score": score,
            "matched_terms": matched_terms,
            "snippet": make_snippet(chunk.get("content", ""), matched_terms),
            "relevance": relevance_label(score),
        })

    results.sort(key=lambda item: item["score"], reverse=True)

    unique_results = []
    seen_pages = set()

    for result in results:
        page_key = (result["file_name"], result["page"])

        if page_key in seen_pages:
            continue

        seen_pages.add(page_key)
        unique_results.append(result)

        if len(unique_results) >= top_k:
            break

    return unique_results


def make_definition_answer(target: str, evidence: list[dict]) -> str | None:
    if not target or not evidence:
        return None

    sentence = clean_display_text(evidence[0]["sentence"])

    position = sentence.find(target)

    if position != -1:
        sentence = sentence[position + len(target):]

    sentence = sentence.strip(" ：:，,。、「」『』()（） ")

    for prefix in ["係指", "是指", "指", "為", "係"]:
        if sentence.startswith(prefix):
            sentence = sentence[len(prefix):].strip(" ：:，,。 ")

    if not sentence:
        return None

    return f"{target}是指{sentence}。"


def extract_definition_from_text(target: str, text: str) -> str | None:
    """
    從條款原文中抽取「某名詞：指……」這種定義。
    例如：「大眾運輸交通工具」：指領有合法營業執照之……
    """
    if not target:
        return None

    clean_text = clean_display_text(text)
    escaped_target = re.escape(target)

    patterns = [
        rf"[一二三四五六七八九十\d]+[、.．]\s*[「『]?{escaped_target}[」』]?\s*[：:]\s*(.+?)(?=(?:[一二三四五六七八九十\d]+[、.．]\s*[「『])|。|；|;|$)",
        rf"[「『]?{escaped_target}[」』]?\s*[：:]\s*(.+?)(?=。|；|;|$)",
    ]

    for pattern in patterns:
        match = re.search(pattern, clean_text)

        if not match:
            continue

        definition = match.group(1).strip(" ：:，,。、「」『』()（） ")

        for prefix in ["係指", "是指", "指", "為", "係"]:
            if definition.startswith(prefix):
                definition = definition[len(prefix):].strip(" ：:，,。 ")

        if definition:
            return f"{target}是指{definition}。"

    return None


def extract_direct_definition_answer(question: str, results: list[dict]) -> str | None:
    """
    專門處理「是什麼 / 定義 / 怎麼定義」問題。
    優先找明確的名詞定義，不要從其他條款中硬切句子。
    """
    target = detect_definition_target(question)

    if not target:
        return None

    for result in results:
        answer = extract_definition_from_text(target, result.get("content", ""))

        if answer:
            return answer

    return None


def build_chat_answer(question: str, results: list[dict]) -> str:
    terms = extract_query_terms(question)
    intent_rule = detect_intent(question)
    evidence = extract_evidence_sentences(question, results, terms, intent_rule)
    target_definition = detect_definition_target(question)

    if not results:
        return (
            "我目前沒有在已建立的文件庫中找到足夠相關的內容。"
            "請確認 PDF 是否已放進 data/sample_docs，或把問題問得更明確一點。"
        )

    direct_definition_answer = extract_direct_definition_answer(question, results)

    if direct_definition_answer:
        return direct_definition_answer

    definition_answer = make_definition_answer(target_definition, evidence)

    if definition_answer:
        return definition_answer

    if "承保年齡" in question and evidence:
        return f"依文件內容，{evidence[0]['sentence']}。"

    if "保額限制" in question and evidence:
        return f"依文件內容，{evidence[0]['sentence']}。"

    if "保險期間" in question and evidence:
        return f"依文件內容，{evidence[0]['sentence']}。"

    if "理賠" in question:
        return (
            "理賠申請通常需要準備可證明保險事故與損失的文件，例如申請書、"
            "診斷證明、收據、事故證明，或保險公司要求的其他相關資料。"
            "實際文件仍以下方引用來源為準。"
        )

    if "除外" in question:
        return (
            "除外責任是指保單條款中約定保險公司不負賠償或給付責任的情況。"
            "也就是說，即使事故發生，只要符合除外責任條款，保險公司就可能不予理賠。"
        )

    if evidence:
        first = evidence[0]["sentence"]

        if len(evidence) > 1:
            second = evidence[1]["sentence"]
            return f"根據文件內容，{first}。另外，{second}。"

        return f"根據文件內容，{first}。"

    return f"根據最相關的文件段落，{results[0]['snippet']}"


def build_answer(question: str, results: list[dict]) -> dict:
    terms = extract_query_terms(question)
    doc_rule = detect_document_type(question)
    intent_rule = detect_intent(question)
    evidence = extract_evidence_sentences(question, results, terms, intent_rule)

    summary = build_chat_answer(question, results)

    if not results:
        return {
            "summary": summary,
            "query_type": "查無結果",
            "document_type": doc_rule["label"] if doc_rule else "未指定",
            "confidence": "低",
            "confidence_reason": "系統沒有找到符合問題與文件類型的段落。",
            "sources": [],
            "evidence": [],
        }

    document_type = doc_rule["label"] if doc_rule else "未指定文件類型"
    query_type = intent_rule["label"]
    confidence = confidence_label(results)

    sources = []
    seen_sources = set()

    for result in results:
        key = (result.get("file_name", ""), result.get("page", ""))

        if key in seen_sources:
            continue

        seen_sources.add(key)
        sources.append({
            "file_name": result.get("file_name", ""),
            "page": result.get("page", ""),
            "score": result.get("score", 0),
            "relevance": result.get("relevance", ""),
            "snippet": result.get("snippet", ""),
            "content": result.get("content", ""),
            "matched_terms": result.get("matched_terms", []),
        })

        if len(sources) >= 2:
            break

    matched = results[0].get("matched_terms", [])
    matched_text = "、".join(matched[:4]) if matched else "相關詞"

    return {
        "summary": summary,
        "query_type": query_type,
        "document_type": document_type,
        "confidence": confidence,
        "confidence_reason": f"此回答根據文件檢索結果產生，最高相關段落命中「{matched_text}」，並保留來源檔案與頁碼。",
        "sources": sources,
        "evidence": evidence[:2],
    }