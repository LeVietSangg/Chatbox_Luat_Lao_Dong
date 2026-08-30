import os
import json

questions = []

def add_q(qid, q, category, gold_ids, relaxed_ids=None):
    questions.append({
        "id": qid,
        "question": q,
        "category": category,
        "gold_provision_ids": gold_ids,
        "gold_provision_ids_relaxed": relaxed_ids or []
    })

# In-scope questions (25 questions)
add_q("d1_01", "Ký hợp đồng thử việc tối đa bao lâu với người lao động phổ thông?", "hop_dong_lao_dong", ["45_2019_QH14__D25__K4"])
add_q("d1_02", "Hợp đồng lao động bằng miệng có giá trị pháp lý không?", "hop_dong_lao_dong", ["45_2019_QH14__D14__K2"])
add_q("d1_03", "Công ty giữ giấy tờ gốc của tôi khi nhận việc có đúng luật không?", "hop_dong_lao_dong", ["45_2019_QH14__D17__K1"])

add_q("d2_01", "Mức lương tối thiểu vùng hiện nay là bao nhiêu?", "tien_luong", ["293_2025_NDCP__D3__K1"])
add_q("d2_02", "Công ty chậm trả lương bao lâu thì tôi được quyền nghỉ việc ngay?", "tien_luong", ["45_2019_QH14__D35__K2"])
add_q("d2_03", "Trợ cấp thôi việc được tính như thế nào khi nghỉ việc?", "tien_luong", ["45_2019_QH14__D46__K1"])
add_q("d2_04", "Hình thức trả lương cho người lao động gồm những gì?", "tien_luong", ["45_2019_QH14__D96__K1"])

add_q("d3_01", "Tiền lương làm thêm giờ vào ngày nghỉ lễ được tính thế nào?", "lam_them_gio", ["45_2019_QH14__D98__K1"])
add_q("d3_02", "Tôi phải làm thêm giờ vào ban đêm thì được trả lương như thế nào?", "lam_them_gio", ["45_2019_QH14__D98__K3"])
add_q("d3_03", "Làm thêm giờ tối đa trong một tháng là bao nhiêu giờ?", "lam_them_gio", ["45_2019_QH14__D107__K2"])

add_q("d4_01", "Thời giờ làm việc bình thường của người lao động là bao nhiêu tiếng một ngày?", "nghi_phep", ["45_2019_QH14__D105__K1"])
add_q("d4_02", "Mỗi tuần tôi được nghỉ ít nhất bao nhiêu ngày?", "nghi_phep", ["45_2019_QH14__D111__K1"])
add_q("d4_03", "Làm việc đủ 12 tháng thì được nghỉ phép năm bao nhiêu ngày?", "nghi_phep", ["45_2019_QH14__D113__K1"])
add_q("d4_04", "Người lao động được nghỉ lễ, tết như thế nào tại Việt Nam?", "nghi_phep", ["45_2019_QH14__D112__K1"])

add_q("d5_01", "Người lao động có được đơn phương chấm dứt hợp đồng không?", "cham_dut_hop_dong", ["45_2019_QH14__D35__K1"])
add_q("d5_02", "Người lao động tổ chức đánh bạc tại nơi làm việc thì có bị sa thải không?", "cham_dut_hop_dong", ["45_2019_QH14__D125__K1"])
add_q("d5_03", "Tự ý bỏ việc mấy ngày thì công ty có quyền sa thải?", "cham_dut_hop_dong", ["45_2019_QH14__D125__K4"])
add_q("d5_04", "Người sử dụng lao động có quyền đơn phương chấm dứt hợp đồng lao động trong trường hợp nào?", "cham_dut_hop_dong", ["45_2019_QH14__D36__K1"])

add_q("d6_01", "Lao động nữ sẩy thai thì được nghỉ việc hưởng BHXH bao nhiêu ngày?", "bao_hiem", ["58_VBHN-VPQH__D52__K1"], ["58_VBHN-VPQH__D52__K2"])
add_q("d6_02", "Điều kiện hưởng lương hưu đối với lao động nam làm việc bình thường là gì?", "bao_hiem", ["58_VBHN-VPQH__D64__K1"], ["45_2019_QH14__D169__K2"])
add_q("d6_03", "Mức đóng bảo hiểm xã hội bắt buộc đối với người lao động là bao nhiêu?", "bao_hiem", ["58_VBHN-VPQH__D33__K1"], ["58_VBHN-VPQH__D33__K2", "58_VBHN-VPQH__D33__K3", "58_VBHN-VPQH__D33__K4"])

add_q("d7_01", "Công ty có bắt buộc phải tổ chức khám sức khỏe định kỳ cho nhân viên không?", "quyen_loi_khac", ["84_2015_QH13__D21__K1"])
add_q("d7_02", "Khi bị tai nạn lao động, người sử dụng lao động phải sơ cứu như thế nào?", "quyen_loi_khac", ["84_2015_QH13__D38__K1"])
add_q("d7_03", "Đoàn viên công đoàn có quyền được đại diện bảo vệ quyền lợi không?", "quyen_loi_khac", ["50_2024_QH15__D21__K1"])
add_q("d7_04", "Việc thu thập dữ liệu cá nhân của người lao động phải đảm bảo nguyên tắc gì?", "quyen_loi_khac", ["91_2025_QH15__D3__K3"])

# Out-of-scope questions (5 questions)
add_q("d8_01", "Công ty tôi phá sản thì giám đốc có bị đi tù không?", "out_of_scope", [])
add_q("d8_02", "Tôi bị tai nạn giao thông trên đường đi chơi, có được bảo hiểm y tế chi trả không?", "out_of_scope", [])
add_q("d8_03", "Mức thuế thu nhập doanh nghiệp năm 2025 là bao nhiêu?", "out_of_scope", [])
add_q("d8_04", "Tôi cãi nhau với đồng nghiệp sứt đầu mẻ trán, công ty có nên đuổi cả hai không?", "out_of_scope", [])
add_q("d8_05", "Alo chatbot, tối nay ăn gì ngon?", "out_of_scope", [])

output_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'eval', 'dev_set.json')
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(questions, f, ensure_ascii=False, indent=2)

print(f"Created {len(questions)} dev set questions at {output_path}")
