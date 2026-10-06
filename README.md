# ⚖️ CHATBOT HỖ TRỢ TRA CỨU QUY ĐỊNH PHÁP LUẬT LAO ĐỘNG
> **Đồ án môn học / Nghiên cứu:** Xây dựng hệ thống Hỏi - Đáp (QA) Pháp luật Lao động có kiểm chứng căn cứ pháp lý và quản lý hiệu lực văn bản bằng mô hình Retrieval-Augmented Generation (RAG).

---

## MỤC LỤC
1. [Giới thiệu Đề tài & Phạm vi Corpus](#1-giới-thiệu-đề-tài--phạm-vi-corpus)
2. [Kiến trúc Kỹ thuật (RAG Pipeline)](#2-kiến-trúc-kỹ-thuật-rag-pipeline)
3. [Cấu trúc Thư mục Dự án](#3-cấu-trúc-thư-mục-dự-án)
4. [Yêu cầu Hệ thống](#4-yêu-cầu-hệ-thống)
5. [Hướng dẫn Cài đặt Chi tiết (Từng bước)](#5-hướng-dẫn-cài-đặt-chi-tiết-từng-bước)
6. [Hướng dẫn Chạy Ứng dụng Giao diện Web (Streamlit)](#6-hướng-dẫn-chạy-ứng-dụng-giao-diện-web-streamlit)
7. [Hướng dẫn Chạy Thực nghiệm & Đánh giá (Benchmark)](#7-hướng-dẫn-chạy-thực-nghiệm--đánh-giá-benchmark)
8. [Hướng dẫn Đóng gói Nộp bài An toàn](#8-hướng-dẫn-đóng-gói-nộp-bài-an-toàn)
9. [Xử lý Sự cố Thường gặp (Troubleshooting)](#9-xử-lý-sự-cố-thường-gặp-troubleshooting)

---

## 1. GIỚI THIỆU ĐỀ TÀI & PHẠM VI CORPUS

Hệ thống được xây dựng nhằm giải quyết bài toán tra cứu văn bản pháp luật lao động Việt Nam một cách **nhanh chóng, chính xác và minh bạch**, giải quyết triệt để vấn đề "ảo giác" (hallucination) của các mô hình ngôn ngữ lớn (LLM).

###  Danh mục Văn bản Pháp luật trong Cơ sở dữ liệu:
1. **Bộ luật Lao động 2019** (`45/2019/QH14`) — Còn hiệu lực.
2. **Nghị định 145/2020/NĐ-CP** — Quy định chi tiết và hướng dẫn thi hành một số điều của Bộ luật Lao động.
3. **Luật Bảo hiểm xã hội** (`58/VBHN-VPQH`) — Văn bản hợp nhất số 58.
4. **Luật An toàn, vệ sinh lao động 2015** (`84/2015/QH13`).
5. **Luật Công đoàn 2024** (`50/2024/QH15`).
6. **Bộ luật Lao động 2012** (`10/2012/QH13`) — Hết hiệu lực (dùng đối sánh lịch sử hiệu lực).

### Cơ chế Quản lý Dữ liệu:
- Dữ liệu được bóc tách và phân rã chính xác tới **cấp Khoản** (hoặc cấp Điều đối với Điều không chia Khoản).
- Mỗi đơn vị dữ liệu được định danh bằng mã duy nhất (`provision_id`), ví dụ: `45_2019_QH14__D113__K1`.
- Quản lý trạng thái hiệu lực: `con_hieu_luc` (còn hiệu lực) và `het_hieu_luc` (hết hiệu lực).

---

## 2. KIẾN TRÚC KỸ THUẬT (RAG PIPELINE)

```
       [Câu hỏi của Người dùng]
                  │
                  ▼
       [Tầng Chuẩn hóa & Mở rộng Từ khóa]
       (Xử lý từ viết tắt, tiếng lóng đời thường)
                  │
        ┌─────────┴─────────┐
        ▼                   ▼
 [BM25 Retrieval]   [Dense Retrieval]
 (PyVi tách từ)     (bkai-foundation-models/vietnamese-bi-encoder + FAISS)
        └─────────┬─────────┘
                  ▼
     [Hybrid Fusion — RRF (k=10, α=0.5)]
                  │
                  ▼
     [Lọc Hiệu lực Văn bản & Mở rộng Ngữ cảnh Điều luật]
     (Sibling Provision Expansion: gom các Khoản liên quan)
                  │
                  ▼
     [LLM Generation — Gemini 3.5 Flash Lite]
     (Strict System Prompt: Grounding + Colloquial Mapping + Anti-hallucination)
                  │
                  ▼
     [Citation Verification Layer]
     (Kiểm chứng mã trích dẫn hợp lệ, loại bỏ trích dẫn ảo)
                  │
                  ▼
     [Giao diện Chatbot Streamlit + Panel Nguồn Pháp lý]
```

---

## 3. CẤU TRÚC THƯ MỤC DỰ ÁN

```
project/
│
├── app.py                      # Ứng dụng Web Chatbot (Streamlit)
├── requirements.txt            # Danh sách thư viện phụ thuộc của toàn bộ dự án
├── .env.example                # File mẫu cấu hình biến môi trường (không chứa khóa thật)
├── README.md                   # Tài liệu hướng dẫn cài đặt và sử dụng
│
├── data/                       # Thư mục dữ liệu và chỉ mục tìm kiếm
│   ├── corpus_chunks.jsonl     # Toàn bộ các đoạn quy định pháp luật đã tiền xử lý
│   ├── bm25_index.pkl          # File chỉ mục BM25 lưu trên đĩa
│   ├── faiss_index.bin         # File chỉ mục vector FAISS
│   ├── id_mapping.json         # Bản đồ ánh xạ provision_id và index
│   └── eval/                   # Bộ dữ liệu test và kết quả thực nghiệm (JSON, JSONL)
│
├── docs/                       # Tài liệu nghiên cứu, danh mục corpus
│   └── corpus_catalog.md       # Chi tiết danh mục văn bản và ngày snapshot
│
└── scripts/                    # Các module mã nguồn cốt lõi
    ├── retriever.py            # Module tìm kiếm Hybrid (BM25 + FAISS + RRF + Sibling Expansion)
    ├── generator.py            # Module tạo câu trả lời với LLM & Citation Verification
    ├── create_test_set.py      # Script sinh bộ câu hỏi kiểm thử chuẩn (155 câu)
    ├── run_experiments.py      # Script chạy thực nghiệm tự động đánh giá các chỉ số
    └── package_submission.py   # Script đóng gói nộp bài an toàn (tự động loại trừ .env & history)
```

---

## 4. YÊU CẦU HỆ THỐNG

- **Hệ điều hành:** Windows 10/11, macOS hoặc Linux (Ubuntu 20.04+).
- **Phiên bản Python:** Python `3.10` hoặc `3.11` (khuyến nghị `3.11`).
- **Bộ nhớ RAM:** Tối thiểu 8 GB RAM (khuyến nghị 16 GB để nạp mô hình embedding mượt mà).
- **Bộ nhớ ổ đĩa trống:** Tối thiểu 3 GB trống (cho mô hình PyTorch, FAISS và Corpus).
- **Kết nối mạng Internet:** Cần thiết để tải mô hình ban đầu và gọi API Google Gemini.

---

## 5. HƯỚNG DẪN CÀI ĐẶT CHI TIẾT (TỪNG BƯỚC)

### Bước 1: Mở Terminal tại thư mục dự án
Mở PowerShell / Command Prompt / Terminal và điều hướng vào thư mục `project`:
```bash
cd /d c:\Users\Admin\Downloads\TT\project
```
*(Thay đổi đường dẫn phù hợp với máy của bạn).*

---

### Bước 2: Tạo và kích hoạt môi trường ảo (Virtual Environment)
Khuyến nghị tạo môi trường ảo độc lập để tránh xung đột thư viện:

- **Trên Windows (PowerShell):**
  ```powershell
  python -m venv venv
  .\venv\Scripts\Activate.ps1
  ```
  *(Nếu gặp lỗi PowerShell Execution Policy, chạy lệnh: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` rồi kích hoạt lại).*

- **Trên Windows (Command Prompt - cmd):**
  ```cmd
  python -m venv venv
  venv\Scripts\activate.bat
  ```

- **Trên Linux / macOS:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

---

### Bước 3: Cài đặt các thư viện phụ thuộc
Nâng cấp `pip` và cài đặt toàn bộ gói thư viện từ file `requirements.txt`:
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

> **Ghi chú về PyTorch:** Nếu máy tính của bạn có card đồ họa NVIDIA (CUDA), bạn có thể cài phiên bản PyTorch hỗ trợ GPU để tăng tốc độ nạp mô hình embedding từ [trang chủ PyTorch](https://pytorch.org/). Nếu chạy CPU thông thường, gói `torch` mặc định trong `requirements.txt` đã hoạt động tốt.

---

### Bước 4: Thiết lập Khóa API (Google Gemini API Key)
Mô hình sử dụng `gemini-3.5-flash-lite` thông qua Google GenAI SDK.
1. Truy cập [Google AI Studio](https://aistudio.google.com/app/apikey) để tạo API Key miễn phí.
2. Sao chép file `.env.example` thành file `.env` cá nhân:
   - **Trên Windows (PowerShell / CMD):**
     ```powershell
     copy .env.example .env
     ```
   - **Trên Linux / macOS:**
     ```bash
     cp .env.example .env
     ```
3. Mở file `.env` vừa tạo và điền API Key thực tế của bạn:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```
> ⚠️ **Lưu ý an toàn:** File `.env` chứa khóa bí mật cá nhân và đã được đưa vào `.gitignore`. Tuyệt đối không commit file này lên Git hoặc chia sẻ cho người khác.

---

### Bước 5: Xây dựng chỉ mục tìm kiếm (BM25 & FAISS Vector Index)
Do thư mục `data/index/` có dung lượng lớn và nằm trong `.gitignore`, khi thiết lập trên máy mới hoặc clone repo, bạn cần chạy script sau **một lần** để xây dựng chỉ mục tìm kiếm:
```bash
python scripts/build_index.py
```
*(Script sẽ tự động đọc `corpus.json`, xây dựng chỉ mục BM25 lưu tại `data/index/bm25_index.pkl` và mô hình hóa vector Dense lưu tại `data/index/faiss_index.bin` trong khoảng 1–2 phút).*

---

### 💡 Khởi chạy nhanh bằng một dòng lệnh (One-command Setup):
Sau khi đã cấu hình file `.env`, bạn có thể thực hiện toàn bộ quy trình chỉ bằng một câu lệnh:
- **Trên Windows (PowerShell):**
  ```powershell
  pip install -r requirements.txt; python scripts/build_index.py; streamlit run app.py
  ```
- **Trên Linux / macOS (Bash):**
  ```bash
  pip install -r requirements.txt && python scripts/build_index.py && streamlit run app.py
  ```

---

## 6. HƯỚNG DẪN CHẠY ỨNG DỤNG GIAO DIỆN WEB (STREAMLIT)

### Khởi chạy ứng dụng:
Tại thư mục `project/` (trong môi trường ảo đã kích hoạt), thực thi lệnh:
```bash
streamlit run app.py
```

Sau vài giây, Streamlit sẽ khởi động máy chủ cục bộ và hiển thị thông báo:
```text
  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```
Trình duyệt web mặc định sẽ tự động mở trang web tra cứu. Nếu không tự mở, hãy truy cập thủ công địa chỉ: `http://localhost:8501`.

### Các tính năng nổi bật trên giao diện:
1. **Khung hội thoại tương tác tức thì:** Câu hỏi được hiển thị ngay kèm đồng hồ thời gian và hiệu ứng loading trong khi hệ thống tra cứu.
2. **Cột hiển thị nguồn trích dẫn pháp lý (Bên phải):**
   - Đánh nhãn trạng thái trực quan: **Còn hiệu lực** (màu xanh lá) và **Hết hiệu lực** (màu đỏ).
   - Hiển thị trích đoạn ngắn và cho phép bấm *"Xem chi tiết ▾"* để đọc toàn văn điều khoản.
3. **Quản lý đa cuộc trò chuyện:**
   - Nút `＋ Cuộc trò chuyện mới` trên thanh Sidebar cho phép mở nhiều phiên hỏi đáp song song.
   - Lịch sử trò chuyện được lưu trữ và có thể chuyển đổi linh hoạt.
4. **Gợi ý câu hỏi mẫu:** Tích hợp sẵn các câu hỏi mẫu phổ biến về thử việc, nghỉ phép, hợp đồng lao động giúp người dùng thử nghiệm nhanh.

---

## 7. HƯỚNG DẪN CHẠY THỰC NGHIỆM & ĐÁNH GIÁ (BENCHMARK)

Dự án có sẵn quy trình đánh giá khoa học định lượng (Quantitative Evaluation) phục vụ báo cáo đồ án:

### Bước 7.1: Khởi tạo bộ câu hỏi kiểm thử (Test Set)
Tạo bộ dữ liệu chuẩn 155 câu hỏi (bao gồm câu hỏi dễ, trung bình, phức tạp, đa bước, lịch sử hiệu lực và câu hỏi ngoài phạm vi):
```bash
python scripts/create_test_set.py
```
File kết quả sẽ được lưu tại: `data/eval/test_set.json`.

### Bước 7.2: Chạy thực nghiệm đánh giá Retrieval & Generation
Chạy toàn bộ pipeline kiểm thử để đo lường các chỉ số: Recall@k, MRR, Citation Exact Match, Refusal Accuracy, Latency:
```bash
python scripts/run_experiments.py
```
Kết quả tổng hợp sẽ tự động được ghi lại tại: `data/eval/generation_metrics.json`.

---

## 8. HƯỚNG DẪN ĐÓNG GÓI NỘP BÀI AN TOÀN

Để nộp bài chấm đồ án mà **không bị lộ khóa bí mật API** và **không kèm lịch sử thử nghiệm rác**:
Chạy script đóng gói tự động:
```bash
python scripts/package_submission.py
```
Script sẽ tự động:
- Loại bỏ toàn bộ file cấu hình chứa API Key thật (`.env`, `.env.*`).
- Loại bỏ lịch sử chat cá nhân khi thử nghiệm (`data/chat_history.json`).
- Loại bỏ thư mục ảo `venv/`, cache `__pycache__/`, thư mục `.git/`.
- Tự động đính kèm file template chuẩn `.env.example`.
- Quét kiểm tra bảo mật (Secret Scanning) và xuất file zip nộp bài sạch sẽ tại: `../Chatbox_Luat_Lao_Dong_Submission.zip`.

---

## 9. XỬ LÝ SỰ CỐ THƯỜNG GẶP (TROUBLESHOOTING)

| Hiện tượng / Lỗi | Nguyên nhân | Hướng khắc phục |
|---|---|---|
| `GEMINI_API_KEY không tìm thấy` | Chưa có file `.env` hoặc file `.env` đặt sai thư mục. | Đảm bảo copy `.env.example` thành `.env` nằm ngay trong thư mục `project/` và chứa dòng `GEMINI_API_KEY=...`. |
| `Port 8501 is already in use` | Có một tiến trình Streamlit khác đang chạy ngầm. | Chạy lệnh chỉ định cổng khác: `streamlit run app.py --server.port 8502`. |
| Lỗi mã hóa font chữ Tiếng Việt trên Windows cmd | Bảng mã mặc định của Windows console là CP1252. | Chạy lệnh `chcp 65001` trước khi chạy script hoặc sử dụng PowerShell / Windows Terminal. |
| Quá trình nạp mô hình mất nhiều thời gian ở lần chạy đầu | Mô hình `vietnamese-bi-encoder` đang được tải tự động từ HuggingFace (~500MB). | Chờ hoàn tất tải về; từ lần chạy thứ hai trở đi mô hình sẽ được nạp trực tiếp từ cache cục bộ (mất ~5-10 giây). |
| Cảnh báo `Redirects are currently not supported in Windows` | Cảnh báo mặc định của thư viện PyTorch khi chạy đa luồng trên Windows. | Đây là cảnh báo vô hại, không ảnh hưởng đến độ chính xác và hoạt động của hệ thống. |

---

##  TÁC GIẢ & BẢN QUYỀN
- **Đề tài:** Hệ thống Chatbot hỗ trợ tra cứu một số quy định về pháp luật về lao động.
- **Nguồn dữ liệu pháp luật:** Cổng thông tin điện tử Cơ sở dữ liệu Quốc gia về Văn bản Pháp luật (vbpl.vn / chinhphu.vn).
- **Mã nguồn:** Dự án phục vụ mục đích học tập và nghiên cứu khoa học.
