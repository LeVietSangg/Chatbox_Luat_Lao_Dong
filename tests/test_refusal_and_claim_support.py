import os
import sys
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from generator import (
    LegalGenerator,
    classify_refusal,
    extract_claims,
    verify_claim_support_heuristic,
    evaluate_answer_claim_support,
)
from evaluate_generation import compute_metrics


# =====================================================================
# 1. PHÂN LOẠI TỪ CHỐI CÓ CẤU TRÚC (STRUCTURED REFUSAL CLASSIFICATION)
# =====================================================================

class TestStructuredRefusalClassification:
    """Kiểm tra khắc phục lỗi 'Từ chối nhận bằng so khớp chuỗi y hệt'."""

    def test_canonical_exact_match(self):
        """Khớp chuỗi từ chối chuẩn xác."""
        ans = "Tôi không tìm thấy thông tin để trả lời."
        res = classify_refusal(ans)
        assert res["is_refusal"] is True
        assert res["confidence"] >= 0.95

    def test_canonical_without_period_and_spaces(self):
        """Khớp câu từ chối chuẩn khi thiếu dấu chấm hoặc thừa khoảng trắng."""
        ans = "  Tôi không tìm thấy thông tin để trả lời   "
        res = classify_refusal(ans)
        assert res["is_refusal"] is True

    def test_canonical_with_polite_or_context_prefix(self):
        """Từ chối có biến thể câu chữ hoặc văn cảnh bổ sung."""
        variations = [
            "Tôi không tìm thấy thông tin để trả lời trong tài liệu được cung cấp.",
            "Xin lỗi, tôi không tìm thấy thông tin liên quan đến câu hỏi này.",
            "Hiện tại tài liệu không có thông tin về vấn đề bạn đang hỏi.",
            "Nội dung này nằm ngoài phạm vi tài liệu pháp luật lao động được cung cấp.",
            "Ngữ cảnh không chứa thông tin về quy định xử phạt giao thông.",
            "Tài liệu được cung cấp không đề cập đến trường hợp này.",
            "Chưa đủ thông tin để trả lời câu hỏi của bạn.",
        ]
        for v in variations:
            res = classify_refusal(v)
            assert res["is_refusal"] is True, f"Thất bại với câu: '{v}'"

    def test_empty_or_whitespace_answer(self):
        """Câu trả lời rỗng hoặc chỉ có khoảng trắng phải được xem là từ chối."""
        assert classify_refusal("")["is_refusal"] is True
        assert classify_refusal("   \n\t  ")["is_refusal"] is True

    def test_substantive_answer_with_citations_is_not_refusal(self):
        """Câu trả lời thực chất có căn cứ và trích dẫn không được coi là từ chối."""
        ans = "Người lao động được nghỉ phép 12 ngày làm việc trong điều kiện bình thường [45_2019_QH14__D113__K1]."
        res = classify_refusal(ans)
        assert res["is_refusal"] is False

    def test_answer_mentioning_lack_of_subsidiary_info_is_not_refusal(self):
        """Câu trả lời giải thích quy định chính nhưng ghi chú thêm tài liệu không nói chi tiết phụ."""
        ans = (
            "Theo quy định tại Điều 113, người lao động được nghỉ phép 12 ngày [45_2019_QH14__D113__K1]. "
            "Đối với các trường hợp đặc thù ngoài danh mục, tài liệu không quy định chi tiết."
        )
        res = classify_refusal(ans)
        assert res["is_refusal"] is False

    def test_legal_generator_method_integration(self):
        """Phương thức generator.is_refusal_response hoạt động đồng bộ."""
        gen = LegalGenerator.__new__(LegalGenerator)
        gen.REFUSAL_TEXT = "Tôi không tìm thấy thông tin để trả lời."
        
        assert gen.is_refusal_response("Tôi không tìm thấy thông tin để trả lời.") is True
        assert gen.is_refusal_response("Tôi không tìm thấy thông tin trong tài liệu.") is True
        assert gen.is_refusal_response("Theo Điều 35, bạn được quyền nghỉ việc [45_2019_QH14__D35].") is False


# =====================================================================
# 2. ĐO LƯỜNG CLAIM SUPPORT (CLAIM EXTRACTION & SEMANTIC VERIFICATION)
# =====================================================================

