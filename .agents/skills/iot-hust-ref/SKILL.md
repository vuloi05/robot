---
name: iot-hust-ref
description: >-
  Academic reference from HUST IT4735 (IoT và Ứng dụng, 2025) covering IoT layered
  architecture, sensors and wireless communication standards, MQTT/HTTP/AMQP protocol theory,
  Web API design, IoT infrastructure attack vectors, security hardening (TLS/ACL/auth), and
  Vietnamese academic terminology. Use this skill when designing or hardening the Mosquitto MQTT
  broker, ESP32 IoT table/dock nodes, Rust IoT Gateway security/API architecture, or writing
  Vietnamese thesis chapters on IoT concepts and security analysis.
---

# IT4735 IoT và Ứng Dụng (SoICT - HUST) — Tài Liệu Tham Chiếu IoT

Bộ tham chiếu tách từ bài giảng *IT4735 — IoT và Ứng dụng* ([it4735_iot_va_ung_dung_v2025_16.1m.pdf](../../../docs/it4735_iot_va_ung_dung_v2025_16.1m.pdf), 349 slides) phục vụ thiết kế kiến trúc IoT, giao thức truyền thông, bảo mật Mosquitto/VPS và chuẩn hóa thuật ngữ tiếng Việt cho luận văn.

## Quy Trình Tra Cứu 3 Bước (Progressive Disclosure)

1. **Bước 1 — Đọc mục lục trước:** Mở [references/INDEX.md](references/INDEX.md) để chọn đúng file chương liên quan trong 6 phần.
2. **Bước 2 — Chỉ mở chương cần thiết:** Đọc phần tương ứng trong `references/`:
   - [ch01_tong_quan_iot.md](references/ch01_tong_quan_iot.md): Kiến trúc phân lớp IoT, Edge/Gateway/Cloud, thách thức hệ thống.
   - [ch02a_cam_bien_va_truyen_thong.md](references/ch02a_cam_bien_va_truyen_thong.md): Cảm biến, cơ cấu chấp hành, chuẩn truyền thông không dây (Wi-Fi/BLE/Zigbee/LoRa).
   - [ch02b_giao_thuc_mqtt_http_cloud.md](references/ch02b_giao_thuc_mqtt_http_cloud.md): Lý thuyết **MQTT** (Pub/Sub, Broker, QoS, Retain, LWT) vs HTTP vs AMQP.
   - [ch03_lap_trinh_iot_va_web_api.md](references/ch03_lap_trinh_iot_va_web_api.md): Nguyên lý lập trình thiết bị IoT & thiết kế Web API.
   - [ch04_an_toan_bao_mat_iot.md](references/ch04_an_toan_bao_mat_iot.md): Các dạng tấn công hạ tầng & điểm yếu bảo mật IoT (làm cơ sở cấu hình TLS/MQTTS, ACL và viết mục An toàn thông tin).
   - [ch05_thiet_ke_he_thong_iot.md](references/ch05_thiet_ke_he_thong_iot.md): Quy trình thiết kế và xây dựng hệ thống IoT hoàn chỉnh.
3. **Bước 3 — Xem slide sơ đồ/hình vẽ (khi gặp `[Slide hình ảnh/sơ đồ]`):** Xuất đúng slide `[Slide XX]` thành PNG và đọc bằng `read_file`:
   ```bash
   pdftoppm -f XX -l XX -png -r 150 /home/vuloi/prj/robot/docs/it4735_iot_va_ung_dung_v2025_16.1m.pdf /tmp/iot_slide
   ```

## Quy Tắc Chống Lệch Tech Stack (Bắt Buộc)

- Bộ slide minh họa code bằng **Java / ThingSpeak** phục vụ giảng dạy đại cương. **Tuyệt đối không** đưa Java hay ThingSpeak vào codebase dự án.
- Chỉ trích xuất **lý thuyết kiến trúc IoT, đặc tính giao thức MQTT/HTTP, mô hình đe dọa/bảo mật và quy trình thiết kế**, sau đó ánh xạ vào đúng stack đã chốt của dự án:
  - Broker: **Eclipse Mosquitto** (`infra/`)
  - IoT Gateway & Dispatcher: **Rust (`Axum + rumqttc + sqlx`)** (`server/`)
  - Thiết bị IoT & Supervisor: **ESP32 / ESP32-S3 (C++ / PlatformIO)** (`firmware_robot_esp32/`, `firmware_iot/`)
  - On-board Bridge: **Python `rclpy` + `paho-mqtt`** (`ros2_ws/src/restaurant_mqtt_bridge/`)
