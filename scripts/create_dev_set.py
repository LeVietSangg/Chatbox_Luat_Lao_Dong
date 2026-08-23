import os
import json

questions = []

def add_q(qid, q, category, gold_ids):
    questions.append({
        "id": qid,
        "question": q,
        "category": category,
        "gold_provision_ids": gold_ids,
        "gold_provision_ids_relaxed": []
    })

# In-scope questions (25 questions)
add_q("d1_01", "Người lao động có được đơn phương chấm dứt hợp đồng không?", "hop_dong", ["45_2019_QH14__D35__K1"])
add_q("d1_02", "Công ty giữ giấy tờ gốc của tôi khi nhận việc có đúng luật không?", "hop_dong", ["45_2019_QH14__D17__K1"])
add_q("d1_03", "Ký hợp đồng thử việc tối đa bao lâu với người lao động phổ thông?", "hop_dong", ["45_2019_QH14__D25__K4"])
add_q("d1_04", "Hợp đồng lao động bằng miệng có giá trị pháp lý không?", "hop_dong", ["45_2019_QH14__D14__K2"])

add_q("d2_01", "Tôi phải làm thêm giờ vào ban đêm thì được trả lương như thế nào?", "tien_luong", ["45_2019_QH14__D98__K3"])
add_q("d2_02", "Tiền lương làm thêm giờ vào ngày nghỉ lễ được tính thế nào?", "tien_luong", ["45_2019_QH14__D98__K1"])
add_q("d2_03", "Trợ cấp thôi việc được tính như thế nào khi nghỉ việc?", "tien_luong", ["45_2019_QH14__D46__K1"])
add_q("d2_04", "Công ty chậm trả lương bao lâu thì tôi được quyền nghỉ việc ngay?", "tien_luong", ["45_2019_QH14__D35__K2"])

add_q("d3_01", "Thời giờ làm việc bình thường của người lao động là bao nhiêu tiếng một ngày?", "thoi_gian", ["45_2019_QH14__D105__K1"])
add_q("d3_02", "Người lao động được nghỉ thai sản tổng cộng mấy tháng?", "thoi_gian", ["45_2019_QH14__D139__K1"])
add_q("d3_03", "Mỗi tuần tôi được nghỉ ít nhất bao nhiêu ngày?", "thoi_gian", ["45_2019_QH14__D111__K1"])
add_q("d3_04", "Làm việc đủ 12 tháng thì được nghỉ phép năm bao nhiêu ngày?", "thoi_gian", ["45_2019_QH14__D113__K1"])

add_q("d4_01", "Khi nào thì bị sa thải?", "ky_luat", ["45_2019_QH14__D125__K1"])
add_q("d4_02", "Hình thức kỷ luật lao động bao gồm những gì?", "ky_luat", ["45_2019_QH14__D124"])
add_q("d4_03", "Tự ý bỏ việc mấy ngày thì công ty có quyền sa thải?", "ky_luat", ["45_2019_QH14__D125__K4"])
add_q("d4_04", "Có được dùng hình thức phạt tiền để thay cho kỷ luật lao động không?", "ky_luat", ["45_2019_QH14__D127__K2"])

add_q("d5_01", "Công ty có bắt buộc phải tổ chức khám sức khỏe định kỳ cho nhân viên không?", "an_toan", ["84_2015_QH13__D21__K1"])
add_q("d5_02", "Khi bị tai nạn lao động, người sử dụng lao động phải sơ cứu như thế nào?", "an_toan", ["84_2015_QH13__D38__K1"])
add_q("d5_03", "Việc thu thập dữ liệu cá nhân của người lao động có cần báo trước không?", "an_toan", ["91_2025_QH15__D3__K1"])

add_q("d6_01", "Lao động nữ sẩy thai thì được nghỉ việc hưởng BHXH bao nhiêu ngày?", "bhxh", ["58_VBHN-VPQH__D33__K1"])
add_q("d6_02", "Điều kiện hưởng lương hưu đối với lao động nam làm việc bình thường là gì?", "bhxh", ["58_VBHN-VPQH__D54__K1"])
add_q("d6_03", "Mức đóng bảo hiểm xã hội bắt buộc đối với người lao động là bao nhiêu?", "bhxh", ["58_VBHN-VPQH__D85__K1"])

add_q("d7_01", "Độ tuổi tối thiểu của người lao động là bao nhiêu?", "dac_biet", ["45_2019_QH14__D3__K1"])
add_q("d7_02", "Người lao động cao tuổi có được thỏa thuận rút ngắn thời gian làm việc không?", "dac_biet", ["45_2019_QH14__D148__K2"])
add_q("d7_03", "Đoàn viên công đoàn có quyền được đại diện bảo vệ quyền lợi không?", "dac_biet", ["50_2024_QH15__D21__K1"])

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
