"""
rag_pipeline.py — Lõi xử lý RAG & Tiện ích nghiệp vụ Chatbot Pháp luật Lao động.
Tách biệt hoàn toàn phần lõi RAG (logic xử lý câu hỏi, truy xuất, trích dẫn, lưu trữ)
khỏi tầng hiển thị giao diện Streamlit (app.py).
"""

import os
import re
import json
import time
import uuid
import html

try:
    from filelock import FileLock, Timeout
    HAS_FILELOCK = True
except ImportError:
    HAS_FILELOCK = False

# ── 1. Danh mục và hàm chuẩn hóa hiển thị văn bản ─────────────────────────────
DOC_NAMES = {
    "45_2019_QH14":  "Bộ luật Lao động 2019",
    "145_2020_NDCP": "Nghị định 145/2020/NĐ-CP",
    "58_VBHN-VPQH":  "Luật BHXH (VBHN)",
    "84_2015_QH13":  "Luật ATVSLĐ 2015",
    "10_2012_QH13":  "Bộ luật Lao động 2012",
    "50_2024_QH15":  "Luật Công đoàn 2024",
}

def doc_name(code: str) -> str:
    """Chuyển mã ký hiệu văn bản sang tên đầy đủ."""
    for k, v in DOC_NAMES.items():
        if k in code:
            return v
    return code.replace("_", "/")

def parse_pid(pid: str) -> dict:
    """Tách mã provision_id thành thông tin chi tiết: tên văn bản, Điều, Khoản."""
    parts = pid.split("__")
    code  = parts[0]
    dieu  = next((p[1:] for p in parts[1:] if p.startswith("D") and p[1:].isdigit()), "")
    khoan = next((p[1:] for p in parts[1:] if p.startswith("K")), "")
    clause = ("Điều " + dieu if dieu else "") + (", Khoản " + khoan if khoan else "")
    return {"doc": doc_name(code), "clause": clause.strip(", ") or pid, "pid": pid}

def strip_cit(text: str) -> str:
    """Loại bỏ thẻ [provision_id] khỏi câu trả lời để hiển thị tự nhiên cho người đọc."""
    return re.sub(r'\[[^\[\]]+\]', '', text).strip()

def safe_escape(text: str) -> str:
    """Escape an toàn mọi nội dung người dùng, điều luật và tham số trước khi chèn HTML."""
    if not text:
        return ""
    return html.escape(str(text), quote=True)

def safe_render_llm_answer(text: str) -> str:
    """
    Escape an toàn câu trả lời của LLM trước khi render HTML,
    chỉ hỗ trợ chuyển đổi an toàn các thẻ in đậm (**) và in nghiêng (*).
    """
    if not text:
        return ""
    # 1. Escape toàn bộ thẻ HTML nguy hiểm (<script>, <img onerror>, ...)
    escaped = html.escape(str(text).strip(), quote=True)
    # 2. Hỗ trợ hiển thị an toàn cú pháp in đậm **text**
    escaped = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', escaped)
    # 3. Hỗ trợ hiển thị an toàn cú pháp in nghiêng *text*
    escaped = re.sub(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)', r'<em>\1</em>', escaped)
    return escaped


# ── 2. Mở rộng câu hỏi đời thường (Query Expansion) ───────────────────────────
ABBREVIATIONS = {
    r"\bnlđ\b": "người lao động",
    r"\bnsdlđ\b": "người sử dụng lao động",
    r"\bhđlđ\b": "hợp đồng lao động",
    r"\bhđ\b": "hợp đồng",
    r"\bbhxh\b": "bảo hiểm xã hội",
    r"\bbhtn\b": "bảo hiểm thất nghiệp",
    r"\bbhyt\b": "bảo hiểm y tế",
    r"\bcty\b": "công ty",
    r"\bnv\b": "nhân viên",
    r"\b(k|ko|kh|khg)\b": "không",
    r"\b(đc|dc)\b": "được",
    r"\bot\b": "làm thêm giờ",
}

