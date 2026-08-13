# -*- coding: utf-8 -*-
"""
parse_structure.py – Tách cấu trúc Chương–Mục–Điều–Khoản–Điểm từ text đã làm sạch.

Đọc các file .txt trong project/data/clean/, phân tích cấu trúc pháp luật,
gán provision ID duy nhất, metadata hiệu lực, và xuất ra JSON + CSV.

Logic chunking (theo project.md):
  - Chunk theo Khoản: mỗi khoản = 1 chunk
  - Lùi về Điều khi Điều không có Khoản: cả Điều = 1 chunk
  - Chèn tiêu đề Điều vào đầu mỗi chunk
"""

import os
import re
import sys
import json
import csv
from pathlib import Path

# ============================================================
# CẤU HÌNH
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent.parent  # TT/
DATA_CLEAN = BASE_DIR / "project" / "data" / "clean"
DATA_STRUCTURED = BASE_DIR / "project" / "data" / "structured"

SNAPSHOT_DATE = "2026-08-01"

from overrides import DOC_REGISTRY, MODIFIED_PROVISIONS, ADDED_PROVISIONS


# ============================================================
# REGEX PATTERNS
# ============================================================

# Chương (Chương I, Chương II, Chương 1, Chương I.)
RE_CHUONG = re.compile(
    r'^[ \t]*Ch(?:ư|u)(?:ơ|o)ng[ \t]+([IVXLCDM]+|\d+)\.?[ \t]*(.*)',
    re.IGNORECASE | re.MULTILINE
)

# Mục (Mục 1, Mục 2, ...)
RE_MUC = re.compile(
    r'^[ \t]*M(?:ụ|u)c[ \t]+(\d+)\.?[ \t]*(.*)',
    re.IGNORECASE | re.MULTILINE
)

# Điều – bắt đầu dòng
# Xử lý cả "Điều 1. Tiêu đề" và "Điều 1." (không có tiêu đề, như Hiến pháp)
RE_DIEU = re.compile(
    r'^[ \t]*Đi[eề]u[ \t]+(\d+)\b(?:\.[ \t]*(.*))?[ \t]*$',
    re.MULTILINE
)

# Khoản: "1. ", "2. ", ... ở đầu dòng
RE_KHOAN = re.compile(
    r'^[ \t]*(\d{1,2})\.[ \t]+',
    re.MULTILINE
)

# Điểm: "a) ", "b) ", "a. ", ...
RE_DIEM = re.compile(
    r'^[ \t]*([a-zđ])[)\.]?\)[ \t]*',
    re.MULTILINE
)


def get_doc_info(filename: str, text: str) -> dict:
    """
    Lấy thông tin văn bản từ bảng registry hoặc tự phát hiện.
    """
    stem = Path(filename).stem

    if stem in DOC_REGISTRY:
        info = DOC_REGISTRY[stem].copy()
        return info

    # Fallback: tự phát hiện
    info = {
        "doc_code": re.sub(r'[^\w]', '_', stem),
        "doc_name": stem,
        "doc_type": "Khác",
        "so_hieu": "",
        "ngay_hieu_luc": "",
        "ngay_het_hieu_luc": "",
        "trang_thai_chung": "con_hieu_luc",
        "ghi_chu": "Tự phát hiện - cần kiểm tra",
    }

    # Thử tìm số hiệu
    so_hieu_match = re.search(
        r'[Ss][ốo][\s:]*(\d+)[/\-](\d{4})[/\-]([A-ZĐa-zđ\-]+)',
        text[:3000]
    )
    if so_hieu_match:
        num, year, org = so_hieu_match.group(1), so_hieu_match.group(2), so_hieu_match.group(3)
        org_clean = org.upper().replace('-', '').replace('NĐ', 'ND')
        info["doc_code"] = f"{num}_{year}_{org_clean}"
        info["so_hieu"] = f"{num}/{year}/{org}"

    text_upper = text[:5000].upper()
    if 'HIẾN PHÁP' in text_upper:
        info["doc_type"] = "Hiến pháp"
    elif 'BỘ LUẬT' in text_upper:
        info["doc_type"] = "Bộ luật"
    elif 'NGHỊ ĐỊNH' in text_upper:
        info["doc_type"] = "Nghị định"
    elif 'LUẬT' in text_upper:
        info["doc_type"] = "Luật"

    return info


