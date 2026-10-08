import os
import json
import re
import time
import random
import logging
import hashlib

from dotenv import load_dotenv
from google import genai
from google.genai import types

# Tắt cảnh báo AFC không cần thiết của SDK google-genai
logging.getLogger("google").setLevel(logging.ERROR)

# ====================================================================
# STRUCTURED REFUSAL CLASSIFIER & LLM JUDGE
# ====================================================================

REFUSAL_PATTERNS = [
    r"tôi không tìm thấy thông tin",
    r"không tìm thấy thông tin",
    r"không có thông tin",
    r"ngữ cảnh không (?:chứa|có|đề cập|cung cấp)",
    r"tài liệu (?:được cung cấp )?không (?:chứa|có|đề cập|cung cấp|nêu|quy định)",
    r"văn bản (?:được cung cấp )?không (?:chứa|có|đề cập|cung cấp|nêu|quy định)",
    r"(?:nằm )?ngoài phạm vi (?:pháp luật lao động|tài liệu|ngữ cảnh|hệ thống)",
    r"không thuộc phạm vi",
    r"chưa đủ thông tin để trả lời",
    r"không thể trả lời (?:câu hỏi|vấn đề|dựa trên)",
    r"xin lỗi,? (?:tôi )?không thể",
    r"không tìm thấy quy định",
    r"không có căn cứ (?:pháp luật )?để trả lời",
]
RE_REFUSAL_COMPILED = [re.compile(p, re.IGNORECASE) for p in REFUSAL_PATTERNS]
RE_CITATION = re.compile(r"\[([a-zA-Z0-9_]+)\]")

STOPWORDS_VI = {
    'là', 'của', 'và', 'các', 'cho', 'với', 'trong', 'ở', 'theo', 'được', 'khi',
    'này', 'đó', 'thì', 'có', 'những', 'về', 'tại', 'đến', 'từ', 'như', 'sau', 'bởi'
}
COMMON_LEGAL_WORDS = {'người', 'lao', 'động', 'sử', 'dụng'}


def classify_refusal(
    text: str,
    query: str = None,
    use_judge: bool = False,
    client = None,
    model_name: str = "gemini-2.5-flash"
) -> dict:
    """
    Phân loại từ chối (Refusal Classification) có cấu trúc.
    
    Khắc phục hạn chế của việc so khớp chuỗi y hệt (text == REFUSAL_TEXT):
    1. Chuẩn hóa văn bản loại bỏ khoảng trắng, dấu câu cuối, chữ hoa/thường.
    2. Nhận diện các mẫu từ chối ngữ nghĩa đa dạng (out-of-scope, thiếu thông tin, xin lỗi...).
    3. Kiểm tra sự vắng mặt của trích dẫn hợp lệ để tránh nhận nhầm câu trả lời thực tế.
    4. Hỗ trợ LLM Judge khi use_judge=True hoặc khi có yêu cầu thẩm định chuyên sâu.
    """
    if not text or not text.strip():
        return {
            "is_refusal": True,
            "confidence": 1.0,
            "method": "empty_text",
            "reason": "Câu trả lời rỗng hoặc không có nội dung."
        }

    # Nếu bật LLM Judge và có client
    if use_judge and client is not None:
        return judge_refusal(query=query, answer=text, client=client, model_name=model_name)

    clean = text.strip().lower().rstrip(".!? ")
    canonical = "tôi không tìm thấy thông tin để trả lời"

    # 1. Khớp câu chuẩn canonical (cho phép linh hoạt dấu câu)
    if clean == canonical:
        return {
            "is_refusal": True,
            "confidence": 1.0,
            "method": "canonical_exact",
            "reason": "Khớp chính xác câu từ chối chuẩn."
        }

    # 2. Bắt đầu bằng câu từ chối chuẩn
    if clean.startswith(canonical):
        return {
            "is_refusal": True,
            "confidence": 0.98,
            "method": "canonical_prefix",
            "reason": "Bắt đầu bằng câu từ chối chuẩn."
        }

    # 3. Phân loại theo mẫu cấu trúc ngữ nghĩa
    has_citations = bool(RE_CITATION.search(text))
    has_refusal_phrase = any(p.search(clean) for p in RE_REFUSAL_COMPILED)

    # Nếu có cụm từ từ chối và KHÔNG kèm citation hợp lệ -> chắc chắn từ chối
    if has_refusal_phrase and not has_citations:
        return {
            "is_refusal": True,
            "confidence": 0.95,
            "method": "structured_pattern",
            "reason": "Chứa cụm từ từ chối ngữ nghĩa và không có trích dẫn điều luật."
        }

    # Nếu câu ngắn (< 250 ký tự) chứa từ khóa từ chối
    if has_refusal_phrase and len(text.strip()) < 250 and not has_citations:
        return {
            "is_refusal": True,
            "confidence": 0.90,
            "method": "structured_short_refusal",
            "reason": "Đoạn văn ngắn mang ý định từ chối rõ ràng."
        }

    return {
        "is_refusal": False,
        "confidence": 0.95 if has_citations else 0.80,
        "method": "structured_answer",
        "reason": "Chứa nội dung giải đáp quy định pháp lý."
    }


