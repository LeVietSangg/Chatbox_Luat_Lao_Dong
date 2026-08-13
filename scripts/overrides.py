# -*- coding: utf-8 -*-

# ============================================================
# BẢNG MAPPING THỦ CÔNG: filename → (doc_code, doc_name, doc_type, ngay_hieu_luc, trang_thai)
# Đảm bảo doc_code duy nhất cho mỗi văn bản
# ============================================================

DOC_REGISTRY = {
    "VBHN-BoLuatLaoDong": {
        "doc_code": "45_2019_QH14",
        "doc_name": "Bộ luật Lao động",
        "doc_type": "Bộ luật",
        "so_hieu": "45/2019/QH14",
        "ngay_hieu_luc": "2026-01-01",
        "trang_thai_chung": "con_hieu_luc",
        "ghi_chu": "VBHN, sửa đổi bởi Luật 71/2025/QH15",
    },
    "VBHN-LuatBHXH": {
        "doc_code": "58_VBHN-VPQH",
        "doc_name": "Luật Bảo hiểm xã hội",
        "doc_type": "Luật",
        "so_hieu": "58/VBHN-VPQH",
        "ngay_hieu_luc": "2025-08-15",
        "trang_thai_chung": "con_hieu_luc",
        "ghi_chu": "VBHN, sửa đổi bởi Luật 73/2025 và 84/2025",
    },
    "VanBanGoc_84.2015.QH13": {
        "doc_code": "84_2015_QH13",
        "doc_name": "Luật An toàn, vệ sinh lao động",
        "doc_type": "Luật",
        "so_hieu": "84/2015/QH13",
        "ngay_hieu_luc": "2016-07-01",
        "trang_thai_chung": "het_hieu_luc_mot_phan",
        "ghi_chu": "",
    },
    "hienphap": {
        "doc_code": "HP_2013",
        "doc_name": "Hiến pháp 2013",
        "doc_type": "Hiến pháp",
        "so_hieu": "Hiến pháp 2013",
        "ngay_hieu_luc": "2014-01-01",
        "trang_thai_chung": "con_hieu_luc",
        "ghi_chu": "",
    },
    "LuatCongDoan": {
        "doc_code": "50_2024_QH15",
        "doc_name": "Luật Công đoàn",
        "doc_type": "Luật",
        "so_hieu": "50/2024/QH15",
        "ngay_hieu_luc": "2025-07-01",
        "trang_thai_chung": "het_hieu_luc_mot_phan",
        "ghi_chu": "",
    },
    "LuatViecLam": {
        "doc_code": "74_2025_QH15",
        "doc_name": "Luật Việc làm",
        "doc_type": "Luật",
        "so_hieu": "74/2025/QH15",
        "ngay_hieu_luc": "2026-01-01",
        "trang_thai_chung": "con_hieu_luc",
        "ghi_chu": "",
    },
    "luatnguoikhuyettat": {
        "doc_code": "51_2010_QH12",
        "doc_name": "Luật Người khuyết tật",
        "doc_type": "Luật",
        "so_hieu": "51/2010/QH12",
        "ngay_hieu_luc": "2011-01-01",
        "trang_thai_chung": "het_hieu_luc_mot_phan",
        "ghi_chu": "",
    },
    "10.2012.QH13": {
        "doc_code": "10_2012_QH13",
        "doc_name": "Bộ luật Lao động 2012",
        "doc_type": "Bộ luật",
        "so_hieu": "10/2012/QH13",
        "ngay_hieu_luc": "2013-05-01",
        "trang_thai_chung": "het_hieu_luc",
        "ghi_chu": "Hết hiệu lực, thay thế bởi 45/2019/QH14",
    },
    "LuatThanhTra": {
        "doc_code": "84_2025_QH15",
        "doc_name": "Luật Thanh tra",
        "doc_type": "Luật",
        "so_hieu": "84/2025/QH15",
        "ngay_hieu_luc": "2025-07-01",
        "trang_thai_chung": "het_hieu_luc_mot_phan",
        "ghi_chu": "",
    },
    "LuatBaoVeDuLieuCaNhan": {
        "doc_code": "91_2025_QH15",
        "doc_name": "Luật Bảo vệ dữ liệu cá nhân",
        "doc_type": "Luật",
        "so_hieu": "91/2025/QH15",
        "ngay_hieu_luc": "2026-01-01",
        "trang_thai_chung": "con_hieu_luc",
        "ghi_chu": "",
    },
    "Luật_số_69.2020.QH14": {
        "doc_code": "69_2020_QH14",
        "doc_name": "Luật Người lao động Việt Nam đi làm việc ở nước ngoài theo hợp đồng",
        "doc_type": "Luật",
        "so_hieu": "69/2020/QH14",
        "ngay_hieu_luc": "2022-01-01",
        "trang_thai_chung": "con_hieu_luc",
        "ghi_chu": "",
    },
    # --- Nghị định ---
    "Nghị_định_số_145.2020.NĐ-CP": {
        "doc_code": "145_2020_NDCP",
        "doc_name": "Nghị định 145/2020/NĐ-CP",
        "doc_type": "Nghị định",
        "so_hieu": "145/2020/NĐ-CP",
        "ngay_hieu_luc": "2021-02-01",
        "trang_thai_chung": "het_hieu_luc_mot_phan",
        "ghi_chu": "Hướng dẫn BLLĐ về điều kiện lao động và quan hệ lao động",
    },
    "Nghị_định_số_293.2025.NĐ-CP": {
        "doc_code": "293_2025_NDCP",
        "doc_name": "Nghị định 293/2025/NĐ-CP",
        "doc_type": "Nghị định",
        "so_hieu": "293/2025/NĐ-CP",
        "ngay_hieu_luc": "2026-01-01",
        "trang_thai_chung": "con_hieu_luc",
        "ghi_chu": "Mức lương tối thiểu",
    },
    "Nghị_định_số_152.2020.NĐ-CP": {
        "doc_code": "152_2020_NDCP",
        "doc_name": "Nghị định 152/2020/NĐ-CP",
        "doc_type": "Nghị định",
        "so_hieu": "152/2020/NĐ-CP",
        "ngay_hieu_luc": "2021-02-15",
        "trang_thai_chung": "het_hieu_luc_mot_phan",
        "ghi_chu": "Lao động nước ngoài làm việc tại Việt Nam",
    },
    "Nghị_định_số_12.2022.NĐ-CP": {
        "doc_code": "12_2022_NDCP",
        "doc_name": "Nghị định 12/2022/NĐ-CP",
        "doc_type": "Nghị định",
        "so_hieu": "12/2022/NĐ-CP",
        "ngay_hieu_luc": "2022-01-17",
        "trang_thai_chung": "con_hieu_luc",
        "ghi_chu": "Xử phạt vi phạm hành chính trong lĩnh vực lao động",
    },
    "Nghị_định_số_70.2023.NĐ-CP": {
        "doc_code": "70_2023_NDCP",
        "doc_name": "Nghị định 70/2023/NĐ-CP",
        "doc_type": "Nghị định",
        "so_hieu": "70/2023/NĐ-CP",
        "ngay_hieu_luc": "2023-09-18",
        "trang_thai_chung": "het_hieu_luc_mot_phan",
        "ghi_chu": "Sửa đổi NĐ 152/2020 về lao động nước ngoài",
    },
    "ND_luatbaovedulieu": {
        "doc_code": "356_2025_NDCP",
        "doc_name": "Nghị định 356/2025/NĐ-CP",
        "doc_type": "Nghị định",
        "so_hieu": "356/2025/NĐ-CP",
        "ngay_hieu_luc": "2026-01-01",
        "trang_thai_chung": "con_hieu_luc",
        "ghi_chu": "Hướng dẫn thi hành Luật Bảo vệ dữ liệu cá nhân",
    },
}

