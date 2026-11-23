# Chương 4: An toàn và Bảo mật IoT

- **PDF gốc:** `docs/it4735_iot_va_ung_dung_v2025_16.1m.pdf` (*IT4735 IoT và Ứng dụng*, SoICT - HUST, 2025)
- **Phạm vi slide:** 292–314
- **Các mục lớn:** 4.1 Tổng quan bảo mật IoT (293–295); 4.2 Các dạng tấn công hạ tầng IoT (296–302); 4.3 Các điểm yếu bảo mật IoT (303–314)
- **Ứng dụng vào dự án Robot Nhà Hàng:** Rất quan trọng khi thiết kế bảo mật VPS/Mosquitto: TLS/MQTTS, password & ACL, bảo vệ API và phân tích rủi ro trong luận văn.

---

### [Slide 292]

Chương 4. An toàn và Bảo mật IoT
▪ 4.1. Tổng quan về bảo mật IoT
▪ 4.2. Các dạng tấn công vào hạ tầng IoT
▪ 4.3. Các điểm yếu bảo mật trong IoT

292

---

### [Slide 293]

4.1. Tổng quan về bảo mật IoT
▪ Các vấn đề trong bảo mật IoT:
▪ Thiết kế ban đầu cho mạng truyền thông riêng sau đó được
chuyển sang mạng IP và Internet
▪ Cập nhật firmware cho thiết bị IoT khó khăn
▪ Xuất phát từ những yêu cầu bảo mật cơ bản, sau đó xuất hiện
các lỗi bảo mật kèm theo các yêu cầu bảo mật phức tạp hơn.
▪ Các thiết bị bảo mật kém từ các thiết kế ban đầu đã được sử
dụng trên thực tế

293

---

### [Slide 294]

Tổng quan về bảo mật IoT
▪ Phân loại nguy cơ trong bảo mật IoT:
▪ Capture: Các nguy cơ liên quan đến “bắt” (thu thập, ăn cắp) thông tin dữ
liệu từ hệ thống
▪ Disrupt: Các nguy cơ liên quan đến tấn công từ chối dịch vụ (denying), phá
hủy (destroying), ngắt/dừng (interrupting) hệ thống
▪ Manipulate: Các nguy cơ liên quan đến can thiệp/thay đổi (manipulating)
dữ liệu, định danh.

294

---

### [Slide 295]

Tổng quan về bảo mật IoT
▪ Các yêu cầu bảo mật IoT:
▪ Confidentiality – Tính tin cẩn:
• Dữ liệu truyền chỉ có thể được đọc bởi bên nhận

▪ Availability – Tính sẵn dùng:
• Việc truyền thông giữa các thiết bị truyền và nhận luôn luôn sẵn sàng

▪ Integrity – Tính toàn vẹn
• Dữ liệu nhận không bị nhiễu trong quá trình truyền, đảm bảo tính chính xác, vẹn toàn
của dữ liệu

▪ Authenticity – Tính xác thực
• Bên gửi luôn luôn có thể xác thực dữ liệu được gửi
• Dữ liệu chỉ có thể được truy cập bởi bên nhận được cho phép

295

---

### [Slide 296]

4.2. Các dạng tấn công hạ tầng IoT
▪ Hạ tầng IoT thông dụng

296

---

### [Slide 297]

Một số dạng tấn công
▪ Fake Control Server

297

> [Slide hình ảnh/sơ đồ — xem trực tiếp Slide 297 trong docs/it4735_iot_va_ung_dung_v2025_16.1m.pdf nếu cần]

---

### [Slide 298]

Một số dạng tấn công
▪ Attack on device open ports

298

---

### [Slide 299]

Một số dạng tấn công
▪ Attack on server open ports

299

---

### [Slide 300]

Một số dạng tấn công
▪ Steal Credential

300

> [Slide hình ảnh/sơ đồ — xem trực tiếp Slide 300 trong docs/it4735_iot_va_ung_dung_v2025_16.1m.pdf nếu cần]

---

### [Slide 301]

Một số dạng tấn công
▪ Inject bad configuration or firmware

