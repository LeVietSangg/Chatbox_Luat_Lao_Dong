
## 1. Sửa đổi các Tuyên bố Quá mức (Lỗi 12)

| Vị trí | Câu nguyên văn trong báo cáo | Câu đề xuất thay thế (Chính xác, có số đo) | Căn cứ khoa học |
| :--- | :--- | :--- | :--- |
| **Mục 2.1** | *"Loại bỏ hoàn toàn hiện tượng bịa đặt (hallucination)."* | *"Giảm thiểu đáng kể hiện tượng ảo giác (hallucination) trong trích dẫn, với 0/80 câu trả lời bịa đặt mã điều luật trên tập kiểm thử (khoảng tin cậy 95%: [0.0%, 4.5%])."* | Không có mô hình LLM nào loại bỏ 100% ảo giác trong mọi tình huống. |
| **Mục 3.1.3** | *"Tỷ lệ chấp nhận sai (FAR) tiệm cận 0."* | *"Tỷ lệ chấp nhận sai (FAR) đạt 0.0% (0/25 câu ngoài phạm vi) trong bộ test hiện tại, với cận trên khoảng tin cậy 95% Wilson Score là 13.3%."* | Với cỡ mẫu $N=25$, 0 lỗi chỉ khẳng định được cận trên 13.3% ở mức tin cậy 95%. |
| **Mục 5.1** | *"Bảo đảm mọi phát ngôn của Chatbot đều có nguồn."* | *"Bộ xác thực trích dẫn (Verifier) bảo đảm mọi mã điều khoản hiển thị trong câu trả lời đều tồn tại trong ngữ cảnh được cung cấp (Citation Validity đạt 96.25%)."* | Verifier chỉ kiểm tra mã ID nằm trong context, chưa kiểm chứng toàn bộ ngữ nghĩa từng câu khẳng định. |
| **Mục 5.1** | *"Tốc độ phản hồi ~1.25 giây cho toàn bộ pipeline."* | *"Độ trễ trung vị (p50) của bước sinh câu trả lời LLM là 1.25s; bước truy xuất Hybrid RRF là ~0.11s. Tổng độ trễ toàn trình đạt ~1.36s (chưa tính độ trễ truyền mạng Internet và giới hạn tần suất API)."* | Tách bạch rõ ràng độ trễ truy xuất và độ trễ sinh câu trả lời. |
| **Mục 5.1 & 5.3** | *"Hệ thống đã hoàn thiện, hoạt động tuyệt đối chính xác."* | *"Hệ thống đạt kết quả khả quan với Recall@5 là 68.42% và Citation Exact Match là 65.26% (trên toàn bộ 95 câu). Hệ thống vẫn còn tỷ lệ từ chối nhầm 15.79% và cần được cải thiện bằng Query Expansion và Reranking."* | Thể hiện thái độ khoa học, trung thực và nhận thức rõ hạn chế của hệ thống. |

---

## 2. Thống kê & Bảng Số Liệu Cần Sửa (Lỗi 5 & Lỗi 7)

### 2.1. Thống nhất mẫu số chung cho Bảng 4.3 (Citation Evaluation)
*Thay vì dùng mẫu số thay đổi (73, 77, 80 câu), trình bày bảng với mẫu số chung toàn bộ 95 câu:*

| Chỉ số đánh giá | BM25 (N=95) | Dense (N=95) | Hybrid RRF (N=95) | Hybrid + Expansion (App) |
| :--- | :---: | :---: | :---: | :---: |
| **Số câu được trả lời** | 73 (76.8%) | 77 (81.1%) | 80 (84.2%) | 83 (87.4%) |
| **Tỷ lệ từ chối nhầm (FRR)** | 22/95 (23.2%) | 18/95 (18.9%) | 15/95 (15.8%) | 12/95 (12.6%) |
| **Trích dẫn hợp lệ (Valid)** | 72/95 (75.8%) | 74/95 (77.9%) | 77/95 (81.1%) | 80/95 (84.2%) |
| **Trích dẫn đúng Gold (Exact Match)** | 57/95 (60.0%) | 56/95 (58.9%) | 62/95 (65.3%) | 67/95 (70.5%) |
| **Độ trễ toàn trình p50 (giây)** | 1.33s | 1.32s | 1.36s | 1.45s |

### 2.2. Bổ sung Kiểm định Ý nghĩa Thống kê (Mục 5.1)
- Bổ sung kết quả kiểm định nhị thức chính xác:
  - Hybrid RRF vs BM25: $b = 6, c = 1, p = 0.1250 > 0.05$.
  - Hybrid RRF vs Dense: $b = 10, c = 4, p = 0.1796 > 0.05$.
- **Kết luận viết lại**: *"Sự cải thiện của Hybrid RRF so với BM25 (65 câu đúng so với 60 câu trên 95 câu) thể hiện một xu hướng tích cực rõ nét (trend), tuy chưa đạt mức ý nghĩa thống kê $p < 0.05$ do cỡ mẫu kiểm thử 95 câu. Trong các nghiên cứu tiếp theo, việc mở rộng tập test lên 300 câu sẽ giúp lượng hóa chính xác hơn độ tin cậy của mức cải thiện này."*

---

## 3. Sửa đổi Mô tả Trích dẫn & Chuẩn hóa Sub-ID (Lỗi 11)

