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
            for item in self.corpus_list:
                pid = item.get("provision_id", "")
                if "__K" in pid:
                    alt_pid = pid.replace("__K", "__")
                    if alt_pid not in self.corpus_dict:
                        self.corpus_dict[alt_pid] = item

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

        # Build mapping: (doc_code, dieu) -> list of provision_ids in sequential order
        self.article_to_provisions = {}
        for item in self.corpus_list:
            doc_code = item.get("doc_code", "")
            dieu = str(item.get("dieu", "")).strip()
            if doc_code and dieu:
                key = (doc_code, dieu)
                if key not in self.article_to_provisions:
                    self.article_to_provisions[key] = []
                self.article_to_provisions[key].append(item["provision_id"])

        print("All resources loaded successfully!\n")

    # ------------------------------------------------------------------
    # Sparse Retrieval (BM25)
    # ------------------------------------------------------------------
    def search_bm25(self, query, top_k=10, hieu_luc_filter="con_hieu_luc", expand_siblings=False):
        """Tìm kiếm bằng BM25 và lọc theo hiệu lực trước khi lấy Top-K.
        
        Args:
            query: Câu truy vấn.
            top_k: Số kết quả cần lấy (mặc định 10).
            hieu_luc_filter: Trạng thái hiệu lực cần lọc ('con_hieu_luc', ...).
            expand_siblings: Có mở rộng các khoản anh em cùng Điều hay không.
        """
        tokenized_query = ViTokenizer.tokenize(query).lower().split()
        scores = self.bm25.get_scores(tokenized_query)

        # Xếp hạng toàn bộ corpus theo điểm BM25
        ranked_indices = np.argsort(scores)[::-1]

        results = []

        for idx in ranked_indices:
            prov_id = self.provision_ids[idx]
            content = self.corpus_dict.get(prov_id)
            if not content:
                continue

            # Lọc hiệu lực trước khi lấy Top-K
            if hieu_luc_filter is not None:
                if content.get("hieu_luc") != hieu_luc_filter:
                    continue

            results.append({
                "provision_id": prov_id,
                "score": float(scores[idx]),
                "content": content,
            })

            if len(results) >= top_k:
                break

        if expand_siblings:
            results = self.expand_sibling_provisions(results, query)

        return results

    # ------------------------------------------------------------------
    # Dense Retrieval (FAISS + Bi-Encoder)
    # ------------------------------------------------------------------
    def search_dense(self, query, top_k=10, hieu_luc_filter="con_hieu_luc", expand_siblings=False):
        """Tìm kiếm bằng Dense Retrieval và lọc theo hiệu lực trước khi lấy Top-K.
        
        Args:
            query: Câu truy vấn.
            top_k: Số kết quả cần lấy (mặc định 10).
            hieu_luc_filter: Trạng thái hiệu lực cần lọc ('con_hieu_luc', ...).
            expand_siblings: Có mở rộng các khoản anh em cùng Điều hay không.
        """
        tokenized_query = ViTokenizer.tokenize(query).lower()
        query_embedding = self.model.encode([tokenized_query], normalize_embeddings=True)
        query_embedding = np.array(query_embedding).astype("float32")

        # Lấy nhiều candidate hơn top_k để có đủ kết quả sau khi lọc
        search_k = max(top_k * 10, 50)

        scores, indices = self.faiss_index.search(query_embedding, search_k)

        results = []

        for i in range(search_k):
            idx = indices[0][i]

            if idx == -1:
                continue

            prov_id = self.provision_ids[idx]
            content = self.corpus_dict.get(prov_id)
            if not content:
                continue

            # Lọc hiệu lực trước khi lấy Top-K
            if hieu_luc_filter is not None:
                if content.get("hieu_luc") != hieu_luc_filter:
                    continue

            results.append({
                "provision_id": prov_id,
                "score": float(scores[0][i]),
                "content": content,
            })

            if len(results) >= top_k:
                break

        if expand_siblings:
            results = self.expand_sibling_provisions(results, query)

        return results

    # ------------------------------------------------------------------
    # Ý định câu hỏi & Mở rộng ngữ cảnh cùng Điều (Context Expansion)
    # ------------------------------------------------------------------
    @staticmethod
    def detect_query_intent(query: str) -> dict:
        """Phát hiện ý định của câu hỏi: tổng quan (broad) vs chi tiết (narrow), và nhận diện Điều/Văn bản cụ thể."""
        import re
        q_lower = query.lower()

        # Các từ khóa hỏi tổng quan, trách nhiệm, phạm vi hoặc liệt kê toàn bộ
        broad_keywords = [
            "trách nhiệm", "chính sách", "quy định thế nào", "quy định gì", "gồm những gì",
            "gồm các", "những điều kiện gì", "các trường hợp", "như thế nào",
            "nội dung của", "bao gồm những gì", "các quyền", "nghĩa vụ của", "nghĩa vụ",
            "nguyên tắc", "nêu các", "cho biết các", "chế độ", "biện pháp", "là gì",
            "có bị gì", "bị gì", "hậu quả", "bị phạt", "xử lý thế nào",
            "có được không", "có được nhận", "được nhận tiền", "có được hưởng",
            "thì sao", "thì làm sao", "có sao không", "đột ngột"
        ]

        # Kiểm tra hỏi đích danh Điều luật: ví dụ "điều 14", "điều 112"
        dieu_match = re.search(r"\bđiều\s+(\d+)\b", q_lower)

        # Nhận diện văn bản cụ thể nếu có (sử dụng regex có biên từ \b để tránh khớp nhầm)
        explicit_doc = None

        # 1. BLLĐ 2012 (10/2012/QH13)
        if re.search(r"\b(?:bộ\s*luật\s*lao\s*động|bllđ|luật\s*lao\s*động)\s*(?:năm\s*)?2012\b", q_lower) or re.search(r"\b10/2012(?:/qh13)?\b", q_lower):
            explicit_doc = "10_2012_QH13"
        # 2. Nghị định 145/2020/NĐ-CP (Tránh nhận nhầm số tiền hoặc số 145 độc lập)
        elif re.search(r"\b(?:nghị\s*định|nđ)\s*(?:số\s*)?145\b", q_lower) or re.search(r"\b145/2020(?:/nđ-cp)?\b", q_lower):
            explicit_doc = "145_2020_NDCP"
        # 3. Luật Việc làm / Bảo hiểm thất nghiệp (74/2025/QH15)
        # Kiểm tra trước BHXH để tránh "bảo hiểm thất nghiệp" bị coi là Luật BHXH
        elif re.search(r"\b(?:luật\s*việc\s*làm|bảo\s*hiểm\s*thất\s*nghiệp|bhtn|trợ\s*cấp\s*thất\s*nghiệp)\b", q_lower) or re.search(r"\b74/2025(?:/qh15)?\b", q_lower):
            explicit_doc = "74_2025_QH15"
        # 4. Luật Bảo hiểm xã hội (58/VBHN-VPQH)
        # Yêu cầu rõ "bảo hiểm xã hội" hoặc "bhxh", không lấy từ "bảo hiểm" chung chung
        elif re.search(r"\b(?:luật\s*)?(?:bảo\s*hiểm\s*xã\s*hội|bhxh)\b", q_lower) or re.search(r"\b58/vbhn(?:-vpqh)?\b", q_lower):
            explicit_doc = "58_VBHN-VPQH"
        # 5. Luật An toàn, vệ sinh lao động (84/2015/QH13)
        elif re.search(r"\b(?:luật\s*)?(?:an\s*toàn[,\s]*vệ\s*sinh\s*lao\s*động|atvslđ|an\s*toàn\s*lao\s*động)\b", q_lower) or re.search(r"\b84/2015(?:/qh13)?\b", q_lower):
            explicit_doc = "84_2015_QH13"
        # 6. Luật Công đoàn (50/2024/QH15)
        elif re.search(r"\b(?:luật\s*công\s*đoàn|công\s*đoàn)\b", q_lower) or re.search(r"\b50/2024(?:/qh15)?\b", q_lower):
            explicit_doc = "50_2024_QH15"
        # 7. Nghị định 12/2022/NĐ-CP (Xử phạt vi phạm)
        elif re.search(r"\b(?:nghị\s*định|nđ)\s*(?:số\s*)?12\b", q_lower) or re.search(r"\b12/2022(?:/nđ-cp)?\b", q_lower):
            explicit_doc = "12_2022_NDCP"
        # 8. Nghị định 152/2020/NĐ-CP (Lao động nước ngoài)
        elif re.search(r"\b(?:nghị\s*định|nđ)\s*(?:số\s*)?152\b", q_lower) or re.search(r"\b152/2020(?:/nđ-cp)?\b", q_lower):
            explicit_doc = "152_2020_NDCP"
        # 9. Bộ luật Lao động 2019 (45/2019/QH14)
        # Chỉ nhận diện khi có BLLĐ/Bộ luật lao động hoặc số hiệu 45/2019, tránh nhận nhầm năm 2019
        elif re.search(r"\b(?:bộ\s*luật\s*lao\s*động|bllđ|luật\s*lao\s*động)(?:\s*(?:năm\s*)?2019)?\b", q_lower) or re.search(r"\b45/2019(?:/qh14)?\b", q_lower):
            explicit_doc = "45_2019_QH14"

        is_broad = any(kw in q_lower for kw in broad_keywords) or (dieu_match is not None)

        return {
            "is_broad": is_broad,
            "explicit_dieu": dieu_match.group(1) if dieu_match else None,
            "explicit_doc": explicit_doc,
        }

    def expand_sibling_provisions(self, results, query, max_siblings_per_article=4, max_total=15):
        """Mở rộng ngữ cảnh: Nếu câu hỏi có tính bao quát hoặc hỏi trực tiếp một Điều,
        bổ sung các Khoản anh em (cùng Điều) của các kết quả hàng đầu (Top 1-3).
        Đặc biệt: Nếu hỏi đích danh một Điều, tra cứu trực tiếp và ưu tiên đưa lên đầu.
        """
        if not results:
            return results

        intent = self.detect_query_intent(query)
        if not intent["is_broad"]:
            return results

        existing_pids = {r["provision_id"] for r in results}
        expanded_results = list(results)

        # 1. TRƯỜNG HỢP HỎI ĐÍCH DANH ĐIỀU LUẬT (Direct Article Lookup)
        if intent["explicit_dieu"]:
            exp_dieu = intent["explicit_dieu"]
            exp_doc = intent["explicit_doc"] or "45_2019_QH14"

            direct_pids = self.article_to_provisions.get((exp_doc, exp_dieu), [])
            if not direct_pids:
                # Tìm trong các văn bản phổ biến khác nếu chưa có
                for doc_code in ["45_2019_QH14", "145_2020_NDCP", "74_2025_QH15", "58_VBHN-VPQH", "84_2015_QH13", "50_2024_QH15", "10_2012_QH13", "12_2022_NDCP"]:
                    if (doc_code, exp_dieu) in self.article_to_provisions:
                        direct_pids = self.article_to_provisions[(doc_code, exp_dieu)]
                        break

            if direct_pids:
                injected_chunks = []
                for pid in direct_pids:
                    sib_content = self.corpus_dict.get(pid)
                    if sib_content:
                        injected_chunks.append({
                            "provision_id": pid,
                            "score": 1.0,  # Điểm ưu tiên cao nhất
                            "content": sib_content,
                            "is_expanded": True,
                        })
                        existing_pids.add(pid)

                # Giữ các điều khoản của Điều được hỏi ở đầu danh sách
                other_chunks = [r for r in expanded_results if r["provision_id"] not in {c["provision_id"] for c in injected_chunks}]
                return (injected_chunks + other_chunks)[:max_total]

        # 2. TRƯỜNG HỢP CÂU HỎI TỔNG QUAN KHÁC (Sibling expansion trên top kết quả)
        top_candidates = results[:3]
        target_articles = []
        for r in top_candidates:
            item = r["content"]
            doc_code = item.get("doc_code")
            dieu = str(item.get("dieu", "")).strip()
            if doc_code and dieu and (doc_code, dieu) not in target_articles:
                target_articles.append((doc_code, dieu))

        for doc_code, dieu in target_articles:
            siblings = self.article_to_provisions.get((doc_code, dieu), [])
            added_count = 0
            for sib_id in siblings:
                if sib_id not in existing_pids:
                    sib_content = self.corpus_dict.get(sib_id)
                    if sib_content:
                        expanded_results.append({
                            "provision_id": sib_id,
                            "score": 0.0,
                            "content": sib_content,
                            "is_expanded": True,
                        })
                        existing_pids.add(sib_id)
                        added_count += 1
                        if added_count >= max_siblings_per_article or len(expanded_results) >= max_total:
                            break
            if len(expanded_results) >= max_total:
                break

        return expanded_results

    # ------------------------------------------------------------------
    # Hybrid Retrieval – Reciprocal Rank Fusion (RRF)
    # ------------------------------------------------------------------
    def search_hybrid(
        self,
        query,
        top_k=10,
        rrf_k=5,
        retrieval_depth=50,
        alpha=0.5,
        expand_siblings=False,
        hieu_luc_filter="con_hieu_luc"
    ):
        """Kết hợp BM25 và Dense Retrieval bằng Reciprocal Rank Fusion.

        Công thức RRF:
            score_rrf(d) = alpha * (1 / (k + rank_bm25(d)))
                        + (1 - alpha) * (1 / (k + rank_dense(d)))

        Trong đó:
            rrf_k: hằng số k trong công thức RRF.
            alpha: trọng số của BM25; Dense có trọng số (1 - alpha).

        Args:
            query: Câu hỏi tìm kiếm.
            top_k: Số kết quả trả về cuối cùng.
            rrf_k: Hằng số k trong công thức RRF.
            retrieval_depth: Số candidate lấy từ mỗi phương pháp trước khi RRF.
            alpha: Trọng số cho BM25.
            expand_siblings: Có mở rộng các khoản cùng Điều hay không.
            hieu_luc_filter: Chỉ giữ các văn bản có trạng thái hiệu lực này.
        """
        # Lấy kết quả từ cả hai phương pháp với retrieval_depth lớn hơn top_k
        bm25_results = self.search_bm25(
            query,
            top_k=retrieval_depth,
            hieu_luc_filter=hieu_luc_filter
        )

        dense_results = self.search_dense(
            query,
            top_k=retrieval_depth,
            hieu_luc_filter=hieu_luc_filter
        )

        # Tính điểm RRF cho từng provision_id
        rrf_scores = {}  # provision_id -> rrf_score

        for rank, res in enumerate(bm25_results, start=1):
            pid = res["provision_id"]
            rrf_scores[pid] = rrf_scores.get(pid, 0.0) + alpha * (1.0 / (rrf_k + rank))

        for rank, res in enumerate(dense_results, start=1):
            pid = res["provision_id"]
            rrf_scores[pid] = rrf_scores.get(pid, 0.0) + (1.0 - alpha) * (1.0 / (rrf_k + rank))

        # Sắp xếp theo điểm RRF giảm dần
        sorted_pids = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)

        results = []
        for pid, score in sorted_pids[:top_k]:
            results.append({
                "provision_id": pid,
                "score": score,
                "content": self.corpus_dict[pid],
                "is_expanded": False,
            })

        if expand_siblings:
            results = self.expand_sibling_provisions(results, query)

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
        "Ký hợp đồng thử việc tối đa bao lâu với người lao động phổ thông",
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
        hybrid_results = retriever.search_hybrid(
    query,
    top_k=10,
    rrf_k=10,
    alpha=0.5,
    retrieval_depth=50,
    expand_siblings=False,
    hieu_luc_filter="con_hieu_luc"
    )
        hybrid_time = time.time() - t0
        print(f"[Hybrid RRF] ({hybrid_time:.4f}s)")
        print_results(hybrid_results, "Hybrid (RRF)")

        # --- Hybrid RRF + chỉ còn hiệu lực ---
        filtered = retriever.filter_by_hieu_luc(hybrid_results, "con_hieu_luc")
        print(f"[Hybrid RRF – chỉ còn hiệu lực] ({len(filtered)}/{len(hybrid_results)} kết quả)")
        print_results(filtered, "Hybrid RRF (chỉ còn hiệu lực)")

        print()


if __name__ == "__main__":
    main()
