# Danh mục Corpus Pháp luật Lao động

> **Ngày snapshot**: 01/08/2026  
> **Nguồn**: vbpl.vn  
> **Tổng số văn bản**: 17  
> **Tổng số chunk**: 5.036  

---

## 1. Tổng quan

| Chỉ số | Giá trị |
|--------|---------|
| Tổng số văn bản | 17 |
| Tổng số Điều | 1.400 |
| Tổng số chunk | 5.036 |
| Chunk theo Khoản | 4.800 |
| Số lượng Điểm | 3.081 |
| Còn hiệu lực | 2.792 (55.4%) |
| Hết hiệu lực một phần | 1.569 (31.2%) |
| Hết hiệu lực | 675 (13.4%) |

---

## 2. Danh sách văn bản

### 2.1. Bộ luật

| # | Văn bản | Số hiệu | Ngày HL | Trạng thái | Điều | Chunk |
|---|---------|---------|---------|-----------|------|-------|
| 1 | Bộ luật Lao động (VBHN) | 45/2019/QH14 | 01/01/2021 | ✅ Còn HL | 220 | 683 |
| 2 | Bộ luật Lao động 2012 | 10/2012/QH13 | 01/05/2013 | ❌ Hết HL | 242 | 675 |

### 2.2. Luật

| # | Văn bản | Số hiệu | Ngày HL | Trạng thái | Điều | Chunk |
|---|---------|---------|---------|-----------|------|-------|
| 3 | Luật Bảo hiểm xã hội (VBHN) | 41/2024/QH15 | 01/07/2025 | ✅ Còn HL | 141 | 569 |
| 4 | Luật An toàn, vệ sinh lao động | 84/2015/QH13 | 01/07/2016 | ⚠️ Hết HL một phần | 93 | 365 |
| 5 | Luật Người LĐ VN đi làm việc ở nước ngoài | 69/2020/QH14 | 01/01/2022 | ✅ Còn HL | 74 | 266 |
| 6 | Luật Thanh tra | 84/2025/QH15 | 01/07/2025 | ⚠️ Hết HL một phần | 64 | 218 |
| 7 | Luật Việc làm | 74/2025/QH15 | 01/07/2025 | ✅ Còn HL | 55 | 203 |
| 8 | Luật Người khuyết tật | 51/2010/QH12 | 01/01/2011 | ⚠️ Hết HL một phần | 53 | 182 |
| 9 | Luật Bảo vệ dữ liệu cá nhân | 91/2025/QH15 | 01/01/2026 | ✅ Còn HL | 39 | 171 |
| 10 | Luật Công đoàn | 50/2024/QH15 | 01/07/2025 | ⚠️ Hết HL một phần | 37 | 164 |

### 2.3. Hiến pháp

| # | Văn bản | Số hiệu | Ngày HL | Trạng thái | Điều | Chunk |
|---|---------|---------|---------|-----------|------|-------|
| 11 | Hiến pháp 2013 | HP 2013 | 01/01/2014 | ✅ Còn HL | 120 | 290 |

### 2.4. Nghị định

| # | Văn bản | Số hiệu | Ngày HL | Trạng thái | Điều | Chunk |
|---|---------|---------|---------|-----------|------|-------|
| 12 | NĐ hướng dẫn BLLĐ (ĐK LĐ & QHLĐ) | 145/2020/NĐ-CP | 01/02/2021 | ⚠️ Hết HL một phần | 118 | 479 |
| 13 | NĐ xử phạt vi phạm HC lĩnh vực LĐ | 12/2022/NĐ-CP | 17/01/2022 | ✅ Còn HL | 64 | 328 |
| 14 | NĐ hướng dẫn Luật BVDLCN | 356/2025/NĐ-CP | 01/01/2026 | ✅ Còn HL | 42 | 233 |
| 15 | NĐ về LĐ nước ngoài tại VN | 152/2020/NĐ-CP | 15/02/2021 | ⚠️ Hết HL một phần | 30 | 130 |
| 16 | NĐ mức lương tối thiểu | 293/2025/NĐ-CP | 10/11/2025 | ✅ Còn HL | 5 | 49 |
| 17 | NĐ sửa đổi NĐ 152/2020 | 70/2023/NĐ-CP | 14/09/2023 | ⚠️ Hết HL một phần | 3 | 31 |

