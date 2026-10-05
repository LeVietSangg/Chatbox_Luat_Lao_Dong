"""
create_test_set_v3.py
=====================
Khung tạo Test Set V3 (Held-out độc lập hoàn toàn) – 135 câu hỏi (85 in-scope + 50 out-of-scope).
Cấu trúc chuẩn hóa giống create_test_set_v2.py:
  - 1. Hợp đồng lao động: 13 câu 
  - 2. Tiền lương: 17 câu 
  - 3. Làm thêm giờ: 13 câu 
  - 4. Nghỉ phép: 5 câu (bị ít hơn do các bộ test/dev có rồi và vi yêu cầu tính độc lập nên chỉ còn nhiêu đây câu)
  - 5. Chấm dứt hợp đồng: 10 câu 
  - 6. Bảo hiểm: 15 câu 
  - 7. Quyền lợi khác: 12 câu 
  - 8. Ngoài phạm vi: 50 câu 
      * 8.1 Luật khác: 7 câu 
      * 8.2 Tư vấn cá nhân: 6 câu 
      * 8.3 Vô nghĩa / Chat: 6 câu 
      * 8.4 Cận biên giới: 6 câu 
      * 8.5 BHXH / Văn bản pháp luật cũ hết hiệu lực: 8 câu 
      * 8.6 Luật dân sự / Luật gần miền: 17 câu 

LƯU Ý QUAN TRỌNG VỀ TÍNH ĐỘC LẬP & CHỐNG RÒ:
  - Tất cả các câu chừa sẵn phần nội dung câu hỏi ("") và phần gold_provision_ids ([]).
  - Khi điền câu hỏi và nhãn gold, ĐẢM BẢO KHÔNG TRÙNG với dev_set_v2.json:
    + Tuyệt đối không dùng lại 17 mã gold đã xuất hiện trong Dev Set.
    + Tránh các tình huống ngữ nghĩa cận trùng (near-duplicates) với Dev Set.
  - Sau khi điền, script sẽ tự động kiểm tra rò rỉ với dev_set_v2 và sinh mã băm SHA-256 để đóng băng (freeze).
"""

import json
import os
import hashlib
from collections import Counter

questions = []

def add_q(q_id, text, cat, gold):
    questions.append({
        "id": q_id,
        "question": text,
        "category": cat,
        "gold_provision_ids": gold
    })

# =============================================================================
# 1. HỢP ĐỒNG LAO ĐỘNG 
# =============================================================================

add_q("v3_01_01",
      "Ai có thẩm quyền giao kết hợp đồng lao động với người lao động bên phía công ty?",
      "hop_dong_lao_dong",
      ["45_2019_QH14__D18__K3"])

add_q("v3_01_02",
      "Người lao động từ đủ 18 tuổi trở lên có thể tự mình ký hợp đồng lao động không?",
      "hop_dong_lao_dong",
      ["45_2019_QH14__D18__K1"])

add_q("v3_01_03",
      "Hợp đồng lao động là gì?",
      "hop_dong_lao_dong",
      ["45_2019_QH14__D13__K1"])

add_q("v3_01_04",
      "Hợp đồng lao động có hiệu lực từ khi nào?",
      "hop_dong_lao_dong",
      ["45_2019_QH14__D23"])

add_q("v3_01_05",
      "Công việc và địa điểm làm việc của người lao động được thực hiện như thế nào theo hợp đồng lao động?",
      "hop_dong_lao_dong",
      ["45_2019_QH14__D28"])

add_q("v3_01_06",
      "Nguyên tắc giao kết hợp đồng lao động là gì?",
      "hop_dong_lao_dong",
      ["45_2019_QH14__D15__K1"])

add_q("v3_01_07",
      "Phụ lục hợp đồng lao động là gì",
      "hop_dong_lao_dong",
      ["45_2019_QH14__D22__K1"])

add_q("v3_01_08",
      "Nếu chỉ giao kết hợp đồng lao đồng dưới 1 tháng thì có cần thử việc không?",
      "hop_dong_lao_dong",
      ["45_2019_QH14__D24__K3"])

add_q("v3_01_09",
      "Nếu hai bên không thỏa thuận được việc sửa đổi, bổ sung hợp đồng lao động thì hợp đồng đã ký được xử lý như thế nào?",
      "hop_dong_lao_dong",
      ["45_2019_QH14__D33__K3"])

add_q("v3_01_10",
      "Người sử dụng lao động có được yêu cầu người lao động đặt cọc tiền hoặc tài sản để bảo đảm thực hiện hợp đồng không?",
      "hop_dong_lao_dong",
      ["45_2019_QH14__D17__K2"])

