"""
evaluate_generation.py
Đánh giá hiệu suất Generation trên dev set / test set.

Các chỉ số đo lường:
  - Refusal Accuracy: Tỷ lệ câu out_of_scope bị từ chối đúng (dùng phân loại có cấu trúc / judge).
  - False Refusal Rate: Tỷ lệ câu in_scope bị từ chối sai.
  - Citation Accuracy: Tỷ lệ câu có citation vừa có thật vừa đúng nội dung (khớp gold_id và không bị hallucinate).
  - Citation Precision: Tỷ lệ citation đúng trên tổng số citation mà LLM sinh ra.
  - Citation Validity (Cú pháp): Tỷ lệ câu citation hợp lệ trong context (sau khi verifier chuẩn hóa mã con __a về mã cha).
  - Claim Support Rate (Ngữ nghĩa): Tỷ lệ các luận điểm có trích dẫn được nội dung điều luật bảo chứng thực sự.
  - Overall Claim Support Rate: Tỷ lệ toàn bộ luận điểm trong câu trả lời được điều luật bảo chứng.
  - Fully Supported Answer Rate: Tỷ lệ câu trả lời có 100% luận điểm được bảo chứng.
"""

import os
import sys
import json
import time

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

sys.path.insert(0, os.path.dirname(__file__))

from retriever import LegalRetriever
from generator import (
    LegalGenerator,
    classify_refusal,
    judge_refusal,
    extract_claims,
    verify_claim_support,
    evaluate_answer_claim_support,
)
from rag_pipeline import execute_rag_pipeline



def run_evaluation(retriever, generator, eval_set, top_k=5, use_judge=False):
    """Chạy pipeline RAG trên toàn bộ eval set và thu thập kết quả."""

    results = []

    for i, item in enumerate(eval_set):
        qid = item["id"]
        query = item["question"]
        category = item["category"]
        gold_ids = item.get("gold_provision_ids", [])
        is_out_of_scope = (category == "out_of_scope")

        print(f"  [{i+1}/{len(eval_set)}] {qid}: {query[:60]}...")

        # Thực thi qua execute_rag_pipeline đồng bộ với app.py
        res = execute_rag_pipeline(
            query=query,
            retriever=retriever,
            generator=generator,
            top_k=top_k,
        )

        # Thu thập kết quả
        retrieved_ids = [r["provision_id"] for r in res.get("chunks", [])]
        context_map = {
            r["provision_id"]: r.get("content", {}).get("noi_dung", "")
            for r in res.get("chunks", [])
        }

        # Phân loại từ chối có cấu trúc / Judge thay vì so khớp chuỗi y hệt
        ref_info = classify_refusal(
            res["answer"],
            query=query,
            use_judge=use_judge,
            client=getattr(generator, "client", None),
            model_name=getattr(generator, "model_name", "gemini-2.5-flash")
        )
        is_ref = ref_info["is_refusal"]

        results.append({
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
            "is_refusal": is_ref,
            "refusal_info": ref_info,
            "api_error": res.get("api_error", False),
            "error": res.get("error"),
            "retrieval_time": res.get("retrieval_time", 0.0),
            "generation_time": res.get("generation_time", 0.0),
        })

        # Trạng thái nhanh
        status = "REFUSE" if is_ref else "ANSWER"
        halluc = f" [HALLUC: {res['hallucinated_ids']}]" if res["hallucinated_ids"] else ""
        norm_tag = f" [NORMALIZED: {res.get('normalized_ids')}]" if res.get("normalized_ids") else ""
        print(f"         → {status}{halluc}{norm_tag}")

        # Chờ giữa các request để tránh rate limit (5 req/min free tier)
        if i < len(eval_set) - 1:
            time.sleep(13)

    return results


