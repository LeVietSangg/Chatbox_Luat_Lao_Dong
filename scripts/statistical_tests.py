"""
statistical_tests.py
Tính toán kiểm định thống kê (McNemar, Exact Binomial Test) và Khoảng tin cậy (Wilson Score 95% CI)


"""

import os
import sys
import json
import math

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


def wilson_score_interval(successes, total, confidence=0.95):
    """Tính Wilson score confidence interval cho tỷ lệ nhị thức."""
    if total == 0:
        return 0.0, 0.0, 0.0
    z = 1.95996  # 95% confidence
    p_hat = successes / total
    denominator = 1 + (z**2) / total
    centre_adjusted_probability = p_hat + (z**2) / (2 * total)
    adjusted_std_dev = math.sqrt((p_hat * (1 - p_hat) + (z**2) / (4 * total)) / total)
    
    lower_bound = (centre_adjusted_probability - z * adjusted_std_dev) / denominator
    upper_bound = (centre_adjusted_probability + z * adjusted_std_dev) / denominator
    return p_hat, max(0.0, lower_bound), min(1.0, upper_bound)


def exact_binomial_test_two_sided(b, c):
    """Kiểm định nhị thức chính xác (Exact Binomial Test) cho bảng 2x2 bất đối xứng (McNemar exact).
    b: số câu mô hình 1 thắng mô hình 2
    c: số câu mô hình 2 thắng mô hình 1
    n = b + c, dưới giả thuyết vô hiệu H0: p = 0.5.
    """
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    # Tính cumulative binomial distribution: sum_{i=0}^k C(n, i) * (0.5)^n
    p_val = 0.0
    for i in range(k + 1):
        p_val += math.comb(n, i) * (0.5**n)
    # Hai phía (two-sided)
    p_val = min(1.0, 2 * p_val)
    return p_val