add_q("v3_01_11",
      "Hợp đồng lao động xác định thời hạn hết hạn nhưng người lao động vẫn tiếp tục làm việc thì được xử lý như thế nào?",
      "hop_dong_lao_dong",
      ["45_2019_QH14__D20__K2"])

add_q("v3_01_12",
      "Hợp đồng thử việc có những nội dung chủ yếu nào?",
      "hop_dong_lao_dong",
      ["45_2019_QH14__D24__K2"])

add_q("v3_01_13",
      "Người lao động làm việc bán thời gian được hưởng những quyền lợi gì?",
      "hop_dong_lao_dong",
      ["45_2019_QH14__D32__K3"])

# =============================================================================
# 2. TIỀN LƯƠNG 
# =============================================================================

add_q("v3_02_01",
      "Mức lương tối thiểu là gì",
      "tien_luong",
      ["45_2019_QH14__D91__K1"])

add_q("v3_02_02",
      "Mức lương tối thiểu được xác lập dựa trên yếu tố nào?",
      "tien_luong",
      ["45_2019_QH14__D91__K2"])

add_q("v3_02_03",
      "Cơ quan nào quyết định và công bố mức lương tối thiểu",
      "tien_luong",
      ["45_2019_QH14__D91__K4"])

add_q("v3_02_04",
      "Hội đồng tiền lương quốc gia có chức năng gì trong chính sách tiền lương?",
      "tien_luong",
      ["45_2019_QH14__D92__K1"])

add_q("v3_02_05",
      "Hội đồng tiền lương quốc gia gồm đại diện của những tổ chức, cơ quan và thành phần nào?",
      "tien_luong",
      ["45_2019_QH14__D92__K2"])

add_q("v3_02_06",
      "Cơ quan nào quy định chức năng, nhiệm vụ và cơ cấu tổ chức của Hội đồng tiền lương quốc gia?",
      "tien_luong",
      ["45_2019_QH14__D92__K3"])

add_q("v3_02_07",
      "Thang lương, bảng lương và định mức lao động được xây dựng để làm gì?",
      "tien_luong",
      ["45_2019_QH14__D93__K1"])

add_q("v3_02_08",
      "Mức lao động phải đáp ứng những yêu cầu gì?",
      "tien_luong",
      ["45_2019_QH14__D93__K2"])

add_q("v3_02_09",
      "Người sử dụng lao động phải trả lương cho người lao động như thế nào?",
      "tien_luong",
      ["45_2019_QH14__D95__K1"])

add_q("v3_02_10",
      "Người lao động hưởng lương theo sản phẩm hoặc theo khoán được trả lương như thế nào?",
      "tien_luong",
      ["45_2019_QH14__D97__K3"])

add_q("v3_02_11",
      "Nếu người cai thầu không trả đủ lương và quyền lợi cho người lao động thì ai phải chịu trách nhiệm?",
      "tien_luong",
      ["45_2019_QH14__D100__K2"])

add_q("v3_02_12",
      "Người lao động nhập ngũ có được tạm ứng tiền lương không?",
      "tien_luong",
      ["45_2019_QH14__D101__K2"])

add_q("v3_02_13",
      "Khi nghỉ phép năm, người lao động có được tạm ứng tiền lương không?",
      "tien_luong",
      ["45_2019_QH14__D101__K3"])

add_q("v3_02_14",
      "Người sử dụng lao động được khấu trừ tối đa bao nhiêu phần trăm tiền lương của người lao động mỗi tháng?",
      "tien_luong",
      ["45_2019_QH14__D102__K3"])

add_q("v3_02_15",
      "Tiền tàu xe và tiền lương trong những ngày đi đường khi nghỉ phép năm được quy định như thế nào?",
      "tien_luong",
      ["145_2020_NDCP__D67__K1"])

add_q("v3_02_16",
      "Tiền lương làm căn cứ trả cho những ngày nghỉ lễ, Tết, nghỉ hằng năm và nghỉ việc riêng được xác định như thế nào?",
      "tien_luong",
      ["145_2020_NDCP__D67__K2"])

add_q("v3_02_17",
      "Tiền lương làm căn cứ trả cho những ngày nghỉ hằng năm chưa nghỉ khi người lao động thôi việc được xác định như thế nào?",
      "tien_luong",
      ["145_2020_NDCP__D67__K3"])

# =============================================================================
# 3. LÀM THÊM GIỜ 
# =============================================================================

add_q("v3_03_01",
      "Khi tổ chức làm thêm giờ, người sử dụng lao động có phải được sự đồng ý của người lao động về gì?",
      "lam_them_gio",
      ["145_2020_NDCP__D59__K1"])

