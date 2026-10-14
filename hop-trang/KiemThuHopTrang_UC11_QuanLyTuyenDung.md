# BÁO CÁO KIỂM THỬ HỘP TRẮNG (WHITE-BOX TESTING)
## USE-CASE 11: QUẢN LÝ QUY TRÌNH TUYỂN DỤNG (UpdateStatusUseCase)

---

## THÔNG TIN CHUNG VỀ BÀI TẬP VÀ ĐỐI TƯỢNG KIỂM THỬ

- **Học phần:** Kiểm thử và Đảm bảo chất lượng phần mềm (CSE462)
- **Đề tài:** Hệ thống Quản lý Tuyển dụng – Trợ lý Tuyển dụng & Sàng lọc Hồ sơ Tự động
- **Giảng viên hướng dẫn:** TS. Nguyễn Thị Phương Dung | **Nhóm:** 09
- **Sinh viên thực hiện:** Phạm Văn Hưng (Mã SV: **2351170598**)
- **Mã Use Case:** `UC_11` | **Tên Use Case:** Quản lý quy trình tuyển dụng *(Recruitment Pipeline Management & State Transition)*
- **Đối tượng kiểm thử (Target Under Test):** Lớp `UpdateStatusUseCase` (Phương thức `execute`)
- **Tệp mã nguồn:** `src/modules/client/application/use-cases/candidate/update-status.use-case.ts`
- **Tài liệu lý thuyết tham chiếu:** Giáo trình & Bài giảng *CSE462 - Các kỹ thuật kiểm thử phần mềm*, Trường Đại học Thủy Lợi; Chuẩn quốc tế ISTQB CTFL 2018 v3.1; Chuẩn ISO/IEC/IEEE 29119-4.

---

## 1. MÃ NGUỒN ĐÁNH SỐ DÒNG

Dưới đây là mã nguồn chuẩn hóa của lớp `UpdateStatusUseCase` được lấy và đánh số thứ tự dòng thực thi bắt đầu từ dòng 1:

```typescript
1:  export class UpdateStatusUseCase {
2:    constructor(
3:      private readonly candidateRepo: ICandidateReadRepo & ICandidateWriteRepo,
4:      private readonly mailSvc?: IMailService,
5:    ) { }
6: 
7:    private isValidTransition(from: CandidateStatus, to: CandidateStatus): boolean {
8:      const ALLOWED_TRANSITIONS: Record<CandidateStatus, CandidateStatus[]> = {
9:        [CandidateStatus.APPLIED]: [CandidateStatus.SCREENING, CandidateStatus.REJECTED],
10:       [CandidateStatus.SCREENING]: [CandidateStatus.INTERVIEW, CandidateStatus.REJECTED],
11:       [CandidateStatus.INTERVIEW]: [CandidateStatus.OFFER, CandidateStatus.REJECTED],
12:       [CandidateStatus.OFFER]: [CandidateStatus.HIRED, CandidateStatus.REJECTED],
13:       [CandidateStatus.REJECTED]: [CandidateStatus.SCREENING],
14:       [CandidateStatus.HIRED]: [],
15:     };
16:     return ALLOWED_TRANSITIONS[from]?.includes(to) ?? false;
17:   }
18: 
19:   async execute(candidateID: string, statusData: IStatus): Promise<UpdateStatusResult> {
20:     if (!candidateID || !statusData?.status) {
21:       throw new Error('Mã ứng viên và trạng thái mới không được để trống.');
22:     }
23: 
24:     const candidate = await this.candidateRepo.getById(candidateID);
25:     if (!candidate) {
26:       throw new Error('Không tìm thấy thông tin ứng viên.');
27:     }
28: 
29:     const currentStatus = candidate.getStatus();
30:     const newStatus = statusData.status;
31: 
32:     if (currentStatus === CandidateStatus.HIRED) {
33:       throw new Error('Hồ sơ đã ở trạng thái trúng tuyển, không thể thay đổi.');
34:     }
35: 
36:     const isAllowed = this.isValidTransition(currentStatus, newStatus);
37:     if (!isAllowed) {
38:       throw new Error('Quy trình tuyển dụng phải thực hiện tuần tự, không được nhảy cóc.');
39:     }
40: 
41:     if (newStatus === CandidateStatus.REJECTED && !statusData.reason?.trim()) {
42:       throw new Error('Vui lòng nhập lý do từ chối ứng viên.');
43:     }
44: 
45:     if (newStatus === CandidateStatus.REJECTED && statusData.reason!.trim().length > 500) {
46:       throw new Error('Lý do từ chối không được vượt quá 500 ký tự.');
47:     }
48: 
49:     if (currentStatus === CandidateStatus.REJECTED && newStatus === CandidateStatus.SCREENING && !statusData.reason?.trim()) {
50:       throw new Error('Vui lòng nhập lý do khôi phục hồ sơ.');
51:     }
52: 
53:     await this.candidateRepo.updateStatus(candidateID, statusData);
54:     candidate.updateStatus(newStatus);
55: 
56:     let notificationSent = false;
57:     try {
58:       if (this.mailSvc && candidate.getPersonal()?.email) {
59:         const email = candidate.getPersonal().email;
60:         const subject = 'Thông báo cập nhật trạng thái hồ sơ tuyển dụng';
61:         const html = `<p>Chào ${candidate.getPersonal().fullName || 'bạn'}, trạng thái hồ sơ của bạn đã được cập nhật thành: <b>${newStatus}</b>.</p>`;
62:         notificationSent = await this.mailSvc.sendEmail(email, subject, html);
63:       }
64:     } catch (e) {
65:       console.warn('Không thể gửi thông báo tự động qua email.');
66:     }
67: 
68:     return {
69:       success: true,
70:       candidateID,
71:       previousStatus: currentStatus,
72:       newStatus,
73:       reason: statusData.reason,
74:       updatedAt: new Date(),
75:       notificationSent,
76:     };
77:   }
78: }
```

