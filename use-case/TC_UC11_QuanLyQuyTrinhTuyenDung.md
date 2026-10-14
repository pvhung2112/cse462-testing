# TÀI LIỆU ĐẶC TẢ CA KIỂM THỬ
## HỌC PHẦN: KIỂM THỬ VÀ ĐẢM BẢO CHẤT LƯỢNG PHẦN MỀM (CSE462)
### BÀI TẬP LỚN / USE CASE: UC_11 - QUẢN LÝ QUY TRÌNH TUYỂN DỤNG (RECRUITMENT PIPELINE MANAGEMENT)

---

## 📌 PHẦN 1: THÔNG TIN CHUNG

- **Mã Use Case:** `UC_11`
- **Tên Use Case:** Quản lý quy trình tuyển dụng *(Recruitment Pipeline Management)*
- **Người đảm nhận / Tạo:** Phạm Văn Hưng
- **Ngày tạo:** 30/01/2026
- **Tác nhân chính (Actor):** Chuyên viên tuyển dụng (HR / Recruiter) - Có đầy đủ thẩm quyền vận hành và quản lý dữ liệu trong hệ thống tuyển dụng chuyên dụng.
- **Tác nhân phụ / Hệ thống liên kết:** Cơ sở dữ liệu tuyển dụng (Database Server), Hệ thống tự động gửi Email thông báo (Mail Server / Event Bus).
- **Mục tiêu Use Case:** 
  1. Cho phép Chuyên viên tuyển dụng theo dõi tiến độ và quản lý trạng thái của ứng viên qua từng giai đoạn trong phễu tuyển dụng (*Recruitment Funnel*).
  2. Thực thi nghiêm ngặt các quy tắc chuyển đổi trạng thái logic nghiệp vụ (*State Machine Rules*), đảm bảo tính tuần tự, ngăn ngừa hành vi nhảy cóc quy trình hoặc chuyển ngược trạng thái bất hợp lệ.
  3. Kiểm tra tính toàn vẹn và các điều kiện tiên quyết của từng giai đoạn (ví dụ: vòng phỏng vấn phải có kết quả đánh giá mới được chuyển sang giai đoạn Đề nghị nhận việc).
  4. Tự động lưu vết lịch sử kiểm toán (*Audit Trail / Activity Log*), cập nhật số lượng thống kê theo giai đoạn và đồng bộ dữ liệu tức thời trên toàn hệ thống.
- **Tiêu chuẩn học thuật và kỹ thuật áp dụng:**
  - Giáo trình Kiểm thử và Đảm bảo chất lượng phần mềm (**CSE462**) – Trường Đại học Thủy Lợi.
  - Chuẩn kiểm thử quốc tế **ISTQB CTFL 2018 v3.1** (Black-box Test Techniques: EP, BVA, Decision Table, State Transition Testing).
  - Chuẩn quy trình kiểm thử phần mềm **ISO/IEC/IEEE 29119-4**.
  - Tiêu chuẩn mô hình chất lượng phần mềm **ISO/IEC 25010** (Functional Suitability, Reliability, Security, Data Integrity, Concurrency).

---

## 🎯 PHẦN 2: PHÂN TÍCH CƠ SỞ KIỂM THỬ VÀ LUỒNG SỰ KIỆN

### 1. Điều kiện tiên quyết (Pre-conditions)
1. Chuyên viên tuyển dụng (HR) đã đăng nhập thành công vào hệ thống quản lý tuyển dụng (Phiên làm việc / Token xác thực còn hiệu lực).
2. Quy trình tuyển dụng và các giai đoạn chuẩn đã được thiết lập sẵn trong CSDL: *Mới (New)*, *Sàng lọc (Screening)*, *Phỏng vấn (Interview)*, *Đề nghị nhận việc (Offer)*, *Trúng tuyển (Hired)*, *Từ chối (Rejected)*.
3. Có ít nhất một hồ sơ ứng viên đang tồn tại ở trạng thái hoạt động trong hệ thống.

### 2. Hậu điều kiện (Post-conditions)
1. Trạng thái của hồ sơ ứng viên được cập nhật chính xác vào CSDL theo đúng quy tắc chuyển trạng thái hợp lệ.
2. Hệ thống ghi vết lịch sử kiểm toán (*Activity Log*) đầy đủ: Mã ứng viên, Trạng thái cũ $\rightarrow$ Trạng thái mới, Thời điểm thực hiện, Mã chuyên viên thực hiện, Lý do (nếu là từ chối/khôi phục).
3. Số lượng thống kê hồ sơ tại giai đoạn nguồn và giai đoạn đích được đồng bộ cập nhật chính xác (Nguồn: $-1$, Đích: $+1$).
4. Kích hoạt sự kiện nghiệp vụ phụ trợ tương ứng (ví dụ: tự động kích hoạt hàng đợi gửi email thông báo lịch hẹn khi chuyển sang giai đoạn Phỏng vấn).

---

### 3. Sơ đồ chuyển đổi trạng thái logic nghiệp vụ (State Transition Diagram)

```mermaid
stateDiagram-v2
    [*] --> S0_Moi : Hồ sơ mới tiếp nhận
    
    S0_Moi --> S1_SangLoc : Chuyển duyệt hồ sơ
    S0_Moi --> S5_TuChoi : Từ chối (Bắt buộc có lý do)
    
    S1_SangLoc --> S2_PhongVan : Duyệt CV đạt yêu cầu
    S1_SangLoc --> S5_TuChoi : Loại hồ sơ không đạt
    
    S2_PhongVan --> S3_Offer : Phỏng vấn đạt đánh giá
    S2_PhongVan --> S5_TuChoi : Phỏng vấn không đạt
    
    S3_Offer --> S4_TrungTuyen : Ứng viên đồng ý Offer
    S3_Offer --> S5_TuChoi : Ứng viên từ chối Offer
    
    S5_TuChoi --> S1_SangLoc : Khôi phục / Tái kích hoạt
    
    S4_TrungTuyen --> [*] : Hoàn tất quy trình tuyển dụng
    
    note right of S0_Moi
        Chặn nhảy cóc sang Trúng tuyển (EX_01)
        Chặn chuyển ngược từ Trúng tuyển về Mới (EX_02)
        Yêu cầu kết quả đánh giá trước khi sang Offer (EX_03)
    end note
```

---

### 4. Phân rã luồng sự kiện chi tiết (Flow of Events - Business Logic Standard)

#### 1.1. Luồng chính (Main Flow - Chuyển đổi trạng thái tuần tự hợp lệ)
- **Bước 1:** Chuyên viên tuyển dụng truy cập vào màn hình Quản lý quy trình tuyển dụng (*Pipeline Management*).
- **Bước 2:** Hệ thống truy vấn CSDL và hiển thị danh sách các hồ sơ ứng viên tương ứng với từng giai đoạn tuyển dụng (Ví dụ: *"Hồ sơ mới"*, *"Sơ tuyển"*, *"Phỏng vấn"*, *"Đề nghị nhận việc"*, *"Trúng tuyển"*, *"Từ chối"*).
- **Bước 3:** Chuyên viên tuyển dụng lựa chọn hồ sơ ứng viên cần xử lý và chọn chuyển từ giai đoạn hiện tại sang giai đoạn tuyển dụng mới.
- **Bước 4:** Hệ thống kiểm tra điều kiện chuyển đổi trạng thái (*Business Rules Validation*) và yêu cầu xác nhận hoặc điền thông tin bổ sung của giai đoạn đích (nếu có).
- **Bước 5:** Chuyên viên xác nhận cập nhật trạng thái mới.
- **Bước 6:** Hệ thống cập nhật trạng thái mới cho hồ sơ trong CSDL, ghi vết lịch sử tiến trình (*Activity Log*) và tự động kích hoạt tiến trình thông báo/email tương ứng.