def parse_document(text: str, doc_info: dict) -> list[dict]:
    """
    Phân tích cấu trúc văn bản pháp luật và tạo các chunk.

    Logic chunking:
    - Chunk theo Khoản (mỗi khoản = 1 chunk)
    - Nếu Điều không có Khoản → cả Điều = 1 chunk
    - Chèn tiêu đề Điều vào đầu mỗi chunk
    """
    chunks = []
    doc_code = doc_info["doc_code"]

    current_chuong = ""

    # Tìm tất cả Điều
    dieu_matches = list(RE_DIEU.finditer(text))

    if not dieu_matches:
        # Không tìm thấy Điều nào
        chunk = _make_chunk(
            doc_info, chuong="", dieu_num="0",
            tieu_de_dieu="(Toàn bộ văn bản)",
            khoan_num=None, diem=None,
            noi_dung=text[:5000],
        )
        chunks.append(chunk)
        return chunks

    # Pre-compute tất cả Chương positions
    chuong_list = []
    for cm in RE_CHUONG.finditer(text):
        chuong_num = cm.group(1)
        chuong_title = cm.group(2).strip().rstrip('.')
        chuong_label = f"Chương {chuong_num}"
        if chuong_title:
            chuong_label += f" - {chuong_title}"
        chuong_list.append((cm.start(), chuong_label))

    for idx, dieu_match in enumerate(dieu_matches):
        dieu_num = dieu_match.group(1)
        tieu_de_dieu = dieu_match.group(2).strip().rstrip('.')

        # Nội dung Điều: từ sau match đến Điều tiếp
        start = dieu_match.end()
        end = dieu_matches[idx + 1].start() if idx + 1 < len(dieu_matches) else len(text)
        dieu_content = text[start:end].strip()

        # Xác định Chương chứa Điều (chương có vị trí gần nhất trước Điều)
        for pos, label in chuong_list:
            if pos < dieu_match.start():
                current_chuong = label

        # Tách Khoản
        khoan_matches = list(RE_KHOAN.finditer(dieu_content))

        if not khoan_matches:
            # Điều không có Khoản → cả Điều = 1 chunk
            noi_dung = dieu_content.strip() or tieu_de_dieu
            chunk = _make_chunk(
                doc_info, chuong=current_chuong, dieu_num=dieu_num,
                tieu_de_dieu=tieu_de_dieu,
                khoan_num=None, diem=None, noi_dung=noi_dung,
            )
            chunks.append(chunk)
        else:
            # Nội dung trước Khoản 1 (intro text)
            intro = dieu_content[:khoan_matches[0].start()].strip()

            for k_idx, k_match in enumerate(khoan_matches):
                khoan_num = k_match.group(1)
                k_start = k_match.start()
                k_end = (khoan_matches[k_idx + 1].start()
                         if k_idx + 1 < len(khoan_matches)
                         else len(dieu_content))
                khoan_content = dieu_content[k_start:k_end].strip()

                # Phát hiện Điểm trong Khoản
                diem_matches = list(RE_DIEM.finditer(khoan_content))
                diem_str = ", ".join(dm.group(1) for dm in diem_matches) if diem_matches else None

                chunk = _make_chunk(
                    doc_info, chuong=current_chuong, dieu_num=dieu_num,
                    tieu_de_dieu=tieu_de_dieu,
                    khoan_num=khoan_num, diem=diem_str,
                    noi_dung=khoan_content,
                )
                chunks.append(chunk)

    return chunks


def _make_chunk(doc_info: dict, chuong: str, dieu_num: str,
                tieu_de_dieu: str, khoan_num: str | None,
                diem: str | None, noi_dung: str) -> dict:
    """Tạo một chunk với provision_id và metadata."""
    doc_code = doc_info["doc_code"]

    # Tạo provision_id
    provision_id = f"{doc_code}__D{dieu_num}"
    if khoan_num:
        provision_id += f"__K{khoan_num}"

    # Chèn tiêu đề Điều vào đầu nội dung
    header = f"Điều {dieu_num}"
    if tieu_de_dieu:
        header += f". {tieu_de_dieu}"

    full_content = f"{header}\n{noi_dung}" if noi_dung and noi_dung != tieu_de_dieu else header

    trang_thai = doc_info.get("trang_thai_chung", "con_hieu_luc")
    # Nếu văn bản hết hiệu lực một phần, mặc định các chunk là còn hiệu lực
    if trang_thai == "het_hieu_luc_mot_phan":
        trang_thai = "con_hieu_luc"

    ghi_chu = doc_info.get("ghi_chu", "")

    return {
        "provision_id": provision_id,
        "van_ban": f"{doc_info.get('doc_name', '')} ({doc_info.get('so_hieu', doc_code)})",
        "doc_code": doc_code,
        "chuong": chuong,
        "dieu": dieu_num,
        "tieu_de_dieu": tieu_de_dieu,
        "khoan": khoan_num or "",
        "diem": diem or "",
        "noi_dung": full_content,
        "hieu_luc": trang_thai,
        "ngay_hieu_luc": doc_info.get("ngay_hieu_luc", ""),
        "ngay_het_hieu_luc": doc_info.get("ngay_het_hieu_luc", ""),
        "thay_the_boi": "",
        "thay_the_cho": "",
        "van_ban_sua_doi": "",
        "ghi_chu": ghi_chu,
    }


