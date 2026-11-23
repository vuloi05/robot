# AGENTS.md — Quy Tắc Dự Án Robot Tự Hành Phục Vụ Nhà Hàng

Đây là Workspace Rule luôn được nạp ở thư mục gốc của dự án `/home/vuloi/prj/robot`. Mọi agent khi khảo sát, thiết kế, viết hoặc sửa code **bắt buộc** tuân thủ các quy chuẩn dưới đây.

---

## 1. Tổng Quan & Kiến Trúc Đã Chốt (Bản 2 + Cách B)

- **Mục tiêu:** Hệ thống robot phục vụ nhà hàng khép kín **Bếp ↔ Bàn ăn ↔ Lễ tân / Nhân viên ↔ Robot**, phát triển theo chiến lược **Simulation-First (Digital Twin trên Gazebo Harmonic → Chuyển giao lên Robot thật)** trên nền **Ubuntu 24.04 + ROS 2 Jazzy**.
- **6 Tầng kiến trúc:**
  1. **Tầng 1 (Digital Twin / Hardware):** Gazebo Harmonic (`ros_gz`) → Robot 2 tầng Differential Drive (LiDAR 2D, IMU, Camera dock, 2 khay, màn hình 7 inch, loa, trạm sạc AprilTag).
  2. **Tầng 2 (Embedded & IoT — Cách B):**
     - **STM32 tầng đáy (`firmware_robot_stm32/`):** Motion, Power & Safety thời gian thực (Encoder Hardware Timer, PID 50–100 Hz, IMU, INA219, E-Stop cứng, Watchdog 500 ms) ↔ UART/USB Serial (CRC16) ↔ `ros2_control`.
     - **ESP32 tầng trên (`firmware_robot_esp32/`):** Cảm biến khay (IR/HX711), LED WS2812B, ToF VL53L0X, nút phụ + kênh MQTT supervisor (`robot/{id}/supervisor`) dự phòng khi Pi 5 treo/tắt.
     - **ESP32 IoT rời (`firmware_iot/`):** Nút gọi bàn (`table/{id}/call` & `table/{id}/led`) và trạm sạc thông minh (`dock/{id}/status`).
  3. **Tầng 3 (Navigation — On-board SBC):** ROS 2 Jazzy + `robot_localization` (EKF) + `slam_toolbox` + `AMCL` + Nav2 (`velocity_smoother`, Keepout/Speed Zones) + `opennav_docking` + `apriltag_ros`.
  4. **Tầng 4 (On-board Mission & HRI):** Python `rclpy` (`restaurant_robot_mission` FSM, Audio TTS tiếng Việt offline, `restaurant_mqtt_bridge`).
  5. **Tầng 5 (IoT Gateway & Fleet Server):** Mosquitto MQTT Broker (`infra/`) + Rust (`Axum + Tokio + rumqttc + sqlx` SQLite/Postgres tại `server/`).
  6. **Tầng 6 (UI & Kiosk):** React + Vite + TypeScript + Tailwind CSS (`web_app/`) với 5 giao diện `/kitchen`, `/reception`, `/table/:tableId`, `/admin`, `/robot-face`.

---

## 2. Các Quy Tắc Bất Biến (Invariants)

1. **Nguồn chuẩn duy nhất (Single Source of Truth):**
   - Kiến trúc & FSM: `docs/architecture.md`
   - Giao thức MQTT (Contract v1): `docs/mqtt_protocol.md`
   - Giao thức Serial nhị phân (CRC16-CCITT): `docs/serial_protocol.md`
   - Mọi thay đổi tên topic MQTT, JSON payload, `RobotState`/`TaskType`/`EventType`, hoặc `MSG_ID`/struct Serial **phải cập nhật đồng bộ** giữa `docs/`, `ros2_ws/`, `server/src/models.rs`, `web_app/src/types/protocol.ts` và `firmware_*/include/serial_protocol.h`.
