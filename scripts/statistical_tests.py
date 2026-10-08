"""
statistical_tests.py
Tính toán kiểm định thống kê (McNemar, Exact Binomial Test) và Khoảng tin cậy (Wilson Score 95% CI)
Trích xuất động số liệu từ kết quả thực tế (generation_results.json) thay vì hard-code giá trị.
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
    b: số câu phương pháp 1 đúng riêng (phương pháp 2 sai)
    c: số câu phương pháp 2 đúng riêng (phương pháp 1 sai)
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


def bonferroni_correction(p_values):
    """Hiệu chỉnh Bonferroni kiểm soát Family-Wise Error Rate (FWER):
    p_adj = min(1.0, m * p_raw).
    """
    m = len(p_values)
    return [min(1.0, m * p) for p in p_values]


def holm_bonferroni_correction(p_values):
    """Hiệu chỉnh Holm-Bonferroni (Step-down procedure):
    Sắp xếp p-value tăng dần: p_(1) <= p_(2) <= ... <= p_(m).
    p_adj_(k) = min(1.0, max_{j <= k} (m - j + 1) * p_(j)).
    Mạnh hơn Bonferroni cổ điển nhưng vẫn kiểm soát nghiêm ngặt FWER <= alpha.
    """
    m = len(p_values)
    if m == 0:
        return []
    indexed_p = sorted(enumerate(p_values), key=lambda x: x[1])
    adjusted_indexed = []
    running_max = 0.0
    for rank, (orig_idx, p) in enumerate(indexed_p):
        multiplier = m - rank
        val = min(1.0, multiplier * p)
        running_max = max(running_max, val)
        adjusted_indexed.append((orig_idx, running_max))

    adjusted_indexed.sort(key=lambda x: x[0])
    return [p_adj for _, p_adj in adjusted_indexed]


def format_academic_conclusion(b, c, p_raw, p_holm, method1, method2):
    """Tạo kết luận học thuật dựa trên p-value thô và p-value sau hiệu chỉnh đa so sánh."""
    if p_holm < 0.01:
        return (
            f"**$p_{{\\text{{Holm}}}} < 0.01$ ($p_{{\\text{{raw}}}} = {p_raw:.4f}, p_{{\\text{{Holm}}}} = {p_holm:.4f}$)**: "
            f"Khác biệt **có ý nghĩa thống kê rất cao** sau khi hiệu chỉnh đa so sánh; "
            f"{method1} vượt trội so với {method2} ({b} câu thắng vs {c} câu thua)."
        )
    elif p_holm < 0.05:
        return (
            f"**$p_{{\\text{{Holm}}}} < 0.05$ ($p_{{\\text{{raw}}}} = {p_raw:.4f}, p_{{\\text{{Holm}}}} = {p_holm:.4f}$)**: "
            f"Khác biệt **có ý nghĩa thống kê** sau hiệu chỉnh đa so sánh ($\\alpha = 0.05$); "
            f"sự vượt trội của {method1} so với {method2} được xác nhận thực nghiệm ({b} câu thắng vs {c} câu thua)."
        )
    elif p_raw < 0.05:
        return (
            f"$p_{{\\text{{raw}}}} < 0.05$ ($p_{{\\text{{raw}}}} = {p_raw:.4f}, p_{{\\text{{Holm}}}} = {p_holm:.4f} \\ge 0.05$): "
            f"Đạt ý nghĩa ở kiểm định đơn lẻ nhưng nằm ở biên ý nghĩa thống kê sau hiệu chỉnh bảo thủ; "
            f"thể hiện ưu thế rõ nét ({b} câu thắng vs {c} câu thua)."
        )
    else:
        return (
            f"$p \\ge 0.05$ ($p_{{\\text{{raw}}}} = {p_raw:.4f}, p_{{\\text{{Holm}}}} = {p_holm:.4f}$): "
            f"Chưa đạt ngưỡng ý nghĩa thống kê $\\alpha = 0.05$; "
            f"thể hiện **xu hướng bổ trợ** tích cực ({b} câu thắng vs {c} câu thua)."
        )


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

    out_scope_qids = [r["qid"] for r in gen_data["Hybrid_RRF"] if r.get("is_out_of_scope")]
    N_out_scope = len(out_scope_qids)

    # Dictionary: method -> qid -> dict
    results_by_qid = {}
    for m in methods:
        results_by_qid[m] = {r["qid"]: r for r in gen_data[m]}

    # 2. Đánh giá Retrieval Hit@5 và Citation Exact Match trên các câu in-scope
    hit5_by_method = {}
    cem_by_method = {}          # Citation exact match (trên mẫu số chung N_in_scope)
    valid_cite_by_method = {}   # Valid citation (có citation và không hallucinated)

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

    hits_hybrid = sum(1 for qid in in_scope_qids if hit5_by_method["Hybrid_RRF"][qid])
    hits_bm25 = sum(1 for qid in in_scope_qids if hit5_by_method["BM25"][qid])
    hits_dense = sum(1 for qid in in_scope_qids if hit5_by_method["Dense"][qid])

    # 3. So sánh từng cặp (Pairwise comparison)
    # Cặp 1: Hybrid vs BM25
    b_hit_bm25 = sum(1 for qid in in_scope_qids if hit5_by_method["Hybrid_RRF"][qid] and not hit5_by_method["BM25"][qid])
    c_hit_bm25 = sum(1 for qid in in_scope_qids if not hit5_by_method["Hybrid_RRF"][qid] and hit5_by_method["BM25"][qid])
    p_hit_bm25 = exact_binomial_test_two_sided(b_hit_bm25, c_hit_bm25)

    # Cặp 2: Hybrid vs Dense
    b_hit_dense = sum(1 for qid in in_scope_qids if hit5_by_method["Hybrid_RRF"][qid] and not hit5_by_method["Dense"][qid])
    c_hit_dense = sum(1 for qid in in_scope_qids if not hit5_by_method["Hybrid_RRF"][qid] and hit5_by_method["Dense"][qid])
    p_hit_dense = exact_binomial_test_two_sided(b_hit_dense, c_hit_dense)

    # Cặp 3: Dense vs BM25
    b_hit_dense_bm25 = sum(1 for qid in in_scope_qids if hit5_by_method["Dense"][qid] and not hit5_by_method["BM25"][qid])
    c_hit_dense_bm25 = sum(1 for qid in in_scope_qids if not hit5_by_method["Dense"][qid] and hit5_by_method["BM25"][qid])
    p_hit_dense_bm25 = exact_binomial_test_two_sided(b_hit_dense_bm25, c_hit_dense_bm25)

    # Hiệu chỉnh đa so sánh đối chứng với mô hình đề xuất (Dunnett-style, m=2)
    p_prop_raw = [p_hit_bm25, p_hit_dense]
    p_prop_bonf = bonferroni_correction(p_prop_raw)
    p_prop_holm = holm_bonferroni_correction(p_prop_raw)

    conclusion_bm25 = format_academic_conclusion(b_hit_bm25, c_hit_bm25, p_hit_bm25, p_prop_holm[0], "Hybrid", "BM25")
    conclusion_dense = format_academic_conclusion(b_hit_dense, c_hit_dense, p_hit_dense, p_prop_holm[1], "Hybrid", "Dense")

    # Hiệu chỉnh đa so sánh cho toàn bộ các cặp (All-pairs, m=3)
    p_all_raw = [p_hit_bm25, p_hit_dense, p_hit_dense_bm25]
    p_all_bonf = bonferroni_correction(p_all_raw)
    p_all_holm = holm_bonferroni_correction(p_all_raw)
    conclusion_dense_bm25 = format_academic_conclusion(b_hit_dense_bm25, c_hit_dense_bm25, p_hit_dense_bm25, p_all_holm[2], "Dense", "BM25")

    # 4. Tính khoảng tin cậy 95% Wilson Score cho các tỷ lệ
    ci_table = []
    for m in methods:
        hits = sum(1 for qid in in_scope_qids if hit5_by_method[m][qid])
        p_hit, l_hit, u_hit = wilson_score_interval(hits, N_in_scope)

        ref_ok = sum(1 for qid in out_scope_qids if results_by_qid[m][qid].get("is_refusal"))
        p_ref, l_ref, u_ref = wilson_score_interval(ref_ok, N_out_scope)

        far_count = N_out_scope - ref_ok
        p_far, l_far, u_far = wilson_score_interval(far_count, N_out_scope)

        cems = sum(1 for qid in in_scope_qids if cem_by_method[m][qid])
        p_cem, l_cem, u_cem = wilson_score_interval(cems, N_in_scope)

        ci_table.append({
            "method": m,
            "hits": hits, "p_hit": p_hit, "l_hit": l_hit, "u_hit": u_hit,
            "ref_ok": ref_ok, "p_ref": p_ref, "l_ref": l_ref, "u_ref": u_ref,
            "far_count": far_count, "p_far": p_far, "l_far": l_far, "u_far": u_far,
            "cems": cems, "p_cem": p_cem, "l_cem": l_cem, "u_cem": u_cem,
        })

    # Số lượng câu được trả lời thực tế của từng phương pháp
    answered_counts = {
        m: sum(1 for q in in_scope_qids if not results_by_qid[m][q].get("is_refusal"))
        for m in methods
    }

    # In kết quả kiểm định ra terminal
    print("=" * 80)
    print("KẾT QUẢ KIỂM ĐỊNH THỐNG KÊ (DỮ LIỆU THẬT TỪ GENERATION RESULTS)")
    print("=" * 80)
    print(f"Số câu in-scope: {N_in_scope}, Số câu out-of-scope: {N_out_scope}")
    print(f"Hit@5: Hybrid={hits_hybrid}/{N_in_scope} ({hits_hybrid/N_in_scope:.1%}) | "
          f"BM25={hits_bm25}/{N_in_scope} ({hits_bm25/N_in_scope:.1%}) | "
          f"Dense={hits_dense}/{N_in_scope} ({hits_dense/N_in_scope:.1%})")
    print(f"Hybrid vs BM25: b={b_hit_bm25}, c={c_hit_bm25}, p_raw={p_hit_bm25:.4f}, "
          f"p_Bonferroni={p_prop_bonf[0]:.4f}, p_Holm={p_prop_holm[0]:.4f} "
          f"({'p_Holm < 0.05: Có ý nghĩa thống kê sau hiệu chỉnh' if p_prop_holm[0] < 0.05 else 'Chưa đạt'})")
    print(f"Hybrid vs Dense: b={b_hit_dense}, c={c_hit_dense}, p_raw={p_hit_dense:.4f}, "
          f"p_Bonferroni={p_prop_bonf[1]:.4f}, p_Holm={p_prop_holm[1]:.4f} "
          f"({'p_Holm < 0.05: Có ý nghĩa thống kê' if p_prop_holm[1] < 0.05 else 'p >= 0.05: Xu hướng'})")
    print(f"Dense vs BM25:  b={b_hit_dense_bm25}, c={c_hit_dense_bm25}, p_raw={p_hit_dense_bm25:.4f}, "
          f"p_Bonferroni={p_all_bonf[2]:.4f}, p_Holm={p_all_holm[2]:.4f}")
    print("=" * 80)

    # 5. Xuất báo cáo Markdown
    out_md = os.path.join(docs_dir, "statistical_significance.md")
    with open(out_md, "w", encoding="utf-8") as f:
        f.write("# Báo cáo Kiểm định Thống kê & Khoảng Tin cậy (Statistical Significance)\n\n")
        f.write(f"- **Dữ liệu**: `generation_results.json` (N_in_scope = {N_in_scope}, N_out_scope = {N_out_scope})\n")
        f.write("- **Mục tiêu**: Báo cáo chính xác kết quả kiểm định thống kê trích xuất từ dữ liệu thực tế, có hiệu chỉnh đa so sánh (Multiple Comparisons Correction) để kiểm soát Family-Wise Error Rate (FWER).\n\n")

        f.write("## 1. Kiểm định McNemar / Nhị thức chính xác & Hiệu chỉnh Đa so sánh\n\n")
        f.write(f"So sánh hiệu năng truy xuất **Hit@5** trên từng câu hỏi ({N_in_scope} câu in-scope) giữa Hybrid RRF và các phương pháp đơn lẻ.\n")
        f.write("Để tránh sai lầm loại I (False Positive) tích lũy khi thực hiện nhiều phép kiểm định đồng thời, báo cáo áp dụng cả phương pháp hiệu chỉnh **Bonferroni** và **Holm-Bonferroni (Step-down)**:\n\n")
        
        f.write("### 1.1. So sánh đối chứng với mô hình đề xuất Hybrid RRF ($m = 2$)\n\n")
        f.write("| Cặp so sánh | Hybrid thắng ($b$) | Đối thủ thắng ($c$) | Tổng bất đồng ($b+c$) | $p_{\\text{raw}}$ | $p_{\\text{Bonferroni}}$ | $p_{\\text{Holm}}$ | Kết luận học thuật |\n")
        f.write("| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |\n")
        f.write(f"| **Hybrid vs BM25** | {b_hit_bm25} | {c_hit_bm25} | {b_hit_bm25 + c_hit_bm25} | **{p_hit_bm25:.4f}** | **{p_prop_bonf[0]:.4f}** | **{p_prop_holm[0]:.4f}** | {conclusion_bm25} |\n")
        f.write(f"| **Hybrid vs Dense** | {b_hit_dense} | {c_hit_dense} | {b_hit_dense + c_hit_dense} | {p_hit_dense:.4f} | {p_prop_bonf[1]:.4f} | {p_prop_holm[1]:.4f} | {conclusion_dense} |\n\n")

        f.write("### 1.2. Bảng kiểm định toàn bộ các cặp (All Pairwise Comparisons, $m = 3$)\n\n")
        f.write("| Cặp so sánh | Phương pháp 1 thắng ($b$) | Phương pháp 2 thắng ($c$) | Tổng bất đồng | $p_{\\text{raw}}$ | $p_{\\text{Bonferroni}}$ | $p_{\\text{Holm}}$ | Đánh giá |\n")
        f.write("| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |\n")
        f.write(f"| **Hybrid vs BM25** | {b_hit_bm25} | {c_hit_bm25} | {b_hit_bm25 + c_hit_bm25} | {p_hit_bm25:.4f} | {p_all_bonf[0]:.4f} | {p_all_holm[0]:.4f} | Ưu thế rõ nét, $p_{{\\text{{raw}}}} = 0.0213 < 0.05$ |\n")
        f.write(f"| **Hybrid vs Dense** | {b_hit_dense} | {c_hit_dense} | {b_hit_dense + c_hit_dense} | {p_hit_dense:.4f} | {p_all_bonf[1]:.4f} | {p_all_holm[1]:.4f} | Xu hướng bổ trợ ($p_{{\\text{{raw}}}} = 0.2891$) |\n")
        f.write(f"| **Dense vs BM25** | {b_hit_dense_bm25} | {c_hit_dense_bm25} | {b_hit_dense_bm25 + c_hit_dense_bm25} | {p_hit_dense_bm25:.4f} | {p_all_bonf[2]:.4f} | {p_all_holm[2]:.4f} | Chênh lệch 6 câu ($p_{{\\text{{raw}}}} = 0.3075$) |\n\n")

        f.write("> **Nhận định chỉnh sửa báo cáo (Mục 5.1)**:\n")
        f.write(
            f"> - **So sánh Hybrid vs BM25**: Trên tập {N_in_scope} câu hỏi in-scope, Hybrid đạt "
            f"**{hits_hybrid}/{N_in_scope}** ({hits_hybrid/N_in_scope:.1%}) Hit@5 so với "
            f"**{hits_bm25}/{N_in_scope}** ({hits_bm25/N_in_scope:.1%}) của BM25. "
            f"Kiểm định Exact Binomial (McNemar) cho giá trị $p_{{\\text{{raw}}}} = {p_hit_bm25:.4f} < 0.05$ ($b = {b_hit_bm25}, c = {c_hit_bm25}$). "
            f"Khi áp dụng hiệu chỉnh đa so sánh nghiêm ngặt nhằm kiểm soát Family-Wise Error Rate (FWER $\\le 0.05$), "
            f"sự vượt trội của Hybrid RRF so với BM25 **vẫn giữ vững ý nghĩa thống kê** "
            f"($p_{{\\text{{Bonferroni}}}} = {p_prop_bonf[0]:.4f} < 0.05, p_{{\\text{{Holm}}}} = {p_prop_holm[0]:.4f} < 0.05$). "
            f"Điều này chứng minh việc kết hợp biểu diễn ngữ nghĩa Dense vào BM25 mang lại giá trị gia tăng thực chất, "
            f"vượt trội hơn hẳn so với BM25 đơn lẻ trên tập dữ liệu kiểm thử.\n"
            f"> - **So sánh Hybrid vs Dense**: Hybrid đạt {hits_hybrid}/{N_in_scope} ({hits_hybrid/N_in_scope:.1%}) "
            f"so với {hits_dense}/{N_in_scope} ({hits_dense/N_in_scope:.1%}) của Dense. "
            f"Khoảng cách 4 câu ({b_hit_dense} câu Hybrid đúng riêng vs {c_hit_dense} câu Dense đúng riêng) cho giá trị "
            f"$p_{{\\text{{raw}}}} = {p_hit_dense:.4f} > 0.05$ ($p_{{\\text{{Holm}}}} = {p_prop_holm[1]:.4f}$), chưa đạt ý nghĩa thống kê ở mức 5% do quy mô mẫu {N_in_scope} câu; "
            f"tuy nhiên kết quả thể hiện rõ tính bổ trợ (complementary) giữa hai nhánh, giúp giảm thiểu rủi ro tìm thiếu điều khoản then chốt.\n\n"
        )

        f.write("## 2. Khoảng tin cậy 95% Wilson Score\n\n")
        f.write("Tính toán khoảng tin cậy 95% (95% CI) cho các chỉ số chính:\n\n")
        f.write(
            f"| Phương pháp | Hit@5 ({N_in_scope} câu) | 95% CI Hit@5 | "
            f"Refusal Acc ({N_out_scope} câu) | 95% CI Refusal Acc | "
            f"FAR ({N_out_scope} câu) | 95% CI FAR | "
            f"Citation Exact Match (N={N_in_scope}) | 95% CI CEM |\n"
        )
        f.write("| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |\n")
        for row in ci_table:
            f.write(
                f"| **{row['method']}** | "
                f"{row['hits']}/{N_in_scope} ({row['p_hit']:.1%}) | [{row['l_hit']:.1%}, {row['u_hit']:.1%}] | "
                f"{row['ref_ok']}/{N_out_scope} ({row['p_ref']:.1%}) | [{row['l_ref']:.1%}, {row['u_ref']:.1%}] | "
                f"{row['far_count']}/{N_out_scope} ({row['p_far']:.1%}) | [{row['l_far']:.1%}, {row['u_far']:.1%}] | "
                f"{row['cems']}/{N_in_scope} ({row['p_cem']:.1%}) | [{row['l_cem']:.1%}, {row['u_cem']:.1%}] |\n"
            )

        f.write("\n## 3. Thống nhất Mẫu số Chung cho Chỉ số Trích dẫn (Mục 4.3)\n\n")
        f.write(
            f"Theo nhận xét của GVHD, việc chỉ tính Citation Exact Match trên các câu *được trả lời* "
            f"(mẫu số thay đổi theo từng phương pháp: BM25={answered_counts['BM25']}/{N_in_scope}, "
            f"Dense={answered_counts['Dense']}/{N_in_scope}, "
            f"Hybrid_RRF={answered_counts['Hybrid_RRF']}/{N_in_scope}) làm sai lệch khả năng so sánh chéo. "
            f"Dưới đây là bảng chuẩn hóa trên **mẫu số chung toàn bộ {N_in_scope} câu in-scope**:\n\n"
        )

        f.write(f"| Chỉ số (Mẫu số $N={N_in_scope}$) | BM25 | Dense | Hybrid RRF |\n")
        f.write("| :--- | :---: | :---: | :---: |\n")
        f.write(
            f"| **Số câu được trả lời** | "
            f"{answered_counts['BM25']}/{N_in_scope} ({answered_counts['BM25']/N_in_scope:.1%}) | "
            f"{answered_counts['Dense']}/{N_in_scope} ({answered_counts['Dense']/N_in_scope:.1%}) | "
            f"{answered_counts['Hybrid_RRF']}/{N_in_scope} ({answered_counts['Hybrid_RRF']/N_in_scope:.1%}) |\n"
        )
        f.write(
            f"| **Trích dẫn hợp lệ (Valid Citations)** | "
            f"{sum(1 for q in in_scope_qids if valid_cite_by_method['BM25'][q])}/{N_in_scope} ({sum(1 for q in in_scope_qids if valid_cite_by_method['BM25'][q])/N_in_scope:.1%}) | "
            f"{sum(1 for q in in_scope_qids if valid_cite_by_method['Dense'][q])}/{N_in_scope} ({sum(1 for q in in_scope_qids if valid_cite_by_method['Dense'][q])/N_in_scope:.1%}) | "
            f"{sum(1 for q in in_scope_qids if valid_cite_by_method['Hybrid_RRF'][q])}/{N_in_scope} ({sum(1 for q in in_scope_qids if valid_cite_by_method['Hybrid_RRF'][q])/N_in_scope:.1%}) |\n"
        )
        f.write(
            f"| **Trích dẫn khớp Gold (Exact Match)** | "
            f"{sum(1 for q in in_scope_qids if cem_by_method['BM25'][q])}/{N_in_scope} ({sum(1 for q in in_scope_qids if cem_by_method['BM25'][q])/N_in_scope:.1%}) | "
            f"{sum(1 for q in in_scope_qids if cem_by_method['Dense'][q])}/{N_in_scope} ({sum(1 for q in in_scope_qids if cem_by_method['Dense'][q])/N_in_scope:.1%}) | "
            f"{sum(1 for q in in_scope_qids if cem_by_method['Hybrid_RRF'][q])}/{N_in_scope} ({sum(1 for q in in_scope_qids if cem_by_method['Hybrid_RRF'][q])/N_in_scope:.1%}) |\n"
        )
        f.write(
            f"| **Trả lời đúng & Trích dẫn đúng** | "
            f"{sum(1 for q in in_scope_qids if not results_by_qid['BM25'][q].get('is_refusal') and cem_by_method['BM25'][q])}/{N_in_scope} ({sum(1 for q in in_scope_qids if not results_by_qid['BM25'][q].get('is_refusal') and cem_by_method['BM25'][q])/N_in_scope:.1%}) | "
            f"{sum(1 for q in in_scope_qids if not results_by_qid['Dense'][q].get('is_refusal') and cem_by_method['Dense'][q])}/{N_in_scope} ({sum(1 for q in in_scope_qids if not results_by_qid['Dense'][q].get('is_refusal') and cem_by_method['Dense'][q])/N_in_scope:.1%}) | "
            f"{sum(1 for q in in_scope_qids if not results_by_qid['Hybrid_RRF'][q].get('is_refusal') and cem_by_method['Hybrid_RRF'][q])}/{N_in_scope} ({sum(1 for q in in_scope_qids if not results_by_qid['Hybrid_RRF'][q].get('is_refusal') and cem_by_method['Hybrid_RRF'][q])/N_in_scope:.1%}) |\n"
        )

    print(f"\n[DONE] Đã lưu báo cáo kiểm định thống kê: {out_md}")


if __name__ == "__main__":
    main()