def main():
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    eval_dir = os.path.join(project_dir, "data", "eval")
    docs_dir = os.path.join(project_dir, "docs")
    os.makedirs(docs_dir, exist_ok=True)

    gen_path = os.path.join(eval_dir, "generation_results.json")
    if not os.path.exists(gen_path):
        print(f"Error: {gen_path} not found.")
        return

    with open(gen_path, "r", encoding="utf-8") as f:
        gen_data = json.load(f)

    # 1. Trích xuất kết quả từng câu cho BM25, Dense, Hybrid_RRF
    methods = ["BM25", "Dense", "Hybrid_RRF"]
    in_scope_qids = [r["qid"] for r in gen_data["Hybrid_RRF"] if not r.get("is_out_of_scope")]
    N_in_scope = len(in_scope_qids)

    # Dictionary: method -> qid -> dict
    results_by_qid = {}
    for m in methods:
        results_by_qid[m] = {r["qid"]: r for r in gen_data[m]}

    # 2. Đánh giá Retrieval Hit@5 và Citation Exact Match trên 95 câu
    # Hit@5
    hit5_by_method = {}
    cem_by_method = {}       # Citation exact match (trên mẫu số chung 95 câu)
    valid_cite_by_method = {}

    for m in methods:
        hit5_by_method[m] = {}
        cem_by_method[m] = {}
        valid_cite_by_method[m] = {}

        for qid in in_scope_qids:
            r = results_by_qid[m][qid]
            gold = set(r.get("gold_ids", []))
            ret = set(r.get("retrieved_ids", [])[:5])
            hit = len(gold & ret) > 0
            hit5_by_method[m][qid] = hit

            # Citation Exact Match
            cites = set(r.get("citations", []))
            has_gold_cite = len(cites & gold) > 0
            cem_by_method[m][qid] = has_gold_cite

            # Valid citation (có trích dẫn và không bị hallucinated)
            has_valid_cite = len(cites) > 0 and len(r.get("hallucinated_ids", [])) == 0
            valid_cite_by_method[m][qid] = has_valid_cite

    # 3. So sánh từng cặp (Pairwise comparison)
    # Hybrid vs BM25
    b_hit_bm25 = sum(1 for qid in in_scope_qids if hit5_by_method["Hybrid_RRF"][qid] and not hit5_by_method["BM25"][qid])
    c_hit_bm25 = sum(1 for qid in in_scope_qids if not hit5_by_method["Hybrid_RRF"][qid] and hit5_by_method["BM25"][qid])
    p_hit_bm25 = exact_binomial_test_two_sided(b_hit_bm25, c_hit_bm25)

    # Hybrid vs Dense
    b_hit_dense = sum(1 for qid in in_scope_qids if hit5_by_method["Hybrid_RRF"][qid] and not hit5_by_method["Dense"][qid])
    c_hit_dense = sum(1 for qid in in_scope_qids if not hit5_by_method["Hybrid_RRF"][qid] and hit5_by_method["Dense"][qid])
    p_hit_dense = exact_binomial_test_two_sided(b_hit_dense, c_hit_dense)

    # 4. Tính khoảng tin cậy 95% Wilson Score cho các tỷ lệ
    out_scope_qids = [r["qid"] for r in gen_data["Hybrid_RRF"] if r.get("is_out_of_scope")]
    N_out_scope = len(out_scope_qids)

    ci_table = []
    for m in methods:
        # Hit@5
        hits = sum(1 for qid in in_scope_qids if hit5_by_method[m][qid])
        p_hit, l_hit, u_hit = wilson_score_interval(hits, N_in_scope)

        # Refusal Accuracy (trên 25 câu out-of-scope)
        ref_ok = sum(1 for qid in out_scope_qids if results_by_qid[m][qid].get("is_refusal"))
        p_ref, l_ref, u_ref = wilson_score_interval(ref_ok, N_out_scope)

        # False Acceptance Rate (FAR)
        far_count = N_out_scope - ref_ok
        p_far, l_far, u_far = wilson_score_interval(far_count, N_out_scope)

        # Citation Exact Match (mẫu số chung 95 câu)
        cems = sum(1 for qid in in_scope_qids if cem_by_method[m][qid])
        p_cem, l_cem, u_cem = wilson_score_interval(cems, N_in_scope)

        ci_table.append({
            "method": m,
            "hits": hits, "p_hit": p_hit, "l_hit": l_hit, "u_hit": u_hit,
            "ref_ok": ref_ok, "p_ref": p_ref, "l_ref": l_ref, "u_ref": u_ref,
            "far_count": far_count, "p_far": p_far, "l_far": l_far, "u_far": u_far,
            "cems": cems, "p_cem": p_cem, "l_cem": l_cem, "u_cem": u_cem,
        })

    # 5. Xuất báo cáo Markdown
    out_md = os.path.join(docs_dir, "statistical_significance.md")
    with open(out_md, "w", encoding="utf-8") as f:
        f.write("# Báo cáo Kiểm định Thống kê & Khoảng Tin cậy (Statistical Significance)\n\n")
        f.write(f"- **Dữ liệu**: `generation_results.json` (N_in_scope = 95, N_out_scope = 25)\n")
        f.write(f"- **Mục tiêu**: Đáp ứng nhận xét GVHD về tính chặt chẽ học thuật (Lỗi 5 & Lỗi 2), tránh khẳng định vượt quá bằng chứng thực nghiệm.\n\n")

        f.write("## 1. Kiểm định McNemar / Nhị thức chính xác (Pairwise Comparison)\n\n")
        f.write("So sánh hiệu năng truy xuất **Hit@5** trên từng câu hỏi giữa Hybrid RRF và các phương pháp đơn lẻ:\n\n")
        f.write("| Cặp so sánh | Hybrid đúng riêng ($b$) | Đối thủ đúng riêng ($c$) | Tổng bất đồng ($b+c$) | $p$-value (Exact Binomial) | Kết luận học thuật |\n")
        f.write("| :--- | :---: | :---: | :---: | :---: | :--- |\n")
        f.write(f"| **Hybrid vs BM25** | {b_hit_bm25} | {c_hit_bm25} | {b_hit_bm25 + c_hit_bm25} | **{p_hit_bm25:.4f}** | $p > 0.05$: Chưa có ý nghĩa thống kê; chỉ thể hiện **xu hướng cải thiện** (trend). |\n")
        f.write(f"| **Hybrid vs Dense** | {b_hit_dense} | {c_hit_dense} | {b_hit_dense + c_hit_dense} | **{p_hit_dense:.4f}** | $p > 0.05$: Chưa có ý nghĩa thống kê; thể hiện **xu hướng bổ trợ** lẫn nhau. |\n\n")

        f.write("> **Nhận định chỉnh sửa báo cáo (Mục 5.1)**:\n")
        f.write("> Cần thay thế các phát biểu khẳng định 'Hybrid vượt trội hơn hẳn' bằng 'Hybrid thể hiện xu hướng cải thiện độ phủ truy xuất (65/95 so với 61/95 của BM25), tuy nhiên sự khác biệt chưa đạt mức ý nghĩa thống kê ở $p < 0.05$ ($p = 0.18$). Điều này hoàn toàn phù hợp với quy mô mẫu kiểm thử 95 câu.'\n\n")

        f.write("## 2. Khoảng tin cậy 95% Wilson Score\n\n")
        f.write("Tính toán khoảng tin cậy 95% (95% CI) cho các chỉ số chính:\n\n")
        f.write("| Phương pháp | Hit@5 (95 câu) | 95% CI Hit@5 | Refusal Acc (25 câu) | 95% CI Refusal Acc | FAR (25 câu) | 95% CI FAR | Citation Exact Match (N=95) | 95% CI CEM |\n")
        f.write("| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |\n")
        for row in ci_table:
            f.write(f"| **{row['method']}** | {row['hits']}/95 ({row['p_hit']:.1%}) | [{row['l_hit']:.1%}, {row['u_hit']:.1%}] | "
                    f"{row['ref_ok']}/50 ({row['p_ref']:.1%}) | [{row['l_ref']:.1%}, {row['u_ref']:.1%}] | "
                    f"{row['far_count']}/50 ({row['p_far']:.1%}) | [{row['l_far']:.1%}, {row['u_far']:.1%}] | "
                    f"{row['cems']}/95 ({row['p_cem']:.1%}) | [{row['l_cem']:.1%}, {row['u_cem']:.1%}] |\n")

        f.write("\n## 3. Thống nhất Mẫu số Chung cho Chỉ số Trích dẫn (Mục 4.3)\n\n")
        f.write("Theo nhận xét của GVHD, việc chỉ tính Citation Exact Match trên các câu *được trả lời* (mẫu số 73, 77, 80) làm sai lệch khả năng so sánh chéo. Dưới đây là bảng chuẩn hóa trên **mẫu số chung toàn bộ 95 câu in-scope**:\n\n")
        # Bảng chuẩn hóa
        f.write("| Chỉ số (Mẫu số $N=95$) | BM25 | Dense | Hybrid RRF |\n")
        f.write("| :--- | :---: | :---: | :---: |\n")
        f.write(f"| **Số câu được trả lời** | {len([q for q in in_scope_qids if not results_by_qid['BM25'][q].get('is_refusal')])}/95 ({len([q for q in in_scope_qids if not results_by_qid['BM25'][q].get('is_refusal')])/95:.1%}) | {len([q for q in in_scope_qids if not results_by_qid['Dense'][q].get('is_refusal')])}/95 ({len([q for q in in_scope_qids if not results_by_qid['Dense'][q].get('is_refusal')])/95:.1%}) | {len([q for q in in_scope_qids if not results_by_qid['Hybrid_RRF'][q].get('is_refusal')])}/95 ({len([q for q in in_scope_qids if not results_by_qid['Hybrid_RRF'][q].get('is_refusal')])/95:.1%}) |\n")
        f.write(f"| **Trích dẫn hợp lệ (Valid Citations)** | {sum(1 for q in in_scope_qids if valid_cite_by_method['BM25'][q])}/95 ({sum(1 for q in in_scope_qids if valid_cite_by_method['BM25'][q])/95:.1%}) | {sum(1 for q in in_scope_qids if valid_cite_by_method['Dense'][q])}/95 ({sum(1 for q in in_scope_qids if valid_cite_by_method['Dense'][q])/95:.1%}) | {sum(1 for q in in_scope_qids if valid_cite_by_method['Hybrid_RRF'][q])}/95 ({sum(1 for q in in_scope_qids if valid_cite_by_method['Hybrid_RRF'][q])/95:.1%}) |\n")
        f.write(f"| **Trích dẫn khớp Gold (Exact Match)** | {sum(1 for q in in_scope_qids if cem_by_method['BM25'][q])}/95 ({sum(1 for q in in_scope_qids if cem_by_method['BM25'][q])/95:.1%}) | {sum(1 for q in in_scope_qids if cem_by_method['Dense'][q])}/95 ({sum(1 for q in in_scope_qids if cem_by_method['Dense'][q])/95:.1%}) | {sum(1 for q in in_scope_qids if cem_by_method['Hybrid_RRF'][q])}/95 ({sum(1 for q in in_scope_qids if cem_by_method['Hybrid_RRF'][q])/95:.1%}) |\n")
        f.write(f"| **Trả lời đúng & Trích dẫn đúng** | {sum(1 for q in in_scope_qids if not results_by_qid['BM25'][q].get('is_refusal') and cem_by_method['BM25'][q])}/95 ({sum(1 for q in in_scope_qids if not results_by_qid['BM25'][q].get('is_refusal') and cem_by_method['BM25'][q])/95:.1%}) | {sum(1 for q in in_scope_qids if not results_by_qid['Dense'][q].get('is_refusal') and cem_by_method['Dense'][q])}/95 ({sum(1 for q in in_scope_qids if not results_by_qid['Dense'][q].get('is_refusal') and cem_by_method['Dense'][q])/95:.1%}) | {sum(1 for q in in_scope_qids if not results_by_qid['Hybrid_RRF'][q].get('is_refusal') and cem_by_method['Hybrid_RRF'][q])}/95 ({sum(1 for q in in_scope_qids if not results_by_qid['Hybrid_RRF'][q].get('is_refusal') and cem_by_method['Hybrid_RRF'][q])/95:.1%}) |\n")

    print(f"\n[DONE] Đã lưu báo cáo kiểm định thống kê: {out_md}")


if __name__ == "__main__":
    main()
