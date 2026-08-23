"""
evaluate_retrieval.py
Đánh giá hiệu suất của BM25, Dense và Hybrid Retrieval trên dev set.

Các chỉ số đo lường:
  - Recall@k (k=1, 3, 5): tỷ lệ gold provisions xuất hiện trong top-k.
  - MRR (Mean Reciprocal Rank): trung bình nghịch đảo hạng đầu tiên đúng.

Hỗ trợ 2 chế độ:
  - strict : gold_provision_ids (chỉ những provision trả lời trực tiếp).
  - relaxed: gold_provision_ids_relaxed (bao gồm cả các provision liên quan).
"""

import os
import sys
import json
import time
import numpy as np

# Thêm thư mục scripts vào path
sys.path.insert(0, os.path.dirname(__file__))
from retriever import LegalRetriever


# ======================================================================
# Các hàm tính metric
# ======================================================================

def recall_at_k(retrieved_ids, gold_ids, k):
    """Recall@k: bao nhiêu phần trăm gold_ids xuất hiện trong top-k kết quả."""
    if not gold_ids:
        return 0.0
    top_k_ids = retrieved_ids[:k]
    hits = len(set(top_k_ids) & set(gold_ids))
    return hits / len(gold_ids)


def reciprocal_rank(retrieved_ids, gold_ids, max_k=10):
    """Reciprocal Rank: 1/rank của kết quả đúng đầu tiên (giới hạn trong top max_k)."""
    top_k_ids = retrieved_ids[:max_k]
    for i, rid in enumerate(top_k_ids):
        if rid in gold_ids:
            return 1.0 / (i + 1)
    return 0.0


def hit_at_k(retrieved_ids, gold_ids, k):
    """Hit@k: 1 nếu có ít nhất 1 gold_id trong top-k, 0 nếu không."""
    top_k_ids = retrieved_ids[:k]
    return 1.0 if len(set(top_k_ids) & set(gold_ids)) > 0 else 0.0


# ======================================================================
# Hàm chạy đánh giá
# ======================================================================

def evaluate(retriever, dev_set, mode="strict", top_k_values=None):
    """Chạy đánh giá trên dev set.

    Args:
        retriever: LegalRetriever instance.
        dev_set: list of dicts, mỗi dict chứa question, gold_provision_ids, v.v.
        mode: 'strict' hoặc 'relaxed'.
        top_k_values: list các giá trị k cần đánh giá. Mặc định [1, 3, 5].

    Returns:
        dict chứa kết quả đánh giá theo từng phương pháp.
    """
    if top_k_values is None:
        top_k_values = [1, 3, 5]

    max_k = max(top_k_values)
    methods = {
        "BM25": lambda q: retriever.search_bm25(q, top_k=max_k),
        "Dense": lambda q: retriever.search_dense(q, top_k=max_k),
        "Hybrid_RRF": lambda q: retriever.search_hybrid(q, top_k=max_k, rrf_k=60),
    }

    # Khởi tạo accumulators
    results = {}
    for method_name in methods:
        results[method_name] = {
            "recall": {k: [] for k in top_k_values},
            "hit": {k: [] for k in top_k_values},
            "mrr": [],
            "latency": [],
            "per_query": [],
        }

    gold_key = "gold_provision_ids" if mode == "strict" else "gold_provision_ids_relaxed"

    for item in dev_set:
        qid = item["id"]
        question = item["question"]
        gold_ids = item.get(gold_key, item["gold_provision_ids"])

        for method_name, search_fn in methods.items():
            t0 = time.time()
            search_results = search_fn(question)
            latency = time.time() - t0

            retrieved_ids = [r["provision_id"] for r in search_results]

            # Tính metrics
            rr = reciprocal_rank(retrieved_ids, gold_ids)
            results[method_name]["mrr"].append(rr)
            results[method_name]["latency"].append(latency)

            query_detail = {
                "qid": qid,
                "question": question,
                "gold_ids": gold_ids,
                "retrieved_ids": retrieved_ids,
                "rr": rr,
                "latency": latency,
            }

            for k in top_k_values:
                r = recall_at_k(retrieved_ids, gold_ids, k)
                h = hit_at_k(retrieved_ids, gold_ids, k)
                results[method_name]["recall"][k].append(r)
                results[method_name]["hit"][k].append(h)
                query_detail[f"recall@{k}"] = r
                query_detail[f"hit@{k}"] = h

            results[method_name]["per_query"].append(query_detail)

    # Tính trung bình
    summary = {}
    for method_name, data in results.items():
        n = len(data["mrr"])
        latencies = np.array(data["latency"])
        method_summary = {
            "MRR@10": sum(data["mrr"]) / n,
            "Latency_p50_s": np.percentile(latencies, 50),
            "Latency_p95_s": np.percentile(latencies, 95),
        }
        for k in top_k_values:
            method_summary[f"Recall@{k}"] = sum(data["recall"][k]) / n
            method_summary[f"Hit@{k}"] = sum(data["hit"][k]) / n
        method_summary["per_query"] = data["per_query"]
        summary[method_name] = method_summary

    return summary


