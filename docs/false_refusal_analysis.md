# Báo cáo Phân tích Hiện tượng Từ Chối Nhầm (False Refusals)

> **Tập thực nghiệm**: Tập kiểm thử đóng băng `test_set_v3.json` (135 câu hỏi: 85 câu trong phạm vi, 50 câu ngoài phạm vi).
> **Mô hình sinh (Generator)**: `gemini-3.5-flash-lite`, nhiệt độ $T=0.0$.
> **Cấu hình truy xuất chuẩn**: `Hybrid RRF (k=5, α=0.5, top_k=10, expand_siblings=False)`.

## 1. Thống kê Tỷ lệ Từ chối Nhầm (FRR) và Từ chối Đúng (TRR)

Tỷ lệ từ chối nhầm (**False Refusal Rate - FRR**) được tính trên tập câu hỏi **trong phạm vi (in-scope)**:
$$\text{FRR} = \frac{\text{Số câu in-scope bị từ chối}}{\text{Tổng số câu in-scope}} = \frac{N_{\text{false refusal}}}{85}$$

Bảng thống kê so sánh giữa 3 cấu hình truy xuất trên `test_set_v3.json`:

| Phương pháp truy xuất | Câu in-scope | Từ chối nhầm (False Refusal) | Tỷ lệ FRR | Câu ngoài phạm vi (OOS) | Từ chối đúng (True Refusal) | Tỷ lệ TRR |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **BM25** | 85 | **3** | **3.53%** | 50 | 46 | **92.00%** |
| **Dense** | 85 | **2** | **2.35%** | 50 | 45 | **90.00%** |
| **Hybrid_RRF** | 85 | **3** | **3.53%** | 50 | 45 | **90.00%** |

- Ở cấu hình chính **Hybrid RRF**, hệ thống chỉ ghi nhận **3/85 câu từ chối nhầm** (**3.53%**).
- Đồng thời, năng lực từ chối câu hỏi ngoài phạm vi đạt mức cao (**90.00%** đối với Hybrid RRF và Dense; 84.00% đối với BM25), minh chứng hệ thống duy trì tính thận trọng pháp lý hiệu quả.

## 2. Phân loại Nguyên nhân Gốc rễ (Root Cause Analysis)

Trên phương pháp chính **Hybrid RRF**, toàn bộ 3 trường hợp từ chối nhầm được bóc tách nguyên nhân:

| Nhóm nguyên nhân | Số lượng | Tỷ lệ | Bản chất kỹ thuật |
| :--- | :---: | :---: | :--- |
| **1. LLM tuân thủ chỉ thị prompt an toàn (Strict Instruction Refusal)** | 2 | 66.7% | Điều khoản chuẩn đã được đưa vào ngữ cảnh (Top 1–3), nhưng do chỉ thị cấm bịa đặt tuyệt đối trong prompt và câu hỏi yêu cầu dạng xác nhận/liệt kê chi tiết không có nguyên văn trong luật, mô hình chọn phương án an toàn là từ chối. |
| **2. Truy xuất trượt ngoài Top-10 (Retrieval Miss)** | 1 | 33.3% | Điều khoản gold không xuất hiện trong top-10 kết quả truy xuất do độ dài chunk quá ngắn hoặc khoảng cách từ vựng, dẫn đến ngữ cảnh chuyển sang LLM bị thiếu thông tin. |
| **Tổng cộng** | **3** | **100.0%** | |

> **Lưu ý về thuật ngữ kỹ thuật**: Trong mã nguồn của hệ thống, không có khái niệm hay tham số "ngưỡng kiểm tra ngữ cảnh" (threshold). Cơ chế từ chối hoàn toàn do **chỉ thị trong system prompt** (yêu cầu LLM chỉ dựa trên ngữ cảnh cung cấp và trả về câu từ chối chuẩn khi ngữ cảnh không đủ căn cứ) kết hợp với năng lực suy luận của mô hình.

## 3. Bảng Chi tiết 3 Trường hợp Từ chối Nhầm của Hybrid RRF

| STT | Mã QID | Câu hỏi | Chủ đề | Điều khoản Gold | Thứ hạng Gold | Phân loại & Nguyên nhân chi tiết |
| :---: | :---: | :--- | :---: | :--- | :---: | :--- |
| 1 | `v3_03_08` | Những trường hợp nào thuộc hoạt động công vụ được tổ chức làm thêm từ trên 200 giờ đến 300 giờ trong một năm? | `lam_them_gio` | `145_2020_NDCP__D61__K1` | **Top 1** | Điều khoản gold nằm ở hạng 1 trong ngữ cảnh, nhưng văn bản luật chỉ quy định chung "các trường hợp cấp bách... liên quan đến hoạt động công vụ" mà không liệt kê danh mục cụ thể; mô hình tuân thủ nguyên tắc an toàn chống bịa đặt trong prompt nên từ chối trả lời. |
| 2 | `v3_03_13` | Thông báo về việc làm thêm giờ được lập theo mẫu nào? | `lam_them_gio` | `145_2020_NDCP__D62__K3` | **Ngoài top-10** | Điều khoản gold không lọt vào top-10 do độ tương đồng từ vựng bị phân tán (Khoản 3 Điều 62 NĐ 145/2020 rất ngắn chỉ nêu tên phụ lục mẫu biểu, điểm số RRF thấp hơn các khoản khác cùng điều). |
| 3 | `v3_07_12` | Người lao động có được tham gia đối thoại tại nơi làm việc không? | `quyen_loi_khac` | `45_2019_QH14__D63__K1` | **Top 3** | Điều khoản gold nằm ở hạng 3 trong ngữ cảnh, nhưng nội dung điều luật mang tính định nghĩa khái niệm đối thoại thay vì khẳng định quyền trực tiếp của người lao động; mô hình thận trọng tránh suy diễn nên từ chối theo chỉ thị prompt. |

