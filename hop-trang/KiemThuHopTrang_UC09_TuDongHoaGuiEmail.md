# BÁO CÁO KIỂM THỬ HỘP TRẮNG (WHITE-BOX TESTING)
## USE-CASE 09: TỰ ĐỘNG HÓA GỬI EMAIL TUYỂN DỤNG CHO ỨNG VIÊN (SendBulkEmailUseCase)

---

## THÔNG TIN CHUNG VỀ BÀI TẬP VÀ ĐỐI TƯỢNG KIỂM THỬ

- **Học phần:** Kiểm thử và Đảm bảo chất lượng phần mềm (CSE462)
- **Đề tài:** Hệ thống Quản lý Tuyển dụng – Trợ lý Tuyển dụng & Sàng lọc Hồ sơ Tự động
- **Giảng viên hướng dẫn:** TS. Nguyễn Thị Phương Dung | **Nhóm:** 09
- **Sinh viên thực hiện:** Phạm Văn Hưng (Mã SV: **2351170598**)
- **Mã Use Case:** `UC_09` | **Tên Use Case:** Tự động hóa gửi email tuyển dụng cho ứng viên
- **Đối tượng kiểm thử (Target Under Test):** Lớp `SendBulkEmailUseCase` (Phương thức `execute`)
- **Tệp mã nguồn:** `src/modules/client/application/use-cases/email/send-bulk-email.use-case.ts`
- **Tài liệu lý thuyết tham chiếu:** Giáo trình & Bài giảng *CSE462 - Các kỹ thuật kiểm thử phần mềm*, Trường Đại học Thủy Lợi; Chuẩn quốc tế ISTQB CTFL 2018 v3.1.

---

## 1. MÃ NGUỒN ĐÁNH SỐ DÒNG

Dưới đây là mã nguồn chuẩn hóa của lớp `SendBulkEmailUseCase` được đánh số thứ tự dòng thực thi:

```typescript
1:  class SendBulkEmailUseCase {
2:    constructor(
3:      private readonly candidateRepo: ICandidateReadRepo,
4:      private readonly jobRepo: IJobReadRepo,
5:      private readonly mailSvc: IMailService,
6:    ) { }
7:
8:    async execute(input: SendBulkEmailInput): Promise<SendBulkEmailResult> {
9:      if (!input.candidateIds || input.candidateIds.length === 0) {
10:       throw new Error('Danh sách ứng viên không được để trống.');
11:     }
12:
13:     if (!input.title?.trim()) { 
14:       throw new Error('Tiêu đề email không được để trống.');
15:     }
16:
17:     if (!input.content?.trim()) {
18:       throw new Error('Nội dung email không được để trống.');
19:     }
20:
21:     const failed: Array<{
22:       candidateId: string;
23:       candidateName?: string;
24:       error: string;
25:     }> = [];
26:     let totalSent = 0;
27:
28:     const candidatePromises = input.candidateIds.map(id =>
29:       this.candidateRepo.getById(id)
30:     );
31:     const candidates = await Promise.all(candidatePromises);
32:
33:     for (let i = 0; i < candidates.length; i++) {
34:       const candidate = candidates[i];
35:       const candidateId = input.candidateIds[i]!;
36:
37:       try {
38:         if (!candidate) {
39:           failed.push({
40:             candidateId,
41:             error: 'Không tìm thấy ứng viên.',
42:           });
43:           continue;
44:         }
45:
46:         const personal = candidate.getPersonal();
47:         if (!personal?.email) {
48:           failed.push({
49:             candidateId,
50:             candidateName: personal?.fullName,
51:             error: 'Ứng viên không có email.',
52:           });
53:           continue;
54:         }
55:
56:         let jobTitle: string | undefined;
57:         const jobID = candidate.getJobID();
58:         if (jobID) {
59:           try {
60:             const job = await this.jobRepo.getById(jobID.toString());
61:             jobTitle = job?.getTitle();
62:           } catch (e) {
63:             console.warn(`Could not fetch job for candidate ${candidateId}`);
64:           }
65:         }
66:
67:         const personalizedTitle = this.replacePlaceholders(input.title, candidate, jobTitle);
68:         const personalizedContent = this.replacePlaceholders(input.content, candidate, jobTitle);
69:
70:         const htmlContent = `
71:           <html>
72:             <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
73:               <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
74:                 ${personalizedContent.split('\n').map(line => `<p>${line}</p>`).join('')}
75:               </div>
76:             </body>
77:           </html>
78:         `;
79:
80:         // Send email
81:         const sent = await this.mailSvc.sendEmail(
82:           personal.email,
83:           personalizedTitle,
84:           htmlContent,
85:         );
86:
87:         if (sent) {
88:           totalSent++;
89:         } else {
90:           failed.push({
91:             candidateId,
92:             candidateName: personal?.fullName,
93:             error: 'Lỗi gửi email từ dịch vụ mail.',
94:           });
95:         }
96:       } catch (error: unknown) {
97:         const e = error as { message?: string };
98:         const personal = candidate?.getPersonal();
99:         failed.push({
100:          candidateId,
101:          candidateName: personal?.fullName,
102:          error: e.message ?? 'Lỗi không xác định.',
103:        });
104:      }
105:    }
106:
107:    return {
108:      success: true,
109:      message: `Gửi email thành công tới ${totalSent}/${input.candidateIds.length} ứng viên.`,
110:      totalSent,
111:      failed,
112:    };
113:  }
114:}
```