301

---

### [Slide 302]

Một số dạng tấn công
▪ Sniff data on private network

302

---

### [Slide 303]

4.3. Các điểm yếu bảo mật IoT
▪ I1. Insecure Web Interface (Giao diện quản trị không an toàn)
▪ I2. Insufficient Authentication/Authorization (Xác thực không đủ an toàn)
▪ I3. Insecure Network Services (Các dịch vụ mạng thiếu bảo mật)
▪ I4. Lack of Transport Encryption/Integrity Verifcation (Thiếu mã hóa tầng giao
vận)
▪ I5. Privacy Concerns (Các vấn đề liên quan quyền riêng tư)
▪ I6. Insecure Cloud Interface (Giao diện Cloud thiếu bảo mật)
▪ I7. Insecure Mobile Interface (Giao diện mobile thiếu bảo mật)
▪ I8. Insufficient Security Configurability (Cấu hình bảo mật không an toàn)
▪ I9. Insecure Software/Firmware (Phần mềm không an toàn)
▪ I10. Poor Physical Security (Thiếu bảo mật tầng vật lý)

303

---

### [Slide 304]

1. Giao diện quản trị không an toàn

304

> [Slide hình ảnh/sơ đồ — xem trực tiếp Slide 304 trong docs/it4735_iot_va_ung_dung_v2025_16.1m.pdf nếu cần]

---

### [Slide 305]

2. Cơ chế xác thực không an toàn

305

> [Slide hình ảnh/sơ đồ — xem trực tiếp Slide 305 trong docs/it4735_iot_va_ung_dung_v2025_16.1m.pdf nếu cần]

---

### [Slide 306]

3. Các dịch vụ mạng không an toàn

306

> [Slide hình ảnh/sơ đồ — xem trực tiếp Slide 306 trong docs/it4735_iot_va_ung_dung_v2025_16.1m.pdf nếu cần]

---

### [Slide 307]

4. Thiếu sử dụng mã hóa tầng giao vận

307

> [Slide hình ảnh/sơ đồ — xem trực tiếp Slide 307 trong docs/it4735_iot_va_ung_dung_v2025_16.1m.pdf nếu cần]

---

### [Slide 308]

5. Các vấn đề về quyền riêng tư

308

> [Slide hình ảnh/sơ đồ — xem trực tiếp Slide 308 trong docs/it4735_iot_va_ung_dung_v2025_16.1m.pdf nếu cần]

---

### [Slide 309]

6. Giao diện Cloud không an toàn

309

> [Slide hình ảnh/sơ đồ — xem trực tiếp Slide 309 trong docs/it4735_iot_va_ung_dung_v2025_16.1m.pdf nếu cần]

---

### [Slide 310]

7. Giao diện Mobile không an toàn

310

> [Slide hình ảnh/sơ đồ — xem trực tiếp Slide 310 trong docs/it4735_iot_va_ung_dung_v2025_16.1m.pdf nếu cần]

---

### [Slide 311]

8. Thiếu cấu hình bảo mật

311

> [Slide hình ảnh/sơ đồ — xem trực tiếp Slide 311 trong docs/it4735_iot_va_ung_dung_v2025_16.1m.pdf nếu cần]

---

### [Slide 312]

9. Phần mềm không an toàn

312

> [Slide hình ảnh/sơ đồ — xem trực tiếp Slide 312 trong docs/it4735_iot_va_ung_dung_v2025_16.1m.pdf nếu cần]

---

### [Slide 313]

10. Thiếu bảo mật tầng vật lý

313

> [Slide hình ảnh/sơ đồ — xem trực tiếp Slide 313 trong docs/it4735_iot_va_ung_dung_v2025_16.1m.pdf nếu cần]

---

### [Slide 314]

Nội dung
▪ Chương 1. Tổng quan về IoT
▪ Chương 2. Các công nghệ IoT
▪ Chương 3. Lập trình ứng dụng IoT
▪ Chương 4. An toàn và Bảo mật IoT
▪ Chương 5. Thiết kế và xây dựng hệ thống IoT

314