def expand_legal_query(q: str) -> str:
    """
    Mở rộng câu hỏi đời thường sang thuật ngữ pháp lý chuẩn xác.
    Giúp tăng Recall@k cho bộ truy xuất Hybrid RAG.
    """
    q_low = q.lower()

    # Nếu là câu hỏi ngoài phạm vi rõ rệt -> Giữ nguyên để LLM từ chối chính xác
    if re.search(r"\b(tôi\s+có\s+nên\s+kiện|kiện\s+ra\s+tòa|tính\s+toán\s+xem\s+tôi|tư\s+vấn\s+giúp\s+tôi\s+mua|viết\s+cho\s+tôi|soạn\s+cho\s+tôi|làm\s+thơ|thời\s+tiết|sữa\s+nào|làm\s+riêng\s+kinh\s+doanh)\b", q_low):
        return q

    # Chuẩn hóa viết tắt
    norm_q = q_low
    for pattern, repl in ABBREVIATIONS.items():
        norm_q = re.sub(pattern, repl, norm_q)

    additions = []

    # 1. Nghỉ trước hạn / xin nghỉ việc / muốn nghỉ việc
    if re.search(r"nghỉ\s+(việc\s+)?trước\s+hạn|xin\s+nghỉ\s+việc|muốn\s+nghỉ\s+việc|đơn\s+phương\s+chấm\s+dứt\s+hợp\s+đồng", norm_q):
        additions.append("quyền đơn phương chấm dứt hợp đồng lao động của người lao động thời hạn báo trước Điều 35")

    # 2. Nghỉ ngang / tự ý bỏ việc / không báo trước
    elif re.search(r"nghỉ\s+(việc\s+)?ngang|tự\s+(ý\s+)?(nghỉ|bỏ)\s*(việc)?|bỏ\s+việc|nghỉ\s+(không|k|ko)\s*(phép|xin|báo)|nghỉ\s+đùng|thôi\s+việc\s+không", norm_q):
        additions.append("đơn phương chấm dứt hợp đồng lao động trái pháp luật nghĩa vụ bồi thường Điều 39 Điều 40")

    # 3. Cho nghỉ việc đột ngột / đuổi đột ngột (không báo trước)
    if re.search(r"nghỉ\s+việc\s+đột\s+ngột|đuổi\s+đột\s+ngột|nghỉ\s+đột\s+ngột|đuổi\s+(việc\s+)?ngay|thôi\s+việc\s+ngay", norm_q):
        additions.append("người sử dụng lao động đơn phương chấm dứt hợp đồng lao động thời hạn báo trước trái pháp luật Điều 36 Điều 39 Điều 41")
    elif re.search(r"sa\s*thải|kỷ\s*luật\s*sa\s*thải", norm_q):
        additions.append("kỷ luật sa thải xử lý kỷ luật lao động Điều 125")

    # 4. Hết hạn hợp đồng
    if re.search(r"hết\s+(hạn\s+)?hợp\s+đồng|hết\s+hđ", norm_q) and not re.search(r"trước\s+hạn", norm_q):
        additions.append("chấm dứt hợp đồng lao động hết hạn Điều 34")

    # 5. Ép buộc / cưỡng bức lao động
    if re.search(r"\b(bắt|ép|cưỡng\s*bức|bắt\s*buộc|cưỡng\s*ép)\b", norm_q):
        additions.append("cưỡng bức lao động hành vi bị nghiêm cấm Điều 8 Điều 17")

    # 6. Tiền lương / nợ lương / chậm lương
    if re.search(r"quỵt\s*lương|nợ\s*lương|chậm\s*lương|bùng\s*lương|không\s*trả\s*lương", norm_q):
        additions.append("tiền lương chậm trả lương đền bù tiền lãi quyền đơn phương chấm dứt Điều 97 Điều 35")
    elif re.search(r"tiền\s*lương|trả\s*lương|lương\s*tối\s*thiểu", norm_q):
        additions.append("tiền lương kỳ hạn trả lương Điều 97")

    # 7. Làm thêm giờ / tăng ca
    if re.search(r"làm\s*thêm|tăng\s*ca|ngoài\s*giờ|làm\s*đêm", norm_q):
        additions.append("làm thêm giờ thời giờ làm việc sự đồng ý của người lao động Điều 107")

    # 8. Nghỉ phép năm
    if re.search(r"nghỉ\s*phép\s*năm|nghỉ\s*phép|nghỉ\s*hằng\s*năm", norm_q):
        additions.append("nghỉ hằng năm hưởng nguyên lương tiền lương ngày nghỉ thanh toán ngày chưa nghỉ Điều 113")
    elif re.search(r"nghỉ\s*lễ|nghỉ\s*tết|lễ\s*tết", norm_q):
        additions.append("nghỉ lễ tết hưởng nguyên lương Điều 112")

    # 9. Người sử dụng lao động
    if re.search(r"\b(chủ|sếp)\b", norm_q):
        additions.append("người sử dụng lao động")

    # 10. Thử việc
    if re.search(r"thử\s*việc", norm_q):
        additions.append("thời gian thử việc tiền lương thử việc Điều 25 Điều 26")

    # 11. Thai sản
    if re.search(r"thai\s*sản|nghỉ\s*đẻ|sinh\s*con", norm_q):
        additions.append("chế độ thai sản lao động nữ Điều 137 Điều 139")

    if additions:
        return q + " " + " ".join(additions)
    return q


