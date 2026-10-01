import os
import sys
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from generator import LegalGenerator


@pytest.fixture
def generator():
    # Khởi tạo instance thuần túy để test verify_citations mà không cần gọi API key
    gen = LegalGenerator.__new__(LegalGenerator)
    gen.REFUSAL_TEXT = "Tôi không tìm thấy thông tin để trả lời."
    return gen


class TestVerifyCitations:
    """Kiểm thử tầng lọc và chuẩn hóa trích dẫn (verify_citations)."""

    def test_valid_single_citation(self, generator):
        raw = "Người lao động được nghỉ phép 12 ngày [45_2019_QH14__D113__K1]."
        valid_ids = ["45_2019_QH14__D113__K1"]
        ans, hal, cit = generator.verify_citations(raw, valid_ids)

        assert "[45_2019_QH14__D113__K1]" in ans
        assert cit == ["45_2019_QH14__D113__K1"]
        assert hal == []

    def test_sub_id_normalization_to_khoan(self, generator):
        """Kiểm tra rút gọn mã con (__a, __b) về cấp Khoản cha khi Khoản cha có trong context."""
        raw = "Hình thức hợp đồng lao động [145_2020_NDCP__D10__K2__a]."
        valid_ids = ["145_2020_NDCP__D10__K2"]
        ans, hal, cit = generator.verify_citations(raw, valid_ids)

        assert "[145_2020_NDCP__D10__K2]" in ans
        assert "145_2020_NDCP__D10__K2" in cit
        assert hal == []

    def test_sub_id_normalization_uppercase_and_dieu(self, generator):
        """Kiểm tra rút gọn mã con chữ hoa hoặc cấp Điều."""
        raw = "Quy định áp dụng [45_2019_QH14__D103__A]."
        valid_ids = ["45_2019_QH14__D103"]
        ans, hal, cit = generator.verify_citations(raw, valid_ids)

        assert "[45_2019_QH14__D103]" in ans
        assert "45_2019_QH14__D103" in cit
        assert hal == []

    def test_multiple_citations_merged_in_one_bracket(self, generator):
        """Chuẩn hóa [ID1, ID2] thành [ID1][ID2]."""
        raw = "Căn cứ quy định [45_2019_QH14__D113__K1, 45_2019_QH14__D114__K1]."
        valid_ids = ["45_2019_QH14__D113__K1", "45_2019_QH14__D114__K1"]
        ans, hal, cit = generator.verify_citations(raw, valid_ids)

        assert "[45_2019_QH14__D113__K1][45_2019_QH14__D114__K1]" in ans
        assert set(cit) == {"45_2019_QH14__D113__K1", "45_2019_QH14__D114__K1"}
        assert hal == []

    def test_hallucinated_citation_removed(self, generator):
        """Citation bịa hoặc ngoài context phải bị loại bỏ và ghi vào danh sách hallucinated."""
        raw = "Nghĩa vụ của người lao động [999_2025_FAKE__D1__K1]."
        valid_ids = ["45_2019_QH14__D113__K1"]
        ans, hal, cit = generator.verify_citations(raw, valid_ids)

        assert "[999_2025_FAKE__D1__K1]" not in ans
        assert "999_2025_FAKE__D1__K1" in hal
        assert cit == []

    def test_mixed_valid_and_hallucinated_citations(self, generator):
        """Giữ citation hợp lệ, loại citation bịa."""
        raw = "Quy định [45_2019_QH14__D113__K1, 999_2025_FAKE__D1]."
        valid_ids = ["45_2019_QH14__D113__K1"]
        ans, hal, cit = generator.verify_citations(raw, valid_ids)

        assert "[45_2019_QH14__D113__K1]" in ans
        assert "999_2025_FAKE__D1" not in ans
        assert "45_2019_QH14__D113__K1" in cit
        assert "999_2025_FAKE__D1" in hal

    def test_no_citations_in_text(self, generator):
        """Văn bản không chứa citation."""
        raw = "Tôi không tìm thấy thông tin phù hợp trong tài liệu được cung cấp."
        valid_ids = ["45_2019_QH14__D113__K1"]
        ans, hal, cit = generator.verify_citations(raw, valid_ids)

        assert ans == raw
        assert cit == []
        assert hal == []
