# HƯỚNG DẪN CÀI ĐẶT VÀ VẬN HÀNH HỆ THỐNG
### Đề tài: Xây dựng chatbot hỗ trợ tra cứu một số quy định về pháp luật về lao động

---

## 1. YÊU CẦU MÔI TRƯỜNG
- **Python**: Phiên bản `3.10` hoặc `3.11` (khuyến nghị `Python 3.11`).
- **RAM**: Tối thiểu 8 GB.
- **Hệ điều hành**: Windows 10/11, macOS hoặc Linux.

---

## 2. CÁC BƯỚC CÀI ĐẶT CHI TIẾT

### Bước 1: Mở thư mục dự án
Mở Terminal / PowerShell trên máy tính và chuyển vào thư mục `project`:
```bash
cd project
```

### Bước 2: Tạo và kích hoạt môi trường ảo Python
Để tránh xung đột với các thư viện khác trên máy:
- **Trên Windows (PowerShell):**
  ```powershell
  python -m venv venv
  .\venv\Scripts\Activate.ps1
  ```
- **Trên Windows (Command Prompt - CMD):**
  ```cmd
  python -m venv venv
  venv\Scripts\activate.bat
  ```
- **Trên Linux / macOS:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### Bước 3: Cài đặt toàn bộ thư viện
Cài đặt từ file `requirements.txt`:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Bước 4: Cấu hình Khóa API (Google Gemini API Key)
Tạo file `.env` nằm ngay trong thư mục `project/` với nội dung sau:
```env
GEMINI_API_KEY=điền_mã_api_key_của_bạn_vào_đây
```
*(Bạn có thể lấy mã API miễn phí tại: [Google AI Studio](https://aistudio.google.com/)).*

---

## 3. KHỞI CHẠY ỨNG DỤNG WEB (STREAMLIT)

Chạy câu lệnh sau trong terminal:
```bash
streamlit run app.py
```

Sau khi chạy, mở trình duyệt web và truy cập địa chỉ:
 **`http://localhost:8501`**

Giao diện sẽ hiển thị đầy đủ:
- Khung chat hỏi đáp pháp luật với đồng hồ thời gian thực.
- Cột bên phải hiển thị danh sách các văn bản trích dẫn nguồn, kèm nhãn **Còn hiệu lực** (màu xanh) hoặc **Hết hiệu lực** (màu đỏ) và nút bấm xem chi tiết toàn văn điều khoản.
- Thanh bên trái hỗ trợ tạo cuộc trò chuyện mới và lưu lịch sử hỏi đáp.

---

## 4. CHẠY THỰC NGHIỆM ĐÁNH GIÁ (NẾU CẦN CHẤM ĐIỂM)

- **Tạo bộ câu hỏi đánh giá chuẩn (155 câu):**
  ```bash
  python scripts/create_test_set.py
  ```
- **Chạy quy trình đánh giá tự động (Retrieval + Generation):**
  ```bash
  python scripts/run_experiments.py
  ```
- Kết quả báo cáo định lượng (Recall@k, MRR, Refusal Accuracy, Latency) sẽ nằm tại:
  `data/eval/week6_generation_metrics.json`.