# ── 3. Lõi thực thi RAG Pipeline (Retrieval + Filter + Generation) ────────────
def execute_rag_pipeline(
    query: str,
    retriever,
    generator,
    top_k: int = 10,
    rrf_k: int = 5,
    alpha: float = 0.5,
    retrieval_depth: int = 50,
    expand_siblings: bool = True,
    hieu_luc_filter: str = "con_hieu_luc",
    max_context_chars: int = 10_000,
    retrieval_method: str = "hybrid"
) -> dict:
    """
    Thực thi chuỗi RAG hoàn chỉnh cho một câu hỏi:
    1. Query Expansion sang thuật ngữ pháp lý.
    2. Retrieval theo phương pháp (Hybrid RRF / BM25 / Dense).
    3. Lọc hiệu lực văn bản & gom cụm Điều (Sibling Expansion), có nhánh dự phòng khi lọc rỗng.
    4. Cắt tỉa ngữ cảnh vừa vặn giới hạn ký tự (mặc định 10.000 ký tự).
    5. Gọi LLM sinh câu trả lời và xác minh trích dẫn (Citation Verification).
    """
    t0 = time.time()
    search_q = expand_legal_query(query)

    method_key = str(retrieval_method).lower() if not callable(retrieval_method) else ""
    if callable(retrieval_method):
        raw_chunks = retrieval_method(search_q)
    elif method_key in ("bm25",):
        raw_chunks = retriever.search_bm25(
            search_q,
            top_k=top_k,
            hieu_luc_filter=hieu_luc_filter
        )
    elif method_key in ("dense",):
        raw_chunks = retriever.search_dense(
            search_q,
            top_k=top_k,
            hieu_luc_filter=hieu_luc_filter
        )
    else:
        raw_chunks = retriever.search_hybrid(
            search_q,
            top_k=top_k,
            rrf_k=rrf_k,
            alpha=alpha,
            retrieval_depth=retrieval_depth,
            expand_siblings=expand_siblings,
            hieu_luc_filter=hieu_luc_filter
        )
    retrieval_time = time.time() - t0

    valid_chunks = retriever.filter_by_hieu_luc(raw_chunks, hieu_luc_filter)
    chunks = valid_chunks[:top_k] if valid_chunks else raw_chunks[:top_k]

    # Giới hạn context theo số ký tự tối đa
    budget = 0
    capped = []
    for ch in chunks:
        noi_dung = ch.get("content", {}).get("noi_dung", "")
        if budget + len(noi_dung) > max_context_chars and capped:
            break
        capped.append(ch)
        budget += len(noi_dung)
    chunks = capped

    # Gọi mô hình sinh câu trả lời
    t1 = time.time()
    res = generator.generate(query, chunks)
    generation_time = time.time() - t1

    return {
        "answer": res.get("answer", ""),
        "citations": res.get("citations", []),
        "hallucinated_ids": res.get("hallucinated_ids", []),
        "is_refusal": res.get("is_refusal", False),
        "api_error": res.get("api_error", False),
        "error": res.get("error"),
        "chunks": chunks,
        "retrieval_time": retrieval_time,
        "generation_time": generation_time,
    }