def apply_versioning(all_chunks: list[dict]) -> list[dict]:
    """Áp dụng versioning cho các provision bị sửa đổi.
    
    Với mỗi provision_id nằm trong MODIFIED_PROVISIONS:
    - Chunk gốc → gắn _v1, đánh dấu het_hieu_luc, thêm trường thay_the_boi
    - Tạo chunk mới → gắn _v2, đánh dấu con_hieu_luc, thêm trường thay_the_cho
    """
    new_chunks = []
    for chunk in all_chunks:
        pid = chunk["provision_id"]
        if pid in MODIFIED_PROVISIONS:
            override = MODIFIED_PROVISIONS[pid]
            v2_id = f"{pid}_v2"

            is_bai_bo = override.get("bai_bo", False)

            # --- Chunk gốc (nội dung cũ, hết hiệu lực) - giữ nguyên ID ---
            chunk["hieu_luc"] = "het_hieu_luc"
            if not is_bai_bo:
                chunk["thay_the_boi"] = v2_id
            chunk["ngay_het_hieu_luc"] = override.get("ngay_het_hieu_luc", "")
            chunk["van_ban_sua_doi"] = override.get("van_ban_sua_doi", "")
            chunk["ghi_chu"] = override.get("ghi_chu_v1", chunk["ghi_chu"])
            new_chunks.append(chunk)

            if not is_bai_bo:
                # --- Chunk v2 (nội dung mới, còn hiệu lực) ---
                v2_chunk = chunk.copy()
                v2_chunk["provision_id"] = v2_id
                v2_chunk["noi_dung"] = override.get("noi_dung_v2", "")
                v2_chunk["hieu_luc"] = "con_hieu_luc"
                v2_chunk["thay_the_boi"] = ""
                v2_chunk["thay_the_cho"] = pid
                if "ngay_hieu_luc_v2" in override:
                    v2_chunk["ngay_hieu_luc"] = override["ngay_hieu_luc_v2"]
                v2_chunk["van_ban_sua_doi"] = override.get("van_ban_sua_doi", "")
                v2_chunk["ghi_chu"] = override.get("ghi_chu_v2", "")
                
                # Cho phép ghi đè các trường cấu trúc nếu có thay đổi
                for field in ["diem", "khoan", "tieu_de_dieu", "chuong", "dieu"]:
                    if field in override:
                        v2_chunk[field] = override[field]
                        
                new_chunks.append(v2_chunk)
        else:
            new_chunks.append(chunk)
    return new_chunks


def ensure_unique_ids(all_chunks: list[dict]) -> int:
    """Đảm bảo provision_id duy nhất, trả về số trùng đã sửa."""
    seen = {}
    dup_count = 0
    for chunk in all_chunks:
        pid = chunk["provision_id"]
        if pid in seen:
            seen[pid] += 1
            chunk["provision_id"] = f"{pid}__dup{seen[pid]}"
            dup_count += 1
        else:
            seen[pid] = 0
    return dup_count


def save_json(chunks: list[dict], path: Path):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)


def save_csv(chunks: list[dict], path: Path):
    if not chunks:
        return
    with open(path, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=chunks[0].keys())
        writer.writeheader()
        writer.writerows(chunks)


def generate_stats(all_chunks: list[dict]) -> dict:
    stats = {
        "snapshot_date": SNAPSHOT_DATE,
        "total_chunks": len(all_chunks),
        "total_van_ban": len(set(c["doc_code"] for c in all_chunks)),
        "total_dieu": len(set((c["doc_code"], c["dieu"]) for c in all_chunks)),
        "total_khoan": sum(1 for c in all_chunks if c["khoan"]),
        "total_co_diem": sum(len(c["diem"].split(",")) for c in all_chunks if c["diem"]),
        "hieu_luc": {
            "con_hieu_luc": sum(1 for c in all_chunks if c["hieu_luc"] == "con_hieu_luc"),
            "het_hieu_luc": sum(1 for c in all_chunks if c["hieu_luc"] == "het_hieu_luc"),
            "het_hieu_luc_mot_phan": sum(1 for c in all_chunks if c["hieu_luc"] == "het_hieu_luc_mot_phan"),
            "sua_doi": sum(1 for c in all_chunks if c["hieu_luc"] == "sua_doi"),
        },
        "by_document": {},
    }

    for chunk in all_chunks:
        key = chunk["van_ban"]
        if key not in stats["by_document"]:
            stats["by_document"][key] = {
                "doc_code": chunk["doc_code"],
                "chunks": 0,
                "dieu": set(),
                "khoan": 0,
                "diem": 0,
                "hieu_luc": chunk["hieu_luc"],
            }
        stats["by_document"][key]["chunks"] += 1
        stats["by_document"][key]["dieu"].add(chunk["dieu"])
        if chunk["khoan"]:
            stats["by_document"][key]["khoan"] += 1
        if chunk["diem"]:
            stats["by_document"][key]["diem"] += len(chunk["diem"].split(","))

    # Convert sets to counts for JSON serialization
    for key in stats["by_document"]:
        stats["by_document"][key]["dieu"] = len(stats["by_document"][key]["dieu"])

    return stats