add_q("v3_03_02",
      "Nếu người lao động đồng ý làm thêm giờ bằng văn bản riêng thì sử dụng mẫu nào?",
      "lam_them_gio",
      ["145_2020_NDCP__D59__K2"])

add_q("v3_03_03",
      "Số giờ làm thêm trong ngày làm việc bình thường được giới hạn như thế nào?",
      "lam_them_gio",
      ["145_2020_NDCP__D60__K1"])

add_q("v3_03_04",
      "Nếu áp dụng thời giờ làm việc bình thường theo tuần thì tổng thời gian làm việc và làm thêm trong một ngày tối đa là bao nhiêu giờ?",
      "lam_them_gio",
      ["145_2020_NDCP__D60__K2"])

add_q("v3_03_05",
      "Đối với người lao động làm việc không trọn thời gian, tổng số giờ làm việc và làm thêm trong một ngày tối đa là bao nhiêu?",
      "lam_them_gio",
      ["145_2020_NDCP__D60__K3"])

add_q("v3_03_06",
      "Khi làm thêm vào ngày nghỉ lễ, tết hoặc ngày nghỉ hằng tuần, tổng số giờ làm thêm trong một ngày tối đa là bao nhiêu giờ?",
      "lam_them_gio",
      ["145_2020_NDCP__D60__K4"])

add_q("v3_03_07",
      "Thời gian nào được giảm trừ khi tính tổng số giờ làm thêm trong tháng và trong năm?",
      "lam_them_gio",
      ["145_2020_NDCP__D60__K5"])

add_q("v3_03_08",
      "Những trường hợp nào thuộc hoạt động công vụ được tổ chức làm thêm từ trên 200 giờ đến 300 giờ trong một năm?",
      "lam_them_gio",
      ["145_2020_NDCP__D61__K1"])

add_q("v3_03_09",
      "Thời giờ làm việc bình thường của người lao động trực tiếp sản xuất, kinh doanh tại doanh nghiệp tối đa bao nhiêu giờ một tuần?",
      "lam_them_gio",
      ["145_2020_NDCP__D61__K3"])

add_q("v3_03_10",
      "Khi tổ chức làm thêm từ trên 200 đến 300 giờ trong một năm, người sử dụng lao động phải thông báo cho cơ quan nào và ở đâu?",
      "lam_them_gio",
      ["145_2020_NDCP__D62__K1"])

add_q("v3_03_11",
      "Người sử dụng lao động phải thông báo việc làm thêm từ trên 200 đến 300 giờ trong năm trong thời hạn bao lâu?",
      "lam_them_gio",
      ["145_2020_NDCP__D62__K2"])

add_q("v3_03_12",
      "Thế nào được xem là làm thêm giờ?",
      "lam_them_gio",
      ["45_2019_QH14__D107__K1"])

add_q("v3_03_13",
      "Thông báo về việc làm thêm giờ được lập theo mẫu nào?",
      "lam_them_gio",
      ["145_2020_NDCP__D62__K3"])

# =============================================================================
# 4. NGHỈ PHÉP 
# =============================================================================

add_q("v3_04_01",
      "Nếu nghỉ phép năm trước kỳ trả lương thì người lao động có được tạm ứng tiền lương không?",
      "nghi_phep",
      ["45_2019_QH14__D113__K5"])

add_q("v3_04_02",
      "Thời gian được coi là thời gian làm việc để tính số ngày nghỉ hằng năm là thời gian nào?",
      "nghi_phep",
      ["145_2020_NDCP__D65__K1"])

add_q("v3_04_03",
      "Người lao động làm việc chưa đủ 12 tháng được tính số ngày nghỉ hằng năm như thế nào?",
      "nghi_phep",
      ["145_2020_NDCP__D66__K1"])

add_q("v3_04_04",
      "Nếu người lao động chưa làm việc đủ tháng thì trong trường hợp nào được tính là 1 tháng làm việc để tính ngày nghỉ hằng năm?",
      "nghi_phep",
      ["145_2020_NDCP__D66__K2"])

add_q("v3_04_05",
      "Thời gian làm việc tại cơ quan nhà nước và doanh nghiệp nhà nước có được tính để tăng thêm ngày nghỉ hằng năm không?",
      "nghi_phep",
      ["145_2020_NDCP__D66__K3"]) 

# =============================================================================
# 5. CHẤM DỨT HỢP ĐỒNG 
# =============================================================================

add_q("v3_05_01",
      "Thời hạn báo trước khi đơn phương chấm dứt hợp đồng lao động đối với các ngành nghề đặc thù là bao lâu?",
      "cham_dut_hop_dong",
      ["145_2020_NDCP__D7__K1"])

add_q("v3_05_02",
      "Các trường hợp bị chấm dứt hợp đồng lao động là?",
      "cham_dut_hop_dong",
      ["45_2019_QH14__D34__K1"])

