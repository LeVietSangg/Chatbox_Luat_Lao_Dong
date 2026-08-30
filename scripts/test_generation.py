import json
import os
import sys

# Thêm thư mục scripts vào path
sys.path.insert(0, os.path.dirname(__file__))

from retriever import LegalRetriever
from generator import LegalGenerator

def main():
    print("Khởi tạo Retriever...")
    retriever = LegalRetriever()
    
    print("Khởi tạo LLM Generator (Gemini)...")
    generator = LegalGenerator(model_name="gemini-2.5-flash", temperature=0.0)

    # Chọn một số câu hỏi từ dev set
    dev_set_path = os.path.join(os.path.dirname(__file__), "..", "data", "eval", "dev_set.json")
    with open(dev_set_path, "r", encoding="utf-8") as f:
        dev_set = json.load(f)

    # Test với 3 câu: 2 câu trong phạm vi, 1 câu ngoài phạm vi
    test_cases = [
        dev_set[0],  # in-scope
        dev_set[1],  # in-scope
        dev_set[-1]  # out-of-scope (câu giao tiếp)
    ]

    print("=" * 80)
    print("BẮT ĐẦU CHẠY THỬ NGHIỆM TÍCH HỢP RAG")
    print("=" * 80)

    for case in test_cases:
        query = case["question"]
        print(f"\n[CÂU HỎI]: {query}")
        print(f"[CATEGORY]: {case['category']}")
        
        # Bước 1: Retrieval
        # Sử dụng hybrid RRF, lấy top 5, lọc những văn bản còn hiệu lực
        results = retriever.search_hybrid(query, top_k=5)
        filtered_results = retriever.filter_by_hieu_luc(results, "con_hieu_luc")
        
        print(f"[RETRIEVER]: Đã tìm thấy {len(filtered_results)} tài liệu liên quan hợp lệ.")
        
        # Bước 2: Generation & Citation Verification
        gen_result = generator.generate(query, filtered_results)
        
        # In kết quả
        print("\n[LLM ANSWER]:")
        print(gen_result["answer"])
        
        # Phân tích
        if gen_result["hallucinated_ids"]:
            print(f"\n[WARNING] Đã lọc bỏ ảo giác (Hallucinated IDs): {gen_result['hallucinated_ids']}")
            
        print(f"[Citations verified]: {gen_result['citations']}")
        print(f"[Is Refusal?]: {gen_result['is_refusal']}")
        print("-" * 80)

if __name__ == "__main__":
    main()
