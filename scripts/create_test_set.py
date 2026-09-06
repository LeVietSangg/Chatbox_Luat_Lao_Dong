import json
import os

# 7 nhóm chủ đề chính (trong phạm vi)
# 1. Hợp đồng lao động
# 2. Tiền lương
# 3. Làm thêm giờ
# 4. Nghỉ phép
# 5. Chấm dứt hợp đồng
# 6. Bảo hiểm
# 7. Các quyền lợi cơ bản khác
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

# --- 1. Hợp đồng lao động (13 câu) ---
add_q("t1_01", "Thời gian thử việc tối đa đối với lao động phổ thông là bao nhiêu ngày?", "hop_dong_lao_dong", ["45_2019_QH14__D25__K4"])
add_q("t1_02", "Tiền lương trong thời gian thử việc được quy định như thế nào?", "hop_dong_lao_dong", ["45_2019_QH14__D26"])
add_q("t1_03", "Hợp đồng lao động phải bao gồm những nội dung gì?", "hop_dong_lao_dong", ["45_2019_QH14__D21__K1"])
add_q("t1_04", "Hợp đồng lao động được giao kết bằng hình thức nào?", "hop_dong_lao_dong", ["45_2019_QH14__D14__K1"])
add_q("t1_05", "Khi kết thúc thử việc, nếu đạt yêu cầu thì xử lý thế nào?", "hop_dong_lao_dong", ["45_2019_QH14__D27__K1"])
add_q("t1_06", "Có mấy loại hợp đồng lao động hiện nay?", "hop_dong_lao_dong", ["45_2019_QH14__D20__K1"])
add_q("t1_07", "Tạm hoãn thực hiện hợp đồng lao động trong trường hợp nào?", "hop_dong_lao_dong", ["45_2019_QH14__D30__K1"])
add_q("t1_08", "Hợp đồng lao động vô hiệu khi nào?", "hop_dong_lao_dong", ["45_2019_QH14__D49__K1"], ["45_2019_QH14__D49__K2"])
add_q("t1_09", "Quyền của người lao động khi hợp đồng lao động vô hiệu?", "hop_dong_lao_dong", ["45_2019_QH14__D51__K1"])
add_q("t1_10", "Chuyển người lao động làm công việc khác so với hợp đồng lao động được không?", "hop_dong_lao_dong", ["45_2019_QH14__D29__K1"])
add_q("t1_11", "Phụ lục hợp đồng lao động có được sửa đổi thời hạn hợp đồng không?", "hop_dong_lao_dong", ["45_2019_QH14__D22__K2"])
add_q("t1_12", "Người lao động có được giao kết nhiều hợp đồng lao động với nhiều công ty không?", "hop_dong_lao_dong", ["45_2019_QH14__D19__K1"])
add_q("t1_13", "Hợp đồng lao động bằng miệng có giá trị pháp lý không?", "hop_dong_lao_dong", ["45_2019_QH14__D14__K2"], ["45_2019_QH14__D18__K2", "45_2019_QH14__D145__K1", "45_2019_QH14__D162__K1"])

# --- 2. Tiền lương (14 câu) ---
add_q("t2_01", "Mức lương tối thiểu vùng hiện nay là bao nhiêu?", "tien_luong", ["293_2025_NDCP__D3__K1"])
add_q("t2_02", "Hình thức trả lương cho người lao động gồm những gì?", "tien_luong", ["45_2019_QH14__D96__K1"], ["45_2019_QH14__D96__K2", "45_2019_QH14__D96__K3"])
add_q("t2_03", "Kỳ hạn trả lương theo giờ được quy định ra sao?", "tien_luong", ["45_2019_QH14__D97__K1"])
add_q("t2_04", "Nguyên tắc trả lương cho người lao động là gì?", "tien_luong", ["45_2019_QH14__D94__K1"])
add_q("t2_05", "Công ty có được khấu trừ lương của người lao động không?", "tien_luong", ["45_2019_QH14__D102__K1"])
add_q("t2_06", "Tiền thưởng cho người lao động dựa trên tiêu chí nào?", "tien_luong", ["45_2019_QH14__D104__K1"])
add_q("t2_07", "Người lao động có được tạm ứng tiền lương không?", "tien_luong", ["45_2019_QH14__D101__K1"])
add_q("t2_08", "Tiền lương ngừng việc do lỗi của người sử dụng lao động trả bao nhiêu?", "tien_luong", ["45_2019_QH14__D99__K1"])
add_q("t2_09", "Chế độ phụ cấp, trợ cấp được ghi ở đâu?", "tien_luong", ["45_2019_QH14__D103__K1"])
add_q("t2_10", "Tiền lương khi làm việc vào ban đêm tính như thế nào?", "tien_luong", ["45_2019_QH14__D98__K2"])
add_q("t2_11", "Trường hợp trả lương qua thẻ ngân hàng thì ai chịu phí mở thẻ?", "tien_luong", ["45_2019_QH14__D96__K2"])
add_q("t2_12", "Tiền lương ngừng việc do sự cố điện nước tính thế nào?", "tien_luong", ["45_2019_QH14__D99__K3"])
add_q("t2_13", "Quy chế thưởng do ai quyết định?", "tien_luong", ["45_2019_QH14__D104__K2"])
add_q("t2_14", "Khi thay đổi hình thức trả lương công ty phải báo trước bao lâu?", "tien_luong", ["10_2012_QH13__D94__K1"]) # Placeholder