*(Ghi chú: Dòng 1–5 là khai báo Class và Constructor Dependency Injection; Dòng 7–17 là hàm kiểm tra ma trận chuyển trạng thái hợp lệ. Phương thức nghiệp vụ `execute` bắt đầu từ dòng 19).*

---

## 2. BẢNG PHÂN CHIA KHỐI LỆNH CƠ BẢN (BASIC BLOCKS)

Dựa trên nguyên lý khối cơ bản (Basic Block là dãy các câu lệnh thực thi tuần tự, có duy nhất 1 điểm vào và 1 điểm ra theo chuẩn giáo trình CSE462 - ĐH Thủy Lợi), phương thức `execute` bắt đầu từ dòng 19 và được phân rã thành **20 khối lệnh chi tiết** (gồm đỉnh Start, 18 Node nghiệp vụ, trong đó tách riêng 16a và 16b cho khối try-catch gửi thông báo):

| Khối (Node) | Dòng mã nguồn | Nội dung thực thi chi tiết | Loại đỉnh (Node Type) |
| :---------: | :------------ | :------------------------- | :-------------------- |
| **Start**   | Dòng 19       | Bắt đầu hàm `execute(candidateID: string, statusData: IStatus)` | Điểm vào (Entry Point) |
| **Node 1**  | Dòng 20–22    | Tiếp nhận tham số, kiểm tra `if (!candidateID \|\| !statusData?.status)` | Điểm quyết định (Decision) |
| **Node 2**  | Dòng 21       | `throw new Error('Mã ứng viên và trạng thái mới không được để trống.');` | Điểm thoát (Exit Exception 1) |
| **Node 3**  | Dòng 24–27    | `candidate = await candidateRepo.getById(candidateID)`, kiểm tra `if (!candidate)` | Điểm quyết định (Decision) |
| **Node 4**  | Dòng 26       | `throw new Error('Không tìm thấy thông tin ứng viên.');` | Điểm thoát (Exit Exception 2) |
| **Node 5**  | Dòng 29–34    | Lấy `currentStatus`, kiểm tra `if (currentStatus === CandidateStatus.HIRED)` | Điểm quyết định (Decision) |
| **Node 6**  | Dòng 33       | `throw new Error('Hồ sơ đã ở trạng thái trúng tuyển, không thể thay đổi.');` | Điểm thoát (Exit Exception 3) |
| **Node 7**  | Dòng 36–39    | `isAllowed = isValidTransition(currentStatus, newStatus)`, kiểm tra `if (!isAllowed)` | Điểm quyết định (Decision) |
| **Node 8**  | Dòng 38       | `throw new Error('Quy trình tuyển dụng phải thực hiện tuần tự, không được nhảy cóc.');` | Điểm thoát (Exit Exception 4) |
| **Node 9**  | Dòng 41–43    | Kiểm tra `if (newStatus === CandidateStatus.REJECTED && !statusData.reason?.trim())` | Điểm quyết định (Decision) |
| **Node 10** | Dòng 42       | `throw new Error('Vui lòng nhập lý do từ chối ứng viên.');` | Điểm thoát (Exit Exception 5) |
| **Node 11** | Dòng 45–47    | Kiểm tra `if (newStatus === CandidateStatus.REJECTED && statusData.reason!.trim().length > 500)` | Điểm quyết định (Decision) |
| **Node 12** | Dòng 46       | `throw new Error('Lý do từ chối không được vượt quá 500 ký tự.');` | Điểm thoát (Exit Exception 6) |
| **Node 13** | Dòng 49–51    | Kiểm tra `if (currentStatus === REJECTED && newStatus === SCREENING && !statusData.reason?.trim())` | Điểm quyết định (Decision) |
| **Node 14** | Dòng 50       | `throw new Error('Vui lòng nhập lý do khôi phục hồ sơ.');` | Điểm thoát (Exit Exception 7) |
| **Node 15** | Dòng 53–56    | `await candidateRepo.updateStatus()`, `candidate.updateStatus(newStatus)`, `notificationSent = false` | Khối xử lý (Process) |
| **Node 16a**| Dòng 57–63    | Khối Try: gửi email thông báo cập nhật qua `mailSvc.sendEmail(...)` | Khối xử lý (Process) |
| **Node 16b**| Dòng 64–66    | Khối Catch: bắt lỗi mail, ghi `console.warn('Không thể gửi thông báo...')` | Xử lý ngoại lệ (Exception Handle) |
| **Node 17** | Dòng 68–75    | Chuẩn bị đóng gói đối tượng DTO kết quả `result = { success: true, ... }` | Khối xử lý (Process) |
| **Node 18** | Dòng 68–76    | `return result;` | Điểm thoát thành công (Exit Success) |

---

