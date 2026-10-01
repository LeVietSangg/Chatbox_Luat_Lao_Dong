import os
import sys
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from retriever import LegalRetriever


class TestDetectQueryIntent:
    """Kiểm thử phát hiện ý định câu hỏi (detect_query_intent)."""

    def test_direct_article_lookup(self):
        """Nhận diện câu hỏi đích danh Điều luật."""
        intent = LegalRetriever.detect_query_intent("Điều 112 quy định gì về các ngày nghỉ lễ?")
        assert intent["explicit_dieu"] == "112"
        assert intent["is_broad"] is True
        assert intent["explicit_doc"] == "45_2019_QH14"

    def test_explicit_document_recognition(self):
        """Nhận diện văn bản pháp luật được chỉ định rõ trong câu hỏi."""
        cases = [
            ("Theo Nghị định 145, người sử dụng lao động có quyền gì?", "145_2020_NDCP"),
            ("Theo Luật BHXH, mức đóng bảo hiểm là bao nhiêu?", "58_VBHN-VPQH"),
            ("Theo Luật An toàn vệ sinh lao động 2015, trang bị bảo hộ thế nào?", "84_2015_QH13"),
            ("Bộ luật lao động 2012 quy định tiền lương ngừng việc ra sao?", "10_2012_QH13"),
            ("Theo Luật Công đoàn, quyền của cán bộ công đoàn là gì?", "50_2024_QH15"),
        ]
        for query, expected_doc in cases:
            intent = LegalRetriever.detect_query_intent(query)
            assert intent["explicit_doc"] == expected_doc, f"Failed for {query}"

    def test_broad_keyword_detection(self):
        """Kiểm tra nhận diện câu hỏi tổng quan kích hoạt mở rộng."""
        broad_queries = [
            "Trách nhiệm của công ty khi đơn phương chấm dứt hợp đồng là gì?",
            "Chế độ thai sản cho lao động nữ bao gồm những gì?",
            "Các trường hợp được tạm hoãn thực hiện hợp đồng lao động?",
            "Xử lý thế nào khi người lao động tự ý bỏ việc?",
        ]
        for query in broad_queries:
            intent = LegalRetriever.detect_query_intent(query)
            assert intent["is_broad"] is True, f"Failed for: {query}"

    def test_narrow_query_detection(self):
        """Câu hỏi hẹp không chứa từ khóa broad hoặc số Điều."""
        intent = LegalRetriever.detect_query_intent("thời hạn hợp đồng 12 tháng")
        assert intent["explicit_dieu"] is None
        assert intent["is_broad"] is False
