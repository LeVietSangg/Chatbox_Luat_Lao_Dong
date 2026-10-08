# Danh mục Corpus Pháp luật Lao động

> **Ngày snapshot**: 01/08/2026  
> **Nguồn dữ liệu**: vbpl.vn (Cơ sở dữ liệu quốc gia về văn bản quy phạm pháp luật)  
> **Tổng số văn bản trong Chỉ mục chung (Shared Index)**: 17 văn bản  
> **Tổng số chunk**: 4,890 đoạn quy định + 49 chunks được chép tay từ file overrides.py (để thay thế cho các chunk bị hết hiệu lực trong các văn bản mạng trạng thái hết hiệu lực một phần)
> **Phương pháp sinh**: Tự động sinh từ `data/structured/corpus.csv` bằng `scripts/generate_catalog.py` (Single Source of Truth).

---

## 1. Tổng quan Thống kê Corpus & Phân định Vai trò

### 1.1. Thống kê theo Hiệu lực Văn bản & Chunk
| Chỉ số | Cấp Chunk | Tỷ lệ Chunk | Cấp Văn bản |
|---|---|---|---|
| **Tổng số đơn vị** | **4,890** | 100% | **17 văn bản** |
| ✅ **Còn hiệu lực** | 4,167 | 85.2% | 11 văn bản |
| ⚠️ **Hết hiệu lực một phần** | *(quản lý cấp chunk)* | *(49 chunk bị bãi bỏ)* | 5 văn bản |
| ❌ **Hết hiệu lực toàn bộ** | 674 | 13.8% | 1 văn bản (BLLĐ 2012) |
| **Tổng số Điều** | 1,397 | - | - |
| **Chunk có cấp Khoản** | 4,696 | 96.0% | - |
| **Chunk có cấp Điểm** | 817 | 16.7% | - |

### 1.2. Thống kê theo Nhóm Vai trò Chức năng trong Chỉ mục Chung
| Nhóm Vai trò Chức năng | Số Văn bản | Tỷ lệ VB | Số Chunk | Tỷ lệ Chunk | Mục đích Nghiên cứu & Vận hành |
|---|---|---|---|---|---|
| 🏛️ **1. Cốt lõi & Hướng dẫn thi hành** | 12 văn bản | 70.6% | 3,352 | 68.5% | Tra cứu và áp dụng hiện hành trong pháp luật lao động |
| ⏳ **2. Đối sánh lịch sử hiệu lực** | 1 văn bản | 5.9% | 674 | 13.8% | Đánh giá lọc hiệu lực thời gian và tra cứu quy định cũ |
| 🎯 **3. Đối chứng nhiễu (Distractor Benchmark)** | 4 văn bản | 23.5% | 864 | 17.7% | Thử thách chống False Positive & đo lường Refusal Accuracy |
| **Tổng cộng** | **17 văn bản** | **100%** | **4,890** | **100%** | **Cơ sở dữ liệu thống nhất (Shared Index)** |

---

## 2. Danh sách Chi tiết 17 Văn bản Quy phạm Pháp luật