add_q("v3_05_03",
      "Người sử dụng lao động không phải báo trước cho người lao động khi nào",
      "cham_dut_hop_dong",
      ["45_2019_QH14__D36__K3"])

add_q("v3_05_04",
      "Nếu người lao động nghỉ việc riêng hoặc trường hợp khác thì có bị đơn phương chấm dứt hợp đồng lao động không?",
      "cham_dut_hop_dong",
      ["45_2019_QH14__D37__K2"])

add_q("v3_05_05",
      "Khi đơn phương chấm dứt hợp đồng lao động trái pháp luật thì có được hưởng trợ cấp không?",
      "cham_dut_hop_dong",
      ["45_2019_QH14__D40__K1"])

add_q("v3_05_06",
      "Nếu người lao động không muốn tiếp tục làm việc thì người sử dụng lao động phải trả những khoản tiền gì để chấm dứt hợp đồng lao động?",
      "cham_dut_hop_dong",
      ["45_2019_QH14__D41__K2"])

add_q("v3_05_07",
      "Nếu người sử dụng lao động không muốn nhận lại người lao động thì phải bồi thường thêm ít nhất bao nhiêu tháng tiền lương để chấm dứt hợp đồng lao động?",
      "cham_dut_hop_dong",
      ["45_2019_QH14__D41__K3"])

add_q("v3_05_08",
      "Khi người sử dụng lao động không phải là cá nhân chấm dứt hoạt động thì thời điểm chấm dứt hợp đồng lao động tính từ khi nào?",
      "cham_dut_hop_dong",
      ["45_2019_QH14__D45__K2"])

add_q("v3_05_09",
      "Khi doanh nghiệp, hợp tác xã chấm dứt hoạt động, giải thể hoặc phá sản, các khoản tiền và quyền lợi của người lao động có được ưu tiên thanh toán không?",
      "cham_dut_hop_dong",
      ["45_2019_QH14__D48__K2"])

add_q("v3_05_10",
      "Nếu hợp đồng lao động bị tuyên bố vô hiệu từng phần mà hai bên không thống nhất sửa đổi, bổ sung thì giải quyết như thế nào?",
      "cham_dut_hop_dong",
      ["145_2020_NDCP__D9__K3"])

# =============================================================================
# 6. BẢO HIỂM 
# =============================================================================

add_q("v3_06_01",
      "Người lao động nước ngoài làm việc tại Việt Nam có phải tham gia bảo hiểm xã hội bắt buộc không?",
      "bao_hiem",
      ["58_VBHN-VPQH__D2__K2"])

add_q("v3_06_02",
      "Những người sử dụng lao động nào thuộc đối tượng tham gia bảo hiểm xã hội bắt buộc?",
      "bao_hiem",
      ["58_VBHN-VPQH__D2__K3"])

add_q("v3_06_03",
      "Người thụ hưởng chế độ bảo hiểm xã hội có những quyền gì?",
      "bao_hiem",
      ["58_VBHN-VPQH__D10__K2"])

add_q("v3_06_04",
      "Người tham gia bảo hiểm xã hội có những trách nhiệm gì?",
      "bao_hiem",
      ["58_VBHN-VPQH__D11__K1"])

add_q("v3_06_05",
      "Người thụ hưởng chế độ bảo hiểm xã hội có những trách nhiệm gì?",
      "bao_hiem",
      ["58_VBHN-VPQH__D11__K2"])

add_q("v3_06_06",
      "Giao dịch điện tử trong lĩnh vực bảo hiểm xã hội có giá trị pháp lý như thế nào so với giao dịch bằng bản giấy?",
      "bao_hiem",
      ["58_VBHN-VPQH__D26__K2"])

add_q("v3_06_07",
      "Cơ quan bảo hiểm xã hội phải bảo đảm điều kiện thực hiện giao dịch điện tử chậm nhất khi nào?",
      "bao_hiem",
      ["58_VBHN-VPQH__D26__K3"])

add_q("v3_06_08",
      "Cơ quan nào quy định chi tiết việc chuyển hồ sơ, thủ tục bảo hiểm xã hội từ bản giấy sang giao dịch điện tử?",
      "bao_hiem",
      ["58_VBHN-VPQH__D26__K4"])

add_q("v3_06_09",
      "Hồ sơ đăng ký tham gia bảo hiểm xã hội bắt buộc gồm những gì?",
      "bao_hiem",
      ["58_VBHN-VPQH__D27__K1"])

add_q("v3_06_10",
      "Hồ sơ đăng ký tham gia bảo hiểm xã hội tự nguyện gồm những gì?",
      "bao_hiem",
      ["58_VBHN-VPQH__D27__K3"])