def compute_metrics(results, corpus_dict=None, use_judge=False, client=None):
    """Tính toán các chỉ số đánh giá Generation (Refusal có cấu trúc, Citation cú pháp, và Claim Support)."""

    # Phân loại câu hỏi
    # Loại các câu bị lỗi API khỏi việc tính metrics
    valid_results = [
        r for r in results
        if not r.get("api_error", False)
    ]

    # Đồng bộ / chuẩn hóa trạng thái từ chối bằng bộ phân loại có cấu trúc
    for r in valid_results:
        if "refusal_info" not in r:
            ref_info = classify_refusal(
                r.get("answer", ""),
                query=r.get("question"),
                use_judge=use_judge,
                client=client
            )
            r["is_refusal"] = ref_info["is_refusal"]
            r["refusal_info"] = ref_info

    in_scope = [
        r for r in valid_results
        if not r["is_out_of_scope"]
    ]

    out_scope = [
        r for r in valid_results
        if r["is_out_of_scope"]
    ]

    # =================================================================
    # 1. REFUSAL METRICS (Phân loại có cấu trúc / Judge)
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
    # 2. CITATION METRICS (Cú pháp - Kiểm tra ID trong context)
    # =================================================================

    answered_in_scope = [r for r in in_scope if not r["is_refusal"]]

    # Citation Validity (Chính xác): Tỷ lệ câu có citation hoàn toàn hợp lệ
    # QUY TẮC: Bất kỳ câu nào có mã hallucinated HOẶC mã con bị rút gọn (ví dụ __a về __K)
    # thì ĐỀU BỊ TÍNH LÀ KHÔNG HỢP LỆ (vì tự chế ra mã con ngoài context được cấp).
    if answered_in_scope:
        strict_valid = sum(
            1 for r in answered_in_scope
            if not r.get("hallucinated_ids") and not r.get("normalized_ids")
        )
        citation_validity = strict_valid / len(answered_in_scope)

        # Relaxed Citation Validity: Tỷ lệ câu không có mã bịa hoàn toàn (châm chước mã rút về cha)
        relaxed_valid = sum(
            1 for r in answered_in_scope
            if not r.get("hallucinated_ids")
        )
        citation_validity_relaxed = relaxed_valid / len(answered_in_scope)

        # Số lượng và tỷ lệ câu có mã bị rút gọn
        normalized_count = sum(
            1 for r in answered_in_scope
            if r.get("normalized_ids")
        )
        citation_normalized_rate = normalized_count / len(answered_in_scope)
    else:
        citation_validity = None
        citation_validity_relaxed = None
        citation_normalized_rate = None
        normalized_count = 0

    # Citation Accuracy: Tỷ lệ câu có citation vừa có thật (không hallucinate, không bị rút mã) vừa đúng nội dung (khớp gold_id)
    # Citation Precision: Tỷ lệ citation đúng trên tổng số citation sinh ra (|Cits ∩ Golds| / |Cits|)
    if answered_in_scope:
        accurate_count = 0
        precisions = []

        for r in answered_in_scope:
            cits = set(r.get("citations", []))
            golds = set(r.get("gold_ids", []))
            hallucs = r.get("hallucinated_ids", [])
            norms = r.get("normalized_ids", [])

            # Citation Accuracy (Strict): vừa có thật (không bịa đặt, không bị rút mã) vừa đúng nội dung
            if cits and golds and (cits & golds) and not hallucs and not norms:
                accurate_count += 1

            # Citation Precision cho câu này
            if cits:
                prec = len(cits & golds) / len(cits)
                precisions.append(prec)
            else:
                precisions.append(0.0)

        citation_accuracy = accurate_count / len(answered_in_scope)
        citation_precision = sum(precisions) / len(precisions) if precisions else 0.0
    else:
        citation_accuracy = None
        citation_precision = None

    # =================================================================
    # 3. CLAIM SUPPORT METRICS (Ngữ nghĩa - Căn cứ bảo chứng Luận điểm)
    # =================================================================
    # Khắc phục hạn chế của Citation Validity (chỉ kiểm tra cú pháp ID tồn tại sau khi rút gọn __a):
    # Trích xuất từng luận điểm (claim) và kiểm chứng xem nội dung điều luật có
    # thực sự bảo chứng cho luận điểm đó hay không.
    for r in answered_in_scope:
        lookup = r.get("context_map", {})

        cs_res = evaluate_answer_claim_support(
            answer=r.get("answer", ""),
            context_lookup=lookup,
            judge_client=client if use_judge else None
        )

        r["claim_support"] = cs_res

    total_claims = sum(r.get("claim_support", {}).get("total_claims", 0) for r in answered_in_scope)
    cited_claims = sum(r.get("claim_support", {}).get("cited_claims", 0) for r in answered_in_scope)
    supported_claims = sum(r.get("claim_support", {}).get("supported_claims", 0) for r in answered_in_scope)
    unsupported_claims = sum(r.get("claim_support", {}).get("unsupported_claims", 0) for r in answered_in_scope)

    claim_support_rate = (supported_claims / cited_claims) if cited_claims > 0 else (1.0 if not answered_in_scope else 0.0)
    overall_claim_support_rate = (supported_claims / total_claims) if total_claims > 0 else 0.0
    fully_supported_count = sum(1 for r in answered_in_scope if r.get("claim_support", {}).get("is_fully_supported", False))
    fully_supported_rate = (fully_supported_count / len(answered_in_scope)) if answered_in_scope else None

    # =================================================================
    # 4. LATENCY
    # =================================================================

    import numpy as np
    gen_times = [
        r["generation_time"]
        for r in valid_results
    ]
    api_error_count = sum(
        1 for r in results
        if r.get("api_error", False)
    )
    metrics = {
        "total_questions": len(results),
        "valid_questions": len(valid_results),
        "api_error_count": api_error_count,

        "in_scope_count": len(in_scope),
        "out_scope_count": len(out_scope),
        "answered_in_scope_count": len(answered_in_scope),

        "refusal_accuracy": refusal_accuracy,
        "false_refusal_rate": false_refusal_rate,
        "false_acceptance_rate": false_acceptance_rate,

        "citation_validity": citation_validity,
        "citation_validity_strict": citation_validity,
        "citation_validity_relaxed": citation_validity_relaxed,
        "citation_normalized_rate": citation_normalized_rate,
        "normalized_count": normalized_count,
        "citation_accuracy": citation_accuracy,
        "citation_precision": citation_precision,

        "total_claims": total_claims,
        "cited_claims": cited_claims,
        "supported_claims": supported_claims,
        "unsupported_claims": unsupported_claims,
        "claim_support_rate": claim_support_rate,
        "overall_claim_support_rate": overall_claim_support_rate,
        "fully_supported_rate": fully_supported_rate,

        "generation_latency_p50_s": float(np.percentile(gen_times, 50)) if gen_times else 0.0,
        "generation_latency_p95_s": float(np.percentile(gen_times, 95)) if gen_times else 0.0,
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
    print(f"  - API lỗi:              {metrics['api_error_count']}")

    print(f"\n--- Refusal Metrics (Phân loại có cấu trúc / Judge) ---")
    if metrics["refusal_accuracy"] is not None:
        print(f"  Refusal Accuracy:       {metrics['refusal_accuracy']:.2%}")
    if metrics["false_refusal_rate"] is not None:
        print(f"  False Refusal Rate:     {metrics['false_refusal_rate']:.2%}")
    if metrics["false_acceptance_rate"] is not None:
        print(f"  False Acceptance Rate:  {metrics['false_acceptance_rate']:.2%}")

    print(f"\n--- Citation Metrics (Cú pháp - Kiểm tra ID chính xác trong Context) ---")
    if metrics.get("citation_validity") is not None:
        print(f"  Citation Validity (Chính xác):  {metrics['citation_validity']:.2%}  (Phạt cả mã bịa và mã tự chế bị rút)")
    if metrics.get("citation_validity_relaxed") is not None:
        print(f"  Citation Validity (Nới lỏng):   {metrics['citation_validity_relaxed']:.2%}  (Châm chước mã rút về cha)")
    if metrics.get("citation_normalized_rate") is not None:
        print(f"  Tỷ lệ câu bị rút mã con:       {metrics['citation_normalized_rate']:.2%}  ({metrics.get('normalized_count', 0)}/{metrics['answered_in_scope_count']} câu)")
    if metrics.get("citation_accuracy") is not None:
        print(f"  Citation Accuracy:              {metrics['citation_accuracy']:.2%}")
    if metrics.get("citation_precision") is not None:
        print(f"  Citation Precision:             {metrics['citation_precision']:.2%}")

    print(f"\n--- Claim Support Metrics (Ngữ nghĩa - Căn cứ bảo chứng Luận điểm) ---")
    print(f"  Tổng số Luận điểm (Claims):      {metrics.get('total_claims', 0)}")
    print(f"  Luận điểm có trích dẫn:          {metrics.get('cited_claims', 0)}")
    print(f"  Luận điểm được bảo chứng:        {metrics.get('supported_claims', 0)}")
    if metrics.get("claim_support_rate") is not None:
        print(f"  Claim Support Rate:              {metrics['claim_support_rate']:.2%} (trên các claim có citation)")
    if metrics.get("overall_claim_support_rate") is not None:
        print(f"  Overall Support Rate:            {metrics['overall_claim_support_rate']:.2%} (trên toàn bộ claim)")
    if metrics.get("fully_supported_rate") is not None:
        print(f"  Fully Supported Answer Rate:     {metrics['fully_supported_rate']:.2%}")

    print(f"\n--- Latency ---")
    print(f"  Generation p50:         {metrics['generation_latency_p50_s']:.2f}s")
    print(f"  Generation p95:         {metrics['generation_latency_p95_s']:.2f}s")

    # Chi tiết các câu bị lỗi
    print(f"\n--- Chi tiết False Refusal (câu in-scope bị từ chối sai) ---")
    false_refs = [
        r for r in results
        if not r.get("api_error", False)
        and not r["is_out_of_scope"]
        and r["is_refusal"]
    ]
    if false_refs:
        for r in false_refs:
            print(f"  ✗ [{r['qid']}] {r['question'][:60]}")
            print(f"      Gold: {r['gold_ids'][:3]}")
    else:
        print("  (Không có)")

    print(f"\n--- Chi tiết False Acceptance (câu out-of-scope bị trả lời sai) ---")
    false_accs = [
        r for r in results
        if not r.get("api_error", False)
        and r["is_out_of_scope"]
        and not r["is_refusal"]
    ]
    if false_accs:
        for r in false_accs:
            print(f"  ✗ [{r['qid']}] {r['question'][:60]}")
            print(f"      Answer: {r['answer'][:80]}...")
    else:
        print("  (Không có)")

    print(f"\n--- Chi tiết Hallucination ---")
    halluc_cases = [r for r in results if r.get("hallucinated_ids")]
    if halluc_cases:
        for r in halluc_cases:
            print(f"  ✗ [{r['qid']}] {r['question'][:60]}")
            print(f"      Hallucinated: {r['hallucinated_ids']}")
    else:
        print("  (Không có)")

    print(f"\n--- Chi tiết Normalized Citations (mã con tự chế bị rút về cha - tính KHÔNG hợp lệ) ---")
    norm_cases = [r for r in results if r.get("normalized_ids")]
    if norm_cases:
        for r in norm_cases:
            print(f"  ⚠ [{r['qid']}] {r['question'][:60]}")
            print(f"      Mã tự chế bị rút: {r['normalized_ids']}")
            print(f"      Citations sau rút: {r.get('citations')}")
    else:
        print("  (Không có)")

    print(f"\n--- Chi tiết Luận điểm không được bảo chứng (Unsupported Claims) ---")
    unsupp_found = False
    for r in results:
        cs = r.get("claim_support", {})
        bad_claims = [c for c in cs.get("claims", []) if not c.get("supported") and c.get("has_citation")]
        if bad_claims:
            unsupp_found = True
            print(f"  ✗ [{r['qid']}] {r['question'][:60]}")
            for bc in bad_claims:
                print(f"      - Claim: {bc['text'][:80]}")
                print(f"        Cites: {bc['citations']}")
                print(f"        Lý do: {'; '.join(bc['reasons'])}")
    if not unsupp_found:
        print("  (Không có)")

    print()



def main():
    data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    eval_dir = os.path.join(data_dir, "eval")

    # Load dev set
    dev_set_path = os.path.join(eval_dir, "dev_set_v2.json")
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