*(Ghi chú: Dòng 1–6 là khai báo Class và Constructor Dependency Injection, không chứa luồng điều khiển nghiệp vụ. Đồ thị CFG được xây dựng cho phương thức `execute` từ dòng 8).*

---

## 2. BẢNG PHÂN CHIA KHỐI LỆNH CƠ BẢN (BASIC BLOCKS)

Dựa trên nguyên lý khối cơ bản (Basic Block là dãy các câu lệnh thực thi tuần tự, có duy nhất 1 điểm vào và 1 điểm ra), phương thức `execute` được phân tách thành 21 khối lệnh chi tiết và tách bạch tuyệt đối các nhánh ngoại lệ:

| Khối (Node) | Dòng mã nguồn | Nội dung thực thi chi tiết | Loại đỉnh (Node Type) |
| :---------: | :------------ | :------------------------- | :-------------------- |
| **Start**   | Dòng 8        | Bắt đầu hàm `execute(input)` | Điểm vào (Entry Point) |
| **Node 1**  | Dòng 9        | Điều kiện `if (!input.candidateIds \|\| input.candidateIds.length === 0)` | Decision (Điểm quyết định 1) |
| **Node 2**  | Dòng 10       | `throw new Error('Danh sách ứng viên không được để trống.')` | Exit (Ngoại lệ 1) |
| **Node 3**  | Dòng 13       | Điều kiện kiểm tra tiêu đề email `if (!input.title?.trim())` | Decision (Điểm quyết định 2) |
| **Node 4**  | Dòng 14       | `throw new Error('Tiêu đề email không được để trống.')` | Exit (Ngoại lệ 2) |
| **Node 5**  | Dòng 17       | Điều kiện kiểm tra nội dung email `if (!input.content?.trim())` | Decision (Điểm quyết định 3) |
| **Node 6**  | Dòng 18       | `throw new Error('Nội dung email không được để trống.')` | Exit (Ngoại lệ 3) |
| **Node 7**  | Dòng 21–31    | Khởi tạo `failed = []`, `totalSent = 0`, lấy `candidates = await Promise.all(...)` | Process (Xử lý chuẩn bị) |
| **Node 8**  | Dòng 33       | Vòng lặp `for (let i = 0; i < candidates.length; i++)` | Decision / Loop Header (Điểm quyết định 4) |
| **Node 9**  | Dòng 34–38    | Lấy `candidate`, `candidateId`, bắt đầu `try`, kiểm tra `if (!candidate)` | Decision (Điểm quyết định 5) |
| **Node 10** | Dòng 39–43    | Thân if: `failed.push(...)`, `continue` (quay lại đỉnh vòng lặp Node 8) | Process (Xử lý rẽ nhánh) |
| **Node 11** | Dòng 46–47    | Lấy `personal = candidate.getPersonal()`, kiểm tra `if (!personal?.email)` | Decision (Điểm quyết định 6) |
| **Node 12** | Dòng 48–53    | Thân if: `failed.push(...)`, `continue` (quay lại đỉnh vòng lặp Node 8) | Process (Xử lý rẽ nhánh) |
| **Node 13** | Dòng 56–58    | Khởi tạo `jobTitle`, lấy `jobID`, kiểm tra `if (jobID)` | Decision (Điểm quyết định 7) |
| **Node 14a**| Dòng 59–61    | Khối `try`: truy vấn công việc `jobRepo.getById(jobID)` và gán `jobTitle` | Process (Xử lý truy vấn thành công) |
| **Node 14b**| Dòng 62–64    | Khối `catch`: bắt lỗi truy vấn Job, ghi log cảnh báo `console.warn(...)` | Exception Handler (Xử lý lỗi truy vấn Job) |
| **Node 15** | Dòng 67–85    | Thay thế placeholder, dựng `htmlContent`, gọi `sent = await mailSvc.sendEmail(...)` | Process (Xử lý gửi mail) |
| **Node 16** | Dòng 87       | Kiểm tra kết quả gửi thư: `if (sent)` | Decision (Điểm quyết định 8) |
| **Node 17** | Dòng 88       | Thân True của if 8: tăng biến đếm `totalSent++` | Process (Xử lý thành công) |
| **Node 18** | Dòng 89–94    | Thân False (else) của if 8: `failed.push('Lỗi gửi email từ dịch vụ mail.')` | Process (Xử lý thất bại) |
| **Node 19** | Dòng 96–103   | Khối bắt ngoại lệ ngoài: `catch (error) { failed.push(...) }` | Exception Handler (Xử lý ngoại lệ runtime) |
| **Node 20** | Dòng 107–112  | Hết vòng lặp `for`: tạo kết quả và trả về `return { success: true, ... }` | Exit (Thoát bình thường) |