def judge_refusal(
    query: str,
    answer: str,
    client = None,
    model_name: str = "gemini-2.5-flash"
) -> dict:
    """
    Sử dụng LLM-as-a-Judge để phân loại có cấu trúc xem câu trả lời có phải là lời từ chối hay không.
    """
    if client is None:
        return classify_refusal(answer, query=query, use_judge=False)

    judge_prompt = f"""Bạn là trọng tài AI (LLM Judge) đánh giá Chatbot Pháp luật Lao động.
Nhiệm vụ: Phân loại câu trả lời sau đây có phải là một lời "TỪ CHỐI TRẢ LỜI" (Refusal) hay không.

Tiêu chí TỪ CHỐI (is_refusal = true):
- Chatbot từ chối vì câu hỏi nằm ngoài phạm vi pháp luật lao động (hình sự, thuế, đất đai, giải trí...).
- Chatbot từ chối vì không tìm thấy thông tin/căn cứ pháp lý trong tài liệu được cung cấp.
- Chatbot tuyên bố không thể cung cấp câu trả lời hoặc tài liệu không đề cập.

Tiêu chí KHÔNG TỪ CHỐI (is_refusal = false):
- Chatbot cung cấp giải đáp quy định pháp lý, quyền, nghĩa vụ, thời hạn, hoặc căn cứ điều luật.

Câu hỏi:
\"\"\"{query or 'N/A'}\"\"\"

Câu trả lời của Chatbot:
\"\"\"{answer}\"\"\"

Chỉ trả về JSON hợp lệ:
{{"is_refusal": true, "confidence": 0.95, "reason": "Lý do ngắn gọn"}}
"""
    try:
        config = types.GenerateContentConfig(
            temperature=0.0,
            response_mime_type="application/json"
        )
        res = client.models.generate_content(
            model=model_name,
            contents=judge_prompt,
            config=config
        )
        raw = res.text.strip()
        data = json.loads(raw)
        return {
            "is_refusal": bool(data.get("is_refusal", False)),
            "confidence": float(data.get("confidence", 0.9)),
            "method": "llm_judge",
            "reason": str(data.get("reason", "LLM Judge classification"))
        }
    except Exception as e:
        fallback = classify_refusal(answer, query=query, use_judge=False)
        fallback["reason"] += f" (Judge error fallback: {e})"
        return fallback


# ====================================================================
# CLAIM EXTRACTION & CLAIM SUPPORT MEASUREMENT
# ====================================================================