# Từ điển ghi đè (Override) dành cho các Điều/Khoản bị bãi bỏ hoặc sửa đổi
# đối với các văn bản "hết hiệu lực một phần"
# Mỗi entry tạo ra 2 chunk: v1 (nội dung cũ, hết hiệu lực) + v2 (nội dung mới, còn hiệu lực)
MODIFIED_PROVISIONS = {
    "145_2020_NDCP__D4__K2": {
        "ghi_chu_v1": "Điều khoản sửa đổi, bổ sung",
        "ngay_het_hieu_luc": "",
        "van_ban_sua_doi": "Khoản 1, Điều 73, Chương VIII Nghị định số 35/2022/NĐ-CP Quy định về quản lý khu công nghiệp và khu kinh tế",
        "noi_dung_v2": """Điều 4. Báo cáo sử dụng lao động\n2. Định kỳ 06 tháng (trước ngày 05 tháng 6) và hằng năm (trước ngày 05 tháng 12), người sử dụng lao động phải báo cáo tình hình thay đổi lao động đến Sở Lao động - Thương binh và Xã hội thông qua Cổng Dịch vụ công Quốc gia theo Mẫu số 01/PLI Phụ lục I ban hành kèm theo Nghị định này và thông báo đến cơ quan bảo hiểm xã hội cấp huyện nơi đặt trụ sở, chi nhánh, văn phòng đại diện. Trường hợp người sử dụng lao động không thể báo cáo tình hình thay đổi lao động thông qua Cổng Dịch vụ công Quốc gia thì gửi báo cáo bằng bản giấy theo Mẫu số 01/PLI Phụ lục I ban hành kèm theo Nghị định này đến Sở Lao động - Thương binh và Xã hội và thông báo đến cơ quan bảo hiểm xã hội cấp huyện nơi đặt trụ sở, chi nhánh, văn phòng đại diện. Đối với lao động làm việc trong khu công nghiệp, khu kinh tế, người sử dụng lao động phải báo cáo tình hình thay đổi lao động đến Sở Lao động - Thương binh và Xã hội, cơ quan bảo hiểm xã hội cấp huyện nơi đặt trụ sở, chi nhánh, văn phòng đại diện và Ban quản lý khu công nghiệp, khu kinh tế để theo dõi.
Sở Lao động - Thương binh và Xã hội có trách nhiệm tổng hợp tình hình thay đổi về lao động trong trường hợp người sử dụng lao động gửi báo cáo bằng bản giấy để cập nhật đầy đủ thông tin theo Mẫu số 02/PLI Phụ lục I ban hành kèm theo Nghị định này""",
        "ngay_hieu_luc_v2": "2022-07-15",
        "ghi_chu_v2": "Sửa đổi, bổ sung bởi điểm a khoản 1 Điều 9 Nghị định 128/2025/NĐ-CP",
    },

    "145_2020_NDCP__D31__K2": {
        "ghi_chu_v1": "Điều khoản sửa đổi, bổ sung",
        "ngay_het_hieu_luc": "",
        "van_ban_sua_doi": "Khoản 2, Điều 73, Chương VIII Nghị định số 35/2022/NĐ-CP Quy định về quản lý khu công nghiệp và khu kinh tế",
        "noi_dung_v2": """Điều 4. Báo cáo sử dụng lao động\n2. Định kỳ 06 tháng và hằng năm, báo cáo tình hình hoạt động cho thuê lại lao động theo Mẫu số 09/PLIII Phụ lục III ban hành kèm theo Nghị định này, gửi Chủ tịch Ủy ban nhân dân cấp tỉnh, Sở Lao động - Thương binh và Xã hội và Ban quản lý khu công nghiệp, khu kinh tế nơi doanh nghiệp đặt trụ sở chính; đồng thời báo cáo Sở Lao động - Thương binh và Xã hội và Ban quản lý khu công nghiệp, khu kinh tế nơi doanh nghiệp đến hoạt động cho thuê lại lao động về tình hình hoạt động cho thuê lại lao động trên địa bàn đó đối với trường hợp doanh nghiệp cho thuê lại sang địa bàn cấp tỉnh khác hoạt động. Báo cáo 06 tháng gửi trước ngày 20 tháng 6 và báo cáo năm gửi trước ngày 20 tháng 12""",
        "ngay_hieu_luc_v2": "2022-07-15",
        "ghi_chu_v2": "Sửa đổi, bổ sung bởi điểm a khoản 1 Điều 9 Nghị định 128/2025/NĐ-CP",
    },

    "50_2024_QH15__D1": {
        "ghi_chu_v1": "Điều khoản sửa đổi, bổ sung",
        "ngay_het_hieu_luc": "",
        "van_ban_sua_doi": "Khoản 1, Điều 2 Luật sửa đổi, bổ sung một số điều của Luật Mặt trận Tổ quốc Việt Nam, Luật Công đoàn, Luật Thanh niên và Luật Thực hiện dân chủ ở cơ sở số 97/2025/QH15",
        "noi_dung_v2": """Điều 1. Công đoàn Việt Nam
Công đoàn Việt Nam là tổ chức chính trị - xã hội rộng lớn của giai cấp công nhân và của người lao động, được thành lập trên cơ sở tự nguyện, là thành viên trong hệ thống chính trị do Đảng Cộng sản Việt Nam lãnh đạo, trực thuộc Mặt trận Tổ quốc Việt Nam; đại diện, chăm lo và bảo vệ quyền, lợi ích hợp pháp, chính đáng cho đoàn viên công đoàn và người lao động; là đại diện duy nhất của người lao động ở cấp quốc gia trong quan hệ lao động và quan hệ quốc tế về công đoàn; tham gia quản lý nhà nước, quản lý kinh tế - xã hội; tham gia kiểm tra, thanh tra, giám sát hoạt động của cơ quan nhà nước, tổ chức, đơn vị, doanh nghiệp về những vấn đề liên quan đến quyền, nghĩa vụ của người lao động; tuyên truyền, vận động người lao động học tập, nâng cao trình độ, kỹ năng nghề nghiệp, chấp hành pháp luật, xây dựng và bảo vệ Tổ quốc.""",
        "ngay_hieu_luc_v2": "2025-07-01",
        "ghi_chu_v2": "bổ sung mới",
    },

    "50_2024_QH15__D4__K2": {
        "ghi_chu_v1": "Điều khoản sửa đổi, bổ sung",
        "ngay_het_hieu_luc": "",
        "van_ban_sua_doi": "Luật Mặt trận Tổ quốc Việt Nam, Luật Công đoàn, Luật Thanh niên và Luật Thực hiện dân chủ ở cơ sở số 97/2025/QH15",
        "noi_dung_v2": """Điều 4. Giải thích từ ngữ
2. Công đoàn cơ sở là tổ chức cơ sở của Công đoàn Việt Nam, tập hợp đoàn viên công đoàn trong một hoặc một số tổ chức, đơn vị, doanh nghiệp, được công đoàn cấp trên cơ sở công nhận theo quy định của pháp luật và Điều lệ Công đoàn Việt Nam.""",
        "ngay_hieu_luc_v2": "2025-07-01",
        "ghi_chu_v2": "bổ sung mới",
    },

    "50_2024_QH15__D4__K3": {
        "ghi_chu_v1": "Điều khoản sửa đổi, bổ sung",
        "ngay_het_hieu_luc": "",
        "van_ban_sua_doi": "Luật Mặt trận Tổ quốc Việt Nam, Luật Công đoàn, Luật Thanh niên và Luật Thực hiện dân chủ ở cơ sở số 97/2025/QH15",
        "noi_dung_v2": """Điều 4. Giải thích từ ngữ
3. Nghiệp đoàn cơ sở là tổ chức cơ sở của Công đoàn Việt Nam, tập hợp những người làm việc không có quan hệ lao động, cùng ngành, nghề hoặc những người lao động đặc thù khác, được công đoàn cấp trên cơ sở công nhận theo quy định của pháp luật và Điều lệ Công đoàn Việt Nam.""",
        "ngay_hieu_luc_v2": "2025-07-01",
        "ghi_chu_v2": "bổ sung mới",
    },

    "50_2024_QH15__D4__K4": {
        "bai_bo": True, 
        "ghi_chu_v1": "Điều khoản bãi bỏ",
        "ngay_het_hieu_luc": "2025-07-01",
    },

    "50_2024_QH15__D8__K1": {
        "ghi_chu_v1": "Điều khoản sửa đổi, bổ sung",
        "ngay_het_hieu_luc": "",
        "van_ban_sua_doi": "Luật Mặt trận Tổ quốc Việt Nam, Luật Công đoàn, Luật Thanh niên và Luật Thực hiện dân chủ ở cơ sở số 97/2025/QH15",
        "noi_dung_v2": """Điều 8. Hệ thống tổ chức của Công đoàn Việt Nam
1. Công đoàn Việt Nam là tổ chức thống nhất gồm các cấp sau đây:
a) Cấp trung ương là Tổng Liên đoàn Lao động Việt Nam;
b) Công đoàn cấp trên cơ sở gồm liên đoàn lao động tỉnh, thành phố (sau đây gọi là liên đoàn lao động cấp tỉnh); công đoàn ngành trung ương; công đoàn tập đoàn kinh tế, công đoàn tổng công ty trực thuộc Tổng Liên đoàn Lao động Việt Nam và công đoàn cấp trên cơ sở đặc thù do cấp có thẩm quyền cho phép thành lập phù hợp với tổ chức Công đoàn;
c) Công đoàn cấp cơ sở gồm công đoàn cơ sở, nghiệp đoàn cơ sở.""",
        "ngay_hieu_luc_v2": "2025-07-01",
        "ghi_chu_v2": "bổ sung mới",
    },

    "50_2024_QH15__D14__K2": {
        "ghi_chu_v1": "Điều khoản sửa đổi, bổ sung",
        "ngay_het_hieu_luc": "",
        "van_ban_sua_doi": "Luật Mặt trận Tổ quốc Việt Nam, Luật Công đoàn, Luật Thanh niên và Luật Thực hiện dân chủ ở cơ sở số 97/2025/QH15",
        "noi_dung_v2": """Điều 14. Tham dự kỳ họp, phiên họp, cuộc họp và hội nghị
2. Chủ tịch liên đoàn lao động cấp tỉnh được mời tham dự kỳ họp, phiên họp, hội nghị của Hội đồng nhân dân, Thường trực Hội đồng nhân dân, Ủy ban nhân dân cùng cấp và cơ quan, tổ chức có liên quan khi bàn các vấn đề liên quan đến quyền, nghĩa vụ của đoàn viên công đoàn, người lao động, tổ chức Công đoàn và phát triển kinh tế - xã hội trên địa bàn.""",
        "ngay_hieu_luc_v2": "2025-07-01",
        "ghi_chu_v2": "bổ sung mới",
    },

    "50_2024_QH15__D14__K3": {
        "ghi_chu_v1": "Điều khoản sửa đổi, bổ sung",
        "ngay_het_hieu_luc": "",
        "van_ban_sua_doi": "Luật Mặt trận Tổ quốc Việt Nam, Luật Công đoàn, Luật Thanh niên và Luật Thực hiện dân chủ ở cơ sở số 97/2025/QH15",
        "noi_dung_v2": """Điều 14. Tham dự kỳ họp, phiên họp, cuộc họp và hội nghị
3. Chủ tịch công đoàn ngành trung ương, công đoàn tập đoàn kinh tế, công đoàn tổng công ty, công đoàn cấp trên cơ sở khác được mời tham dự cuộc họp, hội nghị của cơ quan chuyên môn, cơ quan, tổ chức có liên quan khi bàn các vấn đề liên quan đến quyền, nghĩa vụ của đoàn viên công đoàn, người lao động và tổ chức Công đoàn.""",
        "ngay_hieu_luc_v2": "2025-07-01",
        "ghi_chu_v2": "bổ sung mới",
    },

    "50_2024_QH15__D19__K2": {
        "ghi_chu_v1": "Điều khoản sửa đổi, bổ sung",
        "ngay_het_hieu_luc": "",
        "van_ban_sua_doi": "Luật Mặt trận Tổ quốc Việt Nam, Luật Công đoàn, Luật Thanh niên và Luật Thực hiện dân chủ ở cơ sở số 97/2025/QH15",
        "noi_dung_v2": """Điều 19. Phát triển đoàn viên công đoàn, công đoàn cơ sở, nghiệp đoàn cơ sở
2. Công đoàn cấp trên cơ sở có quyền, trách nhiệm cử cán bộ công đoàn đến doanh nghiệp, hợp tác xã, liên hiệp hợp tác xã, tổ chức, đơn vị để tuyên truyền, vận động, hướng dẫn người lao động gia nhập, thành lập công đoàn cơ sở.""",
        "ngay_hieu_luc_v2": "2025-07-01",
        "ghi_chu_v2": "bổ sung mới",
    },

    "50_2024_QH15__D19__K3": {
        "bai_bo": True, 
        "ghi_chu_v1": "Điều khoản bãi bỏ",
        "ngay_het_hieu_luc": "2025-07-01",
    },    

    "50_2024_QH15__D29__K1": {
        "ghi_chu_v1": "Điều khoản sửa đổi, bổ sung",
        "ngay_het_hieu_luc": "",
        "van_ban_sua_doi": "Luật Mặt trận Tổ quốc Việt Nam, Luật Công đoàn, Luật Thanh niên và Luật Thực hiện dân chủ ở cơ sở số 97/2025/QH15",
        "noi_dung_v2": """Điều 29. Tài chính công đoàn
1. Nguồn tài chính công đoàn bao gồm:
a) Đoàn phí công đoàn do đoàn viên công đoàn đóng theo quy định của Điều lệ Công đoàn Việt Nam;
b) Kinh phí công đoàn do doanh nghiệp, đơn vị sự nghiệp không hưởng 100% lương từ ngân sách nhà nước, hợp tác xã, liên hiệp hợp tác xã và cơ quan, tổ chức, đơn vị khác có sử dụng lao động theo quy định của pháp luật đóng bằng 2% quỹ tiền lương làm căn cứ đóng bảo hiểm xã hội bắt buộc cho người lao động;
c) Ngân sách nhà nước cấp hỗ trợ theo quy định của pháp luật về ngân sách nhà nước;
d) Nguồn thu khác từ hoạt động văn hóa, thể thao, hoạt động kinh tế của Công đoàn; từ đề án, dự án do Nhà nước giao; từ viện trợ, tài trợ hợp pháp của tổ chức, cá nhân trong nước và nước ngoài theo quy định của pháp luật.""",
        "ngay_hieu_luc_v2": "2025-07-01",
        "ghi_chu_v2": "bổ sung mới",
    },

    "50_2024_QH15__D29__K2": {
        "ghi_chu_v1": "Điều khoản sửa đổi, bổ sung",
        "ngay_het_hieu_luc": "",
        "van_ban_sua_doi": "Luật Mặt trận Tổ quốc Việt Nam, Luật Công đoàn, Luật Thanh niên và Luật Thực hiện dân chủ ở cơ sở số 97/2025/QH15",
        "noi_dung_v2": """Điều 29. Tài chính công đoàn
2. Chính phủ quy định phương thức, thời hạn và nguồn đóng kinh phí công đoàn; trường hợp không đóng hoặc chậm đóng kinh phí công đoàn; đơn vị sự nghiệp không hưởng 100% lương từ ngân sách nhà nước quy định tại điểm b khoản 1 Điều này; nội dung ngân sách nhà nước cấp hỗ trợ quy định tại điểm c khoản 1 Điều này.""",
        "ngay_hieu_luc_v2": "2025-07-01",
        "ghi_chu_v2": "bổ sung mới",
    },

    "50_2024_QH15__D32__K2": {
        "ghi_chu_v1": "Điều khoản sửa đổi, bổ sung",
        "ngay_het_hieu_luc": "",
        "van_ban_sua_doi": "Luật Mặt trận Tổ quốc Việt Nam, Luật Công đoàn, Luật Thanh niên và Luật Thực hiện dân chủ ở cơ sở số 97/2025/QH15",
        "noi_dung_v2": """Điều 32. Tài sản công đoàn
2. Việc quản lý, sử dụng, khai thác tài sản công đoàn được thực hiện như sau:
a) Việc quản lý, sử dụng, khai thác tài sản công đoàn tại Tổng Liên đoàn Lao động Việt Nam, công đoàn cấp trên cơ sở, đơn vị sự nghiệp của Công đoàn thực hiện theo quy định của pháp luật về quản lý, sử dụng tài sản công và các quy định khác của pháp luật có liên quan;
b) Việc quản lý, sử dụng, khai thác tài sản công đoàn không thuộc quy định tại điểm a khoản này thực hiện theo quy định của pháp luật có liên quan và quy định của Tổng Liên đoàn Lao động Việt Nam.""",
        "ngay_hieu_luc_v2": "2025-07-01",
        "ghi_chu_v2": "bổ sung mới",
    },

    "84_2025_QH15__D62__K1": {
        "ghi_chu_v1": "Điều khoản bãi bỏ",
        "ngay_het_hieu_luc": "",
        "van_ban_sua_doi": "Luật Mặt trận Tổ quốc Việt Nam, Luật Công đoàn, Luật Thanh niên và Luật Thực hiện dân chủ ở cơ sở số 97/2025/QH15",
        "noi_dung_v2": """Điều 62. Sửa đổi, bổ sung một số điều của luật, nghị quyết của Quốc hội và các văn bản quy phạm pháp luật khác có liên quan đến thanh tra
1. Bãi bỏ các điều, khoản, điểm, cụm từ tại các luật, nghị quyết của Quốc hội sau đây:
a) Bãi bỏ Điều 101 của Luật Giao thông đường thủy nội địa số 23/2004/QH11 đã được sửa đổi, bổ sung một số điều theo Luật số 48/2014/QH13, Luật số 97/2015/QH13, Luật số 35/2018/QH14 và Luật số 44/2019/QH14;
c) Bãi bỏ Điều 7 của Luật Thể dục, thể thao số 77/2006/QH11 đã được sửa đổi, bổ sung một số điều theo Luật số 26/2018/QH14;
d) Bãi bỏ Điều 44 của Luật Đê điều số 79/2006/QH11 đã được sửa đổi, bổ sung một số điều theo Luật số 15/2008/QH12, Luật số 35/2018/QH14, Luật số 60/2020/QH14, Luật số 18/2023/QH15 và Luật số 47/2024/QH15;
đ) Bãi bỏ cụm từ "Thanh tra," tại điểm e khoản 2 Điều 5; bãi bỏ Điều 7 của Luật Tần số vô tuyến điện số 42/2009/QH12 đã được sửa đổi, bổ sung một số điều theo Luật số 09/2022/QH15;
e) Bãi bỏ cụm từ "Thanh tra," tại điểm e khoản 1, điểm d khoản 2 Điều 62, khoản 6 Điều 63, khoản 7 Điều 64; bãi bỏ Điều 66 của Luật An toàn thực phẩm số 55/2010/QH12 đã được sửa đổi, bổ sung một số điều theo Luật số 28/2018/QH14;
g) Bãi bỏ cụm từ ", thanh tra sở, thanh tra huyện, quận, thị xã, thành phố thuộc tỉnh" tại khoản 3 Điều 63 của Luật Khiếu nại số 02/2011/QH13 đã được sửa đổi, bổ sung một số điều theo Luật số 42/2013/QH13;
h) Bãi bỏ Điều 50; cụm từ "Chánh thanh tra Bộ Khoa học và Công nghệ," tại khoản 5 Điều 52; cụm từ "Thanh tra," tại khoản 8 Điều 54 của Luật Đo lường số 04/2011/QH13 đã được sửa đổi, bổ sung một số điều theo Luật số 35/2018/QH14;
i) Bãi bỏ cụm từ "thanh tra," tại khoản 6 Điều 162; bãi bỏ Điều 165 của Luật Xây dựng số 50/2014/QH13 đã được sửa đổi, bổ sung một số điều theo Luật số 03/2016/QH14, Luật số 35/2018/QH14, Luật số 40/2019/QH14, Luật số 62/2020/QH14, Luật số 45/2024/QH15, Luật số 47/2024/QH15, Luật số 55/2024/QH15 và Luật số 61/2024/QH15;
k) Bãi bỏ cụm từ "Thanh tra việc sử dụng ngân sách, việc tuyển dụng, sử dụng, quản lý, thực hiện chế độ chính sách đối với công chức, viên chức, người lao động trong hệ thống tổ chức thi hành án dân sự;" tại điểm e khoản 1 Điều 167 của Luật Thi hành án dân sự số 26/2008/QH12 đã được sửa đổi, bổ sung một số điều theo Luật số 64/2014/QH13, Luật số 23/2018/QH14, Luật số 67/2020/QH14, Luật số 03/2022/QH15, Luật số 31/2024/QH15 và Luật số 43/2024/QH15;
l) Bãi bỏ cụm từ "Thanh tra," tại điểm m khoản 2 Điều 71; bãi bỏ Điều 72 của Luật Giáo dục nghề nghiệp số 74/2014/QH13 đã được sửa đổi, bổ sung một số điều theo Luật số 97/2015/QH13, Luật số 21/2017/QH14 và Luật số 43/2019/QH14;
m) Bãi bỏ Điều 62 của Luật Tín ngưỡng, tôn giáo số 02/2016/QH14;
n) Bãi bỏ cụm từ ", Chánh thanh tra sở, Chánh thanh tra cấp huyện" tại khoản 1 Điều 32 của Luật Tố cáo số 25/2018/QH14 đã được sửa đổi, bổ sung một số điều theo Luật số 59/2020/QH14;
o) Bãi bỏ cụm từ "Thanh tra," tại điểm l khoản 2 Điều 57; bãi bỏ điểm a khoản 1 Điều 59 của Luật Đo đạc và bản đồ số 27/2018/QH14;
p) Bãi bỏ cụm từ "thanh tra," tại khoản 15 Điều 191; bãi bỏ Điều 192 của Luật Nhà ở số 27/2023/QH15 đã được sửa đổi, bổ sung một số điều theo Luật số 43/2024/QH15;
q) Bãi bỏ Điều 82 của Luật Tài nguyên nước số 28/2023/QH15;
r) Bãi bỏ cụm từ "thanh tra," tại điểm a khoản 5 Điều 190, khoản 3 Điều 234 của Luật Đất đai số 31/2024/QH15 đã được sửa đổi, bổ sung một số điều theo Luật số 43/2024/QH15, Luật số 47/2024/QH15 và Luật số 58/2024/QH15;
s) Bãi bỏ cụm từ "thanh tra chuyên ngành về đóng bảo hiểm xã hội, bảo hiểm thất nghiệp, bảo hiểm y tế;" tại khoản 1 Điều 16; cụm từ "Thanh tra chuyên ngành về đóng bảo hiểm xã hội, bảo hiểm thất nghiệp, bảo hiểm y tế." tại khoản 5 Điều 17; cụm từ "thanh tra," tại khoản 5 Điều 136; cụm từ "thanh tra," tại khoản 2, khoản 6 Điều 137 của Luật Bảo hiểm xã hội số 41/2024/QH15;
t) Bãi bỏ cụm từ "thanh tra," tại điểm i khoản 2 Điều 90; bãi bỏ Điều 92 của Luật Di sản văn hóa số 45/2024/QH15;
u) Bãi bỏ khoản 1 và khoản 2 Điều 7 của Nghị quyết số 190/2025/QH15.""",
        "ngay_hieu_luc_v2": "2026-07-01",
        "ghi_chu_v2": "Bãi bỏ điểm b khoản 1 điều 62",
    },  

    "152_2020_NDCP__D3__K3": {
        "ghi_chu_v1": "Điều khoản sửa đổi, bổ sung",
        "ngay_het_hieu_luc": "",
        "van_ban_sua_doi": "Nghị định số 70/2023/NĐ-CP",
        "noi_dung_v2": """Điều 3. Giải thích từ ngữ
3. Chuyên gia là người lao động nước ngoài thuộc một trong các trường hợp sau đây:
a) Tốt nghiệp đại học trở lên hoặc tương đương và có ít nhất 3 năm kinh nghiệm làm việc phù hợp với vị trí công việc mà người lao động nước ngoài dự kiến làm việc tại Việt Nam.
b) Có ít nhất 5 năm kinh nghiệm và có chứng chỉ hành nghề phù hợp với vị trí công việc mà người lao động nước ngoài dự kiến làm việc tại Việt Nam;
c) Trường hợp đặc biệt do Thủ tướng Chính phủ quyết định theo đề nghị của Bộ Lao động - Thương binh và Xã hội.""",
        "ngay_hieu_luc_v2": "2023-09-18",
        "ghi_chu_v2": "bổ sung mới",
    },

    "152_2020_NDCP__D3__K5": {
        "ghi_chu_v1": "Điều khoản sửa đổi, bổ sung",
        "ngay_het_hieu_luc": "",
        "van_ban_sua_doi": "Nghị định số 70/2023/NĐ-CP",
        "noi_dung_v2": """Điều 3. Giải thích từ ngữ
5. Giám đốc điều hành là người thuộc một trong các trường hợp sau đây:
a) Người đứng đầu chi nhánh, văn phòng đại diện hoặc địa điểm kinh doanh của doanh nghiệp.
b) Người đứng đầu và trực tiếp điều hành ít nhất một lĩnh vực của cơ quan, tổ chức, doanh nghiệp và chịu sự chỉ đạo, điều hành trực tiếp của người đứng đầu cơ quan, tổ chức, doanh nghiệp.""",
        "ngay_hieu_luc_v2": "2023-09-18",
        "ghi_chu_v2": "bổ sung mới",
        "diem": "a, b",
    },

    "152_2020_NDCP__D3__K6": {
        "ghi_chu_v1": "Điều khoản sửa đổi, bổ sung",
        "ngay_het_hieu_luc": "",
        "van_ban_sua_doi": "Nghị định số 70/2023/NĐ-CP",
        "noi_dung_v2": """Điều 3. Giải thích từ ngữ
6. Lao động kỹ thuật là người lao động nước ngoài thuộc một trong các trường hợp sau đây:
a) Được đào tạo ít nhất 1 năm và có ít nhất 3 năm kinh nghiệm phù hợp với vị trí công việc mà người lao động nước ngoài dự kiến làm việc tại Việt Nam.
b) Có ít nhất 5 năm kinh nghiệm làm công việc phù hợp với vị trí công việc mà người lao động nước ngoài dự kiến làm việc tại Việt Nam.""",
        "ngay_hieu_luc_v2": "2023-09-18",
        "ghi_chu_v2": "bổ sung mới",
    },

    "152_2020_NDCP__D4__K1": {
        "ghi_chu_v1": "Điều khoản sửa đổi, bổ sung",
        "ngay_het_hieu_luc": "",
        "van_ban_sua_doi": "Nghị định số 70/2023/NĐ-CP",
        "noi_dung_v2": """Điều 4. Sử dụng người lao động nước ngoài
1. Xác định nhu cầu sử dụng người lao động nước ngoài
a) Trước ít nhất 15 ngày kể từ ngày dự kiến sử dụng người lao động nước ngoài, người sử dụng lao động (trừ nhà thầu) có trách nhiệm xác định nhu cầu sử dụng người lao động nước ngoài đối với từng vị trí công việc mà người lao động Việt Nam chưa đáp ứng được và báo cáo giải trình với Bộ Lao động - Thương binh và Xã hội hoặc Sở Lao động - Thương binh và Xã hội nơi người lao động nước ngoài dự kiến làm việc theo Mẫu số 01/PLI Phụ lục I ban hành kèm theo Nghị định này.
Trong quá trình thực hiện nếu thay đổi nhu cầu sử dụng người lao động nước ngoài về vị trí, chức danh công việc, hình thức làm việc, số lượng, địa điểm thì người sử dụng lao động phải báo cáo Bộ Lao động - Thương binh và Xã hội hoặc Sở Lao động - Thương binh và Xã hội theo Mẫu số 02/PLI Phụ lục I ban hành kèm theo Nghị định này trước ít nhất 15 ngày kể từ ngày dự kiến sử dụng người lao động nước ngoài.
b) Trường hợp người lao động nước ngoài quy định tại các khoản 3, 4, 5, 6 và 8 Điều 154 của Bộ luật Lao động và các khoản 1, 2, 4, 5, 7, 8, 9, 10, 11, 12, 13 và 14 Điều 7 Nghị định này thì người sử dụng lao động không phải thực hiện xác định nhu cầu sử dụng người lao động nước ngoài.
c) Kể từ ngày 01 tháng 01 năm 2024, việc thông báo tuyển dụng người lao động Việt Nam vào các vị trí dự kiến tuyển dụng người lao động nước ngoài được thực hiện trên Cổng thông tin điện tử của Bộ Lao động - Thương binh và Xã hội (Cục Việc làm) hoặc Cổng thông tin điện tử của Trung tâm dịch vụ việc làm do Chủ tịch Ủy ban nhân dân tỉnh, thành phố trực thuộc trung ương quyết định thành lập trong thời gian ít nhất 15 ngày kể từ ngày dự kiến báo cáo giải trình với Bộ Lao động - Thương binh và Xã hội hoặc Sở Lao động - Thương binh và Xã hội nơi người lao động nước ngoài dự kiến làm việc. Nội dung thông báo tuyển dụng bao gồm: vị trí và chức danh công việc, mô tả công việc, số lượng, yêu cầu về trình độ, kinh nghiệm, mức lương, thời gian và địa điểm làm việc. Sau khi không tuyển được người lao động Việt Nam vào các vị ví tuyển dụng người lao động nước ngoài, người sử dụng lao động có trách nhiệm xác định nhu cầu sử dụng người lao động nước ngoài theo quy định tại điểm a khoản 1 Điều này.""",
        "ngay_hieu_luc_v2": "2023-09-18",
        "ghi_chu_v2": "bổ sung mới",
        "diem": "a, b, c",
    },

    "152_2020_NDCP__D4__K2": {
        "ghi_chu_v1": "Điều khoản sửa đổi, bổ sung",
        "ngay_het_hieu_luc": "",
        "van_ban_sua_doi": "Nghị định số 70/2023/NĐ-CP",
        "noi_dung_v2": """Điều 4. Sử dụng người lao động nước ngoài
2. Bộ Lao động - Thương binh và Xã hội hoặc Sở Lao động - Thương binh và Xã hội có văn bản chấp thuận hoặc không chấp thuận về việc sử dụng người lao động nước ngoài đối với từng vị trí công việc theo Mẫu số 03/PLI Phụ lục I ban hành kèm theo Nghị định này trong thời hạn 10 ngày làm việc kể từ ngày nhận được báo cáo giải trình hoặc báo cáo giải trình thay đổi nhu cầu sử dụng người lao động nước ngoài.""",
        "ngay_hieu_luc_v2": "2023-09-18",
        "ghi_chu_v2": "bổ sung mới",
    },

    "152_2020_NDCP__D5__K1": {
        "ghi_chu_v1": "Điều khoản sửa đổi, bổ sung",
        "ngay_het_hieu_luc": "",
        "van_ban_sua_doi": "Nghị định số 70/2023/NĐ-CP",
        "noi_dung_v2": """Điều 5. Sử dụng người lao động nước ngoài của nhà thầu
Trước khi tuyển người lao động nước ngoài, nhà thầu có trách nhiệm kê khai số lượng, trình độ, năng lực chuyên môn, kinh nghiệm của người lao động nước ngoài cần tuyển để thực hiện gói thầu tại Việt Nam và đề nghị tuyển người lao động Việt Nam vào các vị trí công việc dự kiến tuyển người lao động nước ngoài với Sở Lao động - Thương binh và Xã hội nơi nhà thầu thực hiện gói thầu theo Mẫu số 04/PLI Phụ lục I ban hành kèm theo Nghị định này.
Trường hợp nhà thầu có nhu cầu điều chỉnh, bổ sung số lao động đã kê khai thì chủ đầu tư phải xác nhận phương án điều chỉnh, bổ sung nhu cầu lao động cần sử dụng của nhà thầu theo Mẫu số 05/PLI Phụ lục I ban hành kèm theo Nghị định này.""",
        "ngay_hieu_luc_v2": "2023-09-18",
        "ghi_chu_v2": "bổ sung mới",
    },

    "152_2020_NDCP__D5__K2": {
        "ghi_chu_v1": "Điều khoản sửa đổi, bổ sung",
        "ngay_het_hieu_luc": "",
        "van_ban_sua_doi": "Nghị định số 70/2023/NĐ-CP",
        "noi_dung_v2": """Điều 5. Sử dụng người lao động nước ngoài của nhà thầu
2. Sở Lao động - Thương binh và Xã hội đề nghị các cơ quan, tổ chức của địa phương giới thiệu, cung ứng người lao động Việt Nam cho nhà thầu hoặc phối hợp với các cơ quan, tổ chức ở địa phương khác để giới thiệu, cung ứng người lao động Việt Nam cho nhà thầu. Trong thời hạn tối đa 02 tháng, kể từ ngày nhận được đề nghị tuyển từ 500 người lao động Việt Nam trở lên và tối đa 01 tháng kể từ ngày nhận được đề nghị tuyển từ 100 đến dưới 500 người lao động Việt Nam và 15 ngày kể từ ngày nhận được đề nghị tuyển dưới 100 người lao động Việt Nam mà không giới thiệu hoặc cung ứng người lao động Việt Nam được cho nhà thầu thì Chủ tịch Ủy ban nhân dân cấp tỉnh xem xét, quyết định việc nhà thầu được tuyển người lao động nước ngoài vào các vị trí công việc không tuyển được người lao động Việt Nam theo Mẫu số 06/PLI Phụ lục I ban hành kèm theo Nghị định này.""",
        "ngay_hieu_luc_v2": "2023-09-18",
        "ghi_chu_v2": "bổ sung mới",
    },

    "152_2020_NDCP__D7__K6": {
        "ghi_chu_v1": "Điều khoản sửa đổi, bổ sung",
        "ngay_het_hieu_luc": "",
        "van_ban_sua_doi": "Nghị định số 70/2023/NĐ-CP",
        "noi_dung_v2": """Điều 7. Trường hợp người lao động nước ngoài không thuộc diện cấp giấy phép lao động
6. Được cơ quan, tổ chức có thẩm quyền của nước ngoài cử sang Việt Nam giảng dạy hoặc làm nhà quản lý, giám đốc điều hành tại cơ sở giáo dục do cơ quan đại diện ngoại giao nước ngoài, tổ chức liên chính phủ đề nghị thành lập tại Việt Nam; các cơ sở, tổ chức được thành lập theo các điều ước quốc tế mà Việt Nam đã ký kết, tham gia.""",
        "ngay_hieu_luc_v2": "2023-09-18",
        "ghi_chu_v2": "bổ sung mới",
    },

    "152_2020_NDCP__D7__K14": {
        "ghi_chu_v1": "Điều khoản sửa đổi, bổ sung",
        "ngay_het_hieu_luc": "",
        "van_ban_sua_doi": "Nghị định số 70/2023/NĐ-CP",
        "noi_dung_v2": """Điều 7. Trường hợp người lao động nước ngoài không thuộc diện cấp giấy phép lao động
14. Được Bộ Giáo dục và Đào tạo xác nhận người lao động nước ngoài vào Việt Nam để thực hiện các công việc sau:
a) Giảng dạy, nghiên cứu;
b) Làm nhà quản lý, giám đốc điều hành, hiệu trưởng, phó hiệu trưởng cơ sở giáo dục do cơ quan đại diện ngoại giao nước ngoài hoặc tổ chức liên chính phủ đề nghị thành lập tại Việt Nam.""",
        "ngay_hieu_luc_v2": "2023-09-18",
        "ghi_chu_v2": "bổ sung mới",
        "diem": "a, b",
    },

    "152_2020_NDCP__D8__K2": {
        "ghi_chu_v1": "Điều khoản sửa đổi, bổ sung",
        "ngay_het_hieu_luc": "",
        "van_ban_sua_doi": "Nghị định số 70/2023/NĐ-CP",
        "noi_dung_v2": """Điều 8. Xác nhận người lao động nước ngoài không thuộc diện cấp giấy phép lao động
2. Người sử dụng lao động đề nghị Bộ Lao động - Thương binh và Xã hội hoặc Sở Lao động - Thương binh và Xã hội nơi người lao động nước ngoài dự kiến làm việc xác nhận người lao động nước ngoài không thuộc diện cấp giấy phép lao động trước ít nhất 10 ngày, kể từ ngày người lao động nước ngoài bắt đầu làm việc.
Trường hợp quy định tại khoản 4 và khoản 6 Điều 154 của Bộ luật Lao động và khoản 1, 2, 8 và 11 Điều 7 Nghị định này thì không phải làm thủ tục xác nhận người lao động nước ngoài không thuộc diện cấp giấy phép lao động nhưng phải báo cáo với Bộ Lao động - Thương binh và Xã hội hoặc Sở Lao động - Thương binh và Xã hội nơi người lao động nước ngoài dự kiến làm việc thông tin: họ và tên, tuổi, quốc tịch, số hộ chiếu, tên người sử dụng lao động nước ngoài, ngày bắt đầu và ngày kết thúc làm việc trước ít nhất 3 ngày làm việc, kể từ ngày người lao động nước ngoài dự kiến bắt đầu làm việc tại Việt Nam.
Thời hạn xác nhận người lao động nước ngoài không thuộc diện cấp giấy phép lao động tối đa là 02 năm và theo thời hạn của một trong các trường hợp quy định tại Điều 10 Nghị định này. Trường hợp cấp lại xác nhận người lao động nước ngoài không thuộc diện cấp giấy phép lao động thì thời hạn tối đa là 02 năm.""",
        "ngay_hieu_luc_v2": "2023-09-18",
        "ghi_chu_v2": "bổ sung mới",
    },

    "152_2020_NDCP__D8__K3": {
        "ghi_chu_v1": "Điều khoản sửa đổi, bổ sung",
        "ngay_het_hieu_luc": "",
        "van_ban_sua_doi": "Nghị định số 70/2023/NĐ-CP",
        "noi_dung_v2": """Điều 8. Xác nhận người lao động nước ngoài không thuộc diện cấp giấy phép lao động
3. Hồ sơ đề nghị xác nhận không thuộc diện cấp giấy phép lao động, bao gồm:
a) Văn bản đề nghị xác nhận người lao động nước ngoài không thuộc diện cấp giấy phép lao động theo Mẫu số 09/PLI Phụ lục I ban hành kèm theo Nghị định này;
b) Giấy chứng nhận sức khỏe hoặc giấy khám sức khỏe theo quy định tại khoản 2 Điều 9 Nghị định này;
c) Văn bản chấp thuận nhu cầu sử dụng người lao động nước ngoài trừ những trường hợp không phải xác định nhu cầu sử dụng người lao động nước ngoài;
d) Bản sao có chứng thực hộ chiếu hoặc bản sao hộ chiếu có xác nhận của người sử dụng lao động còn giá trị theo quy định của pháp luật;
đ) Các giấy tờ để chứng minh người lao động nước ngoài không thuộc diện cấp giấy phép lao động;
e) Các giấy tờ quy định tại điểm b, c và d khoản này là 01 bản gốc hoặc bản sao có chứng thực, nếu của nước ngoài thì phải hợp pháp hóa lãnh sự, dịch ra tiếng Việt và công chứng hoặc chứng thực trừ trường hợp được miễn hợp pháp hóa lãnh sự theo điều ước quốc tế mà nước Cộng hòa xã hội chủ nghĩa Việt Nam và nước ngoài liên quan đều là thành viên hoặc theo nguyên tắc có đi có lại hoặc theo quy định của pháp luật.""",
        "ngay_hieu_luc_v2": "2023-09-18",
        "ghi_chu_v2": "bổ sung mới",
    },

    "152_2020_NDCP__D9__K1": {
        "ghi_chu_v1": "Điều khoản sửa đổi, bổ sung",
        "ngay_het_hieu_luc": "",
        "van_ban_sua_doi": "Nghị định số 70/2023/NĐ-CP",
        "noi_dung_v2": """Điều 9. Hồ sơ đề nghị cấp giấy phép lao động
1. Văn bản đề nghị cấp giấy phép lao động của người sử dụng lao động theo Mẫu số 11/PLI Phụ lục I ban hành kèm theo Nghị định này. Trường hợp người lao động nước ngoài làm việc cho một người sử dụng lao động tại nhiều địa điểm thì trong văn bản đề nghị cấp giấy phép lao động phải liệt kê đầy đủ các địa điểm làm việc.""",
        "ngay_hieu_luc_v2": "2023-09-18",
        "ghi_chu_v2": "bổ sung mới",
    },

    "152_2020_NDCP__D9__K4": {
        "ghi_chu_v1": "Điều khoản sửa đổi, bổ sung",
        "ngay_het_hieu_luc": "",
        "van_ban_sua_doi": "Nghị định số 70/2023/NĐ-CP",
        "noi_dung_v2": """Điều 9. Hồ sơ đề nghị cấp giấy phép lao động
4. Văn bản, giấy tờ chứng minh là nhà quản lý, giám đốc điều hành, chuyên gia, lao động kỹ thuật và một số nghề, công việc được quy định như sau:
a) Giấy tờ chứng minh là nhà quản lý, giám đốc điều hành theo quy định tại khoản 4, 5 Điều 3 Nghị định này bao gồm 3 loại giấy tờ sau:
Điều lệ công ty hoặc quy chế hoạt động của cơ quan, tổ chức, doanh nghiệp;
Giấy chứng nhận đăng ký doanh nghiệp hoặc giấy chứng nhận thành lập hoặc quyết định thành lập hoặc giấy tờ khác có giá trị pháp lý tương đương;
Nghị quyết hoặc Quyết định bổ nhiệm của cơ quan, tổ chức, doanh nghiệp.
b) Giấy tờ chứng minh chuyên gia, lao động kỹ thuật theo quy định tại khoản 3, 6 Điều 3 Nghị định này bao gồm 2 loại giấy tờ sau:
Văn bằng hoặc chứng chỉ hoặc giấy chứng nhận;
Văn bản xác nhận của cơ quan, tổ chức, doanh nghiệp tại nước ngoài về số năm kinh nghiệm của chuyên gia, lao động kỹ thuật hoặc giấy phép lao động đã được cấp hoặc xác nhận không thuộc diện cấp giấy phép lao động đã được cấp.
c) Văn bản chứng minh kinh nghiệm của cầu thủ bóng đá nước ngoài hoặc giấy chứng nhận chuyển nhượng quốc tế (ITC) cấp cho cầu thủ bóng đá nước ngoài hoặc văn bản của Liên đoàn Bóng đá Việt Nam xác nhận đăng ký tạm thời hoặc chính thức cho cầu thủ của câu lạc bộ thuộc Liên đoàn Bóng đá Việt Nam;
d) Giấy phép lái tàu bay do cơ quan có thẩm quyền của Việt Nam cấp hoặc do cơ quan có thẩm quyền của nước ngoài cấp và được cơ quan có thẩm quyền của Việt Nam công nhận đối với phi công nước ngoài hoặc chứng chỉ chuyên môn được phép làm việc trên tàu bay do Bộ Giao thông vận tải cấp cho tiếp viên hàng không;
đ) Giấy chứng nhận trình độ chuyên môn trong lĩnh vực bảo dưỡng tàu bay do cơ quan có thẩm quyền của Việt Nam cấp hoặc do cơ quan có thẩm quyền của nước ngoài cấp và được cơ quan có thẩm quyền của Việt Nam công nhận đối với người lao động nước ngoài làm công việc bảo dưỡng tàu bay;
e) Giấy chứng nhận khả năng chuyên môn hoặc giấy công nhận giấy chứng nhận khả năng chuyên môn do cơ quan có thẩm quyền của Việt Nam cấp cho thuyền viên nước ngoài;
g) Giấy chứng nhận thành tích cao trong lĩnh vực thể thao và được Bộ Văn hóa, Thể thao và Du lịch xác nhận đối với huấn luyện viên thể thao hoặc có tối thiểu một trong các bằng cấp như: bằng B huấn luyện viên bóng đá của Liên đoàn Bóng đá Châu Á (AFC) hoặc bằng huấn luyện viên thủ môn cấp độ 1 của AFC hoặc bằng huấn luyện viên thể lực cấp độ 1 của AFC hoặc bằng huấn luyện viên bóng đá trong nhà (Futsal) cấp độ 1 của AFC hoặc bất kỳ bằng cấp huấn luyện tương đương của nước ngoài được AFC công nhận;
h) Văn bằng do cơ quan có thẩm quyền cấp đáp ứng quy định về trình độ, trình độ chuẩn theo Luật Giáo dục, Luật Giáo dục đại học, Luật Giáo dục nghề nghiệp và Quy chế tổ chức hcạt động của trung tâm ngoại ngữ, tin học do Bộ trưởng Bộ Giáo dục và Đào tạo ban hành.""",
        "ngay_hieu_luc_v2": "2023-09-18",
        "ghi_chu_v2": "Sửa đổi, bổ sung điểm a và điểm b",
    },

    "152_2020_NDCP__D9__K7": {
        "ghi_chu_v1": "Điều khoản sửa đổi, bổ sung",
        "ngay_het_hieu_luc": "",
        "van_ban_sua_doi": "Nghị định số 70/2023/NĐ-CP",
        "noi_dung_v2": """Điều 9. Hồ sơ đề nghị cấp giấy phép lao động
7. Bản sao có chứng thực hộ chiếu hoặc bản sao hộ chiếu có xác nhận của người sử dụng lao động còn giá trị theo quy định của pháp luật.""",
        "ngay_hieu_luc_v2": "2023-09-18",
        "ghi_chu_v2": """Thay thế cụm từ "Bản sao có chứng thực hộ chiếu" bằng cụm từ "Bản sao có chứng thực hộ chiếu hoặc bản sao hộ chiếu có xác nhận của người sử dụng lao động""",
    },

    "152_2020_NDCP__D9__K8": {
        "ghi_chu_v1": "Điều khoản sửa đổi, bổ sung",
        "ngay_het_hieu_luc": "",
        "van_ban_sua_doi": "Nghị định số 70/2023/NĐ-CP",
        "noi_dung_v2": """Điều 9. Hồ sơ đề nghị cấp giấy phép lao động
8. Các giấy tờ liên quan đến người lao động nước ngoài trừ trường hợp người lao động nước ngoài quy định tại điểm a khoản 1 Điều 2 Nghị định này.
a) Đối với người lao động nước ngoài theo quy định tại điểm b khoản 1 Điều 2 Nghị định này phải có văn bản của doanh nghiệp nước ngoài cử sang làm việc tại hiện diện thương mại của doanh nghiệp nước ngoài đó trên lãnh thổ Việt Nam và văn bản chứng minh người lao động nước ngoài đã được doanh nghiệp nước ngoài đó tuyển dụng trước khi làm việc tại Việt Nam ít nhất 12 tháng liên tục;
b) Đối với người lao động nước ngoài theo quy định tại điểm c khoản 1 Điều 2 Nghị định này phải có hợp đồng hoặc thỏa thuận ký kết giữa đối tác phía Việt Nam và phía nước ngoài, trong đó phải có thỏa thuận về việc người lao động nước ngoài làm việc tại Việt Nam;
c) Đối với người lao động nước ngoài theo quy định tại điểm d khoản 1 Điều 2 Nghị định này phải có hợp đồng cung cấp dịch vụ ký kết giữa đối tác phía Việt Nam và phía nước ngoài và văn bản chứng minh người lao động nước ngoài đã làm việc cho doanh nghiệp nước ngoài không có hiện diện thương mại tại Việt Nam được ít nhất 02 năm;
d) Đối với người lao động nước ngoài theo quy định tại điểm đ khoản 1 Điều 2 Nghị định này phải có văn bản của nhà cung cấp dịch vụ cử người lao động nước ngoài vào Việt Nam để đàm phán cung cấp dịch vụ;
đ) Đối với người lao động nước ngoài theo quy định tại điểm e khoản 1 Điều 2 Nghị định này phải có văn bản của cơ quan, tổ chức cử người lao động nước ngoài đến làm việc cho tổ chức phi chính phủ nước ngoài, tổ chức quốc tế tại Việt Nam trừ trường hợp quy định tại điểm a khoản 1 Điều 2 Nghị định này và giấy phép hoạt động của tổ chức phi chính phủ nước ngoài, tổ chức quốc tế tại Việt Nam theo quy định của pháp luật;
e) Đối với người lao động nước ngoài làm việc theo quy định tại điểm i khoản 1 Điều 2 Nghị định này thì phải có văn bản của cơ quan, tổ chức, doanh nghiệp nước ngoài cử người lao động nước ngoài sang làm việc tại Việt Nam và phù hợp với vị trí công việc dự kiến làm việc hoặc giấy tờ chứng minh là nhà quản lý theo quy định tại khoản 4 Điều 3 Nghị định này.""",
        "ngay_hieu_luc_v2": "2023-09-18",
        "ghi_chu_v2": "Sửa đổi, bổ sung tên khoản 8 và điều e ",
    },

    "152_2020_NDCP__D9__K9": {
        "ghi_chu_v1": "Điều khoản bổ sung",
        "ngay_het_hieu_luc": "",
        "van_ban_sua_doi": "Nghị định số 70/2023/NĐ-CP",
        "noi_dung_v2": """Điều 9. Hồ sơ đề nghị cấp giấy phép lao động
9. Hồ sơ đề nghị cấp giấy phép lao động đối với một số trường hợp đặc biệt:
a) Đối với người lao động nước ngoài đã được cấp giấy phép lao động, đang còn hiệu lực mà có nhu cầu làm việc cho người sử dụng lao động khác ở cùng vị trí công việc và cùng chức danh công việc ghi trong giấy phép lao động thì hồ sơ đề nghị cấp giấy phép lao động mới gồm: giấy xác nhận của người sử dụng lao động trước đó về việc người lao động hiện đang làm việc, các giấy tờ quy định tại khoản 1, 5, 6, 7, 8 Điều này và bản sao có chứng thực giấy phép lao động đã được cấp;
b) Đối với người lao động nước ngoài đã được cấp giấy phép lao động và đang còn hiệu lực mà thay đổi vị trí công việc hoặc chức danh công việc hoặc hình thức làm việc ghi trong giấy phép lao động theo quy định của pháp luật nhưng không thay đổi người sử dụng lao động thì hồ sơ đề nghị cấp giấy phép lao động mới gồm các giấy tờ quy định tại khoản 1, 4, 5, 6, 7 và 8 Điều này và giấy phép lao động hoặc bản sao có chứng thực giấy phép lao động đã được cấp.
c) Đối với người lao động nước ngoài là chuyên gia, lao động kỹ thuật đã được cấp giấy phép lao động và đã được gia hạn một lần mà có nhu cầu tiếp tục làm việc với cùng vị trí công việc và chức danh công việc ghi trong giấy phép lao động thì hồ sơ đề nghị cấp giấy phép lao động mới gồm các giấy tờ quy định tại khoản 1, 2, 5, 6, 7, 8 Điều này và bản sao giấy phép lao động đã được cấp.""",
        "ngay_hieu_luc_v2": "2023-09-18",
        "ghi_chu_v2": "Bổ sung điểm c",
        "diem": "a, b, c",
    },

    "152_2020_NDCP__D9__K10": {
        "ghi_chu_v1": "Điều khoản sửa đổi, bổ sung",
        "ngay_het_hieu_luc": "",
        "van_ban_sua_doi": "Nghị định số 70/2023/NĐ-CP",
        "noi_dung_v2": """Điều 9. Hồ sơ đề nghị cấp giấy phép lao động
10. Hợp pháp hóa lãnh sự, chứng thực các giấy tờ:
Các giấy tờ quy định tại các khoản 2, 3, 4, 6 và 8 Điều này là 01 bản gốc hoặc bản sao có chứng thực, nếu của nước ngoài thì phải được hợp pháp hóa lãnh sự, trừ trường hợp được miễn hợp pháp hóa lãnh sự theo điều ước quốc tế mà nước Cộng hòa xã hội chủ nghĩa Việt Nam và nước ngoài liên quan đều là thành viên hoặc theo nguyên tắc có đi có lại hoặc theo quy định của pháp luật; dịch ra tiếng Việt và công chứng hoặc chứng thực theo quy định của pháp luật Việt Nam.""",
        "ngay_hieu_luc_v2": "2023-09-18",
        "ghi_chu_v2": """Thay thế cụm từ "dịch ra tiếng Việt và chứng thực" bằng cụm từ "dịch ra tiếng Việt và công chứng hoặc chứng thực""",
    },

    "152_2020_NDCP__D9__K10": {
        "ghi_chu_v1": "Điều khoản sửa đổi, bổ sung",
        "ngay_het_hieu_luc": "",
        "van_ban_sua_doi": "Nghị định số 70/2023/NĐ-CP",
        "noi_dung_v2": """Điều 9. Hồ sơ đề nghị cấp giấy phép lao động
10. Hợp pháp hóa lãnh sự, chứng thực các giấy tờ:
Các giấy tờ quy định tại các khoản 2, 3, 4, 6 và 8 Điều này là 01 bản gốc hoặc bản sao có chứng thực, nếu của nước ngoài thì phải được hợp pháp hóa lãnh sự, trừ trường hợp được miễn hợp pháp hóa lãnh sự theo điều ước quốc tế mà nước Cộng hòa xã hội chủ nghĩa Việt Nam và nước ngoài liên quan đều là thành viên hoặc theo nguyên tắc có đi có lại hoặc theo quy định của pháp luật; dịch ra tiếng Việt và công chứng hoặc chứng thực theo quy định của pháp luật Việt Nam.""",
        "ngay_hieu_luc_v2": "2023-09-18",
        "ghi_chu_v2": """Thay thế cụm từ "dịch ra tiếng Việt và chứng thực" bằng cụm từ "dịch ra tiếng Việt và công chứng hoặc chứng thực""",
    },

    "152_2020_NDCP__D11__K2": {
        "ghi_chu_v1": "Điều khoản sửa đổi, bổ sung",
        "ngay_het_hieu_luc": "",
        "van_ban_sua_doi": "Nghị định số 70/2023/NĐ-CP",
        "noi_dung_v2": """Điều 11. Trình tự cấp giấy phép lao động
2. Trong thời hạn 05 ngày làm việc, kể từ ngày nhận đủ hồ sơ đề nghị cấp giấy phép lao động, Bộ Lao động - Thương binh và Xã hội hoặc Sở Lao động - Thương binh và Xã hội nơi người lao động nước ngoài dự kiến làm việc thực hiện cấp giấy phép lao động cho người lao động nước ngoài theo Mẫu số 12/PLI Phụ lục I ban hành kèm theo Nghị định này. Trường hợp không cấp giấy phép lao động thì có văn bản trả lời và nêu rõ lý do.
Giấy phép lao động có kích thước khổ A4 (21 cm x 29,7 cm), gồm 2 trang: trang 1 có màu xanh; trang 2 có nền màu trắng, hoa văn màu xanh, ở giữa có hình ngôi sao. Giấy phép lao động được mã số như sau: mã số tỉnh, thành phố trực thuộc trung ương và mà số Bộ Lao động - Thương binh và Xã hội theo Mẫu số 16/PLI Phụ lục I ban hành kèm theo Nghị định này; 2 chữ số cuối của năm cấp giấy phép; loại giấy phép (cấp mới ký hiệu 1; gia hạn ký hiệu 2; cấp lại ký hiệu 3); số thứ tự (từ 000.001).
Trường hợp giấy phép lao động là bản điện tử thì phải phù hợp với quy định của pháp luật liên quan và đáp ứng nội dung theo Mẫu số 12/PLI Phụ lục I ban hành kèm theo Nghị định này.""",
        "ngay_hieu_luc_v2": "2023-09-18",
        "ghi_chu_v2": "Sửa đổi, bổ sung khoản 2 Điều 11",
    },

    "152_2020_NDCP__D12__K3": {
        "ghi_chu_v1": "Điều khoản sửa đổi, bổ sung",
        "ngay_het_hieu_luc": "",
        "van_ban_sua_doi": "Nghị định số 70/2023/NĐ-CP",
        "noi_dung_v2": """Điều 12. Các trường hợp cấp lại giấy phép lao động
3. Thay đổi một trong các nội dung sau: họ và tên, quốc tịch, số hộ chiếu, địa điểm làm việc, đổi tên doanh nghiệp mà không thay đổi mã số doanh nghiệp ghi trong giấy phép lao động còn thời hạn.""",
        "ngay_hieu_luc_v2": "2023-09-18",
        "ghi_chu_v2": "Sửa đổi, bổ sung khoản 2 Điều 11",
    },

    "152_2020_NDCP__D13__K4": {
        "bai_bo": True, 
        "ghi_chu_v1": "Điều khoản bãi bỏ",
        "ngay_het_hieu_luc": "2023-09-18",
    },  

    "152_2020_NDCP__D13__K5": {
        "ghi_chu_v1": "Điều khoản sửa đổi, bổ sung",
        "ngay_het_hieu_luc": "",
        "van_ban_sua_doi": "Nghị định số 70/2023/NĐ-CP",
        "noi_dung_v2": """Điều 13. Hồ sơ đề nghị cấp lại giấy phép lao động
5. Giấy tờ quy định tại khoản 3 Điều này là bản gốc hoặc bản sao có chứng thực trừ trường hợp quy định tại khoản 1 Điều 12 Nghị định này, nếu của nước ngoài thì phải hợp pháp hóa lãnh sự và phải dịch ra tiếng Việt và công chứng hoặc chứng thực trừ trường hợp được miễn hợp pháp hóa lãnh sự theo điều ước quốc tế mà nước Cộng hòa xã hội chủ nghĩa Việt Nam và nước ngoài liên quan đều là thành viên hoặc theo nguyên tắc có đi có lại hoặc theo quy định của pháp luật.""",
        "ngay_hieu_luc_v2": "2023-09-18",
        "ghi_chu_v2": """Thay thế cụm từ "Giấy tờ quy định tại khoản 3 và 4 Điều này" bằng cụm từ "Giấy tờ quy định tại khoản 3 Điều này và Thay thế cụm từ "dịch ra tiếng Việt" bằng cụm từ "dịch ra tiếng Việt và công chứng hoặc chứng thực""""",
    },

    "152_2020_NDCP__D17__K5": {
        "ghi_chu_v1": "Điều khoản sửa đổi, bổ sung",
        "ngay_het_hieu_luc": "",
        "van_ban_sua_doi": "Nghị định số 70/2023/NĐ-CP",
        "noi_dung_v2": """Điều 17. Hồ sơ đề nghị gia hạn giấy phép lao động
5. Bản sao có chứng thực hộ chiếu hoặc bản sao hộ chiếu có xác nhận của người sử dụng lao động còn giá trị theo quy định của pháp luật.""",
        "ngay_hieu_luc_v2": "2023-09-18",
        "ghi_chu_v2": """Thay thế cụm từ "Bản sao có chứng thực hộ chiếu" bằng cụm từ "Bản sao có chứng thực hộ chiếu hoặc bản sao hộ chiếu có xác nhận của người sử dụng lao động""""",
    },

    "152_2020_NDCP__D17__K7": {
        "ghi_chu_v1": "Điều khoản sửa đổi, bổ sung",
        "ngay_het_hieu_luc": "",
        "van_ban_sua_doi": "Nghị định số 70/2023/NĐ-CP",
        "noi_dung_v2": """Điều 17. Hồ sơ đề nghị gia hạn giấy phép lao động
7. Một trong các giấy tờ quy định tại khoản 8 Điều 9 Nghị định này chứng minh người lao động nước ngoài tiếp tục làm việc cho người sử dụng lao động theo nội dung giấy phép lao động đã được cấp trừ trường hợp người lao động nước ngoài làm việc theo quy định tại điểm a khoản 1 Điều 2 Nghị định này.""",
        "ngay_hieu_luc_v2": "2023-09-18",
        "ghi_chu_v2": "Sửa đổi, bổ sung khoản 7 Điều 17",
    },

    "152_2020_NDCP__D17__K8": {
        "ghi_chu_v1": "Điều khoản sửa đổi, bổ sung",
        "ngay_het_hieu_luc": "",
        "van_ban_sua_doi": "Nghị định số 70/2023/NĐ-CP",
        "noi_dung_v2": """Điều 17. Hồ sơ đề nghị gia hạn giấy phép lao động
8. Giấy tờ quy định tại các khoản 3, 4, 6 và 7 Điều này là 01 bản gốc hoặc bản sao có chứng thực, nếu của nước ngoài thì phải hợp pháp hóa lãnh sự và phải dịch ra tiếng Việt và công chứng hoặc chứng thực trừ trường hợp được miễn hợp pháp hóa lãnh sự theo điều ước quốc tế mà nước Cộng hòa xã hội chủ nghĩa Việt Nam và nước ngoài liên quan đều là thành viên hoặc theo nguyên tắc có đi có lại hoặc theo quy định của pháp luật.""",
        "ngay_hieu_luc_v2": "2023-09-18",
        "ghi_chu_v2": """Thay thế cụm từ "dịch ra tiếng Việt" bằng cụm từ "dịch ra tiếng Việt và công chứng hoặc chứng thực""",
    },

    "152_2020_NDCP__D22__K1": {
        "ghi_chu_v1": "Điều khoản sửa đổi, bổ sung",
        "ngay_het_hieu_luc": "",
        "van_ban_sua_doi": "Nghị định số 70/2023/NĐ-CP",
        "noi_dung_v2": """Điều 22. Thẩm quyền tuyển dụng, quản lý người lao động Việt Nam làm việc cho tổ chức, cá nhân nước ngoài
1. Tổ chức có thẩm quyền tuyển dụng, quản lý người lao động Việt Nam làm việc cho tổ chức, cá nhân nước ngoài (sau đây gọi là tổ chức có thẩm quyền tuyển dụng, quản lý người lao động Việt Nam) bao gồm:
a) Tổ chức được Bộ Ngoại giao phân cấp, ủy quyền, giao nhiệm vụ, đặt hàng hoặc đấu thầu;
b) Tổ chức được Ủy ban nhân dân cấp tỉnh phân cấp, uỷ quyền, giao nhiệm vụ, đặt hàng hoặc đấu thầu.""",
        "ngay_hieu_luc_v2": "2023-09-18",
        "ghi_chu_v2": """Sửa đổi, bổ sung điểm b khoản 1 Điều 22""",
    },

    "152_2020_NDCP__D23__K4": {
        "ghi_chu_v1": "Điều khoản sửa đổi, bổ sung",
        "ngay_het_hieu_luc": "",
        "van_ban_sua_doi": "Nghị định số 70/2023/NĐ-CP",
        "noi_dung_v2": """Điều 23. Hồ Sơ đăng ký dự tuyển của người lao động Việt Nam
4. Bản sao có chứng thực văn bằng, chứng chỉ về trình độ chuyên môn kỹ thuật, nghiệp vụ, ngoại ngữ liên quan đến công việc mà người lao động đăng ký dự tuyển. Nếu của nước ngoài thì phải được hợp pháp hóa lãnh sự, trừ trường hợp được miễn hợp pháp hỏa lãnh sự theo điều ước quốc tế mà nước Cộng hòa xã hội chủ nghĩa Việt Nam và nước ngoài liên quan đều là thành viên hoặc theo nguyên tắc có đi có lại hoặc theo quy định của pháp luật; dịch ra tiếng Việt và công chứng hoặc chứng thực theo quy định của pháp luật Việt Nam.""",
        "ngay_hieu_luc_v2": "2023-09-18",
        "ghi_chu_v2": """Thay thế cụm từ "dịch ra tiếng Việt và chứng thực" bằng cụm từ "dịch ra tiếng Việt và công chứng hoặc chứng thực""",
    },

    "152_2020_NDCP__D27__K4": {
        "ghi_chu_v1": "Điều khoản sửa đổi, bổ sung",
        "ngay_het_hieu_luc": "",
        "van_ban_sua_doi": "Nghị định số 70/2023/NĐ-CP",
        "noi_dung_v2": """Điều 27. Trách nhiệm của tổ chức có thẩm quyền tuyển dụng, quản lý người lao động Việt Nam
4. Trước ngày 20 tháng 12 hằng năm hoặc đột xuất khi có yêu cầu, tổ chức có thẩm quyền tuyển dụng, quản lý người lao động Việt Nam báo cáo về tình hình tuyển dụng, quản lý người lao động Việt Nam làm việc cho tổ chức, cá nhân nước ngoài tại Việt Nam theo Mẫu số 03/PLII Phụ lục II ban hành kèm theo Nghị định này. Thời gian chốt số liệu báo cáo hằng năm tính từ ngày 15 tháng 12 năm trước kỳ báo cáo đến ngày 14 tháng 12 của kỳ báo cáo và gửi báo cáo như sau:
a) Tổ chức được Bộ Ngoại giao phân cấp, ủy quyền, giao nhiệm vụ, đặt hàng hoặc đấu thầu thực hiện việc tuyển dụng, quản lý người lao động Việt Nam làm việc cho tổ chức, cá nhân nước ngoài thì báo cáo Bộ Ngoại giao;
b) Tổ chức được Ủy ban nhân dân cấp tỉnh phân cấp, uỷ quyền, giao nhiệm vụ, đặt hàng hoặc đấu thầu thực hiện việc tuyển dụng, quản lý người lao động Việt Nam làm việc cho tổ chức, cá nhân nước ngoài thì báo cáo Sở Lao động - Thương binh và Xã hội.""",
        "ngay_hieu_luc_v2": "2023-09-18",
        "ghi_chu_v2": "Sửa đổi, bổ sung điểm b khoản 4 Điều 27",
    },

    "152_2020_NDCP__D30__K1": {
        "ghi_chu_v1": "Điều khoản sửa đổi, bổ sung",
        "ngay_het_hieu_luc": "",
        "van_ban_sua_doi": "Nghị định số 70/2023/NĐ-CP",
        "noi_dung_v2": """Điều 30. Trách nhiệm thi hành
1. Trách nhiệm của Bộ Lao động - Thương binh và Xã hội:
a) Thực hiện chấp thuận nhu cầu sử dụng người lao động nước ngoài; xác nhận không thuộc diện cấp giấy phép lao động; cấp, cấp lại, gia hạn và thu hồi giấy phép lao động đối với người lao động nước ngoài thuộc một trong các trường hợp sau:
Làm việc cho người sử dụng lao động quy định tại điểm g khoản 2 Điều 2 và người sử dụng lao động quy định tại điểm c, d, e khoản 2 Điều 2 Nghị định này do Chính phủ, Thủ tướng Chính phủ, bộ, cơ quan ngang bộ, cơ quan thuộc Chính phủ cho phép thành lập;
Làm việc cho một người sử dụng lao động tại nhiều tỉnh, thành phố trực thuộc trung ương.
b) Người sử dụng lao động quy định tại điểm a khoản 2 Điều 2 có trụ sở chính tại một tỉnh, thành phố nhưng có văn phòng đại diện hoặc chi nhánh tại tỉnh, thành phố khác và người sử dụng lao động quy định tại điểm d khoản 2 Điều 2 Nghị định này có thể lựa chọn thực hiện việc chấp thuận nhu cầu sử dụng người lao động nước ngoài; xác nhận không thuộc diện cấp giấy phép lao động; cấp, cấp lại, gia hạn và thu hồi giấy phép lao động tại Bộ Lao động - Thương binh và Xã hội;
c) Thực hiện thống nhất quản lý nhà nước về tuyển dụng, quản lý người lao động nước ngoài làm việc tại Việt Nam từ trung ương đến địa phương và quản lý người Việt Nam làm việc cho tổ chức, cá nhân nước ngoài tại Việt Nam.
d) Chủ trì và phối hợp với các bộ, ngành tổ chức giám sát, đánh giá, kiểm tra và thanh tra hằng năm hoặc đột xuất các cơ quan, tổ chức, doanh nghiệp có liên quan về việc thực hiện các quy định của pháp luật về người lao động nước ngoài làm việc tại Việt Nam và người lao động Việt Nam làm việc cho tổ chức, cá nhân nước ngoài tại Việt Nam;
đ) Chủ trì, phối hợp với các bộ, ngành, cơ quan trung ương và địa phương hướng dẫn, tuyên truyền, thu thập thông tin, nghiên cứu, đánh giá hiệu quả triển khai thực hiện Nghị định này;
e) Tổng hợp, báo cáo Thủ tướng Chính phủ về người lao động nước ngoài làm việc tại Việt Nam và người lao động Việt Nam làm việc cho tổ chức, cá nhân nước ngoài khi có yêu cầu;
g) Kiến nghị, xử lý các hành vi vi phạm đối với các cơ quan, tổ chức, cá nhân vi phạm các quy định của Nghị định này.""",
        "ngay_hieu_luc_v2": "2023-09-18",
        "ghi_chu_v2": "Sửa đổi, bổ sung điểm a và c khoản 1 Điều 30",
    },

    "152_2020_NDCP__D30__K3": {
        "ghi_chu_v1": "Điều khoản sửa đổi, bổ sung",
        "ngay_het_hieu_luc": "",
        "van_ban_sua_doi": "Nghị định số 70/2023/NĐ-CP",
        "noi_dung_v2": """Điều 30. Trách nhiệm thi hành
3. Trách nhiệm của Bộ Quốc phòng:
a) Phối hợp với các cơ quan có thẩm quyền quản lý người lao động nước ngoài, người lao động Việt Nam làm việc cho các tổ chức, cá nhân nước ngoài tại Việt Nam thực hiện các quy định của pháp luật về đảm bảo an ninh, trật tự địa bàn các vùng chiến lược, trọng điểm, địa bàn xung yếu về quốc phòng.
b) Chỉ đạo Bộ đội Biên phòng phối hợp với các lực lượng chức năng quản lý, kiểm tra người lao động Việt Nam làm việc cho tổ chức, cá nhân nước ngoài tại Việt Nam và người lao động nước ngoài vào làm việc ở khu vực biên giới, cửa khẩu, hải đảo, vùng biển nhằm bảo vệ vững chắc chủ quyền lãnh thổ, an ninh, biên giới quốc gia của Tổ quốc.""",
        "ngay_hieu_luc_v2": "2023-09-18",
        "ghi_chu_v2": "Sửa đổi, bổ sung khoản 3 Điều 30",
        "diem": "a, b",
    },

    "152_2020_NDCP__D30__K4": {
        "ghi_chu_v1": "Điều khoản sửa đổi, bổ sung",
        "ngay_het_hieu_luc": "",
        "van_ban_sua_doi": "Nghị định số 70/2023/NĐ-CP",
        "noi_dung_v2": """Điều 30. Trách nhiệm thi hành
4. Trách nhiệm của Bộ Công an:
a) Định kỳ hằng tháng cung cấp thông tin về người lao động nước ngoài được cấp thị thực ký hiệu gồm: DN1, DN2, LV1, LV2, LĐ1, LĐ2, ĐT1, ĐT2, ĐT3, ĐT4 vào làm việc cho cơ quan, tổ chức, doanh nghiệp tới Bộ Lao động - Thương binh và Xã hội;
b) Phối hợp với các cơ quan có thẩm quyền quản lý người lao động Việt Nam làm việc cho tổ chức, cá nhân nước ngoài tại Việt Nam và các tổ chức, cá nhân nước ngoài sử dụng người lao động Việt Nam thực hiện các quy định của pháp luật về đảm bảo an ninh, trật tự, an toàn xã hội.""",
        "ngay_hieu_luc_v2": "2023-09-18",
        "ghi_chu_v2": "Sửa đổi, bổ sung điểm a khoản 4 Điều 30",
    },

    "152_2020_NDCP__D30__K5": {
        "ghi_chu_v1": "Điều khoản bãi bỏ",
        "ngay_het_hieu_luc": "",
        "van_ban_sua_doi": "Nghị định số 70/2023/NĐ-CP",
        "noi_dung_v2": """Điều 30. Trách nhiệm thi hành
5. Trách nhiệm của Ủy ban nhân dân tỉnh, thành phố trực thuộc trung ương:
a) Quản lý, hướng dẫn cơ quan, tổ chức tại địa phương thực hiện các quy định của pháp luật về người lao động nước ngoài làm việc tại Việt Nam và người lao động Việt Nam làm việc cho tổ chức, cá nhân nước ngoài tại Việt Nam;
b) Chỉ đạo các cơ quan chức năng ở địa phương tổ chức tuyên truyền, phổ biến pháp luật; kiểm tra, thanh tra và xử lý vi phạm theo quy định của pháp luật về việc tuyển dụng, quản lý người lao động nước ngoài và người lao động Việt Nam Làm việc cho tổ chức, cá nhân nước ngoài tại Việt Nam trên địa bàn;
""",
        "ngay_hieu_luc_v2": "2023-09-18",
        "ghi_chu_v2": "Bãi bỏ điểm c, d, đ khoản 5 điều 30",
        "diem": "a, b",
    },

    "152_2020_NDCP__D30__K6": {
        "ghi_chu_v1": "Điều khoản được sửa đổi, bổ sung và bãi bỏ",
        "ngay_het_hieu_luc": "",
        "van_ban_sua_doi": "Nghị định số 70/2023/NĐ-CP",
        "noi_dung_v2": """Điều 30. Trách nhiệm thi hành
6. Trách nhiệm của Sở Lao động - Thương binh và Xã hội:
a) Thực hiện chấp thuận nhu cầu sử dụng người lao động nước ngoài; xác nhận không thuộc diện cấp giấy phép lao động; cấp, cấp lại, gia hạn và thu hồi giấy phép lao động đối với người lao động nước ngoài thuộc một trong các trường hợp sau:
Làm việc cho người sử dụng lao động quy định tại điểm a, b, h, i, k, l khoản 2 Điều 2 và cơ quan, tổ chức quy định tại điểm c, d, e khoản 2 Điều 2 Nghị định này do Ủy ban nhân dân cấp tỉnh, cơ quan chuyên môn thuộc Ủy ban nhân dân cấp tỉnh, Ủy ban nhân dân cấp huyện thành lập;
Làm việc cho người sử dụng lao động tại nhiều địa điểm trong cùng một tỉnh, thành phố trực thuộc trung ương.
b) Người sử dụng lao động quy định tại điểm a khoản 2 Điều 2 có trụ sở chính tại một tỉnh, thành phố nhưng có văn phòng đại diện hoặc chi nhánh tại tỉnh, thành phố khác và người sử dụng lao động quy định tại điểm d khoản 2 Điều 2 Nghị định này có thể lựa chọn thực hiện việc chấp thuận nhu cầu sử dụng người lao động nước ngoài; xác nhận không thuộc diện cấp giấy phép lao động; cấp, cấp lại, gia hạn và thu hồi giấy phép lao động tại Sở Lao động - Thương binh và Xã hội;
c) Khi nhận hồ sơ đề nghị cấp, cấp lại, gia hạn giấy phép lao động; xác nhận người lao động nước ngoài không thuộc diện cấp giấy phép lao động phải vào sổ theo dõi theo Mẫu số 14/PLI Phụ lục I ban hành kèm theo Nghị định này và có giấy biên nhận trao cho người sử dụng lao động. Trong giấy biên nhận phải ghi rõ ngày, tháng, năm nhận hồ sơ; những giấy tờ có trong hồ sơ và thời hạn trả lời;
d) Trường hợp không xác nhận không thuộc diện cấp giấy phép lao động; không cấp, cấp lại, gia hạn giấy phép lao động thì trả lời bằng văn bản theo Mẫu số 15/PLI Phụ lục I ban hành kèm theo Nghị định này;
đ) Chủ trì, phối hợp với các cơ quan địa phương hướng dẫn, tuyên truyền Nghị định này;
e) Thực hiện quản lý nhà nước về người lao động nước ngoài làm việc tại Việt Nam và tuyển dụng, quản lý người lao động Việt Nam làm việc cho tổ chức, cá nhân nước ngoài thuộc phạm vi quản lý của địa phương;
h) Thanh tra, kiểm tra và giám sát việc thực hiện quy định pháp luật về người lao động nước ngoài làm việc tại Việt Nam và tuyển dụng, quản lý người lao động Việt Nam làm việc cho tổ chức, cá nhân nước ngoài thuộc phạm vi quản lý của địa phương;
i) Trước ngày 30 tháng 12 hằng năm hoặc đột xuất khi có yêu cầu, Sở Lao động - Thương binh và Xã hội báo cáo Bộ Lao động - Thương binh và Xã hội về tình hình tuyển dụng, quản lý người lao động Việt Nam làm việc cho tổ chức, cá nhân nước ngoài thuộc phạm vi quản lý theo Mẫu số 03/PLII Phụ lục II ban hành kèm theo Nghị định này. Thời gian chốt số liệu báo cáo hằng năm thực hiện theo quy định của Chính phủ về chế độ báo cáo của cơ quan hành chính nhà nước.""",
        "ngay_hieu_luc_v2": "2023-09-18",
        "ghi_chu_v2": "Bãi bỏ điểm g khoản 6 điều 30",
        "diem": "a, b, c, d, d, e, h, i",
    },

    "51_2010_QH12__D34": {
        "bai_bo": True, 
        "ghi_chu_v1": "Điều khoản bãi bỏ",
        "ngay_het_hieu_luc": "2014-01-01",
    },
}

