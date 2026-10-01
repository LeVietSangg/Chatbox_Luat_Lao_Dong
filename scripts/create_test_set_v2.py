"""
create_test_set_v2.py
=====================
Tạo Test Set V2 (Held-out) – 120 câu hỏi mới hoàn toàn.
Cấu trúc giống test_set_v1.json:
  - 13 câu hop_dong_lao_dong
  - 14 câu tien_luong
  - 13 câu lam_them_gio
  - 14 câu nghi_phep
  - 14 câu cham_dut_hop_dong
  - 13 câu bao_hiem
  - 14 câu quyen_loi_khac
  - 25 câu out_of_scope (7 luật khác + 6 tư vấn cá nhân + 6 vô nghĩa + 6 cận biên)

KHÔNG trùng câu hỏi hay gold provision với test_set_v1 hoặc dev_set.
Phong cách: tình huống thực tế, khác v1 (hỏi trực tiếp điều khoản).
"""

import json
import os

questions = []

def add_q(q_id, text, cat, gold):
    questions.append({
        "id": q_id,
        "question": text,
        "category": cat,
        "gold_provision_ids": gold
    })

# =============================================================================
# 1. HỢP ĐỒNG LAO ĐỘNG (13 câu)
# =============================================================================

add_q("v2_01",
      "Người lao động có những quyền cơ bản nào theo Bộ luật Lao động?",
      "hop_dong_lao_dong",
      ["45_2019_QH14__D5__K1"])

add_q("v2_02",
      "Người sử dụng lao động có những quyền gì theo quy định?",
      "hop_dong_lao_dong",
      ["45_2019_QH14__D6__K1"])

add_q("v2_03",
      "Những hành vi nào bị nghiêm cấm trong lĩnh vực lao động?",
      "hop_dong_lao_dong",
      ["45_2019_QH14__D8__K1"])

add_q("v2_04",
      "Trước khi ký hợp đồng, người sử dụng lao động phải cung cấp thông tin gì cho người lao động?",
      "hop_dong_lao_dong",
      ["45_2019_QH14__D16__K1"])

add_q("v2_05",
      "Người lao động phải cung cấp thông tin gì cho công ty trước khi ký hợp đồng?",
      "hop_dong_lao_dong",
      ["45_2019_QH14__D16__K2"])

add_q("v2_06",
      "Thỏa thuận thử việc có thể được ghi trong hợp đồng lao động không?",
      "hop_dong_lao_dong",
      ["45_2019_QH14__D24__K1"])

add_q("v2_07",
      "Thời gian thử việc đối với công việc cần trình độ cao đẳng là bao lâu?",
      "hop_dong_lao_dong",
      ["45_2019_QH14__D25__K2"])

add_q("v2_08",
      "Trong thời gian thử việc, mỗi bên có quyền hủy bỏ thỏa thuận thử việc không?",
      "hop_dong_lao_dong",
      ["45_2019_QH14__D27__K2"])

add_q("v2_09",
      "Sau khi hết tạm hoãn hợp đồng, người lao động phải quay lại làm việc trong bao lâu?",
      "hop_dong_lao_dong",
      ["45_2019_QH14__D31"])

add_q("v2_10",
      "Muốn sửa đổi nội dung hợp đồng lao động thì phải làm thế nào?",
      "hop_dong_lao_dong",
      ["45_2019_QH14__D33__K1"])

add_q("v2_11",
      "Hợp đồng lao động chấm dứt khi hai bên thỏa thuận thì có cần báo trước không?",
      "hop_dong_lao_dong",
      ["45_2019_QH14__D34__K3"])

add_q("v2_12",
      "Người lao động bị tuyên bố mất tích thì hợp đồng lao động có chấm dứt không?",
      "hop_dong_lao_dong",
      ["45_2019_QH14__D34__K7"])

add_q("v2_13",
      "Muốn sử dụng lao động dưới 15 tuổi thì cần tuân thủ gì?",
      "hop_dong_lao_dong",
      ["45_2019_QH14__D145__K1"])

# =============================================================================
# 2. TIỀN LƯƠNG (14 câu)
# =============================================================================

