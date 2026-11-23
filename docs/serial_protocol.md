# Đặc Tả Giao Thức Serial Nhị Phân (SBC ↔ STM32 & ESP32 Tầng Trên)

Tài liệu quy định giao thức có dây tốc độ cao trên thân robot (**Tầng 2 ↔ Tầng 3/4**), dùng chung một cấu trúc đóng gói (`serial_protocol.h`) cho cả:
- **Board Tầng Đáy (STM32):** `/dev/robot_stm32` — `230400 bps` (hoặc `115200 bps`), 8N1.
- **Board Tầng Trên (ESP32):** `/dev/robot_esp32` — `115200 bps`, 8N1.

> [!NOTE]
> Quy tắc udev cố định tên thiết bị (`/dev/robot_stm32`, `/dev/robot_esp32`, `/dev/robot_lidar`) được đặt mẫu tại [99-restaurant-robot.rules](../ros2_ws/src/restaurant_robot_bringup/udev/99-restaurant-robot.rules) để tránh nhảy cổng `/dev/ttyUSB0`/`/dev/ttyACM0` khi khởi động lại Pi 5.

---

## 1. Cấu Trúc Khung Gói Tin (Frame Format — Little Endian)

Mọi trường nhiều byte sử dụng **Little-Endian** (tương thích native với ARM Cortex-M STM32, Xtensa/RISC-V ESP32 và ARM64/x86_64 Linux).

| Trường | Kích thước | Giá trị / Ý nghĩa |
| :--- | :---: | :--- |
| `SOF0` | 1 byte | `0xAA` (Start of Frame byte 0) |
| `SOF1` | 1 byte | `0x55` (Start of Frame byte 1) |
| `VER` | 1 byte | `0x01` (Phiên bản giao thức) |
| `MSG_ID` | 1 byte | Mã loại bản tin |
| `SEQ` | 1 byte | Số thứ tự tăng dần `0..255` (dùng phát hiện rớt gói) |
| `LEN` | 1 byte | Độ dài `PAYLOAD` tính bằng byte (`0..128`) |
| `PAYLOAD` | `LEN` bytes | Dữ liệu nhị phân packed (`__attribute__((packed))`) |
| `CRC16` | 2 bytes | **CRC16-CCITT** (u16 LE) tính trên vùng `[VER, MSG_ID, SEQ, LEN, PAYLOAD...]` |

### Tham số CRC16-CCITT
- **Polynomial:** `0x1021`
- **Initial Value:** `0xFFFF`
- **XorOut:** `0x0000`
- **Phạm vi tính:** từ byte `VER` (index 2) đến hết byte cuối của `PAYLOAD` (tổng cộng `4 + LEN` byte). Không tính `SOF0`, `SOF1`.

```c
static inline uint16_t crc16_ccitt(const uint8_t *data, size_t len) {
    uint16_t crc = 0xFFFFu;
    for (size_t i = 0; i < len; ++i) {
        crc ^= (uint16_t)data[i] << 8;
        for (uint8_t b = 0; b < 8; ++b) {
            if (crc & 0x8000u) {
                crc = (uint16_t)((crc << 1) ^ 0x1021u);
            } else {
                crc = (uint16_t)(crc << 1);
            }
        }
    }
    return crc;
}
```

---

## 2. Bản Tin Giao Tiếp Pi 5 ↔ STM32 (Tầng Đáy — Motion & Safety)

### `0x01` — `CMD_WHEEL_VEL` (Pi 5 → STM32, 50–100 Hz, 10 bytes)
| Offset | Kiểu | Tên trường | Ý nghĩa |
| :---: | :--- | :--- | :--- |
| 0 | `float32` | `left_rad_s` | Vận tốc góc đặt bánh trái (rad/s) |
| 4 | `float32` | `right_rad_s` | Vận tốc góc đặt bánh phải (rad/s) |
| 8 | `uint8` | `estop_req` | `1` = yêu cầu phanh khẩn cấp bằng phần mềm, `0` = chạy bình thường |
| 9 | `uint8` | `reserved` | Dự phòng (`0`) |