class TestClaimSupportMeasurement:
    """Kiểm tra khắc phục hạn chế 'verifier rút mã con __a về mã cha khiến Citation Validity chỉ là cú pháp'."""

    def test_extract_claims_from_various_formats(self):
        """Trích xuất claim chính xác từ đoạn văn và danh sách đánh số."""
        text = """Khi nghỉ việc, trợ cấp thôi việc được tính như sau:
1. Thời gian làm việc để tính trợ cấp thôi việc là tổng thời gian thực tế [45_2019_QH14__D46__K2].
2. Tiền lương để tính trợ cấp thôi việc là bình quân của 06 tháng [45_2019_QH14__D46__K3]."""

        claims = extract_claims(text)
        assert len(claims) == 3
        # Claim 1: câu dẫn, không có citation
        assert claims[0]["has_citation"] is False
        # Claim 2: có citation D46__K2
        assert claims[1]["has_citation"] is True
        assert claims[1]["citations"] == ["45_2019_QH14__D46__K2"]
        # Claim 3: có citation D46__K3
        assert claims[2]["has_citation"] is True
        assert claims[2]["citations"] == ["45_2019_QH14__D46__K3"]

    def test_verify_claim_support_exact_match(self):
        """Luận điểm khớp chính xác nội dung điều luật -> SUPPORTED."""
        prov = "3. Tiền lương để tính trợ cấp thôi việc là tiền lương bình quân của 06 tháng liền kề theo hợp đồng lao động trước khi người lao động thôi việc."
        claim = "Tiền lương để tính trợ cấp thôi việc là tiền lương bình quân của 06 tháng liền kề"
        res = verify_claim_support_heuristic(claim, prov)
        assert res["supported"] is True

    def test_verify_claim_support_numerical_mismatch(self):
        """Luận điểm bịa đặt / sai số liệu (hallucination) -> UNSUPPORTED."""
        prov = "3. Tiền lương để tính trợ cấp thôi việc là tiền lương bình quân của 06 tháng liền kề."
        # Thay 06 tháng thành 12 tháng (mặc dù ID Điều 46 Khoản 3 tồn tại trong context)
        claim = "Tiền lương để tính trợ cấp thôi việc là tiền lương bình quân của 12 tháng liền kề"
        res = verify_claim_support_heuristic(claim, prov)
        assert res["supported"] is False
        assert "12 tháng" in res["reason"] or "Số liệu" in res["reason"]

    def test_verify_claim_support_unrelated_topic(self):
        """Luận điểm gán mã điều luật hoàn toàn không liên quan -> UNSUPPORTED."""
        prov = "Điều 46. Trợ cấp thôi việc\nTiền lương để tính trợ cấp thôi việc là bình quân của 06 tháng liền kề."
        claim = "Người lao động được nghỉ thai sản 06 tháng và hưởng chế độ bảo hiểm xã hội"
        res = verify_claim_support_heuristic(claim, prov)
        assert res["supported"] is False

    def test_evaluate_answer_claim_support_with_sub_id_parent_lookup(self):
        """
        Chứng minh kiểm tra ngữ nghĩa khi mã con __a được rút gọn về mã cha:
        Nội dung Khoản 2 chứa Điểm a -> claim vẫn được bảo chứng dựa trên nội dung Khoản cha.
        """
        prov_k2 = """Điều 10. Hình thức hợp đồng lao động
2. Hợp đồng lao động có thể giao kết bằng các hình thức:
a) Văn bản giấy có chữ ký của hai bên;
b) Thông điệp dữ liệu điện tử có giá trị như văn bản giấy."""

        context_lookup = {
            "145_2020_NDCP__D10__K2": prov_k2
        }

        # LLM trích dẫn mã cha (sau khi verifier đã chuẩn hóa từ __a về __K2)
        answer = "Hợp đồng lao động có thể giao kết bằng thông điệp dữ liệu điện tử [145_2020_NDCP__D10__K2]."
        res = evaluate_answer_claim_support(answer, context_lookup)

        assert res["total_claims"] == 1
        assert res["cited_claims"] == 1
        assert res["supported_claims"] == 1
        assert res["claim_support_rate"] == 1.0
        assert res["is_fully_supported"] is True

    def test_evaluate_answer_claim_support_with_hallucinated_claim(self):
        """Phát hiện luận điểm bịa đặt số liệu dù ID nằm trong context."""
        prov_k1 = "1. Người lao động làm việc đủ 12 tháng thì được nghỉ 12 ngày phép hằng năm."
        context_lookup = {
            "45_2019_QH14__D113__K1": prov_k1
        }

        # ID hoàn toàn hợp lệ, nhưng số liệu nói 50 ngày (Citation Validity nói đúng, Claim Support nói sai)
        answer = "Người lao động làm việc đủ 12 tháng thì được nghỉ 50 ngày phép hằng năm [45_2019_QH14__D113__K1]."
        res = evaluate_answer_claim_support(answer, context_lookup)

        assert res["supported_claims"] == 0
        assert res["unsupported_claims"] == 1
        assert res["claim_support_rate"] == 0.0
        assert res["is_fully_supported"] is False


