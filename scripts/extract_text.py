# -*- coding: utf-8 -*-
"""
extract_text.py – Trích xuất và làm sạch text từ các file PDF pháp luật.

Quét tất cả file .pdf trong thư mục TT/ (bao gồm các thư mục con Nhom_1 – Nhom_6),
trích xuất text bằng pdfplumber (ưu tiên) hoặc PyMuPDF (fallback), làm sạch, và lưu vào project/data/clean/.
"""

import os
import re
import sys
import json
import shutil
from pathlib import Path

# Đường dẫn gốc
BASE_DIR = Path(__file__).resolve().parent.parent.parent  # TT/
DATA_RAW = BASE_DIR / "project" / "data" / "raw"
DATA_CLEAN = BASE_DIR / "project" / "data" / "clean"

# Ngưỡng tối thiểu ký tự để coi là trích xuất thành công
MIN_CHARS = 500


def find_all_pdfs(base_dir: Path) -> list[Path]:
    """Tìm tất cả file PDF trong thư mục TT/ và các thư mục con."""
    pdfs = []
    for root, dirs, files in os.walk(base_dir):
        if "project" in root:
            continue
        for f in files:
            if f.lower().endswith(".pdf"):
                pdfs.append(Path(root) / f)
    return sorted(pdfs)


def extract_with_pdfplumber(pdf_path: Path) -> str:
    """Trích xuất text bằng pdfplumber."""
    try:
        import pdfplumber
        text_parts = []
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)
        return "\n".join(text_parts)
    except Exception:
        return ""


def extract_with_pymupdf(pdf_path: Path) -> str:
    """Trích xuất text bằng PyMuPDF (fitz) – tốt hơn với signed/encrypted PDF."""
    try:
        import fitz  # PyMuPDF
        text_parts = []
        doc = fitz.open(str(pdf_path))
        for page in doc:
            page_text = page.get_text("text")
            if page_text:
                text_parts.append(page_text)
        doc.close()
        return "\n".join(text_parts)
    except Exception:
        return ""


def extract_text_from_pdf(pdf_path: Path) -> tuple[str, str]:
    """
    Trích xuất text từ PDF, thử pdfplumber trước, rồi PyMuPDF.
    Trả về (text, method).
    """
    text = extract_with_pdfplumber(pdf_path)
    if text and len(text.strip()) > MIN_CHARS:
        return text, "pdfplumber"

    text = extract_with_pymupdf(pdf_path)
    if text and len(text.strip()) > MIN_CHARS:
        return text, "PyMuPDF"

    return "", "none"


def clean_text(raw_text: str, filename: str) -> str:
    """Làm sạch text đã trích xuất."""
    text = raw_text

    # 1. Loại bỏ header/footer CÔNG BÁO (rất phổ biến trong văn bản pháp luật VN)
    # Dạng: "CÔNG BÁO/Số XXX + XXX/Ngày DD-MM-YYYY [số trang]"
    # hoặc: "[số trang] CÔNG BÁO/Số XXX..."
    text = re.sub(
        r'(?m)^\s*\d*\s*C[OÔ]NG B[AÁ]O/S[oố]\s*\d+[^/\n]*/Ng[aà]y\s*[\d\-]+\s*\d*\s*$',
        '', text, flags=re.IGNORECASE
    )

    # 2. Loại bỏ số trang dạng phổ biến
    text = re.sub(r'(?m)^\s*-?\s*\d{1,3}\s*-?\s*$', '', text)
    text = re.sub(r'(?mi)^\s*(Trang|Page)\s*\d+\s*$', '', text)

    # 3. Loại bỏ header/footer lặp (dòng giống nhau xuất hiện > 3 lần)
    lines = text.split('\n')
    line_count = {}
    for line in lines:
        stripped = line.strip()
        if stripped and len(stripped) > 3:
            line_count[stripped] = line_count.get(stripped, 0) + 1
    repeated_lines = {line for line, count in line_count.items() if count > 3}
    lines = [l for l in lines if l.strip() not in repeated_lines]
    text = '\n'.join(lines)

    # 4. Chuẩn hóa khoảng trắng
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r' +\n', '\n', text)

    # 5. Sửa lỗi OCR phổ biến
    text = text.replace('\ufb01', 'fi')
    text = text.replace('\ufb02', 'fl')
    text = text.replace('\ufb00', 'ff')
    text = text.replace('\u00a0', ' ')   # non-breaking space
    text = text.replace('\u200b', '')    # zero-width space
    text = text.replace('\u200c', '')    # zero-width non-joiner
    text = text.replace('\u200d', '')    # zero-width joiner
    text = text.replace('\ufeff', '')    # BOM

    # 6. Chuẩn hóa dấu câu
    text = re.sub(r'\s+([.,;:!?])', r'\1', text)
    text = re.sub(r'([.,;:!?])(?=[^\s\d\n"\')}\]])', r'\1 ', text)

    # 7. Strip
    text = text.strip()

    return text


