import os
import sys
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from retriever import LegalRetriever


data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
index_dir = os.path.join(data_dir, "index")
corpus_file = os.path.join(data_dir, "structured", "corpus.json")
INDEX_READY = (
    os.path.exists(corpus_file)
    and os.path.exists(os.path.join(index_dir, "bm25_index.pkl"))
    and os.path.exists(os.path.join(index_dir, "faiss_index.bin"))
    and os.path.exists(os.path.join(index_dir, "provision_mapping.json"))
)


@pytest.fixture(scope="module")
def retriever():
    if not INDEX_READY:
        pytest.skip("Test hồi quy cần chỉ mục thật (data/index/ và data/structured/corpus.json)")
    return LegalRetriever(data_dir=data_dir)


REGRESSION_CASES = [
    {
        "id": "reg_01",
        "question": "Thời gian thử việc tối đa đối với lao động phổ thông là bao nhiêu ngày?",
        "expected_dieu": "25",
        "doc_code": "45_2019_QH14"
    },
    {
        "id": "reg_02",
        "question": "Tiền lương trong thời gian thử việc được trả ít nhất bao nhiêu %?",
        "expected_dieu": "26",
        "doc_code": "45_2019_QH14"
    },
    {
        "id": "reg_03",
        "question": "Người lao động làm việc theo hợp đồng không xác định thời hạn muốn nghỉ việc phải báo trước bao nhiêu ngày?",
        "expected_dieu": "35",
        "doc_code": "45_2019_QH14"
    },
    {
        "id": "reg_04",
        "question": "Người sử dụng lao động đơn phương chấm dứt hợp đồng lao động phải báo trước bao nhiêu ngày?",
        "expected_dieu": "36",
        "doc_code": "45_2019_QH14"
    },
    {
        "id": "reg_05",
        "question": "Số ngày nghỉ phép năm của người lao động làm việc trong điều kiện bình thường là bao nhiêu ngày?",
        "expected_dieu": "113",
        "doc_code": "45_2019_QH14"
    },
    {
        "id": "reg_06",
        "question": "Người lao động được nghỉ làm việc, hưởng nguyên lương trong những ngày lễ, tết nào?",
        "expected_dieu": "112",
        "doc_code": "45_2019_QH14"
    },
    {
        "id": "reg_07",
        "question": "Tiền lương làm thêm giờ vào ngày nghỉ lễ, tết được tính ít nhất bao nhiêu phần trăm?",
        "expected_dieu": "98",
        "doc_code": "45_2019_QH14"
    },
    {
        "id": "reg_08",
        "question": "Số giờ làm thêm tối đa của người lao động trong một năm là bao nhiêu giờ?",
        "expected_dieu": "107",
        "doc_code": "45_2019_QH14"
    },
    {
        "id": "reg_09",
        "question": "Người sử dụng lao động được áp dụng hình thức kỷ luật sa thải trong trường hợp nào?",
        "expected_dieu": "125",
        "doc_code": "45_2019_QH14"
    },
    {
        "id": "reg_10",
        "question": "Điều kiện và mức hưởng trợ cấp thôi việc của người lao động được quy định thế nào?",
        "expected_dieu": "46",
        "doc_code": "45_2019_QH14"
    },
    {
        "id": "reg_11",
        "question": "Trợ cấp mất việc làm được tính như thế nào khi người lao động bị mất việc?",
        "expected_dieu": "47",
        "doc_code": "45_2019_QH14"
    },
    {
        "id": "reg_12",
        "question": "Thời gian nghỉ thai sản trước và sau khi sinh con của lao động nữ là bao nhiêu tháng?",
        "expected_dieu": "139",
        "doc_code": "45_2019_QH14"
    },
    {
        "id": "reg_13",
        "question": "Người sử dụng lao động có được sa thải lao động nữ vì lý do có thai hoặc nuôi con nhỏ dưới 12 tháng tuổi?",
        "expected_dieu": "137",
        "doc_code": "45_2019_QH14"
    },
    {
        "id": "reg_14",
        "question": "Kỳ hạn trả lương cho người lao động hưởng lương theo tháng được quy định ra sao?",
        "expected_dieu": "97",
        "doc_code": "45_2019_QH14"
    },
    {
        "id": "reg_15",
        "question": "Tiền lương làm việc vào ban đêm được trả thêm ít nhất bao nhiêu phần trăm?",
        "expected_dieu": "98",
        "doc_code": "45_2019_QH14"
    },
]


class TestRegressionQA:
    """Bộ 15 câu hỏi hồi quy cố định kiểm tra độ ổn định truy xuất của hệ thống (yêu cầu chỉ mục thật, đánh giá top-10)."""

    @pytest.mark.parametrize("case", REGRESSION_CASES, ids=[c["id"] for c in REGRESSION_CASES])
    def test_regression_retrieval(self, retriever, case):
        results = retriever.search_hybrid(
            case["question"],
            top_k=10,
            rrf_k=5,
            retrieval_depth=50,
            expand_siblings=True,
            hieu_luc_filter="con_hieu_luc"
        )
        assert len(results) > 0, f"Retriever trả về rỗng cho {case['id']}"

        # Kiểm tra xem Điều mong đợi có xuất hiện trong top-10 kết quả hay không
        retrieved_dieus = [
            str(r["content"].get("dieu", "")).strip()
            for r in results
            if r["content"].get("doc_code") == case["doc_code"]
        ]

        assert case["expected_dieu"] in retrieved_dieus, (
            f"Câu {case['id']} không tìm thấy Điều {case['expected_dieu']} trong top-10! "
            f"Các điều tìm được: {retrieved_dieus}"
        )