# ── 4. Quản lý lưu trữ lịch sử hội thoại bền vững (Persistence Storage) ───────
def get_current_time_str() -> str:
    t = time.localtime()
    return f"{t.tm_hour:02d}:{t.tm_min:02d}"

def new_conversation() -> dict:
    return {
        "title": "Cuộc trò chuyện mới",
        "time": get_current_time_str(),
        "messages": [],
        "chunks": None
    }

def _get_file_lock(storage_path: str, timeout: float = 10.0):
    """Khởi tạo context manager khóa tệp chống xung đột ghi đồng thời."""
    if HAS_FILELOCK and storage_path:
        lock_path = storage_path + ".lock"
        return FileLock(lock_path, timeout=timeout)
    from contextlib import nullcontext
    return nullcontext()

def load_chat_history(storage_path: str) -> dict:
    """Nạp lịch sử các cuộc trò chuyện từ file lưu trữ có khóa tệp an toàn."""
    if not storage_path or not os.path.exists(storage_path):
        return {0: new_conversation()}
    try:
        with _get_file_lock(storage_path, timeout=5.0):
            if not os.path.exists(storage_path):
                return {0: new_conversation()}
            with open(storage_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                # Chuyển key dạng chuỗi về int
                convs = {int(k): v for k, v in data.items()}
                if convs:
                    return convs
    except Exception:
        pass
    return {0: new_conversation()}

def save_chat_history(convs: dict, storage_path: str):
    """Lưu trữ lịch sử ra file JSON với khóa tệp và cơ chế ghi nguyên tử (atomic write)."""
    if not storage_path:
        return
    temp_path = None
    try:
        os.makedirs(os.path.dirname(storage_path), exist_ok=True)
        # Chuẩn bị dữ liệu lưu
        to_save = {}
        for cid, c in convs.items():
            to_save[str(cid)] = {
                "title": c.get("title", "Cuộc trò chuyện"),
                "time": c.get("time", get_current_time_str()),
                "messages": c.get("messages", []),
                # Lưu provision_id của chunks để tải lại nhẹ nhàng
                "chunks": c.get("chunks", [])
            }

        with _get_file_lock(storage_path, timeout=10.0):
            # Ghi ra file tạm thời trước rồi thay thế nguyên tử (atomic replace)
            temp_path = f"{storage_path}.tmp.{uuid.uuid4().hex[:8]}"
            with open(temp_path, "w", encoding="utf-8") as f:
                json.dump(to_save, f, ensure_ascii=False, indent=2)
                f.flush()
                os.fsync(f.fileno())
            os.replace(temp_path, storage_path)
    except Exception:
        pass
    finally:
        if temp_path and os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except Exception:
                pass

def delete_chat_history(storage_path: str):
    """Xóa tệp lịch sử và tệp khóa liên quan một cách an toàn."""
    if not storage_path:
        return
    try:
        with _get_file_lock(storage_path, timeout=5.0):
            if os.path.exists(storage_path):
                os.remove(storage_path)
        lock_file = storage_path + ".lock"
        if os.path.exists(lock_file):
            try:
                os.remove(lock_file)
            except Exception:
                pass
    except Exception:
        pass

# Aliases ngắn gọn tiện dụng
hm = get_current_time_str
new_conv = new_conversation

