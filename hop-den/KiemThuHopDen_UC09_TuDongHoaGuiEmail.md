# USE-CASE 09: TỰ ĐỘNG HÓA GỬI EMAIL TUYỂN DỤNG CHO ỨNG VIÊN

---

## 1. THÔNG TIN CHUNG VỀ BÀI TẬP VÀ USE CASE 09

- **Học phần:** Kiểm thử và Đảm bảo chất lượng phần mềm (CSE462)
- **Đề tài:** Hệ thống Quản lý Tuyển dụng – Trợ lý Tuyển dụng & Sàng lọc Hồ sơ Tự động
- **Giảng viên hướng dẫn:** TS. Nguyễn Thị Phương Dung
- **Nhóm sinh viên thực hiện:** Nhóm 09
- **Sinh viên đảm nhận Use Case:** Phạm Văn Hưng (Mã SV: **2351170598**)
- **Mã Use Case:** `UC_09`
- **Tên Use Case:** Tự động hóa gửi email tuyển dụng cho ứng viên
- **Người tạo:** Phạm Văn Hưng
- **Ngày tạo:** 30/01/2026
- **Tác nhân chính:** Chuyên viên tuyển dụng (HR / Recruiter)
- **Tác nhân phụ:** Mail Server (SMTP / AWS SES / SendGrid)
- **Kích hoạt:** Người dùng tích chọn một hoặc nhiều ứng viên và nhấn nút "Gửi Email" tại mục Danh sách ứng viên.
- **Tiền điều kiện:**
  - Chuyên viên tuyển dụng đã đăng nhập thành công vào hệ thống quản trị.
  - Hồ sơ ứng viên đã có trong CSDL và có địa chỉ Email được xác thực.
  - Cấu hình Mail Server (SMTP) đang hoạt động ổn định.
  - Các mẫu email (Templates) đã được định nghĩa sẵn trong hệ thống.
- **Hậu điều kiện:**
  - Email được gửi thành công đến địa chỉ hòm thư của ứng viên.
  - Nội dung email, người gửi và thời gian gửi được lưu vào Lịch sử hoạt động (Activity Log) của hồ sơ ứng viên.
  - Trạng thái ứng viên tự động chuyển đổi tương ứng (Ví dụ: Từ "Mới" sang "Đã liên hệ" hoặc "Chờ phỏng vấn").
- **Mô tả nghiệp vụ:**
  Cho phép Chuyên viên tuyển dụng nhanh chóng liên hệ với một hoặc nhiều ứng viên thông qua email tuyển dụng chuyên nghiệp (thư mời phỏng vấn, từ chối, gửi offer...). Hệ thống ứng dụng trợ lý AI tự động cá nhân hóa nội dung qua thẻ dữ liệu động (Merge Tags), cung cấp cơ chế soạn thảo thủ công linh hoạt, hỗ trợ đính kèm tài liệu và tự động cập nhật trạng thái vòng tuyển dụng.
- **Tiêu chuẩn học thuật áp dụng:**
  - Giáo trình Kiểm thử và Đảm bảo chất lượng phần mềm (CSE462).
  - Chuẩn kiểm thử quốc tế **ISTQB CTFL 2018 v3.1** (Black-box Test Techniques).
  - Chuẩn quy trình kiểm thử phần mềm **ISO/IEC/IEEE 29119-4**.
  - Tiêu chuẩn mô hình chất lượng phần mềm **ISO/IEC 25010**.

---

## 2. PHÂN TÍCH RÀNG BUỘC TỪNG TRƯỜNG DỮ LIỆU

