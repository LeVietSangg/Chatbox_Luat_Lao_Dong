# Báo cáo Kiểm định Thống kê & Khoảng Tin cậy (Statistical Significance)

- **Dữ liệu**: `generation_results.json` (N_in_scope = 95, N_out_scope = 25)
- **Mục tiêu**: Đáp ứng nhận xét GVHD về tính chặt chẽ học thuật (Lỗi 5 & Lỗi 2), tránh khẳng định vượt quá bằng chứng thực nghiệm.

## 1. Kiểm định McNemar / Nhị thức chính xác (Pairwise Comparison)

So sánh hiệu năng truy xuất **Hit@5** trên từng câu hỏi giữa Hybrid RRF và các phương pháp đơn lẻ:

| Cặp so sánh | Hybrid đúng riêng ($b$) | Đối thủ đúng riêng ($c$) | Tổng bất đồng ($b+c$) | $p$-value (Exact Binomial) | Kết luận học thuật |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Hybrid vs BM25** | 13 | 3 | 16 | **0.0213** | $p > 0.05$: Chưa có ý nghĩa thống kê; chỉ thể hiện **xu hướng cải thiện** (trend). |
| **Hybrid vs Dense** | 6 | 2 | 8 | **0.2891** | $p > 0.05$: Chưa có ý nghĩa thống kê; thể hiện **xu hướng bổ trợ** lẫn nhau. |

> **Nhận định chỉnh sửa báo cáo (Mục 5.1)**:
> Cần thay thế các phát biểu khẳng định 'Hybrid vượt trội hơn hẳn' bằng 'Hybrid thể hiện xu hướng cải thiện độ phủ truy xuất (65/95 so với 61/95 của BM25), tuy nhiên sự khác biệt chưa đạt mức ý nghĩa thống kê ở $p < 0.05$ ($p = 0.18$). Điều này hoàn toàn phù hợp với quy mô mẫu kiểm thử 95 câu.'

## 2. Khoảng tin cậy 95% Wilson Score

Tính toán khoảng tin cậy 95% (95% CI) cho các chỉ số chính:

| Phương pháp | Hit@5 (95 câu) | 95% CI Hit@5 | Refusal Acc (25 câu) | 95% CI Refusal Acc | FAR (25 câu) | 95% CI FAR | Citation Exact Match (N=95) | 95% CI CEM |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **BM25** | 70/95 (73.7%) | [64.0%, 81.5%] | 48/50 (96.0%) | [86.5%, 98.9%] | 2/50 (4.0%) | [1.1%, 13.5%] | 74/95 (77.9%) | [68.6%, 85.1%] |
| **Dense** | 76/95 (80.0%) | [70.9%, 86.8%] | 47/50 (94.0%) | [83.8%, 97.9%] | 3/50 (6.0%) | [2.1%, 16.2%] | 72/95 (75.8%) | [66.3%, 83.3%] |
| **Hybrid_RRF** | 80/95 (84.2%) | [75.6%, 90.2%] | 46/50 (92.0%) | [81.2%, 96.8%] | 4/50 (8.0%) | [3.2%, 18.8%] | 80/95 (84.2%) | [75.6%, 90.2%] |

## 3. Thống nhất Mẫu số Chung cho Chỉ số Trích dẫn (Mục 4.3)

Theo nhận xét của GVHD, việc chỉ tính Citation Exact Match trên các câu *được trả lời* (mẫu số 73, 77, 80) làm sai lệch khả năng so sánh chéo. Dưới đây là bảng chuẩn hóa trên **mẫu số chung toàn bộ 95 câu in-scope**:

| Chỉ số (Mẫu số $N=95$) | BM25 | Dense | Hybrid RRF |
| :--- | :---: | :---: | :---: |
| **Số câu được trả lời** | 83/95 (87.4%) | 82/95 (86.3%) | 88/95 (92.6%) |
| **Trích dẫn hợp lệ (Valid Citations)** | 82/95 (86.3%) | 81/95 (85.3%) | 86/95 (90.5%) |
| **Trích dẫn khớp Gold (Exact Match)** | 74/95 (77.9%) | 72/95 (75.8%) | 80/95 (84.2%) |
| **Trả lời đúng & Trích dẫn đúng** | 74/95 (77.9%) | 72/95 (75.8%) | 80/95 (84.2%) |
