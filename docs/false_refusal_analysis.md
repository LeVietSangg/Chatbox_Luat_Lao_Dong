# Báo cáo Phân tích Chi tiết 15 Câu Từ Chối Nhầm (False Refusals)

- **Tỷ lệ từ chối nhầm (FRR)**: `15 / 95` (7.37%)
- **Pipeline thực nghiệm**: `Hybrid RRF (k=10, w=0.5, top_k=5)` trên `test_set_v1.json`
- **Mục tiêu**: Bóc tách nguyên nhân gốc rễ (Root Cause Analysis) và đề xuất kế hoạch khắc phục theo nhận xét của GVHD (Lỗi 7).

## 1. Thống kê theo nhóm nguyên nhân gốc rễ

| Nhóm nguyên nhân | Số lượng | Tỷ lệ | Mô tả |
| :--- | :---: | :---: | :--- |
| **1. Lỗi nhãn Gold (Hết hiệu lực / Mã không tồn tại)** | 0 | 0.0% | Gold thuộc văn bản hết hiệu lực bị bộ lọc loại bỏ, hoặc mã gold không có trong corpus. |
| **2. Khoảng cách từ vựng / Khẩu ngữ đời thường** | 0 | 0.0% | Câu hỏi dùng từ đời thường (nghỉ ngang, quỵt lương...) không khớp câu chữ văn bản luật. |
| **3. Truy xuất trượt Top-5 (Thứ hạng ngoài Top-5)** | 2 | 13.3% | Điều luật liên quan nằm ở top 6-15, bị cắt mất khi chỉ lấy top-5. |
| **4. Generator từ chối khắt khe dù có điều khoản** | 5 | 33.3% | Điều khoản đã được truy xuất nhưng prompt/ngưỡng tự kiểm tra từ chối trả lời. |
| **Tổng cộng** | **7** | **100%** | |

## 2. Bảng phân tích chi tiết từng câu hỏi

| STT | Mã QID | Câu hỏi | Chủ đề | Gold Provision ID | Top-3 Retrieved | Nguyên nhân |
| :---: | :---: | :--- | :---: | :--- | :--- | :--- |
| 1 | `v2_33` | Trong trường hợp khắc phục hậu quả thiên tai, hỏa hoạn, dịch bệnh nguy hiểm, người lao động có được từ chối làm thêm giờ không? | lam_them_gio | `45_2019_QH14__D108__K2` | `45_2019_QH14__D29__K1<br>45_2019_QH14__D129__K2<br>45_2019_QH14__D108__K2` | Truy xuất thành công gold trong top-5 nhưng Generator từ chối do ngưỡng kiểm tra ngữ cảnh khắt khe |
| 2 | `v2_51` | Người sử dụng lao động có trách nhiệm thanh toán tiền tàu xe đi đường cho người lao động khi nghỉ phép không? | nghi_phep | `45_2019_QH14__D113__K6` | `45_2019_QH14__D163__K6<br>145_2020_NDCP__D67__K3<br>84_2015_QH13__D38__K2` | Điều luật cần thiết rơi ra ngoài top-5 (cần mở rộng top-k hoặc mở rộng Điều anh em) |
| 3 | `v2_65` | Người sử dụng lao động có cần thông báo trước cho người lao động khi hợp đồng sắp hết hạn không? | cham_dut_hop_dong | `45_2019_QH14__D45__K1` | `45_2019_QH14__D38<br>45_2019_QH14__D177__K4<br>45_2019_QH14__D36__K2` | Truy xuất thành công gold trong top-5 nhưng Generator từ chối do ngưỡng kiểm tra ngữ cảnh khắt khe |
| 4 | `v2_77` | Trợ cấp một lần khi sinh con hoặc nhận con nuôi bằng bao nhiêu tháng lương cơ sở? | bao_hiem | `58_VBHN-VPQH__D58__K1` | `58_VBHN-VPQH__D58__K4<br>58_VBHN-VPQH__D58__K3<br>58_VBHN-VPQH__D59__K3` | Truy xuất thành công gold trong top-5 nhưng Generator từ chối do ngưỡng kiểm tra ngữ cảnh khắt khe |
| 5 | `v2_79` | Mức đóng bảo hiểm xã hội bắt buộc hằng tháng của người lao động là bao nhiêu phần trăm? | bao_hiem | `58_VBHN-VPQH__D33__K1` | `58_VBHN-VPQH__D33__K7<br>58_VBHN-VPQH__D34__K1<br>58_VBHN-VPQH__D34__K4` | Điều luật cần thiết rơi ra ngoài top-5 (cần mở rộng top-k hoặc mở rộng Điều anh em) |
| 6 | `v2_89` | Người thử việc có cần phải được huấn luyện vệ sinh an toàn, thực phẩm không? | quyen_loi_khac | `84_2015_QH13__D14__K4` | `84_2015_QH13__D14__K4<br>84_2015_QH13__D14__K1<br>84_2015_QH13__D14__K5` | Truy xuất thành công gold trong top-5 nhưng Generator từ chối do ngưỡng kiểm tra ngữ cảnh khắt khe |
| 7 | `v2_95` | Dữ liệu cá nhân nhạy cảm bao gồm những loại nào? | quyen_loi_khac | `91_2025_QH15__D2__K3` | `91_2025_QH15__D2__K1<br>91_2025_QH15__D2__K3<br>356_2025_NDCP__D4__K2` | Truy xuất thành công gold trong top-5 nhưng Generator từ chối do ngưỡng kiểm tra ngữ cảnh khắt khe |