def extract_claims(answer: str) -> list[dict]:
    """
    Trích xuất các luận điểm (claims) từ câu trả lời và liên kết với citation tương ứng.
    """
    if not answer or not answer.strip():
        return []

    lines = [line.strip() for line in answer.strip().split('\n') if line.strip()]
    raw_segments = []

    for line in lines:
        if re.match(r'^(?:[-*•]|\d+\.)\s+', line):
            raw_segments.append(line)
        else:
            parts = re.split(r'(?<=[.!?])\s+(?=[A-Z0-9À-ỸĐ])', line)
            for p in parts:
                p = p.strip()
                if p:
                    raw_segments.append(p)

    claims = []
    for idx, seg in enumerate(raw_segments):
        cits = RE_CITATION.findall(seg)
        claim_text = RE_CITATION.sub('', seg).strip()
        claim_text = re.sub(r'^(?:[-*•]|\d+\.)\s*', '', claim_text)
        claim_text = re.sub(r'[*_#`]', '', claim_text)
        claim_text = re.sub(r'[ \t]+', ' ', claim_text).strip()
        claim_text = claim_text.rstrip(' ,;:')

        if len(claim_text.split()) < 3:
            continue

        claims.append({
            'claim_id': f'c_{idx+1}',
            'text': claim_text,
            'citations': list(dict.fromkeys(cits)),
            'has_citation': len(cits) > 0
        })

    return claims


