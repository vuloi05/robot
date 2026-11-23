# Chương 5: Thiết kế và Xây dựng Hệ thống IoT

- **PDF gốc:** `docs/it4735_iot_va_ung_dung_v2025_16.1m.pdf` (*IT4735 IoT và Ứng dụng*, SoICT - HUST, 2025)
- **Phạm vi slide:** 315–349
- **Các mục lớn:** Quy trình phân tích yêu cầu, thiết kế kiến trúc, lựa chọn phần cứng/giao thức và triển khai hệ thống IoT
- **Ứng dụng vào dự án Robot Nhà Hàng:** Áp dụng quy trình thiết kế hệ thống IoT đầu-cuối cho hệ thống nhà hàng thông minh (Robot + Bàn + Smart Dock + Server).

---

### [Slide 315]

Chương 5. Thiết kế và xây dựng hệ thống IoT
▪ Project-Based Learning:
▪ Học dựa trên giải quyết một bài toán/dự án IoT cụ thể

▪ Kỹ năng:
▪ Tìm vấn đề cần giải quyết (Finding the problems)
▪ Phân tích thiết kế (System design and Analysis)
▪ Xây dựng hệ thống (Implementing, Programming)
▪ Trình bày (Presentation, Report)
▪ Làm việc nhóm (Teamwork)

315

---

### [Slide 316]

Cách thức thực hiện
▪ Lập nhóm dự án: 3-4 thành viên
▪ Xác định bài toán ứng dụng IoT
▪ Phân tích và thiết kế hệ thống IoT:
▪ Thiết kế kiến trúc tổng quan của hệ thống
▪ Thiết kế chi tiết các thành phần của hệ thống
▪ Lựa chọn thiết bị phần cứng: máy tính nhúng, sensors
▪ Lựa chọn giải pháp phần mềm/công nghệ IoT

▪ Xây dựng hệ thống:
▪ Lập trình triển khai các thành phần của hệ thống
▪ Vận dụng các giải pháp, dịch vụ, công nghệ IoT

▪ Thuyết trình và báo cáo

316

---

### [Slide 317]

Các chủ đề ứng dụng IoT
▪ P1. Smart Agriculture:
▪ Ứng dụng IoT trong nông nghiệp thông minh

317

---

### [Slide 318]

P1. Smart Agriculture

https://www.smartofthings.co.th/2018/08/27/smart-agriculture-solution/
318

---

### [Slide 319]

P2. Smart Home
▪ Ứng dụng IoT trong nhà thông minh:
▪ Điều khiển các thiết bị từ xa (mobile app)
▪ Điều khiển bằng giọng nói (Google assistant)
▪ Giám sát từ xa

319

---

### [Slide 320]

P2. Smart Home
▪ Ví dụ:

320

> [Slide hình ảnh/sơ đồ — xem trực tiếp Slide 320 trong docs/it4735_iot_va_ung_dung_v2025_16.1m.pdf nếu cần]

---

### [Slide 321]

Các chủ đề ứng dụng IoT
▪ P3. Smart Water Supply Monitoring:
▪ Ứng dụng IoT trong cấp nước thông minh

▪ P4. Smart Electrical Power Monitoring:
▪ Ứng dụng IoT trong giám sát phân phối điện năng thông minh

321

---

### [Slide 322]

Smart Utitlies (Electrical power, Water)

https://www.smartofthings.co.th/2018/08/27/smart-utilities-solution/
322

---

### [Slide 323]

Các chủ đề ứng dụng IoT
▪ P5. Smart Transportation:
▪ Ứng dụng IoT trong giám sát vận tải thông minh

323

---

### [Slide 324]

Các chủ đề ứng dụng IoT
▪ 6. Smart Air Quality Monitoring:
▪ Ứng dụng IoT trong giám sát chất lượng không khí

324

---

### [Slide 325]

P6. Smart Air Quality Monitoring
Measuring Station
Sensors

(NO2, CO2, CO, SO2, O3, NH3, PM2.5)

GSM 4G/Wifi
Module

GPS

Field Measurement

TCP/IP

Server

HTTP, TCP/IP

- Database
- Webserver
1. Sensors Data
Collecting

2. Environment
Monitoting and
Warning

Monitoring
Station

3. AI-based Data
Analyzing

HTTP, TCP/IP

Clients
(PC, Tablet,
Mobile phones)

325

---

### [Slide 326]

Các chủ đề ứng dụng IoT
▪ 7. Smart Gabaging:
▪ Ứng dụng IoT trong thu gom rác thông minh
▪ Tham khảo: https://www.instructables.com/id/Smart-Garbage-Monitoring-System-Using-Internetof-/

▪ 8. Smart Parking:
▪ Ứng dụng IoT trong đỗ xe thông minh

▪ 9. Smart Health Monitoring:
▪ Ứng dụng IoT trong giám sát sức khỏe thông minh

▪ 10. Smart Robotic Warehouse:
▪ Ứng dụng IoT trong nhà kho thông minh

326

---

### [Slide 327]

Project 1: Smart Gabage
▪ Tổng quan hệ thống

327

> [Slide hình ảnh/sơ đồ — xem trực tiếp Slide 327 trong docs/it4735_iot_va_ung_dung_v2025_16.1m.pdf nếu cần]

---

### [Slide 328]

Project 1: Smart Gabage
▪ Web app quản lý: thêm/sửa thùng rác