#### 1.2. Luồng rẽ nhánh và thay thế (Alternative Flows)
- **A1 (Cập nhật trạng thái từ màn hình Chi tiết hồ sơ):** Tại Bước 3, chuyên viên mở xem chi tiết hồ sơ ứng viên và chọn cập nhật trạng thái mới trực tiếp từ bảng điều khiển hồ sơ cá nhân $\rightarrow$ Hệ thống chuyển tiếp sang Bước 4.
- **A2 (Chuyển trạng thái hàng loạt - Batch Processing):** Chuyên viên tích chọn nhiều hồ sơ ứng viên trong cùng một giai đoạn $\rightarrow$ Chọn chức năng *"Chuyển trạng thái hàng loạt"* và chọn giai đoạn đích $\rightarrow$ Hệ thống kiểm tra điều kiện và cập nhật đồng loạt cho tất cả các hồ sơ hợp lệ.
- **A3 (Hủy bỏ thao tác chuyển trạng thái):** Tại Bước 4 hoặc Bước 5, chuyên viên chọn *"Hủy"* hoặc đóng hộp thoại $\rightarrow$ Hệ thống hủy bỏ yêu cầu, giữ nguyên trạng thái hiện tại của hồ sơ trong CSDL và không lưu thay đổi.
- **A4 (Tự động kích hoạt email thông báo theo giai đoạn):** Khi chuyển sang giai đoạn có cấu hình gửi email tự động (như *"Thư mời phỏng vấn"*, *"Từ chối"*...) $\rightarrow$ Hệ thống tự động tạo sẵn nội dung thư theo mẫu để chuyên viên rà soát, cá nhân hóa trước khi gửi đi.
- **A5 (Hoàn tác chuyển trạng thái - Undo Action):** Ngay sau khi cập nhật trạng thái thành công, hệ thống cung cấp tùy chọn *"Hoàn tác"* trong khoảng thời gian hiệu lực 5 giây $\rightarrow$ Chuyên viên kích hoạt hoàn tác $\rightarrow$ Hệ thống tự động khôi phục hồ sơ về trạng thái ngay trước đó và cập nhật lại CSDL.

#### 1.3. Luồng ngoại lệ (Exception Flows)
- **EX_01 (Vi phạm quy trình tuyển dụng / Nhảy bước không cho phép):** Chuyên viên yêu cầu chuyển trạng thái không đúng trình tự quy định (Ví dụ: Chuyển trực tiếp từ *"Hồ sơ mới"* sang *"Trúng tuyển"*) $\rightarrow$ Hệ thống từ chối cập nhật, cảnh báo: *"Không thể chuyển trực tiếp trạng thái này. Vui lòng tuân thủ quy trình tuần tự"* và giữ nguyên trạng thái cũ của hồ sơ.
- **EX_02 (Thiếu thông tin điều kiện bắt buộc của giai đoạn đích):** Chuyển sang giai đoạn mới nhưng thiếu dữ liệu điều kiện tiên quyết (Ví dụ: Chuyển sang *"Phỏng vấn"* nhưng chưa thiết lập thời gian/người phỏng vấn; hoặc chuyển sang *"Từ chối"* nhưng để trống lý do) $\rightarrow$ Hệ thống chặn lưu và yêu cầu nhập đủ thông tin bắt buộc.
- **EX_03 (Hồ sơ đã bị khóa hoặc ở trạng thái kết thúc):** Hồ sơ ứng viên đã ở giai đoạn kết thúc (Đã tuyển dụng hoàn tất, Đã đóng hồ sơ hoặc Ứng viên rút đơn tuyển dụng) $\rightarrow$ Hệ thống từ chối thay đổi, báo lỗi: *"Hồ sơ đã đóng, không thể thay đổi trạng thái"*.
- **EX_04 (Xung đột dữ liệu do tương tranh nhiều phiên làm việc):** Hồ sơ đã bị chuyên viên khác cập nhật trạng thái trong cùng thời điểm $\rightarrow$ Hệ thống kích hoạt cơ chế khóa lạc quan (*Optimistic Locking*), từ chối ghi đè và báo lỗi: *"Dữ liệu hồ sơ đã được cập nhật bởi chuyên viên khác. Vui lòng tải lại trang để nhận dữ liệu mới nhất"*.
- **EX_05 (Lỗi gián đoạn kết nối mạng hoặc máy chủ CSDL):** Mất kết nối mạng hoặc máy chủ CSDL phản hồi timeout trong lúc gửi yêu cầu cập nhật $\rightarrow$ Hệ thống tự động *Rollback transaction*, cảnh báo: *"Lỗi kết nối máy chủ. Thao tác cập nhật chưa được lưu"* và bảo toàn dữ liệu gốc.
- **EX_06 (Phiên làm việc của Chuyên viên hết hạn - Session Expired):** Trong quá trình thao tác, phiên đăng nhập của Chuyên viên tuyển dụng hết hạn (Token JWT hết hiệu lực) $\rightarrow$ Hệ thống từ chối ghi nhận vào CSDL, yêu cầu đăng nhập lại để đảm bảo an toàn thông tin tuyển dụng.

---

## 2. BẢNG TỔNG HỢP DANH SÁCH DỮ LIỆU ĐẦU VÀO (INPUT DATA SPECIFICATION)

| STT | Tên trường dữ liệu | Kiểu dữ liệu | Bắt buộc | Ràng buộc kỹ thuật & Nghiệp vụ | Giá trị mặc định |
| :---: | :--- | :---: | :---: | :--- | :---: |
| **1** | **Hồ sơ ứng viên xử lý (Candidate ID / IDs)** | `UUID / Integer / Array[ID]` | **Bắt buộc** | - Mã định danh hợp lệ của ứng viên, tồn tại trong CSDL và hồ sơ đang mở (chưa bị khóa/xóa).<br>- Hỗ trợ truyền 1 ID (đơn lẻ) hoặc danh sách mảng ID (khi thực hiện chuyển trạng thái hàng loạt theo luồng A2). | Lấy từ hồ sơ được chọn |
| **2** | **Giai đoạn nguồn (Source Stage)** | `Enum` | **Bắt buộc** | - Thuộc tập hợp các giai đoạn chuẩn hóa trong hệ thống: `["Hồ sơ mới", "Sơ tuyển", "Phỏng vấn", "Đề nghị nhận việc", "Trúng tuyển", "Từ chối"]`. | Trạng thái hiện tại của hồ sơ trong DB |
| **3** | **Giai đoạn đích (Target Stage)** | `Enum` | **Bắt buộc** | - Phải tuân theo ma trận chuyển đổi tuần tự (không nhảy cóc quy trình).<br>- Không cho phép chuyển ngược từ trạng thái kết thúc (`Trúng tuyển` $\rightarrow$ `Hồ sơ mới`). | Chưa chọn (Bắt buộc HR chỉ định) |
| **4** | **Lý do từ chối (Rejection Reason)** | `Enum / String` | **Bắt buộc** *(khi đích là "Từ chối")* | - Bắt buộc chọn hoặc nhập khi chuyển hồ sơ sang giai đoạn `Từ chối`.<br>- Độ dài: $1 \le L \le 500$ ký tự; không chứa mã độc XSS/HTML script.<br>- Cho phép chọn từ danh mục chuẩn (*Kỹ năng chưa phù hợp, Mức lương không thỏa thuận được, Ứng viên rút hồ sơ...*) hoặc nhập văn bản chi tiết. | Rỗng (`""`) |
| **5** | **Thông tin lịch phỏng vấn (Interview Schedule)** | `Object` | **Bắt buộc** *(khi đích là "Phỏng vấn")* | - Thời gian phỏng vấn: `DateTime` hợp lệ và $>$ Thời điểm hiện tại.<br>- Người phỏng vấn: Ít nhất 1 chuyên viên chuyên môn/HR, không trùng lịch bận.<br>- Hình thức: `Trực tuyến` (Link Google Meet/Zoom) hoặc `Trực tiếp` (Phòng họp nội bộ). | Khung giờ trống gợi ý sớm nhất |
| **6** | **Thông tin đề nghị nhận việc (Offer Details)** | `Object` | **Bắt buộc** *(khi đích là "Đề nghị nhận việc")* | - Mức lương đề xuất: Kiểu số thực $> 0$.<br>- Ngày bắt đầu dự kiến: `Date` $\ge$ Ngày hiện tại.<br>- Hạn phản hồi thỏa thuận: `DateTime` $>$ Thời điểm gửi offer. | Mức lương chuẩn theo cấu hình JD |
| **7** | **Lý do khôi phục hồ sơ (Reactivation Reason)** | `String` | **Bắt buộc** *(khi khôi phục từ chối về sơ tuyển)* | - Bắt buộc nhập khi khôi phục ứng viên theo luồng thay thế A2.<br>- Độ dài: $1 \le L \le 255$ ký tự, khử mã độc kịch bản; ghi rõ lý do mở lại (bổ sung chứng chỉ, mở thêm chỉ tiêu...). | Rỗng (`""`) |
| **8** | **Thứ tự ưu tiên xử lý (Rank / Priority Index)** | `Integer` | **Tùy chọn** | - Số nguyên dương $1 \le \text{Rank} \le N$ ($N$ là tổng số hồ sơ tại giai đoạn đích), xác định mức độ ưu tiên xử lý hồ sơ. | Thêm vào cuối danh sách ($N + 1$) |
| **9** | **Bộ lọc Vị trí tuyển dụng (Job Filter)** | `UUID / Integer` | **Tùy chọn** | - Lọc bảng quy trình theo mã chiến dịch tuyển dụng / JD hợp lệ và đang hoạt động (`Active`). | `"Tất cả vị trí"` (`ALL`) |
| **10**| **Từ khóa tìm kiếm nhanh (Search Keyword)** | `String` | **Tùy chọn** | - Tìm kiếm theo họ tên ứng viên.<br>- Độ dài: $0 \le L \le 50$ ký tự, tự động khử mã độc SQLi/XSS. | Rỗng (`""`) |