### `0x02` — `CMD_PID_CONFIG` (Pi 5 → STM32, khi tinh chỉnh, 16 bytes)
| Offset | Kiểu | Tên trường | Ý nghĩa |
| :---: | :--- | :--- | :--- |
| 0 | `float32` | `kp` | Hệ số P vòng lặp PID vận tốc |
| 4 | `float32` | `ki` | Hệ số I vòng lặp PID vận tốc |
| 8 | `float32` | `kd` | Hệ số D vòng lặp PID vận tốc |
| 12 | `uint16` | `max_pwm` | Giới hạn PWM tối đa cho driver động cơ |
| 14 | `uint16` | `reserved` | Dự phòng (`0`) |

### `0x03` — `CMD_BASE_HEARTBEAT` (Pi 5 → STM32, 10 Hz, 8 bytes)
| Offset | Kiểu | Tên trường | Ý nghĩa |
| :---: | :--- | :--- | :--- |
| 0 | `uint32` | `pi_uptime_ms` | Thời gian hoạt động của node trên Pi 5 |
| 4 | `uint8` | `flags` | Bit 0: `clear_fault` (xóa cờ lỗi sau khi xử lý) |
| 5 | `uint8[3]` | `reserved` | Dự phòng (`0`) |

### `0x11` — `TEL_BASE_STATE` (STM32 → Pi 5, 50–100 Hz, 52 bytes)
| Offset | Kiểu | Tên trường | Ý nghĩa |
| :---: | :--- | :--- | :--- |
| 0 | `uint32` | `mcu_time_ms` | Timestamp nội bộ STM32 (ms) |
| 4 | `int32` | `enc_left_ticks` | Tổng xung Encoder bánh trái tích lũy |
| 8 | `int32` | `enc_right_ticks` | Tổng xung Encoder bánh phải tích lũy |
| 12 | `float32` | `vel_left_rad_s` | Vận tốc đo được bánh trái (rad/s) |
| 16 | `float32` | `vel_right_rad_s` | Vận tốc đo được bánh phải (rad/s) |
| 20 | `float32` | `imu_ax` | Gia tốc trục X (m/s²) |
| 24 | `float32` | `imu_ay` | Gia tốc trục Y (m/s²) |
| 28 | `float32` | `imu_az` | Gia tốc trục Z (m/s²) |
| 32 | `float32` | `imu_gx` | Vận tốc góc trục X (rad/s) |
| 36 | `float32` | `imu_gy` | Vận tốc góc trục Y (rad/s) |
| 40 | `float32` | `imu_gz` | Vận tốc góc trục Z (rad/s) |
| 44 | `uint16` | `batt_mv` | Điện áp pin đo từ INA219 (mV) |
| 46 | `int16` | `batt_ma` | Dòng điện pin (mA, dương = đang sạc, âm = đang xả) |
| 48 | `uint16` | `fault_flags` | Bitmask lỗi (xem bảng dưới) |
| 50 | `uint16` | `reserved` | Dự phòng (`0`) |

**Bitmask `fault_flags` của STM32:**
- `Bit 0 (0x0001)`: `FAULT_ESTOP_HW` — Nút E-Stop cứng đang nhấn.
- `Bit 1 (0x0002)`: `FAULT_WATCHDOG` — Mất lệnh hợp lệ từ Pi 5 quá `500 ms`.
- `Bit 2 (0x0004)`: `FAULT_OVERCURRENT` — Quá dòng động cơ / pin.
- `Bit 3 (0x0008)`: `FAULT_UNDERVOLTAGE` — Điện áp pin dưới ngưỡng an toàn.
- `Bit 4 (0x0010)`: `FAULT_IMU_ERR` — Mất kết nối I2C IMU.

---

## 3. Bản Tin Giao Tiếp Pi 5 ↔ ESP32 Tầng Trên (Tray, LED, ToF, Supervisor)