add_q("v2_14",
      "Tiền lương là gì theo định nghĩa của Bộ luật Lao động?",
      "tien_luong",
      ["45_2019_QH14__D90__K1"])

add_q("v2_15",
      "Mức lương công theo công việc có được thấp hơn mức lương tối thiểu không?",
      "tien_luong",
      ["45_2019_QH14__D90__K2"])

add_q("v2_16",
      "Trả lương bình đẳng, không phân biệt giới tính được quy định ở đâu?",
      "tien_luong",
      ["45_2019_QH14__D90__K3"])

add_q("v2_17",
      "Mức lương tối thiểu theo vùng được xác định dựa trên căn cứ nào?",
      "tien_luong",
      ["45_2019_QH14__D91__K3"])

add_q("v2_18",
      "Người sử dụng lao động xây dựng bảng lương phải tham khảo ý kiến ai?",
      "tien_luong",
      ["45_2019_QH14__D93__K3"])

add_q("v2_19",
      "Người sử dụng lao động có được can thiệp vào quyền tự quyết chi tiêu lương của người lao động không?",
      "tien_luong",
      ["45_2019_QH14__D94__K2"])

add_q("v2_20",
      "Tiền lương ghi trong hợp đồng lao động phải ghi bằng đơn vị tiền tệ nào?",
      "tien_luong",
      ["45_2019_QH14__D95__K2"])

add_q("v2_21",
      "Mỗi lần trả lương, người sử dụng lao động có phải gửi bảng kê lương không?",
      "tien_luong",
      ["45_2019_QH14__D95__K3"])

add_q("v2_22",
      "Người lao động hưởng lương theo tháng thì kỳ hạn trả lương quy định thế nào?",
      "tien_luong",
      ["45_2019_QH14__D97__K2"])

add_q("v2_23",
      "Trà lương chậm quá 15 ngày thì có phải trả thêm cho người lao động không?",
      "tien_luong",
      ["45_2019_QH14__D97__K4"])

add_q("v2_24",
      "Nếu ngừng việc do lỗi của người lao động thì có được trả lương không?",
      "tien_luong",
      ["45_2019_QH14__D99__K2"])

add_q("v2_25",
      "Trả lương thông qua người cai thầu thì trách nhiệm thuộc về ai?",
      "tien_luong",
      ["45_2019_QH14__D100__K1"])

add_q("v2_26",
      "Người lao động bị tạm đình chỉ công việc có được trả lương không?",
      "tien_luong",
      ["45_2019_QH14__D128__K4"])

add_q("v2_27",
      "Mức lương tối thiểu vùng III theo tháng hiện nay là bao nhiêu?",
      "tien_luong",
      ["293_2025_NDCP__D3__K1"])

# =============================================================================
# 3. LÀM THÊM GIỜ (13 câu)
# =============================================================================

add_q("v2_28",
      "Thời gian làm việc tiếp xúc với yếu tố nguy hiểm, yếu tố có hại phải tuân theo quy định nào?",
      "lam_them_gio",
      ["45_2019_QH14__D105__K3"])

add_q("v2_29",
      "Nhà nước khuyến khích làm việc bao nhiêu giờ 1 tuần?",
      "lam_them_gio",
      ["45_2019_QH14__D105__K2"])

add_q("v2_30",
      "Thời gian làm việc bình thường trong ngày được quy định như nào?",
      "lam_them_gio",
      ["45_2019_QH14__D105__K1"])

add_q("v2_31",
      "Có được ép buộc người lao động làm thêm giờ không?",
      "lam_them_gio",
      ["45_2019_QH14__D107__K2"])

add_q("v2_32",
      "Người sử dụng lao động phải đảm bảo điều kiện gì khi tổ chức làm thêm giờ?",
      "lam_them_gio",
      ["45_2019_QH14__D107__K2"])

add_q("v2_33",
      "Trong trường hợp khắc phục hậu quả thiên tai, hỏa hoạn, dịch bệnh nguy hiểm, người lao động có được từ chối làm thêm giờ không?",
      "lam_them_gio",
      ["45_2019_QH14__D108__K2"])