| Tên trường | Ràng buộc nghiệp vụ và kỹ thuật | Phân vùng hợp lệ và Giá trị đại diện | Phân vùng không hợp lệ và Giá trị đại diện | Các giá trị biên cần kiểm thử |
| :--- | :--- | :--- | :--- | :--- |
| **Số lượng ứng viên chọn** | - Kiểu: `Integer`<br>- Bắt buộc chọn ít nhất 1 ứng viên<br>- Giới hạn tối đa 50 ứng viên một lần gửi | - $N = 1$ (Gửi đơn lẻ)<br>- $2 \le N \le 50$ (Gửi hàng loạt) | - $N = 0$ (Chưa chọn ứng viên - EX_01)<br>- $N > 50$ (Vượt quá giới hạn) | - Biên dưới: $N = 0$ (Lỗi), $N = 1$ (Hợp lệ tối thiểu), $N = 2$ (Hàng loạt)<br>- Biên trên: $N = 49$ (Hợp lệ), $N = 50$ (Hợp lệ tối đa), $N = 51$ (Lỗi vượt biên) |
| **Địa chỉ Email ứng viên** | - Kiểu: `String (Email)`<br>- Bắt buộc phải có để gửi thư<br>- Chuẩn định dạng RFC 5322<br>- Độ dài: $6 \le L \le 100$ ký tự | - `an.nguyen@gmail.com`<br>- `hr@company.com.vn` | - Email rỗng: `""`<br>- Thiếu `@`: `an.nguyen.gmail.com`<br>- Thiếu domain: `an@.com`<br>- Chứa script XSS / SQLi | - Biên độ dài: $L = 5$ ký tự (Lỗi), $L = 6$ ký tự (Hợp lệ tối thiểu), $L = 100$ ký tự (Hợp lệ tối đa), $L = 101$ ký tự (Lỗi) |
| **Mẫu email (Template)** | - Kiểu: `Enum / Dropdown`<br>- Bắt buộc chọn 1 mẫu hoặc chọn Soạn thảo trống | - Mời phỏng vấn<br>- Thư cảm ơn & Từ chối<br>- Thư mời nhận việc (Offer)<br>- Soạn thảo trống (Blank) | - Không chọn mẫu nào (`null`)<br>- Mã template lạ / đã bị xóa khỏi hệ thống | - Không áp dụng giá trị biên (Trường lựa chọn danh mục) |
| **Tiêu đề email (Subject)** | - Kiểu: `String`<br>- Bắt buộc phải có nội dung<br>- Độ dài: $1 \le L \le 200$ ký tự<br>- Chống tấn công CRLF Injection | - `"Thư mời phỏng vấn Vòng 1"`<br>- `"Thông báo kết quả tuyển dụng"` | - Để trống: `""`<br>- Vượt quá 200 ký tự<br>- Chứa ký tự xuống dòng `\r\n` | - Biên dưới: $L = 0$ (Lỗi), $L = 1$ (Hợp lệ tối thiểu)<br>- Biên trên: $L = 199$ (Hợp lệ), $L = 200$ (Hợp lệ tối đa), $L = 201$ (Cắt ngắn/Báo lỗi) |
| **Nội dung email (Body)** | - Kiểu: `HTML / Rich Text`<br>- Bắt buộc không được để trống<br>- Độ dài: $1 \le L \le 10,000$ ký tự<br>- Mã hóa an toàn HTML Entity (chống XSS) | - Nội dung do AI tự sinh<br>- Nội dung soạn tay có định dạng | - Để trống: `""`<br>- Chứa mã độc: `<script>alert(1)</script>` | - Biên dưới: $L = 0$ (Lỗi rỗng), $L = 1$ ký tự (Hợp lệ tối thiểu) |
| **Tệp tin đính kèm** | - Kiểu: `Binary File Blob`<br>- Tùy chọn (Không bắt buộc)<br>- Định dạng cho phép: `.pdf`, `.docx`, `.png`, `.jpg`<br>- Dung lượng: $0 < S \le 10\text{ MB}$ | - Tệp PDF: `Offer_Letter.pdf` (2.5 MB)<br>- Tệp JD: `MoTaCongViec.docx` (1.2 MB) | - Tệp rỗng: `Empty.pdf` (0 Byte)<br>- Quá 10MB: `File_15MB.pdf`<br>- Tệp cấm: `.exe`, `.bat`, `.sh` | - Biên dưới: $S = 0\text{ Byte}$ (Lỗi), $S = 1\text{ Byte}$ (Hợp lệ)<br>- Biên trên: $S = 10,240\text{ KB}$ (Hợp lệ tối đa), $S = 10,241\text{ KB}$ (Lỗi quá dung lượng EX_05) |
| **Thời gian phản hồi SMTP** | - Kiểu: `Duration (Giây)`<br>- Ngưỡng Timeout tối đa: $30.0$ giây | - $0.5\text{s} \le T \le 30.0\text{s}$ (Gửi thành công) | - $T > 30.0\text{s}$ (Timeout EX_03) | - $T = 29.9\text{s}$ (Hợp lệ), $T = 30.0\text{s}$ (Ngưỡng biên), $T = 30.1\text{s}$ (Ngắt kết nối, báo lỗi) |

---

## 3. PHÂN TÍCH QUAN HỆ CHÉO VÀ LOGIC NGHIỆP VỤ

1. **Ràng buộc giữa Trạng thái chọn và Chức năng gửi:**
   - Nút "Gửi Email" chỉ được kích hoạt (enabled) khi $N \ge 1$. Nếu $N = 0$, nút ở trạng thái mờ (disabled) hoặc khi click sẽ bật Toast cảnh báo `EX_01`.
