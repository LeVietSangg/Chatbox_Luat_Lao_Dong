import json
import os

# 7 nhóm chủ đề chính (trong phạm vi)
# 1. Hợp đồng lao động & Thử việc
# 2. Tiền lương & Trợ cấp
# 3. Thời giờ làm việc & Thời giờ nghỉ ngơi
# 4. Kỷ luật lao động & Trách nhiệm vật chất
# 5. An toàn, vệ sinh lao động & Bảo vệ dữ liệu cá nhân
# 6. Bảo hiểm xã hội & Thai sản
# 7. Đối tượng đặc biệt & Công đoàn
# + Nhóm ngoài phạm vi

questions = []

def add_q(q_id, text, cat, gold, gold_relaxed=None):
    if not gold_relaxed:
        gold_relaxed = gold
    questions.append({
        "id": q_id,
        "question": text,
        "category": cat,
        "gold_provision_ids": gold,
        "gold_provision_ids_relaxed": gold_relaxed
    })

# --- 1. Hợp đồng lao động & Thử việc (14 câu) ---
add_q("t1_01", "Thời gian thử việc tối đa đối với lao động phổ thông là bao nhiêu ngày?", "hop_dong", ["45_2019_QH14__D25__K4"], ["45_2019_QH14__D25__K4", "45_2019_QH14__D25__K3", "45_2019_QH14__D25__K2", "45_2019_QH14__D25__K1"])
add_q("t1_02", "Tiền lương trong thời gian thử việc được quy định như thế nào?", "hop_dong", ["45_2019_QH14__D26"])
add_q("t1_03", "Người sử dụng lao động có quyền đơn phương chấm dứt hợp đồng lao động trong trường hợp nào?", "hop_dong", ["45_2019_QH14__D36__K1"])
add_q("t1_04", "Người lao động được đơn phương chấm dứt hợp đồng lao động không cần báo trước khi nào?", "hop_dong", ["45_2019_QH14__D35__K2"])
add_q("t1_05", "Trường hợp nào người sử dụng lao động không được đơn phương chấm dứt hợp đồng?", "hop_dong", ["45_2019_QH14__D37__K1"])
add_q("t1_06", "Hợp đồng lao động phải bao gồm những nội dung gì?", "hop_dong", ["45_2019_QH14__D21__K1"])
add_q("t1_07", "Hợp đồng lao động được giao kết bằng hình thức nào?", "hop_dong", ["45_2019_QH14__D14__K1"])
add_q("t1_08", "Khi kết thúc thử việc, nếu đạt yêu cầu thì xử lý thế nào?", "hop_dong", ["45_2019_QH14__D27__K1"])
add_q("t1_09", "Có mấy loại hợp đồng lao động hiện nay?", "hop_dong", ["45_2019_QH14__D20__K1"])
add_q("t1_10", "Thời hạn báo trước khi người lao động đơn phương chấm dứt hợp đồng không xác định thời hạn là bao lâu?", "hop_dong", ["45_2019_QH14__D35__K1"])
add_q("t1_11", "Tạm hoãn thực hiện hợp đồng lao động trong trường hợp nào?", "hop_dong", ["45_2019_QH14__D30__K1"])
add_q("t1_12", "Hợp đồng lao động vô hiệu khi nào?", "hop_dong", ["45_2019_QH14__D49__K1"])
add_q("t1_13", "Quyền của người lao động khi hợp đồng lao động vô hiệu?", "hop_dong", ["45_2019_QH14__D51__K1"])
add_q("t1_14", "Chuyển người lao động làm công việc khác so với hợp đồng lao động được không?", "hop_dong", ["45_2019_QH14__D29__K1"])

