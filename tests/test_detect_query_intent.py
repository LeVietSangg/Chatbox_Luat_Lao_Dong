import os
import sys
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from retriever import LegalRetriever


class TestDetectQueryIntent:
    """Kiểm thử phát hiện ý định câu hỏi (detect_query_intent)."""

    def test_direct_article_lookup_without_document(self):
        """Hỏi đích danh Điều luật nhưng không nêu tên văn bản -> explicit_doc là None (không mặc định BLLĐ)."""
        intent = LegalRetriever.detect_query_intent("Điều 112 quy định gì về các ngày nghỉ lễ?")
        assert intent["explicit_dieu"] == "112"
        assert intent["is_broad"] is True
        assert intent["explicit_doc"] is None

    def test_direct_article_lookup_with_document(self):
        """Hỏi đích danh Điều luật kèm văn bản cụ thể -> nhận diện đúng văn bản."""
        cases = [
            ("Điều 112 Bộ luật Lao động quy định gì về các ngày nghỉ lễ?", "112", "45_2019_QH14"),
            ("Điều 10 Nghị định 145 quy định thời giờ làm việc ra sao?", "10", "145_2020_NDCP"),
            ("Điều 43 Luật Việc làm quy định về bảo hiểm thất nghiệp thế nào?", "43", "74_2025_QH15"),
            ("Điều 21 Luật BHXH quy định trách nhiệm của cơ quan bảo hiểm?", "21", "58_VBHN-VPQH"),
            ("Điều 14 Luật An toàn vệ sinh lao động quy định gì?", "14", "84_2015_QH13"),
            ("Theo Điều 12 Nghị định 12, mức xử phạt vi phạm là bao nhiêu?", "12", "12_2022_NDCP"),
        ]
        for query, expected_dieu, expected_doc in cases:
            intent = LegalRetriever.detect_query_intent(query)
            assert intent["explicit_dieu"] == expected_dieu, f"Sai số Điều cho: {query}"
            assert intent["explicit_doc"] == expected_doc, f"Sai văn bản cho: {query}"
            assert intent["is_broad"] is True

    def test_no_false_positive_145_money_vs_nd145(self):
        """Phân biệt '145' trong số tiền/số thường với Nghị định 145/2020."""
        # 1. Các câu hỏi chứa 145 nhưng là số tiền, mã số -> KHÔNG phải NĐ 145
        money_queries = [
            "Công ty bồi thường 145 triệu đồng cho tôi có đúng không?",
            "Mức lương thỏa thuận 145k mỗi giờ có hợp pháp không?",
            "Bị phạt tiền 145.000 đồng khi đi trễ thì xử lý thế nào?",
            "Hợp đồng số 145 có hiệu lực từ ngày nào?",
            "Chi phí đào tạo 145 triệu thì phải bồi hoàn thế nào?",
        ]
        for query in money_queries:
            intent = LegalRetriever.detect_query_intent(query)
            assert intent["explicit_doc"] != "145_2020_NDCP", f"Bị nhận nhầm NĐ 145: {query}"
            assert intent["explicit_doc"] is None, f"Gán sai explicit_doc: {query}"

        # 2. Các câu hỏi thực sự hỏi Nghị định 145 -> PHẢI nhận diện 145_2020_NDCP
        decree_queries = [
            "Theo Nghị định 145, người sử dụng lao động có quyền gì?",
            "Theo NĐ 145 quy định về đối thoại tại nơi làm việc ra sao?",
            "Căn cứ Nghị định số 145 về thời giờ làm việc và nghỉ ngơi?",
            "Theo Nghị định 145/2020/NĐ-CP, tiền lương làm thêm giờ tính thế nào?",
            "Quy định tại 145/2020 về giải quyết tranh chấp lao động?",
        ]
        for query in decree_queries:
            intent = LegalRetriever.detect_query_intent(query)
            assert intent["explicit_doc"] == "145_2020_NDCP", f"Không nhận diện được NĐ 145: {query}"

    def test_no_false_positive_year_2019_vs_blld2019(self):
        """Phân biệt năm 2019 (thời gian làm việc/hợp đồng) với Bộ luật Lao động 2019."""
        # 1. Năm 2019 mốc thời gian -> KHÔNG phải BLLĐ 2019
        year_queries = [
            "Tôi vào làm việc từ năm 2019 đến nay thì được bao nhiêu ngày phép?",
            "Hợp đồng lao động ký tháng 5 năm 2019 thì chấm dứt thế nào?",
            "Năm 2019 công ty nợ lương thì thời hiệu khởi kiện còn không?",
            "Từ 2019 đến 2024 tôi chưa được nâng lương định kỳ?",
            "Làm việc từ năm 2012 đến nay có được hưởng trợ cấp thôi việc không?",
        ]
        for query in year_queries:
            intent = LegalRetriever.detect_query_intent(query)
            assert intent["explicit_doc"] != "45_2019_QH14", f"Bị nhận nhầm BLLĐ 2019: {query}"
            assert intent["explicit_doc"] != "10_2012_QH13", f"Bị nhận nhầm BLLĐ 2012: {query}"
            assert intent["explicit_doc"] is None, f"Gán sai explicit_doc: {query}"

        # 2. Đích danh Bộ luật Lao động 2019 / BLLĐ -> PHẢI nhận diện 45_2019_QH14
        code_queries = [
            "Theo Bộ luật Lao động 2019, thời gian thử việc tối đa là bao lâu?",
            "Theo BLLĐ 2019 quy định về đơn phương chấm dứt hợp đồng thế nào?",
            "Theo Bộ luật Lao động, người lao động có quyền gì?",
            "Theo BLLĐ, mức lương tối thiểu vùng được xác định ra sao?",
            "Căn cứ Luật 45/2019/QH14 về tiền lương?",
        ]
        for query in code_queries:
            intent = LegalRetriever.detect_query_intent(query)
            assert intent["explicit_doc"] == "45_2019_QH14", f"Không nhận diện được BLLĐ 2019: {query}"

        # 3. Đích danh Bộ luật Lao động 2012 -> PHẢI nhận diện 10_2012_QH13
        cases_2012 = [
            "Bộ luật lao động 2012 quy định tiền lương ngừng việc ra sao?",
            "Theo BLLĐ 2012 thì thời hạn hợp đồng xác định ra sao?",
            "Căn cứ Luật 10/2012/QH13 về kỷ luật lao động?",
        ]
        for query in cases_2012:
            intent = LegalRetriever.detect_query_intent(query)
            assert intent["explicit_doc"] == "10_2012_QH13", f"Không nhận diện được BLLĐ 2012: {query}"

    def test_insurance_distinction_bhtn_vs_bhxh(self):
        """Phân biệt Bảo hiểm thất nghiệp (Luật Việc làm) với BHXH và từ bảo hiểm nói chung."""
        # 1. Bảo hiểm thất nghiệp / BHTN / Trợ cấp thất nghiệp -> 74_2025_QH15 (Luật Việc làm)
        bhtn_queries = [
            "Điều kiện hưởng bảo hiểm thất nghiệp năm 2024?",
            "Hồ sơ hưởng trợ cấp thất nghiệp gồm những gì?",
            "Thời hạn nộp hồ sơ hưởng BHTN là bao lâu sau khi nghỉ việc?",
            "Mức hưởng bảo hiểm thất nghiệp tối đa là bao nhiêu?",
            "Theo Luật Việc làm, lao động mất việc được hỗ trợ những gì?",
        ]
        for query in bhtn_queries:
            intent = LegalRetriever.detect_query_intent(query)
            assert intent["explicit_doc"] == "74_2025_QH15", (
                f"BHTN bị nhận nhầm thành {intent['explicit_doc']} thay vì 74_2025_QH15: {query}"
            )

        # 2. Bảo hiểm xã hội / BHXH -> 58_VBHN-VPQH (Luật BHXH)
        bhxh_queries = [
            "Theo Luật BHXH, mức đóng bảo hiểm là bao nhiêu?",
            "Chế độ thai sản theo bảo hiểm xã hội gồm những điều kiện gì?",
            "Đóng BHXH tự nguyện được hưởng những chế độ nào?",
            "Rút bảo hiểm xã hội một lần cần điều kiện gì?",
        ]
        for query in bhxh_queries:
            intent = LegalRetriever.detect_query_intent(query)
            assert intent["explicit_doc"] == "58_VBHN-VPQH", f"Sai Luật BHXH: {query}"

        # 3. Từ 'bảo hiểm' nói chung -> KHÔNG tự động ép vào Luật BHXH
        general_queries = [
            "Công ty không đóng bảo hiểm thì có vi phạm không?",
            "Người lao động có được tự đóng bảo hiểm không?",
            "Mức trừ tiền lương để đóng các loại bảo hiểm là bao nhiêu?",
        ]
        for query in general_queries:
            intent = LegalRetriever.detect_query_intent(query)
            assert intent["explicit_doc"] is None, f"Không nên gán explicit_doc cho bảo hiểm chung chung: {query}"

    def test_explicit_document_recognition(self):
        """Nhận diện các văn bản pháp luật khác được chỉ định rõ trong câu hỏi."""
        cases = [
            ("Theo Luật An toàn vệ sinh lao động 2015, trang bị bảo hộ thế nào?", "84_2015_QH13"),
            ("Theo Luật Công đoàn, quyền của cán bộ công đoàn là gì?", "50_2024_QH15"),
            ("Theo Nghị định 12, mức phạt không ký hợp đồng lao động là bao nhiêu?", "12_2022_NDCP"),
            ("Theo Nghị định 152, điều kiện cấp giấy phép lao động cho người nước ngoài là gì?", "152_2020_NDCP"),
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
        assert intent["explicit_doc"] is None