---

## 3. XÂY DỰNG ĐỒ THỊ DÒNG ĐIỀU KHIỂN (CONTROL FLOW GRAPH - CFG)

### 3.1. Đồ thị dòng điều khiển ứng với độ đo C1 và C2 (Statement & Decision Coverage)

Đồ thị dưới đây mô tả chính xác luồng điều khiển bao gồm cả nhánh rẽ ngoại lệ của khối `try-catch` khi truy vấn công việc (Node 14a & 14b):

```mermaid
flowchart TD
    Start(["Start: execute(input)"]) --> N1{"Node 1: !candidateIds || length == 0?"}
    
    N1 -- "True" --> N2["Node 2: throw 'Danh sách trống'"]
    N1 -- "False" --> N3{"Node 3: !title?.trim()?"}
    
    N3 -- "True" --> N4["Node 4: throw 'Tiêu đề trống'"]
    N3 -- "False" --> N5{"Node 5: !content?.trim()?"}
    
    N5 -- "True" --> N6["Node 6: throw 'Nội dung trống'"]
    N5 -- "False" --> N7["Node 7: failed=[], totalSent=0, Promise.all"]
    
    N7 --> N8{"Node 8: for (i < candidates.length)?"}
    
    N8 -- "False (Hết ds)" --> N20["Node 20: return { success: true, ... }"]
    N8 -- "True (Còn ứng viên)" --> N9{"Node 9: !candidate?"}
    
    N9 -- "True" --> N10["Node 10: failed.push & continue"]
    N10 --> N8
    
    N9 -- "False" --> N11{"Node 11: !personal?.email?"}
    N11 -- "True" --> N12["Node 12: failed.push & continue"]
    N12 --> N8
    
    N11 -- "False" --> N13{"Node 13: if (jobID)?"}
    N13 -- "True" --> N14a["Node 14a (Try): Fetch jobRepo.getById()"]
    N13 -- "False" --> N15["Node 15: replacePlaceholders & sendEmail"]
    
    N14a -- "Thành công" --> N15
    N14a -. "Lỗi DB" .-> N14b["Node 14b (Catch): console.warn(Lỗi Job)"]
    N14b --> N15
    
    N15 --> N16{"Node 16: if (sent)?"}
    
    N16 -- "True" --> N17["Node 17: totalSent++"]
    N16 -- "False" --> N18["Node 18: failed.push (Lỗi gửi mail)"]
    
    N17 --> N8
    N18 --> N8
    
    N9 -. "Runtime Exception" .-> N19["Node 19: catch (error) -> failed.push"]
    N11 -. "Runtime Exception" .-> N19
    N15 -. "Runtime Exception" .-> N19
    N19 --> N8
```

---

## 4. TÍNH ĐỘ PHỨC TẠP CYCLOMATIC (MCCABE)

Độ phức tạp Cyclomatic $V(G)$ được tính toán độc lập theo 3 phương pháp chuẩn của Thomas McCabe:

### 1. Phương pháp 1: Dựa trên số cung ($E$) và số đỉnh ($N$)
$$V(G) = E - N + 2P$$
Trong đó:
- Số đỉnh (Nodes) $N = 21$ (gồm Node 1 đến Node 20, trong đó Node 14 được phân rã thành Node 14a và Node 14b).
- Số cung (Edges) $E = 29$ (gồm các nhánh rẽ True/False, cung tuần tự và các nhánh ngoại lệ Exception).
- Số thành phần liên thông $P = 1$.

$$\Rightarrow V(G) = 29 - 21 + 2(1) = 10$$

### 2. Phương pháp 2: Dựa trên số điểm quyết định vị từ ($P_n$)
$$V(G) = P_n + 1$$
Trong đó $P_n$ là 9 điểm rẽ nhánh nhị phân (gồm 8 câu lệnh điều kiện `if/for` + 1 điểm rẽ ngoại lệ tại khối `try-catch` truy vấn Job):
1. **Node 1:** `!input.candidateIds || length === 0`
2. **Node 3:** `!input.title?.trim()`
3. **Node 5:** `!input.content?.trim()`
4. **Node 8:** `i < candidates.length`
5. **Node 9:** `!candidate`
6. **Node 11:** `!personal?.email`
7. **Node 13:** `jobID != null`
8. **Khối Job Try-Catch (Node 14a/14b):** Rẽ nhánh khi truy vấn Job thành công hoặc ném Exception
9. **Node 16:** `sent == true`

$$\Rightarrow P_n = 9 \implies V(G) = 9 + 1 = 10$$

### 3. Phương pháp 3: Dựa trên số miền mặt phẳng khép kín ($R$)
$$V(G) = R$$
Đồ thị phẳng có 9 miền kín bao bọc bởi các chu trình rẽ nhánh và vòng lặp ($R_1 \dots R_9$) cộng thêm 1 miền vô hạn bao quanh bên ngoài ($R_{10}$):
$$\Rightarrow V(G) = R = 10$$

> **Kết luận:** Độ phức tạp Cyclomatic của phương thức `execute` là **$V(G) = 10$**. Cần tối thiểu **10 đường dẫn cơ sở (Basis Paths)** độc lập tuyến tính để bao phủ toàn bộ đồ thị dòng điều khiển.

---

## 5. THIẾT KẾ CÁC ĐƯỜNG DẪN CƠ SỞ (BASIS PATHS)

| Mã đường dẫn | Chuỗi các khối lệnh (Nodes Sequence) | Mục tiêu bao phủ |
| :---: | :--- | :--- |
| **Path 1** | $Start \rightarrow 1 \rightarrow 2$ | Nhánh lỗi danh sách ứng viên rỗng / undefined |
| **Path 2** | $Start \rightarrow 1 \rightarrow 3 \rightarrow 4$ | Nhánh lỗi tiêu đề email bị để trống |
| **Path 3** | $Start \rightarrow 1 \rightarrow 3 \rightarrow 5 \rightarrow 6$ | Nhánh lỗi nội dung email bị để trống |
| **Path 4** | $Start \rightarrow 1 \rightarrow 3 \rightarrow 5 \rightarrow 7 \rightarrow 8 \rightarrow 20$ | Nhánh danh sách ứng viên hợp lệ nhưng vòng lặp 0 lần |
| **Path 5** | $Start \rightarrow 1 \rightarrow 3 \rightarrow 5 \rightarrow 7 \rightarrow 8 \rightarrow 9 \rightarrow 10 \rightarrow 8 \rightarrow 20$ | Nhánh không tìm thấy ứng viên trong database (`candidate === null`) |
| **Path 6** | $Start \rightarrow 1 \rightarrow 3 \rightarrow 5 \rightarrow 7 \rightarrow 8 \rightarrow 9 \rightarrow 11 \rightarrow 12 \rightarrow 8 \rightarrow 20$ | Nhánh ứng viên không có địa chỉ email |
| **Path 7** | $Start \rightarrow 1 \rightarrow 3 \rightarrow 5 \rightarrow 7 \rightarrow 8 \rightarrow 9 \rightarrow 11 \rightarrow 13 \rightarrow 15 \rightarrow 16 \rightarrow 18 \rightarrow 8 \rightarrow 20$ | Nhánh không có `jobID`, gửi email qua SMTP thất bại (`sent === false`) |
| **Path 8** | $Start \rightarrow 1 \rightarrow 3 \rightarrow 5 \rightarrow 7 \rightarrow 8 \rightarrow 9 \rightarrow 11 \rightarrow 13 \rightarrow 14a \rightarrow 15 \rightarrow 16 \rightarrow 17 \rightarrow 8 \rightarrow 20$ | Nhánh Happy Path: có `jobID`, truy vấn Job thành công (qua 14a), gửi email thành công |
| **Path 9** | $Start \rightarrow 1 \rightarrow 3 \rightarrow 5 \rightarrow 7 \rightarrow 8 \rightarrow 9 \rightarrow 11 \rightarrow 13 \rightarrow 14a \rightarrow 14b \rightarrow 15 \rightarrow 16 \rightarrow 17 \rightarrow 8 \rightarrow 20$ | Nhánh có `jobID` nhưng truy vấn Job lỗi (qua 14b), bắt log cảnh báo và vẫn gửi email |
| **Path 10**| $Start \rightarrow 1 \rightarrow 3 \rightarrow 5 \rightarrow 7 \rightarrow 8 \rightarrow 9 \rightarrow 11 \rightarrow 19 \rightarrow 8 \rightarrow 20$ | Nhánh phát sinh ngoại lệ đột ngột trong khối `try` ngoài (Runtime Exception) |

