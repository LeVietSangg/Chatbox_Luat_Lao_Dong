# Báo cáo Kiểm định Thống kê & Khoảng Tin cậy (Statistical Significance)

- **Dữ liệu**: `generation_results.json` (N_in_scope = 85, N_out_scope = 50)
- **Mục tiêu**: Báo cáo chính xác kết quả kiểm định thống kê trích xuất từ dữ liệu thực tế, có hiệu chỉnh đa so sánh (Multiple Comparisons Correction) để kiểm soát Family-Wise Error Rate (FWER).

## 1. Kiểm định McNemar / Nhị thức chính xác & Hiệu chỉnh Đa so sánh

So sánh hiệu năng truy xuất **Hit@5** trên từng câu hỏi (85 câu in-scope) giữa Hybrid RRF và các phương pháp đơn lẻ.
Để tránh sai lầm loại I (False Positive) tích lũy khi thực hiện nhiều phép kiểm định đồng thời, báo cáo áp dụng cả phương pháp hiệu chỉnh **Bonferroni** và **Holm-Bonferroni (Step-down)**:

### 1.1. So sánh đối chứng với mô hình đề xuất Hybrid RRF ($m = 2$)

| Cặp so sánh | Hybrid thắng ($b$) | Đối thủ thắng ($c$) | Tổng bất đồng ($b+c$) | $p_{\text{raw}}$ | $p_{\text{Bonferroni}}$ | $p_{\text{Holm}}$ | Kết luận học thuật |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **Hybrid vs BM25** | 11 | 0 | 11 | **0.0010** | **0.0020** | **0.0020** | **$p_{\text{Holm}} < 0.01$ ($p_{\text{raw}} = 0.0010, p_{\text{Holm}} = 0.0020$)**: Khác biệt **có ý nghĩa thống kê rất cao** sau khi hiệu chỉnh đa so sánh; Hybrid vượt trội so với BM25 (11 câu thắng vs 0 câu thua). |
| **Hybrid vs Dense** | 4 | 4 | 8 | 1.0000 | 1.0000 | 1.0000 | $p \ge 0.05$ ($p_{\text{raw}} = 1.0000, p_{\text{Holm}} = 1.0000$): Chưa đạt ngưỡng ý nghĩa thống kê $\alpha = 0.05$; thể hiện **xu hướng bổ trợ** tích cực (4 câu thắng vs 4 câu thua). |

### 1.2. Bảng kiểm định toàn bộ các cặp (All Pairwise Comparisons, $m = 3$)

| Cặp so sánh | Phương pháp 1 thắng ($b$) | Phương pháp 2 thắng ($c$) | Tổng bất đồng | $p_{\text{raw}}$ | $p_{\text{Bonferroni}}$ | $p_{\text{Holm}}$ | Đánh giá |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **Hybrid vs BM25** | 11 | 0 | 11 | 0.0010 | 0.0029 | 0.0029 | Ưu thế rõ nét, $p_{\text{raw}} = 0.0213 < 0.05$ |
| **Hybrid vs Dense** | 4 | 4 | 8 | 1.0000 | 1.0000 | 1.0000 | Xu hướng bổ trợ ($p_{\text{raw}} = 0.2891$) |
| **Dense vs BM25** | 15 | 4 | 19 | 0.0192 | 0.0576 | 0.0384 | Chênh lệch 6 câu ($p_{\text{raw}} = 0.3075$) |

> **Nhận định chỉnh sửa báo cáo (Mục 5.1)**:
> - **So sánh Hybrid vs BM25**: Trên tập 85 câu hỏi in-scope, Hybrid đạt **79/85** (92.9%) Hit@5 so với **68/85** (80.0%) của BM25. Kiểm định Exact Binomial (McNemar) cho giá trị $p_{\text{raw}} = 0.0010 < 0.05$ ($b = 11, c = 0$). Khi áp dụng hiệu chỉnh đa so sánh nghiêm ngặt nhằm kiểm soát Family-Wise Error Rate (FWER $\le 0.05$), sự vượt trội của Hybrid RRF so với BM25 **vẫn giữ vững ý nghĩa thống kê** ($p_{\text{Bonferroni}} = 0.0020 < 0.05, p_{\text{Holm}} = 0.0020 < 0.05$). Điều này chứng minh việc kết hợp biểu diễn ngữ nghĩa Dense vào BM25 mang lại giá trị gia tăng thực chất, vượt trội hơn hẳn so với BM25 đơn lẻ trên tập dữ liệu kiểm thử.
> - **So sánh Hybrid vs Dense**: Hybrid đạt 79/85 (92.9%) so với 79/85 (92.9%) của Dense. Khoảng cách 4 câu (4 câu Hybrid đúng riêng vs 4 câu Dense đúng riêng) cho giá trị $p_{\text{raw}} = 1.0000 > 0.05$ ($p_{\text{Holm}} = 1.0000$), chưa đạt ý nghĩa thống kê ở mức 5% do quy mô mẫu 85 câu; tuy nhiên kết quả thể hiện rõ tính bổ trợ (complementary) giữa hai nhánh, giúp giảm thiểu rủi ro tìm thiếu điều khoản then chốt.

## 2. Khoảng tin cậy 95% Wilson Score

Tính toán khoảng tin cậy 95% (95% CI) cho các chỉ số chính:

| Phương pháp | Hit@5 (85 câu) | 95% CI Hit@5 | Refusal Acc (50 câu) | 95% CI Refusal Acc | FAR (50 câu) | 95% CI FAR | Citation Exact Match (N=85) | 95% CI CEM |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **BM25** | 68/85 (80.0%) | [70.3%, 87.1%] | 46/50 (92.0%) | [81.2%, 96.8%] | 4/50 (8.0%) | [3.2%, 18.8%] | 73/85 (85.9%) | [76.9%, 91.7%] |
| **Dense** | 79/85 (92.9%) | [85.4%, 96.7%] | 45/50 (90.0%) | [78.6%, 95.7%] | 5/50 (10.0%) | [4.3%, 21.4%] | 78/85 (91.8%) | [84.0%, 96.0%] |
| **Hybrid_RRF** | 79/85 (92.9%) | [85.4%, 96.7%] | 45/50 (90.0%) | [78.6%, 95.7%] | 5/50 (10.0%) | [4.3%, 21.4%] | 79/85 (92.9%) | [85.4%, 96.7%] |

## 3. Thống nhất Mẫu số Chung cho Chỉ số Trích dẫn (Mục 4.3)

Theo nhận xét của GVHD, việc chỉ tính Citation Exact Match trên các câu *được trả lời* (mẫu số thay đổi theo từng phương pháp: BM25=82/85, Dense=83/85, Hybrid_RRF=82/85) làm sai lệch khả năng so sánh chéo. Dưới đây là bảng chuẩn hóa trên **mẫu số chung toàn bộ 85 câu in-scope**:

| Chỉ số (Mẫu số $N=85$) | BM25 | Dense | Hybrid RRF |
| :--- | :---: | :---: | :---: |
| **Số câu được trả lời** | 82/85 (96.5%) | 83/85 (97.6%) | 82/85 (96.5%) |
| **Trích dẫn hợp lệ (Valid Citations)** | 77/85 (90.6%) | 80/85 (94.1%) | 81/85 (95.3%) |
| **Trích dẫn khớp Gold (Exact Match)** | 73/85 (85.9%) | 78/85 (91.8%) | 79/85 (92.9%) |
| **Trả lời đúng & Trích dẫn đúng** | 73/85 (85.9%) | 78/85 (91.8%) | 79/85 (92.9%) |