### `0x21` — `CMD_TRAY_LED` (Pi 5 → ESP32, theo sự kiện / 5 Hz, 12 bytes)
| Offset | Kiểu | Tên trường | Ý nghĩa |
| :---: | :--- | :--- | :--- |
| 0 | `uint8` | `tray1_led_mode` | `0=OFF, 1=SOLID, 2=BLINK, 3=BREATHE` |
| 1 | `uint8` | `tray2_led_mode` | `0=OFF, 1=SOLID, 2=BLINK, 3=BREATHE` |
| 2 | `uint8[3]` | `tray1_rgb` | Màu `[R, G, B]` khay 1 |
| 5 | `uint8[3]` | `tray2_rgb` | Màu `[R, G, B]` khay 2 |
| 8 | `uint8` | `status_led_mode` | Đèn viền trạng thái robot (`0=IDLE, 1=BUSY, 2=BLOCKED, 3=CHARGING, 4=ERROR`) |
| 9 | `uint8[3]` | `reserved` | Dự phòng (`0`) |

### `0x22` — `CMD_PI_HEARTBEAT` (Pi 5 → ESP32, 2 Hz, 8 bytes)
| Offset | Kiểu | Tên trường | Ý nghĩa |
| :---: | :--- | :--- | :--- |
| 0 | `uint32` | `pi_uptime_ms` | Timestamp hoạt động Pi 5 |
| 4 | `uint8` | `fsm_state_code` | Mã trạng thái FSM hiện tại |
| 5 | `uint8` | `estop_req` | `1` nếu đang E-Stop |
| 6 | `uint8[2]` | `reserved` | Dự phòng (`0`) |

### `0x31` — `TEL_UPPER_STATE` (ESP32 → Pi 5, 10–20 Hz, 18 bytes)
| Offset | Kiểu | Tên trường | Ý nghĩa |
| :---: | :--- | :--- | :--- |
| 0 | `uint32` | `mcu_time_ms` | Timestamp nội bộ ESP32 (ms) |
| 4 | `uint8` | `tray1_occupied` | `1` = có vật/đồ ăn trên khay 1, `0` = trống |
| 5 | `uint8` | `tray2_occupied` | `1` = có vật/đồ ăn trên khay 2, `0` = trống |
| 6 | `int16` | `tray1_weight_g` | Khối lượng đo trên khay 1 (gram, `0` nếu dùng IR) |
| 8 | `int16` | `tray2_weight_g` | Khối lượng đo trên khay 2 (gram) |
| 10 | `uint16` | `tof_front_mm` | Khoảng cách cảm biến ToF trước (mm, `65535` = ngoài tầm) |
| 12 | `uint16` | `tof_left_mm` | Khoảng cách cảm biến ToF trái (mm) |
| 14 | `uint16` | `tof_right_mm` | Khoảng cách cảm biến ToF phải (mm) |
| 16 | `uint8` | `button_flags` | Bit 0: nút xác nhận khay 1, Bit 1: nút khay 2, Bit 2: nút dừng tạm |
| 17 | `uint8` | `fault_flags` | Bitmask lỗi cảm biến tầng trên |

---

## 4. Cơ Chế An Toàn (Fail-Safe)

1. **Watchdog 500 ms trên STM32:** Nếu quá `500 ms` không nhận được frame hợp lệ `CMD_WHEEL_VEL` (`0x01`) hoặc `CMD_BASE_HEARTBEAT` (`0x03`) có đúng CRC16, STM32 lập tức đặt `target_vel = 0`, ngắt PWM driver động cơ và bật bit `FAULT_WATCHDOG`.
2. **Ngắt E-Stop cứng:** Nút E-Stop cắt trực tiếp nguồn động cơ (qua relay/MOSFET công suất) đồng thời kéo chân EXTI của STM32 để báo `FAULT_ESTOP_HW` lên ROS 2 và MQTT.
3. **Pi-Alive Timeout 5 s trên ESP32 tầng trên:** Nếu quá `5000 ms` không nhận được `CMD_PI_HEARTBEAT` (`0x22`), ESP32 chuyển cờ `pi_alive = false` trên topic MQTT `robot/{id}/supervisor` để cảnh báo Server ngay cả khi Pi 5 bị treo.