# --- 2. Tiền lương & Trợ cấp (14 câu) ---
add_q("t2_01", "Mức lương tối thiểu vùng hiện nay là bao nhiêu?", "tien_luong", ["293_2025_NDCP__D3__K1"])
add_q("t2_02", "Người lao động nghỉ việc có được hưởng trợ cấp thôi việc không?", "tien_luong", ["45_2019_QH14__D46__K1"])
add_q("t2_03", "Thời gian làm việc để tính trợ cấp thôi việc được xác định ra sao?", "tien_luong", ["45_2019_QH14__D46__K2"])
add_q("t2_04", "Trợ cấp mất việc làm được trả như thế nào?", "tien_luong", ["45_2019_QH14__D47__K1"])
add_q("t2_05", "Tiền lương làm thêm giờ vào ngày nghỉ lễ được tính thế nào?", "tien_luong", ["45_2019_QH14__D98__K1"])
add_q("t2_06", "Hình thức trả lương cho người lao động gồm những gì?", "tien_luong", ["45_2019_QH14__D96__K1"])
add_q("t2_07", "Kỳ hạn trả lương được quy định ra sao?", "tien_luong", ["45_2019_QH14__D97__K1"])
add_q("t2_08", "Nguyên tắc trả lương cho người lao động là gì?", "tien_luong", ["45_2019_QH14__D94__K1"])
add_q("t2_09", "Công ty có được khấu trừ lương của người lao động không?", "tien_luong", ["45_2019_QH14__D102__K1"])
add_q("t2_10", "Tiền thưởng cho người lao động dựa trên tiêu chí nào?", "tien_luong", ["45_2019_QH14__D104__K1"])
add_q("t2_11", "Tạm ứng tiền lương được quy định như thế nào?", "tien_luong", ["45_2019_QH14__D101__K1"])
add_q("t2_12", "Tiền lương ngừng việc do lỗi của người sử dụng lao động trả bao nhiêu?", "tien_luong", ["45_2019_QH14__D99__K1"])
add_q("t2_13", "Chế độ phụ cấp, trợ cấp được ghi ở đâu?", "tien_luong", ["45_2019_QH14__D103__K1"])
add_q("t2_14", "Tiền lương khi làm việc vào ban đêm tính như thế nào?", "tien_luong", ["45_2019_QH14__D98__K2"])

# --- 3. Thời giờ làm việc & Thời giờ nghỉ ngơi (14 câu) ---
add_q("t3_01", "Thời giờ làm việc bình thường là bao nhiêu tiếng một ngày?", "thoi_gio", ["45_2019_QH14__D105__K1"])
add_q("t3_02", "Người lao động được nghỉ phép hằng năm bao nhiêu ngày?", "thoi_gio", ["45_2019_QH14__D113__K1"])
add_q("t3_03", "Làm thêm giờ tối đa trong một năm là bao nhiêu?", "thoi_gio", ["45_2019_QH14__D107__K2"])
add_q("t3_04", "Nghỉ lễ, tết người lao động được nghỉ những ngày nào?", "thoi_gio", ["45_2019_QH14__D112__K1"])
add_q("t3_05", "Nghỉ việc riêng hưởng nguyên lương trong trường hợp nào?", "thoi_gio", ["45_2019_QH14__D115__K1"])
add_q("t3_06", "Giờ làm việc ban đêm được tính từ mấy giờ đến mấy giờ?", "thoi_gio", ["45_2019_QH14__D106"])
add_q("t3_07", "Nghỉ trong giờ làm việc được quy định thế nào?", "thoi_gio", ["45_2019_QH14__D109__K1"])
add_q("t3_08", "Thời giờ làm thêm có giới hạn trong tháng không?", "thoi_gio", ["45_2019_QH14__D107__K2"])
add_q("t3_09", "Cách tính ngày nghỉ phép hằng năm khi làm việc chưa đủ năm?", "thoi_gio", ["45_2019_QH14__D113__K2"])
add_q("t3_10", "Thời gian đi đường có được cộng vào ngày nghỉ phép không?", "thoi_gio", ["45_2019_QH14__D113__K6"])
add_q("t3_11", "Có được gộp ngày nghỉ phép của nhiều năm không?", "thoi_gio", ["45_2019_QH14__D113__K4"])
add_q("t3_12", "Nghỉ hằng tuần tối thiểu bao nhiêu giờ?", "thoi_gio", ["45_2019_QH14__D111__K1"])
add_q("t3_13", "Nếu ngày nghỉ lễ trùng ngày nghỉ hằng tuần thì sao?", "thoi_gio", ["45_2019_QH14__D111__K3"])
add_q("t3_14", "Làm công việc nặng nhọc thì thời giờ làm việc là bao nhiêu?", "thoi_gio", ["45_2019_QH14__D105__K3"])