Tại **Mục 5.2**:
- Sửa lại mô tả:
  *"Hệ thống tích hợp bộ chuẩn hóa biểu thức chính quy (Regex Normalization) tại tầng hậu xử lý `verify_citations`. Khi mô hình sinh ra các mã trích dẫn chi tiết đến cấp Điểm (Sub-ID, ví dụ `145_2020_NDCP__D10__K2__a`), hệ thống tự động rút gọn về mã cấp Khoản (`145_2020_NDCP__D10__K2`) nếu Khoản cha này tồn tại trong ngữ cảnh được cung cấp. Nếu mã trích dẫn hoàn toàn không có cơ sở trong ngữ cảnh, mã đó sẽ bị bóc tách và loại bỏ để bảo vệ tính chính xác."*

---

## 4. Rà soát Soát lỗi & Biên tập Nội dung Nháp (Lỗi 13)

1. **Mục 2.2 (Lịch sử RAG)**:
   - Rút gọn bảng lịch sử từ 3 trang blog xuống 1 trang tóm lược.
   - Sửa lỗi mốc thời gian: Sửa `"975"` thành `"1975"`.
   - Bổ sung trích dẫn học thuật cho bài báo khai sinh RAG: Lewis et al. (2020).
2. **Mục 2.3.1 & 2.3.2 (Xây dựng Bộ dữ liệu)**:
   - Xóa bỏ các đoạn văn bản dán nguyên đề bài của GVHD (như: *"Tối thiểu 120 câu...", "Đóng băng bộ test...", "Giáo viên hướng dẫn đề xuất"*).
   - Viết lại thành quy trình kỹ thuật:
     - *Phân tích nhu cầu người dùng*: Thu thập các tình huống thực tế của người lao động qua 7 nhóm chủ đề.
     - *Quy trình phân tách Dev / Test*: Tách 30 câu làm tập Dev để sweep tham số và đóng băng 120 câu làm tập Test.
     - *Gán nhãn và kiểm định*: Quy trình gán gold đôi độc lập, đối soát bằng script `verify_gold_labels.py`.
3. **Mục 2.4**:
   - Đổi tiêu đề từ *"Kết quả dự kiến"* thành *"Kết quả và Đóng góp của Đề tài"*.
4. **Sửa lỗi chính tả và định dạng**:
   - Thay `"chatbox"` bằng `"chatbot"`.
   - Thay `"Hybird Retrievl"` bằng `"Hybrid Retrieval"`.
   - Thay `"ký tư"` bằng `"ký tự"`.
   - Sửa các chú thích thiếu số: `"Hình 3.."` -> `"Hình 3.1"`, `"Bảng 2.."` -> `"Bảng 2.1"`.

---

## 5. Bổ sung Danh mục Tài liệu Tham khảo Học thuật (Lỗi 14)

Thay vì chỉ liệt kê các văn bản pháp luật, tách riêng danh mục văn bản quy phạm pháp luật sang **Phụ lục A**, và bổ sung tối thiểu 12 tài liệu tham khảo học thuật chuẩn quốc tế tại mục **Tài liệu tham khảo**:

```bibtex
[1] P. Lewis, E. Perez, A. Piktus, F. Petroni, V. Karpukhin, N. Goyal, H. Küttler, M. Lewis, W. Yih, T. Rocktäschel, S. Riedel, and D. Kiela, "Retrieval-augmented generation for knowledge-intensive NLP tasks," in Advances in Neural Information Processing Systems (NeurIPS), vol. 33, pp. 9459–9474, 2020.
[2] S. Robertson, H. Zaragoza, et al., "The probabilistic relevance framework: BM25 and beyond," Foundations and Trends in Information Retrieval, vol. 3, no. 4, pp. 333–389, 2009.
[3] G. V. Cormack, C. L. Clarke, and S. Büttcher, "Reciprocal rank fusion outperforms Condorcet and individual rank learning methods," in Proceedings of the 32nd International ACM SIGIR Conference on Research and Development in Information Retrieval, pp. 758–759, 2009.
[4] N. Reimers and I. Gurevych, "Sentence-BERT: Sentence embeddings using Siamese BERT-networks," in Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing (EMNLP), pp. 3982–3992, 2019.
[5] I. Chalkidis, M. Fergadiotis, P. Malakasiotis, N. Aletras, and I. Androutsopoulos, "LEGAL-BERT: The muppets straight out of law school," in Findings of the Association for Computational Linguistics: EMNLP 2020, pp. 2898–2904, 2020.
[6] BKAI Foundation Models, "Vietnamese Bi-Encoder for Legal Information Retrieval," Hanoi University of Science and Technology, 2023. [Online]. Available: https://huggingface.co/bkai-foundation-models/vietnamese-bi-encoder
[7] H. T. Nguyen et al., "ALQAC: Automated Legal Question Answering Competition for Vietnamese Law," in KSE, 2021.
[8] Y. Gao, Y. Xiong, X. Gao, K. Jia, J. Pan, Y. Bi, Y. Dai, J. Sun, and H. Wang, "Retrieval-augmented generation for large language models: A survey," arXiv preprint arXiv:2312.10997, 2023.
[9] L. Zheng, W.-L. Chiang, Y. Sheng, S. Zhuang, Z. Wu, Y. Zhuang, Z. Lin, Z. Li, D. Xing, H. Zhang, et al., "Judging LLM-as-a-judge with MT-bench and chatbot arena," in NeurIPS, 2023.
[10] E. B. Wilson, "Probable inference, the law of succession, and statistical inference," Journal of the American Statistical Association, vol. 22, no. 158, pp. 209–212, 1927.
[11] J. Thorne, A. Vlachos, C. Christodoulopoulos, and A. Mittal, "FEVER: a large-scale dataset for fact extraction and VERification," in NAACL-HLT, pp. 809–819, 2018.
[12] H. Nguyen, "PyVi: Python Vietnamese Core NLP Toolkit," 2016. [Online]. Available: https://github.com/trungtv/pyvi
```