add_q("v2_34",
      "Người lao động làm ca đêm thì thời giờ làm việc ban đêm được tính từ mấy giờ?",
      "lam_them_gio",
      ["45_2019_QH14__D106"])

add_q("v2_35",
      "Người lao động chuyển ca thì được nghỉ ít nhất bao nhiêu giờ?",
      "lam_them_gio",
      ["45_2019_QH14__D110"])

add_q("v2_36",
      "Lao động nữ mang thai có được làm thêm giờ không?",
      "lam_them_gio",
      ["45_2019_QH14__D137__K1"])

add_q("v2_37",
      "Lao động chưa đủ 15 tuổi được làm việc tối đa mấy giờ một ngày?",
      "lam_them_gio",
      ["45_2019_QH14__D146__K1"])

add_q("v2_38",
      "Công việc nào cấm sử dụng lao động chưa thành niên?",
      "lam_them_gio",
      ["45_2019_QH14__D147__K1"])

add_q("v2_39",
      "Người lao động cao tuổi có được rút ngắn thời gian làm việc không?",
      "lam_them_gio",
      ["45_2019_QH14__D148__K2"])

add_q("v2_40",
      "Người lao động có bị bắt buộc phải làm thêm giờ không?",
      "lam_them_gio",
      ["45_2019_QH14__D107__K2"])

# =============================================================================
# 4. NGHỈ PHÉP (14 câu)
# =============================================================================

add_q("v2_41",
      "Nghỉ giữa giờ ca đêm được quy định bao lâu?",
      "nghi_phep",
      ["45_2019_QH14__D109__K1"])

add_q("v2_42",
      "Người lao động làm việc liên tục 8 tiếng thì được nghỉ giữa giờ bao lâu?",
      "nghi_phep",
      ["45_2019_QH14__D109__K1"])

add_q("v2_43",
      "Nếu làm việc theo ca liên tục thì nghỉ giữa giờ có được tính vào thời giờ làm việc không?",
      "nghi_phep",
      ["45_2019_QH14__D109__K1"])

add_q("v2_44",
      "Nghỉ hằng tuần có thể được sắp xếp vào ngày khác ngoài Chủ nhật không?",
      "nghi_phep",
      ["45_2019_QH14__D111__K2"])

add_q("v2_45",
      "Người lao động nước ngoài làm việc tại Việt Nam có được nghỉ thêm ngày Quốc khánh 2/9 không?",
      "nghi_phep",
      ["45_2019_QH14__D112__K2"])

add_q("v2_46",
      "Người lao động làm công việc nặng nhọc, độc hại có được cộng thêm ngày nghỉ phép không?",
      "nghi_phep",
      ["45_2019_QH14__D113__K1"])

add_q("v2_47",
      "Nghỉ phép năm chưa đủ 12 tháng được tính như nào?",
      "nghi_phep",
      ["45_2019_QH14__D113__K2"])

add_q("v2_48",
      "Nghỉ thai sản có tính vào ngày nghỉ phép hằng năm không?",
      "nghi_phep",
      ["145_2020_NDCP__D65__K7"])

add_q("v2_49",
      "Người lao động có 5 năm thâm niên thì nghỉ phép hằng năm tăng thêm bao nhiêu?",
      "nghi_phep",
      ["45_2019_QH14__D114"])

add_q("v2_50",
      "Người lao động con kết hôn thì được nghỉ mấy ngày hưởng nguyên lương?",
      "nghi_phep",
      ["45_2019_QH14__D115__K1"])

add_q("v2_51",
      "Người sử dụng lao động có trách nhiệm thanh toán tiền tàu xe đi đường cho người lao động khi nghỉ phép không?",
      "nghi_phep",
      ["45_2019_QH14__D113__K6"])

add_q("v2_52",
      "Lao động nữ trong thời gian hành kinh được nghỉ bao lâu mỗi ngày?",
      "nghi_phep",
      ["45_2019_QH14__D137__K4"])

add_q("v2_53",
      "Lao động nữ nuôi con dưới 12 tháng tuổi có được nghỉ thêm trong giờ làm không?",
      "nghi_phep",
      ["45_2019_QH14__D137__K4"])