def _clean_text_for_support(text: str) -> str:
    text = text.lower()
    text = re.sub(r'[*_#`]', '', text)
    text = re.sub(r'\[[a-zA-Z0-9_]+\]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def _extract_quantities(text: str) -> list[str]:
    clean = _clean_text_for_support(text)
    patterns = [
        r'\b\d+(?:[.,]\d+)*\s*(?:ngày|tháng|năm|giờ|%|phần trăm|triệu|nghìn|đồng)\b',
        r'\b\d+(?:[.,]\d+)+\b',
    ]
    quantities = []
    for pat in patterns:
        for match in re.finditer(pat, clean, re.IGNORECASE):
            quantities.append(match.group(0).strip())
    return list(dict.fromkeys(quantities))



def _normalize_num(s: str) -> str:
    s = re.sub(r'\.', '', s)
    s = re.sub(r'\b0+(\d+)', r'\1', s)
    return s.strip()


def verify_claim_support_heuristic(claim_text: str, provision_text: str) -> dict:
    """
    Kiểm chứng mức độ bảo chứng của căn cứ pháp lý cho một luận điểm bằng heuristic & NLI grounding.
    """
    if not claim_text or not provision_text:
        return {'supported': False, 'confidence': 1.0, 'method': 'empty_input', 'reason': 'Dữ liệu rỗng'}

    c_clean = _clean_text_for_support(claim_text)
    p_clean = _clean_text_for_support(provision_text)

    # 1. Trực tiếp substring
    if c_clean in p_clean or p_clean in c_clean:
        return {'supported': True, 'confidence': 1.0, 'method': 'direct_substring', 'reason': 'Khẳng định trùng khớp trực tiếp nội dung điều luật'}

    # 2. Số liệu & định lượng
    c_quantities = _extract_quantities(c_clean)
    p_clean_norm = _normalize_num(p_clean)

    for q in c_quantities:
        q_norm = _normalize_num(q)
        num_match = re.search(r'\d+(?:[.,]\d+)*', q)
        if num_match:
            num_val = num_match.group(0)
            num_norm = _normalize_num(num_val)
            # Kiểm tra xem con số có xuất hiện trong điều luật không
            if num_val not in p_clean and num_norm not in p_clean_norm:
                return {
                    'supported': False,
                    'confidence': 0.95,
                    'method': 'numerical_mismatch',
                    'reason': f'Số liệu/thời hạn "{q}" trong khẳng định không có trong điều luật'
                }
            # Nếu có đơn vị đi kèm (đồng, ngày, tháng, năm, giờ, %): kiểm tra đơn vị có trong điều luật
            unit_part = q[num_match.end():].strip()
            if unit_part and len(unit_part) > 1:
                base_unit = re.search(r'(?:ngày|tháng|năm|giờ|%|phần trăm|triệu|nghìn|đồng)', unit_part)
                if base_unit and base_unit.group(0) not in p_clean:
                    return {
                        'supported': False,
                        'confidence': 0.90,
                        'method': 'unit_mismatch',
                        'reason': f'Đơn vị đo lường "{base_unit.group(0)}" của "{q}" không có trong điều luật'
                    }
        elif q not in p_clean and q_norm not in p_clean_norm:
            return {
                'supported': False,
                'confidence': 0.95,
                'method': 'numerical_mismatch',
                'reason': f'Số liệu/thời hạn "{q}" trong khẳng định không có trong điều luật'
            }


    # 3. Phủ định / cấm đoán
    c_prohibited = any(w in c_clean for w in ['không được', 'nghiêm cấm', 'bị cấm'])
    p_prohibited = any(w in p_clean for w in ['không được', 'nghiêm cấm', 'bị cấm'])
    if c_prohibited and not p_prohibited and len(c_clean.split()) < 15:
        return {
            'supported': False,
            'confidence': 0.9,
            'method': 'polarity_mismatch',
            'reason': 'Khẳng định mang tính cấm đoán nhưng điều luật không quy định cấm'
        }

    # 4. Token overlap với lọc từ phổ biến
    c_tokens = [w for w in re.findall(r'\b\w+\b', c_clean) if w not in STOPWORDS_VI and len(w) > 1]
    p_tokens = set(re.findall(r'\b\w+\b', p_clean))

    if not c_tokens:
        return {'supported': True, 'confidence': 0.7, 'method': 'no_content_tokens', 'reason': 'Không có từ khóa phủ định'}

    distinct_c_tokens = [w for w in c_tokens if w not in COMMON_LEGAL_WORDS]
    if distinct_c_tokens:
        distinct_matched = [t for t in distinct_c_tokens if t in p_tokens]
        distinct_coverage = len(distinct_matched) / len(distinct_c_tokens)
    else:
        distinct_coverage = 1.0

    matched_tokens = [t for t in c_tokens if t in p_tokens]
    coverage = len(matched_tokens) / len(c_tokens)

    if coverage >= 0.60 and distinct_coverage >= 0.50:
        return {
            'supported': True,
            'confidence': round((coverage + distinct_coverage) / 2, 2),
            'method': 'content_overlap',
            'reason': f'Độ bao phủ từ khóa pháp lý cao ({coverage:.1%}, đặc trưng: {distinct_coverage:.1%}) và số liệu nhất quán'
        }
    else:
        return {
            'supported': False,
            'confidence': round(1.0 - coverage, 2),
            'method': 'low_content_overlap',
            'reason': f'Độ bao phủ từ khóa pháp lý chưa đủ ({coverage:.1%}, đặc trưng: {distinct_coverage:.1%}), thiếu cơ sở bảo chứng'
        }


def verify_claim_support(
    claim_text: str,
    provision_text: str,
    judge_client = None,
    model_name: str = "gemini-2.5-flash"
) -> dict:
    """
    Đo lường mức độ bảo chứng của căn cứ pháp lý cho một luận điểm (Claim Support).
    Hỗ trợ cả LLM Judge và heuristic NLI grounding.
    """
    if judge_client is not None:
        judge_prompt = f"""Bạn là trọng tài AI (LLM Judge) kiểm chứng mức độ bảo chứng căn cứ pháp luật (Claim Support / Fact Verification).
Nhiệm vụ: Đánh giá xem Nội dung điều luật có chứng thực/bảo chứng cho Khẳng định pháp lý hay không.

NỘI DUNG ĐIỀU LUẬT:
\"\"\"{provision_text}\"\"\"

KHẲNG ĐỊNH CỦA CHATBOT:
\"\"\"{claim_text}\"\"\"

Quy tắc:
- SUPPORTED (true): Toàn bộ thông tin, số liệu, thời hạn, điều kiện trong Khẳng định đều được Căn cứ điều luật xác thực trực tiếp hoặc suy luận tất yếu.
- UNSUPPORTED (false): Khẳng định chứa số liệu sai lệch, gán ghép nghĩa vụ/quyền lợi không có trong điều luật, hoặc điều luật không đề cập đến nội dung khẳng định.

Chỉ trả về JSON hợp lệ:
{{"supported": true, "confidence": 0.95, "reason": "Lý do ngắn gọn"}}
"""
        try:
            config = types.GenerateContentConfig(
                temperature=0.0,
                response_mime_type="application/json"
            )
            res = judge_client.models.generate_content(
                model=model_name,
                contents=judge_prompt,
                config=config
            )
            raw = res.text.strip()
            data = json.loads(raw)
            return {
                "supported": bool(data.get("supported", False)),
                "confidence": float(data.get("confidence", 0.9)),
                "method": "llm_judge",
                "reason": str(data.get("reason", "LLM Judge verification"))
            }
        except Exception:
            return verify_claim_support_heuristic(claim_text, provision_text)

    return verify_claim_support_heuristic(claim_text, provision_text)


def evaluate_answer_claim_support(
    answer: str,
    context_lookup: dict,
    judge_client = None,
    model_name: str = "gemini-2.5-flash"
) -> dict:
    """
    Đánh giá mức độ Claim Support cho toàn bộ câu trả lời.
    """
    claims = extract_claims(answer)
    if not claims:
        return {
            "total_claims": 0,
            "cited_claims": 0,
            "supported_claims": 0,
            "unsupported_claims": 0,
            "claim_support_rate": None,
            "overall_claim_support_rate": None,
            "is_fully_supported": True,
            "claims": []
        }

    def find_provision_text(pid):
        if pid in context_lookup:
            val = context_lookup[pid]
            return val if isinstance(val, str) else val.get("noi_dung", "")
        # Thử tìm theo mã cha nếu mã con bị rút gọn (__a -> __K2)
        cand = pid
        while "__" in cand:
            cand = cand.rsplit("__", 1)[0]
            if cand in context_lookup:
                val = context_lookup[cand]
                return val if isinstance(val, str) else val.get("noi_dung", "")
        return ""

    detailed_claims = []
    supported_count = 0
    cited_count = 0

    for cl in claims:
        c_text = cl["text"]
        cits = cl["citations"]
        is_cited = len(cits) > 0
        if is_cited:
            cited_count += 1

        is_supp = False
        reasons = []

        if not is_cited:
            reasons.append("Luận điểm không kèm trích dẫn điều luật.")
        else:
            for pid in cits:
                prov_text = find_provision_text(pid)
                if not prov_text:
                    reasons.append(f"Mã điều luật {pid} không có trong ngữ cảnh/corpus.")
                    continue
                ver_res = verify_claim_support(
                    claim_text=c_text,
                    provision_text=prov_text,
                    judge_client=judge_client,
                    model_name=model_name
                )
                if ver_res["supported"]:
                    is_supp = True
                    reasons.append(f"[{pid}] {ver_res['reason']}")
                    break
                else:
                    reasons.append(f"[{pid}] {ver_res['reason']}")

        if is_supp:
            supported_count += 1

        detailed_claims.append({
            "claim_id": cl["claim_id"],
            "text": c_text,
            "citations": cits,
            "has_citation": is_cited,
            "supported": is_supp,
            "reasons": reasons
        })

    claim_support_rate = (supported_count / cited_count) if cited_count > 0 else 0.0
    overall_support_rate = (supported_count / len(claims)) if claims else 0.0
    is_fully_supported = (supported_count == len(claims) and len(claims) > 0)

    return {
        "total_claims": len(claims),
        "cited_claims": cited_count,
        "supported_claims": supported_count,
        "unsupported_claims": cited_count - supported_count,
        "claim_support_rate": claim_support_rate,
        "overall_claim_support_rate": overall_support_rate,
        "is_fully_supported": is_fully_supported,
        "claims": detailed_claims
    }


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

    def is_refusal_response(self, text: str, query: str = None, use_judge: bool = False) -> bool:
        """
        Kiểm tra câu trả lời có phải là lời từ chối hay không bằng phân loại có cấu trúc hoặc judge.
        """
        res = classify_refusal(
            text,
            query=query,
            use_judge=use_judge,
            client=getattr(self, "client", None),
            model_name=getattr(self, "model_name", "gemini-2.5-flash")
        )
        return res["is_refusal"]


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
- Người dùng thường dùng từ ngữ đời thường, hãy đối chiếu với các khái niệm và quy định tương ứng trong CONTEXT để trả lời:
  + "Nghỉ ngang", "nghỉ việc ngang", "tự ý nghỉ", "bỏ việc", "nghỉ không báo trước" ➔ Đơn phương chấm dứt hợp đồng lao động trái pháp luật, nghĩa vụ bồi thường khi tự ý bỏ việc.
  + "Nghỉ trước hạn", "xin nghỉ việc", "muốn nghỉ việc" ➔ Quyền đơn phương chấm dứt hợp đồng lao động của người lao động và thời hạn báo trước.
  + "Cho nghỉ đột ngột", "đuổi việc đột ngột", "đuổi việc không báo trước" ➔ Người sử dụng lao động đơn phương chấm dứt hợp đồng lao động trái pháp luật hoặc vi phạm thời hạn báo trước.
  + "Nghỉ phép năm có được nhận tiền không", "tiền lương nghỉ phép" ➔ Tiền lương ngày nghỉ hằng năm hưởng nguyên lương, thanh toán tiền lương những ngày chưa nghỉ.
  + "Chủ", "sếp", "công ty" ➔ Người sử dụng lao động.
  + "Nhân viên", "người làm", "công nhân" ➔ Người lao động.
  + "Bắt làm", "ép làm" ➔ Cưỡng bức lao động, buộc làm việc trái ý muốn hoặc vi phạm điều kiện làm thêm giờ.
  + "Đuổi việc", "cho nghỉ việc" ➔ Sa thải, đơn phương chấm dứt hợp đồng lao động.
  + "Quỵt lương", "nợ lương", "bùng lương" ➔ Chậm trả lương, vi phạm nguyên tắc và kỳ hạn trả lương.

4. PHÂN BIỆT CÂU HỎI VÀ NGUYÊN TẮC TỪ CHỐI (REFUSAL CRITERIA)
- CÂU HỎI THỰC TẾ CÓ ĐẠI TỪ XƯNG HÔ (VẪN TRẢ LỜI QUY ĐỊNH):
  Người dùng thường hỏi tình huống đời thường ("Tôi muốn nghỉ trước hạn thì làm sao", "Sếp cho tôi nghỉ đột ngột có được không", "Công ty nợ lương tôi thì quy định thế nào", "Nghỉ phép năm có được nhận tiền không"). Nếu bản chất là hỏi về quy định, quyền, nghĩa vụ hoặc điều kiện pháp luật lao động ➔ PHẢI TRẢ LỜI các căn cứ pháp luật tương ứng có trong CONTEXT (ví dụ: quy định về quyền đơn phương chấm dứt hợp đồng, thời hạn báo trước, trách nhiệm pháp lý khi chậm trả lương hoặc chế độ tiền lương ngày nghỉ hằng năm có trong CONTEXT).

- CÂU HỎI BẮT BUỘC TỪ CHỐI (OUT-OF-SCOPE):
  CHỈ từ chối bằng chính xác câu sau:
  "Tôi không tìm thấy thông tin để trả lời."
  trong các trường hợp:
  a) Xin lời khuyên/định hướng quyết định cá nhân mang tính chủ quan (như nên khởi kiện ra tòa hay hòa giải, có nên thôi việc để chuyển nghề).
  b) Yêu cầu tính toán cụ thể số tiền bồi thường cho một vụ việc cá nhân thay cho tòa án.
  c) Yêu cầu sáng tác nội dung phi pháp lý (như làm thơ, viết văn nghệ thuật, soạn thư từ mang tính cảm xúc cá nhân).
  d) Lĩnh vực pháp luật khác ngoài pháp luật lao động (hình sự, đất đai, thuế, giao thông, hôn nhân gia đình...).
  e) Chào hỏi thông thường, câu hỏi phiếm, thời tiết, toán học, câu hỏi vô nghĩa.
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

    def verify_citations(self, answer, valid_ids, return_normalized=False):
        """
        Kiểm tra và chuẩn hóa cú pháp citation do LLM sinh ra (Syntactic Verifier).

        - Citation tồn tại trong valid_ids: giữ nguyên.
        - Citation con (__a, __b, ...): nếu citation cha tồn tại
        trong valid_ids thì chuẩn hóa về citation cha để hiển thị.
        - Thu thập `normalized_ids` (những mã con bị rút gọn):
          Dùng để phạt trong chỉ số Citation Validity (câu nào bị rút mã
          sẽ bị tính là KHÔNG HỢP LỆ do tự bịa mã con ngoài context).
        - Citation không tồn tại và không có citation cha hợp lệ:
        loại bỏ và ghi nhận là hallucinated.
        """

        citations = []
        hallucinated = []
        valid_citations = []
        normalized_sub_ids = []

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

                    # Nếu phải rút mã từ mã con về mã cha (khác với mã gốc)
                    if normalized_pid != pid:
                        if pid not in normalized_sub_ids:
                            normalized_sub_ids.append(pid)

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

        self.last_hallucinated_ids = list(set(hallucinated))
        self.last_normalized_ids = list(set(normalized_sub_ids))

        if return_normalized:
            return (
                verified_answer,
                list(set(hallucinated)),
                list(set(valid_citations)),
                list(set(normalized_sub_ids))
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
        citations,
        normalized_ids=None
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
            # Generation input (hash only — avoid leaking full prompt)
            # --------------------------------------------------------

            "prompt_hash": hashlib.sha256(prompt.encode("utf-8")).hexdigest()[:16],

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
            "normalized_ids": normalized_ids or [],

            # --------------------------------------------------------
            # Refusal (Phân loại có cấu trúc / Judge)
            # --------------------------------------------------------

            "is_refusal": self.is_refusal_response(
                final_answer,
                query=query
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

        # Lỗi tạm thời cần retry (phân loại theo mã HTTP và loại exception)
        RETRYABLE_HTTP_CODES = {429, 500, 503}
        RETRYABLE_KEYWORDS = ("resource_exhausted", "overloaded", "empty_response")

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
                    citations,
                    normalized_ids
                ) = self.verify_citations(
                    raw_answer,
                    valid_ids,
                    return_normalized=True
                )

                # --------------------------------------------------------
                # 5. Nếu Gemini trả rỗng
                # --------------------------------------------------------

                if not final_answer:

                    final_answer = self.REFUSAL_TEXT

                # --------------------------------------------------------
                # 6. Kiểm tra refusal (Phân loại có cấu trúc / Judge)
                # --------------------------------------------------------

                is_refusal = self.is_refusal_response(
                    final_answer,
                    query=query
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
                    citations=citations,
                    normalized_ids=normalized_ids
                )

                # --------------------------------------------------------
                # 8. Return
                # --------------------------------------------------------

                return {
                    "answer": final_answer,
                    "raw_answer": raw_answer,
                    "hallucinated_ids": hallucinated,
                    "normalized_ids": normalized_ids,
                    "citations": citations,
                    "is_refusal": is_refusal,
                    "api_error": False
                }

            except Exception as e:

                # Kiểm tra mã HTTP từ thuộc tính exception (ưu tiên) rồi mới fallback string
                http_code = getattr(e, "code", None) or getattr(e, "status_code", None)
                error_str = str(e).lower()

                is_retryable = (
                    isinstance(http_code, int)
                    and http_code in RETRYABLE_HTTP_CODES
                )

                if is_retryable and attempt < max_retries:
                    # Exponential backoff với jitter
                    wait = min(base_delay * (2 ** attempt), max_delay)
                    jitter = wait * 0.2 * random.random()  # ±20%
                    wait = wait + jitter

                    label = "Rate limit" if http_code == 429 else "Overload"
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