# --- 3. Làm thêm giờ (13 câu) ---
add_q("t3_01", "Tiền lương làm thêm giờ vào ngày nghỉ lễ được tính thế nào?", "lam_them_gio", ["45_2019_QH14__D98__K1"])
add_q("t3_02", "Làm thêm giờ tối đa trong một năm là bao nhiêu?", "lam_them_gio", ["45_2019_QH14__D107__K2"])
add_q("t3_03", "Làm thêm giờ tối đa trong một tháng là bao nhiêu giờ?", "lam_them_gio", ["45_2019_QH14__D107__K2"])
add_q("t3_04", "Công ty bắt tôi làm thêm giờ mà tôi không đồng ý thì có sao không?", "lam_them_gio", ["45_2019_QH14__D107__K2"])
add_q("t3_05", "Tiền lương làm thêm giờ vào ngày thường là bao nhiêu %?", "lam_them_gio", ["45_2019_QH14__D98__K1"])
add_q("t3_06", "Làm thêm giờ vào ngày nghỉ hằng tuần được trả lương bao nhiêu?", "lam_them_gio", ["45_2019_QH14__D98__K1"])
add_q("t3_07", "Người lao động làm thêm giờ ban đêm thì tiền lương tính như thế nào?", "lam_them_gio", ["45_2019_QH14__D98__K3"])
add_q("t3_08", "Phụ nữ mang thai tháng thứ 7 có được làm thêm giờ không?", "lam_them_gio", ["45_2019_QH14__D137__K1"])
add_q("t3_09", "Lao động chưa thành niên có được làm thêm giờ không?", "lam_them_gio", ["45_2019_QH14__D146__K2"])
add_q("t3_10", "Công ty huy động làm thêm giờ trong trường hợp khẩn cấp thiên tai thì có quyền từ chối không?", "lam_them_gio", ["45_2019_QH14__D108__K2"])
add_q("t3_11", "Khi tổ chức làm thêm giờ, người sử dụng lao động phải thông báo cho người lao động như thế nào?", "lam_them_gio", ["45_2019_QH14__D107__K4"], ["45_2019_QH14__D107__K3"])
add_q("t3_12", "Giờ làm thêm được giới hạn tối đa bao nhiêu phần trăm số giờ làm việc bình thường trong ngày?", "lam_them_gio", ["45_2019_QH14__D107__K2"])
add_q("t3_13", "Trường hợp đặc biệt nào được làm thêm đến 300 giờ một năm?", "lam_them_gio", ["45_2019_QH14__D107__K3"])

