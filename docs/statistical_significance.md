# Báo cáo Kiểm định Thống kê & Khoảng Tin cậy (Statistical Significance)

- **Dữ liệu**: `generation_results.json` (N_in_scope = 95, N_out_scope = 50)
- **Mục tiêu**: Báo cáo chính xác kết quả kiểm định thống kê trích xuất từ dữ liệu thực tế, tránh hard-code sai lệch.

## 1. Kiểm định McNemar / Nhị thức chính xác (Pairwise Comparison)

So sánh hiệu năng truy xuất **Hit@5** trên từng câu hỏi (95 câu in-scope) giữa Hybrid RRF và các phương pháp đơn lẻ:

| Cặp so sánh | Hybrid đúng riêng ($b$) | Đối thủ đúng riêng ($c$) | Tổng bất đồng ($b+c$) | $p$-value (Exact Binomial) | Kết luận học thuật |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Hybrid vs BM25** | 13 | 3 | 16 | **0.0213** | **$p < 0.05$ ($p = 0.0213$)**: Khác biệt **có ý nghĩa thống kê** ($\alpha = 0.05$); Hybrid đạt kết quả cao hơn BM25 và sự khác biệt có ý nghĩa thống kê trên tập đánh giá này. (13 câu thắng vs 3 câu thua). |
| **Hybrid vs Dense** | 6 | 2 | 8 | **0.2891** | $p \ge 0.05$ ($p = 0.2891$): Chưa đạt ngưỡng ý nghĩa thống kê $\alpha = 0.05$; thể hiện **xu hướng bổ trợ** tích cực (6 câu thắng vs 2 câu thua). |

> **Nhận định chỉnh sửa báo cáo (Mục 5.1)**:
> - **So sánh Hybrid vs BM25**: Trên tập 95 câu hỏi in-scope, Hybrid đạt **80/95** (84.2%) Hit@5 so với **70/95** (73.7%) của BM25. Kiểm định Exact Binomial (McNemar) cho thấy sự cải thiện này đạt mức ý nghĩa thống kê ở ngưỡng $\alpha = 0.05$ ($b = 13, c = 3, p = 0.0213 < 0.05$). Kết quả cho thấy việc kết hợp BM25 và Dense giúp Hybrid đạt Hit@5 cao hơn BM25 đơn lẻ trên tập đánh giá này, với mức chênh lệch 10,5 điểm phần trăm (84,2% so với 73,7%) và sự khác biệt đạt ý nghĩa thống kê ở mức $\alpha=0.05$.
> - **So sánh Hybrid vs Dense**: Hybrid đạt 80/95 (84.2%) so với 76/95 (80.0%) của Dense. Khoảng cách 4 câu (6 câu Hybrid đúng riêng vs 2 câu Dense đúng riêng) cho giá trị $p = 0.2891 > 0.05$, chưa đạt ý nghĩa thống kê ở mức 5%; do đó chưa đủ bằng chứng để kết luận Hybrid khác Dense về Hit@5 trên tập đánh giá này.; Mặc dù chưa đạt ý nghĩa thống kê, kết quả 6 câu Hybrid đúng riêng so với 2 câu Dense đúng riêng cho thấy dấu hiệu bổ trợ giữa hai nhánh, là cơ sở thực nghiệm cho việc kết hợp BM25 và Dense.

## 2. Khoảng tin cậy 95% Wilson Score

Tính toán khoảng tin cậy 95% (95% CI) cho các chỉ số chính:

| Phương pháp | Hit@5 (95 câu) | 95% CI Hit@5 | Refusal Acc (50 câu) | 95% CI Refusal Acc | FAR (50 câu) | 95% CI FAR | Citation khớp Gold (N=95) | 95% CI Citation khớp Gold |
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
| **Trích dẫn khớp Gold** | 74/95 (77.9%) | 72/95 (75.8%) | 80/95 (84.2%) |
| **Không từ chối & có Citation khớp Gold** | 74/95 (77.9%) | 72/95 (75.8%) | 80/95 (84.2%) |