---

## 3. PHÂN TÍCH RÀNG BUỘC TỪNG TRƯỜNG DỮ LIỆU

### 1. Bảng phân tích chi tiết từng trường dữ liệu áp dụng phân vùng tương đương và giá trị biên

| Tên trường | Ràng buộc nghiệp vụ và kỹ thuật | Phân vùng hợp lệ và Giá trị đại diện | Phân vùng không hợp lệ và Giá trị đại diện | Các giá trị biên cần kiểm thử |
| :--- | :--- | :--- | :--- | :--- |
| **Hồ sơ ứng viên xử lý** | - Kiểu: `UUID / Integer / Array`<br>- Bắt buộc phải tồn tại trong CSDL và đang ở trạng thái mở (Active)<br>- Hỗ trợ chuyển đơn lẻ (1 hồ sơ) hoặc chuyển hàng loạt ($1 \le N \le 50$) | - Phân vùng hợp lệ:<br>  + Đơn lẻ: `UV_001` (Nguyễn Văn An)<br>  + Hàng loạt: `["UV_001", "UV_002", "UV_003"]` | - Phân vùng không hợp lệ:<br>  + ID không tồn tại trong CSDL: `UV_999999`<br>  + Hồ sơ đã bị đóng/xóa vĩnh viễn (Kích hoạt EX_03)<br>  + Không chọn hồ sơ nào (`null` hoặc `[]`)<br>  + Vượt quá số lượng 50 hồ sơ/lần | - Biên số lượng hồ sơ chuyển hàng loạt ($N$):<br>  + $N = 0$: Lỗi chưa chọn hồ sơ nào<br>  + $N = 1$: Hợp lệ tối thiểu<br>  + $N = 2$: Hợp lệ cận dưới<br>  + $N = 49$: Hợp lệ cận trên<br>  + $N = 50$: Hợp lệ tối đa một lần chuyển<br>  + $N = 51$: Báo lỗi vượt quá giới hạn 50 hồ sơ |
| **Quy tắc chuyển đổi trạng thái** | - Kiểu: `Enum Transition`<br>- Tập giá trị: `Hồ sơ mới`, `Sơ tuyển`, `Phỏng vấn`, `Đề nghị nhận việc`, `Trúng tuyển`, `Từ chối`<br>- Phải tuân theo quy tắc tuần tự, nghiêm cấm nhảy cóc hoặc chuyển ngược từ kết thúc | - Phân vùng hợp lệ:<br>  + `Hồ sơ mới` $\rightarrow$ `Sơ tuyển`<br>  + `Sơ tuyển` $\rightarrow$ `Phỏng vấn`<br>  + `Phỏng vấn` $\rightarrow$ `Đề nghị nhận việc`<br>  + `Đề nghị nhận việc` $\rightarrow$ `Trúng tuyển`<br>  + Bất kỳ giai đoạn nào $\rightarrow$ `Từ chối`<br>  + `Từ chối` $\rightarrow$ `Sơ tuyển` (Khôi phục) | - Phân vùng không hợp lệ:<br>  + Nhảy cóc: `Hồ sơ mới` $\rightarrow$ `Trúng tuyển` (EX_01)<br>  + Nhảy cóc: `Hồ sơ mới` $\rightarrow$ `Đề nghị nhận việc`<br>  + Nhảy cóc: `Sơ tuyển` $\rightarrow$ `Trúng tuyển`<br>  + Chuyển ngược: `Trúng tuyển` $\rightarrow$ `Hồ sơ mới` (EX_03)<br>  + Chuyển ngược: `Đề nghị nhận việc` $\rightarrow$ `Hồ sơ mới`<br>  + Trạng thái lạ ngoài danh mục enum | - Không áp dụng giá trị biên định lượng (Kiểm thử theo kỹ thuật Bảng chuyển trạng thái - State Transition Testing) |
| **Lý do từ chối hồ sơ** | - Kiểu: `Enum / String`<br>- Bắt buộc khi chuyển sang giai đoạn `Từ chối`<br>- Độ dài: $1 \le L \le 500$ ký tự<br>- Chọn mẫu chuẩn hoặc tự nhập; khử mã độc XSS/HTML Script | - Phân vùng hợp lệ:<br>  + Mẫu chuẩn: `"Kỹ năng chưa phù hợp"`<br>  + Mẫu chuẩn: `"Mức lương không thỏa thuận được"`<br>  + Tự nhập hợp lệ: `"Kỹ năng thuật toán chưa đạt yêu cầu live-code"` | - Phân vùng không hợp lệ:<br>  + Để trống: `""` (Kích hoạt EX_02)<br>  + Chỉ chứa khoảng trắng: `"   "`<br>  + Quá 500 ký tự<br>  + Chứa script: `<script>alert('XSS')</script>` | - Biên độ dài lý do từ chối ($L$):<br>  + $L = 0$: `""` (Báo lỗi để trống EX_02)<br>  + $L = 1$: `"K"` (Hợp lệ tối thiểu)<br>  + $L = 2$: `"Ko"` (Hợp lệ)<br>  + $L = 499$: Chuỗi 499 ký tự (Hợp lệ)<br>  + $L = 500$: Chuỗi 500 ký tự (Hợp lệ tối đa)<br>  + $L = 501$: Báo lỗi vượt quá 500 ký tự |
| **Thời gian phỏng vấn thiết lập** | - Kiểu: `DateTime`<br>- Bắt buộc khi chuyển sang giai đoạn `Phỏng vấn`<br>- Ràng buộc: $T > T_{\text{hiện tại}}$ và cách hiện tại ít nhất 15 phút | - Phân vùng hợp lệ:<br>  + Khung giờ tương lai hợp lệ: $T \ge T_{\text{hiện tại}} + 15\text{ phút}$ (Ví dụ: Ngày mai 09:00 AM) | - Phân vùng không hợp lệ:<br>  + Quá khứ: $T < T_{\text{hiện tại}}$<br>  + Tương lai quá cận: $0 \le T - T_{\text{hiện tại}} < 15\text{ phút}$<br>  + Để trống ngày giờ (EX_02)<br>  + Ngày sai cú pháp: `"31/02/2026"` | - Biên thời gian hẹn ($T$ so với $T_{\text{hiện tại}}$):<br>  + $T = T_{\text{hiện tại}} - 1\text{ phút}$ (Lỗi quá khứ)<br>  + $T = T_{\text{hiện tại}}$ (Lỗi thời gian hiện tại)<br>  + $T = T_{\text{hiện tại}} + 14\text{ phút}$ (Lỗi dưới 15 phút)<br>  + $T = T_{\text{hiện tại}} + 15\text{ phút}$ (Hợp lệ tối thiểu)<br>  + $T = T_{\text{hiện tại}} + 16\text{ phút}$ (Hợp lệ) |
| **Mức lương đề xuất trong Offer** | - Kiểu: `Float / Decimal`<br>- Bắt buộc khi chuyển sang giai đoạn `Đề nghị nhận việc`<br>- Ràng buộc: $1,000,000 \le \text{Salary} \le 500,000,000\text{ VNĐ}$ | - Phân vùng hợp lệ:<br>  + Lương chuẩn: `15000000` (15 triệu VNĐ)<br>  + Lương quản lý: `45000000` (45 triệu VNĐ) | - Phân vùng không hợp lệ:<br>  + Bằng 0 hoặc âm: `0`, `-5000000`<br>  + Dưới mức tối thiểu: `800000`<br>  + Vượt trần: `600000000`<br>  + Nhập ký tự chữ: `"hai mươi triệu"` | - Biên mức lương đề xuất (VNĐ):<br>  + $\text{Salary} = 0$: Lỗi lương không dương<br>  + $\text{Salary} = 999,999$: Lỗi dưới mức sàn<br>  + $\text{Salary} = 1,000,000$: Hợp lệ tối thiểu<br>  + $\text{Salary} = 1,000,001$: Hợp lệ<br>  + $\text{Salary} = 500,000,000$: Hợp lệ tối đa<br>  + $\text{Salary} = 500,000,001$: Lỗi vượt trần |
| **Lý do khôi phục hồ sơ** | - Kiểu: `String`<br>- Bắt buộc khi khôi phục từ `Từ chối` về `Sơ tuyển` (Luồng A2)<br>- Độ dài: $1 \le L \le 255$ ký tự, khử XSS | - Phân vùng hợp lệ:<br>  + `"Ứng viên bổ sung chứng chỉ IELTS 7.5 và mở thêm chỉ tiêu"` | - Phân vùng không hợp lệ:<br>  + Để trống: `""`<br>  + Quá 255 ký tự<br>  + Chứa thẻ script: `<script>` | - Biên độ dài ký tự lý do khôi phục ($L$):<br>  + $L = 0$: `""` (Báo lỗi để trống lý do)<br>  + $L = 1$: `"A"` (Hợp lệ tối thiểu)<br>  + $L = 254$: Hợp lệ<br>  + $L = 255$: Hợp lệ tối đa<br>  + $L = 256$: Báo lỗi vượt quá 255 ký tự |
| **Thời gian hiệu lực thao tác Hoàn tác** | - Kiểu: `Duration (Giây)`<br>- Ngưỡng cửa sổ cho phép: $0.0 \le T \le 5.0\text{ giây}$ | - Phân vùng hợp lệ:<br>  + $0.1\text{s} \le T \le 5.0\text{s}$ (Hoàn tác trạng thái thành công) | - Phân vùng không hợp lệ:<br>  + $T > 5.0\text{s}$ (Hết hạn cửa sổ hoàn tác, không thể đảo ngược tự động) | - Biên thời gian hoàn tác ($T$):<br>  + $T = 0.1\text{s}$ (Hoàn tác tức thì thành công)<br>  + $T = 4.9\text{s}$ (Hoàn tác hợp lệ cận trên)<br>  + $T = 5.0\text{s}$ (Hoàn tác hợp lệ tại giây thứ 5)<br>  + $T = 5.1\text{s}$ (Hết hiệu lực hoàn tác, giữ nguyên trạng thái mới) |
| **Số lượng hồ sơ trong một giai đoạn** | - Kiểu: `Integer`<br>- Số nguyên không âm: $0 \le N \le 500$ hồ sơ | - Phân vùng hợp lệ:<br>  + $N = 0$ (Giai đoạn rỗng - Empty State)<br>  + $1 \le N \le 50$ (Tải dữ liệu mượt mà một trang)<br>  + $51 \le N \le 500$ (Hỗ trợ cuộn tải / phân trang) | - Phân vùng không hợp lệ:<br>  + Số âm: $N < 0$<br>  + Vượt tải: $N > 500$ hồ sơ | - Biên số lượng hồ sơ ($N$):<br>  + $N = -1$: Lỗi dữ liệu số âm<br>  + $N = 0$: Trạng thái rỗng, số đếm = 0<br>  + $N = 1$: Hợp lệ tối thiểu<br>  + $N = 50$: Hợp lệ tối đa 1 màn hình<br>  + $N = 51$: Kích hoạt phân trang / cuộn tải<br>  + $N = 500$: Hợp lệ tối đa toàn hệ thống<br>  + $N = 501$: Cảnh báo vượt tải trọng |
| **Từ khóa tìm kiếm nhanh hồ sơ** | - Kiểu: `String`<br>- Tùy chọn, độ dài: $0 \le L \le 50$ ký tự<br>- Tự động khử SQL Injection và XSS | - Phân vùng hợp lệ:<br>  + Tìm có dấu: `"Nguyễn Văn An"`<br>  + Tìm không dấu: `"Tran Binh"`<br>  + Chuỗi rỗng: `""` (Hiển thị tất cả) | - Phân vùng không hợp lệ:<br>  + Quá 50 ký tự<br>  + Mã độc SQLi: `' OR 1=1 --`<br>  + Mã độc XSS: `<script>` | - Biên độ dài từ khóa tìm kiếm ($L$):<br>  + $L = 0$: `""` (Hiển thị toàn bộ)<br>  + $L = 1$: `"A"` (Hợp lệ tối thiểu)<br>  + $L = 49$: Hợp lệ<br>  + $L = 50$: Hợp lệ tối đa<br>  + $L = 51$: Báo lỗi/Cắt ngắn chuỗi quá 50 ký tự |
| **Thời gian phản hồi cập nhật hệ thống** | - Kiểu: `Duration (Giây)`<br>- Ngưỡng tối đa cho phép: $T \le 3.0\text{ giây}$ | - Phân vùng hợp lệ:<br>  + $0.1\text{s} \le T \le 3.0\text{s}$ (Cập nhật thành công nhanh chóng) | - Phân vùng không hợp lệ:<br>  + $T > 3.0\text{s}$ (Cảnh báo mạng chậm)<br>  + $T > 10.0\text{s}$ (Timeout máy chủ CSDL, kích hoạt Rollback EX_05) | - Biên thời gian phản hồi API ($T$):<br>  + $T = 0.5\text{s}$ (Phản hồi nhanh)<br>  + $T = 2.9\text{s}$ (Hợp lệ)<br>  + $T = 3.0\text{s}$ (Hợp lệ tối đa)<br>  + $T = 3.1\text{s}$ (Cảnh báo mạng phản hồi chậm)<br>  + $T = 10.0\text{s}$ (Ngưỡng ngắt kết nối Timeout)<br>  + $T = 10.1\text{s}$ (Rollback transaction EX_05) |