add_q("v3_06_11",
      "Cơ quan bảo hiểm xã hội phải cấp sổ bảo hiểm xã hội trong thời hạn bao lâu kể từ khi nhận đủ hồ sơ?",
      "bao_hiem",
      ["58_VBHN-VPQH__D28__K4"])

add_q("v3_06_12",
      "Khi thông tin đăng ký tham gia bảo hiểm xã hội thay đổi thì cần làm thủ tục gì?",
      "bao_hiem",
      ["58_VBHN-VPQH__D29__K1"])

add_q("v3_06_13",
      "Cơ quan bảo hiểm xã hội phải điều chỉnh thông tin tham gia bảo hiểm xã hội trong thời hạn bao lâu kể từ khi nhận đủ hồ sơ?",
      "bao_hiem",
      ["58_VBHN-VPQH__D29__K2"])

add_q("v3_06_14",
      "Tỷ lệ đóng bảo hiểm xã hội bắt buộc gồm những khoản nào?",
      "bao_hiem",
      ["58_VBHN-VPQH__D32__K1"])

add_q("v3_06_15",
      "Tỷ lệ đóng bảo hiểm xã hội tự nguyện là bao nhiêu?",
      "bao_hiem",
      ["58_VBHN-VPQH__D32__K2"])

# =============================================================================
# 7. QUYỀN LỢI KHÁC 
# =============================================================================

add_q("v3_07_01",
      "Những người làm công tác an toàn, vệ sinh lao động trong cơ sở sản xuất, kinh doanh có phải tham gia huấn luyện không?",
      "quyen_loi_khac",
      ["84_2015_QH13__D14__K1"])

add_q("v3_07_02",
      "Chi phí khám sức khỏe và điều trị bệnh nghề nghiệp cho người lao động do ai chi trả?",
      "quyen_loi_khac",
      ["84_2015_QH13__D21__K6"])

add_q("v3_07_03",
      "Cơ quan, tổ chức có thẩm quyền có trách nhiệm gì khi tiếp nhận tin báo về tai nạn lao động?",
      "quyen_loi_khac",
      ["84_2015_QH13__D34__K2"])

add_q("v3_07_04",
      "Người lao động bị tai nạn lao động do lỗi của chính họ thì được trợ cấp ít nhất bao nhiêu?",
      "quyen_loi_khac",
      ["84_2015_QH13__D38__K5"])

add_q("v3_07_05",
      "Người lao động bị tai nạn lao động hoặc bệnh nghề nghiệp sau điều trị, phục hồi chức năng được bố trí công việc như thế nào?",
      "quyen_loi_khac",
      ["84_2015_QH13__D38__K8"])

add_q("v3_07_06",
      "Việc huấn luyện an toàn, vệ sinh lao động phải được tổ chức như thế nào để phù hợp với đặc điểm của cơ sở sản xuất, kinh doanh?",
      "quyen_loi_khac",
      ["84_2015_QH13__D14__K5"])

add_q("v3_07_07",
      "Hợp đồng của cán bộ công đoàn không chuyên trách hết hạn trong nhiệm kỳ công đoàn thì có được gia hạn không?",
      "quyen_loi_khac",
      ["50_2024_QH15__D28__K1"])

add_q("v3_07_08",
      "Người sử dụng lao động có được đơn phương chấm dứt hợp đồng hoặc sa thải cán bộ công đoàn không chuyên trách không?",
      "quyen_loi_khac",
      ["50_2024_QH15__D28__K2"])

add_q("v3_07_09",
      "Công đoàn có trách nhiệm gì khi cán bộ công đoàn không chuyên trách bị chấm dứt hợp đồng hoặc sa thải trái pháp luật?",
      "quyen_loi_khac",
      ["50_2024_QH15__D28__K3"])

add_q("v3_07_10",
      "Quyền của người sử dụng lao động là gì?",
      "quyen_loi_khac",
      ["45_2019_QH14__D6__K1"])

add_q("v3_07_11",
      "Ngoài thời gian nghỉ theo quy định, người lao động có được nghỉ giải lao thêm trong giờ làm việc không?",
      "quyen_loi_khac",
      ["45_2019_QH14__D109__K2"])

add_q("v3_07_12",
      "Người lao động có được tham gia đối thoại tại nơi làm việc không?",
      "quyen_loi_khac",
      ["45_2019_QH14__D63__K1"])

# =============================================================================
# 8. NGOÀI PHẠM VI 
# =============================================================================

# 8.1 Luật khác 
add_q("v3_oos_01",
      "Điều kiện để được cấp hộ chiếu phổ thông tại Việt Nam là gì?",
      "out_of_scope", [])

