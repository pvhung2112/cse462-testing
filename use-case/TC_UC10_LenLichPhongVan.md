# TÀI LIỆU ĐẶC TẢ CA KIỂM THỬ
## HỌC PHẦN: KIỂM THỬ VÀ ĐẢM BẢO CHẤT LƯỢNG PHẦN MỀM (CSE462)
### BÀI TẬP LỚN / USE CASE: UC_10 - LÊN LỊCH PHỎNG VẤN ỨNG VIÊN

---

## 📌 PHẦN 1: THÔNG TIN CHUNG

- **Mã Use Case:** `UC_10`
- **Tên Use Case:** Lên lịch phỏng vấn ứng viên *(Candidate Interview Scheduling & Google Calendar Integration)*
- **Người đảm nhận / Tạo:** Phạm Văn Hưng
- **Ngày tạo:** 30/01/2026
- **Tác nhân chính (Actor):** Chuyên viên tuyển dụng (HR / Recruiter)
- **Hệ thống liên kết (Secondary Actor):** Dịch vụ Google Calendar API, Google Meet API, Mail Server (Gửi file `.ics`)
- **Mục tiêu Use Case:** 
  1. Hỗ trợ HR nhanh chóng thiết lập cuộc hẹn phỏng vấn (Online qua Google Meet hoặc Offline tại văn phòng công ty).
  2. Tự động kiểm tra lịch bận (*Free/Busy query*) của HR và Người phỏng vấn chuyên môn (Tech Lead) để chống trùng lịch hẹn (*Conflict Prevention*).
  3. Tự động đồng bộ và tạo sự kiện trực tiếp trên Google Calendar, sinh link Google Meet và gửi thư mời họp kèm file lịch `.ics` cho ứng viên.
  4. Cập nhật trạng thái vòng tuyển dụng sang *"Chờ phỏng vấn"* và ghi vết kiểm toán (*Activity Log*).
- **Tiêu chuẩn học thuật áp dụng:**
  - Giáo trình Kiểm thử và Đảm bảo chất lượng phần mềm (**CSE462**) – Trường Đại học Thủy Lợi.
  - Chuẩn kiểm thử quốc tế **ISTQB CTFL 2018 v3.1** (Black-box Test Techniques).
  - Chuẩn quy trình kiểm thử phần mềm **ISO/IEC/IEEE 29119-4**.
  - Tiêu chuẩn mô hình chất lượng **ISO/IEC 25010** (Functionality, Reliability, Usability, Security).

---

## 🎯 PHẦN 2: PHÂN TÍCH CƠ SỞ KIỂM THỬ VÀ LUỒNG SỰ KIỆN

### 1. Phân rã luồng sự kiện chi tiết
- **Luồng chính (Main Flow - Lên lịch Online qua Google Meet):**
  1. Chuyên viên đăng nhập hệ thống, truy cập màn hình Chi tiết hồ sơ ứng viên.
  2. Chuyên viên nhấn nút chức năng **"Lên lịch phỏng vấn"**.
  3. Hệ thống kiểm tra kết nối Google Calendar và hiển thị Form **"Tạo lịch phỏng vấn"** với các thông tin tự động điền sẵn: Tiêu đề (`Phỏng vấn [Vị trí] - [Tên UV]`), Khung giờ trống gợi ý, Email người tham gia và Link Google Meet tự sinh.
  4. Chuyên viên rà soát lại thông tin (thời lượng họp: 30p, 45p, 60p).
  5. Chuyên viên nhấn nút **"Tạo lịch & Gửi lời mời"**.
  6. Hệ thống gọi Google Calendar API tạo sự kiện thành công, tự động gửi thư mời họp kèm link Meet đến ứng viên và HR.
  7. Hệ thống thông báo thành công, đổi trạng thái ứng viên sang **"Chờ phỏng vấn"** và lưu Activity Log.
- **Các luồng thay thế (Alternative Flows):**
  - `A1` *(Phỏng vấn trực tiếp tại văn phòng):* Chọn hình thức "Trực tiếp" $\rightarrow$ Chọn phòng họp nội bộ trong danh mục $\rightarrow$ Tiếp tục bước 5.
  - `A2` *(Chọn khung giờ thủ công):* Bấm vào biểu đồ lịch chọn ngày/giờ khác phù hợp $\rightarrow$ Tiếp tục bước 5.
  - `A3` *(Thêm Tech Lead vào phỏng vấn):* Nhập thêm email Trưởng nhóm kỹ thuật $\rightarrow$ Gửi thư mời cho cả 2 người $\rightarrow$ Tiếp tục bước 5.
  - `A4` *(Hủy bỏ thao tác):* Bấm "Hủy bỏ" hoặc (X) $\rightarrow$ Đóng form, không tạo sự kiện trên Calendar.
- **Các luồng ngoại lệ (Exceptions):**
  - `EX_01` *(Trùng lịch hẹn):* Khung giờ chọn đã có sự kiện họp khác $\rightarrow$ Báo lỗi trùng lịch và yêu cầu chọn giờ khác.
  - `EX_02` *(Thời gian hẹn không hợp lệ):* Chọn giờ quá khứ hoặc thời lượng $< 15$ phút $\rightarrow$ Báo lỗi.
  - `EX_03` *(Lỗi Google API / Hết hạn Token):* Token OAuth2 hết hạn hoặc API delay $> 10\text{s}$ $\rightarrow$ Báo lỗi kết nối máy chủ Google.
  - `EX_04` *(Thiếu email ứng viên):* Hồ sơ ứng viên chưa có email $\rightarrow$ Báo lỗi yêu cầu cập nhật email trước khi lên lịch.

