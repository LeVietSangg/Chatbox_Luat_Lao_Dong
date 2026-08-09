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

# ============================================================
# BẢNG MAPPING THỦ CÔNG: filename → (doc_code, doc_name, doc_type, ngay_hieu_luc, trang_thai)
# Đảm bảo doc_code duy nhất cho mỗi văn bản
# ============================================================

DOC_REGISTRY = {
    "VBHN-BoLuatLaoDong": {
        "doc_code": "45_2019_QH14",
        "doc_name": "Bộ luật Lao động",
        "doc_type": "Bộ luật",
        "so_hieu": "45/2019/QH14",
        "ngay_hieu_luc": "2026-01-01",
        "trang_thai_chung": "con_hieu_luc",
        "ghi_chu": "VBHN, sửa đổi bởi Luật 71/2025/QH15",
    },
    "VBHN-LuatBHXH": {
        "doc_code": "58_VBHN-VPQH",
        "doc_name": "Luật Bảo hiểm xã hội",
        "doc_type": "Luật",
        "so_hieu": "58/VBHN-VPQH",
        "ngay_hieu_luc": "2025-08-15",
        "trang_thai_chung": "con_hieu_luc",
        "ghi_chu": "VBHN, sửa đổi bởi Luật 73/2025 và 84/2025",
    },
    "VanBanGoc_84.2015.QH13": {
        "doc_code": "84_2015_QH13",
        "doc_name": "Luật An toàn, vệ sinh lao động",
        "doc_type": "Luật",
        "so_hieu": "84/2015/QH13",
        "ngay_hieu_luc": "2016-07-01",
        "trang_thai_chung": "het_hieu_luc_mot_phan",
        "ghi_chu": "Hết hiệu lực một phần",
    },
    "hienphap": {
        "doc_code": "HP_2013",
        "doc_name": "Hiến pháp 2013",
        "doc_type": "Hiến pháp",
        "so_hieu": "Hiến pháp 2013",
        "ngay_hieu_luc": "2014-01-01",
        "trang_thai_chung": "con_hieu_luc",
        "ghi_chu": "",
    },
    "LuatCongDoan": {
        "doc_code": "50_2024_QH15",
        "doc_name": "Luật Công đoàn",
        "doc_type": "Luật",
        "so_hieu": "50/2024/QH15",
        "ngay_hieu_luc": "2025-07-01",
        "trang_thai_chung": "het_hieu_luc_mot_phan",
        "ghi_chu": "Hết hiệu lực một phần",
    },
    "LuatViecLam": {
        "doc_code": "74_2025_QH15",
        "doc_name": "Luật Việc làm",
        "doc_type": "Luật",
        "so_hieu": "74/2025/QH15",
        "ngay_hieu_luc": "2026-01-01",
        "trang_thai_chung": "con_hieu_luc",
        "ghi_chu": "",
    },
    "luatnguoikhuyettat": {
        "doc_code": "51_2010_QH12",
        "doc_name": "Luật Người khuyết tật",
        "doc_type": "Luật",
        "so_hieu": "51/2010/QH12",
        "ngay_hieu_luc": "2011-01-01",
        "trang_thai_chung": "het_hieu_luc_mot_phan",
        "ghi_chu": "Hết hiệu lực một phần",
    },
    "10.2012.QH13": {
        "doc_code": "10_2012_QH13",
        "doc_name": "Bộ luật Lao động 2012",
        "doc_type": "Bộ luật",
        "so_hieu": "10/2012/QH13",
        "ngay_hieu_luc": "2013-05-01",
        "trang_thai_chung": "het_hieu_luc",
        "ghi_chu": "Hết hiệu lực, thay thế bởi 45/2019/QH14",
    },
    "LuatThanhTra": {
        "doc_code": "84_2025_QH15",
        "doc_name": "Luật Thanh tra",
        "doc_type": "Luật",
        "so_hieu": "84/2025/QH15",
        "ngay_hieu_luc": "2025-07-01",
        "trang_thai_chung": "het_hieu_luc_mot_phan",
        "ghi_chu": "Hết hiệu lực một phần",
    },
    "LuatBaoVeDuLieuCaNhan": {
        "doc_code": "91_2025_QH15",
        "doc_name": "Luật Bảo vệ dữ liệu cá nhân",
        "doc_type": "Luật",
        "so_hieu": "91/2025/QH15",
        "ngay_hieu_luc": "2026-01-01",
        "trang_thai_chung": "con_hieu_luc",
        "ghi_chu": "",
    },
    "Luật_số_69.2020.QH14": {
        "doc_code": "69_2020_QH14",
        "doc_name": "Luật Người lao động Việt Nam đi làm việc ở nước ngoài theo hợp đồng",
        "doc_type": "Luật",
        "so_hieu": "69/2020/QH14",
        "ngay_hieu_luc": "2022-01-01",
        "trang_thai_chung": "con_hieu_luc",
        "ghi_chu": "",
    },
    # --- Nghị định ---
    "Nghị_định_số_145.2020.NĐ-CP": {
        "doc_code": "145_2020_NDCP",
        "doc_name": "Nghị định 145/2020/NĐ-CP",
        "doc_type": "Nghị định",
        "so_hieu": "145/2020/NĐ-CP",
        "ngay_hieu_luc": "2021-02-01",
        "trang_thai_chung": "het_hieu_luc_mot_phan",
        "ghi_chu": "Hết hiệu lực một phần. Hướng dẫn BLLĐ về điều kiện lao động và quan hệ lao động",
    },
    "Nghị_định_số_293.2025.NĐ-CP": {
        "doc_code": "293_2025_NDCP",
        "doc_name": "Nghị định 293/2025/NĐ-CP",
        "doc_type": "Nghị định",
        "so_hieu": "293/2025/NĐ-CP",
        "ngay_hieu_luc": "2026-01-01",
        "trang_thai_chung": "con_hieu_luc",
        "ghi_chu": "Mức lương tối thiểu",
    },
    "Nghị_định_số_152.2020.NĐ-CP": {
        "doc_code": "152_2020_NDCP",
        "doc_name": "Nghị định 152/2020/NĐ-CP",
        "doc_type": "Nghị định",
        "so_hieu": "152/2020/NĐ-CP",
        "ngay_hieu_luc": "2021-02-15",
        "trang_thai_chung": "het_hieu_luc_mot_phan",
        "ghi_chu": "Hết hiệu lực một phần. Lao động nước ngoài làm việc tại Việt Nam",
    },
    "Nghị_định_số_12.2022.NĐ-CP": {
        "doc_code": "12_2022_NDCP",
        "doc_name": "Nghị định 12/2022/NĐ-CP",
        "doc_type": "Nghị định",
        "so_hieu": "12/2022/NĐ-CP",
        "ngay_hieu_luc": "2022-01-17",
        "trang_thai_chung": "con_hieu_luc",
        "ghi_chu": "Xử phạt vi phạm hành chính trong lĩnh vực lao động",
    },
    "Nghị_định_số_70.2023.NĐ-CP": {
        "doc_code": "70_2023_NDCP",
        "doc_name": "Nghị định 70/2023/NĐ-CP",
        "doc_type": "Nghị định",
        "so_hieu": "70/2023/NĐ-CP",
        "ngay_hieu_luc": "2023-09-18",
        "trang_thai_chung": "het_hieu_luc_mot_phan",
        "ghi_chu": "Hết hiệu lực một phần. Sửa đổi NĐ 152/2020 về lao động nước ngoài",
    },
    "ND_luatbaovedulieu": {
        "doc_code": "356_2025_NDCP",
        "doc_name": "Nghị định 356/2025/NĐ-CP",
        "doc_type": "Nghị định",
        "so_hieu": "356/2025/NĐ-CP",
        "ngay_hieu_luc": "2026-01-01",
        "trang_thai_chung": "con_hieu_luc",
        "ghi_chu": "Hướng dẫn thi hành Luật Bảo vệ dữ liệu cá nhân",
    },
}


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
    r'^[ \t]*Đi[eề]u[ \t]+(\d+)\b\.?[ \t]*(.*)',
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
        "hieu_luc": doc_info.get("trang_thai_chung", "con_hieu_luc"),
        "ngay_hieu_luc": doc_info.get("ngay_hieu_luc", ""),
        "ngay_het_hieu_luc": doc_info.get("ngay_het_hieu_luc", ""),
        "van_ban_sua_doi": "",
        "ghi_chu": doc_info.get("ghi_chu", ""),
    }


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
