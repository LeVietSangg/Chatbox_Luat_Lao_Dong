import os
import json
import pickle
import numpy as np
import faiss
from pyvi import ViTokenizer
from sentence_transformers import SentenceTransformer
import time


class LegalRetriever:
    """Hệ thống truy xuất văn bản pháp luật hỗ trợ BM25, Dense và Hybrid (RRF)."""

    def __init__(self, data_dir=None):
        if data_dir is None:
            self.data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
        else:
            self.data_dir = data_dir

        self.index_dir = os.path.join(self.data_dir, "index")
        self.corpus_file = os.path.join(self.data_dir, "structured", "corpus.json")

        # Load corpus
        print("Loading corpus...")
        with open(self.corpus_file, "r", encoding="utf-8") as f:
            self.corpus_list = json.load(f)
            self.corpus_dict = {item["provision_id"]: item for item in self.corpus_list}

        # Load mapping (index position -> provision_id)
        print("Loading mapping...")
        mapping_path = os.path.join(self.index_dir, "provision_mapping.json")
        with open(mapping_path, "r", encoding="utf-8") as f:
            self.provision_ids = json.load(f)

        # Load BM25
        print("Loading BM25 index...")
        bm25_path = os.path.join(self.index_dir, "bm25_index.pkl")
        with open(bm25_path, "rb") as f:
            self.bm25 = pickle.load(f)

        # Load FAISS
        print("Loading FAISS index...")
        faiss_path = os.path.join(self.index_dir, "faiss_index.bin")
        self.faiss_index = faiss.read_index(faiss_path)

        # Load Sentence Transformer
        model_name = "bkai-foundation-models/vietnamese-bi-encoder"
        print(f"Loading SentenceTransformer model ({model_name})...")
        self.model = SentenceTransformer(model_name)

        print("All resources loaded successfully!\n")

    # ------------------------------------------------------------------
    # Sparse Retrieval (BM25)
    # ------------------------------------------------------------------
    def search_bm25(self, query, top_k=5):
        """Tìm kiếm bằng BM25 (sparse, keyword-based)."""
        tokenized_query = ViTokenizer.tokenize(query).lower().split()
        scores = self.bm25.get_scores(tokenized_query)
        top_n = np.argsort(scores)[::-1][:top_k]

        results = []
        for idx in top_n:
            prov_id = self.provision_ids[idx]
            results.append({
                "provision_id": prov_id,
                "score": float(scores[idx]),
                "content": self.corpus_dict[prov_id],
            })
        return results

    # ------------------------------------------------------------------
    # Dense Retrieval (FAISS + Bi-Encoder)
    # ------------------------------------------------------------------
    def search_dense(self, query, top_k=5):
        """Tìm kiếm bằng Dense Retrieval (semantic, bi-encoder + FAISS)."""
        query_embedding = self.model.encode([query], normalize_embeddings=True)
        query_embedding = np.array(query_embedding).astype("float32")

        scores, indices = self.faiss_index.search(query_embedding, top_k)

        results = []
        for i in range(top_k):
            idx = indices[0][i]
            if idx != -1:
                prov_id = self.provision_ids[idx]
                results.append({
                    "provision_id": prov_id,
                    "score": float(scores[0][i]),
                    "content": self.corpus_dict[prov_id],
                })
        return results

    # ------------------------------------------------------------------
    # Hybrid Retrieval – Reciprocal Rank Fusion (RRF)
    # ------------------------------------------------------------------
    def search_hybrid(self, query, top_k=5, rrf_k=60, retrieval_depth=100):
        """Kết hợp BM25 và Dense Retrieval bằng Reciprocal Rank Fusion.

        Công thức RRF:
            score_rrf(d) = Σ  1 / (k + rank_i(d))
        với k là hằng số (mặc định 60, theo bài báo gốc của Cormack et al.).

        Args:
            query: Câu hỏi tìm kiếm.
            top_k: Số kết quả trả về cuối cùng.
            rrf_k: Hằng số k trong công thức RRF (giá trị lớn hơn giảm
                   ảnh hưởng của thứ hạng cao; 60 là giá trị phổ biến).
            retrieval_depth: Số lượng kết quả lấy từ mỗi phương pháp trước
                             khi gộp (nên >= top_k, thường gấp 2-3 lần).
        """
        # Lấy kết quả từ cả hai phương pháp với retrieval_depth lớn hơn top_k
        bm25_results = self.search_bm25(query, top_k=retrieval_depth)
        dense_results = self.search_dense(query, top_k=retrieval_depth)

        # Tính điểm RRF cho từng provision_id
        rrf_scores = {}  # provision_id -> rrf_score

        for rank, res in enumerate(bm25_results, start=1):
            pid = res["provision_id"]
            rrf_scores[pid] = rrf_scores.get(pid, 0.0) + 1.0 / (rrf_k + rank)

        for rank, res in enumerate(dense_results, start=1):
            pid = res["provision_id"]
            rrf_scores[pid] = rrf_scores.get(pid, 0.0) + 1.0 / (rrf_k + rank)

        # Sắp xếp theo điểm RRF giảm dần
        sorted_pids = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)

        results = []
        for pid, score in sorted_pids[:top_k]:
            results.append({
                "provision_id": pid,
                "score": score,
                "content": self.corpus_dict[pid],
            })
        return results

    # ------------------------------------------------------------------
    # Tiện ích: lọc theo hiệu lực
    # ------------------------------------------------------------------
    @staticmethod
    def filter_by_hieu_luc(results, hieu_luc="con_hieu_luc"):
        """Lọc kết quả chỉ giữ lại các provision có trạng thái hiệu lực mong muốn.

        Args:
            results: Danh sách kết quả từ search_*.
            hieu_luc: Giá trị cần lọc, ví dụ 'con_hieu_luc' hoặc 'het_hieu_luc'.
        """
        return [r for r in results if r["content"]["hieu_luc"] == hieu_luc]


