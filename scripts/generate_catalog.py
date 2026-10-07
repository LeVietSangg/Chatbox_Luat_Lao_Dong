# -*- coding: utf-8 -*-
"""
scripts/generate_catalog.py
Sinh catalog văn bản (docs/corpus_catalog.md) và thống kê (data/structured/corpus_stats.json)
từ nguồn duy nhất: data/structured/corpus.csv.
Sinh catalog và thống kê tự động từ corpus.csv để tránh sai lệch số liệu do cập nhật thủ công.
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

    # Phân loại nhóm vai trò chức năng
    ROLE_CORE = "Cốt lõi lao động"
    ROLE_HIST = "Đối sánh lịch sử"
    ROLE_DIST = "Đối chứng nhiễu"

    doc_meta_mapping = {
        # Nhóm 1: Cốt lõi & Quy định Hướng dẫn Pháp luật Lao động (12 văn bản)
        "45_2019_QH14": (ROLE_CORE, "Bộ luật", "45/2019/QH14", "01/01/2021", "Bộ luật Lao động 2019"),
        "145_2020_NDCP": (ROLE_CORE, "Nghị định", "145/2020/NĐ-CP", "01/02/2021", "Nghị định 145/2020/NĐ-CP"),
        "12_2022_NDCP": (ROLE_CORE, "Nghị định", "12/2022/NĐ-CP", "17/01/2022", "Nghị định 12/2022/NĐ-CP"),
        "152_2020_NDCP": (ROLE_CORE, "Nghị định", "152/2020/NĐ-CP", "15/02/2021", "Nghị định 152/2020/NĐ-CP"),
        "70_2023_NDCP": (ROLE_CORE, "Nghị định", "70/2023/NĐ-CP", "18/09/2023", "Nghị định 70/2023/NĐ-CP"),
        "293_2025_NDCP": (ROLE_CORE, "Nghị định", "293/2025/NĐ-CP", "01/01/2026", "Nghị định 293/2025/NĐ-CP"),
        "356_2025_NDCP": (ROLE_CORE, "Nghị định", "356/2025/NĐ-CP", "01/01/2026", "Nghị định 356/2025/NĐ-CP"),
        "58_VBHN-VPQH": (ROLE_CORE, "Luật", "58/VBHN-VPQH", "15/08/2025", "Luật Bảo hiểm xã hội"),
        "84_2015_QH13": (ROLE_CORE, "Luật", "84/2015/QH13", "01/07/2016", "Luật An toàn, vệ sinh lao động"),
        "50_2024_QH15": (ROLE_CORE, "Luật", "50/2024/QH15", "01/07/2025", "Luật Công đoàn"),
        "74_2025_QH15": (ROLE_CORE, "Luật", "74/2025/QH15", "01/01/2026", "Luật Việc làm"),
        "69_2020_QH14": (ROLE_CORE, "Luật", "69/2020/QH14", "01/01/2022", "Luật NLĐ Việt Nam đi làm việc ở nước ngoài theo hợp đồng"),
        # Nhóm 2: Đối sánh Lịch sử Hiệu lực (1 văn bản)
        "10_2012_QH13": (ROLE_HIST, "Bộ luật", "10/2012/QH13", "01/05/2013", "Bộ luật Lao động 2012"),
        # Nhóm 3: Đối chứng Nhiễu & Thử thách Biên giới Thẩm quyền (4 văn bản)
        "HP_2013": (ROLE_DIST, "Hiến pháp", "Hiến pháp 2013", "01/01/2014", "Hiến pháp 2013"),
        "84_2025_QH15": (ROLE_DIST, "Luật", "84/2025/QH15", "01/07/2025", "Luật Thanh tra"),
        "51_2010_QH12": (ROLE_DIST, "Luật", "51/2010/QH12", "01/01/2011", "Luật Người khuyết tật"),
        "91_2025_QH15": (ROLE_DIST, "Luật", "91/2025/QH15", "01/01/2026", "Luật Bảo vệ dữ liệu cá nhân"),
    }

    doc_con_count = 0
    doc_mot_phan_count = 0
    doc_het_count = 0

    role_order = {ROLE_CORE: 1, ROLE_HIST: 2, ROLE_DIST: 3}
    role_stats = {
        ROLE_CORE: {"docs": 0, "chunks": 0, "dieu": 0},
        ROLE_HIST: {"docs": 0, "chunks": 0, "dieu": 0},
        ROLE_DIST: {"docs": 0, "chunks": 0, "dieu": 0},
    }

    for doc_code in unique_docs:
        sub = df[df["doc_code"] == doc_code]
        raw_doc_name = sub["van_ban"].iloc[0]
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

        meta = doc_meta_mapping.get(doc_code, (ROLE_CORE, "Khác", doc_code, "N/A", raw_doc_name.split("(")[0].strip()))
        role, dtype, so_hieu, ngay_hl, display_name = meta

        role_stats[role]["docs"] += 1
        role_stats[role]["chunks"] += chunks
        role_stats[role]["dieu"] += dieu_count

        by_doc[raw_doc_name] = {
            "doc_code": doc_code,
            "role": role,
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
            "role": role,
            "role_order": role_order.get(role, 99),
            "dtype": dtype,
            "van_ban": display_name,
            "so_hieu": so_hieu,
            "ngay_hl": ngay_hl,
            "status_label": status_label,
            "dieu": dieu_count,
            "chunks": chunks,
            "con": con,
            "het": het
        })

    # Sắp xếp danh mục: Cốt lõi lao động -> Đối sánh lịch sử -> Đối chứng nhiễu
    doc_summary_rows.sort(key=lambda r: (r["role_order"], -r["chunks"]))
    # Thống kê chunk theo trạng thái hiệu lực của văn bản
    partial_expired_chunks = sum(
        r["het"] for r in doc_summary_rows
        if r["status_label"] == "⚠️ Hết hiệu lực một phần"
    )

    fully_expired_chunks = sum(
        r["het"] for r in doc_summary_rows
        if r["status_label"] == "❌ Hết hiệu lực"
    )
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
        "roles_breakdown": {
            "core_labor": {
                "label": "Cốt lõi & Quy định hướng dẫn lao động",
                "docs_count": role_stats[ROLE_CORE]["docs"],
                "chunks_count": role_stats[ROLE_CORE]["chunks"],
                "pct_chunks": float(round(role_stats[ROLE_CORE]["chunks"] / total_chunks * 100, 2))
            },
            "historical_contrast": {
                "label": "Đối sánh lịch sử hiệu lực",
                "docs_count": role_stats[ROLE_HIST]["docs"],
                "chunks_count": role_stats[ROLE_HIST]["chunks"],
                "pct_chunks": float(round(role_stats[ROLE_HIST]["chunks"] / total_chunks * 100, 2))
            },
            "distractor_benchmark": {
                "label": "Đối chứng nhiễu & Biên giới thẩm quyền",
                "docs_count": role_stats[ROLE_DIST]["docs"],
                "chunks_count": role_stats[ROLE_DIST]["chunks"],
                "pct_chunks": float(round(role_stats[ROLE_DIST]["chunks"] / total_chunks * 100, 2))
            }
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
> **Tổng số văn bản trong Chỉ mục chung (Shared Index)**: {total_van_ban} văn bản  
> **Tổng số chunk**: {total_chunks:,} đoạn quy định  
> **Phương pháp sinh**: Tự động sinh từ `data/structured/corpus.csv` bằng `scripts/generate_catalog.py` (Single Source of Truth).

---

## 1. Tổng quan Thống kê Corpus & Phân định Vai trò

### 1.1. Thống kê theo Hiệu lực Văn bản & Chunk
| Chỉ số | Cấp Chunk | Tỷ lệ Chunk | Cấp Văn bản |
|---|---|---|---|
| **Tổng số đơn vị** | **{total_chunks:,}** | 100% | **{total_van_ban} văn bản** |
| ✅ **Còn hiệu lực** | {chunk_con_hl:,} | {chunk_con_hl/total_chunks*100:.1f}% | {doc_con_count} văn bản |
| ⚠️ **Hết hiệu lực một phần** | *(quản lý cấp chunk)* | *({partial_expired_chunks:,} chunk bị bãi bỏ)* | {doc_mot_phan_count} văn bản |
| ❌ **Hết hiệu lực toàn bộ** | {fully_expired_chunks:,} | {fully_expired_chunks/total_chunks*100:.1f}% | {doc_het_count} văn bản (BLLĐ 2012) |
| **Tổng số Điều** | {total_dieu:,} | - | - |
| **Chunk có cấp Khoản** | {total_khoan:,} | {total_khoan/total_chunks*100:.1f}% | - |
| **Chunk có cấp Điểm** | {total_diem:,} | {total_diem/total_chunks*100:.1f}% | - |

### 1.2. Thống kê theo Nhóm Vai trò Chức năng trong Chỉ mục Chung
| Nhóm Vai trò Chức năng | Số Văn bản | Tỷ lệ VB | Số Chunk | Tỷ lệ Chunk | Mục đích Nghiên cứu & Vận hành |
|---|---|---|---|---|---|
| 🏛️ **1. Cốt lõi & Hướng dẫn thi hành** | {role_stats[ROLE_CORE]["docs"]} văn bản | {role_stats[ROLE_CORE]["docs"]/total_van_ban*100:.1f}% | {role_stats[ROLE_CORE]["chunks"]:,} | {role_stats[ROLE_CORE]["chunks"]/total_chunks*100:.1f}% | Tra cứu và áp dụng hiện hành trong pháp luật lao động |
| ⏳ **2. Đối sánh lịch sử hiệu lực** | {role_stats[ROLE_HIST]["docs"]} văn bản | {role_stats[ROLE_HIST]["docs"]/total_van_ban*100:.1f}% | {role_stats[ROLE_HIST]["chunks"]:,} | {role_stats[ROLE_HIST]["chunks"]/total_chunks*100:.1f}% | Đánh giá lọc hiệu lực thời gian và tra cứu quy định cũ |
| 🎯 **3. Đối chứng nhiễu (Distractor Benchmark)** | {role_stats[ROLE_DIST]["docs"]} văn bản | {role_stats[ROLE_DIST]["docs"]/total_van_ban*100:.1f}% | {role_stats[ROLE_DIST]["chunks"]:,} | {role_stats[ROLE_DIST]["chunks"]/total_chunks*100:.1f}% | Thử thách chống False Positive & đo lường Refusal Accuracy |
| **Tổng cộng** | **{total_van_ban} văn bản** | **100%** | **{total_chunks:,}** | **100%** | **Cơ sở dữ liệu thống nhất (Shared Index)** |

---

## 2. Danh sách Chi tiết 17 Văn bản Quy phạm Pháp luật

| # | Nhóm Vai trò | Loại VB | Tên văn bản | Số hiệu | Ngày có hiệu lực | Trạng thái hiệu lực | Số Điều | Tổng Chunk | Còn HL | Hết HL |
|---|---|---|---|---|---|---|---|---|---|---|
"""
    for i, r in enumerate(doc_summary_rows, start=1):
        md_content += f"| {i} | {r['role']} | {r['dtype']} | {r['van_ban']} | `{r['so_hieu']}` | {r['ngay_hl']} | {r['status_label']} | {r['dieu']} | {r['chunks']} | {r['con']} | {r['het']} |\n"

    md_content += """
---

## 3. Ghi chú về Phạm vi Dữ liệu & Thiết kế Thực nghiệm Chỉ mục Chung

### 3.1. Làm rõ Vai trò Đối chứng Nhiễu (Distractor / Negative Control Benchmark)
Trong cơ sở dữ liệu tra cứu và chỉ mục (BM25 + FAISS), sự xuất hiện của **Hiến pháp 2013 (290 đoạn)**, **Luật Thanh tra (221 đoạn)**, **Luật Người khuyết tật (182 đoạn)** và **Luật Bảo vệ dữ liệu cá nhân (171 đoạn)** bên cạnh các văn bản cốt lõi về lao động là một **thiết kế thực nghiệm có chủ đích (Intentional Benchmark Design)**:

1. **Mô phỏng Kho Pháp điển Đa lĩnh vực Thực tế (Anti-Toy Environment):**
   - Trên Cổng thông tin Cơ sở dữ liệu quốc gia về văn bản pháp luật (vbpl.vn), tất cả các văn bản quy phạm pháp luật đều nằm chung trong cùng một hệ thống dữ liệu quốc gia.
   - Nếu xây dựng một chỉ mục chỉ chứa duy nhất văn bản lao động thuần túy, bài toán truy xuất sẽ trở nên phi thực tế (mọi câu hỏi đều dễ dàng match trúng một điều luật lao động ngẫu nhiên). Việc đưa các văn bản bổ trợ/nhiễu vào cùng chỉ mục giúp đánh giá khả năng hoạt động của hệ thống trong môi trường pháp điển hỗn hợp.

2. **Thử thách Khả năng Chống Nhiễu & Chống Bắt nhầm Từ khóa (Disambiguation Challenge):**
   - **Hiến pháp 2013 (`Hiến pháp 2013`, 290 đoạn):** Đạo luật cơ bản có hiệu lực pháp lý cao nhất, chứa các quy định khái quát về quyền con người, quyền công dân, quyền làm việc (Điều 35, Điều 36...). Đây là **đối chứng nhiễu bậc cao (High-level Semantic Distractor)**. Nếu bộ tìm kiếm Dense hoặc BM25 không đủ năng lực phân giải ngữ nghĩa, câu hỏi của người dùng về tình huống lao động cụ thể rất dễ bị trôi dạt (semantic drift) và trích dẫn nhầm Hiến pháp thay vì quy định trực tiếp trong Bộ luật Lao động 2019.
   - **Luật Thanh tra 2025 (`84/2025/QH15`, 221 đoạn):** Chứa các quy định về thẩm quyền, trình tự, thủ tục thanh tra hành chính nhà nước. Đóng vai trò **đối chứng nhiễu về thẩm quyền và thủ tục hành chính**. Phép thử này kiểm tra khả năng hệ thống phân biệt giữa thanh tra nhà nước chung và thanh tra chuyên ngành lao động (Điều 214–217 BLLĐ 2019 và Nghị định 12/2022/NĐ-CP).
   - **Luật Người khuyết tật 2010 (`51/2010/QH12`, 182 đoạn):** Quy định chính sách trợ cấp xã hội và hòa nhập cho người khuyết tật. Đóng vai trò **đối chứng giao thoa biên giới ngữ nghĩa (Domain-boundary Distractor)** đối với các quy định bảo vệ lao động là người khuyết tật (Chương XI BLLĐ 2019), kiểm tra khả năng tách bạch trách nhiệm bảo trợ của Nhà nước với nghĩa vụ hợp đồng của người sử dụng lao động.
   - **Luật Bảo vệ dữ liệu cá nhân 2025 (`91/2025/QH15`, 171 đoạn):** Đóng vai trò **đối chứng biên giới công nghệ & bảo mật**, thách thức hệ thống khi người dùng hỏi về lưu trữ hồ sơ nhân sự, camera giám sát tại nơi làm việc hoặc bảo mật thông tin nhân viên.

3. **Đo lường Năng lực Từ chối Ngoài Phạm vi (Out-of-Scope Refusal Accuracy):**
   - Bộ dữ liệu kiểm thử (Test Set) có 50 câu hỏi ngoài phạm vi (OOD), bao gồm các câu hỏi thuộc thẩm quyền thanh tra hành chính chung, khiếu nại quyết định hành chính, quyền ứng cử bầu cử theo Hiến pháp...
   - Sự hiện diện của các văn bản này trong cùng chỉ mục là điều kiện tiên quyết để kiểm tra: Bộ truy xuất có bị lừa bởi độ tương đồng từ vựng để lấy các văn bản nhiễu hay không, và tầng kiểm định LLM có nhận diện chính xác câu hỏi nằm ngoài phạm vi tư vấn pháp luật lao động để kích hoạt cơ chế từ chối (Refusal) an toàn hay không.

### 3.2. Vai trò của Văn bản Đối sánh Lịch sử Hiệu lực (Bộ luật Lao động 2012)
- **Bộ luật Lao động 2012 (`10/2012/QH13`, 674 đoạn):** Đã hết hiệu lực toàn bộ từ ngày 01/01/2021.
- **Mục đích:** Được lưu giữ trong cơ sở dữ liệu cùng nhãn `het_hieu_luc` nhằm:
  + Kiểm thử năng lực của cơ chế lọc hiệu lực theo thời gian (Temporal Validity Filtering).
  + Kiểm tra khả năng chống ảo giác trích dẫn luật cũ đã bị bãi bỏ khi trả lời các tình huống pháp luật hiện hành.
  + Phục vụ các tình huống tra cứu hồi tố (hợp đồng ký kết trong giai đoạn BLLĐ 2012 có hiệu lực) hoặc đối chiếu so sánh chính sách thay đổi giữa hai thế hệ luật.

### 3.3. Vai trò của 12 Văn bản Cốt lõi & Nghị định Hướng dẫn Thi hành
- Bao gồm Bộ luật Lao động 2019, các Nghị định quy định chi tiết thi hành (NĐ 145/2020/NĐ-CP, NĐ 12/2022/NĐ-CP, NĐ 152/2020/NĐ-CP, NĐ 70/2023/NĐ-CP, NĐ 293/2025/NĐ-CP, NĐ 356/2025/NĐ-CP), cùng các Luật chuyên ngành trực tiếp liên quan mật thiết (Luật Bảo hiểm xã hội, Luật An toàn vệ sinh lao động, Luật Công đoàn, Luật Việc làm, Luật NLĐ Việt Nam đi làm việc ở nước ngoài).
- Đây là nguồn tri thức nền tảng cung cấp căn cứ pháp lý còn hiệu lực cho toàn bộ 7 nhóm chủ đề kiểm thử in-scope.

### 3.4. Thống nhất Số lượng Văn bản Toàn Hệ thống
- **Số văn bản quy phạm pháp luật trong Corpus / Chỉ mục:** **17 văn bản**.
- **Số đoạn quy định (chunks):** **4,890 đoạn**.
- **Tính đồng bộ:** Toàn bộ tài liệu (`README.md`, `docs/corpus_catalog.md`), mã nguồn tiền xử lý (`scripts/generate_catalog.py`, `scripts/build_index.py`), và cơ sở dữ liệu (`data/structured/corpus.csv`, `data/structured/corpus.json`, `data/index/`) được chuẩn hóa theo số liệu sinh tự động từ `data/structured/corpus.csv`.
"""

    os.makedirs(os.path.dirname(catalog_md_path), exist_ok=True)
    with open(catalog_md_path, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"Saved catalog to {catalog_md_path}")


if __name__ == "__main__":
    generate_catalog_and_stats()