add_q("v3_oos_02",
      "Người dân muốn đăng ký thường trú tại một địa phương cần những điều kiện gì?",
      "out_of_scope", [])

add_q("v3_oos_03",
      "Hành vi lấn chiếm lòng lề đường, vỉa hè để kinh doanh bị xử phạt hành chính thế nào?",
      "out_of_scope", [])

add_q("v3_oos_04",
      "Người điều khiển xe máy đi vào đường cao tốc bị tước bằng lái xe bao lâu?",
      "out_of_scope", [])

add_q("v3_oos_05",
      "Thủ tục đăng ký khai sinh cho trẻ em cần những giấy tờ nào?",
      "out_of_scope", [])

add_q("v3_oos_06",
      "Hành vi cá độ bóng đá qua mạng có thể bị truy cứu trách nhiệm hình sự ở khung hình phạt nào?",
      "out_of_scope", [])

add_q("v3_oos_07",
      "Hồ sơ xin cấp giấy phép thành lập trường mầm non tư thục gồm những gì?",
      "out_of_scope", [])

# 8.2 Tư vấn cá nhân 
add_q("v3_oos_08",
      "Khối lượng công việc tại phòng ban quá tải, tôi nên đề xuất phương án tuyển thêm người với trưởng phòng ra sao?",
      "out_of_scope", [])

add_q("v3_oos_09",
      "Tôi chuẩn bị bước vào vòng phỏng vấn với giám đốc điều hành, bạn có mẹo nào giúp tôi tự tin hơn không?",
      "out_of_scope", [])

add_q("v3_oos_10",
      "Tôi cảm thấy áp lực vì công việc, bạn có thể tư vấn cho tôi cách cân bằng cuộc sống không?",
      "out_of_scope", [])

add_q("v3_oos_11",
      "Đồng nghiệp trong nhóm thường xuyên chậm tiến độ bàn giao việc, tôi nên xử lý tình huống này thế nào?",
      "out_of_scope", [])

add_q("v3_oos_12",
      "Tôi muốn học thêm chứng chỉ quản lý dự án để thăng tiến, bạn có lời khuyên gì không?",
      "out_of_scope", [])

add_q("v3_oos_13",
      "Tôi vừa nhận được lời mời làm việc mới, bạn có thể giúp tôi cân nhắc ưu nhược điểm không?",
      "out_of_scope", [])

# 8.3 Vô nghĩa / Chat 
add_q("v3_oos_14",
      "Bạn hôm nay có khỏe không?",
      "out_of_scope", [])

add_q("v3_oos_15",
      "Loài cá voi sát thủ có phải là loài cá heo không?",
      "out_of_scope", [])

add_q("v3_oos_16",
      "qwerty 9876 asdfgh",
      "out_of_scope", [])

add_q("v3_oos_17",
      "Hãy tóm tắt ngắn gọn nội dung và ý nghĩa của tác phẩm văn học Lão Hạc.",
      "out_of_scope", [])

add_q("v3_oos_18",
      "Bạn thích uống cà phê hay trà?",
      "out_of_scope", [])

add_q("v3_oos_19",
      "What is your favorite movie?",
      "out_of_scope", [])

# 8.4 Cận biên giới 
add_q("v3_oos_20",
      "Khoản tiền thưởng Tết Nguyên đán của nhân viên có phải tính vào thu nhập chịu thuế TNCN không?",
      "out_of_scope", [])

add_q("v3_oos_21",
      "Nhân viên công ty tư nhân nghỉ việc thì có phải làm thủ tục chốt thuế thu nhập cá nhân không?",
      "out_of_scope", [])

add_q("v3_oos_22",
      "Người lao động bị tai nạn giao thông trên đường về nhà thì quỹ BHYT hay quỹ tai nạn lao động chi trả?",
      "out_of_scope", [])

add_q("v3_oos_23",
      "Thủ tục xin cấp thẻ tạm trú cho chuyên gia nước ngoài sang làm việc tại Việt Nam gồm hồ sơ gì?",
      "out_of_scope", [])

add_q("v3_oos_24",
      "Làm việc theo chế độ hợp đồng trong doanh nghiệp nhà nước thì có được phong ngạch viên chức không?",
      "out_of_scope", [])

add_q("v3_oos_25",
      "Thẻ bảo hiểm y tế hộ gia đình có thể dùng chung giữa các thành viên trong sổ hộ khẩu không?",
      "out_of_scope", [])

# 8.5 BHXH / Văn bản pháp luật cũ, hết hiệu lực 
add_q("v3_oos_26",
      "Lao động nữ mang thai hộ được hưởng chế độ thai sản như thế nào theo Luật BHXH 2014 trước đây?",
      "out_of_scope", [])

