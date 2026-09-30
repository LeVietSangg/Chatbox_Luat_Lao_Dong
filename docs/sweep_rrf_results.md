# Báo cáo Quét Tham số RRF (Hyperparameter Tuning trên Dev Set)

- **Ngày thực hiện**: 2026-09-30 17:00:02
- **Dữ liệu**: `data/eval/dev_set.json` (95 câu in-scope)
- **Top-K**: 10
- **Retrieval depth**: 50
- **Bộ lọc hiệu lực**: `con_hieu_luc`
- **Expand siblings**: `False`
- **Mục tiêu**: Xác định giá trị phù hợp của hằng số RRF $k$ và trọng số nhánh $\alpha$ trên Dev Set.

## 1. Bảng kết quả thực nghiệm

| $k$ | $\alpha$ (BM25) | Recall@1 | Recall@3 | Recall@5 | MRR@10 | Latency p50 (ms) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 5 | 0.3 | 0.4421 | 0.6316 | 0.6947 | 0.5527 | 50.66 |
| 5 | 0.5 | 0.4632 | 0.6632 | 0.7158 | 0.5777 ⭐ | 44.30 |
| 5 | 0.7 | 0.3895 | 0.6000 | 0.6737 | 0.5200 | 77.21 |
| 10 | 0.3 | 0.4632 | 0.6526 | 0.6947 | 0.5646 | 77.34 |
| 10 | 0.5 | 0.4632 | 0.6316 | 0.6947 | 0.5732 | 76.93 |
| 10 | 0.7 | 0.4000 | 0.6000 | 0.6526 | 0.5237 | 76.91 |
| 20 | 0.3 | 0.4737 | 0.6526 | 0.6947 | 0.5726 | 76.64 |
| 20 | 0.5 | 0.4526 | 0.6421 | 0.6842 | 0.5662 | 77.00 |
| 20 | 0.7 | 0.4000 | 0.6105 | 0.6632 | 0.5240 | 76.24 |
| 60 | 0.3 | 0.4632 | 0.6526 | 0.6947 | 0.5662 | 75.26 |
| 60 | 0.5 | 0.4526 | 0.6316 | 0.6737 | 0.5577 | 76.40 |
| 60 | 0.7 | 0.4000 | 0.6211 | 0.6737 | 0.5277 | 76.46 |

## 2. Lựa chọn tham số

Cấu hình được lựa chọn trên Dev Set là **$k = 5$** và **$\alpha = 0.5$**, với MRR@10 = `0.5777` và Recall@5 = `0.7158`. Tiêu chí lựa chọn ưu tiên MRR@10 và sử dụng Recall@5 làm tiêu chí phụ khi MRR@10 bằng nhau.