add_q("v2_54",
      "Người lao động nữ mang thai được giảm bớt giờ làm hay chuyển công việc nhẹ hơn không?",
      "nghi_phep",
      ["45_2019_QH14__D137__K2"])

# =============================================================================
# 5. CHẤM DỨT HỢP ĐỒNG (14 câu)
# =============================================================================

add_q("v2_55",
      "Người lao động ký hợp đồng xác định thời hạn muốn nghỉ phải báo trước bao nhiêu ngày?",
      "cham_dut_hop_dong",
      ["45_2019_QH14__D35__K1"])

add_q("v2_56",
      "Có được đơn phương chấm dứt hợp đồng khi bị quấy rối tình dục tại nơi làm việc không?",
      "cham_dut_hop_dong",
      ["45_2019_QH14__D35__K2"])

add_q("v2_57",
      "Người sử dụng lao động phải báo trước bao nhiêu ngày khi đơn phương chấm dứt hợp đồng?",
      "cham_dut_hop_dong",
      ["45_2019_QH14__D36__K2"])

add_q("v2_58",
      "Có được sa thải lao động nữ đang mang thai vì lý do thu hẹp sản xuất không?",
      "cham_dut_hop_dong",
      ["45_2019_QH14__D37__K3"])

add_q("v2_59",
      "Quyền đơn phương chấm dứt hợp đồng lao động được áp dụng trong các trường hợp nào",
      "cham_dut_hop_dong",
      ["45_2019_QH14__D36__K1"])

add_q("v2_60",
      "Người lao động nghỉ ốm do bệnh thì có bị chấm dứt hợp đồng lao động không?",
      "cham_dut_hop_dong",
      ["45_2019_QH14__D37__K1"])

add_q("v2_61",
      "Nếu tự ý nghỉ việc trái luật, người lao động có phải hoàn trả chi phí đào tạo không?",
      "cham_dut_hop_dong",
      ["45_2019_QH14__D40__K3"])

add_q("v2_62",
      "Công ty đơn phương chấm dứt hợp đồng trái luật thì người lao động được bồi thường thế nào?",
      "cham_dut_hop_dong",
      ["45_2019_QH14__D41__K1"])

add_q("v2_63",
      "Khi thay đổi cơ cấu, công nghệ mà nhiều người mất việc thì công ty phải xây dựng phương án gì?",
      "cham_dut_hop_dong",
      ["45_2019_QH14__D44__K1"])

add_q("v2_64",
      "Khi công ty sáp nhập thì người sử dụng lao động kế tiếp có trách nhiệm gì với người lao động?",
      "cham_dut_hop_dong",
      ["45_2019_QH14__D43__K1"])

add_q("v2_65",
      "Người sử dụng lao động có cần thông báo trước cho người lao động khi hợp đồng sắp hết hạn không?",
      "cham_dut_hop_dong",
      ["45_2019_QH14__D45__K1"])

add_q("v2_66",
      "Tiền lương để tính trợ cấp thôi việc là bình quân của bao nhiêu tháng cuối?",
      "cham_dut_hop_dong",
      ["45_2019_QH14__D46__K3"])

add_q("v2_67",
      "Thời gian làm việc để tính trợ cấp mất việc làm được xác định thế nào?",
      "cham_dut_hop_dong",
      ["45_2019_QH14__D47__K2"])

add_q("v2_68",
      "Khi chấm dứt hợp đồng, nếu có tranh chấp tiền lương thì thời hạn thanh toán kéo dài bao lâu?",
      "cham_dut_hop_dong",
      ["45_2019_QH14__D48__K1"])

# =============================================================================
# 6. BẢO HIỂM (13 câu)
# =============================================================================

add_q("v2_69",
      "Đối tượng nào thuộc diện tham gia bảo hiểm xã hội tự nguyện?",
      "bao_hiem",
      ["58_VBHN-VPQH__D2__K4"])

add_q("v2_70",
      "Người lao động có quyền gì khi tham gia bảo hiểm xã hội?",
      "bao_hiem",
      ["58_VBHN-VPQH__D10__K1"])

