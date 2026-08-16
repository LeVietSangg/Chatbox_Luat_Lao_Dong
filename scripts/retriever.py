import os
import json
import pickle
import numpy as np
import faiss
from pyvi import ViTokenizer
from sentence_transformers import SentenceTransformer
import time

class LegalRetriever:
    def __init__(self, data_dir=None):
        if data_dir is None:
            self.data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
        else:
            self.data_dir = data_dir
            
        self.index_dir = os.path.join(self.data_dir, "index")
        self.corpus_file = os.path.join(self.data_dir, "structured", "corpus.json")
        
        # Load corpus for printing results
        print("Loading corpus...")
        with open(self.corpus_file, "r", encoding="utf-8") as f:
            self.corpus_list = json.load(f)
            # Create a dict for O(1) lookup
            self.corpus_dict = {item["provision_id"]: item for item in self.corpus_list}
            
        # Load mapping
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
        model_name = 'bkai-foundation-models/vietnamese-bi-encoder'
        print(f"Loading SentenceTransformer model ({model_name})...")
        self.model = SentenceTransformer(model_name)
        
        print("All resources loaded successfully!\n")

    def search_bm25(self, query, top_k=5):
        tokenized_query = ViTokenizer.tokenize(query).lower().split()
        scores = self.bm25.get_scores(tokenized_query)
        top_n = np.argsort(scores)[::-1][:top_k]
        
        results = []
        for idx in top_n:
            prov_id = self.provision_ids[idx]
            results.append({
                "provision_id": prov_id,
                "score": scores[idx],
                "content": self.corpus_dict[prov_id]
            })
        return results

    def search_dense(self, query, top_k=5):
        query_embedding = self.model.encode([query], normalize_embeddings=True)
        query_embedding = np.array(query_embedding).astype("float32")
        
        scores, indices = self.faiss_index.search(query_embedding, top_k)
        
        results = []
        for i in range(top_k):
            idx = indices[0][i]
            if idx != -1: # FAISS returns -1 if not enough results
                prov_id = self.provision_ids[idx]
                results.append({
                    "provision_id": prov_id,
                    "score": float(scores[0][i]),
                    "content": self.corpus_dict[prov_id]
                })
        return results

def print_results(results, method_name):
    print(f"--- Top kết quả từ {method_name} ---")
    for i, res in enumerate(results):
        prov = res["content"]
        # In tóm tắt kết quả
        hieu_luc_str = "Hết hiệu lực" if prov["hieu_luc"] == "het_hieu_luc" else "Còn hiệu lực"
        print(f"[{i+1}] {prov['van_ban']} | {prov['tieu_de_dieu']} | Điểm: {res['score']:.4f}")
        print(f"Trạng thái: {hieu_luc_str}")
        print(f"Nội dung trích đoạn: {prov['noi_dung'][:200]}...\n")

def main():
    retriever = LegalRetriever()
    
    test_queries = [
        "Người lao động nghỉ việc có được hưởng trợ cấp thôi việc không?",
        "Thời gian thử việc tối đa là bao nhiêu ngày đối với lao động phổ thông?",
        "Người sử dụng lao động có quyền đơn phương chấm dứt hợp đồng lao động khi nào?"
    ]
    
    for query in test_queries:
        print("="*60)
        print(f"QUERY: {query}")
        print("="*60)
        
        # Sparse Retrieval
        start_time = time.time()
        bm25_results = retriever.search_bm25(query, top_k=3)
        bm25_time = time.time() - start_time
        print(f"BM25 Search Time: {bm25_time:.4f}s")
        print_results(bm25_results, "BM25 (Sparse)")
        
        # Dense Retrieval
        start_time = time.time()
        dense_results = retriever.search_dense(query, top_k=3)
        dense_time = time.time() - start_time
        print(f"Dense Search Time: {dense_time:.4f}s")
        print_results(dense_results, "FAISS (Dense)")

if __name__ == "__main__":
    main()
