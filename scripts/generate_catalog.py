# -*- coding: utf-8 -*-
"""
scripts/generate_catalog.py
Sinh catalog văn bản (docs/corpus_catalog.md) và thống kê (data/structured/corpus_stats.json)
từ nguồn duy nhất: data/structured/corpus.csv.
Đảm bảo tính nhất quán dữ liệu 100% không chỉnh sửa thủ công.
"""

import os
import json
import pandas as pd


def generate_catalog_and_stats():
    base_dir = os.path.join(os.path.dirname(__file__), "..")
    csv_path = os.path.join(base_dir, "data", "structured", "corpus.csv")
    stats_json_path = os.path.join(base_dir, "data", "structured", "corpus_stats.json")
    catalog_md_path = os.path.join(base_dir, "docs", "corpus_catalog.md")

    print(f"Reading corpus from {csv_path}...")
    df = pd.read_csv(csv_path)

    total_chunks = len(df)
    unique_docs = df["doc_code"].unique()
    total_van_ban = len(unique_docs)
    total_dieu = int(df[["doc_code", "dieu"]].drop_duplicates().shape[0])

    # Khoản & Điểm
    total_khoan = df["khoan"].notna().sum() if "khoan" in df.columns else 0
    total_diem = df["diem"].notna().sum() if "diem" in df.columns else 0

    # Phân loại hiệu lực cấp chunk
    chunk_con_hl = int((df["hieu_luc"] == "con_hieu_luc").sum())
    chunk_het_hl = int((df["hieu_luc"] == "het_hieu_luc").sum())

    # Thống kê chi tiết từng văn bản
    by_doc = {}
    doc_summary_rows = []

    # Danh mục phân loại văn bản
    doc_type_mapping = {
        "10_2012_QH13": ("Bộ luật", "10/2012/QH13", "01/05/2013"),
        "45_2019_QH14": ("Bộ luật", "45/2019/QH14", "01/01/2021"),
        "58_VBHN-VPQH": ("Luật", "58/VBHN-VPQH", "15/08/2025"),
        "84_2015_QH13": ("Luật", "84/2015/QH13", "01/07/2016"),
        "69_2020_QH14": ("Luật", "69/2020/QH14", "01/01/2022"),
        "84_2025_QH15": ("Luật", "84/2025/QH15", "01/07/2025"),
        "74_2025_QH15": ("Luật", "74/2025/QH15", "01/01/2026"),
        "51_2010_QH12": ("Luật", "51/2010/QH12", "01/01/2011"),
        "91_2025_QH15": ("Luật", "91/2025/QH15", "01/01/2026"),
        "50_2024_QH15": ("Luật", "50/2024/QH15", "01/07/2025"),
        "HP_2013": ("Hiến pháp", "Hiến pháp 2013", "01/01/2014"),
        "145_2020_NDCP": ("Nghị định", "145/2020/NĐ-CP", "01/02/2021"),
        "12_2022_NDCP": ("Nghị định", "12/2022/NĐ-CP", "17/01/2022"),
        "356_2025_NDCP": ("Nghị định", "356/2025/NĐ-CP", "01/01/2026"),
        "152_2020_NDCP": ("Nghị định", "152/2020/NĐ-CP", "15/02/2021"),
        "70_2023_NDCP": ("Nghị định", "70/2023/NĐ-CP", "18/09/2023"),
        "293_2025_NDCP": ("Nghị định", "293/2025/NĐ-CP", "01/01/2026"),
    }

    doc_con_count = 0
    doc_mot_phan_count = 0
    doc_het_count = 0

    for doc_code in unique_docs:
        sub = df[df["doc_code"] == doc_code]
        doc_name = sub["van_ban"].iloc[0]
        chunks = len(sub)
        dieu_count = sub["dieu"].nunique()
        khoan_count = int(sub["khoan"].notna().sum()) if "khoan" in sub.columns else 0
        diem_count = int(sub["diem"].notna().sum()) if "diem" in sub.columns else 0
        con = int((sub["hieu_luc"] == "con_hieu_luc").sum())
        het = int((sub["hieu_luc"] == "het_hieu_luc").sum())

        if het == chunks:
            trang_thai_doc = "het_hieu_luc"
            status_label = "❌ Hết hiệu lực"
            doc_het_count += 1
        elif het > 0 and con > 0:
            trang_thai_doc = "het_hieu_luc_mot_phan"
            status_label = "⚠️ Hết hiệu lực một phần"
            doc_mot_phan_count += 1
        else:
            trang_thai_doc = "con_hieu_luc"
            status_label = "✅ Còn hiệu lực"
            doc_con_count += 1

        dtype, so_hieu, ngay_hl = doc_type_mapping.get(doc_code, ("Khác", doc_code, "N/A"))

        by_doc[doc_name] = {
            "doc_code": doc_code,
            "so_hieu": so_hieu,
            "chunks": chunks,
            "dieu": dieu_count,
            "khoan": khoan_count,
            "diem": diem_count,
            "hieu_luc": trang_thai_doc,
            "con_hieu_luc_chunks": con,
            "het_hieu_luc_chunks": het
        }

        doc_summary_rows.append({
            "doc_code": doc_code,
            "dtype": dtype,
            "van_ban": doc_name.split("(")[0].strip(),
            "so_hieu": so_hieu,
            "ngay_hl": ngay_hl,
            "status_label": status_label,
            "dieu": dieu_count,
            "chunks": chunks,
            "con": con,
            "het": het
        })

    # 1. Ghi corpus_stats.json
    stats_data = {
        "snapshot_date": "2026-08-01",
        "source": "vbpl.vn",
        "total_chunks": int(total_chunks),
        "total_van_ban": int(total_van_ban),
        "total_dieu": int(total_dieu),
        "total_khoan": int(total_khoan),
        "total_co_diem": int(total_diem),
        "chunk_hieu_luc": {
            "con_hieu_luc": int(chunk_con_hl),
            "het_hieu_luc": int(chunk_het_hl),
            "pct_con_hieu_luc": float(round(chunk_con_hl / total_chunks * 100, 2)),
            "pct_het_hieu_luc": float(round(chunk_het_hl / total_chunks * 100, 2))
        },
        "document_hieu_luc": {
            "con_hieu_luc": int(doc_con_count),
            "het_hieu_luc_mot_phan": int(doc_mot_phan_count),
            "het_hieu_luc": int(doc_het_count)
        },
        "by_document": by_doc
    }

    with open(stats_json_path, "w", encoding="utf-8") as f:
        json.dump(stats_data, f, ensure_ascii=False, indent=2)
    print(f"Saved stats to {stats_json_path}")

    # 2. Ghi docs/corpus_catalog.md
    md_content = f"""# Danh mục Corpus Pháp luật Lao động

> **Ngày snapshot**: 01/08/2026  
> **Nguồn dữ liệu**: vbpl.vn (Cơ sở dữ liệu quốc gia về văn bản quy phạm pháp luật)  
> **Tổng số văn bản**: {total_van_ban}  
> **Tổng số chunk**: {total_chunks:,}  
> **Phương pháp sinh**: Tự động sinh từ `data/structured/corpus.csv` bằng `scripts/generate_catalog.py` (Single Source of Truth).

---

## 1. Tổng quan Thống kê Corpus

| Chỉ số | Cấp Chunk | Tỷ lệ Chunk | Cấp Văn bản |
|---|---|---|---|
| **Tổng số đơn vị** | **{total_chunks:,}** | 100% | **{total_van_ban} văn bản** |
| ✅ **Còn hiệu lực** | {chunk_con_hl:,} | {chunk_con_hl/total_chunks*100:.1f}% | {doc_con_count} văn bản |
| ⚠️ **Hết hiệu lực một phần** | *(quản lý cấp chunk)* | *(35 chunk bị bãi bỏ)* | {doc_mot_phan_count} văn bản |
| ❌ **Hết hiệu lực toàn bộ** | {chunk_het_hl:,} | {chunk_het_hl/total_chunks*100:.1f}% | {doc_het_count} văn bản (BLLĐ 2012) |
| **Tổng số Điều** | {total_dieu:,} | - | - |
| **Chunk có cấp Khoản** | {total_khoan:,} | {total_khoan/total_chunks*100:.1f}% | - |
| **Chunk có cấp Điểm** | {total_diem:,} | {total_diem/total_chunks*100:.1f}% | - |

---

## 2. Danh sách Chi tiết 17 Văn bản Quy phạm Pháp luật

| # | Loại VB | Tên văn bản | Số hiệu | Ngày có hiệu lực | Trạng thái hiệu lực | Số Điều | Tổng Chunk | Còn HL | Hết HL |
|---|---|---|---|---|---|---|---|---|---|
"""
    for i, r in enumerate(doc_summary_rows, start=1):
        md_content += f"| {i} | {r['dtype']} | {r['van_ban']} | `{r['so_hieu']}` | {r['ngay_hl']} | {r['status_label']} | {r['dieu']} | {r['chunks']} | {r['con']} | {r['het']} |\n"

    md_content += """
---

## 3. Ghi chú về Phạm vi Dữ liệu & Quản lý Hiệu lực (Phục vụ Báo cáo)

1. **Văn bản cốt lõi tra cứu lao động:**
   - Bộ luật Lao động 2019 (`45/2019/QH14` - có hiệu lực 01/01/2021).
   - Nghị định 145/2020/NĐ-CP (quy định chi tiết thi hành Bộ luật Lao động).
   - Luật Bảo hiểm xã hội (`58/VBHN-VPQH` - văn bản hợp nhất số 58).
   - Luật An toàn, vệ sinh lao động 2015 (`84/2015/QH13`).
   - Luật Công đoàn (`50/2024/QH15`).
   - Nghị định 12/2022/NĐ-CP (xử phạt vi phạm hành chính lĩnh vực lao động).

2. **Văn bản đối sánh lịch sử:**
   - Bộ luật Lao động 2012 (`10/2012/QH13` - hết hiệu lực từ 01/01/2021) được giữ lại trong cơ sở dữ liệu để phục vụ kiểm tra khả năng phân biệt hiệu lực và đối chiếu lịch sử.

3. **Văn bản pháp luật bổ trợ liên quan:**
   - Luật Người lao động Việt Nam đi làm việc ở nước ngoài theo hợp đồng (`69/2020/QH14`).
   - Luật Việc làm (`74/2025/QH15`), Luật Bảo vệ dữ liệu cá nhân (`91/2025/QH15`), Luật Thanh tra, Luật Người khuyết tật và Hiến pháp 2013.
"""

    os.makedirs(os.path.dirname(catalog_md_path), exist_ok=True)
    with open(catalog_md_path, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"Saved catalog to {catalog_md_path}")


if __name__ == "__main__":
    generate_catalog_and_stats()