---

## 🔬 PHẦN 3: BẢNG QUYẾT ĐỊNH CHO TỔ HỢP LOGIC NGHIỆP VỤ

| Mã | Thành phần kiểm tra | $R_1$ | $R_2$ | $R_3$ | $R_4$ | $R_5$ | $R_6$ | $R_7$ | $R_8$ |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **C1** | Ứng viên có Email hợp lệ trong CSDL | Có | Có | Có | Có | Có | **Không** | Có | Có |
| **C2** | Khung giờ chọn không bị trùng lịch bận (Conflict) | Có | Có | **Không** | Có | Có | - | Có | Có |
| **C3** | Thời gian hẹn ở tương lai và thời lượng $\ge 15$p | Có | Có | - | **Không** | Có | - | Có | Có |
| **C4** | Hình thức phỏng vấn được chọn | Online | Offline | - | - | Online | - | Offline | Online |
| **C5** | Đã chọn phòng họp hợp lệ (khi Offline) | - | Có | - | - | - | - | **Không** | - |
| **C6** | Kết nối Google Calendar API ổn định, Token còn hạn | Có | Có | - | - | **Không** | - | Có | Có |
| **C7** | Thao tác của chuyên viên tuyển dụng | Tạo lịch | Tạo lịch | Tạo lịch | Tạo lịch | Tạo lịch | Tạo lịch | Tạo lịch | **Hủy bỏ** |
| **A1** | Tạo thành công sự kiện trên Google Calendar | **X** | **X** | - | - | - | - | - | - |
| **A2** | Tự động sinh link Google Meet | **X** | - | - | - | - | - | - | - |
| **A3** | Gửi email thư mời họp (Invite) kèm file .ics cho UV | **X** | **X** | - | - | - | - | - | - |
| **A4** | Cập nhật trạng thái hồ sơ sang "Chờ phỏng vấn" | **X** | **X** | - | - | - | - | - | - |
| **A5** | Báo lỗi ngoại lệ EX_01: Trùng lịch hẹn phỏng vấn | - | - | **X** | - | - | - | - | - |
| **A6** | Báo lỗi ngoại lệ EX_02: Thời gian hẹn không hợp lệ | - | - | - | **X** | - | - | - | - |
| **A7** | Báo lỗi ngoại lệ EX_03: Mất kết nối / Hết hạn Token Google | - | - | - | - | **X** | - | - | - |
| **A8** | Báo lỗi ngoại lệ EX_04: Ứng viên chưa có Email | - | - | - | - | - | **X** | - | - |
| **A9** | Báo lỗi: Vui lòng chọn phòng họp cho phỏng vấn trực tiếp | - | - | - | - | - | - | **X** | - |
| **A10**| Đóng form tạo lịch, không tạo sự kiện, giữ nguyên hồ sơ | - | - | - | - | - | - | - | **X** |

---

## 📋 PHẦN 4: MA TRẬN PHÂN BỔ 38 CA KIỂM THỬ (TRACEABILITY MATRIX)

| Phân nhóm kiểm thử | Dải Test Case ID | Số lượng | Kỹ thuật & Trọng tâm |
| :--- | :---: | :---: | :--- |
| **Nhóm 1: Luồng chính - Phỏng vấn Online qua Meet** | `TC_UC10_001` $\rightarrow$ `TC_UC10_005` | 5 ca | Use Case Flow, Tự sinh link Google Meet, Gợi ý giờ AI. |
| **Nhóm 2: Luồng thay thế - Phỏng vấn Offline & Thêm Lead** | `TC_UC10_006` $\rightarrow$ `TC_UC10_010` | 5 ca | Chọn phòng họp văn phòng (A1), Chọn giờ thủ công (A2), Mời Tech Lead (A3), Hủy (A4). |
| **Nhóm 3: Kiểm tra Giá trị biên thời gian (BVA & EP)** | `TC_UC10_011` $\rightarrow$ `TC_UC10_018` | 8 ca | Biên thời gian hiện tại, quá khứ, tương lai gần (+15p), thời lượng min 15p, max 240p, tiêu đề 200 ký tự. |
| **Nhóm 4: Kiểm tra xử lý ngoại lệ (Exceptions)** | `TC_UC10_019` $\rightarrow$ `TC_UC10_026` | 8 ca | Trùng lịch HR/Lead (EX_01), Thời gian sai (EX_02), Hết hạn Token OAuth2/Timeout (EX_03), Thiếu email (EX_04). |
| **Nhóm 5: Đồng bộ trạng thái & Lịch sử hoạt động** | `TC_UC10_027` $\rightarrow$ `TC_UC10_031` | 5 ca | Cập nhật trạng thái "Chờ phỏng vấn", Activity Log, gửi file `.ics`, đồng bộ Outlook/Google, Dời lịch (Reschedule). |
| **Nhóm 6: Bảo mật, Tương tranh & Phân quyền** | `TC_UC10_032` $\rightarrow$ `TC_UC10_038` | 7 ca | Chống XSS ghi chú, chống Double Click nút Tạo lịch, rel=noopener noreferrer, phân quyền Viewer, Hủy lịch hẹn. |
| **TỔNG CỘNG** | `TC_UC10_001` $\rightarrow$ `TC_UC10_038` | **38 ca** | **Bao phủ 100% chuẩn học phần CSE462** |