---

## 4. BẢNG QUYẾT ĐỊNH CHO TỔ HỢP LOGIC NGHIỆP VỤ

### 4.1. Phân tích quan hệ ràng buộc chéo và tiền điều kiện

Trong quy trình quản lý tuyển dụng (*Recruitment Pipeline Management*), việc chuyển đổi trạng thái của hồ sơ ứng viên giữa các giai đoạn bị chi phối bởi các quan hệ phụ thuộc chéo và ràng buộc tiền điều kiện chặt chẽ:

1. **Ràng buộc phụ thuộc giữa Giai đoạn đích "Từ chối" và Lý do từ chối:**
   - Khi chuyên viên chuyển hồ sơ sang giai đoạn `Từ chối` (từ bất kỳ giai đoạn nào: *Mới, Sơ tuyển, Phỏng vấn, Đề nghị nhận việc*), hệ thống kích hoạt ràng buộc bắt buộc phải chọn hoặc nhập `Lý do từ chối` ($1 \le L \le 500$ ký tự).
   - Biểu thức logic:
     $$\text{TargetStage} = \text{REJECTED} \implies (\text{Reason} \ne \emptyset) \land (1 \le \text{Length}(\text{Reason}) \le 500)$$
   - Nếu để trống lý do $\rightarrow$ Hệ thống chặn cập nhật, kích hoạt lỗi `EX_02` và giữ nguyên trạng thái cũ của hồ sơ.