# =====================================================================
# 3. TÍCH HỢP ĐÁNH GIÁ TỔNG THỂ (COMPUTE_METRICS)
# =====================================================================

class TestComputeMetricsWithStructuredRefusalAndClaimSupport:
    """Kiểm tra hàm compute_metrics tổng thể xuất đầy đủ chỉ số mới."""

    def test_compute_metrics_integrated(self):
        fake_results = [
            # In-scope: trả lời đúng, trích dẫn đúng, claim được bảo chứng
            {
                "qid": "q_01",
                "question": "Hợp đồng lao động bằng lời nói có được không?",
                "is_out_of_scope": False,
                "gold_ids": ["45_2019_QH14__D14__K2"],
                "retrieved_ids": ["45_2019_QH14__D14__K2"],
                "context_map": {
                    "45_2019_QH14__D14__K2": "2. Hai bên có thể giao kết hợp đồng lao động bằng lời nói đối với hợp đồng dưới 01 tháng."
                },
                "answer": "Hai bên có thể giao kết hợp đồng lao động bằng lời nói đối với hợp đồng dưới 01 tháng [45_2019_QH14__D14__K2].",
                "citations": ["45_2019_QH14__D14__K2"],
                "hallucinated_ids": [],
                "is_refusal": False,
                "generation_time": 1.2
            },
            # Out-of-scope: từ chối bằng biến thể ngữ nghĩa (không trùng chuỗi y hệt)
            {
                "qid": "q_02",
                "question": "Vượt đèn đỏ bị phạt bao nhiêu tiền?",
                "is_out_of_scope": True,
                "gold_ids": [],
                "retrieved_ids": [],
                "context_map": {},
                "answer": "Nội dung câu hỏi này nằm ngoài phạm vi tài liệu pháp luật lao động được cung cấp.",
                "citations": [],
                "hallucinated_ids": [],
                "is_refusal": False,  # Trước đây so khớp y hệt sẽ đánh giá sai là False
                "generation_time": 0.8
            }
        ]

        metrics = compute_metrics(fake_results)

        # 1. Refusal Accuracy nhận diện đúng biến thể câu ngoài phạm vi
        assert metrics["refusal_accuracy"] == 1.0
        assert metrics["false_acceptance_rate"] == 0.0

        # 2. Citation Validity (cú pháp)
        assert metrics["citation_validity"] == 1.0

        # 3. Claim Support (ngữ nghĩa)
        assert metrics["total_claims"] >= 1
        assert metrics["supported_claims"] >= 1
        assert metrics["claim_support_rate"] == 1.0
        assert metrics["fully_supported_rate"] == 1.0


# =====================================================================
# 4. KIỂM THỬ CITATION VALIDITY CHÍNH XÁC (PHẠT MÃ CON TỰ CHẾ BỊ RÚT)
# =====================================================================