add_q("v2_71",
      "Thời gian nghỉ ốm đau đối với lao động làm nghề nặng nhọc, độc hại là bao lâu?",
      "bao_hiem",
      ["58_VBHN-VPQH__D43__K1"])

add_q("v2_72",
      "Được nghỉ tối đa bao nhiêu ngày để chăm sóc con đau ốm?",
      "bao_hiem",
      ["58_VBHN-VPQH__D44__K1"])

add_q("v2_73",
      "Nghỉ dưỡng sức sau ốm đau được tối đa bao nhiêu ngày trong một năm?",
      "bao_hiem",
      ["58_VBHN-VPQH__D46__K1"])

add_q("v2_74",
      "Lao động nữ được nghỉ nghỉ để đi khám thai bao nhiêu lần?",
      "bao_hiem",
      ["58_VBHN-VPQH__D51__K1"])

add_q("v2_75",
      "Hồ sơ khi để hưởng trợ cấp cho lao động nam khi vợ sinh con bao gồm gì?",
      "bao_hiem",
      ["58_VBHN-VPQH__D61__K5"])

add_q("v2_76",
      "Chế độ thai sản khi nhận con nuôi dưới 6 tháng tuổi được quy định thế nào?",
      "bao_hiem",
      ["58_VBHN-VPQH__D56__K1"])

add_q("v2_77",
      "Trợ cấp một lần khi sinh con hoặc nhận con nuôi bằng bao nhiêu tháng lương cơ sở?",
      "bao_hiem",
      ["58_VBHN-VPQH__D58__K1"])

add_q("v2_78",
      "Người lao động đủ tuổi nghỉ hưu nhưng chưa đủ thời gian đóng bảo hiểm xã hội thì được hưởng gì?",
      "bao_hiem",
      ["58_VBHN-VPQH__D23__K1"])

add_q("v2_79",
      "Mức đóng bảo hiểm xã hội bắt buộc hằng tháng của người lao động là bao nhiêu phần trăm?",
      "bao_hiem",
      ["58_VBHN-VPQH__D33__K1"])

add_q("v2_80",
      "Điều kiện hưởng trợ cấp thất nghiệp là gì?",
      "bao_hiem",
      ["74_2025_QH15__D38__K1"])

add_q("v2_81",
      "Mức trợ cấp thất nghiệp hằng tháng bằng bao nhiêu phần trăm bình quân tiền lương?",
      "bao_hiem",
      ["74_2025_QH15__D39__K1"])

# =============================================================================
# 7. CÁC QUYỀN LỢI CƠ BẢN KHÁC (14 câu)
# =============================================================================

add_q("v2_82",
      "Nội quy lao động phải có những nội dung chủ yếu nào?",
      "quyen_loi_khac",
      ["45_2019_QH14__D118__K2"])

add_q("v2_83",
      "Nội quy lao động có hiệu lực sau bao nhiêu ngày kể từ ngày người sử dụng lao động ban hành?",
      "quyen_loi_khac",
      ["45_2019_QH14__D121"])

add_q("v2_84",
      "Người sử dụng lao động sử dụng bao nhiêu người lao động thì phải đăng ký nội quy lao động?",
      "quyen_loi_khac",
      ["45_2019_QH14__D119__K1"])

add_q("v2_85",
      "Việc xử lý kỷ luật lao động được quy định như nào?",
      "quyen_loi_khac",
      ["45_2019_QH14__D122__K1"])

add_q("v2_86",
      "Trường hợp nào không được xử lý kỷ luật lao động?",
      "quyen_loi_khac",
      ["45_2019_QH14__D122__K4"])

add_q("v2_87",
      "Thời hiệu xử lý kỷ luật lao động là bao lâu?",
      "quyen_loi_khac",
      ["45_2019_QH14__D123__K1"])

add_q("v2_88",
      "Các hình thức kỷ luật lao động bao gồm những gì?",
      "quyen_loi_khac",
      ["45_2019_QH14__D124__K1"])