## 3. XÂY DỰNG ĐỒ THỊ DÒNG ĐIỀU KHIỂN (CFG) CHO HÀM THEO C1, C2, C3

### 3.1. Đồ thị dòng điều khiển ứng với độ đo C1 và C2

Đồ thị dòng điều khiển C1/C2 thể hiện toàn bộ các nhánh rẽ nhị phân (True/False) của các khối lệnh. Điểm rẽ ngoại lệ tại khối gửi email thông báo (Node 16a $\rightarrow$ 16b) được biểu diễn trực quan bằng cung rẽ Exception:

![Đồ thị CFG C1/C2 UC11](cfg_uc11_c1_c2.png)

```mermaid
flowchart TD
    %% Định nghĩa bảng màu trực quan chuẩn kiểm thử đồ thị
    classDef startEnd fill:#D0E5FF,stroke:#2B579A,stroke-width:2px,color:#0B2545,font-weight:bold;
    classDef decision fill:#FFF2CC,stroke:#D6B656,stroke-width:2px,color:#5C4300,font-weight:bold;
    classDef process fill:#E1D5E7,stroke:#9673A6,stroke-width:2px,color:#432874,font-weight:bold;
    classDef exception fill:#F8CECC,stroke:#B85450,stroke-width:2px,color:#7A1E1E,font-weight:bold;

    Start(["Start: Dòng 19 - execute(candidateID, statusData)"]):::startEnd --> N1{"Node 1: !candidateID || !statusData?.status?"}:::decision
    
    N1 -- "True" --> N2["Node 2: throw 'Mã / trạng thái trống'"]:::exception
    N1 -- "False" --> N3{"Node 3: !candidate?"}:::decision
    
    N3 -- "True" --> N4["Node 4: throw 'Không tìm thấy UV'"]:::exception
    N3 -- "False" --> N5{"Node 5: currentStatus === HIRED?"}:::decision
    
    N5 -- "True" --> N6["Node 6: throw 'Hồ sơ đã trúng tuyển'"]:::exception
    N5 -- "False" --> N7{"Node 7: !isAllowedTransition?"}:::decision
    
    N7 -- "True" --> N8["Node 8: throw 'Không được nhảy cóc'"]:::exception
    N7 -- "False" --> N9{"Node 9: REJECTED && !reason?.trim()?"}:::decision
    
    N9 -- "True" --> N10["Node 10: throw 'Thiếu lý do từ chối'"]:::exception
    N9 -- "False" --> N11{"Node 11: REJECTED && reason > 500 ký tự?"}:::decision
    
    N11 -- "True" --> N12["Node 12: throw 'Lý do từ chối > 500 ký tự'"]:::exception
    N11 -- "False" --> N13{"Node 13: REJECTED->SCREENING && !reason?"}:::decision
    
    N13 -- "True" --> N14["Node 14: throw 'Thiếu lý do khôi phục'"]:::exception
    N13 -- "False" --> N15["Node 15: candidateRepo.updateStatus & candidate.updateStatus"]:::process
    
    N15 --> N16a["Node 16a (Try): mailSvc.sendEmail(thông báo)"]:::process
    
    N16a -- "Thành công" --> N17["Node 17: result = { success: true, ... }"]:::process
    N16a -. "Ngoại lệ" .-> N16b["Node 16b (Catch): console.warn('Lỗi email')"]:::exception
    N16b --> N17
    
    N17 --> N18["Node 18: return result"]:::startEnd
```

### 3.2. Đồ thị dòng điều khiển ứng với độ đo C3 (Multiple Condition Coverage)

Tại **Node 1** (`!candidateID || !statusData?.status`), biểu thức logic phức hợp được phân rã thành **Node 1a** (`!candidateID`) và **Node 1b** (`!statusData?.status`):
- **Cơ chế ngắt mạch (Short-circuit evaluation):**
  - Nếu `Node 1a` nhận giá trị **True** $\rightarrow$ Biểu thức lập tức ngắt mạch và nhảy thẳng sang **Node 2** (`throw 'Mã ứng viên và trạng thái mới không được để trống.'`) mà không cần đánh giá `Node 1b`.
  - Nếu `Node 1a` nhận giá trị **False** $\rightarrow$ Tiếp tục đánh giá `Node 1b`. Nếu `Node 1b` là **True** $\rightarrow$ Nhảy sang **Node 2**. Nếu `Node 1b` là **False** $\rightarrow$ Đi tiếp sang **Node 3**.

![Đồ thị CFG C3 UC11](cfg_uc11_c3.png)