2. **Quy tắc bảo mật danh tính người nhận khi gửi hàng loạt (Bulk Email):**
   - Khi chuyên viên chọn gửi cho $N \ge 2$ ứng viên, hệ thống bắt buộc phải tạo các tác vụ gửi thư riêng biệt (gửi đơn lẻ từng người hoặc dùng trường BCC ngầm). Tuyệt đối không để ứng viên nhìn thấy địa chỉ email của các ứng viên khác trong trường `To:` hoặc `Cc:`.
3. **Quy tắc điền thẻ dữ liệu động (Merge Tags):**
   - Khi chọn Template AI, hệ thống tự động đối chiếu thông tin ứng viên trong DB để thay thế toàn bộ các biến `{{candidate_name}}`, `{{job_title}}`. Nếu trường nào bị khuyết thiếu trong DB (ví dụ không có chức danh), hệ thống hiển thị ô nhập màu vàng trên Form xem trước để chuyên viên điền tay trước khi gửi.
4. **Quy tắc chống spam gửi nhiều lần (Double Click Protection):**
   - Nút "Xác nhận gửi" tự động bị vô hiệu hóa ngay sau cú click đầu tiên, hiển thị biểu tượng quay (*Spinner Loading*) cho đến khi nhận được phản hồi từ Mail Server.

---

## 4. PHÂN TÍCH LUỒNG SỰ KIỆN

### 1. Luồng chính thành công chuẩn (Main Flow)
- **Mục tiêu:** Gửi thành công email tuyển dụng (thư mời phỏng vấn, từ chối, gửi offer...) cho ứng viên bằng mẫu AI chuẩn hóa.
- **Kịch bản thực hiện:**
  1. Chuyên viên đăng nhập hệ thống, truy cập màn hình Danh sách ứng viên trên Dashboard.
  2. Tích chọn ứng viên cần liên hệ và nhấn nút chức năng **"Gửi Email"**.
  3. Hệ thống kiểm tra hợp lệ dữ liệu (đảm bảo $N \ge 1$ và email đúng chuẩn RFC 5322), mở Modal **"Soạn & Gửi Email Tuyển Dụng"**.
  4. Chuyên viên chọn mẫu thư phù hợp (ví dụ: *"Thư mời phỏng vấn Vòng 1"*).
  5. Trợ lý AI tự động trích xuất thông tin ứng viên (Họ tên, Vị trí ứng tuyển) để điền vào các thẻ động và hiển thị Form xem trước hoàn chỉnh trong thời gian $T \le 3\text{s}$.
  6. Chuyên viên rà soát thông tin (bổ sung thời gian, địa điểm, link họp online nếu cần) và nhấn nút **"Xác nhận gửi"**.
  7. Hệ thống chuyển phát email thành công qua Mail Server, hiển thị thông báo toast: *"Gửi email thành công"*, tự động cập nhật trạng thái hồ sơ ứng viên sang *"Chờ phỏng vấn"* (hoặc *"Đã liên hệ"*) và lưu vết đầy đủ vào Lịch sử hoạt động (Activity Log).

### 2. Các luồng thay thế và nhánh rẽ (Alternative Flows)
- **Luồng thay thế 5a (Soạn thảo thủ công từ mẫu trống):**
  1. Tại bước 4, chuyên viên không chọn mẫu có sẵn mà nhấn chọn **"Soạn thảo trống"** (*Blank Template*).
  2. Chuyên viên tự nhập tiêu đề (*Subject*) và nội dung thư bằng trình soạn thảo Rich-Text Editor (in đậm, chèn danh sách gạch đầu dòng).
  3. Nhấn "Xác nhận gửi" $\rightarrow$ Hệ thống chuyển sang Bước 7 để gửi thư bình thường.
- **Luồng thay thế 7a (Đính kèm tệp tin tài liệu):**
  1. Tại Form xem trước, chuyên viên bấm nút "Đính kèm tệp" để thêm Thư mời nhận việc (Offer Letter PDF) hoặc bản mô tả công việc (JD).
  2. Hệ thống kiểm tra dung lượng ($\le 10\text{MB}$) và định dạng tệp tin hợp lệ.
  3. Tệp đính kèm hiển thị tên và dung lượng trên form $\rightarrow$ Tiếp tục bấm "Xác nhận gửi".
- **Luồng thay thế 7b (Xem trước khi gửi hàng loạt):**
  1. Khi tích chọn $N \ge 2$ ứng viên, tại Form xem trước, chuyên viên mở dropdown danh sách người nhận để duyệt qua từng bức thư đã cá nhân hóa tên của từng người trước khi bấm gửi toàn bộ.
- **Luồng nhánh hủy bỏ (Cancel):**
  - Chuyên viên nhấn nút "Hủy bỏ" hoặc biểu tượng đóng (X) $\rightarrow$ Modal đóng lại mượt mà, không có email nào được gửi và trạng thái ứng viên được giữ nguyên.