# --- 4. Kỷ luật lao động & Trách nhiệm vật chất (13 câu) ---
add_q("t4_01", "Các hình thức xử lý kỷ luật lao động gồm những gì?", "ky_luat", ["45_2019_QH14__D124__K1"])
add_q("t4_02", "Hình thức kỷ luật sa thải được áp dụng trong trường hợp nào?", "ky_luat", ["45_2019_QH14__D125__K1"])
add_q("t4_03", "Trình tự, thủ tục xử lý kỷ luật lao động?", "ky_luat", ["45_2019_QH14__D122__K1"])
add_q("t4_04", "Khi nào không được xử lý kỷ luật lao động?", "ky_luat", ["45_2019_QH14__D122__K4"])
add_q("t4_05", "Thời hiệu xử lý kỷ luật lao động là bao lâu?", "ky_luat", ["45_2019_QH14__D123__K1"])
add_q("t4_06", "Hành vi nào bị nghiêm cấm khi xử lý kỷ luật lao động?", "ky_luat", ["45_2019_QH14__D127__K1"])
add_q("t4_07", "Xóa kỷ luật lao động sau bao lâu?", "ky_luat", ["45_2019_QH14__D126__K1"])
add_q("t4_08", "Người lao động làm hư hỏng dụng cụ phải bồi thường bao nhiêu?", "ky_luat", ["45_2019_QH14__D129__K1"])
add_q("t4_09", "Nếu làm mất thiết bị thì bồi thường thế nào?", "ky_luat", ["45_2019_QH14__D129__K2"])
add_q("t4_10", "Xử lý bồi thường thiệt hại theo nguyên tắc nào?", "ky_luat", ["45_2019_QH14__D128__K1"])
add_q("t4_11", "Tạm đình chỉ công việc trong trường hợp nào?", "ky_luat", ["45_2019_QH14__D128__K1"]) # Placeholder, thuc ra la D128, dung tam K1
add_q("t4_12", "Trong thời gian đình chỉ công việc có được trả lương không?", "ky_luat", ["45_2019_QH14__D128__K2"])
add_q("t4_13", "Nếu làm hư hỏng do thiên tai thì có phải bồi thường không?", "ky_luat", ["45_2019_QH14__D129__K2"])

# --- 5. An toàn, vệ sinh lao động & Dữ liệu cá nhân (13 câu) ---
add_q("t5_01", "Người sử dụng lao động có trách nhiệm gì trong việc bảo đảm an toàn lao động?", "an_toan", ["84_2015_QH13__D16__K1"])
add_q("t5_02", "Khi xảy ra tai nạn lao động, công ty phải làm gì?", "an_toan", ["84_2015_QH13__D38__K1"])
add_q("t5_03", "Người lao động có quyền từ chối làm việc nếu thấy không an toàn không?", "an_toan", ["84_2015_QH13__D14__K1"])
add_q("t5_04", "Được trang bị bảo hộ lao động khi nào?", "an_toan", ["84_2015_QH13__D16__K3"])
add_q("t5_05", "Trách nhiệm đóng chi phí khám tai nạn lao động thuộc về ai?", "an_toan", ["84_2015_QH13__D38__K2"])
add_q("t5_06", "Người lao động bị bệnh nghề nghiệp được hưởng chế độ gì?", "an_toan", ["84_2015_QH13__D38__K3"])
add_q("t5_07", "Huấn luyện an toàn lao động tổ chức khi nào?", "an_toan", ["84_2015_QH13__D14__K2"])
add_q("t5_08", "Nguyên tắc bảo vệ dữ liệu cá nhân là gì?", "du_lieu_ca_nhan", ["91_2025_QH15__D3__K1"])
add_q("t5_09", "Việc thu thập dữ liệu cá nhân có cần đồng ý không?", "du_lieu_ca_nhan", ["91_2025_QH15__D11__K1"])
add_q("t5_10", "Dữ liệu cá nhân nhạy cảm gồm những gì?", "du_lieu_ca_nhan", ["91_2025_QH15__D2__K3"])
add_q("t5_11", "Quyền của chủ thể dữ liệu đối với dữ liệu của mình?", "du_lieu_ca_nhan", ["91_2025_QH15__D3__K3"])
add_q("t5_12", "Cơ quan nào được phép xử lý dữ liệu cá nhân không cần đồng ý?", "du_lieu_ca_nhan", ["91_2025_QH15__D11__K2"])
add_q("t5_13", "Vi phạm bảo vệ dữ liệu cá nhân bị xử lý thế nào?", "du_lieu_ca_nhan", ["91_2025_QH15__D3__K5"])