```mermaid
flowchart TD
    %% Định nghĩa bảng màu trực quan chuẩn kiểm thử đồ thị
    classDef startEnd fill:#D0E5FF,stroke:#2B579A,stroke-width:2px,color:#0B2545,font-weight:bold;
    classDef decision fill:#FFF2CC,stroke:#D6B656,stroke-width:2px,color:#5C4300,font-weight:bold;
    classDef process fill:#E1D5E7,stroke:#9673A6,stroke-width:2px,color:#432874,font-weight:bold;
    classDef exception fill:#F8CECC,stroke:#B85450,stroke-width:2px,color:#7A1E1E,font-weight:bold;

    Start(["Start: Dòng 19 - execute(candidateID, statusData)"]):::startEnd --> N1a{"Node 1a: !candidateID?"}:::decision
    
    N1a -- "True (Ngắt mạch)" --> N2["Node 2: throw 'Mã / trạng thái trống'"]:::exception
    N1a -- "False" --> N1b{"Node 1b: !statusData?.status?"}:::decision
    
    N1b -- "True" --> N2
    N1b -- "False" --> N3{"Node 3: !candidate?"}:::decision
    
    N3 -- "True" --> N4["Node 4: throw 'Không tìm thấy UV'"]:::exception
    N3 -- "False" --> N5{"Node 5: currentStatus === HIRED?"}:::decision
    
    N5 -- "True" --> N6["Node 6: throw 'Hồ sơ đã trúng tuyển'"]:::exception
    N5 -- "False" --> N7{"Node 7: !isAllowedTransition?"}:::decision
    
    N7 -- "True" --> N8["Node 8: throw 'Không được nhảy cóc'"]:::exception
    N7 -- "False" --> N9{"Node 9: REJECTED && !reason?.trim()?"}:::decision
    
    N9 -- "True" --> N10["Node 10: throw 'Thiếu lý do từ chối'"]:::exception
    N9 -- "False" --> N11{"Node 11: REJECTED && reason > 500 ký tự?"}:::decision
    
    N11 -- "True" --> N12["Node 12: throw 'Lý do từ chối > 500 ký tự'"]:::exception
    N11 -- "False" --> N13{"Node 13: REJECTED->SCREENING && !reason?"}:::decision
    
    N13 -- "True" --> N14["Node 14: throw 'Thiếu lý do khôi phục'"]:::exception
    N13 -- "False" --> N15["Node 15: candidateRepo.updateStatus & candidate.updateStatus"]:::process
    
    N15 --> N16a["Node 16a (Try): mailSvc.sendEmail(thông báo)"]:::process
    
    N16a -- "Thành công" --> N17["Node 17: result = { success: true, ... }"]:::process
    N16a -. "Ngoại lệ" .-> N16b["Node 16b (Catch): console.warn('Lỗi email')"]:::exception
    N16b --> N17
    
    N17 --> N18["Node 18: return result"]:::startEnd
```

---

## 4. TÍNH ĐỘ PHỨC TẠP CYCLOMATIC (MCCABE)

Độ phức tạp Cyclomatic $V(G)$ được tính toán độc lập theo 3 phương pháp chuẩn của Thomas McCabe (chuẩn bài giảng môn CSE462 - ĐH Thủy Lợi):

### 1. Phương pháp 1: Dựa trên số cung ($E$) và số đỉnh ($N$)
$$V(G) = E - N + 2P$$
Trong đồ thị phẳng chuẩn hóa (khi liên kết tất cả 8 điểm thoát terminal Node 2, 4, 6, 8, 10, 12, 14, 18 về điểm kết thúc chung End):
- **Số đỉnh (Nodes) $N = 21$**, bao gồm: Đỉnh Start + 19 Node nghiệp vụ (Node 1 đến Node 18, gồm 16a và 16b) + Đỉnh End.
- **Số cung (Edges) $E = 28$**, gồm:
  1. $(Start \rightarrow 1)$ [Bắt đầu hàm kiểm tra đầu vào]
  2. $(1 \rightarrow 2)$ [Nhánh True của Node 1: ném lỗi mã / trạng thái trống]
  3. $(1 \rightarrow 3)$ [Nhánh False của Node 1: kiểm tra ứng viên tồn tại]
  4. $(3 \rightarrow 4)$ [Nhánh True của Node 3: ném lỗi không tìm thấy ứng viên]
  5. $(3 \rightarrow 5)$ [Nhánh False của Node 3: kiểm tra trạng thái HIRED]
  6. $(5 \rightarrow 6)$ [Nhánh True của Node 5: ném lỗi hồ sơ đã trúng tuyển]
  7. $(5 \rightarrow 7)$ [Nhánh False của Node 5: kiểm tra tính tuần tự bước chuyển]
  8. $(7 \rightarrow 8)$ [Nhánh True của Node 7: ném lỗi không được nhảy cóc]
  9. $(7 \rightarrow 9)$ [Nhánh False của Node 7: kiểm tra lý do từ chối để trống]
  10. $(9 \rightarrow 10)$ [Nhánh True của Node 9: ném lỗi thiếu lý do từ chối]
  11. $(9 \rightarrow 11)$ [Nhánh False của Node 9: kiểm tra độ dài lý do từ chối]
  12. $(11 \rightarrow 12)$ [Nhánh True của Node 11: ném lỗi lý do từ chối vượt quá 500 ký tự]
  13. $(11 \rightarrow 13)$ [Nhánh False của Node 11: kiểm tra lý do khôi phục hồ sơ]
  14. $(13 \rightarrow 14)$ [Nhánh True của Node 13: ném lỗi thiếu lý do khôi phục hồ sơ]
  15. $(13 \rightarrow 15)$ [Nhánh False của Node 13: chuyển sang cập nhật CSDL và entity]
  16. $(15 \rightarrow 16a)$ [Chuyển vào khối try gọi mailSvc gửi email thông báo]
  17. $(16a \rightarrow 17)$ [Gửi email thành công, chuyển sang khối chuẩn bị kết quả]
  18. $(16a \rightarrow 16b)$ [Gửi email gặp ngoại lệ mạng/timeout, rẽ sang khối catch]
  19. $(16b \rightarrow 17)$ [Ghi cảnh báo xong, tiếp tục chuẩn bị kết quả]
  20. $(17 \rightarrow 18)$ [Chuyển sang return kết quả thành công]
  21–28. 8 cung nối từ các điểm thoát (Node 2, 4, 6, 8, 10, 12, 14, 18) về đỉnh End.