add_q("v2_89",
      "Người thử việc có cần phải được huấn luyện vệ sinh an toàn, thực phẩm không?",
      "quyen_loi_khac",
      ["84_2015_QH13__D14__K4"])

add_q("v2_90",
      "Người lao động có quyền rời khỏi nơi làm việc khi thấy nguy hiểm không?",
      "quyen_loi_khac",
      ["84_2015_QH13__D6__K1"])

add_q("v2_91",
      "Tai nạn lao động xảy ra thì ai có trách nhiệm khai báo?",
      "quyen_loi_khac",
      ["84_2015_QH13__D34__K1"])

add_q("v2_92",
      "Người sử dụng lao động có trách nhiệm bồi thường tai nạn lao động cho người lao động không?",
      "quyen_loi_khac",
      ["84_2015_QH13__D38__K4"])

add_q("v2_93",
      "Đoàn viên công đoàn có quyền được Công đoàn hỗ trợ tìm việc làm không?",
      "quyen_loi_khac",
      ["50_2024_QH15__D21__K7"])

add_q("v2_94",
      "Người sử dụng lao động có trách nhiệm gì đối với Công đoàn?",
      "quyen_loi_khac",
      ["50_2024_QH15__D25__K1"])

add_q("v2_95",
      "Dữ liệu cá nhân nhạy cảm bao gồm những loại nào?",
      "quyen_loi_khac",
      ["91_2025_QH15__D2__K3"])

# =============================================================================
# 8. NGOÀI PHẠM VI (25 câu)
# =============================================================================

# 8.1 Luật khác (7 câu)
add_q("v2_oos_01",
      "Đăng ký kết hôn đồng giới ở Việt Nam có được pháp luật công nhận không?",
      "out_of_scope", [])

add_q("v2_oos_02",
      "Lãi suất cho vay tín chấp của ngân hàng hiện nay bao nhiêu phần trăm?",
      "out_of_scope", [])

add_q("v2_oos_03",
      "Nồng độ cồn bao nhiêu thì bị tước giấy phép lái xe?",
      "out_of_scope", [])

add_q("v2_oos_04",
      "Quy trình kê khai thuế thu nhập cá nhân trực tuyến như thế nào?",
      "out_of_scope", [])

add_q("v2_oos_05",
      "Thủ tục xin cấp giấy phép xây dựng nhà ở riêng lẻ cần giấy tờ gì?",
      "out_of_scope", [])

add_q("v2_oos_06",
      "Thủ tục sang tên xe máy cần những gì?",
      "out_of_scope", [])

add_q("v2_oos_07",
      "Điều kiện để được nhận thừa kế theo di chúc là gì?",
      "out_of_scope", [])

# 8.2 Tư vấn cá nhân (6 câu)
add_q("v2_oos_08",
      "Công ty yêu cầu tôi ký thỏa thuận chấm dứt hợp đồng ngay trong hôm nay, tôi nên xử lý thế nào?",
      "out_of_scope", [])

add_q("v2_oos_09",
      "Nếu muốn khởi kiện công ty cũ thì tôi nên chọn Tòa án nào để giải quyết?",
      "out_of_scope", [])

add_q("v2_oos_10",
      "Lương tôi 15 triệu, bạn lập kế hoạch tài chính cho tôi xem nên chi tiêu thế nào.",
      "out_of_scope", [])

add_q("v2_oos_11",
      "Tôi bị công ty cho nghỉ việc, theo bạn tôi có nên yêu cầu họ bồi thường hay không?",
      "out_of_scope", [])

add_q("v2_oos_12",
      "Tôi muốn chuyển việc sang ngành IT, bạn tư vấn nên học trường nào?",
      "out_of_scope", [])

add_q("v2_oos_13",
      "Viết cho tôi email xin tăng lương thật thuyết phục gửi sếp.",
      "out_of_scope", [])

# 8.3 Vô nghĩa / Conversational (6 câu)
add_q("v2_oos_14",
      "Kể cho tôi một câu chuyện cười hay.",
      "out_of_scope", [])

add_q("v2_oos_15",
      "Bạn có thể chơi cờ vua với tôi được không?",
      "out_of_scope", [])