# --- 6. Bảo hiểm xã hội & Thai sản (14 câu) ---
add_q("t6_01", "Đối tượng nào phải tham gia BHXH bắt buộc?", "bao_hiem", ["58_VBHN-VPQH__D2__K1"])
add_q("t6_02", "Điều kiện hưởng lương hưu hằng tháng là gì?", "bao_hiem", ["58_VBHN-VPQH__D54__K1"])
add_q("t6_03", "Doanh nghiệp phải đóng BHXH theo tỷ lệ bao nhiêu?", "bao_hiem", ["58_VBHN-VPQH__D86__K1"])
add_q("t6_04", "Lao động nữ nghỉ thai sản được bao nhiêu tháng?", "bao_hiem", ["45_2019_QH14__D139__K1"])
add_q("t6_05", "Điều kiện hưởng chế độ thai sản khi sinh con?", "bao_hiem", ["58_VBHN-VPQH__D31__K1"])
add_q("t6_06", "Mức hưởng chế độ thai sản là bao nhiêu?", "bao_hiem", ["58_VBHN-VPQH__D39__K1"])
add_q("t6_07", "Lao động nam có vợ sinh con được nghỉ thai sản mấy ngày?", "bao_hiem", ["58_VBHN-VPQH__D34__K2"])
add_q("t6_08", "Người lao động ốm đau được nghỉ bao nhiêu ngày một năm?", "bao_hiem", ["58_VBHN-VPQH__D26__K1"])
add_q("t6_09", "Mức hưởng chế độ ốm đau tính như thế nào?", "bao_hiem", ["58_VBHN-VPQH__D28__K1"])
add_q("t6_10", "Thời gian nghỉ dưỡng sức sau thai sản là bao lâu?", "bao_hiem", ["58_VBHN-VPQH__D41__K1"])
add_q("t6_11", "Rút BHXH một lần được thực hiện trong điều kiện nào?", "bao_hiem", ["58_VBHN-VPQH__D60__K1"])
add_q("t6_12", "Trợ cấp mai táng phí được bao nhiêu tháng lương cơ sở?", "bao_hiem", ["58_VBHN-VPQH__D85__K2"])
add_q("t6_13", "Mức bình quân tiền lương tháng đóng BHXH tính hưu trí ra sao?", "bao_hiem", ["58_VBHN-VPQH__D62__K1"])
add_q("t6_14", "Lao động nữ mang thai có được đơn phương chấm dứt hợp đồng không?", "bao_hiem", ["45_2019_QH14__D138__K1"])

# --- 7. Đối tượng đặc biệt & Công đoàn (13 câu) ---
add_q("t7_01", "Người khuyết tật có quyền lợi gì trong việc làm?", "dac_biet", ["51_2010_QH12__D33__K1"])
add_q("t7_02", "Doanh nghiệp có được từ chối tuyển dụng người khuyết tật không?", "dac_biet", ["51_2010_QH12__D33__K2"])
add_q("t7_03", "Điều kiện để người nước ngoài làm việc tại Việt Nam?", "dac_biet", ["45_2019_QH14__D151__K1"])
add_q("t7_04", "Giấy phép lao động cho người nước ngoài có thời hạn bao lâu?", "dac_biet", ["45_2019_QH14__D155"])
add_q("t7_05", "Độ tuổi lao động tối thiểu là bao nhiêu?", "dac_biet", ["45_2019_QH14__D3__K1"])
add_q("t7_06", "Sử dụng lao động dưới 15 tuổi có được không?", "dac_biet", ["45_2019_QH14__D143__K1"])
add_q("t7_07", "Công đoàn cơ sở được thành lập theo quy trình nào?", "dac_biet", ["50_2024_QH15__D13__K1"])
add_q("t7_08", "Kinh phí công đoàn doanh nghiệp phải đóng là bao nhiêu?", "dac_biet", ["50_2024_QH15__D29__K1_v2"])
add_q("t7_09", "Đoàn viên công đoàn có những quyền gì?", "dac_biet", ["50_2024_QH15__D21__K7"])
add_q("t7_10", "Thời gian làm việc của cán bộ công đoàn không chuyên trách?", "dac_biet", ["50_2024_QH15__D28__K2"])
add_q("t7_11", "Quyền đại diện của công đoàn trong doanh nghiệp?", "dac_biet", ["50_2024_QH15__D11__K8"])
add_q("t7_12", "Có được sa thải cán bộ công đoàn vì lý do hoạt động công đoàn không?", "dac_biet", ["45_2019_QH14__D137__K1"])
add_q("t7_13", "Cán bộ công đoàn được hưởng phụ cấp gì?", "dac_biet", ["50_2024_QH15__D31__K2"])

