# Báo cáo Kiểm định Thống kê & Khoảng Tin cậy (Statistical Significance)

- **Dữ liệu**: `generation_results.json` (N_in_scope = 95, N_out_scope = 50)
- **Mục tiêu**: Báo cáo chính xác kết quả kiểm định thống kê trích xuất từ dữ liệu thực tế, có hiệu chỉnh đa so sánh (Multiple Comparisons Correction) để kiểm soát Family-Wise Error Rate (FWER).

## 1. Kiểm định McNemar / Nhị thức chính xác & Hiệu chỉnh Đa so sánh

So sánh hiệu năng truy xuất **Hit@5** trên từng câu hỏi (95 câu in-scope) giữa Hybrid RRF và các phương pháp đơn lẻ.
Để tránh sai lầm loại I (False Positive) tích lũy khi thực hiện nhiều phép kiểm định đồng thời, báo cáo áp dụng cả phương pháp hiệu chỉnh **Bonferroni** và **Holm-Bonferroni (Step-down)**:

### 1.1. So sánh đối chứng với mô hình đề xuất Hybrid RRF ($m = 2$)

| Cặp so sánh | Hybrid thắng ($b$) | Đối thủ thắng ($c$) | Tổng bất đồng ($b+c$) | $p_{\text{raw}}$ | $p_{\text{Bonferroni}}$ | $p_{\text{Holm}}$ | Kết luận học thuật |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **Hybrid vs BM25** | 13 | 3 | 16 | **0.0213** | **0.0425** | **0.0425** | **$p_{\text{Holm}} < 0.05$ ($p_{\text{raw}} = 0.0213, p_{\text{Holm}} = 0.0425$)**: Khác biệt **có ý nghĩa thống kê** sau hiệu chỉnh đa so sánh ($\alpha = 0.05$); sự vượt trội của Hybrid so với BM25 được xác nhận thực nghiệm (13 câu thắng vs 3 câu thua). |
| **Hybrid vs Dense** | 6 | 2 | 8 | 0.2891 | 0.5781 | 0.2891 | $p \ge 0.05$ ($p_{\text{raw}} = 0.2891, p_{\text{Holm}} = 0.2891$): Chưa đạt ngưỡng ý nghĩa thống kê $\alpha = 0.05$; thể hiện **xu hướng bổ trợ** tích cực (6 câu thắng vs 2 câu thua). |

### 1.2. Bảng kiểm định toàn bộ các cặp (All Pairwise Comparisons, $m = 3$)

| Cặp so sánh | Phương pháp 1 thắng ($b$) | Phương pháp 2 thắng ($c$) | Tổng bất đồng | $p_{\text{raw}}$ | $p_{\text{Bonferroni}}$ | $p_{\text{Holm}}$ | Đánh giá |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **Hybrid vs BM25** | 13 | 3 | 16 | 0.0213 | 0.0638 | 0.0638 | Ưu thế rõ nét, $p_{\text{raw}} = 0.0213 < 0.05$ |
| **Hybrid vs Dense** | 6 | 2 | 8 | 0.2891 | 0.8672 | 0.5781 | Xu hướng bổ trợ ($p_{\text{raw}} = 0.2891$) |
| **Dense vs BM25** | 15 | 9 | 24 | 0.3075 | 0.9224 | 0.5781 | Chênh lệch 6 câu ($p_{\text{raw}} = 0.3075$) |

> **Nhận định chỉnh sửa báo cáo (Mục 5.1)**:
> - **So sánh Hybrid vs BM25**: Trên tập 95 câu hỏi in-scope, Hybrid đạt **80/95** (84.2%) Hit@5 so với **70/95** (73.7%) của BM25. Kiểm định Exact Binomial (McNemar) cho giá trị $p_{\text{raw}} = 0.0213 < 0.05$ ($b = 13, c = 3$). Khi áp dụng hiệu chỉnh đa so sánh nghiêm ngặt nhằm kiểm soát Family-Wise Error Rate (FWER $\le 0.05$), sự vượt trội của Hybrid RRF so với BM25 **vẫn giữ vững ý nghĩa thống kê** ($p_{\text{Bonferroni}} = 0.0425 < 0.05, p_{\text{Holm}} = 0.0425 < 0.05$). Điều này chứng minh việc kết hợp biểu diễn ngữ nghĩa Dense vào BM25 mang lại giá trị gia tăng thực chất, vượt trội hơn hẳn so với BM25 đơn lẻ trên tập dữ liệu kiểm thử.
> - **So sánh Hybrid vs Dense**: Hybrid đạt 80/95 (84.2%) so với 76/95 (80.0%) của Dense. Khoảng cách 4 câu (6 câu Hybrid đúng riêng vs 2 câu Dense đúng riêng) cho giá trị $p_{\text{raw}} = 0.2891 > 0.05$ ($p_{\text{Holm}} = 0.2891$), chưa đạt ý nghĩa thống kê ở mức 5% do quy mô mẫu 95 câu; tuy nhiên kết quả thể hiện rõ tính bổ trợ (complementary) giữa hai nhánh, giúp giảm thiểu rủi ro tìm thiếu điều khoản then chốt.

## 2. Khoảng tin cậy 95% Wilson Score

Tính toán khoảng tin cậy 95% (95% CI) cho các chỉ số chính:

| Phương pháp | Hit@5 (95 câu) | 95% CI Hit@5 | Refusal Acc (50 câu) | 95% CI Refusal Acc | FAR (50 câu) | 95% CI FAR | Citation Exact Match (N=95) | 95% CI CEM |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **BM25** | 70/95 (73.7%) | [64.0%, 81.5%] | 48/50 (96.0%) | [86.5%, 98.9%] | 2/50 (4.0%) | [1.1%, 13.5%] | 74/95 (77.9%) | [68.6%, 85.1%] |
| **Dense** | 76/95 (80.0%) | [70.9%, 86.8%] | 47/50 (94.0%) | [83.8%, 97.9%] | 3/50 (6.0%) | [2.1%, 16.2%] | 72/95 (75.8%) | [66.3%, 83.3%] |
| **Hybrid_RRF** | 80/95 (84.2%) | [75.6%, 90.2%] | 46/50 (92.0%) | [81.2%, 96.8%] | 4/50 (8.0%) | [3.2%, 18.8%] | 80/95 (84.2%) | [75.6%, 90.2%] |

## 3. Thống nhất Mẫu số Chung cho Chỉ số Trích dẫn (Mục 4.3)

Theo nhận xét của GVHD, việc chỉ tính Citation Exact Match trên các câu *được trả lời* (mẫu số thay đổi theo từng phương pháp: BM25=83/95, Dense=82/95, Hybrid_RRF=88/95) làm sai lệch khả năng so sánh chéo. Dưới đây là bảng chuẩn hóa trên **mẫu số chung toàn bộ 95 câu in-scope**:

| Chỉ số (Mẫu số $N=95$) | BM25 | Dense | Hybrid RRF |
| :--- | :---: | :---: | :---: |
| **Số câu được trả lời** | 83/95 (87.4%) | 82/95 (86.3%) | 88/95 (92.6%) |
| **Trích dẫn hợp lệ (Valid Citations)** | 82/95 (86.3%) | 81/95 (85.3%) | 86/95 (90.5%) |
| **Trích dẫn khớp Gold (Exact Match)** | 74/95 (77.9%) | 72/95 (75.8%) | 80/95 (84.2%) |
| **Trả lời đúng & Trích dẫn đúng** | 74/95 (77.9%) | 72/95 (75.8%) | 80/95 (84.2%) |