def main():
    print("=" * 60)
    print("TACH CAU TRUC DIEU-KHOAN-DIEM & GAN PROVISION ID")
    print("=" * 60)

    DATA_STRUCTURED.mkdir(parents=True, exist_ok=True)

    # Đọc tất cả file text đã làm sạch (bỏ qua file _extraction_report.json)
    clean_files = sorted(
        f for f in DATA_CLEAN.glob("*.txt")
        if not f.name.startswith("_")
    )

    if not clean_files:
        print("KHONG TIM THAY file text nao trong data/clean/!")
        sys.exit(1)

    print(f"\nTim thay {len(clean_files)} file text.\n")

    all_chunks = []

    for txt_path in clean_files:
        print(f"Dang phan tich: {txt_path.name}")

        with open(txt_path, 'r', encoding='utf-8') as f:
            text = f.read()

        # Lấy thông tin văn bản
        doc_info = get_doc_info(txt_path.name, text)
        print(f"  Ma VB: {doc_info['doc_code']}")
        print(f"  Loai:  {doc_info['doc_type']}")
        print(f"  Ten:   {doc_info['doc_name']}")

        # Tách cấu trúc
        chunks = parse_document(text, doc_info)
        print(f"  -> {len(chunks)} chunk(s)")

        all_chunks.extend(chunks)

    # Áp dụng versioning cho các provision bị sửa đổi
    print(f"\nAp dung versioning cho cac provision bi sua doi...")
    count_before = len(all_chunks)
    all_chunks = apply_versioning(all_chunks)
    count_new = len(all_chunks) - count_before
    if count_new:
        print(f"  Da tao {count_new} chunk v2 moi (tong: {len(all_chunks)} chunks).")
    else:
        print(f"  Khong co provision nao can versioning.")

    # Bổ sung các provision mới hoàn toàn (thêm khoản mới)
    if ADDED_PROVISIONS:
        print(f"\nBo sung cac provision moi...")
        all_chunks.extend(ADDED_PROVISIONS)
        print(f"  Da them {len(ADDED_PROVISIONS)} chunk moi.")

    # Kiểm tra provision_id duy nhất
    print(f"\nKiem tra tinh duy nhat cua provision_id...")
    dup_count = ensure_unique_ids(all_chunks)
    if dup_count:
        print(f"  [CANH BAO] {dup_count} provision_id trung lap da duoc sua tu dong.")
    else:
        print(f"  OK - Tat ca provision_id deu duy nhat.")

    # Lưu JSON
    json_path = DATA_STRUCTURED / "corpus.json"
    save_json(all_chunks, json_path)
    print(f"\nDa luu corpus JSON: {json_path}")

    # Lưu CSV
    csv_path = DATA_STRUCTURED / "corpus.csv"
    save_csv(all_chunks, csv_path)
    print(f"Da luu corpus CSV: {csv_path}")

    # Thống kê
    stats = generate_stats(all_chunks)
    stats_path = DATA_STRUCTURED / "corpus_stats.json"
    with open(stats_path, 'w', encoding='utf-8') as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)
    print(f"Da luu thong ke: {stats_path}")

    # In thống kê
    print(f"\n{'=' * 60}")
    print(f"THONG KE CORPUS")
    print(f"{'=' * 60}")
    print(f"Ngay snapshot:    {stats['snapshot_date']}")
    print(f"Tong so van ban:  {stats['total_van_ban']}")
    print(f"Tong so Dieu:     {stats['total_dieu']}")
    print(f"Tong so chunk:    {stats['total_chunks']}")
    print(f"  - Chunk co Khoan: {stats['total_khoan']}")
    print(f"  - Chunk co Diem:  {stats['total_co_diem']}")
    print(f"Hieu luc:")
    print(f"  - Con hieu luc:  {stats['hieu_luc']['con_hieu_luc']}")
    print(f"  - Het hieu luc:  {stats['hieu_luc']['het_hieu_luc']}")
    print(f"  - Sua doi:       {stats['hieu_luc']['sua_doi']}")

    print(f"\nThong ke theo van ban:")
    for doc, ds in stats["by_document"].items():
        print(f"  {doc}")
        print(f"    {ds['dieu']} Dieu, {ds['chunks']} chunk, trang thai: {ds['hieu_luc']}")

    print(f"\n{'=' * 60}")
    print(f"HOAN TAT!")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