# --- 8. Ngoài phạm vi (25 câu) ---
# 8.1 Luật khác (7 câu)
add_q("t8_01", "Tội trộm cắp tài sản bị phạt tù mấy năm?", "out_of_scope", [])
add_q("t8_02", "Điều kiện tách thửa đất nông nghiệp là gì?", "out_of_scope", [])
add_q("t8_03", "Thủ tục ly hôn đơn phương cần những giấy tờ gì?", "out_of_scope", [])
add_q("t8_04", "Công ty chậm nộp thuế GTGT bị phạt bao nhiêu tiền?", "out_of_scope", [])
add_q("t8_05", "Vượt đèn đỏ đi xe máy phạt bao nhiêu?", "out_of_scope", [])
add_q("t8_06", "Cách đăng ký nhãn hiệu hàng hóa độc quyền?", "out_of_scope", [])
add_q("t8_07", "Điều kiện thành lập công ty cổ phần?", "out_of_scope", [])

# 8.2 Tư vấn cá nhân (6 câu)
add_q("t8_08", "Công ty ép tôi làm OT không trả tiền, tôi có nên kiện ra tòa án không?", "out_of_scope", [])
add_q("t8_09", "Sếp hay mắng chửi tôi thậm tệ, tôi muốn nghỉ việc ngay lập tức thì làm sao để lấy lại lương?", "out_of_scope", [])
add_q("t8_10", "Tôi bị sếp đuổi việc vô lý, hãy tính toán xem tôi được bồi thường chính xác bao nhiêu tiền nếu kiện?", "out_of_scope", [])
add_q("t8_11", "Tôi sắp sinh con, bạn tư vấn giúp tôi mua loại sữa nào tốt cho bé được không?", "out_of_scope", [])
add_q("t8_12", "Năm nay kinh tế khó khăn, theo bạn tôi có nên nghỉ việc để ra làm riêng kinh doanh không?", "out_of_scope", [])
add_q("t8_13", "Viết cho tôi một lá đơn xin nghỉ việc thật lâm li bi đát để sếp cảm động.", "out_of_scope", [])

# 8.3 Vô nghĩa/Conversational (6 câu)
add_q("t8_14", "Chào bạn, hôm nay thời tiết thế nào?", "out_of_scope", [])
add_q("t8_15", "Bạn là ai, do ai tạo ra?", "out_of_scope", [])
add_q("t8_16", "1 cộng 1 bằng mấy?", "out_of_scope", [])
add_q("t8_17", "Hãy làm một bài thơ về mùa thu Hà Nội.", "out_of_scope", [])
add_q("t8_18", "asdasdjaskljd aksd", "out_of_scope", [])
add_q("t8_19", "Hello, do you speak English?", "out_of_scope", [])

# 8.4 Cận biên giới (Khó - 6 câu)
# Liên quan thu nhập nhưng thuộc luật Thuế TNCN
add_q("t8_20", "Tiền lương làm thêm giờ có phải đóng thuế thu nhập cá nhân không?", "out_of_scope", [])
# Liên quan viên chức (Luật Viên chức, không áp dụng BLLĐ trực tiếp ở một số khía cạnh, nhưng rất sát)
add_q("t8_21", "Giáo viên trường công lập xin thôi việc thì thủ tục như thế nào?", "out_of_scope", [])
# Liên quan xử phạt hành chính doanh nghiệp (Cần NĐ 12 nhưng cụ thể quá)
add_q("t8_22", "Công ty bị phạt 50 triệu do vi phạm an toàn lao động thì nộp phạt vào kho bạc nào?", "out_of_scope", [])
# Liên quan bảo hiểm y tế (BHYT khác BHXH/BHTN)
add_q("t8_23", "Khi đi khám bệnh, tôi được bảo hiểm y tế chi trả bao nhiêu phần trăm tiền thuốc?", "out_of_scope", [])
# Tình huống cụ thể
add_q("t8_24", "Giám đốc công ty TNHH MTV có được ký hợp đồng lao động với chính mình không?", "out_of_scope", [])
add_q("t8_25", "Nghỉ hưu trước tuổi do suy giảm khả năng lao động 61% thì bị trừ bao nhiêu phần trăm lương hưu?", "out_of_scope", [])

import json
output_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'eval', 'test_set_v1.json')
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(questions, f, ensure_ascii=False, indent=2)

print(f"Created {len(questions)} test questions at {output_path}")