328

---

### [Slide 329]

Project 1: Smart Gabage
▪ Mobile app

329

> [Slide hình ảnh/sơ đồ — xem trực tiếp Slide 329 trong docs/it4735_iot_va_ung_dung_v2025_16.1m.pdf nếu cần]

---

### [Slide 330]

Project 1: Smart Gabage
▪ Mobile app

330

> [Slide hình ảnh/sơ đồ — xem trực tiếp Slide 330 trong docs/it4735_iot_va_ung_dung_v2025_16.1m.pdf nếu cần]

---

### [Slide 331]

Project 2. Smart Home
▪ Sơ đồ thiết kế tổng quan

331

---

### [Slide 332]

Project 2. Smart home
▪ Mobile app:
▪ Quản lý home/rooms (add/edit)

332

---

### [Slide 333]

Project 2. Smart home
▪ Mobile app:
▪ Quản lý home/rooms (add/edit)

333

---

### [Slide 334]

Project 2. Smart home
▪ Mobile app:
▪ Add thiết bị, ghép nối thiết bị vật lý

334

---

### [Slide 335]

Project 2. Smart home
▪ Mobile app:
▪ Automation

335

---

### [Slide 336]

Project 2. Smart home
▪ Xây dựng server:

336

> [Slide hình ảnh/sơ đồ — xem trực tiếp Slide 336 trong docs/it4735_iot_va_ung_dung_v2025_16.1m.pdf nếu cần]

---

### [Slide 337]

Project 2. Smart home
▪ Xây dựng server:
▪ Luồng nghiệp vụ thêm/xóa người dùng

Thêm/xóa người dùng
337

---

### [Slide 338]

Project 2. Smart home
▪ Xây dựng server:
▪ Luồng nghiệp vụ thêm nhà

Thêm một ngôi nhà mới
338

---

### [Slide 339]

Project 3. Smart home
▪ Thiết kế hệ thống

339

> [Slide hình ảnh/sơ đồ — xem trực tiếp Slide 339 trong docs/it4735_iot_va_ung_dung_v2025_16.1m.pdf nếu cần]

---

### [Slide 340]

Project 3. Smart home
▪ Mobile app

340

> [Slide hình ảnh/sơ đồ — xem trực tiếp Slide 340 trong docs/it4735_iot_va_ung_dung_v2025_16.1m.pdf nếu cần]

---

### [Slide 341]

Project 4. Smart garden
▪ Kiến trúc hệ thống

341

> [Slide hình ảnh/sơ đồ — xem trực tiếp Slide 341 trong docs/it4735_iot_va_ung_dung_v2025_16.1m.pdf nếu cần]

---

### [Slide 342]

Project 4. Smart garden
▪ Công nghệ sử dụng:
▪ Sử dụng dữ liệu ảo cho các thiết bị cảm biến.
▪ Server: NodeJS, ExpressJS.
▪ Database: MongoDB.
▪ Website: React JS.
▪ Mobile App: React Native.

342

---

### [Slide 343]

Project 4. Smart garden
▪ Thiết kế CSDL

343

> [Slide hình ảnh/sơ đồ — xem trực tiếp Slide 343 trong docs/it4735_iot_va_ung_dung_v2025_16.1m.pdf nếu cần]

---

### [Slide 344]

Project 4. Smart garden
▪ Xây dựng các API
▪ Đăng ký: POST /v1/auth/register
▪ Đăng nhập: POST /v1/auth/login
▪ Lấy danh sách các thiết bị: GET /v1/device/{houseId}
▪ Sửa thông tin thiết bị:PUT /v1/device/{deviceId}
▪ Lấy dữ liệu thống kê: GET /v1/data/{houseId}
▪ Lấy danh sách các cảnh báo: GET /v1/house/events/{houseId}
▪ Lấy thông tin nhà nấm: GET /v1/house
▪ Thêm nhà nấm mới: POST /v1/house
▪ Sửa thông tin nhà nấm: PUT /v1/house/update-house/{houseId}
▪ Thêm thành viên: PUT /v1/house/update-member/{houseId}
▪ Xóa thành viên: PUT /v1/house/delete-member/{houseId}/{userId}

344

---

### [Slide 345]

Project 4. Smart garden
▪ Ví dụ API lấy ds thiết bị

345

---

### [Slide 346]

Project 4. Smart garden
▪ Web app quản trị:

346

> [Slide hình ảnh/sơ đồ — xem trực tiếp Slide 346 trong docs/it4735_iot_va_ung_dung_v2025_16.1m.pdf nếu cần]

---

### [Slide 347]

Project 4. Smart garden
▪ Web app quản trị:

347

> [Slide hình ảnh/sơ đồ — xem trực tiếp Slide 347 trong docs/it4735_iot_va_ung_dung_v2025_16.1m.pdf nếu cần]

---

### [Slide 348]

Project 4. Smart garden
▪ Web app quản trị:

348

> [Slide hình ảnh/sơ đồ — xem trực tiếp Slide 348 trong docs/it4735_iot_va_ung_dung_v2025_16.1m.pdf nếu cần]

---

### [Slide 349]

Project 4. Smart garden
▪ Mobile app

349

> [Slide hình ảnh/sơ đồ — xem trực tiếp Slide 349 trong docs/it4735_iot_va_ung_dung_v2025_16.1m.pdf nếu cần]
