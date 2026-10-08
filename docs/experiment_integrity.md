
## 1. Minh bạch Lịch sử Phiên bản và Git Commits

Trong quá trình thực hiện đề tài, nhóm nghiên cứu đã trải qua 2 giai đoạn thực nghiệm chính. Thay vì thay thế âm thầm, báo cáo giữ lại đầy đủ kết quả của cả hai giai đoạn:

| Giai đoạn | Thời gian | Git Commit đại diện | Mã nguồn & Dữ liệu tương ứng | Mô tả & Mục đích |
| :--- | :---: | :---: | :--- | :--- |
| **Giai đoạn 1** *(Bản đầu)* | 06/09/2026 | `1f50c5e` | - Test Set gốc (120 câu)<br>- `scripts/generator.py` v1<br>- Kết quả: `data/eval/archive/*_old.json` | Thực nghiệm thăm dò ban đầu. Kết quả cho thấy tỷ lệ từ chối nhầm còn cao và phát hiện một số nhãn gold bị lệch văn bản cũ (BLLĐ 2012). |
| **Giai đoạn 2** *(Bản chuẩn hóa)* | 17/09/2026 - nay | `0e94425` | - Test Set đóng băng (`test_set_v3.json`)<br>- Dev Set độc lập (`dev_set_v2.json`)<br>- Tối ưu hóa prompt RAG & chuẩn hóa Sub-ID<br>- Kết quả: `generation_results.json` | Thực nghiệm chính thức có kiểm định và đối chiếu. Giữ cố định mã nguồn và tham số ($k=5, \alpha=0.5$). |

Toàn bộ dữ liệu của Giai đoạn 1 đã được lưu trữ minh bạch tại thư mục `data/eval/archive/` kèm file [README.md](file:///c:/Users/Admin/Downloads/TT/project/data/eval/archive/README.md).

---

## 2. Phân tách Tập Dev Set (dev_set_v2) và Test Set (test_set_v3)

Để khắc phục hiện tượng tinh chỉnh mô hình trực tiếp trên tập kiểm thử (overfitting on test), dự án đã phân tách rạch ròi 2 tập dữ liệu:

### 2.1. Tập Phát triển (Dev Set - 120 câu hỏi)
- **Vị trí**: `data/eval/dev_set_v2.json` (chuẩn hóa từ `dev_set.json` 30 câu sơ khai)
- **Thành phần**: 95 câu hỏi trong phạm vi (In-scope) và 25 câu hỏi ngoài phạm vi (Out-of-scope).
- **Mục đích**:
  1. Quét tìm siêu tham số tối ưu ($k \in [1, 2, 3, 5, 10, 20, 30, 60]$, trọng số $\alpha \in [0.3, 0.4, 0.5, 0.6, 0.7]$) cho thuật toán RRF với cấu hình mở rộng ngữ cảnh thống nhất (`expand_siblings=True`).
  2. Tinh chỉnh cấu trúc prompt và chỉ thị an toàn của LLM nhằm giảm thiểu hiện tượng ảo giác.
  3. Thử nghiệm mở rộng ngữ cảnh Điều khoản anh em (Sibling Provision Expansion).
- **Rà soát nhãn**: Tập Dev Set v1 sơ khai từng ghi nhận 13/95 câu in-scope có nhãn chưa phù hợp (BLLĐ 2012, 58/VBHN-VPQH, văn bản ngoài phạm vi). Dữ liệu đã được rà soát và cập nhật trong `dev_set_v2.json` (commit `d6b48bd`).
- **Kết quả chọn tham số**: Được ghi nhận chi tiết tại [sweep_rrf_results.md](file:///c:/Users/Admin/Downloads/TT/project/docs/sweep_rrf_results.md). Báo cáo cung cấp kèm khoảng tin cậy 95% Wilson Score CI cho Recall@5 và giải thích cơ sở chọn $k=5, \alpha=0.5$ (MRR@10 = 0.7280, Recall@5 = 0.8632, 95% CI: [78.0%, 91.8%]).

### 2.2. Tập Kiểm thử Đóng băng (Test Set - 135 câu hỏi)
- **Vị trí**: `data/eval/test_set_v3.json`
- **Nguyên tắc**: **Đóng băng hoàn toàn (Frozen)** sau khi hoàn thiện kiểm tra tính hợp lệ bằng công cụ tự động. Không được can thiệp sửa câu hỏi hay gán lại nhãn gold theo kết quả sinh của mô hình.
- **Thành phần**:
  - **85 câu hỏi trong phạm vi (In-scope)** thuộc 7 chủ đề pháp luật lao động.
  - **50 câu hỏi ngoài phạm vi (Out-of-scope)** gồm các câu hỏi thuộc luật khác, tư vấn tình huống ngoài thẩm quyền, hoặc không liên quan.

---

## 3. Quy trình Kiểm thử Tự động Nhãn Gold (Gold Label Verification)

Để ngăn chặn lỗi dữ liệu như câu `t2_09` (mã gold không có trong corpus) và câu `t2_14` (gold thuộc luật đã hết hiệu lực), dự án xây dựng script tự động [verify_gold_labels.py](file:///c:/Users/Admin/Downloads/TT/project/scripts/verify_gold_labels.py).

### Quy tắc kiểm định:
1. **Kiểm tra Tồn tại**: Mọi `gold_provision_id` bắt buộc phải có mặt trong `data/structured/corpus.csv`.
2. **Kiểm tra Hiệu lực**: Mọi `gold_provision_id` phải có trạng thái `con_hieu_luc` tại ngày chốt dữ liệu (01/08/2026).
3. **Báo cáo sai lệch**: Tự động thông báo và yêu cầu xử lý trước khi bất kỳ thực nghiệm nào được thực thi.