add_q("v3_oos_27",
      "Chính sách tham gia bảo hiểm xã hội tự nguyện theo Luật BHXH 2014 bao gồm những chế độ nào?",
      "out_of_scope", [])

add_q("v3_oos_28",
      "Trước ngày 01/7/2025, người lao động bị suy giảm khả năng lao động từ bao nhiêu % thì đủ điều kiện nghỉ hưu sớm?",
      "out_of_scope", [])

add_q("v3_oos_29",
      "Thời gian nghỉ việc khi thực hiện biện pháp triệt sản theo quy định BHXH năm 2014 là bao nhiêu ngày?",
      "out_of_scope", [])

add_q("v3_oos_30",
      "Mắc bệnh thuộc danh mục chữa trị dài ngày thì thời gian nghỉ hưởng chế độ ốm đau theo Luật 2014 tối đa là bao lâu?",
      "out_of_scope", [])

add_q("v3_oos_31",
      "Hồ sơ đề nghị hưởng chế độ tử tuất theo quy định bảo hiểm xã hội cũ gồm các loại giấy tờ bắt buộc nào?",
      "out_of_scope", [])

add_q("v3_oos_32",
      "Trường hợp người lao động vừa đủ điều kiện lương hưu vừa đủ điều kiện BHXH một lần theo luật cũ xử lý ra sao?",
      "out_of_scope", [])

add_q("v3_oos_33",
      "Trợ cấp khu vực một lần khi thanh toán chế độ hưu trí theo quy định bảo hiểm xã hội trước đây được tính thế nào?",
      "out_of_scope", [])

# 8.6 Luật dân sự / Luật gần miền 
add_q("v3_oos_34",
      "Quy định về tiền đặt cọc và mức bồi thường khi một bên hủy hợp đồng đặt cọc theo Bộ luật Dân sự là gì?",
      "out_of_scope", [])

add_q("v3_oos_35",
      "Nghĩa vụ của bên vay tài sản không có lãi được Bộ luật Dân sự quy định cụ thể ra sao?",
      "out_of_scope", [])

add_q("v3_oos_36",
      "Khi sức khỏe bị người khác xâm phạm thì mức bồi thường tổn thất về tinh thần được pháp luật dân sự giới hạn tối đa bao nhiêu?",
      "out_of_scope", [])

add_q("v3_oos_37",
      "Hợp đồng ủy quyền chấm dứt hiệu lực trong những trường hợp cụ thể nào theo Bộ luật Dân sự?",
      "out_of_scope", [])

add_q("v3_oos_38",
      "Giao dịch dân sự do người chưa đủ 15 tuổi thực hiện có bắt buộc phải được người đại diện đồng ý không?",
      "out_of_scope", [])

add_q("v3_oos_39",
      "Một người mất năng lực hành vi dân sự thì ai là người đại diện theo pháp luật?",
      "out_of_scope", [])

add_q("v3_oos_40",
      "Di chúc của người bị hạn chế về thể chất hoặc người không biết chữ cần đáp ứng điều kiện gì để được xem là hợp pháp?",
      "out_of_scope", [])

add_q("v3_oos_41",
      "Người lập di chúc có quyền sửa đổi hoặc hủy bỏ di chúc đã lập không?",
      "out_of_scope", [])

add_q("v3_oos_42",
      "Khi ly hôn, nguyên tắc chia tài sản chung của vợ chồng gắn liền với quyền sử dụng đất được giải quyết thế nào?",
      "out_of_scope", [])

add_q("v3_oos_43",
      "Thời hạn thực hiện nghĩa vụ trả tiền trong hợp đồng dân sự được xác định như thế nào?",
      "out_of_scope", [])

add_q("v3_oos_44",
      "Bên mua nhà không thanh toán đúng hạn theo hợp đồng thì có thể phải chịu trách nhiệm gì?",
      "out_of_scope", [])

add_q("v3_oos_45",
      "Hậu quả pháp lý khi một giao dịch dân sự bị Tòa án tuyên vô hiệu do bị lừa dối hoặc đe dọa là gì?",
      "out_of_scope", [])

add_q("v3_oos_46",
      "Người chiếm hữu tài sản không có căn cứ pháp luật có phải hoàn trả tài sản cho chủ sở hữu không?",
      "out_of_scope", [])

add_q("v3_oos_47",
      "Theo pháp luật dân sự, người thừa kế có được thỏa thuận phân chia di sản khác với nội dung di chúc không?",
      "out_of_scope", [])

add_q("v3_oos_48",
      "Hợp đồng mua bán tài sản bị vô hiệu thì số tiền đã thanh toán được xử lý như thế nào?",
      "out_of_scope", [])

