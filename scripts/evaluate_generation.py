"""
evaluate_generation.py
Đánh giá hiệu suất Generation trên dev set.

Các chỉ số đo lường:
  - Refusal Accuracy: Tỷ lệ câu out_of_scope bị từ chối đúng.
  - False Refusal Rate: Tỷ lệ câu in_scope bị từ chối sai.
  - Citation Validity: Tỷ lệ citation hợp lệ (không bị hallucinate).
  - Citation Exact Match: Tỷ lệ câu mà citation khớp đúng gold_provision_ids.
"""

import os
import sys
import json
import time

sys.path.insert(0, os.path.dirname(__file__))

from retriever import LegalRetriever
from generator import LegalGenerator


def run_evaluation(retriever, generator, eval_set, top_k=5):
    """Chạy pipeline RAG trên toàn bộ eval set và thu thập kết quả."""

    results = []

    for i, item in enumerate(eval_set):
        qid = item["id"]
        query = item["question"]
        category = item["category"]
        gold_ids = item.get("gold_provision_ids", [])
        is_out_of_scope = (category == "out_of_scope")

        print(f"  [{i+1}/{len(eval_set)}] {qid}: {query[:60]}...")

        # Retrieval
        t0 = time.time()
        search_results = retriever.search_hybrid(query, top_k=top_k)
        filtered = retriever.filter_by_hieu_luc(search_results, "con_hieu_luc")
        retrieval_time = time.time() - t0

        # Generation
        t0 = time.time()
        gen_result = generator.generate(query, filtered)
        generation_time = time.time() - t0

        # Thu thập kết quả
        retrieved_ids = [r["provision_id"] for r in filtered]
        results.append({
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
            "retrieval_time": retrieval_time,
            "generation_time": generation_time,
        })

        # Trạng thái nhanh
        status = "REFUSE" if gen_result["is_refusal"] else "ANSWER"
        halluc = f" [HALLUC: {gen_result['hallucinated_ids']}]" if gen_result["hallucinated_ids"] else ""
        print(f"         → {status}{halluc}")

        # Chờ giữa các request để tránh rate limit (5 req/min free tier)
        if i < len(eval_set) - 1:
            time.sleep(13)

    return results


def compute_metrics(results):
    """Tính toán các chỉ số đánh giá Generation."""

    # Phân loại câu hỏi
    in_scope = [r for r in results if not r["is_out_of_scope"]]
    out_scope = [r for r in results if r["is_out_of_scope"]]

    # =================================================================
    # 1. REFUSAL METRICS
    # =================================================================

    # Refusal Accuracy: Tỷ lệ câu out_of_scope bị từ chối đúng
    if out_scope:
        correct_refusals = sum(1 for r in out_scope if r["is_refusal"])
        refusal_accuracy = correct_refusals / len(out_scope)
    else:
        refusal_accuracy = None

    # False Refusal Rate: Tỷ lệ câu in_scope bị từ chối sai
    if in_scope:
        false_refusals = sum(1 for r in in_scope if r["is_refusal"])
        false_refusal_rate = false_refusals / len(in_scope)
    else:
        false_refusal_rate = None

    # False Acceptance Rate: Tỷ lệ câu out_of_scope mà LLM trả lời (sai)
    if out_scope:
        false_accepts = sum(1 for r in out_scope if not r["is_refusal"])
        false_acceptance_rate = false_accepts / len(out_scope)
    else:
        false_acceptance_rate = None

    # =================================================================
    # 2. CITATION METRICS (chỉ tính trên câu in_scope mà LLM trả lời)
    # =================================================================

    answered_in_scope = [r for r in in_scope if not r["is_refusal"]]

    # Citation Validity: Tỷ lệ câu KHÔNG có hallucinated citation
    if answered_in_scope:
        no_halluc = sum(1 for r in answered_in_scope if not r["hallucinated_ids"])
        citation_validity = no_halluc / len(answered_in_scope)
    else:
        citation_validity = None

    # Citation Exact Match: Tỷ lệ câu mà ít nhất 1 citation khớp gold_id
    if answered_in_scope:
        exact_matches = 0
        for r in answered_in_scope:
            if r["gold_ids"] and r["citations"]:
                if set(r["citations"]) & set(r["gold_ids"]):
                    exact_matches += 1
        citation_exact_match = exact_matches / len(answered_in_scope)
    else:
        citation_exact_match = None

    # =================================================================
    # 3. LATENCY
    # =================================================================

    import numpy as np
    gen_times = [r["generation_time"] for r in results]

    metrics = {
        "total_questions": len(results),
        "in_scope_count": len(in_scope),
        "out_scope_count": len(out_scope),
        "answered_in_scope_count": len(answered_in_scope),

        "refusal_accuracy": refusal_accuracy,
        "false_refusal_rate": false_refusal_rate,
        "false_acceptance_rate": false_acceptance_rate,

        "citation_validity": citation_validity,
        "citation_exact_match": citation_exact_match,

        "generation_latency_p50_s": float(np.percentile(gen_times, 50)),
        "generation_latency_p95_s": float(np.percentile(gen_times, 95)),
    }

    return metrics