add_q("v2_oos_16",
      "abc xyz 123 456",
      "out_of_scope", [])

add_q("v2_oos_17",
      "Sáng nay trời mưa to quá, bạn có ô không?",
      "out_of_scope", [])

add_q("v2_oos_18",
      "Hello, how are you?",
      "out_of_scope", [])

add_q("v2_oos_19",
      "Hãy dịch câu 'I love my job' sang tiếng Nhật.",
      "out_of_scope", [])

# 8.4 Cận biên giới (6 câu)
add_q("v2_oos_20",
      "Người nước ngoài mua nhà ở Việt Nam cần điều kiện gì?",
      "out_of_scope", [])

add_q("v2_oos_21",
      "Thuế thu nhập cá nhân đối với khoản tiền thưởng cuối năm được tính như thế nào?",
      "out_of_scope", [])

add_q("v2_oos_22",
      "Công chức nhà nước xin thôi việc thì thủ tục khác gì so với người lao động thường?",
      "out_of_scope", [])

add_q("v2_oos_23",
      "Doanh nghiệp cổ phần hóa thì người lao động có được mua cổ phần ưu đãi không?",
      "out_of_scope", [])

add_q("v2_oos_24",
      "Bảo hiểm y tế chi trả bao nhiêu phần trăm khi khám bệnh?",
      "out_of_scope", [])

add_q("v2_oos_25",
      "Thuế thu nhập cá nhân phải đóng bao nhiêu nếu lương 20 triệu một tháng?",
      "out_of_scope", [])

# 8.5 BHXH / văn bản pháp luật cũ, hết hiệu lực (8 câu)
add_q("v2_oos_26",
      "Theo Luật Bảo hiểm xã hội năm 2014, điều kiện hưởng lương hưu của người lao động là gì?",
      "out_of_scope", [])

add_q("v2_oos_27",
      "Theo Luật Bảo hiểm xã hội năm 2014, người lao động đóng bảo hiểm xã hội bao nhiêu năm thì được hưởng lương hưu?",
      "out_of_scope", [])

add_q("v2_oos_28",
      "Theo quy định bảo hiểm xã hội trước đây, mức hưởng bảo hiểm xã hội một lần được tính như thế nào?",
      "out_of_scope", [])

add_q("v2_oos_29",
      "Luật Bảo hiểm xã hội năm 2014 quy định chế độ thai sản cho lao động nữ như thế nào?",
      "out_of_scope", [])

add_q("v2_oos_30",
      "Theo quy định bảo hiểm xã hội cũ, người lao động nghỉ ốm được hưởng chế độ trong bao lâu?",
      "out_of_scope", [])

add_q("v2_oos_31",
      "Mức đóng bảo hiểm xã hội bắt buộc theo quy định cũ được tính như thế nào?",
      "out_of_scope", [])

add_q("v2_oos_32",
      "Theo quy định bảo hiểm xã hội trước đây, người lao động có thể nhận bảo hiểm xã hội một lần trong những trường hợp nào?",
      "out_of_scope", [])

add_q("v2_oos_33",
      "Quy định về trợ cấp thất nghiệp theo pháp luật bảo hiểm xã hội cũ được áp dụng như thế nào?",
      "out_of_scope", [])

# 8.6 Luật dân sự / luật gần miền (6 câu)      
add_q("v2_oos_34",
      "Theo Bộ luật Dân sự, hợp đồng vay tài sản giữa hai cá nhân được quy định như thế nào?",
      "out_of_scope", [])

add_q("v2_oos_35",
      "Nếu một người gây thiệt hại cho tài sản của người khác thì trách nhiệm bồi thường được xác định thế nào?",
      "out_of_scope", [])

add_q("v2_oos_36",
      "Thời hiệu khởi kiện tranh chấp hợp đồng dân sự là bao lâu?",
      "out_of_scope", [])

add_q("v2_oos_37",
      "Người thừa kế có quyền từ chối nhận di sản trong trường hợp nào?",
      "out_of_scope", [])

add_q("v2_oos_38",
      "Hợp đồng dân sự vô hiệu thì các bên phải hoàn trả cho nhau những gì?",
      "out_of_scope", [])

