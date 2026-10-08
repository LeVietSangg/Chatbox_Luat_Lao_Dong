## 2. Phân tích & Cơ sở Lựa chọn Tham số

Cấu hình được lựa chọn trên Dev Set là **(k=5, alpha=0.5)**, với **MRR@10 = 0.7280** và **Recall@5 = 0.8632** (95% CI Wilson: **[78.0%, 91.8%]**).

### 2.1. Quá trình rà soát và chuẩn hóa nhãn Dev Set (13/95 nhãn)

Trong phiên bản thử nghiệm ban đầu (`dev_set_v2.json`), nhóm ghi nhận có **13/95 câu hỏi in-scope (13.7%)** có nhãn chưa phù hợp do lịch sử cập nhật dữ liệu, bao gồm:
- Viện dẫn văn bản đã hết hiệu lực (Bộ luật Lao động 2012 thay vì BLLĐ 2019).
- Lệch số Điều trong Văn bản hợp nhất `58/VBHN-VPQH` về Bảo hiểm xã hội.
- Nhầm lẫn văn bản ngoài phạm vi luật lao động (như quy định về dữ liệu cá nhân).

Các nhãn này đã được rà soát và cập nhật trong **`dev_set_v2.json`** (commit `d6b48bd`). Thực nghiệm sweep được tiến hành trên phiên bản dữ liệu đã rà soát này để đảm bảo tính nhất quán của kết quả.

### 2.2. Khoảng tin cậy và mức độ biến động của Recall@5

1. **Khoảng tin cậy của Recall@5:** Trên cỡ mẫu **N=95** câu, Recall@5 được báo cáo kèm khoảng tin cậy 95% Wilson nhằm thể hiện độ bất định của ước lượng. Ví dụ, với Recall@5 = 86.3%, khoảng tin cậy 95% là **[78.0%, 91.8%]**.

2. **Mức độ biến động:** Ở các cấu hình có hiệu năng gần nhau, các khoảng tin cậy của Recall@5 có mức giao thoa đáng kể. Vì vậy, các chênh lệch nhỏ về Recall@5 trên Dev Set cần được diễn giải thận trọng và không được sử dụng đơn độc để phân tách các cấu hình.

3. **Tiêu chí lựa chọn:** MRR@10 được sử dụng làm tiêu chí chính để lựa chọn cấu hình, trong khi Recall@5 được sử dụng làm tiêu chí phụ khi các cấu hình có MRR@10 tương đương. MRR@10 phản ánh cả việc truy hồi đúng và vị trí của kết quả đúng trong danh sách xếp hạng.

### 2.3. Mở rộng lưới tham số và đánh giá cấu hình `k=5`

1. **Đồng bộ cấu hình:** Thực nghiệm sweep được thực hiện với `expand_siblings = True`, thống nhất với pipeline đánh giá cuối (`run_experiments.py`).

2. **Mở rộng lưới quanh `k=5`:** Nhằm kiểm tra xem `k=5` có bị giới hạn bởi mép dưới của lưới cũ (`k ∈ [5,10,20,60]`) hay không, phạm vi quét được mở rộng xuống `k ∈ [1,2,3]` và bổ sung `k=30`.

   - Khi `k<5` tại `alpha=0.5`: k=1,2,3 có MRR@10 lần lượt là **0.6968, 0.7038, 0.7205**, đều thấp hơn k=5 (**0.7280**).
   - Khi `k>5` tại `alpha=0.5`: k=10,20,30,60 có MRR@10 lần lượt là **0.7224, 0.7159, 0.7150, 0.7169**, đều thấp hơn k=5.

3. **Nhận định:** Trên toàn bộ **40 cấu hình** được khảo sát, `(k=5, alpha=0.5)` đạt MRR@10 cao nhất. Việc mở rộng lưới cho thấy `k=5` vẫn đạt kết quả cao hơn các giá trị lân cận đã khảo sát, thay vì chỉ là giá trị thấp nhất của lưới thử nghiệm ban đầu.
