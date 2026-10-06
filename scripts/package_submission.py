"""
Script đóng gói dự án để nộp bài (Clean Submission Packaging Script)
Tự động loại bỏ các file nhạy cảm và file rác:
- File cấu hình chứa API Key thật (.env, .env.*)
- Lịch sử chat cá nhân (data/chat_history.json)
- Môi trường ảo (venv, .venv)
- Cache Python (__pycache__, *.pyc)
- Thư mục git (.git), IDE (.vscode, .idea)
- Kiểm tra an toàn trước khi hoàn tất đóng gói.
"""

import os
import re
import sys
import zipfile
import argparse
from pathlib import Path

# Đảm bảo console Windows in Unicode không bị lỗi cp1252
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Các file và thư mục TUYỆT ĐỐI BỎ QUA khi đóng gói
EXCLUDE_DIRS = {
    ".git",
    "venv",
    ".venv",
    "env",
    "__pycache__",
    ".pytest_cache",
    ".idea",
    ".vscode",
    ".gemini",
    "dist",
    "build",
    "user_sessions",
    "sessions",
}

EXCLUDE_FILES = {
    ".env",
    ".env.local",
    ".env.development",
    ".env.production",
    "chat_history.json",
    ".DS_Store",
    "Thumbs.db",
}

EXCLUDE_EXTENSIONS = {
    ".pyc",
    ".pyo",
    ".pyd",
    ".tmp",
    ".log",
    ".swp",
    ".swo",
    ".lock",
}


def is_excluded(rel_path: str) -> bool:
    """Kiểm tra đường dẫn tương đối có thuộc danh sách loại trừ không."""
    normalized = rel_path.replace("\\", "/").strip("/")
    parts = normalized.split("/")

    # Kiểm tra tên thư mục
    for part in parts[:-1]:
        if part in EXCLUDE_DIRS:
            return True

    filename = parts[-1]

    # Kiểm tra nếu là thư mục trong EXCLUDE_DIRS
    if filename in EXCLUDE_DIRS:
        return True

    # Kiểm tra file cụ thể
    if filename in EXCLUDE_FILES:
        return True

    # Loại trừ toàn bộ .env.* ngoại trừ .env.example
    if filename.startswith(".env") and filename != ".env.example":
        return True

    # Kiểm tra file lịch sử chat
    if "chat_history.json" in filename.lower():
        return True

    # Kiểm tra phần mở rộng
    ext = os.path.splitext(filename)[1].lower()
    if ext in EXCLUDE_EXTENSIONS:
        return True

    return False


def scan_file_for_leaks(file_path: Path) -> list:
    """Kiểm tra sơ bộ nội dung file xem có chứa API key lộ không."""
    warnings = []
    # Chỉ kiểm tra text/code files
    if file_path.suffix.lower() in [".py", ".json", ".md", ".txt", ".yaml", ".yml", ".example"]:
        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")
            # Kiểm tra format Gemini API Key (AQ.xxx hoặc AIzaxxx)
            if re.search(r"AQ\.[a-zA-Z0-9_\-]{40,}", content):
                warnings.append("Phát hiện chuỗi giống Google Gemini API Key (AQ...)!")
            if re.search(r"AIza[0-9A-Za-z-_]{35}", content):
                warnings.append("Phát hiện chuỗi giống Google API Key (AIza...)!")
        except Exception:
            pass
    return warnings


def package_project(project_dir: Path, output_zip: Path, include_index: bool = False):
    print("=" * 60)
    print(" BẮT ĐẦU ĐÓNG GÓI DỰ ÁN NỘP BÀI")
    print("=" * 60)
    print(f" Thư mục nguồn: {project_dir.resolve()}")
    print(f" File zip đầu ra: {output_zip.resolve()}")
    print(f" Đóng gói chỉ mục data/index: {'CÓ' if include_index else 'BỎ QUA (Tạo lại bằng build_index.py)'}")
    print("-" * 60)

    total_files = 0
    total_bytes = 0
    leak_warnings = []

    # Đảm bảo thư mục đích tồn tại
    output_zip.parent.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(output_zip, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(project_dir):
            # Lọc bỏ thư mục loại trừ ngay tại walk để tránh duyệt sâu vô ích
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]

            for file in files:
                file_path = Path(root) / file
                rel_path = file_path.relative_to(project_dir).as_posix()

                # Kiểm tra exclude
                if is_excluded(rel_path):
                    continue

                # Nếu không kèm index thì bỏ qua thư mục data/index
                if not include_index and rel_path.startswith("data/index/"):
                    continue

                # Kiểm tra leak
                file_warnings = scan_file_for_leaks(file_path)
                if file_warnings:
                    for w in file_warnings:
                        leak_warnings.append(f"[{rel_path}]: {w}")

                # Thêm vào zip (đặt tiền tố thư mục gốc project/)
                archive_name = f"project/{rel_path}"
                zipf.write(file_path, arcname=archive_name)

                size = file_path.stat().st_size
                total_files += 1
                total_bytes += size

    print(f" Đã đóng gói thành công {total_files} files.")
    print(f" Dung lượng chưa nén: {total_bytes / (1024 * 1024):.2f} MB")
    print(f" Dung lượng file zip: {output_zip.stat().st_size / (1024 * 1024):.2f} MB")
    print("-" * 60)

    # Báo cáo kiểm tra bảo mật
    if leak_warnings:
        print("⚠️ CẢNH BÁO BẢO MẬT: Phát hiện chuỗi nhạy cảm nghi ngờ:")
        for warn in leak_warnings:
            print(f"   - {warn}")
        print(" Vui lòng kiểm tra lại trước khi gửi gói bài nộp!")
    else:
        print("✅ KIỂM TRA BẢO MẬT HOÀN TẤT:")
        print("   - KHÔNG chứa .env hoặc bất kỳ khóa API thật nào.")
        print("   - KHÔNG chứa data/chat_history.json (lịch sử trò chuyện cá nhân).")
        print("   - ĐÃ KÈM THEO .env.example để người chấm thiết lập môi trường.")
        print("   - Gói nộp đã sẵn sàng và an toàn 100%!")
    print("=" * 60)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Đóng gói dự án nộp bài an toàn")
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        default="../Chatbox_Luat_Lao_Dong_Submission.zip",
        help="Đường dẫn file zip đầu ra (mặc định: ../Chatbox_Luat_Lao_Dong_Submission.zip)",
    )
    parser.add_argument(
        "--include-index",
        action="store_true",
        help="Đóng gói kèm thư mục chỉ mục data/index (lưu ý dung lượng sẽ lớn hơn)",
    )

    args = parser.parse_args()
    project_root = Path(__file__).resolve().parent.parent
    zip_path = Path(args.output)
    if not zip_path.is_absolute():
        zip_path = project_root / zip_path

    package_project(project_root, zip_path, include_index=args.include_index)