### 3. Các luồng ngoại lệ và xử lý sự cố (Exception Flows)
- **Ngoại lệ EX_01 (Chưa chọn ứng viên):**
  - Chuyên viên nhấn nút "Gửi Email" khi chưa tích chọn bất kỳ ô checkbox ứng viên nào.
  - Hệ thống không mở modal, hiển thị thông báo Toast cảnh báo: *"Vui lòng chọn ít nhất một ứng viên để thực hiện!"*.
- **Ngoại lệ EX_02 (Email ứng viên không hợp lệ hoặc bị trống):**
  - Hồ sơ ứng viên được chọn chưa có email hoặc email sai cú pháp RFC (thiếu `@`, thiếu domain).
  - Hệ thống cảnh báo đỏ: *"Hồ sơ ứng viên [Tên] chưa có địa chỉ email hợp lệ. Vui lòng cập nhật trước khi gửi!"*.
  - *Nếu gửi hàng loạt:* Hệ thống thông báo số lượng ứng viên lỗi, cho phép chuyên viên chọn: *"Bỏ qua các ứng viên lỗi và tiếp tục gửi cho các ứng viên hợp lệ"* hoặc *"Hủy bỏ"*.
- **Ngoại lệ EX_03 (Lỗi kết nối máy chủ Mail Server / SMTP Timeout):**
  - Máy chủ SMTP bị mất kết nối, sai thông tin xác thực hoặc phản hồi kéo dài quá 30.0 giây.
  - Hệ thống ngắt kết nối an toàn, hiển thị thông báo lỗi: *"Không thể kết nối đến máy chủ Mail Server. Vui lòng kiểm tra lại cấu hình hoặc thử lại sau!"*, bảo lưu nội dung thư đang soạn để người dùng gửi lại.
- **Ngoại lệ EX_04 (Vượt hạn mức gửi thư trong ngày - Quota Limit):**
  - Số lượng email gửi vượt quá giới hạn ngày của dịch vụ email.
  - Hệ thống thông báo: *"Đã vượt hạn mức gửi thư trong ngày (Quota Exceeded). Tiến trình gửi bị tạm dừng!"*.
- **Ngoại lệ EX_05 (Tệp đính kèm không hợp lệ):**
  - Chuyên viên đính kèm tệp rỗng $0\text{ Byte}$, tệp quá $10\text{MB}$ hoặc tệp nguy hiểm (`.exe`, `.bat`).
  - Hệ thống chặn ngay tại tầng Client và hiển thị thông báo: *"Tệp đính kèm không được vượt quá 10MB và không được chứa tệp thực thi độc hại"*.

---

## 5. BẢNG CA KIỂM THỬ CHI TIẾT TỔNG HỢP (38 TEST CASES)

*(Chi tiết toàn bộ 38 ca kiểm thử từ `TC_UC09_001` đến `TC_UC09_038` đã được đặc tả chuẩn hóa trong tệp `use-case/TC_UC09_TuDongHoaGuiEmail.md` và tệp dữ liệu `use-case/TC_UC09_TuDongHoaGuiEmail.csv` đi kèm).*

---

## 6. ĐÁNH GIÁ ĐỘ BAO PHỦ VÀ KẾT LUẬN USE CASE 09

### 1. Ma trận bao phủ các phương pháp kiểm thử hộp đen
- **Phân vùng tương đương (EP):** 18 ca (chiếm 47.4%) – Bao phủ số lượng người nhận, định dạng email, loại template, tệp đính kèm.
- **Phân tích giá trị biên (BVA):** 9 ca (chiếm 23.7%) – Biên số lượng ($0, 1, 2, 50, 51$), biên tiêu đề ($1, 200, 201$), biên tệp ($0\text{B}, 9.9\text{MB}, 10.0\text{MB}, 10.1\text{MB}$) và timeout SMTP ($30.0\text{s}$).
- **Bảng quyết định (Decision Table):** 9 ca (chiếm 23.7%) – Tổ hợp logic gửi thư, chọn template, kết nối SMTP và quyền hạn.
- **Kiểm thử chuyển trạng thái:** 8 ca (chiếm 21.1%) – Đồng bộ trạng thái vòng tuyển dụng và ghi vết Activity Log.
- **Bảo mật và đoán lỗi:** 7 ca (chiếm 18.4%) – Chống Stored XSS, Email Header Injection, chống Spam double click và phân quyền truy cập.

### 2. Kết luận
Bộ tài liệu kiểm thử Use Case 09 được hoàn thiện theo đúng chuẩn mực cao nhất của học phần CSE462, đảm bảo tính khoa học, đầy đủ, khả thi và đồng bộ 100% với các Use Case khác của Nhóm 09.