# --- 4. Nghỉ phép (14 câu) ---
add_q("t4_01", "Người lao động được nghỉ phép hằng năm bao nhiêu ngày?", "nghi_phep", ["45_2019_QH14__D113__K1"])
add_q("t4_02", "Người lao động được nghỉ lễ và Tết như thế nào?", "nghi_phep", ["45_2019_QH14__D112__K1"])
add_q("t4_03", "Nghỉ việc riêng hưởng nguyên lương trong trường hợp nào?", "nghi_phep", ["45_2019_QH14__D115__K1"])
add_q("t4_04", "Nghỉ trong giờ làm việc được quy định thế nào?", "nghi_phep", ["45_2019_QH14__D109__K1"])
add_q("t4_05", "Cách tính ngày nghỉ phép hằng năm khi làm việc chưa đủ năm?", "nghi_phep", ["45_2019_QH14__D113__K2"])
add_q("t4_06", "Thời gian đi đường có được cộng vào ngày nghỉ phép không?", "nghi_phep", ["45_2019_QH14__D113__K6"])
add_q("t4_07", "Có được gộp ngày nghỉ phép của nhiều năm không?", "nghi_phep", ["45_2019_QH14__D113__K4"])
add_q("t4_08", "Nghỉ hằng tuần tối thiểu bao nhiêu giờ?", "nghi_phep", ["45_2019_QH14__D111__K1"])
add_q("t4_09", "Nếu ngày nghỉ lễ trùng ngày nghỉ hằng tuần thì sao?", "nghi_phep", ["45_2019_QH14__D111__K3"])
add_q("t4_10", "Nghỉ việc riêng không hưởng lương thì phải báo trước mấy ngày?", "nghi_phep", ["45_2019_QH14__D115__K2"])
add_q("t4_11", "Làm việc lâu năm có được tăng ngày nghỉ phép không?", "nghi_phep", ["45_2019_QH14__D114"])
add_q("t4_12", "Chưa nghỉ hết phép năm thì có được thanh toán tiền không?", "nghi_phep", ["45_2019_QH14__D113__K3"])
add_q("t4_13", "Lao động nữ trong thời gian hành kinh được nghỉ bao lâu?", "nghi_phep", ["45_2019_QH14__D137__K4"])
add_q("t4_14", "Nghỉ tết Âm lịch do ai quyết định cụ thể?", "nghi_phep", ["45_2019_QH14__D112__K3"])

# --- 5. Chấm dứt hợp đồng (14 câu) ---
add_q("t5_01", "Người sử dụng lao động có quyền đơn phương chấm dứt hợp đồng lao động trong trường hợp nào?", "cham_dut_hop_dong", ["45_2019_QH14__D36__K1"])
add_q("t5_02", "Người lao động được đơn phương chấm dứt hợp đồng lao động không cần báo trước khi nào?", "cham_dut_hop_dong", ["45_2019_QH14__D35__K2"])
add_q("t5_03", "Người lao động bị bệnh nghỉ thì có bị chấm dứt hợp đông lao động không?", "cham_dut_hop_dong", ["45_2019_QH14__D37__K1"])
add_q("t5_04", "Thời hạn báo trước khi người lao động đơn phương chấm dứt hợp đồng không xác định thời hạn là bao lâu?", "cham_dut_hop_dong", ["45_2019_QH14__D35__K1"])
add_q("t5_05", "Người lao động nghỉ việc có được hưởng trợ cấp thôi việc không?", "cham_dut_hop_dong", ["45_2019_QH14__D46__K1"])
add_q("t5_06", "Thời gian làm việc để tính trợ cấp thôi việc được xác định ra sao?", "cham_dut_hop_dong", ["45_2019_QH14__D46__K2"])
add_q("t5_07", "Trợ cấp mất việc làm được trả như thế nào?", "cham_dut_hop_dong", ["45_2019_QH14__D47__K1"])
add_q("t5_08", "Hình thức kỷ luật sa thải được áp dụng trong trường hợp nào?", "cham_dut_hop_dong", ["45_2019_QH14__D125__K1"])
add_q("t5_09", "Lao động nữ mang thai có được đơn phương chấm dứt hợp đồng không?", "cham_dut_hop_dong", ["45_2019_QH14__D138__K1"])
add_q("t5_10", "Khi nào thì bị sa thải do tự ý bỏ việc?", "cham_dut_hop_dong", ["45_2019_QH14__D125__K4"])
add_q("t5_11", "Khi chấm dứt hợp đồng lao động, công ty phải thanh toán các khoản tiền trong thời gian bao lâu?", "cham_dut_hop_dong", ["45_2019_QH14__D48__K1"])
add_q("t5_12", "Công ty có trách nhiệm trả lại sổ bảo hiểm xã hội khi nhân viên nghỉ việc không?", "cham_dut_hop_dong", ["45_2019_QH14__D48__K3"])
add_q("t5_13", "Nếu đơn phương chấm dứt hợp đồng trái pháp luật, người lao động phải bồi thường gì?", "cham_dut_hop_dong", ["45_2019_QH14__D40__K2"])
add_q("t5_14", "Người lao động bị kết án phạt tù thì hợp đồng lao động có chấm dứt không?", "cham_dut_hop_dong", ["45_2019_QH14__D34__K4"])

