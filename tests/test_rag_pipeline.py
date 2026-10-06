import os
import sys
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from rag_pipeline import execute_rag_pipeline, expand_legal_query


class DummyRetriever:
    def __init__(self):
        self.last_query = None
        self.last_method = None

    def search_hybrid(self, query, top_k=10, rrf_k=5, alpha=0.5, retrieval_depth=50, expand_siblings=True, hieu_luc_filter="con_hieu_luc"):
        self.last_query = query
        self.last_method = "hybrid"
        return [
            {
                "provision_id": f"doc__D1__K{i}",
                "content": {"noi_dung": f"Nội dung điều khoản {i} " * 10, "hieu_luc": "con_hieu_luc"},
                "score": 1.0 - i * 0.1
            }
            for i in range(1, top_k + 1)
        ]

    def search_bm25(self, query, top_k=10, hieu_luc_filter="con_hieu_luc"):
        self.last_query = query
        self.last_method = "bm25"
        return [
            {
                "provision_id": f"doc_bm25__D1__K{i}",
                "content": {"noi_dung": f"Nội dung BM25 {i}", "hieu_luc": "con_hieu_luc"},
                "score": 5.0 - i
            }
            for i in range(1, top_k + 1)
        ]

    def search_dense(self, query, top_k=10, hieu_luc_filter="con_hieu_luc"):
        self.last_query = query
        self.last_method = "dense"
        return [
            {
                "provision_id": f"doc_dense__D1__K{i}",
                "content": {"noi_dung": f"Nội dung Dense {i}", "hieu_luc": "con_hieu_luc"},
                "score": 0.9 - i * 0.05
            }
            for i in range(1, top_k + 1)
        ]

    @staticmethod
    def filter_by_hieu_luc(results, hieu_luc="con_hieu_luc"):
        return [r for r in results if r.get("content", {}).get("hieu_luc") == hieu_luc]


class DummyGenerator:
    def __init__(self):
        self.last_query = None
        self.last_chunks = None

    def generate(self, query, chunks):
        self.last_query = query
        self.last_chunks = chunks
        return {
            "answer": "Câu trả lời thử nghiệm [doc__D1__K1].",
            "citations": ["doc__D1__K1"],
            "hallucinated_ids": [],
            "is_refusal": False,
            "api_error": False,
            "error": None
        }


def test_execute_rag_pipeline_query_expansion():
    """Kiểm tra pipeline tự động mở rộng query bằng expand_legal_query khi truy xuất."""
    retriever = DummyRetriever()
    generator = DummyGenerator()

    # Query đời thường về xin nghỉ việc trước hạn
    res = execute_rag_pipeline("tôi muốn xin nghỉ việc trước hạn", retriever, generator)

    # Retriever nhận query đã mở rộng (có thêm thuật ngữ pháp lý và Điều luật)
    assert retriever.last_query is not None
    assert "quyền đơn phương chấm dứt" in retriever.last_query
    assert "người lao động" in retriever.last_query
    assert "Điều 35" in retriever.last_query

    # LLM nhận query gốc của người dùng
    assert generator.last_query == "tôi muốn xin nghỉ việc trước hạn"
    assert res["answer"] == "Câu trả lời thử nghiệm [doc__D1__K1]."
    assert res["citations"] == ["doc__D1__K1"]
    assert "retrieval_time" in res
    assert "generation_time" in res


def test_execute_rag_pipeline_fallback_when_filter_empty():
    """Kiểm tra nhánh dự phòng khi tất cả kết quả bị lọc rỗng bởi filter_by_hieu_luc."""
    retriever = DummyRetriever()
    generator = DummyGenerator()

    # Giả lập search_hybrid trả về các văn bản đã hết hiệu lực
    retriever.search_hybrid = lambda query, **kw: [
        {
            "provision_id": "old_doc__D1",
            "content": {"noi_dung": "Luật cũ", "hieu_luc": "het_hieu_luc"},
            "score": 0.8
        }
    ]

    # Lọc con_hieu_luc sẽ bị rỗng, pipeline phải fallback sang raw_chunks
    res = execute_rag_pipeline("thử việc thế nào?", retriever, generator, hieu_luc_filter="con_hieu_luc")

    assert len(res["chunks"]) == 1
    assert res["chunks"][0]["provision_id"] == "old_doc__D1"
    assert len(generator.last_chunks) == 1


def test_execute_rag_pipeline_max_context_chars():
    """Kiểm tra giới hạn ký tự context đưa vào generator (max_context_chars)."""
    retriever = DummyRetriever()
    generator = DummyGenerator()

    # Mỗi chunk dài 500 ký tự, có 10 chunks -> tổng 5000 ký tự
    retriever.search_hybrid = lambda query, **kw: [
        {
            "provision_id": f"doc__D1__K{i}",
            "content": {"noi_dung": "A" * 500, "hieu_luc": "con_hieu_luc"},
            "score": 1.0
        }
        for i in range(10)
    ]

    # Giới hạn 1200 ký tự -> chỉ nhận tối đa 2 chunks (1000 ký tự, chunk thứ 3 vượt 1200)
    res = execute_rag_pipeline("thử nghiệm", retriever, generator, max_context_chars=1200)

    assert len(res["chunks"]) == 2
    total_chars = sum(len(c["content"]["noi_dung"]) for c in res["chunks"])
    assert total_chars <= 1200


def test_execute_rag_pipeline_retrieval_methods():
    """Kiểm tra thực thi các phương pháp retrieval khác nhau (BM25, Dense, Hybrid)."""
    retriever = DummyRetriever()
    generator = DummyGenerator()

    # BM25
    res_bm25 = execute_rag_pipeline("câu hỏi 1", retriever, generator, retrieval_method="BM25")
    assert retriever.last_method == "bm25"
    assert "doc_bm25__D1__K1" in res_bm25["chunks"][0]["provision_id"]

    # Dense
    res_dense = execute_rag_pipeline("câu hỏi 2", retriever, generator, retrieval_method="Dense")
    assert retriever.last_method == "dense"
    assert "doc_dense__D1__K1" in res_dense["chunks"][0]["provision_id"]

    # Hybrid
    res_hybrid = execute_rag_pipeline("câu hỏi 3", retriever, generator, retrieval_method="Hybrid_RRF")
    assert retriever.last_method == "hybrid"
    assert "doc__D1__K1" in res_hybrid["chunks"][0]["provision_id"]