2. **Ràng buộc điều kiện tiên quyết cho Giai đoạn đích "Phỏng vấn":**
   - Chuyển hồ sơ từ `Sơ tuyển` sang `Phỏng vấn` bắt buộc phải hoàn thành thiết lập lịch phỏng vấn (Thời gian phỏng vấn hợp lệ ở tương lai $> 15$ phút, có ít nhất 01 người phỏng vấn chuyên môn và xác định hình thức Online/Offline).
   - Biểu thức logic:
     $$\text{TargetStage} = \text{INTERVIEW} \implies (\text{Time} > \text{CurrentTime} + 15\text{m}) \land (\text{Interviewer} \ne \emptyset)$$
   - Nếu thiếu thông tin lịch phỏng vấn $\rightarrow$ Hệ thống chặn chuyển bước và yêu cầu bổ sung thông tin.

3. **Ràng buộc điều kiện tiên quyết cho Giai đoạn đích "Đề nghị nhận việc (Offer)":**
   - Chỉ cho phép chuyển ứng viên sang giai đoạn `Đề nghị nhận việc` khi ứng viên đã hoàn thành vòng `Phỏng vấn` và có kết quả đánh giá là *"Đạt"* (Pass) từ Hội đồng phỏng vấn.
   - Biểu thức logic:
     $$\text{TargetStage} = \text{OFFER} \implies (\text{SourceStage} = \text{INTERVIEW}) \land (\text{InterviewEvaluation} = \text{"PASS"})$$
   - Nếu chưa nhập đánh giá hoặc đánh giá không đạt $\rightarrow$ Hệ thống chặn chuyển sang Offer và kích hoạt ngoại lệ `EX_02`.

4. **Quy tắc ma trận chuyển đổi tuần tự (Chống nhảy cóc quy trình):**
   - Quy trình tuyển dụng phải tuân theo luồng chuyển tiếp một chiều tuần tự:
     $$\text{Hồ sơ mới} \longrightarrow \text{Sơ tuyển} \longrightarrow \text{Phỏng vấn} \longrightarrow \text{Đề nghị nhận việc} \longrightarrow \text{Trúng tuyển}$$
   - Mọi hành vi nhảy bước (ví dụ: `Hồ sơ mới` $\rightarrow$ `Trúng tuyển`, `Hồ sơ mới` $\rightarrow$ `Đề nghị nhận việc`, `Sơ tuyển` $\rightarrow$ `Trúng tuyển`) đều bị hệ thống từ chối và kích hoạt ngoại lệ `EX_01`.

5. **Ràng buộc logic chuyển trạng thái ngược và Hồ sơ đã đóng:**
   - Nghiêm cấm chuyển ngược trạng thái từ giai đoạn kết thúc `Trúng tuyển` về giai đoạn khởi tạo `Hồ sơ mới` hoặc `Sơ tuyển`.
   - Đối với hồ sơ đã ở trạng thái kết thúc (Đã tuyển dụng, Đã đóng hồ sơ hoặc Ứng viên rút đơn), mọi thao tác chuyển trạng thái đều bị khóa (Kích hoạt `EX_03`).
   - Riêng hồ sơ ở giai đoạn `Từ chối` chỉ được phép chuyển về duy nhất giai đoạn `Sơ tuyển` thông qua chức năng "Khôi phục hồ sơ" kèm lý do mở lại.

6. **Ràng buộc xử lý tương tranh dữ liệu (Concurrency & Optimistic Locking):**
   - Khi hai chuyên viên HR cùng thao tác cập nhật trạng thái trên cùng 1 hồ sơ trong cùng thời điểm, hệ thống so sánh khóa phiên bản dữ liệu (`version` / `updated_at`).
   - Giao dịch đến trước được ghi nhận thành công, giao dịch đến sau bị từ chối và nhận thông báo lỗi xung đột dữ liệu `EX_04`.

---

### 4.2. Bảng quyết định logic nghiệp vụ

| Mã | Điều kiện / Hành động | $R_1$ | $R_2$ | $R_3$ | $R_4$ | $R_5$ | $R_6$ | $R_7$ | $R_8$ |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **C1** | Đã chọn hồ sơ và giai đoạn đích hợp lệ | Có | **Không** | Có | Có | Có | Có | Có | Có |
| **C2** | Chuyển trạng thái đúng tuần tự quy trình | Có | - | **Không** | Có | Có | Có | Có | Có |
| **C3** | Đã nhập đủ thông tin bắt buộc của giai đoạn đích | Có | - | - | **Không** | Có | Có | Có | Có |
| **C4** | Hồ sơ chưa ở trạng thái kết thúc/bị khóa | Có | - | - | - | **Không** | Có | Có | Có |
| **C5** | Không có xung đột dữ liệu (Optimistic Locking) | Có | - | - | - | - | **Không** | Có | Có |
| **C6** | Chuyên viên nhấn "Xác nhận" | Có | - | - | - | - | - | **Không** | Có |
| **C7** | Thực hiện hoàn tác trong vòng 5 giây (A5) | Không | - | - | - | - | - | - | **Có** |
| **A1** | Cập nhật trạng thái mới cho hồ sơ trong CSDL | **X** | - | - | - | - | - | - | - |
| **A2** | Ghi vết lịch sử tiến trình và kích hoạt email tự động | **X** | - | - | - | - | - | - | - |
| **A3** | Báo lỗi EX_01: Cảnh báo vi phạm quy trình nhảy bước | - | - | **X** | - | - | - | - | - |
| **A4** | Báo lỗi EX_02: Yêu cầu nhập đủ thông tin điều kiện | - | - | - | **X** | - | - | - | - |
| **A5** | Báo lỗi EX_03: Hồ sơ đã đóng, không thể thay đổi | - | - | - | - | **X** | - | - | - |
| **A6** | Báo lỗi EX_04: Cảnh báo xung đột tương tranh dữ liệu | - | - | - | - | - | **X** | - | - |
| **A7** | Hủy bỏ thao tác (A3), giữ nguyên trạng thái cũ | - | **X** | - | - | - | - | **X** | - |
| **A8** | Khôi phục hồ sơ về trạng thái trước đó (A5) | - | - | - | - | - | - | - | **X** |

---

## 5. BẢNG CA KIỂM THỬ CHI TIẾT TỔNG HỢP

### 5.1. Ma trận phân bổ 38 ca kiểm thử (Traceability Matrix)

