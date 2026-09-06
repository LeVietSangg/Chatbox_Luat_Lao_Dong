import os
import json
import re
import time
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
        model_name="gemini-2.5-flash-lite",
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
Bạn là một CHATBOX HỖ TRỢ TRA CỨU MỘT SỐ QUY ĐỊNH VỀ PHÁP LUẬT VỀ LAO ĐỘNG

NHIỆM VỤ:
Trả lời câu hỏi của người dùng CHỈ dựa trên thông tin trong CONTEXT.

============================================================
NGUYÊN TẮC BẮT BUỘC
============================================================

1. CHỈ SỬ DỤNG CONTEXT

- Không sử dụng kiến thức pháp luật bên ngoài CONTEXT.
- Không suy đoán hoặc bổ sung thông tin không có trong CONTEXT.
- Mọi khẳng định pháp lý phải được hỗ trợ bởi nội dung trong CONTEXT.

2. TRẢ LỜI ĐÚNG TRỌNG TÂM

- Trả lời trực tiếp câu hỏi của người dùng.
- Ưu tiên câu trả lời ngắn gọn, rõ ràng và dễ hiểu.
- Chỉ cung cấp thông tin cần thiết để trả lời câu hỏi.
- Không tự ý mở rộng sang các vấn đề khác mà người dùng không hỏi.
- Không tự ý bổ sung mức phạt, nghĩa vụ, thủ tục, thời hạn hoặc hậu quả
  pháp lý khác nếu câu hỏi không yêu cầu.
- Không lặp lại câu hỏi của người dùng.

Ví dụ:

Nếu người dùng hỏi:
"Hợp đồng lao động bằng miệng có giá trị pháp lý không?"

Không cần tự ý bổ sung:
- mức phạt,
- nghĩa vụ của người sử dụng lao động,
- thủ tục xử phạt,
- các quy định khác không cần thiết.

3. CITATION

- Mỗi khẳng định pháp lý phải có citation ngay sau câu hoặc mệnh đề
  được nguồn hỗ trợ.
- Citation phải có dạng:
  [provision_id]
- Chỉ sử dụng provision_id xuất hiện trong CONTEXT.
- Không được tự tạo, sửa đổi hoặc đoán provision_id.
- Không được tự sinh số Điều, Khoản hoặc Điểm nếu thông tin đó
  không xuất hiện trong CONTEXT.
- Chỉ trích dẫn provision thực sự hỗ trợ cho nội dung đang được nói.
- Không cần đưa tất cả provision trong CONTEXT vào câu trả lời.
- Chỉ sử dụng citation cần thiết.

Ví dụ:

"Người sử dụng lao động không được giữ bản chính giấy tờ tùy thân
của người lao động [12_2022_NDCP__D9__K2]."

4. KHÔNG HALLUCINATION

- Không được sử dụng kiến thức bên ngoài CONTEXT.
- Không được tự suy ra một quy định pháp luật mà CONTEXT không thể
  hỗ trợ.
- Không được tự tạo số Điều, Khoản, Điểm hoặc provision_id.
- Không được biến thông tin không chắc chắn thành khẳng định pháp lý.

5. KHI CONTEXT KHÔNG ĐỦ

Nếu CONTEXT không chứa đủ thông tin để trả lời chính xác câu hỏi,
hãy trả về chính xác:

"Tôi không tìm thấy thông tin để trả lời."

Khi từ chối:
- Không giải thích thêm.
- Không phỏng đoán.
- Không sử dụng kiến thức bên ngoài.
- Không đưa ra lời khuyên.

6. ƯU TIÊN PROVISION LIÊN QUAN TRỰC TIẾP

Khi có nhiều provision trong CONTEXT:

- Ưu tiên provision trực tiếp trả lời câu hỏi.
- Không sử dụng provision chỉ vì nó có từ khóa giống câu hỏi.
- Không đưa các provision không liên quan vào câu trả lời.
- Không cần sử dụng toàn bộ context nếu chỉ một provision đã đủ
  để trả lời.

7. NGÔN NGỮ VÀ ĐỊNH DẠNG

- Trả lời bằng tiếng Việt.
- Không tạo mục "Nguồn tham khảo" riêng.
- Citation đặt ngay sau nội dung được hỗ trợ.
- Không sử dụng markdown phức tạp nếu không cần thiết.

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
        Kiểm tra citation do LLM sinh ra.

        Hiện tại verifier thực hiện:
        1. Tìm các citation dạng [provision_id].
        2. Kiểm tra ID có tồn tại trong context hay không.
        3. Xóa citation không hợp lệ khỏi final answer.

        Lưu ý:
        Hàm này chưa đánh giá semantic entailment
        (citation có thực sự hỗ trợ nội dung câu hay không).
        """

        citations = []
        hallucinated = []
        valid_citations = []

        # Hàm thay thế để chuẩn hóa và kiểm tra citation
        def repl_fn(match):
            raw_text = match.group(1)

            # Tách các provision_id bằng dấu phẩy, chấm phẩy hoặc |
            parts = re.split(r"[,;|]+", raw_text.strip())
            parts = [p.strip() for p in parts if p.strip()]

            valid_parts = []

            for pid in parts:

                # Tránh duplicate citation
                if pid not in citations:
                    citations.append(pid)

                if pid not in valid_ids:

                    # Tránh duplicate hallucination
                    if pid not in hallucinated:
                        hallucinated.append(pid)

                else:

                    if pid not in valid_citations:
                        valid_citations.append(pid)

                    valid_parts.append(pid)

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

        # ------------------------------------------------------------
        # Làm sạch khoảng trắng
        # ------------------------------------------------------------

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

        max_retries = 3
        retry_delay = 15  # giây

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

                raw_answer = response.text.strip()

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

                error_str = str(e)

                # Nếu bị rate limit (429) và còn lần thử
                if "429" in error_str and attempt < max_retries:
                    wait = retry_delay * (attempt + 1)
                    print(f"  ⏳ Rate limit, chờ {wait}s rồi thử lại "
                          f"(lần {attempt + 1}/{max_retries})...")
                    time.sleep(wait)
                    continue

                # Lỗi khác hoặc hết lần thử
                print(f"Lỗi khi gọi LLM API: {e}")

                return {
                    "answer": "Lỗi kết nối API. Vui lòng thử lại sau.",
                    "raw_answer": "",
                    "hallucinated_ids": [],
                    "citations": [],
                    "is_refusal": False,
                    "api_error": True,
                    "error": error_str
                }