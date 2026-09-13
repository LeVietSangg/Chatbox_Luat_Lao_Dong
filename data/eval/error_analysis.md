# Phân tích lỗi (Error Analysis) - Tuần 7

## Tổng quan: BM25

| Chỉ số | Giá trị |
|--------|---------|
| Tổng câu hỏi | 120 |
| In-scope | 95 |
| Out-of-scope | 25 |
| Đã trả lời (in-scope) | 68 |
| False Refusal | 27 (28.42%) |
| False Accept | 1 |
| Refusal Accuracy | 96.00% |
| Citation Validity | 98.53% |
| Citation Exact Match | 79.41% |
| Hallucination Cases | 1 |

## Tổng quan: Dense

| Chỉ số | Giá trị |
|--------|---------|
| Tổng câu hỏi | 120 |
| In-scope | 95 |
| Out-of-scope | 25 |
| Đã trả lời (in-scope) | 76 |
| False Refusal | 19 (20.00%) |
| False Accept | 0 |
| Refusal Accuracy | 100.00% |
| Citation Validity | 96.05% |
| Citation Exact Match | 72.37% |
| Hallucination Cases | 3 |

## Tổng quan: Hybrid_RRF

| Chỉ số | Giá trị |
|--------|---------|
| Tổng câu hỏi | 120 |
| In-scope | 95 |
| Out-of-scope | 25 |
| Đã trả lời (in-scope) | 77 |
| False Refusal | 18 (18.95%) |
| False Accept | 0 |
| Refusal Accuracy | 100.00% |
| Citation Validity | 97.40% |
| Citation Exact Match | 80.52% |
| Hallucination Cases | 2 |

---

# Chi tiết phân tích lỗi: Hybrid_RRF

## 1. False Refusals (câu in-scope bị từ chối sai)

Tổng: **18/95** câu in-scope bị từ chối sai.

| # | QID | Câu hỏi | Gold ID | Gold có trong Retrieved? | Nguyên nhân |
|---|-----|---------|---------|--------------------------|-------------|
| 1 | t1_08 | Hợp đồng lao động vô hiệu khi nào?... | 45_2019_QH14__D49__K1 | ✗ | Retriever Miss |
| 2 | t2_14 | Khi thay đổi hình thức trả lương công ty phải báo ... | 10_2012_QH13__D94__K1 | ✗ | Retriever Miss |
| 3 | t3_02 | Làm thêm giờ tối đa trong một năm là bao nhiêu?... | 45_2019_QH14__D107__K2 | ✗ | Retriever Miss |
| 4 | t3_03 | Làm thêm giờ tối đa trong một tháng là bao nhiêu g... | 45_2019_QH14__D107__K2 | ✗ | Retriever Miss |
| 5 | t3_10 | Công ty huy động làm thêm giờ trong trường hợp khẩ... | 45_2019_QH14__D108__K2 | ✗ | Retriever Miss |
| 6 | t3_11 | Khi tổ chức làm thêm giờ, người sử dụng lao động p... | 45_2019_QH14__D107__K4 | ✓ | LLM Miss (context có nhưng LLM vẫn từ chối) |
| 7 | t3_13 | Trường hợp đặc biệt nào được làm thêm đến 300 giờ ... | 45_2019_QH14__D107__K3 | ✗ | Retriever Miss |
| 8 | t5_01 | Người sử dụng lao động có quyền đơn phương chấm dứ... | 45_2019_QH14__D36__K1 | ✗ | Retriever Miss |
| 9 | t5_02 | Người lao động được đơn phương chấm dứt hợp đồng l... | 45_2019_QH14__D35__K2 | ✗ | Retriever Miss |
| 10 | t5_03 | Người lao động bị bệnh nghỉ thì có bị chấm dứt hợp... | 45_2019_QH14__D37__K1 | ✗ | Retriever Miss |
| 11 | t5_05 | Người lao động nghỉ việc có được hưởng trợ cấp thô... | 45_2019_QH14__D46__K1 | ✗ | Retriever Miss |
| 12 | t6_02 | Điều kiện hưởng lương hưu hằng tháng là gì?... | 58_VBHN-VPQH__D54__K1 | ✗ | Retriever Miss |
| 13 | t6_05 | Điều kiện hưởng chế độ thai sản khi sinh con?... | 58_VBHN-VPQH__D31__K1 | ✗ | Retriever Miss |
| 14 | t6_08 | Người lao động ốm đau được nghỉ bao nhiêu ngày một... | 58_VBHN-VPQH__D26__K1 | ✗ | Retriever Miss |
| 15 | t6_11 | Rút BHXH một lần được thực hiện trong điều kiện nà... | 58_VBHN-VPQH__D60__K1 | ✗ | Retriever Miss |
| 16 | t6_12 | Trợ cấp mai táng phí được bao nhiêu tháng lương cơ... | 58_VBHN-VPQH__D85__K2 | ✓ | LLM Miss (context có nhưng LLM vẫn từ chối) |
| 17 | t7_05 | Người lao động bị bệnh nghề nghiệp được hưởng chế ... | 84_2015_QH13__D38__K3 | ✗ | Retriever Miss |
| 18 | t7_14 | Quyền của chủ thể dữ liệu đối với dữ liệu của mình... | 91_2025_QH15__D3__K3 | ✗ | Retriever Miss |

**Phân loại nguyên nhân False Refusal:**
- Retriever Miss (không tìm được gold provision): **16**
- LLM Miss (context đúng nhưng LLM vẫn từ chối): **2**
- API Error: **0**

## 2. False Accepts (câu out-of-scope bị trả lời sai)

