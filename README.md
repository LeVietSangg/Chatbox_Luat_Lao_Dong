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

Hệ thống được xây dựng nhằm giải quyết bài toán tra cứu văn bản pháp luật lao động Việt Nam một cách **nhanh chóng, chính xác và minh bạch**, giảm thiểu tối đa hiện tượng "ảo giác" (hallucination) của các mô hình ngôn ngữ lớn (LLM) thông qua kiến trúc RAG kiểm chứng đa tầng.

### 📋 Thống nhất Danh mục Dữ liệu (Corpus Overview):
Toàn bộ cơ sở dữ liệu tra cứu và chỉ mục (BM25 & FAISS) được xây dựng từ **17 văn bản quy phạm pháp luật** với tổng cộng **4,890 đoạn quy định (chunks) + 49 đoạn đc chép tay từ file overrides.py (để thay thế cho các chunk bị hết hiệu lực trong các văn bản mạng trạng thái hết hiệu lực một phần)**, phân rã tới cấp Khoản và lùi về Điều nếu không có Khoản. Chi tiết danh mục và ngày snapshot được chuẩn hóa tại [docs/corpus_catalog.md](docs/corpus_catalog.md).

Nhằm phục vụ đánh giá khoa học và mô phỏng thực tế kho pháp điển quốc gia, 17 văn bản trong cùng một chỉ mục chung (Shared Index) được phân loại thành **3 nhóm vai trò chức năng**:

#### Nhóm 1: Văn bản Cốt lõi & Quy định Hướng dẫn Pháp luật Lao động (12 văn bản — 3,352 chunks)
Các văn bản in-domain trực tiếp điều chỉnh quyền, nghĩa vụ và chế độ của người lao động:
1. **Bộ luật Lao động 2019** (`45/2019/QH14`) — 678 chunks (Văn bản nền tảng, còn hiệu lực).
2. **Nghị định 145/2020/NĐ-CP** — 390 chunks (Quy định chi tiết thi hành Bộ luật Lao động về điều kiện lao động, quan hệ lao động).
3. **Nghị định 12/2022/NĐ-CP** — 323 chunks (Quy định xử phạt vi phạm hành chính trong lĩnh vực lao động, BHXH).
4. **Nghị định 152/2020/NĐ-CP** — 162 chunks (Quản lý người lao động nước ngoài tại VN và tuyển dụng NLĐ VN cho tổ chức nước ngoài).
5. **Nghị định 70/2023/NĐ-CP** — 21 chunks (Sửa đổi, bổ sung một số điều của Nghị định 152/2020/NĐ-CP).
6. **Nghị định 293/2025/NĐ-CP** — 15 chunks (Quy định mức lương tối thiểu đối với người lao động làm việc theo HĐLĐ).
7. **Nghị định 356/2025/NĐ-CP** — 196 chunks (Quy định chi tiết và hướng dẫn thi hành một số điều của Luật Việc làm).
8. **Luật Bảo hiểm xã hội** (`58/VBHN-VPQH`) — 558 chunks (Chế độ ốm đau, thai sản, hưu trí, tai nạn LĐ, BHXH 1 lần).
9. **Luật An toàn, vệ sinh lao động 2015** (`84/2015/QH13`) — 365 chunks (Quy chuẩn kỹ thuật, bồi thường TNLĐ - BNN).
10. **Luật Công đoàn 2024** (`50/2024/QH15`) — 175 chunks (Quyền và trách nhiệm của tổ chức đại diện người lao động).
11. **Luật Việc làm 2025** (`74/2025/QH15`) — 203 chunks (Bảo hiểm thất nghiệp, chính sách hỗ trợ việc làm).
12. **Luật Người lao động Việt Nam đi làm việc ở nước ngoài theo hợp đồng 2020** (`69/2020/QH14`) — 266 chunks.

#### Nhóm 2: Văn bản Đối sánh Lịch sử Hiệu lực (1 văn bản — 674 chunks)
13. **Bộ luật Lao động 2012** (`10/2012/QH13`) — 674 chunks (Đã hết hiệu lực toàn bộ từ 01/01/2021).
    - **Vai trò kỹ thuật:** Được chủ động lưu giữ trong cơ sở dữ liệu cùng nhãn `het_hieu_luc` nhằm kiểm thử năng lực lọc hiệu lực theo thời gian (Temporal Validity Filtering), đánh giá khả năng chống ảo giác trích dẫn luật cũ đã bị bãi bỏ khi trả lời các tình huống hiện hành, và phục vụ các truy vấn đối chiếu lịch sử áp dụng luật.

#### Nhóm 3: Văn bản Đối chứng Nhiễu & Thử thách Biên giới Thẩm quyền (4 văn bản — 864 chunks)
14. **Hiến pháp 2013** (`Hiến pháp 2013`) — 290 chunks (Còn hiệu lực).
15. **Luật Thanh tra 2025** (`84/2025/QH15`) — 221 chunks (Hết hiệu lực một phần / Còn hiệu lực).
16. **Luật Người khuyết tật 2010** (`51/2010/QH12`) — 182 chunks (Hết hiệu lực một phần / Còn hiệu lực).
17. **Luật Bảo vệ dữ liệu cá nhân 2025** (`91/2025/QH15`) — 171 chunks (Còn hiệu lực).