# ======================================================================
# Hàm in kết quả
# ======================================================================
def print_results(results, method_name):
    """In kết quả truy xuất ra console."""
    print(f"--- Top kết quả từ {method_name} ---")
    if not results:
        print("  (Không có kết quả)\n")
        return
    for i, res in enumerate(results):
        prov = res["content"]
        hieu_luc_map = {
            "con_hieu_luc": "Còn hiệu lực",
            "het_hieu_luc": "Hết hiệu lực",
            "het_hieu_luc_mot_phan": "Hết hiệu lực một phần",
        }
        hieu_luc_str = hieu_luc_map.get(prov["hieu_luc"], prov["hieu_luc"])
        dieu_khoan = f"Điều {prov['dieu']}"
        if prov.get("khoan"):
            dieu_khoan += f", Khoản {prov['khoan']}"
        if prov.get("diem"):
            dieu_khoan += f", Điểm {prov['diem']}"

        print(f"  [{i+1}] (Score: {res['score']:.4f}) [{hieu_luc_str}]")
        print(f"      {prov['van_ban']}")
        print(f"      {dieu_khoan}. {prov['tieu_de_dieu']}")
        print(f"      ID: {res['provision_id']}")
        # Trích nội dung ngắn (150 ký tự đầu, bỏ ký tự xuống dòng)
        snippet = prov["noi_dung"].replace("\n", " ")[:150]
        print(f"      \"{snippet}...\"\n")


# ======================================================================
# Demo chạy thử
# ======================================================================
def main():
    retriever = LegalRetriever()

    test_queries = [
        "Người lao động nghỉ việc có được hưởng trợ cấp thôi việc không?",
        "Thời gian thử việc tối đa là bao nhiêu ngày đối với lao động phổ thông?",
        "Người sử dụng lao động có quyền đơn phương chấm dứt hợp đồng lao động khi nào?",
        "Mức lương tối thiểu vùng hiện nay là bao nhiêu?",
        "Điều kiện để người lao động nước ngoài làm việc tại Việt Nam là gì?",
    ]

    for query in test_queries:
        print("=" * 80)
        print(f"QUERY: {query}")
        print("=" * 80)

        # --- BM25 ---
        t0 = time.time()
        bm25_results = retriever.search_bm25(query, top_k=5)
        bm25_time = time.time() - t0
        print(f"\n[BM25] ({bm25_time:.4f}s)")
        print_results(bm25_results, "BM25 (Sparse)")

        # --- Dense ---
        t0 = time.time()
        dense_results = retriever.search_dense(query, top_k=5)
        dense_time = time.time() - t0
        print(f"[Dense] ({dense_time:.4f}s)")
        print_results(dense_results, "Dense (Bi-Encoder + FAISS)")

        # --- Hybrid RRF ---
        t0 = time.time()
        hybrid_results = retriever.search_hybrid(query, top_k=5, rrf_k=60)
        hybrid_time = time.time() - t0
        print(f"[Hybrid RRF] ({hybrid_time:.4f}s)")
        print_results(hybrid_results, "Hybrid (RRF k=60)")

        # --- Hybrid RRF + chỉ còn hiệu lực ---
        filtered = retriever.filter_by_hieu_luc(hybrid_results, "con_hieu_luc")
        print(f"[Hybrid RRF – chỉ còn hiệu lực] ({len(filtered)}/{len(hybrid_results)} kết quả)")
        print_results(filtered, "Hybrid RRF (chỉ còn hiệu lực)")

        print()


if __name__ == "__main__":
    main()