| Phân nhóm kiểm thử | Dải Test Case ID | Số lượng | Kỹ thuật áp dụng & Trọng tâm nghiệp vụ |
| :--- | :---: | :---: | :--- |
| **Nhóm 1: Luồng chính - Chuyển trạng thái tuần tự hợp lệ** | `TC_UC11_001` $\rightarrow$ `TC_UC11_005` | 5 ca | Use Case Flow: Chuyển tuần tự qua các giai đoạn Mới, Sàng lọc, Phỏng vấn, Offer, Trúng tuyển, Từ chối kèm lý do. |
| **Nhóm 2: Các luồng thay thế & Nghiệp vụ phụ trợ** | `TC_UC11_006` $\rightarrow$ `TC_UC11_010` | 5 ca | Luồng thay thế A1-A5: Khôi phục hồ sơ từ chối (A2), Lọc theo Job (A3), Tìm kiếm theo tên, Điều chỉnh ưu tiên, Hủy thao tác (A3/A4). |
| **Nhóm 3: Kiểm tra Quy tắc trạng thái & Ngoại lệ nghiệp vụ** | `TC_UC11_011` $\rightarrow$ `TC_UC11_018` | 8 ca | Business Rules & Exceptions: Chặn nhảy cóc (EX_01), Chặn chuyển ngược/hồ sơ đã đóng (EX_03), Thiếu đánh giá PV / lý do (EX_02), Chuyển trùng lặp (No-op). |
| **Nhóm 4: Phân tích giá trị biên & Ràng buộc dữ liệu** | `TC_UC11_019` $\rightarrow$ `TC_UC11_025` | 7 ca | BVA & EP: Giai đoạn rỗng ($N=0$), 1 hồ sơ ($N=1$), Tải trọng tối đa ($N=50$), Biên lý do từ chối ($L=1, 500, 501$), Lọc Job không có hồ sơ. |
| **Nhóm 5: Kiểm tra Ngoại lệ hệ thống, Mạng & Tích hợp** | `TC_UC11_026` $\rightarrow$ `TC_UC11_031` | 6 ca | Error Handling & Integration: Mất kết nối CSDL (EX_05), HTTP 500 Rollback, Token hết hạn (EX_06), Ghi vết Activity Log, Kích hoạt Auto-email, Đồng bộ Table View. |
| **Nhóm 6: Tương tranh dữ liệu, Toàn vẹn & An toàn thông tin** | `TC_UC11_032` $\rightarrow$ `TC_UC11_038` | 7 ca | Concurrency, Security & Integrity: Optimistic Locking 2 HR (EX_04), Chống XSS lý do từ chối, Chống SQLi bộ lọc, Toàn vẹn số lượng đếm, Idempotency, Bộ lọc kép, Khóa ngoại CSDL. |
| **TỔNG CỘNG TOÀN USE CASE** | `TC_UC11_001` $\rightarrow$ `TC_UC11_038` | **38 ca** | **Bao phủ 100% chuẩn học phần CSE462 và thực tiễn kiểm thử** |

---

### 5.2. Bảng chi tiết tổng hợp 38 ca kiểm thử (UC_11)

