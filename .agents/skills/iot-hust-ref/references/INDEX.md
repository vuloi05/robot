# Mục Lục Tài Liệu: IT4735 — IoT và Ứng Dụng (`it4735_iot_va_ung_dung_v2025_16.1m.pdf`)

- **Nguồn:** Phạm Ngọc Hưng, Nguyễn Đình Thuận, Đặng Tuấn Linh — Trường CNTT&TT (SoICT), ĐH Bách khoa Hà Nội (2025)
- **Tổng số phần đã tách:** 6 files (từ 349 slides PDF; ước lượng ~23,678 tokens toàn bộ)

## Lưu Ý Khi Tham Chiếu Cho Dự Án Robot Nhà Hàng

1. **Không chép code Java / ThingSpeak trong slide:** Slide dùng Java/ThingSpeak cho mục đích giảng dạy đại cương; khi code cho dự án luôn giữ đúng stack đã chốt (**Rust Axum + rumqttc + Mosquitto + ESP32/STM32 + ROS 2 Jazzy**).
2. **Slide sơ đồ/hình vẽ (`< 50` ký tự text):** Khi gặp ghi chú `[Slide hình ảnh/sơ đồ]`, có thể xuất đúng slide đó bằng `pdftoppm` và xem bằng `read_file`:

```bash
pdftoppm -f XX -l XX -png -r 150 /home/vuloi/prj/robot/docs/it4735_iot_va_ung_dung_v2025_16.1m.pdf /tmp/iot_slide
```

## Danh Sách Chương & Ánh Xạ Dự Án

| File | Slides | Các mục lớn | Slide ít chữ/sơ đồ | ~Tokens | Ứng dụng trực tiếp vào dự án |
| :--- | :---: | :--- | :---: | :---: | :--- |
| [ch01_tong_quan_iot.md](./ch01_tong_quan_iot.md) | 1–60 | Giới thiệu môn học (1–4); 1.1 Tổng quan (6–18); 1.2 Kiến trúc (19–22); 1.3 Công nghệ (23–35); 1.4 Ứng dụng (36–52); 1.5 Thách thức (53–60) | 13 | ~4,071 | Khái niệm hệ thống IoT, mô hình kiến trúc phân lớp (Edge/Gateway/Cloud) dùng chuẩn cho chương Thiết kế hệ thống trong luận văn. |
| [ch02a_cam_bien_va_truyen_thong.md](./ch02a_cam_bien_va_truyen_thong.md) | 61–91 | 2.1 Cảm biến và thiết bị IoT (62–81); 2.2 Một số chuẩn truyền thông (82–91) | 1 | ~2,207 | Phân loại cảm biến/cơ cấu chấp hành và so sánh các chuẩn truyền thông không dây (Wi-Fi, BLE, Zigbee, LoRa) cho ESP32 IoT. |
| [ch02b_giao_thuc_mqtt_http_cloud.md](./ch02b_giao_thuc_mqtt_http_cloud.md) | 92–190 | 2.3 Giao thức ứng dụng IoT: HTTP, MQTT, AMQP (92–178); 2.4 IoT Cloud Platform (179–190) | 32 | ~7,240 | Cốt lõi cho tầng MQTT Broker (Pub/Sub, QoS 0/1/2, Retain, LWT) và so sánh lý thuyết MQTT vs HTTP trong luận văn. |
| [ch03_lap_trinh_iot_va_web_api.md](./ch03_lap_trinh_iot_va_web_api.md) | 191–291 | 3.1 Lập trình thiết bị IoT (192–240); 3.2 Xây dựng Web API (241–277); 3.3 Lập trình với IoT Platform (278–291) | 15 | ~6,992 | Nguyên lý tương tác phần cứng & thiết kế REST/WebSocket API. Lưu ý: code mẫu Java/ThingSpeak chỉ dùng tham khảo khái niệm, dự án code bằng Rust/ESP32. |
| [ch04_an_toan_bao_mat_iot.md](./ch04_an_toan_bao_mat_iot.md) | 292–314 | 4.1 Tổng quan bảo mật IoT (293–295); 4.2 Các dạng tấn công hạ tầng IoT (296–302); 4.3 Các điểm yếu bảo mật IoT (303–314) | 12 | ~1,362 | Rất quan trọng khi thiết kế bảo mật VPS/Mosquitto: TLS/MQTTS, password & ACL, bảo vệ API và phân tích rủi ro trong luận văn. |
| [ch05_thiet_ke_he_thong_iot.md](./ch05_thiet_ke_he_thong_iot.md) | 315–349 | Quy trình phân tích yêu cầu, thiết kế kiến trúc, lựa chọn phần cứng/giao thức và triển khai hệ thống IoT | 13 | ~1,806 | Áp dụng quy trình thiết kế hệ thống IoT đầu-cuối cho hệ thống nhà hàng thông minh (Robot + Bàn + Smart Dock + Server). |