| # | Nhóm Vai trò | Loại VB | Tên văn bản | Số hiệu | Ngày có hiệu lực | Trạng thái hiệu lực | Số Điều | Tổng Chunk | Còn HL | Hết HL |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Cốt lõi lao động | Bộ luật | Bộ luật Lao động 2019 | `45/2019/QH14` | 01/01/2021 | ✅ Còn hiệu lực | 220 | 678 | 678 | 0 |
| 2 | Cốt lõi lao động | Luật | Luật Bảo hiểm xã hội | `58/VBHN-VPQH` | 15/08/2025 | ✅ Còn hiệu lực | 141 | 558 | 558 | 0 |
| 3 | Cốt lõi lao động | Nghị định | Nghị định 145/2020/NĐ-CP | `145/2020/NĐ-CP` | 01/02/2021 | ⚠️ Hết hiệu lực một phần | 115 | 390 | 388 | 2 |
| 4 | Cốt lõi lao động | Luật | Luật An toàn, vệ sinh lao động | `84/2015/QH13` | 01/07/2016 | ✅ Còn hiệu lực | 93 | 365 | 365 | 0 |
| 5 | Cốt lõi lao động | Nghị định | Nghị định 12/2022/NĐ-CP | `12/2022/NĐ-CP` | 17/01/2022 | ✅ Còn hiệu lực | 64 | 323 | 323 | 0 |
| 6 | Cốt lõi lao động | Luật | Luật NLĐ Việt Nam đi làm việc ở nước ngoài theo hợp đồng | `69/2020/QH14` | 01/01/2022 | ✅ Còn hiệu lực | 74 | 266 | 266 | 0 |
| 7 | Cốt lõi lao động | Luật | Luật Việc làm | `74/2025/QH15` | 01/01/2026 | ✅ Còn hiệu lực | 55 | 203 | 203 | 0 |
| 8 | Cốt lõi lao động | Nghị định | Nghị định 356/2025/NĐ-CP | `356/2025/NĐ-CP` | 01/01/2026 | ✅ Còn hiệu lực | 42 | 196 | 196 | 0 |
| 9 | Cốt lõi lao động | Luật | Luật Công đoàn | `50/2024/QH15` | 01/07/2025 | ⚠️ Hết hiệu lực một phần | 37 | 175 | 163 | 12 |
| 10 | Cốt lõi lao động | Nghị định | Nghị định 152/2020/NĐ-CP | `152/2020/NĐ-CP` | 15/02/2021 | ⚠️ Hết hiệu lực một phần | 30 | 162 | 130 | 32 |
| 11 | Cốt lõi lao động | Nghị định | Nghị định 70/2023/NĐ-CP | `70/2023/NĐ-CP` | 18/09/2023 | ✅ Còn hiệu lực | 3 | 21 | 21 | 0 |
| 12 | Cốt lõi lao động | Nghị định | Nghị định 293/2025/NĐ-CP | `293/2025/NĐ-CP` | 01/01/2026 | ✅ Còn hiệu lực | 5 | 15 | 15 | 0 |
| 13 | Đối sánh lịch sử | Bộ luật | Bộ luật Lao động 2012 | `10/2012/QH13` | 01/05/2013 | ❌ Hết hiệu lực | 242 | 674 | 0 | 674 |
| 14 | Đối chứng nhiễu | Hiến pháp | Hiến pháp 2013 | `Hiến pháp 2013` | 01/01/2014 | ✅ Còn hiệu lực | 120 | 290 | 290 | 0 |
| 15 | Đối chứng nhiễu | Luật | Luật Thanh tra | `84/2025/QH15` | 01/07/2025 | ⚠️ Hết hiệu lực một phần | 64 | 221 | 219 | 2 |
| 16 | Đối chứng nhiễu | Luật | Luật Người khuyết tật | `51/2010/QH12` | 01/01/2011 | ⚠️ Hết hiệu lực một phần | 53 | 182 | 181 | 1 |
| 17 | Đối chứng nhiễu | Luật | Luật Bảo vệ dữ liệu cá nhân | `91/2025/QH15` | 01/01/2026 | ✅ Còn hiệu lực | 39 | 171 | 171 | 0 |

---

## 3. Ghi chú về Phạm vi Dữ liệu & Thiết kế Thực nghiệm Chỉ mục Chung

### 3.1. Làm rõ Vai trò Đối chứng Nhiễu (Distractor / Negative Control Benchmark)
Trong cơ sở dữ liệu tra cứu và chỉ mục (BM25 + FAISS), sự xuất hiện của **Hiến pháp 2013 (290 đoạn)**, **Luật Thanh tra (221 đoạn)**, **Luật Người khuyết tật (182 đoạn)** và **Luật Bảo vệ dữ liệu cá nhân (171 đoạn)** bên cạnh các văn bản cốt lõi về lao động là một **thiết kế thực nghiệm có chủ đích (Intentional Benchmark Design)**:

1. **Mô phỏng Kho Pháp điển Đa lĩnh vực Thực tế (Anti-Toy Environment):**
   - Trên Cổng thông tin Cơ sở dữ liệu quốc gia về văn bản pháp luật (vbpl.vn), tất cả các văn bản quy phạm pháp luật đều nằm chung trong cùng một hệ thống dữ liệu quốc gia.
   - Nếu xây dựng một chỉ mục chỉ chứa duy nhất văn bản lao động thuần túy, bài toán truy xuất sẽ trở nên phi thực tế (mọi câu hỏi đều dễ dàng match trúng một điều luật lao động ngẫu nhiên). Việc đưa các văn bản bổ trợ/nhiễu vào cùng chỉ mục giúp đánh giá khả năng hoạt động của hệ thống trong môi trường pháp điển hỗn hợp.

