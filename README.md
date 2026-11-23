# Robot Tự Hành Phục Vụ Nhà Hàng (ROS 2 Jazzy + MQTT + Rust + React + STM32/ESP32)

Đồ án tốt nghiệp hệ thống **Robot tự hành phục vụ nhà hàng** phát triển theo phương pháp **Simulation-First (Digital Twin trên Gazebo Harmonic → Chuyển giao lên Robot thực tế cỡ nhỏ/vừa)**, khép kín luồng nghiệp vụ:

**Bếp ↔ Bàn ăn của khách ↔ Lễ tân / Nhân viên phục vụ ↔ Robot**

---

## Kiến trúc 6 Tầng (Bản 2 + Cách B)

1. **Tầng 1 — Digital Twin / Phần cứng Vật lý:** Gazebo Harmonic (`ros_gz`) → Khung 2 tầng nhôm 2020 + mica/alu + in 3D, Differential Drive, LiDAR 2D 360°, IMU, Camera, 2 khay, màn hình cảm ứng 7 inch, loa, trạm sạc AprilTag & nút gọi bàn.
2. **Tầng 2 — Điều khiển Cấp thấp & IoT (Cách B):**
   - **STM32 (Tầng đáy robot):** Motion, Power & Safety (Encoder Hardware Timer, PID 50–100 Hz, IMU, INA219, E-Stop cứng, Watchdog 500 ms) ↔ UART/USB Serial (CRC16) ↔ `ros2_control`.
   - **ESP32 (Tầng trên robot):** Cảm biến khay (IR/HX711), dải LED WS2812B, ToF chống quệt mặt bàn, nút chạm + kênh MQTT supervisor dự phòng khi Pi 5 treo/tắt.
   - **ESP32 IoT nhà hàng:** Nút gọi bàn vật lý (`table/{id}/call` & `table/{id}/led`) và trạm sạc thông minh (`dock/{id}/status`).
3. **Tầng 3 — Điều hướng Tự hành (On-board SBC):** ROS 2 Jazzy + `robot_localization` (EKF) + `slam_toolbox` + `AMCL` + Nav2 (Smac/NavFn, MPPI/RPP, Velocity Smoother, Keepout/Speed Zones) + `opennav_docking` + `apriltag_ros`.
4. **Tầng 4 — Quản lý Nhiệm vụ & HRI (On-board SBC):** Python (`rclpy`) — `mission_manager` FSM, tối ưu đa bàn, Audio TTS tiếng Việt offline, `restaurant_mqtt_bridge` (QoS 1, LWT).
5. **Tầng 5 — IoT Gateway & Điều phối Trung tâm:** Mosquitto MQTT Broker + Rust (`Axum + Tokio + rumqttc + sqlx` SQLite/Postgres), đóng gói Docker chạy được cả **mạng LAN cục bộ (khi demo/không có Internet)** lẫn **VPS**.
6. **Tầng 6 — Giao diện Người dùng & Kiosk:** React + Vite + TypeScript + Tailwind CSS với 5 giao diện:
   - `/kitchen` — Giao diện Bếp (gán khay & bàn, bấm giao món)
   - `/reception` — Giao diện Lễ tân (gọi robot đón & dẫn khách)
   - `/table/:tableId` — Giao diện Nhân viên / QR tại bàn (gọi thu dọn / hỗ trợ)
   - `/admin` — Admin Dashboard (bản đồ 2D realtime, vị trí robot, pin, hàng đợi, E-Stop)
   - `/robot-face` — Màn hình Kiosk 7 inch trên thân robot (biểu cảm động & xác nhận lấy món)

---

## Cấu Trúc Thư Mục Monorepo

```text
/home/vuloi/prj/robot/
├── AGENTS.md                   # Workspace Rule cho AI (kiến trúc, Contract v1, cách dùng skills)
├── .agents/skills/             # 2 Knowledge Skills (robot-autonomy-ref, iot-hust-ref) tách từ PDF
├── docs/                       # Tài liệu kiến trúc, giao thức MQTT/Serial, hướng dẫn cài đặt & PDF gốc
├── infra/                      # Docker Compose + cấu hình Mosquitto MQTT Broker + ACL/.env mẫu
├── scripts/                    # Script kiểm tra môi trường, cài đặt và tách tài liệu PDF (extract_pdf_refs.py)
├── ros2_ws/src/                # 7 packages ROS 2 Jazzy (msgs, description, sim, bringup, nav, mission, mqtt_bridge)
├── server/                     # Backend IoT Gateway & Fleet Dispatcher bằng Rust (Axum + rumqttc + sqlx)
├── web_app/                    # Frontend React + Vite + TypeScript + Tailwind CSS
├── firmware_robot_stm32/       # Firmware STM32 tầng đáy (Motion, Power, Safety)
├── firmware_robot_esp32/       # Firmware ESP32 tầng trên (Tray, LED, ToF, MQTT Supervisor)
├── firmware_iot/               # Firmware ESP32 nút gọi bàn & trạm sạc thông minh
└── hardware/                   # Tài liệu cơ khí, nguyên tắc thiết kế và bảng BOM linh kiện
```

---

## Tài Liệu Đặc Tả Cốt Lõi

- [Quy tắc dự án (AGENTS.md)](AGENTS.md)
- [Kiến trúc hệ thống & Lộ trình 24 tuần](docs/architecture.md)
- [Đặc tả giao thức MQTT](docs/mqtt_protocol.md)
- [Đặc tả giao thức Serial nhị phân (Pi 5 ↔ STM32 / ESP32)](docs/serial_protocol.md)
- [Hướng dẫn cài đặt môi trường Ubuntu 24.04](docs/setup_guide.md)
- [Danh mục vật tư linh kiện (BOM)](hardware/bom.csv)
- Tham chiếu học thuật (Skills): [robot-autonomy-ref](.agents/skills/robot-autonomy-ref/SKILL.md) | [iot-hust-ref](.agents/skills/iot-hust-ref/SKILL.md)

---

## Kiểm Tra & Cài Đặt Môi Trường Nhanh (Ubuntu 24.04)

1. **Kiểm tra công cụ hiện có trên máy:**
   ```bash
   ./scripts/check_env.sh
   ```

2. **Xem các tùy chọn và cài đặt ROS 2 Jazzy, Gazebo Harmonic, Docker, Rust, Node.js:**
   ```bash
   ./scripts/setup_dev_env.sh --help
   ./scripts/setup_dev_env.sh --all
   ```

3. **Khởi chạy thử các tầng (sau khi cài đủ môi trường):**
   ```bash
   # Tầng 5a: Khởi chạy MQTT Broker (Mosquitto)
   docker compose -f infra/docker-compose.yml up -d mosquitto

   # Tầng 5b: Chạy Rust Backend Server (port 8080)
   cd server && cargo run

   # Tầng 6: Chạy Frontend React (port 5173)
   cd web_app && npm install && npm run dev

   # Tầng 3-4: Build ROS 2 Workspace
   cd ros2_ws && source /opt/ros/jazzy/setup.bash && colcon build --symlink-install
   ```
