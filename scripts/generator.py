import os
import json
import re
import time
import random
import logging

from dotenv import load_dotenv
from google import genai
from google.genai import types

# Tắt cảnh báo AFC không cần thiết của SDK google-genai
logging.getLogger("google").setLevel(logging.ERROR)

class LegalGenerator:
    """
    LLM Generation cho chatbot tra cứu pháp luật lao động.

    Pipeline:
        Query
          ↓
        Retrieved chunks
          ↓
        Prompt + Context
          ↓
        Gemini
          ↓
        Raw answer
          ↓
        Citation verification
          ↓
        Final answer
          ↓
        JSONL log
    """

    REFUSAL_TEXT = "Tôi không tìm thấy thông tin để trả lời."

    def __init__(
        self,
        model_name="gemini-3.5-flash-lite",
        temperature=0.0
    ):
        # ============================================================
        # 1. LOAD API KEY
        # ============================================================

        env_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            ".env"
        )

        load_dotenv(dotenv_path=env_path)

        api_key = os.environ.get("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "Không tìm thấy GEMINI_API_KEY trong file .env "
                "hoặc biến môi trường."
            )

        self.client = genai.Client(api_key=api_key)

        self.model_name = model_name
        self.temperature = temperature

        # ============================================================
        # 2. LOG FILE
        # ============================================================

        self.log_dir = os.path.join(
            os.path.dirname(__file__),
            "..",
            "data",
            "eval"
        )

        os.makedirs(self.log_dir, exist_ok=True)

        self.log_file = os.path.join(
            self.log_dir,
            "generation_logs.jsonl"
        )

    # ================================================================
    # BUILD PROMPT
    # ================================================================

    def _build_prompt(self, query, retrieved_chunks):
        """
        Tạo system prompt chứa context được Retrieval truy hồi.

        LLM chỉ được phép sử dụng thông tin trong context.
        """

        context_parts = []
        valid_ids = []

        for chunk in retrieved_chunks:

            # --------------------------------------------------------
            # Lấy provision
            # --------------------------------------------------------

            prov = chunk["content"]
            pid = chunk["provision_id"]

            valid_ids.append(pid)

            # --------------------------------------------------------
            # Tạo thông tin Điều / Khoản / Điểm
            # --------------------------------------------------------

            dieu_khoan = f"Điều {prov['dieu']}"

            if prov.get("khoan"):
                dieu_khoan += f", Khoản {prov['khoan']}"

            if prov.get("diem"):
                dieu_khoan += f", Điểm {prov['diem']}"

            # --------------------------------------------------------
            # Đưa provision vào context
            # --------------------------------------------------------

            context_parts.append(
                f"[ID: {pid}]\n"
                f"Nguồn: {prov['van_ban']}, {dieu_khoan}\n"
                f"Nội dung: {prov['noi_dung']}"
            )

        context_str = "\n\n".join(context_parts)

        # ============================================================
        # SYSTEM PROMPT
        # ============================================================

        system_prompt = f"""
Bạn là CHATBOT HỖ TRỢ TRA CỨU PHÁP LUẬT LAO ĐỘNG VIỆT NAM.

NHIỆM VỤ:
Trả lời câu hỏi tra cứu pháp luật của người dùng CHỈ dựa trên thông tin trong CONTEXT được cung cấp.

============================================================
NGUYÊN TẮC BẮT BUỘC
============================================================

1. CĂN CỨ VÀ TRÍCH DẪN (STRICT GROUNDING & CITATION)
- CHỈ sử dụng thông tin có trong CONTEXT. Tuyệt đối không dùng kiến thức bên ngoài, không suy đoán hay tự tạo điều luật.
- Mọi khẳng định pháp lý phải có citation [provision_id] ngay sau câu khẳng định đó.
- Chỉ sử dụng đúng provision_id có mặt trong CONTEXT. Không trích dẫn thừa thãi.

2. TRẢ LỜI TRỰC TIẾP, ĐÚNG TRỌNG TÂM
- Với câu hỏi dạng "có được... không?", "có quyền... không?", "có phải... không?": Nêu ngay kết luận rõ ràng (Có / Không) ở câu đầu tiên, sau đó mới giải thích ngắn gọn quy định, điều kiện hoặc nghĩa vụ liên quan.
- Với câu hỏi tổng quan hoặc hỏi về một Điều (ví dụ: "Điều 12 quy định gì", "nghĩa vụ gồm những gì"): Liệt kê đầy đủ các Khoản/quy định có trong CONTEXT thành các gạch đầu dòng rõ ràng kèm citation.
- Diễn đạt tự nhiên, dễ hiểu; KHÔNG sao chép nguyên văn từng câu từng chữ của văn bản luật để tránh lỗi chính sách trích dẫn.

3. HIỂU VÀ ÁNH XẠ NGÔN NGỮ ĐỜI THƯỜNG
- Người dùng thường dùng từ ngữ đời thường, hãy đối chiếu với quy định tương ứng trong CONTEXT để trả lời:
  + "Nghỉ ngang", "nghỉ việc ngang", "tự ý nghỉ", "bỏ việc", "nghỉ không báo trước" ➔ Đơn phương chấm dứt HĐLĐ trái pháp luật (Điều 39, Điều 40).
  + "Nghỉ trước hạn", "xin nghỉ việc", "muốn nghỉ việc" ➔ Quyền đơn phương chấm dứt HĐLĐ của người lao động và nghĩa vụ báo trước (Điều 35).
  + "Cho nghỉ đột ngột", "đuổi việc đột ngột", "đuổi việc không báo trước" ➔ Người sử dụng lao động đơn phương chấm dứt HĐLĐ trái pháp luật (Điều 36, Điều 39, Điều 41).
  + "Nghỉ phép năm có được nhận tiền không", "tiền lương nghỉ phép" ➔ Tiền lương ngày nghỉ hằng năm hưởng nguyên lương (Điều 113).
  + "Chủ", "sếp", "công ty" ➔ Người sử dụng lao động.
  + "Nhân viên", "người làm", "công nhân" ➔ Người lao động.
  + "Bắt làm", "ép làm" ➔ Cưỡng bức lao động, buộc làm việc trái ý muốn (Điều 8, Điều 17, Điều 107).
  + "Đuổi việc", "cho nghỉ việc" ➔ Sa thải, đơn phương chấm dứt hợp đồng lao động.
  + "Quỵt lương", "nợ lương", "bùng lương" ➔ Chậm trả lương, vi phạm nghĩa vụ trả lương (Điều 97).

4. PHÂN BIỆT CÂU HỎI VÀ NGUYÊN TẮC TỪ CHỐI (REFUSAL CRITERIA)
- CÂU HỎI THỰC TẾ CÓ ĐẠI TỪ XƯNG HÔ (VẪN TRẢ LỜI QUY ĐỊNH):
  Người dùng thường hỏi tình huống đời thường ("Tôi muốn nghỉ trước hạn thì làm sao", "Sếp cho tôi nghỉ đột ngột có được không", "Công ty nợ lương tôi thì quy định thế nào", "Nghỉ phép năm có được nhận tiền không"). Nếu bản chất là hỏi về quy định, quyền, nghĩa vụ hoặc điều kiện pháp luật lao động ➔ PHẢI TRẢ LỜI các căn cứ pháp luật tương ứng có trong CONTEXT (ví dụ: người lao động được nghỉ việc nếu báo trước theo Điều 35; người sử dụng lao động phải báo trước theo Điều 36; nợ lương bị phạt lãi theo Điều 97; nghỉ phép năm được hưởng nguyên lương theo Điều 113).

- CÂU HỎI BẮT BUỘC TỪ CHỐI (OUT-OF-SCOPE):
  CHỈ từ chối bằng chính xác câu sau:
  "Tôi không tìm thấy thông tin để trả lời."
  trong các trường hợp:
  a) Xin lời khuyên quyết định tranh tụng/đời sống cá nhân: "tôi có nên kiện ra tòa án không?", "có nên nghỉ việc ra ngoài kinh doanh không?".
  b) Yêu cầu tính toán cụ thể số tiền cho vụ kiện cá nhân: "tính toán xem tôi được bồi thường chính xác bao nhiêu tiền nếu kiện?".
  c) Nhờ làm thơ, viết văn, soạn đơn hộ: "viết lá đơn xin nghỉ việc lâm li bi đát", "làm thơ mùa thu".
  d) Lĩnh vực pháp luật khác (hình sự, đất đai, thuế, giao thông, ly hôn...).
  e) Chào hỏi, thời tiết, toán học, câu hỏi vô nghĩa.
  f) CONTEXT hoàn toàn không có thông tin để trả lời.
- Khi từ chối: CHỈ trả về đúng câu: "Tôi không tìm thấy thông tin để trả lời." Không giải thích thêm, không đưa ra lời khuyên.

============================================================
CONTEXT
============================================================

{context_str}
"""

        return system_prompt.strip(), valid_ids

    # ================================================================
    # CITATION VERIFIER
    # ================================================================

    def verify_citations(self, answer, valid_ids):
        """
        Kiểm tra và chuẩn hóa citation do LLM sinh ra.

        - Citation tồn tại trong valid_ids: giữ nguyên.
        - Citation con (__a, __b, ...): nếu citation cha tồn tại
        trong valid_ids thì chuẩn hóa về citation cha.
        - Citation không tồn tại và không có citation cha hợp lệ:
        loại bỏ và ghi nhận là hallucinated.
        """

        citations = []
        hallucinated = []
        valid_citations = []

        # Hàm tìm citation cha
        def normalize_citation(pid):
            # Citation đã hợp lệ
            if pid in valid_ids:
                return pid

            # Ví dụ:
            # 145_2020_NDCP__D10__K2__a
            #              ↓
            # 145_2020_NDCP__D10__K2
            #
            # 45_2019_QH14__D103__A
            #            ↓
            # 45_2019_QH14__D103

            candidate = pid

            while "__" in candidate:
                candidate = candidate.rsplit("__", 1)[0]

                if candidate in valid_ids:
                    return candidate

            return None

        def repl_fn(match):
            raw_text = match.group(1)

            # Tách các provision_id bằng dấu phẩy,
            # chấm phẩy hoặc |
            parts = re.split(r"[,;|]+", raw_text.strip())
            parts = [p.strip() for p in parts if p.strip()]

            valid_parts = []

            for pid in parts:

                # Tránh duplicate citation
                if pid not in citations:
                    citations.append(pid)

                # Tìm ID hợp lệ hoặc ID cha hợp lệ
                normalized_pid = normalize_citation(pid)

                if normalized_pid is None:

                    # Citation không hợp lệ
                    if pid not in hallucinated:
                        hallucinated.append(pid)

                else:

                    if normalized_pid not in valid_citations:
                        valid_citations.append(normalized_pid)

                    if normalized_pid not in valid_parts:
                        valid_parts.append(normalized_pid)

            if not valid_parts:
                return ""

            # Chuẩn hóa:
            # [D10_K2, D11_K2]
            # thành:
            # [D10_K2][D11_K2]
            return "[" + "][".join(valid_parts) + "]"

        verified_answer = re.sub(
            r"\[([^\[\]]+)\]",
            repl_fn,
            answer
        )

        # Làm sạch khoảng trắng
        verified_answer = re.sub(
            r"[ \t]+",
            " ",
            verified_answer
        )

        verified_answer = re.sub(
            r"\n\s*\n+",
            "\n",
            verified_answer
        )

        verified_answer = verified_answer.strip()

        # Sửa khoảng trắng trước dấu câu
        verified_answer = re.sub(
            r"\s+([,.!?;:])",
            r"\1",
            verified_answer
        )

        return (
            verified_answer,
            list(set(hallucinated)),
            list(set(valid_citations))
        )

    # ================================================================
    # LOG INTERACTION
    # ================================================================

    def log_interaction(
        self,
        query,
        retrieved_chunks,
        prompt,
        raw_answer,
        final_answer,
        valid_ids,
        hallucinated,
        citations
    ):
        """
        Ghi toàn bộ lượt chạy vào JSONL.

        Mỗi lượt chạy = một JSON object trên một dòng.
        """

        log_entry = {
            # --------------------------------------------------------
            # Metadata
            # --------------------------------------------------------

            "timestamp": time.time(),
            "model": self.model_name,
            "temperature": self.temperature,

            # --------------------------------------------------------
            # Query
            # --------------------------------------------------------

            "query": query,

            # --------------------------------------------------------
            # Retrieval output
            # --------------------------------------------------------

            "retrieved_chunks": [
                {
                    "id": c["provision_id"],
                    "score": c["score"]
                }
                for c in retrieved_chunks
            ],

            # --------------------------------------------------------
            # Generation input
            # --------------------------------------------------------

            "prompt": prompt,

            # --------------------------------------------------------
            # Generation output
            # --------------------------------------------------------

            "raw_answer": raw_answer,

            # --------------------------------------------------------
            # Citation verification
            # --------------------------------------------------------

            "final_answer": final_answer,
            "valid_ids_in_context": valid_ids,
            "citations": citations,
            "hallucinated_ids": hallucinated,

            # --------------------------------------------------------
            # Refusal
            # --------------------------------------------------------

            "is_refusal": (
                final_answer.strip() == self.REFUSAL_TEXT
            )
        }

        # ------------------------------------------------------------
        # Append JSONL
        # ------------------------------------------------------------

        with open(
            self.log_file,
            "a",
            encoding="utf-8"
        ) as f:

            f.write(
                json.dumps(
                    log_entry,
                    ensure_ascii=False
                )
                + "\n"
            )

    # ================================================================
    # GENERATE
    # ================================================================

    def generate(self, query, retrieved_chunks):
        """
        Hàm chính:

            Query
              ↓
            Build prompt
              ↓
            Gemini
              ↓
            Citation verifier
              ↓
            JSONL log
              ↓
            Return result
        """

        # ------------------------------------------------------------
        # 1. Build prompt
        # ------------------------------------------------------------

        prompt, valid_ids = self._build_prompt(
            query,
            retrieved_chunks
        )

        # ------------------------------------------------------------
        # 2. Gemini configuration
        # ------------------------------------------------------------

        config = types.GenerateContentConfig(
            temperature=self.temperature,
            top_p=1.0,
            system_instruction=prompt
        )

        # Exponential backoff: base 5s, tối đa 60s, jitter ±20%
        max_retries = 4
        base_delay = 5
        max_delay = 60

        # Lỗi tạm thời cần retry
        RETRYABLE_CODES = (
            "429", "500", "503",
            "overload", "resource_exhausted",
            "empty_response"   # model trả rỗng — có thể do quá tải nội bộ
        )

        for attempt in range(max_retries + 1):

            try:

                # --------------------------------------------------------
                # 3. Gọi Gemini
                # --------------------------------------------------------

                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=query,
                    config=config
                )

                raw_answer = ""
                finish_reason = None

                # Kiểm tra finish_reason để phân biệt safety block vs empty
                try:
                    if response.candidates:
                        finish_reason = str(
                            response.candidates[0].finish_reason
                        )
                        raw_answer = (
                            response.candidates[0].content.parts[0].text
                            if response.candidates[0].content
                            and response.candidates[0].content.parts
                            else ""
                        )
                    else:
                        raw_answer = (response.text or "").strip()
                except Exception:
                    raw_answer = (response.text or "").strip()

                raw_answer = raw_answer.strip()

                # Safety block → từ chối, không retry
                if not raw_answer and finish_reason and "SAFETY" in finish_reason:
                    return {
                        "answer": self.REFUSAL_TEXT,
                        "raw_answer": "",
                        "hallucinated_ids": [],
                        "citations": [],
                        "is_refusal": True,
                        "api_error": False
                    }

                # Recitation block (Gemini chặn do model trích dẫn y nguyên văn bản luật)
                # Tự động xử lý ngay, KHÔNG lặp lại chờ đợi gây treo
                if not raw_answer and finish_reason and "RECITATION" in finish_reason:
                    print("  ⚠️ Phát hiện FinishReason.RECITATION - Kích hoạt cơ chế xử lý dự phòng...", flush=True)

                    # Bước 1: Thử gọi lại 1 lần duy nhất với chỉ dẫn diễn đạt tự nhiên + temp 0.25
                    try:
                        recit_prompt = (
                            prompt
                            + "\n\nLƯU Ý ĐẶC BIỆT ĐỂ TRÁNH LỖI RECITATION:\n"
                            "- Tuyệt đối KHÔNG sao chép nguyên văn các câu từ trong văn bản luật.\n"
                            "- Hãy diễn giải tóm tắt ngắn gọn quy định bằng lời của bạn, "
                            "kèm mã citation [provision_id] tương ứng."
                        )
                        recit_cfg = types.GenerateContentConfig(
                            temperature=self.temperature,
                            top_p=1.0,
                            system_instruction=recit_prompt
                        )
                        recit_res = self.client.models.generate_content(
                            model=self.model_name,
                            contents=query,
                            config=recit_cfg
                        )
                        if recit_res.text and recit_res.text.strip():
                            raw_answer = recit_res.text.strip()
                    except Exception as e_recit:
                        print(f"  Thử lại do recitation không thành công: {e_recit}", flush=True)

                    # Bước 2: Chỉ trích xuất trực tiếp nếu là câu hỏi tra cứu đích danh một Điều luật
                    if not raw_answer and retrieved_chunks:
                        direct_chunks = [c for c in retrieved_chunks if c.get("score", 0) >= 1.0]
                        if direct_chunks:
                            fallback_lines = []
                            for c in direct_chunks[:3]:
                                prov = c.get("content", {})
                                pid = c.get("provision_id", "")
                                dieu = prov.get("dieu", "")
                                khoan = prov.get("khoan", "")
                                vb = prov.get("van_ban", "")
                                tieu_de = prov.get("tieu_de_dieu", "")
                                noi_dung = prov.get("noi_dung", "").strip()

                                header = f"Theo quy định tại {vb}, Điều {dieu}"
                                if khoan:
                                    header += f", Khoản {khoan}"
                                if tieu_de:
                                    header += f" ({tieu_de})"
                                header += ":"

                                fallback_lines.append(f"{header}\n{noi_dung} [{pid}]")

                            raw_answer = "\n\n".join(fallback_lines)

                if not raw_answer:
                    raise ValueError(
                        f"empty_response|finish={finish_reason}"
                    )

                # --------------------------------------------------------
                # 4. Citation verification
                # --------------------------------------------------------

                (
                    final_answer,
                    hallucinated,
                    citations
                ) = self.verify_citations(
                    raw_answer,
                    valid_ids
                )

                # --------------------------------------------------------
                # 5. Nếu Gemini trả rỗng
                # --------------------------------------------------------

                if not final_answer:

                    final_answer = self.REFUSAL_TEXT

                # --------------------------------------------------------
                # 6. Kiểm tra refusal
                # --------------------------------------------------------

                is_refusal = (
                    final_answer.strip()
                    == self.REFUSAL_TEXT
                )

                # --------------------------------------------------------
                # 7. Ghi log
                # --------------------------------------------------------

                self.log_interaction(
                    query=query,
                    retrieved_chunks=retrieved_chunks,
                    prompt=prompt,
                    raw_answer=raw_answer,
                    final_answer=final_answer,
                    valid_ids=valid_ids,
                    hallucinated=hallucinated,
                    citations=citations
                )

                # --------------------------------------------------------
                # 8. Return
                # --------------------------------------------------------

                return {
                    "answer": final_answer,
                    "raw_answer": raw_answer,
                    "hallucinated_ids": hallucinated,
                    "citations": citations,
                    "is_refusal": is_refusal,
                    "api_error": False
                }

            except Exception as e:

                error_str = str(e).lower()
                is_retryable = any(
                    code in error_str
                    for code in RETRYABLE_CODES
                )

                if is_retryable and attempt < max_retries:
                    # Exponential backoff với jitter
                    wait = min(base_delay * (2 ** attempt), max_delay)
                    jitter = wait * 0.2 * random.random()  # ±20%
                    wait = wait + jitter

                    label = "Rate limit" if "429" in error_str else "Overload"
                    print(f"  ⏳ {label} (lần {attempt + 1}/{max_retries}), "
                          f"chờ {wait:.1f}s rồi thử lại...", flush=True)
                    time.sleep(wait)
                    continue

                # Lỗi khác hoặc hết lần thử
                print(f"Lỗi khi gọi LLM API: {e}", flush=True)

                return {
                    "answer": "Lỗi kết nối API. Vui lòng thử lại sau.",
                    "raw_answer": "",
                    "hallucinated_ids": [],
                    "citations": [],
                    "is_refusal": False,
                    "api_error": True,
                    "error": str(e)
                }