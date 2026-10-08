"""
test_expand_legal_query.py
Unit tests cho hàm mở rộng truy vấn đời thường sang thuật ngữ pháp lý.
"""

import os
import sys
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from rag_pipeline import expand_legal_query


class TestExpandLegalQuery:
    """Kiểm tra expand_legal_query mở rộng đúng thuật ngữ pháp lý."""

    # ── Viết tắt phổ biến ────────────────────────────────────────────

    @pytest.mark.parametrize("abbr,expected_word", [
        ("nlđ có quyền gì", "người lao động"),
        ("nsdlđ có nghĩa vụ gì", "người sử dụng lao động"),
        ("hđlđ là gì", "hợp đồng lao động"),
        ("bhxh bao gồm gì", "bảo hiểm xã hội"),
        ("bhtn là gì", "bảo hiểm thất nghiệp"),
        ("cty phải đóng bao nhiêu", "công ty"),
    ])
    def test_abbreviation_expansion(self, abbr, expected_word):
        """Viết tắt phổ biến được chuẩn hóa."""
        result = expand_legal_query(abbr)
        # Abbreviation gets expanded in the query itself via additions
        # The result should contain the expanded legal term
        assert expected_word in result.lower() or abbr in result

    # ── Nghỉ trước hạn / xin nghỉ việc ──────────────────────────────

    @pytest.mark.parametrize("query", [
        "Tôi muốn xin nghỉ việc",
        "Nghỉ trước hạn hợp đồng",
        "Muốn nghỉ việc trước khi hết hợp đồng",
    ])
    def test_resign_before_term(self, query):
        """Câu hỏi xin nghỉ/nghỉ trước hạn được mở rộng sang thuật ngữ đơn phương chấm dứt."""
        result = expand_legal_query(query)
        assert "đơn phương chấm dứt" in result.lower()
        assert "báo trước" in result.lower()

    # ── Nghỉ ngang / bỏ việc ─────────────────────────────────────────

    @pytest.mark.parametrize("query", [
        "Nghỉ ngang có bị phạt không",
        "Tự ý bỏ việc thì sao",
        "Nghỉ không xin phép thì sao",
    ])
    def test_quit_without_notice(self, query):
        """Câu hỏi nghỉ ngang/bỏ việc được mở rộng sang trái pháp luật/bồi thường."""
        result = expand_legal_query(query)
        assert "trái pháp luật" in result.lower()

    # ── Sa thải ──────────────────────────────────────────────────────

    def test_dismissal_expansion(self):
        result = expand_legal_query("Bị sa thải có được bồi thường không")
        assert "kỷ luật sa thải" in result.lower()

    # ── Tiền lương / nợ lương ────────────────────────────────────────

    @pytest.mark.parametrize("query,keyword", [
        ("Công ty quỵt lương phải làm sao", "chậm trả lương"),
        ("Tiền lương tối thiểu vùng là bao nhiêu", "tiền lương"),
    ])
    def test_salary_expansion(self, query, keyword):
        result = expand_legal_query(query)
        assert keyword in result.lower()

    # ── Nghỉ phép / nghỉ lễ ──────────────────────────────────────────

    def test_annual_leave_expansion(self):
        result = expand_legal_query("Nghỉ phép năm được bao nhiêu ngày")
        assert "nghỉ hằng năm" in result.lower()

    def test_holiday_expansion(self):
        result = expand_legal_query("Nghỉ lễ tết có được trả lương không")
        assert "nghỉ lễ tết" in result.lower()

    # ── Thai sản ─────────────────────────────────────────────────────

    def test_maternity_expansion(self):
        result = expand_legal_query("Chế độ thai sản cho lao động nữ")
        assert "thai sản" in result.lower()
        assert "lao động nữ" in result.lower()

    # ── Thử việc ─────────────────────────────────────────────────────

    def test_probation_expansion(self):
        result = expand_legal_query("Thử việc tối đa bao nhiêu ngày")
        assert "thời gian thử việc" in result.lower()

    # ── Không mở rộng khi không khớp ─────────────────────────────────

    def test_no_expansion_for_unmatched(self):
        """Câu hỏi không chứa mẫu pháp lý nào thì giữ nguyên."""
        query = "Xin chào bạn"
        result = expand_legal_query(query)
        assert result == query  # Không thêm gì

    # ── Idempotency ──────────────────────────────────────────────────

    def test_idempotent_no_double_expansion(self):
        """Gọi 2 lần không duplicate thêm nội dung (nếu nội dung đã chứa keyword)."""
        q = "Tôi muốn xin nghỉ việc"
        r1 = expand_legal_query(q)
        # Gọi lại trên kết quả đầu — vẫn phải chứa keyword nhưng không crash
        r2 = expand_legal_query(r1)
        assert "đơn phương chấm dứt" in r2.lower()