---

## 6. THIẾT KẾ BẢNG CA KIỂM THỬ HỘP TRẮNG (WHITE-BOX TEST CASES)

### 6.1. Bảng ca kiểm thử đáp ứng độ đo C1 (Statement Coverage) & C2 (Branch Coverage)

| Mã Test Case | Đường đi (Basis Path) | Dữ liệu đầu vào (Test Input Data) | Trạng thái Mock / Giả lập hệ thống | Kết quả mong đợi (Expected Output) | Đánh giá |
| :---: | :--- | :--- | :--- | :--- | :---: |
| **TC_WB_01** | Path 1: $Start \rightarrow 1 \rightarrow 2$ | `candidateIds: []`, `title: "Thư mời"`, `content: "Nội dung"` | Không tương tác Repo | Ném ngoại lệ: `'Danh sách ứng viên không được để trống.'` | Đạt |
| **TC_WB_02** | Path 2: $Start \rightarrow 1 \rightarrow 3 \rightarrow 4$ | `candidateIds: ['C01']`, `title: "   "`, `content: "Nội dung"` | Không tương tác Repo | Ném ngoại lệ: `'Tiêu đề email không được để trống.'` | Đạt |
| **TC_WB_03** | Path 3: $Start \rightarrow 1 \rightarrow 3 \rightarrow 5 \rightarrow 6$ | `candidateIds: ['C01']`, `title: "Thư mời"`, `content: ""` | Không tương tác Repo | Ném ngoại lệ: `'Nội dung email không được để trống.'` | Đạt |
| **TC_WB_04** | Path 5: $Start \dots \rightarrow 8 \rightarrow 9 \rightarrow 10 \rightarrow 8 \rightarrow 20$ | `candidateIds: ['CAN_UNKNOWN']`, `title: "Hẹn PV"`, `content: "Chào bạn"` | `candidateRepo.getById('CAN_UNKNOWN')` trả về `null` | Trả về `totalSent: 0`, `failed` chứa `error: 'Không tìm thấy ứng viên.'` | Đạt |
| **TC_WB_05** | Path 6: $Start \dots \rightarrow 8 \rightarrow 9 \rightarrow 11 \rightarrow 12 \rightarrow 8 \rightarrow 20$ | `candidateIds: ['C02']`, `title: "Hẹn PV"`, `content: "Chào bạn"` | Candidate tìm thấy nhưng `personal.email = undefined` | Trả về `totalSent: 0`, `failed` chứa `error: 'Ứng viên không có email.'` | Đạt |
| **TC_WB_06** | Path 7: $Start \dots \rightarrow 13 \rightarrow 15 \rightarrow 16 \rightarrow 18 \rightarrow 8 \rightarrow 20$ | `candidateIds: ['C03']`, `title: "Hẹn PV"`, `content: "Chào [Tên Ứng Viên]"` | Candidate hợp lệ, `jobID = null`, `mailSvc.sendEmail` trả về `false` | Trả về `totalSent: 0`, `failed` chứa `error: 'Lỗi gửi email từ dịch vụ mail.'` | Đạt |
| **TC_WB_07** | Path 8: $Start \dots \rightarrow 13 \rightarrow 14a \rightarrow 15 \rightarrow 16 \rightarrow 17 \rightarrow 8 \rightarrow 20$ | `candidateIds: ['C04']`, `title: "Tuyển dụng [Vị Trí]"`, `content: "Chào [Tên Ứng Viên]"` | Candidate hợp lệ, `jobID = 'JOB_01'`, `jobRepo.getById` trả về Job, `mailSvc.sendEmail` trả về `true` | Trả về `totalSent: 1`, `failed: []`, `message: 'Gửi email thành công tới 1/1 ứng viên.'` (Happy Path) | Đạt |
| **TC_WB_08** | Path 9: $Start \dots \rightarrow 13 \rightarrow 14a \rightarrow 14b \rightarrow 15 \rightarrow 16 \rightarrow 17 \rightarrow 8 \rightarrow 20$ | `candidateIds: ['C05']`, `title: "Tuyển dụng [Vị Trí]"`, `content: "Chào bạn"` | Candidate hợp lệ, `jobID = 'JOB_ERR'`, `jobRepo.getById` ném Exception mạng $\rightarrow$ bắt tại Node 14b | In `console.warn`, email vẫn gửi thành công không có tên job, `totalSent: 1` | Đạt |
| **TC_WB_09** | Path 10: $Start \dots \rightarrow 11 \rightarrow 19 \rightarrow 8 \rightarrow 20$ | `candidateIds: ['C06']`, `title: "Hẹn PV"`, `content: "Chào bạn"` | `candidate.getPersonal()` ném ngoại lệ đột ngột: `Error('Crash')` | Khối `catch` (Node 19) bắt lỗi, thêm vào mảng `failed` với thông điệp: `'Crash'` | Đạt |