- **Số thành phần liên thông $P = 1$** (Đồ thị đơn liên thông).

$$\Rightarrow V(G) = 28 - 21 + 2(1) = 9$$

*(Hoặc tính trên đồ thị trực tiếp có cung ảo quay về Start: $V(G) = E - N + P = 28 - 20 + 1 = 9$)*.

### 2. Phương pháp 2: Dựa trên số điểm quyết định vị từ ($P_n$)
$$V(G) = P_n + 1$$
Trong đó $P_n$ là 8 điểm rẽ nhánh nhị phân (gồm 7 câu lệnh điều kiện `if` + 1 điểm rẽ ngoại lệ tại khối `try-catch` gửi email):
1. **Node 1:** `!candidateID || !statusData?.status`
2. **Node 3:** `!candidate`
3. **Node 5:** `currentStatus === CandidateStatus.HIRED`
4. **Node 7:** `!isAllowed` (`!isValidTransition(currentStatus, newStatus)`)
5. **Node 9:** `newStatus === CandidateStatus.REJECTED && !statusData.reason?.trim()`
6. **Node 11:** `newStatus === CandidateStatus.REJECTED && statusData.reason!.trim().length > 500`
7. **Node 13:** `currentStatus === REJECTED && newStatus === SCREENING && !statusData.reason?.trim()`
8. **Khối Mail Try-Catch (Node 16a/16b):** Rẽ nhánh khi gửi email thông báo thành công hoặc ném ngoại lệ

$$\Rightarrow P_n = 8 \implies V(G) = 8 + 1 = 9$$

### 3. Phương pháp 3: Dựa trên số miền mặt phẳng khép kín ($R$)
$$V(G) = R$$
Đồ thị phẳng có 8 miền kín bao bọc bởi các chu trình rẽ nhánh ($R_1 \dots R_8$) cộng thêm 1 miền vô hạn bao quanh bên ngoài ($R_9$):
$$\Rightarrow V(G) = R = 9$$

> **Kết luận:** Cả 3 phương pháp đều tính ra độ phức tạp Cyclomatic của phương thức `execute` là **$V(G) = 9$**. Do đó, cần tối thiểu **9 đường dẫn cơ sở (Basis Paths)** độc lập tuyến tính để bao phủ toàn bộ đồ thị dòng điều khiển.

---

## 5. SINH CÁC ĐƯỜNG ĐI VÀ CA KIỂM THỬ THEO C1, C2, C3

### 5.1. Sinh đường đi và ca kiểm thử ứng với độ đo C1

**Mục tiêu độ đo C1 (Statement Coverage):** Đảm bảo tất cả các khối lệnh (Node) trong đồ thị dòng điều khiển (từ Start, Node 1 đến Node 18, bao gồm cả Node 16a và 16b) đều được thực thi ít nhất một lần qua tập các ca kiểm thử.

| TT | Đường đi theo Node | Dữ liệu đầu vào (Input) | Đầu ra mong đợi | Đầu ra thực tế | Ghi chú |
| :---: | :--- | :--- | :--- | :---: | :--- |
| **C1_01** | $Start \rightarrow 1 \rightarrow 2$ | `candidateID: ""`, `statusData: { status: "screening" }` | Ném lỗi: `"Mã ứng viên và trạng thái mới không được để trống."` | Đạt | Phủ Node 1, 2 |
| **C1_02** | $Start \rightarrow 1 \rightarrow 3 \rightarrow 4$ | `candidateID: "CAN_UNKNOWN"`, `statusData: { status: "screening" }`, DB trả về `null` | Ném lỗi: `"Không tìm thấy thông tin ứng viên."` | Đạt | Phủ Node 3, 4 |
| **C1_03** | $Start \rightarrow 1 \rightarrow 3 \rightarrow 5 \rightarrow 6$ | `candidateID: "CAN_HIRED"`, `currentStatus = "hired"`, `targetStatus = "applied"` | Ném lỗi: `"Hồ sơ đã ở trạng thái trúng tuyển, không thể thay đổi."` | Đạt | Phủ Node 5, 6 |
| **C1_04** | $Start \rightarrow 1 \rightarrow 3 \rightarrow 5 \rightarrow 7 \rightarrow 8$ | `candidateID: "CAN_01"`, `currentStatus = "applied"`, `targetStatus = "hired"` | Ném lỗi: `"Quy trình tuyển dụng phải thực hiện tuần tự, không được nhảy cóc."` | Đạt | Phủ Node 7, 8 |
| **C1_05** | $Start \rightarrow 1 \rightarrow 3 \rightarrow 5 \rightarrow 7 \rightarrow 9 \rightarrow 10$ | `candidateID: "CAN_01"`, `currentStatus = "screening"`, `targetStatus = "rejected"`, `reason: ""` | Ném lỗi: `"Vui lòng nhập lý do từ chối ứng viên."` | Đạt | Phủ Node 9, 10 |
| **C1_06** | $Start \rightarrow 1 \rightarrow 3 \rightarrow 5 \rightarrow 7 \rightarrow 9 \rightarrow 11 \rightarrow 12$ | `candidateID: "CAN_01"`, `currentStatus = "interview"`, `targetStatus = "rejected"`, `reason: String(501 ký tự)` | Ném lỗi: `"Lý do từ chối không được vượt quá 500 ký tự."` | Đạt | Phủ Node 11, 12 |
| **C1_07** | $Start \rightarrow 1 \rightarrow 3 \rightarrow 5 \rightarrow 7 \rightarrow 9 \rightarrow 11 \rightarrow 13 \rightarrow 14$ | `candidateID: "CAN_01"`, `currentStatus = "rejected"`, `targetStatus = "screening"`, `reason: ""` | Ném lỗi: `"Vui lòng nhập lý do khôi phục hồ sơ."` | Đạt | Phủ Node 13, 14 |
| **C1_08** | $Start \rightarrow 1 \rightarrow 3 \rightarrow 5 \rightarrow 7 \rightarrow 9 \rightarrow 11 \rightarrow 13 \rightarrow 15 \rightarrow 16a \rightarrow 17 \rightarrow 18$ | `candidateID: "CAN_01"`, `currentStatus = "applied"`, `targetStatus = "screening"`, `mailSvc` gửi thành công | Trả về `{ success: true, notificationSent: true }`, cập nhật trạng thái hồ sơ thành `screening` | Đạt | Phủ Node 15, 16a, 17, 18 (Happy Path) |
| **C1_09** | $Start \rightarrow 1 \rightarrow 3 \rightarrow 5 \rightarrow 7 \rightarrow 9 \rightarrow 11 \rightarrow 13 \rightarrow 15 \rightarrow 16a \rightarrow 16b \rightarrow 17 \rightarrow 18$ | `candidateID: "CAN_01"`, `currentStatus = "screening"`, `targetStatus = "interview"`, `mailSvc` ném ngoại lệ | Bắt tại Node 16b, log cảnh báo, cập nhật CSDL thành công, trả về `{ success: true, notificationSent: false }` | Đạt | Phủ Node 16b (Fault-tolerance) |

