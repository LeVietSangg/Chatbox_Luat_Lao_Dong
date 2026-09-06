"""
run_experiments.py
Chạy thực nghiệm chính thức (Tuần 6) trên tập Test Set 120 câu.
Bao gồm:
1. Đánh giá Retrieval (BM25, Dense, Hybrid) - Tính Recall@1/3/5, MRR@10
2. Đánh giá Generation (Refusal, Citation) trên 3 cấu hình Retrieval.

Do giới hạn Rate Limit của Gemini API (5 req/min), quá trình Generation sẽ mất khá nhiều thời gian.
Script có cơ chế lưu checkpoint để có thể chạy tiếp nếu bị gián đoạn.
"""

import os
import sys
import json
import time
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))

from retriever import LegalRetriever
from generator import LegalGenerator
from evaluate_retrieval import evaluate as eval_retrieval, print_summary_table as print_ret_summary
from evaluate_generation import compute_metrics as comp_gen_metrics, print_report as print_gen_report

def main():
    data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    eval_dir = os.path.join(data_dir, "eval")
    test_set_path = os.path.join(eval_dir, "test_set_v1.json")
    
    print("=" * 80)
    print("BẮT ĐẦU CHẠY THỬ NGHIỆM CHÍNH THỨC - TUẦN 6")
    print("=" * 80)

    # 1. Load Test Set
    with open(test_set_path, "r", encoding="utf-8") as f:
        test_set = json.load(f)
    print(f"[INFO] Loaded Test Set: {len(test_set)} câu hỏi.")

    # 2. Khởi tạo Modules
    print("[INFO] Khởi tạo LegalRetriever và LegalGenerator...")
    retriever = LegalRetriever(data_dir=data_dir)
    generator = LegalGenerator(model_name="gemini-3.5-flash-lite", temperature=0.0)

    # =========================================================================
    # PHẦN 1: RETRIEVAL EVALUATION
    # =========================================================================
    print("\n" + "=" * 80)
    print("PHẦN 1: RETRIEVAL EVALUATION (BM25 vs Dense vs Hybrid)")
    print("=" * 80)
    
    # Lọc các câu in_scope để tính retrieval
    in_scope_test = [q for q in test_set if q["category"] != "out_of_scope"]
    
    retrieval_results = eval_retrieval(retriever, in_scope_test, mode="strict")
    print_ret_summary(retrieval_results, mode="strict")
    
    ret_output_path = os.path.join(eval_dir, "week6_retrieval_results.json")
    with open(ret_output_path, "w", encoding="utf-8") as f:
        # Chỉ lưu metric, bỏ qua per_query cho nhẹ
        summary_to_save = {method: {k: v for k,v in data.items() if k != 'per_query'} for method, data in retrieval_results.items()}
        json.dump(summary_to_save, f, ensure_ascii=False, indent=2)
    print(f"[LƯU] Kết quả Retrieval đã lưu tại: {ret_output_path}")

    # =========================================================================
    # PHẦN 2: GENERATION EVALUATION CHÉO CÁC PIPELINE
    # =========================================================================
    print("\n" + "=" * 80)
    print("PHẦN 2: GENERATION EVALUATION CHÉO TRÊN 3 THIẾT LẬP RETRIEVAL")
    print("LƯU Ý: Quá trình này sẽ mất khoảng 1.5 tiếng do giới hạn Rate Limit của Gemini (5 req/min)")
    print("=" * 80)

    methods = {
        "BM25": lambda q: retriever.search_bm25(q, top_k=5),
        "Dense": lambda q: retriever.search_dense(q, top_k=5),
        "Hybrid_RRF": lambda q: retriever.search_hybrid(q, top_k=5, rrf_k=60),
    }

    gen_output_path = os.path.join(eval_dir, "week6_generation_results.json")
    
    # Đọc kết quả đã chạy trước đó để resume (nếu có)
    if os.path.exists(gen_output_path):
        with open(gen_output_path, "r", encoding="utf-8") as f:
            all_gen_results = json.load(f)
    else:
        all_gen_results = {method: [] for method in methods}

    for method_name, search_fn in methods.items():
        print(f"\n---> Bắt đầu đánh giá Generation cho pipeline: {method_name}")
        
        results_for_method = all_gen_results.get(method_name, [])
        processed_qids = {r["qid"] for r in results_for_method}
        
        for i, item in enumerate(test_set):
            qid = item["id"]
            if qid in processed_qids:
                continue # Đã xử lý, bỏ qua
                
            query = item["question"]
            category = item["category"]
            gold_ids = item.get("gold_provision_ids", [])
            is_out_of_scope = (category == "out_of_scope")

            print(f"  [{method_name}] [{i+1}/{len(test_set)}] {qid}: {query[:50]}...")
            
            # Retrieval Step
            t0 = time.time()
            search_results = search_fn(query)
            filtered = retriever.filter_by_hieu_luc(search_results, "con_hieu_luc")
            retrieval_time = time.time() - t0
            
            # Generation Step
            t0 = time.time()
            gen_result = generator.generate(query, filtered)
            generation_time = time.time() - t0
            
            retrieved_ids = [r["provision_id"] for r in filtered]
            
            res_dict = {
                "qid": qid,
                "question": query,
                "category": category,
                "is_out_of_scope": is_out_of_scope,
                "gold_ids": gold_ids,
                "retrieved_ids": retrieved_ids,
                "answer": gen_result["answer"],
                "citations": gen_result["citations"],
                "hallucinated_ids": gen_result["hallucinated_ids"],
                "is_refusal": gen_result["is_refusal"],
                "api_error": gen_result.get("api_error", False),
                "error": gen_result.get("error"),
                "retrieval_time": retrieval_time,
                "generation_time": generation_time,
            }
            
            results_for_method.append(res_dict)
            all_gen_results[method_name] = results_for_method
            
            status = "REFUSE" if gen_result["is_refusal"] else "ANSWER"
            halluc = f" [HALLUC: {gen_result['hallucinated_ids']}]" if gen_result["hallucinated_ids"] else ""
            print(f"         → {status}{halluc}")
            
            # Lưu ngay sau mỗi request để không mất dữ liệu
            with open(gen_output_path, "w", encoding="utf-8") as f:
                json.dump(all_gen_results, f, ensure_ascii=False, indent=2)
                
            # Rate limit backoff (13s cho chắc chắn an toàn)
            time.sleep(13)
            
        print(f"\n[DONE] Hoàn thành pipeline: {method_name}")
        
        # Tính và in báo cáo ngay cho method này
        metrics = comp_gen_metrics(results_for_method)
        print(f"\n[METRICS CHO {method_name}]:")
        print(f"  - Refusal Accuracy: {metrics['refusal_accuracy']:.2%}" if metrics['refusal_accuracy'] is not None else "  - Refusal Accuracy: N/A")
        print(f"  - False Refusal Rate: {metrics['false_refusal_rate']:.2%}" if metrics['false_refusal_rate'] is not None else "  - False Refusal Rate: N/A")
        print(f"  - Citation Validity: {metrics['citation_validity']:.2%}" if metrics['citation_validity'] is not None else "  - Citation Validity: N/A")
        print(f"  - Citation Exact Match: {metrics['citation_exact_match']:.2%}" if metrics['citation_exact_match'] is not None else "  - Citation Exact Match: N/A")

    print("\n" + "=" * 80)
    print("ĐÃ HOÀN THÀNH TOÀN BỘ THỰC NGHIỆM TUẦN 6!")
    print(f"Kết quả lưu tại: {gen_output_path}")
    print("=" * 80)

if __name__ == "__main__":
    main()
