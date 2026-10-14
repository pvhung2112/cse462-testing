import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=140, right=140):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def set_table_borders(table, color="CCCCCC"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'  <w:top w:val="single" w:sz="6" w:space="0" w:color="{color}"/>'
        f'  <w:bottom w:val="single" w:sz="6" w:space="0" w:color="{color}"/>'
        f'  <w:left w:val="none"/>'
        f'  <w:right w:val="none"/>'
        f'  <w:insideH w:val="single" w:sz="4" w:space="0" w:color="{color}"/>'
        f'  <w:insideV w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def add_header(doc):
    p_uni = doc.add_paragraph()
    p_uni.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_uni = p_uni.add_run("TRƯỜNG ĐẠI HỌC THỦY LỢI - KHOA CÔNG NGHỆ THÔNG TIN\n")
    r_uni.bold = True
    r_uni.font.size = Pt(12)
    r_uni.font.color.rgb = RGBColor(0x1F, 0x4E, 0x79)
    
    r_sub = p_uni.add_run("BỘ MÔN CÔNG NGHỆ PHẦN MỀM | HỌC PHẦN: CSE462 - KIỂM THỬ VÀ ĐẢM BẢO CHẤT LƯỢNG PHẦN MỀM\n")
    r_sub.font.size = Pt(10)
    r_sub.font.italic = True
    r_sub.font.color.rgb = RGBColor(0x55, 0x55, 0x55)

    p_div = doc.add_paragraph()
    p_div.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_div = p_div.add_run("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    r_div.font.color.rgb = RGBColor(0x1F, 0x4E, 0x79)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_title = p_title.add_run("BÁO CÁO KIỂM THỬ HỘP TRẮNG (WHITE-BOX TESTING)\nUSE-CASE 10: LÊN LỊCH PHỎNG VẤN ỨNG VIÊN")
    r_title.bold = True
    r_title.font.size = Pt(16)
    r_title.font.color.rgb = RGBColor(0xC0, 0x00, 0x00)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_sub2 = p_sub.add_run("Đề tài: Hệ thống Quản lý Tuyển dụng – Trợ lý Tuyển dụng & Sàng lọc Hồ sơ Tự động\nĐối tượng: Lớp ScheduleInterviewUseCase (Phương thức execute)\n")
    r_sub2.font.size = Pt(10.5)
    r_sub2.font.color.rgb = RGBColor(0x2E, 0x75, 0xB6)

def add_info_table(doc):
    table = doc.add_table(rows=6, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table)
    data = [
        ("Học phần & Mã môn:", "Kiểm thử và Đảm bảo chất lượng phần mềm (CSE462)"),
        ("Giảng viên hướng dẫn:", "TS. Nguyễn Thị Phương Dung"),
        ("Sinh viên thực hiện:", "Phạm Văn Hưng (Mã SV: 2351170598) - Nhóm 09"),
        ("Mã & Tên Use Case:", "UC_10 - Lên lịch phỏng vấn ứng viên (Candidate Interview Scheduling)"),
        ("Tệp mã nguồn đối tượng:", "src/modules/client/application/use-cases/interview/schedule-interview.use-case.ts"),
        ("Phạm vi & Chuẩn áp dụng:", "Kiểm thử dòng điều khiển (CFG), Cyclomatic V(G), Độ đo C1, C2, C3 (ISTQB CTFL)")
    ]
    for i, (k, v) in enumerate(data):
        row = table.rows[i]
        c0, c1 = row.cells[0], row.cells[1]
        c0.width, c1.width = Inches(2.2), Inches(4.7)
        set_cell_background(c0, "F2F4F7")
        set_cell_margins(c0)
        set_cell_margins(c1)
        p0, p1 = c0.paragraphs[0], c1.paragraphs[0]
        r0 = p0.add_run(k)
        r0.bold = True
        r0.font.size = Pt(10)
        r1 = p1.add_run(v)
        r1.font.size = Pt(10)
    doc.add_paragraph()

def add_code_section(doc):
    h = doc.add_heading("1. MÃ NGUỒN ĐÁNH SỐ DÒNG (TARGET UNDER TEST)", level=1)
    h.style.font.color.rgb = RGBColor(0x1F, 0x4E, 0x79)
    
    code_text = (
        "1:  export class ScheduleInterviewUseCase {\n"
        "2:    constructor(\n"
        "3:      private readonly candidateRepo: ICandidateReadRepo & ICandidateWriteRepo,\n"
        "4:      private readonly jobRepo: IJobReadRepo,\n"
        "5:      private readonly aiAnalysisRepo: IAnalysisReadRepo,\n"
        "6:      private readonly interviewScheduleRepo: IInterviewScheduleRepository,\n"
        "7:      private readonly geminiSvc: IAIService,\n"
        "8:      private readonly mailSvc: IMailService,\n"
        "9:    ) { }\n"
        "10: \n"
        "11:   async execute(input: ScheduleInterviewInput): Promise<ScheduleInterviewResult> {\n"
        "12:     if (!input.candidateID || !input.jobID) {\n"
        "13:       throw new Error('Mã ứng viên và mã công việc không được để trống.');\n"
        "14:     }\n"
        "15: \n"
        "16:     const candidate = await this.candidateRepo.getById(input.candidateID);\n"
        "17:     if (!candidate) throw new Error('Không tìm thấy thông tin ứng viên.');\n"
        "18:     if (!candidate.getPersonal().email) throw new Error('Ứng viên chưa có email để gửi thư mời.');\n"
        "19: \n"
        "20:     const job = await this.jobRepo.getById(input.jobID);\n"
        "21:     if (!job) throw new Error('Không tìm thấy thông tin công việc (Job).');\n"
        "22: \n"
        "23:     const analysis = await this.aiAnalysisRepo.getAnalysisByCandidateId(input.candidateID);\n"
        "24:     if (!analysis) throw new Error('Ứng viên chưa được AI phân tích. Vui lòng chạy phân tích trước khi đặt lịch.');\n"
        "25: \n"
        "26:     const isOverlap = await this.interviewScheduleRepo.checkOverlap(input.userId, input.time, input.durationMinutes);\n"
        "27:     if (isOverlap) {\n"
        "28:       throw new Error('Khung giờ này đã có lịch khác. Vui lòng chọn giờ lại');\n"
        "29:     }\n"
        "30: \n"
        "31:     const created = await this.interviewScheduleRepo.createSchedule({\n"
        "32:       time: input.time,\n"
        "33:       address: input.address,\n"
        "34:       candidateId: input.candidateID,\n"
        "35:       userId: input.userId,\n"
        "36:       status: 'scheduled',\n"
        "37:     });\n"
        "38:     if (!created) throw new Error('Không thể tạo lịch phỏng vấn.');\n"
        "39: \n"
        "40:     const invite = buildInterviewCalendarInvite({\n"
        "41:       uid: `${created.getId()}@hr-agent`,\n"
        "42:       startTime: input.time,\n"
        "43:       durationMinutes: input.durationMinutes,\n"
        "44:       summary: `Phỏng vấn - ${job.getTitle()}`,\n"
        "45:       description: [\n"
        "46:         `Phỏng vấn vị trí: ${job.getTitle()}`,\n"
        "47:         `Ghi chú: ${input.notes ?? ''}`,\n"
        "48:       ].filter(Boolean).join('\\n'),\n"
        "49:       location: input.address,\n"
        "50:       organizerEmail: process.env.MAIL_USER,\n"
        "51:       attendeeEmail: candidate.getPersonal().email,\n"
        "52:     });\n"
        "53: \n"
        "54:     const emailPayload = {\n"
        "55:       candidate: {\n"
        "56:         fullName: candidate.getPersonal().fullName,\n"
        "57:         email: candidate.getPersonal().email,\n"
        "58:       },\n"
        "59:       job: job.getDetailJob(),\n"
        "60:       schedule: {\n"
        "61:         time: input.time.toISOString(),\n"
        "62:         durationMinutes: input.durationMinutes,\n"
        "63:         address: input.address,\n"
        "64:       },\n"
        "65:       aiAnalysis: analysis,\n"
        "66:       notes: input.notes ?? '',\n"
        "67:     };\n"
        "68: \n"
        "69:     let subject = `Thư mời phỏng vấn - ${job.getTitle()}`;\n"
        "70:     let html = `<p>Xin chào ${candidate.getPersonal().fullName || 'bạn'},</p><p>Chúng tôi xin mời bạn tham gia phỏng vấn cho vị trí <b>${job.getTitle()}</b>.</p>`;\n"
        "71: \n"
        "72:     try {\n"
        "73:       const generated = await this.geminiSvc.generateInterviewEmail(emailPayload);\n"
        "74:       if (generated?.subject?.trim()) {\n"
        "75:         subject = generated.subject.trim();\n"
        "76:       }\n"
        "77:       if (generated?.html) {\n"
        "78:         html = generated.html;\n"
        "79:       }\n"
        "80:     } catch (e) {\n"
        "81:       console.warn('Không thể tạo email bằng AI, sử dụng mẫu mặc định.');\n"
        "82:     }\n"
        "83: \n"
        "84:     const emailSent = await this.mailSvc.sendEmail(candidate.getPersonal().email, subject, html, [\n"
        "85:       {\n"
        "86:         filename: invite.filename,\n"
        "87:         content: invite.content,\n"
        "88:         contentType: invite.contentType,\n"
        "89:       },\n"
        "90:     ]);\n"
        "91: \n"
        "92:     await this.candidateRepo.updateStatus(input.candidateID, { status: CandidateStatus.INTERVIEW });\n"
        "93: \n"
        "94:     return { schedule: created.getDetail(), emailSent };\n"
        "95:   }\n"
        "96: }"
    )

    p = doc.add_paragraph()
    r = p.add_run(code_text)
    r.font.name = 'Consolas'
    r.font.size = Pt(8.5)
    r.font.color.rgb = RGBColor(0x33, 0x33, 0x33)
    p_format = p.paragraph_format
    p_format.space_before = Pt(4)
    p_format.space_after = Pt(8)
    p_format.line_spacing = 1.15
    doc.add_paragraph()

def add_blocks_table(doc):
    h = doc.add_heading("2. BẢNG PHÂN CHIA KHỐI LỆNH CƠ BẢN (BASIC BLOCKS)", level=1)
    h.style.font.color.rgb = RGBColor(0x1F, 0x4E, 0x79)

    blocks = [
        ("Start", "Dòng 11", "Bắt đầu hàm execute(input: ScheduleInterviewInput)", "Điểm vào (Entry Point)"),
        ("Node 1", "Dòng 12–14", "Tiếp nhận tham số, kiểm tra if (!input.candidateID || !input.jobID)", "Điểm quyết định (Decision)"),
        ("Node 2", "Dòng 13", "throw new Error('Mã ứng viên và mã công việc không được để trống.')", "Điểm thoát (Exit Exception 1)"),
        ("Node 3", "Dòng 16–17", "candidate = await candidateRepo.getById(candidateID), if (!candidate)", "Điểm quyết định (Decision)"),
        ("Node 4", "Dòng 17", "throw new Error('Không tìm thấy thông tin ứng viên.')", "Điểm thoát (Exit Exception 2)"),
        ("Node 5", "Dòng 18", "Kiểm tra if (!candidate.getPersonal().email)", "Điểm quyết định (Decision)"),
        ("Node 6", "Dòng 18", "throw new Error('Ứng viên chưa có email để gửi thư mời.')", "Điểm thoát (Exit Exception 3)"),
        ("Node 7", "Dòng 20–21", "job = await jobRepo.getById(input.jobID), if (!job)", "Điểm quyết định (Decision)"),
        ("Node 8", "Dòng 21", "throw new Error('Không tìm thấy thông tin công việc (Job).')", "Điểm thoát (Exit Exception 4)"),
        ("Node 9", "Dòng 23–24", "analysis = await aiAnalysisRepo.getAnalysisByCandidateId(), if (!analysis)", "Điểm quyết định (Decision)"),
        ("Node 10", "Dòng 24", "throw new Error('Ứng viên chưa được AI phân tích. Vui lòng chạy phân tích...')", "Điểm thoát (Exit Exception 5)"),
        ("Node 11", "Dòng 26–29", "isOverlap = await interviewScheduleRepo.checkOverlap(), if (isOverlap)", "Điểm quyết định (Decision)"),
        ("Node 12", "Dòng 28", "throw new Error('Khung giờ này đã có lịch khác. Vui lòng chọn giờ lại')", "Điểm thoát (Exit Exception 6)"),
        ("Node 13", "Dòng 31–38", "created = await interviewScheduleRepo.createSchedule(), if (!created)", "Điểm quyết định (Decision)"),
        ("Node 14", "Dòng 38", "throw new Error('Không thể tạo lịch phỏng vấn.')", "Điểm thoát (Exit Exception 7)"),
        ("Node 15", "Dòng 40–70", "buildCalendarInvite, chuẩn bị emailPayload, gán template mặc định subject, html", "Khối xử lý (Process)"),
        ("Node 16a", "Dòng 72–79", "Khối Try: gọi AI geminiSvc.generateInterviewEmail(), cập nhật subject, html", "Khối xử lý (Process)"),
        ("Node 16b", "Dòng 80–82", "Khối Catch: bắt lỗi AI, ghi log console.warn(), giữ nguyên mẫu email mặc định", "Xử lý ngoại lệ (Exception Handle)"),
        ("Node 17", "Dòng 84–92", "Gửi email invite: mailSvc.sendEmail(), candidateRepo.updateStatus('INTERVIEW')", "Khối xử lý (Process)"),
        ("Node 18", "Dòng 94", "return { schedule: created.getDetail(), emailSent }", "Điểm thoát (Exit Success)")
    ]

    table = doc.add_table(rows=len(blocks) + 1, cols=4)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table)

    headers = ["Khối (Node)", "Dòng mã nguồn", "Nội dung thực thi chi tiết", "Loại đỉnh (Node Type)"]
    widths = [Inches(0.9), Inches(1.1), Inches(3.4), Inches(1.5)]

    for j, h_text in enumerate(headers):
        cell = table.rows[0].cells[j]
        cell.width = widths[j]
        set_cell_background(cell, "1F4E79")
        set_cell_margins(cell)
        p = cell.paragraphs[0]
        r = p.add_run(h_text)
        r.bold = True
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    for i, row_data in enumerate(blocks):
        row = table.rows[i + 1]
        for j, val in enumerate(row_data):
            cell = row.cells[j]
            cell.width = widths[j]
            if i % 2 == 1:
                set_cell_background(cell, "F9FAFB")
            set_cell_margins(cell)
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.size = Pt(8.5)
            if j == 0:
                r.bold = True

    doc.add_paragraph()

def add_cfg_section(doc, base_dir):
    h = doc.add_heading("3. XÂY DỰNG ĐỒ THỊ DÒNG ĐIỀU KHIỂN (CFG) CHO HÀM THEO C1, C2, C3", level=1)
    h.style.font.color.rgb = RGBColor(0x1F, 0x4E, 0x79)

    h_sub1 = doc.add_heading("3.1. Đồ thị dòng điều khiển ứng với độ đo C1 và C2", level=2)
    h_sub1.style.font.color.rgb = RGBColor(0x2E, 0x75, 0xB6)

    img_c1_c2 = os.path.join(base_dir, "cfg_uc10_c1_c2.png")
    if os.path.exists(img_c1_c2):
        doc.add_paragraph().alignment = WD_ALIGN_PARAGRAPH.CENTER
        p = doc.paragraphs[-1]
        p.add_run().add_picture(img_c1_c2, width=Inches(5.0))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_cap = p_cap.add_run("Hình 1: Đồ thị dòng điều khiển (CFG) phương thức execute ứng với độ đo C1 và C2")
        r_cap.font.size = Pt(9)
        r_cap.font.italic = True
        r_cap.font.color.rgb = RGBColor(0x55, 0x55, 0x55)

    doc.add_paragraph()

    h_sub2 = doc.add_heading("3.2. Đồ thị dòng điều khiển ứng với độ đo C3 (Phân rã điều kiện con)", level=2)
    h_sub2.style.font.color.rgb = RGBColor(0x2E, 0x75, 0xB6)

    p_c3_desc = doc.add_paragraph()
    r_desc = p_c3_desc.add_run(
        "Theo lý thuyết kiểm thử độ đo C3, biểu thức điều kiện phức hợp tại Node 1 (!input.candidateID || !input.jobID) được phân rã thành hai nút quyết định con tương ứng:\n"
        "• Node 1a: Kiểm tra !input.candidateID. Nếu True -> ngắt mạch (Short-circuit) nhảy thẳng sang Node 2.\n"
        "• Node 1b: Kiểm tra !input.jobID. Nếu True -> ném lỗi Node 2. Nếu False -> đi tiếp sang Node 3."
    )
    r_desc.font.size = Pt(9.5)

    img_c3 = os.path.join(base_dir, "cfg_uc10_c3.png")
    if os.path.exists(img_c3):
        doc.add_paragraph().alignment = WD_ALIGN_PARAGRAPH.CENTER
        p = doc.paragraphs[-1]
        p.add_run().add_picture(img_c3, width=Inches(5.0))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_cap = p_cap.add_run("Hình 2: Đồ thị dòng điều khiển phân rã điều kiện con (CFG C3) tại Node 1")
        r_cap.font.size = Pt(9)
        r_cap.font.italic = True
        r_cap.font.color.rgb = RGBColor(0x55, 0x55, 0x55)

    doc.add_paragraph()

def add_mccabe_section(doc):
    h = doc.add_heading("4. TÍNH ĐỘ PHỨC TẠP CYCLOMATIC (MCCABE)", level=1)
    h.style.font.color.rgb = RGBColor(0x1F, 0x4E, 0x79)

    p = doc.add_paragraph()
    r = p.add_run(
        "Độ phức tạp Cyclomatic V(G) được tính toán độc lập theo 3 phương pháp chuẩn Thomas McCabe:\n\n"
        "• Phương pháp 1 (Dựa trên số cung E và số đỉnh N):\n"
        "   Công thức: V(G) = E - N + 2P\n"
        "   - Số đỉnh N = 21 (Đỉnh Start + 19 Node nghiệp vụ 1..18 gồm 16a, 16b + Đỉnh End kết thúc chung).\n"
        "   - Số cung E = 28 cung (gồm 20 cung liên kết nội bộ giữa các Node + 8 cung kết nối các điểm thoát về đỉnh End).\n"
        "   - Số thành phần liên thông P = 1.\n"
        "   ==> V(G) = E - N + 2P = 28 - 21 + 2(1) = 9\n\n"
        "• Phương pháp 2 (Dựa trên số điểm quyết định vị từ Pn):\n"
        "   Công thức: V(G) = Pn + 1\n"
        "   - 8 điểm quyết định nhị phân: Node 1 (!candidateID || !jobID), Node 3 (!candidate), Node 5 (!personal?.email),\n"
        "     Node 7 (!job), Node 9 (!analysis), Node 11 (isOverlap), Node 13 (!created) và Khối Try/Catch AI (Node 16a/16b).\n"
        "   ==> Pn = 8  ==>  V(G) = 8 + 1 = 9\n\n"
        "• Phương pháp 3 (Dựa trên số miền mặt phẳng khép kín R):\n"
        "   Công thức: V(G) = R\n"
        "   - Đồ thị phẳng có 8 miền mặt phẳng khép kín (R1 đến R8) + 1 miền vô hạn bao quanh ngoài (R9).\n"
        "   ==> V(G) = R = 9\n\n"
        "==> KẾT LUẬN: Cả 3 phương pháp đều tính ra độ phức tạp Cyclomatic V(G) = 9. Do đó cần tối thiểu 9 đường dẫn cơ sở (Basis Paths) để bao phủ toàn bộ đồ thị dòng điều khiển."
    )
    r.font.size = Pt(10)
    doc.add_paragraph()

def add_section_5(doc):
    h = doc.add_heading("5. SINH CÁC ĐƯỜNG ĐI VÀ CA KIỂM THỬ THEO C1, C2, C3", level=1)
    h.style.font.color.rgb = RGBColor(0x1F, 0x4E, 0x79)

    # 5.1 C1 Table
    h_c1 = doc.add_heading("5.1. Sinh đường đi và ca kiểm thử ứng với độ đo C1", level=2)
    h_c1.style.font.color.rgb = RGBColor(0x2E, 0x75, 0xB6)

    p_c1 = doc.add_paragraph()
    r_c1 = p_c1.add_run("Mục tiêu độ đo C1 (Statement Coverage): Đảm bảo tất cả các khối lệnh (Node) trong đồ thị dòng điều khiển (từ Start, Node 1 đến Node 18, bao gồm cả Node 16a và 16b) đều được thực thi ít nhất một lần qua tập các ca kiểm thử.")
    r_c1.font.size = Pt(9.5)
    r_c1.font.italic = True

    c1_data = [
        ("C1_01", "Start -> 1 -> 2", "candidateID: '', jobID: 'JOB_01', time: valid", "Ném lỗi: 'Mã ứng viên và mã công việc không được để trống.'", "Đạt", "Phủ Node 1, 2"),
        ("C1_02", "Start -> 1 -> 3 -> 4", "candidateID: 'CAN_UNKNOWN', candidateRepo trả về null", "Ném lỗi: 'Không tìm thấy thông tin ứng viên.'", "Đạt", "Phủ Node 3, 4"),
        ("C1_03", "Start -> 1 -> 3 -> 5 -> 6", "candidateID: 'CAN_02', personal.email = undefined", "Ném lỗi: 'Ứng viên chưa có email để gửi thư mời.'", "Đạt", "Phủ Node 5, 6"),
        ("C1_04", "Start..->5->7->8", "candidateID: 'CAN_03', jobID: 'JOB_UNKNOWN', jobRepo trả về null", "Ném lỗi: 'Không tìm thấy thông tin công việc (Job).'", "Đạt", "Phủ Node 7, 8"),
        ("C1_05", "Start..->7->9->10", "candidateID: 'CAN_04', aiAnalysisRepo trả về null", "Ném lỗi: 'Ứng viên chưa được AI phân tích. Vui lòng chạy phân tích...'", "Đạt", "Phủ Node 9, 10"),
        ("C1_06", "Start..->9->11->12", "candidateID: 'CAN_05', checkOverlap trả về true (Trùng lịch)", "Ném lỗi: 'Khung giờ này đã có lịch khác. Vui lòng chọn giờ lại'", "Đạt", "Phủ Node 11, 12"),
        ("C1_07", "Start..->11->13->14", "candidateID: 'CAN_06', createSchedule trả về null (Lỗi DB)", "Ném lỗi: 'Không thể tạo lịch phỏng vấn.'", "Đạt", "Phủ Node 13, 14"),
        ("C1_08", "Start..->13->15->16a->17->18", "candidateID: 'CAN_07', Happy Path, AI và Mail gửi thành công", "Tạo lịch OK, gửi mail thành công, cập nhật trạng thái INTERVIEW", "Đạt", "Phủ Node 15, 16a, 17, 18"),
        ("C1_09", "Start..->15->16a->16b->17->18", "candidateID: 'CAN_08', geminiSvc ném Exception (AI timeout/quota)", "Bắt tại 16b, ghi log cảnh báo, gửi thư theo template mặc định", "Đạt", "Phủ Node 16b")
    ]

    table_c1 = doc.add_table(rows=len(c1_data) + 1, cols=6)
    table_c1.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table_c1)

    c1_headers = ["TT", "Đường đi theo Node", "Dữ liệu đầu vào (Input)", "Đầu ra mong đợi", "Đầu ra thực tế", "Ghi chú"]
    c1_widths = [Inches(0.6), Inches(1.8), Inches(1.6), Inches(1.5), Inches(0.6), Inches(0.8)]

    for j, h_text in enumerate(c1_headers):
        cell = table_c1.rows[0].cells[j]
        cell.width = c1_widths[j]
        set_cell_background(cell, "2E75B6")
        set_cell_margins(cell)
        p = cell.paragraphs[0]
        r = p.add_run(h_text)
        r.bold = True
        r.font.size = Pt(9)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    for i, row_data in enumerate(c1_data):
        row = table_c1.rows[i + 1]
        for j, val in enumerate(row_data):
            cell = row.cells[j]
            cell.width = c1_widths[j]
            if i % 2 == 1:
                set_cell_background(cell, "F2F4F7")
            set_cell_margins(cell)
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.size = Pt(8)
            if j == 0 or j == 4:
                r.bold = True

    doc.add_paragraph()

    # 5.2 C2 Branch Matrix
    h_c2 = doc.add_heading("5.2. Sinh đường đi và ca kiểm thử ứng với độ đo C2", level=2)
    h_c2.style.font.color.rgb = RGBColor(0x2E, 0x75, 0xB6)

    p_c2 = doc.add_paragraph()
    r_c2 = p_c2.add_run("Mục tiêu độ đo C2 (Branch Coverage): Mỗi điểm quyết định trong đồ thị đều được duyệt qua cả hai nhánh Đúng (True) và Sai (False) ít nhất một lần.\n\nBảng ma trận điều kiện rẽ nhánh C2:")
    r_c2.font.size = Pt(9.5)
    r_c2.font.italic = True

    c2_data = [
        ("Node 1", "!input.candidateID || !input.jobID", "Sang Node 2", "Sang Node 3", "C1_01", "C1_02"),
        ("Node 3", "!candidate", "Sang Node 4", "Sang Node 5", "C1_02", "C1_03"),
        ("Node 5", "!candidate.getPersonal().email", "Sang Node 6", "Sang Node 7", "C1_03", "C1_04"),
        ("Node 7", "!job", "Sang Node 8", "Sang Node 9", "C1_04", "C1_05"),
        ("Node 9", "!analysis", "Sang Node 10", "Sang Node 11", "C1_05", "C1_06"),
        ("Node 11", "isOverlap (Kiểm tra trùng lịch hẹn)", "Sang Node 12", "Sang Node 13", "C1_06", "C1_07"),
        ("Node 13", "!created (Lưu CSDL lịch phỏng vấn)", "Sang Node 14", "Sang Node 15", "C1_07", "C1_08"),
        ("Khối AI Try/Catch", "Khối geminiSvc.generateInterviewEmail()", "Sang Node 17 (OK)", "Sang Node 16b (Lỗi AI)", "C1_08", "C1_09")
    ]

    table_c2 = doc.add_table(rows=len(c2_data) + 1, cols=6)
    table_c2.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table_c2)

    c2_headers = ["Điểm quyết định", "Biểu thức điều kiện tương ứng", "Nhánh Đúng (True)", "Nhánh Sai (False)", "Ca kiểm thử Đúng", "Ca kiểm thử Sai"]
    c2_widths = [Inches(1.1), Inches(2.2), Inches(1.0), Inches(1.0), Inches(0.8), Inches(0.8)]

    for j, h_text in enumerate(c2_headers):
        cell = table_c2.rows[0].cells[j]
        cell.width = c2_widths[j]
        set_cell_background(cell, "1F4E79")
        set_cell_margins(cell)
        p = cell.paragraphs[0]
        r = p.add_run(h_text)
        r.bold = True
        r.font.size = Pt(8.5)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    for i, row_data in enumerate(c2_data):
        row = table_c2.rows[i + 1]
        for j, val in enumerate(row_data):
            cell = row.cells[j]
            cell.width = c2_widths[j]
            if i % 2 == 1:
                set_cell_background(cell, "F9FAFB")
            set_cell_margins(cell)
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.size = Pt(8)
            if j == 0 or j >= 4:
                r.bold = True

    doc.add_paragraph()

    # 5.3 C3 Section
    h_c3 = doc.add_heading("5.3. Sinh đường đi và ca kiểm thử ứng với độ đo C3 (Phủ điều kiện con)", level=2)
    h_c3.style.font.color.rgb = RGBColor(0x2E, 0x75, 0xB6)

    p_c3_intro = doc.add_paragraph()
    r_c3_intro = p_c3_intro.add_run(
        "Mục tiêu độ đo C3 (Condition Coverage): Các điều kiện con trong biểu thức phức hợp tại Node 1 (!input.candidateID || !input.jobID) đều nhận cả hai giá trị Chân và Giả ít nhất một lần.\n\n"
        "Bảng ma trận điều kiện con C3:"
    )
    r_c3_intro.font.size = Pt(9.5)
    r_c3_intro.font.italic = True

    c3_matrix = [
        ("Node 1", "!input.candidateID (A)", "True (candidateID = '')", "TC_C3_01", "Sang Node 2", "True (Short-circuit)"),
        ("Node 1", "!input.candidateID (A)", "False (candidateID = 'CAN_01')", "TC_C3_02", "Đánh giá tiếp B", "-"),
        ("Node 1", "!input.jobID (B)", "True (jobID = '')", "TC_C3_02", "Sang Node 2", "True (Lỗi thiếu jobID)"),
        ("Node 1", "!input.jobID (B)", "False (jobID = 'JOB_01')", "TC_C3_03", "Sang Node 3", "False (Hợp lệ, đi tiếp)")
    ]

    table_c3_m = doc.add_table(rows=len(c3_matrix) + 1, cols=6)
    table_c3_m.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table_c3_m)

    c3_m_headers = ["Điểm quyết định", "Điều kiện con tương ứng", "Giá trị kiểm tra", "Ca kiểm thử tương ứng", "Nhánh thực thi", "Kết quả biểu thức"]
    c3_m_widths = [Inches(1.0), Inches(1.8), Inches(1.3), Inches(0.9), Inches(1.0), Inches(0.9)]

    for j, h_text in enumerate(c3_m_headers):
        cell = table_c3_m.rows[0].cells[j]
        cell.width = c3_m_widths[j]
        set_cell_background(cell, "2E75B6")
        set_cell_margins(cell)
        p = cell.paragraphs[0]
        r = p.add_run(h_text)
        r.bold = True
        r.font.size = Pt(8.5)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    for i, row_data in enumerate(c3_matrix):
        row = table_c3_m.rows[i + 1]
        for j, val in enumerate(row_data):
            cell = row.cells[j]
            cell.width = c3_m_widths[j]
            if i % 2 == 1:
                set_cell_background(cell, "F2F4F7")
            set_cell_margins(cell)
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.size = Pt(8)
            if j == 0 or j == 3:
                r.bold = True

    doc.add_paragraph()

    p_c3_detail = doc.add_paragraph()
    r_c3_detail = p_c3_detail.add_run("Bảng danh sách ca kiểm thử chi tiết cho độ đo C3:")
    r_c3_detail.font.size = Pt(9.5)
    r_c3_detail.bold = True

    c3_cases = [
        ("TC_C3_01", "Kiểm tra lỗi khi thiếu candidateID", "A = True", "candidateID = '', jobID = 'JOB_01', time = valid", "Ném lỗi: 'Mã ứng viên và mã công việc không được để trống.'"),
        ("TC_C3_02", "Kiểm tra lỗi khi thiếu jobID", "A = False, B = True", "candidateID = 'CAN_01', jobID = '', time = valid", "Ném lỗi: 'Mã ứng viên và mã công việc không được để trống.'"),
        ("TC_C3_03", "Cả hai tham số candidateID và jobID hợp lệ", "A = False, B = False", "candidateID = 'CAN_01', jobID = 'JOB_01', time = valid", "Đi tiếp sang Node 3 (Truy vấn ứng viên trong DB)")
    ]

    table_c3_c = doc.add_table(rows=len(c3_cases) + 1, cols=5)
    table_c3_c.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table_c3_c)

    c3_c_headers = ["TT", "Tên ca kiểm thử", "Điều kiện con kích hoạt", "Dữ liệu đầu vào (Input)", "Đầu ra mong đợi"]
    c3_c_widths = [Inches(0.8), Inches(1.9), Inches(1.1), Inches(1.6), Inches(1.5)]

    for j, h_text in enumerate(c3_c_headers):
        cell = table_c3_c.rows[0].cells[j]
        cell.width = c3_c_widths[j]
        set_cell_background(cell, "1F4E79")
        set_cell_margins(cell)
        p = cell.paragraphs[0]
        r = p.add_run(h_text)
        r.bold = True
        r.font.size = Pt(8.5)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    for i, row_data in enumerate(c3_cases):
        row = table_c3_c.rows[i + 1]
        for j, val in enumerate(row_data):
            cell = row.cells[j]
            cell.width = c3_c_widths[j]
            if i % 2 == 1:
                set_cell_background(cell, "F9FAFB")
            set_cell_margins(cell)
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.size = Pt(8)
            if j == 0:
                r.bold = True

    doc.add_paragraph()