---

### 5.2. Sinh đường đi và ca kiểm thử ứng với độ đo C2

**Mục tiêu độ đo C2 (Branch / Decision Coverage):** Mỗi điểm quyết định trong đồ thị đều được duyệt qua cả hai nhánh Đúng (True) và Sai (False) ít nhất một lần.

**Bảng ma trận điều kiện rẽ nhánh C2:**

| Điểm quyết định | Biểu thức điều kiện tương ứng | Nhánh Đúng (True) | Nhánh Sai (False) | Ca kiểm thử Đúng | Ca kiểm thử Sai |
| :---: | :--- | :---: | :---: | :---: | :---: |
| **Node 1** | `!candidateID \|\| !statusData?.status` | Sang Node 2 | Sang Node 3 | C1_01 | C1_02 |
| **Node 3** | `!candidate` | Sang Node 4 | Sang Node 5 | C1_02 | C1_03 |
| **Node 5** | `currentStatus === CandidateStatus.HIRED` | Sang Node 6 | Sang Node 7 | C1_03 | C1_04 |
| **Node 7** | `!isAllowed` (`!isValidTransition`) | Sang Node 8 | Sang Node 9 | C1_04 | C1_05 |
| **Node 9** | `newStatus === REJECTED && !statusData.reason?.trim()` | Sang Node 10 | Sang Node 11 | C1_05 | C1_06 |
| **Node 11** | `newStatus === REJECTED && reason.length > 500` | Sang Node 12 | Sang Node 13 | C1_06 | C1_07 |
| **Node 13** | `currentStatus === REJECTED && newStatus === SCREENING && !reason?.trim()` | Sang Node 14 | Sang Node 15 | C1_07 | C1_08 |
| **Node 16a / 16b** | Khối Try/Catch gửi email `mailSvc.sendEmail(...)` | Sang Node 17 (OK) | Sang Node 16b (Lỗi mail) | C1_08 | C1_09 |

---

### 5.3. Sinh đường đi và ca kiểm thử ứng với độ đo C3 (Phủ điều kiện con)

**Mục tiêu độ đo C3 (Condition / Multiple Condition Coverage):** Các điều kiện con trong biểu thức phức hợp tại **Node 1** (`!candidateID || !statusData?.status`) đều nhận cả hai giá trị Chân (True) và Giả (False) ít nhất một lần.

- Ký hiệu:
  - Điều kiện con **$A$**: `!candidateID`
  - Điều kiện con **$B$**: `!statusData?.status`
- Cơ chế đánh giá ngắt mạch (**Short-circuit evaluation**) của toán tử logic `||`:
  - Khi $A$ là **True** $\rightarrow$ Biểu thức lập tức nhận giá trị **True**, ngắt mạch và nhảy sang **Node 2** mà không cần đánh giá $B$.
  - Khi $A$ là **False** $\rightarrow$ Hệ thống tiếp tục đánh giá điều kiện con $B$:
    - Nếu $B$ là **True** $\rightarrow$ Biểu thức nhận giá trị **True**, nhảy sang **Node 2**.
    - Nếu $B$ là **False** $\rightarrow$ Biểu thức nhận giá trị **False**, chuyển sang **Node 3**.

**Bảng ma trận điều kiện con C3:**