add_q("v2_oos_39",
      "Một người đủ bao nhiêu tuổi thì có đầy đủ năng lực hành vi dân sự?",
      "out_of_scope", [])

# 8.7 Lời khuyên chiến lược / quyết định cá nhân (5 câu)
add_q("v2_oos_40",
      "Tôi đang có hai công việc với mức lương khác nhau, bạn nghĩ tôi nên chọn công việc nào?",
      "out_of_scope", [])

add_q("v2_oos_41",
      "Công ty đề nghị tôi ký một thỏa thuận mới, theo bạn tôi có nên ký ngay không?",
      "out_of_scope", [])

add_q("v2_oos_42",
      "Tôi đang tranh chấp với công ty, bạn nghĩ tôi nên thương lượng hay đưa vụ việc ra Tòa án?",
      "out_of_scope", [])

add_q("v2_oos_43",
      "Tôi muốn nghỉ việc nhưng chưa biết thời điểm nào là phù hợp nhất, bạn tư vấn giúp tôi.",
      "out_of_scope", [])

add_q("v2_oos_44",
      "Nếu công ty không đồng ý với yêu cầu của tôi thì tôi nên làm gì tiếp theo?",
      "out_of_scope", [])

# 8.8 Câu gài / near-domain trap (6 câu)
add_q("v2_oos_45",
      "Người lao động bị tai nạn trên đường đi làm thì mức bồi thường dân sự được tính thế nào?",
      "out_of_scope", [])

add_q("v2_oos_46",
      "Tiền lương của người lao động có được dùng để thế chấp khoản vay ngân hàng không?",
      "out_of_scope", [])

add_q("v2_oos_47",
      "Người lao động nghỉ việc rồi có được yêu cầu công ty trả lại tài sản cá nhân đã gửi tại nơi làm việc không?",
      "out_of_scope", [])

add_q("v2_oos_48",
      "Nếu doanh nghiệp phá sản thì thứ tự thanh toán các khoản nợ đối với người lao động được xác định theo luật phá sản như thế nào?",
      "out_of_scope", [])

add_q("v2_oos_49",
      "Người lao động có phải chịu trách nhiệm hình sự nếu làm lộ bí mật kinh doanh của công ty không?",
      "out_of_scope", [])

add_q("v2_oos_50",
      "Khi người lao động làm mất tài sản của công ty thì trách nhiệm bồi thường được xác định theo pháp luật dân sự như thế nào?",
      "out_of_scope", [])

# =============================================================================
# XUẤT FILE
# =============================================================================
output_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'eval', 'test_set_v2.json')
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(questions, f, ensure_ascii=False, indent=2)

in_scope = [q for q in questions if q["category"] != "out_of_scope"]
out_scope = [q for q in questions if q["category"] == "out_of_scope"]

# In thống kê
from collections import Counter
cats = Counter(q["category"] for q in questions)

print(f"Created Test Set V2: {len(questions)} questions ({len(in_scope)} in-scope, {len(out_scope)} out-of-scope)")
for cat, cnt in sorted(cats.items()):
    print(f"  {cat}: {cnt}")
print(f"Saved to: {output_path}")

# Kiểm tra có trùng câu hỏi với bộ test set cũ
test_v1_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'eval', 'archive', 'test_set_v1.json')
if not os.path.exists(test_v1_path):
    test_v1_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'eval', 'test_set_v1.json')
dev_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'eval', 'dev_set.json')

v1 = []
if os.path.exists(test_v1_path):
    with open(test_v1_path, 'r', encoding='utf-8') as f:
        v1 = json.load(f)
dev = []
if os.path.exists(dev_path):
    with open(dev_path, 'r', encoding='utf-8') as f:
        dev = json.load(f)

old_questions = set(q["question"] for q in v1 + dev)
new_questions = set(q["question"] for q in questions)
q_overlap = old_questions & new_questions
if q_overlap:
    print(f"\nWARNING: Overlapping questions ({len(q_overlap)}):")
    for q in q_overlap:
        print(f"  - {q}")
else:
    print(f"No question text overlap with v1/dev.")