def print_report(metrics, results):
    """In báo cáo kết quả."""

    print("\n" + "=" * 72)
    print("KẾT QUẢ ĐÁNH GIÁ GENERATION")
    print("=" * 72)

    print(f"\nTổng số câu hỏi:         {metrics['total_questions']}")
    print(f"  - Trong phạm vi:       {metrics['in_scope_count']}")
    print(f"  - Ngoài phạm vi:       {metrics['out_scope_count']}")
    print(f"  - Đã trả lời (in):     {metrics['answered_in_scope_count']}")

    print(f"\n--- Refusal Metrics ---")
    if metrics["refusal_accuracy"] is not None:
        print(f"  Refusal Accuracy:       {metrics['refusal_accuracy']:.2%}")
    if metrics["false_refusal_rate"] is not None:
        print(f"  False Refusal Rate:     {metrics['false_refusal_rate']:.2%}")
    if metrics["false_acceptance_rate"] is not None:
        print(f"  False Acceptance Rate:  {metrics['false_acceptance_rate']:.2%}")

    print(f"\n--- Citation Metrics ---")
    if metrics["citation_validity"] is not None:
        print(f"  Citation Validity:      {metrics['citation_validity']:.2%}")
    if metrics["citation_exact_match"] is not None:
        print(f"  Citation Exact Match:   {metrics['citation_exact_match']:.2%}")

    print(f"\n--- Latency ---")
    print(f"  Generation p50:         {metrics['generation_latency_p50_s']:.2f}s")
    print(f"  Generation p95:         {metrics['generation_latency_p95_s']:.2f}s")

    # Chi tiết các câu bị lỗi
    print(f"\n--- Chi tiết False Refusal (câu in-scope bị từ chối sai) ---")
    false_refs = [r for r in results if not r["is_out_of_scope"] and r["is_refusal"]]
    if false_refs:
        for r in false_refs:
            print(f"  ✗ [{r['qid']}] {r['question'][:60]}")
            print(f"      Gold: {r['gold_ids'][:3]}")
    else:
        print("  (Không có)")

    print(f"\n--- Chi tiết False Acceptance (câu out-of-scope bị trả lời sai) ---")
    false_accs = [r for r in results if r["is_out_of_scope"] and not r["is_refusal"]]
    if false_accs:
        for r in false_accs:
            print(f"  ✗ [{r['qid']}] {r['question'][:60]}")
            print(f"      Answer: {r['answer'][:80]}...")
    else:
        print("  (Không có)")

    print(f"\n--- Chi tiết Hallucination ---")
    halluc_cases = [r for r in results if r["hallucinated_ids"]]
    if halluc_cases:
        for r in halluc_cases:
            print(f"  ✗ [{r['qid']}] {r['question'][:60]}")
            print(f"      Hallucinated: {r['hallucinated_ids']}")
    else:
        print("  (Không có)")

    print()


def main():
    data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    eval_dir = os.path.join(data_dir, "eval")

    # Load dev set
    dev_set_path = os.path.join(eval_dir, "dev_set.json")
    print(f"Loading dev set from {dev_set_path}...")
    with open(dev_set_path, "r", encoding="utf-8") as f:
        dev_set = json.load(f)
    print(f"Loaded {len(dev_set)} questions.\n")

    # Load retriever & generator
    retriever = LegalRetriever(data_dir=data_dir)
    generator = LegalGenerator(model_name="gemini-2.5-flash", temperature=0.0)

    # Chạy đánh giá
    print("Bắt đầu đánh giá Generation trên Dev Set...")
    results = run_evaluation(retriever, generator, dev_set)

    # Tính metrics
    metrics = compute_metrics(results)

    # In báo cáo
    print_report(metrics, results)

    # Lưu kết quả
    output_path = os.path.join(eval_dir, "generation_eval_results.json")
    save_data = {
        "metrics": metrics,
        "per_query": results
    }
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(save_data, f, ensure_ascii=False, indent=2)
    print(f"Đã lưu kết quả đánh giá: {output_path}")


if __name__ == "__main__":
    main()