---

### 6.2. Kiểm tra độ đo bao phủ điều kiện C3 (Condition Coverage cho Node 1)

Biểu thức điều kiện tại Node 1 (Dòng 9): `!input.candidateIds || input.candidateIds.length === 0`

| Ca kiểm thử C3 | `!input.candidateIds` ($A$) | `input.candidateIds.length === 0` ($B$) | Kết quả biểu thức ($A \lor B$) | Nhánh rẽ | Dữ liệu đầu vào minh họa |
| :---: | :---: | :---: | :---: | :---: | :--- |
| **C3_01** | **True** | Không xét (Short-circuit) | **True** | Node 2 (Ném ngoại lệ) | `input.candidateIds = null` hoặc `undefined` |
| **C3_02** | **False** | **True** | **True** | Node 2 (Ném ngoại lệ) | `input.candidateIds = []` (Mảng rỗng) |
| **C3_03** | **False** | **False** | **False** | Node 3 (Đi tiếp) | `input.candidateIds = ['CAN_01']` |

$\Rightarrow$ **Kết luận C3:** 3 ca kiểm thử trên đảm bảo mỗi điều kiện thành phần $A$ và $B$ đều được đánh giá đầy đủ cả hai giá trị chân lý Đúng (True) và Sai (False), đạt **100% độ bao phủ điều kiện C3**.

---

## 7. ĐÁNH GIÁ ĐỘ ĐO BAO PHỦ VÀ KẾT LUẬN

1. **Độ bao phủ câu lệnh ($C_1$ - Statement Coverage):**
   - Tổng số khối lệnh (Basic Blocks): $21/21$ khối.
   - Số khối được thực thi qua tập Test Cases: $21/21$ khối (bao gồm cả khối Try 14a và khối Catch 14b).
   - **Tỷ lệ bao phủ $C_1$:** $\mathbf{100\%}$.

2. **Độ bao phủ nhánh quyết định ($C_2$ - Branch Coverage):**
   - Tất cả 9 điểm quyết định và rẽ nhánh ngoại lệ đều được kích hoạt đầy đủ 2 nhánh **Đúng (True)** và **Sai (False)**.
   - **Tỷ lệ bao phủ $C_2$:** $\mathbf{100\%}$.

3. **Tính độc lập và khả năng bảo trì:**
   - Bộ Test Case bao phủ toàn diện cả các trường hợp biên dữ liệu rỗng (Boundary Values), các nhánh lỗi logic ứng viên không tồn tại, lỗi thiếu email, lỗi dịch vụ gửi thư SMTP bên ngoài, lỗi kết nối cơ sở dữ liệu khi truy vấn công việc và ngoại lệ thời gian chạy (Runtime Exception).