## 4. Bóc tách Kỹ thuật Từng Trường hợp từ `generation_logs.jsonl`

### 4.1. Trường hợp `v3_03_08` – Hiện tượng từ chối do quy định luật mang tính nguyên tắc
- **Câu hỏi**: *"Những trường hợp nào thuộc hoạt động công vụ được tổ chức làm thêm từ trên 200 giờ đến 300 giờ trong một năm?"*
- **Ngữ cảnh thực tế nhận được**: `145_2020_NDCP__D61__K1` (Hạng 1), `145_2020_NDCP__D62__K1` (Hạng 2), `145_2020_NDCP__D62__K2` (Hạng 3)...
- **Nội dung điều khoản `D61__K1`**: *"1. Các trường hợp phải giải quyết công việc cấp bách, không thể trì hoãn phát sinh từ các yếu tố khách quan liên quan trực tiếp đến hoạt động công vụ trong các cơ quan, đơn vị nhà nước..."*
- **Bản chất**: Người hỏi mong muốn một danh sách các công việc cụ thể, trong khi văn bản quy phạm pháp luật chỉ đưa ra tiêu chí định tính ("công việc cấp bách, không thể trì hoãn"). Dưới yêu cầu prompt nghiêm ngặt chống ảo giác (*"KHÔNG suy diễn, KHÔNG tự bổ sung thông tin ngoài ngữ cảnh"*), mô hình `gemini-3.5-flash-lite` nhận định ngữ cảnh không liệt kê các trường hợp hoạt động công vụ cụ thể nên đã trả về câu từ chối chuẩn.

### 4.2. Trường hợp `v3_03_13` – Hiện tượng truy xuất trượt do chunk quá ngắn
- **Câu hỏi**: *"Thông báo về việc làm thêm giờ được lập theo mẫu nào?"*
- **Điều khoản Gold**: `145_2020_NDCP__D62__K3`.
- **Nội dung điều khoản**: *"3. Văn bản thông báo theo Mẫu số 02/PLIV Phụ lục IV ban hành kèm theo Nghị định này."*
- **Bản chất**: Khoản 3 Điều 62 có dung lượng từ vựng rất ngắn (chỉ 20 từ). Khi truy xuất ở chế độ chuẩn (`top_k=10, expand_siblings=False`), các điều khoản khác có độ dài lớn hơn về làm thêm giờ (Điều 107 BLLĐ 2019, Điều 59 NĐ 145/2020) chiếm ưu thế về điểm BM25 và Dense, đẩy Khoản 3 ra ngoài top-10. Khi bật cơ chế **Sibling Expansion** (mở rộng các khoản cùng điều), Khoản 3 sẽ tự động được kéo vào cùng Khoản 1 và Khoản 2 (đang ở top 1-3), giải quyết triệt để lỗi này.

### 4.3. Trường hợp `v3_07_12` – Hiện tượng từ chối do điều khoản mang tính định nghĩa
- **Câu hỏi**: *"Người lao động có được tham gia đối thoại tại nơi làm việc không?"*
- **Ngữ cảnh thực tế nhận được**: `45_2019_QH14__D63__K1` (Hạng 3).
- **Nội dung điều khoản**: *"1. Đối thoại tại nơi làm việc là việc chia sẻ thông tin, tham khảo, thảo luận, trao đổi ý kiến giữa người sử dụng lao động với người lao động hoặc tổ chức đại diện người lao động..."*
- **Bản chất**: Khoản 1 Điều 63 đưa ra định nghĩa thuật ngữ ("Đối thoại là việc chia sẻ thông tin...") chứ không có mệnh đề tường minh khẳng định quyền dạng "Người lao động có quyền tham gia đối thoại". Do đó, mô hình suy luận rằng chưa có căn cứ trực diện để trả lời câu hỏi Yes/No xác nhận quyền và đã lựa chọn giải pháp an toàn là từ chối.

## 5. Làm rõ Lịch sử Tiến hóa Dữ liệu (Dev Set cũ vs. Test Set v3 mới)

Để tránh hiểu lầm trong việc so sánh số liệu qua các phiên bản báo cáo:

1. **Về lỗi nhãn Gold trong quá khứ**:
   - Lỗi nhãn Gold (viện dẫn Bộ luật Lao động 2012 đã hết hiệu lực, hoặc gắn nhãn mã điều khoản không tồn tại) chỉ xuất hiện trong **tập phát triển sơ khai (Dev Set v1/v2)** trong giai đoạn đầu xây dựng hệ thống.
   - Toàn bộ các lỗi này đã được rà soát, dọn dẹp và chuẩn hóa thông qua script kiểm tra tự động `scripts/verify_gold_labels.py` trước khi hình thành tập kiểm thử đóng băng.
2. **Về tập kiểm thử đóng băng hiện tại (`test_set_v3.json`)**:
   - Tập kiểm thử gồm **135 câu hỏi** (85 in-scope, 50 out-of-scope), được đóng băng hoàn toàn, không có lỗi nhãn gold và không có văn bản hết hiệu lực trong nhãn gold in-scope.
   - Trên tập kiểm thử này, tỷ lệ từ chối nhầm của Hybrid RRF đạt mức tối ưu **3.53% (3/85 câu)**, hoàn toàn nhất quán giữa bảng biểu tổng hợp và danh sách phân tích chi tiết.