2. **Thử thách Khả năng Chống Nhiễu & Chống Bắt nhầm Từ khóa (Disambiguation Challenge):**
   - **Hiến pháp 2013 (`Hiến pháp 2013`, 290 đoạn):** Đạo luật cơ bản có hiệu lực pháp lý cao nhất, chứa các quy định khái quát về quyền con người, quyền công dân, quyền làm việc (Điều 35, Điều 36...). Đây là **đối chứng nhiễu bậc cao (High-level Semantic Distractor)**. Nếu bộ tìm kiếm Dense hoặc BM25 không đủ năng lực phân giải ngữ nghĩa, câu hỏi của người dùng về tình huống lao động cụ thể rất dễ bị trôi dạt (semantic drift) và trích dẫn nhầm Hiến pháp thay vì quy định trực tiếp trong Bộ luật Lao động 2019.
   - **Luật Thanh tra 2025 (`84/2025/QH15`, 221 đoạn):** Chứa các quy định về thẩm quyền, trình tự, thủ tục thanh tra hành chính nhà nước. Đóng vai trò **đối chứng nhiễu về thẩm quyền và thủ tục hành chính**. Phép thử này kiểm tra khả năng hệ thống phân biệt giữa thanh tra nhà nước chung và thanh tra chuyên ngành lao động (Điều 214–217 BLLĐ 2019 và Nghị định 12/2022/NĐ-CP).
   - **Luật Người khuyết tật 2010 (`51/2010/QH12`, 182 đoạn):** Quy định chính sách trợ cấp xã hội và hòa nhập cho người khuyết tật. Đóng vai trò **đối chứng giao thoa biên giới ngữ nghĩa (Domain-boundary Distractor)** đối với các quy định bảo vệ lao động là người khuyết tật (Chương XI BLLĐ 2019), kiểm tra khả năng tách bạch trách nhiệm bảo trợ của Nhà nước với nghĩa vụ hợp đồng của người sử dụng lao động.
   - **Luật Bảo vệ dữ liệu cá nhân 2025 (`91/2025/QH15`, 171 đoạn):** Đóng vai trò **đối chứng biên giới công nghệ & bảo mật**, thách thức hệ thống khi người dùng hỏi về lưu trữ hồ sơ nhân sự, camera giám sát tại nơi làm việc hoặc bảo mật thông tin nhân viên.

3. **Đo lường Năng lực Từ chối Ngoài Phạm vi (Out-of-Scope Refusal Accuracy):**
   - Bộ dữ liệu kiểm thử (Test Set) có 50 câu hỏi ngoài phạm vi (OOD), bao gồm các câu hỏi thuộc thẩm quyền thanh tra hành chính chung, khiếu nại quyết định hành chính, quyền ứng cử bầu cử theo Hiến pháp...
   - Sự hiện diện của các văn bản này trong cùng chỉ mục là điều kiện tiên quyết để kiểm tra: Bộ truy xuất có bị lừa bởi độ tương đồng từ vựng để lấy các văn bản nhiễu hay không, và tầng kiểm định LLM có nhận diện chính xác câu hỏi nằm ngoài phạm vi tư vấn pháp luật lao động để kích hoạt cơ chế từ chối (Refusal) an toàn hay không.

### 3.2. Vai trò của Văn bản Đối sánh Lịch sử Hiệu lực (Bộ luật Lao động 2012)
- **Bộ luật Lao động 2012 (`10/2012/QH13`, 674 đoạn):** Đã hết hiệu lực toàn bộ từ ngày 01/01/2021.
- **Mục đích:** Được lưu giữ trong cơ sở dữ liệu cùng nhãn `het_hieu_luc` nhằm:
  + Kiểm thử năng lực của cơ chế lọc hiệu lực theo thời gian (Temporal Validity Filtering).
  + Kiểm tra khả năng chống ảo giác trích dẫn luật cũ đã bị bãi bỏ khi trả lời các tình huống pháp luật hiện hành.
  + Phục vụ các tình huống tra cứu hồi tố (hợp đồng ký kết trong giai đoạn BLLĐ 2012 có hiệu lực) hoặc đối chiếu so sánh chính sách thay đổi giữa hai thế hệ luật.

### 3.3. Vai trò của 12 Văn bản Cốt lõi & Nghị định Hướng dẫn Thi hành
- Bao gồm Bộ luật Lao động 2019, các Nghị định quy định chi tiết thi hành (NĐ 145/2020/NĐ-CP, NĐ 12/2022/NĐ-CP, NĐ 152/2020/NĐ-CP, NĐ 70/2023/NĐ-CP, NĐ 293/2025/NĐ-CP, NĐ 356/2025/NĐ-CP), cùng các Luật chuyên ngành trực tiếp liên quan mật thiết (Luật Bảo hiểm xã hội, Luật An toàn vệ sinh lao động, Luật Công đoàn, Luật Việc làm, Luật NLĐ Việt Nam đi làm việc ở nước ngoài).
- Đây là nguồn tri thức nền tảng cung cấp căn cứ pháp lý còn hiệu lực cho toàn bộ 7 nhóm chủ đề kiểm thử in-scope.

### 3.4. Thống nhất Số lượng Văn bản Toàn Hệ thống
- **Số văn bản quy phạm pháp luật trong Corpus / Chỉ mục:** **17 văn bản**.
- **Số đoạn quy định (chunks):** **4,890 đoạn + 49 đoạn đc chép tay từ file overrides.py (để thay thế cho các chunk bị hết hiệu lực trong các văn bản mạng trạng thái hết hiệu lực một phần)**.
- **Tính đồng bộ:** Toàn bộ tài liệu (`README.md`, `docs/corpus_catalog.md`), mã nguồn tiền xử lý (`scripts/generate_catalog.py`, `scripts/build_index.py`), và cơ sở dữ liệu (`data/structured/corpus.csv`, `data/structured/corpus.json`, `data/index/`) được chuẩn hóa theo số liệu sinh tự động từ `data/structured/corpus.csv`.