def add_conclusion(doc):
    h = doc.add_heading("6. ĐÁNH GIÁ ĐỘ ĐO BAO PHỦ VÀ KẾT LUẬN", level=1)
    h.style.font.color.rgb = RGBColor(0x1F, 0x4E, 0x79)
    p = doc.add_paragraph()
    r = p.add_run(
        "1. Độ bao phủ câu lệnh (C1 - Statement Coverage): Đạt 100% (20/20 khối lệnh cơ bản bao gồm đỉnh Start, 18 Node nghiệp vụ trong đó có cả đỉnh Try 16a và Catch 16b được thực thi đầy đủ qua 9 ca kiểm thử C1_01 - C1_09).\n"
        "2. Độ bao phủ nhánh quyết định (C2 - Branch Coverage): Đạt 100% (tất cả 8 điểm quyết định rẽ nhánh logic và khối ngoại lệ AI đều được kích hoạt đầy đủ 2 nhánh True và False).\n"
        "3. Độ bao phủ điều kiện (C3 - Condition Coverage): Đạt 100% cho biểu thức logic phức hợp tại Node 1 (!candidateID || !jobID) theo đúng nguyên lý ngắt mạch Short-circuit evaluation.\n\n"
        "Bộ ca kiểm thử hộp trắng của Use Case 10 được thiết kế bao phủ toàn diện cả các trường hợp lỗi dữ liệu đầu vào rỗng, lỗi ứng viên không tồn tại, lỗi thiếu email, lỗi trùng lịch hẹn phỏng vấn (Conflict Prevention), lỗi kết nối cơ sở dữ liệu và khả năng chịu lỗi (Fault-tolerance) khi dịch vụ AI gặp sự cố."
    )
    r.font.size = Pt(10)

def main():
    base_dir = r'd:\test\cse462-testing\hop-trang'
    doc = docx.Document()
    for s in doc.sections:
        s.top_margin = Inches(0.8)
        s.bottom_margin = Inches(0.8)
        s.left_margin = Inches(0.8)
        s.right_margin = Inches(0.8)

    add_header(doc)
    add_info_table(doc)
    add_code_section(doc)
    add_blocks_table(doc)
    add_cfg_section(doc, base_dir)
    add_mccabe_section(doc)
    add_section_5(doc)
    add_conclusion(doc)

    out_path = os.path.join(base_dir, "KiemThuHopTrang_UC10_LenLichPhongVan.docx")
    doc.save(out_path)
    print(f"Document saved to: {out_path}")

if __name__ == '__main__':
    main()