2. **Tách bạch Real-time vs. Mạng Wi-Fi:**
   - **Tuyệt đối không** đưa vòng điều khiển thời gian thực (`Encoder`, `PID`, `IMU`, `LiDAR`, `EKF`, `Nav2`, `cmd_vel`) qua MQTT hoặc HTTP/REST. Mọi giao tiếp điều khiển chuyển động trên robot phải chạy cục bộ có dây hoặc nội bộ SBC.
3. **Giữ đúng phân tách phần cứng Cách B:**
   - Không đưa logic LED WS2812B hoặc cảm biến khay vào STM32 tầng đáy (tránh làm nhiễu ngắt timer/PID).
   - Không bỏ cơ chế an toàn **Watchdog 500 ms** trên STM32 và **E-Stop cứng**.
4. **Local-First, VPS-Ready:**
   - Hệ thống mặc định chạy khép kín trong mạng LAN nội bộ (qua `infra/docker-compose.yml` và Router Wi-Fi riêng khi demo, không phụ thuộc Internet). Khi cấu hình deploy VPS phải giữ tương thích qua biến môi trường và bật ACL/TLS cho Mosquitto.
5. **Giữ đúng Tech Stack:**
   - Không thay thế stack đã chốt bằng công nghệ khác (không dùng Java/ThingSpeak, không viết server bằng framework khác khi chưa có yêu cầu).

---

## 3. Sử Dụng 2 Workspace Skills Tài Liệu Tham Khảo

Workspace đã tích hợp sẵn 2 bộ sách/giáo trình dưới dạng Skill chuẩn Progressive Disclosure trong `.agents/skills/`:

1. **`robot-autonomy-ref`** ([.agents/skills/robot-autonomy-ref/SKILL.md](.agents/skills/robot-autonomy-ref/SKILL.md)) — Giáo trình *Principles of Robot Autonomy* (531 trang):
   - Kích hoạt khi làm việc với động học xe vi sai, PID/LQR/MPC, Nav2 planning, nhiễu cảm biến, hiệu chuẩn camera AprilTag, Bayes/EKF/Particle/AMCL, SLAM, sensor fusion, FSM, hoặc viết cơ sở lý thuyết luận văn.
2. **`iot-hust-ref`** ([.agents/skills/iot-hust-ref/SKILL.md](.agents/skills/iot-hust-ref/SKILL.md)) — Slide *IT4735 IoT và Ứng dụng* (349 slides):
   - Kích hoạt khi làm việc với kiến trúc phân lớp IoT, giao thức MQTT/HTTP/AMQP, bảo mật Mosquitto/TLS/ACL, Web API IoT, thiết kế hệ thống IoT và chuẩn hóa thuật ngữ tiếng Việt.

**Cách tra cứu bắt buộc:** Đọc `references/INDEX.md` của skill trước → chỉ mở 1–2 file chương liên quan trực tiếp → nếu cần công thức/sơ đồ gốc bị vỡ trong text thuần, dùng `pdftoppm` xuất đúng `[PDF p.XX]` hoặc `[Slide XX]` từ `docs/` để xem ảnh. Tuyệt đối **không đọc toàn bộ 23 chương cùng lúc**.

---

## 4. Quy Chuẩn Kiểm Chứng & Thao Tác Hệ Thống

- **Kiểm chứng trước khi báo xong:**
  - Sửa header Serial C/C++: chạy `gcc -std=c11 -Wall -Wextra -Werror -fsyntax-only` và `g++ -std=c++17 -Wall -Wextra -Werror -fsyntax-only` trên cả 2 bản `serial_protocol.h`.
  - Sửa Python ROS 2 / scripts: chạy `python3 -m py_compile` (và `colcon build` / pytest khi ROS 2 đã cài).
  - Sửa Rust (`server/`) / TypeScript (`web_app/`): chạy `cargo check` / `npm run build` khi toolchain đã cài.
  - Sửa cấu trúc PDF skills: chạy `python3 scripts/extract_pdf_refs.py` nếu cần tái tạo `references/`.
- **An toàn môi trường:** Không tự chạy `sudo apt` cài phần mềm hệ thống ngoài phạm vi dự án khi người dùng chưa yêu cầu; không tự ý `git commit` nếu không được yêu cầu.
