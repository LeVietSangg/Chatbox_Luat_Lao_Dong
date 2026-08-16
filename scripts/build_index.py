import os
import json
import pickle
import numpy as np
import faiss
from pyvi import ViTokenizer
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer
import time

def main():
    data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    corpus_file = os.path.join(data_dir, "structured", "corpus.json")
    index_dir = os.path.join(data_dir, "index")
    os.makedirs(index_dir, exist_ok=True)

    print(f"Loading corpus from {corpus_file}...")
    with open(corpus_file, "r", encoding="utf-8") as f:
        corpus = json.load(f)

    # Lọc ra các provision có nội dung (nếu có null)
    # Lấy thông tin
    provision_ids = []
    documents = []

    for item in corpus:
        provision_ids.append(item["provision_id"])
        # Có thể gộp thêm tiêu đề hoặc văn bản nếu cần, nhưng nội dung thường đã đủ
        # Nội dung đã chứa "Điều X. Tiêu đề..." ở đầu.
        text = item["noi_dung"]
        if not text:
            text = " "
        documents.append(text)

    print(f"Total documents: {len(documents)}")

    # 1. BM25 Index
    print("Tokenizing documents for BM25 (using pyvi)...")
    start_time = time.time()
    tokenized_docs = [ViTokenizer.tokenize(doc).lower().split() for doc in documents]
    print(f"Tokenization took {time.time() - start_time:.2f} seconds.")

    print("Building BM25 index...")
    bm25 = BM25Okapi(tokenized_docs)
    
    bm25_path = os.path.join(index_dir, "bm25_index.pkl")
    with open(bm25_path, "wb") as f:
        pickle.dump(bm25, f)
    print(f"Saved BM25 index to {bm25_path}")

    # 2. Dense Retrieval (FAISS)
    model_name = 'bkai-foundation-models/vietnamese-bi-encoder'
    print(f"Loading SentenceTransformer model ({model_name})...")
    # Sử dụng device cuda nếu có, nếu không thì cpu
    model = SentenceTransformer(model_name)

    print("Encoding documents for Dense Retrieval...")
    start_time = time.time()
    # Normalize embeddings for cosine similarity with Inner Product FAISS index
    embeddings = model.encode(documents, show_progress_bar=True, normalize_embeddings=True)
    embeddings = np.array(embeddings).astype("float32")
    print(f"Encoding took {time.time() - start_time:.2f} seconds.")
    print(f"Embeddings shape: {embeddings.shape}")

    # Build FAISS index
    dim = embeddings.shape[1]
    # faiss.IndexFlatIP for cosine similarity since embeddings are normalized
    faiss_index = faiss.IndexFlatIP(dim)
    faiss_index.add(embeddings)

    faiss_path = os.path.join(index_dir, "faiss_index.bin")
    faiss.write_index(faiss_index, faiss_path)
    print(f"Saved FAISS index to {faiss_path}")

    # Save mapping
    mapping_path = os.path.join(index_dir, "provision_mapping.json")
    with open(mapping_path, "w", encoding="utf-8") as f:
        json.dump(provision_ids, f, ensure_ascii=False, indent=2)
    print(f"Saved mapping to {mapping_path}")

    print("Index building completed successfully!")

if __name__ == "__main__":
    main()
