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

sys.path.insert(0, os.path.dirname(__file__))

from retriever import LegalRetriever
from generator import LegalGenerator
from evaluate_retrieval import evaluate as eval_retrieval, print_summary_table as print_ret_summary
from evaluate_generation import compute_metrics as comp_gen_metrics
from rag_pipeline import execute_rag_pipeline

def main():
    data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    eval_dir = os.path.join(data_dir, "eval")
    test_set_path = os.path.join(eval_dir, "test_set_v2.json")
    TOP_K = 10
    RRF_K = 5
    ALPHA = 0.5
    RETRIEVAL_DEPTH = 50
    EXPAND_SIBLINGS = True
    HIEU_LUC_FILTER = "con_hieu_luc"
    MAX_CONTEXT_CHARS = 10_000
    
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
    
    retrieval_results = eval_retrieval(retriever, in_scope_test)
    print_ret_summary(retrieval_results)
    
    ret_output_path = os.path.join(eval_dir, "retrieval_results.json")
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

    methods = ["BM25", "Dense", "Hybrid_RRF"]

    gen_output_path = os.path.join(eval_dir, "generation_results.json")
    
    # Đọc kết quả đã chạy trước đó để resume (nếu có)
    if os.path.exists(gen_output_path):
        with open(gen_output_path, "r", encoding="utf-8") as f:
            all_gen_results = json.load(f)
    else:
        all_gen_results = {method: [] for method in methods}

    for method_name in methods:
        print(f"\n---> Bắt đầu đánh giá Generation cho pipeline: {method_name}")
        
        results_for_method = all_gen_results.get(method_name, [])
        
        # Chỉ skip những câu ĐÃ CÓ KẾT QUẢ THÀNH CÔNG (không bị api_error)
        processed_qids = {r["qid"] for r in results_for_method if not r.get("api_error", False)}
        
        # Lọc lại danh sách kết quả, vứt bỏ những câu lỗi API cũ để chạy lại đè lên
        results_for_method = [r for r in results_for_method if not r.get("api_error", False)]
        all_gen_results[method_name] = results_for_method
        
        for i, item in enumerate(test_set):
            qid = item["id"]
            if qid in processed_qids:
                continue # Đã xử lý, bỏ qua
                
            query = item["question"]
            category = item["category"]
            gold_ids = item.get("gold_provision_ids", [])
            is_out_of_scope = (category == "out_of_scope")

            print(f"  [{method_name}] [{i+1}/{len(test_set)}] {qid}: {query[:50]}...")
            
            # Thực thi chuỗi RAG qua đúng execute_rag_pipeline đồng bộ với app.py
            # (bao gồm query expansion, lọc hiệu lực với nhánh dự phòng khi rỗng, và giới hạn context 10.000 ký tự)
            res = execute_rag_pipeline(
                query=query,
                retriever=retriever,
                generator=generator,
                top_k=TOP_K,
                rrf_k=RRF_K,
                alpha=ALPHA,
                retrieval_depth=RETRIEVAL_DEPTH,
                expand_siblings=EXPAND_SIBLINGS,
                hieu_luc_filter=HIEU_LUC_FILTER,
                max_context_chars=MAX_CONTEXT_CHARS,
                retrieval_method=method_name,
            )
            
            retrieved_ids = [r["provision_id"] for r in res.get("chunks", [])]
            context_map = {
                r["provision_id"]: r.get("content", {}).get("noi_dung", "")
                for r in res.get("chunks", [])
            }

            res_dict = {
                "qid": qid,
                "question": query,
                "category": category,
                "is_out_of_scope": is_out_of_scope,
                "gold_ids": gold_ids,
                "retrieved_ids": retrieved_ids,
                "context_map": context_map,
                "raw_answer": res.get("raw_answer", ""),
                "answer": res["answer"],
                "citations": res["citations"],
                "hallucinated_ids": res["hallucinated_ids"],
                "normalized_ids": res.get("normalized_ids", []),
                "is_refusal": res["is_refusal"],
                "api_error": res.get("api_error", False),
                "error": res.get("error"),
                "retrieval_time": res.get("retrieval_time", 0.0),
                "generation_time": res.get("generation_time", 0.0),
            }
            
            results_for_method.append(res_dict)
            all_gen_results[method_name] = results_for_method
            
            status = "REFUSE" if res["is_refusal"] else "ANSWER"
            halluc = f" [HALLUC: {res['hallucinated_ids']}]" if res['hallucinated_ids'] else ""
            norm_tag = f" [NORMALIZED: {res.get('normalized_ids')}]" if res.get('normalized_ids') else ""
            print(f"         → {status}{halluc}{norm_tag}")
            
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
        print(f"  - Citation Validity (Chính xác - Phạt rút mã): {metrics['citation_validity']:.2%}" if metrics['citation_validity'] is not None else "  - Citation Validity (Chính xác): N/A")
        if metrics.get('citation_validity_relaxed') is not None:
            print(f"  - Citation Validity (Nới lỏng): {metrics['citation_validity_relaxed']:.2%}")
        if metrics.get('citation_normalized_rate') is not None:
            print(f"  - Tỷ lệ câu bị rút mã con: {metrics['citation_normalized_rate']:.2%}")
        print(f"  - Citation Accuracy: {metrics['citation_accuracy']:.2%}" if metrics.get('citation_accuracy') is not None else "  - Citation Accuracy: N/A")
        print(f"  - Citation Precision: {metrics['citation_precision']:.2%}" if metrics.get('citation_precision') is not None else "  - Citation Precision: N/A")
        print(f"  - Claim Support Rate (Ngữ nghĩa): {metrics['claim_support_rate']:.2%}" if metrics.get('claim_support_rate') is not None else "  - Claim Support Rate: N/A")


    # Lưu metrics tổng hợp ra file JSON riêng để tiện theo dõi và báo cáo
    gen_metrics_path = os.path.join(eval_dir, "generation_metrics.json")
    all_metrics = {m: comp_gen_metrics(res) for m, res in all_gen_results.items()}
    with open(gen_metrics_path, "w", encoding="utf-8") as f:
        json.dump(all_metrics, f, ensure_ascii=False, indent=2)

    print("\n" + "=" * 80)
    print("ĐÃ HOÀN THÀNH TOÀN BỘ THỰC NGHIỆM")
    print(f"Kết quả chi tiết lưu tại: {gen_output_path}")
    print(f"Kết quả metrics lưu tại:   {gen_metrics_path}")
    print("=" * 80)

if __name__ == "__main__":
    main()