## 3. Kế hoạch và Giải pháp Khắc phục Đã/Đang Triển khai

Dựa trên kết quả phân tích trên, các giải pháp kỹ thuật cụ thể đã và đang được triển khai:

### 3.1. Chuẩn hóa và làm sạch bộ dữ liệu Đánh giá (Lỗi 1 & Lỗi 8)
- **Sửa mã gold không tồn tại**: Chuyển `45_2019_QH14__D103__K1` về `45_2019_QH14__D103` (toàn bộ Điều 103 là một chunk).
- **Cập nhật căn cứ pháp luật còn hiệu lực**: Cập nhật câu `t2_14` (hình thức trả lương) sang Điều 96 BLLĐ 2019 thay vì BLLĐ 2012 đã hết hiệu lực.
- **Script tự động hóa**: Sử dụng `scripts/verify_gold_labels.py` trong quy trình CI/CD để đảm bảo mọi gold trong test/dev luôn tồn tại và còn hiệu lực.

### 3.2. Mở rộng truy vấn pháp lý (Legal Query Expansion)
- Tích hợp hàm `expand_legal_query()` chuyển đổi các từ ngữ đời thường (nghỉ ngang -> Điều 39, 40; quỵt lương -> Điều 97; sa thải đột ngột -> Điều 36, 41).
- Giải quyết dứt điểm nhóm lỗi *Khoảng cách từ vựng*, giúp BM25 và Dense nhận diện chính xác ý định pháp lý.

### 3.3. Áp dụng Mở rộng Điều khoản Anh em (Sibling Provision Expansion) & Tăng Top-k (Lỗi 4)
- Khi câu hỏi mang tính tổng quan hoặc hỏi về một Điều, hệ thống tự động bổ sung các Khoản cùng Điều.
- Tăng ngưỡng truy xuất từ `top_k=5` lên `top_k=10-15` trước khi đưa vào Generator, hạn chế tình trạng trượt tài liệu đúng.

### 3.4. Lọc hiệu lực trước khi xếp hạng (Pre-ranking Validity Filter) (Lỗi 10)
- Sửa đổi `LegalRetriever` để lọc các chunk hết hiệu lực trước khi cắt top-k, ngăn không cho các điều khoản hết hiệu lực chiếm chỗ của điều khoản còn hiệu lực.