**Không có False Accept nào.** Mọi câu out-of-scope đều bị từ chối đúng. ✓

## 3. Hallucinated Citations

Tổng: **2** câu có citation ảo giác.

| # | QID | Câu hỏi | Hallucinated IDs | Loại |
|---|-----|---------|------------------|------|
| 1 | t5_11 | Khi chấm dứt hợp đồng lao động, công ty phải ... | ['45_2019_QH14__D48__K1__d', '45_2019_QH14__D48__K1__a', '45_2019_QH14__D48__K1__c'] | Sub-ID |
| 2 | t6_07 | Lao động nam có vợ sinh con được nghỉ thai sả... | ['58_VBHN-VPQH__D53__K2__b', '58_VBHN-VPQH__D53__K2__a', '58_VBHN-VPQH__D53__K2__c'] | Sub-ID |

**Phân loại Hallucination:**
- Sub-ID (LLM tự sinh ID con như `__Da`, `__Db`): **8**
- Multi-ID (LLM gộp nhiều ID vào 1 ngoặc vuông): **0**
- Fabricated (LLM bịa ID hoàn toàn): **0**

## 4. Citation Mismatch (trả lời nhưng trích dẫn sai provision)

Tổng: **14** câu có câu trả lời nhưng citation không khớp gold_provision_ids.

| # | QID | Câu hỏi | Gold IDs | LLM Citations |
|---|-----|---------|----------|---------------|
| 1 | t1_09 | Quyền của người lao động khi hợp đồng lao độn... | 45_2019_QH14__D51__K1 | 145_2020_NDCP__D10__K2, 145_2020_NDCP__D11__K2 |
| 2 | t2_09 | Chế độ phụ cấp, trợ cấp được ghi ở đâu?... | 45_2019_QH14__D103__K1 | 45_2019_QH14__D103 |
| 3 | t4_05 | Cách tính ngày nghỉ phép hằng năm khi làm việ... | 45_2019_QH14__D113__K2 | 145_2020_NDCP__D66__K1, 145_2020_NDCP__D66__K2 |
| 4 | t5_12 | Công ty có trách nhiệm trả lại sổ bảo hiểm xã... | 45_2019_QH14__D48__K3 | 58_VBHN-VPQH__D13__K1 |
| 5 | t6_01 | Đối tượng nào phải tham gia BHXH bắt buộc?... | 58_VBHN-VPQH__D2__K1 | 58_VBHN-VPQH__D3__K3 |
| 6 | t6_03 | Doanh nghiệp phải đóng BHXH theo tỷ lệ bao nh... | 58_VBHN-VPQH__D86__K1 | 58_VBHN-VPQH__D32__K1 |
| 7 | t6_06 | Mức hưởng chế độ thai sản là bao nhiêu?... | 58_VBHN-VPQH__D39__K1 | 58_VBHN-VPQH__D95__K1 |
| 8 | t6_09 | Mức hưởng chế độ ốm đau tính như thế nào?... | 58_VBHN-VPQH__D28__K1 | 58_VBHN-VPQH__D45__K1, 58_VBHN-VPQH__D45__K5 |
| 9 | t6_10 | Thời gian nghỉ dưỡng sức sau thai sản là bao ... | 58_VBHN-VPQH__D41__K1 | 58_VBHN-VPQH__D60__K2 |
| 10 | t6_13 | Mức bình quân tiền lương tháng đóng BHXH tính... | 58_VBHN-VPQH__D62__K1 | 58_VBHN-VPQH__D72__K3, 58_VBHN-VPQH__D72__K1 |
| 11 | t7_01 | Người sử dụng lao động có trách nhiệm gì tron... | 84_2015_QH13__D16__K1 | 84_2015_QH13__D16__K2, 45_2019_QH14__D134__K1 |
| 12 | t7_02 | Khi xảy ra tai nạn lao động, người sử dụng la... | 84_2015_QH13__D38__K1 | 84_2015_QH13__D67__K2, 84_2015_QH13__D34__K1 |
| 13 | t7_06 | Người lao động có quyền từ chối làm việc khi ... | 84_2015_QH13__D6__K1 | 84_2015_QH13__D12__K5 |
| 14 | t7_11 | Công đoàn có quyền đại diện cho tập thể người... | 50_2024_QH15__D11__K2 | 84_2015_QH13__D10__K2 |

---

# So sánh chéo 3 Pipeline

## Câu hỏi chỉ một pipeline trả lời đúng (unique wins)

- **BM25** unique wins: **1** câu
  - [t3_03] Làm thêm giờ tối đa trong một tháng là bao nhiêu giờ?
- **Dense** unique wins: **3** câu
  - [t5_05] Người lao động nghỉ việc có được hưởng trợ cấp thôi việc khô
  - [t6_01] Đối tượng nào phải tham gia BHXH bắt buộc?
  - [t7_02] Khi xảy ra tai nạn lao động, người sử dụng lao động phải làm
- **Hybrid_RRF** unique wins: **2** câu
  - [t1_01] Thời gian thử việc tối đa đối với lao động phổ thông là bao 
  - [t1_13] Hợp đồng lao động bằng miệng có giá trị pháp lý không?

---

# Bảng tổng hợp kết quả Retrieval

| Metric | BM25 | Dense | Hybrid RRF |
|--------|------|-------|------------|
| MRR@10 | 0.3970 | 0.4326 | **0.4833** |
| Recall@1 | 0.2421 | 0.3053 | **0.3474** |
| Recall@3 | 0.5263 | 0.5579 | **0.6105** |
| Recall@5 | 0.6421 | 0.6316 | **0.6947** |