# ======================================================================
# In kết quả dạng bảng
# ======================================================================

def print_summary_table(summary, mode, top_k_values=None):
    """In bảng tổng hợp kết quả."""
    if top_k_values is None:
        top_k_values = [1, 3, 5]

    print(f"\n{'='*80}")
    print(f"KẾT QUẢ ĐÁNH GIÁ RETRIEVAL (mode={mode})")
    print(f"{'='*80}")

    # Header
    metrics = ["MRR@10"] + [f"Recall@{k}" for k in top_k_values] + \
              [f"Hit@{k}" for k in top_k_values] + ["Lat_p50", "Lat_p95"]
    header = f"{'Method':<16}" + "".join(f"{m:>12}" for m in metrics)
    print(header)
    print("-" * len(header))

    for method_name, data in summary.items():
        row = f"{method_name:<16}"
        row += f"{data['MRR@10']:>12.4f}"
        for k in top_k_values:
            row += f"{data[f'Recall@{k}']:>12.4f}"
        for k in top_k_values:
            row += f"{data[f'Hit@{k}']:>12.4f}"
        row += f"{data['Latency_p50_s']:>12.4f}"
        row += f"{data['Latency_p95_s']:>12.4f}"
        print(row)

    print()


def print_per_query_detail(summary, method_name, top_k_values=None):
    """In chi tiết từng câu hỏi cho một phương pháp."""
    if top_k_values is None:
        top_k_values = [1, 3, 5]

    print(f"\n--- Chi tiết {method_name} ---")
    for q in summary[method_name]["per_query"]:
        status = "✓" if q["rr"] > 0 else "✗"
        print(f"  {status} [{q['qid']}] RR={q['rr']:.2f} | {q['question'][:60]}")
        if q["rr"] == 0:
            print(f"      Gold: {q['gold_ids'][:3]}")
            print(f"      Got:  {q['retrieved_ids'][:3]}")


# ======================================================================
# Main
# ======================================================================

def main():
    data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    eval_dir = os.path.join(data_dir, "eval")

    # Load test set (changed from dev_set)
    test_set_path = os.path.join(eval_dir, "test_set_v1.json")
    print(f"Loading test set from {test_set_path}...")
    with open(test_set_path, "r", encoding="utf-8") as f:
        dev_set = json.load(f)
    # Filter out out_of_scope questions for pure retrieval evaluation
    dev_set = [q for q in dev_set if q["category"] != "out_of_scope"]
    print(f"Loaded {len(dev_set)} in-scope questions for retrieval evaluation.\n")

    # Load retriever
    retriever = LegalRetriever(data_dir=data_dir)

    # Đánh giá cả 2 mode
    for mode in ["strict", "relaxed"]:
        summary = evaluate(retriever, dev_set, mode=mode)
        print_summary_table(summary, mode)

        # Chi tiết cho các câu hỏi bị miss ở Hybrid
        print_per_query_detail(summary, "Hybrid_RRF")

    # Lưu kết quả đánh giá
    output_path = os.path.join(eval_dir, "eval_results.json")
    # Lưu bản tổng hợp (không bao gồm per_query để file nhỏ gọn)
    save_summary = {}
    for mode in ["strict", "relaxed"]:
        summary = evaluate(retriever, dev_set, mode=mode)
        save_summary[mode] = {}
        for method_name, data in summary.items():
            save_summary[mode][method_name] = {
                k: v for k, v in data.items() if k != "per_query"
            }
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(save_summary, f, ensure_ascii=False, indent=2)
    print(f"\nĐã lưu kết quả đánh giá: {output_path}")


if __name__ == "__main__":
    main()