# --- 6. Bảo hiểm (13 câu) ---
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

# --- 7. Các quyền lợi cơ bản khác (14 câu) ---
add_q("t7_01", "Người sử dụng lao động có trách nhiệm gì trong việc bảo đảm an toàn tại nơi làm việc?", "quyen_loi_khac", ["84_2015_QH13__D16__K1"])
add_q("t7_02", "Khi xảy ra tai nạn lao động, người sử dụng lao động phải làm gì?", "quyen_loi_khac", ["84_2015_QH13__D38__K1"])
add_q("t7_03", "Trách nhiệm đóng chi phí khám tai nạn lao động thuộc về ai?", "quyen_loi_khac", ["84_2015_QH13__D38__K2"])
add_q("t7_04", "Người lao động được trang bị bảo hộ lao động khi nào?", "quyen_loi_khac", ["84_2015_QH13__D16__K3"])
add_q("t7_05", "Người lao động bị bệnh nghề nghiệp được hưởng chế độ gì?", "quyen_loi_khac", ["84_2015_QH13__D38__K3"])
add_q("t7_06", "Người lao động có quyền từ chối làm việc khi có nguy cơ rõ ràng đe dọa nghiêm trọng tính mạng, sức khỏe không?", "quyen_loi_khac", ["84_2015_QH13__D6__K1"])
add_q("t7_07", "Người sử dụng lao động có được phạt tiền người lao động thay cho xử lý kỷ luật không?", "quyen_loi_khac", ["45_2019_QH14__D127__K2"])
add_q("t7_08", "Xóa kỷ luật lao động sau bao lâu?", "quyen_loi_khac", ["45_2019_QH14__D126__K1"])
add_q("t7_09", "Người lao động làm hư hỏng dụng cụ phải bồi thường bao nhiêu?", "quyen_loi_khac", ["45_2019_QH14__D129__K1"])
add_q("t7_10", "Đoàn viên công đoàn có được hỗ trợ pháp lý miễn phí không?", "quyen_loi_khac", ["50_2024_QH15__D21__K6"])
add_q("t7_11", "Công đoàn có quyền đại diện cho tập thể người lao động thương lượng tập thể không?", "quyen_loi_khac", ["50_2024_QH15__D11__K2"])
add_q("t7_12", "Độ tuổi lao động tối thiểu là bao nhiêu?", "quyen_loi_khac", ["45_2019_QH14__D3__K1"])
add_q("t7_13", "Việc thu thập dữ liệu cá nhân có cần đồng ý không?", "quyen_loi_khac", ["91_2025_QH15__D11__K1"])
add_q("t7_14", "Quyền của chủ thể dữ liệu đối với dữ liệu của mình?", "quyen_loi_khac", ["91_2025_QH15__D3__K3"])

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
add_q("t8_20", "Tiền lương làm thêm giờ có phải đóng thuế thu nhập cá nhân không?", "out_of_scope", [])
add_q("t8_21", "Giáo viên trường công lập xin thôi việc thì thủ tục như thế nào?", "out_of_scope", [])
add_q("t8_22", "Công ty bị phạt 50 triệu do vi phạm an toàn lao động thì nộp phạt vào kho bạc nào?", "out_of_scope", [])
add_q("t8_23", "Khi đi khám bệnh, tôi được bảo hiểm y tế chi trả bao nhiêu phần trăm tiền thuốc?", "out_of_scope", [])
add_q("t8_24", "Giám đốc công ty TNHH MTV có được ký hợp đồng lao động với chính mình không?", "out_of_scope", [])
add_q("t8_25", "Người lao động nghỉ hưu có phải nộp thuế thu nhập cá nhân đối với lương hưu không?", "out_of_scope", [])

output_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'eval', 'test_set_v1.json')
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(questions, f, ensure_ascii=False, indent=2)

print(f"Created {len(questions)} test questions at {output_path}")