add_q("v3_oos_49",
      "Thời hiệu yêu cầu người thừa kế thực hiện nghĩa vụ về tài sản do người chết để lại được quy định là mấy năm?",
      "out_of_scope", [])

add_q("v3_oos_50",
      "Người gây thiệt hại cho người khác trong tình trạng mất khả năng nhận thức có phải bồi thường không?",
      "out_of_scope", [])
      
# =============================================================================
# XUẤT FILE & KIỂM TRA TÍNH TOÀN VẸN
# =============================================================================

output_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'eval')
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, 'test_set_v3.json')
sha256_path = os.path.join(output_dir, 'test_set_v3.sha256')

# Ghi file JSON với mã hóa UTF-8 chuẩn xác
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(questions, f, ensure_ascii=False, indent=2)

# Tính toán mã băm SHA-256 để đóng băng bộ dữ liệu
with open(output_path, 'rb') as f:
    content_bytes = f.read()
    test_v3_hash = hashlib.sha256(content_bytes).hexdigest()

with open(sha256_path, 'w', encoding='utf-8') as f:
    f.write(f"{test_v3_hash}  test_set_v3.json\n")

in_scope = [q for q in questions if q["category"] != "out_of_scope"]
out_scope = [q for q in questions if q["category"] == "out_of_scope"]
cats = Counter(q["category"] for q in questions)

filled_questions = [q for q in questions if q["question"].strip()]
filled_golds = [q for q in in_scope if len(q["gold_provision_ids"]) > 0]

print("=" * 75)
print(f"Khởi tạo thành công Test Set V3: {len(questions)} câu hỏi")
print(f"  - Trong phạm vi (In-scope): {len(in_scope)} câu")
print(f"  - Ngoài phạm vi (Out-of-scope): {len(out_scope)} câu")
print("-" * 75)
print("Phân bố danh mục:")
for cat, cnt in sorted(cats.items()):
    print(f"  * {cat:20s}: {cnt} câu")
print("-" * 75)
print(f"Tiến độ điền dữ liệu:")
print(f"  - Số câu đã có nội dung câu hỏi : {len(filled_questions)}/{len(questions)}")
print(f"  - Số câu in-scope đã có nhãn gold: {len(filled_golds)}/{len(in_scope)}")
print(f"Đã lưu file dữ liệu: {output_path}")
print(f"Mã băm SHA-256     : {test_v3_hash}")
print(f"Đã lưu mã băm tại  : {sha256_path}")
print("=" * 75)

# =============================================================================
# KIỂM ĐỊNH RÒ RỈ DỮ LIỆU VỚI DEV SET V2 VÀ TEST SET V2
# =============================================================================

dev_path = os.path.join(output_dir, 'dev_set_v2.json')
test_v2_path = os.path.join(output_dir, 'test_set_v2.json')

dev_data = []
if os.path.exists(dev_path):
    with open(dev_path, 'r', encoding='utf-8') as f:
        dev_data = json.load(f)

test_v2_data = []
if os.path.exists(test_v2_path):
    with open(test_v2_path, 'r', encoding='utf-8') as f:
        test_v2_data = json.load(f)

# 1. Kiểm tra trùng text câu hỏi
dev_q_set = set(q["question"].strip() for q in dev_data if q["question"].strip())
v2_q_set = set(q["question"].strip() for q in test_v2_data if q["question"].strip())
current_q_set = set(q["question"].strip() for q in filled_questions)

q_leak_dev = current_q_set & dev_q_set
q_leak_v2 = current_q_set & v2_q_set

# 2. Kiểm tra trùng mã gold provision với Dev Set
dev_golds = set()
for q in dev_data:
    for g in q.get("gold_provision_ids", []):
        dev_golds.add(g)

current_golds = set()
for q in filled_questions:
    for g in q.get("gold_provision_ids", []):
        current_golds.add(g)

gold_leak = current_golds & dev_golds

print("\nKẾT QUẢ KIỂM TRA RÒ RỈ DỮ LIỆU (LEAKAGE AUDIT):")
if q_leak_dev:
    print(f"  [CẢNH BÁO NGUY HIỂM] Phát hiện {len(q_leak_dev)} câu hỏi trùng chữ với dev_set_v2:")
    for q_text in q_leak_dev:
        print(f"    - {q_text}")
else:
    print("  [OK] Không có câu hỏi nào trùng chữ với dev_set_v2.")

if gold_leak:
    print(f"  [CẢNH BÁO NGUY HIỂM] Phát hiện {len(gold_leak)} mã gold trùng lặp với dev_set_v2:")
    for g_id in sorted(gold_leak):
        print(f"    - {g_id}")
else:
    print("  [OK] Không có mã gold nào trùng lặp với dev_set_v2.")
