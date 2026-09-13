"""
error_analysis.py
Phân tích lỗi chi tiết trên kết quả thực nghiệm Tuần 6.
Xuất kết quả ra file Markdown để dùng cho báo cáo Tuần 7.
"""
import os
import json

def main():
    eval_dir = os.path.join(os.path.dirname(__file__), "..", "data", "eval")
    gen_path = os.path.join(eval_dir, "week6_generation_results.json")
    ret_path = os.path.join(eval_dir, "week6_retrieval_results.json")

    with open(gen_path, "r", encoding="utf-8") as f:
        gen_data = json.load(f)
    with open(ret_path, "r", encoding="utf-8") as f:
        ret_data = json.load(f)

    report_lines = []
    def p(line=""):
        report_lines.append(line)

    p("# Phân tích lỗi (Error Analysis) - Tuần 7")
    p()

    # =====================================================================
    # TỔNG QUAN
    # =====================================================================
    for method in ["BM25", "Dense", "Hybrid_RRF"]:
        results = gen_data[method]
        in_scope = [r for r in results if not r["is_out_of_scope"]]
        out_scope = [r for r in results if r["is_out_of_scope"]]
        answered = [r for r in in_scope if not r["is_refusal"]]
        false_refs = [r for r in in_scope if r["is_refusal"]]
        false_accs = [r for r in out_scope if not r["is_refusal"]]
        halluc_cases = [r for r in results if r["hallucinated_ids"]]

        # Citation metrics
        no_halluc = sum(1 for r in answered if not r["hallucinated_ids"])
        cv = no_halluc / len(answered) * 100 if answered else 0
        exact = sum(1 for r in answered if r["gold_ids"] and r["citations"] and (set(r["citations"]) & set(r["gold_ids"])))
        cem = exact / len(answered) * 100 if answered else 0

        ra = sum(1 for r in out_scope if r["is_refusal"]) / len(out_scope) * 100 if out_scope else 0
        frr = len(false_refs) / len(in_scope) * 100 if in_scope else 0

        p(f"## Tổng quan: {method}")
        p()
        p(f"| Chỉ số | Giá trị |")
        p(f"|--------|---------|")
        p(f"| Tổng câu hỏi | {len(results)} |")
        p(f"| In-scope | {len(in_scope)} |")
        p(f"| Out-of-scope | {len(out_scope)} |")
        p(f"| Đã trả lời (in-scope) | {len(answered)} |")
        p(f"| False Refusal | {len(false_refs)} ({frr:.2f}%) |")
        p(f"| False Accept | {len(false_accs)} |")
        p(f"| Refusal Accuracy | {ra:.2f}% |")
        p(f"| Citation Validity | {cv:.2f}% |")
        p(f"| Citation Exact Match | {cem:.2f}% |")
        p(f"| Hallucination Cases | {len(halluc_cases)} |")
        p()

    # =====================================================================
    # CHI TIẾT PHÂN TÍCH LỖI CHO HYBRID_RRF (pipeline chính)
    # =====================================================================
    p("---")
    p()
    p("# Chi tiết phân tích lỗi: Hybrid_RRF")
    p()
    hybrid = gen_data["Hybrid_RRF"]
    in_scope = [r for r in hybrid if not r["is_out_of_scope"]]
    out_scope = [r for r in hybrid if r["is_out_of_scope"]]

    # --- 1. FALSE REFUSALS ---
    false_refs = [r for r in in_scope if r["is_refusal"]]
    p("## 1. False Refusals (câu in-scope bị từ chối sai)")
    p()
    p(f"Tổng: **{len(false_refs)}/{len(in_scope)}** câu in-scope bị từ chối sai.")
    p()

    # Phân loại nguyên nhân
    retriever_miss = 0
    retriever_found_but_refused = 0
    api_error = 0

    p("| # | QID | Câu hỏi | Gold ID | Gold có trong Retrieved? | Nguyên nhân |")
    p("|---|-----|---------|---------|--------------------------|-------------|")
    for i, r in enumerate(false_refs, 1):
        gold_in_ret = bool(set(r["gold_ids"]) & set(r["retrieved_ids"]))
        has_api_err = r.get("api_error", False) or bool(r.get("error"))
        
        if has_api_err:
            cause = "API Error"
            api_error += 1
        elif not gold_in_ret:
            cause = "Retriever Miss"
            retriever_miss += 1
        else:
            cause = "LLM Miss (context có nhưng LLM vẫn từ chối)"
            retriever_found_but_refused += 1

        q_short = r["question"][:50].replace("|", "\\|")
        gold_short = ", ".join(r["gold_ids"][:2])
        p(f"| {i} | {r['qid']} | {q_short}... | {gold_short} | {'✓' if gold_in_ret else '✗'} | {cause} |")

    p()
    p(f"**Phân loại nguyên nhân False Refusal:**")
    p(f"- Retriever Miss (không tìm được gold provision): **{retriever_miss}**")
    p(f"- LLM Miss (context đúng nhưng LLM vẫn từ chối): **{retriever_found_but_refused}**")
    p(f"- API Error: **{api_error}**")
    p()

    # --- 2. FALSE ACCEPTS ---
    false_accs = [r for r in out_scope if not r["is_refusal"]]
    p("## 2. False Accepts (câu out-of-scope bị trả lời sai)")
    p()
    if false_accs:
        p(f"Tổng: **{len(false_accs)}/{len(out_scope)}** câu out-of-scope bị trả lời.")
        p()
        for r in false_accs:
            p(f"- **[{r['qid']}]** {r['question']}")
            p(f"  - Answer: {r['answer'][:100]}...")
            p()
    else:
        p("**Không có False Accept nào.** Mọi câu out-of-scope đều bị từ chối đúng. ✓")
        p()

    # --- 3. HALLUCINATIONS ---
    halluc_cases = [r for r in hybrid if r["hallucinated_ids"]]
    p("## 3. Hallucinated Citations")
    p()
    p(f"Tổng: **{len(halluc_cases)}** câu có citation ảo giác.")
    p()

    # Phân loại kiểu hallucination
    sub_id_halluc = 0  # LLM tự sinh ID con (thêm __Da, __Db...)
    multi_id_halluc = 0  # LLM gộp nhiều ID vào 1 ngoặc
    fabricated = 0  # LLM bịa hoàn toàn

    if halluc_cases:
        p("| # | QID | Câu hỏi | Hallucinated IDs | Loại |")
        p("|---|-----|---------|------------------|------|")
        for i, r in enumerate(halluc_cases, 1):
            q_short = r["question"][:45].replace("|", "\\|")
            h_ids = r["hallucinated_ids"]

            types_found = []
            for hid in h_ids:
                if "__D" in hid and any(c.isalpha() for c in hid.split("__")[-1]):
                    types_found.append("Sub-ID")
                    sub_id_halluc += 1
                elif "," in hid:
                    types_found.append("Multi-ID")
                    multi_id_halluc += 1
                else:
                    types_found.append("Fabricated")
                    fabricated += 1

            h_short = str(h_ids[:3])
            type_str = ", ".join(set(types_found))
            p(f"| {i} | {r['qid']} | {q_short}... | {h_short} | {type_str} |")

        p()
        p(f"**Phân loại Hallucination:**")
        p(f"- Sub-ID (LLM tự sinh ID con như `__Da`, `__Db`): **{sub_id_halluc}**")
        p(f"- Multi-ID (LLM gộp nhiều ID vào 1 ngoặc vuông): **{multi_id_halluc}**")
        p(f"- Fabricated (LLM bịa ID hoàn toàn): **{fabricated}**")
        p()
    else:
        p("Không có hallucination.")
        p()

    # --- 4. CITATION MISMATCH ---
    answered = [r for r in in_scope if not r["is_refusal"]]
    no_match = [r for r in answered if r["gold_ids"] and r["citations"] and not (set(r["citations"]) & set(r["gold_ids"]))]
    p("## 4. Citation Mismatch (trả lời nhưng trích dẫn sai provision)")
    p()
    p(f"Tổng: **{len(no_match)}** câu có câu trả lời nhưng citation không khớp gold_provision_ids.")
    p()
    if no_match:
        p("| # | QID | Câu hỏi | Gold IDs | LLM Citations |")
        p("|---|-----|---------|----------|---------------|")
        for i, r in enumerate(no_match, 1):
            q_short = r["question"][:45].replace("|", "\\|")
            g = ", ".join(r["gold_ids"][:2])
            c = ", ".join(r["citations"][:2])
            p(f"| {i} | {r['qid']} | {q_short}... | {g} | {c} |")
        p()

    # --- 5. SO SÁNH CHÉO 3 PIPELINE ---
    p("---")
    p()
    p("# So sánh chéo 3 Pipeline")
    p()

    # Tìm câu mà chỉ 1 method trả lời đúng
    all_qids = [r["qid"] for r in hybrid]
    
    p("## Câu hỏi chỉ một pipeline trả lời đúng (unique wins)")
    p()
    
    method_answers = {}
    for method in ["BM25", "Dense", "Hybrid_RRF"]:
        method_answers[method] = {}
        for r in gen_data[method]:
            method_answers[method][r["qid"]] = r

    unique_wins = {"BM25": [], "Dense": [], "Hybrid_RRF": []}
    for qid in all_qids:
        for method in ["BM25", "Dense", "Hybrid_RRF"]:
            r = method_answers[method][qid]
            if r["is_out_of_scope"]:
                continue
            # Method này trả lời đúng (có citation khớp gold)
            has_match = bool(r["gold_ids"] and r["citations"] and (set(r["citations"]) & set(r["gold_ids"])))
            if not has_match:
                continue
            # Các method khác trả lời sai
            others_wrong = True
            for other in ["BM25", "Dense", "Hybrid_RRF"]:
                if other == method:
                    continue
                ro = method_answers[other][qid]
                other_match = bool(ro["gold_ids"] and ro["citations"] and (set(ro["citations"]) & set(ro["gold_ids"])))
                if other_match:
                    others_wrong = False
                    break
            if others_wrong:
                unique_wins[method].append(qid)

    for method in ["BM25", "Dense", "Hybrid_RRF"]:
        p(f"- **{method}** unique wins: **{len(unique_wins[method])}** câu")
        if unique_wins[method]:
            for qid in unique_wins[method][:5]:
                r = method_answers[method][qid]
                p(f"  - [{qid}] {r['question'][:60]}")
    p()

    # --- 6. RETRIEVAL METRICS COMPARISON TABLE ---
    p("---")
    p()
    p("# Bảng tổng hợp kết quả Retrieval")
    p()
    p("| Metric | BM25 | Dense | Hybrid RRF |")
    p("|--------|------|-------|------------|")
    for metric in ["MRR@10", "Recall@1", "Recall@3", "Recall@5"]:
        bm = ret_data["BM25"][metric]
        de = ret_data["Dense"][metric]
        hy = ret_data["Hybrid_RRF"][metric]
        p(f"| {metric} | {bm:.4f} | {de:.4f} | **{hy:.4f}** |")
    p()

    # Lưu báo cáo
    output_path = os.path.join(eval_dir, "error_analysis.md")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))
    print(f"Đã lưu Error Analysis: {output_path}")

    # In ra console
    print("\n".join(report_lines))

if __name__ == "__main__":
    main()