# Danh sách các Điều/Khoản/Điểm được BỔ SUNG MỚI HOÀN TOÀN (chưa từng có trong văn bản gốc)
ADDED_PROVISIONS = [
    # Mẫu cấu trúc (bỏ comment dấu # ở đầu dòng để dùng):
    {
        "provision_id": "145_2020_NDCP__D4__K4",
        "van_ban": "Nghị định 145/2020/NĐ-CP (145/2020/NĐ-CP)",
        "doc_code": "145_2020_NDCP",
        "chuong": "Chương II",
        "dieu": "4",
        "tieu_de_dieu": "Báo cáo sử dụng lao động",
        "khoan": "4",
        "diem": "a, b",
"noi_dung": """Điều 4. Báo cáo sử dụng lao động
4. Đối với khu công nghệ cao, việc báo cáo sử dụng lao động thực hiện như sau:
a) Người sử dụng lao động báo cáo tình hình thay đổi lao động đến Sở Lao động - Thương binh và Xã hội và Ban quản lý khu công nghệ cao thông qua Cổng Dịch vụ công Quốc gia. Trường hợp người sử dụng lao động không thể báo cáo tình hình thay đổi lao động thông qua Cổng Dịch vụ công Quốc gia thì gửi báo cáo bằng bản giấy đến Ban quản lý khu công nghệ cao.
Yêu cầu về thời gian và biểu mẫu báo cáo của người sử dụng lao động thực hiện theo quy định tại khoản 2 Điều này.
b) Ban quản lý khu công nghệ cao có trách nhiệm cập nhật đầy đủ thông tin và báo cáo Bộ Lao động - Thương binh và Xã hội, Sở Lao động - Thương binh và Xã hội về tình hình sử dụng lao động trên địa bàn thông qua Cổng Dịch vụ công Quốc gia theo thời gian và biểu mẫu quy định tại khoản 3 Điều này.""",
        "hieu_luc": "con_hieu_luc",
        "ngay_hieu_luc": "2024-03-25",
        "ngay_het_hieu_luc": "",
        "thay_the_boi": "",
        "thay_the_cho": "",
        "van_ban_sua_doi": "",
        "ghi_chu": "Hướng dẫn BLLĐ về điều kiện lao động và quan hệ lao động"
    },

    {
        "provision_id": "145_2020_NDCP__D31__5",
        "van_ban": "Nghị định 145/2020/NĐ-CP (145/2020/NĐ-CP)",
        "doc_code": "145_2020_NDCP",
        "chuong": "Chương IV",
        "dieu": "31",
        "tieu_de_dieu": "Phối hợp quản lý lao động",
        "khoan": "5",
        "diem": "",
        "noi_dung": """Điều 31. Phối hợp quản lý lao động
5. Trường hợp doanh nghiệp cho thuê lại lao động đặt trụ sở chính hoặc có hoạt động cho thuê lại lao động trên địa bàn khu công nghệ cao thì khi gửi các báo cáo theo quy định tại Điều này, doanh nghiệp cho thuê lại lao động đồng thời gửi 01 bản báo cáo cho Ban quản lý khu công nghệ cao.""",
        "hieu_luc": "con_hieu_luc",
        "ngay_hieu_luc": "2024-03-25",
        "ngay_het_hieu_luc": "",
        "thay_the_boi": "",
        "thay_the_cho": "",
        "van_ban_sua_doi": "",
        "ghi_chu": "Hướng dẫn BLLĐ về điều kiện lao động và quan hệ lao động"
    },

    {
        "provision_id": "145_2020_NDCP__D62__4",
        "van_ban": "Nghị định 145/2020/NĐ-CP (145/2020/NĐ-CP)",
        "doc_code": "145_2020_NDCP",
        "chuong": "Chương VII",
        "dieu": "62",
        "tieu_de_dieu": "Thông báo về việc tổ chức làm thêm từ trên 200 giờ đến 300 giờ trong một năm",
        "khoan": "4",
        "diem": "",
        "noi_dung": """Điều 62. Thông báo về việc tổ chức làm thêm từ trên 200 giờ đến 300 giờ trong một năm 
4. Trường hợp người sử dụng lao động đặt trụ sở chính hoặc tổ chức làm thêm từ trên 200 giờ đến 300 giờ trong một năm trên địa bàn khu công nghệ cao thì phải thông báo cho Ban quản lý khu công nghệ cao về việc tổ chức làm thêm theo thời gian và biểu mẫu quy định tại khoản 2 và khoản 3 Điều này.""",
        "hieu_luc": "con_hieu_luc",
        "ngay_hieu_luc": "2024-03-25",
        "ngay_het_hieu_luc": "",
        "thay_the_boi": "",
        "thay_the_cho": "",
        "van_ban_sua_doi": "",
        "ghi_chu": "Hướng dẫn BLLĐ về điều kiện lao động và quan hệ lao động"
    },

    {
        "provision_id": "50_2024_QH15__D31__K7",
        "van_ban": "Luật Công đoàn (50/2024/QH15)",
        "doc_code": "50_2024_QH15",
        "chuong": "Chương IV",
        "dieu": "31",
        "tieu_de_dieu": "Quản lý, sử dụng tài chính công đoàn",
        "khoan": "7",
        "diem": "",
        "noi_dung": """Điều 31. Quản lý, sử dụng tài chính công đoàn
7. Hằng năm, Tổng Liên đoàn Lao động Việt Nam báo cáo Ban Thường trực Ủy ban Trung ương Mặt trận Tổ quốc Việt Nam dự toán và quyết toán tài chính công đoàn của Công đoàn Việt Nam quy định tại các điểm a, b, d khoản 1 Điều 29 và khoản 2 Điều 31 của Luật này.""",
        "hieu_luc": "con_hieu_luc",
        "ngay_hieu_luc": "2025-07-01",
        "ngay_het_hieu_luc": "",
        "thay_the_boi": "",
        "thay_the_cho": "",
        "van_ban_sua_doi": "",
        "ghi_chu": ""
    },    

    {
        "provision_id": "152_2020_NDCP__D6__K3",
        "van_ban": "Nghị định 152/2020/NĐ-CP (152/2020/NĐ-CP)",
        "doc_code": "152_2020_NDCP",
        "chuong": "Chương II",
        "dieu": "6",
        "tieu_de_dieu": "Báo cáo sử dụng người lao động nước ngoài",
        "khoan": "3",
        "diem": "",
        "noi_dung": """Điều 6. Báo cáo sử dụng người lao động nước ngoài
3. Trường hợp người lao động nước ngoài làm việc cho một người sử dụng lao động tại nhiều tỉnh, thành phố trực thuộc trung ương thì trong vòng 3 ngày làm việc kể từ ngày người lao động nước ngoài bắt đầu làm việc, người sử dụng lao động phải báo cáo qua môi trường điện tử về Bộ Lao động - Thương binh và Xã hội và Sở Lao động - Thương binh và Xã hội nơi người lao động nước ngoài đến làm việc theo Mẫu số 17/PLI Phụ lục I ban hành kèm theo Nghị định này.""",
        "hieu_luc": "con_hieu_luc",
        "ngay_hieu_luc": "2023-09-18",
        "ngay_het_hieu_luc": "",
        "thay_the_boi": "",
        "thay_the_cho": "",
        "van_ban_sua_doi": "",
        "ghi_chu": "Lao động nước ngoài làm việc tại Việt Nam"
    },    

    {
        "provision_id": "152_2020_NDCP__D30__K6a",
        "van_ban": "Nghị định 152/2020/NĐ-CP (152/2020/NĐ-CP)",
        "doc_code": "152_2020_NDCP",
        "chuong": "Chương IV",
        "dieu": "30",
        "tieu_de_dieu": "Trách nhiệm thi hành",
        "khoan": "6a",
        "diem": "a, b, c, d",
        "noi_dung": """Điều 30. Trách nhiệm thi hành
6a. Đối với lao động làm việc trong khu công nghiệp, khu kinh tế, Ban quản lý khu công nghiệp, khu kinh tế thực hiện các trách nhiệm sau đây:
a) Cấp, cấp lại, gia hạn, thu hồi Giấy phép lao động và xác nhận người lao động nước ngoài không thuộc diện cấp giấy phép lao động cho người nước ngoài làm việc trong khu công nghiệp, khu kinh tế;
b) Tổ chức thực hiện đăng ký nội quy lao động;
c) Nhận báo cáo về việc kết quả đào tạo, bồi dưỡng nâng cao trình độ kỹ năng nghề hằng năm;
d) Nhận thông báo tổ chức làm thêm từ trên 200 giờ đến 300 giờ trong một năm của doanh nghiệp""",
        "hieu_luc": "con_hieu_luc",
        "ngay_hieu_luc": "2022-07-15",
        "ngay_het_hieu_luc": "",
        "thay_the_boi": "",
        "thay_the_cho": "",
        "van_ban_sua_doi": "",
        "ghi_chu": "Lao động nước ngoài làm việc tại Việt Nam"
    },
]
