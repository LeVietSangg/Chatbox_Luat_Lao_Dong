"""
sweep_rrf_params.py

Thực nghiệm quét tham số (hyperparameter sweep) trên tập Dev Set:
- Hằng số RRF: k in [5, 10, 20, 60]
- Trọng số nhánh alpha (BM25): alpha in [0.3, 0.5, 0.7]

Mục đích:
- Xác định cấu hình RRF phù hợp trên Dev Set.
- Sau khi sweep, chọn một cặp (k, alpha) để sử dụng thống nhất
  cho evaluate_retrieval.py và run_experiments.py.
"""

import os
import sys
import json
import time
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from retriever import LegalRetriever
from evaluate_retrieval import recall_at_k, reciprocal_rank


def run_sweep():
    # ==============================================================
    # 1. Đường dẫn dữ liệu
    # ==============================================================

    data_dir = os.path.join(
        os.path.dirname(__file__), "..", "data"
    )

    eval_dir = os.path.join(data_dir, "eval")

    docs_dir = os.path.join(
        os.path.dirname(__file__), "..", "docs"
    )

    os.makedirs(docs_dir, exist_ok=True)

    # ==============================================================
    # 2. Đọc Dev Set
    # ==============================================================

    dev_set_path = os.path.join(
        eval_dir, "dev_set_v2.json"
    )

    with open(dev_set_path, "r", encoding="utf-8") as f:
        dev_set = json.load(f)

    # Chỉ đánh giá các câu hỏi trong phạm vi
    in_scope_dev = [
        q for q in dev_set
        if q.get("category") != "out_of_scope"
    ]

    print(
        f"Loaded {len(in_scope_dev)} in-scope questions "
        f"from Dev Set."
    )

    if not in_scope_dev:
        raise ValueError("Dev Set không có câu hỏi in-scope.")

    # ==============================================================
    # 3. Khởi tạo Retriever
    # ==============================================================

    retriever = LegalRetriever(data_dir=data_dir)

    # ==============================================================
    # 4. Các giá trị cần sweep
    # ==============================================================

    k_values = [5, 10, 20, 60]

    alpha_values = [0.3, 0.5, 0.7]

    # Các điều kiện cố định trong toàn bộ sweep
    TOP_K = 10
    RETRIEVAL_DEPTH = 50
    HIEU_LUC_FILTER = "con_hieu_luc"
    EXPAND_SIBLINGS = False

    # ==============================================================
    # 5. Lưu kết quả
    # ==============================================================

    results_table = []
    full_log = {}

    print("\n" + "=" * 90)

    print(
        f"{'k':<8}"
        f"{'alpha':<10}"
        f"{'Rec@1':<12}"
        f"{'Rec@3':<12}"
        f"{'Rec@5':<12}"
        f"{'MRR@10':<12}"
        f"{'Lat_p50(ms)':<14}"
    )

    print("=" * 90)

    # ==============================================================
    # 6. Sweep 12 cấu hình
    # ==============================================================

    for k in k_values:

        for alpha in alpha_values:

            config_key = f"k={k}_alpha={alpha}"

            rec1 = []
            rec3 = []
            rec5 = []
            mrrs = []
            lats = []

            print(
                f"\nRunning configuration: "
                f"k={k}, alpha={alpha}"
            )

            # ------------------------------------------------------
            # Chạy toàn bộ Dev Set
            # ------------------------------------------------------

            for item in in_scope_dev:

                q = item["question"]
                gold_ids = item["gold_provision_ids"]

                # Đo latency của Hybrid Retrieval
                t0 = time.time()

                res = retriever.search_hybrid(
                    q,
                    top_k=TOP_K,
                    rrf_k=k,
                    alpha=alpha,
                    retrieval_depth=RETRIEVAL_DEPTH,
                    expand_siblings=EXPAND_SIBLINGS,
                    hieu_luc_filter=HIEU_LUC_FILTER
                )

                lat = (time.time() - t0) * 1000.0

                pids = [
                    r["provision_id"]
                    for r in res
                ]

                # --------------------------------------------------
                # Tính các metric
                # --------------------------------------------------

                rec1.append(
                    recall_at_k(
                        pids,
                        gold_ids,
                        1
                    )
                )

                rec3.append(
                    recall_at_k(
                        pids,
                        gold_ids,
                        3
                    )
                )

                rec5.append(
                    recall_at_k(
                        pids,
                        gold_ids,
                        5
                    )
                )

                mrrs.append(
                    reciprocal_rank(
                        pids,
                        gold_ids,
                        max_k=10
                    )
                )

                lats.append(lat)

            # ------------------------------------------------------
            # Tính trung bình cho cấu hình hiện tại
            # ------------------------------------------------------

            n = len(in_scope_dev)

            m_rec1 = sum(rec1) / n
            m_rec3 = sum(rec3) / n
            m_rec5 = sum(rec5) / n
            m_mrr = sum(mrrs) / n

            p50_lat = float(
                np.percentile(lats, 50)
            )

            # ------------------------------------------------------
            # Lưu kết quả
            # ------------------------------------------------------

            row_data = {
                "k": k,
                "alpha": alpha,
                "recall@1": m_rec1,
                "recall@3": m_rec3,
                "recall@5": m_rec5,
                "mrr@10": m_mrr,
                "latency_p50_ms": p50_lat,
            }

            results_table.append(row_data)
            full_log[config_key] = row_data

            print(
                f"{k:<8}"
                f"{alpha:<10.1f}"
                f"{m_rec1:<12.4f}"
                f"{m_rec3:<12.4f}"
                f"{m_rec5:<12.4f}"
                f"{m_mrr:<12.4f}"
                f"{p50_lat:<14.2f}"
            )

    print("=" * 90)

    # ==============================================================
    # 7. Chọn cấu hình tốt nhất
    #
    # Tiêu chí:
    #   - Ưu tiên MRR@10
    #   - Nếu bằng nhau thì ưu tiên Recall@5
    # ==============================================================

    best_config = max(
        results_table,
        key=lambda x: (
            x["mrr@10"],
            x["recall@5"]
        )
    )

    print(
        f"\n[BEST CONFIG] "
        f"k = {best_config['k']}, "
        f"alpha = {best_config['alpha']}"
    )

    print(
        f"MRR@10 = {best_config['mrr@10']:.4f}, "
        f"Recall@5 = {best_config['recall@5']:.4f}"
    )

    # ==============================================================
    # 8. Lưu kết quả JSON
    # ==============================================================

    output_json = os.path.join(
        eval_dir,
        "rrf_param_sweep.json"
    )

    save_data = {
        "_metadata": {
            "timestamp": time.strftime(
                "%Y-%m-%d %H:%M:%S"
            ),

            "dataset": (
                f"dev_set.json "
                f"({len(in_scope_dev)} in-scope questions)"
            ),

            "k_values": k_values,
            "alpha_values": alpha_values,

            "top_k": TOP_K,
            "retrieval_depth": RETRIEVAL_DEPTH,
            "hieu_luc_filter": HIEU_LUC_FILTER,
            "expand_siblings": EXPAND_SIBLINGS,

            "selection_criterion": (
                "Maximize MRR@10, "
                "then Recall@5 as tie-break"
            ),

            "best_config": {
                "k": best_config["k"],
                "alpha": best_config["alpha"],
            },
        },

        "results": full_log,
    }

    with open(
        output_json,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            save_data,
            f,
            ensure_ascii=False,
            indent=2
        )

    # ==============================================================
    # 9. Xuất báo cáo Markdown
    # ==============================================================

    output_md = os.path.join(
        docs_dir,
        "sweep_rrf_results.md"
    )

    with open(
        output_md,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(
            "# Báo cáo Quét Tham số RRF "
            "(Hyperparameter Tuning trên Dev Set)\n\n"
        )

        f.write(
            f"- **Ngày thực hiện**: "
            f"{time.strftime('%Y-%m-%d %H:%M:%S')}\n"
        )

        f.write(
            f"- **Dữ liệu**: `data/eval/dev_set.json` "
            f"({len(in_scope_dev)} câu in-scope)\n"
        )

        f.write(
            f"- **Top-K**: {TOP_K}\n"
        )

        f.write(
            f"- **Retrieval depth**: {RETRIEVAL_DEPTH}\n"
        )

        f.write(
            f"- **Bộ lọc hiệu lực**: "
            f"`{HIEU_LUC_FILTER}`\n"
        )

        f.write(
            f"- **Expand siblings**: "
            f"`{EXPAND_SIBLINGS}`\n"
        )

        f.write(
            "- **Mục tiêu**: Xác định giá trị phù hợp "
            "của hằng số RRF $k$ và trọng số nhánh "
            "$\\alpha$ trên Dev Set.\n\n"
        )

        # ----------------------------------------------------------
        # Bảng kết quả
        # ----------------------------------------------------------

        f.write(
            "## 1. Bảng kết quả thực nghiệm\n\n"
        )

        f.write(
            "| $k$ | $\\alpha$ (BM25) | "
            "Recall@1 | Recall@3 | Recall@5 | "
            "MRR@10 | Latency p50 (ms) |\n"
        )

        f.write(
            "| :---: | :---: | :---: | :---: | "
            ":---: | :---: | :---: |\n"
        )

        for r in results_table:

            is_best = (
                " ⭐"
                if (
                    r["k"] == best_config["k"]
                    and r["alpha"] == best_config["alpha"]
                )
                else ""
            )

            f.write(
                f"| {r['k']} "
                f"| {r['alpha']} "
                f"| {r['recall@1']:.4f} "
                f"| {r['recall@3']:.4f} "
                f"| {r['recall@5']:.4f} "
                f"| {r['mrr@10']:.4f}{is_best} "
                f"| {r['latency_p50_ms']:.2f} |\n"
            )

        # ----------------------------------------------------------
        # Kết luận
        # ----------------------------------------------------------

        f.write(
            "\n## 2. Lựa chọn tham số\n\n"
        )

        f.write(
            f"Cấu hình được lựa chọn trên Dev Set là "
            f"**$k = {best_config['k']}$** và "
            f"**$\\alpha = {best_config['alpha']}$**, "
            f"với MRR@10 = "
            f"`{best_config['mrr@10']:.4f}` và "
            f"Recall@5 = "
            f"`{best_config['recall@5']:.4f}`. "
            f"Tiêu chí lựa chọn ưu tiên MRR@10 và sử dụng "
            f"Recall@5 làm tiêu chí phụ khi MRR@10 bằng nhau.\n"
        )

    # ==============================================================
    # 10. Thông báo file kết quả
    # ==============================================================

    print(
        f"\nSaved report to: {output_md}"
    )

    print(
        f"Saved JSON data to: {output_json}"
    )


if __name__ == "__main__":
    run_sweep()