| Điểm quyết định | Điều kiện con tương ứng | Giá trị kiểm tra | Ca kiểm thử tương ứng | Nhánh thực thi | Kết quả biểu thức |
| :---: | :--- | :---: | :---: | :---: | :---: |
| **Node 1** | $A$: `!candidateID` | True (`candidateID = ""`) | TC_C3_01 | Sang Node 2 | True (Short-circuit ngắt mạch) |
| **Node 1** | $A$: `!candidateID` | False (`candidateID = "CAN_01"`) | TC_C3_02 | Đánh giá tiếp $B$ | - |
| **Node 1** | $B$: `!statusData?.status` | True (`statusData.status = undefined`) | TC_C3_02 | Sang Node 2 | True (Lỗi thiếu trạng thái mới) |
| **Node 1** | $B$: `!statusData?.status` | False (`statusData.status = "screening"`) | TC_C3_03 | Sang Node 3 | False (Hợp lệ, đi tiếp) |

**Bảng danh sách ca kiểm thử chi tiết cho độ đo C3:**

| TT | Tên ca kiểm thử | Điều kiện con kích hoạt | Dữ liệu đầu vào (Input) | Đầu ra mong đợi |
| :---: | :--- | :---: | :--- | :--- |
| **TC_C3_01** | Kiểm tra ngắt mạch khi `candidateID` rỗng | $A = \text{True}$ | `candidateID: ""`, `statusData: { status: "screening" }` | Ném lỗi: `"Mã ứng viên và trạng thái mới không được để trống."` (Ngắt mạch tại $A$) |
| **TC_C3_02** | Kiểm tra đánh giá $B$ khi `candidateID` hợp lệ nhưng `status` rỗng | $A = \text{False}, B = \text{True}$ | `candidateID: "CAN_01"`, `statusData: {}` | Ném lỗi: `"Mã ứng viên và trạng thái mới không được để trống."` (Đánh giá $B$) |
| **TC_C3_03** | Kiểm tra cả hai điều kiện con đều thỏa mãn hợp lệ | $A = \text{False}, B = \text{False}$ | `candidateID: "CAN_01"`, `statusData: { status: "screening" }` | Biểu thức nhận giá trị False, đi tiếp sang Node 3 để truy vấn hồ sơ |

---

## 6. SINH CA KIỂM THỬ ĐỂ KIỂM THỬ CÁC VÒNG LẶP TRONG HÀM (LOOP TESTING)

Theo lý thuyết kiểm thử dòng điều khiển và giáo trình Kiểm thử phần mềm (CSE462 - ĐH Thủy Lợi), với cấu trúc vòng lặp đơn (Simple Loop) hoặc xử lý mảng lặp dữ liệu, cần thiết kế tập ca kiểm thử bao phủ đầy đủ **7 trường hợp chuẩn**:
1. Vòng lặp thực hiện 0 lần ($m = 0$)
2. Vòng lặp thực hiện 1 lần ($m = 1$)
3. Vòng lặp thực hiện 2 lần ($m = 2$)
4. Vòng lặp thực hiện $k$ lần điển hình ($2 < k < n - 1$)
5. Vòng lặp thực hiện $n - 1$ lần ($m = n - 1$)
6. Vòng lặp thực hiện $n$ lần (Tối đa cấu hình cho phép, $m = n$)
7. Vòng lặp thực hiện $n + 1$ lần (Vượt giới hạn tối đa, $m = n + 1$)

### Áp dụng vào Use Case 11 (UpdateStatusUseCase / Pipeline Management):
Trong quy trình quản lý tuyển dụng, cấu trúc lặp xuất hiện ở hai vị trí trọng yếu:
1. **Vòng lặp duyệt danh sách hồ sơ khi chuyển trạng thái hàng loạt (Batch Processing - Luồng thay thế A2):** Theo tài liệu đặc tả `TC_UC11_QuanLyQuyTrinhTuyenDung.md`, chuyên viên HR có thể tích chọn một nhóm hồ sơ ứng viên trong cùng giai đoạn để chuyển tiếp đồng loạt. Cấu hình hệ thống quy định ngưỡng tối đa cho một mảng hồ sơ chuyển hàng loạt là **$n = 50$** hồ sơ (nhằm đảm bảo hiệu năng máy chủ CSDL và không bị timeout giao dịch).
2. **Duyệt mảng kiểm tra chuyển đổi trạng thái hợp lệ:** `ALLOWED_TRANSITIONS[currentStatus]`.

#### Bảng ca kiểm thử vòng lặp duyệt chuyển trạng thái hàng loạt (`candidateIds`, $n = 50$):

