# data/eval/archive/README.md

Thư mục này chứa các file kết quả từ lần thực nghiệm ban đầu (Baseline, commit `1f50c5e`, ngày 06/09/2026)
trước khi test set và mã nguồn được chỉnh sửa.

## Nội dung

| File | Mô tả |
|---|---|
| `week6_generation_results_old.json` | Kết quả Generation lần chạy đầu trên test set v1.0 gốc (commit `1f50c5e`) |
| `week6_retrieval_results_old.json` | Kết quả Retrieval Evaluation lần chạy đầu trên test set v1.0 gốc (commit `1f50c5e`) |
| `generation_logs.jsonl` | Nhật ký chi tiết của các lượt sinh câu trả lời trong quá trình thực nghiệm |

## Bối cảnh

- **Commit baseline:** `1f50c5e` (06/09/2026)  
- **Commit sau chỉnh sửa:** `0e94425` (17/09/2026) — sửa 17 câu trong test set, viết lại prompt, tối ưu retriever.
- Các file kết quả hiện tại trong `data/eval/` (ngoài thư mục `archive/`) tương ứng với phiên bản sau chỉnh sửa.