### 🎯 Tại sao các Văn bản Đối chứng Nhiễu nằm cùng Chỉ mục (Shared Index)?
Việc tích hợp Hiến pháp 2013 (290 đoạn), Luật Thanh tra, Luật Người khuyết tật... vào cùng chỉ mục tìm kiếm với Bộ luật Lao động là một **thiết kế thực nghiệm có chủ đích (Intentional Benchmark Design)** xuất phát từ yêu cầu học thuật và thực tiễn:
1. **Tránh môi trường thử nghiệm "đóng kín" phi thực tế (Anti-Toy Environment):** Trong một hệ thống tìm kiếm pháp điển quốc gia (như vbpl.vn), hàng chục ngàn văn bản thuộc mọi lĩnh vực cùng nằm chung một kho dữ liệu. Nếu chỉ mục chỉ chứa duy nhất văn bản lao động, bài toán truy xuất sẽ trở nên quá dễ dàng và không phản ánh đúng năng lực phân biệt ngữ nghĩa thực tế.
2. **Thử thách khả năng chống bắt nhầm từ khóa (Disambiguation Challenge):**
   - **Hiến pháp 2013 (290 đoạn):** Chứa các tuyên ngôn khái quát về quyền con người, quyền làm việc (Điều 35, Điều 36...). Đây là *đối chứng nhiễu bậc cao (high-level semantic distractor)*, thách thức bộ truy xuất Dense/BM25 không được trích dẫn Hiến pháp chung chung khi người dùng hỏi về tình huống tranh chấp cụ thể thuộc BLLĐ 2019.
   - **Luật Thanh tra 2025 (221 đoạn):** Chứa các thuật ngữ về thẩm quyền kiểm tra, xử lý vi phạm hành chính nói chung. Đóng vai trò *đối chứng nhiễu về thẩm quyền*, kiểm tra hệ thống có phân biệt được thanh tra hành chính nhà nước với thanh tra chuyên ngành lao động (Điều 214–217 BLLĐ 2019 và Nghị định 12/2022/NĐ-CP).
   - **Luật Người khuyết tật 2010 (182 đoạn):** Tạo sự giao thoa biên giới ngữ nghĩa với các điều khoản bảo vệ lao động là người khuyết tật (Chương XI BLLĐ 2019), kiểm tra khả năng tách bạch chính sách an sinh xã hội nói chung và nghĩa vụ của người sử dụng lao động.
   - **Luật Bảo vệ dữ liệu cá nhân 2025 (171 đoạn):** Đóng vai trò đối chứng biên giới trong các tình huống giám sát nơi làm việc và bảo mật hồ sơ nhân sự.
3. **Đo lường năng lực Từ chối Ngoài Phạm vi (Out-of-Scope Refusal Accuracy):**
   - Tập kiểm thử có 50 câu hỏi ngoài phạm vi (OOD). Việc có sẵn các văn bản đối chứng nhiễu trong cùng chỉ mục giúp đo lường chính xác: Hệ thống có bị lừa bởi độ trùng lặp từ vựng để trả lời sai thẩm quyền hay không, và tầng kiểm định LLM có kích hoạt chính xác cơ chế từ chối (Refusal) hay không.

### ⚙️ Cơ chế Quản lý Dữ liệu:
- Dữ liệu được bóc tách và phân rã chính xác tới **cấp Khoản** (hoặc cấp Điều đối với Điều không chia Khoản).
- Mỗi đơn vị dữ liệu được định danh bằng mã duy nhất (`provision_id`), ví dụ: `45_2019_QH14__D113__K1`.
- Quản lý trạng thái hiệu lực: `con_hieu_luc` (4,167 chunks), `het_hieu_luc` (723 chunks, gồm 674 chunks BLLĐ 2012 và các chunk bị sửa đổi/bãi bỏ).

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
     [Hybrid Fusion — RRF (k=5, α=0.5)]
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
    ├── create_test_set_v3.py   # Script chuẩn hóa bộ câu hỏi kiểm thử đóng băng (135 câu)
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

### Bước 7.1: Chuẩn bị bộ câu hỏi kiểm thử đóng băng (Test Set v3)
Tập kiểm thử chính thức gồm 135 câu hỏi (85 câu trong phạm vi, 50 câu ngoài phạm vi) đã được kiểm định hợp lệ và lưu trữ cố định tại `data/eval/test_set_v3.json`. Để tái sinh hoặc kiểm tra tính toàn vẹn:
```bash
python scripts/create_test_set_v3.py
python scripts/verify_gold_labels.py
```
File dữ liệu: `data/eval/test_set_v3.json`.

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
