"""
test_refusal_flow.py
Unit tests cho luồng từ chối (Refusal Classification) trong hệ thống.
"""

import os
import sys
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from generator import classify_refusal, extract_claims


class TestClassifyRefusal:
    """Kiểm tra bộ phân loại từ chối có cấu trúc."""

    # ── Canonical refusal ────────────────────────────────────────────

    def test_canonical_exact(self):
        """Câu từ chối chuẩn được nhận diện chính xác."""
        res = classify_refusal("Tôi không tìm thấy thông tin để trả lời.")
        assert res["is_refusal"] is True
        assert res["confidence"] >= 0.98

    def test_canonical_no_period(self):
        """Câu chuẩn không có dấu chấm cuối cũng phải nhận diện."""
        res = classify_refusal("Tôi không tìm thấy thông tin để trả lời")
        assert res["is_refusal"] is True

    def test_canonical_extra_whitespace(self):
        """Khoảng trắng thừa không ảnh hưởng."""
        res = classify_refusal("  Tôi không tìm thấy thông tin để trả lời.  ")
        assert res["is_refusal"] is True

    # ── Structured pattern refusals ──────────────────────────────────

    @pytest.mark.parametrize("text", [
        "Không tìm thấy thông tin liên quan trong cơ sở dữ liệu.",
        "Ngữ cảnh không chứa quy định về lĩnh vực này.",
        "Câu hỏi nằm ngoài phạm vi pháp luật lao động.",
        "Tài liệu được cung cấp không đề cập đến vấn đề này.",
        "Xin lỗi, tôi không thể trả lời câu hỏi này.",
        "Không thể trả lời dựa trên tài liệu hiện có.",
        "Chưa đủ thông tin để trả lời câu hỏi của bạn.",
    ])
    def test_structured_refusal_patterns(self, text):
        """Các mẫu từ chối ngữ nghĩa đa dạng đều được nhận diện."""
        res = classify_refusal(text)
        assert res["is_refusal"] is True
        assert res["method"] in ("canonical_exact", "canonical_prefix", "structured_pattern", "structured_short_refusal")

    # ── Non-refusals ─────────────────────────────────────────────────

    def test_legal_answer_with_citation(self):
        """Câu trả lời có trích dẫn điều luật KHÔNG phải từ chối."""
        text = "Theo quy định tại Điều 35, người lao động có quyền đơn phương chấm dứt hợp đồng [45_2019_QH14__D35]"
        res = classify_refusal(text)
        assert res["is_refusal"] is False

    def test_normal_answer(self):
        """Câu trả lời bình thường không chứa mẫu từ chối."""
        text = "Thời gian thử việc tối đa là 60 ngày đối với lao động có trình độ đại học."
        res = classify_refusal(text)
        assert res["is_refusal"] is False

    def test_answer_with_negation_not_refusal(self):
        """Câu chứa phủ định nhưng trả lời quy định, không phải từ chối."""
        text = "Người sử dụng lao động không được sa thải lao động nữ đang mang thai [45_2019_QH14__D137]"
        res = classify_refusal(text)
        assert res["is_refusal"] is False

    # ── Empty / edge cases ───────────────────────────────────────────

    def test_empty_is_refusal(self):
        """Câu trả lời rỗng được phân loại là từ chối."""
        res = classify_refusal("")
        assert res["is_refusal"] is True
        assert res["method"] == "empty_text"

    def test_none_text(self):
        """None cũng phải xử lý an toàn."""
        res = classify_refusal(None)
        assert res["is_refusal"] is True

    def test_whitespace_only(self):
        """Chỉ có khoảng trắng = rỗng = từ chối."""
        res = classify_refusal("   \n\t  ")
        assert res["is_refusal"] is True


class TestExtractClaims:
    """Kiểm tra trích xuất luận điểm từ câu trả lời."""

    def test_extract_with_citations(self):
        """Trích xuất claim kèm citation."""
        answer = "Thời gian thử việc tối đa là 60 ngày. [45_2019_QH14__D25__K1]"
        claims = extract_claims(answer)
        assert len(claims) >= 1
        assert claims[0]["has_citation"] is True
        assert "45_2019_QH14__D25__K1" in claims[0]["citations"]

    def test_extract_without_citations(self):
        """Claim không có citation cũng phải được trích xuất."""
        answer = "Người lao động phải tuân thủ kỷ luật lao động."
        claims = extract_claims(answer)
        assert len(claims) >= 1
        assert claims[0]["has_citation"] is False

    def test_extract_bullet_points(self):
        """Danh sách gạch đầu dòng trích xuất nhiều claim riêng biệt."""
        answer = (
            "- Thời gian thử việc tối đa 60 ngày [45_2019_QH14__D25__K1]\n"
            "- Tiền lương thử việc ít nhất 85% [45_2019_QH14__D26]\n"
            "- Kết thúc thử việc phải thông báo kết quả [45_2019_QH14__D27]"
        )
        claims = extract_claims(answer)
        assert len(claims) >= 3

    def test_empty_answer(self):
        """Câu rỗng trả về danh sách rỗng."""
        claims = extract_claims("")
        assert claims == []

    def test_refusal_answer(self):
        """Câu từ chối có thể không trích xuất được claim có ý nghĩa."""
        claims = extract_claims("Tôi không tìm thấy thông tin để trả lời.")
        # Câu quá ngắn, split < 3 tokens → có thể rỗng hoặc 1 claim
        assert len(claims) <= 1