def copy_pdf_to_raw(pdf_path: Path):
    """Copy file PDF gốc vào thư mục data/raw/."""
    dest = DATA_RAW / pdf_path.name
    if not dest.exists():
        shutil.copy2(pdf_path, dest)


def main():
    print("=" * 60)
    print("TRICH XUAT VA LAM SACH TEXT TU PDF PHAP LUAT")
    print("=" * 60)

    DATA_RAW.mkdir(parents=True, exist_ok=True)
    DATA_CLEAN.mkdir(parents=True, exist_ok=True)

    pdfs = find_all_pdfs(BASE_DIR)
    print(f"\nTim thay {len(pdfs)} file PDF:\n")

    results = []
    success_count = 0
    failed = []

    for i, pdf_path in enumerate(pdfs):
        rel_path = pdf_path.relative_to(BASE_DIR)
        print(f"[{i+1}/{len(pdfs)}] Dang xu ly: {rel_path}")

        raw_text, method = extract_text_from_pdf(pdf_path)
        if not raw_text:
            print(f"  -> Bo qua (khong trich xuat duoc text hoac qua ngan < {MIN_CHARS} ky tu)")
            failed.append(str(rel_path))
            continue

        clean = clean_text(raw_text, pdf_path.name)

        # Kiểm tra lại sau khi clean
        if len(clean) < MIN_CHARS:
            print(f"  -> Bo qua (text qua ngan sau khi lam sach: {len(clean)} ky tu)")
            failed.append(str(rel_path))
            continue

        stem = pdf_path.stem
        safe_stem = re.sub(r'[^\w\-.]', '_', stem)
        output_path = DATA_CLEAN / f"{safe_stem}.txt"

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(clean)

        copy_pdf_to_raw(pdf_path)

        stats = {
            "source": str(rel_path),
            "output": str(output_path.name),
            "method": method,
            "raw_chars": len(raw_text),
            "clean_chars": len(clean),
            "clean_lines": len(clean.split('\n')),
        }
        results.append(stats)
        success_count += 1
        print(f"  -> Da luu: {output_path.name} ({stats['clean_chars']:,} ky tu, {stats['clean_lines']:,} dong) [{method}]")

    report = {
        "extracted": results,
        "failed": failed,
        "summary": {
            "total_pdfs": len(pdfs),
            "success": success_count,
            "failed": len(failed),
        }
    }
    report_path = DATA_CLEAN / "_extraction_report.json"
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"\n{'=' * 60}")
    print(f"HOAN TAT: Da xu ly {success_count}/{len(pdfs)} file PDF")
    if failed:
        print(f"\nCac file khong doc duoc ({len(failed)}):")
        for f_name in failed:
            print(f"  - {f_name}")
    print(f"\nKet qua luu tai: {DATA_CLEAN}")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