class TestStrictCitationValidityAndNormalization:
    """
    Kiểm tra xử lý triệt để: Khi LLM tự chế mã con (ví dụ __D25__K4__a)
    và verifier rút về mã cha (__D25__K4), câu đó PHẢI ĐƯỢC TÍNH LÀ KHÔNG HỢP LỆ
    trong chỉ số Citation Validity (Strict).
    """

    @pytest.fixture
    def generator(self):
        gen = LegalGenerator.__new__(LegalGenerator)
        gen.REFUSAL_TEXT = "Tôi không tìm thấy thông tin để trả lời."
        return gen

    def test_verify_citations_returns_normalized_sub_ids(self, generator):
        """Hàm verify_citations ghi nhận đúng các ID con bị rút về ID cha khi return_normalized=True."""
        raw = "Thời gian thử việc không quá 30 ngày [45_2019_QH14__D25__K4__a]."
        valid_ids = ["45_2019_QH14__D25__K4"]

        ans, hal, cit, norm = generator.verify_citations(raw, valid_ids, return_normalized=True)

        assert "[45_2019_QH14__D25__K4]" in ans
        assert cit == ["45_2019_QH14__D25__K4"]
        assert hal == []
        assert norm == ["45_2019_QH14__D25__K4__a"]
        assert generator.last_normalized_ids == ["45_2019_QH14__D25__K4__a"]

    def test_verify_citations_backward_compatibility(self, generator):
        """Khi không truyền return_normalized, trả về 3-tuple như cũ không làm vỡ code cũ."""
        raw = "Thời gian thử việc [45_2019_QH14__D25__K4__a]."
        valid_ids = ["45_2019_QH14__D25__K4"]

        res = generator.verify_citations(raw, valid_ids)
        assert len(res) == 3
        ans, hal, cit = res
        assert cit == ["45_2019_QH14__D25__K4"]

    def test_sentence_with_normalized_citation_is_invalid_in_citation_validity(self):
        """Câu có mã bị rút (__a về __K) PHẢI bị tính là KHÔNG HỢP LỆ trong Citation Validity."""
        fake_results = [
            {
                "qid": "q_norm_01",
                "question": "Thời gian thử việc đối với công việc có chức danh nghề nghiệp là bao lâu?",
                "is_out_of_scope": False,
                "gold_ids": ["45_2019_QH14__D25__K4"],
                "retrieved_ids": ["45_2019_QH14__D25__K4"],
                "context_map": {
                    "45_2019_QH14__D25__K4": "4. Không quá 30 ngày đối với công việc có chức danh nghề nghiệp."
                },
                "answer": "Không quá 30 ngày [45_2019_QH14__D25__K4].",
                "citations": ["45_2019_QH14__D25__K4"],
                "hallucinated_ids": [],
                "normalized_ids": ["45_2019_QH14__D25__K4__a"],  # Đã bị rút từ mã con tự chế __a
                "is_refusal": False,
                "generation_time": 1.0
            }
        ]

        metrics = compute_metrics(fake_results)

        # Citation Validity (Chính xác): PHẢI BẰNG 0.0 VÌ CÓ MÃ BỊ RÚT GỌN (tự chế cấp điểm)
        assert metrics["citation_validity"] == 0.0
        assert metrics["citation_validity_strict"] == 0.0

        # Relaxed Citation Validity: Bằng 1.0 nếu châm chước
        assert metrics["citation_validity_relaxed"] == 1.0

        # Thống kê câu bị rút mã
        assert metrics["citation_normalized_rate"] == 1.0
        assert metrics["normalized_count"] == 1

        # Citation Accuracy cũng bị phạt do mã không chuẩn xác
        assert metrics["citation_accuracy"] == 0.0

    def test_sentence_with_clean_citation_is_valid(self):
        """Câu có mã chuẩn xác trong context, không hallucinated và không bị rút, phải hợp lệ 100%."""
        fake_results = [
            {
                "qid": "q_clean_01",
                "question": "Thời gian thử việc?",
                "is_out_of_scope": False,
                "gold_ids": ["45_2019_QH14__D25__K4"],
                "retrieved_ids": ["45_2019_QH14__D25__K4"],
                "context_map": {
                    "45_2019_QH14__D25__K4": "4. Không quá 30 ngày đối với công việc có chức danh nghề nghiệp."
                },
                "answer": "Không quá 30 ngày [45_2019_QH14__D25__K4].",
                "citations": ["45_2019_QH14__D25__K4"],
                "hallucinated_ids": [],
                "normalized_ids": [],  # Sạch sẽ, không bị rút
                "is_refusal": False,
                "generation_time": 1.0
            }
        ]

        metrics = compute_metrics(fake_results)
        assert metrics["citation_validity"] == 1.0
        assert metrics["citation_validity_relaxed"] == 1.0
        assert metrics["citation_normalized_rate"] == 0.0
        assert metrics["normalized_count"] == 0
        assert metrics["citation_accuracy"] == 1.0