---

## 3. Schema dữ liệu

### 3.1. Provision ID

Mỗi chunk được gán một `provision_id` duy nhất theo quy tắc:

```
{mã_văn_bản}__D{số_điều}[__K{số_khoản}]
```

**Ví dụ:**
| provision_id | Ý nghĩa |
|-------------|---------|
| `45_2019_QH14__D13` | BLLĐ 2019, Điều 13 (không có khoản) |
| `45_2019_QH14__D13__K1` | BLLĐ 2019, Điều 13, Khoản 1 |
| `HP_2013__D1` | Hiến pháp 2013, Điều 1 |
| `293_2025_NDCP__D3__K1` | NĐ 293/2025, Điều 3, Khoản 1 |

### 3.2. Metadata fields

| Trường | Kiểu | Mô tả |
|--------|------|-------|
| `provision_id` | string | Mã duy nhất – dùng làm chunk_id |
| `van_ban` | string | Tên và số hiệu văn bản |
| `doc_code` | string | Mã rút gọn |
| `chuong` | string | Chương chứa Điều |
| `dieu` | string | Số Điều |
| `tieu_de_dieu` | string | Tiêu đề của Điều |
| `khoan` | string | Số Khoản (nếu có) |
| `diem` | string | Các Điểm (nếu có) |
| `noi_dung` | string | Nội dung đầy đủ (có tiêu đề Điều) |
| `hieu_luc` | string | `con_hieu_luc` / `het_hieu_luc` / `sua_doi` |
| `ngay_hieu_luc` | string | Ngày bắt đầu có hiệu lực (YYYY-MM-DD) |
| `ngay_het_hieu_luc` | string | Ngày hết hiệu lực (nếu có) |
| `van_ban_sua_doi` | string | Mã VB thay thế/sửa đổi (nếu có) |
| `ghi_chu` | string | Ghi chú bổ sung |

---

## 4. Quy tắc chunking

Theo nguyên tắc trong `project.md`:

1. **Chunk theo Khoản**: mỗi Khoản = 1 chunk (đơn vị nhỏ nhất cho retrieval)
2. **Lùi về Điều**: nếu Điều không có Khoản → cả Điều = 1 chunk
3. **Chèn tiêu đề Điều**: mỗi chunk bắt đầu bằng `Điều X. [Tiêu đề]` để cung cấp ngữ cảnh
4. **Điểm**: nằm trong chunk của Khoản chứa nó, được ghi nhận trong trường `diem`

---

## 5. File đầu ra

| File | Đường dẫn | Mô tả |
|------|----------|-------|
| `corpus.json` | `data/structured/corpus.json` | Toàn bộ corpus dạng JSON |
| `corpus.csv` | `data/structured/corpus.csv` | Toàn bộ corpus dạng CSV |
| `corpus_stats.json` | `data/structured/corpus_stats.json` | Thống kê chi tiết |

---

## 6. Lưu ý

- **BLLĐ 2012** (10/2012/QH13) đã **hết hiệu lực**, được giữ trong corpus để so sánh/tham chiếu.
- **BLLĐ 2019** (45/2019/QH14) là bản **VBHN** (văn bản hợp nhất), đã bao gồm sửa đổi bởi Luật 71/2025/QH15.
- **Luật BHXH** (41/2024/QH15) cũng là bản VBHN, sửa đổi bởi Luật 73/2025 và 84/2025.
- 181 provision_id trùng lặp đã được tự động gán suffix `__dup` để đảm bảo tính duy nhất.