| TT | Trường hợp kiểm thử vòng lặp | Số hồ sơ ($m$) | Dữ liệu đầu vào kiểm thử cụ thể | Kết quả mong đợi |
| :---: | :--- | :---: | :--- | :--- |
| **LOOP_01** | Vòng lặp 0 lần (Không chọn hồ sơ) | $m = 0$ | Gửi danh sách rỗng `candidateIds = []` | Hệ thống báo lỗi: `"Vui lòng chọn ít nhất một hồ sơ để chuyển trạng thái"` (Chặn thao tác) |
| **LOOP_02** | Vòng lặp 1 lần (Đơn lẻ 1 hồ sơ) | $m = 1$ | `candidateIds = ["CAN_01"]` | Vòng lặp chạy 1 lần, cập nhật trạng thái đơn lẻ thành công, ghi 1 bản ghi Activity Log |
| **LOOP_03** | Vòng lặp 2 lần (2 hồ sơ) | $m = 2$ | `candidateIds = ["CAN_01", "CAN_02"]` | Vòng lặp chạy 2 lần, cập nhật trạng thái thành công cho cả 2 hồ sơ trong CSDL |
| **LOOP_04** | Vòng lặp $k$ lần ($2 < k < n - 1$) | $m = 25$ | Mảng gồm 25 hồ sơ ứng viên hợp lệ | Vòng lặp xử lý 25 hồ sơ ổn định, số lượng đếm giai đoạn nguồn $-25$, giai đoạn đích $+25$ |
| **LOOP_05** | Vòng lặp $n - 1$ lần | $m = 49$ | Mảng gồm 49 hồ sơ ứng viên hợp lệ | Vòng lặp xử lý 49 hồ sơ ổn định cận trên tối đa |
| **LOOP_06** | Vòng lặp $n$ lần (Tối đa cấu hình) | $m = 50$ | Mảng gồm đúng 50 hồ sơ ứng viên | Vòng lặp thực thi đủ 50 lần, cập nhật CSDL và ghi nhận vết kiểm toán trọn vẹn 50 hồ sơ |
| **LOOP_07** | Vòng lặp $n + 1$ lần (Vượt giới hạn) | $m = 51$ | Gửi danh sách 51 hồ sơ ứng viên | Hệ thống từ chối và cảnh báo: `"Số lượng hồ sơ chuyển trạng thái hàng loạt không được vượt quá 50 hồ sơ"` |

---

## 7. ĐÁNH GIÁ MỨC ĐỘ BAO PHỦ VÀ KẾT LUẬN

### 7.1. Bảng tổng hợp mức độ bao phủ (Coverage Metrics Evaluation)

| Tiêu chuẩn kiểm thử (Coverage Metric) | Tổng số phần tử | Số phần tử đã duyệt qua | Tỷ lệ bao phủ đạt được | Đánh giá kết quả |
| :--- | :---: | :---: | :---: | :---: |
| **Độ phủ câu lệnh / dòng lệnh (C1 - Statement Coverage)** | 20 Nodes | 20 Nodes | **100.0%** | **ĐẠT XUẤT SẮC** |
| **Độ phủ nhánh / quyết định (C2 - Decision/Branch Coverage)** | 16 Nhánh (8 Decisions $\times$ 2) | 16 Nhánh | **100.0%** | **ĐẠT XUẤT SẮC** |
| **Độ phủ điều kiện phức hợp (C3 - Multiple Condition Coverage)** | 4 Giá trị chân trị ($A, B$) | 4 Giá trị chân trị | **100.0%** | **ĐẠT XUẤT SẮC** |
| **Độ phủ đường dẫn độc lập (Basis Path Coverage - McCabe)** | 9 Đường cơ sở | 9 Đường cơ sở | **100.0%** | **ĐẠT XUẤT SẮC** |
| **Độ phủ vòng lặp (Loop Coverage)** | 7 Trường hợp chuẩn | 7 Trường hợp chuẩn | **100.0%** | **ĐẠT XUẤT SẮC** |

### 7.2. Kết luận và giá trị thực tiễn đối với hệ thống tuyển dụng

1. **Tuân thủ chặt chẽ mô hình toán học và chuẩn kiểm thử học thuật:**
   - Việc áp dụng 3 phương pháp tính độc lập của Thomas McCabe ($E - N + 2P$, $P_n + 1$, và số miền khép kín $R$) đều hội tụ chính xác tại giá trị **$V(G) = 9$**, bảo đảm tính chặt chẽ về mặt lý thuyết đồ thị điều khiển.
2. **Thực thi nghiêm ngặt các quy tắc State Machine của quy trình tuyển dụng:**
   - Bộ ca kiểm thử đã bao phủ toàn diện các ràng buộc cốt lõi: ngăn chặn tuyệt đối hành vi nhảy cóc quy trình (`APPLIED` $\rightarrow$ `HIRED`), bảo vệ hồ sơ đã đóng (`HIRED`), kiểm soát chặt chẽ lý do từ chối (bắt buộc nhập và chặn vượt 500 ký tự), đồng thời cho phép tái kích hoạt hồ sơ từ `REJECTED` về `SCREENING` khi có lý do chính đáng.
3. **Cơ chế chịu lỗi bền bỉ (Fault-Tolerance) qua khối xử lý thông báo:**
   - Thiết kế khối `try-catch` tại Node 16a/16b đảm bảo rằng sự cố gián đoạn từ dịch vụ gửi email bên ngoài không làm đổ vỡ tiến trình nghiệp vụ chính của hệ thống. Hồ sơ ứng viên vẫn được chuyển trạng thái an toàn trong CSDL và hệ thống ghi nhận cảnh báo để xử lý sau.
4. **Xác minh tự động 100% bằng Unit Test:**
   - Toàn bộ 12 ca kiểm thử (9 ca kiểm thử cơ sở và 3 ca bổ trợ / ngắt mạch) đã được hiện thực hóa trong tệp `update-status.wb.test.ts` và chạy thành công 100% thông qua trình thực thi `tsx` với thời gian phản hồi siêu tốc ($< 10\text{ms}$).
