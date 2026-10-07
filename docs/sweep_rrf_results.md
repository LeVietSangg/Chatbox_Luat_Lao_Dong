# Báo cáo Quét Tham số RRF (Hyperparameter Tuning trên Dev Set)

- **Ngày thực hiện**: 2026-10-05 22:50:05
- **Dữ liệu**: `data/eval/dev_set.json` (95 câu in-scope)
- **Top-K**: 10
- **Retrieval depth**: 50
- **Bộ lọc hiệu lực**: `con_hieu_luc`
- **Expand siblings**: `False`
- **Mục tiêu**: Xác định giá trị phù hợp của hằng số RRF $k$ và trọng số nhánh $\alpha$ trên Dev Set.

## 1. Bảng kết quả thực nghiệm

| $k$ | $\alpha$ (BM25) | Recall@1 | Recall@3 | Recall@5 | MRR@10 | Latency p50 (ms) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 5 | 0.3 | 0.4947 | 0.7263 | 0.7895 | 0.6290 | 72.89 |
| 5 | 0.5 | 0.5368 | 0.7684 | 0.8316 | 0.6706 ⭐ | 60.59 |
| 5 | 0.7 | 0.4632 | 0.7158 | 0.7895 | 0.6128 | 59.11 |
| 10 | 0.3 | 0.5158 | 0.7474 | 0.7895 | 0.6426 | 57.11 |
| 10 | 0.5 | 0.5368 | 0.7368 | 0.8105 | 0.6661 | 59.11 |
| 10 | 0.7 | 0.4842 | 0.7053 | 0.7684 | 0.6208 | 59.09 |
| 20 | 0.3 | 0.5263 | 0.7579 | 0.8000 | 0.6524 | 60.30 |
| 20 | 0.5 | 0.5263 | 0.7474 | 0.7895 | 0.6587 | 58.22 |
| 20 | 0.7 | 0.4842 | 0.7158 | 0.7789 | 0.6224 | 60.64 |
| 60 | 0.3 | 0.5263 | 0.7579 | 0.8000 | 0.6530 | 58.14 |
| 60 | 0.5 | 0.5263 | 0.7368 | 0.7789 | 0.6500 | 56.32 |
| 60 | 0.7 | 0.4842 | 0.7263 | 0.7895 | 0.6260 | 58.22 |

## 2. Lựa chọn tham số

Cấu hình được lựa chọn trên Dev Set là **$k = 5$** và **$\alpha = 0.5$**, với MRR@10 = `0.6706` và Recall@5 = `0.8316`. Tiêu chí lựa chọn ưu tiên MRR@10 và sử dụng Recall@5 làm tiêu chí phụ khi MRR@10 bằng nhau.