| Mã ca kiểm thử | Tên ca kiểm thử | Loại kiểm thử | Kỹ thuật áp dụng | Tiền điều kiện | Các bước thực hiện | Dữ liệu thử nghiệm | Kết quả mong đợi | Mức độ ưu tiên |
| :---: | :--- | :---: | :---: | :--- | :--- | :--- | :--- | :---: |
| **TC_UC11_001** | Chuyển trạng thái ứng viên từ Mới sang Sàng lọc thành công | Kiểm thử chức năng | Use Case Flow | Hồ sơ ứng viên ở trạng thái Mới | 1. Chọn ứng viên cần xử lý;<br>2. Chọn chuyển sang trạng thái Sàng lọc;<br>3. Xác nhận cập nhật | Hồ sơ: Nguyễn Văn An (`UV_001`) | Cập nhật trạng thái sang Sàng lọc trong CSDL; ghi Activity Log; số lượng hồ sơ giai đoạn Mới -1, Sàng lọc +1 | P1 - Cao |
| **TC_UC11_002** | Chuyển trạng thái từ Sàng lọc sang Phỏng vấn thành công | Kiểm thử chức năng | Use Case Flow | Hồ sơ ứng viên ở trạng thái Sàng lọc đã qua vòng duyệt CV | 1. Chọn ứng viên;<br>2. Chọn chuyển sang trạng thái Phỏng vấn;<br>3. Xác nhận | Hồ sơ: Trần Thị Bình (`UV_002`) | Cập nhật trạng thái sang Phỏng vấn; ghi nhận thời gian và người thực hiện vào Activity Log | P1 - Cao |
| **TC_UC11_003** | Chuyển trạng thái từ Phỏng vấn sang Đề nghị nhận việc (Offer) | Kiểm thử chức năng | Use Case Flow | Hồ sơ ứng viên có kết quả phỏng vấn Đạt | 1. Chọn ứng viên;<br>2. Chọn chuyển sang trạng thái Đề nghị nhận việc;<br>3. Xác nhận | Hồ sơ: Lê Văn Cường (`UV_003`) | Cập nhật trạng thái sang Đề nghị nhận việc; kích hoạt tiến trình tạo thư mời offer | P1 - Cao |
| **TC_UC11_004** | Chuyển trạng thái từ Đề nghị nhận việc sang Trúng tuyển | Kiểm thử chức năng | Use Case Flow | Ứng viên đã phản hồi đồng ý ký Offer | 1. Chọn ứng viên;<br>2. Chọn chuyển sang trạng thái Trúng tuyển;<br>3. Xác nhận | Hồ sơ: Phạm Minh Đức (`UV_004`) | Cập nhật trạng thái Trúng tuyển; đánh dấu hoàn tất quy trình tuyển dụng cho ứng viên | P1 - Cao |
| **TC_UC11_005** | Chuyển trạng thái sang Từ chối từ bất kỳ giai đoạn nào kèm lý do | Kiểm thử chức năng | Use Case Flow | Hồ sơ ứng viên ở giai đoạn Sàng lọc hoặc Phỏng vấn | 1. Chọn ứng viên;<br>2. Chọn chuyển sang Từ chối;<br>3. Nhập lý do từ chối;<br>4. Xác nhận | Lý do: `"Chưa đạt yêu cầu kỹ thuật chuyên môn"` | Cập nhật trạng thái Từ chối; lưu trữ lý do từ chối vào hồ sơ; ghi vết Activity Log | P1 - Cao |
| **TC_UC11_006** | Khôi phục hồ sơ ứng viên từ trạng thái Từ chối về Sàng lọc | Kiểm thử chức năng | Luồng thay thế A2 | Hồ sơ ứng viên đang ở trạng thái Từ chối | 1. Chọn hồ sơ bị từ chối;<br>2. Chọn Khôi phục về Sàng lọc;<br>3. Nhập lý do mở lại;<br>4. Xác nhận | Lý do khôi phục: `"Ứng viên bổ sung chứng chỉ hợp lệ"` | Trạng thái cập nhật về Sàng lọc; lưu vết tái kích hoạt hồ sơ trong Activity Log | P2 - Trung bình |
| **TC_UC11_007** | Lọc quy trình tuyển dụng theo Vị trí tuyển dụng (Job Filter) | Kiểm thử chức năng | Luồng thay thế A3 | Hệ thống có nhiều ứng viên ở các vị trí tuyển dụng khác nhau | 1. Chọn tiêu chí lọc theo vị trí tuyển dụng Backend Developer | Mã vị trí: `JD_JAVA_BACKEND` | Quy trình chỉ hiển thị các hồ sơ ứng tuyển vị trí Backend Developer; số lượng đếm cập nhật đúng | P2 - Trung bình |
| **TC_UC11_008** | Tìm kiếm hồ sơ ứng viên theo Họ tên trong quy trình tuyển dụng | Kiểm thử chức năng | Luồng thay thế A3 | Quy trình có nhiều hồ sơ ứng viên | 1. Nhập từ khóa tìm kiếm theo tên ứng viên | Từ khóa: `"Nguyễn Văn An"` | Hiển thị chính xác hồ sơ khớp tên; ẩn các hồ sơ không thỏa mãn điều kiện tìm kiếm | P2 - Trung bình |
| **TC_UC11_009** | Điều chỉnh thứ tự ưu tiên xử lý của hồ sơ trong cùng một giai đoạn | Kiểm thử chức năng | Data Manipulation | Giai đoạn Sàng lọc có nhiều hồ sơ đang chờ duyệt | 1. Điều chỉnh thứ tự ưu tiên của hồ sơ từ hạng 3 lên hạng 1;<br>2. Lưu thay đổi | Thứ tự ưu tiên: `Rank = 1` | Thứ tự ưu tiên mới được lưu vào CSDL; hồ sơ được xếp lên đầu danh sách xử lý | P2 - Trung bình |
| **TC_UC11_010** | Hủy bỏ thao tác chuyển trạng thái trước khi xác nhận | Kiểm thử nghiệp vụ | Luồng thay thế A4 | Đang mở hộp thoại xác nhận chuyển trạng thái | 1. Chọn chuyển trạng thái;<br>2. Nhấn nút Hủy bỏ | Hành động: Cancel | Hủy bỏ thao tác; trạng thái hồ sơ giữ nguyên không thay đổi; không ghi nhận vào CSDL | P3 - Thấp |
| **TC_UC11_011** | Chặn chuyển nhảy cóc từ Mới sang Trúng tuyển (Ngoại lệ EX_01) | Kiểm thử nghiệp vụ / Ngoại lệ | Ngoại lệ EX_01 | Hồ sơ ứng viên đang ở trạng thái Mới | 1. Yêu cầu chuyển thẳng hồ sơ từ Mới sang Trúng tuyển | Hành vi vi phạm tuần tự quy trình | Hệ thống từ chối cập nhật; báo lỗi EX_01: Quy trình tuyển dụng phải thực hiện tuần tự | P1 - Cao |
| **TC_UC11_012** | Chặn chuyển nhảy cóc từ Mới sang Đề nghị nhận việc | Kiểm thử nghiệp vụ / Ngoại lệ | Ngoại lệ EX_01 | Hồ sơ ứng viên đang ở trạng thái Mới | 1. Yêu cầu chuyển từ Mới sang Đề nghị nhận việc | Bỏ qua vòng Sàng lọc và Phỏng vấn | Chặn cập nhật; báo lỗi EX_01: Không thể bỏ qua các giai đoạn sàng lọc và phỏng vấn | P1 - Cao |
| **TC_UC11_013** | Chặn chuyển nhảy cóc từ Sàng lọc sang Trúng tuyển | Kiểm thử nghiệp vụ / Ngoại lệ | Ngoại lệ EX_01 | Hồ sơ ứng viên đang ở trạng thái Sàng lọc | 1. Yêu cầu chuyển trực tiếp sang Trúng tuyển | Bỏ qua vòng Phỏng vấn và Offer | Chặn cập nhật; thông báo yêu cầu ứng viên phải hoàn thành vòng phỏng vấn | P1 - Cao |
| **TC_UC11_014** | Chặn chuyển ngược bất hợp lệ từ Trúng tuyển về Mới (Ngoại lệ EX_02) | Kiểm thử nghiệp vụ / Ngoại lệ | Ngoại lệ EX_02 | Hồ sơ ứng viên đang ở trạng thái kết thúc Trúng tuyển | 1. Yêu cầu chuyển trạng thái từ Trúng tuyển về Mới | Chuyển ngược trạng thái kết thúc | Hệ thống từ chối cập nhật; báo lỗi EX_02: Không cho phép chuyển ngược từ Trúng tuyển về Mới | P1 - Cao |
| **TC_UC11_015** | Chặn chuyển ngược trạng thái từ Đề nghị nhận việc về Mới | Kiểm thử nghiệp vụ / Ngoại lệ | State Machine Logic | Hồ sơ ứng viên đang ở trạng thái Đề nghị nhận việc | 1. Yêu cầu chuyển trạng thái từ Đề nghị nhận việc về Mới | Chuyển ngược về giai đoạn khởi tạo | Từ chối thao tác; thông báo quy tắc trạng thái không cho phép quay về giai đoạn Mới | P1 - Cao |
| **TC_UC11_016** | Chặn chuyển sang Đề nghị nhận việc khi chưa có đánh giá phỏng vấn (EX_03) | Kiểm thử nghiệp vụ / Ngoại lệ | Ngoại lệ EX_03 | Hồ sơ ở giai đoạn Phỏng vấn nhưng chưa có kết quả đánh giá | 1. Yêu cầu chuyển sang Đề nghị nhận việc | Kết quả phỏng vấn = Chưa đánh giá | Hệ thống báo lỗi EX_03: Bắt buộc hoàn tất đánh giá phỏng vấn trước khi chuyển sang Offer | P1 - Cao |
| **TC_UC11_017** | Chặn chuyển sang Từ chối khi để trống lý do từ chối (Ngoại lệ EX_04) | Kiểm thử nghiệp vụ / Ngoại lệ | Ngoại lệ EX_04 | Hồ sơ ở giai đoạn Phỏng vấn | 1. Chọn chuyển sang Từ chối;<br>2. Để trống lý do từ chối;<br>3. Xác nhận | Lý do từ chối = Rỗng (`""`) | Hệ thống báo lỗi EX_04: Vui lòng nhập hoặc chọn lý do từ chối ứng viên; không cập nhật CSDL | P1 - Cao |
| **TC_UC11_018** | Hoàn tác chuyển trạng thái ứng viên trong vòng 5 giây (A5 / R8) | Kiểm thử chức năng / Phục hồi | Luồng thay thế A5 / Quy tắc R8 | Vừa cập nhật trạng thái ứng viên thành công; thông báo có nút Hoàn tác đang hiển thị | 1. Thực hiện chuyển trạng thái thành công;<br>2. Nhấn nút "Hoàn tác" trong vòng 5 giây;<br>3. Kiểm tra trạng thái | Thời gian: $T = 2.5\text{s} \le 5.0\text{s}$ | Hệ thống khôi phục hồ sơ về trạng thái ngay trước đó trong CSDL; cập nhật lại số lượng đếm giai đoạn; ghi vết Activity Log | P1 - Cao |
| **TC_UC11_019** | Kiểm tra giai đoạn tuyển dụng không có hồ sơ nào (Rỗng) | Kiểm thử biên | BVA ($N = 0$) | Giai đoạn Đề nghị nhận việc chưa có hồ sơ nào | 1. Truy vấn danh sách hồ sơ tại giai đoạn Đề nghị nhận việc | Số lượng hồ sơ: $N = 0$ | Hệ thống trả về danh sách rỗng an toàn; số lượng đếm hiển thị 0; không phát sinh lỗi | P2 - Trung bình |
| **TC_UC11_020** | Kiểm tra giai đoạn tuyển dụng có đúng 1 hồ sơ (Biên min) | Kiểm thử biên | BVA ($N = 1$) | Giai đoạn Phỏng vấn chỉ có 1 hồ sơ duy nhất | 1. Xem danh sách;<br>2. Chuyển hồ sơ duy nhất đó sang Offer | Số lượng hồ sơ: $N = 1$ | Chuyển trạng thái thành công; số lượng giai đoạn Phỏng vấn về 0; Offer tăng lên 1 | P2 - Trung bình |
| **TC_UC11_021** | Kiểm tra giai đoạn tuyển dụng chứa số lượng lớn hồ sơ (50 hồ sơ) | Kiểm thử hiệu năng / Biên | BVA ($N = 50$) | Giai đoạn Sàng lọc có 50 hồ sơ đang chờ duyệt | 1. Tải danh sách hồ sơ trong giai đoạn;<br>2. Phân trang hoặc tải toàn bộ | Số lượng hồ sơ: $N = 50$ | Hệ thống xử lý và hiển thị đầy đủ 50 hồ sơ; thời gian phản hồi API $< 1.5\text{s}$ | P1 - Cao |
| **TC_UC11_022** | Kiểm tra độ dài lý do từ chối tại biên tối thiểu (1 ký tự) | Kiểm thử biên | BVA ($L = 1$) | Đang chuyển hồ sơ sang trạng thái Từ chối | 1. Nhập lý do từ chối đúng 1 ký tự;<br>2. Xác nhận | Lý do: `"K"` | Hệ thống chấp nhận; lưu lý do hợp lệ vào CSDL; chuyển trạng thái thành công | P2 - Trung bình |
| **TC_UC11_023** | Kiểm tra độ dài lý do từ chối tại biên tối đa (500 ký tự) | Kiểm thử biên | BVA ($L = 500$) | Đang chuyển hồ sơ sang trạng thái Từ chối | 1. Nhập lý do từ chối đúng 500 ký tự hợp lệ;<br>2. Xác nhận | Chuỗi văn bản dài 500 ký tự | Hệ thống chấp nhận; lưu toàn vẹn 500 ký tự; chuyển trạng thái thành công | P1 - Cao |
| **TC_UC11_024** | Chặn lưu lý do từ chối vượt quá độ dài tối đa (501 ký tự) | Kiểm thử biên | BVA ($L = 501$) | Đang chuyển hồ sơ sang trạng thái Từ chối | 1. Nhập lý do từ chối dài 501 ký tự;<br>2. Xác nhận | Chuỗi văn bản 501 ký tự | Hệ thống chặn gửi yêu cầu; thông báo lỗi: Lý do từ chối không được vượt quá 500 ký tự | P2 - Trung bình |
| **TC_UC11_025** | Lọc theo vị trí tuyển dụng không có bất kỳ hồ sơ nào | Kiểm thử ngoại lệ | Empty State Testing | Chọn vị trí tuyển dụng mới tạo chưa có ứng viên nộp hồ sơ | 1. Áp dụng bộ lọc vị trí mới tạo | Vị trí: Giám đốc Tài chính (CFO) | Hệ thống trả về danh sách rỗng cho tất cả các giai đoạn; thông báo không có hồ sơ phù hợp | P2 - Trung bình |
| **TC_UC11_026** | Mất kết nối CSDL hoặc mạng khi đang cập nhật trạng thái (EX_05) | Kiểm thử chịu lỗi | Ngoại lệ EX_05 | Gửi yêu cầu cập nhật trạng thái trong điều kiện ngắt kết nối mạng | 1. Gửi lệnh chuyển trạng thái;<br>2. Giả lập mất kết nối mạng | Mất kết nối Internet / Database | Báo lỗi EX_05: Mất kết nối máy chủ; trạng thái hồ sơ trong CSDL không bị thay đổi (Rollback) | P1 - Cao |
| **TC_UC11_027** | Máy chủ CSDL trả về mã lỗi HTTP 500 / Transaction Rollback | Kiểm thử tích hợp | Server Error Handling | Mock server CSDL trả về lỗi Internal Server Error (500) | 1. Gửi yêu cầu chuyển trạng thái khi server lỗi | Mã phản hồi: HTTP 500 | Hệ thống thực hiện rollback transaction; giữ nguyên trạng thái cũ; thông báo lỗi hệ thống | P1 - Cao |
| **TC_UC11_028** | Phiên làm việc hết hạn trong quá trình thao tác chuyển trạng thái | Kiểm thử bảo mật | Session Timeout | Token xác thực người dùng hết hạn trong lúc thao tác | 1. Thực hiện chuyển trạng thái khi Token hết hiệu lực | JWT Token = Expired | Chặn yêu cầu; từ chối cập nhật CSDL; yêu cầu chuyên viên đăng nhập lại hệ thống | P1 - Cao |
| **TC_UC11_029** | Tự động ghi vết sự kiện chuyển trạng thái vào Activity Log | Kiểm thử chức năng / Audit | Use Case Flow | Thực hiện chuyển trạng thái thành công từ Mới sang Sàng lọc | 1. Chuyển trạng thái;<br>2. Truy vấn nhật ký hoạt động của hồ sơ | Bản ghi chuyển trạng thái | Nhật ký ghi nhận chính xác: Mã HR, Thời gian thực hiện, Trạng thái cũ $\rightarrow$ Trạng thái mới | P1 - Cao |
| **TC_UC11_030** | Tự động kích hoạt email thông báo khi chuyển sang trạng thái Phỏng vấn | Kiểm thử tích hợp | Integration Testing | Hệ thống có cấu hình bật tự động gửi email thông báo | 1. Chuyển trạng thái hồ sơ sang Phỏng vấn | Cấu hình auto-email = Bật | Hệ thống kích hoạt hàng đợi gửi email thông báo mời phỏng vấn đến ứng viên thành công | P2 - Trung bình |
| **TC_UC11_031** | Đồng bộ dữ liệu trạng thái mới sang bảng Danh sách ứng viên | Kiểm thử tích hợp | Data Consistency | Vừa cập nhật trạng thái ứng viên trong quy trình tuyển dụng | 1. Chuyển sang màn hình danh sách ứng viên tổng thể;<br>2. Kiểm tra hồ sơ | Hồ sơ: Nguyễn Văn An | Trạng thái hồ sơ trên màn hình danh sách đồng bộ chính xác với trạng thái mới cập nhật | P1 - Cao |
| **TC_UC11_032** | Xử lý xung đột tương tranh khi 2 HR cập nhật cùng 1 hồ sơ (Optimistic Locking) | Kiểm thử tương tranh | Concurrency Testing | 2 chuyên viên HR mở cùng 1 hồ sơ ứng viên ở trạng thái Mới | 1. HR1 chuyển sang Sàng lọc;<br>2. Cùng thời điểm HR2 chuyển sang Từ chối | Thao tác đồng thời cùng phiên bản version | HR1 thành công; HR2 nhận thông báo: Hồ sơ đã được cập nhật bởi chuyên viên khác (Version Conflict) | P1 - Cao |
| **TC_UC11_033** | Chống tấn công XSS / HTML Injection trong nội dung lý do từ chối | Kiểm thử bảo mật | Security Testing | Đang thực hiện chuyển hồ sơ sang trạng thái Từ chối | 1. Nhập mã script vào ô lý do từ chối;<br>2. Xác nhận lưu | Lý do: `<script>alert('XSS_Test')</script>` | Hệ thống khử mã độc (sanitize/encode HTML entity); lưu văn bản an toàn vào CSDL; không kích hoạt mã độc | P1 - Cao |
| **TC_UC11_034** | Chống tấn công SQL Injection khi lọc quy trình theo vị trí tuyển dụng | Kiểm thử bảo mật | Security Testing | Thực hiện lọc danh sách quy trình theo mã vị trí | 1. Nhập chuỗi SQLi vào tham số lọc vị trí tuyển dụng | Tham số: `' OR 1=1 --` | Hệ thống sử dụng Prepared Statement/ORM; không bị rò rỉ dữ liệu hoặc lỗi cú pháp SQL | P1 - Cao |
| **TC_UC11_035** | Kiểm tra tính nhất quán số lượng tổng hợp trước và sau khi chuyển trạng thái | Kiểm thử chức năng | Data Consistency | Giai đoạn Mới có 10 hồ sơ, Sàng lọc có 5 hồ sơ | 1. Chuyển 1 hồ sơ từ Mới sang Sàng lọc;<br>2. Kiểm tra số lượng | Tổng số hồ sơ = 15 | Số lượng giai đoạn Mới giảm còn 9, Sàng lọc tăng lên 6; tổng số hồ sơ toàn quy trình không đổi | P2 - Trung bình |
| **TC_UC11_036** | Chống gửi trùng lặp yêu cầu cập nhật liên tiếp (Idempotency) | Kiểm thử độ tin cậy | Reliability Testing | Thao tác gửi yêu cầu chuyển trạng thái | 1. Kích hoạt liên tiếp 2 yêu cầu cập nhật trạng thái trong 100ms | Cùng payload và Idempotency-Key | Chỉ 1 yêu cầu được xử lý và ghi CSDL; yêu cầu thứ 2 bị bỏ qua an toàn; không tạo log trùng lặp | P2 - Trung bình |
| **TC_UC11_037** | Cập nhật trạng thái thành công khi đang áp dụng đồng thời bộ lọc và tìm kiếm | Kiểm thử tích hợp | Integration Flow | Đang lọc theo vị trí Java Dev và từ khóa tìm kiếm "An" | 1. Chọn hồ sơ trong kết quả lọc;<br>2. Chuyển trạng thái;<br>3. Kiểm tra | Bộ lọc kép: Job + Tên | Trạng thái hồ sơ được cập nhật thành công; kết quả lọc và tìm kiếm vẫn được duy trì nhất quán | P2 - Trung bình |
| **TC_UC11_038** | Kiểm tra toàn vẹn dữ liệu khi cập nhật hồ sơ không tồn tại hoặc đã xóa | Kiểm thử nghiệp vụ / DB | Data Integrity | Hồ sơ ứng viên đã bị xóa khỏi hệ thống trong CSDL | 1. Gửi yêu cầu chuyển trạng thái với Candidate ID không tồn tại | Candidate ID = 999999 (Invalid ID) | Hệ thống từ chối cập nhật; trả về mã lỗi 404 Not Found; bảo toàn toàn vẹn cơ sở dữ liệu | P1 - Cao |
