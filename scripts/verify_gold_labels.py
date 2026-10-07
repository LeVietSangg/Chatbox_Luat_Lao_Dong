"""
verify_gold_labels.py
Script kiểm tra tính hợp lệ của tất cả gold_provision_ids:
1. Có tồn tại trong corpus.csv hay không.
2. Trạng thái hiệu lực (con_hieu_luc hay het_hieu_luc/het_hieu_luc_mot_phan).
3. Phân bố văn bản quy phạm pháp luật trong test set.
"""

import os
import sys
import json
import pandas as pd

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    corpus_path = os.path.join(base_dir, "data", "structured", "corpus.csv")
    test_set_path = os.path.join(base_dir, "data", "eval", "dev_set_v2.json")

    if not os.path.exists(corpus_path):
        print(f"Error: Không tìm thấy {corpus_path}")
        return
    if not os.path.exists(test_set_path):
        print(f"Error: Không tìm thấy {test_set_path}")
        return

    df = pd.read_csv(corpus_path)
    corpus_pids = set(df["provision_id"].dropna().unique())
    pid_to_status = dict(zip(df["provision_id"], df["hieu_luc"]))
    pid_to_vanban = dict(zip(df["provision_id"], df["van_ban"]))

    with open(test_set_path, "r", encoding="utf-8") as f:
        test_set = json.load(f)

    print(f"Tổng số câu hỏi trong test set: {len(test_set)}")
    
    missing_golds = []
    expired_golds = []
    vanban_counts = {}
    missing_relaxed_golds = []

    for q in test_set:
        qid = q["id"]
        question = q["question"]
        category = q.get("category", "")
        golds = q.get("gold_provision_ids", [])
        golds_relaxed = q.get("gold_provision_ids_relaxed", [])

        # Kiểm tra gold strict
        for g in golds:
            if g not in corpus_pids:
                missing_golds.append({
                    "qid": qid,
                    "question": question,
                    "category": category,
                    "gold": g
                })
            else:
                status = pid_to_status.get(g)
                vb = pid_to_vanban.get(g)
                vanban_counts[vb] = vanban_counts.get(vb, 0) + 1
                if status != "con_hieu_luc":
                    expired_golds.append({
                        "qid": qid,
                        "question": question,
                        "category": category,
                        "gold": g,
                        "status": status,
                        "van_ban": vb
                    })

        # Kiểm tra gold relaxed
        for g in golds_relaxed:
            if g not in corpus_pids:
                missing_relaxed_golds.append({
                    "qid": qid,
                    "question": question,
                    "gold": g
                })

    print("\n" + "=" * 70)
    print(f"1. CÁC GOLD KHÔNG TỒN TẠI TRONG CORPUS.CSV (Số lượng: {len(missing_golds)}):")
    print("=" * 70)
    for m in missing_golds:
        print(f"  - [{m['qid']}] ({m['category']}): {m['gold']}")
        print(f"    Câu hỏi: {m['question']}")

    print("\n" + "=" * 70)
    print(f"2. CÁC GOLD KHÔNG CÒN HIỆU LỰC (Số lượng: {len(expired_golds)}):")
    print("=" * 70)
    for e in expired_golds:
        print(f"  - [{e['qid']}] ({e['category']}): {e['gold']}")
        print(f"    Trạng thái: {e['status']} | Văn bản: {e['van_ban']}")
        print(f"    Câu hỏi: {e['question']}")

    print("\n" + "=" * 70)
    print(f"3. CÁC GOLD RELAXED KHÔNG TỒN TẠI (Số lượng: {len(missing_relaxed_golds)}):")
    print("=" * 70)
    for m in missing_relaxed_golds:
        print(f"  - [{m['qid']}]: {m['gold']} (Câu hỏi: {m['question']})")

    print("\n" + "=" * 70)
    print("4. PHÂN BỐ CÁC VĂN BẢN TRONG TEST SET:")
    print("=" * 70)
    for vb, cnt in sorted(vanban_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  - {vb}: {cnt} câu ({cnt/85*100:.1f}% trên 85 câu in-scope)")

if __name__ == "__main__":
    main()
